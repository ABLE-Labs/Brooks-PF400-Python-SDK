"""설정값을 PC JSON에 저장합니다. 장비에 접속하거나 값을 적용하지 않습니다.

파라미터 의미·단위·제조사 출처는 README.md의 03 설명을 참고하세요.
기존 다른 슬롯은 유지합니다. 손상된 기존 파일은 덮어쓰지 않습니다.
"""

import sys
from pathlib import Path

# IDE에서 파일을 직접 실행해도 examples 패키지를 찾도록 SDK 루트를 지정합니다.
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))


from examples.common.motion_profiles import PROFILE_FILE, load_profiles, save_profiles

PROFILE_INDEX = 1  # 슬롯 번호 1~20.
MASTER_SPEED = 20.0  # 시스템 전체 속도 배율 [%].
SPEED = 10.0  # 기준 최고 속도 대비 [%].
SPEED2 = 10.0  # Cartesian 이동 중 일부 축의 보조 속도 [%]. 0=보조값 무시.
ACCEL = 10.0  # 기준 최고 가속도 대비 [%].
DECEL = 10.0  # 기준 최고 감속도 대비 [%].
ACC_RAMP = 0.2  # 가속도 램프 시간 [s]. 전체 가속 시간이 아닙니다.
DEC_RAMP = 0.2  # 감속도 램프 시간 [s].
IN_RANGE = 0.0  # 단위 없음. <0 블렌딩, 0 정지/오차 조건 없음, >0 오차 판정.
STRAIGHT = 0  # 단위 없음. 0=관절 보간, 1=Cartesian 직선 경로.


def main():
    if type(PROFILE_INDEX) is not int or not 1 <= PROFILE_INDEX <= 20:
        raise ValueError("PROFILE_INDEX는 1~20 정수여야 합니다.")
    # 최초 파일이 없을 때만 새 저장소를 만듭니다. 파싱 오류는 그대로 전달합니다.
    try:
        data = load_profiles(PROFILE_FILE)
    except FileNotFoundError:
        data = {"master_speed": MASTER_SPEED, "profiles": {}}
    data["master_speed"] = MASTER_SPEED
    data["profiles"][str(PROFILE_INDEX)] = {
        "speed": SPEED, "speed2": SPEED2, "accel": ACCEL, "decel": DECEL,
        "acc_ramp": ACC_RAMP, "dec_ramp": DEC_RAMP, "in_range": IN_RANGE, "straight": STRAIGHT,
    }
    save_profiles(PROFILE_FILE, data)
    print("Saved on PC:", PROFILE_FILE, "profile:", PROFILE_INDEX)
    print("장비 적용은 03_profile_apply.py 또는 시작 초기화에서 수행합니다.")


if __name__ == "__main__":
    main()
