"""한 축을 절대 목표 위치로 이동합니다."""

import sys
from pathlib import Path

# IDE에서 파일을 직접 실행해도 examples 패키지를 찾도록 SDK 루트를 지정합니다.
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))


from examples.common.initialization import configure_session, initialize_robot, validate_number, validate_profile

from pf400 import PF400
from examples.common.motion_profiles import PROFILE_FILE, load_profiles

# 실제 장비 주소와 필요한 값으로 수정한 뒤 이 파일을 실행하세요.
HOST = "192.168.0.1"
ROBOT_ID = 1
PORT = 10100
STATUS_PORT = 10000
TIMEOUT = 10.0
MOTION_TIMEOUT = 120.0  # 완료 대기 [s]. 타임아웃은 물리 정지가 아닙니다.
PROFILE_INDEX = 1
AXIS = 1  # 축 번호 예시. 실제 장비의 축 정의 확인.
# 입력 형식 예시: TARGET_POSITION = 100.0
TARGET_POSITION = None  # 확인한 절대 목표를 입력. 이동량이 아니며 단위는 축 정의 확인.


def main():
    if AXIS is None or TARGET_POSITION is None:
        raise ValueError("AXIS와 TARGET_POSITION을 입력하세요.")
    if type(AXIS) is not int or not 1 <= AXIS <= 12:
        raise ValueError("AXIS는 1~12 범위의 정수여야 합니다.")
    validate_number(TARGET_POSITION, "TARGET_POSITION")
    profiles = load_profiles(PROFILE_FILE)
    validate_profile(PROFILE_INDEX, profiles=profiles)
    with PF400(HOST, port=PORT, status_port=STATUS_PORT, timeout=TIMEOUT) as robot:
        configure_session(robot, robot_id=ROBOT_ID)
        axis_count = len(robot.where_j().as_floats())
        if AXIS > axis_count:
            raise ValueError(f"장비 축 번호 범위는 1~{axis_count}입니다.")
        initialize_robot(robot, open_gripper=False, home=True, profiles=profiles)
        print("Before:", robot.where_j().values)
        print("Move reply:", robot.move_one_axis(AXIS, TARGET_POSITION, PROFILE_INDEX).raw)
        robot.wait_for_eom(timeout=MOTION_TIMEOUT)
        print("After:", robot.where_j().values)


if __name__ == "__main__":
    main()
