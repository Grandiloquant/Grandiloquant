"""EVG1003 Okafor - software exceptions (log-only, workbook tab 2; ProConnect equivalents).
Amounts tie to the EVG1003 answer key (line 1c / Form 4137 1,600; Schedule C gross receipts 39,870; Schedule 1-A tips 25,000)."""
from software_exceptions import exc

CLIENT_ID, DISPLAY = "EVG1003", "Daniel Okafor"
PREPARER, REVIEWER = "M. Alvarez (staff)", "R. Patel (senior)"
INTRO = """
Bartender + rideshare driver. Three silent software defaults: the W-2 box 8 allocated-tips default (Form 4137 on the full
allocation), a duplicate 1099-K doubling Schedule C gross receipts, and the Schedule 1-A tips deduction, which the software
can only compute from the qualified-tip amounts it is given. The Form 2210 check needs no override - with withholding treated
as paid evenly plus the April/June estimates every installment of the $3,159 prior-year safe harbor is met, and the software
reaches the same no-penalty result on its own (not logged as an exception).
"""

ITEMS = [
    exc("EVG1003-SX1", "2", "Other", "W-2 box 8 allocated tips flow to Form 4137 in full - actual tips per diary are $1,600",
        axcess_default="Keying W-2 box 8 ($2,900 allocated tips) makes Axcess report the full allocation as unreported tip income "
                       "on line 1c and compute Form 4137 on it (the first draft did exactly this). The software has no way to know "
                       "the taxpayer kept adequate daily records of actual tips.",
        axcess_diagnostic="None - silent",
        manual_calc="Yes",
        axcess_fix="W-2 input: leave box 8 as reported on the W-2 for matching, and use the Form 4137 unreported-tips override "
                   "(verify field path in current release) to report actual unreported tips $1,600 instead of the $2,900 "
                   "allocation. Form 4137 tax $122 (7.65%). Tip diary (WP 6) and client confirmation (02/18 email) retained.",
        amount=1600,
        proconnect_default="Same default - allocated tips from box 8 are treated as unreported tips on Form 4137.",
        proconnect_fix="W-2 / Form 4137 inputs: enter actual unreported tips $1,600 as the Form 4137 amount (override of the allocated "
                       "amount - field per current release - verify); document the override.",
        proconnect_ref="Intuit help: 'Using overrides and adjustments in ProConnect Tax' (document overrides); field per current release - verify",
        efile_impact="None",
        affected_lines=["1c", "Form 4137", "Sch 2 line 5"],
        procedure_section="Scan - Unstructured PBC (handwritten statements)",
        notes="Position depends on adequate contemporaneous records; without the diary the $2,900 allocation would be reported."),
    exc("EVG1003-SX2", "2", "Other", "Duplicate Uber 1099-K ('(1)' download) doubled Schedule C gross receipts",
        axcess_default="AutoFlow picked up the 1099-K twice (original download and a '(1)' re-download - same form) and both "
                       "records feed Schedule C line 1: gross receipts $78,590 instead of $39,870, with SE tax and QBI following.",
        axcess_diagnostic="None - silent",
        manual_calc="No",
        axcess_fix="Business Income (Schedule C) > 1099-K input: delete the duplicate record; bookmark the '(1)' file DUP. Gross receipts "
                   "= 1099-K $38,720 + 1099-NEC incentives $1,150 = $39,870; Uber service/booking/airport fees $11,140 on line 10.",
        amount=39870,
        proconnect_default="Same overstatement if both copies are keyed or imported (import options per current release - verify).",
        proconnect_fix="Schedule C gross receipts: one 1099-K ($38,720) plus the 1099-NEC ($1,150). Tie to bank deposits $28,730 + "
                       "fees $11,140 before finalizing.",
        proconnect_ref="Screen name per current release - verify",
        efile_impact="None",
        affected_lines=["Sch C line 1", "Sch C line 10", "23", "13a"],
        procedure_section="Return - Schedule C (1099-K gross vs net)"),
    exc("EVG1003-SX3", "2", "Other", "Schedule 1-A no-tax-on-tips: software uses only the qualified tips it is given",
        axcess_default="The first draft deducted W-2 box 7 only ($24,600). Axcess cannot identify the rider tips buried inside the "
                       "Uber 1099-K gross, and it does not know whether the Form 4137 tips are qualified - they must be entered as "
                       "qualified tips.",
        axcess_diagnostic="None - silent",
        manual_calc="Yes",
        axcess_fix="Schedule 1-A qualified tips inputs (W-2 and Schedule C activity - verify field paths in current release): W-2 "
                   "social-security tips $24,600 + Form 4137 tips $1,600 + rideshare rider tips $2,860 (limited to Schedule C net "
                   "$16,647 - not limiting) = $29,060; deduction capped at $25,000. Occupation: bartender / rideshare driver "
                   "(both on Treasury's list). MAGI $61,471 < $150,000.",
        amount=25000,
        proconnect_default="Same - computed from the qualified tip amounts entered on each source screen.",
        proconnect_fix="Enter qualified tips on the W-2 / Form 4137 and Schedule C (rideshare) Schedule 1-A inputs; confirm line 13b "
                       "$25,000 (screen/field per current release - verify).",
        proconnect_ref="Screen/field per current release - verify",
        efile_impact="None",
        affected_lines=["13b", "Schedule 1-A Part II"],
        procedure_section="Return - OBBBA no tax on tips (Schedule 1-A Part II)",
        notes="Allocated tips (box 8) never qualify. The deduction does not reduce SE tax or the Form 4137 FICA."),
]

TABS = {}

CHECKS = {
    "'2. Diagnostics Log'!H14": 1600,
    "'2. Diagnostics Log'!H15": 39870,
    "'2. Diagnostics Log'!H16": 25000,
}
