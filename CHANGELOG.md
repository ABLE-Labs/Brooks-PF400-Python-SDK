# 공통 import 경로 수정 — 2026-11-09

- 단축 import를 examples.common 명시적 패키지 경로로 교체하고 패키지 초기화 파일 추가.
- IDE 인식과 하위 폴더 파일 직접 실행을 함께 지원. 설정·티칭 JSON 내용은 변경하지 않음.

# 예제 폴더 정리 — 2026-11-09

- 실행 예제를 01~14 기능별 폴더로 분류. 기존 파일명과 동작을 유지.
- 공통 코드는 examples/common, 프로파일·티칭 JSON은 examples/config로 이동.
- IDE 직접 실행과 작업 디렉터리에 무관한 공통 모듈·설정 경로를 검증.

# 변경 사항 — 2026-11-09

- 예제용 motion_profiles.json을 프로파일·MSpeed의 공통 저장소로 추가. 연결 전 검증과 원자적 PC 저장 지원.
- 제어 준비와 02 시작이 같은 파일을 읽어 MSpeed·프로파일을 재적용.
- 03 저장/적용/조회 및 07~10·13~14를 작업별 실행 파일로 분리. 이전 통합 파일 대체.
- 일반 이동의 자동 그리퍼 열기 제거, 잡기 실패 시 중단, 해제 완료 대기 추가.
- core SDK 명령 API와 기존 teaching_positions.json은 변경하지 않음. 실장비 실행 없음.

# Changelog

## 0.1.0a1 — 2026-11-09

- Initial 82-command synchronous and asynchronous SDK for Tcp_cmd_server_ablelabs.
- All eight vision commands excluded, including generic command dispatch.
- Deadline-bounded independent TCP channels, explicit recovery, no automatic retries.
- Normal/Telnet framing, immutable responses, all negative controller errors preserved.
- Firmware source fingerprints, command reference, tests and integration examples.
- Removed the FastAPI integration example; examples focus on Python SDK usage.
- Added 12 functional code-configured Python examples, an asynchronous read-only example, execution documentation and loopback example tests.
- Added local JSON teaching save/list/move example, coordinate validation and atomic file replacement.
- Added multi-axis selection through an AXES list, with explicit Attach, previous-mode reset and all-axis restore.
- Corrected the free-mode example to Attach 1; added descriptions/hints for 49 known controller/TCS errors while retaining raw responses.
- Audited every example: explicit session selection, shared pendant-style initialization and conditional Home; preserved read/capture/stop/off semantics.
- Replaced example 02 ACTION dispatch with separate explicit startup and shutdown scripts.
- Development alpha; no physical PF400 validation or public registry release.
