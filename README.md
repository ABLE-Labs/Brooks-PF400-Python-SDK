# PF400 Python SDK

고객 전달 펌웨어 **Tcp_cmd_server_ablelabs**의 비전 제외 명령 **82개**를 Python으로 호출합니다.
기준 버전 문자열은 `Command Server 3.0D4 10-25-2024`입니다. 런타임 외부 의존성이 없으며 Python 3.10 이상에서 사용할 수 있습니다.

동기 `PF400`과 비동기 `AsyncPF400`은 동일한 메서드와 인자를 제공합니다. 기존 사내 드라이버나 현장별 좌표 파일을 설치할 필요가 없습니다.

**현재 상태: 0.1.0a1 / 개발용 알파. 로컬 TCP 테스트와 패키징을 검증하며 실장비 동작은 미검증입니다.**
Python 버전별 테스트 설정은 CI에 있으며, 실제 실행 결과와 장비 검증은 [검증 기록](docs/VALIDATION.md)에 구분합니다.

## 설치

```powershell
# 저장소에서 개발 설치
python -m pip install -e .

# 제공받은 wheel 설치
python -m pip install .\ablelabs_pf400_sdk-0.1.0a1-py3-none-any.whl
```

배포 이름은 `ablelabs-pf400-sdk`, Python import 이름은 `pf400`입니다. PyPI에 등록된 패키지라는 뜻은 아닙니다.
기존 사내 `pf400` 패키지와 import 이름이 같으므로 새 가상환경에 설치하세요.

## 상태 조회만 실행

```python
from pf400 import PF400

with PF400("192.168.0.1", timeout=5) as robot:
    print(robot.version().data)
    print(robot.where_j().as_floats())
```

연결은 두 TCP 소켓을 여는 작업만 수행합니다. 전원, 모드, 원점, 그리퍼 또는 이동 명령은 자동 실행하지 않습니다.
`connected`는 로컬 소켓의 열림 상태이며 실제 로봇 준비 상태나 통신 생존을 보장하는 상태 값이 아닙니다.

## 기능별 실행 예제

각 파일 상단의 접속·목표값을 수정하고 IDE에서 실행합니다. 한 파일이 한 작업을 수행하며 ACTION 분기는 없습니다.
전체 목록과 초기화 영향은 [예제 안내서](examples/README.md)에 있습니다.

- [사용 시작](examples/02_power/02_startup.py) / [사용 종료](examples/02_power/02_shutdown.py)
- 프로파일 [PC 저장](examples/03_profiles/03_profile_save.py) / [장비 적용](examples/03_profiles/03_profile_apply.py) / [장비 조회](examples/03_profiles/03_profile_read.py)
- [공통 프로파일 JSON](examples/config/motion_profiles.json): MSpeed와 번호별 프로파일을 저장합니다. 시작 초기화가 같은 파일을 읽어 재적용합니다.
- 티칭 위치 [목록](examples/13_teaching_positions/13_positions_list.py) / [저장](examples/13_teaching_positions/13_position_save.py) / [이동](examples/13_teaching_positions/13_position_move.py)
- 축 [수동 모드](examples/14_free_mode/14_axes_free.py) / [복원](examples/14_free_mode/14_axes_restore.py)

공통 파일·JSON이 필요하므로 examples 폴더 전체를 같은 버전으로 받으세요.
저장은 PC 파일 갱신이고 적용은 장비 명령 전송입니다. SDK connect 자체는 설정을 적용하지 않습니다.

## 명령 사용 방식

메서드는 제조사 명령의 의미와 인자 순서를 유지합니다. 관절·직교 좌표는 리스트 또는 튜플로 전달합니다.
모든 메서드에 `channel="motion" | "status"` 및 `timeout=초`를 지정할 수 있습니다.

```python
# 다음은 동작 API의 호출 형태입니다. 실행하면 실제 장비가 동작합니다.
# robot.hp(1, wait=10)
# robot.attach(1)
# robot.home(timeout=120)
# robot.move_j(profile_index=1, joints=target_joints)
# robot.wait_for_eom(timeout=60)
# robot.gripper(1)  # 제조사 정의: 1=open, 2=close
```

