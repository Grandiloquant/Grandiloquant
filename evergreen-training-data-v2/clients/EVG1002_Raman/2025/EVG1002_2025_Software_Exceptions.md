# EVG1002 - Priya Raman - 2025 Software Exceptions (CCH Axcess & Intuit ProConnect)

*Synthetic training data - Project Evergreen v2. Companion workbook: `EVG1002_2025_Software_Exception_Workbook.xlsx` (firm's corrected CCH Axcess Exception Workbook, filled in).*

Low-income HOH return with EIC/CTC. No calculation tab applies; the exceptions are a filing-status carry-forward, a 1099-K that
the input defaults treat as business income, a state refund the software cannot test without prior-year data, and an e-file
reject that no override can clear (paper filing is the only path). The software's credit ordering (Form 8880 before the CTC on
Credit Limit Worksheet A) and the EIC calculation are correct once the inputs are right - they are not exceptions.

| ID | Workbook tab | Exception | Axcess diagnostic? | Override amount | E-file impact |
|---|---|---|---|---:|---|
| EVG1002-SX1 | 2. Diagnostics Log | Filing status carried forward as Single (organizer + self-prepared PY returns) | **silent** (no diagnostic) | 23,625 | See SX4 - the dependent claim triggers the IND-507-01 reject |
| EVG1002-SX2 | 2. Diagnostics Log | PayPal 1099-K for personal items sold at a loss | **silent** (no diagnostic) | 6,812 | None |
| EVG1002-SX3 | 2. Diagnostics Log | 1099-G IL refund $212 - prior year used the standard deduction | yes | 0 | None |
| EVG1002-SX4 | 2. Diagnostics Log | IND-507-01 reject - dependent's SSN already used by the father | yes | 5,141 | Federal must be paper filed |
| EVG1002-SX5 | 2. Diagnostics Log | IL Schedule M subtraction for TreasuryDirect interest | **silent** (no diagnostic) | 310 | None |

## EVG1002-SX1 - Filing status carried forward as Single (organizer + self-prepared PY returns)

*Workbook tab:* 2. Diagnostics Log  |  *Category:* Other  |  *Manual calc:* No  |  *Amount:* $23,625  |  *Procedure doc:* Review - Filing Status (Single vs HOH)

- **CCH Axcess by default:** New Axcess return built from the organizer and her self-prepared 2023/2024 returns: Single, no dependent. Axcess calculates a valid Single return (standard deduction $15,750, no EIC/CTC) - a $361 balance due. Nothing in the software tests head-of-household eligibility.
- **Axcess diagnostic:** None - silent
- **Axcess fix:** General > Basic Data: filing status Head of household; Dependents: add Arjun (son, 12 months, qualifying child - lived with Priya ~315 nights; no Form 8332). Complete the Form 8867 due-diligence inputs (EIC/CTC/HOH). Standard deduction $23,625; refund $5,141.
- **ProConnect by default:** Same - filing status and dependents are whatever is entered.
- **ProConnect fix:** General > Filing Status: Head of household; Dependents screen: Arjun with EIC/CTC qualifying-child answers; Form 8867 due-diligence questions (screen names per current release - verify). *(ref: Screen name per current release - verify)*
- **E-file impact:** See SX4 - the dependent claim triggers the IND-507-01 reject
- **Return lines affected:** Filing status, 12e, 16, 19, 27a, 28
- **Notes:** Refund $5,141 vs balance due $361 on the Single/no-dependent draft.

## EVG1002-SX2 - PayPal 1099-K for personal items sold at a loss

*Workbook tab:* 2. Diagnostics Log  |  *Category:* Other  |  *Manual calc:* No  |  *Amount:* $6,812  |  *Procedure doc:* Scan - Unstructured PBC / 1099-K

- **CCH Axcess by default:** The AutoFlowed 1099-K landed as business income (Schedule 1 line 3 / Schedule C gross receipts) and the return computed SE tax and cut the EIC. Axcess cannot know the items were personal-use property sold below cost.
- **Axcess diagnostic:** None - silent
- **Axcess fix:** Remove the 1099-K from the business-income input. Income > Other income: Schedule 1 line 8z 'Form 1099-K personal items sold at a loss' $6,812; Adjustments > other adjustments line 24z, same description, $6,812 (verify field path in current release). AGI unaffected ($36,463); no Schedule C / SE.
- **ProConnect by default:** Same risk if the 1099-K is entered on a business screen.
- **ProConnect fix:** Enter $6,812 as other income (Sch 1 line 8z) and the same amount as an other adjustment (line 24z) with the IRS description (screen/field per current release - verify). Keep the PayPal CSV (WP 9) as support. *(ref: Screen/field per current release - verify)*
- **E-file impact:** None
- **Return lines affected:** Sch 1 8z, Sch 1 24z, 11, 27a
- **Notes:** If gains existed they would go on Form 8949; losses on personal-use property are not deductible.

