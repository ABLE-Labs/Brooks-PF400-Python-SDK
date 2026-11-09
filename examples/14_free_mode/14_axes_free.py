"""선택한 축을 수동 모드로 전환. 종료 후에도 유지되며 restore가 별도로 필요합니다.

상단 설정을 확인하고 IDE에서 실행하세요. 자동 재시도하지 않습니다.
"""

import sys
from pathlib import Path

# IDE에서 파일을 직접 실행해도 examples 패키지를 찾도록 SDK 루트를 지정합니다.
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))


from pf400 import PF400
from examples.common.initialization import configure_session
from examples.common.initialization import initialize_robot
from examples.common.motion_profiles import PROFILE_FILE, load_profiles

HOST = "192.168.0.1"
ROBOT_ID = 1
PORT = 10100
STATUS_PORT = 10000
TIMEOUT = 10.0
AXES = [1, 2, 3, 4]  # 1부터 시작. 장비 정지 상태에서만 사용.


def main():
    if not isinstance(AXES, list) or not AXES:
        raise ValueError("AXES에는 축 번호 목록이 필요합니다.")
    if any(type(axis) is not int or not 1 <= axis <= 12 for axis in AXES):
        raise ValueError("축 번호는 1~12 정수여야 합니다.")
    if len(set(AXES)) != len(AXES):
        raise ValueError("중복 축 번호를 제거하세요.")
    profiles = load_profiles(PROFILE_FILE)
    with PF400(HOST, port=PORT, status_port=STATUS_PORT, timeout=TIMEOUT) as robot:
        configure_session(robot, robot_id=ROBOT_ID)
        axis_count = len(robot.where_j().as_floats())
        if any(axis > axis_count for axis in AXES):
            raise ValueError("실제 축 개수를 초과했습니다.")
        initialize_robot(robot, profiles=profiles, open_gripper=False)
        for axis in AXES:
            print("Free axis:", axis, robot.free_mode(axis).raw)
        print("수동 모드 유지 중. 14_axes_restore.py로 복원하세요. 오류 시에도 자동 복원하지 않습니다.")


if __name__ == "__main__":
    main()
