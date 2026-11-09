# PF400 SDK 작업별 실행 예제

상단 Python 변수에 IP·목표·설정 파일 경로를 입력하고 IDE에서 원하는 작업 파일을 실행합니다.
한 파일이 한 작업을 수행합니다. `ACTION` 값으로 작업을 전환하지 않습니다.
명령줄 옵션은 없습니다. import만으로 장비 연결·초기화·파일 저장을 하지 않습니다.

## 폴더 구조

```text
examples/
├── 01_connection/           연결·상태
├── 02_power/                시작·종료
├── 03_profiles/             프로파일 저장·적용·조회
├── 04_joint_motion/         관절 이동
├── 05_cartesian_motion/     Cartesian 목표 이동
├── 06_single_axis/          단일 축 이동
├── 07_gripper/              그리퍼 조회·설정·개폐
├── 08_gripper_force/        힘 제한 잡기·해제
├── 09_controller_teaching/  컨트롤러 티칭
├── 10_coordinate_conversion/ 좌표 변환
├── 11_stop/                 정지
├── 12_error_handling/       오류 처리
├── 13_teaching_positions/   PC 티칭 목록·저장·이동
├── 14_free_mode/            수동 모드·복원
├── async/                   비동기 조회
├── common/                  공통 Python 모듈
└── config/                  프로파일·티칭 JSON
```

각 하위 폴더의 Python 파일을 IDE에서 직접 실행할 수 있습니다.
공통 모듈은 `from examples.common...` 형태로 가져옵니다. IDE에서는 SDK 루트 폴더를 프로젝트로 여세요.
파일 직접 실행 시 SDK 루트를 등록하므로 실행 작업 디렉터리에 의존하지 않습니다.
common과 config도 필요하므로 examples 전체 폴더 구조를 유지하세요.

## 폴더별 안내

각 폴더의 README에 파일별 설정, 동작 순서, 로봇 동작 여부가 정리되어 있습니다.

| 폴더 | 내용 | 안내 |
|---|---|---|
| 01_connection | 연결·상태 | [한국어](01_connection/README.ko.md) · [English](01_connection/README.md) |
| 02_power | 시작·종료 | [한국어](02_power/README.ko.md) · [English](02_power/README.md) |
| 03_profiles | 프로파일 저장·적용·조회 | [한국어](03_profiles/README.ko.md) · [English](03_profiles/README.md) |
| 04_joint_motion | 관절 이동 | [한국어](04_joint_motion/README.ko.md) · [English](04_joint_motion/README.md) |
| 05_cartesian_motion | Cartesian 목표 이동 | [한국어](05_cartesian_motion/README.ko.md) · [English](05_cartesian_motion/README.md) |
| 06_single_axis | 단일 축 이동 | [한국어](06_single_axis/README.ko.md) · [English](06_single_axis/README.md) |
| 07_gripper | 그리퍼 조회·설정·개폐 | [한국어](07_gripper/README.ko.md) · [English](07_gripper/README.md) |
| 08_gripper_force | 힘 제한 잡기·해제 | [한국어](08_gripper_force/README.ko.md) · [English](08_gripper_force/README.md) |
| 09_controller_teaching | 컨트롤러 티칭 | [한국어](09_controller_teaching/README.ko.md) · [English](09_controller_teaching/README.md) |
| 10_coordinate_conversion | 좌표 변환 | [한국어](10_coordinate_conversion/README.ko.md) · [English](10_coordinate_conversion/README.md) |
| 11_stop | 정지 | [한국어](11_stop/README.ko.md) · [English](11_stop/README.md) |
| 12_error_handling | 오류 처리 | [한국어](12_error_handling/README.ko.md) · [English](12_error_handling/README.md) |
| 13_teaching_positions | PC 티칭 목록·저장·이동 | [한국어](13_teaching_positions/README.ko.md) · [English](13_teaching_positions/README.md) |
| 14_free_mode | 수동 모드·복원 | [한국어](14_free_mode/README.ko.md) · [English](14_free_mode/README.md) |
| async | 비동기 조회 | [한국어](async/README.ko.md) · [English](async/README.md) |
| common | 공통 Python 모듈 | [한국어](common/README.ko.md) · [English](common/README.md) |
| config | 프로파일·티칭 JSON | [한국어](config/README.ko.md) · [English](config/README.md) |

## 공통 파일

