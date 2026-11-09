"""컨트롤러 GPO 파일에서 위치·프로파일을 메모리로 복원. Home·이동 없음.

파일이 컨트롤러에 먼저 저장되어 있어야 하며 기존 메모리 값을 갱신합니다.

상단 설정을 확인하고 IDE에서 실행하세요. 자동 재시도하지 않습니다.
"""

import sys
from pathlib import Path

# IDE에서 파일을 직접 실행해도 examples 패키지를 찾도록 SDK 루트를 지정합니다.
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))


from pf400 import PF400
from examples.common.initialization import configure_session


HOST = "192.168.0.1"
ROBOT_ID = 1
PORT = 10100
STATUS_PORT = 10000
TIMEOUT = 10.0
LOAD_FILE = "Tcs_example.gpo"  # 컨트롤러의 파일명.


def main():
    with PF400(HOST, port=PORT, status_port=STATUS_PORT, timeout=TIMEOUT) as robot:
        configure_session(robot, robot_id=ROBOT_ID)
        print("Load reply:", robot.load_file(LOAD_FILE).raw)


if __name__ == "__main__":
    main()
