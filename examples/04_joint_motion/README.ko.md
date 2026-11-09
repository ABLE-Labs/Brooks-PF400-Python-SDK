# 04 · 관절 이동

[English](README.md) · [예제 안내서](../README.md)

관절 목표 위치로 이동하고 동작이 끝날 때까지 기다립니다.

> [!WARNING]
> 실제로 로봇이 움직이는 예제입니다. 장비에서 확인한 목표값을 입력하고 주변을 비운 뒤 실행하세요.

## 파일

| 파일 | 설명 | 로봇 동작 |
|---|---|---|
| [04_joint_motion.py](04_joint_motion.py) | `move_j()`로 `TARGET_JOINTS`에 이동하고 `wait_for_eom()`으로 대기 | 전원 ON, 필요 시 Home, 이동 |

## 설정

| 변수 | 기본값 | 설명 |
|---|---|---|
| `TARGET_JOINTS` | `None` | 관절 목표 리스트. 실제 축 개수·순서와 같아야 합니다. 입력하기 전에는 실행되지 않습니다 |
| `PROFILE_INDEX` | `1` | 프로파일 슬롯. [config/motion_profiles.json](../config/motion_profiles.json)에 등록되어 있어야 합니다 |
| `MOTION_TIMEOUT` | `120.0` | 동작 완료 대기 시간 [s] |

## 동작 순서

1. 연결 전에 목표값과 프로파일 파일을 검증합니다.
2. 세션을 설정하고 `TARGET_JOINTS` 개수가 실제 축 개수와 같은지 확인합니다.
3. 공통 초기화와 필요 시 Home을 수행합니다(`initialize_robot(..., home=True)`, [common](../common/) 참고).
4. 이동 전 관절 좌표를 출력하고 `move_j(PROFILE_INDEX, TARGET_JOINTS)` 후 완료를 기다린 뒤 다시 출력합니다.

## 참고

- 그리퍼를 자동으로 열지 않습니다. 목표값에 그리퍼 축이 포함되어 있으면 그 값으로 그리퍼가 움직입니다.
- 타임아웃은 대기만 멈춥니다. 로봇을 정지시키지 않습니다.

## 실행

```bash
python examples/04_joint_motion/04_joint_motion.py
```
