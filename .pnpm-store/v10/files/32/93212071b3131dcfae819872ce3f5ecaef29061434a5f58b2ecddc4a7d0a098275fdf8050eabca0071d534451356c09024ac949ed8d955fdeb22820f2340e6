export class MsgPackWriter {
  private buf: number[] = [];

  private writeByte(b: number): void { this.buf.push(b & 0xFF); }
  private writeU16(v: number): void { this.buf.push((v >> 8) & 0xFF, v & 0xFF); }
  private writeU32(v: number): void { this.buf.push((v >> 24) & 0xFF, (v >> 16) & 0xFF, (v >> 8) & 0xFF, v & 0xFF); }
  private writeU64(v: bigint): void {
    this.writeU32(Number(v >> BigInt(32)));
    this.writeU32(Number(v & BigInt(0xFFFFFFFF)));
  }

  writeString(value: string): void {
    const bytes = new TextEncoder().encode(value);
    const len = bytes.length;
    if (len <= 0x1F) this.writeByte(0xA0 | len);
    else if (len <= 0xFF) { this.writeByte(0xD9); this.writeByte(len); }
    else if (len <= 0xFFFF) { this.writeByte(0xDA); this.writeU16(len); }
    else { this.writeByte(0xDB); this.writeU32(len); }
    for (const b of bytes) this.buf.push(b);
  }

  writeBool(value: boolean): void { this.writeByte(value ? 0xC3 : 0xC2); }

  writeInt32(value: number): void {
    if (value >= 0 && value <= 0x7F) { this.writeByte(value); }
    else if (value < 0 && value >= -0x20) { this.writeByte(value & 0xFF); }
    else if (value >= 0 && value <= 0xFF) { this.writeByte(0xCC); this.writeByte(value); }
    else if (value >= 0 && value <= 0xFFFF) { this.writeByte(0xCD); this.writeU16(value); }
    else if (value >= 0) { this.writeByte(0xCE); this.writeU32(value); }
    else if (value >= -0x80) { this.writeByte(0xD0); this.writeByte(value & 0xFF); }
    else if (value >= -0x8000) { this.writeByte(0xD1); this.writeU16(value & 0xFFFF); }
    else { this.writeByte(0xD2); this.writeU32(value >>> 0); }
  }

  writeInt64(value: bigint): void {
    if (value >= BigInt(0) && value <= BigInt(0x7F)) this.writeByte(Number(value));
    else if (value < BigInt(0) && value >= BigInt(-0x20)) this.writeByte(Number(value) & 0xFF);
    else if (value >= BigInt(0) && value <= BigInt(0xFF)) { this.writeByte(0xCC); this.writeByte(Number(value)); }
    else if (value >= BigInt(0) && value <= BigInt(0xFFFF)) { this.writeByte(0xCD); this.writeU16(Number(value)); }
    else if (value >= BigInt(0) && value <= BigInt(0xFFFFFFFF)) { this.writeByte(0xCE); this.writeU32(Number(value)); }
    else if (value >= BigInt(0)) { this.writeByte(0xCF); this.writeU64(value); }
    else if (value >= BigInt(-0x80)) { this.writeByte(0xD0); this.writeByte(Number(value) & 0xFF); }
    else if (value >= BigInt(-0x8000)) { this.writeByte(0xD1); this.writeU16(Number(value) & 0xFFFF); }
    else if (value >= BigInt(-0x80000000)) { this.writeByte(0xD2); this.writeU32(Number(value) >>> 0); }
    else { this.writeByte(0xD3); this.writeU64(value); }
  }

  writeUint32(value: number): void {
    if (value <= 0x7F) this.writeByte(value);
    else if (value <= 0xFF) { this.writeByte(0xCC); this.writeByte(value); }
    else if (value <= 0xFFFF) { this.writeByte(0xCD); this.writeU16(value); }
    else { this.writeByte(0xCE); this.writeU32(value); }
  }

  writeUint64(value: bigint): void {
    if (value <= BigInt(0x7F)) this.writeByte(Number(value));
    else if (value <= BigInt(0xFF)) { this.writeByte(0xCC); this.writeByte(Number(value)); }
    else if (value <= BigInt(0xFFFF)) { this.writeByte(0xCD); this.writeU16(Number(value)); }
    else if (value <= BigInt(0xFFFFFFFF)) { this.writeByte(0xCE); this.writeU32(Number(value)); }
    else { this.writeByte(0xCF); this.writeU64(value); }
  }

  writeFloat32(value: number): void {
    this.writeByte(0xCA);
    const buf = new ArrayBuffer(4);
    new DataView(buf).setFloat32(0, value, false);
    for (const b of new Uint8Array(buf)) this.buf.push(b);
  }

  writeFloat64(value: number): void {
    this.writeByte(0xCB);
    const buf = new ArrayBuffer(8);
    new DataView(buf).setFloat64(0, value, false);
    for (const b of new Uint8Array(buf)) this.buf.push(b);
  }

  writeNull(): void { this.writeByte(0xC0); }

  writeBytes(value: Uint8Array): void {
    const len = value.length;
    if (len <= 0xFF) { this.writeByte(0xC4); this.writeByte(len); }
    else if (len <= 0xFFFF) { this.writeByte(0xC5); this.writeU16(len); }
    else { this.writeByte(0xC6); this.writeU32(len); }
    for (const b of value) this.buf.push(b);
  }

  beginObject(fieldCount: number): void {
    if (fieldCount <= 0x0F) this.writeByte(0x80 | fieldCount);
    else if (fieldCount <= 0xFFFF) { this.writeByte(0xDE); this.writeU16(fieldCount); }
    else { this.writeByte(0xDF); this.writeU32(fieldCount); }
  }

  writeField(name: string): void { this.writeString(name); }

  endObject(): void {}

  beginArray(elementCount: number): void {
    if (elementCount <= 0x0F) this.writeByte(0x90 | elementCount);
    else if (elementCount <= 0xFFFF) { this.writeByte(0xDC); this.writeU16(elementCount); }
    else { this.writeByte(0xDD); this.writeU32(elementCount); }
  }

  nextElement(): void {}

  endArray(): void {}

  writeEnum(value: string): void { this.writeString(value); }

  toBytes(): Uint8Array { return new Uint8Array(this.buf); }
}
