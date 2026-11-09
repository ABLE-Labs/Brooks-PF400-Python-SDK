"""Reviewed non-vision wire mappings. Signatures use firmware parameter order.

Each entry: command, python name, signature, argument expression, wire-count rule.
The firmware remains responsible for installed axis counts, index ranges and units.
"""

SPECS = []


def add(command, name, signature="", arguments="()", counts=(0,)):
    SPECS.append(dict(command=command, method=name, signature=signature, arguments=arguments, counts=counts))


for command, name in [
    ("Version", "version"),
    ("Nop", "nop"),
    ("SysState", "sys_state"),
    ("Home", "home"),
    ("HomeAll", "home_all"),
    ("Where", "where"),
    ("WhereC", "where_c"),
    ("WhereJ", "where_j"),
    ("WaitForEom", "wait_for_eom"),
    ("State", "state"),
    ("Halt", "halt"),
    ("MoveToSafe", "move_to_safe"),
    ("HomeAll_IfNoPlate", "home_all_if_no_plate"),
    ("IsFullyClosed", "is_fully_closed"),
    ("GetActiveGripper", "get_active_gripper"),
    ("Exit", "exit"),
]:
    add(command, name)

for command, name, arg in [
    ("Mode", "mode", "value"),
    ("Attach", "attach", "value"),
    ("SelectRobot", "select_robot", "robot_id"),
    ("Mspeed", "mspeed", "value"),
    ("Payload", "payload", "value"),
    ("DestC", "dest_c", "destination_only"),
    ("DestJ", "dest_j", "destination_only"),
    ("GripOpenPos", "grip_open_pos", "width"),
    ("GripClosePos", "grip_close_pos", "width"),
]:
    add(command, name, f"{arg}: float | None = None", f"_params({arg})", (0, 1))

add("Hp", "hp", "value: int | None = None, wait: float | None = None", "_params(value, wait)", (0, 1, 2))
add(
    "Pd",
    "pd",
    "parameter_id: int, index1: int | None = None, index2: int | None = None, index3: int | None = None",
    "_params(parameter_id, index1, index2, index3)",
    (1, 2, 3, 4),
)
add(
    "Pc",
    "pc",
    "parameter_id: int, value: Scalar, *, indices: Sequence[int] | None = None",
    "(parameter_id, value) if indices is None else (parameter_id, *_vector(indices, (3,)), value)",
    (2, 5),
)

for command, name in [
    ("Speed", "speed"),
    ("Speed2", "speed2"),
    ("Accel", "accel"),
    ("Decel", "decel"),
    ("AccRamp", "acc_ramp"),
    ("DecRamp", "dec_ramp"),
    ("InRange", "in_range"),
    ("Straight", "straight"),
]:
    add(
        command,
        name,
        "profile_index: int, value: float | None = None",
        "_params(profile_index, value)",
        (1, 2),
    )
add(
    "Profile",
    "profile",
    "profile_index: int, values: Sequence[float] | None = None",
    "(profile_index,) if values is None else (profile_index, *_vector(values, (8,)))",
    (1, 9),
)
add("Loc", "loc", "index: int", "(index,)", (1,))
add(
    "LocAngles",
    "loc_angles",
    "index: int, joints: Sequence[float] | None = None",
    "(index,) if joints is None else (index, *_vector(joints, range(1,13)))",
    tuple(range(1, 14)),
)
add(
    "LocXyz",
    "loc_xyz",
    "index: int, pose: Sequence[float] | None = None",
    "(index,) if pose is None else (index, *_vector(pose, (6,)))",
    (1, 7),
)
add(
    "LocZClearance",
    "loc_z_clearance",
    "index: int, clearance: float | None = None, world: int | None = None",
    "_params(index, clearance, world)",
    (1, 2, 3),
)
add("LocConfig", "loc_config", "index: int, config: int | None = None", "_params(index, config)", (1, 2))
for command, name, arg in [
    ("HereJ", "here_j", "index"),
    ("HereC", "here_c", "index"),
    ("ReleaseBrake", "release_brake", "axis"),
    ("SetBrake", "set_brake", "axis"),
    ("Reset", "reset", "thread_id"),
    ("ChangeConfig", "change_config", "gripper_mode"),
    ("ChangeConfig2", "change_config2", "gripper_mode"),
    ("Gripper", "gripper", "action"),
    ("FreeMode", "free_mode", "axis"),
]:
    add(command, name, f"{arg}: int", f"({arg},)", (1,))
add(
    "ZeroTorque",
    "zero_torque",
    "enabled: int, axis_mask: int | None = None",
    "_params(enabled, axis_mask)",
    (1, 2),
)
for command, name, length in [("Base", "base", 4), ("Tool", "tool", 6)]:
    add(
        command,
        name,
        "pose: Sequence[float] | None = None",
        f"() if pose is None else _vector(pose, ({length},))",
        (0, length),
    )
