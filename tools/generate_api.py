"""Regenerate explicit command wrappers and provenance from a firmware folder.

Usage: python tools/generate_api.py --firmware /path/to/tcs_firmware_project
Only this generator reads firmware. Neither building nor importing the SDK needs it.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re

from api_spec import EXCLUDED, SPECS

ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--firmware", type=Path, required=True)
    args = parser.parse_args()
    firmware = args.firmware
    found = {}
    files = {}
    for path in sorted(firmware.glob("*.gpl")):
        raw = path.read_bytes()
        text = raw.decode("utf-8-sig")
        for match in re.finditer(r"^[ \t]*Public[ \t]+(?:Sub|Function)[ \t]+Cmd_(\w+)", text, re.M | re.I):
            name = match[1]
            start = text.rfind("#Region", 0, match.start())
            comments = "\n".join(
                re.sub(r"^\s*' ?", "", line)
                for line in text[max(0, start) : match.start()].splitlines()
                if line.lstrip().startswith("'")
            )
            found[name] = dict(
                source_file=path.name,
                source_line=text[: match.start()].count("\n") + 1,
                firmware_comments=comments.strip(),
            )
            files[path.name] = hashlib.sha256(raw).hexdigest()
    commands = {spec["command"] for spec in SPECS}
    if len(SPECS) != 82 or len(commands) != 82 or set(found) != commands | set(EXCLUDED):
        raise SystemExit(
            f"Firmware/API mismatch: unwrapped={set(found) - commands - set(EXCLUDED)}, absent={commands - set(found)}"
        )
    entries = []
    for spec in SPECS:
        entries.append(
            {**spec, **found[spec["command"]], "verification": "mock TCP only; hardware not tested"}
        )
    manifest = dict(
        firmware_project="PF400 TCP Command Server",
        version="Command Server 3.0D4 10-25-2024",
        source_sha256=files,
        commands=entries,
        excluded_vision=list(EXCLUDED),
    )
    (ROOT / "docs/firmware_manifest.json").write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    mappings = {
        spec["command"]: (spec["counts"], "status" if spec["command"] == "Reset" else "motion")
        for spec in SPECS
    }
    (ROOT / "src/pf400/commands.py").write_text(
        '"""Generated non-vision command registry. Do not edit by hand."""\n\nCOMMANDS = '
        + repr(mappings)
        + "\n",
        encoding="utf-8",
    )
    for asynchronous, filename, classname, base in [
        (False, "client.py", "PF400", "ClientBase"),
        (True, "async_client.py", "AsyncPF400", "AsyncClientBase"),
    ]:
        text = [
            '"""Generated explicit firmware API; regenerate with tools/generate_api.py."""',
            "from __future__ import annotations",
            "",
            "from collections.abc import Sequence",
            "from .protocol import Response, Scalar",
            f"from .client_base import {base}" + ("" if asynchronous else ", _params, _vector"),
            "",
            "",
            f"class {classname}({base}):",
            '    """82 non-vision TCS commands. See docs/API.md for wire semantics."""',
            "",
        ]
        for spec in SPECS:
            sig = spec["signature"]
            sep = ", " if "*" in sig else ", *, "
            signature = (
                sig + sep if sig else "*, "
            ) + "channel: str | None = None, timeout: float | None = None"
            result = "None" if spec["command"] == "Exit" else "Response"
            text.append(
                f"    {'async ' if asynchronous else ''}def {spec['method']}(self, {signature}) -> {result}:"
            )
            info = found[spec["command"]]
            doc = (
                f"{spec['command']} — {info['source_file']}:{info['source_line']}.\n\n"
                + info["firmware_comments"]
            )
            text.append('        r"""' + doc.replace('"""', '\\"\\"\\"').replace("\n", "\n        ") + '"""')
            if asynchronous:
                # Forward according to Python's parsed signature, preserving keyword-only arguments.
                import ast

                node = ast.parse(f"def f({sig}): pass").body[0]
                forwarded = [arg.arg for arg in node.args.args]
                if node.args.vararg:
                    forwarded.append("*" + node.args.vararg.arg)
                forwarded += [arg.arg + "=" + arg.arg for arg in node.args.kwonlyargs]
                arguments = ", ".join(forwarded + ["channel=channel", "timeout=timeout"])
                text.append(f"        return await self._call({spec['method']!r}, {arguments})")
            else:
                text.append(
                    f"        return self._invoke({spec['command']!r}, {spec['arguments']}, channel=channel, timeout=timeout)"
                )
            text.append("")
        (ROOT / "src/pf400" / filename).write_text("\n".join(text) + "\n", encoding="utf-8")
    docs = [
        "# Firmware command API",
        "",
        "82 non-vision firmware commands. Every method has keyword-only `channel` and `timeout`.",
        "Default channel: motion, except `reset` which defaults to status. `connect()` sends no commands.",
        'Before per-robot calls on status, explicitly use `select_robot(robot_id, channel="status")`.',
        "Status-port Reset requires robot selection 0; Halt requires the intended robot selection.",
        "",
        "Numeric units, robot/axis availability and controller index limits remain firmware-defined.",
        "Sequences are expanded in wire order. Omitted trailing arguments remain omitted; gaps are rejected.",
        "Profile setters require all 8 fields; GraspData and HeightDetect setters require complete groups.",
        "This prevents silently zero-padding missing values. `execute()` exposes supported raw parameter forms.",
        "ReleasePlate argument 3 is InRange, not a profile ID. Payload is a percentage, not a mass.",
        "HomeAll affects all robots. MoveExtraAxis only schedules an extra-axis target for the next Cartesian move.",
        "Disconnect/cancellation/timeout do not stop the robot. No command is automatically retried.",
        "",
        "## Method index",
        "",
        "| Firmware | Python | Source |",
        "|---|---|---|",
    ]
    for spec in sorted(entries, key=lambda s: s["command"].lower()):
        docs.append(
            f"| `{spec['command']}` | `{spec['method']}({spec['signature']})` | {spec['source_file']}:{spec['source_line']} |"
        )
    for spec in sorted(entries, key=lambda s: s["command"].lower()):
        docs.extend(
            [
                "",
                f"## {spec['command']}",
                "",
                f"`{spec['method']}({spec['signature']})`",
                "",
                f"Source: `{spec['source_file']}:{spec['source_line']}`. Verification: mock TCP only.",
                "",
                "```text",
                spec["firmware_comments"]
                or "See implementation and firmware documentation; no header comment.",
                "```",
            ]
        )
    (ROOT / "docs/API.md").write_text("\n".join(docs) + "\n", encoding="utf-8")
    print(
        "Generated 82 sync methods, 82 async methods, reference and firmware manifest; excluded 8 vision commands."
    )


if __name__ == "__main__":
    main()
