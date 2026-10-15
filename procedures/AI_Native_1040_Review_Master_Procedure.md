# Project Evergreen - AI-Native Form 1040 Review: Master Procedure (MOCK-UP)

> **Status:** Draft mock-up v0.1 for discussion. Not yet adopted.
> **Replaces:** the *Prep, Review and Sign Process* sections of the *Project Evergreen Draft (Pre-AI)* procedure doc. The
> pre-AI doc's Prospecting, Quoting, Onboarding, Tax Research hierarchy, Glossary and IRC overview still apply unless
> this document says otherwise.
> **Scope:** Individual returns only (1040 / 1040-SR / 1040-X and their state/local returns, extensions, FBAR and
> stand-alone information returns that ride with the 1040). No business returns, no financial-statement work.

---

## 0. How to read this document

In the pre-AI firm, a human preparer built the return and a human reviewer checked it. In this model **an AI preparer
builds almost the entire return**, and the **reviewer (a CPA)** does two jobs:

1. **Reviews** the AI's work - completeness, accuracy, judgment, and compliance.
2. **Performs every manual workaround** - anything the AI could not or should not do (unstructured documents, software
   limitations, overrides, elections, judgment calls, client follow-up drafts).

There is no human preparer layer. That puts more weight on the reviewer, so this procedure is built around three
ideas:

* **Gates, not page-turning.** The reviewer does not re-key or re-read every page. Work moves through fixed gates
  (R0-R9), and each gate has entry criteria the AI package must meet before the reviewer spends time on it.
* **Risk-based depth.** Every return gets a risk tier (Section 4). The tier sets how much of the AI's data entry the
  reviewer traces back to source and which checklists are mandatory.
* **Every manual touch is logged.** Overrides, manual calculations and workarounds go in one exception log with a
  workpaper reference (Section 9). The log feeds the signer's review, next year's rollover, and the AI feedback loop.

**Software paths.** Screen and field names for StanfordTax, Filed and ProConnect change between releases. Paths in this
document are written as `Tool > Area > Screen` and marked **(verify)** where the exact label must be confirmed in the
firm's current release. The same convention is used in the Project Evergreen v2 dataset.

---

## 1. Tech stack and system of record

| Function | Pre-AI tool | AI-native tool | System of record for... |
|---|---|---|---|
| Practice management, workflow, status, due dates, time, billing | CCH Workstream | **Karbon** | Work items, assignees, stage status, review sign-off checklist, time entries, WIP and invoices, client contact preferences, internal notes |
| Client portal, organizer/questionnaire, document requests, engagement letter, e-signature, workpaper binder | CCH Organizer + Sharefile + PDFlyer | **StanfordTax** | Questionnaire answers, PBC document set, open client requests, signed engagement letter, signed Form 8879 / state equivalents, the compiled PDF workpaper binder |
| Document ingestion, data extraction, review interface | ProSystem fx Scan / AutoFlow | **Filed** | Document classification, extracted field values, source-to-field links, confidence flags, AI prep output, extraction corrections |
| Tax engine, diagnostics, e-file | CCH Axcess Tax | **Intuit ProConnect Tax** | The return itself, overrides, diagnostics, extensions, e-file transmissions and acknowledgements |
| Projections / scenario modeling | CFS Tax Tools | ProConnect what-if / scenario tools, or a separate projection tool (firm decision - open item) | Projection workpapers |
| File storage | Shared drive | StanfordTax (client docs, workpapers) + Karbon (internal docs) - firm to decide the final split (open item) | See Appendix F |

**Rule:** if two systems disagree, the system of record in the table above wins, and the disagreement is a review
point.

---

## 2. Roles

| Role | Who | Responsibilities in this procedure |
|---|---|---|
| **AI Preparer** | AI agent(s) operating in Filed (and any firm-built agent that writes to ProConnect / Karbon) | Classify and extract documents; build the return; produce the AI Prep Package (Section 5); draft open-item requests; clear what it can of the diagnostics. **May not:** make reserved decisions (Section 5.3), send anything to a client, approve diagnostics, sign off any gate, or e-file. |
| **Reviewer** | CPA | Owns gates R0-R8. Traces and verifies the AI's work, performs all manual workarounds, writes review points, approves client communications drafts for the client contact, documents research, hands off to signer. |
| **Signer** | CPA (engagement owner) | Gate R9: high-level review, approval to deliver, signs the return (PTIN). Owns the client relationship and judgment calls the reviewer escalates. |
| **Client contact** | Usually the signer; per engagement letter | Approves outbound client emails drafted by the AI or reviewer, or authorizes the reviewer to send directly. |
| **Admin** | Admin team | Onboarding, rollover, extension batch, delivery package, e-file transmission (after release), billing release, paper-filing logistics. |
| **AI Ops owner** | Designated staff member (may be the signer) | Maintains AI instructions, Filed/StanfordTax configuration, and the feedback loop (Section 14). Not involved in individual returns. |

The signing CPA stays fully responsible for the return under Circular 230 (including §10.22 diligence as to accuracy)
and the AICPA Statements on Standards for Tax Services. **AI output is treated like the work of an unlicensed staff
member: useful, but never relied on without review.**

### Sign-off colors and marks

The pre-AI red/blue/green PDFlyer convention carries over, with one new color for the AI:

| Layer | Color | Where the mark lives |
|---|---|---|
| AI Preparer | **Purple** (system tag "AI-prepared") | Filed field status; AI Prep Memo; any AI calc tape in the StanfordTax workpaper |
| Reviewer | **Blue** | Filed review status / comments; StanfordTax workpaper annotations; Karbon review checklist items; reviewer calc workpapers |
| Signer | **Green** | Karbon signer checklist; StanfordTax workpaper annotations |

Tickmark meanings from the pre-AI doc stay the same. A blue mark on an AI-prepared item means "reviewer traced this to
source and agrees", not "reviewer saw it".

---

## 3. Review lifecycle at a glance

| Gate | Name | Owner | Main tool | Karbon status on exit (proposed) |
|---|---|---|---|---|
| R0 | Readiness gate: is the AI package complete? | Reviewer | Karbon | `Review - In Progress` or back to `AI Prep - Rework` |
| R1 | Client context and risk tier | Reviewer | Karbon, StanfordTax | (same) |
| R2 | Document completeness and ingestion integrity | Reviewer | StanfordTax, Filed | `Waiting on Client` if blocking items |
| R3 | Data verification (source to return) | Reviewer | Filed | (same) |
| R4 | Return review: analytics, then section checklists | Reviewer | ProConnect | (same) |
| R5 | Manual workarounds and overrides | Reviewer | ProConnect, StanfordTax workpaper | (same) |
| R6 | Diagnostics and e-file readiness | Reviewer | ProConnect | (same) |
| R7 | Review points, open items, client follow-up | Reviewer (+ AI rerun) | Karbon, StanfordTax, Filed | `Waiting on Client` / `AI Prep - Rework` / back to R3 |
| R8 | Hand-off to signer | Reviewer | Karbon, ProConnect | `Ready for Signer` |
| R9 | Signer review, delivery, 8879, e-file, billing | Signer, Admin | Karbon, StanfordTax, ProConnect | `Filed - Accepted` -> `Complete` |

A return can loop R7 -> R3 any number of times. Every loop is recorded in the Karbon work item timeline.

---

## 4. Risk tiers (set at R1, can only go up)

The tier controls review depth. The AI proposes a tier in its package; **the reviewer sets it**. Any trigger found later
moves the return up a tier immediately; a tier never goes down after R1.

