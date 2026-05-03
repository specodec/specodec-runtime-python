export declare class GronWriter {
    private lines;
    private segments;
    private nestingStack;
    private buildPath;
    private escape;
    private b64;
    private emit;
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
    beginObject(_fieldCount: number): void;
    writeField(name: string): void;
    endObject(): void;
    beginArray(_elementCount: number): void;
    nextElement(): void;
    endArray(): void;
    writeEnum(value: string): void;
    toBytes(): Uint8Array;
}
