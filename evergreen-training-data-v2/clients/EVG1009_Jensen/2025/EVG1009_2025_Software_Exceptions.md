# EVG1009 - Harold Jensen (and Eleanor Jensen, deceased) - 2025 Software Exceptions (CCH Axcess & Intuit ProConnect)

*Synthetic training data - Project Evergreen v2. Companion workbook: `EVG1009_2025_Software_Exception_Workbook.xlsx` (firm's corrected CCH Axcess Exception Workbook, filled in).*

Year-of-death joint return in a community property state. The two biggest exceptions are basis items the software cannot
know: Schwab's 1099-B still shows original cost (and no basis on noncovered lots) although BOTH community halves were stepped up
to date-of-death value, and the home sale needs the DOD appraisal plus a code-H exclusion. Both are one-off, fact-intensive events,
logged on tab 24 with the DOD valuation and appraisal as the supporting workpapers. The rest are AutoFlow / setup traps.

| ID | Workbook tab | Exception | Axcess diagnostic? | Override amount | E-file impact |
|---|---|---|---|---:|---|
| EVG1009-SX1 | 24. Rare-Event Log | Inherited community-property securities - 1099-B shows original cost; noncovered lots no basis | **silent** (no diagnostic) | 11,387 | None |
| EVG1009-SX2 | 24. Rare-Event Log | Sale of the marital home (1099-S) - DOD appraisal basis and sec. 121 exclusion, code H | **silent** (no diagnostic) | -18,227 | None |
| EVG1009-SX3 | 2. Diagnostics Log | Vanguard spousal 'transfer out' AutoFlowed as an IRA distribution | **silent** (no diagnostic) | 0 | None |
| EVG1009-SX4 | 2. Diagnostics Log | Year-of-death filing status: MFJ, not 'qualifying widower' (organizer + procedure wording) | yes | 0 | None (MFJ with deceased spouse e-files normally) |
| EVG1009-SX5 | 2. Diagnostics Log | Schedule 1-A senior deduction for the deceased spouse | **silent** (no diagnostic) | 12,000 | None |

## EVG1009-SX1 - Inherited community-property securities - 1099-B shows original cost; noncovered lots no basis

*Workbook tab:* 24. Rare-Event Log  |  *Category:* Capital Loss  |  *Manual calc:* Yes  |  *Amount:* $11,387  |  *Procedure doc:* Estate Implications - step-up in basis (community property)

- **CCH Axcess by default:** AutoFlow brought in the Schwab 1099-B as reported: MSFT covered lot basis $13,500 (original cost), VFIAX and JNJ noncovered with no basis -> Schedule D gain $347,120 (or $179,254 if only Eleanor's half were stepped up). Axcess has no way to know the account was community property or that a death occurred.
- **Axcess diagnostic:** None - silent
- **Axcess fix:** Gains and Losses > Form 8949: MSFT (box D) keep 1099-B basis $13,500, adjustment code B, column (g) -142,605 -> basis $156,105; VFIAX and JNJ (box E) basis = DOD FMV $222,048 and $31,080; date acquired 'INHERITED' (long-term, sec. 1223(9)). Total DOD basis $409,233; gain $11,387. Attach the step-up schedule.
- **ProConnect by default:** Same - ProConnect computes gain from the basis entered on the Dispositions screen.
- **ProConnect fix:** Dispositions (Schedule D/4797) screen: enter DOD basis per lot, code B adjustment for the covered MSFT lot, long-term / inherited acquisition designation (field per current release - verify). *(ref: Field per current release - verify)*
- **E-file impact:** None
- **Return lines affected:** 7, Form 8949 boxes D/E, Sch D
- **Notes:** Sec. 1014(b)(6): survivor's half of community property also takes DOD basis. DOD 08/09/2025 was a Saturday - mean of 08/08 and 08/11 values (Reg. 20.2031-2(b)). Avoids a WA capital gains excise filing.

## EVG1009-SX2 - Sale of the marital home (1099-S) - DOD appraisal basis and sec. 121 exclusion, code H

*Workbook tab:* 24. Rare-Event Log  |  *Category:* Other  |  *Manual calc:* Yes  |  *Amount:* $-18,227  |  *Procedure doc:* Estate Implications - sale of a home received from an estate; Schedule D code H

- **CCH Axcess by default:** The home-sale worksheet computes gain from the basis keyed; if basis is taken from the PERM / client records (1998 cost + improvements $295,000) and the exclusion is limited to $250,000, the return would show $88,227 of gain. If the sale is omitted because it is 'excluded', the 1099-S goes unmatched. Axcess cannot know about the community-property step-up.
- **Axcess diagnostic:** None - silent
- **Axcess fix:** Sale of principal residence input (Form 8949 box F, code H): gross proceeds $685,000 (ties to 1099-S), selling expenses $51,773, basis $615,000 (retrospective DOD appraisal - full step-up), gain $18,227, sec. 121 exclusion $18,227 (MFJ $500,000 limit; ownership/use since 1998). Net $0.
- **ProConnect by default:** Same - basis and exclusion are computed from the inputs on the home-sale worksheet.
- **ProConnect fix:** Sale of home (Form 8949 code H) inputs: proceeds $685,000, expenses $51,773, basis $615,000, exclusion applies (screen/field per current release - verify). *(ref: Screen/field per current release - verify)*
- **E-file impact:** None
- **Return lines affected:** Form 8949 box F, 7

## EVG1009-SX3 - Vanguard spousal 'transfer out' AutoFlowed as an IRA distribution

*Workbook tab:* 2. Diagnostics Log  |  *Category:* Other  |  *Manual calc:* No  |  *Amount:* $0  |  *Procedure doc:* Client IRAs / inherited IRA

- **CCH Axcess by default:** AutoFlow read Eleanor's Vanguard IRA statement ('transfer out $418,902.66') as a distribution and created a line 4a/4b entry. There is no 1099-R for a direct trustee-to-trustee transfer to the surviving spouse's own IRA.
- **Axcess diagnostic:** None - silent
- **Axcess fix:** Delete the AutoFlowed distribution; tickmark the statement 'spousal transfer - not reportable'. Only Harold's own $10,000 withdrawal (1099-R, 10% withheld) remains on lines 4a/4b.
- **ProConnect by default:** No AutoFlow equivalent in the firm's ProConnect workflow; the error occurs only if the statement is keyed.
- **ProConnect fix:** Enter only actual 1099-Rs; nothing for the transfer.
- **E-file impact:** None
- **Return lines affected:** 4a, 4b
- **Notes:** Harold's first RMD year is 2026 and will include the former inherited balance.

## EVG1009-SX4 - Year-of-death filing status: MFJ, not 'qualifying widower' (organizer + procedure wording)

*Workbook tab:* 2. Diagnostics Log  |  *Category:* Other  |  *Manual calc:* No  |  *Amount:* $0  |  *Procedure doc:* Review - Filing Status (spouse deceased)

- **CCH Axcess by default:** The organizer and the firm procedure say 'qualifying widower'. Axcess prepares whatever filing status is selected; the QSS dependent-child and 'two years after death' tests are preparer determinations.
- **Axcess diagnostic:** Not relied on - verify whether the current release flags QSS without a qualifying child
- **Axcess fix:** General > Basic Data: filing status MFJ; spouse date of death 08/09/2025 (prints 'DECEASED' and the surviving-spouse signature). No Form 1310 (no refund claimed by a non-spouse). PERM: 2026 status Single (no dependent child).
- **ProConnect by default:** Same - filing status is an input; enter the spouse's date of death on the General/taxpayer information screen.
- **ProConnect fix:** General > Filing Status: MFJ; spouse date of death 08/09/2025 (screen/field per current release - verify). *(ref: Screen/field per current release - verify)*
- **E-file impact:** None (MFJ with deceased spouse e-files normally)
- **Return lines affected:** Filing status, 12e
- **Notes:** Procedure wording is imprecise - follow sec. 6013(a)(2) / sec. 2(a).

## EVG1009-SX5 - Schedule 1-A senior deduction for the deceased spouse

*Workbook tab:* 2. Diagnostics Log  |  *Category:* Other  |  *Manual calc:* No  |  *Amount:* $12,000  |  *Procedure doc:* OBBBA - senior deduction (Schedule 1-A Part V)

- **CCH Axcess by default:** The first draft showed the senior deduction for Harold only ($6,000). Once the spouse's date of death is entered, confirm the software still counts Eleanor (65+ at death, valid SSN) on Schedule 1-A Part V - the draft result suggests it did not (verify current-release logic).
- **Axcess diagnostic:** None - silent
- **Axcess fix:** Schedule 1-A senior deduction input: both spouses 65+ (verify field / override in current release). MAGI $95,881 < $150,000 -> 2 x $6,000 = $12,000, allowed in addition to itemizing ($52,845).
- **ProConnect by default:** Same check - confirm both spouses are counted when a date of death is entered.
- **ProConnect fix:** Verify Schedule 1-A Part V shows two qualifying individuals; override if needed and document (field per current release - verify). *(ref: Intuit help: 'Using overrides and adjustments in ProConnect Tax' (document overrides))*
- **E-file impact:** None
- **Return lines affected:** 13b, Schedule 1-A Part V

