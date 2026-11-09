"""Pendant-style example setup: tests only target local TCP simulators."""

import importlib.util
from pathlib import Path

import pytest

from test_sdk import devices  # noqa: F401


def setup_module_api():
    path = Path(__file__).parents[1] / "examples/common/initialization.py"
    assert path.exists(), "Example initialization has not been implemented"
    spec = importlib.util.spec_from_file_location("examples.common.example_initialization", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


SESSION_MOTION = ["Mode 0", "SelectRobot 1"]
SESSION_STATUS = ["Mode 0", "SelectRobot 1"]
INITIALIZATION = [
    "FreeMode -1",
    "Mspeed 20.0",
    "Profile 1 10.0 10.0 10.0 10.0 0.2 0.2 0.0 0",
    "Profile 2 5.0 5.0 10.0 10.0 0.2 0.2 0.0 0",
    "GripOpenPos 100.0",
    "GripClosePos 70.0",
    "Hp 1 30.0",
    "Attach 1",
]


def test_session_configuration_does_not_power_or_move(devices):  # noqa: F811
    api = setup_module_api()
    from pf400 import PF400

    motion, status = devices(), devices()
    with PF400("127.0.0.1", port=motion.port, status_port=status.port) as robot:
        api.configure_session(robot, robot_id=1)
    assert motion.received == SESSION_MOTION
    assert status.received == SESSION_STATUS


@pytest.mark.parametrize("open_gripper", [False, True])
def test_all_initialization_steps_are_transmitted(devices, open_gripper):  # noqa: F811
    api = setup_module_api()
    from pf400 import PF400

    motion, status = devices(), devices()
    with PF400("127.0.0.1", port=motion.port, status_port=status.port) as robot:
        api.configure_session(robot, robot_id=1)
        api.initialize_robot(robot, open_gripper=open_gripper)
    assert motion.received == SESSION_MOTION + INITIALIZATION + (["Gripper 1"] if open_gripper else [])
    assert status.received == SESSION_STATUS


@pytest.mark.parametrize("initial_homed", [False, True])
def test_home_runs_only_if_needed_and_completion_is_checked(devices, initial_homed):  # noqa: F811
    api = setup_module_api()
    from pf400 import PF400

    homed = initial_homed

    def motion_reply(command):
        nonlocal homed
        if command == "Home":
            homed = True
        return b"0\r\n"

    motion = devices(motion_reply)
    status = devices(lambda command: b"0 1\r\n" if homed else b"0 0\r\n")
    with PF400("127.0.0.1", port=motion.port, status_port=status.port) as robot:
        api.home_if_needed(robot)
    assert motion.received == ([] if initial_homed else ["Home"])
    assert status.received == (["Pd 2800"] if initial_homed else ["Pd 2800", "Pd 2800"])


def test_failed_initialization_does_not_continue_to_attach_or_gripper(devices):  # noqa: F811
    api = setup_module_api()
    from pf400 import PF400, DeviceError

    motion = devices(lambda command: b"-1046\r\n" if command.startswith("Hp ") else b"0\r\n")
    status = devices()
    with PF400("127.0.0.1", port=motion.port, status_port=status.port) as robot:
        with pytest.raises(DeviceError):
            api.initialize_robot(robot)
    assert motion.received == INITIALIZATION[:-1]
    assert "Attach 1" not in motion.received and "Gripper 1" not in motion.received


def test_home_must_be_confirmed_before_further_motion(devices):  # noqa: F811
    api = setup_module_api()
    from pf400 import PF400

    motion, status = devices(), devices(lambda command: b"0 0\r\n")
    with PF400("127.0.0.1", port=motion.port, status_port=status.port) as robot:
        with pytest.raises(RuntimeError):
            api.home_if_needed(robot)
    assert motion.received == ["Home"]
