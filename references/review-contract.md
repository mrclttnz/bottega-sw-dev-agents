# Review contract

Rules shared by `code-reviewer`, `security-engineer`, and whoever consumes their results.

## Finding format

```markdown
### CR-SL03-002 · HIGH · BLOCKER
- **Location:** `src/orders/service.ts:88`
- **Category:** correctness | security (CWE-xxx) | performance | maintainability | tests | design
- **Problem:** what is wrong, in one or two sentences.
- **Scenario:** concrete input or state → wrong behavior or impact.
- **Suggested fix:** how to fix it (with example code if useful).
- **Verification:** how to prove it is fixed (test to add, command to run).
- **Status:** OPEN | RESOLVED | ACCEPTED (see ADR-NNNN) | DISMISSED (rationale)
```

## Severity
| Severity | Meaning |
|---|---|
| **CRITICAL** | Remotely exploitable without authentication, data loss or exposure, code execution, authentication bypass, or a bug that corrupts data |
| **HIGH** | Vulnerability exploitable under realistic preconditions, or a bug that breaks an acceptance criterion |
| **MEDIUM** | Defect with limited impact or unlikely conditions, or missing defense in depth |
| **LOW** | Robustness, clarity or maintainability improvement |
| **INFO** | Observation, no action required |

## Class (drives the gate)
| Class | Rule |
|---|---|
| **BLOCKER** | The slice cannot close. Applies to every CRITICAL or HIGH finding, every violation of a [MUST] rule in the security standard, and every unmet acceptance criterion |
| **FIX-IN-SLICE** | Must be fixed in the current slice, but needs only a targeted check, not a full new review |
| **BACKLOG** | Recorded as technical debt in `docs/STATUS.md`, to be scheduled |

## Risk acceptance
- **CRITICAL** and **HIGH** security findings and [MUST] violations **cannot be accepted**. They must be fixed.
- A **MEDIUM** security finding can be accepted only by the user, explicitly, through a risk-acceptance ADR that states the rationale, compensating controls and a review date.

## Fix cycle
1. The reviewer produces the report with its findings.
2. The developer fixes the BLOCKER and FIX-IN-SLICE findings and adds a regression test for every bug.
3. The reviewer **re-checks only** the open findings and the diff of the fix. At this point it may open new findings only if they are BLOCKERs introduced by the fix (anti-loop rule).
4. After **3 cycles** with BLOCKERs still open, the orchestrator stops and takes the problem to the user.

## Reviewer rules
- Report only findings verified by reading the code, never generic speculation. If you are unsure, write "TO VERIFY" and explain the check you would run.
- Every finding has a precise location and a concrete scenario.
- The reviewer **does not change the code**: it describes the problem and the fix.
- Also acknowledge what is done well, in one line, to reinforce good choices.
