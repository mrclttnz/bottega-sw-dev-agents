---
name: review
description: On-demand independent review of code changes (current diff, branch, commit or path), run in parallel by the code reviewer and the security engineer, with classified findings and a proposed fix. Use to review code outside a slice cycle, such as hand-written code or urgent changes.
argument-hint: "[diff | <branch> | <commit> | <path>] (empty = uncommitted changes)"
---

# Code and security review

Rules: `${CLAUDE_PLUGIN_ROOT}/references/review-contract.md`. Target: `$ARGUMENTS`.

1. **Determine the scope:**
   - empty → `git diff HEAD` plus untracked files (`git status --porcelain`)
   - a branch name → `git diff <base-branch>...<branch>` (ask for the base if it isn't obvious; usually `main`)
   - a commit → `git show <commit>`
   - a path → full review of the given files

   If the scope is empty, tell the user and stop.
2. **Pick an identifier** for the report: the current slice if relevant, otherwise `REV-YYYY-MM-DD`.
3. **Launch in parallel** `bottega:code-reviewer` and `bottega:security-engineer` (mode B), with the same scope and identifier.
4. **Summarize** for the user a single table sorted by severity (ID, severity, class, location, one-line problem) and the overall verdict. The details stay in the reports under `docs/reviews/`.
5. **Propose** with AskUserQuestion: "Fix BLOCKER and FIX-IN-SLICE findings" (recommended), "Fix BLOCKERs only", "No fixes now". If the user chooses to fix, delegate to the developers and then request a re-check according to the contract.
