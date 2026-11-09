# common · 예제 공통 모듈

[English](README.md) · [예제 안내서](../README.md)

예제 스크립트가 함께 쓰는 보조 모듈입니다. import만으로는 로봇에 연결하거나, 파일을 쓰거나, 동작하지 않습니다.
`examples.common.<모듈>` 형태로 가져오며, `examples` 패키지를 찾을 수 있도록 IDE에서 SDK 루트 폴더를 여세요.

## 파일

| 파일 | 내용 |
|---|---|
| [initialization.py](initialization.py) | 입력 검사, 세션 설정, 로봇 초기화 |
| [motion_profiles.py](motion_profiles.py) | [config/motion_profiles.json](../config/motion_profiles.json) 읽기·검증·저장·적용 |
| [teaching_positions.py](teaching_positions.py) | [config/teaching_positions.json](../config/teaching_positions.json) 읽기·검증·저장 |

## initialization.py

| 함수 | 설명 |
|---|---|
| `configure_session(robot, robot_id=1)` | 양쪽 채널에 Normal 모드(`mode(0)`)와 로봇을 설정. 전원·이동 없음 |
| `initialize_robot(robot, open_gripper=False, home=False, profiles=None)` | 제어 준비 (아래 순서) |
| `home_if_needed(robot)` | `pd(2800)`이 원점 미완료일 때만 `home()` 실행 후 다시 확인 |
| `validate_number()` / `validate_values()` / `validate_profile()` | 연결 전에 쓰는 입력 검사 |

`initialize_robot()` 순서:

```text
free_mode(-1)                       수동 모드 종료
mspeed / profile                    config/motion_profiles.json 값
grip_open_pos / grip_close_pos      GRIPPER_OPEN / GRIPPER_CLOSE
hp(1, wait=POWER_WAIT)              전원 ON, INITIALIZE_TIMEOUT
attach(1)
home_if_needed()                    home=True일 때만
gripper(1)                          open_gripper=True일 때만
```

오류는 그대로 전달하며 재시도하지 않습니다. 로봇 자세와 잡고 있는 물체를 바꿀 수 있으므로,
조회·저장·정지·전원 OFF·복원 예제에서는 호출하지 않습니다.

| 상수 | 값 | 설명 |
|---|---|---|
| `GRIPPER_OPEN` / `GRIPPER_CLOSE` | `100.0` / `70.0` | 초기화 때 설정하는 그리퍼 위치 [mm] |
| `POWER_WAIT` | `30.0` | `hp()`에 전달하는 전원 대기 시간 [s] |
| `INITIALIZE_TIMEOUT` | `60.0` | 전원 ON 통신 제한 시간 [s] (`POWER_WAIT`보다 커야 함) |
| `HOME_TIMEOUT` | `120.0` | `home()` 제한 시간 [s] |

## motion_profiles.py

| 이름 | 설명 |
|---|---|
| `PROFILE_FILE` | `config/motion_profiles.json`의 절대 경로. 작업 디렉터리와 무관 |
| `load_profiles(path)` | 파일을 읽고 검증. 파일이 없거나 잘못되면 오류 |
| `save_profiles(path, data)` | 검증 후 파일을 원자적으로 교체 |
| `apply_profiles(robot, data)` | MSpeed와 모든 프로파일 전송. 전원·Home·그리퍼 동작 없음 |
| `validate_profiles()` / `profile_values()` | 검증, 8개 인자 리스트로 변환 |

## teaching_positions.py

| 이름 | 설명 |
|---|---|
| `JSON_FILE` | `config/teaching_positions.json`의 절대 경로 |
| `read_positions(path)` | 파일을 읽고 검증. 파일이 없으면 빈 목록 |
| `load_position(path, name)` | `name`으로 저장된 관절 좌표 반환 |
| `save_position(path, name, joints)` | `name`을 추가·갱신하고 다른 항목은 유지하며 파일을 원자적으로 교체 |
| `validate_joints()` / `validate_name()` | 입력 검사 |
