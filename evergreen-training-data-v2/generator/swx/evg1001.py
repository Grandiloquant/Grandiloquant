"""EVG1001 Bell - software exceptions (log-only, workbook tab 2; ProConnect equivalents).
Simple W-2 return: the exceptions are input/AutoFlow traps where both packages calculate exactly what they are fed.
Amounts tie to the EVG1001 answer key (wages 105,478 / withholding 6,770; Schedule 1-A overtime 3,150; car-loan interest 2,452)."""
from software_exceptions import exc

CLIENT_ID, DISPLAY = "EVG1001", "Marcus & Tanya Bell"
PREPARER, REVIEWER = "J. Ortiz (staff)", "L. Chen (senior)"
INTRO = """
A basic W-2 return with no calculation-tab exceptions. The three items below are places where CCH Axcess (and ProConnect)
compute a wrong answer from facially valid inputs and raise no diagnostic: a duplicate scanned W-2, the new Schedule 1-A
overtime deduction (the software cannot tell total overtime pay from the FLSA premium), and the Schedule 1-A car-loan interest
deduction (eligibility of each loan is a preparer determination). Everything else on the return (CTC for the newborn, Form 2441
with the FSA exclusion, Form 8889) calculates correctly once the inputs are right.
"""

ITEMS = [
    exc("EVG1001-SX1", "2", "Other", "Duplicate W-2 (PDF + phone photo) picked up by Scan/AutoFlow",
        axcess_default="Axcess Scan/AutoFlow created three W-2 input records - Marcus (Lone Star Distribution) plus Tanya's Brightsmile "
                       "Dental W-2 twice (client PDF and phone photo, same EIN and control no. BSD-22-014). The return calculates on "
                       "both copies: wages and withholding overstated by Tanya's W-2 amounts (about $47,000 of wages).",
        axcess_diagnostic="None - silent",
        manual_calc="No",
        axcess_fix="Income/Deductions > Wages, Salaries, Tips (W-2): delete the duplicate W-2 record created from the phone photo; "
                   "bookmark the photo DUP in the binder so it does not AutoFlow again. Line 1a = $105,478; line 25a = $6,770.",
        amount=105478,
        proconnect_default="ProConnect has no binder-based AutoFlow in the firm's workflow; W-2s are keyed (or imported - import "
                           "options per current release - verify). The same overstatement occurs if both copies are entered.",
        proconnect_fix="Wages, Salaries, Tips > W-2 screen: one record per W-2 (two total). Tie line 1a to the W-2 box 1 tape "
                       "(105,478) before finalizing.",
        proconnect_ref="Screen name per current release - verify",
        efile_impact="None",
        affected_lines=["1a", "25a"],
        procedure_section="Scan - duplicate documents",
        notes="Control number and EIN match is the tell; the photo is a re-upload, not a second job."),
    exc("EVG1001-SX2", "2", "Other", "Schedule 1-A Part III overtime: W-2 box 14 shows TOTAL overtime pay, not the premium",
        axcess_default="The qualified-overtime input takes whatever is keyed. If box 14 'OVERTIME 9,450.00' is keyed (or mapped) as "
                       "qualified overtime compensation, Axcess deducts $9,450 on Schedule 1-A - it cannot know the box 14 figure is "
                       "total overtime pay at 1.5x rather than the FLSA premium.",
        axcess_diagnostic="None - silent",
        manual_calc="Yes",
        axcess_fix="W-2 worksheet / Schedule 1-A qualified overtime input (verify field path in current release): enter $3,150 "
                   "(9,450 / 1.5 x 0.5 = 9,450 / 3). Keep the calculator tape on WP 3. MAGI $106,763 < $300,000 MFJ - no phase-out.",
        amount=3150,
        proconnect_default="Same - ProConnect deducts the qualified overtime amount entered; it has no way to split total OT pay.",
        proconnect_fix="Enter $3,150 in the qualified overtime compensation field for Marcus (Schedule 1-A input - screen/field per "
                       "current release - verify).",
        proconnect_ref="Screen/field per current release - verify",
        efile_impact="None",
        affected_lines=["13b", "Schedule 1-A Part III"],
        procedure_section="OBBBA - no tax on overtime (Schedule 1-A Part III)",
        notes="2025 transition: employers were not required to report qualified overtime separately; a reasonable method "
              "(premium = 1/3 of time-and-a-half pay) is allowed. From 2026 use W-2 box 12 code TT if reported."),
    exc("EVG1001-SX3", "2", "Other", "Schedule 1-A Part IV car-loan interest: only the new F-150 loan qualifies",
        axcess_default="Both lender year-end interest statements (Ford Credit F-150, Honda CR-V) were keyed as qualified passenger "
                       "vehicle loan interest; Axcess deducts $3,557. The software cannot test 'new vehicle', 'loan originated after "
                       "12/31/2024' or 'final assembly in the U.S.' - those are preparer determinations.",
        axcess_diagnostic="None - silent",
        manual_calc="No",
        axcess_fix="Schedule 1-A qualified vehicle loan interest input (verify field path in current release): keep only the Ford "
                   "Credit loan - interest $2,452, VIN entered (required on Schedule 1-A). Delete the Honda record (used vehicle, "
                   "2024 loan - personal interest, nondeductible).",
        amount=2452,
        proconnect_default="Same - the deduction is computed from the loans entered.",
        proconnect_fix="Schedule 1-A vehicle loan interest input: one record (F-150, VIN, $2,452). Screen/field per current release - verify.",
        proconnect_ref="Screen/field per current release - verify",
        efile_impact="None (VIN must be reported on Schedule 1-A)",
        affected_lines=["13b", "Schedule 1-A Part IV"],
        procedure_section="OBBBA - car loan interest (Schedule 1-A Part IV)",
        notes="Line 13b total = 3,150 + 2,452 = 5,602."),
]

TABS = {}

# Diagnostics Log rows are filled from ITEMS (tab 2 has no formulas); check the logged override amounts tie to the return.
CHECKS = {
    "'2. Diagnostics Log'!H14": 105478,
    "'2. Diagnostics Log'!H15": 3150,
    "'2. Diagnostics Log'!H16": 2452,
}
