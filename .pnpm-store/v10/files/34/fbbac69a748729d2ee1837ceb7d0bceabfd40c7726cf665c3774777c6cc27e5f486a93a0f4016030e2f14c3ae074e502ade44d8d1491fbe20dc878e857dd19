export declare class GronReader {
    private lines;
    private cursor;
    private ctx;
    constructor(data: Uint8Array);
    private unescape;
    readString(): string;
    readBool(): boolean;
    readInt32(): number;
    readInt64(): bigint;
    readUint32(): number;
    readUint64(): bigint;
    readFloat32(): number;
    readFloat64(): number;
    readNull(): null;
    readBytes(): Uint8Array;
    readEnum(): string;
    beginObject(): void;
    hasNextField(): boolean;
    readFieldName(): string;
    endObject(): void;
    beginArray(): void;
    hasNextElement(): boolean;
    nextElement(): void;
    endArray(): void;
    isNull(): boolean;
    skip(): void;
}
