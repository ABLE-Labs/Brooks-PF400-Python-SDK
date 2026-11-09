# 02 · 전원 (사용 시작·종료)

[English](README.md) · [예제 안내서](../README.md)

로봇 사용을 준비하고 종료합니다. 순서를 따라 읽을 수 있도록 파일 안에 SDK 호출을 모두 그대로 적었습니다.

> [!WARNING]
> 사용 시작 예제는 전원을 켜고 Home을 실행할 수 있습니다. 실행 전에 로봇 주변을 확인하세요.

## 파일

| 파일 | 설명 | 로봇 동작 |
|---|---|---|
| [02_startup.py](02_startup.py) | 세션 설정 → 프로파일 → 전원 ON → Attach → 필요 시 Home → 그리퍼 열기 | 전원 ON, 필요 시 Home, 그리퍼 열기 |
| [02_shutdown.py](02_shutdown.py) | 세션 설정 → Halt → 수동 모드 종료 → Detach → 전원 OFF | 정지, 전원 OFF |

## 설정

접속 설정(`HOST`, `ROBOT_ID`, `PORT`, `STATUS_PORT`)만 있습니다. 두 파일 모두 `TIMEOUT`은 `30.0`초입니다.

## 동작 순서

`02_startup.py`

1. 연결 전에 [config/motion_profiles.json](../config/motion_profiles.json)을 읽고 검증합니다.
2. 양쪽 채널에 Normal 모드와 로봇을 설정하고 수동 모드를 종료합니다(`free_mode(-1)`).
3. JSON의 MSpeed와 모든 프로파일을 적용합니다.
4. 그리퍼 개방·닫힘 위치를 `100.0` / `70.0` mm로 설정합니다(파일 안의 값).
5. 전원을 켜고(`hp(1, wait=30)`, 제한 60초) 제어권을 연결합니다(`attach(1)`).
6. 원점 상태(`pd(2800)`)가 `0`일 때만 `home()`을 실행하고 다시 확인합니다.
7. 그리퍼를 열고(`gripper(1)`) TCP 연결만 닫습니다. 전원은 켜진 상태로 남습니다.

`02_shutdown.py`

1. 양쪽 채널에 Normal 모드와 로봇을 설정합니다.
2. status 채널로 `halt()`를 보내고 수동 모드를 종료합니다.
3. 제어권을 해제하고(`attach(0)`) 전원을 끈 뒤(`hp(0)`) 연결을 닫습니다.

사용 종료 예제는 초기화나 Home을 먼저 하지 않습니다.

## 참고

- 컨트롤러를 재부팅하면 프로파일을 다시 적용해야 합니다. 사용 시작 예제가 JSON 값을 다시 적용합니다.
- 시작 후 계속 제어하려면 파일 주석이 안내하는 위치에 SDK 호출을 추가하세요.

## 실행

```bash
python examples/02_power/02_startup.py
python examples/02_power/02_shutdown.py
```
