<a id="readme-top"></a>

<!-- PROJECT SHIELDS -->
[![CI][ci-shield]][ci-url]
[![Python][python-shield]][python-url]
[![Status][status-shield]][status-url]
[![License][license-shield]][license-url]
[![Issues][issues-shield]][issues-url]

<!-- PROJECT HEADER -->
<br />
<div align="center">
  <h3 align="center">PF400 Python SDK</h3>

  <p align="center">
    Brooks PreciseFlex PF400 TCP Command Server (TCS)용 Python 클라이언트
    <br />
    <a href="docs/USAGE.ko.md"><strong>문서 보기 »</strong></a>
    <br />
    <br />
    <a href="examples/README.md">예제 보기</a>
    &middot;
    <a href="https://github.com/ABLE-Labs/Brooks-PF400-Python-SDK/issues/new?labels=bug">버그 신고</a>
    &middot;
    <a href="https://github.com/ABLE-Labs/Brooks-PF400-Python-SDK/issues/new?labels=enhancement">기능 요청</a>
    &middot;
    <a href="README.md">English</a>
  </p>
</div>

<!-- TABLE OF CONTENTS -->
<details>
  <summary>목차</summary>
  <ol>
    <li>
      <a href="#프로젝트-소개">프로젝트 소개</a>
      <ul>
        <li><a href="#사용-기술">사용 기술</a></li>
      </ul>
    </li>
    <li>
      <a href="#시작하기">시작하기</a>
      <ul>
        <li><a href="#사전-요구-사항">사전 요구 사항</a></li>
        <li><a href="#설치">설치</a></li>
      </ul>
    </li>
    <li><a href="#사용법">사용법</a></li>
    <li><a href="#기여">기여</a></li>
    <li><a href="#라이선스">라이선스</a></li>
    <li><a href="#문의">문의</a></li>
    <li><a href="#참고-자료">참고 자료</a></li>
  </ol>
</details>

<!-- ABOUT THE PROJECT -->
## 프로젝트 소개

PF400 Python SDK는 Brooks PreciseFlex PF400 로봇을 TCP Command Server (TCS) 프로토콜로 제어합니다.
지원 대상 TCS 펌웨어의 비전 제외 명령 82개를 타입이 지정된 Python 메서드로 제공합니다.

- 동기(`PF400`)·비동기(`AsyncPF400`) 클라이언트가 동일한 메서드와 인자를 제공
- motion / status 채널 독립 사용
- 응답 원문과 컨트롤러 오류 코드를 항상 보존
- 자동 재시도·재접속·명령 재전송 없음

> [!NOTE]
> **알파 버전 (`0.1.0a1`).** 로컬 TCP 테스트 서버와 패키징 검증까지 완료했으며,
> 실제 PF400 장비에서는 아직 검증하지 않았습니다. [검증 기록](docs/VALIDATION.md)을 참고하세요.

<p align="right">(<a href="#readme-top">맨 위로</a>)</p>

### 사용 기술

[![Python][python-shield]][python-url] — 표준 라이브러리만 사용, 런타임 외부 의존성 없음

<p align="right">(<a href="#readme-top">맨 위로</a>)</p>

<!-- GETTING STARTED -->
## 시작하기

### 사전 요구 사항

- Python 3.10 이상
- 버전 문자열 `Command Server 3.0D4 10-25-2024`를 반환하는 TCS 펌웨어가 설치된 PF400,
  motion 포트(`10100`)와 status 포트(`10000`)로 접속 가능

TCS 빌드와 장비 구성(레일, 서보/공압/듀얼 그리퍼, 높이 감지 등)에 따라 지원되는 명령이 다를 수 있습니다.

### 설치

아직 PyPI에 등록되지 않았습니다. 이 저장소에서 설치합니다.

```bash
python -m pip install "git+https://github.com/ABLE-Labs/Brooks-PF400-Python-SDK.git"
```

또는 저장소를 내려받아 개발 모드로 설치합니다.

```bash
git clone https://github.com/ABLE-Labs/Brooks-PF400-Python-SDK.git
cd Brooks-PF400-Python-SDK
python -m pip install -e .
```

배포 이름은 `ablelabs-pf400-sdk`, import 이름은 `pf400`입니다. 새 가상환경에 설치하는 것을 권장합니다.

<p align="right">(<a href="#readme-top">맨 위로</a>)</p>

<!-- USAGE -->
## 사용법

로봇 버전과 관절 위치를 조회합니다.

```python
from pf400 import PF400

with PF400("192.168.0.1", timeout=5) as robot:
    print(robot.version().data)
    print(robot.where_j().as_floats())
```

연결은 TCP 소켓만 엽니다. 전원, 원점, 이동 명령은 보내지 않습니다.

