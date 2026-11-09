# Profile storage and operation examples implementation plan

**Goal:** Keep MSpeed and numbered motion profiles in one PC JSON file, and give each example operation its own runnable file.

**Architecture:** Standard-library JSON storage next to examples. Load and validate before robot connection or initialization; save atomically without contacting hardware. Initialization reads the same file and reapplies MSpeed plus profiles on each startup. Core SDK remains a raw command interface. Existing teaching coordinates are preserved.

**Tech stack:** Python 3.10+, json/pathlib/tempfile, pytest loopback device fixtures.

1. Add failing tests for profile roundtrip, invalid files leaving originals intact, configuration applied by initialization, per-operation files with no ACTION branch, grasp failure and release completion.
2. Implement motion_profiles.py with named fields, strict schema/finite numbers, atomic save, and explicit apply. Seed motion_profiles.json from existing initialization values (Ramp 0.2 seconds; MSpeed 20%). No manufacturer-recommended values claimed.
3. Replace hardcoded profiles in initialization and startup; load before connections and retain explicit startup command sequence. Split 03 into save/apply/read, 07 into read/settings/open/close, 08 into grasp/release, 09 into show/teach-joint/teach-cartesian/store, 10 into conversion directions, 13 into list/save/move, 14 into free/restore. Extract only reusable teaching JSON functions. Retire superseded ACTION files.
4. Migrate existing example tests; keep transport/command regressions. Verify no initialization on query, no unexpected gripper opening on generic motion, invalid configuration rejected before hardware actions, no automatic retries.
5. Update examples README, root README, changelog and source distribution inventory. Preserve manufacturer parameter references. Run loopback-only tests, lint and build; inspect source archive for JSON/common files. Review diffs and copy only verified changed files back after baseline hash checks.

**Boundaries:** No live hardware commands, firmware changes, publication, commits, or overwrite of teaching_positions.json. PC file persistence is not controller flash persistence; applications must reapply after controller restart. Free mode remains explicit until restore; disconnect is not Halt.
