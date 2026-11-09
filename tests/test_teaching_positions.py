"""JSON teaching examples use temporary files and loopback TCP only."""

import json
import runpy
import socket
from pathlib import Path

import pytest

from test_examples import run_example
from test_sdk import devices  # noqa: F401
from test_initialization import INITIALIZATION, SESSION_MOTION, SESSION_STATUS

EXAMPLES = Path(__file__).parents[1] / "examples"


def module():
    path = EXAMPLES / "common/teaching_positions.py"
    assert path.exists(), "JSON teaching example has not been implemented"
    return runpy.run_path(str(path), run_name="teaching_example")


def test_bundled_json_has_valid_position_structure():
    path = EXAMPLES / "config/teaching_positions.json"
    assert path.exists(), "Teaching JSON has not been created"
    assert isinstance(module()["read_positions"](path)["positions"], dict)


def test_save_preserves_other_positions_and_metadata(tmp_path):
    api = module()
    path = tmp_path / "positions.json"
    path.write_text(
        json.dumps({"description": "sample", "positions": {"old": {"joints": [1, 2, 3]}}}), encoding="utf-8"
    )
    api["save_position"](path, "new", [4.0, 5.0, 6.0])
    data = json.loads(path.read_text(encoding="utf-8"))
    assert data["description"] == "sample"
    assert data["positions"]["old"]["joints"] == [1, 2, 3]
    assert api["load_position"](path, "new") == [4.0, 5.0, 6.0]
    assert list(tmp_path.iterdir()) == [path]


def test_save_new_file_and_reteach_same_name(tmp_path):
    api = module()
    path = tmp_path / "positions.json"
    api["save_position"](path, "position_a", [1, 2, 3])
    api["save_position"](path, "position_a", [4, 5, 6])
    assert api["load_position"](path, "position_a") == [4, 5, 6]
    assert len(api["read_positions"](path)["positions"]) == 1


@pytest.mark.parametrize("joints", [[], [True], ["1"], [float("nan")], [float("inf")], list(range(13))])
def test_invalid_coordinates_leave_file_intact(tmp_path, joints):
    api = module()
    path = tmp_path / "positions.json"
    original = '{"positions": {}}'
    path.write_text(original, encoding="utf-8")
    with pytest.raises(ValueError):
        api["save_position"](path, "bad", joints)
    assert path.read_text(encoding="utf-8") == original


@pytest.mark.parametrize(
    "text", ["{broken", "[]", '{"positions": []}', '{"positions":{"bad":{"joints":["1"]}}}']
)
def test_malformed_json_is_not_replaced(tmp_path, text):
    api = module()
    path = tmp_path / "positions.json"
    path.write_text(text, encoding="utf-8")
    with pytest.raises(ValueError):
        api["save_position"](path, "new", [1, 2, 3])
    assert path.read_text(encoding="utf-8") == text


def test_list_and_missing_move_do_not_connect(tmp_path, monkeypatch, capsys):
    module()
    path = tmp_path / "positions.json"
    path.write_text('{"positions": {}}', encoding="utf-8")

    def forbidden(*args, **kwargs):
        pytest.fail("Listing or unknown position must not open a socket")

    monkeypatch.setattr(socket, "create_connection", forbidden)
    run_example("13_teaching_positions/13_positions_list.py", {"JSON_FILE": path})
    assert "없습니다" in capsys.readouterr().out
    with pytest.raises(ValueError):
        run_example(
            "13_teaching_positions/13_position_move.py", {"ACTION": "move", "JSON_FILE": path, "POSITION_NAME": "missing"}
        )


def test_save_then_load_and_move_same_position(devices, tmp_path):  # noqa: F811
    module()
    motion = devices(lambda _: b"0 1 2 3 4 5 6\r\n")
    status = devices(lambda command: b"0 1\r\n" if command == "Pd 2800" else b"0\r\n")
    path = tmp_path / "positions.json"
    settings = {
        "HOST": "127.0.0.1",
        "PORT": motion.port,
        "STATUS_PORT": status.port,
        "JSON_FILE": path,
        "POSITION_NAME": "station_a",
        "PROFILE_INDEX": 2,
    }
    run_example("13_teaching_positions/13_position_save.py", settings)
    assert json.loads(path.read_text(encoding="utf-8"))["positions"]["station_a"]["joints"] == [
        1.0,
        2.0,
        3.0,
        4.0,
        5.0,
        6.0,
    ]
    assert motion.received == SESSION_MOTION + ["WhereJ"]
    run_example("13_teaching_positions/13_position_move.py", settings)
    assert motion.received == SESSION_MOTION + ["WhereJ"] + SESSION_MOTION + ["WhereJ"] + INITIALIZATION + [
        "MoveJ 2 1.0 2.0 3.0 4.0 5.0 6.0",
        "WaitForEom",
        "WhereJ",
    ]
    assert status.received == SESSION_STATUS + SESSION_STATUS + ["Pd 2800"]


def test_axis_count_mismatch_does_not_send_motion(devices, tmp_path):  # noqa: F811
    api = module()
    path = tmp_path / "positions.json"
    api["save_position"](path, "position_a", [1, 2, 3])
    motion, status = devices(lambda _: b"0 1 2 3 4 5 6\r\n"), devices()
    with pytest.raises(ValueError):
        run_example(
            "13_teaching_positions/13_position_move.py",
            {
                "HOST": "127.0.0.1",
                "PORT": motion.port,
                "STATUS_PORT": status.port,
                "JSON_FILE": path,
                "POSITION_NAME": "position_a",
            },
        )
    assert motion.received == SESSION_MOTION + ["WhereJ"]
