from __future__ import annotations

import base64
import struct

from .float_fmt import format_float32, format_float64


class JsonWriter:
    def __init__(self) -> None:
        self._parts: list[str] = []
        self._first_item: list[bool] = []

    @staticmethod
    def _escape(s: str) -> str:
        r = []
        for c in s:
            code = ord(c)
            if code == 0x22:
                r.append('\\"')
            elif code == 0x5C:
                r.append("\\\\")
            elif code == 0x08:
                r.append("\\b")
            elif code == 0x0C:
                r.append("\\f")
            elif code == 0x0A:
                r.append("\\n")
            elif code == 0x0D:
                r.append("\\r")
            elif code == 0x09:
                r.append("\\t")
            elif code < 0x20:
                r.append(f"\\u{code:04x}")
            else:
                r.append(c)
        return "".join(r)

    def write_string(self, value: str) -> None:
        self._parts.append('"' + self._escape(value) + '"')

    def write_bool(self, value: bool) -> None:
        self._parts.append("true" if value else "false")

    def write_int32(self, value: int) -> None:
        self._parts.append(str(value))

    def write_int64(self, value: int) -> None:
        self._parts.append('"' + str(value) + '"')

    def write_uint32(self, value: int) -> None:
        self._parts.append(str(value))

    def write_uint64(self, value: int) -> None:
        self._parts.append('"' + str(value) + '"')

    def write_float32(self, value: float) -> None:
        f32 = struct.unpack("f", struct.pack("f", value))[0]
        if f32 != f32 or abs(f32) == float("inf"):
            raise ValueError("float32: NaN/Infinity not valid JSON")
        self._parts.append(format_float32(value))

    def write_float64(self, value: float) -> None:
        if value != value or abs(value) == float("inf"):
            raise ValueError("float64: NaN/Infinity not valid JSON")
        self._parts.append(format_float64(value))

    def write_null(self) -> None:
        self._parts.append("null")

    def write_bytes(self, value: bytes) -> None:
        self._parts.append('"' + base64.b64encode(value).decode("ascii") + '"')

    def write_enum(self, value: str) -> None:
        self._parts.append('"' + self._escape(value) + '"')

    def begin_object(self, _field_count: int = 0) -> None:
        self._parts.append("{")
        self._first_item.append(True)

    def write_field(self, name: str) -> None:
        top = len(self._first_item) - 1
        if not self._first_item[top]:
            self._parts.append(",")
        self._first_item[top] = False
        self._parts.append('"' + self._escape(name) + '":')

    def end_object(self) -> None:
        self._first_item.pop()
        self._parts.append("}")

    def begin_array(self, _size: int | None = None) -> None:
        self._parts.append("[")
        self._first_item.append(True)

    def next_element(self) -> None:
        top = len(self._first_item) - 1
        if not self._first_item[top]:
            self._parts.append(",")
        self._first_item[top] = False

    def end_array(self) -> None:
        self._first_item.pop()
        self._parts.append("]")

    def to_bytes(self) -> bytes:
        return "".join(self._parts).encode("utf-8")
