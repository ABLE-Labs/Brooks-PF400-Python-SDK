"""PC JSON의 MSpeed와 모든 프로파일을 장비에 적용. 전원·Home·개폐 없음.

상단 설정을 확인하고 IDE에서 실행하세요. 자동 재시도하지 않습니다.
"""

import sys
from pathlib import Path

# IDE에서 파일을 직접 실행해도 examples 패키지를 찾도록 SDK 루트를 지정합니다.
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))


from pf400 import PF400
from examples.common.initialization import configure_session
from examples.common.motion_profiles import PROFILE_FILE, load_profiles, apply_profiles

HOST = "192.168.0.1"
ROBOT_ID = 1
PORT = 10100
STATUS_PORT = 10000
TIMEOUT = 10.0


def main():
    profiles = load_profiles(PROFILE_FILE)
    with PF400(HOST, port=PORT, status_port=STATUS_PORT, timeout=TIMEOUT) as robot:
        configure_session(robot, robot_id=ROBOT_ID)
        apply_profiles(robot, profiles)
        print("Applied from:", PROFILE_FILE)


if __name__ == "__main__":
    main()
