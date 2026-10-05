# EVG1024 - Margaret "Peggy" Abernathy - 2025 Software Exceptions (CCH Axcess & Intuit ProConnect)

*Synthetic training data - Project Evergreen v2. Companion workbook: `EVG1024_2025_Software_Exception_Workbook.xlsx` (firm's corrected CCH Axcess Exception Workbook, filled in).*

Peggy's return is built almost entirely from documents that neither package can interpret on its own: a 1099-C that is excluded
under the insolvency exception, the attribute reduction that exclusion forces on next year's capital loss carryover, founder stock
that is part IRC 1244 ordinary loss and part worthless-stock capital loss (no 1099-B), an estate-tax deduction (IRC 691(c)) that
depends on an attorney's letter, and a distribution from a foreign non-grantor trust that must be split by character from a
Foreign Nongrantor Trust Beneficiary Statement and reported on a Form 3520 that is filed on paper. Most of these are **silent** -
the software calculates a facially valid return from the 1099s. Same tax answer in both packages; only the mechanics differ.

| ID | Workbook tab | Exception | Axcess diagnostic? | Override amount | E-file impact |
|---|---|---|---|---:|---|
| EVG1024-SX1 | 20. Insolvency (Form 982) | 1099-C $38,000 - insolvency exclusion (Form 982) must be built and elected manually | **silent** (no diagnostic) | 38,000 | None (Form 982 is e-filed with the 1040) |
| EVG1024-SX2 | 10. Capital Loss Carryover | IRC 108(b) attribute reduction - 2026 capital loss carryover must be overridden (67,000 -> 29,000) | **silent** (no diagnostic) | 29,000 | None |
| EVG1024-SX3 | 22. Reorg, Liquidation, 1244 | Brightline founder stock - IRC 1244 ordinary loss + worthless-stock capital loss (no 1099-B) | **silent** (no diagnostic) | -50,000 | None |
| EVG1024-SX4 | 18. NUA & IRD Deduction | IRC 691(c) deduction on inherited IRA distribution - not derived from the 1099-R | **silent** (no diagnostic) | 60,000 | None |
| EVG1024-SX5 | 24. Rare-Event Log | Foreign non-grantor trust distribution - actual method character split from the FNTBS | **silent** (no diagnostic) | 85,000 | None for the 1040 (Form 3520 - see SX6) |
| EVG1024-SX6 | ProConnect-only | Form 3520 Part III - not supported in ProConnect; separate paper filing | **silent** (no diagnostic) | 120,000 | 1040 e-filed; Form 3520 paper-filed separately (IRS Ogden) |
| EVG1024-SX7 | 2. Diagnostics Log | Schedule B Part III line 8 and Form 8938 - foreign trust interest (excepted asset) | **silent** (no diagnostic) | 120,000 | None |

## EVG1024-SX1 - 1099-C $38,000 - insolvency exclusion (Form 982) must be built and elected manually

*Workbook tab:* 20. Insolvency (Form 982)  |  *Category:* Other  |  *Manual calc:* Yes  |  *Amount:* $38,000  |  *Procedure doc:* Return - Form 982 (insolvency)

- **CCH Axcess by default:** The 1099-C input flows the $38,000 to Schedule 1 line 8c as cancellation-of-debt income. Axcess has no balance sheet and cannot test insolvency, so the return simply taxes the COD (about $10,191 of extra tax including NIIT).
- **Axcess diagnostic:** None - silent
- **Axcess fix:** Workbook tab 20: assets 377,000 / liabilities 425,000 immediately before the 03/18/2025 discharge (incl. the 401(k); excl. the July inheritance) -> insolvency 48,000 -> excludable 38,000. Then Income > Cancellation of debt / Form 982 input: check 'Discharge of indebtedness to the extent insolvent' (line 1b) and enter 38,000 as the excluded amount; confirm Schedule 1 line 8c drops to $0 (verify field path in current release).
- **ProConnect by default:** Same - the 1099-C amount is taxable unless the insolvency section is completed.
- **ProConnect fix:** Income > 1099-C > Canceled Debt Worksheet: complete the Insolvency section (total liabilities 425,000 and total assets 377,000 immediately before the cancellation); the excluded $38,000 flows to Form 982 line 1b/line 2. Attribute reduction still requires manual review (see SX2). *(ref: Intuit help: 'Entering a Form 1099-C with insolvency (Form 982)')*
- **E-file impact:** None (Form 982 is e-filed with the 1040)
- **Return lines affected:** 8 (Sch 1 line 8c), Form 982 lines 1b, 2
- **Notes:** Client's own worksheet used 12/31/2025 balances, counted the inherited IRA and omitted the 401(k) - all three wrong.

## EVG1024-SX2 - IRC 108(b) attribute reduction - 2026 capital loss carryover must be overridden (67,000 -> 29,000)

*Workbook tab:* 10. Capital Loss Carryover  |  *Category:* Capital Loss  |  *Manual calc:* Yes  |  *Amount:* $29,000  |  *Procedure doc:* Return - Form 982 Part II (attribute reduction)

- **CCH Axcess by default:** Axcess computes the 2025 Capital Loss Carryover Worksheet (LT 67,000) and proformas it to 2026. Completing Form 982 Part II does not reduce the carryover that rolls forward - the 2026 return would deduct losses that were eliminated by the excluded COD.
- **Axcess diagnostic:** None - silent
- **Axcess fix:** Form 982 Part II line 9 (net capital loss / carryovers; verify line number in current revision) = 38,000. Workbook tab 10 documents the pre-reduction carryover (ST 0 / LT 67,000); attach the reduction statement. In the 2026 proforma: Income > Capital Gains and Losses > Carryovers: override LT capital loss carryover to 29,000 (ST 0).
- **ProConnect by default:** Same - ProConnect carries the unreduced 67,000 forward; the 982 attribute-reduction lines are informational for the carryover.
- **ProConnect fix:** Form 982 Part II line 9 = 38,000 (Canceled Debt / 982 inputs); in the 2026 return override the prior-year long-term capital loss carryover to 29,000 on the Schedule D carryover input (screen/field per current release - verify). *(ref: Intuit help: 'Entering a Form 1099-C with insolvency (Form 982)' - attribute reduction requires manual review)*
- **E-file impact:** None
- **Return lines affected:** Form 982 line 9, 2026 Schedule D lines 6/14
- **Notes:** Reduction is made after the 2025 tax is determined (IRC 108(b)(4)(A)); the 2025 $3,000 deduction is unaffected. Tab 10 inputs here are the 2025 (year-of-discharge) Schedule D figures, used to compute the 2025->2026 carryover.

## EVG1024-SX3 - Brightline founder stock - IRC 1244 ordinary loss + worthless-stock capital loss (no 1099-B)

*Workbook tab:* 22. Reorg, Liquidation, 1244  |  *Category:* Capital Loss  |  *Manual calc:* Yes  |  *Amount:* $-50,000  |  *Procedure doc:* Schedule D

- **CCH Axcess by default:** There is no 1099-B for worthless stock. If the preparer keys the $150,000 on the Capital Gains worksheet with default 'Capital' character, Axcess reports a $150,000 LT capital loss and allows $3,000 - the $50,000 ordinary loss is lost. Axcess cannot know the stock qualifies under IRC 1244.
- **Axcess diagnostic:** None - silent
- **Axcess fix:** Workbook tab 22 (two rows). Capital Gains and Losses worksheet: line 1 - Brightline Analytics common, acquired 06/12/2019, sold 12/31/2025 (IRC 165(g) deemed date), proceeds 0, cost 50,000, category changed from 'Capital' to 'Section 1244 Ordinary Loss' -> Form 4797 Part II line 10 (Schedule 1 line 4: -50,000). Line 2 - same stock, cost 100,000, 'Worthless', long-term, Form 8949 box F.
- **ProConnect by default:** Same - a disposition entered without the section 1244 indicator is a capital loss.
- **ProConnect fix:** Dispositions (Schedule D/4797): enter two lines - $50,000 marked as section 1244 / ordinary (flows to Form 4797 Part II) and $100,000 as a long-term worthless-security capital loss with date sold 12/31/2025, box F (screen/field per current release - verify).
- **E-file impact:** None
- **Return lines affected:** Sch 1 line 4, Form 4797 line 10, Form 8949 box F, 7
- **Notes:** 1244 limit $50,000 single; original issuance for cash; capitalization $750,000 <= $1M; active receipts. Worthless in 2025 (plan of dissolution, no stockholder distributions).

## EVG1024-SX4 - IRC 691(c) deduction on inherited IRA distribution - not derived from the 1099-R

*Workbook tab:* 18. NUA & IRD Deduction  |  *Category:* Other  |  *Manual calc:* Yes  |  *Amount:* $60,000  |  *Procedure doc:* Estate Implications

- **CCH Axcess by default:** The 1099-R (code 4) flows $150,000 to line 4b. Axcess computes no IRC 691(c) deduction - it has no estate-tax data. The firm workbook's ORIGINAL tab 18 formula (IRA value - estate tax = 2,400,000 - 1,764,000 = 636,000) would have produced a meaningless figure.
- **Axcess diagnostic:** None - silent
- **Axcess fix:** Workbook tab 18 (IRD row - column E typed over per the Corrections Log): (1,764,000 - 804,000) x 150,000 / 2,400,000 = 60,000. Enter on Itemized Deductions > Miscellaneous Deductions > Income in Respect of a Decedent (Schedule A line 16, no 2% floor); attach the computation statement.
- **ProConnect by default:** Same - the 1099-R entry produces no 691(c) deduction.
- **ProConnect fix:** Itemized Deductions > Other itemized deductions: 'Federal estate tax on income in respect of a decedent' = 60,000 (screen/field per current release - verify); statement attached.
- **E-file impact:** None
- **Return lines affected:** 12e, Schedule A line 16
- **Notes:** Federal estate tax only - Connecticut estate tax excluded. Remaining 691(c) pool for Peggy's future withdrawals 420,000.

## EVG1024-SX5 - Foreign non-grantor trust distribution - actual method character split from the FNTBS

*Workbook tab:* 24. Rare-Event Log  |  *Category:* Other  |  *Manual calc:* Yes  |  *Amount:* $85,000  |  *Procedure doc:* Foreign Trusts

- **CCH Axcess by default:** Axcess has no input that reads a Foreign Nongrantor Trust Beneficiary Statement. Keyed as one $120,000 'other income' amount it is all ordinary (and the $35,000 of corpus is taxed); left out because the client calls it an inheritance, $85,000 of income is omitted. The software also cannot know undistributed net income is $0.
- **Axcess diagnostic:** None - silent
- **Axcess fix:** Workbook tab 24 (rare-event log, FNTBS as the workpaper). Enter by character: Interest input - 'Hale Family Settlement (foreign trust)' 15,000; Dividends input - 40,000 ordinary / 40,000 qualified; Capital Gains - Schedule D line 12 (estates and trusts) 30,000 LT. Corpus 35,000 not entered. No accumulation distribution -> no Form 4970 / Form 3520 interest-charge override.
- **ProConnect by default:** Same - ProConnect has no FNTBS import; amounts are taxed as entered.
- **ProConnect fix:** Enter the three income items on the Interest, Dividends and Dispositions/Schedule D screens with the trust as payer; do not enter the 35,000 corpus (screen/field per current release - verify).
- **E-file impact:** None for the 1040 (Form 3520 - see SX6)
- **Return lines affected:** 2b, 3a, 3b, 7, Sch B Part III line 8
- **Notes:** Actual method allowed: trustee appointed a U.S. agent and issued the FNTBS. Default method / throwback would be wrong.

## EVG1024-SX6 - Form 3520 Part III - not supported in ProConnect; separate paper filing

*Workbook tab:* ProConnect-only  |  *Category:* E-file Disqualifying  |  *Manual calc:* No  |  *Amount:* $120,000  |  *Procedure doc:* Foreign Trusts / Paper Filing Returns

- **CCH Axcess by default:** Form 3520 is not part of the 1040 e-file in any package. Per the workbook's tab 24 guidance Axcess has a Form 3520 / Miscellaneous Taxes input; whether the current release produces a complete Part III is not relied on - firm practice: prepare Form 3520 separately and mail it.
- **Axcess diagnostic:** None - silent
- **Axcess fix:** Prepare Form 3520 Part III (lines 24-33, FNTBS attached, actual method) outside the 1040 e-file; mail to IRS Ogden by 10/15/2026 (extended due date), certified. Log on workbook tab 24.
- **ProConnect by default:** ProConnect does not generate Form 3520.
- **ProConnect fix:** Prepare Form 3520 outside ProConnect (IRS fillable PDF) and mail it separately to the IRS (it cannot be e-filed). In ProConnect answer the Schedule B Part III foreign-trust question 'Yes' so line 8 prints. *(ref: Intuit Accountants Community: 'Does ProConnect generate Form 3520...')*
- **E-file impact:** 1040 e-filed; Form 3520 paper-filed separately (IRS Ogden)
- **Return lines affected:** Form 3520, Sch B line 8
- **Notes:** Penalty for failure to file: greater of $10,000 or 35% of the distribution ($42,000).

## EVG1024-SX7 - Schedule B Part III line 8 and Form 8938 - foreign trust interest (excepted asset)

*Workbook tab:* 2. Diagnostics Log  |  *Category:* Other  |  *Manual calc:* No  |  *Amount:* $120,000  |  *Procedure doc:* Foreign Trusts

- **CCH Axcess by default:** Schedule B line 8 (distribution from a foreign trust) is answered from the general foreign-trust question - it defaults to No. Form 8938 is only produced from 8938 inputs; nothing tells the software that a beneficial interest in a foreign trust (value = distributions received $120,000) crosses the $75,000 any-time threshold.
- **Axcess diagnostic:** None - silent
- **Axcess fix:** General / Foreign accounts and trusts input: 'received a distribution from a foreign trust' = Yes. Form 8938 input: Part IV excepted specified foreign financial assets - number of Forms 3520 = 1 (verify field path in current release).
- **ProConnect by default:** Same - question-driven; Form 8938 only if 8938 inputs are completed.
- **ProConnect fix:** Schedule B foreign trust question = Yes; Foreign Reporting > Form 8938: list the excepted asset (Form 3520 count 1) (screen/field per current release - verify).
- **E-file impact:** None
- **Return lines affected:** Sch B line 8, Form 8938
- **Notes:** No FBAR - no foreign financial account; discretionary beneficiary does not report the trust's accounts.

