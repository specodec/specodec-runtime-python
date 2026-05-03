export declare class JsonWriter {
    private parts;
    private firstItem;
    private escape;
    private b64;
    writeString(value: string): void;
    writeBool(value: boolean): void;
    writeInt32(value: number): void;
    writeInt64(value: bigint): void;
    writeUint32(value: number): void;
    writeUint64(value: bigint): void;
    writeFloat32(value: number): void;
    writeFloat64(value: number): void;
    writeNull(): void;
    writeBytes(value: Uint8Array): void;
    writeEnum(value: string): void;
    beginObject(_fieldCount?: number): void;
    writeField(name: string): void;
    endObject(): void;
    beginArray(_size?: number): void;
    nextElement(): void;
    endArray(): void;
    toBytes(): Uint8Array;
}
