"""PreToolUse hook (Bash).

- Blocks insecure commands (piping from the Internet into a shell, disabling
  TLS verification, 777 permissions, catastrophic deletions, plaintext secrets).
- Asks for confirmation on irreversible or outward-facing actions (deploys,
  pushes, publishing, infrastructure changes, dropping tables, reading .env).
"""

import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from secret_patterns import find_certain  # noqa: E402

BLOCK = [
    (re.compile(r"\b(?:curl|wget)\b[^|;&]*\|\s*(?:sudo\s+)?(?:ba|z|da|k)?sh\b"),
     "it runs a script downloaded from the Internet directly in the shell. Download it, check its content "
     "and checksum, then run it"),
    (re.compile(r"\brm\s+(?:-[a-zA-Z]*[rR][a-zA-Z]*\s+(?:-[a-zA-Z]+\s+)*|--recursive\s+)(?:/|~|\$HOME|/\*|\.\.?)(?:\s|$|/\s|/\*)"),
     "it recursively deletes the root, the home or the current directory"),
    (re.compile(r"\bchmod\s+(?:-R\s+)?0?777\b"),
     "it sets 777 permissions. Use the minimum permissions needed"),
    (re.compile(r"(?:git\s+config[^\n]*http\.sslVerify\s+false|npm\s+config\s+set\s+strict-ssl\s+false|"
                r"NODE_TLS_REJECT_UNAUTHORIZED\s*=\s*0|PYTHONHTTPSVERIFY\s*=\s*0|\bcurl\b[^\n]*\s(?:-k|--insecure)\b|"
                r"\bpip\b[^\n]*--trusted-host)"),
     "it disables TLS certificate verification"),
    (re.compile(r"\bgit\s+push\b[^\n]*(?:--force\b|-f\b)[^\n]*\b(?:main|master|production|prod)\b"),
     "it force-pushes to a main branch"),
]

ASK = [
    (re.compile(r"\bgit\s+push\b"), "push to a remote repository"),
    (re.compile(r"(?:^|\s)--no-verify\b"), "skipping git verification hooks"),
    (re.compile(r"\bterraform\s+(?:apply|destroy|import|state\s+rm)\b|\bpulumi\s+(?:up|destroy)\b|\btofu\s+(?:apply|destroy)\b"),
     "changing or destroying infrastructure"),
    (re.compile(r"\bkubectl\s+(?:apply|delete|replace|patch|scale|rollout\s+undo)\b|\bhelm\s+(?:install|upgrade|uninstall|rollback)\b"),
     "changing a Kubernetes cluster"),
    (re.compile(r"\b(?:fly|flyctl)\s+deploy\b|\bvercel\b[^\n]*--prod\b|\brailway\s+up\b|\bnetlify\s+deploy\b[^\n]*--prod\b|"
                r"\bgcloud\b[^\n]*\bdeploy\b|\baz\s+(?:webapp|containerapp|functionapp)\b[^\n]*\b(?:up|deploy|create)\b|"
                r"\baws\s+(?:ecs\s+update-service|lambda\s+update-function-code|cloudformation\s+deploy)\b|\bheroku\b[^\n]*\b(?:deploy|releases)\b"),
     "deploying to a remote environment"),
    (re.compile(r"\baws\b[^\n]*\b(?:delete|terminate|remove|rb)\b|\bgcloud\b[^\n]*\bdelete\b|\baz\b[^\n]*\bdelete\b"),
     "deleting cloud resources"),
    (re.compile(r"\b(?:npm|pnpm|yarn)\s+publish\b|\btwine\s+upload\b|\bcargo\s+publish\b|\bdocker\s+push\b|\bgh\s+release\s+create\b"),
     "publishing a package or image"),
    (re.compile(r"(?i)\b(?:drop\s+(?:database|schema|table)|truncate\s+table)\b"),
     "deleting data from the database"),
    (re.compile(r"\b(?:cat|less|more|head|tail|bat)\s+[^\n|;&]*\.env(?:\.(?!example\b)[\w.]+)?(?:\s|$)"),
     "reading a .env file that may contain secrets (they would end up in the conversation)"),
    (re.compile(r"\bgit\s+reset\s+--hard\b|\bgit\s+clean\s+-[a-zA-Z]*f"),
     "irreversibly discarding local changes"),
]


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

    command = (event.get("tool_input") or {}).get("command")
    if not isinstance(command, str) or not command.strip():
        sys.exit(0)

    for regex, reason in BLOCK:
        if regex.search(command):
            respond("deny", f"Bottega · command guard: command blocked because {reason}.")

    certain = find_certain(command)
    if certain:
        respond("deny", f"Bottega · command guard: the command contains a plaintext secret ({', '.join(sorted(set(certain)))}). "
                        "Pass it through an environment variable that is already set.")

    reasons = [reason for regex, reason in ASK if regex.search(command)]
    if reasons:
        respond("ask", f"Bottega · command guard: confirmation required ({'; '.join(reasons)}).")

    sys.exit(0)


if __name__ == "__main__":
    main()
