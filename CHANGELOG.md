# Changelog

## 0.1.0a1 — 2026-11-09

First development alpha. Not yet validated on physical PF400 hardware and not published on PyPI.

### SDK

- Synchronous (`PF400`) and asynchronous (`AsyncPF400`) clients for the 82 non-vision commands of the
  PF400 TCP Command Server (TCS) firmware. The eight vision commands are excluded, including from `execute()`.
- Independent motion and status TCP channels with a single deadline per command.
  No automatic retries, reconnects or resends; the affected connection is closed after a timeout or protocol error.
- Normal and Telnet response modes, immutable `Response` objects, and all controller error codes preserved.
- Descriptions and hints for 49 known controller / TCS error codes, keeping the raw reply.
- Firmware source fingerprints in `docs/firmware_manifest.json` and a generated command reference.

### Examples

- 30 task-based scripts in 14 numbered folders plus an asynchronous read-only example, configured by variables
  at the top of each file. Each folder has an English and Korean README.
- Shared session setup and initialization with conditional Home (`examples/common`).
- PC JSON storage for motion profiles and named teaching positions, with validation and atomic file replacement
  (`examples/config`).
- Move examples require an explicit target, location slot or position name before connecting.

### Documentation

- English and Korean README, usage guide, command reference, error code descriptions and validation record.
