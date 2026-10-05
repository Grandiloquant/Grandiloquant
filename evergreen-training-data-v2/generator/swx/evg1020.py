"""EVG1020 Turner - software exceptions (CCH Axcess workbook tabs 5, 16, 7 + log items; ProConnect equivalents).
Amounts tie to the EVG1020 answer key (Sch E (15,147) nonpassive; 192 rental / 6 personal days -> 96.97%; shared expenses
56,323 -> 54,616 rental; building depreciation 6,005 (39-yr); furniture 100% bonus 24,600; NC Sch PN 12,000 / 89,104 -> tax 437;
QBI loss carryforward 15,147)."""
from software_exceptions import exc

CLIENT_ID, DISPLAY = "EVG1020", "Ashley Turner"
PREPARER, REVIEWER = "Staff preparer", "L. Chen (senior)"
INTRO = """
A first-year short-term rental. The software's Schedule E defaults all assume a long-term residential rental: passive
with a $25,000 active-participation allowance, 27.5-year building, not a QBI trade or business. For an Airbnb with a
3.1-night average stay that she materially participates in, every one of those defaults is wrong - and because her MAGI
is under $100,000, the passive default even produced the right 2025 dollars for the wrong reason, which is exactly why it is
silent. The NC nonresident return for the casino jackpot is not created by the W-2G alone.
"""

ITEMS = [
    exc("EVG1020-SX1", "5", "Basis/At-Risk/Passive", "Short-term rental treated as a passive rental with the $25,000 allowance",
        axcess_default="A Schedule E rental defaults to rental real estate, passive, active participation. Form 8582 then allows the ($15,147) "
                       "loss under the $25,000 special allowance (MAGI $89,104 < $100,000) - right number, wrong reason. In any year MAGI "
                       "exceeds $150,000 (or for an LP-style owner) the same default would suspend the loss.",
        axcess_diagnostic="None - silent",
        manual_calc="Yes",
        axcess_fix="Rental and Royalty Income (Schedule E): property type 3 (short-term rental); activity is NOT a rental activity for 469 "
                   "(average stay 192/62 = 3.10 nights <= 7 - Reg. 1.469-1T(e)(3)(ii)(A)); material participation = Yes (test 3: 180 hours, "
                   "more than the cleaner's ~95). Nonpassive -> no Form 8582; loss offsets wages. No substantial services -> stays on "
                   "Schedule E, no SE tax (verify field names in current release).",
        amount=-15147,
        proconnect_default="Same - a rental defaults to passive with the special allowance unless the activity is marked nonpassive / "
                           "material participation.",
        proconnect_fix="Rental & Royalty Income (Sch E): property type 'Short-term rental'; check 'Materially participated' / not a passive "
                       "activity; Form 8582 not generated (screen/field per current release - verify).",
        efile_impact="None",
        affected_lines=["8 (Schedule 1 line 5)", "Schedule E line 26"],
        procedure_section="Rental Properties",
        notes="Audit-exposed position: contemporaneous dated hours log advised for 2026; the average-stay test is annual."),
    exc("EVG1020-SX2", "16", "Other", "Personal-use days - 280A(e) allocation of shared expenses (not the vacation-home limit)",
        axcess_default="With personal-use days left at 0, Axcess deducts 100% of shared expenses. Entering the girls' trip (6 days) makes the "
                       "software allocate by rental/total days used; personal use is under the greater of 14 days or 10% of rental days, "
                       "so the 280A(c)(5) income limit does not apply.",
        axcess_diagnostic="None - silent",
        manual_calc="No",
        axcess_fix="Rental input: days rented at fair rental 192; personal-use days 6 (10/12-10/18; the two August repair days are not "
                   "personal days). Shared expenses $56,323 (incl. depreciation) x 192/198 = 96.97% -> $54,616. Guest-only costs 100% "
                   "rental. Personal share of property tax ($66) to Schedule A; personal mortgage interest ($429) nondeductible.",
        amount=54616,
        proconnect_default="Same - expenses are prorated only when personal-use days are entered.",
        proconnect_fix="Rental & Royalty Income: 'Days rented at fair rental value' 192, 'Personal use days' 6; vacation-home limitation not "
                       "applicable (screen/field per current release - verify).",
        efile_impact="None",
        affected_lines=["Schedule E expenses", "Schedule A line 5b"],
        procedure_section="Rental Properties"),
    exc("EVG1020-SX3", "2", "Depreciation", "STR building life (39-yr, transient use) and 100% bonus on furniture acquired after 01/19/2025",
        axcess_default="A building on a residential rental defaults to 27.5-year residential rental property. Furniture added as 5-year "
                       "property gets the bonus rate tied to the acquisition date entered - if the acquisition date is blank or before "
                       "01/20/2025 the 40% phase-down rate applies instead of 100%. Client spreadsheet expensed closing costs and furniture.",
        axcess_diagnostic="None - silent",
        manual_calc="Yes",
        axcess_fix="Depreciation (4562) for the rental: building $330,148 (basis $388,410 incl. $3,410 closing costs; land $58,262 by assessor "
                   "ratio) = 39-year nonresidential SL MM, PIS 04/2025 -> $6,005 (a unit used predominantly by transients is not a "
                   "'dwelling unit' - 168(e)(2)(A); 27.5-yr is the aggressive alternative, signer agreed 39). Furniture $24,600 5-yr, "
                   "acquisition dates 03/22-03/30/2025 -> 100% special allowance. Loan costs $4,510 amortized 360 months ($113 for 9).",
        amount=6005,
        proconnect_default="Same - asset method/life follow the asset category chosen; bonus % follows the acquisition date entered.",
        proconnect_fix="Rental > Depreciation: building as nonresidential real property (39-yr, MM); furniture 5-yr with acquisition date after "
                       "01/19/2025 so 100% special allowance applies (screen/field per current release - verify).",
        efile_impact="None",
        affected_lines=["Schedule E line 18", "Form 4562"],
        procedure_section="Rental Properties"),
    exc("EVG1020-SX4", "7", "State Allocation", "NC casino W-2G - NC nonresident D-400 / Schedule PN not created automatically",
        axcess_default="The W-2G's state boxes (NC, $510 withheld) do not by themselves create a nonresident NC return for a Tennessee "
                       "resident; the NC withholding can be lost or (wrongly) claimed nowhere.",
        axcess_diagnostic="None - silent",
        manual_calc="No",
        axcess_fix="Add North Carolina nonresident (D-400 with Schedule PN): NC-source income = gambling winnings $12,000 of federal AGI "
                   "$89,104 = 13.47%; NC standard $12,750 (no NC gambling-loss deduction) -> NC TI $76,354 x 13.47% = $10,285 x 4.25% = "
                   "$437; withholding $510 -> refund $73. No resident credit (TN has no income tax).",
        amount=437,
        proconnect_default="Same - the nonresident state return must be activated and the W-2G sourced to NC.",
        proconnect_fix="State > North Carolina (nonresident): source the W-2G winnings to NC and enter NC withholding 510 (screen/field per "
                       "current release - verify).",
        efile_impact="NC D-400 nonresident e-filed",
        affected_lines=["NC D-400 / Schedule PN"],
        procedure_section="SALT Implications - New State Filing Requirements"),
    exc("EVG1020-SX5", "2", "Other", "Rental not flagged as a QBI trade or business - $15,147 QBI loss carryforward dropped",
        axcess_default="Rental activities default to 'not a section 199A trade or business'. With a net loss there is no 2025 deduction either "
                       "way, so nothing looks wrong - but the $15,147 qualified business loss is not carried to 2026 and 2026 QBI is "
                       "overstated.",
        axcess_diagnostic="None - silent",
        manual_calc="No",
        axcess_fix="Rental input > Section 199A: mark the STR as a qualified trade or business (self-managed, regular and continuous); Form "
                   "8995 shows QBI (15,147) -> deduction $0, QBI loss carryforward $15,147 to 2026 (PERM / carryforward report).",
        amount=-15147,
        proconnect_default="Same - the rental must be designated as a QBI trade or business for the loss to carry forward.",
        proconnect_fix="Rental & Royalty Income > Qualified Business Income (199A): 'Trade or business' = Yes (field per current release - verify).",
        efile_impact="None",
        affected_lines=["13a", "Form 8995", "2026 carryforward"],
        procedure_section="QBI (QOFs, QROFs)"),
]

