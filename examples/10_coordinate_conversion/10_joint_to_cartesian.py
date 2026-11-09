"""관절 → Cartesian 좌표 변환. 전원·Home·이동 없음.

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
JOINTS = None  # 실제 축 순서의 좌표. 직선 축 mm, 회전 축 deg.


def main():
    validate_values(JOINTS, "JOINTS")
    with PF400(HOST, port=PORT, status_port=STATUS_PORT, timeout=TIMEOUT) as robot:
        configure_session(robot, robot_id=ROBOT_ID)
        if len(robot.where_j().as_floats()) != len(JOINTS):
            raise ValueError("JOINTS 개수가 실제 축 개수와 다릅니다.")
        print("Cartesian [X,Y,Z,yaw,pitch,roll,config]:", robot.convert_joint_to_cartesian(JOINTS).values)


if __name__ == "__main__":
    main()
