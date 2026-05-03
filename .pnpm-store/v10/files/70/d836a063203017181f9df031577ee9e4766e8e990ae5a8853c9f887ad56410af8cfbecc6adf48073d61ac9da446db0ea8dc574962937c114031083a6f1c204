import type { SpecReader } from "./spec_reader.js";
import type { SpecWriter } from "./spec_writer.js";
export interface SpecCodec<T> {
    encode(w: SpecWriter, obj: T): void;
    decode(r: SpecReader): T;
}
export interface FormatEntry {
    name: string;
    newWriter(): SpecWriter;
    newReader(body: Uint8Array): SpecReader;
}
export declare class FormatRegistry {
    private readonly entries;
    register(entry: FormatEntry): this;
    match(format: string): FormatEntry;
}
export declare const defaultRegistry: FormatRegistry;
export declare function dispatch<T>(codec: SpecCodec<T>, body: Uint8Array, format: string, registry?: FormatRegistry): T;
export interface RespondResult {
    body: Uint8Array;
    name: string;
}
export declare function respond<T>(codec: SpecCodec<T>, obj: T, format: string, registry?: FormatRegistry): RespondResult;
