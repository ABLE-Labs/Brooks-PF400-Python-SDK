# Async · Read status

[한국어](README.ko.md) · [Examples guide](../README.md)

Uses `AsyncPF400` with `asyncio` to read the version and joint positions. Nothing is initialized or moved.

## Files

| File | Description | Robot action |
|---|---|---|
| [read_status.py](read_status.py) | Sets Normal mode and selects the robot on both channels, then prints `version()` and `where_j()` | Read only |

## Settings

Connection settings only (`HOST`, `ROBOT_ID`, `PORT`, `STATUS_PORT`, `TIMEOUT`).

## Notes

- `AsyncPF400` has the same methods and arguments as `PF400`; each call is awaited.
- Cancelling a task does not stop the robot. See the [usage guide](../../docs/USAGE.md#asynchronous-usage).

## Run

```bash
python examples/async/read_status.py
```
