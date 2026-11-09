# 07 · 그리퍼

[English](README.md) · [예제 안내서](../README.md)

서보 그리퍼의 개방·닫힘 위치를 조회·설정하고, 그리퍼를 열거나 닫습니다.

## 파일

| 파일 | 설명 | 로봇 동작 |
|---|---|---|
| [07_gripper_read.py](07_gripper_read.py) | 개방·닫힘 위치 조회 | 조회만 |
| [07_gripper_settings.py](07_gripper_settings.py) | 개방·닫힘 위치 설정. 실제로 열거나 닫지 않음 | 설정만 |
| [07_gripper_open.py](07_gripper_open.py) | 초기화 후 위치를 적용하고 그리퍼 열기(`gripper(1)`) | 전원 ON, 필요 시 Home, 그리퍼 열기 |
| [07_gripper_close.py](07_gripper_close.py) | 초기화 후 위치를 적용하고 그리퍼 닫기(`gripper(2)`) | 전원 ON, 필요 시 Home, 그리퍼 닫기 |

## 설정

`07_gripper_settings.py`, `07_gripper_open.py`, `07_gripper_close.py`

| 변수 | 기본값 | 설명 |
|---|---|---|
| `OPEN_POSITION` | `100.0` | 개방 위치 [mm] |
| `CLOSE_POSITION` | `80.0` | 닫힘 위치 [mm] |

값을 바꾸기 전에 사용하는 그리퍼의 허용 범위를 확인하세요.

## 동작 순서

`07_gripper_open.py` / `07_gripper_close.py`

1. 연결 전에 프로파일 파일과 위치값을 검증합니다.
2. 공통 초기화와 필요 시 Home을 수행합니다([common](../common/) 참고).
   이때 `common/initialization.py`의 위치(`100.0` / `70.0` mm)가 먼저 설정됩니다.
3. 파일의 `OPEN_POSITION` / `CLOSE_POSITION`을 적용한 뒤 그리퍼를 열거나 닫습니다.

## 참고

- Home으로 현재 로봇 자세가 바뀔 수 있습니다. 물체를 잡고 있다면 열기·닫기 전에 확인하세요.
- 그리퍼 위치는 이동 프로파일 JSON에 저장하지 않습니다.

## 실행

```bash
python examples/07_gripper/07_gripper_read.py
python examples/07_gripper/07_gripper_settings.py
python examples/07_gripper/07_gripper_open.py
python examples/07_gripper/07_gripper_close.py
```
