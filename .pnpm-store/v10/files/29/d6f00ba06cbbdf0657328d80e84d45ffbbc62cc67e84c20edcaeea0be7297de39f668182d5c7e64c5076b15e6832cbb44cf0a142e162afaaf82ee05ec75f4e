import type { SpecReader } from "./spec_reader.js";

export class JsonReader implements SpecReader {
  private readonly src: string;
  private _pos: number;
  private _firstField: boolean[] = [];
  private _firstElement: boolean[] = [];

  constructor(data: Uint8Array) {
    this.src = new TextDecoder().decode(data);
    this._pos = 0;
  }

  get pos(): number { return this._pos; }

  private ws(): void {
    while (this._pos < this.src.length) {
      const c = this.src.charCodeAt(this._pos);
      if (c === 0x20 || c === 0x09 || c === 0x0A || c === 0x0D) {
        this._pos++;
      } else {
        break;
      }
    }
  }

  private peek(): string {
    this.ws();
    if (this._pos >= this.src.length) throw new Error("json: unexpected end of input");
    return this.src[this._pos];
  }

  private read(): string {
    this.ws();
    if (this._pos >= this.src.length) throw new Error("json: unexpected end of input");
    return this.src[this._pos++];
  }

  private expect(ch: string): void {
    const got = this.read();
    if (got !== ch) throw new Error(`json: expected '${ch}', got '${got}' at position ${this._pos - 1}`);
  }

  private parseString(): string {
    this.expect('"');
    let r = "";
    while (this._pos < this.src.length) {
      const c = this.src.charCodeAt(this._pos);
      if (c === 0x22) {
        this._pos++;
        return r;
      }
      if (c === 0x5C) {
        this._pos++;
        if (this._pos >= this.src.length) throw new Error("json: unexpected end of string escape");
        const esc = this.src.charCodeAt(this._pos);
        switch (esc) {
          case 0x22: r += '"'; this._pos++; break;
          case 0x5C: r += '\\'; this._pos++; break;
          case 0x2F: r += '/'; this._pos++; break;
          case 0x62: r += '\b'; this._pos++; break;
          case 0x66: r += '\f'; this._pos++; break;
          case 0x6E: r += '\n'; this._pos++; break;
          case 0x72: r += '\r'; this._pos++; break;
          case 0x74: r += '\t'; this._pos++; break;
          case 0x75: {
            this._pos++;
            if (this._pos + 4 > this.src.length) throw new Error("json: incomplete unicode escape");
            const hex = this.src.slice(this._pos, this._pos + 4);
            let cp = parseInt(hex, 16);
            if (isNaN(cp)) throw new Error(`json: invalid unicode escape \\u${hex}`);
            this._pos += 4;
            if (cp >= 0xD800 && cp <= 0xDBFF) {
              if (this._pos + 6 <= this.src.length &&
                  this.src.charCodeAt(this._pos) === 0x5C &&
                  this.src.charCodeAt(this._pos + 1) === 0x75) {
                this._pos += 2;
                const hex2 = this.src.slice(this._pos, this._pos + 4);
                const low = parseInt(hex2, 16);
                if (isNaN(low)) throw new Error(`json: invalid low surrogate \\u${hex2}`);
                this._pos += 4;
                if (low >= 0xDC00 && low <= 0xDFFF) {
                  cp = 0x10000 + ((cp - 0xD800) << 10) + (low - 0xDC00);
                } else {
                  throw new Error("json: expected low surrogate after high surrogate");
                }
              } else {
                throw new Error("json: expected low surrogate after high surrogate");
              }
            }
            r += String.fromCodePoint(cp);
            break;
          }
          default:
            throw new Error(`json: invalid escape character '\\${this.src[this._pos]}'`);
        }
      } else if (c < 0x20) {
        throw new Error(`json: unescaped control character U+${c.toString(16).padStart(4, "0")}`);
      } else {
        r += this.src[this._pos];
        this._pos++;
      }
    }
    throw new Error("json: unterminated string");
  }

