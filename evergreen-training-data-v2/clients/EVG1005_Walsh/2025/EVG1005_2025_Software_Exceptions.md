# EVG1005 - Jennifer Walsh - 2025 Software Exceptions (CCH Axcess & Intuit ProConnect)

*Synthetic training data - Project Evergreen v2. Companion workbook: `EVG1005_2025_Software_Exception_Workbook.xlsx` (firm's corrected CCH Axcess Exception Workbook, filled in).*

Two W-2 jobs, a mid-year move out of Detroit, and a backdoor Roth with a forgotten rollover IRA. Tab 23 documents the Detroit
resident-period wage split for the second employer (its W-2 box 18 reports Detroit wages for a period when she was neither a
resident nor working in Detroit). The Form 8606 pro-rata trap is the most valuable item: with the 12/31 value of the other IRA
left blank the software produces a facially correct, nearly tax-free conversion and no diagnostic.

| ID | Workbook tab | Exception | Axcess diagnostic? | Override amount | E-file impact |
|---|---|---|---|---:|---|
| EVG1005-SX1 | 2. Diagnostics Log | Form 8606 line 6 blank - rollover IRA omitted, conversion shown as tax-free | **silent** (no diagnostic) | 6,315 | None |
| EVG1005-SX2 | 2. Diagnostics Log | ADP REPRINT of the first W-2 AutoFlowed as a third W-2 | **silent** (no diagnostic) | 2,880 | None |
| EVG1005-SX3 | 23. Multi-State W-2 Days | Detroit part-year resident return: Lakeshore W-2 box 18 shows Detroit wages through 09/15 | **silent** (no diagnostic) | 4,154 | Detroit return e-filed through MI Treasury (accepted 03/19/2026) |
| EVG1005-SX4 | 2. Diagnostics Log | MI-1040: no retirement subtraction for the Roth conversion | **silent** (no diagnostic) | 0 | None |

## EVG1005-SX1 - Form 8606 line 6 blank - rollover IRA omitted, conversion shown as tax-free

*Workbook tab:* 2. Diagnostics Log  |  *Category:* Other  |  *Manual calc:* Yes  |  *Amount:* $6,315  |  *Procedure doc:* Review - Client IRAs / General Return Prep Notes (organizer answers vs PY WP)

- **CCH Axcess by default:** The draft keyed the 1099-R as a backdoor Roth conversion with 2025 nondeductible contribution $7,000 and line 6 (value of all traditional/SEP/SIMPLE IRAs at 12/31/2025) = $0 per the organizer. Axcess computes taxable conversion $12 (earnings only). The rollover IRA has no 1099 in 2025 - only a Form 5498 - so nothing prompts the input.
- **Axcess diagnostic:** None - silent
- **Axcess fix:** Retirement > Form 8606 (nondeductible IRAs) input: 12/31/2025 value of all traditional IRAs = $63,412.77 (Fidelity Rollover IRA 5498). Line 7 conversion $7,012; nontaxable ratio 0.0994 -> nontaxable $697, taxable $6,315 (line 4b); basis carried to 2026 (line 14) $6,303. No additional tax (code 2).
- **ProConnect by default:** Same - ProConnect's Form 8606 calculation uses the year-end traditional IRA value entered; blank = $0.
- **ProConnect fix:** IRA Information (8606) screen: enter the 12/31/2025 value of all traditional IRAs $63,412.77 and the 2025 nondeductible contribution $7,000; prior basis $0 (screen/field per current release - verify). *(ref: Screen/field per current release - verify)*
- **E-file impact:** None
- **Return lines affected:** 4a, 4b, Form 8606 lines 6-14
- **Notes:** Tax cost of the pro-rata rule ~$1,520. Advise rolling the Rollover IRA into the Lakeshore 401(k) before 12/31/2026.

## EVG1005-SX2 - ADP REPRINT of the first W-2 AutoFlowed as a third W-2

*Workbook tab:* 2. Diagnostics Log  |  *Category:* Other  |  *Manual calc:* No  |  *Amount:* $2,880  |  *Procedure doc:* Scan - duplicate documents / Return - Schedule 3 (excess social security)

- **CCH Axcess by default:** AutoFlow created a third W-2 from the ADP 'REPRINT' (same control no. MCA-2025-0417). Wages, withholding and the excess social security credit are all overstated; the duplicate also inflates the Detroit box 18/19 inputs.
- **Axcess diagnostic:** None - silent
- **Axcess fix:** W-2 input: delete the REPRINT record (bookmark DUP). Keep both remaining W-2s under the taxpayer so the excess SS credit computes: SS withheld 13,798.34 - 10,918.20 (6.2% x $176,100) = $2,880 (Schedule 3 line 11). Form 8959 on combined Medicare wages 222,553.85 -> $203.
- **ProConnect by default:** Same overstatement if the reprint is keyed/imported as another W-2.
- **ProConnect fix:** W-2 screen: two records only (both Taxpayer). Excess SS credit and Form 8959 then calculate automatically. *(ref: Screen name per current release - verify)*
- **E-file impact:** None
- **Return lines affected:** 1a, 25a, 31, Sch 3 line 11, Form 8959

## EVG1005-SX3 - Detroit part-year resident return: Lakeshore W-2 box 18 shows Detroit wages through 09/15

*Workbook tab:* 23. Multi-State W-2 Days  |  *Category:* State Allocation  |  *Manual calc:* Yes  |  *Amount:* $4,154  |  *Procedure doc:* SALT Implications - Local Filing Requirements

- **CCH Axcess by default:** The local return proformas as a Detroit RESIDENT return (2024) and picks up both W-2s' box 18 wages at 2.4%: Motor City $128,400 + Lakeshore $41,653.85. Axcess cannot know she moved 07/01, never worked in Detroit for Lakeshore, or that payroll kept her old address until 09/16.
- **Axcess diagnostic:** None - silent
- **Axcess fix:** Detroit city return input: change residency to part-year (resident 01/01-06/30/2025). Override Lakeshore resident wages to $4,153.85 (06/23-06/30 paycheck: 6 workdays x $180,000/260 - earned and paid while a resident) and nonresident Detroit-source wages to $0 (worked in Southfield/home). Keep the full Lakeshore box 19 withholding $999.69 as a payment. Resident income 128,400 + 4,154 + interest 91 - exemption 600 = 132,045 x 2.4% = $3,169; withheld $4,081 -> refund $912. City form/field names per current release - verify.
- **ProConnect by default:** Same allocation problem - local wages default from W-2 box 18. Michigan city return availability and screens per current release - verify; if the Detroit return is not supported, prepare it outside the package and file through MI Treasury.
- **ProConnect fix:** W-2 local wage fields / Detroit part-year inputs: resident-period wages $4,153.85 for Lakeshore, nonresident $0, withholding $999.69 (screen/field per current release - verify). *(ref: Michigan city return support per current release - verify)*
- **E-file impact:** Detroit return e-filed through MI Treasury (accepted 03/19/2026)
- **Return lines affected:** Detroit return
- **Notes:** The 02/2025 Roth conversion is excluded from Detroit income as an IRA distribution (assumption per the return - verify against current Detroit part-year instructions).

## EVG1005-SX4 - MI-1040: no retirement subtraction for the Roth conversion

*Workbook tab:* 2. Diagnostics Log  |  *Category:* State Allocation  |  *Manual calc:* No  |  *Amount:* $0  |  *Procedure doc:* SALT Implications - Michigan

- **CCH Axcess by default:** The draft carried the 1099-R into the Michigan pension/retirement subtraction (Form 4884 / Schedule 1). The software keys off the 1099-R record; it does not recognize that a Roth conversion is not a retirement benefit eligible for the subtraction unless the record is excluded (verify how the current release treats a code-2 conversion).
- **Axcess diagnostic:** None - silent
- **Axcess fix:** Michigan > retirement/pension subtraction input: exclude the conversion 1099-R (subtraction $0). MI tax 4.25% x (205,555 - 5,800) = $8,490; withheld $8,251 -> balance due $239.
- **ProConnect by default:** Same risk - the MI pension subtraction worksheet draws on 1099-R records.
- **ProConnect fix:** Michigan retirement subtraction (4884) inputs: exclude the conversion (field per current release - verify). *(ref: Field per current release - verify)*
- **E-file impact:** None
- **Return lines affected:** MI-1040 Schedule 1

