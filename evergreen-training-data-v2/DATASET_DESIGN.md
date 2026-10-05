# Project Evergreen - Synthetic Client Data Set v2 - Design Spec

This is the design doc for the 25 synthetic 2025 individual clients (24 households + 1 separate child return
required by the kiddie-tax procedure). Each client is built to test specific **manual exceptions called out in the
Project Evergreen procedure doc** (the Scan, Workpapers, Return, Review and SALT sections), plus other real-world
traps that trip up AI preparers.

## Global conventions

* **Tax year 2025**, prepared and filed during 2026 under current law: Rev. Proc. 2024-40 as amended by the
  One Big Beautiful Bill Act (P.L. 119-21, "OBBBA"). Some returns were filed by 04/15/2026; others were extended and
  finished in Aug-Oct 2026 (extended due date 10/15/2026).
* Firm: "Evergreen Tax" (synthetic). Signer S. Kennedy, CPA; reviewers/preparers are fictional staff.
* Client IDs `EVG10xx`. Folder layout follows the procedure's *Folder Structures* section (see `README.md`).
* All names, SSNs (shown truncated `XXX-XX-1234`), EINs (`00-xxxxxxx`), addresses, and account numbers are fictional.
  Every document is stamped "SYNTHETIC TRAINING DATA".
* The answer key is produced by `generator/tax2025.py` so arithmetic is internally consistent. Judgment calls
  (what is taxable, basis fixes, limits) are made explicitly in each `generator/clients/cNN_*.py` script, with
  comments.
* State returns are shown at summary level (tax base, rate, credits, withholding, refund or balance due) for
  flat-rate states (IL 4.95%, MI 4.25% + Detroit, PA 3.07%, NC 4.25%). No-income-tax states: TX, FL, NV, TN, WA
  (WA capital gains excise noted where relevant).

## Key 2025 figures used (beyond the engine's constants)
| Item | 2025 |
|---|---|
| Standard deduction (OBBBA) | S/MFS $15,750, MFJ/QSS $31,500, HOH $23,625; +$2,000 (S/HOH) / +$1,600 (married) per 65+/blind |
| Senior deduction (new) | $6,000 per person 65+ by 12/31/2025; less 6% of MAGI over $75k ($150k MFJ); MFS not allowed |
| No tax on tips / overtime | tips up to $25,000; OT premium up to $12,500 ($25,000 MFJ); phase-out $100 per $1,000 over $150k ($300k MFJ); MFS not allowed |
| Car-loan interest | up to $10,000, new vehicle, final assembly in US, bought after 2024; phase-out $200/$1,000 over $100k ($200k MFJ) |
| SALT cap | $40,000 ($20,000 MFS), reduced by 30% of MAGI over $500,000 ($250k MFS), floor $10,000 |
| CTC / ACTC / ODC | $2,200 / $1,700 / $500 |
| Kiddie tax | unearned income > $2,700; Form 8814 election if child income < $13,500 and only interest/dividends |
| QBI threshold | $197,300 / $394,600 MFJ; phase-in $50k / $100k |
| Dependent care FSA exclusion | $5,000 (rises to $7,500 in 2026) |
| Gambling losses | 100% of winnings in 2025 (OBBBA 90% limit starts **2026**) |
| Charitable | Non-itemizer deduction and 0.5% floor start **2026** - not for 2025 |
| Personal casualty | Federally declared disasters only (state-declared expansion starts 2026) |
| 1099-K threshold | $20,000 and 200 transactions (OBBBA reinstated) |
| 1099-DA | 2025: gross proceeds only; basis reporting begins for 2026 |
| Clean vehicle credit (30D/25E) | Terminated for vehicles acquired after 09/30/2025 |
| 25D residential clean energy / 25C | Expenditures through 12/31/2025 only (30%; 25C $1,200/$2,000 heat pump caps) |
| IRA / 401(k) / HSA | $7,000 (+$1,000 50+) / $23,500 / $4,300 self, $8,550 family (+$1,000 55+) |
| QCD limit | $108,000 |
| SS wage base | $176,100 |
| Mileage | 70 cents |
| FX (IRS yearly average 2025) | CAD 1.398; INR 87.147 |
| PTC | Enhanced (no 400% FPL cliff) through 2025; 2024 FPL $15,060 (1 person); applicable % 8.5% at 400%+; no repayment cap at 400%+ |

## Client roster and gotcha map

