# 14 · Free mode

[한국어](README.ko.md) · [Examples guide](../README.md)

Puts selected axes into free mode so they can be moved by hand, and restores all axes afterwards.

> [!WARNING]
> Use free mode only while the robot is stopped. Free mode stays on after the script ends, even after an error.
> Run `14_axes_restore.py` to end it.

## Files

| File | Description | Robot action |
|---|---|---|
| [14_axes_free.py](14_axes_free.py) | Initializes the robot and calls `free_mode(axis)` for each axis in `AXES` | Power on, frees selected axes |
| [14_axes_restore.py](14_axes_restore.py) | Ends free mode on all axes (`free_mode(-1)`) | Restores all axes |

## Settings

`14_axes_free.py`

| Variable | Default | Description |
|---|---|---|
| `AXES` | `[1, 2, 3, 4]` | Axis numbers to free (1–12, no duplicates, not more than the robot's axis count) |

`14_axes_restore.py` has connection settings only. It restores all axes regardless of `AXES`.

## What it does

- **Free:** checks `AXES` against the robot's axis count, runs the shared initialization without Home
  (see [common](../common/)) and frees only the selected axes.
- **Restore:** ends free mode on all axes. No power on, Home or gripper initialization.

## Notes

- Free mode is not the same as turning off servo power or releasing a brake.
- Typical use with [13](../13_teaching_positions/): free → move by hand → 13 save → restore → 13 move.

## Run

```bash
python examples/14_free_mode/14_axes_free.py
python examples/14_free_mode/14_axes_restore.py
```