이동 응답을 받았다는 사실과 동작 완료는 다를 수 있습니다. 필요한 경우 명시적으로 `wait_for_eom()`을 호출하세요.
`home_all()`은 전체 로봇에 영향을 줍니다. `move_extra_axis()`는 다음 직교 이동의 추가 축 목표 예약이며 즉시 이동이 아닙니다.
`release_plate()`의 세 번째 인자는 프로파일 번호가 아니라 `in_range`입니다. `payload()`는 질량이 아닌 백분율입니다.

### 상태 채널과 정지

기본 명령 채널은 `motion`입니다. `reset()`만 기본 `status`를 사용합니다.
펌웨어 시작 시 상태 채널의 선택 로봇은 0이므로, 로봇별 조회와 정지 전 대상 로봇을 명시적으로 선택해야 합니다.

```python
with PF400("192.168.0.1") as robot:
    robot.select_robot(1, channel="status")
    print(robot.state(channel="status").as_ints())
    # robot.halt(channel="status")  # 이동 대기 중인 motion 채널과 독립적으로 전송
```

`halt()`를 기본 motion 채널로 호출하면 앞 명령이 응답할 때까지 대기할 수 있습니다.
`Halt`는 펌웨어의 급감속 명령이고 전원을 유지합니다. 하드웨어 비상정지와 동일한 기능으로 취급하지 마세요.
`Reset`은 로봇 스레드를 재시작합니다. 펌웨어는 상태 채널의 선택 로봇 번호가 0인 경우에만 허용합니다.
상태 채널을 다른 로봇으로 선택한 후라면 `select_robot(0, channel="status")`를 먼저 호출해야 합니다.

## 반환값과 오류

```python
from pf400 import CommandTimeout, DeviceError

try:
    response = robot.where_j()
    print(response.raw)          # 원문: "0 10.0 20.0 ..."
    print(response.code)         # Normal 모드 성공 코드: 0
    print(response.values)       # 상태 코드 뒤의 필드들: tuple[str, ...]
    print(response.as_floats())  # 필드 전체를 숫자로 변환
except DeviceError as exc:
    print(exc.code, exc.description)  # 알려진 코드의 설명
    print(exc.hint)                   # 확인 사항 (없으면 빈 문자열)
    print(exc.raw)                    # 제조사 원문은 그대로 보존
except CommandTimeout as exc:
    print(exc.command, exc.may_have_executed)
    # 장비 상태와 실제 위치를 확인한 다음 복구 여부를 판단
```

`0 -1`은 성공 응답이며 -1 데이터가 삭제되지 않습니다. `IsFullyClosed`는 듀얼 그리퍼에서 비트마스크를 반환할 수 있으므로 모든 응답을 bool로 강제 변환하지 않습니다.
문자열·좌표·그리퍼 번호 등 각 반환 필드의 의미는 [명령별 레퍼런스](docs/API.md)를 따릅니다.

타임아웃에는 채널 잠금 대기·전송·응답 수신을 포함한 단일 제한 시간을 적용합니다. 전송이 시작됐으면 `may_have_executed=True`입니다.
타임아웃·연결 손실·잘못된 응답 시 해당 연결을 닫아 지연 응답이 다음 명령과 섞이지 않게 합니다.
자동 재시도·재접속·명령 재전송을 하지 않습니다. `connect()`를 명시적으로 다시 호출하기 전 장비 상태를 확인하세요.
연결 해제나 Python 예외는 물리 동작을 정지시키지 않습니다.

오류 메시지에는 알려진 제조사·TCS 코드의 설명과 필요한 확인 사항을 덧붙입니다. [오류 코드 설명](docs/ERRORS.md)을 참고하세요. 전체 제조사 오류 목록은 아니며, 미등록 코드와 원문도 항상 전달합니다.

## 비동기 사용