- `config/motion_profiles.json`: PC에 영구 보관하는 MSpeed와 번호별 이동 프로파일.
- `common/motion_profiles.py`: 설정 파일 검증·읽기·원자적 저장·장비 적용 함수.
- `common/initialization.py`: 세션 설정과 제어 준비. 프로파일·MSpeed는 JSON에서 읽습니다.
- `config/teaching_positions.json`: 이름별 관절 좌표. 기본 파일에는 저장된 위치가 없습니다.
- `common/teaching_positions.py`: 티칭 JSON 읽기·저장 공통 함수.

SDK와 **examples 폴더 전체를 같은 버전으로** 받으세요.
wheel에는 예제가 없으며, sdist에는 공통 Python 파일·JSON·안내서가 함께 포함됩니다.

## 실행할 파일 선택

| 번호 | 파일 | 수행 작업 |
|---|---|---|
| 01 | `01_connection/01_connect_and_status.py` | 연결·상태 조회 |
| 02 | `02_power/02_startup.py` / `02_power/02_shutdown.py` | 사용 시작 / 종료 |
| 03 | `03_profiles/03_profile_save.py` | 상단 설정값을 PC JSON에 저장. 장비 접속 없음 |
| 03 | `03_profiles/03_profile_apply.py` | JSON의 MSpeed·모든 프로파일을 장비에 적용 |
| 03 | `03_profiles/03_profile_read.py` | 장비의 MSpeed·선택 프로파일 조회만 수행 |
| 04 | `04_joint_motion/04_joint_motion.py` | 관절 목표로 이동 |
| 05 | `05_cartesian_motion/05_cartesian_motion.py` | Cartesian 좌표 목표로 이동 |
| 06 | `06_single_axis/06_single_axis_motion.py` | 단일 축의 절대 목표 위치로 이동 |
| 07 | `07_gripper/07_gripper_read.py` | 개폐 위치 조회만 수행 |
| 07 | `07_gripper/07_gripper_settings.py` | 개폐 위치 설정. 실제 개폐·전원 ON 없음 |
| 07 | `07_gripper/07_gripper_open.py` / `07_gripper/07_gripper_close.py` | 그리퍼 열기 / 닫기 |
| 08 | `08_gripper_force/08_grasp_plate.py` / `08_gripper_force/08_release_plate.py` | 힘 제한 잡기 / 해제 |
| 09 | `09_controller_teaching/09_location_show.py` | 컨트롤러 위치 슬롯 조회 |
| 09 | `09_controller_teaching/09_teach_joint.py` / `09_controller_teaching/09_teach_cartesian.py` | 현재 관절 / Cartesian 좌표 티칭 |
| 09 | `09_controller_teaching/09_locations_store.py` | 컨트롤러 위치·프로파일을 GPO로 저장 |
| 09 | `09_controller_teaching/09_locations_load.py` | 컨트롤러 GPO에서 위치·프로파일 복원 |
| 09 | `09_controller_teaching/09_locations_move.py` | GPO를 불러온 뒤 지정 슬롯으로 이동 |
| 10 | `10_coordinate_conversion/10_joint_to_cartesian.py` / `10_coordinate_conversion/10_cartesian_to_joint.py` | 좌표 변환 방향별 실행 |
| 11 | `11_stop/11_stop.py` | 연결된 객체의 status 채널로 Halt |
| 12 | `12_error_handling/12_error_handling.py` | 조회·세션 오류 처리 예제 |
| 13 | `13_teaching_positions/13_positions_list.py` | PC 티칭 목록 조회. 장비 접속 없음 |
| 13 | `13_teaching_positions/13_position_save.py` / `13_teaching_positions/13_position_move.py` | 현재 좌표를 PC에 저장 / 저장 좌표로 이동 |
| 14 | `14_free_mode/14_axes_free.py` / `14_free_mode/14_axes_restore.py` | 선택 축 수동 모드 / 모든 축 복원 |

## 접속과 초기화

`HOST`, `ROBOT_ID`, `PORT`, `STATUS_PORT`, `TIMEOUT`은 각 파일 상단에서 수정합니다.
기본 IP `192.168.0.1`은 예시입니다. 같은 로봇 포트에 여러 앱을 동시에 연결하지 마세요.
세션 설정은 양쪽 채널의 `Mode 0`과 `SelectRobot`을 명시적으로 호출합니다.

`02_power/02_startup.py`는 JSON을 읽은 뒤 필요한 SDK 명령을 코드에 직접 표시합니다.
제어 준비가 필요한 다른 예제는 연결 전에 JSON과 입력값을 검사하고,
`initialize_robot(robot, profiles=profiles, ...)`로 다음 순서를 수행합니다.

