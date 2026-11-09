# 09 · 컨트롤러 티칭

[English](README.md) · [예제 안내서](../README.md)

컨트롤러의 위치 슬롯에 현재 위치를 티칭하고, 컨트롤러의 GPO 파일로 저장·복원하고, 저장된 슬롯으로 이동합니다.

## 파일

| 파일 | 설명 | 로봇 동작 |
|---|---|---|
| [09_location_show.py](09_location_show.py) | 위치 슬롯 하나 조회(`loc()`) | 조회만 |
| [09_teach_joint.py](09_teach_joint.py) | 현재 관절 좌표를 슬롯에 저장(`here_j()`) | 컨트롤러 메모리 갱신 |
| [09_teach_cartesian.py](09_teach_cartesian.py) | 현재 직교 좌표를 슬롯에 저장(`here_c()`) | 컨트롤러 메모리 갱신 |
| [09_locations_store.py](09_locations_store.py) | 컨트롤러의 위치·프로파일을 GPO 파일로 저장(`store_file()`) | 컨트롤러 파일 저장 |
| [09_locations_load.py](09_locations_load.py) | GPO 파일의 위치·프로파일을 메모리로 복원(`load_file()`) | 컨트롤러 메모리 덮어쓰기 |
| [09_locations_move.py](09_locations_move.py) | GPO 파일을 불러와 슬롯으로 이동(`move()`) | 전원 ON, 필요 시 Home, 이동 |

## 설정

| 변수 | 기본값 | 사용 파일 | 설명 |
|---|---|---|---|
| `LOCATION_INDEX` | `1` (show, teach) / `None` (move) | show, teach, move | 위치 슬롯 번호 (1 이상). move 파일은 입력하기 전에는 실행되지 않습니다 |
| `SAVE_FILE` / `LOAD_FILE` | `"Tcs_example.gpo"` | store / load, move | 컨트롤러의 파일명. PC 경로가 아닙니다 |
| `PROFILE_INDEX` | `1` | move | GPO에서 불러온 프로파일 번호 |
| `MSPEED` | `20.0` | move | 전체 속도 배율 [%], 0 초과 100 이하 |
| `MOTION_TIMEOUT` | `120.0` | move | 동작 완료 대기 시간 [s] |

## 사용 순서

1. 로봇을 원하는 위치에 두고 **teach**(관절 또는 직교)를 실행합니다. **show**로 확인합니다.
2. **store**로 슬롯을 컨트롤러의 GPO 파일에 저장합니다.
3. 컨트롤러를 재부팅한 뒤에는 **load**로 복원합니다. 부팅 시 자동으로 실행되지 않습니다.
4. **move**로 슬롯 위치로 이동합니다. `LOCATION_INDEX`는 위치와 경로를 확인한 슬롯으로 지정하세요.

`09_locations_move.py`는 GPO 파일을 불러오고 목표 슬롯과 프로파일을 출력한 뒤, 수동 모드 종료, `MSPEED` 설정,
전원 ON, Attach, 필요 시 Home을 거쳐 `move(LOCATION_INDEX, PROFILE_INDEX)`를 호출하고 완료를 기다립니다.
GPO의 프로파일을 그대로 사용하며 PC 프로파일 JSON은 적용하지 않습니다. 그리퍼는 열거나 닫지 않습니다.

> [!WARNING]
> `09_locations_move.py`는 실제로 로봇을 움직입니다. 이동 경로의 간섭은 확인하지 않습니다.

## 참고

- teach와 load는 컨트롤러 메모리의 기존 값을 덮어씁니다. teach는 Home이나 이동을 하지 않습니다.
- GPO 파일은 컨트롤러에 있으며 [config](../config/)의 PC JSON 파일과 별개입니다.

## 실행

```bash
python examples/09_controller_teaching/09_teach_joint.py
python examples/09_controller_teaching/09_location_show.py
python examples/09_controller_teaching/09_locations_store.py
python examples/09_controller_teaching/09_locations_load.py
python examples/09_controller_teaching/09_locations_move.py
```
