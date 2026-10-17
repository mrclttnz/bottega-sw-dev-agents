---
name: requirements
description: Interactive requirements elicitation and definition. Explores features, roles and permissions, flows, data, error cases and non-functional requirements with the user, then has the product-analyst produce FR, NFR, SR and user stories with acceptance criteria, the critic challenge them and the security-engineer complete them. Use after the vision, or to revise the requirements.
argument-hint: "[area or feature to focus on]"
---

# P2 — Requirements

Goal: a complete, testable, traceable and approved `docs/02-requirements.md`. Rules: `${CLAUDE_PLUGIN_ROOT}/references/protocol.md`.

Prerequisite: an approved `docs/01-vision.md` (G1). If it's missing, suggest `/bottega:idea`.

Requested focus: `$ARGUMENTS` (if empty, the whole MVP).

## 1. Exploration (you run it)
Start from the MVP in the vision. Work **feature by feature**: for each one, ask a few focused questions, using AskUserQuestion where there are clear options.

For each feature, clarify:
1. **Who** uses it (role) and **what** they get.
2. **Main flow**, step by step (ask for a concrete example with realistic data).
3. **Data** involved: what gets entered, what gets shown, and who else can see it.
4. **Business rules:** constraints, calculations, states, deadlines.
5. **Error cases and limits:** what happens if the data is wrong, missing or duplicated, if two people edit it at once, or if something linked to it is deleted.
6. **Permissions:** who can create, view, edit and delete? Who must **not** be able to see it?

Then cover the cross-cutting topics users often overlook. Propose sensible defaults yourself and ask for confirmation, instead of asking open questions:
- **Accounts:** open sign-up or invite-only? Email and password, Google or Microsoft login, corporate SSO? MFA?
- **Administration:** who manages users and configuration?
- **Notifications:** email, in-app, none?
- **Performance and volume:** how many concurrent users, how much data, what response times are acceptable?
- **Availability:** what happens if the app is down for an hour? Does it need to work offline?
- **Languages, accessibility, devices.**
- **Personal data:** which data, how long it is kept, export and deletion on request.
- **Audit:** do we need to know who did what?
- **Import and export** of existing data.

Recap at regular intervals. Don't aim for perfection in a single pass: open questions become `Q` items and get closed later.

## 2. Drafting
Delegate to `bottega:product-analyst` with all the notes, and ask it to produce or update `docs/02-requirements.md`.

## 3. Security and critique, in parallel
Launch together:
- `bottega:security-engineer`: "Review the requirements and propose the missing SRs (authentication, authorization, privacy, audit, retention, abuse). No threat model yet."
- `bottega:critic` on `docs/02-requirements.md`.

## 4. Closing the questions
Gather the product-analyst's Qs, the critic's objections and the proposed SRs. Bring them to the user in batches of at most 4 questions, each with a recommendation. Send the answers back to the product-analyst to update the document. Repeat at most 2 rounds. Whatever is still open and non-blocking gets marked as a non-blocking Q.

## 5. Gate G2
Check yourself:
- [ ] every Must user story in the MVP has ACs in Given/When/Then form, including negative cases
- [ ] every NFR has a measure
- [ ] the roles × actions matrix is complete
- [ ] there are SRs for authentication, authorization, personal data, logging and audit
- [ ] no Q is marked blocking

Present the summary (number of FRs, NFRs, SRs and user stories, scope, remaining Qs) and ask for approval. Update `docs/STATUS.md`. Next step: `/bottega:design`.
