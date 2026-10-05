"""EVG1009 Jensen - software exceptions (workbook tab 24 + log items; ProConnect equivalents).
Amounts tie to the EVG1009 answer key (inherited securities: DOD basis 409,233, gain 11,387 vs 1099-B-based 347,120; MSFT code B
adjustment (142,605); home: amount realized 633,227 - DOD basis 615,000 = 18,227 excluded (code H); spousal IRA transfer
418,903 not reportable; senior deduction 12,000)."""
from software_exceptions import exc

CLIENT_ID, DISPLAY = "EVG1009", "Harold Jensen (and Eleanor Jensen, deceased)"
PREPARER, REVIEWER = "T. Nguyen (staff)", "L. Chen (senior)"
INTRO = """
Year-of-death joint return in a community property state. The two biggest exceptions are basis items the software cannot
know: Schwab's 1099-B still shows original cost (and no basis on noncovered lots) although BOTH community halves were stepped up
to date-of-death value, and the home sale needs the DOD appraisal plus a code-H exclusion. Both are one-off, fact-intensive events,
logged on tab 24 with the DOD valuation and appraisal as the supporting workpapers. The rest are AutoFlow / setup traps.
"""

ITEMS = [
    exc("EVG1009-SX1", "24", "Capital Loss", "Inherited community-property securities - 1099-B shows original cost; noncovered lots no basis",
        axcess_default="AutoFlow brought in the Schwab 1099-B as reported: MSFT covered lot basis $13,500 (original cost), VFIAX and JNJ "
                       "noncovered with no basis -> Schedule D gain $347,120 (or $179,254 if only Eleanor's half were stepped up). "
                       "Axcess has no way to know the account was community property or that a death occurred.",
        axcess_diagnostic="None - silent",
        manual_calc="Yes",
        axcess_fix="Gains and Losses > Form 8949: MSFT (box D) keep 1099-B basis $13,500, adjustment code B, column (g) -142,605 -> basis "
                   "$156,105; VFIAX and JNJ (box E) basis = DOD FMV $222,048 and $31,080; date acquired 'INHERITED' (long-term, sec. "
                   "1223(9)). Total DOD basis $409,233; gain $11,387. Attach the step-up schedule.",
        amount=11387,
        proconnect_default="Same - ProConnect computes gain from the basis entered on the Dispositions screen.",
        proconnect_fix="Dispositions (Schedule D/4797) screen: enter DOD basis per lot, code B adjustment for the covered MSFT lot, "
                       "long-term / inherited acquisition designation (field per current release - verify).",
        proconnect_ref="Field per current release - verify",
        efile_impact="None",
        affected_lines=["7", "Form 8949 boxes D/E", "Sch D"],
        procedure_section="Estate Implications - step-up in basis (community property)",
        notes="Sec. 1014(b)(6): survivor's half of community property also takes DOD basis. DOD 08/09/2025 was a Saturday - mean of "
              "08/08 and 08/11 values (Reg. 20.2031-2(b)). Avoids a WA capital gains excise filing."),
    exc("EVG1009-SX2", "24", "Other", "Sale of the marital home (1099-S) - DOD appraisal basis and sec. 121 exclusion, code H",
        axcess_default="The home-sale worksheet computes gain from the basis keyed; if basis is taken from the PERM / client records "
                       "(1998 cost + improvements $295,000) and the exclusion is limited to $250,000, "
                       "the return would show $88,227 of gain. If the sale is omitted because it is "
                       "'excluded', the 1099-S goes unmatched. Axcess cannot know about the community-property step-up.",
        axcess_diagnostic="None - silent",
        manual_calc="Yes",
        axcess_fix="Sale of principal residence input (Form 8949 box F, code H): gross proceeds $685,000 (ties to 1099-S), selling "
                   "expenses $51,773, basis $615,000 (retrospective DOD appraisal - full step-up), gain $18,227, sec. 121 exclusion "
                   "$18,227 (MFJ $500,000 limit; ownership/use since 1998). Net $0.",
        amount=-18227,
        proconnect_default="Same - basis and exclusion are computed from the inputs on the home-sale worksheet.",
        proconnect_fix="Sale of home (Form 8949 code H) inputs: proceeds $685,000, expenses $51,773, basis $615,000, exclusion applies "
                       "(screen/field per current release - verify).",
        proconnect_ref="Screen/field per current release - verify",
        efile_impact="None",
        affected_lines=["Form 8949 box F", "7"],
        procedure_section="Estate Implications - sale of a home received from an estate; Schedule D code H"),
    exc("EVG1009-SX3", "2", "Other", "Vanguard spousal 'transfer out' AutoFlowed as an IRA distribution",
        axcess_default="AutoFlow read Eleanor's Vanguard IRA statement ('transfer out $418,902.66') as a distribution and created a "
                       "line 4a/4b entry. There is no 1099-R for a direct trustee-to-trustee transfer to the surviving spouse's own IRA.",
        axcess_diagnostic="None - silent",
        manual_calc="No",
        axcess_fix="Delete the AutoFlowed distribution; tickmark the statement 'spousal transfer - not reportable'. Only Harold's own "
                   "$10,000 withdrawal (1099-R, 10% withheld) remains on lines 4a/4b.",
        amount=0,
        proconnect_default="No AutoFlow equivalent in the firm's ProConnect workflow; the error occurs only if the statement is keyed.",
        proconnect_fix="Enter only actual 1099-Rs; nothing for the transfer.",
        efile_impact="None",
        affected_lines=["4a", "4b"],
        procedure_section="Client IRAs / inherited IRA",
        notes="Harold's first RMD year is 2026 and will include the former inherited balance."),
    exc("EVG1009-SX4", "2", "Other", "Year-of-death filing status: MFJ, not 'qualifying widower' (organizer + procedure wording)",
        axcess_default="The organizer and the firm procedure say 'qualifying widower'. Axcess prepares whatever filing status is "
                       "selected; the QSS dependent-child and 'two years after death' tests are preparer determinations.",
        axcess_diagnostic="Not relied on - verify whether the current release flags QSS without a qualifying child",
        manual_calc="No",
        axcess_fix="General > Basic Data: filing status MFJ; spouse date of death 08/09/2025 (prints 'DECEASED' and the surviving-spouse "
                   "signature). No Form 1310 (no refund claimed by a non-spouse). PERM: 2026 status Single (no dependent child).",
        amount=0,
        proconnect_default="Same - filing status is an input; enter the spouse's date of death on the General/taxpayer information screen.",
        proconnect_fix="General > Filing Status: MFJ; spouse date of death 08/09/2025 (screen/field per current release - verify).",
        proconnect_ref="Screen/field per current release - verify",
        efile_impact="None (MFJ with deceased spouse e-files normally)",
        affected_lines=["Filing status", "12e"],
        procedure_section="Review - Filing Status (spouse deceased)",
        notes="Procedure wording is imprecise - follow sec. 6013(a)(2) / sec. 2(a)."),
    exc("EVG1009-SX5", "2", "Other", "Schedule 1-A senior deduction for the deceased spouse",
        axcess_default="The first draft showed the senior deduction for Harold only ($6,000). Once the spouse's date of death is entered, "
                       "confirm the software still counts Eleanor (65+ at death, valid SSN) on Schedule 1-A Part V - the draft result "
                       "suggests it did not (verify current-release logic).",
        axcess_diagnostic="None - silent",
        manual_calc="No",
        axcess_fix="Schedule 1-A senior deduction input: both spouses 65+ (verify field / override in current release). MAGI $95,881 < "
                   "$150,000 -> 2 x $6,000 = $12,000, allowed in addition to itemizing ($52,845).",
        amount=12000,
        proconnect_default="Same check - confirm both spouses are counted when a date of death is entered.",
        proconnect_fix="Verify Schedule 1-A Part V shows two qualifying individuals; override if needed and document "
                       "(field per current release - verify).",
        proconnect_ref="Intuit help: 'Using overrides and adjustments in ProConnect Tax' (document overrides)",
        efile_impact="None",
        affected_lines=["13b", "Schedule 1-A Part V"],
        procedure_section="OBBBA - senior deduction (Schedule 1-A Part V)"),
]

