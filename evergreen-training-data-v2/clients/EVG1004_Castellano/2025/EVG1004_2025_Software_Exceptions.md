# EVG1004 - Robert & Linda Castellano - 2025 Software Exceptions (CCH Axcess & Intuit ProConnect)

*Synthetic training data - Project Evergreen v2. Companion workbook: `EVG1004_2025_Software_Exception_Workbook.xlsx` (firm's corrected CCH Axcess Exception Workbook, filled in).*

Retirees with a Canadian pension, a consolidated brokerage 1099 and an IRA distribution the client called a QCD. One calculation
tab applies (tab 14 - accrued interest paid at purchase). The other exceptions are AutoFlow/input traps where nothing fires:
a superseded 1099-R AutoFlowed next to its correction (and the software cannot test the QCD age rule from a code on the form),
a foreign pension with no U.S. information return, and an IRA year-end statement AutoFlowed as if it were a taxable 1099.

| ID | Workbook tab | Exception | Axcess diagnostic? | Override amount | E-file impact |
|---|---|---|---|---:|---|
| EVG1004-SX1 | 2. Diagnostics Log | Original (code 7Y) and CORRECTED (code 7) 1099-R both AutoFlowed; 'QCD' by a 67-year-old | **silent** (no diagnostic) | 30,000 | None |
| EVG1004-SX2 | 14. Bond Interest & Premium | Accrued interest paid on the Home Depot bond purchase not netted in box 1 | **silent** (no diagnostic) | -169 | None |
| EVG1004-SX3 | 2. Diagnostics Log | Canadian NR-4 pension: no U.S. form, CAD amounts, Form 1116 general category with carryforward | **silent** (no diagnostic) | 1,185 | None |
| EVG1004-SX4 | 2. Diagnostics Log | Schwab IRA year-end statement AutoFlowed as taxable dividends/interest/gains | **silent** (no diagnostic) | 0 | None |

## EVG1004-SX1 - Original (code 7Y) and CORRECTED (code 7) 1099-R both AutoFlowed; 'QCD' by a 67-year-old

*Workbook tab:* 2. Diagnostics Log  |  *Category:* Other  |  *Manual calc:* No  |  *Amount:* $30,000  |  *Procedure doc:* Scan - Duplicate documents (corrected 1099-R) / QCD age test

- **CCH Axcess by default:** AutoFlow created two 1099-R records ($60,000 gross, $4,400 withholding). The original carries code Y (qualified charitable distribution) and the draft excluded $8,000 as a QCD on the client's word. Axcess excludes whatever QCD amount is entered; do not rely on the software to test the 70 1/2 age requirement against the QCD input (verify behavior in current release).
- **Axcess diagnostic:** None - silent
- **Axcess fix:** Retirement Income > 1099-R: delete the original (bookmark 'superseded'); keep the CORRECTED form only - gross $30,000, taxable $30,000, code 7, withholding $2,200, QCD amount blank. Line 4b $30,000. The $8,000 church gift is a Schedule A cash contribution (standard deduction still wins).
- **ProConnect by default:** Same - ProConnect excludes the QCD amount entered on the 1099-R screen; a second 1099-R record doubles income.
- **ProConnect fix:** Pensions, IRAs (1099-R): one record from the corrected form, QCD field blank (field per current release - verify). *(ref: Field per current release - verify)*
- **E-file impact:** None
- **Return lines affected:** 4a, 4b, 25b
- **Notes:** Robert reaches 70 1/2 on 11/14/2028. Refund $894 lower than the client expected; discussed 03/04.

## EVG1004-SX2 - Accrued interest paid on the Home Depot bond purchase not netted in box 1

*Workbook tab:* 14. Bond Interest & Premium  |  *Category:* Other  |  *Manual calc:* Yes  |  *Amount:* $-169  |  *Procedure doc:* Return - Schedule B (accrued interest reversal)

- **CCH Axcess by default:** Box 1 interest $2,439 is AutoFlowed as reported. Schwab shows the $169 accrued interest only on a supplemental page ('not netted against box 1'), so Axcess taxes the full coupon.
- **Axcess diagnostic:** None - silent
- **Axcess fix:** Interest Income > Schwab 1099-INT: enter the accrued-interest adjustment ($169) so Schedule B shows a separate negative line 'Accrued interest' under the payer (verify field path in current release). Taxable interest $4,162.
- **ProConnect by default:** Same - the 1099-INT box 1 amount is taxed unless an adjustment is entered.
- **ProConnect fix:** Interest Income screen: enter the accrued interest paid as an adjustment to the Schwab payer so Schedule B shows the subtraction (field per current release - verify). *(ref: Field per current release - verify)*
- **E-file impact:** None
- **Return lines affected:** 2b, Schedule B
- **Notes:** Muni interest $3,115 goes on line 2a (no premium reported - box 13 blank) and still counts in provisional income for taxable SS. Accrued interest = 367.50 semiannual coupon x 83/180 days (04/15-07/08, 30/360) = 169.46.

## EVG1004-SX3 - Canadian NR-4 pension: no U.S. form, CAD amounts, Form 1116 general category with carryforward

*Workbook tab:* 2. Diagnostics Log  |  *Category:* Other  |  *Manual calc:* Yes  |  *Amount:* $1,185  |  *Procedure doc:* Foreign Transactions - Form 1116 (Canadian NR-4 pension)

- **CCH Axcess by default:** There is no 1099 to AutoFlow. The draft keyed the NR-4 at face value in CAD (24,000) and the Canadian tax as a direct foreign tax credit. Axcess calculates on the numbers entered - it does not convert currency, and a foreign tax entered without Form 1116 detail is not tested against the limitation by category.
- **Axcess diagnostic:** None - silent
- **Axcess fix:** Retirement Income: foreign pension $17,167 (CAD 24,000 / 1.398 IRS 2025 yearly average). Foreign Tax Credit (1116) worksheet: general category, Canada, income $17,167, tax $2,575 (CAD 3,600 / 1.398), no de minimis election; carryover input general category $2,468 (2023 $1,210 + 2024 $1,258). Limitation/credit $1,185; carryforward to 2026 $3,858.
- **ProConnect by default:** Same - amounts must be entered in USD; the credit is limited only if the Form 1116 inputs are completed.
- **ProConnect fix:** Pensions (foreign pension, USD) and Foreign Tax Credit (1116) screens: general category, country Canada, income and tax in USD, prior-year carryover $2,468 (screen names per current release - verify). *(ref: Screen names per current release - verify)*
- **E-file impact:** None
- **Return lines affected:** 5a, 5b, 6b, 20, Sch 3 line 1, Form 1116
- **Notes:** The pension also enters provisional income (taxable SS 85% maximum). FBAR for the RBC account is a separate filing (BSA E-Filing) and is not a 1040 calculation item.

## EVG1004-SX4 - Schwab IRA year-end statement AutoFlowed as taxable dividends/interest/gains

*Workbook tab:* 2. Diagnostics Log  |  *Category:* Other  |  *Manual calc:* No  |  *Amount:* $0  |  *Procedure doc:* Review - Client IRAs

- **CCH Axcess by default:** AutoFlow read the IRA year-end statement like a consolidated 1099 and created dividend ($9,812), interest ($3,105) and gain ($14,280) entries - about $27,197 of income earned inside a traditional IRA.
- **Axcess diagnostic:** None - silent
- **Axcess fix:** Delete the AutoFlowed entries from the IRA statement; tickmark the page 'IRA - info only'. Only the 1099-R (SX1) is reportable.
- **ProConnect by default:** No AutoFlow equivalent in the firm's ProConnect workflow; the same error occurs only if the statement is keyed.
- **ProConnect fix:** Do not enter IRA-internal income; only the 1099-R.
- **E-file impact:** None
- **Return lines affected:** 2b, 3b, 7

