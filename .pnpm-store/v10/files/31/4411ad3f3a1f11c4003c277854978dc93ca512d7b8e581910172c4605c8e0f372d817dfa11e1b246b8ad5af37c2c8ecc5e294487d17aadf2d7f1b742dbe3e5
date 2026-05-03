export class GronReader {
    lines = [];
    cursor = 0;
    ctx = [];
    constructor(data) {
        const text = new TextDecoder().decode(data);
        for (const raw of text.split("\n")) {
            const line = raw.trim();
            if (line === "")
                continue;
            const eq = line.indexOf(" = ");
            if (eq < 0)
                continue;
            const path = line.substring(0, eq);
            let val = line.substring(eq + 3);
            if (val.endsWith(";"))
                val = val.substring(0, val.length - 1);
            this.lines.push({ path, rawValue: val });
        }
    }
    unescape(s) {
        if (s.length < 2 || s[0] !== '"' || s[s.length - 1] !== '"')
            throw new Error("gron: expected quoted string");
        let r = "";
        for (let i = 1; i < s.length - 1; i++) {
            if (s[i] === "\\") {
                i++;
                switch (s[i]) {
                    case '"':
                        r += '"';
                        break;
                    case "\\":
                        r += "\\";
                        break;
                    case "/":
                        r += "/";
                        break;
                    case "b":
                        r += "\b";
                        break;
                    case "f":
                        r += "\f";
                        break;
                    case "n":
                        r += "\n";
                        break;
                    case "r":
                        r += "\r";
                        break;
                    case "t":
                        r += "\t";
                        break;
                    case "u": {
                        r += String.fromCharCode(parseInt(s.substring(i + 1, i + 5), 16));
                        i += 4;
                        break;
                    }
                }
            }
            else {
                r += s[i];
            }
        }
        return r;
    }
    readString() {
        return this.unescape(this.lines[this.cursor++].rawValue);
    }
    readBool() {
        return this.lines[this.cursor++].rawValue === "true";
    }
    readInt32() {
        return parseInt(this.lines[this.cursor++].rawValue, 10) | 0;
    }
    readInt64() {
        return BigInt(this.unescape(this.lines[this.cursor++].rawValue));
    }
    readUint32() {
        return parseInt(this.lines[this.cursor++].rawValue, 10) >>> 0;
    }
    readUint64() {
        return BigInt(this.unescape(this.lines[this.cursor++].rawValue));
    }
    readFloat32() {
        const v = this.lines[this.cursor++].rawValue;
        const f32 = new Float32Array(1);
        f32[0] = parseFloat(v);
        return f32[0];
    }
    readFloat64() {
        const v = this.lines[this.cursor++].rawValue;
        return parseFloat(v);
    }
    readNull() {
        const line = this.lines[this.cursor++];
        if (line.rawValue !== "null")
            throw new Error("gron: expected null");
        return null;
    }
    readBytes() {
        const b64 = this.unescape(this.lines[this.cursor++].rawValue);
        const bin = atob(b64);
        const buf = new Uint8Array(bin.length);
        for (let i = 0; i < bin.length; i++)
            buf[i] = bin.charCodeAt(i);
        return buf;
    }
    readEnum() {
        return this.readString();
    }
    beginObject() {
        const line = this.lines[this.cursor++];
        this.ctx.push({ prefix: line.path, type: "object" });
    }
    hasNextField() {
        if (this.cursor >= this.lines.length)
            return false;
        const pfx = this.ctx[this.ctx.length - 1].prefix + ".";
        const p = this.lines[this.cursor].path;
        if (!p.startsWith(pfx))
            return false;
        const rem = p.substring(pfx.length);
        return !rem.includes(".") && !rem.includes("[");
    }
    readFieldName() {
        const pfx = this.ctx[this.ctx.length - 1].prefix + ".";
        return this.lines[this.cursor].path.substring(pfx.length);
    }
    endObject() {
        this.ctx.pop();
    }
    beginArray() {
        const line = this.lines[this.cursor++];
        this.ctx.push({ prefix: line.path, type: "array", index: -1 });
    }
    hasNextElement() {
        if (this.cursor >= this.lines.length)
            return false;
        const arr = this.ctx[this.ctx.length - 1];
        const ni = (arr.index ?? -1) + 1;
        const exp = arr.prefix + "[" + ni + "]";
        const p = this.lines[this.cursor].path;
        return p === exp || p.startsWith(exp + ".") || p.startsWith(exp + "[");
    }
    nextElement() {
        const arr = this.ctx[this.ctx.length - 1];
        arr.index = (arr.index ?? -1) + 1;
    }
    endArray() {
        this.ctx.pop();
    }
    isNull() {
        return this.cursor < this.lines.length && this.lines[this.cursor].rawValue === "null";
    }
    skip() {
        const sp = this.lines[this.cursor++].path;
        while (this.cursor < this.lines.length) {
            const np = this.lines[this.cursor].path;
            if (np.length > sp.length && (np.startsWith(sp + ".") || np.startsWith(sp + "[")))
                this.cursor++;
            else
                break;
        }
    }
}
