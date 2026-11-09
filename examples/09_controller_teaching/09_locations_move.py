"""컨트롤러 GPO를 불러온 뒤 지정한 슬롯으로 이동하고 완료를 기다립니다.

실제 이동 예제입니다. 저장 좌표와 경로를 확인하고 LOCATION_INDEX를 지정하세요.
전원·Attach·필요 시 Home을 수행합니다. 그리퍼 개폐는 하지 않습니다.
"""

import sys
from pathlib import Path

# IDE에서 파일을 직접 실행해도 examples 패키지를 찾도록 SDK 루트를 지정합니다.
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from pf400 import PF400
from examples.common.initialization import (
    INITIALIZE_TIMEOUT,
    POWER_WAIT,
    configure_session,
    home_if_needed,
    validate_number,
    validate_profile,
)

HOST = "192.168.0.1"
ROBOT_ID = 1
PORT = 10100
STATUS_PORT = 10000
TIMEOUT = 10.0
LOAD_FILE = "Tcs_example.gpo"  # 컨트롤러에 저장된 파일명. PC 경로가 아닙니다.
LOCATION_INDEX = 1  # GPO에 저장된, 이동 경로를 확인한 슬롯 번호로 변경하세요.
PROFILE_INDEX = 1  # GPO에서 불러올 이동 프로파일 번호.
MSPEED = 20.0  # 전체 속도 배율 [%]. GPO 프로파일의 속도에도 적용됩니다.
MOTION_TIMEOUT = 120.0  # 완료 대기 [s]. 타임아웃은 물리 정지가 아닙니다.


def main():
    if type(LOCATION_INDEX) is not int or LOCATION_INDEX < 1:
        raise ValueError("LOCATION_INDEX에 GPO에 저장된 1 이상의 슬롯 번호를 지정하세요.")
    validate_profile(PROFILE_INDEX, registered=False)
    validate_number(MSPEED, "MSPEED")
    if not 0 < MSPEED <= 100:
        raise ValueError("MSPEED는 0 초과 100 이하로 지정하세요.")
    validate_number(MOTION_TIMEOUT, "MOTION_TIMEOUT")
    if MOTION_TIMEOUT <= 0:
        raise ValueError("MOTION_TIMEOUT은 양수여야 합니다.")
    with PF400(HOST, port=PORT, status_port=STATUS_PORT, timeout=TIMEOUT) as robot:
        configure_session(robot, robot_id=ROBOT_ID)
        print("Load reply:", robot.load_file(LOAD_FILE).raw)
        print("Target location:", robot.loc(LOCATION_INDEX).raw)
        print("Loaded profile:", robot.profile(PROFILE_INDEX).raw)
        # PC JSON을 적용하는 initialize_robot() 대신 GPO의 프로파일을 그대로 사용합니다.
        print("Clear free mode:", robot.free_mode(-1).raw)
        print("MSpeed:", robot.mspeed(MSPEED).raw)
        print("Power:", robot.hp(1, wait=POWER_WAIT, timeout=INITIALIZE_TIMEOUT).raw)
        print("Attach:", robot.attach(1).raw)
        home_if_needed(robot)
        print("Move reply:", robot.move(LOCATION_INDEX, PROFILE_INDEX).raw)
        robot.wait_for_eom(timeout=MOTION_TIMEOUT)
        print("Move complete")


if __name__ == "__main__":
    main()