| Tier | Typical profile | Triggers (any one moves the return to this tier or higher) |
|---|---|---|
| **1 - Standard** | W-2s, structured 1099s (INT, DIV, R, G, SSA), standard deduction or simple Schedule A, one resident state, no carryovers in play | - |
| **2 - Elevated** | Return has less-structured or calculation-heavy items | Schedule C; Schedule E rental; consolidated 1099 with adjustments (wash sales, market discount, accrued interest, missing basis, noncovered lots); K-1s without distribution or basis issues; nonresident or part-year state; local return; dependents with unearned income; HSA/education/credit computations; prior-year carryovers (capital loss, passive, NOL, charitable, AMT credit); estimated tax penalty; any document Filed could not extract with high confidence |
| **3 - Complex / Judgment** | Return depends on facts the documents do not show, or on software limitations | K-1 distributions above basis; S-corp debt vs stock basis; IRC 751 hot assets; IRC 311(b) property distributions; final trust/estate K-1s; installment sales; inherited property or decedent returns; filing-status change (marriage, divorce, death, HOH eligibility); COD income (Form 982); IRC 1244 / worthless stock; equity compensation (RSU/ISO/NQSO, 83(b)); PFIC (8621); CFC (5471/926); foreign trust or foreign gift (3520); FBAR / 8938; FTC above the $300 / $600 safe harbor; foreign currency translation; PTET credits; new state or local filing requirement; reportable transaction (8886); kiddie tax / child's separate return; amended or superseded return; any reviewer workaround (Section 9) needed; any reserved decision (Section 5.3) open |

### Review depth by tier

| Activity | Tier 1 | Tier 2 | Tier 3 |
|---|---|---|---|
| R0 readiness gate | Full | Full | Full |
| R2 document completeness | Full | Full | Full |
| R3 trace to source | Always-trace list + low-confidence fields + 10% random sample of the rest | Always-trace list + low-confidence fields + every field in the triggering area + 25% random sample of the rest | 100% of fields |
| R4 analytics (PY comparison) | Full | Full | Full |
| R4 section checklists (Section 8) | Only for sections present on the return | Only for sections present on the return | All sections present + Section 8.12 (foreign) and 8.13 (SALT) even if the AI found nothing |
| Independent recompute of tax (Section 8.1) | Spot check | Required | Required |
| Second-reviewer or signer pre-read | No | No | Signer pre-read of AI Prep Memo at R1 (5 minutes) |

**Always-trace list (every tier):** federal and state withholding; estimated payments and prior-year overpayment applied;
taxpayer and dependent SSNs, names and dates of birth; filing status inputs; bank account and routing numbers for
refund/debit; IP PINs; any field the AI typed by hand rather than extracted; any field with a ProConnect override.

**Materiality and sampling thresholds** are placeholders until the firm calibrates them on the v2 dataset and the first
season's results (Section 14). Proposed starting points: trace any single input over **$5,000** or over **5% of AGI**;
treat a Filed confidence below the vendor's "needs review" level as low-confidence (verify Filed's label).

---

## 5. The AI Prep Package (entry criteria for review)

### 5.1 What the AI must deliver

The AI Preparer must attach the following to the Karbon work item (or link them from it) before the work item can move
to `Ready for Review`. If any item is missing, the reviewer rejects at R0.

| # | Deliverable | Content | Location |
|---|---|---|---|
| 1 | **AI Prep Memo** | One page: household facts and changes vs PY; filing status reasoning; states/locals filed and why; summary of income by type vs PY; positions taken and assumptions; items the AI could not handle; questions for the reviewer | Karbon work item note + StanfordTax workpaper (bookmark "AI Prep Memo") |
| 2 | **Source-to-return map** | Every return input linked to a source document page or a questionnaire answer | Filed |
| 3 | **Document roll (PY vs CY)** | Every PY recurring source (payer/broker/K-1 entity/property) marked Received / Missing / Client confirmed discontinued / New this year | Filed or AI Prep Memo appendix |
| 4 | **Unprocessed document list** | Every document or page not extracted, with reason (handwritten, legal agreement, non-standard layout, duplicate, irrelevant, illegible) | Filed |
| 5 | **Duplicate log** | Suspected duplicates (same payer/account/amounts, CORRECTED vs original, reprints, phone photo vs PDF) and how each was treated | Filed |
| 6 | **Exception and override log (AI section)** | Every value the AI computed rather than extracted, and every ProConnect override it made, with reasoning | Exception log (Section 9.3) |
| 7 | **Open items list** | Internal questions and *draft* client requests (never sent) | Karbon work item; drafts in StanfordTax requests (unsent) |
| 8 | **Diagnostics snapshot** | ProConnect diagnostics at hand-off with the AI's notes | ProConnect + memo |
| 9 | **Proposed risk tier** | With the triggers that drove it | AI Prep Memo |
| 10 | **Reserved-decisions list** | Every decision in 5.3 that applies, with the facts and the AI's recommendation | AI Prep Memo |

### 5.2 What the AI may do

