"""PC 프로파일 저장소. 파일 읽기/저장만으로 장비에 접속하지 않습니다."""

import json
import math
import os
import tempfile
from pathlib import Path

PROFILE_FILE = Path(__file__).resolve().parents[1] / "config" / "motion_profiles.json"
PROFILE_FIELDS = (
    "speed", "speed2", "accel", "decel", "acc_ramp", "dec_ramp", "in_range", "straight",
)


def validate_profiles(data):
    if not isinstance(data, dict) or set(data) != {"master_speed", "profiles"}:
        raise ValueError("설정에는 master_speed와 profiles가 필요합니다.")
    profiles = data["profiles"]
    if not isinstance(profiles, dict) or not profiles:
        raise ValueError("profiles에는 프로파일을 하나 이상 등록하세요.")
    numbers = [("master_speed", data["master_speed"])]
    for key, profile in profiles.items():
        if not isinstance(key, str) or not key.isascii() or not key.isdecimal():
            raise ValueError("프로파일 번호는 1~20의 문자열이어야 합니다.")
        if not 1 <= int(key) <= 20 or str(int(key)) != key:
            raise ValueError("프로파일 번호는 1~20의 문자열이어야 합니다.")
        if not isinstance(profile, dict) or set(profile) != set(PROFILE_FIELDS):
            raise ValueError(f"프로파일 {key}에는 {PROFILE_FIELDS} 필드가 필요합니다.")
        numbers.extend((f"profiles.{key}.{field}", profile[field]) for field in PROFILE_FIELDS)
        if type(profile["straight"]) is not int or profile["straight"] not in (0, 1):
            raise ValueError("straight는 정수 0 또는 1이어야 합니다.")
    for name, value in numbers:
        try:
            valid = type(value) in (int, float) and math.isfinite(value)
        except OverflowError:
            valid = False
        if not valid:
            raise ValueError(f"{name}에는 유한한 숫자가 필요합니다.")
    return data


def load_profiles(path=PROFILE_FILE):
    """누락·손상 파일은 오류. 숨은 기본값으로 운전을 계속하지 않습니다."""
    return validate_profiles(json.loads(Path(path).read_text(encoding="utf-8")))


def save_profiles(path, data):
    """전체 내용을 검증한 뒤 같은 디렉터리에서 원자적으로 교체합니다."""
    validate_profiles(data)
    text = json.dumps(data, ensure_ascii=False, indent=2, allow_nan=False) + "\n"
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w", encoding="utf-8", dir=path.parent, prefix=path.name + ".", suffix=".tmp", delete=False
        ) as stream:
            temporary = Path(stream.name)
            stream.write(text)
        os.replace(temporary, path)
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)


def profile_values(profile):
    return [profile[field] for field in PROFILE_FIELDS]


def apply_profiles(robot, data):
    """검증한 데이터를 전송합니다. 전원·Home·그리퍼 동작은 수행하지 않습니다."""
    validate_profiles(data)
    print("Master speed:", robot.mspeed(data["master_speed"]).raw)
    for key, profile in sorted(data["profiles"].items(), key=lambda item: int(item[0])):
        print("Profile:", key, robot.profile(int(key), profile_values(profile)).raw)