```python
from pf400 import AsyncPF400

async def read_position():
    async with AsyncPF400("192.168.0.1") as robot:
        return (await robot.where_j()).as_floats()
```

비동기 어댑터는 `asyncio.to_thread`로 블로킹 통신을 이벤트 루프 밖에서 실행합니다.
취소를 요청해도 로봇은 정지하지 않습니다. 통신 작업이 제한 시간 내 종료될 때까지 기다린 뒤 취소를 전달합니다.
동일 채널의 명령은 직렬화되며, motion/status는 독립적으로 사용할 수 있습니다.
펌웨어는 포트별 한 TCP 연결만 처리하므로 같은 로봇 포트에 여러 클라이언트를 동시에 연결하지 마세요.

## 제공 범위

- 펌웨어에 선언된 90개 중 비전 8개를 제외한 82개를 메서드로 제공합니다.
- 제조사 내장 PickPlate / PlacePlate / TeachPlate / 팔레트 명령을 포함합니다.
- 기존 Python의 호텔·플레이트 시퀀스, 자체 기구학 계산, Teach Pendant, 사이트 좌표 파일을 포함하지 않습니다.
- `Custom`은 펌웨어에 포함된 예제 명령이라는 점을 레퍼런스에 표시합니다.
- `execute()`도 등록된 비전 제외 명령만 허용합니다. 비전이나 임의 명령 전달용 우회 API를 제공하지 않습니다.

제외: `Vprocess`, `VresultLoc`, `VresultInfo`, `VresultInspect`, `VToolProperty`, `VresultInfoString`, `StereoParam`, `StereoLocate`.

비전 외 명령도 레일·서보/공압/듀얼 그리퍼·높이 감지 등 장비 구성과 설정에 따라 지원 범위가 달라집니다.
MoveToSafe / ChangeConfig 계열은 원문에 작업 공간 내부 충돌 확인이 없다고 기재되어 있습니다.
PickPlate / PlacePlate 주석에는 `BES NOT UPDATED` 표시가 있어 출하 구성에서 검증해야 합니다.

### 응답 모드

권장 모드는 시작 기본값인 Normal입니다. `mode(1)`은 Telnet 모드, `mode(0)`은 Normal 모드로 전환합니다.
이 값은 서버 전체 채널에 공유되므로 SDK는 전환 중 양쪽 채널을 잠급니다. 다른 클라이언트가 모드를 바꾸면 연결을 다시 설정해야 합니다.
이미 Telnet 모드인 서버에 연결할 때는 `telnet_mode=True`를 생성자에 전달하세요.
Telnet 응답은 사람이 읽는 문자열이므로 `Response.code=None`일 수 있고, 숫자 오류 코드가 없는 응답의 성공 여부를 SDK가 추정하지 않습니다.
모드 전환 중 통신이 실패하면 양쪽 연결을 닫습니다. 서버의 현재 모드를 확인해 일치하는 `telnet_mode`로 새 인스턴스를 만드세요.

## 개발과 배포

```powershell
python -m pip install -e ".[dev]"
python -m pytest
python -m ruff check .
python -m build
```

API는 생성된 명시적 Python 메서드로 제공해 IDE의 서명·문서·타입 표시를 지원합니다.
일반 사용·설치·빌드에 펌웨어 폴더가 필요하지 않습니다.
수정 후 재생성은 `tools/api_spec.py`와 `python tools/generate_api.py --firmware <폴더>`를 사용합니다.
원본 파일별 SHA-256과 소스 위치는 [firmware_manifest.json](docs/firmware_manifest.json)에 기록되어 있습니다.

공개 원격 저장소와 PyPI 업로드는 아직 수행하지 않았습니다. 패키지명은 외부 서비스에서 확보된 이름이 아닙니다.
이 저장소에는 공개 라이선스를 임의로 부여하지 않았습니다. 회사의 라이선스 확정 후 LICENSE와 배포 메타데이터를 추가하세요.
원문에서 가져온 명령 설명의 고지는 [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md)에 보존합니다. 제조사 펌웨어 자체는 배포 패키지에 포함하지 않습니다.
