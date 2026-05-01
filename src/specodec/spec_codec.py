from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable, Generic, TypeVar

from .spec_reader import SpecReader
from .spec_writer import SpecWriter
from .json_reader import JsonReader
from .json_writer import JsonWriter
from .msgpack_reader import MsgPackReader
from .msgpack_writer import MsgPackWriter
from .gron_reader import GronReader
from .gron_writer import GronWriter

T = TypeVar("T")


@dataclass
class SpecCodec(Generic[T]):
    encode: Callable[[SpecWriter, T], None]
    decode: Callable[[SpecReader], T]


# ---------------------------------------------------------------------------
# FormatEntry
# ---------------------------------------------------------------------------
@dataclass
class FormatEntry:
    content_type: str
    new_writer: Callable[[], SpecWriter]
    new_reader: Callable[[bytes], SpecReader]


# ---------------------------------------------------------------------------
# FormatRegistry
# ---------------------------------------------------------------------------
class FormatRegistry:
    def __init__(self) -> None:
        self._entries: list[FormatEntry] = []

    def register(self, entry: FormatEntry) -> "FormatRegistry":
        self._entries.append(entry)
        return self

    def match(self, content_type: str) -> FormatEntry:
        for e in self._entries:
            sub = e.content_type.split("/", 1)[-1]
            if sub in content_type:
                return e
        return self._entries[0]


# ---------------------------------------------------------------------------
# Default registry
# ---------------------------------------------------------------------------
default_registry = FormatRegistry()
default_registry.register(FormatEntry("application/json",    JsonWriter,               JsonReader))
default_registry.register(FormatEntry("application/msgpack", MsgPackWriter,             MsgPackReader))
default_registry.register(FormatEntry("application/gron",    GronWriter,                GronReader))


# ---------------------------------------------------------------------------
# dispatch / respond
# ---------------------------------------------------------------------------
def dispatch(codec: SpecCodec[T], body: bytes, content_type: str,
             registry: FormatRegistry | None = None) -> T:
    reg = registry or default_registry
    fmt = reg.match(content_type)
    return codec.decode(fmt.new_reader(body))


@dataclass
class RespondResult:
    body: bytes
    content_type: str


def respond(codec: SpecCodec[T], obj: T, accept: str,
            registry: FormatRegistry | None = None) -> RespondResult:
    reg = registry or default_registry
    fmt = reg.match(accept)
    w = fmt.new_writer()
    codec.encode(w, obj)
    return RespondResult(body=w.to_bytes(), content_type=fmt.content_type)
