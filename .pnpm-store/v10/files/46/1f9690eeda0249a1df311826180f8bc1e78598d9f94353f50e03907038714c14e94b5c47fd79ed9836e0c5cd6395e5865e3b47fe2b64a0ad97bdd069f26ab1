// Float64 configuration constants
const DOUBLE_MANTISSA_BITS = 52;
const DOUBLE_BIAS = 1023;
const DOUBLE_POW5_INV_BITCOUNT = 125;
const DOUBLE_POW5_BITCOUNT = 125;
import { pow5bits, log10Pow2, log10Pow5, decimalLength17, mulShift64, multipleOfPowerOf5_64, multipleOfPowerOf2_64 } from './ryu_math.js';
import { DOUBLE_POW5_INV_SPLIT, DOUBLE_POW5_SPLIT } from './tables_f64.js';
export function float64ToString(d) {
    const buf = new ArrayBuffer(8);
    const f64 = new Float64Array(buf);
    const u64 = new BigUint64Array(buf);
    f64[0] = d;
    const bits = u64[0];
    const sign = (bits >> 63n) !== 0n;
    const ieeeMantissa = bits & 0xfffffffffffffn;
    const ieeeExponent = Number((bits >> 52n) & 0x7ffn);
    if (ieeeExponent === 2047) {
        if (ieeeMantissa === 0n)
            return sign ? "-Infinity" : "Infinity";
        return "NaN";
    }
    if (ieeeExponent === 0 && ieeeMantissa === 0n) {
        return sign ? "-0E0" : "0E0";
    }
    const e2 = ieeeExponent === 0
        ? 1 - DOUBLE_BIAS - DOUBLE_MANTISSA_BITS - 2
        : ieeeExponent - DOUBLE_BIAS - DOUBLE_MANTISSA_BITS - 2;
    const m2 = ieeeExponent === 0 ? ieeeMantissa : (1n << BigInt(DOUBLE_MANTISSA_BITS)) | ieeeMantissa;
    const even = (m2 & 1n) === 0n;
    const acceptBounds = even;
    const mv = m2 * 4n;
    const mp = mv + 2n;
    const mmShift = (ieeeMantissa !== 0n || ieeeExponent <= 1) ? 1 : 0;
    const mm = mv - 1n - BigInt(mmShift);
    let vrIsTrailingZeros = false;
    let vmIsTrailingZeros = false;
    let lastDigit = 0n;
    let e10;
    let vr, vp, vm_;
    if (e2 >= 0) {
        const q = log10Pow2(e2);
        e10 = q;
        const k = DOUBLE_POW5_INV_BITCOUNT + pow5bits(q) - 1;
        const i = -e2 + q + k;
        vr = mulShift64(mv, DOUBLE_POW5_INV_SPLIT[q], i);
        vp = mulShift64(mp, DOUBLE_POW5_INV_SPLIT[q], i);
        vm_ = mulShift64(mm, DOUBLE_POW5_INV_SPLIT[q], i);
        if (q !== 0 && (vp - 1n) / 10n <= vm_ / 10n) {
            const l = DOUBLE_POW5_INV_BITCOUNT + pow5bits(q - 1) - 1;
            lastDigit = mulShift64(mv, DOUBLE_POW5_INV_SPLIT[q - 1], -e2 + q - 1 + l) % 10n;
        }
        if (q <= 21) {
            if (mv % 5n === 0n) {
                vrIsTrailingZeros = multipleOfPowerOf5_64(mv, q);
            }
            else if (acceptBounds) {
                vmIsTrailingZeros = multipleOfPowerOf5_64(mm, q);
            }
            else {
                if (multipleOfPowerOf5_64(mp, q))
                    vp = vp - 1n;
            }
        }
    }
    else {
        const q = log10Pow5(-e2);
        e10 = q + e2;
        const i = -e2 - q;
        const k = pow5bits(i) - DOUBLE_POW5_BITCOUNT;
        const j = q - k;
        vr = mulShift64(mv, DOUBLE_POW5_SPLIT[i], j);
        vp = mulShift64(mp, DOUBLE_POW5_SPLIT[i], j);
        vm_ = mulShift64(mm, DOUBLE_POW5_SPLIT[i], j);
        if (q !== 0 && (vp - 1n) / 10n <= vm_ / 10n) {
            const j2 = q - 1 - (pow5bits(i + 1) - DOUBLE_POW5_BITCOUNT);
            lastDigit = mulShift64(mv, DOUBLE_POW5_SPLIT[i + 1], j2) % 10n;
        }
        if (q <= 1) {
            vrIsTrailingZeros = true;
            if (acceptBounds) {
                vmIsTrailingZeros = mmShift === 1;
            }
            else {
                vp = vp - 1n;
            }
        }
        else if (q < 63) {
            vrIsTrailingZeros = multipleOfPowerOf2_64(mv, q - 1);
            if (acceptBounds) {
                vmIsTrailingZeros = multipleOfPowerOf5_64(mm, q);
            }
            else {
                if (multipleOfPowerOf5_64(mp, q))
                    vp = vp - 1n;
            }
        }
    }
    let removed = 0;
    let vr2 = vr, vp2 = vp, vm2 = vm_;
    if (vmIsTrailingZeros || vrIsTrailingZeros) {
        while (vp2 / 10n > vm2 / 10n) {
            vmIsTrailingZeros = vmIsTrailingZeros && (vm2 % 10n === 0n);
            vrIsTrailingZeros = vrIsTrailingZeros && (lastDigit === 0n);
            lastDigit = vr2 % 10n;
            vr2 = vr2 / 10n;
            vp2 = vp2 / 10n;
            vm2 = vm2 / 10n;
            removed++;
        }
        if (vmIsTrailingZeros) {
            while (vm2 % 10n === 0n) {
                vrIsTrailingZeros = vrIsTrailingZeros && (lastDigit === 0n);
                lastDigit = vr2 % 10n;
                vr2 = vr2 / 10n;
                vp2 = vp2 / 10n;
                vm2 = vm2 / 10n;
                removed++;
            }
        }
        if (vrIsTrailingZeros && lastDigit === 5n && (vr2 & 1n) === 0n) {
            lastDigit = 4n;
        }
        const roundUp = (vr2 === vm2 && (!acceptBounds || !vmIsTrailingZeros)) || lastDigit >= 5n;
        const output = roundUp ? vr2 + 1n : vr2;
        const exp = e10 + removed;
        const olength = decimalLength17(output);
        let result = sign ? "-" : "";
        const digits = output.toString();
        if (olength === 1) {
            result += digits;
        }
        else {
            result += digits[0] + "." + digits.substring(1);
        }
        result += "E" + (exp + olength - 1).toString();
        return result;
    }
    else {
        while (vp2 / 10n > vm2 / 10n) {
            lastDigit = vr2 % 10n;
            vr2 = vr2 / 10n;
            vp2 = vp2 / 10n;
            vm2 = vm2 / 10n;
            removed++;
        }
        const output = (vr2 === vm2 || lastDigit >= 5n) ? vr2 + 1n : vr2;
        const exp = e10 + removed;
        const olength = decimalLength17(output);
        let result = sign ? "-" : "";
        const digits = output.toString();
        if (olength === 1) {
            result += digits;
        }
        else {
            result += digits[0] + "." + digits.substring(1);
        }
        result += "E" + (exp + olength - 1).toString();
        return result;
    }
}
