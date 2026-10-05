# EVG1016 - Megan Doyle - 2025 Software Exceptions (CCH Axcess & Intuit ProConnect)

*Synthetic training data - Project Evergreen v2. Companion workbook: `EVG1016_2025_Software_Exception_Workbook.xlsx` (firm's corrected CCH Axcess Exception Workbook, filled in).*

A separation-year return. None of these items has a calculation tab - they are all input-level traps where the software
does exactly what the document or the dependent screen implies: a 1099-R code 1 means a 10% additional tax, a dependent
on the screen gets the child tax credit and a state exemption, and a W-2 box 14 overtime figure is taken at face value.
All five are silent. The fix in each case is one correct input, documented.

| ID | Workbook tab | Exception | Axcess diagnostic? | Override amount | E-file impact |
|---|---|---|---|---:|---|
| EVG1016-SX1 | 2. Diagnostics Log | QDRO distribution to an alternate payee - 1099-R code 1 triggers a $3,000 additional tax | **silent** (no diagnostic) | 30,000 | None |
| EVG1016-SX2 | 2. Diagnostics Log | Form 8332 release - Liam stays on the return for HOH and Form 2441 but not for the CTC | **silent** (no diagnostic) | 2,200 | None (duplicate-dependent reject risk if both parents claim Liam's CTC) |
| EVG1016-SX3 | 2. Diagnostics Log | Qualified overtime - W-2 box 14 already shows only the FLSA premium | **silent** (no diagnostic) | 4,860 | None |
| EVG1016-SX4 | 2. Diagnostics Log | Michigan exemptions count the released child (Liam) because he is still on the federal dependent input | **silent** (no diagnostic) | 11,600 | MI-1040 e-filed |
| EVG1016-SX5 | 2. Diagnostics Log | Grand Rapids GR-1040R - premature QDRO distribution is city-taxable, not an exempt pension | **silent** (no diagnostic) | 1,762 | GR-1040R e-filed 03/26/2026; balance $451 by direct debit |

## EVG1016-SX1 - QDRO distribution to an alternate payee - 1099-R code 1 triggers a $3,000 additional tax

*Workbook tab:* 2. Diagnostics Log  |  *Category:* Other  |  *Manual calc:* No  |  *Amount:* $30,000  |  *Procedure doc:* Client IRAs

- **CCH Axcess by default:** Autoflow put the 1099-R on line 4a/4b (IRA) and, because box 7 shows code 1 (early distribution, no known exception) and Megan is 36, Axcess computed the 10% additional tax ($3,000) on Schedule 2. The 1099-R gives no hint that the payment was made under a QDRO.
- **Axcess diagnostic:** None - silent
- **Axcess fix:** Income > Pensions, Annuities and Retirement Plans (1099-R): uncheck IRA/SEP/SIMPLE (it is a 401(k)) -> line 5a/5b $30,000; Form 5329 exception: amount $30,000, code 04 (72(t)(2)(C) - payment to an alternate payee under a QDRO). Additional tax $0. Federal withholding $6,000 (20%) on line 25b.
- **ProConnect by default:** Same - a code 1 distribution without an exception code computes the 10% additional tax.
- **ProConnect fix:** Income > Pensions, IRAs (1099-R): not an IRA; Form 5329 / early-distribution exception = 04 (QDRO) on the full $30,000 (field per current release - verify).
- **E-file impact:** None
- **Return lines affected:** 5b, Schedule 2 line 8, Form 5329
- **Notes:** The exception would have been lost had she rolled the money to an IRA first and then withdrawn it.

## EVG1016-SX2 - Form 8332 release - Liam stays on the return for HOH and Form 2441 but not for the CTC

*Workbook tab:* 2. Diagnostics Log  |  *Category:* Other  |  *Manual calc:* No  |  *Amount:* $2,200  |  *Procedure doc:* Filing Status

- **CCH Axcess by default:** A child entered on the Dependents input with normal codes gets the child tax credit. Deleting Liam to stop the CTC also removes him as Megan's HOH qualifying person and Form 2441 qualifying person (limit drops to $3,000).
- **Axcess diagnostic:** None - silent
- **Axcess fix:** General > Dependents, Liam: keep him with the 'custodial parent released claim to noncustodial parent (Form 8332)' code so he counts for HOH and Form 2441 but not Schedule 8812. Schedule 8812: 1 qualifying child (Nora) -> $2,200. Form 2441: 2 qualifying persons, $5,200 x 20% = $1,040. Do not attach the 8332 (noncustodial parent attaches it) (verify code values in current release).
- **ProConnect by default:** Same - the dependent's 8332 release status must be set so the CTC goes to the other parent while HOH/2441 stay.
- **ProConnect fix:** General > Dependents: for Liam set 'Custodial parent released claim (8332)' / not claimed for CTC; keep as qualifying person for HOH and dependent care (field per current release - verify).
- **E-file impact:** None (duplicate-dependent reject risk if both parents claim Liam's CTC)
- **Return lines affected:** 19, Schedule 8812, Form 2441, Filing status

## EVG1016-SX3 - Qualified overtime - W-2 box 14 already shows only the FLSA premium

*Workbook tab:* 2. Diagnostics Log  |  *Category:* Other  |  *Manual calc:* Yes  |  *Amount:* $4,860  |  *Procedure doc:* Return - General Return Prep Notes

- **CCH Axcess by default:** The Schedule 1-A overtime deduction is driven by the amount entered as qualified overtime compensation. The software cannot tell whether box 14 is total overtime pay (divide by 3 for the half-time premium) or the premium itself; the firm's EVG1001 workaround (1/3 of box 14) applied here deducts only $1,620.
- **Axcess diagnostic:** None - silent
- **Axcess fix:** Wages (W-2) > box 14 / Schedule 1-A qualified overtime input: $4,860 (box 14 'QUAL OT PREM' + employer letter: 162 OT hours x $30 half-time). MAGI $118,662 < $150,000 - no phase-out. HOH (considered unmarried under 7703(b)) - joint-return requirement does not apply (verify field path in current release).
- **ProConnect by default:** Same - the qualified overtime amount is whatever is entered; no inference from box 14 labels.
- **ProConnect fix:** Wages (W-2) / Schedule 1-A input: qualified overtime compensation = 4,860 (screen/field per current release - verify).
- **E-file impact:** None
- **Return lines affected:** 13b, Schedule 1-A

## EVG1016-SX4 - Michigan exemptions count the released child (Liam) because he is still on the federal dependent input

*Workbook tab:* 2. Diagnostics Log  |  *Category:* State Allocation  |  *Manual calc:* No  |  *Amount:* $11,600  |  *Procedure doc:* SALT Implications

- **CCH Axcess by default:** Liam must stay on the federal Dependents input (HOH / Form 2441), and the MI return counts dependents from that input, so it can claim 3 exemptions (Megan + Nora + Liam) - $5,800 more than allowed, MI tax $247 too low.
- **Axcess diagnostic:** None - silent
- **Axcess fix:** Michigan > Exemptions: override number of dependents/exemptions to 2 x $5,800 = $11,600 (Megan + Nora). Assumption documented: MI exemption follows the federal dependency claim, which Brian takes for Liam in odd years. MI tax $4,550, refund $175 (verify field path in current release).
- **ProConnect by default:** Same risk - the state exemption count is derived from the federal dependents unless overridden on the MI screen.
- **ProConnect fix:** Michigan return > exemptions: override to 2 (screen/field per current release - verify).
- **E-file impact:** MI-1040 e-filed
- **Return lines affected:** MI-1040 exemptions

## EVG1016-SX5 - Grand Rapids GR-1040R - premature QDRO distribution is city-taxable, not an exempt pension

*Workbook tab:* 2. Diagnostics Log  |  *Category:* State Allocation  |  *Manual calc:* No  |  *Amount:* $1,762  |  *Procedure doc:* Local Filing Requirements

- **CCH Axcess by default:** Michigan cities exclude pensions/retirement benefits, so a 1099-R treated as a pension on the city input drops out of city income. A code 1 premature distribution is not a retirement benefit for the city and is taxable. The draft excluded the $30,000 (review point 7) - the city return then shows about $1 due instead of $451.
- **Axcess diagnostic:** None - silent
- **Axcess fix:** Michigan > City (Grand Rapids resident GR-1040R): include the $30,000 1099-R (code 1 premature distribution) in city income; wages + interest + distribution - 2 x $600 exemptions = $117,462 x 1.5% = $1,762 vs withheld $1,311 -> $451 due 04/30/2026 (verify field path in current release).
- **ProConnect by default:** City return support and its pension-exclusion logic vary by release - verify that the 1099-R is included as city-taxable.
- **ProConnect fix:** Grand Rapids city return input (if supported in current release - verify): mark the 1099-R as taxable to the city; otherwise prepare GR-1040R outside the package.
- **E-file impact:** GR-1040R e-filed 03/26/2026; balance $451 by direct debit
- **Return lines affected:** GR-1040R

