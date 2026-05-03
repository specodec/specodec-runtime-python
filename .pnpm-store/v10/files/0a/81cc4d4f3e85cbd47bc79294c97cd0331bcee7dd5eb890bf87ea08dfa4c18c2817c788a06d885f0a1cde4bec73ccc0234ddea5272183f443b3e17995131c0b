import fs from "fs";
import path from "path";
import { fileURLToPath } from "url";
import {
  MsgPackWriter, MsgPackReader,
  JsonWriter, JsonReader,
  GronWriter, GronReader,
} from "@specodec/specodec-ts";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const VEC = process.env.VEC_DIR || path.join(__dirname, "..", "vectors");
const OUT = process.env.OUT_DIR || path.join(__dirname, "..", "output");
fs.mkdirSync(path.join(OUT, "scalars"), { recursive: true });

const manifest = JSON.parse(fs.readFileSync(path.join(VEC, "manifest.json"), "utf-8"));
const schema = JSON.parse(fs.readFileSync(path.join(VEC, "typeschema.json"), "utf-8"));
const results: { scalars: Record<string, { pass: boolean; error?: string }>; objects: Record<string, { mp?: boolean; json?: boolean; gron?: boolean; error?: string }> } = { scalars: {}, objects: {} };

function tryScalar(name: string, fn: () => void) {
  try {
    fn();
    results.scalars[name] = { pass: true };
  } catch (e: any) {
    results.scalars[name] = { pass: false, error: e.message };
    console.error(`  FAIL ${name}: ${e.message}`);
  }
}

function tryObject(name: string, fn: () => { mp: boolean; json: boolean; gron: boolean }) {
  try {
    const r = fn();
    results.objects[name] = { mp: r.mp, json: r.json, gron: r.gron };
  } catch (e: any) {
    results.objects[name] = { mp: false, json: false, gron: false, error: e.message };
    console.error(`  FAIL ${name}: ${e.message}`);
  }
}

// ═══════════════════════════════════════════
// 1. Scalar MsgPack round-trips
// ═══════════════════════════════════════════
console.log("TS: processing scalars...");

for (const [name, spec] of Object.entries(manifest.scalars)) {
  const refBuf = new Uint8Array(fs.readFileSync(path.join(VEC, "scalars", name + ".mp")));
  const w = new MsgPackWriter();

  switch (spec.type) {
    case "int32": tryScalar(name, () => { w.writeInt32(new MsgPackReader(refBuf).readInt32()); }); break;
    case "int64": tryScalar(name, () => { w.writeInt64(new MsgPackReader(refBuf).readInt64()); }); break;
    case "uint32": tryScalar(name, () => { w.writeUint32(new MsgPackReader(refBuf).readUint32()); }); break;
    case "uint64": tryScalar(name, () => { w.writeUint64(new MsgPackReader(refBuf).readUint64()); }); break;
    case "float32": tryScalar(name, () => { w.writeFloat32(new MsgPackReader(refBuf).readFloat32()); }); break;
    case "float64": tryScalar(name, () => { w.writeFloat64(new MsgPackReader(refBuf).readFloat64()); }); break;
    case "string": tryScalar(name, () => { w.writeString(new MsgPackReader(refBuf).readString()); }); break;
    case "bytes": tryScalar(name, () => { w.writeBytes(new MsgPackReader(refBuf).readBytes()); }); break;
    case "bool": tryScalar(name, () => { w.writeBool(new MsgPackReader(refBuf).readBool()); }); break;
  }

  if (results.scalars[name]?.pass) {
    fs.writeFileSync(path.join(OUT, "scalars", name + ".mp"), w.toBytes());
  }
}

// ═══════════════════════════════════════════
// 2. Generic schema-driven decode/encode
// ═══════════════════════════════════════════

function readScalar(r: MsgPackReader, type: string): any {
  switch (type) {
    case "string": return r.readString();
    case "boolean": return r.readBool();
    case "int8": case "int16": case "int32": return r.readInt32();
    case "int64": return r.readInt64();
    case "uint8": case "uint16": case "uint32": return r.readUint32();
    case "uint64": return r.readUint64();
    case "float32": return r.readFloat32();
    case "float64": return r.readFloat64();
    case "bytes": return r.readBytes();
    default: throw new Error(`unknown scalar: ${type}`);
  }
}