  private parseNumberRaw(): string {
    this.ws();
    const start = this._pos;
    if (this.src.charCodeAt(this._pos) === 0x2D) this._pos++;
    if (this._pos >= this.src.length) throw new Error("json: unexpected end of number");
    if (this.src.charCodeAt(this._pos) === 0x30) {
      this._pos++;
    } else if (this.src.charCodeAt(this._pos) >= 0x31 && this.src.charCodeAt(this._pos) <= 0x39) {
      this._pos++;
      while (this._pos < this.src.length && this.src.charCodeAt(this._pos) >= 0x30 && this.src.charCodeAt(this._pos) <= 0x39) this._pos++;
    } else {
      throw new Error("json: invalid number");
    }
    if (this._pos < this.src.length && this.src.charCodeAt(this._pos) === 0x2E) {
      this._pos++;
      if (this._pos >= this.src.length || this.src.charCodeAt(this._pos) < 0x30 || this.src.charCodeAt(this._pos) > 0x39) {
        throw new Error("json: invalid number fraction");
      }
      while (this._pos < this.src.length && this.src.charCodeAt(this._pos) >= 0x30 && this.src.charCodeAt(this._pos) <= 0x39) this._pos++;
    }
    if (this._pos < this.src.length && (this.src.charCodeAt(this._pos) === 0x65 || this.src.charCodeAt(this._pos) === 0x45)) {
      this._pos++;
      if (this._pos < this.src.length && (this.src.charCodeAt(this._pos) === 0x2B || this.src.charCodeAt(this._pos) === 0x2D)) this._pos++;
      if (this._pos >= this.src.length || this.src.charCodeAt(this._pos) < 0x30 || this.src.charCodeAt(this._pos) > 0x39) {
        throw new Error("json: invalid number exponent");
      }
      while (this._pos < this.src.length && this.src.charCodeAt(this._pos) >= 0x30 && this.src.charCodeAt(this._pos) <= 0x39) this._pos++;
    }
    return this.src.slice(start, this._pos);
  }

  readString(): string {
    return this.parseString();
  }

  readBool(): boolean {
    const ch = this.peek();
    if (ch === "t") {
      for (const c of "true") { if (this.read() !== c) throw new Error("json: expected 'true'"); }
      return true;
    }
    if (ch === "f") {
      for (const c of "false") { if (this.read() !== c) throw new Error("json: expected 'false'"); }
      return false;
    }
    throw new Error(`json: expected bool, got '${ch}'`);
  }

  readInt32(): number {
    const raw = this.parseNumberRaw();
    const v = Number(raw);
    if (!Number.isInteger(v)) throw new Error(`json: int32 must be integer, got ${raw}`);
    if (v < -2147483648 || v > 2147483647) throw new Error(`json: int32 overflow: ${raw}`);
    return v | 0;
  }

  readInt64(): bigint {
    const ch = this.peek();
    if (ch === '"') {
      const s = this.parseString();
      const v = BigInt(s);
      if (v < BigInt("-9223372036854775808") || v > BigInt("9223372036854775807")) {
        throw new Error(`json: int64 overflow: ${s}`);
      }
      return v;
    }
    const raw = this.parseNumberRaw();
    const v = BigInt(raw);
    if (v < BigInt("-9223372036854775808") || v > BigInt("9223372036854775807")) {
      throw new Error(`json: int64 overflow: ${raw}`);
    }
    return v;
  }

  readUint32(): number {
    const raw = this.parseNumberRaw();
    const v = Number(raw);
    if (!Number.isInteger(v)) throw new Error(`json: uint32 must be integer, got ${raw}`);
    if (v < 0 || v > 4294967295) throw new Error(`json: uint32 overflow: ${raw}`);
    return v >>> 0;
  }

  readUint64(): bigint {
    const ch = this.peek();
    if (ch === '"') {
      const s = this.parseString();
      const v = BigInt(s);
      if (v < BigInt(0) || v > BigInt("18446744073709551615")) {
        throw new Error(`json: uint64 overflow: ${s}`);
      }
      return v;
    }
    const raw = this.parseNumberRaw();
    const v = BigInt(raw);
    if (v < BigInt(0) || v > BigInt("18446744073709551615")) {
      throw new Error(`json: uint64 overflow: ${raw}`);
    }
    return v;
  }

  readFloat32(): number {
    const raw = this.parseNumberRaw();
    const v = parseFloat(raw);
    const f32 = new Float32Array(1);
    f32[0] = v;
    return f32[0];
  }

