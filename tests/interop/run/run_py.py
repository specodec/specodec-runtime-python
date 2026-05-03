#!/usr/bin/env python3
import sys, os, json, base64

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../specodec-python/src'))
from specodec import MsgPackWriter, MsgPackReader, JsonWriter, JsonReader, GronWriter, GronReader

VEC = os.path.join(os.path.dirname(__file__), "vectors")
OUT = os.path.join(os.path.dirname(__file__), "output_py")
os.makedirs(os.path.join(OUT, "scalars"), exist_ok=True)

with open(os.path.join(VEC, "manifest.json")) as f:
    manifest = json.load(f)
with open(os.path.join(VEC, "typeschema.json")) as f:
    schema = json.load(f)

results = {"scalars": {}, "objects": {}}

# ═══════════════════════════════════
# 1. Scalar MsgPack round-trips
# ═══════════════════════════════════
print("Python: processing scalars...")

for name, spec in manifest["scalars"].items():
    ref_path = os.path.join(VEC, "scalars", name + ".mp")
    with open(ref_path, "rb") as f:
        ref_buf = f.read()
    w = MsgPackWriter()
    r = MsgPackReader(ref_buf)
    t = spec["type"]

    try:
        if t == "int32": w.write_int32(r.read_int32())
        elif t == "int64": w.write_int64(r.read_int64())
        elif t == "uint32": w.write_uint32(r.read_uint32())
        elif t == "uint64": w.write_uint64(r.read_uint64())
        elif t == "float32": w.write_float32(r.read_float32())
        elif t == "float64": w.write_float64(r.read_float64())
        elif t == "string": w.write_string(r.read_string())
        elif t == "bytes": w.write_bytes(r.read_bytes())
        elif t == "bool": w.write_bool(r.read_bool())
        out_path = os.path.join(OUT, "scalars", name + ".mp")
        with open(out_path, "wb") as f:
            f.write(w.to_bytes())
        results["scalars"][name] = {"pass": True}
    except Exception as e:
        results["scalars"][name] = {"pass": False, "error": str(e)}
        print(f"  FAIL {name}: {e}")

# ═══════════════════════════════════
# 2. Generic schema-driven decode/encode
# ═══════════════════════════════════

def read_scalar(r, typ):
    if typ == "string": return r.read_string()
    if typ == "boolean": return r.read_bool()
    if typ in ("int8", "int16", "int32"): return r.read_int32()
    if typ == "int64": return r.read_int64()
    if typ in ("uint8", "uint16", "uint32"): return r.read_uint32()
    if typ == "uint64": return r.read_uint64()
    if typ == "float32": return r.read_float32()
    if typ == "float64": return r.read_float64()
    if typ == "bytes": return r.read_bytes()
    raise Exception(f"unknown scalar: {typ}")

def write_scalar(w, val, typ):
    if typ == "string": w.write_string(val)
    elif typ == "boolean": w.write_bool(val)
    elif typ in ("int8", "int16", "int32"): w.write_int32(val)
    elif typ == "int64": w.write_int64(val)
    elif typ in ("uint8", "uint16", "uint32"): w.write_uint32(val)
    elif typ == "uint64": w.write_uint64(val)
    elif typ == "float32": w.write_float32(val)
    elif typ == "float64": w.write_float64(val)
    elif typ == "bytes": w.write_bytes(val)

def decode_field(r, field):
    if field.get("isArray"):
        arr = []
        r.begin_array()
        while r.has_next_element():
            if hasattr(r, 'next_element'): r.next_element()
            if field.get("isModel"): arr.append(decode_model(r, field["type"]))
            else: arr.append(read_scalar(r, field["type"]))
        r.end_array()
        return arr
    if field.get("isModel"): return decode_model(r, field["type"])
    return read_scalar(r, field["type"])

def decode_model(r, model_name):
    s = schema[model_name]
    o = {}
    r.begin_object()
    while r.has_next_field():
        k = r.read_field_name()
        field = next((f for f in s["fields"] if f["name"] == k), None)
        if field: o[k] = decode_field(r, field)
        else: r.skip()
    r.end_object()
    return o

def encode_model_mp(o, model_name):
    w = MsgPackWriter()
    _encode_model_inline_mp(w, o, model_name)
    return w.to_bytes()

def _encode_model_inline_mp(w, o, model_name):
    s = schema[model_name]
    count = sum(1 for f in s["fields"] if not f.get("optional") or f["name"] in o)
    w.begin_object(count)
    for field in s["fields"]:
        if field.get("optional") and field["name"] not in o: continue
        w.write_field(field["name"])
        _encode_field_mp(w, o[field["name"]], field)
    w.end_object()

def _encode_field_mp(w, val, field):
    if field.get("isArray"):
        w.begin_array(len(val))
        for item in val:
            if field.get("isModel"): _encode_model_inline_mp(w, item, field["type"])
            else: write_scalar(w, item, field["type"])
        w.end_array()
        return
    if field.get("isModel"):
        _encode_model_inline_mp(w, val, field["type"])
        return
    write_scalar(w, val, field["type"])

