# 13 · PC 티칭 위치

[English](README.md) · [예제 안내서](../README.md)

이름을 붙인 관절 좌표를 PC의 JSON 파일에 저장하고, 목록을 보고, 저장한 위치로 이동합니다.
위치는 [config/teaching_positions.json](../config/teaching_positions.json)에 저장됩니다.

## 파일

| 파일 | 설명 | 로봇 동작 |
|---|---|---|
| [13_positions_list.py](13_positions_list.py) | 저장된 위치 목록 출력 | 없음 (접속 안 함) |
| [13_position_save.py](13_position_save.py) | 현재 관절 좌표를 `POSITION_NAME`으로 저장 | 조회만 (PC 파일 저장) |
| [13_position_move.py](13_position_move.py) | 저장 위치로 `move_j()` 이동 후 대기 | 전원 ON, 필요 시 Home, 이동 |

## 설정

| 변수 | 기본값 | 사용 파일 | 설명 |
|---|---|---|---|
| `POSITION_NAME` | `"position_a"` (save) / `None` (move) | save, move | 위치 이름. 같은 이름으로 저장하면 갱신됩니다. move 파일은 입력하기 전에는 실행되지 않습니다 |
| `PROFILE_INDEX` | `1` | move | 프로파일 슬롯. [config/motion_profiles.json](../config/motion_profiles.json)에 등록되어 있어야 합니다 |
| `MOTION_TIMEOUT` | `120.0` | move | 동작 완료 대기 시간 [s] |

## 동작 순서

- **저장:** 현재 관절 좌표를 읽어 JSON 파일에 씁니다. 다른 위치와 메타데이터는 유지합니다.
  손상된 JSON 파일은 오류를 내며 덮어쓰지 않습니다.
- **이동:** 저장 좌표의 축 개수가 실제 로봇과 같은지 확인하고, 공통 초기화와 필요 시 Home을 수행한 뒤
  ([common](../common/) 참고) `move_j()`로 이동하고 완료를 기다립니다.

> [!WARNING]
> 기본 JSON 파일에는 저장된 위치가 없습니다. 먼저 `13_position_save.py`로 저장하세요.
> 축 구성이 다른 로봇에서 저장한 좌표를 재사용하지 마세요.

## 참고

- 그리퍼를 자동으로 열지 않습니다. 저장 좌표에 그리퍼 축이 포함되어 있으면 그 축도 움직입니다.
- [14](../14_free_mode/)와 함께 손으로 위치를 잡을 수 있습니다: 수동 모드 → 손으로 이동 → 저장 → 복원 → 이동.

## 실행

```bash
python examples/13_teaching_positions/13_positions_list.py
python examples/13_teaching_positions/13_position_save.py
python examples/13_teaching_positions/13_position_move.py
```
