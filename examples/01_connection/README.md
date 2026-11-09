# 01 · Connection and status

[한국어](README.ko.md) · [Examples guide](../README.md)

Connects to the robot and reads its version, state and current position. Nothing is initialized or moved.

## Files

| File | Description | Robot action |
|---|---|---|
| [01_connect_and_status.py](01_connect_and_status.py) | Prints the version, system state, motion state, joint positions and Cartesian pose | Read only |

## Settings

| Variable | Default | Description |
|---|---|---|
| `HOST` | `"192.168.0.1"` | Controller IP address or host name (example value) |
| `ROBOT_ID` | `1` | Target robot number |
| `PORT` / `STATUS_PORT` | `10100` / `10000` | Motion / status TCP ports |
| `TIMEOUT` | `10.0` | SDK communication timeout [s] |

Every example file has these connection settings at the top.

## What it does

1. Opens the motion and status connections.
2. Sets Normal mode and selects `ROBOT_ID` on both channels (`configure_session()`).
3. Calls `version()`, `sys_state()`, `state()`, `where_j()` and `where_c()` and prints the results.

## Run

Install the SDK, open the SDK root folder in your IDE and run the file, or from the SDK root:

```bash
python examples/01_connection/01_connect_and_status.py
```
