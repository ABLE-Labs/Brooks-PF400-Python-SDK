# 11 · 정지

[English](README.md) · [예제 안내서](../README.md)

motion 채널에서 응답을 기다리는 이동 명령에 막히지 않도록, status 채널로 `halt()`를 보냅니다.

> [!WARNING]
> `Halt`는 급감속이며 전원은 유지됩니다. **하드웨어 비상정지를 대신할 수 없습니다.**

## 파일

| 파일 | 설명 | 로봇 동작 |
|---|---|---|
| [11_stop.py](11_stop.py) | `stop_robot(robot, robot_id)`가 status 채널에서 로봇을 선택하고 `halt()`를 보냄. `main()`은 연결 후 정지하고 모션 상태를 출력 | 정지 |

## 애플리케이션에서 사용하기

애플리케이션이 이미 사용 중인 SDK 객체로 `stop_robot()`을 호출하세요.

```python
stop_robot(robot, robot_id=1)
```

펌웨어는 포트당 하나의 TCP 연결만 받으므로, 다른 앱이 연결을 점유한 상태에서 별도 프로세스로 로봇을 멈추는 도구가 아닙니다.

## 참고

- 정지 전에 전원 ON, 그리퍼, Home 초기화를 하지 않습니다.
- 연결 해제, Ctrl+C, 예외, 타임아웃은 로봇을 멈추지 않습니다.

## 실행

```bash
python examples/11_stop/11_stop.py
```
