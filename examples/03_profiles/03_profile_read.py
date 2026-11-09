"""장비에 적용된 MSpeed와 선택 프로파일 조회. 설정·전원·이동 없음.

상단 설정을 확인하고 IDE에서 실행하세요. 자동 재시도하지 않습니다.
"""

import sys
from pathlib import Path

# IDE에서 파일을 직접 실행해도 examples 패키지를 찾도록 SDK 루트를 지정합니다.
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))


from pf400 import PF400
from examples.common.initialization import configure_session
from examples.common.initialization import validate_profile

HOST = "192.168.0.1"
ROBOT_ID = 1
PORT = 10100
STATUS_PORT = 10000
TIMEOUT = 10.0
PROFILE_INDEX = 1


def main():
    validate_profile(PROFILE_INDEX, registered=False)
    with PF400(HOST, port=PORT, status_port=STATUS_PORT, timeout=TIMEOUT) as robot:
        configure_session(robot, robot_id=ROBOT_ID)
        print("Master speed [%]:", robot.mspeed().values)
        print("Profile [index, Speed%, Speed2%, Accel%, Decel%, AccRamp s, DecRamp s, InRange, Straight]:")
        print(robot.profile(PROFILE_INDEX).values)


if __name__ == "__main__":
    main()