```text
FreeMode -1
Mspeed <JSON master_speed>
Profile <JSON의 각 슬롯과 8개 필드>
GripOpenPos / GripClosePos
Hp 1 30  (통신 제한 60초)
Attach 1
필요 시 Pd 2800 → Home → 원점 완료 재확인
open_gripper=True일 때만 Gripper 1
```

일반 이동(04~06·13)은 그리퍼를 자동으로 열지 않습니다.
그리퍼 축을 포함한 목표 관절 좌표를 입력하면 그 목표값에 따라 그리퍼가 움직일 수 있습니다.
02 시작 예제는 원점 확인 후 그리퍼를 엽니다.
07 개폐·08 잡기는 필요 시 Home을 수행하므로 현재 로봇 자세가 바뀔 수 있습니다.
08 해제와 14 수동 모드는 자동 Home·개폐를 수행하지 않습니다.
조회·좌표 저장·변환·정지·수동 모드 복원에는 공통 제어 초기화를 넣지 않습니다.
오류 시 후속 단계로 진행하거나 자동 재전송하지 않습니다.

## 03. 속도·프로파일 저장과 적용

프로파일 설정의 기준은 **PC의 `config/motion_profiles.json` 한 곳**입니다.
각 예제의 `PROFILE_FILE`은 기본적으로 examples/config에 있는 이 파일의 절대 경로를 사용합니다.
필요하면 다른 PC 설정 파일 경로를 지정할 수 있습니다.
작업 디렉터리가 달라도 기본 경로는 같은 파일을 가리킵니다.

```json
{
  "master_speed": 20.0,
  "profiles": {
    "1": {
      "speed": 10.0, "speed2": 10.0, "accel": 10.0, "decel": 10.0,
      "acc_ramp": 0.2, "dec_ramp": 0.2, "in_range": 0.0, "straight": 0
    }
  }
}
```

1. `03_profiles/03_profile_save.py`에서 번호·MSpeed·8개 필드 값을 지정하고 실행합니다.
   선택 슬롯만 추가·갱신하고 다른 슬롯은 유지합니다. MSpeed는 전체 공통값으로 갱신됩니다.
   최초 파일이 없으면 새로 만들고, 기존 파일이 손상되었으면 오류를 내며 덮어쓰지 않습니다.
   장비에서 현재 값을 캡처하는 기능은 아니며 **상단 Python 변수값을 PC에 저장**합니다.
2. `03_profiles/03_profile_apply.py`를 실행하면 파일의 모든 프로파일과 MSpeed를 장비에 적용합니다.
   여기서는 전원 ON·Attach·Home·그리퍼 개폐를 하지 않습니다.
3. `03_profiles/03_profile_read.py`로 실제 장비 적용값을 조회합니다.
   `PROFILE_INDEX` 슬롯과 MSpeed를 숫자로 비교하세요.

JSON을 직접 편집해도 됩니다. 저장·읽기 시 모든 슬롯을 검증하며 잘못된 필드·번호·비유한 숫자는 거부합니다.
PC 저장과 장비 적용은 별도입니다. 장비에서 값을 바꿔도 PC JSON은 자동 갱신되지 않습니다.
둘이 다를 때 시작 초기화는 **PC 파일값을 장비에 재적용**합니다.
여러 프로그램이 같은 파일에 동시에 저장하는 용도로 설계하지 않았습니다.

### 전원 재인가 후

지원 대상 TCS는 시작할 때 프로파일 객체를 기본값으로 만듭니다.
PC JSON 파일은 전원 재인가와 무관하게 남지만, 장비에는 별도 복원 처리가 없다면 다시 적용해야 합니다.
02 시작 및 제어 예제 초기화가 파일값을 다시 읽어 적용합니다.
이는 컨트롤러 재부팅을 뜻하며 `Hp 0`/`Hp 1`로 구동 전원만 OFF/ON하는 것과 구분합니다.
MSpeed(PDb 601)의 장비 내 유지 여부에도 의존하지 않고 초기화 시 함께 설정합니다.
SDK의 단순 `connect()`나 조회 예제는 설정을 자동 복원하지 않습니다.

### 기본값

JSON의 기본값은 프로파일 1·2(Ramp **0.2초**)와 MSpeed **20%**입니다.
운전값을 바꾸려면 03 저장 예제 또는 JSON을 수정하세요. 모든 숫자는 실장비에서 검증해야 하는 예시값입니다.

