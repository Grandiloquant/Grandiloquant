# EVG1010 - Daniel & Grace Kim - 2025 Software Exceptions (CCH Axcess & Intuit ProConnect)

*Synthetic training data - Project Evergreen v2. Companion workbook: `EVG1010_2025_Software_Exception_Workbook.xlsx` (firm's corrected CCH Axcess Exception Workbook, filled in).*

Tech couple with RSUs, a nanny paid as a contractor, and two children with investment income. Tab 17 carries the RSU basis
correction lot by lot (the broker reports $0 basis). The other items are silent because the software calculates exactly what it
is given: Form 8814 accepts only the income types it has lines for (a fund sale is simply left off), Schedule H exists only if the
preparer creates it, and a 1099-Q is taxable unless qualified expenses are entered. The Form 2210 result (no penalty - 2025
withholding $87,480 exceeds 110% of 2024 tax, $80,077, with Schedule H included) is computed correctly and is not an exception.

| ID | Workbook tab | Exception | Axcess diagnostic? | Override amount | E-file impact |
|---|---|---|---|---:|---|
| EVG1010-SX1 | 17. Equity Comp & Wash Sales | RSU sales reported with $0 basis (basis not reported to IRS) | **silent** (no diagnostic) | 59,880 | None (Form 8949 boxes B/E detail transmitted) |
| EVG1010-SX2 | 2. Diagnostics Log | Kid taxes: Ethan not eligible for Form 8814 (fund sale + wages); Chloe 8814 elected | **silent** (no diagnostic) | 55 | None (two separate e-filed returns) |
| EVG1010-SX3 | 2. Diagnostics Log | Nanny paid on a 1099-NEC is a household employee - Schedule H | **silent** (no diagnostic) | 4,326 | None (Schedule H e-filed with the 1040; W-2/W-3 filed with SSA separately) |
| EVG1010-SX4 | 2. Diagnostics Log | 1099-Q for private K-12 tuition - earnings not taxable | **silent** (no diagnostic) | 0 | None |

## EVG1010-SX1 - RSU sales reported with $0 basis (basis not reported to IRS)

*Workbook tab:* 17. Equity Comp & Wash Sales  |  *Category:* Capital Loss  |  *Manual calc:* Yes  |  *Amount:* $59,880  |  *Procedure doc:* Schedule D - missing cost basis on Consolidated 1099 (equity comp)

- **CCH Axcess by default:** AutoFlow imported the Summit Shareworks 1099-B as reported - six sales, proceeds $69,338, basis $0 - and Schedule D showed ~$70,545 of gain (with the CG distributions). The FMV at vest ($59,880 for the lots sold) was already taxed as W-2 wages; Axcess cannot see the employer's supplemental statement.
- **Axcess diagnostic:** None - silent
- **Axcess fix:** Gains and Losses > Form 8949: box B (short-term: four sell-to-cover sales + 12/05 sale) / box E (150 sh from the 03/15/2023 release); keep 1099-B basis $0, adjustment code B, column (g) = -FMV at vest per lot (total $59,880). Net RSU gain $9,458 (ST $788, LT $8,670). Tie W-2 box 14 RSU $86,400 to the release schedule.
- **ProConnect by default:** Same - ProConnect computes gain from the basis entered; $0 from the 1099-B means the full proceeds are taxed.
- **ProConnect fix:** Dispositions screen: per lot, cost basis $0 as reported plus adjustment code B and the FMV-at-vest adjustment (or enter the corrected basis with code B) - field per current release - verify. *(ref: Field per current release - verify)*
- **E-file impact:** None (Form 8949 boxes B/E detail transmitted)
- **Return lines affected:** 7, Form 8949 boxes B/E, Sch D, Form 8960
- **Notes:** Sell-to-cover lots STC1/STC2/STC4 show small losses ($22.80/$5.70/$22.80): the retained shares come from the same release, no other NSCS purchases in any account - no wash-sale adjustment taken (de minimis $51; firm position).

## EVG1010-SX2 - Kid taxes: Ethan not eligible for Form 8814 (fund sale + wages); Chloe 8814 elected

*Workbook tab:* 2. Diagnostics Log  |  *Category:* Other  |  *Manual calc:* No  |  *Amount:* $55  |  *Procedure doc:* Review - Kid Taxes and Filings (separate client ID / project code)

- **CCH Axcess by default:** Following the client's request and the 2024 return, Form 8814 was set up for both children. Form 8814 has lines only for interest, ordinary dividends and capital gain distributions, so Ethan's $3,100 gain from a fund SALE (and his W-2) simply never enters the calculation - Axcess produces a tidy but invalid 8814 with no diagnostic.
- **Axcess diagnostic:** None - silent
- **Axcess fix:** Delete Ethan's Form 8814 from the parents' return. Ethan files his own 1040 with Form 8615 (separate client ID EVG1021, own project code); parents' information for his 8615: taxable income $402,319, tax, qualified dividends $5,904, net capital gain $9,877 (Axcess parent-information input on the child's return - verify field path). Chloe's 8814 stays: $1,900 interest < $2,700 -> $0 added to income; tax $55 on line 16.
- **ProConnect by default:** Same Form 8814 limitation. Ethan's return needs Form 8615 and ProConnect has no Family Link (a Lacerte feature): the parents' figures must be keyed manually; until they are, diagnostic ref 826 ('Form 8615 must be filed').
- **ProConnect fix:** Parents' return: Children's Interest and Dividends (8814) for Chloe only. Ethan's return: Taxes > Children Under 18 (8615) > Parent's Information - parents' TI $402,319, tax, filing status MFJ; re-check if the parents' return changes. *(ref: Intuit help: 'How do you generate Form 8615 in ProConnect Tax'; 'resolve diagnostic Ref 826')*
- **E-file impact:** None (two separate e-filed returns)
- **Return lines affected:** 16, Form 8814, EVG1021 Form 8615
- **Notes:** Ethan's return must be finalized after the parents' (export of final TI).