TABS = {
    "5": [{"A": "Gatlinburg condo - Airbnb STR (avg stay 3.10 nights)", "B": "N - not a rental activity (<= 7-day avg stay)", "C": 15147,
           "D": 0, "F": "NOT a passive activity: material participation test 3 (180 hrs > cleaner ~95). Shown only to document why the "
                        "8582/$25k default is wrong - the allowance below would have masked it in 2025."}],
    "5cells": {"E23": 89104},
    "16": [{"A": "Gatlinburg condo (STR)", "B": 6, "C": 192, "F": 56323.07,
            "G": "IRS method 280A(e): 192/198 = 96.97% on shared costs (incl. depreciation) -> 54,616 rental. Bolton not relevant - personal "
                 "use < greater of 14 days / 10% of rental days, so not a residence and no 280A(c)(5) income limit."}],
    "7": [{"A": "NC (nonresident - W-2G Harrah's Cherokee)", "B": 89104, "C": 12000, "E": 437, "G": 0}],
}

CHECKS = {
    "'5. Passive Activity (8582)'!E13": 15147,
    "'5. Passive Activity (8582)'!E28": 25000,
    "'16. Vacation Home Allocation'!E12": 0.9697,
    "'7. Multi-State Allocation'!D12": 0.1347,
    "'7. Multi-State Allocation'!F12": 0,
}
