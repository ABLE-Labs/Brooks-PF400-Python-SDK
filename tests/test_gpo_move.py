"""GPO movement is checked only against loopback controllers."""
import runpy
from pathlib import Path

import pytest
from test_sdk import devices  # noqa: F401
from test_initialization import SESSION_MOTION, SESSION_STATUS


def example():
    path = Path(__file__).parents[1] / 'examples/09_controller_teaching/09_locations_move.py'
    assert path.exists(), 'GPO movement example is missing'
    return runpy.run_path(str(path), run_name='gpo_example')['main']


@pytest.mark.parametrize('homed', [0, 1])
def test_loaded_slot_and_profile_are_used_without_json_overwrite(devices, homed):  # noqa: F811
    main = example()
    motion = devices()
    states = iter([homed, 1])
    status = devices(lambda cmd: f'0 {next(states)}\r\n'.encode() if cmd == 'Pd 2800' else b'0\r\n')
    main.__globals__.update(HOST='127.0.0.1', PORT=motion.port, STATUS_PORT=status.port,
                            LOCATION_INDEX=3, PROFILE_INDEX=2, LOAD_FILE='saved.gpo')
    main()
    assert motion.received == SESSION_MOTION + [
        'LoadFile saved.gpo', 'Loc 3', 'Profile 2', 'FreeMode -1', 'Mspeed 20.0',
        'Hp 1 30.0', 'Attach 1',
    ] + ([] if homed else ['Home']) + ['Move 3 2', 'WaitForEom']
    assert status.received == SESSION_STATUS + ['Pd 2800'] * (1 if homed else 2)


def test_slot_must_be_selected_before_connect(monkeypatch):
    main = example()
    def forbidden(*args, **kwargs):
        pytest.fail('Unset slot must fail before connecting')
    monkeypatch.setitem(main.__globals__, 'PF400', forbidden)
    monkeypatch.setitem(main.__globals__, 'LOCATION_INDEX', None)
    with pytest.raises(ValueError, match='LOCATION_INDEX'):
        main()


def test_failed_load_does_not_power_or_move(devices):  # noqa: F811
    main = example()
    motion = devices(lambda cmd: b'-1 missing file\r\n' if cmd.startswith('LoadFile') else b'0\r\n')
    status = devices()
    main.__globals__.update(HOST='127.0.0.1', PORT=motion.port, STATUS_PORT=status.port, LOCATION_INDEX=1)
    from pf400 import PF400Error
    with pytest.raises(PF400Error):
        main()
    assert motion.received == SESSION_MOTION + ['LoadFile Tcs_example.gpo']
    assert status.received == SESSION_STATUS
