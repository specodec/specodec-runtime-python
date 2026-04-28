from __future__ import annotations
import struct


class MsgPackWriter:
    def __init__(self) -> None:
        self._buf: bytearray = bytearray()

    def _write_byte(self, b: int) -> None:
        self._buf.append(b & 0xFF)

    def _write_u16(self, v: int) -> None:
        self._buf.extend(struct.pack(">H", v))

    def _write_u32(self, v: int) -> None:
        self._buf.extend(struct.pack(">I", v))

    def _write_u64(self, v: int) -> None:
        self._buf.extend(struct.pack(">Q", v))

    def write_string(self, value: str) -> None:
        encoded = value.encode("utf-8")
        length = len(encoded)
        if length <= 0x1F:
            self._write_byte(0xA0 | length)
        elif length <= 0xFF:
            self._write_byte(0xD9)
            self._write_byte(length)
        elif length <= 0xFFFF:
            self._write_byte(0xDA)
            self._write_u16(length)
        else:
            self._write_byte(0xDB)
            self._write_u32(length)
        self._buf.extend(encoded)

    def write_bool(self, value: bool) -> None:
        self._write_byte(0xC3 if value else 0xC2)

    def write_int32(self, value: int) -> None:
        if 0 <= value <= 0x7F:
            self._write_byte(value)
        elif -0x20 <= value < 0:
            self._write_byte(value & 0xFF)
        elif 0 <= value <= 0xFF:
            self._write_byte(0xCC)
            self._write_byte(value)
        elif 0 <= value <= 0xFFFF:
            self._write_byte(0xCD)
            self._write_u16(value)
        elif value >= 0:
            self._write_byte(0xCE)
            self._write_u32(value)
        elif value >= -0x80:
            self._write_byte(0xD0)
            self._write_byte(value & 0xFF)
        elif value >= -0x8000:
            self._write_byte(0xD1)
            self._write_u16(value & 0xFFFF)
        else:
            self._write_byte(0xD2)
            self._write_u32(value & 0xFFFFFFFF)

    def write_int64(self, value: int) -> None:
        if 0 <= value <= 0x7F:
            self._write_byte(value)
        elif -0x20 <= value < 0:
            self._write_byte(value & 0xFF)
        elif 0 <= value <= 0xFF:
            self._write_byte(0xCC)
            self._write_byte(value)
        elif 0 <= value <= 0xFFFF:
            self._write_byte(0xCD)
            self._write_u16(value)
        elif 0 <= value <= 0xFFFFFFFF:
            self._write_byte(0xCE)
            self._write_u32(value)
        elif value >= 0:
            self._write_byte(0xCF)
            self._write_u64(value)
        elif value >= -0x80:
            self._write_byte(0xD0)
            self._write_byte(value & 0xFF)
        elif value >= -0x8000:
            self._write_byte(0xD1)
            self._write_u16(value & 0xFFFF)
        elif value >= -0x80000000:
            self._write_byte(0xD2)
            self._write_u32(value & 0xFFFFFFFF)
        else:
            self._write_byte(0xD3)
            self._write_u64(value & 0xFFFFFFFFFFFFFFFF)

    def write_uint32(self, value: int) -> None:
        if value <= 0x7F:
            self._write_byte(value)
        elif value <= 0xFF:
            self._write_byte(0xCC)
            self._write_byte(value)
        elif value <= 0xFFFF:
            self._write_byte(0xCD)
            self._write_u16(value)
        else:
            self._write_byte(0xCE)
            self._write_u32(value)

    def write_uint64(self, value: int) -> None:
        if value <= 0x7F:
            self._write_byte(value)
        elif value <= 0xFF:
            self._write_byte(0xCC)
            self._write_byte(value)
        elif value <= 0xFFFF:
            self._write_byte(0xCD)
            self._write_u16(value)
        elif value <= 0xFFFFFFFF:
            self._write_byte(0xCE)
            self._write_u32(value)
        else:
            self._write_byte(0xCF)
            self._write_u64(value)

    def write_float32(self, value: float) -> None:
        self._write_byte(0xCA)
        self._buf.extend(struct.pack(">f", value))

    def write_float64(self, value: float) -> None:
        self._write_byte(0xCB)
        self._buf.extend(struct.pack(">d", value))

    def write_null(self) -> None:
        self._write_byte(0xC0)

    def write_bytes(self, value: bytes) -> None:
        length = len(value)
        if length <= 0xFF:
            self._write_byte(0xC4)
            self._write_byte(length)
        elif length <= 0xFFFF:
            self._write_byte(0xC5)
            self._write_u16(length)
        else:
            self._write_byte(0xC6)
            self._write_u32(length)
        self._buf.extend(value)

    def begin_object(self, field_count: int) -> None:
        if field_count <= 0x0F:
            self._write_byte(0x80 | field_count)
        elif field_count <= 0xFFFF:
            self._write_byte(0xDE)
            self._write_u16(field_count)
        else:
            self._write_byte(0xDF)
            self._write_u32(field_count)

    def write_field(self, name: str) -> None:
        self.write_string(name)

    def end_object(self) -> None:
        pass

    def begin_array(self, element_count: int) -> None:
        if element_count <= 0x0F:
            self._write_byte(0x90 | element_count)
        elif element_count <= 0xFFFF:
            self._write_byte(0xDC)
            self._write_u16(element_count)
        else:
            self._write_byte(0xDD)
            self._write_u32(element_count)

    def next_element(self) -> None:
        pass

    def end_array(self) -> None:
        pass

    def to_bytes(self) -> bytes:
        return bytes(self._buf)
