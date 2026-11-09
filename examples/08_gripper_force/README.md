# 08 · Force-limited grasp

[한국어](README.ko.md) · [Examples guide](../README.md)

Grasps an object with a force limit and releases it.

> [!WARNING]
> These examples move the gripper. The actual grip force can vary with friction, springs and other factors.

## Files

| File | Description | Robot action |
|---|---|---|
| [08_grasp_plate.py](08_grasp_plate.py) | Grasps with `grasp_plate()` and stops with an error unless the grasp is confirmed | Power on, Home if needed, grasps |
| [08_release_plate.py](08_release_plate.py) | Releases with `release_plate()` and waits with `wait_for_eom()` | Power on, releases (no Home) |

## Settings

`08_grasp_plate.py`

| Variable | Default | Description |
|---|---|---|
| `WIDTH` | `85.0` | Object width [mm]. Enter it within about 1 mm |
| `SPEED` | `20.0` | Gripper speed [%] |
| `FORCE` | `5.0` | Grip force [N]. Positive closes to grip, negative opens to grip |

`08_release_plate.py`

| Variable | Default | Description |
|---|---|---|
| `WIDTH` | `85.0` | Release target width [mm] — a width at which the object is free |
| `SPEED` | `20.0` | Speed [%] |
| `IN_RANGE` | `0.0` | Must be `0` or more (no blending in a standalone release) |
| `MOTION_TIMEOUT` | `120.0` | Time to wait for the end of motion [s] |

## What it does

- **Grasp:** initializes with Home if needed (see [common](../common/)), then calls `grasp_plate(WIDTH, SPEED, FORCE)`.
  Only a reply of `-1` counts as success. `0` or any other data raises `RuntimeError`.
- **Release:** initializes without Home or opening the gripper, calls `release_plate(WIDTH, SPEED, in_range=IN_RANGE)`
  and waits for the end of motion. `IN_RANGE=0` does not guarantee that the position error has settled.

## Run

```bash
python examples/08_gripper_force/08_grasp_plate.py
python examples/08_gripper_force/08_release_plate.py
```
