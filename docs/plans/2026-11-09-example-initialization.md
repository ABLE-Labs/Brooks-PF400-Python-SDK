# Example initialization implementation plan

**Goal:** Audit every runnable example and ensure that control commands have the preparation performed by the existing pendant, without changing low-level SDK connect semantics.

**Architecture:** An examples-only initialization.py provides session configuration, shared profile/gripper/power/Attach setup, and conditional Home with result verification. Each example explicitly calls the appropriate preparation after connecting. Configuration remains Python code, with no CLI flags. SDK core and user-selected HOST/ACTION/targets/AXES remain unchanged.

1. Add failing wire-order tests for session setup, initialization, conditional Home and abort-on-error behavior.
2. Implement configurable example profiles/gripper settings and finite power/Home deadlines. Never retry device commands.
3. Audit/integrate every example. Read-only queries/conversions and current-position capture configure sessions only. Normal controls initialize; movements check Home. Stop and power-off/detach do not initialize first. Gripper release and JSON capture preserve current mechanical state.
4. Extend the power example with an explicit initialize action, preserving the user's current action. Validate saved target axis counts before any initialization motion.
5. Update wire regressions and add assertions that read/save/stop do not send power/home/gripper-motion commands.
6. Document the per-example preparation matrix, rebuild artifacts, install/import the wheel, and verify archive contents. No live robot commands, commits or pushes.
