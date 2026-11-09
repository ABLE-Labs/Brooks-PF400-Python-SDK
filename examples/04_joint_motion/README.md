# 04 · Joint motion

[한국어](README.ko.md) · [Examples guide](../README.md)

Moves the robot to a joint target and waits for the motion to finish.

> [!WARNING]
> This example moves the robot. Enter a target you have checked on your robot and clear the area before running it.

## Files

| File | Description | Robot action |
|---|---|---|
| [04_joint_motion.py](04_joint_motion.py) | Moves to `TARGET_JOINTS` with `move_j()` and waits with `wait_for_eom()` | Power on, Home if needed, moves |

## Settings

| Variable | Default | Description |
|---|---|---|
| `TARGET_JOINTS` | `None` | Joint target as a list. Must match the robot's axis count and order. The file will not run until you set it |
| `PROFILE_INDEX` | `1` | Profile slot. Must exist in [config/motion_profiles.json](../config/motion_profiles.json) |
| `MOTION_TIMEOUT` | `120.0` | Time to wait for the end of motion [s] |

## What it does

1. Validates the target and the profile file before connecting.
2. Sets up the session and checks that `TARGET_JOINTS` matches the robot's axis count.
3. Runs the shared initialization with Home if needed (`initialize_robot(..., home=True)`, see [common](../common/)).
4. Prints the joint positions, sends `move_j(PROFILE_INDEX, TARGET_JOINTS)`, waits for the end of motion and prints them again.

## Notes

- The gripper is not opened automatically. If the target includes the gripper axis, the gripper moves to that value.
- A timeout only stops waiting. It does not stop the robot.

## Run

```bash
python examples/04_joint_motion/04_joint_motion.py
```