| ID | Client | Status / State | Profile | Procedure-driven gotchas | Other traps |
|---|---|---|---|---|---|
| EVG1001 | Bell | MFJ / TX | Hourly W-2 family, 3 kids | Duplicate W-2 (Scan); blank organizer line with PY interest (Return Prep Notes) | OT premium only; car-loan interest new vs used; newborn; FSA vs 2441; HSA code W |
| EVG1002 | Raman | HOH / IL | Single mom, low income, EITC | Filing status Single -> HOH (Review/Filing Status); dependent claimed by other parent -> paper file (Paper Filing) | 1099-K personal items at a loss; 1099-G refund not taxable (std ded PY); LLC credit; IL US-Treasury subtraction |
| EVG1003 | Okafor | S / NV | Bartender + rideshare | Handwritten tip log & mileage log (Scan: handwritten); Sch C records | Allocated tips (W-2 box 8) & unreported tips Form 4137; no tax on tips (W-2 + Sch C tips); rideshare 1099-K vs gross fares |
| EVG1004 | Castellano | MFJ / FL | Retirees 67/64, Canadian spouse | SSA-1099 Medicare premiums to Sch A (Sch A); Canadian NR-4 pension FX + taxable SS (Foreign/1116); FBAR; accrued interest reversal (Sch B); IRA statement not reportable (Client IRAs) | QCD; senior deduction age test; muni interest in provisional income; corrected 1099-R |
| EVG1005 | Walsh | S / MI + Detroit | Tech worker, 2 jobs, moved | Local filing (Detroit part-year) & new state/local requirement (SALT) | Excess SS credit; Additional Medicare not withheld; backdoor Roth pro-rata (8606) |
| EVG1006 | Mendoza | MFJ / TX | Landscaping Sch C | Accrual books -> cash; meals/gifts/club dues/personal; de minimis $2,500; 1099 filing boxes; tax-prep fee proration; SEP max; SE health (Sch C section); AJEs not booked | SE health barred by spouse's employer plan; qualifying relative mother (SS not gross income); educator expense |
| EVG1007 | Rahman | S / IL | Physician, S-corp owner | S-corp distribution > stock basis despite debt basis (K-1 debt/stock trap); PTET (K-1); state refund & tax benefit rule (Sch A) | SSTB QBI phase-out; SALT cap phase-down >$500k; DAF vs GoFundMe; clothing FMV; missed estimate |
| EVG1008 | O'Brien | MFJ / PA | Two rentals + college kid | 1098 for rental treated as personal; personal-use days; capitalize vs repair; de minimis election (Sch E) | Passive loss limit at MAGI > $150k + PY suspended loss carryforward; AOTC phase-out; PA class rules |
| EVG1009 | Jensen | MFJ (year of death) / WA | Widower 72 | Filing status year of death (MFJ, not QSS) (Filing Status); inherited property step-up (Estate) | WA community-property full step-up; §121 $500k within 2 yrs of death; decedent medical §213(c); SSA repaid benefit; WA CG excise check |
| EVG1010 | Kim | MFJ / WA | Tech couple, 2 kids, nanny | Kiddie tax -> separate child client ID (Kid Taxes); Form 8814 election for younger child | RSU sell-to-cover $0 basis; Schedule H nanny (not a 1099 contractor); 1099-Q K-12 tuition |
| EVG1011 | Nguyen | S / TN | Crypto trader | CoinLedger 8949 vs 1099-DA duplication (Sch D); IP PIN (E-file rejects) | 1099-DA no basis; staking income 1099-MISC; self-transfers not sales; no wash sale for crypto; NFT collectible 28%; 1095-A full APTC repayment |
| EVG1012 | Hoffman | MFJ / NC | Retirees, seller-financed land | Installment sale 6252 (Installment Sales); legal agreement + handwritten payment ledger (Scan) | Payment received in Jan 2026 is 2026; interest portion to Sch B; NC Bailey exclusion; senior deduction x2 |
| EVG1013 | Brooks | S / IL | Startup employee | Restricted stock 83(b) filed late (Restricted Stock / Form 15620) | ISO AMT (6251); NSO same-day sale basis; HSA excess corrected by extended due date |
| EVG1014 | Martinez / Hart | MFJ / MI | Newlyweds, freelancer | Married by 12/31 -> MFJ; MFJ vs MFS simulation (Projections); name mismatch e-file reject (E-File Rejects) | 1099-K and 1099-NEC double-count; home office 8829 vs simplified; new business checkbox; unemployment |
| EVG1015 | Iyer | MFJ / WA | Indian-born H-1B family | FBAR; Form 8938; PFIC 8621; Form 3520 foreign gift; FTC 1116 not de minimis (Foreign) | NRE interest taxable in US; INR conversion; nonresident-alien parents not dependents |
| EVG1016 | Doyle | HOH / MI | Separated nurse, 2 kids | Separated is not divorced - but "considered unmarried" -> HOH (Filing Status); divorce/separation agreement (Scan: legal agreements) | Form 8332 release; QDRO distribution 10% exception; alimony under post-2018 instrument not income; OT premium reported separately |
| EVG1017 | Russo | MFJ / IL | High-net-worth investor | Partnership distribution > outside basis; PTP/oil & gas K-1; K-1 state apportionment matrix (SALT); consolidated 1099: market discount, wash sale, accrued interest, UIT/WHFIT, margin interest to 4952/8960 (Sch B/D/NIIT); corrected 1099 duplication | 199A REIT dividends; nondividend distributions; PA nonresident return |
| EVG1018 | Vasquez | S / FL | S-corp owner + trust beneficiary | §311(b) property distribution omitted from K-1; trust termination suspended passive loss (K-1 section) | QBI with W-2 wage data; §1245 character |
| EVG1019 | Fitzgerald | MFJ / NC | Dual income, consultant, new solar | Pre-2017 mortgage $1M limit override; home office 8829 vs Sch A double count (Sch A / Sch C); sales tax on large purchase vs income tax (Sch A) | 25D solar credit + carryforward; EV bought after 09/30/2025 (no 30D); SEP; NC state |
| EVG1020 | Turner | S / TN | Nurse with Airbnb condo | Gambling winnings/losses (Sch A - OBBBA timing); disaster loss must be federally declared (Sch A); Sch E rental records (Scan) | Short-term rental (avg stay <= 7 days) not a "rental activity" - material participation; 1099-K gross vs net |
| EVG1021 | Kim, Ethan | S (dependent) / WA | 16-year-old with UTMA account | Separate client ID and 1040 project for child (Kid Taxes); Form 8615 using parents' rate | Can't use 8814 (has capital gains); dependent standard deduction; no senior/OBBBA items |
| EVG1022 | Whitfield | MFJ / PA (+ MA nonresident) | Retiring mobile executive | Multi-state W-2 workdays, NJ reciprocity and IL 30-day rule, MA nonresident + PA resident credit; capital loss carryover from prior preparer (new client) | NUA lump-sum distribution; cross-account wash sale into spouse's IRA; bond premium and accrued interest |
| EVG1023 | Delgado | MFJ / NC | Partnership investor + designer | K-1 basis, at-risk (Form 6198), passive (new-client Regular/AMT carryovers), AMT line 2n, 704(c)(1)(B) mixing bowl + 752(b) | §1033 fire-loss deferral and deadline; NC bonus-depreciation addback; Form 8865 (not supported in ProConnect) + Form 8938 |
| EVG1024 | Abernathy | S / FL | Founder whose startup failed; heir | Insolvency (Form 982) + attribute reduction; §1244 ordinary loss; capital loss carryover | §691(c) IRD deduction on inherited IRA; foreign trust distribution (Form 3520 - not supported in ProConnect) with actual-method statement |
| EVG1025 | Brennan-Ochoa | MFJ / TX | CFC owner; merger | Rare-event specialist items: GILTI with §962 election (ProConnect manual entry), FBAR signature authority | Reorganization boot §356; §331 liquidation; §1259 constructive sale; Form 1042-S issued to a US citizen (paper filing) |

