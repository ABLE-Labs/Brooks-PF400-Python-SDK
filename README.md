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
    Python client for the Brooks PreciseFlex PF400 TCP Command Server (TCS)
    <br />
    <a href="docs/USAGE.md"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="examples/README.md">View Examples</a>
    &middot;
    <a href="https://github.com/ABLE-Labs/Brooks-PF400-Python-SDK/issues/new?labels=bug">Report Bug</a>
    &middot;
    <a href="https://github.com/ABLE-Labs/Brooks-PF400-Python-SDK/issues/new?labels=enhancement">Request Feature</a>
    &middot;
    <a href="README.ko.md">한국어</a>
  </p>
</div>

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>

<!-- ABOUT THE PROJECT -->
## About The Project

PF400 Python SDK controls the Brooks PreciseFlex PF400 robot over the TCP Command Server (TCS) protocol.
It exposes the 82 non-vision commands of the supported TCS firmware as typed Python methods.

- Synchronous (`PF400`) and asynchronous (`AsyncPF400`) clients with identical methods and arguments
- Independent motion and status channels
- Raw responses and controller error codes are always preserved
- No automatic retries, reconnects or command resends

> [!NOTE]
> **Alpha (`0.1.0a1`).** Verified against a local TCP test server and through packaging checks.
> Not yet validated on physical PF400 hardware. See the [validation record](docs/VALIDATION.md).

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Built With

[![Python][python-shield]][python-url] — standard library only, no runtime dependencies

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- GETTING STARTED -->
## Getting Started

### Prerequisites

- Python 3.10 or later
- A PF400 running TCS firmware that reports `Command Server 3.0D4 10-25-2024`,
  reachable on the motion port (`10100`) and status port (`10000`)

Command availability can differ between TCS builds and hardware configurations
(rail, servo / pneumatic / dual gripper, height detection, etc.).

### Installation

The package is not published on PyPI yet. Install it from this repository:

```bash
python -m pip install "git+https://github.com/ABLE-Labs/Brooks-PF400-Python-SDK.git"
```

Or clone and install in editable mode:

```bash
git clone https://github.com/ABLE-Labs/Brooks-PF400-Python-SDK.git
cd Brooks-PF400-Python-SDK
python -m pip install -e .
```

The distribution name is `ablelabs-pf400-sdk` and the import name is `pf400`.
A fresh virtual environment is recommended.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- USAGE -->
## Usage

Read the robot version and joint positions:

```python
from pf400 import PF400

with PF400("192.168.0.1", timeout=5) as robot:
    print(robot.version().data)
    print(robot.where_j().as_floats())
```

Connecting only opens the TCP sockets. It does not send power, homing or motion commands.

> [!WARNING]
> - `halt()` is a rapid deceleration command. **It is not a substitute for a hardware emergency stop.**
> - Disconnecting, cancelling a task or raising a Python exception does not stop physical motion.
> - The SDK never retries a command. After a timeout, check the robot before reconnecting.
> - The firmware accepts one TCP connection per port. Do not connect multiple clients to the same robot.

The [examples](examples/README.md) folder contains one script per task. Each folder has its own README:

| Area | Examples |
|---|---|
| Basics | [connection](examples/01_connection/README.md) · [power](examples/02_power/README.md) · [motion profiles](examples/03_profiles/README.md) · [async](examples/async/README.md) |
| Motion | [joint](examples/04_joint_motion/README.md) · [Cartesian](examples/05_cartesian_motion/README.md) · [single axis](examples/06_single_axis/README.md) · [stop](examples/11_stop/README.md) |
| Gripper | [gripper](examples/07_gripper/README.md) · [force-limited grasp](examples/08_gripper_force/README.md) |
| Teaching | [controller teaching](examples/09_controller_teaching/README.md) · [coordinate conversion](examples/10_coordinate_conversion/README.md) · [PC positions](examples/13_teaching_positions/README.md) · [free mode](examples/14_free_mode/README.md) |
| Other | [error handling](examples/12_error_handling/README.md) · [shared modules](examples/common/README.md) · [settings files](examples/config/README.md) |

_For channels, errors, timeouts, async usage and response modes, see the [Usage guide](docs/USAGE.md).
Every command is listed in the [Command reference](docs/API.md)._

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- CONTRIBUTING -->
## Contributing

Bug reports and feature requests are welcome through [GitHub Issues](https://github.com/ABLE-Labs/Brooks-PF400-Python-SDK/issues).

To set up a development environment:

```bash
python -m pip install -e ".[dev]"
python -m pytest
python -m ruff check .
python -m build
```

Command methods are generated by `tools/generate_api.py` from the firmware sources, which are not part of this repository.
Firmware sources are not needed to use, install or build the SDK.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- LICENSE -->
## License

The license for this SDK has not been finalized yet.
Command descriptions derived from the manufacturer's sources keep their original notices in
[THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md). The manufacturer's firmware is not included.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- CONTACT -->
## Contact

ABLE Labs — please open an issue on [GitHub](https://github.com/ABLE-Labs/Brooks-PF400-Python-SDK/issues).

Project Link: [https://github.com/ABLE-Labs/Brooks-PF400-Python-SDK](https://github.com/ABLE-Labs/Brooks-PF400-Python-SDK)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

- [Brooks Automation GPL documentation](https://www2.brooksautomation.com/Controller_Software/Software_Reference/GPL_Dictionary/Profile_class/profileintro.htm)
- [Shields.io](https://shields.io)
- [Best-README-Template](https://github.com/othneildrew/Best-README-Template)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

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
