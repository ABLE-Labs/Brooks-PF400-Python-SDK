# 07 · Gripper

[한국어](README.ko.md) · [Examples guide](../README.md)

Reads and sets the servo gripper's open / close positions, and opens or closes the gripper.

## Files

| File | Description | Robot action |
|---|---|---|
| [07_gripper_read.py](07_gripper_read.py) | Reads the open / close positions | Read only |
| [07_gripper_settings.py](07_gripper_settings.py) | Sets the open / close positions. Does not open or close | Settings only |
| [07_gripper_open.py](07_gripper_open.py) | Initializes, applies the positions and opens the gripper (`gripper(1)`) | Power on, Home if needed, opens gripper |
| [07_gripper_close.py](07_gripper_close.py) | Initializes, applies the positions and closes the gripper (`gripper(2)`) | Power on, Home if needed, closes gripper |

## Settings

`07_gripper_settings.py`, `07_gripper_open.py`, `07_gripper_close.py`

| Variable | Default | Description |
|---|---|---|
| `OPEN_POSITION` | `100.0` | Open position [mm] |
| `CLOSE_POSITION` | `80.0` | Close position [mm] |

Check the valid range on your gripper before changing these values.

## What it does

`07_gripper_open.py` / `07_gripper_close.py`

1. Validates the profile file and the positions before connecting.
2. Runs the shared initialization with Home if needed (see [common](../common/)).
   This first sets the positions from `common/initialization.py` (`100.0` / `70.0` mm).
3. Applies `OPEN_POSITION` / `CLOSE_POSITION` from the file, then opens or closes the gripper.

## Notes

- Home may change the robot's current posture. If the robot is holding an object, check before running open / close.
- Gripper positions are not stored in the motion profile JSON.

## Run

```bash
python examples/07_gripper/07_gripper_read.py
python examples/07_gripper/07_gripper_settings.py
python examples/07_gripper/07_gripper_open.py
python examples/07_gripper/07_gripper_close.py
```