function writeScalarMP(w: MsgPackWriter, val: any, type: string) {
  switch (type) {
    case "string": w.writeString(val); break;
    case "boolean": w.writeBool(val); break;
    case "int8": case "int16": case "int32": w.writeInt32(val); break;
    case "int64": w.writeInt64(val); break;
    case "uint8": case "uint16": case "uint32": w.writeUint32(val); break;
    case "uint64": w.writeUint64(val); break;
    case "float32": w.writeFloat32(val); break;
    case "float64": w.writeFloat64(val); break;
    case "bytes": w.writeBytes(val); break;
  }
}

function decodeField(r: MsgPackReader, field: any): any {
  if (field.optional && r.isNull()) {
    r.readNull();
    return null;
  }
  if (field.isArray) {
    const arr: any[] = [];
    r.beginArray();
    while (r.hasNextElement()) {
      if (typeof r.nextElement === "function") r.nextElement();
      if (field.isModel) arr.push(decodeModel(r, field.type));
      else arr.push(readScalar(r, field.type));
    }
    r.endArray();
    return arr;
  }
  if (field.isModel) return decodeModel(r, field.type);
  return readScalar(r, field.type);
}

function decodeModel(r: MsgPackReader, modelName: string): any {
  const modelSchema = schema[modelName];
  if (!modelSchema) throw new Error(`unknown model: ${modelName}`);
  const obj: any = {};
  r.beginObject();
  while (r.hasNextField()) {
    const fName = r.nextField();
    const field = modelSchema.fields.find((f: any) => f.name === fName);
    if (!field) throw new Error(`unknown field ${fName} in ${modelName}`);
    obj[fName] = decodeField(r, field);
  }
  r.endObject();
  return obj;
}

function encodeFieldMP(w: MsgPackWriter, val: any, field: any) {
  if (val === null) {
    if (field.optional) w.writeNull();
    else throw new Error(`null value for required field ${field.name}`);
    return;
  }
  if (field.isArray) {
    w.beginArray(val.length);
    for (const item of val) {
      if (field.isModel) encodeModelMP(w, item, field.type);
      else writeScalarMP(w, item, field.type);
    }
    w.endArray();
    return;
  }
  if (field.isModel) {
    encodeModelMP(w, val, field.type);
    return;
  }
  writeScalarMP(w, val, field.type);
}

function encodeModelMP(w: MsgPackWriter, obj: any, modelName: string) {
  const modelSchema = schema[modelName];
  if (!modelSchema) throw new Error(`unknown model: ${modelName}`);
  w.beginObject(modelSchema.fields.length);
  for (const field of modelSchema.fields) {
    w.nextField(field.name);
    encodeFieldMP(w, obj[field.name], field);
  }
  w.endObject();
}

// JSON path
function writeScalarJSON(w: JsonWriter, val: any, type: string) {
  switch (type) {
    case "string": w.writeString(val); break;
    case "boolean": w.writeBool(val); break;
    case "int8": case "int16": case "int32": w.writeInt32(val); break;
    case "int64": w.writeInt64(val); break;
    case "uint8": case "uint16": case "uint32": w.writeUint32(val); break;
    case "uint64": w.writeUint64(val); break;
    case "float32": w.writeFloat32(val); break;
    case "float64": w.writeFloat64(val); break;
    case "bytes": w.writeBytes(val); break;
  }
}

function encodeFieldJSON(w: JsonWriter, val: any, field: any) {
  if (val === null) {
    if (field.optional) w.writeNull();
    else throw new Error(`null value for required field ${field.name}`);
    return;
  }
  if (field.isArray) {
    w.beginArray(val.length);
    for (const item of val) {
      if (field.isModel) encodeModelJSON(w, item, field.type);
      else writeScalarJSON(w, item, field.type);
    }
    w.endArray();
    return;
  }
  if (field.isModel) {
    encodeModelJSON(w, val, field.type);
    return;
  }
  writeScalarJSON(w, val, field.type);
}

