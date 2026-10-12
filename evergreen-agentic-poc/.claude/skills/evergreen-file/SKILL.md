---
name: evergreen-file
description: Final stage of an Evergreen Tax individual engagement - turns a reviewed 2025 return into a filing package - signer hand-off checklist, every federal/state/local/separate filing with method (e-file vs paper and why), due dates, e-file blocker checks (IP PIN, name control, unsupported forms, 1042-S), Form 8879/payment/estimated-tax instructions, the client delivery letter and the invoice summary. Use this whenever a return is ready to go out: "file it", "get this ready for e-file", "prepare the client package", "what do we need to file for X", "hand off to the signer", or as step 4 of the Evergreen pipeline.
---

# Evergreen File (SOP: Hand-Off to Signer, Sign-Off, Billing, Send to Client, E-Filing, Post-Submission Exceptions)

You are the final gate before anything leaves the firm. In this proof of concept nothing is actually transmitted - you
produce the package a human signer would approve and the exact instructions admin would follow. Your job is to make sure
**every required filing is on the list, each goes by the right method, and nothing will reject.**

Read `CLAUDE.md` and `references/filing_rules.md`.

## Inputs and outputs
* Inputs: `<run>/final/return.json` (+ `final/state_returns.json`), `<run>/03_review/review.json` and review points,
  `<run>/02_prepare/prep_notes.md`, `<run>/01_intake/intake.json`.
* Outputs in `<run>/04_file/`:
  * `filing_package.json` (schema below)
  * `signer_handoff.md` - the SOP hand-off checklist, filled in
  * `client_letter.md` - plain-English cover letter: results, what to sign, payments and due dates, 2026 estimates, documents
    the client should keep, separate filings they must sign/mail, advice raised during prep/review
  * `invoice.md` - two columns (Description, $ Amount), forms prepared, keep it simple (SOP: Billing); flag write-offs vs
    client-chargeable items and the 15% expedite fee if documents arrived within 15 days of the deadline

## Workflow
1. Confirm review status. If review was "returned" with open errors, stop and say so - don't package a return with known errors.
2. Build the filing list: federal 1040 (+ forms/attachments), each state/local return, separate filings (FBAR - FinCEN 114,
   Form 3520, late 1099-NEC/W-2 for household employees, 8865 if unsupported by software, child's own return), and any
   amended prior-year returns or projects recommended.
3. Work as of the engagement date in `intake.json` (see CLAUDE.md). If the receipt log/documents don't show an extension and
   that date is after 04/15/2026, list "confirm extension status" as an open item - don't assume either way.
4. For each filing decide **method** and **due date** with the reason (rules in `references/filing_rules.md`): e-file unless
   a paper trigger exists. Note extensions on file.
5. Run the **e-file blocker check**: IP PIN currency (they change every year), name control vs SSA record (recent name
   change), dependent claimed elsewhere, 1042-S withholding, unsupported/separately-filed forms, required PDF attachments
   (8949 statements, 7203, elections), self-select PIN/8879, driver's license data.
6. Payments: balance due (how/when; interest after 4/15 on extensions), refund (direct deposit), 2026 estimates (amounts,
   dates, safe-harbor rule used).
7. Write the four outputs. `final/return.md` comes from the engine run that produced `final/return.json`.

## filing_package.json
```json
{"client_id": "", "review_decision": "", "federal": {"form": "1040", "method": "e-file|paper", "reason": "", "due": "2026-10-15",
  "attachments": ["Form 8949 statement (PDF)", "Form 7203", "§1033 election statement"], "refund": 0, "balance_due": 0},
 "states": [{"return": "IL-1040", "type": "resident|part-year|nonresident", "method": "", "due": "", "refund": 0, "balance_due": 0}],
 "locals": [{"return": "Detroit part-year", "method": "", "due": ""}],
 "not_required": [{"return": "NJ-1040NR", "reason": "PA-NJ reciprocity"}],
 "separate_filings": [{"filing": "FinCEN 114 (FBAR)", "method": "BSA e-file", "due": "2026-04-15 (auto-ext 10/15)", "who": "Linda"}],
 "efile_blockers": [{"issue": "", "resolution": ""}],
 "signatures": ["Form 8879", "IL-8453"], "payments": [], "estimates_2026": [], "carryforwards_to_2026": [],
 "open_items_at_filing": [], "as_of_date": ""}
```
