# Bottega Python standard

These rules apply to every project, or part of a project, written in Python. They supplement `security-standard.md` and never override it.

Each rule is tagged with the class of finding its violation produces (see `review-contract.md`):
- **[BLOCKER]**: the slice cannot close until it is fixed.
- **[FIX-IN-SLICE]**: it must be fixed in the current slice, with a targeted check.
- Untagged rules are recommendations: the reviewer classifies a violation by its impact, usually as `BACKLOG`.

## 1. Environment and dependencies
- [BLOCKER] Always work inside a virtual environment, never with the system Python. The project's environment lives in `.venv/` at the repository root (created with `python -m venv .venv`, or managed by the tool chosen in the plan, such as `uv` or `poetry`), and `.venv/` is listed in `.gitignore`.
- [BLOCKER] Never install packages into the system Python: no `sudo pip`, no `pip install --user`, no `--break-system-packages`, no `uv pip install --system`. Before running `pip`, check that the virtual environment is active (`VIRTUAL_ENV` is set, or call `.venv/bin/pip` / `.venv/bin/python` directly).
- Containers follow the same rule: the Dockerfile creates a virtual environment and installs dependencies there.
- Python command-line tools needed outside a project are installed with `pipx` or `uv tool`, which give each tool its own isolated environment.
