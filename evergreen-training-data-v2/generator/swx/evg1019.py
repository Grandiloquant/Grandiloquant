"""EVG1019 Fitzgerald - software exceptions (CCH Axcess workbook tab 15 + log items; ProConnect equivalents).
Amounts tie to the EVG1019 answer key (1098 interest 28,340; Sch A mortgage 25,506 (90%) vs Axcess default 21,938;
8829 share 2,834 / 984; Sch A real estate tax 8,856; NC income tax paid in 2025 11,890)."""
from software_exceptions import exc

CLIENT_ID, DISPLAY = "EVG1019", "Owen & Chloe Fitzgerald"
PREPARER, REVIEWER = "Staff preparer", "L. Chen (senior)"
INTRO = """
The headline exception on this return is the classic one in the firm's workbook: a pre-12/16/2017 mortgage that Axcess
limited to the $750,000 ceiling because the grandfathering is not something the 1098 tells it. The other two are
double-count/timing traps between Form 8829 and Schedule A and between state estimate vouchers and the federal SALT
deduction. All three are silent.
"""

ITEMS = [
    exc("EVG1019-SX1", "15", "Other", "Grandfathered 2016 mortgage limited to $750,000 by default",
        axcess_default="The 1098 shows outstanding principal $872,000. With no grandfathered-debt indication, Axcess applies the $750,000 "
                       "acquisition-debt limit: 28,340 x 750,000/872,000 x 90% personal = $21,938 on Schedule A line 8a.",
        axcess_diagnostic="None - silent",
        manual_calc="Yes",
        axcess_fix="Itemized Deductions > Home Mortgage Interest: mark the loan as pre-12/16/2017 acquisition debt (originated 08/19/2016, "
                   "1098 box 3) so the $1,000,000 limit applies, or use the interest-limitation override = 100% deductible. Balance $872,000 "
                   "(interest-only, constant) < $1,000,000 -> interest $28,340 fully deductible: Schedule A $25,506 (90%) + Form 8829 $2,834 "
                   "(10%). Tape on the 1098 page (WP 14).",
        amount=25506,
        proconnect_default="Same risk - the mortgage limitation needs the loan date / grandfathered status entered to use the $1M limit.",
        proconnect_fix="Itemized Deductions > Interest: enter the 1098 with origination date 08/19/2016 / pre-12/16/2017 indicator so the "
                       "qualified-loan limit is $1,000,000 (screen/field per current release - verify).",
        efile_impact="None",
        affected_lines=["12e (Schedule A line 8a)"],
        procedure_section="Schedule A",
        notes="2026: loan begins amortizing 10/2026 - no new debt, still grandfathered."),
    exc("EVG1019-SX2", "2", "Other", "Home-office share of mortgage interest and real estate tax deducted on both Form 8829 and Schedule A",
        axcess_default="When the 8829 mortgage interest and real estate tax are keyed directly on the Form 8829 input (instead of allocating "
                       "the 1098 amounts by business-use %), the full 1098 amounts still flow to Schedule A - the 10% office share is "
                       "deducted twice.",
        axcess_diagnostic="None - silent",
        manual_calc="No",
        axcess_fix="Business Use of Home (8829): enter interest $28,340 and real estate tax $9,840 as total (indirect) expenses so 10% "
                   "($2,834 / $984) goes to 8829 and only the 90% personal share reaches Schedule A ($25,506 / $8,856); or reduce the "
                   "Schedule A inputs manually. Office 300/3,000 sq ft; 8829 total $7,017 incl. depreciation $2,359 (vs simplified $1,500).",
        amount=8856,
        proconnect_default="Same - ProConnect splits mortgage interest/taxes between 8829 and Schedule A only when they are entered as "
                           "home-office indirect expenses (not when also entered separately on Schedule A).",
        proconnect_fix="Business Use of Home (8829): enter total mortgage interest and taxes as indirect expenses; do not also enter 100% on "
                       "Itemized Deductions (screen/field per current release - verify).",
        efile_impact="None",
        affected_lines=["Schedule A lines 5b/8a", "Form 8829", "Schedule C line 30"],
        procedure_section="Schedule C / Schedule A",
        notes="Accumulated office depreciation ($16,024) is unrecaptured 1250 gain on a future sale - not excludable under 121."),
    exc("EVG1019-SX3", "2", "Other", "SALT: the 01/15/2026 NC estimate and the EV highway-use tax",
        axcess_default="State estimates keyed with their voucher due dates can all be treated as 2025 payments, so the Q4 voucher paid "
                       "01/15/2026 inflates 2025 Schedule A line 5a; the 2024 Q4 (paid 01/15/2025) and 2024 balance (paid 04/15/2025) are "
                       "2025 deductions only if keyed with their actual payment dates. Separately, a sales-tax large-item entry for the "
                       "Ioniq 5 Highway Use Tax adds to the income-tax figure only if the wrong election is chosen.",
        axcess_diagnostic="None - silent",
        manual_calc="Yes",
        axcess_fix="Itemized Deductions > Taxes / State payments input: date-paid basis - NC income tax paid in 2025 = $11,890 (W-2 $7,350 + "
                   "three 2025 estimates + 2024 Q4 paid 01/15/2025 + 2024 balance paid 04/15/2025); 01/15/2026 voucher excluded (2026 "
                   "deduction; still a 2025 credit on the D-400). Income tax ($11,890) > sales tax ($2,640 table + $1,560 HUT = $4,200) - "
                   "elect income tax; HUT used only in the comparison (verify field path in current release).",
        amount=11890,
        proconnect_default="Same - the federal deduction follows the payment dates and the income-vs-sales-tax election entered.",
        proconnect_fix="Itemized Deductions > Taxes: state income tax paid in 2025 = 11,890 (exclude the 01/15/2026 payment); sales tax option "
                       "not elected (screen/field per current release - verify).",
        efile_impact="None",
        affected_lines=["12e (Schedule A line 5a)"],
        procedure_section="Schedule A",
        notes="Sales tax calculator figure is an assumption (Wake County 7.25%)."),
]

TABS = {
    "15": [{"A": "Oak City Mortgage - main home (10/1 interest-only ARM, originated 08/19/2016)", "B": 872000, "C": 1000000, "D": 28340,
            "F": "Pre-12/16/2017 acquisition debt -> $1M limit; balance constant (interest-only) 872,000 -> 100%. Split: Sch A 90% = 25,506; "
                 "Form 8829 10% = 2,834. Axcess default at $750k: 21,938 (Sch A) - override."}],
}

CHECKS = {
    "'15. Mortgage Interest Limit'!E12": 28340,
    "'15. Mortgage Interest Limit'!E18": 28340,
}
