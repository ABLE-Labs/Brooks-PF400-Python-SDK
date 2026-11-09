# 사용 가이드

[English](USAGE.md) · [README로 돌아가기](../README.ko.md)

- [연결](#연결)
- [명령 호출](#명령-호출)
- [상태 채널과 정지](#상태-채널과-정지)
- [응답과 오류](#응답과-오류)
- [비동기 사용](#비동기-사용)
- [응답 모드](#응답-모드)
- [명령 지원 범위](#명령-지원-범위)

## 연결

```python
from pf400 import PF400

with PF400("192.168.0.1", timeout=5) as robot:
    print(robot.version().data)
```

연결은 TCP 소켓 두 개(기본값: motion 포트 `10100`, status 포트 `10000`)를 여는 작업만 수행합니다.
전원, 모드, 원점, 그리퍼, 이동 명령은 자동으로 보내지 않습니다.
`connected`는 로컬 소켓이 열려 있는지만 나타내며, 로봇이 준비된 상태라는 뜻은 아닙니다.

## 명령 호출

메서드는 펌웨어 명령의 의미와 인자 순서를 그대로 따릅니다. 관절·직교 좌표는 리스트 또는 튜플로 전달합니다.
모든 메서드에 `channel="motion" | "status"`와 `timeout=초`를 지정할 수 있습니다.

```python
# 아래 호출은 실행하면 실제 장비가 동작합니다.
# robot.hp(1, wait=10)
# robot.attach(1)
# robot.home(timeout=120)
# robot.move_j(profile_index=1, joints=target_joints)
# robot.wait_for_eom(timeout=60)
# robot.gripper(1)  # 펌웨어 정의: 1 = 열기, 2 = 닫기
```

이동 명령의 응답을 받았다고 해서 동작이 끝난 것은 아닐 수 있습니다. 필요하면 `wait_for_eom()`을 명시적으로 호출하세요.

| 명령 | 주의 사항 |
|---|---|
| `home_all()` | 모든 로봇에 영향을 줍니다. |
| `move_extra_axis()` | 다음 직교 이동에서 사용할 추가 축 목표를 예약할 뿐, 즉시 이동하지 않습니다. |
| `release_plate()` | 세 번째 인자는 프로파일 번호가 아니라 `in_range`입니다. |
| `payload()` | 값은 질량이 아니라 백분율입니다. |

## 상태 채널과 정지

기본 채널은 `motion`이며, `reset()`만 기본값이 `status`입니다.
펌웨어 시작 시 상태 채널에는 로봇 `0`이 선택되어 있으므로, 로봇별 조회나 정지 전에 대상 로봇을 명시적으로 선택하세요.

```python
with PF400("192.168.0.1") as robot:
    robot.select_robot(1, channel="status")
    print(robot.state(channel="status").as_ints())
    # robot.halt(channel="status")  # 응답을 기다리는 motion 채널과 독립적으로 전송
```

- `halt()`를 기본 motion 채널로 호출하면 앞 명령의 응답이 올 때까지 기다릴 수 있습니다.
- `Halt`는 급감속 명령이며 전원은 유지됩니다. **하드웨어 비상정지를 대신할 수 없습니다.**
- `Reset`은 로봇 스레드를 재시작합니다. 펌웨어는 상태 채널에 로봇 `0`이 선택된 경우에만 허용하므로,
  다른 로봇을 선택했다면 먼저 `select_robot(0, channel="status")`를 호출하세요.

## 응답과 오류

```python
from pf400 import CommandTimeout, DeviceError

try:
    response = robot.where_j()
    print(response.raw)          # 응답 원문, 예: "0 10.0 20.0 ..."
    print(response.code)         # 상태 코드 (Normal 모드 성공 시 0)
    print(response.values)       # 상태 코드 뒤의 필드: tuple[str, ...]
    print(response.as_floats())  # 모든 필드를 float로 변환
except DeviceError as exc:
    print(exc.code, exc.description)  # 알려진 코드의 설명
    print(exc.hint)                   # 확인 사항 (없으면 빈 문자열)
    print(exc.raw)                    # 컨트롤러 응답 원문
except CommandTimeout as exc:
    print(exc.command, exc.may_have_executed)
    # 로봇 상태와 실제 위치를 확인한 뒤 복구 방법을 결정하세요.
```

- `0 -1`은 성공 응답이며 `-1` 데이터는 그대로 유지됩니다.
- 응답을 `bool`로 강제 변환하지 않습니다. 예를 들어 `IsFullyClosed`는 듀얼 그리퍼에서 비트마스크를 반환할 수 있습니다.
- 반환 필드별 의미는 [명령 레퍼런스](API.md)를 참고하세요.

### 타임아웃과 복구

- 채널 잠금 대기, 전송, 응답 수신 전체에 하나의 제한 시간이 적용됩니다.
  전송이 시작된 뒤라면 `may_have_executed`가 `True`입니다.
- 타임아웃, 연결 끊김, 잘못된 응답이 발생하면 해당 연결을 닫아 늦게 도착한 응답이 다음 명령과 섞이지 않게 합니다.
- SDK는 재시도·재접속·재전송을 하지 않습니다. `connect()`를 다시 호출하기 전에 장비 상태를 확인하세요.
- 연결 해제나 Python 예외는 물리적인 동작을 멈추지 않습니다.

### 오류 설명

알려진 컨트롤러·TCS 오류 코드에는 설명과 확인 사항이 덧붙습니다([오류 코드 설명](ERRORS.md)).
제조사 전체 오류 목록은 아니며, 등록되지 않은 코드와 응답 원문도 항상 그대로 전달합니다.

## 비동기 사용

```python
from pf400 import AsyncPF400

async def read_position():
    async with AsyncPF400("192.168.0.1") as robot:
        return (await robot.where_j()).as_floats()
```

- 비동기 클라이언트는 `asyncio.to_thread`로 블로킹 통신을 이벤트 루프 밖에서 실행합니다.
- 작업을 취소해도 로봇은 멈추지 않습니다. 진행 중인 통신이 제한 시간 안에 끝난 뒤 취소가 전달됩니다.
- 같은 채널의 명령은 순서대로 처리되며, motion과 status 채널은 독립적으로 사용할 수 있습니다.
- 펌웨어는 포트당 하나의 TCP 연결만 처리합니다. 같은 로봇 포트에 여러 클라이언트를 동시에 연결하지 마세요.

## 응답 모드

시작 기본값인 Normal 모드를 권장합니다. `mode(1)`은 Telnet 모드로, `mode(0)`은 Normal 모드로 전환합니다.

- 모드는 서버의 모든 채널이 공유하므로, SDK는 전환하는 동안 두 채널을 모두 잠급니다.
  다른 클라이언트가 모드를 바꿨다면 다시 연결하세요.
- 이미 Telnet 모드인 서버에 연결할 때는 생성자에 `telnet_mode=True`를 전달하세요.
- Telnet 응답은 사람이 읽는 문자열이므로 `Response.code`가 `None`일 수 있습니다.
  숫자 코드가 없는 응답의 성공 여부를 SDK가 추정하지 않습니다.
- 모드 전환 중 통신이 실패하면 두 연결을 모두 닫습니다. 서버의 현재 모드에 맞는 `telnet_mode`로 새 인스턴스를 만드세요.

## 명령 지원 범위

- 펌웨어에 선언된 명령 90개 중 비전 명령 8개를 제외한 82개를 메서드로 제공합니다. 제외 명령:
  `Vprocess`, `VresultLoc`, `VresultInfo`, `VresultInspect`, `VToolProperty`, `VresultInfoString`,
  `StereoParam`, `StereoLocate`.
- `PickPlate`, `PlacePlate`, `TeachPlate` 등 펌웨어 내장 플레이트·팔레트 명령을 포함합니다.
- `execute()`는 등록된 비전 제외 명령만 허용합니다. 임의 명령을 그대로 전달하는 API는 제공하지 않습니다.
- `Custom`은 펌웨어에 포함된 예제 명령이라는 점을 레퍼런스에 표시합니다.
- 애플리케이션 수준의 시퀀스, 자체 기구학 계산, 티치 펜던트, 사이트별 좌표 파일은 포함하지 않습니다.

펌웨어 관련 주의 사항:

- `MoveToSafe` / `ChangeConfig` 계열은 펌웨어 문서에 작업 공간 내부 충돌 확인을 하지 않는다고 기재되어 있습니다.
- `PickPlate` / `PlacePlate`는 펌웨어 소스에 `BES NOT UPDATED` 주석이 있으므로 사용하는 장비 구성에서 검증하세요.
