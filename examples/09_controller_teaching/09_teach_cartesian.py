"""현재 Cartesian 좌표를 컨트롤러 슬롯에 티칭. Home·이동 없음.

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
LOCATION_INDEX = 1


def main():
    if type(LOCATION_INDEX) is not int or LOCATION_INDEX < 1:
        raise ValueError("LOCATION_INDEX는 1 이상의 정수여야 합니다.")
    with PF400(HOST, port=PORT, status_port=STATUS_PORT, timeout=TIMEOUT) as robot:
        configure_session(robot, robot_id=ROBOT_ID)
        robot.here_c(LOCATION_INDEX)
        print("Location [status, type, index, coordinates...]:", robot.loc(LOCATION_INDEX).raw)


if __name__ == "__main__":
    main()
