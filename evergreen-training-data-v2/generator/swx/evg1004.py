"""EVG1004 Castellano - software exceptions (workbook tab 14 + log items; ProConnect equivalents).
Amounts tie to the EVG1004 answer key (line 4b 30,000; accrued interest (169); NR-4 pension 17,167; FTC 1,185 with 1,390 added to
the carryforward -> 3,858 total; IRA statement income ~27,197 excluded)."""
from software_exceptions import exc

CLIENT_ID, DISPLAY = "EVG1004", "Robert & Linda Castellano"
PREPARER, REVIEWER = "J. Ortiz (staff)", "R. Patel (senior)"
INTRO = """
Retirees with a Canadian pension, a consolidated brokerage 1099 and an IRA distribution the client called a QCD. One calculation
tab applies (tab 14 - accrued interest paid at purchase). The other exceptions are AutoFlow/input traps where nothing fires:
a superseded 1099-R AutoFlowed next to its correction (and the software cannot test the QCD age rule from a code on the form),
a foreign pension with no U.S. information return, and an IRA year-end statement AutoFlowed as if it were a taxable 1099.
"""

ITEMS = [
    exc("EVG1004-SX1", "2", "Other", "Original (code 7Y) and CORRECTED (code 7) 1099-R both AutoFlowed; 'QCD' by a 67-year-old",
        axcess_default="AutoFlow created two 1099-R records ($60,000 gross, $4,400 withholding). The original carries code Y "
                       "(qualified charitable distribution) and the draft excluded $8,000 as a QCD on the client's word. Axcess "
                       "excludes whatever QCD amount is entered; do not rely on the software to test the 70 1/2 age requirement "
                       "against the QCD input (verify behavior in current release).",
        axcess_diagnostic="None - silent",
        manual_calc="No",
        axcess_fix="Retirement Income > 1099-R: delete the original (bookmark 'superseded'); keep the CORRECTED form only - gross "
                   "$30,000, taxable $30,000, code 7, withholding $2,200, QCD amount blank. Line 4b $30,000. The $8,000 church gift "
                   "is a Schedule A cash contribution (standard deduction still wins).",
        amount=30000,
        proconnect_default="Same - ProConnect excludes the QCD amount entered on the 1099-R screen; a second 1099-R record doubles income.",
        proconnect_fix="Pensions, IRAs (1099-R): one record from the corrected form, QCD field blank (field per current release - verify).",
        proconnect_ref="Field per current release - verify",
        efile_impact="None",
        affected_lines=["4a", "4b", "25b"],
        procedure_section="Scan - Duplicate documents (corrected 1099-R) / QCD age test",
        notes="Robert reaches 70 1/2 on 11/14/2028. Refund $894 lower than the client expected; discussed 03/04."),
    exc("EVG1004-SX2", "14", "Other", "Accrued interest paid on the Home Depot bond purchase not netted in box 1",
        axcess_default="Box 1 interest $2,439 is AutoFlowed as reported. Schwab shows the $169 accrued interest only on a supplemental "
                       "page ('not netted against box 1'), so Axcess taxes the full coupon.",
        axcess_diagnostic="None - silent",
        manual_calc="Yes",
        axcess_fix="Interest Income > Schwab 1099-INT: enter the accrued-interest adjustment ($169) so Schedule B shows a separate "
                   "negative line 'Accrued interest' under the payer (verify field path in current release). Taxable interest $4,162.",
        amount=-169,
        proconnect_default="Same - the 1099-INT box 1 amount is taxed unless an adjustment is entered.",
        proconnect_fix="Interest Income screen: enter the accrued interest paid as an adjustment to the Schwab payer so Schedule B "
                       "shows the subtraction (field per current release - verify).",
        proconnect_ref="Field per current release - verify",
        efile_impact="None",
        affected_lines=["2b", "Schedule B"],
        procedure_section="Return - Schedule B (accrued interest reversal)",
        notes="Muni interest $3,115 goes on line 2a (no premium reported - box 13 blank) and still counts in provisional income "
              "for taxable SS. Accrued interest = 367.50 semiannual coupon x 83/180 days (04/15-07/08, 30/360) = 169.46."),
    exc("EVG1004-SX3", "2", "Other", "Canadian NR-4 pension: no U.S. form, CAD amounts, Form 1116 general category with carryforward",
        axcess_default="There is no 1099 to AutoFlow. The draft keyed the NR-4 at face value in CAD (24,000) and the Canadian tax as a "
                       "direct foreign tax credit. Axcess calculates on the numbers entered - it does not convert currency, and a "
                       "foreign tax entered without Form 1116 detail is not tested against the limitation by category.",
        axcess_diagnostic="None - silent",
        manual_calc="Yes",
        axcess_fix="Retirement Income: foreign pension $17,167 (CAD 24,000 / 1.398 IRS 2025 yearly average). Foreign Tax Credit (1116) "
                   "worksheet: general category, Canada, income $17,167, tax $2,575 (CAD 3,600 / 1.398), no de minimis election; "
                   "carryover input general category $2,468 (2023 $1,210 + 2024 $1,258). Limitation/credit $1,185; carryforward "
                   "to 2026 $3,858.",
        amount=1185,
        proconnect_default="Same - amounts must be entered in USD; the credit is limited only if the Form 1116 inputs are completed.",
        proconnect_fix="Pensions (foreign pension, USD) and Foreign Tax Credit (1116) screens: general category, country Canada, "
                       "income and tax in USD, prior-year carryover $2,468 (screen names per current release - verify).",
        proconnect_ref="Screen names per current release - verify",
        efile_impact="None",
        affected_lines=["5a", "5b", "6b", "20", "Sch 3 line 1", "Form 1116"],
        procedure_section="Foreign Transactions - Form 1116 (Canadian NR-4 pension)",
        notes="The pension also enters provisional income (taxable SS 85% maximum). FBAR for the RBC account is a separate filing "
              "(BSA E-Filing) and is not a 1040 calculation item."),
    exc("EVG1004-SX4", "2", "Other", "Schwab IRA year-end statement AutoFlowed as taxable dividends/interest/gains",
        axcess_default="AutoFlow read the IRA year-end statement like a consolidated 1099 and created dividend ($9,812), interest "
                       "($3,105) and gain ($14,280) entries - about $27,197 of income earned inside a traditional IRA.",
        axcess_diagnostic="None - silent",
        manual_calc="No",
        axcess_fix="Delete the AutoFlowed entries from the IRA statement; tickmark the page 'IRA - info only'. Only the 1099-R "
                   "(SX1) is reportable.",
        amount=0,
        proconnect_default="No AutoFlow equivalent in the firm's ProConnect workflow; the same error occurs only if the statement is keyed.",
        proconnect_fix="Do not enter IRA-internal income; only the 1099-R.",
        efile_impact="None",
        affected_lines=["2b", "3b", "7"],
        procedure_section="Review - Client IRAs"),
]

TABS = {
    "14": [{"A": "Home Depot 4.90% 04/15/2029 (CUSIP 437076CV2) - $15,000 face, bought 07/08/2025",
            "B": 367.50, "C": -169.46, "D": 0, "E": 0,
            "F": "Taxable corporate bond. Accrued interest paid to seller at purchase (Schwab supplemental page) reported as a "
                 "negative Schedule B line 'Accrued interest'. No bond premium reported (box 11 = 0). Schwab box 1 total "
                 "2,438.87 - 169.46 + Treasury 1,862.40 + RBC 30 = taxable interest 4,162."}],
}

CHECKS = {
    "'14. Bond Interest & Premium'!C19": -169,
    "'14. Bond Interest & Premium'!B19": 368,
    "'2. Diagnostics Log'!H14": 30000,
    "'2. Diagnostics Log'!H16": 1185,
}
