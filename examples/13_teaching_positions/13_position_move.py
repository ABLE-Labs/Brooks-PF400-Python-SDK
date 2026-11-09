"""PC JSON의 관절 위치로 이동. 그리퍼 자동 열기 없음. 필요 시 Home 수행.

상단 설정을 확인하고 IDE에서 실행하세요. 자동 재시도하지 않습니다.
"""

import sys
from pathlib import Path

# IDE에서 파일을 직접 실행해도 examples 패키지를 찾도록 SDK 루트를 지정합니다.
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))


from pf400 import PF400
from examples.common.initialization import configure_session
from examples.common.initialization import initialize_robot, validate_profile
from examples.common.motion_profiles import PROFILE_FILE, load_profiles
from examples.common.teaching_positions import JSON_FILE, load_position

HOST = "192.168.0.1"
ROBOT_ID = 1
PORT = 10100
STATUS_PORT = 10000
TIMEOUT = 10.0
POSITION_NAME = None  # 13_positions_list.py로 확인한 저장 위치 이름. 예: "position_a"
PROFILE_INDEX = 1
MOTION_TIMEOUT = 120.0  # 완료 대기 [s]. 타임아웃은 물리 정지가 아닙니다.


def main():
    if POSITION_NAME is None:
        raise ValueError("POSITION_NAME에 저장된 위치 이름을 입력하세요.")
    target = load_position(JSON_FILE, POSITION_NAME)
    profiles = load_profiles(PROFILE_FILE)
    validate_profile(PROFILE_INDEX, profiles=profiles)
    with PF400(HOST, port=PORT, status_port=STATUS_PORT, timeout=TIMEOUT) as robot:
        configure_session(robot, robot_id=ROBOT_ID)
        current = robot.where_j().as_floats()
        if len(current) != len(target):
            raise ValueError("장비 축 개수와 저장 좌표 개수가 다릅니다.")
        initialize_robot(robot, profiles=profiles, open_gripper=False, home=True)
        print("Move reply:", robot.move_j(PROFILE_INDEX, target).raw)
        robot.wait_for_eom(timeout=MOTION_TIMEOUT)
        print("After:", robot.where_j().values)


if __name__ == "__main__":
    main()
