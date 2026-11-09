# 08 · 힘 제한 잡기

[English](README.md) · [예제 안내서](../README.md)

힘을 제한해 물체를 잡고 놓습니다.

> [!WARNING]
> 그리퍼가 실제로 움직이는 예제입니다. 실제 잡는 힘은 마찰, 스프링 등에 따라 달라질 수 있습니다.

## 파일

| 파일 | 설명 | 로봇 동작 |
|---|---|---|
| [08_grasp_plate.py](08_grasp_plate.py) | `grasp_plate()`로 잡고, 성공이 확인되지 않으면 오류로 중단 | 전원 ON, 필요 시 Home, 잡기 |
| [08_release_plate.py](08_release_plate.py) | `release_plate()`로 놓고 `wait_for_eom()`으로 대기 | 전원 ON, 놓기 (Home 없음) |

## 설정

`08_grasp_plate.py`

| 변수 | 기본값 | 설명 |
|---|---|---|
| `WIDTH` | `85.0` | 물체 폭 [mm]. 약 1 mm 이내로 정확히 입력 |
| `SPEED` | `20.0` | 그리퍼 속도 [%] |
| `FORCE` | `5.0` | 잡는 힘 [N]. 양수는 닫아서 잡기, 음수는 열어서 잡기 |

`08_release_plate.py`

| 변수 | 기본값 | 설명 |
|---|---|---|
| `WIDTH` | `85.0` | 해제 목표 폭 [mm]. 물체가 풀리는 폭 |
| `SPEED` | `20.0` | 속도 [%] |
| `IN_RANGE` | `0.0` | `0` 이상이어야 합니다 (단독 해제이므로 블렌딩 사용 안 함) |
| `MOTION_TIMEOUT` | `120.0` | 동작 완료 대기 시간 [s] |

## 동작 순서

- **잡기:** 공통 초기화와 필요 시 Home을 수행한 뒤([common](../common/) 참고) `grasp_plate(WIDTH, SPEED, FORCE)`를 호출합니다.
  응답 데이터가 `-1`일 때만 성공이며, `0`이나 그 밖의 값이면 `RuntimeError`로 중단합니다.
- **놓기:** Home과 그리퍼 열기 없이 초기화한 뒤 `release_plate(WIDTH, SPEED, in_range=IN_RANGE)`를 호출하고
  완료를 기다립니다. `IN_RANGE=0`은 위치 오차가 안정될 때까지 보장하지 않습니다.

## 실행

```bash
python examples/08_gripper_force/08_grasp_plate.py
python examples/08_gripper_force/08_release_plate.py
```