for command, name in [("Move", "move"), ("MoveAppro", "move_appro")]:
    add(command, name, "location_index: int, profile_index: int", "(location_index, profile_index)", (2,))
add(
    "MoveExtraAxis",
    "move_extra_axis",
    "position1: float, position2: float | None = None",
    "_params(position1, position2)",
    (1, 2),
)
add(
    "MoveOneAxis",
    "move_one_axis",
    "axis: int, position: float, profile_index: int",
    "(axis, position, profile_index)",
    (3,),
)
add(
    "MoveJ",
    "move_j",
    "profile_index: int, joints: Sequence[float]",
    "(profile_index, *_vector(joints, range(1,13)))",
    tuple(range(2, 14)),
)
add(
    "MoveC",
    "move_c",
    "profile_index: int, pose: Sequence[float], config: int | None = None",
    "_params(profile_index, *_vector(pose, (6,)), config)",
    (7, 8),
)
add("Sig", "sig", "signal: int, value: int | None = None", "_params(signal, value)", (1, 2))
for command, name in [("LoadFile", "load_file"), ("StoreFile", "store_file")]:
    add(command, name, "filename: str | None = None", "_params(filename)", (0, 1))
for command, name in [("PickPlate", "pick_plate"), ("PlacePlate", "place_plate")]:
    # PlacePlate parameter details are preserved in the reference; see notes.
    add(
        command,
        name,
        "station_id: int, compliance: int | None = None, holding_torque_percent: float | None = None",
        "_params(station_id, compliance, holding_torque_percent)",
        (1, 2, 3),
    )
add(
    "TeachPlate",
    "teach_plate",
    "station_id: int, z_clearance: float | None = None",
    "_params(station_id, z_clearance)",
    (1, 2),
)
add(
    "MoveRail",
    "move_rail",
    "station_id: int, mode: int | None = None, position: float | None = None",
    "_params(station_id, mode, position)",
    (1, 2, 3),
)
add("Rail", "rail", "station_id: int, position: float | None = None", "_params(station_id, position)", (1, 2))
add(
    "GraspData",
    "grasp_data",
    "width: float | None = None, speed: float | None = None, force: float | None = None",
    "_params(width, speed, force)",
    (0, 3),
)
add(
    "StationType",
    "station_type",
    "station_id: int, access: int | None = None, pallet_type: int | None = None, z_clearance: float | None = None, z_above: float | None = None, z_grasp_offset: float | None = None",
    "_params(station_id, access, pallet_type, z_clearance, z_above, z_grasp_offset)",
    tuple(range(1, 7)),
)
add(
    "PalletOrigin",
    "pallet_origin",
    "station_id: int, pose: Sequence[float] | None = None, config: int | None = None",
    "_params(station_id, config) if pose is None else _params(station_id, *_vector(pose, (6,)), config)",
    (1, 7, 8),
)
for command, name in [("PalletX", "pallet_x"), ("PalletY", "pallet_y"), ("PalletZ", "pallet_z")]:
    add(
        command,
        name,
        "station_id: int, count: int | None = None, xyz: Sequence[float] | None = None",
        "_params(station_id, count) if xyz is None else _params(station_id, count, *_vector(xyz, (3,)))",
        (1, 5),
    )
add(
    "PalletIndex",
    "pallet_index",
    "station_id: int, x: int | None = None, y: int | None = None, z: int | None = None",
    "_params(station_id, x, y, z)",
    (1, 2, 3, 4),
)
add("GraspPlate", "grasp_plate", "width: float, speed: float, force: float", "(width, speed, force)", (3,))
add(
    "ReleasePlate",
    "release_plate",
    "width: float, speed: float, in_range: float | None = None",
    "_params(width, speed, in_range)",
    (2, 3),
)
add(
    "SetActiveGripper",
    "set_active_gripper",
    "gripper: int, spin: int | None = None, profile_index: int | None = None",
    "_params(gripper, spin, profile_index)",
    (1, 3),
)
add(
    "HeightDetect",
    "height_detect",
    "quick_mode: int | None = None, search_limit: float | None = None, max_force: float | None = None",
    "_params(quick_mode, search_limit, max_force)",
    (0, 3),
)
add("Custom", "custom", "*values: float", "values", None)
add(
    "ConvertJointToCartesian",
    "convert_joint_to_cartesian",
    "joints: Sequence[float]",
    "_vector(joints, range(1,13))",
    tuple(range(1, 13)),
)
add(
    "ConvertCartesianToJoint",
    "convert_cartesian_to_joint",
    "pose: Sequence[float], config: int | None = None",
    "_params(*_vector(pose, (6,)), config)",
    (6, 7),
)

EXCLUDED = (
    "Vprocess",
    "VresultLoc",
    "VresultInfo",
    "VresultInspect",
    "VToolProperty",
    "VresultInfoString",
    "StereoParam",
    "StereoLocate",
)
