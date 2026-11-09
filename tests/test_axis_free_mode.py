"""Selective free-mode example is checked against loopback devices only."""

import socket
from pathlib import Path

import pytest

from test_examples import run_example
from test_sdk import devices  # noqa: F401
from test_initialization import INITIALIZATION, SESSION_MOTION, SESSION_STATUS


def require_example():
    path = Path(__file__).parents[1] / "examples/14_free_mode/14_axes_free.py"
    assert path.exists(), "Selective axis example has not been implemented"


@pytest.mark.parametrize(
    "action,axes,expected",
    [
        ("free", [3], SESSION_MOTION + ["WhereJ"] + INITIALIZATION + ["FreeMode 3"]),
        ("free", [1, 3], SESSION_MOTION + ["WhereJ"] + INITIALIZATION + ["FreeMode 1", "FreeMode 3"]),
        ("restore", [3], SESSION_MOTION + ["FreeMode -1"]),
    ],
)
def test_selected_axis_and_restore_wire_sequence(devices, action, axes, expected):  # noqa: F811
    require_example()
    motion = devices(lambda cmd: b"0 1 2 3 4 5 6\r\n" if cmd == "WhereJ" else b"0\r\n")
    status = devices()
    run_example(
        "14_free_mode/14_axes_restore.py" if action == "restore" else "14_free_mode/14_axes_free.py",
        {
            "HOST": "127.0.0.1",
            "PORT": motion.port,
            "STATUS_PORT": status.port,
            "AXES": axes,
        },
    )
    assert motion.received == expected
    assert status.received == SESSION_STATUS


@pytest.mark.parametrize("axes", [[], [0], [-1], [13], [True], [1.5], ["3"], [1, 1], "1,3", 3, [1, 0]])
def test_invalid_axis_does_not_connect(monkeypatch, axes):
    require_example()

    def forbidden(*args, **kwargs):
        pytest.fail("Invalid axis must be rejected before connecting")

    monkeypatch.setattr(socket, "create_connection", forbidden)
    with pytest.raises(ValueError):
        run_example("14_free_mode/14_axes_free.py", {"AXES": axes})


def test_unavailable_axis_is_rejected_before_any_mode_change(devices):  # noqa: F811
    require_example()
    motion = devices(lambda _: b"0 1 2 3 4 5 6\r\n")
    status = devices()
    with pytest.raises(ValueError):
        run_example(
            "14_free_mode/14_axes_free.py",
            {
                "HOST": "127.0.0.1",
                "PORT": motion.port,
                "STATUS_PORT": status.port,
                "AXES": [1, 7],
            },
        )
    assert motion.received == SESSION_MOTION + ["WhereJ"]
    assert status.received == SESSION_STATUS