## EVG1010-SX3 - Nanny paid on a 1099-NEC is a household employee - Schedule H

*Workbook tab:* 2. Diagnostics Log  |  *Category:* Other  |  *Manual calc:* Yes  |  *Amount:* $4,326  |  *Procedure doc:* Scan - unstructured documents / Payment-app export (household employee)

- **CCH Axcess by default:** The organizer answered 'no household employees' and the clients issued Maria a 1099-NEC (not the taxpayers' income, so nothing AutoFlows). No Schedule H exists unless the preparer creates it; total tax is understated $4,326 with no diagnostic.
- **Axcess diagnostic:** None - silent
- **Axcess fix:** Other Taxes > Household employment taxes (Schedule H): cash wages $28,000; SS/Medicare 15.3% = $4,284 (employee share paid by employer - not withheld); FUTA wages $7,000 x 0.6% = $42 with state contributions paid 04/06/2026 (line 14 'Yes'); total $4,326 to Schedule 2 line 9. W-2 box 1 for Maria $30,142 (employee FICA paid by employer is income-tax wages only) - prepared outside the 1040.
- **ProConnect by default:** Same - Schedule H is generated only from household employment inputs.
- **ProConnect fix:** Household Employment Taxes (Schedule H) screen: cash wages $28,000, FUTA wages $7,000, state contributions paid timely (screen/field per current release - verify). *(ref: Screen/field per current release - verify)*
- **E-file impact:** None (Schedule H e-filed with the 1040; W-2/W-3 filed with SSA separately)
- **Return lines affected:** 23, 24, Sch 2 line 9
- **Notes:** 2024 wages $6,240 also exceeded the 2024 threshold - 1040-X with Schedule H in a separate MISC project.

## EVG1010-SX4 - 1099-Q for private K-12 tuition - earnings not taxable

*Workbook tab:* 2. Diagnostics Log  |  *Category:* Other  |  *Manual calc:* No  |  *Amount:* $0  |  *Procedure doc:* Form 1099-Q

- **CCH Axcess by default:** The 1099-Q AutoFlowed and the draft showed box 2 earnings $3,123 as other income. The education worksheet treats a 529 distribution as taxable unless qualified expenses are entered; there is no 1098-T for K-12 tuition, so nothing is matched automatically.
- **Axcess diagnostic:** None - silent
- **Axcess fix:** Education > 1099-Q / qualified expenses input: enter K-12 tuition $10,000 (Lakeside Hills Academy, grade 7) as a qualified 529 expense (verify field path in current release) -> taxable earnings $0. No education credit (K-12 tuition is not a credit expense).
- **ProConnect by default:** Same - 1099-Q earnings are taxable unless qualified expenses are entered.
- **ProConnect fix:** Education > 1099-Q: enter qualified K-12 tuition expenses $10,000 for Chloe (field per current release - verify). *(ref: Field per current release - verify)*
- **E-file impact:** None
- **Return lines affected:** 8 (Sch 1 line 8z)
- **Notes:** 2025 limit $10,000 per beneficiary for K-12 tuition (rises to $20,000 from 2026 under OBBBA).

