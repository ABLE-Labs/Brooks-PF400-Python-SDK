"""Connection ownership and command dispatch, independent of web frameworks."""

from __future__ import annotations

import asyncio
import threading
from collections.abc import Iterable, Sequence

from .errors import ConnectionError, ProtocolError
from .protocol import Response, Scalar, format_argument
from .transport import SocketChannel, checked_timeout


def _params(*values: Scalar | None) -> tuple[Scalar, ...]:
    values = tuple(values)
    while values and values[-1] is None:
        values = values[:-1]
    if any(value is None for value in values):
        raise ValueError("Optional arguments cannot have gaps; supply preceding firmware values explicitly")
    return values


def _vector(values: Sequence[float], lengths: Iterable[int]) -> tuple[float, ...]:
    if isinstance(values, (str, bytes)) or not isinstance(values, Sequence):
        raise TypeError("Expected a coordinate sequence")
    result = tuple(values)
    if len(result) not in lengths:
        raise ValueError("Coordinate sequence has an unsupported length")
    if any(not isinstance(value, (int, float)) for value in result):
        raise TypeError("Coordinates must be numeric")
    return result


class ClientBase:
    """One controller with independent motion/status channels.

    connect() opens sockets only. Explicitly select the target on the status
    channel before querying per-robot state or issuing Halt there. Startup gives
    that channel robot number 0; the motion port already selects its robot.
    """

    def __init__(
        self,
        host: str,
        *,
        port: int = 10100,
        status_port: int = 10000,
        timeout: float = 10.0,
        max_response_bytes: int = 1048576,
        telnet_mode: bool = False,
    ):
        checked_timeout(timeout)
        if not isinstance(max_response_bytes, int) or max_response_bytes < 16:
            raise ValueError("max_response_bytes must be an integer >= 16")
        for candidate in (port, status_port):
            if not isinstance(candidate, int) or not 1 <= candidate <= 65535:
                raise ValueError("Ports must be integers between 1 and 65535")
        if not isinstance(host, str) or not host.strip():
            raise ValueError("host must be a nonempty string")
        self._channels = {
            "motion": SocketChannel(host, port, timeout, max_response_bytes),
            "status": SocketChannel(host, status_port, timeout, max_response_bytes),
        }
        self._telnet = bool(telnet_mode)
        self._lifecycle_lock = threading.RLock()

    @property
    def connected(self) -> bool:
        """Both sockets are locally open; this does not poll robot readiness."""
        return self.motion_connected and self.status_connected

    @property
    def motion_connected(self) -> bool:
        return self._channels["motion"].socket is not None

    @property
    def status_connected(self) -> bool:
        return self._channels["status"].socket is not None

    def connect(self) -> None:
        """Open sockets without sending power, home, mode or motion commands."""
        with self._lifecycle_lock:
            try:
                for channel in self._channels.values():
                    channel.connect()
            except Exception:
                self.disconnect()
                raise

    def disconnect(self) -> None:
        """Close connections. This does not halt physical robot motion."""
        with self._lifecycle_lock:
            for channel in self._channels.values():
                channel.close()

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc, traceback):
        self.disconnect()

    def execute(
        self, command: str, *arguments: Scalar, channel: str | None = None, timeout: float | None = None
    ) -> Response | None:
        """Execute one catalog command. Vision and unknown commands are rejected.

        Pc strings are quoted automatically, including spaces. Other string
        arguments are single ASCII tokens. No arbitrary multi-command escape.
        """
        from .commands import COMMANDS

        if not isinstance(command, str):
            raise TypeError("command must be a catalog command name")
        canonical = next((name for name in COMMANDS if name.lower() == command.lower()), None)
        if canonical is None:
            raise ValueError(f"Unknown or excluded command: {command!r}")
        return self._invoke(canonical, arguments, channel=channel, timeout=timeout, check_count=False)

    def _invoke(
        self,
        command: str,
        arguments: Sequence[Scalar],
        *,
        channel: str | None,
        timeout: float | None,
        check_count: bool = True,
    ) -> Response | None:
        from .commands import COMMANDS

        counts, default_channel = COMMANDS[command]
        if check_count and counts is not None and len(arguments) not in counts:
            raise ValueError(f"{command} expects wire argument counts {counts}; got {len(arguments)}")
        if command not in ("Pc", "LoadFile", "StoreFile") and any(
            not isinstance(value, (int, float)) for value in arguments
        ):
            raise TypeError(f"{command} takes numeric arguments")
        selected = default_channel if channel is None else channel
        if selected not in self._channels:
            raise ValueError("channel must be 'motion' or 'status'")
        if timeout is not None:
            checked_timeout(timeout)
        formatted = [
            format_argument(value, quote=command == "Pc" and index == len(arguments) - 1)
            for index, value in enumerate(arguments)
        ]
        wire = " ".join((command, *formatted))
        if command == "Mode" and arguments:
            # bTelnetMode is global in this firmware, including the status port.
            # Lock both connections so no local command reads the old framing.
            duration = self._channels[selected].timeout if timeout is None else timeout
            import time
            from .errors import CommandTimeout

            deadline = time.monotonic() + duration
            acquired = []
            try:
                for connection in self._channels.values():
                    if not connection.lock.acquire(timeout=max(0, deadline - time.monotonic())):
                        raise CommandTimeout("Timed out waiting to change global response mode", command=wire)
                    acquired.append(connection.lock)
                remaining = deadline - time.monotonic()
                if remaining <= 0:
                    raise CommandTimeout("Mode deadline expired before dispatch", command=wire)
                new_mode = bool(arguments[0])
                try:
                    response = self._channels[selected].request(wire, timeout=remaining, telnet=new_mode)
                except (ConnectionError, ProtocolError):
                    # Do not take the lifecycle lock while holding channel locks:
                    # another connect() may hold it while waiting for this channel.
                    for connection in self._channels.values():
                        connection.close()  # Mode outcome may be unknown for both channels.
                    raise
                self._telnet = new_mode
                return response
            finally:
                for lock in reversed(acquired):
                    lock.release()
        return self._channels[selected].request(
            wire, timeout=timeout, telnet=lambda: self._telnet, exit_session=command == "Exit"
        )


