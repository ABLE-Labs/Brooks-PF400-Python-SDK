# 03 · Motion profiles

[한국어](README.ko.md) · [Examples guide](../README.md)

Saves the master speed and motion profiles to a JSON file on the PC, applies them to the robot and reads them back.
[config/motion_profiles.json](../config/motion_profiles.json) is the single source for these values.

## Files

| File | Description | Robot action |
|---|---|---|
| [03_profile_save.py](03_profile_save.py) | Saves the values at the top of the file to the JSON file | None (no connection) |
| [03_profile_apply.py](03_profile_apply.py) | Applies the master speed and every profile in the JSON file | Settings only |
| [03_profile_read.py](03_profile_read.py) | Reads the master speed and one profile from the robot | Read only |

## Settings

`03_profile_save.py`

| Variable | Default | Description |
|---|---|---|
| `PROFILE_INDEX` | `1` | Profile slot (1–20) |
| `MASTER_SPEED` | `20.0` | System-wide speed scale [%] |
| `SPEED` / `SPEED2` | `10.0` / `10.0` | Maximum speed / secondary speed for some axes in Cartesian moves [%] |
| `ACCEL` / `DECEL` | `10.0` / `10.0` | Maximum acceleration / deceleration [%] |
| `ACC_RAMP` / `DEC_RAMP` | `0.2` / `0.2` | S-curve ramp time [s] (not the total acceleration time) |
| `IN_RANGE` | `0.0` | `< 0` blend, `0` stop without position check, `> 0` position check |
| `STRAIGHT` | `0` | `0` joint interpolation, `1` Cartesian straight line |

`03_profile_read.py`: `PROFILE_INDEX` (default `1`).

Units, meanings and manufacturer references are explained in section 03 of the [examples guide](../README.md).

## Workflow

1. **Save** — updates the selected slot and the master speed; other slots are kept.
   A missing file is created. A corrupted file is reported and not overwritten.
2. **Apply** — sends the master speed and all profiles. No power on, Attach, Home or gripper action.
3. **Read** — prints `[index, Speed, Speed2, Accel, Decel, AccRamp, DecRamp, InRange, Straight]` to compare with the file.

Saving and applying are separate. Changing values on the robot does not update the JSON file.
Startup ([02](../02_power/)) and the motion examples re-apply the JSON values to the robot.

## Run

```bash
python examples/03_profiles/03_profile_save.py
python examples/03_profiles/03_profile_apply.py
python examples/03_profiles/03_profile_read.py
```
