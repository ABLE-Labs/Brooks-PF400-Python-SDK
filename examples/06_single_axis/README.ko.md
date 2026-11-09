# 06 · 단일 축 이동

[English](README.md) · [예제 안내서](../README.md)

축 하나를 절대 목표 위치로 이동하고 동작이 끝날 때까지 기다립니다.

> [!WARNING]
> 실제로 로봇이 움직이는 예제입니다. 주변을 비운 뒤 실행하세요.

## 파일

| 파일 | 설명 | 로봇 동작 |
|---|---|---|
| [06_single_axis_motion.py](06_single_axis_motion.py) | `move_one_axis()`로 `AXIS`를 `TARGET_POSITION`에 이동하고 `wait_for_eom()`으로 대기 | 전원 ON, 필요 시 Home, 이동 |

## 설정

| 변수 | 기본값 | 설명 |
|---|---|---|
| `AXIS` | `1` | 축 번호 (1~12, 실제 축 개수 이하) |
| `TARGET_POSITION` | `None` | 절대 목표 위치이며 이동량이 아닙니다. 단위는 축 정의를 따릅니다. 입력하기 전에는 실행되지 않습니다 |
| `PROFILE_INDEX` | `1` | 프로파일 슬롯. [config/motion_profiles.json](../config/motion_profiles.json)에 등록되어 있어야 합니다 |
| `MOTION_TIMEOUT` | `120.0` | 동작 완료 대기 시간 [s] |

## 동작 순서

1. 연결 전에 `AXIS`, `TARGET_POSITION`, 프로파일 파일을 검증합니다.
2. 세션을 설정하고 `AXIS`가 실제 축 개수 이내인지 확인합니다.
3. 공통 초기화와 필요 시 Home을 수행합니다([common](../common/) 참고).
4. 이동 전 관절 좌표를 출력하고 `move_one_axis(AXIS, TARGET_POSITION, PROFILE_INDEX)` 후 완료를 기다린 뒤 다시 출력합니다.

## 참고

- 타임아웃은 대기만 멈춥니다. 로봇을 정지시키지 않습니다.

## 실행

```bash
python examples/06_single_axis/06_single_axis_motion.py
```
