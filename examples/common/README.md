# common · Shared example modules

[한국어](README.ko.md) · [Examples guide](../README.md)

Helper modules used by the example scripts. Importing them does not connect to the robot, write files or move anything.
Import them as `examples.common.<module>`; open the SDK root folder in your IDE so the `examples` package is found.

## Files

| File | Contents |
|---|---|
| [initialization.py](initialization.py) | Input checks, session setup and robot initialization |
| [motion_profiles.py](motion_profiles.py) | Read, validate, save and apply [config/motion_profiles.json](../config/motion_profiles.json) |
| [teaching_positions.py](teaching_positions.py) | Read, validate and save [config/teaching_positions.json](../config/teaching_positions.json) |

## initialization.py

| Function | Description |
|---|---|
| `configure_session(robot, robot_id=1)` | Sets Normal mode (`mode(0)`) and selects the robot on both channels. No power or motion |
| `initialize_robot(robot, open_gripper=False, home=False, profiles=None)` | Prepares the robot for control (sequence below) |
| `home_if_needed(robot)` | Runs `home()` only if `pd(2800)` reports not homed, then checks again |
| `validate_number()` / `validate_values()` / `validate_profile()` | Input checks used before connecting |

`initialize_robot()` sequence:

```text
free_mode(-1)                       end free mode
mspeed / profile                    from config/motion_profiles.json
grip_open_pos / grip_close_pos      GRIPPER_OPEN / GRIPPER_CLOSE
hp(1, wait=POWER_WAIT)              power on, INITIALIZE_TIMEOUT
attach(1)
home_if_needed()                    only when home=True
gripper(1)                          only when open_gripper=True
```

Errors are passed through and nothing is retried. This function can change the robot's posture and what it holds,
so it is not called by the read, save, stop, power-off or restore examples.

| Constant | Value | Description |
|---|---|---|
| `GRIPPER_OPEN` / `GRIPPER_CLOSE` | `100.0` / `70.0` | Gripper positions set during initialization [mm] |
| `POWER_WAIT` | `30.0` | Power-on wait passed to `hp()` [s] |
| `INITIALIZE_TIMEOUT` | `60.0` | Communication timeout for power on [s] (must be greater than `POWER_WAIT`) |
| `HOME_TIMEOUT` | `120.0` | Timeout for `home()` [s] |

## motion_profiles.py

| Name | Description |
|---|---|
| `PROFILE_FILE` | Absolute path to `config/motion_profiles.json`, independent of the working directory |
| `load_profiles(path)` | Reads and validates the file. A missing or invalid file raises an error |
| `save_profiles(path, data)` | Validates and replaces the file atomically |
| `apply_profiles(robot, data)` | Sends the master speed and every profile. No power, Home or gripper action |
| `validate_profiles()` / `profile_values()` | Validation and conversion to the 8-value argument list |

## teaching_positions.py

| Name | Description |
|---|---|
| `JSON_FILE` | Absolute path to `config/teaching_positions.json` |
| `read_positions(path)` | Reads and validates the file. A missing file returns an empty list |
| `load_position(path, name)` | Returns the joints saved under `name` |
| `save_position(path, name, joints)` | Adds or updates `name`, keeps other entries and replaces the file atomically |
| `validate_joints()` / `validate_name()` | Input checks |
