"""TCS Normal/Telnet responses and injection-resistant wire arguments."""

from __future__ import annotations

import math
import re
from dataclasses import dataclass

from .errors import DeviceError, ProtocolError

Scalar = int | float | str


@dataclass(frozen=True)
class Response:
    """Normal response data excludes status code; no payload fields are discarded.

    Telnet human-readable responses have code=None and preserve their whole text.
    Boolean data is firmware-specific: -1 often means True, but some fields are
    bitmasks. Convert only after consulting the command reference.
    """

    command: str
    raw: str
    code: int | None
    data: str

    @property
    def values(self) -> tuple[str, ...]:
        return tuple(self.data.split())

    def as_ints(self) -> tuple[int, ...]:
        return tuple(int(value) for value in self.values)

    def as_floats(self) -> tuple[float, ...]:
        return tuple(float(value) for value in self.values)


def parse_response(command: str, raw: str, *, telnet: bool = False) -> Response:
    if not raw or "\x00" in raw:
        raise ProtocolError(f"{command}: empty or invalid response")
    first, _, data = raw.partition(" ")
    if re.fullmatch(r"-?\d+", first):
        code = int(first)
        if code < 0:
            raise DeviceError(code, raw, command)
        if code == 0:
            return Response(command, raw, code, data)
    if telnet:
        return Response(command, raw, None, raw)
    raise ProtocolError(f"{command}: expected Normal response code, got {raw!r}")


def format_argument(value: Scalar, *, quote: bool = False) -> str:
    if isinstance(value, bool):
        return "1" if value else "0"
    if isinstance(value, int):
        return str(value)
    if isinstance(value, float):
        if not math.isfinite(value):
            raise ValueError("Command numbers must be finite")
        return repr(value)
    if not isinstance(value, str):
        raise TypeError("Command arguments must be int, float or str")
    if (not value and not quote) or any(ord(char) < 32 or ord(char) > 126 for char in value):
        raise ValueError("Command strings must be printable ASCII; only quoted Pc values may be empty")
    if '"' in value:
        raise ValueError("Embedded quote marks cannot be represented by this protocol")
    if quote:
        return '"' + value + '"'
    if any(char.isspace() for char in value):
        raise ValueError("This argument must be a single token (no whitespace)")
    return value
