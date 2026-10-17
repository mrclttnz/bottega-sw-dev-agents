"""Secret detection in text, shared by the Bottega hooks.

Two levels:
- CERTAIN: recognizable credential formats, high confidence -> block.
- SUSPICIOUS: generic assignments like password = "..." -> ask for confirmation.
"""

import re

CERTAIN = [
    ("private key", re.compile(r"-----BEGIN (?:RSA |EC |DSA |OPENSSH |PGP |ENCRYPTED )?PRIVATE KEY(?: BLOCK)?-----")),
    ("AWS access key", re.compile(r"\b(?:AKIA|ASIA)[0-9A-Z]{16}\b")),
    ("GitHub token", re.compile(r"\b(?:gh[pousr]_[A-Za-z0-9]{36,}|github_pat_[A-Za-z0-9_]{60,})\b")),
    ("GitLab token", re.compile(r"\bglpat-[A-Za-z0-9_\-]{20,}\b")),
    ("Slack token", re.compile(r"\bxox[abposr]-[A-Za-z0-9-]{10,}\b")),
    ("Stripe secret key", re.compile(r"\b(?:sk|rk)_live_[A-Za-z0-9]{20,}\b")),
    ("Google API key", re.compile(r"\bAIza[0-9A-Za-z_\-]{35}\b")),
    ("Anthropic API key", re.compile(r"\bsk-ant-[A-Za-z0-9_\-]{20,}\b")),
    ("OpenAI API key", re.compile(r"\bsk-(?:proj-|svcacct-)?[A-Za-z0-9_\-]{20,}T3BlbkFJ[A-Za-z0-9_\-]{20,}\b")),
    ("SendGrid API key", re.compile(r"\bSG\.[A-Za-z0-9_\-]{22}\.[A-Za-z0-9_\-]{43}\b")),
    ("npm token", re.compile(r"\bnpm_[A-Za-z0-9]{36}\b")),
    ("URL with credentials", re.compile(r"\b[a-z][a-z0-9+.\-]*://[^\s:/@'\"]+:[^\s@'\"$%{}<>]{6,}@[^\s'\"]+", re.IGNORECASE)),
]

_SECRET_NAME = r"(?:password|passwd|pwd|secret|api[_-]?key|apikey|access[_-]?token|auth[_-]?token|private[_-]?key|client[_-]?secret)"
SUSPICIOUS = re.compile(
    rf"""(?ix)
    \b[\w.\-]*{_SECRET_NAME}[\w\-]*\b       # variable or key name
    ["']?\s*[:=]\s*                         # assignment
    (["'])(?P<value>[^"'\s]{{8,}})\1        # quoted literal value
    """
)

# Values that indicate a placeholder or a reference, not a real secret.
_PLACEHOLDER = re.compile(
    r"(?i)(change[_-]?me|example|placeholder|dummy|fake|test|sample|your[_-]|"
    r"x{4,}|\*{4,}|<[^>]*>|\$\{|\{\{|process\.env|os\.environ|getenv|env\(|secrets\.)"
)

# Credentials in URLs that are clearly placeholders.
_URL_PLACEHOLDER = re.compile(r"(?i)://[^:/@]+:(?:password|pass|pwd|secret|changeme|\$\{?[A-Z_]+\}?|<[^>]+>)@")


def find_certain(text):
    """Return the kinds of secret recognized with high confidence."""
    found = []
    for name, regex in CERTAIN:
        for m in regex.finditer(text):
            if name == "URL with credentials" and _URL_PLACEHOLDER.search(m.group(0)):
                continue
            found.append(name)
            break
    return found


def find_suspicious(text):
    """Return generic assignments that look like real secrets."""
    found = []
    for m in SUSPICIOUS.finditer(text):
        if _PLACEHOLDER.search(m.group("value")):
            continue
        found.append(m.group(0)[:40] + ("…" if len(m.group(0)) > 40 else ""))
    return found
