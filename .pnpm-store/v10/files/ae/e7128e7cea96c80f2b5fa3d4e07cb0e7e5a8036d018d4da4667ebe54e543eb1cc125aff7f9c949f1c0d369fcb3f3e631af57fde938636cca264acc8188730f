import { formatFloat32, formatFloat64 } from "./float_fmt.js";
export class GronWriter {
    lines = [];
    segments = ["json"];
    nestingStack = [];
    buildPath() {
        let r = this.segments[0];
        for (let i = 1; i < this.segments.length; i++) {
            if (this.segments[i].startsWith("["))
                r += this.segments[i];
            else
                r += "." + this.segments[i];
        }
        return r;
    }
    escape(s) {
        let r = "";
        for (let i = 0; i < s.length; i++) {
            const c = s.charCodeAt(i);
            switch (c) {
                case 0x22:
                    r += '\\"';
                    break;
                case 0x5C:
                    r += "\\\\";
                    break;
                case 0x08:
                    r += "\\b";
                    break;
                case 0x0C:
                    r += "\\f";
                    break;
                case 0x0A:
                    r += "\\n";
                    break;
                case 0x0D:
                    r += "\\r";
                    break;
                case 0x09:
                    r += "\\t";
                    break;
                default:
                    if (c < 0x20)
                        r += "\\u" + c.toString(16).padStart(4, "0");
                    else
                        r += s.charAt(i);
            }
        }
        return r;
    }
    b64(buf) {
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
    emit(raw) {
        this.lines.push(`${this.buildPath()} = ${raw};`);
    }
    writeString(value) {
        this.emit('"' + this.escape(value) + '"');
    }
    writeBool(value) {
        this.emit(value ? "true" : "false");
    }
    writeInt32(value) {
        this.emit(String(value | 0));
    }
    writeInt64(value) {
        this.emit('"' + String(value) + '"');
    }
    writeUint32(value) {
        this.emit(String(value >>> 0));
    }
    writeUint64(value) {
        this.emit('"' + String(value) + '"');
    }
    writeFloat32(value) {
        const f32 = new Float32Array(1);
        f32[0] = value;
        const v = f32[0];
        if (!isFinite(v))
            throw new Error("float32: NaN/Infinity not valid");
        this.emit(formatFloat32(value));
    }
    writeFloat64(value) {
        if (!isFinite(value))
            throw new Error("float64: NaN/Infinity not valid");
        this.emit(formatFloat64(value));
    }
    writeNull() {
        this.emit("null");
    }
    writeBytes(value) {
        this.emit('"' + this.b64(value) + '"');
    }
    beginObject(_fieldCount) {
        this.lines.push(`${this.buildPath()} = {};`);
        this.nestingStack.push({ depth: this.segments.length });
    }
    writeField(name) {
        const top = this.nestingStack[this.nestingStack.length - 1];
        if (this.segments.length > top.depth) {
            this.segments[this.segments.length - 1] = name;
        }
        else {
            this.segments.push(name);
        }
    }
    endObject() {
        const info = this.nestingStack.pop();
        this.segments.length = info.depth;
    }
    beginArray(_elementCount) {
        this.lines.push(`${this.buildPath()} = [];`);
        this.nestingStack.push({ depth: this.segments.length, arrayIndex: -1 });
    }
    nextElement() {
        const info = this.nestingStack[this.nestingStack.length - 1];
        info.arrayIndex++;
        const idx = info.arrayIndex;
        if (this.segments.length > info.depth) {
            this.segments[this.segments.length - 1] = `[${idx}]`;
        }
        else {
            this.segments.push(`[${idx}]`);
        }
    }
    endArray() {
        const info = this.nestingStack.pop();
        this.segments.length = info.depth;
    }
    writeEnum(value) {
        this.emit('"' + this.escape(value) + '"');
    }
    toBytes() {
        return new TextEncoder().encode(this.lines.join("\n") + "\n");
    }
}
