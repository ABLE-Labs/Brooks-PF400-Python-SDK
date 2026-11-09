# 12 · 오류 처리

[English](README.md) · [예제 안내서](../README.md)

SDK의 장비·타임아웃·프로토콜·연결 오류를 처리하는 방법을 보여줍니다. 재시도는 하지 않습니다.

## 파일

| 파일 | 설명 | 로봇 동작 |
|---|---|---|
| [12_error_handling.py](12_error_handling.py) | `nop()`과 `where_j()`를 보내고, 오류가 나면 stderr에 출력한 뒤 종료 코드 `1`로 끝남 | 조회만 |

## 처리하는 오류

| 예외 | 출력 내용 |
|---|---|
| `DeviceError` | `code`, `command`, `description`, `raw`, 있으면 `hint` |
| `CommandTimeout` | `command`, `may_have_executed` |
| `ProtocolError` | 메시지와 `may_have_executed` |
| `ConnectionError` | 메시지와 `may_have_executed` |
| `NotConnectedError` | 메시지 |

`CommandTimeout`과 `ProtocolError`는 `ConnectionError`의 하위 클래스이므로 먼저 처리합니다.
알려진 오류 코드는 [docs/ERRORS.md](../../docs/ERRORS.md)에 있습니다.

## 실행

```bash
python examples/12_error_handling/12_error_handling.py
```
