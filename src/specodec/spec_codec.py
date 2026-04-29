from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Generic, TypeVar

from .spec_reader import SpecReader
from .json_reader import JsonReader
from .json_writer import JsonWriter
from .msgpack_reader import MsgPackReader
from .msgpack_writer import MsgPackWriter

T = TypeVar("T")


@dataclass
class SpecCodec(Generic[T]):
    encode_json: Callable[[T], bytes]
    encode_msgpack: Callable[[T], bytes]
    decode: Callable[[SpecReader], T]


def dispatch(codec: SpecCodec[T], body: bytes, content_type: str) -> T:
    if "msgpack" in content_type:
        return codec.decode(MsgPackReader(body))
    return codec.decode(JsonReader(body))


def respond(codec: SpecCodec[T], obj: T, accept: str) -> bytes:
    if "msgpack" in accept:
        return codec.encode_msgpack(obj)
    return codec.encode_json(obj)
