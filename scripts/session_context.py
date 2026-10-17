"""SessionStart hook: if the project uses Bottega, remind Claude of the phase and next steps."""

import json
import os
import re
import sys

MAX_CHARS = 2500


def main():
    project = os.environ.get("CLAUDE_PROJECT_DIR") or os.getcwd()
    status = os.path.join(project, "docs", "STATUS.md")
    if not os.path.isfile(status):
        sys.exit(0)

    try:
        with open(status, encoding="utf-8") as f:
            text = f.read()
    except OSError:
        sys.exit(0)

    # Header, gates and slices: everything up to (not including) the log section.
    excerpt = re.split(r"(?m)^## Log", text, maxsplit=1)[0].strip()
    if len(excerpt) > MAX_CHARS:
        excerpt = excerpt[:MAX_CHARS] + "\n…(truncated, read docs/STATUS.md)"

    context = (
        "This project is managed with Bottega (plugin `bottega`). Current status from docs/STATUS.md:\n\n"
        f"{excerpt}\n\n"
        "To resume, use /bottega:status or /bottega:start. Respect the gates and the security standard."
    )
    print(json.dumps({"hookSpecificOutput": {"hookEventName": "SessionStart", "additionalContext": context}}))


if __name__ == "__main__":
    main()
