# Bottega team protocol

This document applies to **every** Bottega agent and skill. When it conflicts with other instructions, security wins first, then this protocol.

## 1. Shared state: the project's `docs/` folder

The team has no memory between invocations. The project's memory is the `docs/` folder at the root of the project being worked on.

| File | Owner | Content |
|---|---|---|
| `docs/STATUS.md` | orchestrator | Current phase, gates passed, slice in progress, blockers, activity log |
| `docs/01-vision.md` | product-analyst | Problem, users, value, MVP scope, success metrics |
| `docs/02-requirements.md` | product-analyst | FR, NFR, SR, user stories, acceptance criteria, open questions |
| `docs/03-ux.md` | ux-designer | Personas, flows, screens, states, accessibility |
| `docs/04-architecture.md` | architect | C4 views, components, stack, integrations, quality attributes |
| `docs/adr/ADR-NNNN-title.md` | whoever makes the decision | Architecture Decision Record, one decision per file |
| `docs/05-data.md` | data-architect | Data model, schema, indexes, migrations, data classification |
| `docs/06-threat-model.md` | security-engineer | Assets, actors, trust boundaries, STRIDE threats, mitigations |
| `docs/07-plan.md` | tech-lead | Modules, interfaces, vertical slices, traceability |
| `docs/08-test-strategy.md` | tester | Test pyramid, tools, test data, expected coverage |
| `docs/09-release.md` | devops | Environments, pipeline, configuration, runbook, rollback, observability |
| `docs/reviews/` | code-reviewer, security-engineer | One report per slice or audit: `SL-01-code.md`, `SL-01-security.md`, `audit-YYYY-MM-DD.md` |

Templates for these files live in `${CLAUDE_PLUGIN_ROOT}/templates/`.

**Read first, write after.** Before acting, read `docs/STATUS.md` and the documents your work depends on. When you finish, update your own files and add one line to the *Log* in `docs/STATUS.md`:

```
- YYYY-MM-DD · <agent> · <what you did> · <files touched>
```

Do not edit documents you do not own. If you find a mistake in someone else's document, report it.

## 2. Identifiers and traceability

| Prefix | Meaning | Example |
|---|---|---|
| `FR-NNN` | Functional requirement | FR-004 |
| `NFR-NNN` | Non-functional requirement (performance, availability, usability…) | NFR-002 |
| `SR-NNN` | Security or privacy requirement | SR-007 |
| `US-NNN` | User story | US-012 |
| `AC-NNN.n` | Acceptance criterion of user story NNN | AC-012.3 |
| `Q-NNN` | Open question | Q-003 |
| `ASM-NNN` | Assumption awaiting confirmation | ASM-001 |
| `ADR-NNNN` | Architecture decision | ADR-0005 |
| `THR-NNN` | Threat in the threat model | THR-009 |
| `SL-NN` | Vertical slice in the plan | SL-03 |
| `CHG-NNN` | Change request on an existing project | CHG-002 |
| `CR-SLNN-NNN` | Code review finding | CR-SL03-002 |
| `SEC-SLNN-NNN` | Security finding (`SEC-AUD-NNN` for audits) | SEC-SL03-001 |

Every item cites its parents. A user story cites FRs, a slice cites user stories and SRs, a test cites ACs, and a finding cites a file and line. The chain **FR → US → AC → SL → test → code** must stay reconstructable.

## 3. Rules of conduct

1. **No invented requirements.** If information is missing, record an `ASM-NNN` (assumption) or a `Q-NNN` (question) and surface it. Never fill gaps silently.
2. **Evidence rule.** Say "done", "works" or "tests green" only if your report contains fresh output from the command that proves it. Without evidence the status is `UNVERIFIED`.
3. **Minimal scope.** Do only what your slice or phase asks for. No unrelated refactoring, no unrequested features, no dependency upgrades without a reason.
4. **Security is non-negotiable.** Always apply `${CLAUDE_PLUGIN_ROOT}/references/security-standard.md`. If a requirement conflicts with security, stop and report `NEEDS_DECISION`.
5. **Tracked decisions.** Non-trivial choices (stack, database, authentication, hosting, major libraries, trade-offs) become an ADR. Never make them implicitly in code.
6. **You do not talk to the user.** Subagents cannot ask questions. When you need a decision, return it in your report with options, trade-offs and a recommendation. The orchestrator will ask.
7. **Verified dependencies.** Before adding a package, verify that it really exists on the official registry, that it is maintained, and that the name is exact. Invented or look-alike package names are an attack vector.

## 4. Final report format

Every agent **always** ends with this block, which is its answer to the orchestrator:

```markdown
## Report — <agent-name>
**Outcome:** DONE | DONE_WITH_CONCERNS | BLOCKED | NEEDS_DECISION | UNVERIFIED
**Scope:** <phase or slice, e.g. SL-02>
**Files changed:** <list of paths, or "none">
**Summary:** <3-6 lines on what was done and why>
**Evidence:** <commands run with the relevant output excerpt; "n/a" only for purely documentation work>
**Traceability:** <IDs covered, e.g. US-003, AC-003.1-3, SR-002>
**Decisions needed:** <for each: question, options with trade-offs, recommendation. Or "none">
**Risks and technical debt:** <list, or "none">
**Suggested next step:** <who should do what>
```

## 5. Definition of Done for a slice

A slice `SL-NN` is done only when **all** of these hold:

- [ ] Every acceptance criterion of the slice has at least one automated test that verifies it
- [ ] The tests were written before the implementation and seen failing ("red" evidence)
- [ ] The whole suite is green (fresh "green" evidence, not just the new tests)
- [ ] Linter, formatter and type-check pass with no errors
- [ ] Code review has no open `BLOCKER` findings
- [ ] Security review has no open `BLOCKER` findings
- [ ] Secret and dependency scans are clean, or residual vulnerabilities are accepted under the review contract
- [ ] Database migrations, if any, are reversible and tested
- [ ] Documentation is updated (README, API, `docs/` when something changes)
- [ ] `docs/STATUS.md` is updated
