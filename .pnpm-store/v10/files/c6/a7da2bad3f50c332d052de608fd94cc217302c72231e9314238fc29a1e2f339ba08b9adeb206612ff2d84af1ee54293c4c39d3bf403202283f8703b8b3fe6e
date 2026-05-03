export interface SpecReader {
    beginObject(): void;
    hasNextField(): boolean;
    readFieldName(): string;
    endObject(): void;
    beginArray(): void;
    hasNextElement(): boolean;
    endArray(): void;
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
    isNull(): boolean;
    skip(): void;
}
