# 01 · 연결과 상태 조회

[English](README.md) · [예제 안내서](../README.md)

로봇에 연결해 버전, 상태, 현재 위치를 조회합니다. 초기화나 이동은 하지 않습니다.

## 파일

| 파일 | 설명 | 로봇 동작 |
|---|---|---|
| [01_connect_and_status.py](01_connect_and_status.py) | 버전, 시스템 상태, 모션 상태, 관절 좌표, 직교 좌표 출력 | 조회만 |

## 설정

| 변수 | 기본값 | 설명 |
|---|---|---|
| `HOST` | `"192.168.0.1"` | 컨트롤러 IP 또는 호스트명 (예시값) |
| `ROBOT_ID` | `1` | 대상 로봇 번호 |
| `PORT` / `STATUS_PORT` | `10100` / `10000` | motion / status TCP 포트 |
| `TIMEOUT` | `10.0` | SDK 통신 제한 시간 [s] |

모든 예제 파일 상단에 같은 접속 설정이 있습니다.

## 동작 순서

1. motion·status 연결을 엽니다.
2. 양쪽 채널에 Normal 모드와 `ROBOT_ID`를 설정합니다(`configure_session()`).
3. `version()`, `sys_state()`, `state()`, `where_j()`, `where_c()` 결과를 출력합니다.

## 실행

SDK를 설치한 뒤 IDE에서 SDK 루트 폴더를 열고 파일을 실행합니다. 터미널에서는 SDK 루트에서 실행합니다.

```bash
python examples/01_connection/01_connect_and_status.py
```