## EVG1002-SX3 - 1099-G IL refund $212 - prior year used the standard deduction

*Workbook tab:* 2. Diagnostics Log  |  *Category:* Other  |  *Manual calc:* No  |  *Amount:* $0  |  *Procedure doc:* Return - Schedule A (state refunds of taxes previously itemized)

- **CCH Axcess by default:** With no Axcess prior-year return (new client, self-prepared 2024), the state-refund worksheet has no 2024 itemized data and the AutoFlowed 1099-G is included on Schedule 1 line 1 in full.
- **Axcess diagnostic:** Informational: state and local refund worksheet requires prior-year itemized deduction information
- **Axcess fix:** Income > State and local refund worksheet: mark 2024 as standard deduction (did not itemize) - taxable refund $0. Alternatively remove the 1099-G input and keep it in the binder as 'not taxable - tax benefit rule'.
- **ProConnect by default:** Same - the taxable-refund worksheet needs prior-year itemized information; otherwise the full refund is taxable.
- **ProConnect fix:** Income > State and local tax refunds: indicate the prior year did not itemize so the taxable amount is $0 (field per current release - verify). *(ref: Field per current release - verify)*
- **E-file impact:** None
- **Return lines affected:** Sch 1 line 1, 8

## EVG1002-SX4 - IND-507-01 reject - dependent's SSN already used by the father

*Workbook tab:* 2. Diagnostics Log  |  *Category:* E-file Disqualifying  |  *Manual calc:* No  |  *Amount:* $5,141  |  *Procedure doc:* Post-Submission Exceptions - E-File Rejects / Paper Filing Returns

- **CCH Axcess by default:** Axcess transmits; IRS rejects (IND-507-01, dependent SSN used on another return). No input or override can clear an IRS-side duplicate. The tempting 'fix' - removing Arjun so the e-file goes through - gives up HOH, EIC, CTC and is wrong (custodial parent, no Form 8332).
- **Axcess diagnostic:** E-file reject (IRS business rule IND-507-01) - not a calculation diagnostic
- **Axcess fix:** Keep the return unchanged. Turn off federal e-file for this return (e-file options per current release - verify), print the government copy, client wet-signs, mail certified (done 03/04/2026). IL-1040 sent as a state-only (unlinked) e-file. Reject, school letter and lease kept in the WP.
- **ProConnect by default:** Same IRS reject; ProConnect cannot override it either.
- **ProConnect fix:** Mark the federal return for paper filing (do not e-file federal), print the filing copy and mail; transmit the IL return separately if state-only e-file is supported for the state (per current release - verify). *(ref: E-file settings per current release - verify)*
- **E-file impact:** Federal must be paper filed
- **Return lines affected:** Filing method
- **Notes:** IRS will resolve the duplicate claim with the father (expect CP87A to him / possible residency audit for Priya).

## EVG1002-SX5 - IL Schedule M subtraction for TreasuryDirect interest

*Workbook tab:* 2. Diagnostics Log  |  *Category:* State Allocation  |  *Manual calc:* No  |  *Amount:* $310  |  *Procedure doc:* Return - Schedule B (federal obligations exempt at state level)

- **CCH Axcess by default:** If the TreasuryDirect 1099-INT is keyed or AutoFlowed as box 1 (ordinary taxable interest) instead of box 3 (U.S. obligations), federal tax is identical but the IL return shows no Schedule M subtraction (the first draft had none - review point 7).
- **Axcess diagnostic:** None - silent
- **Axcess fix:** Interest income input: move $310.46 to the U.S. savings bond / Treasury obligation (box 3) column so the IL subtraction generates on Schedule M ($310). IL base income $36,153.
- **ProConnect by default:** Same - the state subtraction keys off the box 3 / U.S. obligation designation.
- **ProConnect fix:** Interest Income screen: enter the TreasuryDirect amount as U.S. bond/Treasury interest (box 3) so the IL subtraction flows (field per current release - verify). *(ref: Field per current release - verify)*
- **E-file impact:** None
- **Return lines affected:** 2b, IL-1040 Schedule M
- **Notes:** A REPRINT copy of the same 1099-INT was also in the PBC - count once.

