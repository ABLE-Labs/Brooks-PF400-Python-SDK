# 12 · Error handling

[한국어](README.ko.md) · [Examples guide](../README.md)

Shows how to handle device, timeout, protocol and connection errors from the SDK. Nothing is retried.

## Files

| File | Description | Robot action |
|---|---|---|
| [12_error_handling.py](12_error_handling.py) | Sends `nop()` and `where_j()`, prints any error to stderr and exits with code `1` | Read only |

## Errors handled

| Exception | What is printed |
|---|---|
| `DeviceError` | `code`, `command`, `description`, `raw`, and `hint` if available |
| `CommandTimeout` | `command`, `may_have_executed` |
| `ProtocolError` | Message and `may_have_executed` |
| `ConnectionError` | Message and `may_have_executed` |
| `NotConnectedError` | Message |

`CommandTimeout` and `ProtocolError` are subclasses of `ConnectionError`, so they are caught first.
Known error codes are listed in [docs/ERRORS.md](../../docs/ERRORS.md).

## Run

```bash
python examples/12_error_handling/12_error_handling.py
```
