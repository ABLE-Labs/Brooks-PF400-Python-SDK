"""Public exceptions; transport failures never trigger command retries."""

from .error_codes import ERROR_HINTS, ERROR_MESSAGES


class PF400Error(Exception):
    """Base SDK error."""


class NotConnectedError(PF400Error):
    """The requested channel must be explicitly connected."""


class ConnectionError(PF400Error):
    """A connection failed or was lost; an issued command may have executed."""

    def __init__(self, message: str, *, command: str = "", may_have_executed: bool = False):
        super().__init__(message)
        self.command = command
        self.may_have_executed = may_have_executed


class CommandTimeout(ConnectionError):
    """The deadline expired. Inspect may_have_executed before recovery."""


class ProtocolError(ConnectionError):
    """Malformed or unexpected framing; the affected channel is closed."""


class DeviceError(PF400Error):
    """Any negative controller error code, including unknown codes."""

    def __init__(self, code: int, raw: str, command: str):
        self.code = code
        self.raw = raw
        self.command = command
        manufacturer_detail = raw.partition(" ")[2].strip()
        self.description = ERROR_MESSAGES.get(code, manufacturer_detail or "알 수 없는 장비 오류")
        self.hint = ERROR_HINTS.get(code, "")
        message = f"{command}: {raw}"
        if self.description not in raw:
            message += f" | {self.description}"
        if self.hint:
            message += f" | {self.hint}"
        super().__init__(message)
