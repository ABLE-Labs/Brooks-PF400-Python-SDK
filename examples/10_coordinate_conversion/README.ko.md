# 10 · 좌표 변환

[English](README.md) · [예제 안내서](../README.md)

컨트롤러에서 관절 좌표와 직교 좌표를 서로 변환합니다. 로봇은 움직이지 않습니다.

## 파일

| 파일 | 설명 | 로봇 동작 |
|---|---|---|
| [10_joint_to_cartesian.py](10_joint_to_cartesian.py) | 관절 → 직교 (`convert_joint_to_cartesian()`) | 조회만 |
| [10_cartesian_to_joint.py](10_cartesian_to_joint.py) | 직교 → 관절 (`convert_cartesian_to_joint()`) | 조회만 |

## 설정

| 변수 | 기본값 | 사용 파일 | 설명 |
|---|---|---|---|
| `JOINTS` | `None` | 관절 → 직교 | 축 순서대로의 관절 값 (직선 축 mm, 회전 축 deg). 실제 축 개수와 같아야 합니다 |
| `POSE` | `None` | 직교 → 관절 | `[X, Y, Z, yaw, pitch, roll]` — 위치 mm, 회전 deg |
| `CONFIG` | `None` | 직교 → 관절 | 로봇 자세 설정값. `None`이면 펌웨어 기본값 `0`이며, 현재 자세를 자동으로 고르지 않습니다 |

`JOINTS` 또는 `POSE`를 입력하기 전에는 실행되지 않습니다.

## 출력

- 관절 → 직교: `[X, Y, Z, yaw, pitch, roll, config]`
- 직교 → 관절: 축 순서대로의 관절 값

## 실행

```bash
python examples/10_coordinate_conversion/10_joint_to_cartesian.py
python examples/10_coordinate_conversion/10_cartesian_to_joint.py
```
