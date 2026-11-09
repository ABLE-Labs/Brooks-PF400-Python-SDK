"""사용 종료: 정지 → 수동 모드 종료 → Detach → 전원 OFF → 통신 해제.

초기화나 Home을 먼저 하지 않습니다. 시작 예제와 별도로 실행합니다.
"""

from pf400 import PF400

HOST = "192.168.0.1"
ROBOT_ID = 1
PORT = 10100
STATUS_PORT = 10000
TIMEOUT = 30.0


def main():
    robot = PF400(HOST, port=PORT, status_port=STATUS_PORT, timeout=TIMEOUT)
    try:
        # 1. 연결하고 종료할 로봇 선택
        robot.connect()
        robot.mode(0, channel="motion")
        robot.mode(0, channel="status")
        robot.select_robot(ROBOT_ID, channel="motion")
        robot.select_robot(ROBOT_ID, channel="status")

        # 2. 로봇 정지 및 수동 모드 종료
        robot.halt(channel="status")
        robot.free_mode(-1)

        # 3. 제어권 해제 및 전원 OFF
        robot.attach(0)
        robot.hp(0)
        print("로봇 사용 종료 완료")
    finally:
        # 4. TCP 연결 해제
        robot.disconnect()


if __name__ == "__main__":
    main()
