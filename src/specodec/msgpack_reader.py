from __future__ import annotations

import struct
from typing import Any


class SCodecError(Exception):
    def __init__(self, code: str, message: str):
        super().__init__(message)
        self.code = code


class MsgPackReader:
    def __init__(self, data: bytes) -> None:
        self._buf = data
        self._pos = 0
        self._container_count: list[int] = []

    @property
    def pos(self) -> int:
        return self._pos

    def _read_byte(self) -> int:
        if self._pos >= len(self._buf):
            raise SCodecError("internal", "msgpack: unexpected end of data")
        b = self._buf[self._pos]
        self._pos += 1
        return b

    def _read_u16(self) -> int:
        v = struct.unpack_from(">H", self._buf, self._pos)[0]
        self._pos += 2
        return v

    def _read_u32(self) -> int:
        v = struct.unpack_from(">I", self._buf, self._pos)[0]
        self._pos += 4
        return v

    def _read_i16(self) -> int:
        v = struct.unpack_from(">h", self._buf, self._pos)[0]
        self._pos += 2
        return v

    def _read_i32(self) -> int:
        v = struct.unpack_from(">i", self._buf, self._pos)[0]
        self._pos += 4
        return v

    def read_map_header(self) -> int:
        b = self._read_byte()
        if b & 0xF0 == 0x80:
            return b & 0x0F
        if b == 0xDE:
            return self._read_u16()
        if b == 0xDF:
            return self._read_u32()
        raise SCodecError("internal", f"msgpack: expected map, got 0x{b:02X}")

    def read_array_header(self) -> int:
        b = self._read_byte()
        if b & 0xF0 == 0x90:
            return b & 0x0F
        if b == 0xDC:
            return self._read_u16()
        if b == 0xDD:
            return self._read_u32()
        raise SCodecError("internal", f"msgpack: expected array, got 0x{b:02X}")

    def read_string(self) -> str:
        b = self._read_byte()
        if b & 0xE0 == 0xA0:
            length = b & 0x1F
        elif b == 0xD9:
            length = self._read_byte()
        elif b == 0xDA:
            length = self._read_u16()
        elif b == 0xDB:
            length = self._read_u32()
        else:
            raise SCodecError("internal", f"msgpack: expected string, got 0x{b:02X}")
        s = self._buf[self._pos:self._pos + length].decode("utf-8")
        self._pos += length
        return s

    def read_int(self) -> int:
        b = self._read_byte()
        if b <= 0x7F:
            return b
        if b >= 0xE0:
            return b - 0x100
        if b == 0xCC:
            return self._read_byte()
        if b == 0xCD:
            return self._read_u16()
        if b == 0xCE:
            return self._read_u32()
        if b == 0xD0:
            return struct.unpack_from(">b", self._buf, self._pos - 0)[0]
        if b == 0xD1:
            return self._read_i16()
        if b == 0xD2:
            return self._read_i32()
        raise SCodecError("internal", f"msgpack: expected int, got 0x{b:02X}")

    def read_float(self) -> float:
        b = self._read_byte()
        if b == 0xCA:
            v = struct.unpack_from(">f", self._buf, self._pos)[0]
            self._pos += 4
            return v
        if b == 0xCB:
            v = struct.unpack_from(">d", self._buf, self._pos)[0]
            self._pos += 8
            return v
        raise SCodecError("internal", f"msgpack: expected float, got 0x{b:02X}")

    def read_bool(self) -> bool:
        b = self._read_byte()
        if b == 0xC3:
            return True
        if b == 0xC2:
            return False
        raise SCodecError("internal", f"msgpack: expected bool, got 0x{b:02X}")

    def read_null(self) -> None:
        b = self._read_byte()
        if b != 0xC0:
            raise SCodecError("internal", f"msgpack: expected null, got 0x{b:02X}")

    def is_null(self) -> bool:
        if self._pos >= len(self._buf):
            return False
        return self._buf[self._pos] == 0xC0

    def skip(self) -> None:
        b = self._read_byte()
        if b <= 0x7F or b >= 0xE0:
            return
        if b & 0xF0 == 0x80:
            for _ in range(b & 0x0F):
                self.skip()
                self.skip()
            return
        if b & 0xF0 == 0x90:
            for _ in range(b & 0x0F):
                self.skip()
            return
        if b & 0xE0 == 0xA0:
            self._pos += b & 0x1F
            return
        skip_map = {
            0xC0: 0, 0xC2: 0, 0xC3: 0,
            0xCC: 1, 0xD0: 1,
            0xCD: 2, 0xD1: 2,
            0xCE: 4, 0xD2: 4, 0xCA: 4,
            0xCF: 8, 0xD3: 8, 0xCB: 8,
            0xD4: 2, 0xD5: 3, 0xD6: 5, 0xD7: 9, 0xD8: 17,
        }
        if b in skip_map:
            self._pos += skip_map[b]
            return
        if b == 0xD9:
            self._pos += self._read_byte()
            return
        if b == 0xDA:
            self._pos += self._read_u16()
            return
        if b == 0xDB:
            self._pos += self._read_u32()
            return
        if b == 0xC4:
            self._pos += self._read_byte()
            return
        if b == 0xC5:
            self._pos += self._read_u16()
            return
        if b == 0xC6:
            self._pos += self._read_u32()
            return
        if b == 0xC7:
            self._pos += 1 + self._read_byte()
            return
        if b == 0xC8:
            self._pos += 1 + self._read_u16()
            return
        if b == 0xC9:
            self._pos += 1 + self._read_u32()
            return
        if b == 0xDC:
            n = self._read_u16()
            for _ in range(n):
                self.skip()
            return
        if b == 0xDD:
            n = self._read_u32()
            for _ in range(n):
                self.skip()
            return
        if b == 0xDE:
            n = self._read_u16()
            for _ in range(n):
                self.skip()
                self.skip()
            return
        if b == 0xDF:
            n = self._read_u32()
            for _ in range(n):
                self.skip()
                self.skip()
            return
        raise SCodecError("internal", f"msgpack: unknown format 0x{b:02X}")

    def begin_object(self) -> None:
        n = self.read_map_header()
        self._container_count.append(n)

    def has_next_field(self) -> bool:
        top = len(self._container_count) - 1
        if self._container_count[top] > 0:
            self._container_count[top] -= 1
            return True
        self._container_count.pop()
        return False

    def read_field_name(self) -> str:
        return self.read_string()

    def end_object(self) -> None:
        pass

    def begin_array(self) -> None:
        n = self.read_array_header()
        self._container_count.append(n)

    def has_next_element(self) -> bool:
        top = len(self._container_count) - 1
        if self._container_count[top] > 0:
            self._container_count[top] -= 1
            return True
        self._container_count.pop()
        return False

    def end_array(self) -> None:
        pass
