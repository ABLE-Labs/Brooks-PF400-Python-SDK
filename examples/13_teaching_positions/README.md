# 13 · PC teaching positions

[한국어](README.ko.md) · [Examples guide](../README.md)

Saves named joint positions to a JSON file on the PC, lists them and moves to one of them.
Positions are stored in [config/teaching_positions.json](../config/teaching_positions.json).

## Files

| File | Description | Robot action |
|---|---|---|
| [13_positions_list.py](13_positions_list.py) | Prints the saved positions | None (no connection) |
| [13_position_save.py](13_position_save.py) | Saves the current joint position under `POSITION_NAME` | Read only (writes a PC file) |
| [13_position_move.py](13_position_move.py) | Moves to the saved position with `move_j()` and waits | Power on, Home if needed, moves |

## Settings

| Variable | Default | Used in | Description |
|---|---|---|---|
| `POSITION_NAME` | `"position_a"` (save) / `None` (move) | save, move | Position name. Saving an existing name updates it. The move file will not run until you set it |
| `PROFILE_INDEX` | `1` | move | Profile slot. Must exist in [config/motion_profiles.json](../config/motion_profiles.json) |
| `MOTION_TIMEOUT` | `120.0` | move | Time to wait for the end of motion [s] |

## What it does

- **Save:** reads the current joint position and writes it to the JSON file. Other positions and metadata are kept.
  A corrupted JSON file is reported and not overwritten.
- **Move:** checks that the saved position has the same number of axes as the robot, runs the shared
  initialization with Home if needed (see [common](../common/)), calls `move_j()` and waits.

> [!WARNING]
> The bundled JSON file has no positions; save one with `13_position_save.py` first.
> Do not reuse positions saved on a robot with a different axis configuration.

## Notes

- The gripper is not opened automatically. If the saved position includes the gripper axis, that axis moves too.
- With [14](../14_free_mode/) you can guide the robot by hand: free → move by hand → save → restore → move.

## Run

```bash
python examples/13_teaching_positions/13_positions_list.py
python examples/13_teaching_positions/13_position_save.py
python examples/13_teaching_positions/13_position_move.py
```
