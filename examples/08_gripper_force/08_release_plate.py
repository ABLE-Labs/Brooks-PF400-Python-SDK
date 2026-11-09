"""힘 제한 잡기 해제 후 완료 대기. Home·자동 열기 없음.

상단 설정을 확인하고 IDE에서 실행하세요. 자동 재시도하지 않습니다.
"""

import sys
from pathlib import Path

# IDE에서 파일을 직접 실행해도 examples 패키지를 찾도록 SDK 루트를 지정합니다.
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))


from pf400 import PF400
from examples.common.initialization import configure_session
from examples.common.initialization import initialize_robot, validate_number
from examples.common.motion_profiles import PROFILE_FILE, load_profiles

HOST = "192.168.0.1"
ROBOT_ID = 1
PORT = 10100
STATUS_PORT = 10000
TIMEOUT = 10.0
WIDTH = 85.0  # 해제 목표 폭 [mm]. 물체가 풀리는 폭으로 설정.
SPEED = 20.0  # 기준 속도 대비 [%].
IN_RANGE = 0.0  # 단위 없음. 독립 해제 예제이므로 블렌딩(음수)은 사용하지 않음.
MOTION_TIMEOUT = 120.0  # 완료 대기 [s].


def main():
    profiles = load_profiles(PROFILE_FILE)
    for name, value in (("WIDTH", WIDTH), ("SPEED", SPEED), ("IN_RANGE", IN_RANGE)):
        validate_number(value, name)
    if IN_RANGE < 0:
        raise ValueError("독립 해제 예제의 IN_RANGE는 0 이상이어야 합니다.")
    with PF400(HOST, port=PORT, status_port=STATUS_PORT, timeout=TIMEOUT) as robot:
        configure_session(robot, robot_id=ROBOT_ID)
        initialize_robot(robot, profiles=profiles, open_gripper=False)
        print("Release reply:", robot.release_plate(WIDTH, SPEED, in_range=IN_RANGE).raw)
        robot.wait_for_eom(timeout=MOTION_TIMEOUT)
        print("Release motion ended")


if __name__ == "__main__":
    main()