## What each client folder contains
1. `PERM/Client_Profile.md` - static data (DOBs, contact, residency history, special notes) and `2024_Form_1040_Return_Summary.pdf`
   (prior-year key lines and carryovers - needed to catch "blank organizer line" and carryforward gotchas).
2. `2025/PBC/` - everything the client sent, in the order received: organizer, W-2s, 1099s, K-1s, statements, spreadsheets,
   handwritten notes (scanned image PDFs), emails. Includes deliberately messy items: duplicates, corrected forms, photos,
   irrelevant documents (e.g. IRA statements), and follow-up documents received after open-item requests.
3. `2025/<ID>_2025_PBC_Receipt_Log.md` - neutral Admin intake log.
4. `2025/Deliverables/<ID>_2025_Form_1040_Client_Copy.pdf` - the final, signed-off return (form-by-form, line-by-line) plus
   supporting statements and state summaries.
5. `2025/<ID>_2025_Preparer_Notes.md` - plain-English notes on the completed return (what was done and why, open items, routing).
6. `2025/<ID>_2025_Review_Points.md` - the reviewer's points on the first draft (the mistakes a first-pass preparer or AI made)
   and the resolution - in the firm's review-point format.
7. `2025/<ID>_2025_Answer_Key.json` - machine-readable expected return (every form/line) and the gotcha rubric
   (`trap`, `correct_treatment`, `impact`, `affected_lines`, `difficulty`) for the eval suite.

## v2 software-exception layer
Every client also has a software-exception pack (see README). The mapping is to the 22 calculation tabs of the firm's
*CCH Axcess 1040 Exception Remediation Workbook*, plus "log-only" items (Diagnostics Log, tab 2) and Intuit ProConnect-only
items. **Every tab 3-24 is exercised by at least one client** (see `SOFTWARE_EXCEPTION_MATRIX.md`).

ProConnect behaviors are stated only where an Intuit help article or community answer documents them, and that reference
is recorded in each item's `proconnect_reference`. These cover Form 3520 and Form 8865 not being supported, Form 8615
with no Family Link, Form 7203 stock-basis requirements, the manual §962 election, the Form 8949 summary attachment
(diagnostic 10322), Form 1042-S withholding not being e-fileable on a 1040, new-client Form 8582 carryovers (Regular vs AMT),
and the 1099-C insolvency worksheet. Every other screen path is marked "verify in current release".
"Highest tier" ProConnect (the Advanced/Elite bundles) has the same form coverage as the other tiers - tiers differ only in
return counts and users. CCH Axcess diagnostic numbers are never invented: they vary by release, so the log records the
message gist or "None - silent".