class AsyncClientBase:
    """Thread-offloaded facade. Cancellation waits for the bounded I/O to finish.

    Cancelling a coroutine does not stop physical motion. Use Halt explicitly
    on a separately selected status channel when that behavior is required.
    """

    def __init__(self, host: str, **kwargs):
        from .client import PF400

        self._client = PF400(host, **kwargs)

    @property
    def connected(self) -> bool:
        return self._client.connected

    @property
    def motion_connected(self) -> bool:
        return self._client.motion_connected

    @property
    def status_connected(self) -> bool:
        return self._client.status_connected

    async def _call(self, method: str, *args, **kwargs):
        task = asyncio.create_task(asyncio.to_thread(getattr(self._client, method), *args, **kwargs))
        try:
            return await asyncio.shield(task)
        except asyncio.CancelledError:
            # Repeated cancellation must not abandon a thread still owning a socket.
            while not task.done():
                try:
                    await asyncio.shield(task)
                except asyncio.CancelledError:
                    continue
                except Exception:
                    break
            if task.done() and not task.cancelled():
                task.exception()  # Retrieve a possible worker exception before propagating cancellation.
            raise

    async def connect(self) -> None:
        try:
            await self._call("connect")
        except asyncio.CancelledError:
            self._client.disconnect()
            raise

    async def disconnect(self) -> None:
        await self._call("disconnect")

    async def execute(
        self, command: str, *arguments: Scalar, channel: str | None = None, timeout: float | None = None
    ) -> Response | None:
        return await self._call("execute", command, *arguments, channel=channel, timeout=timeout)

    async def __aenter__(self):
        await self.connect()
        return self

    async def __aexit__(self, exc_type, exc, traceback):
        await self.disconnect()
