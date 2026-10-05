"""EVG1013 Brooks - software exceptions (CCH Axcess workbook tabs 17, 8 + log item; ProConnect equivalents).
Amounts tie to the EVG1013 answer key (NSO code B adjustment -22,000 -> 8949 loss -25; ISO spread 50,000 -> AMT 4,346;
HSA deduction 0; 2024 tax 23,526 vs withholding 27,600)."""
from software_exceptions import exc

CLIENT_ID, DISPLAY = "EVG1013", "Nathan Brooks"
PREPARER, REVIEWER = "Staff preparer", "L. Chen (senior)"
INTRO = """
An equity-compensation return. Both equity events are classic import traps: the broker's 1099-B basis for an NSO
same-day sale is the exercise price only (the spread is already in W-2 box 1), and Form 3921 for an ISO exercise has no
dollar box an import maps to income, so the AMT adjustment is simply missing. Neither produces a diagnostic. The HSA and
Form 2210 items are cases where the software's default computation is right from its inputs but the inputs are incomplete.
"""

ITEMS = [
    exc("EVG1013-SX1", "17", "Capital Loss", "NSO same-day sale - 1099-B basis is the exercise price only (spread taxed twice)",
        axcess_default="Autoflow brings in the E*TRADE 1099-B (box A, covered) with cost basis $4,000. Axcess computes a $21,975 short-term "
                       "gain even though the $22,000 spread is already in W-2 box 1 (box 12 code V). The Stock Plan Transactions "
                       "Supplement, if also imported/keyed, adds the same sale a second time.",
        axcess_diagnostic="None - silent",
        manual_calc="Yes",
        axcess_fix="Gains and Losses > Capital Gains and Losses, PLXR row (box A): keep the reported basis $4,000 in column (e), adjustment "
                   "code B, amount (22,000) -> loss ($25) = commission. Supplement used only as support (bookmarked DUP), not entered.",
        amount=-22000,
        proconnect_default="Same - ProConnect uses the 1099-B basis as entered/imported; it does not read W-2 code V against the 1099-B.",
        proconnect_fix="Dispositions: on the PLXR sale enter adjustment code B and adjustment amount -22,000 (or 'Adjustment to gain/loss' "
                       "with code B); keep 1099-B basis as reported (field per current release - verify).",
        efile_impact="None",
        affected_lines=["7", "Form 8949 box A"],
        procedure_section="Restricted Stock / Schedule D - adjustment codes",
        notes="Form 8949 instructions: code B when the basis shown on the 1099-B is incorrect; report the reported basis and the adjustment."),
    exc("EVG1013-SX2", "17", "AMT", "ISO exercise-and-hold - Form 3921 is not picked up, so the $50,000 AMT adjustment is missing",
        axcess_default="Form 3921 has no income box an import maps to the return, so nothing flows anywhere. With no line 2i entry Form "
                       "6251 shows no AMT and no Form 8801 credit carryforward is created; the AMT basis of the shares is never tracked.",
        axcess_diagnostic="None - silent",
        manual_calc="Yes",
        axcess_fix="AMT > Adjustments and preferences (or the ISO / Form 3921 input if used): Incentive stock options line 2i = $50,000 "
                   "(4,000 sh x (14.00 - 1.50)). AMTI $215,959; TMT $33,243 vs regular $28,897 -> AMT $4,346 (Schedule 2 line 1). "
                   "Deferral item -> Form 8801 MTC carryforward $4,346. Record AMT basis $56,000 vs regular $6,000 in PERM / asset notes "
                   "(verify field path in current release).",
        amount=50000,
        proconnect_default="Same - an ISO exercise without a sale needs a manual AMT adjustment entry; the 3921 has nothing to import.",
        proconnect_fix="Form 6251 adjustments input: Incentive stock options = 50,000 (or the ISO/3921 input if available); confirm Form 8801 "
                       "carryforward 4,346 for 2026 (screen/field per current release - verify).",
        efile_impact="None",
        affected_lines=["17 (Schedule 2 line 1)", "Form 6251 line 2i", "Form 8801 carryforward"],
        procedure_section="Restricted Stock",
        notes="A sale after 02/14/2026 is a qualifying disposition; the regular/AMT basis difference reverses on Form 6251 that year."),
    exc("EVG1013-SX3", "2", "Other", "HSA excess contribution - Form 5329 excise computed though excess was withdrawn by the due date",
        axcess_default="With 5498-SA contributions $5,300 (code W $4,300 + $1,000 personal) against the $4,300 self-only limit, Form 8889 "
                       "shows a $1,000 excess and Axcess carries it to Form 5329 Part VII (6% = $60) unless the corrective withdrawal is "
                       "entered. If the $1,000 is also keyed as a deductible personal contribution, Schedule 1 line 13 is overstated.",
        axcess_diagnostic="Excess HSA contribution message / Form 5329 generated",
        manual_calc="No",
        axcess_fix="HSA (Form 8889) input: personal contributions deductible $0 (code W already uses the full $4,300); excess contributions "
                   "withdrawn before the extended due date = $1,000 (withdrawn 09/15/2026 with $38 earnings) -> no Form 5329. The $38 is "
                   "2026 income (verify field path in current release).",
        amount=0,
        proconnect_default="Same - Form 5329 excise is computed on any excess not marked as withdrawn timely.",
        proconnect_fix="Health Savings Accounts (8889) input: enter the excess contribution withdrawn before the due date = 1,000; no deduction "
                       "for the $1,000 personal contribution (screen/field per current release - verify).",
        efile_impact="None",
        affected_lines=["10 (Schedule 1 line 13)", "Form 8889", "Form 5329"],
        procedure_section="Client IRAs / HSA",
        notes="Earnings on a corrective HSA withdrawal are income in the year withdrawn (2026) - flagged in PERM."),
    exc("EVG1013-SX4", "8", "Est. Tax Penalty", "Form 2210 - AMT-driven balance due; prior-year safe harbor met",
        axcess_default="The draft generated a penalty: with prior-year tax not available to the 2210 calculation, the test falls back to "
                       "90% of 2025 tax ($29,919) vs withholding $27,600.",
        axcess_diagnostic="None - silent",
        manual_calc="Yes",
        axcess_fix="Penalties and Interest / Form 2210 input: 2024 tax $23,526, 2024 AGI $140,986 (< $150,000 -> 100%). Required annual "
                   "payment = lesser of $29,919 and $23,526 = $23,526; withholding $27,600 (treated as paid evenly) -> penalty $0. "
                   "Extension payment $6,000 on Schedule 3 line 10 covers the balance.",
        amount=0,
        proconnect_default="Same - ProConnect needs the prior-year tax and AGI to apply the prior-year safe harbor.",
        proconnect_fix="Payments, Penalties & Extensions > 2210: enter 2024 tax 23,526 and AGI 140,986; no penalty results "
                       "(screen per current release - verify).",
        efile_impact="None",
        affected_lines=["38"],
        procedure_section="Workpapers / Responding to Review Points"),
]

