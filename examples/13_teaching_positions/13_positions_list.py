"""PC JSON의 티칭 위치 목록만 조회. 장비에 접속하지 않습니다."""

import sys
from pathlib import Path

# IDE에서 파일을 직접 실행해도 examples 패키지를 찾도록 SDK 루트를 지정합니다.
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))


from examples.common.teaching_positions import JSON_FILE, read_positions


def main():
    positions = read_positions(JSON_FILE)["positions"]
    if not positions:
        print("저장된 위치가 없습니다.")
    for name, position in positions.items():
        print(name, position["joints"])


if __name__ == "__main__":
    main()
