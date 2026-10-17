---
name: build
description: Runs the full development cycle of one vertical slice (test-first, implementation, verification, code review and security review in parallel, fixes, Definition of Done), coordinating tester, developers, code reviewer and security engineer. Use to implement the next slice in the plan, or a specific one.
argument-hint: "[SL-NN] (empty = next slice to do)"
---

# P5 — Slice development cycle

Rules: `${CLAUDE_PLUGIN_ROOT}/references/protocol.md` and `${CLAUDE_PLUGIN_ROOT}/references/review-contract.md`. Prerequisite: G4 passed.

Slice: `$ARGUMENTS`. If empty, take from `docs/STATUS.md` the first `TODO` slice whose dependencies are met.

## 0. Preparation
- Read the slice in `docs/07-plan.md`. Check that its dependencies are `DONE`.
- If using git, record the starting commit (`git rev-parse HEAD`) as the slice **base**: the reviews will diff against it. If the working tree has uncommitted changes unrelated to the slice, ask the user how to proceed.
- Mark the slice `IN PROGRESS` in `docs/STATUS.md`.
- Tell the user in 2 lines what the slice will do.

**SL-00 (foundations):** the work is done by `bottega:devops` (mode A), together with the developer named in the plan for the code scaffolding. The tester checks that the test runner works with a sample test. From step 3 onwards the cycle is the same.

## 1. Red: tests before code
Delegate to `bottega:tester`, mode B, for the slice. Require evidence that the tests **fail** for the right reason.

## 2. Green: implementation
Delegate to `bottega:backend-developer` and/or `bottega:frontend-developer`, according to the plan. If both are needed and the contracts are defined, launch them in parallel. If the contracts aren't defined, backend first. If there are migrations, involve `bottega:data-architect` before the backend.

Pass in the prompt: the slice ID, the tests to make pass, and the constraints. If a report comes back `NEEDS_DECISION`, ask the user and send it back.

## 3. Verification
Delegate to `bottega:tester`, mode C. If the suite isn't green or an AC isn't covered, go back to step 2 with the details.

## 4. Independent reviews, in parallel
Launch **together**, in a single message:
- `bottega:code-reviewer` → `docs/reviews/SL-NN-code.md`
- `bottega:security-engineer` in mode B → `docs/reviews/SL-NN-security.md`

In the prompt, give the diff base (`git diff <base>`, so uncommitted changes are included) and the slice.

## 5. Fixes (at most 3 cycles)
If there are BLOCKER or FIX-IN-SLICE findings:
1. Pass them to the right developer, with the IDs and the report paths.
2. After the fix, run the tester again (mode C), then **only** the reviewer who opened the findings, in re-check mode.
3. After 3 cycles with BLOCKERs still open: stop and take the problem to the user.

BACKLOG findings go in the *Technical debt* section of `docs/STATUS.md`. A MEDIUM security finding can be accepted only by the user, through a risk-acceptance ADR. CRITICAL, HIGH and [MUST] violations are never accepted.

## 6. Definition of Done (gate G5)
Check the protocol's DoD yourself, item by item, against the evidence in the reports. Don't mark the slice DONE if even one item is missing.

Then:
- Update `docs/STATUS.md`: slice `DONE`, date, review reports, technical debt.
- If the user chose automatic commits: `git add` the slice's files (check with `git status` that no sensitive files are included) and commit `feat(SL-NN): <goal>`, with the IDs of the covered user stories in the body.
- Report to the user in a few lines: what works now, how to try it (command or local URL), findings fixed, debt added.
- Ask whether to continue with the next slice or stop here.

When every MVP slice is `DONE`, move to phase P6: tester in mode D and `/bottega:security-audit`.
