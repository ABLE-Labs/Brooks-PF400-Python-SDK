"""Independent wire examples, reviewed against the delivered firmware comments."""

import asyncio

import pytest

from test_sdk import client
from test_sdk import devices  # noqa: F401 -- shared fixture


CASES = [
    ("version", (), {}, "Version"),
    ("mode", (0,), {}, "Mode 0"),
    ("nop", (), {}, "Nop"),
    ("sys_state", (), {}, "SysState"),
    ("pd", (2800,), {}, "Pd 2800"),
    ("pc", (100, 2), {}, "Pc 100 2"),
    ("hp", (1, -1), {}, "Hp 1 -1"),
    ("attach", (1,), {}, "Attach 1"),
    ("home", (), {}, "Home"),
    ("home_all", (), {}, "HomeAll"),
    ("dest_c", (1,), {}, "DestC 1"),
    ("dest_j", (1,), {}, "DestJ 1"),
    ("mspeed", (20,), {}, "Mspeed 20"),
    ("select_robot", (1,), {}, "SelectRobot 1"),
    ("speed", (2, 10), {}, "Speed 2 10"),
    ("speed2", (2, 10), {}, "Speed2 2 10"),
    ("accel", (2, 10), {}, "Accel 2 10"),
    ("decel", (2, 10), {}, "Decel 2 10"),
    ("acc_ramp", (2, 10), {}, "AccRamp 2 10"),
    ("dec_ramp", (2, 10), {}, "DecRamp 2 10"),
    ("in_range", (2, 0), {}, "InRange 2 0"),
    ("straight", (2, 1), {}, "Straight 2 1"),
    ("profile", (2, [10, 10, 10, 10, 10, 10, 0, 1]), {}, "Profile 2 10 10 10 10 10 10 0 1"),
    ("loc", (1,), {}, "Loc 1"),
    ("loc_angles", (1, [1, 2, 3, 4, 5, 6]), {}, "LocAngles 1 1 2 3 4 5 6"),
    ("loc_xyz", (1, [1, 2, 3, 4, 5, 6]), {}, "LocXyz 1 1 2 3 4 5 6"),
    ("loc_z_clearance", (1, 20, 1), {}, "LocZClearance 1 20 1"),
    ("loc_config", (1, 2), {}, "LocConfig 1 2"),
    ("where", (), {}, "Where"),
    ("where_c", (), {}, "WhereC"),
    ("where_j", (), {}, "WhereJ"),
    ("here_j", (1,), {}, "HereJ 1"),
    ("here_c", (1,), {}, "HereC 1"),
    ("zero_torque", (1, 7), {}, "ZeroTorque 1 7"),
    ("release_brake", (1,), {}, "ReleaseBrake 1"),
    ("set_brake", (1,), {}, "SetBrake 1"),
    ("base", ([1, 2, 3, 4],), {}, "Base 1 2 3 4"),
    ("tool", ([1, 2, 3, 4, 5, 6],), {}, "Tool 1 2 3 4 5 6"),
    ("move", (1, 2), {}, "Move 1 2"),
    ("move_appro", (1, 2), {}, "MoveAppro 1 2"),
    ("move_extra_axis", (100, 200), {}, "MoveExtraAxis 100 200"),
    ("move_one_axis", (1, 100, 2), {}, "MoveOneAxis 1 100 2"),
    ("wait_for_eom", (), {}, "WaitForEom"),
    ("move_j", (2, [1, 2, 3, 4, 5, 6]), {}, "MoveJ 2 1 2 3 4 5 6"),
    ("move_c", (2, [1, 2, 3, 4, 5, 6], 1), {}, "MoveC 2 1 2 3 4 5 6 1"),
    ("payload", (50,), {}, "Payload 50"),
    ("state", (), {}, "State"),
    ("halt", (), {}, "Halt"),
    ("sig", (1, 1), {}, "Sig 1 1"),
    ("reset", (1,), {}, "Reset 1"),
    ("custom", (1, 2), {}, "Custom 1 2"),
    ("convert_joint_to_cartesian", ([1, 2, 3, 4, 5, 6],), {}, "ConvertJointToCartesian 1 2 3 4 5 6"),
    ("convert_cartesian_to_joint", ([1, 2, 3, 4, 5, 6], 1), {}, "ConvertCartesianToJoint 1 2 3 4 5 6 1"),
    ("load_file", ("Tcs.gpo",), {}, "LoadFile Tcs.gpo"),
    ("store_file", ("Tcs.gpo",), {}, "StoreFile Tcs.gpo"),
    ("move_to_safe", (), {}, "MoveToSafe"),
    ("change_config", (0,), {}, "ChangeConfig 0"),
    ("change_config2", (0,), {}, "ChangeConfig2 0"),
    ("pick_plate", (1, 1, 10), {}, "PickPlate 1 1 10"),
    ("place_plate", (1, 1, 10), {}, "PlacePlate 1 1 10"),
    ("teach_plate", (1, 20), {}, "TeachPlate 1 20"),
    ("move_rail", (1, 1, 100), {}, "MoveRail 1 1 100"),
    ("rail", (1, 100), {}, "Rail 1 100"),
    ("gripper", (1,), {}, "Gripper 1"),
    ("free_mode", (-1,), {}, "FreeMode -1"),
    ("grip_open_pos", (100,), {}, "GripOpenPos 100"),
    ("grip_close_pos", (80,), {}, "GripClosePos 80"),
    ("grasp_data", (85, 10, 5), {}, "GraspData 85 10 5"),
    ("station_type", (1, 0, 1, 20, 5, 2), {}, "StationType 1 0 1 20 5 2"),
    ("pallet_origin", (1, [1, 2, 3, 4, 5, 6], 0), {}, "PalletOrigin 1 1 2 3 4 5 6 0"),
    ("pallet_x", (1, 3, [1, 2, 3]), {}, "PalletX 1 3 1 2 3"),
    ("pallet_y", (1, 3, [1, 2, 3]), {}, "PalletY 1 3 1 2 3"),
    ("pallet_z", (1, 3, [1, 2, 3]), {}, "PalletZ 1 3 1 2 3"),
    ("pallet_index", (1, 1, 2, 3), {}, "PalletIndex 1 1 2 3"),
    ("home_all_if_no_plate", (), {}, "HomeAll_IfNoPlate"),
    ("grasp_plate", (85, 10, 5), {}, "GraspPlate 85 10 5"),
    ("release_plate", (100, 10, 0), {}, "ReleasePlate 100 10 0"),
    ("is_fully_closed", (), {}, "IsFullyClosed"),
    ("set_active_gripper", (1, 0, 2), {}, "SetActiveGripper 1 0 2"),
    ("get_active_gripper", (), {}, "GetActiveGripper"),
    ("height_detect", (2, -100, -15), {}, "HeightDetect 2 -100 -15"),
]


@pytest.mark.parametrize("method,args,kwargs,wire", CASES, ids=[case[0] for case in CASES])
@pytest.mark.parametrize("asynchronous", [False, True], ids=["sync", "async"])
def test_firmware_wire_mapping(devices, method, args, kwargs, wire, asynchronous):  # noqa: F811
    robot, motion, status = client(devices)
    if asynchronous:
        from pf400 import AsyncPF400

        async def exercise():
            async with AsyncPF400("127.0.0.1", port=motion.port, status_port=status.port) as async_robot:
                await getattr(async_robot, method)(*args, **kwargs)

        asyncio.run(exercise())
    else:
        with robot:
            getattr(robot, method)(*args, **kwargs)
    assert (status.received if method == "reset" else motion.received) == [wire]
    assert (motion.received if method == "reset" else status.received) == []


def test_every_command_has_an_independent_wire_example():
    from pf400.commands import COMMANDS

    assert {case[3].split()[0] for case in CASES} | {"Exit"} == set(COMMANDS)
