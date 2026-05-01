from __future__ import annotations

import math
import struct

# fmt_float32: returns the shortest decimal string that uniquely identifies
# the given float32 value and round-trips back to the same float32 bits.
#
# Algorithm: iterate precision p = 1..9, return the first s = f"{v:.{p}g}"
# such that struct.pack(">f", float(s)) == struct.pack(">f", v).
# Float32 has 24 mantissa bits → at most 9 significant decimal digits needed.
#
# TODO: replace body with a Ryu f32 implementation for O(1) performance.
def fmt_float32(value: float) -> str:
    packed = struct.pack(">f", value)
    f32 = struct.unpack(">f", packed)[0]
    if math.isnan(f32) or math.isinf(f32):
        raise ValueError("float32: NaN/Infinity not supported")
    if math.copysign(1.0, f32) < 0 and f32 == 0.0:
        return "-0"
    for prec in range(1, 10):
        s = f"{f32:.{prec}g}"
        if struct.pack(">f", float(s)) == packed:
            return s
    return repr(f32)  # unreachable for valid finite float32
