# 06 · Single-axis motion

[한국어](README.ko.md) · [Examples guide](../README.md)

Moves one axis to an absolute target position and waits for the motion to finish.

> [!WARNING]
> This example moves the robot. Clear the area before running it.

## Files

| File | Description | Robot action |
|---|---|---|
| [06_single_axis_motion.py](06_single_axis_motion.py) | Moves `AXIS` to `TARGET_POSITION` with `move_one_axis()` and waits with `wait_for_eom()` | Power on, Home if needed, moves |

## Settings

| Variable | Default | Description |
|---|---|---|
| `AXIS` | `1` | Axis number (1–12, and not more than the robot's axis count) |
| `TARGET_POSITION` | `None` | Absolute target, not a relative distance. Units follow the axis definition. The file will not run until you set it |
| `PROFILE_INDEX` | `1` | Profile slot. Must exist in [config/motion_profiles.json](../config/motion_profiles.json) |
| `MOTION_TIMEOUT` | `120.0` | Time to wait for the end of motion [s] |

## What it does

1. Validates `AXIS`, `TARGET_POSITION` and the profile file before connecting.
2. Sets up the session and checks `AXIS` against the robot's axis count.
3. Runs the shared initialization with Home if needed (see [common](../common/)).
4. Prints the joint positions, sends `move_one_axis(AXIS, TARGET_POSITION, PROFILE_INDEX)`, waits and prints them again.

## Notes

- A timeout only stops waiting. It does not stop the robot.

## Run

```bash
python examples/06_single_axis/06_single_axis_motion.py
```