### 파라미터 의미와 단위

| Python 변수 / TCS 명령 | 의미 | 단위·해석 | 근거 |
|---|---|---|---|
| `PROFILE_INDEX` / `Profile` 첫 인자 | 선택 로봇의 프로파일 슬롯 번호 | 단위 없음. 지원 대상 TCS는 1~20개 슬롯. 사용 전 공통 JSON에도 등록 필요 | [F] |
| `MASTER_SPEED` / `MSpeed` | 모든 로봇 이동 속도에 적용하는 시스템 배율 | %. `20`은 20%. 선택 프로파일 전용 설정이 아님 | [F] |
| `SPEED` / `Speed` | 해당 이동의 최고 속도 지정 | 기준 속도 대비 %. `100`은 기준 속도. 직선 이동은 Cartesian 경로와 회전, 관절 보간은 관절 기준으로 적용 | [A], [B] |
| `SPEED2` / `Speed2` | Cartesian 이동 중 일부 축의 보조 최고 속도 | 해당 축의 기준 속도 대비 %. GDE 예제는 `0`으로 보조 속도 지정을 무시. 두 번째 동작 단계의 속도가 아님 | [A], [E] |
| `ACCEL` / `Accel` | 최고 가속도 | 기준 가속도 대비 %. mm/s²·deg/s² 직접 입력이 아님 | [A] |
| `DECEL` / `Decel` | 최고 감속도 | 기준 감속도 대비 %. 감속 시간을 직접 지정하는 값이 아님 | [A] |
| `ACC_RAMP` / `AccRamp` → GPL `AccelRamp` | 가속도를 지정 수준까지 올리는 S-curve 램프 시간 | 초(s). 가속도를 다시 0으로 내릴 때도 사용. 전체 가속 시간과 다름 | [A], [C] |
| `DEC_RAMP` / `DecRamp` → GPL `DecelRamp` | 감속도를 지정 수준까지 올리는 S-curve 램프 시간 | 초(s). 전체 감속 시간과 다름 | [A] |
| `IN_RANGE` / `InRange` | 종점 정지 여부와 이동 완료 판정의 위치 오차 조건 | 단위 없음. 거리 mm·시간 s·속도 %가 아님. 부호/크기에 따른 동작은 아래 표 참고 | [D] |
| `STRAIGHT` / `Straight` | 이동 경로 보간 방식 | 단위 없는 논리값. `0`: 관절 보간, `1`: TCP의 Cartesian 직선 경로 | [G], [F] |

접속 변수: `HOST`는 IP/호스트명, `ROBOT_ID`는 대상 로봇 번호,
`PORT`/`STATUS_PORT`는 motion/status TCP 포트, `TIMEOUT`은 SDK 통신 제한 시간(초)입니다.
초기화 중 `Hp`에는 공통 파일의 별도 제한 시간(`INITIALIZE_TIMEOUT`)이 적용됩니다.

### InRange 값의 의미

| 값 | 종점과 완료 판정 |
|---|---|
| `< 0` | 가능하면 다음 이동과 블렌딩. 실제 블렌딩에는 다음 이동이 적시에 주어져야 함 |
| `0` | 종점 정지. 마지막 목표 명령을 서보에 전달하면 완료로 판정하며 위치 오차 조건은 적용하지 않음 |
| 작은 양수 | 종점 정지 후 느슨한 위치 오차 조건으로 완료 판정 |
| `100`에 가까운 양수 | 더 엄격한 위치 오차 조건. `100`은 제조사 기준의 가장 엄격한 오차 범위 |
| `> 100` | 지정 가능하지만 제조사가 권장하는 것보다 작은 오차를 요구 |

`IN_RANGE = 0`의 조회 성공이나 이동 완료 응답을 정밀한 실제 위치 도달 확인과 동일하게 취급하지 않습니다.
특정 InRange 값을 몇 mm로 환산할지는 확인한 문서에 정의되어 있지 않습니다.


### 수치 해석과 결과 확인

Speed2는 두 번째 이동 단계의 속도가 아닙니다. 공식 개요는 Cartesian 이동 중 일부 축의 보조 속도로
정의하며, 확인한 제조사 자료에는 PF400의 구체적 적용 축이 없어 축 번호를 단정하지 않습니다.
Speed의 공식 최소는 0.01이고 최대는 로봇 구성에 따릅니다. 모든 필드의 허용 범위를 일괄 0~100으로 가정하지 않습니다.
Ramp는 전체 가속/감속 시간이 아니며, 이동 거리와 컨트롤러 DB 설정에 따라 실제 적용 시간이 달라질 수 있습니다.
MSpeed와 프로파일 속도를 설정해도 실제 mm/s는 이동 거리·가속·제한에 따라 달라집니다.

