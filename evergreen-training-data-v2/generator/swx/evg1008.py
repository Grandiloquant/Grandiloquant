"""EVG1008 O'Brien - software exceptions (workbook tabs 5 and 16 + log items; ProConnect equivalents).
Amounts tie to the EVG1008 answer key (duplex loss (3,207) + PY unallowed 6,200 -> 9,407 suspended at MAGI 171,682; cabin
62 rental / 21 personal days, 62/83 = 74.70%, net 0 with carryovers operating 260 + depreciation 4,244; roof 14,000 capitalized
-> 276; PA compensation 189,300, PA tax 5,823)."""
from software_exceptions import exc

CLIENT_ID, DISPLAY = "EVG1008", "Kevin & Samantha O'Brien"
PREPARER, REVIEWER = "A. Brennan (staff)", "L. Chen (senior)"
INTRO = """
Two rentals: a long-term duplex (passive, fully suspended) and a cabin that became a sec. 280A residence because of 21 personal
days. Tab 5 documents the $25,000 allowance phase-out and the suspended loss; tab 16 the cabin's IRS-method allocation. The
silent items are the duplex 1098 (rental address) AutoFlowing to Schedule A, the roof coded as a repair in the client's ledger,
the day counts the vacation-home calculation depends on, and PA compensation/rents that do not follow the federal numbers.
"""

