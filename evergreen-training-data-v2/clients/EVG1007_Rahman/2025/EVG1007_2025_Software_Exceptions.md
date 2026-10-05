# EVG1007 - Dr. Aisha Rahman - 2025 Software Exceptions (CCH Axcess & Intuit ProConnect)

*Synthetic training data - Project Evergreen v2. Companion workbook: `EVG1007_2025_Software_Exception_Workbook.xlsx` (firm's corrected CCH Axcess Exception Workbook, filled in).*

Dr. Rahman's return hits two of the workbook's calculation tabs (S-corp dual basis and Form 2210) and four
"silent" software traps where neither package raises a diagnostic - the return simply calculates the wrong answer
from facially reasonable inputs. Those silent items are the most valuable eval cases.

| ID | Workbook tab | Exception | Axcess diagnostic? | Override amount | E-file impact |
|---|---|---|---|---:|---|
| EVG1007-SX1 | 12. S-Corp Dual Basis | S-corp distribution above STOCK basis (debt basis does not cover distributions) | **silent** (no diagnostic) | 21,360 | None (Form 7203 required attachment when a distribution is received) |
| EVG1007-SX2 | 8. Est. Tax Penalty (2210) | Form 2210 - organizer says 4 estimates, only 3 were paid | **silent** (no diagnostic) | 779 | None |
| EVG1007-SX3 | 2. Diagnostics Log | SSTB flag missing from K-1 statement - QBI deduction would be ~$62,000 | **silent** (no diagnostic) | 0 | None |
| EVG1007-SX4 | 2. Diagnostics Log | NIIT - excess-distribution gain on active S-corp stock (Form 8960 line 5c) | **silent** (no diagnostic) | -21,360 | Statement attached as PDF |
| EVG1007-SX5 | 2. Diagnostics Log | State refund (1099-G $2,100) - tax benefit rule when PY SALT was capped | yes | 0 | None |
| EVG1007-SX6 | 2. Diagnostics Log | Illinois PTE tax - federal Schedule A vs IL credit | **silent** (no diagnostic) | 16,073 | IL return e-filed with K-1-P information |

## EVG1007-SX1 - S-corp distribution above STOCK basis (debt basis does not cover distributions)

*Workbook tab:* 12. S-Corp Dual Basis  |  *Category:* Basis/At-Risk/Passive  |  *Manual calc:* Yes  |  *Amount:* $21,360  |  *Procedure doc:* Schedules K-1 - Debt Basis vs Stock Basis Distribution Trap

- **CCH Axcess by default:** If beginning basis is keyed as one blended figure ($28,000 stock + $120,000 shareholder loan = $148,000), Axcess tests the $360,000 distribution against $148,000 + $310,640 of income = $458,640 and treats it as fully tax-free. No capital gain is generated.
- **Axcess diagnostic:** None - silent
- **Axcess fix:** Income/Deductions > S Corporation Passthrough > Basis Limitation section: beginning STOCK basis $28,000 on the stock-basis line; shareholder loan $120,000 entered only in the separate DEBT-basis lines. Recalculate - $21,360 excess distribution flows to Form 8949 box F (LT; held since 2016). Form 7203 attached.
- **ProConnect by default:** ProConnect requires 'Stock basis at beginning of year' to produce Form 7203 (missing entry raises diagnostic ref 56844). If the preparer types the blended $148,000 there, the same tax-free result occurs.
- **ProConnect fix:** S Corp Info (1120S K-1) > Shareholder's Basis (7203): Stock basis at beginning of year = 28,000; Debt basis at beginning of tax year = 120,000 (Shareholder Loan section). 7203 generates because a distribution was received; the $21,360 gain flows to Schedule D. *(ref: Intuit help: 'How to complete Form 7203 and resolve diagnostic 56844 in ProConnect Tax')*
- **E-file impact:** None (Form 7203 required attachment when a distribution is received)
- **Return lines affected:** 7, Form 8949 box F, Form 7203
- **Notes:** Workbook tab 12 formula corrected to apply distributions before losses (Reg. 1.1367-1(f)); see Corrections Log.

## EVG1007-SX2 - Form 2210 - organizer says 4 estimates, only 3 were paid

*Workbook tab:* 8. Est. Tax Penalty (2210)  |  *Category:* Est. Tax Penalty  |  *Manual calc:* Yes  |  *Amount:* $779  |  *Procedure doc:* Workpapers / Responding to Review Points

- **CCH Axcess by default:** Axcess computes the underpayment penalty from whatever estimates are keyed. Keying the organizer (4 x $15,000) shows no penalty; nothing compares the organizer to the IRS account transcript.
- **Axcess diagnostic:** None - silent
- **Axcess fix:** General > Payments: enter federal estimates by actual date paid (04/15, 06/16, 01/15/2026 = $15,000 each; Q3 $0). Penalty section: regular method, no waiver; 110% prior-year safe harbor applies (2024 AGI $508,300 > $150,000). Penalty $779 on line 38.
- **ProConnect by default:** Same - ProConnect uses the estimate amounts/dates entered; no transcript check.
- **ProConnect fix:** Payments, Penalties & Extensions: enter each 2025 federal estimate with its actual date paid (leave Q3 blank); let the Form 2210 penalty compute (do not check 'suppress penalty'). *(ref: Screen name per current release - verify)*
- **E-file impact:** None
- **Return lines affected:** 26, 38
- **Notes:** Workbook tab 8 (corrected) shows required annual payment $120,006 vs payments $101,360 -> NOT met.

## EVG1007-SX3 - SSTB flag missing from K-1 statement - QBI deduction would be ~$62,000

*Workbook tab:* 2. Diagnostics Log  |  *Category:* Other  |  *Manual calc:* No  |  *Amount:* $0  |  *Procedure doc:* QBI (QOFs, QROFs)

- **CCH Axcess by default:** The K-1's Section 199A statement reports QBI, W-2 wages and UBIA but the corporation did not check the SSTB box. Axcess applies the W-2 wage limit only and allows a ~$62,000 QBI deduction (20% x $310,000; wage limit $120,000 and taxable-income limit $91,273 do not bind).
- **Axcess diagnostic:** None - silent
- **Axcess fix:** S Corporation Passthrough > Section 199A: check 'Specified service trade or business'. With taxable income before QBI of $479,825 (> $247,300) the SSTB is fully phased out - QBI deduction $0.
- **ProConnect by default:** Same - ProConnect relies on the SSTB indicator entered from the K-1 statement.
- **ProConnect fix:** S Corp Info (1120S K-1) > Qualified Business Income (199A): 'Specified service trade or business' = Yes.
- **E-file impact:** None
- **Return lines affected:** 13a, Form 8995-A
- **Notes:** Pediatric medical practice is a health SSTB under 199A(d)(2).

## EVG1007-SX4 - NIIT - excess-distribution gain on active S-corp stock (Form 8960 line 5c)

*Workbook tab:* 2. Diagnostics Log  |  *Category:* Other  |  *Manual calc:* Yes  |  *Amount:* $-21,360

- **CCH Axcess by default:** The $21,360 Schedule D gain is treated as net investment income automatically (+$812 NIIT). Axcess cannot know the corporation's assets are 100% used in a nonpassive trade or business.
- **Axcess diagnostic:** None - silent
- **Axcess fix:** Form 8960 input: line 5c adjustment (disposition of partnership interest or S-corp stock) = (21,360), supported by a Reg. 1.1411-7 (proposed, may be relied on) statement. NIIT falls to $186.
- **ProConnect by default:** Same - capital gain flows into NII.
- **ProConnect fix:** Net Investment Income Tax (8960) screen: 'Adjustment for disposition of partnership interest or S corporation stock' = -21,360; attach statement. *(ref: Field label per current release - verify)*
- **E-file impact:** Statement attached as PDF
- **Return lines affected:** Schedule 2 line 12, Form 8960
- **Notes:** Position flagged for signer (NIIT $812 higher if not taken).

## EVG1007-SX5 - State refund (1099-G $2,100) - tax benefit rule when PY SALT was capped

*Workbook tab:* 2. Diagnostics Log  |  *Category:* Other  |  *Manual calc:* Yes  |  *Amount:* $0  |  *Procedure doc:* Schedule A - refunds of taxes itemized in a prior year

- **CCH Axcess by default:** For a new client or when the 2024 Schedule A detail did not proforma, Axcess's state-refund worksheet has no PY SALT/cap data and includes the full $2,100 on Schedule 1 line 1.
- **Axcess diagnostic:** Informational: state and local refund worksheet requires prior-year itemized deduction information
- **Axcess fix:** Income > State and local refund worksheet: enter 2024 state and local taxes paid ($31,000), SALT limitation $10,000, 2024 itemized total; worksheet computes $0 taxable (Rev. Rul. 2019-11).
- **ProConnect by default:** Same - the taxable-refund worksheet needs prior-year itemized and SALT-limit data; otherwise the full refund is taxable.
- **ProConnect fix:** Income > State and local tax refunds: complete the prior-year Schedule A / SALT limitation fields so the worksheet limits the taxable amount to $0. *(ref: Verify field names in current release)*
- **E-file impact:** None
- **Return lines affected:** 8 (Schedule 1 line 1)

## EVG1007-SX6 - Illinois PTE tax - federal Schedule A vs IL credit

*Workbook tab:* 2. Diagnostics Log  |  *Category:* State Allocation  |  *Manual calc:* No  |  *Amount:* $16,073  |  *Procedure doc:* Schedules K-1 - PTE tax

- **CCH Axcess by default:** If the K-1's 'state taxes paid by entity' footnote is keyed as an estimated state payment, Axcess both itemizes it (federal) and credits it (IL) - double benefit. The tax was already deducted inside K-1 box 1.
- **Axcess diagnostic:** None - silent
- **Axcess fix:** Do not enter the PTE tax on the federal Taxes worksheet. Enter $16,073 only on the IL K-1-P passthrough credit input (IL Schedule IL-E / PTE credit). IL exemption and property-tax credit are disallowed (AGI > $250,000).
- **ProConnect by default:** Same risk if entered under state estimated payments.
- **ProConnect fix:** Illinois return > Pass-through entity credits: enter the IL K-1-P PTE tax credit $16,073; nothing on federal Taxes (Schedule A).
- **E-file impact:** IL return e-filed with K-1-P information
- **Return lines affected:** Schedule A line 5a, IL-1040 credits

