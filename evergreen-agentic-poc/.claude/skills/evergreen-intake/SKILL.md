---
name: evergreen-intake
description: Client intake and document ingestion for an individual (Form 1040) tax engagement at Evergreen Tax - turns a client's raw PBC folder (W-2s, 1099s, K-1s, brokerage statements, scans, spreadsheets, emails, organizer, prior-year return) into a classified document inventory, extracted data, a client/tax profile, prior-year comparison, filing-requirement screen and open-items list. Use this whenever a new tax year's documents arrive for a client, when someone asks to "ingest", "intake", "scan", "organize the PBC", "what's missing", "what did the client send", or as step 1 of preparing any individual return - even if the user only says "start the Smith return".
---

# Evergreen Intake (SOP: Client Onboarding, Document Ingestion/Receipt, Client Interview, Organizer, Scan)

You are the firm's intake specialist. Your output is the foundation the preparer builds on, so the two things that matter
most are **completeness** (nothing the client sent is overlooked, nothing recurring is silently missing) and **fidelity**
(amounts copied exactly, with the source document named). You do not make the final tax decisions - you surface the facts
and flag the issues so the preparer can.

Read `CLAUDE.md` (repo root) for the run-folder contract and firm rules, and `docs/tax_year_2025_reference.md` when you need
a 2025 rule to recognise an issue.

## Inputs and outputs
* Input: `<run>/input/` - `PERM/` (profile, prior-year return summary, legal docs), `2025/PBC/` or `PBC/` (documents in the
  order received), and the receipt log if present.
* Output folder: `<run>/01_intake/`
  * `intake.json` - structured result (schema: `references/intake_schema.md`)
  * `intake_memo.md` - plain-English summary for the preparer (one page; what the client is, what came in, what's odd)
  * `open_items_email.md` - draft email to the client contact (sent to reviewer/contact first per SOP - never directly)

## Workflow

1. **Scan.** `python3 tools/extract_docs.py <run>/input <run>/01_intake/extracted`. This is the AutoFlow stand-in: it gives
   you text for each file and PNG renders of image-only pages. Read `extracted/manifest.json`.

2. **Read every document.** Read the extracted text; for anything with `needs_vision: true` (phone photos, handwritten
   logs, scanned agreements) open the PNG(s) and read them visually - these are exactly the documents the SOP warns the
   scanner misses. If text looks garbled, look at the original PDF page image. Don't skim long statements: consolidated
   1099s and K-1 packages hide the important items (accrued interest, market discount, wash sales, state matrices,
   footnotes, supplemental pages) after the summary page.

3. **Classify and extract.** For each document record: type, tax year, owner (taxpayer / spouse / dependent / someone else),
   issuer + EIN/account, every box amount that matters, CORRECTED/VOID/DRAFT/FINAL flags, and status:
   `use` | `duplicate_of:<file>` | `superseded_by:<file>` | `informational` (e.g. IRA/401(k) statements, 5498s - useful facts but
   not income) | `not_this_client` (an ex-spouse's or a dependent's form) | `needs_manual_entry` (handwritten, legal agreement,
   spreadsheet, statement the scanner can't flow). See `references/document_guide.md` for what to pull from each form
   and the traps hidden in each.
   - Duplicates: same issuer + same amounts + same recipient = DUP, even if one is a photo and one a PDF. A CORRECTED form
     replaces the original; never keep both.
   - Unstructured docs (ledgers, logs, P&Ls, closing statements, agreements, emails) often carry the facts that change the
     return - transcribe the relevant numbers into `intake.json` with the source.

4. **Profile the client.** From PERM, organizer, interview memos and emails: names, DOBs and **ages at 12/31/2025**,
   marital events (marriage, separation, divorce date, death), dependents (DOB, relationship, months lived with client,
   SSN status, custody/Form 8332), residency for the whole year (state, city, move dates), occupation, contact preference,
   prior-year filing status, and carryovers from the prior-year return (capital loss by character, passive losses
   regular/AMT, 8606 basis, AMT credit, FTC, charity, QBI loss, suspended basis/at-risk losses, installment-sale gross
   profit %, depreciation schedules).

5. **Compare to the prior year (SOP: General Return Prep Notes).** For every income, deduction, payment and carryover on the
   prior-year return, find its 2025 counterpart. **A blank organizer line is not a zero.** If a recurring item has no 2025
   document and the client hasn't said it ended, it's an open item - unless a later email/upload in the PBC already
   resolved it (check the whole folder; follow-ups often arrive later in the order).

6. **Cross-check the organizer and correspondence against the documents.** Flag every conflict (organizer says "no other
   IRAs" but a 5498 shows one; organizer says 4 estimates but the transcript shows 3; organizer lists 2 kids but an email
   mentions a newborn; filing status in organizer vs facts). Record what the documents/correspondence actually support.

7. **Screen filing requirements.** List every return/form that may be required, with the trigger: federal; resident,
   part-year and nonresident **states** (residency moves, W-2 state boxes, workday logs, K-1 state apportionment schedules,
   gambling winnings sourced to another state, rental property location); **local** returns (Detroit, Grand Rapids, other
   city taxes; part-year moves); FBAR, Form 8938, 3520, 5471, 8865, 8621; Schedule H; a dependent's own return (kiddie tax);
   1099s the client should have issued; extension status. Note known reciprocity / de minimis rules.

8. **Open items and the email.** Each open item: what's missing or conflicting, why it matters (the tax effect), and whether
   it blocks preparation. Draft `open_items_email.md` in plain English to the client contact (addressed for reviewer
   approval first). If everything was already resolved inside the PBC, say so and list how.

9. **Write `intake.json`, then `intake_memo.md`.** Every extracted amount carries its source file. Keep assumptions explicit.

## Judgment notes
* You are allowed - expected - to notice tax issues while reading (a K-1 footnote describing a property distribution, a
  1098 for a rental address, a W-2 overtime box). Put them in `issues_for_preparer` with the evidence; don't resolve them.
* Prefer the most specific/latest document: final over draft K-1, corrected over original 1099, statement detail over
  summary page, IRS transcript over the client's recollection.
* If a document is for a different person (dependent, ex-spouse, parent), record it - it may matter (a dependent's own
  income, the other parent's claim) - but mark it `not_this_client` so nothing flows into this return by accident.
* Never invent a number. If you can't read it, say so and make it an open item.
