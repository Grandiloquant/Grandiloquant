"""EVG1010 Kim - software exceptions (workbook tab 17 + log items; ProConnect equivalents).
Amounts tie to the EVG1010 answer key (RSU FMV-at-vest basis 59,880 added via code B -> net RSU gain 9,458 = ST 788 + LT 8,670;
Schedule H 4,326; Form 8814 tax 55 for Chloe; Ethan on his own return (EVG1021, Form 8615) using parents' TI 402,319;
1099-Q earnings 3,123 not taxable)."""
from software_exceptions import exc

CLIENT_ID, DISPLAY = "EVG1010", "Daniel & Grace Kim"
PREPARER, REVIEWER = "P. Anand (staff)", "M. Okafor (senior)"
INTRO = """
Tech couple with RSUs, a nanny paid as a contractor, and two children with investment income. Tab 17 carries the RSU basis
correction lot by lot (the broker reports $0 basis). The other items are silent because the software calculates exactly what it
is given: Form 8814 accepts only the income types it has lines for (a fund sale is simply left off), Schedule H exists only if the
preparer creates it, and a 1099-Q is taxable unless qualified expenses are entered. The Form 2210 result (no penalty - 2025
withholding $87,480 exceeds 110% of 2024 tax, $80,077, with Schedule H included) is computed correctly and is not an exception.
"""

ITEMS = [
    exc("EVG1010-SX1", "17", "Capital Loss", "RSU sales reported with $0 basis (basis not reported to IRS)",
        axcess_default="AutoFlow imported the Summit Shareworks 1099-B as reported - six sales, proceeds $69,338, basis $0 - and "
                       "Schedule D showed ~$70,545 of gain (with the CG distributions). The FMV at vest ($59,880 for the lots sold) was "
                       "already taxed as W-2 wages; Axcess cannot see the employer's supplemental statement.",
        axcess_diagnostic="None - silent",
        manual_calc="Yes",
        axcess_fix="Gains and Losses > Form 8949: box B (short-term: four sell-to-cover sales + 12/05 sale) / box E (150 sh from the "
                   "03/15/2023 release); keep 1099-B basis $0, adjustment code B, column (g) = -FMV at vest per lot (total $59,880). "
                   "Net RSU gain $9,458 (ST $788, LT $8,670). Tie W-2 box 14 RSU $86,400 to the release schedule.",
        amount=59880,
        proconnect_default="Same - ProConnect computes gain from the basis entered; $0 from the 1099-B means the full proceeds are taxed.",
        proconnect_fix="Dispositions screen: per lot, cost basis $0 as reported plus adjustment code B and the FMV-at-vest adjustment "
                       "(or enter the corrected basis with code B) - field per current release - verify.",
        proconnect_ref="Field per current release - verify",
        efile_impact="None (Form 8949 boxes B/E detail transmitted)",
        affected_lines=["7", "Form 8949 boxes B/E", "Sch D", "Form 8960"],
        procedure_section="Schedule D - missing cost basis on Consolidated 1099 (equity comp)",
        notes="Sell-to-cover lots STC1/STC2/STC4 show small losses ($22.80/$5.70/$22.80): the retained shares come from the same "
              "release, no other NSCS purchases in any account - no wash-sale adjustment taken (de minimis $51; firm position)."),
    exc("EVG1010-SX2", "2", "Other", "Kid taxes: Ethan not eligible for Form 8814 (fund sale + wages); Chloe 8814 elected",
        axcess_default="Following the client's request and the 2024 return, Form 8814 was set up for both children. Form 8814 has lines "
                       "only for interest, ordinary dividends and capital gain distributions, so Ethan's $3,100 gain from a fund SALE "
                       "(and his W-2) simply never enters the calculation - Axcess produces a tidy but invalid 8814 with no diagnostic.",
        axcess_diagnostic="None - silent",
        manual_calc="No",
        axcess_fix="Delete Ethan's Form 8814 from the parents' return. Ethan files his own 1040 with Form 8615 (separate client ID "
                   "EVG1021, own project code); parents' information for his 8615: taxable income $402,319, tax, qualified dividends "
                   "$5,904, net capital gain $9,877 (Axcess parent-information input on the child's return - verify field path). "
                   "Chloe's 8814 stays: $1,900 interest < $2,700 -> $0 added to income; tax $55 on line 16.",
        amount=55,
        proconnect_default="Same Form 8814 limitation. Ethan's return needs Form 8615 and ProConnect has no Family Link (a Lacerte "
                           "feature): the parents' figures must be keyed manually; until they are, diagnostic ref 826 ('Form 8615 must "
                           "be filed').",
        proconnect_fix="Parents' return: Children's Interest and Dividends (8814) for Chloe only. Ethan's return: Taxes > Children Under "
                       "18 (8615) > Parent's Information - parents' TI $402,319, tax, filing status MFJ; re-check if the parents' "
                       "return changes.",
        proconnect_ref="Intuit help: 'How do you generate Form 8615 in ProConnect Tax'; 'resolve diagnostic Ref 826'",
        efile_impact="None (two separate e-filed returns)",
        affected_lines=["16", "Form 8814", "EVG1021 Form 8615"],
        procedure_section="Review - Kid Taxes and Filings (separate client ID / project code)",
        notes="Ethan's return must be finalized after the parents' (export of final TI)."),
    exc("EVG1010-SX3", "2", "Other", "Nanny paid on a 1099-NEC is a household employee - Schedule H",
        axcess_default="The organizer answered 'no household employees' and the clients issued Maria a 1099-NEC (not the taxpayers' "
                       "income, so nothing AutoFlows). No Schedule H exists unless the preparer creates it; total tax is understated "
                       "$4,326 with no diagnostic.",
        axcess_diagnostic="None - silent",
        manual_calc="Yes",
        axcess_fix="Other Taxes > Household employment taxes (Schedule H): cash wages $28,000; SS/Medicare 15.3% = $4,284 (employee share "
                   "paid by employer - not withheld); FUTA wages $7,000 x 0.6% = $42 with state contributions paid 04/06/2026 (line "
                   "14 'Yes'); total $4,326 to Schedule 2 line 9. W-2 box 1 for Maria $30,142 (employee FICA paid by employer is "
                   "income-tax wages only) - prepared outside the 1040.",
        amount=4326,
        proconnect_default="Same - Schedule H is generated only from household employment inputs.",
        proconnect_fix="Household Employment Taxes (Schedule H) screen: cash wages $28,000, FUTA wages $7,000, state contributions paid "
                       "timely (screen/field per current release - verify).",
        proconnect_ref="Screen/field per current release - verify",
        efile_impact="None (Schedule H e-filed with the 1040; W-2/W-3 filed with SSA separately)",
        affected_lines=["23", "24", "Sch 2 line 9"],
        procedure_section="Scan - unstructured documents / Payment-app export (household employee)",
        notes="2024 wages $6,240 also exceeded the 2024 threshold - 1040-X with Schedule H in a separate MISC project."),
    exc("EVG1010-SX4", "2", "Other", "1099-Q for private K-12 tuition - earnings not taxable",
        axcess_default="The 1099-Q AutoFlowed and the draft showed box 2 earnings $3,123 as other income. The education worksheet "
                       "treats a 529 distribution as taxable unless qualified expenses are entered; there is no 1098-T for K-12 "
                       "tuition, so nothing is matched automatically.",
        axcess_diagnostic="None - silent",
        manual_calc="No",
        axcess_fix="Education > 1099-Q / qualified expenses input: enter K-12 tuition $10,000 (Lakeside Hills Academy, grade 7) as a "
                   "qualified 529 expense (verify field path in current release) -> taxable earnings $0. No education credit "
                   "(K-12 tuition is not a credit expense).",
        amount=0,
        proconnect_default="Same - 1099-Q earnings are taxable unless qualified expenses are entered.",
        proconnect_fix="Education > 1099-Q: enter qualified K-12 tuition expenses $10,000 for Chloe (field per current release - verify).",
        proconnect_ref="Field per current release - verify",
        efile_impact="None",
        affected_lines=["8 (Sch 1 line 8z)"],
        procedure_section="Form 1099-Q",
        notes="2025 limit $10,000 per beneficiary for K-12 tuition (rises to $20,000 from 2026 under OBBBA)."),
]

