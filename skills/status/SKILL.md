---
name: status
description: Shows the status of the Bottega project (phase, gates passed, slices, open findings, technical debt, pending decisions) and suggests the next step. Use to resume work in a new session or to take stock.
---

# Project status

1. Read `docs/STATUS.md`. If it doesn't exist, suggest `/bottega:setup`.
2. Check that it matches reality:
   - do the slices marked `DONE` have reports in `docs/reviews/`?
   - are there `OPEN` findings in the reports?
   - are there ADRs in `PROPOSED` status waiting for a decision?
   - are there open blocking Qs in `docs/02-requirements.md`?
   - if using git, are there uncommitted changes?
3. Present a compact dashboard:
   ```
   Project: <name> · Phase: P5 Build · Last update: <date>
   Gates:   G1 ✔  G2 ✔  G3 ✔  G4 ✔  G5 3/8  G6 –  G7 –
   Slices:  SL-00 ✔ SL-01 ✔ SL-02 ✔ SL-03 ▶ SL-04 · SL-05 · …
   Open:    2 BLOCKER findings (SEC-SL03-001, CR-SL03-004) · 1 proposed ADR · 0 blocking Qs
   Debt:    4 items
   Next:    fix the SL-03 findings → /bottega:build SL-03
   ```
4. Point out any inconsistencies you found and propose how to fix them.
