"""EVG1006 Mendoza - software exceptions (log-only, workbook tab 2; ProConnect equivalents).
Amounts tie to the EVG1006 answer key (gross receipts 176,600; SE health insurance 0 (14,400 to Sch A); SEP 15,618;
trailer bonus 6,500 + mower de minimis 2,300; Rosa's SSA-1099 14,200 excluded)."""
from software_exceptions import exc

CLIENT_ID, DISPLAY = "EVG1006", "Carlos & Maria Mendoza"
PREPARER, REVIEWER = "R. Salazar (staff)", "L. Chen (senior)"
INTRO = """
Cash-basis landscaping Schedule C kept on accrual books. No calculation tab applies (Texas - no state depreciation
difference; no AMT exposure). Every exception is silent: the software deducts SE health insurance it has no way to know is
barred, accepts gross receipts that double-count the information returns if they are keyed on top of the P&L, needs the
acquisition date / election inputs to get OBBBA bonus and the de minimis safe harbor right, and AutoFlows a dependent's own
documents onto the parents' return. The Form 2210 result (no penalty - 100% of 2024 tax $10,620 met by withholding + four
timely estimates) is computed correctly by the software and is not an exception.
"""

ITEMS = [
    exc("EVG1006-SX1", "2", "Other", "SE health insurance deduction - spouse's employer offered subsidized family coverage",
        axcess_default="The $14,400 BCBS premiums keyed on the self-employed health insurance input produce a Schedule 1 line 17 "
                       "deduction (limited only by Schedule C net profit). Axcess cannot know Maria's school district offered "
                       "subsidized family coverage every month - eligibility, not enrollment, bars the deduction (sec. 162(l)(2)(B)).",
        axcess_diagnostic="None - silent",
        manual_calc="No",
        axcess_fix="Remove the premiums from the SE health insurance input (or mark every month as eligible for an employer-"
                   "subsidized plan, if the release offers monthly eligibility boxes - verify). Enter $14,400 as Schedule A medical "
                   "insurance; itemized $29,989 < standard $31,500 -> standard deduction.",
        amount=0,
        proconnect_default="Same - the SE health insurance deduction is computed from premiums entered.",
        proconnect_fix="Do not enter the premiums as self-employed health insurance; enter them as itemized medical (screen/field per "
                       "current release - verify).",
        proconnect_ref="Screen/field per current release - verify",
        efile_impact="None",
        affected_lines=["Sch 1 line 17", "10", "13a"],
        procedure_section="Schedule C - Self-employed health insurance",
        notes="An allowed SEHI deduction would also have reduced QBI; with it removed, line 10 = 1/2 SE tax 5,936 + SEP 15,618 + educator 300 = 21,854."),
    exc("EVG1006-SX2", "2", "Other", "Gross receipts: accrual P&L revenue vs 1099-K/1099-NEC inputs (cash method)",
        axcess_default="Gross receipts were keyed from the QuickBooks accrual P&L ($186,400). Separately, Axcess Schedule C 1099 "
                       "inputs (1099-K $61,240; 1099-NEC $24,000 and $18,500) add to gross receipts if they are entered as additional "
                       "income rather than as amounts already included - the software cannot know the information returns are a "
                       "subset of the P&L revenue.",
        axcess_diagnostic="None - silent",
        manual_calc="Yes",
        axcess_fix="Business Income (Schedule C): gross receipts $176,600 = P&L revenue $186,400 - A/R increase $9,800 (6,200 -> "
                   "16,000; Stone Oak HOA invoice collected 01/09/2026). Enter the 1099-K/NEC amounts only as 'included in gross "
                   "receipts' (or not at all) so they do not stack (verify field behavior in current release).",
        amount=176600,
        proconnect_default="Same risk: Schedule C 1099-NEC/1099-K entries can flow to gross receipts in addition to a keyed total.",
        proconnect_fix="Schedule C gross receipts $176,600; link the 1099-K/1099-NEC as included in that total, not additive "
                       "(field per current release - verify).",
        proconnect_ref="Field per current release - verify",
        efile_impact="None",
        affected_lines=["Sch C line 1", "Sch C 31", "23"],
        procedure_section="Schedule C - Accrual Basis books that should be on cash basis; AJEs",
        notes="1099s total $103,740 vs cash receipts $176,600 - no double counting. A/P nil at both dates."),
    exc("EVG1006-SX3", "2", "Depreciation", "Used trailer 100% bonus (acquired after 01/19/2025) and mower de minimis election",
        axcess_default="The draft depreciated the $6,500 used trailer over 5 years with no bonus and capitalized the $2,300 mower as "
                       "7-year property. The bonus percentage depends on the acquisition (binding contract) date input and on any "
                       "elect-out flag proforma'd from the truck (elected out in 2022); the de minimis safe harbor is an annual "
                       "election the software applies only if it is made.",
        axcess_diagnostic="None - silent",
        manual_calc="No",
        axcess_fix="Depreciation (Form 4562) asset input for the trailer: 5-year MACRS, acquisition date 03/22/2025, no elect-out for "
                   "2025 -> 100% special allowance $6,500 (verify the OBBBA acquisition-date field in current release). Mower: "
                   "delete the asset; expense $2,300 on Schedule C line 27a and generate the Reg. 1.263(a)-1(f) election statement "
                   "(General > Elections / statement - verify). Truck: PERM MACRS year 4 on 85% business basis $5,092.",
        amount=6500,
        proconnect_default="Same - bonus follows the asset's dates and elections; the de minimis election statement must be generated.",
        proconnect_fix="Depreciation screen for the trailer: bonus applies (acquired after 01/19/2025; elect-out not checked). Mower "
                       "expensed with the de minimis safe harbor election statement attached (screen/field per current release - verify).",
        proconnect_ref="Screen/field per current release - verify",
        efile_impact="De minimis election statement attached to the e-filed return",
        affected_lines=["Sch C 13", "Sch C 27a", "Form 4562"],
        procedure_section="Schedule C - De-Minimis Safe Harbor Election",
        notes="Bonus chosen over sec. 179 (automatic, not income-limited); same $6,500 deduction this year."),
    exc("EVG1006-SX4", "2", "Other", "SEP-IRA maximum for a self-employed person (20%, not 25% of net profit)",
        axcess_default="The draft keyed the client's planned contribution $21,006 (25% of net profit). Axcess's self-employed "
                       "retirement worksheet computes the limit from the plan rate and net earnings when those inputs are used; a "
                       "keyed dollar amount may be deducted as entered (verify limitation behavior in current release). Either way "
                       "the software cannot tell the client how much to fund before the return is final.",
        axcess_diagnostic="Possible excess-contribution / limitation message if the keyed amount exceeds the computed maximum - verify in current release",
        manual_calc="Yes",
        axcess_fix="Adjustments > Self-employed SEP input: plan contribution rate 25% (worksheet converts to 20% of net earnings after "
                   "1/2 SE tax): (84,025 - 5,936) x 20% = $15,618. Communicated 09/21; funded 09/22/2026 before the 10/15 extended "
                   "due date. QBI reduced by the SEP and 1/2 SE tax.",
        amount=15618,
        proconnect_default="Same - the SEP deduction worksheet computes the maximum from the plan rate; a keyed amount is the preparer's responsibility.",
        proconnect_fix="Self-employed pension (SEP) input: contribution rate 25% / deduct maximum; confirm Schedule 1 line 16 = $15,618 "
                       "(screen/field per current release - verify).",
        proconnect_ref="Screen/field per current release - verify",
        efile_impact="None",
        affected_lines=["Sch 1 line 16", "10", "13a"],
        procedure_section="Schedule C - SEP IRA (compute maximum amount)"),
    exc("EVG1006-SX5", "2", "Other", "Dependent mother's SSA-1099 and 1099-INT AutoFlowed onto the parents' return",
        axcess_default="Rosa's SSA-1099 ($14,200) and Broadway Bank 1099-INT ($85) were in the upload and AutoFlow put them on the "
                       "Mendozas' lines 6a and 2b, creating taxable social security and interest that are not theirs.",
        axcess_diagnostic="None - silent",
        manual_calc="No",
        axcess_fix="Delete both AutoFlowed inputs; bookmark the documents 'not for this return - dependent's own'. Add Rosa as a "
                   "qualifying relative (gross income $85 < $5,200; support ~68% provided) -> $500 ODC.",
        amount=14200,
        proconnect_default="No AutoFlow equivalent in the firm's ProConnect workflow; the error occurs only if the forms are keyed.",
        proconnect_fix="Do not enter Rosa's forms; add her on the Dependents screen as a qualifying relative (ODC).",
        efile_impact="None",
        affected_lines=["6a", "6b", "2b", "19"],
        procedure_section="Dependents / qualifying relative"),
]

TABS = {}

CHECKS = {
    "'2. Diagnostics Log'!H15": 176600,
    "'2. Diagnostics Log'!H16": 6500,
    "'2. Diagnostics Log'!H17": 15618,
}