TABS = {
    "24": [
        {"A": "Community-property basis step-up (sec. 1014(b)(6)) - inherited securities",
         "B": "Eleanor died 08/09/2025 (WA community property agreement). Schwab 1099-B: MSFT 300 sh covered, basis $13,500 "
              "(original); VFIAX 400 sh and JNJ 200 sh noncovered, no basis. DOD values: 156,105 / 222,048 / 31,080 = 409,233. "
              "Proceeds 420,620 -> LTCG 11,387 (vs 347,120 on 1099-B basis).",
         "C": "WP 8 (Schwab 1099-B) / WP 9 (Schwab DOD valuation report) / step-up schedule attached to return",
         "D": 11387,
         "E": "Gains and Losses > Form 8949: box D code B adj (142,605) for MSFT; box E basis = DOD FMV; acquired INHERITED",
         "F": "T. Nguyen 04/2026 / reviewed L. Chen"},
        {"A": "Sale of principal residence received partly from decedent (sec. 121, code H)",
         "B": "Sold 12/12/2025 for 685,000 (1099-S); selling costs 51,773; basis = DOD appraisal 615,000 (both halves stepped up); "
              "gain 18,227 fully excluded (MFJ $500,000; owned/used since 1998).",
         "C": "WP 10 (1099-S) / WP 11 (seller settlement statement) / WP 12 (retrospective appraisal as of 08/09/2025)",
         "D": -18227,
         "E": "Sale of principal residence input -> Form 8949 box F, code H",
         "F": "T. Nguyen 04/2026 / reviewed L. Chen"},
    ],
}

CHECKS = {
    "'24. Rare-Event Log'!D11": 11387,
    "'24. Rare-Event Log'!D12": -18227,
    "'2. Diagnostics Log'!H14": 11387,
    "'2. Diagnostics Log'!H18": 12000,
}
