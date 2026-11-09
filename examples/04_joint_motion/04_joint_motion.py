"""파일 상단에 입력한 관절 목표로 이동한 뒤 완료를 기다립니다."""

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
# 실제 장비의 축 개수와 순서에 맞는 확인된 좌표 리스트를 입력하세요.
# 6축 입력 형식 예시: TARGET_JOINTS = [100.0, 0.0, 45.0, -45.0, 0.0, 90.0]
# 위 숫자는 검증된 목표가 아닙니다. 축 순서·단위를 확인한 실제 좌표로 바꾸세요.
TARGET_JOINTS = None


def main():
    if TARGET_JOINTS is None:
        raise ValueError("TARGET_JOINTS에 장비에서 확인한 관절 좌표를 입력하세요.")
    validate_values(TARGET_JOINTS, "TARGET_JOINTS")
    profiles = load_profiles(PROFILE_FILE)
    validate_profile(PROFILE_INDEX, profiles=profiles)
    with PF400(HOST, port=PORT, status_port=STATUS_PORT, timeout=TIMEOUT) as robot:
        configure_session(robot, robot_id=ROBOT_ID)
        axis_count = len(robot.where_j().as_floats())
        if len(TARGET_JOINTS) != axis_count:
            raise ValueError(f"장비 축 {axis_count}개에 맞는 TARGET_JOINTS가 필요합니다.")
        initialize_robot(robot, open_gripper=False, home=True, profiles=profiles)
        print("Before:", robot.where_j().values)
        print("Move reply:", robot.move_j(PROFILE_INDEX, TARGET_JOINTS).raw)
        robot.wait_for_eom(timeout=MOTION_TIMEOUT)
        print("After:", robot.where_j().values)


if __name__ == "__main__":
    main()