# Tab 17: one row per RSU lot sold (1099-B basis 0 + FMV at vest from the Northshore supplemental statement)
TABS = {
    "17": [
        {"A": "STC1 - 38 sh NSCS released 02/15/2025 @180.00, sold 02/18/2025 (box B)", "B": 0, "C": 6840, "E": "No",
         "G": "Proceeds 6,817.20 -> loss (22.80); see note on sell-to-cover lots"},
        {"A": "STC2 - 38 sh released 05/15/2025 @172.50, sold 05/15/2025 (box B)", "B": 0, "C": 6555, "E": "No",
         "G": "Proceeds 6,549.30 -> loss (5.70)"},
        {"A": "STC3 - 38 sh released 08/15/2025 @185.00, sold 08/15/2025 (box B)", "B": 0, "C": 7030, "E": "No",
         "G": "Proceeds 7,041.40 -> gain 11.40"},
        {"A": "STC4 - 38 sh released 11/15/2025 @182.50, sold 11/17/2025 (box B)", "B": 0, "C": 6935, "E": "No",
         "G": "Proceeds 6,912.20 -> loss (22.80)"},
        {"A": "S5 - 82 sh released 02/15/2025 @180.00, sold 12/05/2025 (box B)", "B": 0, "C": 14760, "E": "No",
         "G": "Proceeds 15,588.20 -> gain 828.20. ST total 788."},
        {"A": "S6 - 150 sh released 03/15/2023 @118.40 (2023 W-2), sold 06/10/2025 (box E, long-term)", "B": 0, "C": 17760, "E": "No",
         "G": "Proceeds 26,430.00 -> LT gain 8,670. Total code B adjustments 59,880; net RSU gain 9,458."},
    ],
}

CHECKS = {
    "'17. Equity Comp & Wash Sales'!D12": 6840,
    "'17. Equity Comp & Wash Sales'!D13": 6555,
    "'17. Equity Comp & Wash Sales'!D14": 7030,
    "'17. Equity Comp & Wash Sales'!D15": 6935,
    "'17. Equity Comp & Wash Sales'!D16": 14760,
    "'17. Equity Comp & Wash Sales'!D17": 17760,
    "'2. Diagnostics Log'!H14": 59880,
    "'2. Diagnostics Log'!H16": 4326,
}
