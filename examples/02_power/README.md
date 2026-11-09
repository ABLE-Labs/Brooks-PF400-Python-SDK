# 02 · Power (startup and shutdown)

[한국어](README.ko.md) · [Examples guide](../README.md)

Prepares the robot for use and shuts it down. Each SDK call is written out in the file so you can follow the sequence.

> [!WARNING]
> Startup powers on the robot and may run Home. Check the area around the robot before running it.

## Files

| File | Description | Robot action |
|---|---|---|
| [02_startup.py](02_startup.py) | Session setup → profiles → power on → Attach → Home if needed → open gripper | Power on, Home if needed, opens gripper |
| [02_shutdown.py](02_shutdown.py) | Session setup → Halt → free mode off → Detach → power off | Stops, power off |

## Settings

Connection settings only (`HOST`, `ROBOT_ID`, `PORT`, `STATUS_PORT`). `TIMEOUT` is `30.0` s in both files.

## What it does

`02_startup.py`

1. Reads and validates [config/motion_profiles.json](../config/motion_profiles.json) before connecting.
2. Sets Normal mode and selects the robot on both channels, then ends free mode (`free_mode(-1)`).
3. Applies the master speed and every profile from the JSON file.
4. Sets the gripper open / close positions to `100.0` / `70.0` mm (values in the file).
5. Powers on (`hp(1, wait=30)`, 60 s timeout) and attaches (`attach(1)`).
6. Runs `home()` only if the homed flag (`pd(2800)`) is `0`, then checks it again.
7. Opens the gripper (`gripper(1)`) and closes the TCP connection. Power stays on.

`02_shutdown.py`

1. Sets Normal mode and selects the robot on both channels.
2. Sends `halt()` on the status channel and ends free mode.
3. Detaches (`attach(0)`), powers off (`hp(0)`) and closes the connection.

Shutdown does not initialize or home the robot first.

## Notes

- After a controller reboot, profiles must be applied again. Startup re-applies them from the JSON file.
- To continue controlling the robot after startup, add your SDK calls where the file comments indicate.

## Run

```bash
python examples/02_power/02_startup.py
python examples/02_power/02_shutdown.py
```