TABS = {
    "17": [
        {"A": "Parallax Robotics (PLXR) NSO - 2,000 sh exercise + same-day sale 09/18/2025", "B": 4000, "C": 22000,
         "E": "No", "G": "1099-B basis = exercise price. Spread 22,000 in W-2 box 1 (code V). 8949 box A code B adj (22,000): proceeds "
                         "25,975 - corrected basis 26,000 = (25) commission."},
        {"A": "Parallax Robotics ISO - 4,000 sh exercised 02/14/2025 and held (Form 3921) - AMT BASIS", "B": 6000, "C": 50000,
         "E": "No (no sale)", "G": "Not a 1099-B row: col B = regular basis (4,000 x 1.50); col C = AMT adjustment line 2i "
                                   "(4,000 x (14.00 - 1.50)); col D = AMT basis 56,000 for the future sale. AMT 4,346 -> Form 8801 "
                                   "carryforward."},
    ],
    "8": {"E12": 33243, "E14": 140986, "E15": 23526, "E19": 27600,
          "C25": 6900, "C26": 6900, "C27": 6900, "C28": 6900,
          "D25": "Y", "D26": "Y", "D27": "Y", "D28": "Y",
          "F25": "W-2 withholding 27,600 treated as paid evenly (6,900/qtr); no estimates",
          "F28": "Extension payment 6,000 on 04/13/2026 is not an estimate (Sch 3 line 10)"},
}

CHECKS = {
    "'17. Equity Comp & Wash Sales'!D12": 26000,
    "'17. Equity Comp & Wash Sales'!D13": 56000,
    "'8. Est. Tax Penalty (2210)'!E13": 29919,
    "'8. Est. Tax Penalty (2210)'!E18": 23526,
    "'8. Est. Tax Penalty (2210)'!E20": 0,
}
