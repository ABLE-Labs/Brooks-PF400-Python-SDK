"""Independent TCP channels with bounded framing and one deadline per request."""

from __future__ import annotations

import math
import socket
import threading
import time
from collections.abc import Callable

from .errors import CommandTimeout, ConnectionError, NotConnectedError, ProtocolError
from .protocol import Response, parse_response


def checked_timeout(value: float) -> float:
    if not isinstance(value, (int, float)) or not math.isfinite(value) or value <= 0:
        raise ValueError("timeout must be a finite positive number")
    return float(value)


class SocketChannel:
    def __init__(self, host: str, port: int, timeout: float, max_response_bytes: int):
        self.host, self.port = host, port
        self.timeout = checked_timeout(timeout)
        self.max_response_bytes = max_response_bytes
        self.lock = threading.RLock()
        self._state_lock = threading.Lock()
        self.socket: socket.socket | None = None

    def connect(self) -> None:
        with self.lock:
            if self.socket is not None:
                return
            try:
                sock = socket.create_connection((self.host, self.port), self.timeout)
                try:
                    sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
                except OSError:
                    sock.close()
                    raise
                with self._state_lock:
                    self.socket = sock
            except OSError as exc:
                self.close()
                raise ConnectionError(f"Cannot connect to {self.host}:{self.port}: {exc}") from exc

    def close(self, expected: socket.socket | None = None) -> None:
        with self._state_lock:
            if expected is not None and self.socket is not expected:
                return
            sock, self.socket = self.socket, None
        if sock is not None:
            try:
                sock.shutdown(socket.SHUT_RDWR)
            except OSError:
                pass
            sock.close()

    def request(
        self,
        command: str,
        *,
        timeout: float | None,
        telnet: bool | Callable[[], bool],
        exit_session: bool = False,
    ) -> Response | None:
        duration = self.timeout if timeout is None else checked_timeout(timeout)
        deadline = time.monotonic() + duration
        if not self.lock.acquire(timeout=duration):
            raise CommandTimeout("Timed out waiting for the channel lock", command=command)
        sent = False
        sock = None
        try:
            telnet = telnet() if callable(telnet) else telnet
            sock = self.socket  # Snapshot once: disconnect may run concurrently.
            if sock is None:
                raise NotConnectedError(
                    f"{self.host}:{self.port} is not connected; call connect() explicitly"
                )

            def remaining() -> float:
                left = deadline - time.monotonic()
                if left <= 0:
                    raise TimeoutError("Request deadline expired")
                return left

            sock.settimeout(remaining())
            sent = True  # A partial send is also an uncertain outcome.
            sock.sendall((command + "\n").encode("ascii"))
            if exit_session:
                sock.settimeout(remaining())
                if sock.recv(1) != b"":
                    raise ProtocolError("Exit expected the server to close the connection")
                self.close(sock)
                return None
            buffer = bytearray()
            delimiter = b"\r\nCMD> " if telnet else b"\r\n"
            while True:
                sock.settimeout(remaining())
                chunk = sock.recv(min(4096, self.max_response_bytes + 1 - len(buffer)))
                if not chunk:
                    raise ConnectionError(
                        "Peer closed before completing the response", command=command, may_have_executed=sent
                    )
                buffer.extend(chunk)
                if len(buffer) > self.max_response_bytes:
                    raise ProtocolError("Response exceeds max_response_bytes")
                position = buffer.find(delimiter)
                if position >= 0:
                    if position + len(delimiter) != len(buffer):
                        raise ProtocolError("Unexpected bytes after response frame")
                    frame = bytes(buffer[:position])
                    if telnet:
                        if not frame.startswith(b"\r\n"):
                            raise ProtocolError("Telnet response is missing its leading CRLF")
                        frame = frame[2:]
                    try:
                        raw = frame.decode("ascii")
                    except UnicodeDecodeError as exc:
                        raise ProtocolError("Non-ASCII response") from exc
                    if not telnet and ("\n" in raw or "\r" in raw):
                        raise ProtocolError("Invalid Normal response framing")
                    return parse_response(command, raw, telnet=telnet)
                if not telnet and b"\n" in buffer:
                    raise ProtocolError("Normal response requires CRLF framing")
        except (TimeoutError, socket.timeout) as exc:
            self.close(sock)
            raise CommandTimeout(
                "Response deadline expired; no command was retried", command=command, may_have_executed=sent
            ) from exc
        except OSError as exc:
            self.close(sock)
            raise ConnectionError(str(exc), command=command, may_have_executed=sent) from exc
        except ProtocolError as exc:
            exc.command = command
            exc.may_have_executed = sent
            self.close(sock)
            raise
        except ConnectionError:
            self.close(sock)
            raise
        finally:
            self.lock.release()
