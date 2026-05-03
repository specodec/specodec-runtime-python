import { formatFloat32, formatFloat64 } from "./float_fmt.js";

export class JsonWriter {
  private parts: string[] = [];
  private firstItem: boolean[] = [];

  private escape(s: string): string {
    let r = "";
    for (let i = 0; i < s.length; i++) {
      const c = s.charCodeAt(i);
      switch (c) {
        case 0x22: r += '\\"'; break;
        case 0x5C: r += "\\\\"; break;
        case 0x08: r += "\\b"; break;
        case 0x0C: r += "\\f"; break;
        case 0x0A: r += "\\n"; break;
        case 0x0D: r += "\\r"; break;
        case 0x09: r += "\\t"; break;
        default:
          if (c < 0x20) {
            r += "\\u" + c.toString(16).padStart(4, "0");
          } else {
            r += s.charAt(i);
          }
      }
    }
    return r;
  }

  private b64(buf: Uint8Array): string {
    const chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/";
    let s = "";
    for (let i = 0; i < buf.length; i += 3) {
      const b0 = buf[i];
      const b1 = i + 1 < buf.length ? buf[i + 1] : 0;
      const b2 = i + 2 < buf.length ? buf[i + 2] : 0;
      s += chars[b0 >> 2];
      s += chars[((b0 & 3) << 4) | (b1 >> 4)];
      s += i + 1 < buf.length ? chars[((b1 & 15) << 2) | (b2 >> 6)] : "=";
      s += i + 2 < buf.length ? chars[b2 & 63] : "=";
    }
    return s;
  }

  writeString(value: string): void {
    this.parts.push('"' + this.escape(value) + '"');
  }

  writeBool(value: boolean): void {
    this.parts.push(value ? "true" : "false");
  }

  writeInt32(value: number): void {
    this.parts.push(String(value | 0));
  }

  writeInt64(value: bigint): void {
    this.parts.push('"' + String(value) + '"');
  }

  writeUint32(value: number): void {
    this.parts.push(String(value >>> 0));
  }

  writeUint64(value: bigint): void {
    this.parts.push('"' + String(value) + '"');
  }

  writeFloat32(value: number): void {
    const f32 = new Float32Array(1);
    f32[0] = value;
    const v = f32[0];
    if (!isFinite(v)) throw new Error("float32: NaN/Infinity not valid JSON");
    this.parts.push(formatFloat32(value));
  }

  writeFloat64(value: number): void {
    if (!isFinite(value)) throw new Error("float64: NaN/Infinity not valid JSON");
    this.parts.push(formatFloat64(value));
  }

  writeNull(): void {
    this.parts.push("null");
  }

  writeBytes(value: Uint8Array): void {
    this.parts.push('"' + this.b64(value) + '"');
  }

  writeEnum(value: string): void {
    this.parts.push('"' + this.escape(value) + '"');
  }

  beginObject(_fieldCount?: number): void {
    this.parts.push("{");
    this.firstItem.push(true);
  }

  writeField(name: string): void {
    const top = this.firstItem.length - 1;
    if (!this.firstItem[top]) this.parts.push(",");
    this.firstItem[top] = false;
    this.parts.push('"' + this.escape(name) + "\":");
  }

  endObject(): void {
    this.firstItem.pop();
    this.parts.push("}");
  }

  beginArray(_size?: number): void {
    this.parts.push("[");
    this.firstItem.push(true);
  }

  nextElement(): void {
    const top = this.firstItem.length - 1;
    if (!this.firstItem[top]) this.parts.push(",");
    this.firstItem[top] = false;
  }

  endArray(): void {
    this.firstItem.pop();
    this.parts.push("]");
  }

  toBytes(): Uint8Array {
    return new TextEncoder().encode(this.parts.join(""));
  }
}
