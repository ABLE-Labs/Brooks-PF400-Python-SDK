"""고객이 입력한 직교 목표로 이동한 뒤 완료를 기다립니다."""

import sys
from pathlib import Path

# IDE에서 파일을 직접 실행해도 examples 패키지를 찾도록 SDK 루트를 지정합니다.
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))


from examples.common.initialization import configure_session, initialize_robot, validate_values, validate_profile

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
# 입력 형식 예시: TARGET_POSE = [300.0, 0.0, 200.0, 0.0, 0.0, 0.0]
# 실제 도달 가능 여부·자세·주변 간섭은 검증하지 않은 예시입니다.
TARGET_POSE = None  # [X, Y, Z, yaw, pitch, roll]
CONFIG = None  # 예: CONFIG = 0. None이면 제조사 기본값 사용.


def main():
    if TARGET_POSE is None:
        raise ValueError("TARGET_POSE에 장비에서 확인한 직교 좌표 6개를 입력하세요.")
    validate_values(TARGET_POSE, "TARGET_POSE", count=6)
    profiles = load_profiles(PROFILE_FILE)
    validate_profile(PROFILE_INDEX, profiles=profiles)
    if CONFIG is not None and type(CONFIG) is not int:
        raise ValueError("CONFIG는 정수여야 합니다.")
    with PF400(HOST, port=PORT, status_port=STATUS_PORT, timeout=TIMEOUT) as robot:
        configure_session(robot, robot_id=ROBOT_ID)
        initialize_robot(robot, open_gripper=False, home=True, profiles=profiles)
        print("Before:", robot.where_c().values)
        print("Move reply:", robot.move_c(PROFILE_INDEX, TARGET_POSE, config=CONFIG).raw)
        robot.wait_for_eom(timeout=MOTION_TIMEOUT)
        print("After:", robot.where_c().values)


if __name__ == "__main__":
    main()
