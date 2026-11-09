# 03 · 이동 프로파일

[English](README.md) · [예제 안내서](../README.md)

MSpeed와 이동 프로파일을 PC의 JSON 파일에 저장하고, 장비에 적용하고, 다시 조회합니다.
이 값의 기준은 [config/motion_profiles.json](../config/motion_profiles.json) 한 곳입니다.

## 파일

| 파일 | 설명 | 로봇 동작 |
|---|---|---|
| [03_profile_save.py](03_profile_save.py) | 파일 상단의 값을 JSON에 저장 | 없음 (접속 안 함) |
| [03_profile_apply.py](03_profile_apply.py) | JSON의 MSpeed와 모든 프로파일을 장비에 적용 | 설정만 |
| [03_profile_read.py](03_profile_read.py) | 장비의 MSpeed와 프로파일 하나를 조회 | 조회만 |

## 설정

`03_profile_save.py`

| 변수 | 기본값 | 설명 |
|---|---|---|
| `PROFILE_INDEX` | `1` | 프로파일 슬롯 (1~20) |
| `MASTER_SPEED` | `20.0` | 시스템 전체 속도 배율 [%] |
| `SPEED` / `SPEED2` | `10.0` / `10.0` | 최고 속도 / Cartesian 이동 중 일부 축의 보조 속도 [%] |
| `ACCEL` / `DECEL` | `10.0` / `10.0` | 최고 가속도 / 감속도 [%] |
| `ACC_RAMP` / `DEC_RAMP` | `0.2` / `0.2` | S-curve 램프 시간 [s] (전체 가속 시간이 아님) |
| `IN_RANGE` | `0.0` | `< 0` 블렌딩, `0` 오차 조건 없이 정지, `> 0` 위치 오차 판정 |
| `STRAIGHT` | `0` | `0` 관절 보간, `1` Cartesian 직선 경로 |

`03_profile_read.py`: `PROFILE_INDEX` (기본값 `1`).

단위, 의미, 제조사 근거는 [예제 안내서](../README.md)의 03 항목에 정리되어 있습니다.

## 사용 순서

1. **저장** — 선택한 슬롯과 MSpeed만 갱신하고 다른 슬롯은 유지합니다.
   파일이 없으면 새로 만들고, 손상된 파일은 오류를 내며 덮어쓰지 않습니다.
2. **적용** — MSpeed와 모든 프로파일을 보냅니다. 전원 ON, Attach, Home, 그리퍼 동작은 없습니다.
3. **조회** — `[번호, Speed, Speed2, Accel, Decel, AccRamp, DecRamp, InRange, Straight]`를 출력합니다. 파일 값과 비교하세요.

저장과 적용은 별개입니다. 장비에서 값을 바꿔도 JSON 파일은 갱신되지 않습니다.
사용 시작([02](../02_power/))과 이동 예제가 JSON 값을 장비에 다시 적용합니다.

## 실행

```bash
python examples/03_profiles/03_profile_save.py
python examples/03_profiles/03_profile_apply.py
python examples/03_profiles/03_profile_read.py
```
