"""버전·상태·현재 좌표 조회. 자동 초기화나 이동은 하지 않습니다."""

import sys
from pathlib import Path

# IDE에서 파일을 직접 실행해도 examples 패키지를 찾도록 SDK 루트를 지정합니다.
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))


from examples.common.initialization import configure_session

from pf400 import PF400

# 실제 장비 주소와 필요한 값으로 수정한 뒤 이 파일을 실행하세요.
HOST = "192.168.0.1"
ROBOT_ID = 1
PORT = 10100
STATUS_PORT = 10000
TIMEOUT = 10.0


def main():
    with PF400(HOST, port=PORT, status_port=STATUS_PORT, timeout=TIMEOUT) as robot:
        configure_session(robot, robot_id=ROBOT_ID)
        print("Version:", robot.version().data)
        print("System state:", robot.sys_state().values)
        print("Motion state:", robot.state().values)
        print("Joint positions:", robot.where_j().as_floats())
        print("Cartesian pose and config:", robot.where_c().as_floats())


if __name__ == "__main__":
    main()
