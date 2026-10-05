# EVG1019 - Owen & Chloe Fitzgerald - 2025 Software Exceptions (CCH Axcess & Intuit ProConnect)

*Synthetic training data - Project Evergreen v2. Companion workbook: `EVG1019_2025_Software_Exception_Workbook.xlsx` (firm's corrected CCH Axcess Exception Workbook, filled in).*

The headline exception on this return is the classic one in the firm's workbook: a pre-12/16/2017 mortgage that Axcess
limited to the $750,000 ceiling because the grandfathering is not something the 1098 tells it. The other two are
double-count/timing traps between Form 8829 and Schedule A and between state estimate vouchers and the federal SALT
deduction. All three are silent.

| ID | Workbook tab | Exception | Axcess diagnostic? | Override amount | E-file impact |
|---|---|---|---|---:|---|
| EVG1019-SX1 | 15. Mortgage Interest Limit | Grandfathered 2016 mortgage limited to $750,000 by default | **silent** (no diagnostic) | 25,506 | None |
| EVG1019-SX2 | 2. Diagnostics Log | Home-office share of mortgage interest and real estate tax deducted on both Form 8829 and Schedule A | **silent** (no diagnostic) | 8,856 | None |
| EVG1019-SX3 | 2. Diagnostics Log | SALT: the 01/15/2026 NC estimate and the EV highway-use tax | **silent** (no diagnostic) | 11,890 | None |

## EVG1019-SX1 - Grandfathered 2016 mortgage limited to $750,000 by default

*Workbook tab:* 15. Mortgage Interest Limit  |  *Category:* Other  |  *Manual calc:* Yes  |  *Amount:* $25,506  |  *Procedure doc:* Schedule A

- **CCH Axcess by default:** The 1098 shows outstanding principal $872,000. With no grandfathered-debt indication, Axcess applies the $750,000 acquisition-debt limit: 28,340 x 750,000/872,000 x 90% personal = $21,938 on Schedule A line 8a.
- **Axcess diagnostic:** None - silent
- **Axcess fix:** Itemized Deductions > Home Mortgage Interest: mark the loan as pre-12/16/2017 acquisition debt (originated 08/19/2016, 1098 box 3) so the $1,000,000 limit applies, or use the interest-limitation override = 100% deductible. Balance $872,000 (interest-only, constant) < $1,000,000 -> interest $28,340 fully deductible: Schedule A $25,506 (90%) + Form 8829 $2,834 (10%). Tape on the 1098 page (WP 14).
- **ProConnect by default:** Same risk - the mortgage limitation needs the loan date / grandfathered status entered to use the $1M limit.
- **ProConnect fix:** Itemized Deductions > Interest: enter the 1098 with origination date 08/19/2016 / pre-12/16/2017 indicator so the qualified-loan limit is $1,000,000 (screen/field per current release - verify).
- **E-file impact:** None
- **Return lines affected:** 12e (Schedule A line 8a)
- **Notes:** 2026: loan begins amortizing 10/2026 - no new debt, still grandfathered.

## EVG1019-SX2 - Home-office share of mortgage interest and real estate tax deducted on both Form 8829 and Schedule A

*Workbook tab:* 2. Diagnostics Log  |  *Category:* Other  |  *Manual calc:* No  |  *Amount:* $8,856  |  *Procedure doc:* Schedule C / Schedule A

- **CCH Axcess by default:** When the 8829 mortgage interest and real estate tax are keyed directly on the Form 8829 input (instead of allocating the 1098 amounts by business-use %), the full 1098 amounts still flow to Schedule A - the 10% office share is deducted twice.
- **Axcess diagnostic:** None - silent
- **Axcess fix:** Business Use of Home (8829): enter interest $28,340 and real estate tax $9,840 as total (indirect) expenses so 10% ($2,834 / $984) goes to 8829 and only the 90% personal share reaches Schedule A ($25,506 / $8,856); or reduce the Schedule A inputs manually. Office 300/3,000 sq ft; 8829 total $7,017 incl. depreciation $2,359 (vs simplified $1,500).
- **ProConnect by default:** Same - ProConnect splits mortgage interest/taxes between 8829 and Schedule A only when they are entered as home-office indirect expenses (not when also entered separately on Schedule A).
- **ProConnect fix:** Business Use of Home (8829): enter total mortgage interest and taxes as indirect expenses; do not also enter 100% on Itemized Deductions (screen/field per current release - verify).
- **E-file impact:** None
- **Return lines affected:** Schedule A lines 5b/8a, Form 8829, Schedule C line 30
- **Notes:** Accumulated office depreciation ($16,024) is unrecaptured 1250 gain on a future sale - not excludable under 121.

## EVG1019-SX3 - SALT: the 01/15/2026 NC estimate and the EV highway-use tax

*Workbook tab:* 2. Diagnostics Log  |  *Category:* Other  |  *Manual calc:* Yes  |  *Amount:* $11,890  |  *Procedure doc:* Schedule A

- **CCH Axcess by default:** State estimates keyed with their voucher due dates can all be treated as 2025 payments, so the Q4 voucher paid 01/15/2026 inflates 2025 Schedule A line 5a; the 2024 Q4 (paid 01/15/2025) and 2024 balance (paid 04/15/2025) are 2025 deductions only if keyed with their actual payment dates. Separately, a sales-tax large-item entry for the Ioniq 5 Highway Use Tax adds to the income-tax figure only if the wrong election is chosen.
- **Axcess diagnostic:** None - silent
- **Axcess fix:** Itemized Deductions > Taxes / State payments input: date-paid basis - NC income tax paid in 2025 = $11,890 (W-2 $7,350 + three 2025 estimates + 2024 Q4 paid 01/15/2025 + 2024 balance paid 04/15/2025); 01/15/2026 voucher excluded (2026 deduction; still a 2025 credit on the D-400). Income tax ($11,890) > sales tax ($2,640 table + $1,560 HUT = $4,200) - elect income tax; HUT used only in the comparison (verify field path in current release).
- **ProConnect by default:** Same - the federal deduction follows the payment dates and the income-vs-sales-tax election entered.
- **ProConnect fix:** Itemized Deductions > Taxes: state income tax paid in 2025 = 11,890 (exclude the 01/15/2026 payment); sales tax option not elected (screen/field per current release - verify).
- **E-file impact:** None
- **Return lines affected:** 12e (Schedule A line 5a)
- **Notes:** Sales tax calculator figure is an assumption (Wake County 7.25%).

