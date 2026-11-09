# 09 · Controller teaching

[한국어](README.ko.md) · [Examples guide](../README.md)

Teaches positions into the controller's location slots, saves and loads them as a GPO file on the controller,
and moves to a stored slot.

## Files

| File | Description | Robot action |
|---|---|---|
| [09_location_show.py](09_location_show.py) | Reads one location slot (`loc()`) | Read only |
| [09_teach_joint.py](09_teach_joint.py) | Stores the current joint position in a slot (`here_j()`) | Updates controller memory |
| [09_teach_cartesian.py](09_teach_cartesian.py) | Stores the current Cartesian position in a slot (`here_c()`) | Updates controller memory |
| [09_locations_store.py](09_locations_store.py) | Saves the controller's locations and profiles to a GPO file (`store_file()`) | Writes a controller file |
| [09_locations_load.py](09_locations_load.py) | Loads locations and profiles from a GPO file into memory (`load_file()`) | Overwrites controller memory |
| [09_locations_move.py](09_locations_move.py) | Loads the GPO file and moves to a slot (`move()`) | Power on, Home if needed, moves |

## Settings

| Variable | Default | Used in | Description |
|---|---|---|---|
| `LOCATION_INDEX` | `1` (show, teach) / `None` (move) | show, teach, move | Location slot (1 or more). The move file will not run until you set it |
| `SAVE_FILE` / `LOAD_FILE` | `"Tcs_example.gpo"` | store / load, move | File name on the controller, not a PC path |
| `PROFILE_INDEX` | `1` | move | Profile number loaded from the GPO file |
| `MSPEED` | `20.0` | move | Master speed [%], greater than 0 and up to 100 |
| `MOTION_TIMEOUT` | `120.0` | move | Time to wait for the end of motion [s] |

## Workflow

1. Move the robot to a position and run **teach** (joint or Cartesian). Check it with **show**.
2. Run **store** to save the slots to the GPO file on the controller.
3. After a controller reboot, run **load** to restore them. Nothing runs automatically at boot.
4. Run **move** to go to a slot. Set `LOCATION_INDEX` to a slot whose position and path you have checked.

`09_locations_move.py` loads the GPO file, prints the target slot and profile, ends free mode, sets `MSPEED`,
powers on, attaches, homes if needed, then calls `move(LOCATION_INDEX, PROFILE_INDEX)` and waits.
It uses the profile from the GPO file and does not apply the PC profile JSON. It does not open or close the gripper.

> [!WARNING]
> `09_locations_move.py` moves the robot. The path is not checked for collisions.

## Notes

- Teach and load overwrite existing values in controller memory. Teach does not run Home or move the robot.
- The GPO file lives on the controller and is separate from the PC JSON files in [config](../config/).

## Run

```bash
python examples/09_controller_teaching/09_teach_joint.py
python examples/09_controller_teaching/09_location_show.py
python examples/09_controller_teaching/09_locations_store.py
python examples/09_controller_teaching/09_locations_load.py
python examples/09_controller_teaching/09_locations_move.py
```
