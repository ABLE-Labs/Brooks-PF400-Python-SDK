# 10 · Coordinate conversion

[한국어](README.ko.md) · [Examples guide](../README.md)

Converts between joint and Cartesian coordinates on the controller. The robot does not move.

## Files

| File | Description | Robot action |
|---|---|---|
| [10_joint_to_cartesian.py](10_joint_to_cartesian.py) | Joint → Cartesian (`convert_joint_to_cartesian()`) | Read only |
| [10_cartesian_to_joint.py](10_cartesian_to_joint.py) | Cartesian → joint (`convert_cartesian_to_joint()`) | Read only |

## Settings

| Variable | Default | Used in | Description |
|---|---|---|---|
| `JOINTS` | `None` | joint → Cartesian | Joint values in axis order (linear axes mm, rotary axes deg). Must match the axis count |
| `POSE` | `None` | Cartesian → joint | `[X, Y, Z, yaw, pitch, roll]` — position in mm, rotation in deg |
| `CONFIG` | `None` | Cartesian → joint | Arm configuration. `None` uses the firmware default `0`; it does not pick the current posture |

Both files will not run until you set `JOINTS` or `POSE`.

## Output

- Joint → Cartesian: `[X, Y, Z, yaw, pitch, roll, config]`
- Cartesian → joint: joint values in axis order

## Run

```bash
python examples/10_coordinate_conversion/10_joint_to_cartesian.py
python examples/10_coordinate_conversion/10_cartesian_to_joint.py
```
