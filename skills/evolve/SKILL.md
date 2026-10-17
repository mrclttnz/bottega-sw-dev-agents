---
name: evolve
description: Handles a change request or new feature on an existing project with a complete mini-cycle (requirements, impact analysis, design and threat model updates, new slices, development with code and security review). Use after the first release, or when a requirement changes.
argument-hint: "<description of the change or feature>"
---

# Evolution: change request

Request: `$ARGUMENTS`. Rules: `${CLAUDE_PLUGIN_ROOT}/references/protocol.md`.

Prerequisite: an existing `docs/`. If the project has code but no `docs/`, first propose a survey: `bottega:architect` and `bottega:tech-lead` reconstruct architecture, data and plan from the code, and `bottega:security-engineer` runs an initial audit.

1. **Clarify the request** with the user, using the questions from the `bottega:requirements` skill, limited to this feature: who, what, why, error cases, permissions, data.
2. **Requirements:** `bottega:product-analyst` updates `docs/02-requirements.md` with new IDs (never renumber), and marks changed or removed requirements as such.
3. **Impact analysis:** `bottega:tech-lead` produces the "Change request CHG-NNN" section in `docs/07-plan.md`. Classify the impact:
   - **Low** (no change to architecture, data or attack surface): go to step 5.
   - **Medium or high:** step 4.
4. **Design update:** depending on what's needed, involve `bottega:architect` (new ADR), `bottega:data-architect` (migrations compatible with existing data) and `bottega:ux-designer`. **Always**, if the attack surface changes or new data is processed, `bottega:security-engineer` updates the threat model.
5. **New slices:** the tech-lead adds them to the plan. Ask the user to approve the change request (impact, slices, risks).
6. **Development:** for each new slice, follow `bottega:build`. The tester includes **regression** tests for the affected existing features.
7. **Release:** before releasing, run a security audit at least on the changed scope, then `/bottega:release`.
