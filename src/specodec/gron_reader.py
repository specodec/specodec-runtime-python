from __future__ import annotations


class GronReader:
    def __init__(self, data: bytes) -> None: pass
    def read_string(self) -> str: raise NotImplementedError("GronReader: not implemented")
    def read_bool(self) -> bool: raise NotImplementedError("GronReader: not implemented")
    def read_int32(self) -> int: raise NotImplementedError("GronReader: not implemented")
    def read_int64(self) -> int: raise NotImplementedError("GronReader: not implemented")
    def read_uint32(self) -> int: raise NotImplementedError("GronReader: not implemented")
    def read_uint64(self) -> int: raise NotImplementedError("GronReader: not implemented")
    def read_float32(self) -> float: raise NotImplementedError("GronReader: not implemented")
    def read_float64(self) -> float: raise NotImplementedError("GronReader: not implemented")
    def read_null(self) -> None: raise NotImplementedError("GronReader: not implemented")
    def read_bytes(self) -> bytes: raise NotImplementedError("GronReader: not implemented")
    def begin_object(self) -> None: raise NotImplementedError("GronReader: not implemented")
    def has_next_field(self) -> bool: raise NotImplementedError("GronReader: not implemented")
    def read_field_name(self) -> str: raise NotImplementedError("GronReader: not implemented")
    def next_field_separator(self) -> None: raise NotImplementedError("GronReader: not implemented")
    def end_object(self) -> None: raise NotImplementedError("GronReader: not implemented")
    def begin_array(self) -> None: raise NotImplementedError("GronReader: not implemented")
    def has_next_element(self) -> bool: raise NotImplementedError("GronReader: not implemented")
    def next_element_separator(self) -> None: raise NotImplementedError("GronReader: not implemented")
    def end_array(self) -> None: raise NotImplementedError("GronReader: not implemented")
    def is_null(self) -> bool: raise NotImplementedError("GronReader: not implemented")
    def skip(self) -> None: raise NotImplementedError("GronReader: not implemented")
