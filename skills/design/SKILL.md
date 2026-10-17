---
name: design
description: Design phase. Coordinates ux-designer, architect, data-architect and security-engineer to produce UX, architecture with ADRs, data model and threat model, bringing the key decisions to the user. Use after the requirements are approved.
argument-hint: "[ux | architecture | data | threat-model] (empty = all)"
---

# P3 — Design

Rules: `${CLAUDE_PLUGIN_ROOT}/references/protocol.md`. Prerequisite: G2 passed (requirements approved). Scope: `$ARGUMENTS` (empty = the whole phase).

## Sequence

**1. High-level architecture.** Delegate to `bottega:architect`: "Produce `docs/04-architecture.md` and the ADRs, with status PROPOSED, for the key decisions. Take into account the user profile in `docs/STATUS.md`."
Bring the **Decisions needed** to the user: usually architectural style, language and framework, database, authentication. For each, present the options and the recommendation. For the heaviest decisions, use the `bottega:decide` process. Have the ADRs updated to `ACCEPTED` with the user's choices.

**2. In parallel**, once the stack is decided:
- `bottega:ux-designer` → `docs/03-ux.md` (skip it if there is no user interface, after confirming with the user)
- `bottega:data-architect` → `docs/05-data.md`

Questions that come up (e.g. "how long is data kept?" or "can a user belong to several organizations?") go to the user, and the answers go back to the agents.

**3. Threat model.** Delegate to `bottega:security-engineer` in mode A: "Produce `docs/06-threat-model.md` from the updated architecture and data model." Any new SRs it proposes go to the product-analyst to be added to the requirements, after the user confirms them if they change the scope. Mitigations that affect the architecture go back to the architect.

**4. Critique.** Delegate to `bottega:critic` a joint review of architecture, data and threat model, looking for consistency between documents, over-engineering and gaps. Resolve the BLOCKER objections with the user and with the agent that owns the document.

## Gate G3
Check:
- [ ] key ADRs ACCEPTED (stack, database, authentication, architectural style)
- [ ] every NFR and SR has an architectural choice that satisfies it (map in `04-architecture.md`)
- [ ] every high- or critical-risk THR has an assigned mitigation
- [ ] every piece of personal data is classified, with retention defined
- [ ] diagrams match the text
- [ ] no open BLOCKER objections from the critic

Present a summary pitched at the user's profile: a C4 context diagram, the chosen stack, the top 3 risks and how they are mitigated. Ask for approval and update `docs/STATUS.md`. Next step: `/bottega:plan`.
