# Project Evergreen - Synthetic Tax Client Data Set (v2, Tax Year 2025)

> **What's new in v2.** v2 is 25 clients: the 21 v1 clients plus four new high-complexity clients (EVG1022-EVG1025).
> Every client also has a **software-exception layer** showing where **CCH Axcess** (per the firm's *1040 Exception
> Remediation Workbook*) and **Intuit ProConnect Tax** need a manual calculation, an override, a special entry or a
> different filing path to get the return right. Each client's folder now includes:
> * `<ID>_2025_Software_Exception_Workbook.xlsx` - the firm's workbook (corrected copy), filled in for that client: the
>   Diagnostics Log, every relevant calculation tab, and an added **ProConnect Exceptions** tab
> * `<ID>_2025_Software_Exceptions.md` - for each exception: what each package does by default, why that is wrong here,
>   the fix and where it is entered, the amount, and the e-file impact
> * a `software_exceptions` rubric inside `<ID>_2025_Answer_Key.json`
>
> **v2 at a glance:** 25 clients - 208 tax gotchas - 126 software exceptions (117 of them *silent*: no software diagnostic fires,
> the wrong answer just calculates) - every Axcess workbook calculation tab (3-24) exercised by at least one client - 16
> ProConnect items backed by an Intuit help article or community answer (all other ProConnect screen paths are marked "verify").
>
> See [`SOFTWARE_EXCEPTION_MATRIX.md`](SOFTWARE_EXCEPTION_MATRIX.md) for the client x workbook-tab coverage, and
> [`reference/WORKBOOK_REVIEW.md`](reference/WORKBOOK_REVIEW.md) for **formula errors found in the workbook itself** (several
> tabs always return the wrong answer; a corrected copy is included). v1 is unchanged in `../evergreen-training-data/`.


Twenty-four synthetic individual-tax households (plus one separate child return) that look like the clients a small CPA
firm prepares for, built for the **Project Evergreen test environment and eval suite**. Each client has:

* **Inputs** - the documents the client sent (W-2s, 1099s, K-1s, brokerage statements, closing statements, spreadsheets,
  handwritten notes, emails) plus permanent-file items (profile, prior-year return summary, legal agreements).
* **Outputs** - the finished, signed-off 2025 return (form by form, line by line), plain-English preparer notes, the
  reviewer's review points, and a machine-readable answer key with a **gotcha rubric**.

The gotchas come straight from the manual exceptions in the *Project Evergreen Draft (Pre-AI)* procedure doc
(Scan, Workpapers, Return, Review, SALT and E-file sections), plus other traps AI preparers commonly fall into.
See [`DATASET_DESIGN.md`](DATASET_DESIGN.md) for the roster and gotcha map, and [`CLIENT_INDEX.md`](CLIENT_INDEX.md) for
key numbers and every rubric item.

> **Everything here is fictional.** Names, SSNs (shown truncated), EINs, addresses and accounts are made up, and every
> document is stamped "SYNTHETIC TRAINING DATA - NOT A REAL TAX DOCUMENT".

## Folder structure (follows the procedure doc's "Folder Structures" section)

```
evergreen-training-data/
  README.md                  <- this file
  DATASET_DESIGN.md          <- design spec: roster, 2025 law figures used, gotcha map
  CLIENT_INDEX.md            <- auto-generated roster, key numbers, all rubric items
  SOFTWARE_EXCEPTION_MATRIX.md  <- auto-generated client x Axcess-workbook-tab matrix + ProConnect references
  reference/                 <- firm's workbook (ORIGINAL + CORRECTED) and WORKBOOK_REVIEW.md
  answer_key/
    summary.csv              <- one row per client, key Form 1040 lines
    all_gotchas.jsonl        <- every rubric item (client_id, procedure_section, trap, correct_treatment, ...)
    all_software_exceptions.jsonl <- every software exception (workbook tab, Axcess default/fix, ProConnect default/fix, amount)
  clients/
    EVG1001_Bell/
      PERM/                  <- permanent info: Client_Profile.md, 2024 return summary, legal agreements
      2025/
        PBC/                 <- source documents exactly as received (INPUTS)
        Deliverables/        <- EVG1001_2025_Form_1040_Client_Copy.pdf (final return)
        EVG1001_2025_PBC_Receipt_Log.md   <- admin intake log (neutral - no hints)
        EVG1001_2025_Preparer_Notes.md    <- plain-English notes on the completed return
        EVG1001_2025_Review_Points.md     <- reviewer points on the first draft + resolutions
        EVG1001_2025_Answer_Key.json      <- expected return (all forms/lines) + gotcha rubric + software_exceptions
        EVG1001_2025_Software_Exception_Workbook.xlsx  <- firm's Axcess exception workbook, filled in (+ ProConnect tab)
        EVG1001_2025_Software_Exceptions.md            <- plain-English Axcess / ProConnect exception walkthrough
    ...
  generator/                 <- Python that builds all of the above deterministically
```

