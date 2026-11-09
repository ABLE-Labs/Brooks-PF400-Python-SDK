"""상태 채널로 Halt를 호출합니다. 제어 앱에서는 기존 SDK 객체를 재사용하세요."""

from pf400 import PF400

# 실제 장비 주소와 필요한 값으로 수정한 뒤 이 파일을 실행하세요.
HOST = "192.168.0.1"
PORT = 10100
STATUS_PORT = 10000
TIMEOUT = 10.0
ROBOT_ID = 1
# 이 파일을 실행하면 아래 main()에서 Halt 명령을 전송합니다.
# 다른 앱이 로봇 포트를 점유 중일 때 새 프로세스로 실행하는 정지 도구는 아닙니다.


def stop_robot(robot, robot_id):
    """제어 중인 SDK 객체를 받아 motion 완료 대기와 별도로 정지를 요청합니다."""
    if type(robot_id) is not int or robot_id < 1:
        raise ValueError("robot_id는 1 이상의 정수여야 합니다.")
    # 정지 전에 전원 ON·그리퍼·Home 초기화를 실행하지 않습니다.
    robot.select_robot(robot_id, channel="status")
    return robot.halt(channel="status")


def main():
    with PF400(HOST, port=PORT, status_port=STATUS_PORT, timeout=TIMEOUT) as robot:
        print("Halt reply:", stop_robot(robot, ROBOT_ID).raw)
        print("Motion state:", robot.state(channel="status").values)


if __name__ == "__main__":
    main()
