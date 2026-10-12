---
name: evergreen-pipeline
description: Runs the full Evergreen Tax individual-return process end to end for one client - intake, preparation, independent review, filing package - by invoking the evergreen-intake, evergreen-prepare, evergreen-review and evergreen-file skills in order with stage gates and a run summary. Use this whenever someone asks to "do the whole return", "run the pipeline", "take client X from intake to filing", process a client folder end to end, or batch-process several clients.
---

# Evergreen Pipeline (intake -> prepare -> review -> file)

One client = one run folder `<run>/` containing `input/` (PERM + PBC). Stages write to `01_intake/`, `02_prepare/`,
`03_review/`, `final/`, `04_file/`. Each stage reads only what the previous stages wrote plus the source documents.

## Steps
1. **Intake** - follow the `evergreen-intake` skill. Gate: `01_intake/intake.json` exists, every PBC file appears in
   `documents`, open items listed.
2. **Prepare** - follow `evergreen-prepare`. Gate: `02_prepare/return.json` has no unresolved E-FILE DISQUALIFYING
   diagnostics; `prep_notes.md` written.
3. **Review** - follow `evergreen-review`. Do this with **fresh eyes**: if you can, hand it to a separate agent/subagent that
   has not seen the preparation reasoning (give it only the run folder and the review skill). If the same agent must do it,
   re-read the source documents before opening `prep_notes.md`. Gate: `final/return.json` written; decision recorded.
4. **File** - follow `evergreen-file`. Gate: `04_file/filing_package.json` written.
5. Write `<run>/run_summary.md`: key numbers (AGI, taxable income, total tax, refund/due, states), review decision and
   number of review points by severity, open items, filings and methods, and anything a human must decide.

Stop and report (don't guess) if a stage gate fails in a way that would make later stages meaningless.
