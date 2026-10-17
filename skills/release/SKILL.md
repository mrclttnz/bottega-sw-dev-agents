---
name: release
description: Release phase. Helps choose the deployment environment, has devops prepare containers, infrastructure, the CD pipeline, observability, backups and runbook, and guides the deploy to staging and then production with explicit user approvals. Use once the application has passed verification and the security audit.
argument-hint: "[choose-environment | prepare | staging | production]"
disable-model-invocation: true
---

# P7 — Release

Rules: `${CLAUDE_PLUGIN_ROOT}/references/protocol.md`. Requested step: `$ARGUMENTS` (empty = resume where things left off, according to `docs/STATUS.md`).

**Prerequisite for any deploy:** G6 passed, i.e. a green suite and a security audit that is **FIT FOR RELEASE** and no older than the latest code change. If not, stop and suggest `/bottega:security-audit`. You may choose the environment and prepare the infrastructure before G6.

## 1. Choosing the environment
If there is no hosting ADR yet:
1. Ask the user about the preferences that matter: monthly budget, providers already in use, EU data residency, and how much operations work they want to take on.
2. Delegate to `bottega:devops` in mode B for the options.
3. Present the comparison and the recommendation, let the user choose, and record the ADR as ACCEPTED (the `bottega:decide` process).

## 2. Preparation
Delegate to `bottega:devops` in mode C. When it's done, have `bottega:security-engineer` (mode B) review the Dockerfile, IaC, pipeline and production configuration. BLOCKERs get fixed before going further.

Tell the user which secrets and variables they must set themselves in the secret manager or platform, by name only, with instructions. **Never ask the user to paste secret values into the chat.**

## 3. Staging
Ask for confirmation with AskUserQuestion: "Deploy to staging?". Only on a yes, delegate to `bottega:devops` in mode D with `AUTHORIZED: deploy to staging`. Then have `bottega:tester` (mode D) run the smoke tests and, if planned, `bottega:security-engineer` run the DAST baseline against staging.

## 4. Production
Present a summary: version or commit, test results, audit, staging smoke tests, planned migrations, pre-release backup, rollback plan. Ask for a **separate, explicit approval** for production. Only then delegate to `bottega:devops` in mode D with `AUTHORIZED: deploy to production`. Check the result of the production smoke tests.

## 5. Wrap-up (gate G7)
- [ ] `docs/09-release.md` complete: environments, variables, procedure, rollback, runbook, backups, costs
- [ ] production smoke tests green
- [ ] monitoring and alerts active
- [ ] backup restore test documented

Update `docs/STATUS.md` (release, version, date). Suggest next steps: collecting feedback, the backlog, new features with `/bottega:evolve`.
