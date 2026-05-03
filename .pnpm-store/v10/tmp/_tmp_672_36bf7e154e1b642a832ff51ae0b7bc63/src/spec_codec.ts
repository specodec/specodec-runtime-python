import type { SpecReader } from "./spec_reader.js";
import type { SpecWriter } from "./spec_writer.js";
import { JsonWriter } from "./json_writer.js";
import { JsonReader } from "./json_reader.js";
import { MsgPackWriter } from "./msgpack_writer.js";
import { MsgPackReader } from "./msgpack_reader.js";
import { GronWriter } from "./gron_writer.js";
import { GronReader } from "./gron_reader.js";

export interface SpecCodec<T> {
  encode(w: SpecWriter, obj: T): void;
  decode(r: SpecReader): T;
}

// ---------------------------------------------------------------------------
// FormatEntry: a reader/writer factory pair for one format
// ---------------------------------------------------------------------------
export interface FormatEntry {
  name: string;        // e.g. "json", "msgpack", "gron"
  newWriter(): SpecWriter;
  newReader(body: Uint8Array): SpecReader;
}

// ---------------------------------------------------------------------------
// FormatRegistry: maps format name substrings to format entries
// ---------------------------------------------------------------------------
export class FormatRegistry {
  private readonly entries: FormatEntry[] = [];

  register(entry: FormatEntry): this {
    this.entries.push(entry);
    return this;
  }

  match(format: string): FormatEntry {
    for (const e of this.entries) {
      if (format === e.name) return e;
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
export function dispatch<T>(
  codec: SpecCodec<T>,
  body: Uint8Array,
  format: string,
  registry: FormatRegistry = defaultRegistry,
): T {
  const fmt = registry.match(format);
  return codec.decode(fmt.newReader(body));
}

export interface RespondResult {
  body: Uint8Array;
  name: string;   // format name: "json" | "msgpack" | "gron"
}

export function respond<T>(
  codec: SpecCodec<T>,
  obj: T,
  format: string,
  registry: FormatRegistry = defaultRegistry,
): RespondResult {
  const fmt = registry.match(format);
  const w = fmt.newWriter();
  codec.encode(w, obj);
  return { body: w.toBytes(), name: fmt.name };
}
