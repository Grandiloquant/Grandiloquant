"""EVG1005 Walsh - software exceptions (workbook tab 23 + log items; ProConnect equivalents).
Amounts tie to the EVG1005 answer key (Form 8606 taxable conversion 6,315 / basis carryforward 6,303; excess SS 2,880;
Detroit part-year: resident wages 128,400 + 4,153.85, taxable 132,045, tax 3,169, refund 912)."""
from software_exceptions import exc

CLIENT_ID, DISPLAY = "EVG1005", "Jennifer Walsh"
PREPARER, REVIEWER = "A. Novak (staff)", "D. Whitfield (senior)"
INTRO = """
Two W-2 jobs, a mid-year move out of Detroit, and a backdoor Roth with a forgotten rollover IRA. Tab 23 documents the Detroit
resident-period wage split for the second employer (its W-2 box 18 reports Detroit wages for a period when she was neither a
resident nor working in Detroit). The Form 8606 pro-rata trap is the most valuable item: with the 12/31 value of the other IRA
left blank the software produces a facially correct, nearly tax-free conversion and no diagnostic.
"""

ITEMS = [
    exc("EVG1005-SX1", "2", "Other", "Form 8606 line 6 blank - rollover IRA omitted, conversion shown as tax-free",
        axcess_default="The draft keyed the 1099-R as a backdoor Roth conversion with 2025 nondeductible contribution $7,000 and "
                       "line 6 (value of all traditional/SEP/SIMPLE IRAs at 12/31/2025) = $0 per the organizer. Axcess computes "
                       "taxable conversion $12 (earnings only). The rollover IRA has no 1099 in 2025 - only a Form 5498 - so nothing "
                       "prompts the input.",
        axcess_diagnostic="None - silent",
        manual_calc="Yes",
        axcess_fix="Retirement > Form 8606 (nondeductible IRAs) input: 12/31/2025 value of all traditional IRAs = $63,412.77 (Fidelity "
                   "Rollover IRA 5498). Line 7 conversion $7,012; nontaxable ratio 0.0994 -> nontaxable $697, taxable $6,315 (line "
                   "4b); basis carried to 2026 (line 14) $6,303. No additional tax (code 2).",
        amount=6315,
        proconnect_default="Same - ProConnect's Form 8606 calculation uses the year-end traditional IRA value entered; blank = $0.",
        proconnect_fix="IRA Information (8606) screen: enter the 12/31/2025 value of all traditional IRAs $63,412.77 and the 2025 "
                       "nondeductible contribution $7,000; prior basis $0 (screen/field per current release - verify).",
        proconnect_ref="Screen/field per current release - verify",
        efile_impact="None",
        affected_lines=["4a", "4b", "Form 8606 lines 6-14"],
        procedure_section="Review - Client IRAs / General Return Prep Notes (organizer answers vs PY WP)",
        notes="Tax cost of the pro-rata rule ~$1,520. Advise rolling the Rollover IRA into the Lakeshore 401(k) before 12/31/2026."),
    exc("EVG1005-SX2", "2", "Other", "ADP REPRINT of the first W-2 AutoFlowed as a third W-2",
        axcess_default="AutoFlow created a third W-2 from the ADP 'REPRINT' (same control no. MCA-2025-0417). Wages, withholding and the "
                       "excess social security credit are all overstated; the duplicate also inflates the Detroit box 18/19 inputs.",
        axcess_diagnostic="None - silent",
        manual_calc="No",
        axcess_fix="W-2 input: delete the REPRINT record (bookmark DUP). Keep both remaining W-2s under the taxpayer so the excess "
                   "SS credit computes: SS withheld 13,798.34 - 10,918.20 (6.2% x $176,100) = $2,880 (Schedule 3 line 11). Form 8959 "
                   "on combined Medicare wages 222,553.85 -> $203.",
        amount=2880,
        proconnect_default="Same overstatement if the reprint is keyed/imported as another W-2.",
        proconnect_fix="W-2 screen: two records only (both Taxpayer). Excess SS credit and Form 8959 then calculate automatically.",
        proconnect_ref="Screen name per current release - verify",
        efile_impact="None",
        affected_lines=["1a", "25a", "31", "Sch 3 line 11", "Form 8959"],
        procedure_section="Scan - duplicate documents / Return - Schedule 3 (excess social security)"),
    exc("EVG1005-SX3", "23", "State Allocation", "Detroit part-year resident return: Lakeshore W-2 box 18 shows Detroit wages through 09/15",
        axcess_default="The local return proformas as a Detroit RESIDENT return (2024) and picks up both W-2s' box 18 wages at 2.4%: "
                       "Motor City $128,400 + Lakeshore $41,653.85. Axcess cannot know she moved 07/01, never worked in Detroit for "
                       "Lakeshore, or that payroll kept her old address until 09/16.",
        axcess_diagnostic="None - silent",
        manual_calc="Yes",
        axcess_fix="Detroit city return input: change residency to part-year (resident 01/01-06/30/2025). Override Lakeshore resident "
                   "wages to $4,153.85 (06/23-06/30 paycheck: 6 workdays x $180,000/260 - earned and paid while a resident) and "
                   "nonresident Detroit-source wages to $0 (worked in Southfield/home). Keep the full Lakeshore box 19 withholding "
                   "$999.69 as a payment. Resident income 128,400 + 4,154 + interest 91 - exemption 600 = 132,045 x 2.4% = $3,169; "
                   "withheld $4,081 -> refund $912. City form/field names per current release - verify.",
        amount=4154,
        proconnect_default="Same allocation problem - local wages default from W-2 box 18. Michigan city return availability and "
                           "screens per current release - verify; if the Detroit return is not supported, prepare it outside the "
                           "package and file through MI Treasury.",
        proconnect_fix="W-2 local wage fields / Detroit part-year inputs: resident-period wages $4,153.85 for Lakeshore, nonresident "
                       "$0, withholding $999.69 (screen/field per current release - verify).",
        proconnect_ref="Michigan city return support per current release - verify",
        efile_impact="Detroit return e-filed through MI Treasury (accepted 03/19/2026)",
        affected_lines=["Detroit return"],
        procedure_section="SALT Implications - Local Filing Requirements",
        notes="The 02/2025 Roth conversion is excluded from Detroit income as an IRA distribution (assumption per the return - "
              "verify against current Detroit part-year instructions)."),
    exc("EVG1005-SX4", "2", "State Allocation", "MI-1040: no retirement subtraction for the Roth conversion",
        axcess_default="The draft carried the 1099-R into the Michigan pension/retirement subtraction (Form 4884 / Schedule 1). The "
                       "software keys off the 1099-R record; it does not recognize that a Roth conversion is not a retirement "
                       "benefit eligible for the subtraction unless the record is excluded (verify how the current release treats a "
                       "code-2 conversion).",
        axcess_diagnostic="None - silent",
        manual_calc="No",
        axcess_fix="Michigan > retirement/pension subtraction input: exclude the conversion 1099-R (subtraction $0). MI tax 4.25% x "
                   "(205,555 - 5,800) = $8,490; withheld $8,251 -> balance due $239.",
        amount=0,
        proconnect_default="Same risk - the MI pension subtraction worksheet draws on 1099-R records.",
        proconnect_fix="Michigan retirement subtraction (4884) inputs: exclude the conversion (field per current release - verify).",
        proconnect_ref="Field per current release - verify",
        efile_impact="None",
        affected_lines=["MI-1040 Schedule 1"],
        procedure_section="SALT Implications - Michigan"),
]

TABS = {
    "23": [
        {"A": "Detroit - resident period 06/23-06/30/2025 (Lakeshore Robotics)", "B": 6, "C": 260, "D": 180000,
         "G": "Columns C/D = payroll basis of the 06/30 paycheck (annual salary $180,000 / 260 workdays) - allocated wages "
              "4,153.85 = the actual paycheck, earned and paid while a Detroit resident -> taxable at 2.4% wherever earned."},
        {"A": "Detroit - nonresident period 07/01-09/15/2025 (Lakeshore box 18 wages 37,500.00)", "B": 0, "C": 260, "D": 180000,
         "G": "0 workdays in Detroit after the move (Southfield office / home in Royal Oak - HR note WP 10). Box 18 Detroit wages "
              "41,653.85 overstated; box 19 withholding 999.69 refunded on the part-year return. No reciprocity issue (city tax)."},
    ],
}

CHECKS = {
    "'23. Multi-State W-2 Days'!F11": 4153.85,
    "'23. Multi-State W-2 Days'!F12": 0,
    "'2. Diagnostics Log'!H14": 6315,
    "'2. Diagnostics Log'!H15": 2880,
}
