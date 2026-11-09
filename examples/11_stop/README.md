# 11 · Stop

[한국어](README.ko.md) · [Examples guide](../README.md)

Sends `halt()` on the status channel so that it is not blocked by a motion command waiting on the motion channel.

> [!WARNING]
> `Halt` is a rapid deceleration and keeps power on. **It is not a substitute for a hardware emergency stop.**

## Files

| File | Description | Robot action |
|---|---|---|
| [11_stop.py](11_stop.py) | `stop_robot(robot, robot_id)` selects the robot on the status channel and sends `halt()`; `main()` connects, halts and prints the motion state | Stops |

## Using it in your application

Call `stop_robot()` with the SDK object your application already uses:

```python
stop_robot(robot, robot_id=1)
```

The firmware accepts one TCP connection per port, so this file is not a tool for stopping the robot from a
separate process while another application holds the connection.

## Notes

- No power on, gripper or Home initialization is done before stopping.
- Disconnecting, Ctrl+C, exceptions and timeouts do not stop the robot.

## Run

```bash
python examples/11_stop/11_stop.py
```
