"""힘 제한 잡기. 잡기 실패는 RuntimeError로 전달합니다.

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
WIDTH = 85.0  # 물체 폭 [mm]. 약 1 mm 이내 정확도로 입력.
SPEED = 20.0  # 기준 그리퍼 속도 대비 [%].
FORCE = 5.0  # [N]. 양수=닫아서 잡기, 음수=열어서 잡기.


def main():
    profiles = load_profiles(PROFILE_FILE)
    for name, value in (("WIDTH", WIDTH), ("SPEED", SPEED), ("FORCE", FORCE)):
        validate_number(value, name)
    with PF400(HOST, port=PORT, status_port=STATUS_PORT, timeout=TIMEOUT) as robot:
        configure_session(robot, robot_id=ROBOT_ID)
        initialize_robot(robot, profiles=profiles, open_gripper=False, home=True)
        response = robot.grasp_plate(WIDTH, SPEED, FORCE)
        if response.as_ints() != (-1,):
            raise RuntimeError(f"잡기 성공을 확인하지 못했습니다: {response.raw}")
        print("Grasp confirmed:", response.raw)


if __name__ == "__main__":
    main()
