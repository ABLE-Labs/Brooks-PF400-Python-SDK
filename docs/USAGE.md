# Usage guide

[한국어](USAGE.ko.md) · [Back to README](../README.md)

- [Connecting](#connecting)
- [Calling commands](#calling-commands)
- [Status channel and stopping](#status-channel-and-stopping)
- [Responses and errors](#responses-and-errors)
- [Asynchronous usage](#asynchronous-usage)
- [Response mode](#response-mode)
- [Command coverage](#command-coverage)

## Connecting

```python
from pf400 import PF400

with PF400("192.168.0.1", timeout=5) as robot:
    print(robot.version().data)
```

Connecting only opens two TCP sockets (motion port `10100`, status port `10000` by default).
It does not send power, mode, homing, gripper or motion commands.
`connected` reflects the local socket state only; it does not indicate that the robot is ready.

## Calling commands

Methods keep the meaning and argument order of the firmware commands.
Joint and Cartesian coordinates are passed as lists or tuples.
Every method accepts `channel="motion" | "status"` and `timeout=<seconds>`.

```python
# The calls below move real hardware when executed.
# robot.hp(1, wait=10)
# robot.attach(1)
# robot.home(timeout=120)
# robot.move_j(profile_index=1, joints=target_joints)
# robot.wait_for_eom(timeout=60)
# robot.gripper(1)  # firmware-defined: 1 = open, 2 = close
```

A motion command's reply does not necessarily mean the motion has finished. Call `wait_for_eom()` explicitly when needed.

| Command | Note |
|---|---|
| `home_all()` | Affects all robots. |
| `move_extra_axis()` | Schedules an extra-axis target for the next Cartesian move; does not move immediately. |
| `release_plate()` | The third argument is `in_range`, not a profile index. |
| `payload()` | Takes a percentage, not a mass. |

## Status channel and stopping

The default channel is `motion`, except `reset()`, which defaults to `status`.
At firmware start-up the status channel has robot `0` selected, so select the target robot explicitly before
per-robot queries or stopping.

```python
with PF400("192.168.0.1") as robot:
    robot.select_robot(1, channel="status")
    print(robot.state(channel="status").as_ints())
    # robot.halt(channel="status")  # sent independently of a motion channel that is waiting
```

- Calling `halt()` on the default motion channel may wait until the previous command replies.
- `Halt` is a rapid deceleration command and keeps power on. **It is not a substitute for a hardware emergency stop.**
- `Reset` restarts a robot thread. The firmware accepts it only when the status channel has robot `0` selected;
  call `select_robot(0, channel="status")` first if another robot was selected.

## Responses and errors

```python
from pf400 import CommandTimeout, DeviceError

try:
    response = robot.where_j()
    print(response.raw)          # raw reply, e.g. "0 10.0 20.0 ..."
    print(response.code)         # status code (0 on success in Normal mode)
    print(response.values)       # fields after the status code: tuple[str, ...]
    print(response.as_floats())  # all fields converted to float
except DeviceError as exc:
    print(exc.code, exc.description)  # description for known codes
    print(exc.hint)                   # suggested checks (empty if none)
    print(exc.raw)                    # original controller reply
except CommandTimeout as exc:
    print(exc.command, exc.may_have_executed)
    # Check the robot state and actual position before deciding how to recover.
```

- `0 -1` is a successful reply; the `-1` data field is kept.
- Responses are not forced to `bool`. For example, `IsFullyClosed` can return a bit mask on dual grippers.
- The meaning of each returned field is documented in the [command reference](API.md).

### Timeouts and recovery

- A single deadline covers channel lock wait, sending and receiving.
  If sending had started, `may_have_executed` is `True`.
- On a timeout, connection loss or malformed reply, the affected connection is closed so that a late reply cannot
  be mixed with the next command.
- The SDK does not retry, reconnect or resend. Check the robot before calling `connect()` again.
- Disconnecting or raising a Python exception does not stop physical motion.

### Error descriptions

Known controller / TCS error codes are annotated with a description and a hint (see [ERRORS.md](ERRORS.md)).
This is not the full manufacturer error list; unknown codes and the raw reply are always passed through.
Descriptions and hints are currently written in Korean.

## Asynchronous usage

```python
from pf400 import AsyncPF400

async def read_position():
    async with AsyncPF400("192.168.0.1") as robot:
        return (await robot.where_j()).as_floats()
```

- The async client runs the blocking I/O outside the event loop using `asyncio.to_thread`.
- Cancelling a task does not stop the robot. Cancellation is delivered after the in-flight I/O ends within its deadline.
- Commands on the same channel are serialized; the motion and status channels can be used independently.
- The firmware handles only one TCP connection per port. Do not connect multiple clients to the same robot port.

## Response mode

Normal mode (the start-up default) is recommended. `mode(1)` switches to Telnet mode and `mode(0)` back to Normal.

- The mode is shared by all server channels, so the SDK locks both channels while switching.
  If another client changes the mode, reconnect.
- When connecting to a server that is already in Telnet mode, pass `telnet_mode=True` to the constructor.
- Telnet replies are human-readable, so `Response.code` may be `None`. The SDK does not guess success for replies
  without a numeric code.
- If communication fails during a mode switch, both connections are closed. Create a new instance with
  `telnet_mode` matching the server's current mode.

## Command coverage

- 82 of the 90 commands declared by the firmware are provided as methods; the 8 vision commands are excluded:
  `Vprocess`, `VresultLoc`, `VresultInfo`, `VresultInspect`, `VToolProperty`, `VresultInfoString`,
  `StereoParam`, `StereoLocate`.
- Built-in plate and pallet commands such as `PickPlate`, `PlacePlate` and `TeachPlate` are included.
- `execute()` only accepts registered non-vision commands. There is no pass-through API for arbitrary commands.
- `Custom` is marked in the reference as a sample command shipped with the firmware.
- The SDK does not include application-level sequences, its own kinematics, a teach pendant or site-specific
  coordinate files.

Firmware caveats:

- `MoveToSafe` / `ChangeConfig` commands are documented in the firmware as not checking for collisions inside the
  workspace.
- `PickPlate` / `PlacePlate` are annotated `BES NOT UPDATED` in the firmware source; verify them on your configuration.
