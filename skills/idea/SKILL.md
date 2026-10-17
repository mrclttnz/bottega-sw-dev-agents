---
name: idea
description: Interactive discovery of a product idea. Interviews the user about problem, users, value, alternatives, constraints and MVP scope, then has the product-analyst write the vision and the critic stress-test it. Use when you have an idea to clarify before defining requirements.
argument-hint: "[initial description of the idea]"
---

# P1 — From idea to vision

Goal: an approved `docs/01-vision.md` with a **small, clear MVP**. Rules: `${CLAUDE_PLUGIN_ROOT}/references/protocol.md`.

Initial idea: `$ARGUMENTS`

## 1. Interview (you run it, in the conversation)
Ask questions **in batches of 2-4**. Use AskUserQuestion when the answers lend themselves to options, and open questions when you need descriptions. Adapt the questions to what the user has already said, and don't ask what you already know.

**Batch A: problem and users**
- What problem does it solve? Who has it today, and how do they deal with it?
- Who are the users (different roles?), and how many will there be at launch and after a year?
- What happens if the app doesn't exist? How much does the problem hurt?

**Batch B: value and scope**
- What is the one thing the app must do extremely well?
- What makes this solution better than the alternatives (including spreadsheets, email, paper)?
- How will we know it works? (1-3 success metrics)

**Batch C: constraints**
- Platforms: web, mobile, desktop, API?
- Timeline, hosting budget, and who will maintain it?
- Data processed: personal? sensitive (health, finance, minors)? payments?
- Regulations or company constraints (GDPR, regulated industry, mandated cloud, corporate single sign-on)?
- Integrations with existing systems?

**Batch D: MVP**
Propose an MVP scope yourself, based on the answers, in the form "In / Out / Later", and ask for confirmation. Push toward the minimum that proves the value.

Every 2 batches, give a short recap ("Here's what I understood… is that right?") to avoid misunderstandings.

## 2. Drafting
Delegate to the `bottega:product-analyst` agent with the full interview notes (report them faithfully, including the user's own words on key points), and ask it to produce `docs/01-vision.md`.

## 3. Critique
Delegate to `bottega:critic` the review of `docs/01-vision.md`. Bring to the user only the BLOCKER and IMPORTANT objections, as questions with options. Have the product-analyst update the vision with the answers.

## 4. Gate G1
Present the vision in summary (problem, users, value, MVP, metrics, constraints) and ask for approval. Update `docs/STATUS.md` (gate G1, current phase `P2 Requirements`). Next step: `/bottega:requirements`.
