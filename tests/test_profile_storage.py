"""PC persistence and explicit operations; no physical devices."""

import importlib.util
import json
import runpy
import socket
from pathlib import Path

import pytest

from test_sdk import devices  # noqa: F401

ROOT = Path(__file__).parents[1]
OPERATIONS = [
    '03_profiles/03_profile_save.py', '03_profiles/03_profile_apply.py', '03_profiles/03_profile_read.py',
    '07_gripper/07_gripper_read.py', '07_gripper/07_gripper_settings.py', '07_gripper/07_gripper_open.py', '07_gripper/07_gripper_close.py',
    '08_gripper_force/08_grasp_plate.py', '08_gripper_force/08_release_plate.py',
    '09_controller_teaching/09_location_show.py', '09_controller_teaching/09_teach_joint.py', '09_controller_teaching/09_teach_cartesian.py', '09_controller_teaching/09_locations_store.py',
    '10_coordinate_conversion/10_joint_to_cartesian.py', '10_coordinate_conversion/10_cartesian_to_joint.py',
    '13_teaching_positions/13_positions_list.py', '13_teaching_positions/13_position_save.py', '13_teaching_positions/13_position_move.py',
    '14_free_mode/14_axes_free.py', '14_free_mode/14_axes_restore.py',
]


def api():
    path = ROOT / 'examples/common/motion_profiles.py'
    assert path.exists(), 'Missing persistent profile storage'
    spec = importlib.util.spec_from_file_location('review_profiles', path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def sample():
    return {
        'master_speed': 17.0,
        'profiles': {'1': dict(zip(
            ('speed', 'speed2', 'accel', 'decel', 'acc_ramp', 'dec_ramp', 'in_range', 'straight'),
            (11.0, 12.0, 13.0, 14.0, 0.3, 0.4, 25.0, 1),
        ))},
    }


def run(name, **settings):
    path = ROOT / 'examples' / name
    if not path.exists():
        path = next((ROOT / 'examples').glob('[0-9]*/' + name))
    assert path.exists(), f'Missing operation example: {name}'
    main = runpy.run_path(str(path), run_name='operation_test')['main']
    main.__globals__.update(settings)
    return main()


def test_profile_roundtrip_and_missing_file(tmp_path):
    module = api()
    path = tmp_path / 'profiles.json'
    with pytest.raises(FileNotFoundError):
        module.load_profiles(path)
    module.save_profiles(path, sample())
    assert module.load_profiles(path) == sample()
    assert list(tmp_path.iterdir()) == [path]


@pytest.mark.parametrize('change', [
    lambda data: data.update(master_speed=float('nan')),
    lambda data: data['profiles']['1'].update(speed=True),
    lambda data: data['profiles']['1'].update(straight=2),
    lambda data: data['profiles']['1'].pop('decel'),
    lambda data: data['profiles'].update({'21': data['profiles'].pop('1')}),
])
def test_bad_profile_never_overwrites_file(tmp_path, change):
    module = api()
    path = tmp_path / 'profiles.json'
    module.save_profiles(path, sample())
    original = path.read_bytes()
    data = sample()
    change(data)
    with pytest.raises(ValueError):
        module.save_profiles(path, data)
    assert path.read_bytes() == original


def test_startup_and_motion_use_file_values(devices, tmp_path):  # noqa: F811
    path = tmp_path / 'profiles.json'
    path.write_text(json.dumps(sample()), encoding='utf-8')
    motion = devices(lambda cmd: b'0 1 2 3 4 5 6\r\n' if cmd == 'WhereJ' else b'0\r\n')
    status = devices(lambda cmd: b'0 1\r\n' if cmd == 'Pd 2800' else b'0\r\n')
    run('04_joint_motion/04_joint_motion.py', HOST='127.0.0.1', PORT=motion.port, STATUS_PORT=status.port,
        PROFILE_FILE=path, TARGET_JOINTS=[1, 2, 3, 4, 5, 6])
    assert 'Mspeed 17.0' in motion.received
    assert 'Profile 1 11.0 12.0 13.0 14.0 0.3 0.4 25.0 1' in motion.received
    assert not any(cmd.startswith('Profile 2 ') for cmd in motion.received)
    assert 'Gripper 1' not in motion.received


@pytest.mark.parametrize('name', OPERATIONS)
def test_operation_files_import_without_connecting(monkeypatch, name):
    path = ROOT / 'examples' / name
    assert path.exists(), f'Missing operation example: {name}'
    def forbidden(*args, **kwargs):
        pytest.fail('Import must not connect')
    monkeypatch.setattr(socket, 'create_connection', forbidden)
    namespace = runpy.run_path(str(path), run_name='operation_test')
    assert 'ACTION' not in namespace
    assert callable(namespace['main'])


def test_profile_save_is_pc_only_and_preserves_other_slots(monkeypatch, tmp_path):
    module = api()
    path = tmp_path / 'profiles.json'
    module.save_profiles(path, sample())
    def forbidden(*args, **kwargs):
        pytest.fail('PC profile save must not connect')
    monkeypatch.setattr(socket, 'create_connection', forbidden)
    run('03_profiles/03_profile_save.py', PROFILE_FILE=path, PROFILE_INDEX=2, MASTER_SPEED=23.0)
    data = module.load_profiles(path)
    assert data['master_speed'] == 23.0
    assert data['profiles']['1'] == sample()['profiles']['1']
    assert '2' in data['profiles']


def test_bad_config_fails_before_connect(monkeypatch, tmp_path):
    path = tmp_path / 'broken.json'
    path.write_text('{broken', encoding='utf-8')
    def forbidden(*args, **kwargs):
        pytest.fail('Invalid stored profile must fail before connecting')
    monkeypatch.setattr(socket, 'create_connection', forbidden)
    with pytest.raises(ValueError):
        run('04_joint_motion/04_joint_motion.py', PROFILE_FILE=path, TARGET_JOINTS=[1, 2, 3, 4, 5, 6])


def test_read_gripper_is_query_only(devices):  # noqa: F811
    motion, status = devices(), devices()
    run('07_gripper/07_gripper_read.py', HOST='127.0.0.1', PORT=motion.port, STATUS_PORT=status.port)
    assert motion.received == ['Mode 0', 'SelectRobot 1', 'GripOpenPos', 'GripClosePos']


def test_failed_grasp_raises(devices):  # noqa: F811
    motion = devices(lambda cmd: b'0 0\r\n' if cmd.startswith('GraspPlate ') else b'0\r\n')
    status = devices(lambda cmd: b'0 1\r\n' if cmd == 'Pd 2800' else b'0\r\n')
    with pytest.raises(RuntimeError, match='잡기'):
        run('08_gripper_force/08_grasp_plate.py', HOST='127.0.0.1', PORT=motion.port, STATUS_PORT=status.port)


def test_release_waits_for_completion(devices):  # noqa: F811
    motion, status = devices(), devices()
    run('08_gripper_force/08_release_plate.py', HOST='127.0.0.1', PORT=motion.port, STATUS_PORT=status.port)
    assert motion.received[-2:] == ['ReleasePlate 85.0 20.0 0.0', 'WaitForEom']
    assert 'Home' not in motion.received and 'Gripper 1' not in motion.received


def test_atomic_save_failure_keeps_original(monkeypatch, tmp_path):
    module = api()
    path = tmp_path / 'profiles.json'
    module.save_profiles(path, sample())
    original = path.read_bytes()
    def fail_replace(*args):
        raise OSError('Disk replacement failed')
    monkeypatch.setattr(module.os, 'replace', fail_replace)
    changed = sample()
    changed['master_speed'] = 29.0
    with pytest.raises(OSError):
        module.save_profiles(path, changed)
    assert path.read_bytes() == original
    assert list(tmp_path.iterdir()) == [path]


def test_apply_profiles_uses_file_without_power(devices, tmp_path):  # noqa: F811
    path = tmp_path / 'profiles.json'
    path.write_text(json.dumps(sample()), encoding='utf-8')
    motion, status = devices(), devices()
    run('03_profiles/03_profile_apply.py', PROFILE_FILE=path, HOST='127.0.0.1',
        PORT=motion.port, STATUS_PORT=status.port)
    assert motion.received == [
        'Mode 0', 'SelectRobot 1', 'Mspeed 17.0', 'Profile 1 11.0 12.0 13.0 14.0 0.3 0.4 25.0 1',
    ]


@pytest.mark.parametrize('operation,command', [('open', 'Gripper 1'), ('close', 'Gripper 2')])
def test_explicit_gripper_operations(devices, operation, command):  # noqa: F811
    motion = devices()
    status = devices(lambda cmd: b'0 1\r\n' if cmd == 'Pd 2800' else b'0\r\n')
    run(f'07_gripper_{operation}.py', HOST='127.0.0.1', PORT=motion.port, STATUS_PORT=status.port)
    assert [cmd for cmd in motion.received if cmd.startswith('Gripper ')] == [command]


def test_startup_reads_custom_configuration(devices, tmp_path):  # noqa: F811
    path = tmp_path / 'profiles.json'
    path.write_text(json.dumps(sample()), encoding='utf-8')
    motion = devices()
    status = devices(lambda cmd: b'0 1\r\n' if cmd == 'Pd 2800' else b'0\r\n')
    run('02_power/02_startup.py', PROFILE_FILE=path, HOST='127.0.0.1', PORT=motion.port, STATUS_PORT=status.port)
    assert 'Mspeed 17.0' in motion.received
    assert 'Profile 1 11.0 12.0 13.0 14.0 0.3 0.4 25.0 1' in motion.received
    assert not any(cmd.startswith('Profile 2 ') for cmd in motion.received)


@pytest.mark.parametrize('name,settings', [
    ('04_joint_motion/04_joint_motion.py', {'TARGET_JOINTS': [1, 2, 3]}),
    ('06_single_axis/06_single_axis_motion.py', {'AXIS': 7, 'TARGET_POSITION': 10}),
])
def test_axis_mismatch_precedes_initialization(devices, name, settings):  # noqa: F811
    motion = devices(lambda cmd: b'0 1 2 3 4 5 6\r\n')
    status = devices()
    with pytest.raises(ValueError):
        run(name, HOST='127.0.0.1', PORT=motion.port, STATUS_PORT=status.port, **settings)
    assert motion.received == ['Mode 0', 'SelectRobot 1', 'WhereJ']


def test_motion_blocked_if_home_not_confirmed(devices):  # noqa: F811
    motion = devices(lambda cmd: b'0 1 2 3 4 5 6\r\n' if cmd == 'WhereJ' else b'0\r\n')
    status = devices(lambda cmd: b'0 0\r\n' if cmd == 'Pd 2800' else b'0\r\n')
    with pytest.raises(RuntimeError):
        run('04_joint_motion/04_joint_motion.py', HOST='127.0.0.1', PORT=motion.port, STATUS_PORT=status.port,
            TARGET_JOINTS=[1, 2, 3, 4, 5, 6])
    assert 'Home' in motion.received
    assert not any(cmd.startswith('MoveJ ') or cmd == 'Gripper 1' for cmd in motion.received)


def test_save_operation_does_not_replace_corrupt_json(tmp_path):
    path = tmp_path / 'profiles.json'
    path.write_text('{broken', encoding='utf-8')
    with pytest.raises(ValueError):
        run('03_profiles/03_profile_save.py', PROFILE_FILE=path)
    assert path.read_text(encoding='utf-8') == '{broken'
