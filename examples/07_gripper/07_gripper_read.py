"""그리퍼 개폐 위치 조회만 수행. 전원·설정·Home·개폐 없음.

상단 설정을 확인하고 IDE에서 실행하세요. 자동 재시도하지 않습니다.
"""

import sys
from pathlib import Path

# IDE에서 파일을 직접 실행해도 examples 패키지를 찾도록 SDK 루트를 지정합니다.
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))


from pf400 import PF400
from examples.common.initialization import configure_session


HOST = "192.168.0.1"
ROBOT_ID = 1
PORT = 10100
STATUS_PORT = 10000
TIMEOUT = 10.0


def main():
    with PF400(HOST, port=PORT, status_port=STATUS_PORT, timeout=TIMEOUT) as robot:
        configure_session(robot, robot_id=ROBOT_ID)
        print("Open position [mm]:", robot.grip_open_pos().values)
        print("Close position [mm]:", robot.grip_close_pos().values)


if __name__ == "__main__":
    main()
