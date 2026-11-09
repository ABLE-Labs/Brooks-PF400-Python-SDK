# 05 · 직교 좌표 이동

[English](README.md) · [예제 안내서](../README.md)

Cartesian 목표 좌표로 이동하고 동작이 끝날 때까지 기다립니다.

> [!WARNING]
> 실제로 로봇이 움직이는 예제입니다. 도달 가능 여부, 자세, 주변 간섭은 확인하지 않습니다.
> 장비에서 확인한 좌표를 입력하고 주변을 비운 뒤 실행하세요.

## 파일

| 파일 | 설명 | 로봇 동작 |
|---|---|---|
| [05_cartesian_motion.py](05_cartesian_motion.py) | `move_c()`로 `TARGET_POSE`에 이동하고 `wait_for_eom()`으로 대기 | 전원 ON, 필요 시 Home, 이동 |

## 설정

| 변수 | 기본값 | 설명 |
|---|---|---|
| `TARGET_POSE` | `None` | `[X, Y, Z, yaw, pitch, roll]` — 위치 mm, 회전 deg. 입력하기 전에는 실행되지 않습니다 |
| `CONFIG` | `None` | 로봇 자세 설정값(정수). `None`이면 펌웨어 기본값 사용 |
| `PROFILE_INDEX` | `1` | 프로파일 슬롯. [config/motion_profiles.json](../config/motion_profiles.json)에 등록되어 있어야 합니다 |
| `MOTION_TIMEOUT` | `120.0` | 동작 완료 대기 시간 [s] |

## 동작 순서

1. 연결 전에 좌표, `CONFIG`, 프로파일 파일을 검증합니다.
2. 세션을 설정하고 공통 초기화와 필요 시 Home을 수행합니다([common](../common/) 참고).
3. 이동 전 직교 좌표를 출력하고 `move_c(PROFILE_INDEX, TARGET_POSE, config=CONFIG)` 후 완료를 기다린 뒤 다시 출력합니다.

## 참고

- 이동 경로는 프로파일의 `straight` 값으로 정해집니다. 기본 JSON의 1·2번은 `straight=0`(관절 보간)입니다.
  직선 경로가 필요하면 [03](../03_profiles/)에서 `straight=1`인 프로파일을 저장하세요.
- 타임아웃은 대기만 멈춥니다. 로봇을 정지시키지 않습니다.

## 실행

```bash
python examples/05_cartesian_motion/05_cartesian_motion.py
```