  readFloat64(): number {
    const raw = this.parseNumberRaw();
    return parseFloat(raw);
  }

  readNull(): null {
    for (const c of "null") { if (this.read() !== c) throw new Error("json: expected 'null'"); }
    return null;
  }

  readBytes(): Uint8Array {
    const s = this.parseString();
    if (s.length % 4 !== 0) throw new Error("json: invalid base64 length");
    const lookup = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/";
    const len = (s.length * 3) / 4 -
      (s.endsWith("==") ? 2 : s.endsWith("=") ? 1 : 0);
    const buf = new Uint8Array(len);
    let bi = 0;
    for (let i = 0; i < s.length; i += 4) {
      const a = lookup.indexOf(s[i]);
      const b = lookup.indexOf(s[i + 1]);
      const c = lookup.indexOf(s[i + 2]);
      const d = lookup.indexOf(s[i + 3]);
      if (a < 0 || b < 0) throw new Error("json: invalid base64");
      buf[bi++] = (a << 2) | (b >> 4);
      if (s[i + 2] !== "=" && c >= 0) {
        buf[bi++] = ((b & 0xF) << 4) | (c >> 2);
        if (s[i + 3] !== "=" && d >= 0) {
          buf[bi++] = ((c & 0x3) << 6) | d;
        }
      }
    }
    return buf;
  }

  readEnum(): string {
    return this.parseString();
  }

  beginObject(): void {
    this.expect("{");
    this._firstField.push(true);
  }

  hasNextField(): boolean {
    const ch = this.peek();
    if (ch === "}") {
      this._firstField.pop();
      return false;
    }
    const top = this._firstField.length - 1;
    if (!this._firstField[top]) {
      if (ch !== ",") throw new Error(`json: expected ',' or '}', got '${ch}'`);
      this._pos++;
    } else {
      this._firstField[top] = false;
    }
    return true;
  }

  readFieldName(): string {
    const key = this.parseString();
    this.ws();
    if (this._pos < this.src.length && this.src[this._pos] === ":") {
      this._pos++;
    } else {
      throw new Error(`json: expected ':' after field name '${key}'`);
    }
    this.ws();
    return key;
  }

  endObject(): void {
    this.expect("}");
  }

  beginArray(): void {
    this.expect("[");
    this._firstElement.push(true);
  }

  hasNextElement(): boolean {
    const ch = this.peek();
    if (ch === "]") {
      this._firstElement.pop();
      return false;
    }
    const top = this._firstElement.length - 1;
    if (!this._firstElement[top]) {
      if (ch !== ",") throw new Error(`json: expected ',' or ']', got '${ch}'`);
      this._pos++;
    } else {
      this._firstElement[top] = false;
    }
    return true;
  }

  endArray(): void {
    this.expect("]");
  }

  isNull(): boolean {
    const ch = this.peek();
    return ch === "n";
  }

  skip(): void {
    this.ws();
    if (this._pos >= this.src.length) throw new Error("json: unexpected end of input");
    const ch = this.src[this._pos];
    switch (ch) {
      case '"': {
        this._pos++;
        while (this._pos < this.src.length) {
          if (this.src.charCodeAt(this._pos) === 0x5C) {
            this._pos += 2;
          } else if (this.src.charCodeAt(this._pos) === 0x22) {
            this._pos++;
            return;
          } else {
            this._pos++;
          }
        }
        throw new Error("json: unterminated string in skip");
      }
      case "{": {
        this.beginObject();
        while (this.hasNextField()) {
          this.readFieldName();
          this.skip();
        }
        this.endObject();
        return;
      }
      case "[": {
        this.beginArray();
        while (this.hasNextElement()) {
          this.skip();
        }
        this.endArray();
        return;
      }
      case "t": { for (const c of "true") { if (this.read() !== c) throw new Error("json: skip expected true"); } return; }
      case "f": { for (const c of "false") { if (this.read() !== c) throw new Error("json: skip expected false"); } return; }
      case "n": { for (const c of "null") { if (this.read() !== c) throw new Error("json: skip expected null"); } return; }
      default:
        if ((ch >= "0" && ch <= "9") || ch === "-") {
          this.parseNumberRaw();
          return;
        }
        throw new Error(`json: unexpected character '${ch}' in skip`);
    }
  }
}
