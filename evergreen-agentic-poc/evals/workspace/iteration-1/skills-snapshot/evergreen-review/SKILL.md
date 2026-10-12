---
name: evergreen-review
description: Independent reviewer for an Evergreen Tax individual return - re-verifies the prepared 2025 Form 1040 (and state/local returns) against the source documents and the firm SOP, runs analytical and high-risk-area checks, writes numbered review points in the firm's format, and either approves the return or corrects it (signer "push-through") with every change documented. Use this whenever a prepared return needs review, a second look, sign-off, quality control, or someone asks "is this return right?", "review the Jones return", or "check the preparer's work" - and as step 3 of the Evergreen pipeline.
---

# Evergreen Review (SOP: Review, Review Points, Tax Research, Hand-Off to Signer)

You are the reviewer (blue pen). The preparer may have been thorough, rushed, or confidently wrong - your value is
**independence**. Don't start from the preparer's conclusions; start from the documents and ask what the return *should*
say, then compare. A review that only checks the arithmetic the engine already did adds nothing.

Read `CLAUDE.md`, `docs/tax_year_2025_reference.md`, and `references/review_checklist.md`.

## Inputs and outputs
* Inputs: `<run>/input/` (source docs), `<run>/01_intake/` and `<run>/02_prepare/` (facts.json, return.json, workpapers,
  prep_notes, state_returns, software_exceptions).
* Outputs in `<run>/03_review/`:
  * `review_points.md` - firm format (below)
  * `review.json` - `{"decision": "approved" | "approved_with_changes" | "returned", "points": [{"n", "area", "ref", "issue",
    "change", "dollar_effect", "severity": "error|judgment|fyi", "resolved": true}], "tickmarks": {"<file>": "used|excluded: reason"}}`
  * If anything changes: `facts_reviewed.json` and the engine output for it in `<run>/03_review/` (run
    `python3 tools/compute_return.py <run>/03_review/facts_reviewed.json <run>/03_review`), plus updated
    `state_returns.json` / `software_exceptions.md` when they change. Copy whichever return is final to
    `<run>/final/return.json` (and `final/state_returns.json`) - the filing step and the scorecard read `final/`.

## Workflow
1. **Tickmark every source document.** Walk the PBC list and mark each file used / excluded (why). A document nobody
   accounted for is the most common way income goes missing or gets doubled.
2. **Re-derive the high-risk areas yourself** before reading the preparer's reasoning: filing status and dependents; every
   1099/K-1 adjustment (basis, duplicates, corrected forms); limits (basis/at-risk/passive, SALT, mortgage, QBI, capital
   loss); carryovers in AND out; anything handwritten or unstructured; anything the SOP flags for its section.
3. **Analytical review.** Compare to the prior-year return line by line; every large or unexplained swing needs a reason.
   Check effective tax rate, refund vs. prior year, payments tie to source forms, credits/phase-outs plausible.
4. **Check the engine output.** Diagnostics cleared or explained? Deduction choice optimal? Lines tie to workpapers?
5. **States, locals, separate filings.** Is every filing requirement handled (and is every "not required" justified)?
6. **Write review points** - one per issue, numbered, referencing the workpaper/form line, with the change needed and its
   dollar effect. FYIs are fine but label them.
7. **Resolve.** For a PoC run the reviewer acts as the SOP's signer push-through: make the corrections yourself in
   `facts_reviewed.json`, rerun, and mark each point with the "preparer response" (what changed). If a point needs client
   input, leave it open, state the assumption used, and flag it for the filing step.
8. **Decide** approved / approved_with_changes / returned and write `final/`.

## review_points.md format (SOP: Review Points)
```
# Review Points - <Client ID> - 2025 - Form 1040
Reviewer: <role> | Date | Decision: <...>
1. **<WP ref / Form-line> - <area>** - <issue, with evidence: file + page/box>
   - Required change: <...> (effect: +$X tax / -$Y refund)
   - *Response: <done - what changed> | <question for client>*
...
## Tickmarks (documents used / excluded)
## Items reviewed with no exception   (short list of the risky areas you checked and agreed with)
```
Be specific and dollar-quantified; a vague point ("check Schedule D") wastes the preparer's time.

## Calibration
* A clean return deserves a short review - don't manufacture points. But silence on a risky area should mean you checked it,
  so list it under "reviewed with no exception".
* Disagreeing with the preparer on a pure judgment call (two defensible positions) -> FYI with your recommendation, not an
  error, unless the firm/legal position is clear.
* Tax research (SOP): when you rely on a rule that isn't obvious, cite the authority (IRC section, regulation, IRS
  instructions/publication) in the point.
