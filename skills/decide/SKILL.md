---
name: decide
description: Helps the user make a technical or product decision in a structured way (options, weighted criteria, trade-offs, risks, recommendation) and records it as an ADR. Use for choices such as language, framework, database, authentication, hosting, build vs buy, or any significant fork in the road.
argument-hint: "<the decision to make>"
---

# Structured decision → ADR

Decision to make: `$ARGUMENTS`

Rules: `${CLAUDE_PLUGIN_ROOT}/references/protocol.md`. ADR template: `${CLAUDE_PLUGIN_ROOT}/templates/adr.md`.

## Process
1. **Frame the decision.** Read `docs/STATUS.md`, the requirements and the existing ADRs. Restate the decision in one sentence and check with the user that this is really it. Find out what makes it hard: what's at stake, what a wrong choice costs, how reversible it is.
2. **Criteria.** Propose 4-7 relevant criteria, drawn from the requirements (NFRs, SRs) and the constraints (skills, budget, timeline), each with a weight. Ask the user to confirm or correct them with AskUserQuestion. This is where the user expresses their priorities.
3. **Options.** Delegate the research to the best-suited agent: `bottega:architect` for architecture, stack and database; `bottega:devops` for hosting; `bottega:security-engineer` for authentication and cryptography; `bottega:product-analyst` for product decisions. Ask for 2-4 **real, current** options, checked on the web (versions, prices, maintenance status), scored against the criteria, with risks and consequences. Always include "the simplest possible" option.
4. **Stress-test it.** For decisions that are hard to reverse, ask `bottega:critic` to challenge the recommendation.
5. **Present** to the user a compact options × criteria table, the main trade-offs in plain words, and the reasoned recommendation. Ask for their choice with AskUserQuestion, with the recommendation as the first option.
6. **Record it.** The ADR goes in `docs/adr/ADR-NNNN-<title>.md` (the number after the last existing one), with status `ACCEPTED`, the date, the rejected options and why, positive and negative consequences, and when to revisit it. If the decision replaces an earlier one, mark the old ADR as `SUPERSEDED BY ADR-NNNN`.
7. Update the Log in `docs/STATUS.md`.

## Principles
- **Reversible or not?** Easily reversible decisions are made quickly. Irreversible ones (database, provider, data model) deserve more analysis.
- **Make the cost of not knowing explicit:** if a decisive piece of information is missing, propose a small experiment (spike) before deciding.
- A choice that weakens security below the standard is not a presentable option.
