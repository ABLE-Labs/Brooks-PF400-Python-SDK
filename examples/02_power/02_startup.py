"""로봇 연결 → 설정 → 전원 → Attach → 필요 시 Home → 그리퍼 열기.

상단 IP를 수정하고 이 파일을 실행하세요. 실제 장비가 준비 동작을 수행합니다.
"""

import sys
from pathlib import Path

# IDE에서 파일을 직접 실행해도 examples 패키지를 찾도록 SDK 루트를 지정합니다.
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))


from pf400 import PF400
from examples.common.motion_profiles import PROFILE_FILE, load_profiles, profile_values

HOST = "192.168.0.1"
ROBOT_ID = 1
PORT = 10100
STATUS_PORT = 10000
TIMEOUT = 30.0


def main():
    profiles = load_profiles(PROFILE_FILE)  # 연결 전에 검증
    robot = PF400(HOST, port=PORT, status_port=STATUS_PORT, timeout=TIMEOUT)
    try:
        # 1. TCP 연결
        robot.connect()

        # 2. 명령 형식과 제어 대상 설정
        robot.mode(0, channel="motion")
        robot.mode(0, channel="status")
        robot.select_robot(ROBOT_ID, channel="motion")
        robot.select_robot(ROBOT_ID, channel="status")
        robot.free_mode(-1)  # 수동 모드 종료

        # 3. 이동 프로파일과 그리퍼 위치 설정 (숫자는 예시)
        # 프로파일: Speed, Speed2, Accel, Decel, AccRamp, DecRamp, InRange, Straight
        robot.mspeed(profiles["master_speed"])
        for index, profile in profiles["profiles"].items():
            robot.profile(int(index), profile_values(profile))
        robot.grip_open_pos(100.0)
        robot.grip_close_pos(70.0)

        # 4. 전원 ON 및 제어권 연결
        robot.hp(1, wait=30.0, timeout=60.0)
        robot.attach(1)

        # 5. 원점 미완료일 때만 Home. 완료 전에는 그리퍼를 열지 않습니다.
        homed = robot.pd(2800, channel="status").as_ints()
        if homed == (0,):
            robot.home(timeout=120.0)
            if robot.pd(2800, channel="status").as_ints() != (1,):
                raise RuntimeError("원점 완료가 확인되지 않았습니다.")
        elif homed != (1,):
            raise RuntimeError("원점 상태 응답을 확인할 수 없습니다.")

        # 6. 그리퍼 열기
        robot.gripper(1)
        print("로봇 사용 준비 완료")
        # 계속 제어하려면 이 위치에 사용자 SDK 호출 코드를 추가하세요.
    finally:
        # 통신만 닫습니다. 전원 OFF는 02_shutdown.py를 참고하세요.
        robot.disconnect()


if __name__ == "__main__":
    main()