> [!WARNING]
> - 정지는 항상 `halt(channel="status")`로 보내세요. `Halt`는 급감속 명령이며 **하드웨어 비상정지를 대신할 수 없습니다.**
> - 연결 해제, 작업 취소, Python 예외는 물리적인 동작을 멈추지 않습니다.
> - SDK는 명령을 재시도하지 않습니다. 타임아웃 후에는 장비 상태를 확인한 뒤 다시 연결하세요.
> - 펌웨어는 포트당 하나의 TCP 연결만 받습니다. 같은 로봇에 여러 클라이언트를 동시에 연결하지 마세요.

[examples](examples/README.md) 폴더에 작업별 실행 파일이 있으며, 폴더마다 README가 있습니다.

| 분류 | 예제 |
|---|---|
| 기본 | [연결](examples/01_connection/README.ko.md) · [전원](examples/02_power/README.ko.md) · [이동 프로파일](examples/03_profiles/README.ko.md) · [비동기](examples/async/README.ko.md) |
| 이동 | [관절](examples/04_joint_motion/README.ko.md) · [직교](examples/05_cartesian_motion/README.ko.md) · [단일 축](examples/06_single_axis/README.ko.md) · [정지](examples/11_stop/README.ko.md) |
| 그리퍼 | [그리퍼](examples/07_gripper/README.ko.md) · [힘 제한 잡기](examples/08_gripper_force/README.ko.md) |
| 티칭 | [컨트롤러 티칭](examples/09_controller_teaching/README.ko.md) · [좌표 변환](examples/10_coordinate_conversion/README.ko.md) · [PC 티칭 위치](examples/13_teaching_positions/README.ko.md) · [수동 모드](examples/14_free_mode/README.ko.md) |
| 기타 | [오류 처리](examples/12_error_handling/README.ko.md) · [공통 모듈](examples/common/README.ko.md) · [설정 파일](examples/config/README.ko.md) |

_채널, 오류, 타임아웃, 비동기 사용, 응답 모드는 [사용 가이드](docs/USAGE.ko.md)를 참고하세요.
전체 명령은 [명령 레퍼런스](docs/API.md)(영문)에 있습니다._

<p align="right">(<a href="#readme-top">맨 위로</a>)</p>

<!-- CONTRIBUTING -->
## 기여

버그 신고와 기능 요청은 [GitHub Issues](https://github.com/ABLE-Labs/Brooks-PF400-Python-SDK/issues)로 남겨 주세요.

개발 환경 준비:

```bash
python -m pip install -e ".[dev]"
python -m pytest
python -m ruff check .
python -m build
```

명령 메서드는 `tools/generate_api.py`가 펌웨어 소스로부터 생성하며, 펌웨어 소스는 이 저장소에 포함되어 있지 않습니다.
SDK를 사용·설치·빌드할 때는 펌웨어 소스가 필요하지 않습니다.

<p align="right">(<a href="#readme-top">맨 위로</a>)</p>

<!-- LICENSE -->
## 라이선스

이 SDK의 라이선스는 아직 확정되지 않았습니다.
제조사 소스에서 가져온 명령 설명의 원문 고지는 [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md)에 보존되어 있습니다.
제조사 펌웨어는 포함되어 있지 않습니다.

<p align="right">(<a href="#readme-top">맨 위로</a>)</p>

<!-- CONTACT -->
## 문의

ABLE Labs — [GitHub Issues](https://github.com/ABLE-Labs/Brooks-PF400-Python-SDK/issues)로 문의해 주세요.

프로젝트 링크: [https://github.com/ABLE-Labs/Brooks-PF400-Python-SDK](https://github.com/ABLE-Labs/Brooks-PF400-Python-SDK)

<p align="right">(<a href="#readme-top">맨 위로</a>)</p>

<!-- ACKNOWLEDGMENTS -->
## 참고 자료

- [Brooks Automation GPL 문서](https://www2.brooksautomation.com/Controller_Software/Software_Reference/GPL_Dictionary/Profile_class/profileintro.htm)
- [Shields.io](https://shields.io)
- [Best-README-Template](https://github.com/othneildrew/Best-README-Template)

<p align="right">(<a href="#readme-top">맨 위로</a>)</p>

<!-- MARKDOWN LINKS & IMAGES -->
[ci-shield]: https://github.com/ABLE-Labs/Brooks-PF400-Python-SDK/actions/workflows/ci.yml/badge.svg
[ci-url]: https://github.com/ABLE-Labs/Brooks-PF400-Python-SDK/actions/workflows/ci.yml
[python-shield]: https://img.shields.io/badge/python-3.10%2B-3776AB?logo=python&logoColor=white
[python-url]: https://www.python.org/
[status-shield]: https://img.shields.io/badge/status-alpha-orange
[status-url]: docs/VALIDATION.md
[license-shield]: https://img.shields.io/badge/license-TBD-lightgrey
[license-url]: THIRD_PARTY_NOTICES.md
[issues-shield]: https://img.shields.io/github/issues/ABLE-Labs/Brooks-PF400-Python-SDK
[issues-url]: https://github.com/ABLE-Labs/Brooks-PF400-Python-SDK/issues
