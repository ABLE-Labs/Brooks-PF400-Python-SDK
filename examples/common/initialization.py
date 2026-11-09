"""예제 공통 준비 코드. import만 해서는 연결하거나 동작하지 않습니다.

각 예제의 연결 코드 다음 configure_session(), 필요한 경우 initialize_robot()을
명시적으로 호출합니다. 프로파일과 MSpeed는 motion_profiles.json에서 읽습니다. 그리퍼 값은 아래에서 수정하세요.
"""

import math

from pf400 import ProtocolError

from .motion_profiles import apply_profiles, load_profiles

GRIPPER_OPEN = 100.0
GRIPPER_CLOSE = 70.0
POWER_WAIT = 30.0
INITIALIZE_TIMEOUT = 60.0
HOME_TIMEOUT = 120.0


def validate_number(value, name):
    if type(value) not in (int, float):
        raise ValueError(f"{name}에는 숫자를 입력하세요.")
    try:
        finite = math.isfinite(value)
    except OverflowError:
        finite = False
    if not finite:
        raise ValueError(f"{name}에는 유한한 숫자를 입력하세요.")


def validate_values(values, name, *, count=None):
    if not isinstance(values, (list, tuple)) or not 1 <= len(values) <= 12:
        raise ValueError(f"{name}에는 숫자 1~12개로 구성된 리스트/튜플을 입력하세요.")
    if count is not None and len(values) != count:
        raise ValueError(f"{name}에는 값 {count}개가 필요합니다.")
    for value in values:
        validate_number(value, name)


def validate_profile(index, *, registered=True, profiles=None):
    if type(index) is not int or index < 1:
        raise ValueError("PROFILE_INDEX는 1 이상의 정수여야 합니다.")
    if index > 20:
        raise ValueError("PROFILE_INDEX는 제공된 TCS의 1~20 범위여야 합니다.")
    if registered:
        data = load_profiles() if profiles is None else profiles
        if str(index) not in data["profiles"]:
            raise ValueError(f"프로파일 파일에 {index}번을 먼저 저장하세요.")


def configure_session(robot, *, robot_id=1):
    """Normal 모드와 제어 대상을 양쪽 연결에 설정합니다. 전원/이동 명령은 없습니다."""
    if type(robot_id) is not int or robot_id < 1:
        raise ValueError("ROBOT_ID는 1 이상의 정수여야 합니다.")
    robot.mode(0, channel="motion")
    robot.mode(0, channel="status")
    robot.select_robot(robot_id, channel="motion")
    robot.select_robot(robot_id, channel="status")
    print("Session ready; robot:", robot_id)


def initialize_robot(robot, *, open_gripper=False, home=False, profiles=None):
    """세션 설정 후 호출. 프로파일/그리퍼 설정 → 전원 → Attach → 선택적 Home/개폐.

    오류는 그대로 전달하며 자동 재시도하지 않습니다. 저장/정지/전원 OFF에는
    이 함수를 무조건 호출하지 않습니다. 현재 자세와 보유 물체를 바꿀 수 있습니다.
    """
    from .motion_profiles import validate_profiles

    profiles = load_profiles() if profiles is None else validate_profiles(profiles)
    for name, value in (
        ("GRIPPER_OPEN", GRIPPER_OPEN),
        ("GRIPPER_CLOSE", GRIPPER_CLOSE),
        ("POWER_WAIT", POWER_WAIT),
        ("INITIALIZE_TIMEOUT", INITIALIZE_TIMEOUT),
        ("HOME_TIMEOUT", HOME_TIMEOUT),
    ):
        validate_number(value, name)
    if POWER_WAIT <= 0 or HOME_TIMEOUT <= 0 or INITIALIZE_TIMEOUT <= POWER_WAIT:
        raise ValueError("대기 시간은 양수이며 INITIALIZE_TIMEOUT은 POWER_WAIT보다 커야 합니다.")

    print("Clear free mode:", robot.free_mode(-1).raw)
    apply_profiles(robot, profiles)
    print("GripOpenPos:", robot.grip_open_pos(GRIPPER_OPEN).raw)
    print("GripClosePos:", robot.grip_close_pos(GRIPPER_CLOSE).raw)
    # 기존 hp 1 -1의 무제한 대기 대신 유한한 전원 대기/통신 제한을 사용합니다.
    print("Power:", robot.hp(1, wait=POWER_WAIT, timeout=INITIALIZE_TIMEOUT).raw)
    print("Attach:", robot.attach(1).raw)
    if home:
        home_if_needed(robot)
    if open_gripper:
        print("Gripper open:", robot.gripper(1).raw)


def _is_homed(robot):
    values = robot.pd(2800, channel="status").as_ints()
    if len(values) != 1 or values[0] not in (0, 1):
        raise ProtocolError("Pd 2800의 원점 상태는 0 또는 1이어야 합니다.")
    return values[0] == 1


def home_if_needed(robot):
    """원점이 미완료일 때만 Home을 실행하고 결과를 다시 확인합니다."""
    if _is_homed(robot):
        print("Already homed")
        return
    print("Home:", robot.home(timeout=HOME_TIMEOUT).raw)
    if not _is_homed(robot):
        raise RuntimeError("Home 응답 후에도 원점 완료가 확인되지 않아 다음 동작을 중단합니다.")
    print("Home complete")