ITEMS = [
    exc("EVG1008-SX1", "2", "Other", "Duplex Form 1098 (box 8 = rental address) AutoFlowed to Schedule A; escrow summary imported as a second 1098",
        axcess_default="AutoFlow treats every Form 1098 as home mortgage interest: the duplex 1098 ($9,860 interest; $5,420 escrowed "
                       "taxes) went to Schedule A, flipping the return to itemized ($41,825) and overstating the duplex result. The "
                       "lender's escrow year-end summary was imported as another 1098 (duplicate).",
        axcess_diagnostic="None - silent",
        manual_calc="No",
        axcess_fix="Delete the Schedule A 1098 entries for the duplex and the escrow-summary record. Rental (Schedule E) Property A: "
                   "mortgage interest $9,860 (line 12), taxes $5,420 (line 16). Itemized $26,545 < standard $31,500 -> standard.",
        amount=9860,
        proconnect_default="If the 1098 is entered on the itemized-deduction mortgage screen it is deducted on Schedule A; ProConnect "
                           "does not read box 8.",
        proconnect_fix="Enter the interest and taxes on the Rental & Royalty Income (Schedule E) screen for the duplex, not on the "
                       "Schedule A mortgage interest screen (screen names per current release - verify).",
        proconnect_ref="Screen names per current release - verify",
        efile_impact="None",
        affected_lines=["12e", "Sch E 12", "Sch E 16"],
        procedure_section="Schedule E - Rental Properties (Form 1098 treated as personal)",
        notes="Box 7 'No' (not the borrower's residence) and box 8 address are the tells."),
    exc("EVG1008-SX2", "2", "Depreciation", "Roof coded 'Repairs' in the client ledger; water heater de minimis; window repair",
        axcess_default="Rental expenses are keyed from the client's ledger by category, so the $14,000 full roof replacement lands on "
                       "Schedule E line 14 as a repair. Axcess cannot distinguish a restoration of a building system from a repair, "
                       "and applies the de minimis safe harbor only if the election is made.",
        axcess_diagnostic="None - silent",
        manual_calc="No",
        axcess_fix="Depreciation (Form 4562) for Property A: add 'Roof replacement' 06/2025, $14,000, residential rental 27.5-yr SL "
                   "mid-month -> $276. Remove it from repairs. Water heater $1,900 on line 19 with the Reg. 1.263(a)-1(f) election "
                   "statement (General > Elections / statement - verify); window $450 stays a repair. Small-taxpayer safe harbor "
                   "not available (> 2% of $265,000 UBB).",
        amount=276,
        proconnect_default="Same - expenses entered as repairs are deducted; capitalization is a preparer determination.",
        proconnect_fix="Add the roof as a residential rental asset on the property's depreciation screen (27.5-yr, 06/2025); generate the "
                       "de minimis election statement (screen/field per current release - verify).",
        proconnect_ref="Screen/field per current release - verify",
        efile_impact="De minimis election statement attached",
        affected_lines=["Sch E 14", "Sch E 18", "Form 4562"],
        procedure_section="Schedule E - capitalization of repairs vs improvements; de minimis election",
        notes="Loss is suspended either way, but the basis and the suspended-loss carryforward would be wrong."),
    exc("EVG1008-SX3", "5", "Basis/At-Risk/Passive", "Form 8582: PY unallowed loss $6,200 not on the organizer; $25,000 allowance fully phased out",
        axcess_default="Axcess releases or suspends only the prior-year unallowed loss present on the activity's carryover input. "
                       "The organizer was silent; if the 2024 carryover is not on the duplex activity (e.g., the property is re-keyed "
                       "as a new activity from the scanned ledger) the $6,200 is silently lost.",
        axcess_diagnostic="None - silent",
        manual_calc="Yes",
        axcess_fix="Rental (Schedule E) Property A > passive carryover input: prior-year unallowed loss (regular) $6,200 per the 2024 "
                   "Form 8582 / PERM (verify AMT carryover - same amount, no AMT preferences). MAGI $171,682 > $150,000 -> special "
                   "allowance $0; 2025 loss ($3,207) also suspended -> $9,407 to 2026.",
        amount=9407,
        proconnect_default="Same - ProConnect uses the prior-year unallowed losses entered on the rental's Passive Losses tab.",
        proconnect_fix="Rental & Royalty Income > Passive Losses tab: prior-year unallowed losses - Regular $6,200 and AMT $6,200 (enter "
                       "both). Form 8582 generates automatically (or force: 1 = when applicable, 2 = force).",
        proconnect_ref="Intuit help: 'How to generate Form 8582 in ProConnect Tax'; community thread on prior years' unallowed losses",
        efile_impact="None",
        affected_lines=["Form 8582", "Sch E 22"],
        procedure_section="General Return Prep Notes - blank organizer line with PY amount (suspended passive loss)",
        notes="The 9,407 carryforward is not listed in the answer key's carryforwards_to_2026 block (only in the gotchas/notes)."),
    exc("EVG1008-SX4", "16", "Basis/At-Risk/Passive", "Cabin - sec. 280A residence: personal days must include the brother's free stay",
        axcess_default="Axcess's vacation-home limitation uses the personal-use and rental days entered. The draft keyed 18 personal "
                       "days (family only) - under 18 days the cabin is still a residence (18 > 14), but the allocation % and the "
                       "carryovers change; the first draft went further and keyed the cabin as a regular rental with a ~$7,000 loss. "
                       "The software cannot know Pat's free nights are personal use or that the deck weekend was repair work.",
        axcess_diagnostic="None - silent",
        manual_calc="Yes",
        axcess_fix="Rental (Schedule E) Property B: type 1 (single family / vacation), fair rental days 62, personal use days 21 (18 "
                   "family + 3 brother; 10/11-10/12 repair weekend excluded). IRS method 62/83 = 74.70%; rental income limit applies "
                   "(Pub. 527 Worksheet 5-1): interest $6,200 + taxes $2,480 + direct $2,430 -> operating $3,770 of $4,030 -> "
                   "depreciation $0 of $4,244. Net $0; carry forward operating $260 + depreciation $4,244. Personal share of interest "
                   "$2,100 / taxes $840 to the Schedule A worksheet.",
        amount=0,
        proconnect_default="Same - the vacation home limitation is computed from the days entered on the rental screen.",
        proconnect_fix="Rental & Royalty Income: days rented at fair rental 62; personal use days 21; vacation home limitation applies "
                       "(IRS method). Check the carryover of operating expenses and depreciation (screen/field per current release - verify).",
        proconnect_ref="Screen/field per current release - verify",
        efile_impact="None",
        affected_lines=["Sch E line 2", "Sch E 21", "Form 4562"],
        procedure_section="Schedule E - personal use days (sec. 280A)",
        notes="Bolton method (interest/taxes x 62/365) would free more operating expense; IRS method used per firm procedure - no "
              "2025 tax difference (standard deduction). Not a passive activity (sec. 469(j)(10)) - no 8582 for the cabin."),
    exc("EVG1008-SX5", "2", "State Allocation", "PA-40: compensation from W-2 box 16 (401k/403b taxable) and rents loss stays in its class",
        axcess_default="The draft PA return used federal W-2 box 1 as PA compensation and netted the rents-class loss against wages. "
                       "PA compensation must come from box 16 (elective deferrals are PA-taxable); if box 16 is blank or copied from box "
                       "1 on the W-2 input, the PA return understates compensation with no diagnostic.",
        axcess_diagnostic="None - silent",
        manual_calc="No",
        axcess_fix="W-2 inputs: PA state wages (box 16) $189,300 combined. PA rents class: duplex ($3,207) + cabin (PA - no sec. 280A "
                   "limit assumed) = loss ($7,711) - not netted against compensation (PA Schedule E / class-netting input - verify). "
                   "PA taxable income $189,682 x 3.07% = $5,823; withheld $5,812 -> due $11.",
        amount=189300,
        proconnect_default="Same - PA compensation follows the state wages entered on the W-2 screen.",
        proconnect_fix="W-2 screen: PA state wages = box 16; PA return rents class shows the loss with no offset (screen/field per "
                       "current release - verify).",
        proconnect_ref="Screen/field per current release - verify",
        efile_impact="PA-40 e-filed with the federal return",
        affected_lines=["PA-40 line 1a", "PA-40 line 6"],
        procedure_section="SALT Implications - Pennsylvania",
        notes="Local Manheim Twp EIT final return filed separately with LCTCB (not in either package's 1040 workflow)."),
]

