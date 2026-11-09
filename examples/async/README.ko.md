# Async · 상태 조회

[English](README.md) · [예제 안내서](../README.md)

`asyncio`와 `AsyncPF400`으로 버전과 관절 좌표를 조회합니다. 초기화나 이동은 하지 않습니다.

## 파일

| 파일 | 설명 | 로봇 동작 |
|---|---|---|
| [read_status.py](read_status.py) | 양쪽 채널에 Normal 모드와 로봇을 설정한 뒤 `version()`, `where_j()` 결과 출력 | 조회만 |

## 설정

접속 설정(`HOST`, `ROBOT_ID`, `PORT`, `STATUS_PORT`, `TIMEOUT`)만 있습니다.

## 참고

- `AsyncPF400`은 `PF400`과 같은 메서드와 인자를 제공하며, 각 호출을 `await`합니다.
- 작업을 취소해도 로봇은 멈추지 않습니다. [사용 가이드](../../docs/USAGE.ko.md#비동기-사용)를 참고하세요.

## 실행

```bash
python examples/async/read_status.py
```
