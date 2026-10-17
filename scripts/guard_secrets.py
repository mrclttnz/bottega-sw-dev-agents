"""PreToolUse hook (Write, Edit, MultiEdit, NotebookEdit).

Blocks writing recognizable secrets to files and asks for confirmation on
suspicious assignments. On unreadable input it stays out of the way, so it
never wedges the session.
"""

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from secret_patterns import find_certain, find_suspicious  # noqa: E402


def written_text(tool_input):
    parts = [tool_input.get("content"), tool_input.get("new_string"), tool_input.get("new_source")]
    for edit in tool_input.get("edits") or []:
        if isinstance(edit, dict):
            parts.append(edit.get("new_string"))
    return "\n".join(p for p in parts if isinstance(p, str))


def respond(decision, reason):
    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": decision,
            "permissionDecisionReason": reason,
        }
    }))
    sys.exit(0)


def main():
    try:
        event = json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
        sys.exit(0)

    tool_input = event.get("tool_input") or {}
    path = tool_input.get("file_path") or tool_input.get("notebook_path") or "file"
    text = written_text(tool_input)
    if not text:
        sys.exit(0)

    certain = find_certain(text)
    if certain:
        respond(
            "deny",
            f"Bottega · secret guard: {path} contains what looks like a real secret "
            f"({', '.join(sorted(set(certain)))}). Secrets must never be written to files: use an environment "
            "variable or a secret manager, and put only a placeholder in .env.example. "
            "If the secret is real and has already been exposed, revoke and rotate it.",
        )

    suspicious = find_suspicious(text)
    if suspicious and not os.path.basename(path).startswith(".env"):
        respond(
            "ask",
            f"Bottega · secret guard: {path} contains assignments that look like literal credentials "
            f"({'; '.join(suspicious[:3])}). Confirm only if they are fake test values.",
        )

    sys.exit(0)


if __name__ == "__main__":
    main()