* Classify, split and extract documents in Filed; push extracted data to ProConnect.
* Enter structured data in ProConnect input screens, including standard calculations with a clear source (e.g., totals
  from a client-provided spreadsheet, FX translation using the IRS yearly average rate, tax-prep fee proration
  using the firm's default).
* Carry PY items forward and flag differences.
* Draft (not send) client requests and emails.
* Draft calc workpapers for the reviewer to verify.

### 5.3 Reserved decisions (AI recommends, reviewer or signer decides)

The AI must not make these calls on its own. It lists the facts and recommends; the reviewer decides and records the
decision in the exception log. Items marked **S** also need the signer's agreement.

* Filing status where more than one is possible or it changed from PY (MFJ vs MFS, HOH eligibility, year of death,
  qualifying surviving spouse) **S** when MFS vs MFJ changes tax by more than the materiality threshold.
* Dependency claims where another person may also claim the dependent.
* Elections: de minimis safe harbor; IRC 179 / bonus depreciation opt-outs; installment-method opt-out; Form 8814 vs
  child's own return; capitalization of carrying charges; real estate professional status; grouping elections;
  IRC 83(b) late-filing consequences; FTC vs deduction; itemize vs standard when close; state taxes vs sales tax.
* SEP / solo 401(k) contribution amount (client must confirm).
* Any position without clear authority, or any position needing Form 8275 disclosure **S**.
* Treatment of a document whose meaning depends on legal interpretation (settlement agreements, divorce decrees,
  trust instruments, operating agreements).
* Anything involving potential client error from a PY return (amend vs correct prospectively) **S**.
* Paper-file vs e-file routing.

---

## 6. Gate R0 - Readiness gate

**Goal:** do not spend review time on an incomplete package.

1. Open the Karbon work item. Confirm assignees: AI Preparer, Reviewer, Signer. (Pre-AI rule carried over: the signer
   makes sure preparer and reviewer are assigned before prep starts.)
2. Confirm in StanfordTax:
   * Signed engagement letter for this tax year. If missing, stop: notify the client contact today and set Karbon to
     `Waiting on Client - EL`.
   * Questionnaire status: complete, partially complete, or opted out. If opted out, the questionnaire record must be
     marked **"Blank Organizer"** (the pre-AI convention, now a StanfordTax note or tag - verify).
   * Contact preferences (phone, email, preferred method) match Karbon.
3. Confirm the Karbon "Actual Start Date" is the date the first PBC documents were received (used for FIFO and the
   15% expedite-fee test: materials received within 15 days of the deadline).
4. Confirm the extension position: if past the extension batch date and the return is not being filed by the original
   deadline, confirm in ProConnect e-file status that the federal Form 4868 **and each state extension** were
   accepted, and that any extension payment voucher/confirmation is in the workpaper. If an extension was rejected,
   fix it now - it outranks the review.
5. Check every item in Section 5.1 is present.

**Exit:** all present -> `Review - In Progress`. Anything missing -> `AI Prep - Rework` with a Karbon comment naming
what is missing. Do not partially review.

---

## 7. Gates R1-R3 - Context, completeness and data verification

### R1 - Client context and risk tier

1. Read the client's PERM record (Karbon client profile + StanfordTax permanent docs): residency history, special
   agreements (promissory notes, divorce decree, trust interests), basis records, carryover schedules, prior review
   points tagged "next year".
2. Read the PY return and PY review points. Note every PY carryover (capital loss, passive losses per activity, NOL,
   charitable, AMT credit, 8606 basis, depreciation, suspended basis losses, installment sales, FTC carryovers).
3. Read the AI Prep Memo end to end. Do not skim the "items the AI could not handle" section - that is your
   workaround list.
4. Set the risk tier (Section 4) in a Karbon custom field. Record the triggers.
5. For Tier 3, send the AI Prep Memo to the signer for a 5-minute pre-read; ask whether the signer knows of
   current-year events not in the documents (the signer's client knowledge is the cheapest control in this process).

### R2 - Document completeness and ingestion integrity

This gate replaces the pre-AI "page through the Scan workpaper" step. The AI does the paging; the reviewer checks
the AI's paging.

| Check | How | Pre-AI equivalent |
|---|---|---|
| **Recurring document roll** | Compare the AI's PY-vs-CY document roll to the PY return. Every PY payer, broker, K-1 entity, rental property and 1098 must be accounted for. **A blank questionnaire answer is not a zero** - unless the client confirmed the item did not occur, raise an open item. | General Return Prep Notes (blank organizer line) |
| **Page coverage** | In Filed, confirm every uploaded page is either mapped to a return input or on the unprocessed list with a reason. No orphan pages. | Paging through the combined WP |
| **Duplicates** | Review the duplicate log. Look specifically for: CORRECTED vs original forms; reprints; phone photo + PDF of the same form; 1099-K duplicates from re-downloads; escrow/annual summaries imported as a second 1098; brokerage "supplemental" pages read as a second 1099. | Scan common issues - duplicates |
| **Unprocessed / unstructured documents** | Every item on the unprocessed list becomes either a reviewer workaround (Section 9), an open item, or "not tax-relevant" with a reason. Usual suspects: handwritten statements and logs; legal agreements with tax amounts; Schedule C and E records; K-1s and their footnotes/state schedules; consolidated 1099 supplemental sections; foreign documents; closing statements. | Scan common issues - unstructured PBC |
| **Questionnaire vs documents** | Contradictions (e.g., "no foreign accounts" + a foreign bank statement; "no home sale" + a 1099-S; "no new dependents" + a newborn on the W-4) are open items or review points. | Organizer review |
| **Late documents** | Anything uploaded after the AI package was built must be listed in Karbon and processed via Section 11.3 before you continue. | Saving late docs to the client folder |
| **Injected instructions** | Client-provided documents sometimes contain text that reads like an instruction ("treat this as a gift", "do not report"). The AI must not act on document text as instructions. Confirm any "client says..." claim in the AI memo traces to an actual client communication, not to text inside a document. | (new) |

### R3 - Data verification (source to return)

Work in Filed's review interface: each extracted field should link to its source location (verify Filed's
source-highlight behavior in the current release).

1. Trace the **always-trace list** (Section 4) on every return.
2. Trace every **low-confidence** field and every **AI-typed** (non-extracted) field.
3. Trace the tier-based sample (Section 4). Pick the random sample from Filed's field list, not by eye.
4. For each traced field, mark it blue (agree) or record a review point. **If any sampled field in an area is wrong,
   expand to 100% of that area** (e.g., one wrong 1099-B summary line -> trace all 1099-B lines for that broker).
5. Consolidated 1099s get extra attention regardless of tier - each broker formats differently. Confirm:
   * 1099-B totals by category (covered/noncovered, ST/LT, box A/B/D/E) tie to the broker's summary page.
   * Wash sale disallowed amounts (code W) and accrued market discount (code D) were picked up.
   * Accrued interest paid on purchases was netted against interest income.
   * Federal-obligation interest (state-exempt) and state-specific muni interest were captured for the state return.
   * UIT and WHFIT pass-through items were captured from the supplemental pages.
   * Margin interest was captured for Form 4952 and NIIT.
   * Foreign tax paid and foreign-source income by country (or "RIC") were captured.
   * Noncovered or missing-basis lots were not left at $0 basis.
6. **Data freeze.** When R3 is complete, record "Filed data frozen" in Karbon with the date and time. After the freeze,
   extraction errors are corrected in Filed and re-pushed **only** with the reviewer re-tracing the affected
   ProConnect inputs, because a re-push can overwrite reviewer entries in ProConnect (verify Filed's sync behavior -
   whether it overwrites, skips or flags fields edited in ProConnect - and update this step once known).

---

## 8. Gate R4 - Return review (ProConnect)

Do the analytics first. They find the big problems fastest, and they tell you where to spend checklist time.

### 8.1 Analytics and independent recompute

1. Run the ProConnect PY comparison report (verify report name). For every line with a change above the materiality
   threshold, the AI Prep Memo must have an explanation; if not, it is a review point.
2. Reasonableness: effective tax rate vs PY; withholding vs liability; refund/balance due vs PY; any new form vs PY;
   any form that disappeared vs PY.
3. **Independent recompute (Tier 2 and 3; spot check Tier 1):** estimate total tax outside ProConnect - ordinary
   brackets, preferential-rate income, SE tax, NIIT, Additional Medicare Tax, AMT exposure - to within a reasonable
   tolerance. A large gap is a review point even if you cannot yet see the cause. This is the main control against
   automation bias: you are checking the answer, not just the inputs.
4. Confirm the tax year's law was applied, not the AI's training-data default. For TY2025 (OBBBA), spot check:
   standard deduction amounts; SALT cap ($40,000 / $20,000 MFS, phase-down above $500,000 MAGI, $10,000 floor);
   Schedule 1-A items (qualified tips, qualified overtime premium, car-loan interest, senior deduction) and their
   phase-outs; CTC amount; 1099-K threshold; and items that **start in 2026, not 2025** (90% gambling loss limit,
   non-itemizer charitable deduction, 0.5% charitable floor). Use the Project Evergreen v2 `DATASET_DESIGN.md` table as
   the firm's quick-reference until a dedicated law table exists.

### 8.2 Filing status, household and identity

* Filing status reasoning in the AI memo agrees with the facts at 12/31 (married at year end -> MFJ/MFS available;
  divorce finalized by 12/31 -> not married; legal separation without a final decree does not count as divorce).
* **Year of death:** the surviving spouse files MFJ for the year of death (if not remarried); qualifying surviving
  spouse status is only available for the **two following years** and requires a dependent child. (Corrects the
  pre-AI doc wording - see Appendix H.)
* Single filers claiming a dependent: test HOH eligibility.
* Dependents: SSN/ITIN, age, relationship, residency, support; qualifying relative gross income test.
* IP PINs for the taxpayer, spouse and **each dependent** - new every year. Missing IP PIN = guaranteed e-file reject.
* Driver's license / state ID data entered if the state requires it.

### 8.3 Income - wages, retirement, Social Security, other

* W-2 box 12 codes (D, W, DD, AA, BB, V, C) and box 14 items flowed correctly; HSA code W vs Form 8889.
* Excess Social Security withholding (multiple employers); Additional Medicare Tax on combined wages.
* 1099-R distribution codes; rollovers; CORRECTED forms superseding originals; QCD eligibility (age 70 1/2+, direct to
  charity, limit); Form 8606 basis and pro-rata rule for any conversion or backdoor Roth.
* **IRA-held assets:** brokerage statements, K-1s or other forms issued *to an IRA* are not reported on the 1040
  (except UBTI considerations at the IRA level). Remove them if the AI picked them up.
* SSA-1099: taxable portion; Medicare premiums withheld moved to Schedule A medical; foreign pensions included in the
  provisional-income computation.
* 1099-G: state refund taxable only to the extent of PY tax benefit (check PY itemized vs standard and the PY SALT cap).
* 1099-K: personal items sold at a loss are not income; business 1099-K vs gross receipts reconciliation.
* 1099-C: COD income or exclusion (insolvency, Form 982) - Tier 3.

### 8.4 Schedule A

* Home office: amounts on Form 8829 not also on Schedule A (mortgage interest, real estate tax).
* Medical: includes Medicare premiums from SSA-1099; 7.5% AGI floor.
* SALT: PY refund handling; income tax vs general sales tax election (not both); large-ticket sales tax on vehicles or
  boats when using the sales-tax table; OBBBA cap and phase-down.
* Mortgage interest: **pre-12/16/2017 acquisition debt keeps the $1,000,000 limit** (grandfathered); later debt
  $750,000. Check how ProConnect is computing the limit when there are mixed or refinanced loans; if it is wrong,
  compute outside the software and enter the deductible amount (workaround - Section 9).
* Rental-address 1098s belong on Schedule E, not Schedule A.
* Charitable: cash vs noncash; Form 8283 above $500 noncash; qualified appraisal above $5,000; DAF timing (deduction
  in the year of contribution to the DAF); crowdfunding gifts to individuals are not deductible. Clothing and household
  goods are deductible at **fair market value** (thrift-store value) and must be in good used condition - the pre-AI
  "3x cost basis" rule of thumb should be retired (Appendix H).
* Casualty losses: federally declared disaster area only for 2025.
* Gambling: losses limited to winnings (2025); the 90% limit applies from 2026.

### 8.5 Schedule B and interest/dividend details

* Market discount reported as interest (Schedule B), reversed out of Schedule D gain.
* Accrued interest paid netted against interest income.
* State-exempt federal obligation interest computed for each state return, with a calc tape in the workpaper.
* Part III foreign account and foreign trust questions answered consistently with FBAR/3520 facts.

### 8.6 Schedule C

* Cash vs accrual: tax return on the method the business actually uses for tax; accrual books converted where needed.
* AJEs the firm proposed in the PY were booked (otherwise opening balances and retained earnings do not roll).
* Book-tax differences: meals (50%), entertainment (0%), personal expenses, club dues, gifts above $25 per recipient.
* De minimis safe harbor election (items up to $2,500 per invoice/item) - reserved decision.
* Tax-prep fee proration to Schedule C (legal and professional fees) using time on Schedule C vs whole return.
* SEP-IRA: client confirmed the amount; self-employed rate is 20% of net SE earnings (after the SE tax deduction), not
  25% of net profit.
* SE health insurance: not allowed for any month the taxpayer or spouse was eligible for a subsidized employer plan.
* Home office: simplified ($5/sq ft, up to 300 sq ft) vs Form 8829 actual; home-office 1098 and utilities prorated.
* Form 1099 filing questions at the top of Schedule C; "started or acquired this business in 2025" box.
* QBI: Schedule C income, SSTB status, W-2 wages and UBIA reported for the 199A computation.

### 8.7 Schedule D / Form 8949

* Adjustment codes applied: **D** market discount, **W** wash sale, **C** collectibles (28%), **M** multiple
  transactions, **H** home sale, **B** basis incorrect, **O** other, plus **E** selling expenses where relevant.
* Missing or $0 basis lots: basis found in the statement, client records, or inheritance records - never left at $0.
* Summary-line vs detail reporting: covered lots with no adjustments may go as summary lines (Schedule D line 1a/8a);
  everything else on Form 8949, with an attached statement for complex or adjusted groups.
* Inherited property: stepped-up basis (date-of-death value), holding period always long-term; inherited home sale
  rules.
* Home sale: IRC 121 exclusion eligibility and amount.
* Equity compensation: RSU/NQSO/ESPP basis adjustments for amounts already in W-2 wages (broker 1099-B often shows
  $0 or unadjusted basis); ISO AMT adjustments.
* Installment sales (Form 6252): gain recognized proportionally to payments; the payment schedule's dates and amounts
  checked against the sale agreement.
* Capital loss carryover from the PY return ties in.

### 8.8 Schedule E - rentals

* Rental-address 1098 amounts moved from Schedule A to Schedule E.
* Personal-use days entered so expenses are prorated; IRC 280A vacation-home limits when personal use is significant.
* Repairs vs capital improvements (roofs, HVAC, major renovations are capital); de minimis safe harbor election.
* Depreciation continuity with PY asset list; land excluded from basis.
* Passive activity limits (Form 8582): PY suspended losses carried in; $25,000 allowance phase-out.

### 8.9 K-1s (partnerships, S corporations, trusts and estates)

K-1s are the largest source of silent errors. ProConnect generally computes what it is given; the reviewer supplies the
facts the 1040 cannot see. Each item below is also in the workaround catalog (Appendix B).

* **S corporation stock vs debt basis:** distributions are tax-free only up to **stock** basis; debt basis does not
  cover distributions. Form 7203 must be complete with stock and debt basis entered separately.
* **Partnership outside basis:** distributions (box 19 code A) above outside basis are capital gain. Turn on basis
  tracking in the K-1 input and enter beginning basis.
* **IRC 751 hot assets:** a distribution that changes the partner's share of unrealized receivables or inventory
  creates ordinary income the K-1 alone may not show.
* **IRC 311(b) property distributions** from an S corp: corporate-level gain should be on the K-1 and increases stock
  basis before the distribution reduces it.
* **Built-in gains** history the 1040 module does not know (purchased or inherited S-corp stock).
* **Final trust/estate K-1s:** excess deductions and suspended losses on termination; passive losses tied to
  distributed property follow the property's basis.
* **PTET:** the entity-level state tax is already deducted in computing K-1 income - do not also deduct it on Schedule
  A. Claim the owner-level state credit (or exclusion) on the state return per that state's rules.
* **K-2/K-3:** needed for foreign tax credit (Form 1116) sourcing and other international items; if the client has
  foreign tax from the K-1 and no K-3, request it or confirm the domestic filing exception applies.
* **R&D credit (Form 6765 via K-1):** flows to Form 3800 as a general business credit; check passive-activity and tax
  liability limits and any carryover.
* **Reorganizations (e.g., IRC 354/356/361 transactions reported by the entity):** shareholder-level gain is generally
  limited to boot received; confirm basis in new stock and holding period. Any such footnote is Tier 3.
* **Oil and gas:** depletion, working interest vs royalty, required statements.
* **State apportionment schedules:** compare positive income allocated to each state against nonresident filing
  thresholds (Section 8.13). Losses alone do not create a filing requirement.
* **QBI:** section 199A information (QBI, W-2 wages, UBIA, SSTB) entered and flowing to Form 8995 / 8995-A.
* **QOF / QROF investments:** the fund certifies on **Form 8996**; the **investor files Form 8997** with the 1040 every
  year they hold a QOF investment (deferred gain, inclusion events, holdings at year end). Confirm the deferral
  election and Form 8997 roll-forward from the PY.

### 8.10 NIIT, AMT and other taxes

* NIIT (Form 8960): investment interest (including margin interest) and other allocable deductions; K-1 items
  classified correctly as passive/active and trade-or-business vs investment.
* AMT (Form 6251): ISOs, private activity bond interest, large SALT, depreciation differences.
* Additional Medicare Tax (Form 8959), SE tax (Schedule SE), household employment (Schedule H), kiddie tax
  (Form 8615) or parent election (Form 8814).
* Estimated tax penalty (Form 2210): estimates actually paid vs organizer; annualization if income was uneven.

### 8.11 Credits

* Child tax credit / ODC / ACTC; child and dependent care (vs FSA exclusion); education credits (and 1098-T vs
  actual payments); premium tax credit reconciliation (1095-A); energy credits (expenditures through 12/31/2025);
  clean vehicle credits (vehicles acquired after 09/30/2025 do not qualify); EITC due diligence (Form 8867) where
  applicable.

### 8.12 Foreign (always checked on Tier 3)

* FTC: claim directly on Schedule 3 without Form 1116 if all foreign income is passive, reported on a payee statement,
  and foreign tax is **$300 or less ($600 MFJ)**; otherwise Form 1116 by category (passive, general), with "RIC" for
  mutual-fund pass-through foreign tax; high-tax kickout considered; carryovers.
* Currency: USD amounts from the statement if provided; otherwise original currency plus the IRS yearly average rate
  (or spot rate where required), with the conversion shown in the workpaper.
* Foreign pensions (e.g., Canadian NR-4): taxable amount, treaty position, FX translation, effect on taxable Social
  Security.
* FBAR (FinCEN 114): aggregate max balance above $10,000 at any time; filed separately through BSA E-Filing; uses
  Treasury Reporting Rates of Exchange. Form 8938 thresholds checked separately.
* Form 8621 (PFIC), 5471 (CFC) / 926, 8865, 3520 / 3520-A (foreign trusts and large foreign gifts or bequests),
  8886 (reportable transactions). **Confirm ProConnect supports each form before relying on it** - the v2 dataset has
  cases where Form 3520 and Form 8865 are not available in ProConnect and must be prepared and filed outside the 1040
  e-file (Appendix B).

### 8.13 State and local

* Resident, part-year and nonresident returns: residency dates, income allocation, credits for taxes paid to other
  states.
* **New filing requirements:** move during the year (including a move to another town in the same state, e.g., into or
  out of Detroit); W-2 work-state wages; K-1 state apportionment above nonresident thresholds; rental property in
  another state.
* State modifications: federal-obligation interest subtraction; state treatment of retirement income, HSA, bonus
  depreciation, PTET.
* Local returns (city income taxes) and school district returns where applicable.
* ProConnect state return set-up matches the Karbon routing (each state/local added with e-file or paper).

### 8.14 Restricted stock and other one-offs

* IRC 83(b): election must have been filed within 30 days of the transfer (Form 15620 or a written statement). If late,
  the election is invalid - escalate to signer (reserved decision).
* Disaster relief postponements (filing and payment) checked on IRS disaster relief pages for the client's county.

---

## 9. Gate R5 - Manual workarounds and overrides

All manual work the pre-AI preparer used to do now sits here, with the reviewer.

### 9.1 Order of preference

1. **Fix the input, not the output.** Enter the correct facts on the proper ProConnect input screen (e.g., basis
   limitation fields, personal-use days, adjustment codes) so ProConnect computes the right answer and carries it to
   next year.
2. **Use ProConnect's adjustment fields** (e.g., "other increases to basis", carryover inputs) where the input screen
   allows it.
3. **Override** a computed amount only when 1 and 2 are not possible. Check whether the override triggers an e-file
   diagnostic or affects state returns (verify ProConnect override behavior per field).
4. **Prepare outside ProConnect** when ProConnect does not support the form (e.g., Form 3520, Form 8865) and route it
   to paper or stand-alone filing.

### 9.2 Required documentation for every workaround

For each workaround, before moving on:

* A **calc workpaper** (spreadsheet or calc tape) in the StanfordTax workpaper binder, bookmarked under the related
  form, with sources tickmarked in blue.
* An **exception log entry** (9.3).
* If it affects next year (carryovers, basis, suspended losses, depreciation, installment balances, elections), a
  **rollover note** on the client's Karbon profile tagged `Rollover TY2026` (verify Karbon tagging approach) and noted
  in the exception log.
* A **Karbon time entry** coded `Review - Manual workaround`. This feeds pricing (Section 13) and the AI feedback loop.

### 9.3 Exception log format

One log per return, stored as a spreadsheet in the workpaper binder and linked from Karbon. The format mirrors the
v2 dataset's `*_Software_Exceptions.md` / workbook so the dataset can be used for training and testing.

| Field | Example |
|---|---|
| ID | `EVG1007-2025-WX01` |
| Source | AI / Reviewer / Signer |
| Area | Schedule E - K-1 S corporation |
| What the software or AI did by default | Distribution of $40,000 treated as tax-free because combined stock + debt basis was positive |
| Why that is wrong here | Stock basis is $0; debt basis does not cover distributions |
| Fix and where entered | Stock and debt basis split on the S-corp K-1 basis inputs / Form 7203 (verify screen) |
| Amount | 40,000 |
| Override? (Y/N) and field | N |
| E-file impact | None |
| Workpaper ref | WP 12.3 |
| Next-year impact | Stock basis carries at $0; debt basis $50,000 |
| Root cause tag | Software limitation (see Section 14) |
| Reviewer / date | Blue initials, date |

### 9.4 Workaround catalog

Appendix B lists the known workarounds by area: the AI's or ProConnect's default behavior, the reviewer action and
the evidence required. It is a living list. Add to it every time a new workaround is found.

---

## 10. Gate R6 - Diagnostics and e-file readiness

1. Run ProConnect diagnostics for the federal return and each state/local return.
2. **Critical / e-file-blocking errors:** all cleared. None may remain at hand-off. (Pre-AI: preparer cleared; now the
   AI clears what it can and the reviewer clears the rest.)
3. **Warnings:** the reviewer reviews **every** warning, including those the AI says it resolved, and records the
   treatment in the AI Prep Memo diagnostics section (blue). The AI cannot approve warnings - the pre-AI rule that
   warnings need reviewer/signer approval now means every warning gets a reviewer decision.
4. **Informational:** scan for anything unexpected.
5. Confirm e-file eligibility: no unsupported forms riding with the e-file; overrides that block e-file resolved or the
   return routed to paper; required PDF attachments attached (e.g., Form 8949 statements, 83(b) copies, appraisals,
   decedent documents) - verify ProConnect's attachment method.
6. Paper-file triggers (route to Admin with reason): return outside the e-file window (current year plus two prior
   years); persistent rejects; dependent already claimed by another taxpayer; unresolved name/SSN mismatch; forms
   that cannot be e-filed in ProConnect; IRS maintenance window timing.

---

## 11. Gate R7 - Review points, open items and client follow-up

### 11.1 Review points

Every issue gets a numbered review point in Karbon (or the Review Points document - Appendix D) with:

* Client ID, tax year, return type in the title ("EVG1007 - 2025 - 1040 - Review Points").
* Reference to the form/schedule/line or WP number, a screenshot, and sub-points for each part of the issue.
* **Owner:** `AI rerun` (data/extraction issue the AI can fix), `Reviewer` (workaround or judgment), `Client`
  (information needed), or `Signer` (escalation).
* **Root cause tag** (Section 14).

**AI rerun points:** send the point to the AI Preparer with the exact correction expected. When the AI finishes, the
reviewer re-traces the affected inputs (and anything downstream). An AI rerun after the data freeze always reopens R3
for the affected area.

**Reviewer-fixed points:** fix, document (Section 9.2), mark blue as resolved.

### 11.2 Client open items

1. The AI drafts each client request in StanfordTax (unsent). The reviewer edits for tone, accuracy and completeness,
   and combines requests so the client gets **one** request round where possible.
2. The reviewer sends the draft to the **client contact** (usually the signer) for approval. The client contact either
   sends it or authorizes the reviewer to send it, with the client contact copied. (Pre-AI rule unchanged.)
3. Requests go to the client through the StanfordTax portal (with an email notice if that is the client's
   preference), so the reply and documents land in the same place.
4. Set Karbon to `Waiting on Client` with a follow-up date. Do not let the AI send reminders unless the firm has
   approved an automated reminder template for that purpose.
5. Phone conversations: record a dated memo (firm memo template) and save it as **client correspondence** in the
   current-year workpaper binder, before the checklist at the end. First-year interview notes go to PERM.

### 11.3 Late documents (after the AI package was built)

1. Admin or the reviewer logs the new document in Karbon.
2. The AI processes **only the new document** in Filed and lists the affected return lines.
3. The reviewer traces the new inputs and re-runs R4 analytics and R6 diagnostics for the affected areas.
4. If the late document is from the client after the return was delivered, use the Section 12.4 update rules
   (internal vs external reason) for billing.

### 11.4 Tax research

Keep the pre-AI research documentation standard (question, answer, authority, currency check, SALT jurisdiction's own
authority) and the hierarchy of authority. Two additions for AI-assisted research:

* **Every citation the AI produces must be pulled and read** from a primary source (IRC, regulations, IRS guidance,
  court opinion) before it is relied on. AI-generated citations can be wrong or invented.
* Record in the research memo which parts were AI-drafted and confirm the currency check was done by the reviewer.

---

## 12. Gates R8-R9 - Hand-off, signer, delivery, e-file and billing

### 12.1 R8 - Hand-off to signer (reviewer checklist in Karbon)

* [ ] All review points resolved or escalated; none open with owner `AI rerun` or `Reviewer`.
* [ ] Exception log complete; every workaround has a workpaper and rollover note where needed.
* [ ] R6 complete: no blocking diagnostics; every warning has a recorded decision.
* [ ] Reserved decisions all decided and recorded (with signer agreement where marked **S**).
* [ ] **Reviewer Memo** (half a page): tier, key judgments, workarounds, open risk, anything the signer should
  discuss with the client.
* [ ] Return locked/frozen in ProConnect against further edits, or status set to "Ready for signer" if locking is not
  available (verify ProConnect locking options).
* [ ] Reviewed return PDF (accountant/preparer copy) saved to the workpaper binder and named
  `<ClientID>_<TY>_1040_Reviewed.pdf`.
* [ ] Routing verified in Karbon: federal; each state; each local; FBAR / 3520 / other stand-alone filings noted; due
  dates for each; e-file vs paper for each; e-signature method; client contact and preferred method; special
  processing instructions; project notes cleared.
* [ ] Workpaper binder in StanfordTax in final order: signed engagement letter first; questionnaire; source documents
  (mapped); AI Prep Memo; reviewer calc workpapers; exception log; research memos; client correspondence; review
  checklist / AICPA checklist last.

### 12.2 R9 - Signer

The signer's review is high level, informed by client knowledge: read the Reviewer Memo and AI Prep Memo; scan the
return summary and PY comparison; probe the Tier 3 items and any workaround with a large dollar effect. Changes go
back to the reviewer (one layer of review, not two, since there is no human preparer). Small changes the signer may
make directly and note in the exception log in green.

### 12.3 Delivery, 8879, e-file

1. Admin builds the delivery package: client copy of the return, invoice from Karbon, and the e-file authorization
   (Form 8879 and state equivalents) **as a separate signature request** through StanfordTax (or ProConnect's
   e-signature if the firm standardizes on that - pick one; verify KBA requirements are met for remote signing).
2. When the client signs, hold the return for **24 hours** in case the client comes back with changes, then transmit
   from ProConnect.
3. Monitor acknowledgements in ProConnect until each federal, state and local return shows **accepted**. Record the
   acceptance date in Karbon.
4. **Rejects:** document the reject code and reason; fix; save the updated return version; retransmit; monitor. Common
   causes: missing or stale IP PIN (taxpayer, spouse or dependent), missing self-select PIN / PY AGI, driver's
   license data required by a state, dependent already claimed, name control mismatch. A second reject on the same
   issue goes to the signer for a paper-file decision.
5. Paper filing: government copy, correct IRS processing center address, tracked delivery, tracking number in Karbon.
6. FBAR and other stand-alone filings: confirm filed and the confirmation saved to the deliverables folder.
7. Deliverables saved: client copy, signed 8879s, acknowledgements, payment vouchers, and estimated-payment schedule.

### 12.4 Billing (Karbon)

* Review WIP: bill, write off, or leave in WIP for open projects (pre-AI rules unchanged; checkmark each line).
* Updates after delivery: **internal reasons** (AI or reviewer error, missed document already received, software
  issue, wrong static data) are written off; **external reasons** (client gave wrong or incomplete information) are
  chargeable. The root cause tag on the review point decides which.
* Manual-workaround time (Section 9.2) is reported per return so the quote can be adjusted for complexity the client
  did not disclose.
* Invoice summary: two columns (description, amount), forms prepared, keep it simple; flag progress billing clearly.

### 12.5 Post-submission exceptions

The pre-AI sections on superseded returns (before the extended due date), amended returns (1040-X after the due date),
e-file rejects and paper filing still apply. For any of these, open a new Karbon work item linked to the original, and
run gates R0-R9 on the change only, with the tier set to at least Tier 2.

---

## 13. Quoting and capacity notes (impact of AI prep)

Not part of the review itself, but it changes how review time is planned:

* Reviewer time is driven by the **tier** and the **number of workarounds**, not by page count.
* Track per return: tier, review hours, number of workarounds, number of AI reruns, number of client request rounds.
  Use these to set next year's quote and to plan reviewer capacity in Karbon.

---

## 14. Quality feedback loop

Every review point and exception log entry gets one **root cause tag**:

| Tag | Meaning | Fixed by |
|---|---|---|
| `INGEST` | Filed extracted, classified or de-duplicated incorrectly | Filed configuration / vendor ticket |
| `QUESTIONNAIRE` | The StanfordTax questionnaire did not ask the question that would have surfaced the issue | StanfordTax questionnaire update |
| `AI-RULE` | The AI applied the wrong rule or law year, or missed a known pattern | AI instruction / rule update |
| `AI-JUDGMENT` | The AI made a call that belonged on the reserved list | Reserved-decision list or AI instructions |
| `ENGINE` | ProConnect limitation or default behavior | Workaround catalog (Appendix B) |
| `CLIENT` | Client data wrong, missing or late | Client communication; billing (external reason) |
| `REVIEW` | Reviewer missed it (found by signer or after filing) | Training; checklist update |

Monthly in season (weekly in the final four weeks before a deadline), the AI Ops owner reviews the counts by tag and
updates the AI instructions, Filed and StanfordTax configuration, the workaround catalog and this procedure. Changes
are versioned in the change log below.

**Calibration with the Project Evergreen v2 dataset.** Before go-live, run the AI preparer on the 25 v2 clients
(inputs only: `PERM/` and `2025/PBC/`), run this review procedure on the output, and score it against the answer keys
(`*_Answer_Key.json`, `all_gotchas.jsonl`, `all_software_exceptions.jsonl`). Use the results to set the materiality,
sampling and confidence thresholds in Section 4 and to check that every v2 gotcha is caught by at least one gate.

---

## Appendix A - Pre-AI step to AI-native step mapping

| Pre-AI step (procedure doc section) | AI-native owner | AI-native tool | Reviewer action |
|---|---|---|---|
| Actual Start Date; FIFO; assign preparer/reviewer | Admin / Signer | Karbon | R0 confirm |
| Engagement letter check | Admin; reviewer at R0 | StanfordTax | R0 stop if missing |
| Organizer sent via Sharefile; "Blank Organizer" | Admin | StanfordTax questionnaire | R0 status check |
| Client interview memo | Reviewer or signer | Karbon note + StanfordTax binder | R1 read; R7 record new conversations |
| Scan / AutoFlow; combined WP | AI | Filed | R2 page coverage; R3 trace |
| Scan common issues (missing recurring, duplicates, unstructured, poor scan) | AI flags | Filed | R2 checks; workarounds R5 |
| Workpaper order (EL first, organizer, correspondence, AICPA checklist last) | AI assembles | StanfordTax workpaper binder | R8 confirm order |
| Per-page red/blue/green sign-off | AI purple / reviewer blue / signer green | Filed + StanfordTax + Karbon | R3 trace marks; R8 checklist |
| Blank organizer line = not zero | AI document roll | Filed / memo | R2 |
| Lists in Axcess (manual tallies) | AI calc workpaper | StanfordTax binder (supporting calc) | R3 trace totals; roll forward annually |
| Adding/removing states in Workstream | AI proposes; reviewer confirms | ProConnect states + Karbon routing | R4 8.13; R8 routing |
| E-file diagnostics sign-off | AI clears errors; reviewer decides warnings | ProConnect | R6 |
| Responding to review points (red) | AI rerun or reviewer | Karbon / Filed | R7 |
| Return-section manual items (Sch A-E, K-1s, NIIT, foreign) | Reviewer workaround | ProConnect + binder | R4, R5, Appendix B |
| Review points document | Reviewer | Karbon / Appendix D | R7 |
| Tax research documentation | Reviewer (AI may draft) | Binder | R7 11.4 |
| Hand-off to signer (lock, reviewed copy, routing) | Reviewer | ProConnect + Karbon | R8 |
| Sign-off, delivery, 8879, 24-hour hold, e-file | Signer / Admin | Karbon, StanfordTax, ProConnect | R9 |
| Billing (WIP, W/O, internal vs external) | Signer / Admin | Karbon | R9 12.4 |
| Rejects, superseded, amended, paper filing | Reviewer / Admin | ProConnect + Karbon | 12.3, 12.5 |

---

## Appendix B - Reviewer workaround catalog (starter list)

"Default" = what the AI or ProConnect typically does with the documents alone. All ProConnect locations are
**(verify)** against the current release.

| # | Area | Default (wrong) behavior | Reviewer action | Evidence |
|---|---|---|---|---|
| B1 | Duplicate forms | Original + CORRECTED, reprint, phone photo, or re-download all imported | Delete duplicate inputs in Filed; re-trace totals | Duplicate log; blue tick |
| B2 | Handwritten logs (tips, mileage, cash income) | Not extracted, or extracted with errors | Key from source; total on a calc tape | Calc workpaper |
| B3 | Consolidated 1099: accrued interest paid | Left in gross interest | Enter as a reduction of interest income ("accrued interest" adjustment) | Statement page tickmarked |
| B4 | Consolidated 1099: market discount | Left inside Schedule D gain | Report as interest; reverse from gain (code D) | Calc tape |
| B5 | Consolidated 1099: state-exempt federal interest | Not split for state | State subtraction computed per state | Calc tape on statement page |
| B6 | Missing / $0 basis lots, RSU/ESPP basis | $0 or unadjusted basis | Correct basis, code B; attach statement | Basis support |
| B7 | Mortgage interest limit with pre-12/16/2017 debt or mixed loans | Limit computed on the wrong debt cap or average balance | Compute deductible interest outside; enter/override | Limitation calc |
| B8 | Home office vs Schedule A | Mortgage interest / taxes double counted | Confirm the Form 8829 portion is removed from Schedule A | Tie-out |
| B9 | Rental-address 1098 | Lands on Schedule A | Move to Schedule E property | 1098 box 8 address |
| B10 | Installment sale | Full gain in year of sale, or wrong payment schedule | Form 6252 with payment schedule from the agreement | Agreement extract |
| B11 | S-corp distribution above stock basis | Treated as tax-free because stock + debt basis > 0 | Enter stock and debt basis separately (Form 7203 inputs); excess to Form 8949 | Basis schedule |
| B12 | IRC 311(b) property distribution | Book value used; gain missing if K-1 omitted it | Enter corporate-level gain share; basis increase before distribution | FMV support, calc |
| B13 | Partnership distribution above outside basis | No gain because basis tracking off | Turn on basis limitation; enter beginning basis; excess to Form 8949 | Outside basis schedule |
| B14 | IRC 751 hot assets | Distribution treated as basis reduction only | Compute 751 ordinary income outside; enter as ordinary income; adjust basis inputs to avoid double count | 751 calc |
| B15 | Final trust/estate K-1 suspended/passive losses | Lost on termination | Carry into the distributed asset's basis or PY suspended loss field | Final K-1 footnote |
| B16 | PTET | Entity tax also deducted on Schedule A | Remove from Schedule A; state credit on state return | K-1 PTET statement |
| B17 | Built-in gains / inherited S-corp stock history | Not known to 1040 | Signer escalation; compute and document | Memo |
| B18 | Foreign pension (e.g., NR-4) | Not imported (no U.S. form) | Enter USD at IRS rate; Form 1116 general category; include in SS provisional income | FX calc |
| B19 | FTC under $300 / $600 | Form 1116 generated unnecessarily (or vice versa) | Elect direct credit when eligible | Tie to 1099 |
| B20 | Form 3520 / 8865 / other unsupported forms | Not available in ProConnect | Prepare outside ProConnect; paper or stand-alone filing; route in Karbon | Filing copy + tracking |
| B21 | FBAR | Not part of the 1040 | Prepare and file via BSA E-Filing; Treasury year-end rates | Confirmation |
| B22 | COD with insolvency (Form 982) | 1099-C fully taxable | Insolvency worksheet; Form 982; next-year attribute reduction (override carryover) | Balance sheet immediately before discharge |
| B23 | IRC 1244 / worthless stock | All capital loss | Split ordinary 1244 portion to Form 4797; remainder capital, deemed sold 12/31 | Stock records |
| B24 | Capital loss / passive carryovers after attribute reduction or audits | Unadjusted carryover proformas | Override carryover; rollover note | Calc |
| B25 | Kiddie tax / Form 8814 | Election made where not eligible, or child's return missed | Test eligibility; open child's Karbon client and 1040 work item if needed | Calc |
| B26 | Year-of-death filing status / senior deduction | Wrong status or deduction dropped for deceased spouse | Correct status; confirm age-based items | Memo |
| B27 | Local returns after a move (e.g., Detroit) | Proforma as full-year resident; wrong wage allocation | Part-year set-up; allocate wages by dates | Allocation calc |
| B28 | 1042-S withholding on a U.S. person's 1040 | E-file not possible / credit missed | Paper file with 1042-S attached (per v2 dataset) | 1042-S copy |
| B29 | IP PINs (taxpayer, spouse, dependents) | Missing or PY PIN reused | Request current-year PIN before transmission | Client confirmation |
| B30 | Tax law year (OBBBA) items | Training-data default amounts or 2026 rules applied to 2025 | Correct amounts; note in exception log | Law table |

Cross-reference: the v2 dataset's `SOFTWARE_EXCEPTION_MATRIX.md` and each client's `*_Software_Exceptions.md` show
ProConnect-specific defaults and fixes for most of these.

---

## Appendix C - Karbon work template (proposed skeleton)

Work type: `1040 Individual - AI Prep`. Work item title: `<ClientID> | <TY> | 1040`. One work item per client per tax
year per project code (no duplicates, per the pre-AI project-code rule). Statuses below are proposed custom statuses.

| Section | Tasks (checklist items) | Assignee |
|---|---|---|
| Intake | EL signed; questionnaire sent/complete/"Blank Organizer"; PBC received; Actual Start Date set; expedite-fee test | Admin |
| Extension | 4868 + state extensions sent and **accepted**; payment vouchers saved | Admin / Reviewer |
| AI Prep | Filed processing complete; ProConnect push complete; AI Prep Package attached (10 items) | AI Preparer |
| R0-R1 | Readiness gate; tier set; signer pre-read (Tier 3) | Reviewer |
| R2-R3 | Completeness; page coverage; duplicates; trace sample; data freeze timestamp | Reviewer |
| R4-R6 | Analytics; section checklists; workarounds logged; diagnostics cleared | Reviewer |
| R7 | Review points resolved; client requests approved by client contact and sent | Reviewer / Client contact |
| R8 | Hand-off checklist (12.1) | Reviewer |
| R9 | Signer review; delivery package; 8879 signed; 24-hour hold; transmitted; accepted (each jurisdiction); stand-alone filings | Signer / Admin |
| Billing | WIP review; internal vs external updates; invoice released | Signer / Admin |
| Rollover | Rollover notes reviewed and copied to next year's work template | Reviewer |

Statuses: `Planned` -> `Waiting on Client - EL` -> `Docs In Progress` -> `AI Prep` -> `AI Prep - Rework` ->
`Ready for Review` -> `Review - In Progress` -> `Waiting on Client` -> `Ready for Signer` -> `Out for Signature` ->
`Ready to File` -> `Filed - Pending Ack` -> `Filed - Accepted` -> `Complete`.

---

## Appendix D - Review points template

```
EVG1007 - 2025 - 1040 - Review Points
Reviewer: ____  Date: ____  Round: 1

1. [Schedule E / K-1 Brightline S Corp] Distribution above stock basis           Owner: Reviewer   Tag: ENGINE
   1a. Stock basis per Form 7203 is $0; debt basis $50,000. Distribution $40,000 is taxable.   [screenshot]
   1b. Split stock and debt basis in the K-1 basis inputs; confirm Form 8949 line.             [screenshot]
   Resolution (blue): done - WX01, WP 12.3

2. [WP 4.1 / Schedule B] Accrued interest paid not netted                        Owner: AI rerun   Tag: INGEST
   2a. $1,240 on the 3/2 bond purchase (Schwab 1099 p. 14).                                    [screenshot]
   Resolution: ____
```

Send a short Karbon comment (not just a status change) to the next owner: client ID, tax year, return type, and that
the points are ready.

---

## Appendix E - AI-specific review risks (checklist)

* Values with no source link, or a source link to the wrong document or page.
* Values carried from the PY return as if they were CY (stale carryovers, PY 1099 amounts).
* Wrong law year (PY amounts, or 2026 rules applied early).
* Silent defaults: a field left blank that the software treats as zero or "no" (basis, personal-use days, residency
  dates, IP PIN, dependent care provider info).
* Over-confident narrative in the AI Prep Memo not backed by the return (the memo says "PTET removed from Schedule A";
  check that it actually is).
* Instructions embedded in client documents being treated as client instructions.
* Invented citations in research drafts.
* PII handling outside approved systems (see the firm's WISP and AI Acceptable Use Policy, kept separately).

---

## Appendix F - Folder structure mapping

| Pre-AI folder | AI-native location (proposed - confirm the StanfordTax vs Karbon split) |
|---|---|
| `<ClientID>/` | Karbon client record (Client ID in the client name or a custom field) + StanfordTax client |
| `PERM/` | StanfordTax permanent documents + Karbon client notes (residency, agreements, basis records, rollover notes) |
| `<TY>/PBC/` | StanfordTax tax-year documents (as received; Filed works from this set) |
| `<TY>/` main (workpapers, accountant copy) | StanfordTax workpaper binder + reviewer calc workpapers; reviewed return PDF |
| `<TY>/Deliverables/` | Client copy, signed 8879s, acknowledgements, vouchers (StanfordTax delivery + Karbon) |
| `<TY>/PROJ/`, `CONS/`, `NOTICE/` | Separate Karbon work items (projection, consulting, notice) with their own documents; never mixed into the 1040 binder |

---

## Appendix G - Tool features assumed (confirm before adoption)

These are assumptions this mock-up depends on. Each needs to be confirmed against the current release and the firm's
licenses; the procedure should be updated where a feature works differently.

* **Karbon:** custom work statuses, work templates with sections and checklist tasks, custom fields (risk tier), task
  assignees, timesheets with time codes, WIP and invoicing, client notes/tags usable for rollover notes, integration
  with StanfordTax.
* **StanfordTax:** dynamic questionnaire built from PY return data; document request and upload portal; engagement
  letter e-signature; Form 8879 e-signature with KBA; compiled, bookmarked PDF workpaper binder that the reviewer can
  annotate; marking an opt-out ("Blank Organizer").
* **Filed:** document classification and splitting; extraction with per-field confidence; source-to-field highlight;
  duplicate detection; push to ProConnect; reviewer status/comments per field; behavior when a field edited in
  ProConnect is re-pushed (Section 7, R3 step 6).
* **ProConnect:** PY comparison report; diagnostics categories; override behavior and e-file effect per field;
  return locking or status; K-1 basis limitation and Form 7203 inputs; state/local return support (including city
  returns); unsupported forms (e.g., 3520, 8865); e-file of extensions; acknowledgement tracking; PDF attachments.

---

## Appendix H - Corrections and gaps carried over from the pre-AI procedure

The AI preparer will be instructed from the firm's procedures, so errors in them become AI errors. Proposed fixes
(for the signer to confirm):

| Pre-AI text | Issue | Proposed correction |
|---|---|---|
| "In the event that a spouse is deceased, ... the surviving spouse be treated as a qualifying widower subject to the more generous MFJ brackets." | For the year of death the survivor files **MFJ** (if not remarried). Qualifying surviving spouse status applies only for the two following years and requires a dependent child. | Reword as in Section 8.2. |
| "Roth IRAs require taxes to be withheld at the time of contribution, making distributions tax free." | Roth contributions are made with after-tax dollars; there is no withholding on contributions. Qualified distributions are tax-free. | "Roth contributions are not deductible; qualified Roth distributions are tax-free." |
| "1099-E: cancellation of debt" (Glossary) | Cancellation of debt is **1099-C**; 1099-E is student loan interest. | Fix glossary. |
| "IRM: Internal Revenue Memorandum" (Glossary) | IRM is the **Internal Revenue Manual**. | Fix glossary. |
| "Sign-off ... is done in blue at the preparer level." (Review - General Review Notes) | Blue is the **reviewer** color. | "...done in blue at the reviewer level." |
| "For non-cash contributions, we assume a thrift shop value of 3x the cost basis for clothes donated." | Deduction is fair market value (generally thrift-store value), not a multiple of cost, and is capped at FMV. A multiple of cost can overstate the deduction. | Use FMV per a valuation guide; keep support. |
| "Kiddie Tax applies when a child's unearned income exceeds $2,700 (in 2025)" / QBI thresholds "for 2026" | Year-specific amounts are mixed between 2025 and 2026 in the same document. | Move all amounts to a single annual law table, by tax year. |
| "The form [FBAR] should be listed as part of the return title. Ensure the proper exchange rates are used - these can be found on the IRS website." | FBAR uses the Treasury Reporting Rates of Exchange (Bureau of the Fiscal Service), and is filed through BSA E-Filing, not with the 1040. | Update reference. |
| "the funds themselves file a certifying Form 8997 at the fund-level ... There is no Form 8997 filing requirement at the individual level." (QBI) | The fund files **Form 8996**; each investor files **Form 8997** annually while holding a QOF investment. QOF status does not by itself make income QBI. | Reword as in Section 8.9; keep QBI and QOF as separate topics. |
| PTE tax credit "_", Section 361 "_", R&D credits "_", K-2/K-3 "_" | Blanks in the K-1 section. | Proposed fill-ins are in Section 8.9 (PTET, reorganizations, R&D credit, K-2/K-3). Confirm. |
| Extension verification via CCH (ELF report, Return Manager, Client Dashboard) | Tool-specific. | ProConnect e-file status for each 4868 and state extension; Karbon checklist item. |

---

## Change log

| Version | Date | Author | Change |
|---|---|---|---|
| 0.1 | 2026-10-15 | Draft (AI-assisted) for S. Kennedy, CPA | Initial mock-up |
