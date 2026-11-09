"""Cartesian → 관절 좌표 변환. 전원·Home·이동 없음.

상단 설정을 확인하고 IDE에서 실행하세요. 자동 재시도하지 않습니다.
"""

import sys
from pathlib import Path

# IDE에서 파일을 직접 실행해도 examples 패키지를 찾도록 SDK 루트를 지정합니다.
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))


from pf400 import PF400
from examples.common.initialization import configure_session
from examples.common.initialization import validate_values

HOST = "192.168.0.1"
ROBOT_ID = 1
PORT = 10100
STATUS_PORT = 10000
TIMEOUT = 10.0
POSE = None  # [X,Y,Z,yaw,pitch,roll]. 위치 mm, 각도 deg.
CONFIG = None  # 생략하면 펌웨어 기본값 0. 현재 자세 자동 선택이 아닙니다.


def main():
    validate_values(POSE, "POSE", count=6)
    if CONFIG is not None and type(CONFIG) is not int:
        raise ValueError("CONFIG는 정수여야 합니다.")
    with PF400(HOST, port=PORT, status_port=STATUS_PORT, timeout=TIMEOUT) as robot:
        configure_session(robot, robot_id=ROBOT_ID)
        print("Joints:", robot.convert_cartesian_to_joint(POSE, config=CONFIG).values)


if __name__ == "__main__":
    main()
