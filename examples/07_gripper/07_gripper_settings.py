"""서보 그리퍼 개폐 위치 설정. 실제 개폐 명령 없음.

상단 설정을 확인하고 IDE에서 실행하세요. 자동 재시도하지 않습니다.
"""

import sys
from pathlib import Path

# IDE에서 파일을 직접 실행해도 examples 패키지를 찾도록 SDK 루트를 지정합니다.
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))


from pf400 import PF400
from examples.common.initialization import configure_session
from examples.common.initialization import validate_number

HOST = "192.168.0.1"
ROBOT_ID = 1
PORT = 10100
STATUS_PORT = 10000
TIMEOUT = 10.0
OPEN_POSITION = 100.0  # 개방 위치 [mm]. 실장비 범위 확인.
CLOSE_POSITION = 80.0  # 닫힘 위치 [mm].


def main():
    validate_number(OPEN_POSITION, "OPEN_POSITION")
    validate_number(CLOSE_POSITION, "CLOSE_POSITION")
    with PF400(HOST, port=PORT, status_port=STATUS_PORT, timeout=TIMEOUT) as robot:
        configure_session(robot, robot_id=ROBOT_ID)
        print("Open setting:", robot.grip_open_pos(OPEN_POSITION).raw)
        print("Close setting:", robot.grip_close_pos(CLOSE_POSITION).raw)


if __name__ == "__main__":
    main()
