"""조회 요청의 장비·통신·타임아웃 오류를 처리합니다. 자동 재시도는 없습니다."""

import sys
from pathlib import Path

# IDE에서 파일을 직접 실행해도 examples 패키지를 찾도록 SDK 루트를 지정합니다.
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))


from examples.common.initialization import configure_session

import sys

from pf400 import PF400, CommandTimeout, ConnectionError, DeviceError, NotConnectedError, ProtocolError

# 실제 장비 주소와 필요한 값으로 수정한 뒤 이 파일을 실행하세요.
HOST = "192.168.0.1"
ROBOT_ID = 1
PORT = 10100
STATUS_PORT = 10000
TIMEOUT = 10.0


def main():
    try:
        with PF400(HOST, port=PORT, status_port=STATUS_PORT, timeout=TIMEOUT) as robot:
            configure_session(robot, robot_id=ROBOT_ID)
            print("Nop:", robot.nop().raw)
            print("Joints:", robot.where_j().values)
    except DeviceError as exc:
        print(
            f"Device error: code={exc.code}, command={exc.command}, description={exc.description}, raw={exc.raw}",
            file=sys.stderr,
        )
        if exc.hint:
            print("Hint:", exc.hint, file=sys.stderr)
        return 1
    except CommandTimeout as exc:
        print(
            f"Timeout: command={exc.command}, may_have_executed={exc.may_have_executed}. No retry.",
            file=sys.stderr,
        )
        return 1
    except ProtocolError as exc:
        print(f"Invalid response: {exc}; may_have_executed={exc.may_have_executed}", file=sys.stderr)
        return 1
    except ConnectionError as exc:
        print(f"Connection error: {exc}; may_have_executed={exc.may_have_executed}", file=sys.stderr)
        return 1
    except NotConnectedError as exc:
        print(f"Not connected: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
