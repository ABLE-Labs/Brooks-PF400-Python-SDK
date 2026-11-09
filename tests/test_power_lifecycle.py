"""Simple startup/shutdown examples are exercised only on loopback TCP."""

from pathlib import Path
import runpy

import pytest

from test_sdk import devices  # noqa: F401

ROOT = Path(__file__).parents[1]


def run_script(name, settings):
    path = ROOT / "examples" / name
    assert path.exists(), f"Missing lifecycle example: {name}"
    main = runpy.run_path(str(path), run_name="lifecycle_example")["main"]
    main.__globals__.update(settings)
    main()


@pytest.mark.parametrize("already_homed", [False, True])
def test_startup_commands_are_explicit_and_home_precedes_gripper(devices, already_homed):  # noqa: F811
    homed = already_homed

    def reply(command):
        nonlocal homed
        if command == "Home":
            homed = True
        return b"0\r\n"

    motion = devices(reply)
    status = devices(lambda command: b"0 1\r\n" if command == "Pd 2800" and homed else b"0 0\r\n")
    run_script("02_power/02_startup.py", {"HOST": "127.0.0.1", "PORT": motion.port, "STATUS_PORT": status.port})
    expected = [
        "Mode 0",
        "SelectRobot 1",
        "FreeMode -1",
        "Mspeed 20.0",
        "Profile 1 10.0 10.0 10.0 10.0 0.2 0.2 0.0 0",
        "Profile 2 5.0 5.0 10.0 10.0 0.2 0.2 0.0 0",
        "GripOpenPos 100.0",
        "GripClosePos 70.0",
        "Hp 1 30.0",
        "Attach 1",
    ]
    assert motion.received == expected + ([] if already_homed else ["Home"]) + ["Gripper 1"]
    assert status.received == ["Mode 0", "SelectRobot 1", "Pd 2800"] + ([] if already_homed else ["Pd 2800"])


def test_shutdown_stops_releases_and_powers_off_without_startup(devices):  # noqa: F811
    motion, status = devices(), devices()
    run_script("02_power/02_shutdown.py", {"HOST": "127.0.0.1", "PORT": motion.port, "STATUS_PORT": status.port})
    assert motion.received == ["Mode 0", "SelectRobot 1", "FreeMode -1", "Attach 0", "Hp 0"]
    assert status.received == ["Mode 0", "SelectRobot 1", "Halt"]


def test_startup_stops_after_power_error(devices):  # noqa: F811
    from pf400 import DeviceError

    motion = devices(lambda command: b"-1046\r\n" if command.startswith("Hp ") else b"0\r\n")
    status = devices()
    with pytest.raises(DeviceError):
        run_script("02_power/02_startup.py", {"HOST": "127.0.0.1", "PORT": motion.port, "STATUS_PORT": status.port})
    assert motion.received[-1] == "Hp 1 30.0"
    assert "Attach 1" not in motion.received and "Gripper 1" not in motion.received


def test_startup_does_not_open_gripper_when_home_is_not_confirmed(devices):  # noqa: F811
    motion = devices()
    status = devices(lambda command: b"0 0\r\n")
    with pytest.raises(RuntimeError):
        run_script("02_power/02_startup.py", {"HOST": "127.0.0.1", "PORT": motion.port, "STATUS_PORT": status.port})
    assert motion.received[-1] == "Home"
    assert "Gripper 1" not in motion.received