## Using it for evals

**Give the model under test only the inputs:** `clients/<ID>/PERM/` and `clients/<ID>/2025/PBC/` (and the receipt log if you
want to simulate the intake step). Hold back `Deliverables/`, `*_Preparer_Notes.md`, `*_Review_Points.md` and
`*_Answer_Key.json`.

Suggested scoring:
1. **Line accuracy** - compare the model's return to `form_1040_summary` and `federal_forms` in the answer key
   (exact match, or within $1 for rounding).
2. **Gotcha handling** - for each item in `gotchas`, did the model avoid the `trap` and apply the `correct_treatment`?
   `affected_lines` points to where the result shows up. `difficulty` is easy / medium / hard.
3. **Workflow behavior** - did it raise the right open items (missing recurring docs, late 83(b), IP PIN), flag duplicates,
   and route filings correctly (state/local returns, FBAR, Form 3520, paper-file triggers)?
4. **Software-exception mode (v2)** - give the model the inputs and say which package it is preparing in (Axcess or
   ProConnect). Score whether it identifies each item in `software_exceptions`, especially the **silent** ones
   (`axcess_diagnostic == "None - silent"`), gives the right override location and amount, and picks the right e-file or
   paper path. You can also hand it the blank workbook and score the filled tabs against `*_Software_Exception_Workbook.xlsx`.
5. **Reviewer mode** - give a model the inputs plus a flawed draft (build one from the "trap" column) and score whether its
   review points match `*_Review_Points.md`.

## Regenerating

```bash
pip install reportlab openpyxl python-docx pillow pycel
cd generator
python3 fix_workbook.py       # rebuild the corrected Axcess workbook from reference/..._ORIGINAL.xlsx
python3 build.py              # all clients + software-exception packs + index files
python3 build.py c01_bell     # one client
```

`tax2025.py` is the calculation engine (2025 brackets and tax table, capital-gain worksheet, SE tax, NIIT, Additional
Medicare, AMT, CTC/ACTC, EITC, education credits, Form 2441, OBBBA Schedule 1-A deductions, SALT phase-down, QBI).
Each `clients/cNN_*.py` script makes the preparer's judgment calls in commented code, then lets the engine do the math,
so notes and forms never disagree.

## Scope and caveats

* **Tax law:** TY2025 under Rev. Proc. 2024-40 as changed by the One Big Beautiful Bill Act (P.L. 119-21). Where a 2026
  change is a trap (gambling 90% limit, non-itemizer charitable deduction, $7,500 dependent-care FSA, state-declared
  disaster losses), the answer key applies 2025 law and says so.
* **Line numbers** follow the 2025 Form 1040 (1a-1z, 11, 12e, 13a, 13b, 15, ...). Schedules that were renumbered for
  2025 also carry a description; the description is what counts.
* **State and local returns** are shown at summary level (base, rate, exemptions/credits, withholding, result) for
  IL, MI (+ Detroit and Grand Rapids), PA, and NC. They're good enough to test filing-requirement and major-adjustment
  logic, but not a line-by-line state return.
* Where the procedure doc and the law disagree, the answer key follows the law and the preparer notes say why. See
  "Procedure doc items flagged" below.

## Procedure doc items flagged while building the data
These are places where following the draft procedure literally would produce a wrong return. Each one shows up in at
least one client's notes:

1. **Filing status after a spouse dies** - in the year of death the survivor files **MFJ**. Qualifying surviving spouse
   status applies only in the two *following* years, and only with a dependent child (EVG1009).
2. **Clothing donations at "3x cost basis"** - a deduction for used clothing is limited to fair market value (thrift
   value), which can't exceed cost basis. The 3x rule would overstate the deduction (EVG1007).
3. **Foreign tax credit de minimis ($300/$600)** - this only works if *all* foreign income is qualified passive income
   reported on a payee statement (1099/K-1). Foreign pensions and foreign bank interest don't qualify, so Form 1116 is
   needed even under $600 (EVG1004, EVG1015). Treaty-excess withholding (for example, Indian TDS above the 15% treaty
   rate) isn't creditable.
4. **"Roth IRAs require taxes to be withheld at the time of contribution"** - Roth contributions are simply made with
   after-tax dollars. Nothing is withheld. Qualified distributions are tax-free.
5. **Separated isn't divorced, but...** - a separated spouse can still file **HOH** under the "considered unmarried"
   rules (EVG1016). The procedure only mentions MFJ/MFS.
6. **Gambling "OBBBA rules in effect for 2026"** - correct for 2026, but 2025 returns still allow losses up to 100% of
   winnings (EVG1020).
7. **Kiddie tax** - Form 8814 is only available when the child's income is solely interest and dividends (including
   capital gain distributions). A child with gains from selling stock must file their own return with Form 8615
   (EVG1010/EVG1021).
