"""PC 티칭 JSON 읽기·저장 공통 함수. 장비 연결 없음."""

import json
import math
import os
import tempfile
from pathlib import Path

JSON_FILE = Path(__file__).resolve().parents[1] / "config" / "teaching_positions.json"

def validate_joints(joints):
    """JSON 숫자 배열만 허용합니다. 축의 실제 단위·순서는 컨트롤러 정의를 따릅니다."""
    if not isinstance(joints, list) or not 1 <= len(joints) <= 12:
        raise ValueError("joints는 숫자 1~12개로 구성된 리스트여야 합니다.")
    for value in joints:
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise ValueError("joints에는 문자열이나 bool이 아닌 숫자를 입력하세요.")
        try:
            finite = math.isfinite(value)
        except OverflowError:
            finite = False
        if not finite:
            raise ValueError("joints에는 유한한 숫자만 입력하세요.")
    return list(joints)


def validate_name(name):
    if not isinstance(name, str) or not name.strip():
        raise ValueError("위치 이름은 비어 있지 않은 문자열이어야 합니다.")


def read_positions(path):
    """파일이 없으면 빈 목록. 잘못된 JSON은 덮어쓰지 않고 오류를 전달합니다."""
    path = Path(path)
    if not path.exists():
        return {"positions": {}}
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict) or not isinstance(data.get("positions"), dict):
        raise ValueError("JSON 최상위에는 positions 객체가 필요합니다.")
    for name, position in data["positions"].items():
        validate_name(name)
        if not isinstance(position, dict):
            raise ValueError(f"위치 {name!r}는 joints를 포함한 객체여야 합니다.")
        validate_joints(position.get("joints"))
    return data


def load_position(path, name):
    validate_name(name)
    positions = read_positions(path)["positions"]
    if name not in positions:
        raise ValueError(f"저장된 위치 {name!r}가 없습니다. 먼저 13_position_save.py로 저장하세요.")
    return list(positions[name]["joints"])


def save_position(path, name, joints):
    """같은 이름은 갱신하고 다른 위치는 유지합니다. 임시 파일 완성 후 교체합니다."""
    validate_name(name)
    joints = validate_joints(joints)
    path = Path(path)
    data = read_positions(path)
    # 해당 위치의 추가 메타데이터도 보존합니다.
    position = data["positions"].setdefault(name, {})
    position["joints"] = joints
    text = json.dumps(data, ensure_ascii=False, indent=2, allow_nan=False) + "\n"
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
