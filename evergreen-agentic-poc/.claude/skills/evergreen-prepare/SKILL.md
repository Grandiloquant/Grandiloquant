---
name: evergreen-prepare
description: Prepares an individual 2025 federal Form 1040 (plus summary-level state/local returns) for an Evergreen Tax client from the intake package - works every judgment area in the firm SOP (filing status, Schedules A/B/C/D/E, K-1 basis/at-risk/passive, installment sales, NIIT, foreign, kiddie tax, OBBBA Schedule 1-A), builds off-system workpapers, writes facts.json, runs the calculation engine, and documents everything in plain-English workpaper notes plus a CCH Axcess / ProConnect software-exception log. Use this whenever someone asks to prepare, draft, compute, rework or fix a client's individual tax return, respond to review points as the preparer, or "run the numbers" for a 1040 - after intake has been done.
---

# Evergreen Prepare (SOP: Prep, Workpapers, Return)

You are the preparer. The engine does arithmetic; **you** decide what the numbers are. A return that calculates cleanly but
treats one item wrongly is still a wrong return, and the dangerous mistakes are the silent ones: a duplicate form loaded
twice, a K-1 footnote ignored, a basis the broker didn't know, a deduction the software can't limit. Work like a careful
senior: trace every number to a source document, write down why each judgment was made, and leave the reviewer a clean
trail.

Read `CLAUDE.md` first. Keep `docs/tax_year_2025_reference.md` open; the SOP text is in `docs/Project_Evergreen_SOP_v2.txt`.

## Inputs and outputs
* Input: `<run>/01_intake/intake.json` (+ `intake_memo.md`) and the source documents in `<run>/input/` and
  `<run>/01_intake/extracted/`. Intake can be wrong - when an amount matters, check it against the document.
* Output folder `<run>/02_prepare/`:
  * `facts.json` - engine input (schema: `references/facts_schema.md`)
  * `return.json`, `return.md`, `diagnostics.json` - produced by `python3 tools/compute_return.py <run>/02_prepare/facts.json <run>/02_prepare`
  * `workpapers.md` - off-system computations (basis, at-risk, passive, 2210, home office, depreciation, 8606, 6252,
    mortgage limit, vacation home, FTC, NIIT, state) with inputs, formula and source for each
  * `state_returns.json` - each state/local return: type, base, rate, exemptions, credits, withholding, refund/due (or
    "not required" with the reason)
  * `software_exceptions.md` - where CCH Axcess / ProConnect would get this return wrong and the override you'd enter
    (`references/software_exceptions.md`)
  * `prep_notes.md` - plain-English notes in the firm format (template below)

## Workflow
1. **Plan.** Read the intake package. List the areas this return touches and open `references/prep_checklist.md` for each -
   it is the SOP's watch-list turned into questions. Skipping an area because "the scanner handled it" is how silent errors
   get in.
2. **Decide filing status and dependents first** - they drive everything else (status reminders in the 2025 reference).
3. **Work each area** and make the judgment calls, writing a workpaper for anything that isn't a straight copy from a form.
   Explain the *why* in a sentence or two; cite the source file (and IRC/regulation/IRS instruction when it's a rule).
4. **Write `facts.json`** (only the keys in the schema; amounts as decided, not as reported when they differ).
5. **Run the engine** and read `diagnostics.json`. Every WARNING/E-FILE DISQUALIFYING item must be fixed or explained
   (SOP: E-file Diagnostics). Then **sanity-check the output** like a reviewer would: does AGI tie to your workpapers? Is the
   deduction choice sensible? Did the credits land? Does withholding tie to the W-2s/1099s? Compare to prior year and
   explain big swings.
6. **States and locals.** For each required return, compute at summary level using the state quick facts; record when a
   return is NOT required and why (reciprocity, de minimis day rules, only losses apportioned).
7. **Software exceptions.** For every place the real package would need a manual calc, override or special input, log it
   (silent ones first).
8. **Write `prep_notes.md`**, then stop. Unresolved open items go in the notes as assumptions; don't block on them unless the
   return would be meaningless without the answer.

When responding to review points, work in the same folder: change `facts.json`/workpapers, rerun the engine, and answer each
point (done / question) in `review_responses.md` - the SOP's red-pen response.

## prep_notes.md template
```
# <Client ID> - <Name> - 2025 Form 1040 - Preparer Notes
## Return summary   (status, AGI, deduction, taxable income, total tax, payments, refund/due; state results)
## What I did and why   (numbered, one paragraph per judgment area; source doc + rule for each)
## Items excluded or treated differently from the documents   (duplicates, superseded, informational, overrides)
## Assumptions and open items
## Carryforwards to 2026
## Filing notes for the signer   (returns required, e-file/paper, separate filings, due dates, advice to client)
```

## Principles worth internalising
* **Documents beat the organizer; the latest/corrected/final document beats the earlier one; detail beats summary.**
* **Not every document is income.** IRA statements, 5498s, drafts, duplicates, other people's forms are evidence, not entries.
* **Reported ≠ taxable.** A 1099 amount often needs adjusting: basis on equity comp, accrued interest, wash sales across
  accounts, QCDs, rollovers, NUA, nondividend distributions, 1099-K vs 1099-NEC overlap, allocated vs actual tips.
* **Limits stack in order** - basis -> at-risk -> passive (-> excess business loss); S-corp distributions test STOCK basis only;
  partnership distributions above outside basis are gain; suspended amounts carry forward by character (regular AND AMT).
* **Check the year.** 2025 law (OBBBA), not 2026. Payments must be paid in (or credited to) 2025; deductions follow the cash
  year (a 01/15/2026 state estimate is a 2026 deduction; a January 2026 installment payment is 2026 income).
* **When the law and the SOP disagree, follow the law and say so** (examples in CLAUDE.md).
