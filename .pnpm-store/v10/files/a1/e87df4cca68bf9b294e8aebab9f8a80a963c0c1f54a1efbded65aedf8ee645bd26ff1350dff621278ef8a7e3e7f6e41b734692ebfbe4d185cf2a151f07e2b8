export function pow5bits(e) {
    return Math.floor((e * 1217359) / 524288) + 1;
}
export function log10Pow2(e) {
    return Math.floor((e * 78913) / 262144);
}
export function log10Pow5(e) {
    return Math.floor((e * 732923) / 1048576);
}
export function decimalLength9(v) {
    if (v >= 100000000)
        return 9;
    if (v >= 10000000)
        return 8;
    if (v >= 1000000)
        return 7;
    if (v >= 100000)
        return 6;
    if (v >= 10000)
        return 5;
    if (v >= 1000)
        return 4;
    if (v >= 100)
        return 3;
    if (v >= 10)
        return 2;
    return 1;
}
export function decimalLength17(v) {
    if (v >= 10000000000000000n)
        return 17;
    if (v >= 1000000000000000n)
        return 16;
    if (v >= 100000000000000n)
        return 15;
    if (v >= 10000000000000n)
        return 14;
    if (v >= 1000000000000n)
        return 13;
    if (v >= 100000000000n)
        return 12;
    if (v >= 10000000000n)
        return 11;
    if (v >= 1000000000n)
        return 10;
    if (v >= 100000000n)
        return 9;
    if (v >= 10000000n)
        return 8;
    if (v >= 1000000n)
        return 7;
    if (v >= 100000n)
        return 6;
    if (v >= 10000n)
        return 5;
    if (v >= 1000n)
        return 4;
    if (v >= 100n)
        return 3;
    if (v >= 10n)
        return 2;
    return 1;
}
export function mulShift32(m, factor, shift) {
    const factorLo = factor & 0xffffffffn;
    const factorHi = (factor >> 32n) & 0xffffffffn;
    const bits0 = m * factorLo;
    const bits1 = m * factorHi;
    const sum = (bits0 >> 32n) + bits1;
    return (sum >> BigInt(shift - 32)) & 0xffffffffn;
}
export function mulShift64(m, mul, shift) {
    const b0 = m * mul[0];
    const b2 = m * mul[1];
    const b0Hi = b0 >> 64n;
    const sumVal = b0Hi + b2;
    return (sumVal >> BigInt(shift - 64)) & 0xffffffffffffffffn;
}
export function multipleOfPowerOf5_64(value, q) {
    if (q === 0)
        return true;
    if (q >= 64)
        return value === 0n;
    const pow5 = BigInt(5) ** BigInt(q);
    return (value % pow5) === 0n;
}
export function multipleOfPowerOf2_64(value, q) {
    if (q === 0)
        return true;
    if (q >= 64)
        return value === 0n;
    return (value & ((1n << BigInt(q)) - 1n)) === 0n;
}