def encode_model_json(o, model_name):
    w = JsonWriter()
    _encode_model_inline_json(w, o, model_name)
    return w.to_bytes()

def _encode_model_inline_json(w, o, model_name):
    s = schema[model_name]
    w.begin_object()
    for field in s["fields"]:
        if field.get("optional") and field["name"] not in o: continue
        w.write_field(field["name"])
        _encode_field_json(w, o[field["name"]], field)
    w.end_object()

def _encode_field_json(w, val, field):
    if field.get("isArray"):
        w.begin_array()
        for item in val:
            w.next_element()
            if field.get("isModel"): _encode_model_inline_json(w, item, field["type"])
            else: write_scalar(w, item, field["type"])
        w.end_array()
        return
    if field.get("isModel"):
        _encode_model_inline_json(w, val, field["type"])
        return
    write_scalar(w, val, field["type"])

def encode_model_gron(o, model_name):
    w = GronWriter()
    _encode_model_inline_gron(w, o, model_name)
    return w.to_bytes()

def _encode_model_inline_gron(w, o, model_name):
    s = schema[model_name]
    count = sum(1 for f in s["fields"] if not f.get("optional") or f["name"] in o)
    w.begin_object(count)
    for field in s["fields"]:
        if field.get("optional") and field["name"] not in o: continue
        w.write_field(field["name"])
        _encode_field_gron(w, o[field["name"]], field)
    w.end_object()

def _encode_field_gron(w, val, field):
    if field.get("isArray"):
        w.begin_array(len(val))
        for item in val:
            w.next_element()
            if field.get("isModel"): _encode_model_inline_gron(w, item, field["type"])
            else: write_scalar(w, item, field["type"])
        w.end_array()
        return
    if field.get("isModel"):
        _encode_model_inline_gron(w, val, field["type"])
        return
    write_scalar(w, val, field["type"])

# ═══════════════════════════════════
# 3. Object round-trips
# ═══════════════════════════════════
print("Python: processing objects...")

for name in manifest["testModels"]:
    results["objects"][name] = {"mp": None, "json": None, "gron": None}

    try:
        with open(os.path.join(VEC, name + ".msgpack"), "rb") as f:
            ref = f.read()
        decoded = decode_model(MsgPackReader(ref), name)
        encoded = encode_model_mp(decoded, name)
        with open(os.path.join(OUT, name + ".msgpack"), "wb") as f:
            f.write(encoded)
        results["objects"][name]["mp"] = True
    except Exception as e:
        results["objects"][name]["mp"] = False
        print(f"  FAIL {name}.msgpack: {e}")

    try:
        with open(os.path.join(VEC, name + ".json"), "rb") as f:
            ref = f.read()
        decoded = decode_model(JsonReader(ref), name)
        encoded = encode_model_json(decoded, name)
        with open(os.path.join(OUT, name + ".json"), "wb") as f:
            f.write(encoded)
        results["objects"][name]["json"] = True
    except Exception as e:
        results["objects"][name]["json"] = False
        encoded = None
        print(f"  FAIL {name}.json: {e}")

    try:
        with open(os.path.join(VEC, name + ".pretty.json"), "rb") as f:
            ref = f.read()
        decoded = decode_model(JsonReader(ref), name)
        pretty_encoded = encode_model_json(decoded, name)
        if encoded is not None and pretty_encoded == encoded:
            results["objects"][name]["prettyJson"] = True
        else:
            results["objects"][name]["prettyJson"] = False
            print(f"  FAIL {name}.pretty.json: re-encoded bytes differ")
    except Exception as e:
        results["objects"][name]["prettyJson"] = False
        print(f"  FAIL {name}.pretty.json: {e}")

    try:
        with open(os.path.join(VEC, name + ".gron"), "rb") as f:
            ref = f.read()
        decoded = decode_model(GronReader(ref), name)
        gron_encoded = encode_model_gron(decoded, name)
        with open(os.path.join(OUT, name + ".gron"), "wb") as f:
            f.write(gron_encoded)
        results["objects"][name]["gron"] = True
    except Exception as e:
        results["objects"][name]["gron"] = False
        print(f"  FAIL {name}.gron: {e}")

# Write results
with open(os.path.join(OUT, "results.json"), "w") as f:
    json.dump(results, f, indent=2)

fail = sum(1 for v in results["scalars"].values() if not v.get("pass")) + \
       sum(1 for v in results["objects"].values() if not v.get("mp") or not v.get("json") or not v.get("prettyJson") or not v.get("gron"))
pass_count = len(results["scalars"]) + len(results["objects"]) - fail
print(f"Python done: {pass_count} passed, {fail} failed")
if fail > 0: sys.exit(1)
