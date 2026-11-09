import asyncio
import importlib
import importlib.util
import inspect
import json
import socketserver
import threading
import time
from pathlib import Path

import pytest


def sdk():
    assert importlib.util.find_spec("pf400") is not None, "SDK package has not been implemented"
    module = importlib.import_module("pf400")
    assert Path(module.__file__).resolve().is_relative_to(Path(__file__).parents[1]), (
        "New SDK package has not been implemented"
    )
    return module


class Device:
    def __init__(self, reply=None):
        self.received = []
        self.reply = reply or (lambda command: b"0\r\n")
        device = self

        class Handler(socketserver.StreamRequestHandler):
            def handle(self):
                while True:
                    try:
                        line = self.rfile.readline()
                    except OSError:
                        return
                    if not line:
                        return
                    command = line.decode("ascii").rstrip("\r\n")
                    device.received.append(command)
                    response = device.reply(command)
                    if response is None:
                        return
                    chunks = response if isinstance(response, list) else [response]
                    for chunk in chunks:
                        try:
                            self.wfile.write(chunk)
                            self.wfile.flush()
                        except OSError:
                            return

        self.server = socketserver.ThreadingTCPServer(("127.0.0.1", 0), Handler)
        self.server.daemon_threads = True
        self.thread = threading.Thread(
            target=self.server.serve_forever, kwargs={"poll_interval": 0.01}, daemon=True
        )
        self.thread.start()

    @property
    def port(self):
        return self.server.server_address[1]

    def close(self):
        self.server.shutdown()
        self.server.server_close()
        self.thread.join(1)


@pytest.fixture
def devices():
    opened = []

    def make(reply=None):
        device = Device(reply)
        opened.append(device)
        return device

    yield make
    for device in opened:
        device.close()


def client(devices, reply=None, **kwargs):
    device = devices(reply)
    status = devices(reply)
    robot = sdk().PF400("127.0.0.1", port=device.port, status_port=status.port, **kwargs)
    return robot, device, status


def test_exact_firmware_coverage_and_async_api():
    module = sdk()
    manifest = json.loads(
        (Path(__file__).parents[1] / "docs/firmware_manifest.json").read_text(encoding="utf-8")
    )
    assert len(manifest["commands"]) == 82
    assert len(manifest["excluded_vision"]) == 8
    for spec in manifest["commands"]:
        assert hasattr(module.PF400, spec["method"])
        assert inspect.iscoroutinefunction(getattr(module.AsyncPF400, spec["method"]))
        assert spec["source_line"] > 0
    for name in ("vprocess", "vresult_loc", "stereo_locate", "vtool_property"):
        assert not hasattr(module.PF400, name)


def test_connect_has_no_robot_side_effects(devices):
    robot, motion, status = client(devices)
    with robot:
        assert robot.connected
        assert not motion.received and not status.received
    assert not robot.connected


def test_wire_order_quotes_and_data_preservation(devices):
    robot, motion, status = client(devices, lambda _: b"0 -1 2.5\r\n")
    with robot:
        response = robot.move_j(2, [1, 2, 3, 4, 5, 6])
        assert response.code == 0 and response.values == ("-1", "2.5")
        assert response.as_floats() == (-1.0, 2.5)
        robot.pc(100, "A quoted value")
        robot.pc(101, 2.5, indices=(1, 0, 1))
        robot.convert_cartesian_to_joint([1, 2, 3, 4, 5, 6], config=3)
    assert motion.received == [
        "MoveJ 2 1 2 3 4 5 6",
        'Pc 100 "A quoted value"',
        "Pc 101 1 0 1 2.5",
        "ConvertCartesianToJoint 1 2 3 4 5 6 3",
    ]
    assert not status.received


def test_unknown_controller_error_is_not_lost(devices):
    robot, _, _ = client(devices, lambda _: b"-99999 unexpected controller error\r\n")
    with robot, pytest.raises(sdk().DeviceError) as exc:
        robot.nop()
    assert exc.value.code == -99999
    assert exc.value.command == "Nop"
    assert "unexpected controller error" in exc.value.raw


def test_fragmented_reply_and_multiword_text(devices):
    robot, _, _ = client(devices, lambda _: [b"0 Command ", b"Server 3.0D4\r", b"\n"])
    with robot:
        response = robot.version()
    assert response.data == "Command Server 3.0D4"


