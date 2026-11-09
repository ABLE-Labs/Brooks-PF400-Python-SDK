"""Runnable operations use only loopback devices in these tests."""

import asyncio
import inspect
import runpy
import socket
from pathlib import Path

import pytest
from test_sdk import devices  # noqa: F401
from test_initialization import INITIALIZATION, SESSION_MOTION, SESSION_STATUS

EXAMPLES = Path(__file__).resolve().parents[1] / "examples"
SCRIPTS = sorted(path.relative_to(EXAMPLES).as_posix() for path in EXAMPLES.glob("[0-9]*/*.py")) + ["async/read_status.py"]


def load_example(name, settings=None):
    main = runpy.run_path(str(EXAMPLES / name), run_name="example")["main"]
    main.__globals__.update(settings or {})
    return main


def run_example(name, settings=None):
    main = load_example(name, settings)
    return asyncio.run(main()) if inspect.iscoroutinefunction(main) else main()


@pytest.mark.parametrize("name", SCRIPTS)
def test_import_does_not_connect(monkeypatch, name):
    def forbidden(*args, **kwargs):
        pytest.fail("Import must not connect")
    monkeypatch.setattr(socket, "create_connection", forbidden)
    assert not inspect.signature(load_example(name)).parameters


@pytest.mark.parametrize("name", [
    "04_joint_motion/04_joint_motion.py", "05_cartesian_motion/05_cartesian_motion.py", "06_single_axis/06_single_axis_motion.py",
    "10_coordinate_conversion/10_joint_to_cartesian.py", "10_coordinate_conversion/10_cartesian_to_joint.py",
    "09_controller_teaching/09_locations_move.py", "13_teaching_positions/13_position_move.py",
])
def test_unset_required_values_fail_before_connect(monkeypatch, name):
    def forbidden(*args, **kwargs):
        pytest.fail("Missing coordinates must fail before connecting")
    monkeypatch.setattr(socket, "create_connection", forbidden)
    with pytest.raises(ValueError):
        run_example(name)


@pytest.mark.parametrize("name,settings,tail", [
    ("04_joint_motion/04_joint_motion.py", {"TARGET_JOINTS": [1,2,3,4,5,6]},
     ["WhereJ", "MoveJ 1 1 2 3 4 5 6", "WaitForEom", "WhereJ"]),
    ("05_cartesian_motion/05_cartesian_motion.py", {"TARGET_POSE": [1,2,3,4,5,6]},
     ["WhereC", "MoveC 1 1 2 3 4 5 6", "WaitForEom", "WhereC"]),
    ("06_single_axis/06_single_axis_motion.py", {"AXIS":1, "TARGET_POSITION":10},
     ["WhereJ", "MoveOneAxis 1 10 1", "WaitForEom", "WhereJ"]),
])
def test_motion_without_gripper_open(devices, name, settings, tail):  # noqa: F811
    motion = devices(lambda cmd: b"0 1 2 3 4 5 6\r\n" if cmd == "WhereJ" else b"0\r\n")
    status = devices(lambda cmd: b"0 1\r\n" if cmd == "Pd 2800" else b"0\r\n")
    run_example(name, {**settings, "HOST":"127.0.0.1", "PORT":motion.port, "STATUS_PORT":status.port})
    assert motion.received == SESSION_MOTION + (["WhereJ"] if name[:2] in ("04","06") else []) + INITIALIZATION + tail
    assert status.received == SESSION_STATUS + ["Pd 2800"]
    assert "Gripper 1" not in motion.received


@pytest.mark.parametrize("name,settings,commands", [
    ("09_controller_teaching/09_location_show.py", {}, ["Loc 1"]),
    ("09_controller_teaching/09_teach_joint.py", {}, ["HereJ 1", "Loc 1"]),
    ("09_controller_teaching/09_teach_cartesian.py", {}, ["HereC 1", "Loc 1"]),
    ("09_controller_teaching/09_locations_store.py", {}, ["StoreFile Tcs_example.gpo"]),
    ("10_coordinate_conversion/10_joint_to_cartesian.py", {"JOINTS":[1,2,3,4,5,6]}, ["WhereJ", "ConvertJointToCartesian 1 2 3 4 5 6"]),
    ("10_coordinate_conversion/10_cartesian_to_joint.py", {"POSE":[1,2,3,4,5,6]}, ["ConvertCartesianToJoint 1 2 3 4 5 6"]),
    ("03_profiles/03_profile_read.py", {}, ["Mspeed", "Profile 1"]),
    ("07_gripper/07_gripper_settings.py", {}, ["GripOpenPos 100.0", "GripClosePos 80.0"]),
    ("12_error_handling/12_error_handling.py", {}, ["Nop", "WhereJ"]),
])
def test_non_motion_operations(devices, name, settings, commands):  # noqa: F811
    motion = devices(lambda cmd: b"0 1 2 3 4 5 6\r\n" if cmd == "WhereJ" else b"0\r\n")
    status = devices()
    run_example(name, {**settings,"HOST":"127.0.0.1","PORT":motion.port,"STATUS_PORT":status.port})
    assert motion.received == SESSION_MOTION + commands
    assert status.received == SESSION_STATUS


def test_stop_only_uses_selected_status_channel(devices):  # noqa: F811
    motion, status = devices(), devices()
    run_example("11_stop/11_stop.py", {"HOST":"127.0.0.1","PORT":motion.port,"STATUS_PORT":status.port})
    assert motion.received == []
    assert status.received == ["SelectRobot 1", "Halt", "State"]


def test_error_example_preserves_vendor_code(devices, capsys):  # noqa: F811
    motion, status = devices(lambda cmd: b"-99999 vendor error\r\n"), devices()
    assert run_example("12_error_handling/12_error_handling.py", {"HOST":"127.0.0.1","PORT":motion.port,"STATUS_PORT":status.port}) == 1
    assert "-99999" in capsys.readouterr().err
