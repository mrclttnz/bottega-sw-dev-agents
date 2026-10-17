---
name: plan
description: Planning phase. Has the tech-lead produce modules, contracts and vertical slices traced to requirements, the tester the test strategy, and the critic a review of the plan, then puts it to the user. Use after the design phase.
---

# P4 — Development plan

Rules: `${CLAUDE_PLUGIN_ROOT}/references/protocol.md`. Prerequisite: G3 passed.

1. Delegate to `bottega:tech-lead`: "Produce `docs/07-plan.md` with structure, contracts, conventions, the SL-00 foundations slice, the vertical slices, the execution order and the traceability matrix."
2. Delegate to `bottega:tester` in mode A: "Produce `docs/08-test-strategy.md`, consistent with the stack and the plan."
3. Delegate to `bottega:critic` a review of the plan and the strategy: slices too big, wrong dependencies, user stories or SRs not covered, risky ordering, too few tests for the SRs.
4. Resolve the objections with the tech-lead, and bring to the user only the real choices, such as the order of priorities.

## Gate G4
- [ ] every Must user story and every SR is covered by at least one slice
- [ ] no slice is size L
- [ ] SL-00 includes CI with lint, tests and blocking security scans
- [ ] API contracts are defined for slices where backend and frontend run in parallel
- [ ] the test strategy includes negative and authorization tests

Show the user the list of slices (ID, goal, user stories, size) as a roadmap and ask for approval. Update `docs/STATUS.md`, filling in the slice table with status `TODO`. Next step: `/bottega:build SL-00`.