TABS = {
    "5": [{"A": "Duplex - 128-130 Chestnut Row, Lancaster (Property A)", "B": "Y", "C": 9407, "D": 0,
           "F": "2025 loss 3,207 + PY unallowed 6,200 (2024 Form 8582 / PERM). MAGI 171,682 -> special allowance 0 -> all 9,407 "
                "suspended to 2026."}],
    "5cells": {"E23": 171682},
    "16": [
        {"A": "Cabin 27 Blue Heron Ln - mortgage interest (1098)", "B": 21, "C": 62, "F": 8300,
         "G": "IRS method 62/83 -> rental 6,200 (Sch E 12); personal 2,100 to Sch A worksheet (standard deduction used)."},
        {"A": "Cabin - real estate taxes", "B": 21, "C": 62, "F": 3320,
         "G": "IRS method -> rental 2,480 (Sch E 16); personal 840."},
        {"A": "Cabin - operating (utilities 2,490, insurance 1,660, repairs 830, supplies 415)", "B": 21, "C": 62, "F": 5395,
         "G": "Rental share 4,030; allowed 3,770 (income limit); carryover 260."},
        {"A": "Cabin - depreciation (MACRS 27.5 SL MM, $250,000 bldg, PIS 05/2025, full amount 5,682)", "B": 21, "C": 62, "F": 5682,
         "G": "Rental share 4,244; allowed 0; carryover 4,244 (sec. 280A(c)(5)). VRBO fees 1,190 + guest cleaning 1,240 are 100% "
              "rental (not allocated). Net Schedule E 0."},
    ],
}

CHECKS = {
    "'5. Passive Activity (8582)'!E13": 9407,
    "'5. Passive Activity (8582)'!E26": 71682,
    "'5. Passive Activity (8582)'!E28": 0,
    "'16. Vacation Home Allocation'!E12": 62 / 83,
    "'16. Vacation Home Allocation'!D12": 62 / 365,
    "'2. Diagnostics Log'!H16": 9407,
}
