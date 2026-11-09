# 14 · 수동 모드

[English](README.md) · [예제 안내서](../README.md)

선택한 축을 수동 모드로 바꿔 손으로 움직일 수 있게 하고, 작업 후 모든 축을 복원합니다.

> [!WARNING]
> 로봇이 정지한 상태에서만 사용하세요. 수동 모드는 스크립트가 끝나거나 오류가 나도 유지됩니다.
> 종료하려면 `14_axes_restore.py`를 실행하세요.

## 파일

| 파일 | 설명 | 로봇 동작 |
|---|---|---|
| [14_axes_free.py](14_axes_free.py) | 초기화 후 `AXES`의 각 축에 `free_mode(axis)` 호출 | 전원 ON, 선택 축 수동 모드 |
| [14_axes_restore.py](14_axes_restore.py) | 모든 축의 수동 모드 종료(`free_mode(-1)`) | 모든 축 복원 |

## 설정

`14_axes_free.py`

| 변수 | 기본값 | 설명 |
|---|---|---|
| `AXES` | `[1, 2, 3, 4]` | 수동 모드로 바꿀 축 번호 (1~12, 중복 없이, 실제 축 개수 이하) |

`14_axes_restore.py`에는 접속 설정만 있습니다. `AXES`와 관계없이 모든 축을 복원합니다.

## 동작 순서

- **수동 모드:** `AXES`가 실제 축 개수 이내인지 확인하고, Home 없이 공통 초기화를 수행한 뒤
  ([common](../common/) 참고) 선택한 축만 수동 모드로 바꿉니다.
- **복원:** 모든 축의 수동 모드를 종료합니다. 전원 ON, Home, 그리퍼 초기화는 하지 않습니다.

## 참고

- 수동 모드는 서보 전원 OFF나 브레이크 해제와 다릅니다.
- [13](../13_teaching_positions/)과 함께 쓰는 순서: 수동 모드 → 손으로 이동 → 13 저장 → 복원 → 13 이동.

## 실행

```bash
python examples/14_free_mode/14_axes_free.py
python examples/14_free_mode/14_axes_restore.py
```