장비 조회의 `.values`는 성공 코드 0을 제외한 문자열 튜플입니다.
프로파일은 `[번호, Speed, Speed2, Accel, Decel, AccelRamp, DecelRamp, InRange, Straight]` 순서입니다.
JSON 초기 슬롯 1의 예상 수치는 `[1, 10, 10, 10, 10, 0.2, 0.2, 0, 0]`입니다.
이는 예상값이며 실제 시험 기록이 아닙니다. 설정·조회 확인과 실제 이동 검증은 구분합니다.

### 제조사 근거

- [A] [Brooks GPL — Profile Class Summary](https://www2.brooksautomation.com/Controller_Software/Software_Reference/GPL_Dictionary/Profile_class/profileintro.htm): 속도·가속도 %, Ramp 초, Speed2의 적용 개요.
- [B] [Brooks GPL — Profile.Speed](https://www2.brooksautomation.com/Controller_Software/Software_Reference/GPL_Dictionary/Profile_class/speed_property.htm): 이동 방식별 적용, 기준 속도, 허용 최대 및 실제 속도와의 차이.
- [C] [Brooks GPL — Profile.AccelRamp](https://www2.brooksautomation.com/Controller_Software/Software_Reference/GPL_Dictionary/Profile_class/accelramp.htm): S-curve 시간, 0의 의미, DB 설정의 영향.
- [D] [Brooks GPL — Profile.InRange](https://www2.brooksautomation.com/Controller_Software/Software_Reference/GPL_Dictionary/Profile_class/inrange.htm): 음수·0·양수·100 초과의 의미.
- [E] [Brooks GDE, PN 609737 Rev. A, p.53](https://www.brooksautomation.com/getmedia/af66374f-fb72-49ae-bae6-28ec3106f0a4/GDE.pdf): 예제에서 Speed2=0을 보조 속도 무시로 설명.
- [F] PF400 TCS 펌웨어 소스: `Cmd.gpl`의 `Cmd_Mspeed`(PDb 601),
  `Cmd_Profile`(8개 인자와 조회 순서), `Cmd_Straight`(논리값 변환), `Globals.gpl`의 `N_PROF = 20`.
  SDK의 `docs/firmware_manifest.json`에 프로젝트 버전과 원본 해시가 있습니다.
- [G] [Brooks GPL — Profile.Straight](https://www2.brooksautomation.com/Controller_Software/Software_Reference/GPL_Dictionary/Profile_class/straight.htm): Cartesian 직선/관절 보간 선택.

SDK 기준 펌웨어 소스와 실제 장비에 설치된 펌웨어가 같은지는 확인하지 않았습니다.


## 04~06. 이동

관절 목표는 실제 축 개수·순서에 맞게, Cartesian 목표는 `[X,Y,Z,yaw,pitch,roll]`로 지정합니다.
위치 단위는 mm, 회전각은 deg이며 단일 축 목표는 상대 이동량이 아닌 절대 좌표입니다.
목표 좌표는 기본 `None`으로 두어 입력 없이 이동하지 못하게 했습니다.
`PROFILE_INDEX`는 공통 JSON에 등록된 번호여야 합니다.

05는 Cartesian **목표 좌표** 예제이며 경로 방식은 선택 프로파일의 `straight`로 결정합니다.
초기 JSON의 1·2번은 `straight=0`(관절 보간)입니다. 직선 이동이 필요하면 전용 슬롯을 `straight=1`로 저장하세요.
경로·간섭 확인이나 장애물 회피는 수행하지 않습니다.
`MOTION_TIMEOUT`은 완료 대기 제한(초)입니다. 타임아웃·연결 해제는 물리 정지가 아닙니다.

## 07~08. 그리퍼

07 read는 조회만, settings는 개폐 위치 설정만 수행합니다. 서보 그리퍼 위치는 mm입니다.
open/close 파일은 제어 초기화·필요 시 Home 후 파일 상단의 개폐 위치를 적용하고 선택한 개폐를 실행합니다.
개폐 위치는 이동 프로파일 JSON에 포함하지 않습니다.

08 grasp의 `WIDTH`는 물체 폭(mm), `SPEED`는 %, `FORCE`는 N입니다.
힘 양수는 닫아서 잡기, 음수는 열어서 잡기입니다. 실제 힘은 마찰·스프링 등에 따라 편차가 있습니다.
잡기 응답 데이터가 -1일 때만 성공으로 처리하며, 0 또는 예상 밖 데이터면 오류로 중단합니다.
release는 목표 폭(mm)으로 해제하고 `WaitForEom`으로 기다립니다.
독립 실행 예제이므로 `IN_RANGE`는 0 이상을 사용합니다. 0은 위치 오차 보정 완료까지 보장하지 않습니다.

## 09~10. 컨트롤러 티칭·좌표 변환

09 show는 슬롯 조회만 수행합니다. teach 파일은 현재 좌표로 슬롯을 갱신하며 Home을 하지 않습니다.
장비 재부팅 후 복원이 필요하면 `09_locations_store.py`로 저장한 뒤 `09_locations_load.py`를 실행하세요.
load의 `LOAD_FILE`은 store의 `SAVE_FILE`과 같은 컨트롤러 파일명으로 지정합니다(기본 `Tcs_example.gpo`).
해당 파일이 컨트롤러에 있어야 하며 불러온 위치·프로파일로 기존 메모리 값을 갱신합니다. Home·이동은 하지 않습니다.
부팅 시 자동 실행되는 예제가 아니므로 필요한 시점에 직접 실행하세요.
`09_locations_move.py`는 `LOAD_FILE`을 불러와 `LOCATION_INDEX` 슬롯으로 실제 이동합니다.
`LOCATION_INDEX`의 기본값은 `None`이므로 실행 전 확인한 슬롯 번호를 입력하세요. `PROFILE_INDEX`는 GPO의 프로파일 번호입니다.
슬롯·프로파일 조회 후 수동 모드 해제, `MSPEED` 적용, 전원·Attach·필요 시 Home, `Move`·완료 대기를 수행합니다.
PC 프로파일 JSON으로 덮어쓰지 않으며 그리퍼 개폐는 하지 않습니다. 이동 경로의 간섭은 자동 확인하지 않습니다.
GPO는 컨트롤러 파일이고 PC의 프로파일 JSON·티칭 JSON과 별도입니다.
10은 방향별 파일에서 변환만 수행하며, `CONFIG=None`은 펌웨어 기본값 0을 뜻합니다.

## 11~12. 정지·오류

11의 `stop_robot(robot, robot_id)`은 이미 연결된 SDK 객체의 status 채널을 사용하세요.
별도 앱이 포트를 점유한 상태에서 추가 프로세스로 정지시키는 도구가 아닙니다.
Halt는 급감속이며 전원을 유지합니다. 12는 조회·세션 오류를 출력하고 실패 종료합니다.
연결 해제·Ctrl+C·예외·타임아웃은 물리 정지가 아니며 자동 재시도하지 않습니다.

## 13. PC 티칭 위치

list는 장비에 연결하지 않고 목록을 읽습니다. save는 `POSITION_NAME`에 현재 관절 좌표를 저장합니다.
같은 이름은 갱신하고 다른 위치·메타데이터는 유지합니다. 손상된 JSON을 빈 데이터로 덮어쓰지 않습니다.
move는 `POSITION_NAME`(기본값 `None`)에 저장 위치 이름을 입력해야 실행됩니다.
파일과 축 개수를 검증한 뒤 공통 초기화·필요 시 Home·이동·완료 대기를 수행합니다.
그리퍼 자동 열기는 없지만, 저장 관절 좌표에 그리퍼 축이 포함되면 그 축도 이동 대상입니다.
장비·축 구성이 다른 좌표를 재사용하지 마세요.

## 14. 수동 모드

free 파일의 `AXES=[1,3]`처럼 축 번호를 선택합니다. 실제 축 개수 확인 후 준비하고 선택 축만 풉니다.
장비가 정지한 상태에서 사용하세요. 종료·예외 뒤에도 수동 모드는 자동 복원되지 않습니다.
restore 파일은 AXES와 무관하게 모든 축의 수동 모드를 종료합니다.
FreeMode는 개별 서보 전원 OFF나 브레이크 해제와 다릅니다.
free → 수동 조작 → 13 save → restore → 13 move 순서로 사용할 수 있습니다.

## 검증 범위

예제 자동 검증은 루프백 TCP 모의 서버로 수행합니다. 실장비 동작·위치·힘은 아직 검증하지 않았습니다.
자세한 내용은 [검증 기록](../docs/VALIDATION.md)을 참고하세요.
