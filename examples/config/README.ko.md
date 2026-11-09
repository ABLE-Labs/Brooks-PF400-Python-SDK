# config · 예제 설정 파일

[English](README.md) · [예제 안내서](../README.md)

예제가 읽고 쓰는 PC의 JSON 파일입니다. 컨트롤러 메모리나 GPO 파일과는 별개입니다.

## 파일

| 파일 | 내용 | 읽는 예제 | 쓰는 예제 |
|---|---|---|---|
| [motion_profiles.json](motion_profiles.json) | MSpeed와 이동 프로파일 | [02](../02_power/) 시작, [03](../03_profiles/) 적용, 이동 예제 | [03](../03_profiles/) 저장 |
| [teaching_positions.json](teaching_positions.json) | 이름을 붙인 관절 좌표 | [13](../13_teaching_positions/) 목록, 이동 | [13](../13_teaching_positions/) 저장 |

## motion_profiles.json

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

- `master_speed`: 시스템 전체 속도 배율 [%].
- `profiles`: 키는 슬롯 번호 `"1"`~`"20"`입니다. 각 프로파일에는 8개 필드가 모두 있어야 합니다.
  `straight`는 정수 `0` 또는 `1`, 나머지 필드는 유한한 숫자여야 합니다.
- 기본 파일에는 프로파일 `1`, `2`(`speed` 10, 5)가 있습니다. 모든 값은 장비에서 검증해야 하는 예시값입니다.

필드 의미와 단위는 [03_profiles](../03_profiles/)와 [예제 안내서](../README.md)의 03 항목을 참고하세요.

## teaching_positions.json

기본 파일에는 저장된 위치가 없습니다. [13](../13_teaching_positions/)으로 저장하면 다음과 같은 형태가 됩니다.

```json
{
  "positions": {
    "position_a": { "joints": [100.0, 0.0, 90.0, 0.0, 80.0] }
  }
}
```

- `positions`: 위치 이름과 `joints` 리스트(축 순서대로 숫자 1~12개)를 가진 객체입니다.
  위 숫자는 형식을 보여주기 위한 값입니다.
- 위치에 추가 필드가 있으면 다시 저장해도 유지됩니다.

## 참고

- 파일을 직접 편집해도 됩니다. 읽고 저장할 때마다 전체를 검증하며 잘못된 값은 거부합니다.
- 손상된 파일은 오류를 내며 덮어쓰지 않습니다.
- 여러 프로그램이 동시에 같은 파일에 저장하는 용도로 설계하지 않았습니다.
- 장비에서 값을 바꿔도 이 파일은 갱신되지 않습니다.