@pytest.mark.parametrize("reply", [b"", b"garbage\r\n", b"0\n", b"\xff\r\n", b"1 unsupported\r\n"])
def test_invalid_frames_invalidate_only_affected_channel(devices, reply):
    robot, _, _ = client(devices, lambda _: reply or None)
    with robot:
        with pytest.raises((sdk().ProtocolError, sdk().ConnectionError)):
            robot.nop()
        assert not robot.motion_connected
        assert robot.status_connected


def test_timeout_no_retry_and_no_implicit_reconnect(devices):
    def slow(_):
        time.sleep(0.15)
        return b"0\r\n"

    robot, motion, _ = client(devices, slow, timeout=0.04)
    with robot:
        with pytest.raises(sdk().CommandTimeout) as exc:
            robot.move_j(1, [0, 0, 0, 0, 0, 0])
        assert exc.value.may_have_executed
        assert not robot.motion_connected
        with pytest.raises(sdk().NotConnectedError):
            robot.nop()
    assert len(motion.received) == 1


def test_status_halt_is_available_while_motion_waits(devices):
    started = threading.Event()
    release = threading.Event()
    failures = []

    def blocked(command):
        if command == "WaitForEom":
            started.set()
            release.wait(1)
        return b"0\r\n"

    robot, motion, status = client(devices, blocked, timeout=2)

    def wait():
        try:
            robot.wait_for_eom()
        except Exception as exc:
            failures.append(exc)

    with robot:
        robot.select_robot(1, channel="status")
        thread = threading.Thread(target=wait)
        thread.start()
        assert started.wait(1)
        robot.halt(channel="status")
        assert status.received == ["SelectRobot 1", "Halt"]
        release.set()
        thread.join(1)
        assert not thread.is_alive() and not failures
    assert motion.received == ["WaitForEom"]


@pytest.mark.parametrize(
    "invoke",
    [
        lambda r: r.custom("1\nHalt"),
        lambda r: r.load_file("file name.gpo"),
        lambda r: r.move_j(1, [float("nan")]),
        lambda r: r.tool([1, 2, 3]),
        lambda r: r.pc(100, 'bad"quote'),
        lambda r: r.set_active_gripper(1, spin=1),
        lambda r: r.height_detect(quick_mode=2, max_force=-15),
        lambda r: r.execute("Vprocess", "run"),
        lambda r: r.execute("Nop\nHalt"),
        lambda r: r.nop(channel="bad"),
    ],
)
def test_invalid_inputs_send_nothing(devices, invoke):
    robot, motion, status = client(devices)
    with robot, pytest.raises((ValueError, TypeError)):
        invoke(robot)
    assert not motion.received and not status.received


def test_exit_expects_eof_and_closes_only_chosen_connection(devices):
    robot, motion, _ = client(devices, lambda cmd: None if cmd == "Exit" else b"0\r\n")
    with robot:
        result = robot.exit()
        assert result is None
        assert not robot.motion_connected and robot.status_connected
    assert motion.received == ["Exit"]


def test_telnet_transition_and_back_to_normal(devices):
    responses = {
        "Mode 1": b"\r\nOk\r\nCMD> ",
        "Version": b"\r\nCommand Server\r\nPARobot\r\nCMD> ",
        "Mode 0": b"0\r\n",
        "Nop": b"0\r\n",
    }
    robot, _, _ = client(devices, responses.__getitem__)
    with robot:
        assert robot.mode(1).raw == "Ok"
        result = robot.version()
        assert result.code is None and "PARobot" in result.data
        assert robot.mode(0).code == 0
        assert robot.nop().code == 0


def test_async_adapter_does_not_block_event_loop(devices):
    device = devices(lambda _: (time.sleep(0.05), b"0 1\r\n")[1])
    status = devices()

    async def exercise():
        ticks = []
        async with sdk().AsyncPF400("127.0.0.1", port=device.port, status_port=status.port) as robot:

            async def ticker():
                await asyncio.sleep(0.01)
                ticks.append("tick")

            response, _ = await asyncio.gather(robot.where_j(), ticker())
            assert ticks == ["tick"] and response.as_ints() == (1,)

    asyncio.run(exercise())


def test_pc_supports_empty_string_value(devices):
    robot, motion, _ = client(devices)
    with robot:
        robot.pc(100, "")
    assert motion.received == ['Pc 100 ""']