function encodeModelJSON(w: JsonWriter, obj: any, modelName: string) {
  const modelSchema = schema[modelName];
  if (!modelSchema) throw new Error(`unknown model: ${modelName}`);
  w.beginObject(modelSchema.fields.length);
  for (const field of modelSchema.fields) {
    w.nextField(field.name);
    encodeFieldJSON(w, obj[field.name], field);
  }
  w.endObject();
}

// Gron path
function writeScalarGron(w: GronWriter, val: any, type: string) {
  switch (type) {
    case "string": w.writeString(val); break;
    case "boolean": w.writeBool(val); break;
    case "int8": case "int16": case "int32": w.writeInt32(val); break;
    case "int64": w.writeInt64(val); break;
    case "uint8": case "uint16": case "uint32": w.writeUint32(val); break;
    case "uint64": w.writeUint64(val); break;
    case "float32": w.writeFloat32(val); break;
    case "float64": w.writeFloat64(val); break;
    case "bytes": w.writeBytes(val); break;
  }
}

function encodeFieldGron(w: GronWriter, val: any, field: any, path: string) {
  if (val === null) {
    if (field.optional) w.writeNull(path);
    else throw new Error(`null value for required field ${field.name}`);
    return;
  }
  if (field.isArray) {
    w.beginArray(path);
    for (let i = 0; i < val.length; i++) {
      const itemPath = `${path}[${i}]`;
      if (field.isModel) encodeModelGron(w, val[i], field.type, itemPath);
      else { w.nextField(itemPath); writeScalarGron(w, val[i], field.type); }
    }
    w.endArray();
    return;
  }
  const fieldPath = `${path}.${field.name}`;
  if (field.isModel) {
    encodeModelGron(w, val, field.type, fieldPath);
    return;
  }
  w.nextField(fieldPath);
  writeScalarGron(w, val, field.type);
}

function encodeModelGron(w: GronWriter, obj: any, modelName: string, path: string) {
  const modelSchema = schema[modelName];
  if (!modelSchema) throw new Error(`unknown model: ${modelName}`);
  w.beginObject(path);
  for (const field of modelSchema.fields) {
    encodeFieldGron(w, obj[field.name], field, path);
  }
  w.endObject();
}

// ═══════════════════════════════════════════
// 3. Process objects
// ═══════════════════════════════════════════
console.log("TS: processing objects...");

for (const name of manifest.testModels) {
  tryObject(name, () => {
    const mpBuf = new Uint8Array(fs.readFileSync(path.join(VEC, name + ".msgpack")));
    const r = new MsgPackReader(mpBuf);
    const obj = decodeModel(r, name);

    // MsgPack roundtrip
    const wMP = new MsgPackWriter();
    encodeModelMP(wMP, obj, name);
    fs.writeFileSync(path.join(OUT, name + ".msgpack"), wMP.toBytes());

    // JSON roundtrip
    const jsonRaw = fs.readFileSync(path.join(VEC, name + ".json"), "utf-8");
    const jsonReader = new JsonReader(jsonRaw);
    const objFromJson = decodeModel(jsonReader as any, name);
    const wJSON = new JsonWriter();
    encodeModelJSON(wJSON, objFromJson, name);
    fs.writeFileSync(path.join(OUT, name + ".json"), wJSON.toBytes());

    // Gron roundtrip
    const gronRaw = fs.readFileSync(path.join(VEC, name + ".gron"), "utf-8");
    const gronReader = new GronReader(gronRaw);
    const objFromGron = decodeModel(gronReader as any, name);
    const wGron = new GronWriter();
    encodeModelGron(wGron, objFromGron, name, name);
    fs.writeFileSync(path.join(OUT, name + ".gron"), wGron.toBytes());

    return { mp: true, json: true, gron: true };
  });
}

fs.writeFileSync(path.join(OUT, "results.json"), JSON.stringify(results, null, 2));
console.log(`TS done: ${Object.values(results.scalars).filter(r => r.pass).length} scalars, ${Object.keys(results.objects).length} objects`);