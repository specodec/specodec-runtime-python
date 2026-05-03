export class MsgPackReader {
    buf;
    _pos;
    _containerCount = [];
    constructor(data) {
        this.buf = data;
        this._pos = 0;
    }
    get pos() { return this._pos; }
    readByte() {
        if (this._pos >= this.buf.length)
            throw new Error("msgpack: unexpected end of data");
        return this.buf[this._pos++];
    }
    readU16() {
        const v = (this.buf[this._pos] << 8) | this.buf[this._pos + 1];
        this._pos += 2;
        return v;
    }
    readU32() {
        const v = (this.buf[this._pos] << 24) | (this.buf[this._pos + 1] << 16) |
            (this.buf[this._pos + 2] << 8) | this.buf[this._pos + 3];
        this._pos += 4;
        return v >>> 0;
    }
    readI16() {
        const v = this.readU16();
        return v > 0x7FFF ? v - 0x10000 : v;
    }
    readI32() {
        const v = this.readU32();
        return v > 0x7FFFFFFF ? v - 0x100000000 : v;
    }
    readF32() {
        const view = new DataView(this.buf.buffer, this.buf.byteOffset + this._pos, 4);
        this._pos += 4;
        return view.getFloat32(0, false);
    }
    readF64() {
        const view = new DataView(this.buf.buffer, this.buf.byteOffset + this._pos, 8);
        this._pos += 8;
        return view.getFloat64(0, false);
    }
    readMapHeader() {
        const b = this.readByte();
        if ((b & 0xF0) === 0x80)
            return b & 0x0F;
        if (b === 0xDE)
            return this.readU16();
        if (b === 0xDF)
            return this.readU32();
        throw new Error(`msgpack: expected map, got 0x${b.toString(16)}`);
    }
    readArrayHeader() {
        const b = this.readByte();
        if ((b & 0xF0) === 0x90)
            return b & 0x0F;
        if (b === 0xDC)
            return this.readU16();
        if (b === 0xDD)
            return this.readU32();
        throw new Error(`msgpack: expected array, got 0x${b.toString(16)}`);
    }
    readString() {
        const b = this.readByte();
        let len;
        if ((b & 0xE0) === 0xA0)
            len = b & 0x1F;
        else if (b === 0xD9)
            len = this.readByte();
        else if (b === 0xDA)
            len = this.readU16();
        else if (b === 0xDB)
            len = this.readU32();
        else
            throw new Error(`msgpack: expected string, got 0x${b.toString(16)}`);
        const s = new TextDecoder().decode(this.buf.slice(this._pos, this._pos + len));
        this._pos += len;
        return s;
    }
    readInt() {
        const b = this.readByte();
        if (b <= 0x7F)
            return b;
        if (b >= 0xE0)
            return b - 0x100;
        if (b === 0xCC)
            return this.readByte();
        if (b === 0xCD)
            return this.readU16();
        if (b === 0xCE)
            return this.readU32();
        if (b === 0xCF) {
            this.readU32();
            return this.readU32();
        }
        if (b === 0xD0) {
            const v = this.readByte();
            return v > 127 ? v - 256 : v;
        }
        if (b === 0xD1)
            return this.readI16();
        if (b === 0xD2)
            return this.readI32();
        if (b === 0xD3) {
            this.readU32();
            return this.readI32();
        }
        throw new Error(`msgpack: expected int, got 0x${b.toString(16)}`);
    }
    readInt32() { return this.readInt() | 0; }
    readInt64() {
        const b = this.readByte();
        if (b <= 0x7F)
            return BigInt(b);
        if (b >= 0xE0)
            return BigInt(b - 0x100);
        if (b === 0xCC)
            return BigInt(this.readByte());
        if (b === 0xCD)
            return BigInt(this.readU16());
        if (b === 0xCE)
            return BigInt(this.readU32());
        if (b === 0xCF) {
            const hi = this.readU32();
            const lo = this.readU32();
            return (BigInt(hi) << BigInt(32)) | BigInt(lo);
        }
        if (b === 0xD0) {
            const v = this.readByte();
            return BigInt(v > 127 ? v - 256 : v);
        }
        if (b === 0xD1)
            return BigInt(this.readI16());
        if (b === 0xD2)
            return BigInt(this.readI32());
        if (b === 0xD3) {
            const hi = this.readU32();
            const lo = this.readU32();
            const unsigned = (BigInt(hi) << BigInt(32)) | BigInt(lo);
            return unsigned >= BigInt("9223372036854775808") ? unsigned - BigInt("18446744073709551616") : unsigned;
        }
        throw new Error(`msgpack: expected int64, got 0x${b.toString(16)}`);
    }
    readUint32() { return this.readInt() >>> 0; }
    readUint64() {
        const b = this.readByte();
        if (b <= 0x7F)
            return BigInt(b);
        if (b === 0xCC)
            return BigInt(this.readByte());
        if (b === 0xCD)
            return BigInt(this.readU16());
        if (b === 0xCE)
            return BigInt(this.readU32());
        if (b === 0xCF) {
            const hi = this.readU32();
            const lo = this.readU32();
            return (BigInt(hi) << BigInt(32)) | BigInt(lo);
        }
        throw new Error(`msgpack: expected uint64, got 0x${b.toString(16)}`);
    }
    readFloat() {
        const b = this.readByte();
        if (b === 0xCA)
            return this.readF32();
        if (b === 0xCB)
            return this.readF64();
        throw new Error(`msgpack: expected float, got 0x${b.toString(16)}`);
    }
    readFloat32() {
        const b = this.readByte();
        const f32 = new Float32Array(1);
        if (b === 0xCA) {
            f32[0] = this.readF32();
            return f32[0];
        }
        if (b === 0xCB) {
            f32[0] = this.readF64();
            return f32[0];
        }
        if (b <= 0x7F)
            return b;
        if (b >= 0xE0)
            return b - 0x100;
        if (b === 0xCC)
            return this.readByte();
        if (b === 0xCD)
            return this.readU16();
        if (b === 0xCE)
            return this.readU32();
        if (b === 0xD0) {
            const v = this.readByte();
            return v > 127 ? v - 256 : v;
        }
        if (b === 0xD1)
            return this.readI16();
        if (b === 0xD2)
            return this.readI32();
        throw new Error(`msgpack: expected float32, got 0x${b.toString(16)}`);
    }
    readFloat64() {
        const b = this.readByte();
        if (b === 0xCA)
            return this.readF32();
        if (b === 0xCB)
            return this.readF64();
        if (b <= 0x7F)
            return b;
        if (b >= 0xE0)
            return b - 0x100;
        if (b === 0xCC)
            return this.readByte();
        if (b === 0xCD)
            return this.readU16();
        if (b === 0xCE)
            return this.readU32();
        if (b === 0xD0) {
            const v = this.readByte();
            return v > 127 ? v - 256 : v;
        }
        if (b === 0xD1)
            return this.readI16();
        if (b === 0xD2)
            return this.readI32();
        throw new Error(`msgpack: expected float64, got 0x${b.toString(16)}`);
    }
    readBytes() {
        const b = this.readByte();
        let len;
        if (b === 0xC4)
            len = this.readByte();
        else if (b === 0xC5)
            len = this.readU16();
        else if (b === 0xC6)
            len = this.readU32();
        else
            throw new Error(`msgpack: expected bin, got 0x${b.toString(16)}`);
        const slice = this.buf.slice(this._pos, this._pos + len);
        this._pos += len;
        return slice;
    }
    readEnum() { return this.readString(); }
    readBool() {
        const b = this.readByte();
        if (b === 0xC3)
            return true;
        if (b === 0xC2)
            return false;
        throw new Error(`msgpack: expected bool, got 0x${b.toString(16)}`);
    }
    readNull() {
        const b = this.readByte();
        if (b === 0xC0)
            return null;
        throw new Error(`msgpack: expected null, got 0x${b.toString(16)}`);
    }
    isNull() {
        if (this._pos >= this.buf.length)
            return false;
        return this.buf[this._pos] === 0xC0;
    }
    skip() {
        const b = this.readByte();
        if (b <= 0x7F || b >= 0xE0)
            return;
        if ((b & 0xF0) === 0x80) {
            const n = b & 0x0F;
            for (let i = 0; i < n; i++) {
                this.skip();
                this.skip();
            }
            return;
        }
        if ((b & 0xF0) === 0x90) {
            const n = b & 0x0F;
            for (let i = 0; i < n; i++)
                this.skip();
            return;
        }
        if ((b & 0xE0) === 0xA0) {
            this._pos += b & 0x1F;
            return;
        }
        switch (b) {
            case 0xC0:
            case 0xC2:
            case 0xC3: return;
            case 0xCC:
                this._pos++;
                return;
            case 0xCD:
                this._pos += 2;
                return;
            case 0xCE:
            case 0xCA:
                this._pos += 4;
                return;
            case 0xCF:
            case 0xCB:
                this._pos += 8;
                return;
            case 0xD0:
                this._pos++;
                return;
            case 0xD1:
                this._pos += 2;
                return;
            case 0xD2:
                this._pos += 4;
                return;
            case 0xD3:
                this._pos += 8;
                return;
            case 0xD9:
                this._pos += this.readByte();
                return;
            case 0xDA:
                this._pos += this.readU16();
                return;
            case 0xDB:
                this._pos += this.readU32();
                return;
            case 0xC4:
                this._pos += this.readByte();
                return;
            case 0xC5:
                this._pos += this.readU16();
                return;
            case 0xC6:
                this._pos += this.readU32();
                return;
            case 0xDC: {
                const n = this.readU16();
                for (let i = 0; i < n; i++)
                    this.skip();
                return;
            }
            case 0xDD: {
                const n = this.readU32();
                for (let i = 0; i < n; i++)
                    this.skip();
                return;
            }
            case 0xDE: {
                const n = this.readU16();
                for (let i = 0; i < n; i++) {
                    this.skip();
                    this.skip();
                }
                return;
            }
            case 0xDF: {
                const n = this.readU32();
                for (let i = 0; i < n; i++) {
                    this.skip();
                    this.skip();
                }
                return;
            }
            case 0xD4:
                this._pos += 2;
                return;
            case 0xD5:
                this._pos += 3;
                return;
            case 0xD6:
                this._pos += 5;
                return;
            case 0xD7:
                this._pos += 9;
                return;
            case 0xD8:
                this._pos += 17;
                return;
            case 0xC7: {
                const l = this.readByte();
                this._pos += 1 + l;
                return;
            }
            case 0xC8: {
                const l = this.readU16();
                this._pos += 1 + l;
                return;
            }
            case 0xC9: {
                const l = this.readU32();
                this._pos += 1 + l;
                return;
            }
            default: throw new Error(`msgpack: unknown format 0x${b.toString(16)}`);
        }
    }
    beginObject() {
        const n = this.readMapHeader();
        this._containerCount.push(n);
    }
    hasNextField() {
        const top = this._containerCount.length - 1;
        if (this._containerCount[top] > 0) {
            this._containerCount[top]--;
            return true;
        }
        this._containerCount.pop();
        return false;
    }
    readFieldName() {
        return this.readString();
    }
    endObject() { }
    beginArray() {
        const n = this.readArrayHeader();
        this._containerCount.push(n);
    }
    hasNextElement() {
        const top = this._containerCount.length - 1;
        if (this._containerCount[top] > 0) {
            this._containerCount[top]--;
            return true;
        }
        this._containerCount.pop();
        return false;
    }
    endArray() { }
}