def test_waiting_request_uses_mode_after_acquiring_channel_lock(devices):
    robot, _, _ = client(devices, lambda _: b"\r\nOk\r\nCMD> ")
    failures = []
    entered = threading.Event()

    def waiting():
        entered.set()
        try:
            robot.nop()
        except Exception as exc:
            failures.append(exc)

    with robot:
        with robot._channels["motion"].lock:
            thread = threading.Thread(target=waiting)
            thread.start()
            assert entered.wait(1)
            # Give the waiting request time to capture the pre-transition mode.
            time.sleep(0.02)
            robot.mode(1)
        thread.join(1)
        assert not thread.is_alive() and not failures


def test_cancelled_async_connect_closes_sockets(devices, monkeypatch):
    module = sdk()
    device, status = devices(), devices()
    original = module.PF400.connect

    def delayed(self):
        time.sleep(0.05)
        original(self)

    monkeypatch.setattr(module.PF400, "connect", delayed)

    async def exercise():
        robot = module.AsyncPF400("127.0.0.1", port=device.port, status_port=status.port)

        async def enter():
            async with robot:
                pytest.fail("Context should not be entered")

        task = asyncio.create_task(enter())
        await asyncio.sleep(0.01)
        task.cancel()
        with pytest.raises(asyncio.CancelledError):
            await task
        assert not robot.motion_connected and not robot.status_connected

    asyncio.run(exercise())


def test_raw_dispatch_preserves_partial_firmware_argument_forms(devices):
    robot, motion, _ = client(devices)
    with robot:
        robot.execute("HeightDetect", 2)
        robot.execute("PalletX", 1, 3)
    assert motion.received == ["HeightDetect 2", "PalletX 1 3"]


def test_protocol_failure_reports_uncertain_command_outcome(devices):
    robot, _, _ = client(devices, lambda _: b"not a normal response\r\n")
    with robot, pytest.raises(sdk().ProtocolError) as exc:
        robot.move_j(1, [1, 2, 3, 4, 5, 6])
    assert exc.value.may_have_executed
    assert exc.value.command.startswith("MoveJ ")


def test_lock_timeout_does_not_close_inflight_channel(devices):
    entered, release = threading.Event(), threading.Event()
    robot, _, _ = client(devices)

    def hold_lock():
        with robot._channels["motion"].lock:
            entered.set()
            release.wait(1)

    with robot:
        thread = threading.Thread(target=hold_lock)
        thread.start()
        assert entered.wait(1)
        try:
            with pytest.raises(sdk().CommandTimeout) as exc:
                robot.nop(timeout=0.02)
            assert not exc.value.may_have_executed and robot.motion_connected
        finally:
            release.set()
            thread.join(1)
        assert robot.nop().code == 0


def test_response_size_limit(devices):
    robot, _, _ = client(devices, lambda _: b"0 " + b"x" * 40 + b"\r\n", max_response_bytes=32)
    with robot, pytest.raises(sdk().ProtocolError):
        robot.version()
    assert not robot.motion_connected


def test_failed_second_connection_cleans_up_first(devices, monkeypatch):
    module = sdk()
    motion = devices()
    from pf400.transport import SocketChannel

    original = SocketChannel.connect

    def connect_channel(self):
        if self.port != motion.port:
            raise module.ConnectionError("Status connection failed")
        original(self)

    monkeypatch.setattr(SocketChannel, "connect", connect_channel)
    robot = module.PF400("127.0.0.1", port=motion.port, status_port=1)
    with pytest.raises(module.ConnectionError):
        robot.connect()
    assert not robot.motion_connected and not robot.status_connected


@pytest.mark.parametrize(
    "command",
    [
        "Vprocess",
        "VresultLoc",
        "VresultInfo",
        "VresultInspect",
        "VToolProperty",
        "VresultInfoString",
        "StereoParam",
        "StereoLocate",
    ],
)
def test_all_vision_commands_are_excluded_from_raw_dispatch(devices, command):
    robot, motion, status = client(devices)
    with robot, pytest.raises(ValueError):
        robot.execute(command)
    assert not motion.received and not status.received


def test_async_exit_closes_only_requested_channel(devices):
    motion = devices(lambda command: None if command == "Exit" else b"0\r\n")
    status = devices()

    async def exercise():
        async with sdk().AsyncPF400("127.0.0.1", port=motion.port, status_port=status.port) as robot:
            assert await robot.exit() is None
            assert not robot.motion_connected and robot.status_connected

    asyncio.run(exercise())
