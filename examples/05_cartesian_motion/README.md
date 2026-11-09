# 05 · Cartesian motion

[한국어](README.ko.md) · [Examples guide](../README.md)

Moves the robot to a Cartesian target pose and waits for the motion to finish.

> [!WARNING]
> This example moves the robot. Reachability, posture and collisions are not checked.
> Enter a pose you have checked on your robot and clear the area before running it.

## Files

| File | Description | Robot action |
|---|---|---|
| [05_cartesian_motion.py](05_cartesian_motion.py) | Moves to `TARGET_POSE` with `move_c()` and waits with `wait_for_eom()` | Power on, Home if needed, moves |

## Settings

| Variable | Default | Description |
|---|---|---|
| `TARGET_POSE` | `None` | `[X, Y, Z, yaw, pitch, roll]` — position in mm, rotation in deg. The file will not run until you set it |
| `CONFIG` | `None` | Arm configuration (integer). `None` uses the firmware default |
| `PROFILE_INDEX` | `1` | Profile slot. Must exist in [config/motion_profiles.json](../config/motion_profiles.json) |
| `MOTION_TIMEOUT` | `120.0` | Time to wait for the end of motion [s] |

## What it does

1. Validates the pose, `CONFIG` and the profile file before connecting.
2. Sets up the session and runs the shared initialization with Home if needed (see [common](../common/)).
3. Prints the Cartesian pose, sends `move_c(PROFILE_INDEX, TARGET_POSE, config=CONFIG)`, waits and prints it again.

## Notes

- The path is set by the profile's `straight` field. Profiles 1 and 2 in the bundled JSON use `straight=0`
  (joint interpolation). For a straight-line path, save a profile with `straight=1` using [03](../03_profiles/).
- A timeout only stops waiting. It does not stop the robot.

## Run

```bash
python examples/05_cartesian_motion/05_cartesian_motion.py
```
