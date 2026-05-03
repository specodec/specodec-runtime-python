import { JsonWriter } from "./json_writer.js";
import { JsonReader } from "./json_reader.js";
import { MsgPackWriter } from "./msgpack_writer.js";
import { MsgPackReader } from "./msgpack_reader.js";
import { GronWriter } from "./gron_writer.js";
import { GronReader } from "./gron_reader.js";
// ---------------------------------------------------------------------------
// FormatRegistry: maps format name substrings to format entries
// ---------------------------------------------------------------------------
export class FormatRegistry {
    entries = [];
    register(entry) {
        this.entries.push(entry);
        return this;
    }
    match(format) {
        for (const e of this.entries) {
            if (format === e.name)
                return e;
        }
        return this.entries[0]; // default: first registered (JSON)
    }
}
// ---------------------------------------------------------------------------
// Default registry: json + msgpack + gron
// ---------------------------------------------------------------------------
export const defaultRegistry = new FormatRegistry()
    .register({
    name: "json",
    newWriter: () => new JsonWriter(),
    newReader: (body) => new JsonReader(body),
})
    .register({
    name: "msgpack",
    newWriter: () => new MsgPackWriter(),
    newReader: (body) => new MsgPackReader(body),
})
    .register({
    name: "gron",
    newWriter: () => new GronWriter(),
    newReader: (body) => new GronReader(body),
});
// ---------------------------------------------------------------------------
// dispatch / respond — use registry
// ---------------------------------------------------------------------------
export function dispatch(codec, body, format, registry = defaultRegistry) {
    const fmt = registry.match(format);
    return codec.decode(fmt.newReader(body));
}
export function respond(codec, obj, format, registry = defaultRegistry) {
    const fmt = registry.match(format);
    const w = fmt.newWriter();
    codec.encode(w, obj);
    return { body: w.toBytes(), name: fmt.name };
}
