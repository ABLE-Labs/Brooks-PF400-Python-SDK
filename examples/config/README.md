# config · Example settings files

[한국어](README.ko.md) · [Examples guide](../README.md)

JSON files on the PC that the examples read and write. They are separate from the controller's memory and GPO files.

## Files

| File | Contents | Read by | Written by |
|---|---|---|---|
| [motion_profiles.json](motion_profiles.json) | Master speed and motion profiles | [02](../02_power/) startup, [03](../03_profiles/) apply, motion examples | [03](../03_profiles/) save |
| [teaching_positions.json](teaching_positions.json) | Named joint positions | [13](../13_teaching_positions/) list, move | [13](../13_teaching_positions/) save |

## motion_profiles.json

```json
{
  "master_speed": 20.0,
  "profiles": {
    "1": {
      "speed": 10.0, "speed2": 10.0, "accel": 10.0, "decel": 10.0,
      "acc_ramp": 0.2, "dec_ramp": 0.2, "in_range": 0.0, "straight": 0
    }
  }
}
```

- `master_speed`: system-wide speed scale [%].
- `profiles`: keys are slot numbers `"1"` to `"20"`. Each profile needs all 8 fields.
  `straight` must be the integer `0` or `1`; every other field must be a finite number.
- The bundled file has profiles `1` and `2` (`speed` 10 and 5). All values are examples to be verified on your robot.

Field meanings and units are described in [03_profiles](../03_profiles/) and section 03 of the [examples guide](../README.md).

## teaching_positions.json

The bundled file has no positions. After saving with [13](../13_teaching_positions/), it looks like this:

```json
{
  "positions": {
    "position_a": { "joints": [100.0, 0.0, 90.0, 0.0, 80.0] }
  }
}
```

- `positions`: position names mapped to objects with a `joints` list (1–12 numbers in axis order).
  The numbers above only show the format.
- Extra fields in a position are kept when it is saved again.

## Notes

- You can edit the files by hand. Every load and save validates the whole file and rejects invalid values.
- A corrupted file is reported and not overwritten.
- The files are not designed for several programs writing at the same time.
- Changing values on the robot does not update these files.
