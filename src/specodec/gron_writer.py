from __future__ import annotations


class GronWriter:
    def write_string(self, value: str) -> None: raise NotImplementedError("GronWriter: not implemented")
    def write_bool(self, value: bool) -> None: raise NotImplementedError("GronWriter: not implemented")
    def write_int32(self, value: int) -> None: raise NotImplementedError("GronWriter: not implemented")
    def write_int64(self, value: int) -> None: raise NotImplementedError("GronWriter: not implemented")
    def write_uint32(self, value: int) -> None: raise NotImplementedError("GronWriter: not implemented")
    def write_uint64(self, value: int) -> None: raise NotImplementedError("GronWriter: not implemented")
    def write_float32(self, value: float) -> None: raise NotImplementedError("GronWriter: not implemented")
    def write_float64(self, value: float) -> None: raise NotImplementedError("GronWriter: not implemented")
    def write_null(self) -> None: raise NotImplementedError("GronWriter: not implemented")
    def write_bytes(self, value: bytes) -> None: raise NotImplementedError("GronWriter: not implemented")
    def begin_object(self, field_count: int) -> None: raise NotImplementedError("GronWriter: not implemented")
    def write_field(self, name: str) -> None: raise NotImplementedError("GronWriter: not implemented")
    def end_object(self) -> None: raise NotImplementedError("GronWriter: not implemented")
    def begin_array(self, element_count: int) -> None: raise NotImplementedError("GronWriter: not implemented")
    def next_element(self) -> None: raise NotImplementedError("GronWriter: not implemented")
    def end_array(self) -> None: raise NotImplementedError("GronWriter: not implemented")
    def to_bytes(self) -> bytes: raise NotImplementedError("GronWriter: not implemented")
