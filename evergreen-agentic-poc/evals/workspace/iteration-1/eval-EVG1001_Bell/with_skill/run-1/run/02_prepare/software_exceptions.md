# EVG1001 - Bell - Software exception log (CCH Axcess / ProConnect)

| ID | Workbook tab | Exception | Silent? | Amount | Axcess fix (input/override location) | ProConnect fix | E-file impact |
|---|---|---|---|---|---|---|---|
| 1 | 2 Diagnostics Log | Duplicate W-2 (phone photo of Tanya's W-2) - do not key twice | Yes - silent | 47,000 wages / 2,810 w/h | Delete/skip second W-2 entry in Income > Wages (W-2); ensure only one Brightsmile W-2 | Same - one W-2 entry only | Duplicate would overstate wages and withholding; IRS matching mismatch |
| 2 | 2 Diagnostics Log | Sch 1-A overtime: box 14 "OVERTIME" is total OT pay, not premium | Yes - silent | 9,450 reported -> 3,150 entered | Enter qualified overtime premium manually in the Sch 1-A / overtime input (screen/field per current release - verify); do not let a box 14 code map flow the full 9,450 | Screen/field per current release - verify; enter 3,150 | None |
| 3 | 2 Diagnostics Log | Sch 1-A car-loan interest: only the F-150 qualifies; CR-V statement must NOT be entered | Yes - silent | 2,452.18 in; 1,104.77 out | Enter vehicle loan interest with VIN, new/US assembly, purchase date for F-150 only (screen per current release - verify) | Same - verify | VIN required for the deduction |
| 4 | 2 Diagnostics Log | Form 2441 expenses: overnight camp excluded; statement total of 5,400 is wrong | Yes - silent | 6,800 qualified (8,200 paid) | Income/Deductions > Dependent Care: enter providers (names/EINs) with qualified amounts only; W-2 box 10 5,000 keyed on Tanya's W-2 | Same | Provider EINs required |
| 5 | 2 Diagnostics Log | Newborn dependent not on organizer | Yes - silent | CTC +2,200 | Add Noah James Bell to General > Dependents (DOB 12/18/2025, 12 months, SSN) | Same | SSN required for CTC |

**1.** Software has no way to know the photo is the same form; keying both would double wages (47,000) and withholding (2,810).
**2.** Software does not split total overtime pay into the FLSA premium; Lone Star reports "OVERTIME 9,450" without saying premium-only. Hourly non-exempt at 1.5x -> premium = 9,450 / 3 = 3,150 (pending employer confirmation).
**3.** The Honda statement looks like the Ford one; the CR-V is used and the loan predates 2025, so it fails Sch 1-A.
**4.** The 2441 input accepts whatever expenses are keyed; overnight-camp exclusion and the statement's sum error must be handled before input. Credit unchanged either way here (base capped at 6,000 - 5,000 FSA).
**5.** Organizer answered "no change in dependents"; the newborn comes only from the 02/11 email.
