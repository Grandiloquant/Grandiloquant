"""EVG1018 Vasquez - software exceptions (CCH Axcess workbook tabs 12, 13 + log items; ProConnect equivalents).
Amounts tie to the EVG1018 answer key (K-1 box 1 82,000 incl. 311(b) gain 20,000; distributions at FMV 72,000; ending stock
basis 101,750; QBI 74,200 -> 14,840; health insurance 7,800; condo basis 222,546 + 18,400 = 240,946)."""
from software_exceptions import exc

CLIENT_ID, DISPLAY = "EVG1018", "Elena Vasquez"
PREPARER, REVIEWER = "Staff preparer", "M. Osei (senior)"
INTRO = """
Two K-1s that are each wrong or incomplete as issued. Bayline's 1120-S omitted the IRC 311(b) gain on the truck it
distributed, so the K-1 must be entered differently from the form (with Form 8082) - and everything downstream (basis,
QBI) then has to be overridden consistently. The grandmother's trust's FINAL K-1 reports suspended passive losses in a
footnote that neither package can deduct and neither package tracks as a basis increase. All five items are silent.
"""

ITEMS = [
    exc("EVG1018-SX1", "2", "Other", "S corp K-1 omits the IRC 311(b) gain on the distributed truck - report inconsistently with Form 8082",
        axcess_default="Entering the K-1 as issued (box 1 $62,000; box 16D property distribution at book value $12,000) gives no gain. "
                       "Axcess has no way to know the corporation distributed appreciated property.",
        axcess_diagnostic="None - silent",
        manual_calc="Yes",
        axcess_fix="Income/Deductions > S Corporation Passthrough: box 1 ordinary income $82,000 (62,000 + 1245 recapture 20,000 = FMV 32,000 - "
                   "adjusted basis 12,000; accumulated depreciation 33,000 > gain); property distribution at FMV $32,000 (16D total $72,000). "
                   "Prepare Form 8082 (inconsistent treatment) identifying box 1 and 16D; e-file compatible. Gulfside agreed 09/02/2026 to "
                   "amend the 1120-S (follow-up 11/15/2026).",
        amount=20000,
        proconnect_default="Same - ProConnect uses the K-1 amounts entered; Form 8082 must be added for the inconsistent position.",
        proconnect_fix="S Corp Info (1120S K-1): ordinary income 82,000; distributions 72,000 (property at FMV); add Form 8082 "
                       "(screen per current release - verify).",
        efile_impact="Form 8082 attached (e-file compatible)",
        affected_lines=["8 (Schedule 1 line 5)", "Schedule E Part II", "Form 8082"],
        procedure_section="Schedules K-1",
        notes="IRC 311(b) / 1371(a): the corporation is treated as selling the property at FMV; Elena's basis in the truck = $32,000 (301(d))."),
    exc("EVG1018-SX2", "12", "Basis/At-Risk/Passive", "Form 7203 ordering with a property distribution - gain first, distribution at FMV",
        axcess_default="With the K-1 as issued the basis worksheet reduces stock basis by the book value ($12,000) and never adds the 311(b) "
                       "gain; if only the distribution is corrected to FMV without the gain, a phantom excess-distribution capital gain can "
                       "appear. Both are silent results of the inputs.",
        axcess_diagnostic="None - silent",
        manual_calc="Yes",
        axcess_fix="S Corporation Passthrough > Basis Limitation section: beginning stock basis $95,000 (debt basis $0); increases $83,150 "
                   "(box 1 82,000 incl. gain + interest 1,150) -> $178,150; distributions at FMV $72,000 (cash 40,000 + truck 32,000) "
                   "-> no excess; then nondeductible expenses and charitable item -> ending $101,750. Form 7203 attached.",
        amount=72000,
        proconnect_default="Form 7203 is produced because there is a distribution; ProConnect requires 'Stock basis at beginning of year' "
                           "(diagnostic ref 56844 if missing).",
        proconnect_fix="S Corp Info (1120S K-1) > Shareholder's Basis (7203): stock basis at beginning of year 95,000; distributions 72,000 "
                       "(at FMV); confirm no gain and ending basis 101,750.",
        proconnect_ref="Intuit help: 'How to complete Form 7203 and resolve diagnostic 56844 in ProConnect Tax'",
        efile_impact="None (Form 7203 attached)",
        affected_lines=["Form 7203", "Schedule D (none)"],
        procedure_section="Schedules K-1 - S corp basis"),
    exc("EVG1018-SX3", "2", "Other", "QBI from K-1 Statement A omits the 1245 recapture; reduce for 2% shareholder health insurance",
        axcess_default="Section 199A amounts come from the K-1 Statement A input (QBI $62,000), which does not change when box 1 is "
                       "overridden to $82,000. The QBI reduction for the Schedule 1 line 17 deduction attributable to the S corp must also "
                       "be reflected (verify whether the current release applies it automatically).",
        axcess_diagnostic="None - silent",
        manual_calc="Yes",
        axcess_fix="S Corporation Passthrough > Section 199A: QBI $82,000 (1245 recapture is ordinary trade-or-business income) less 2% "
                   "shareholder health deduction $7,800 = $74,200; W-2 wages $310,000 / UBIA $180,000 (not limiting - TI before QBI "
                   "$149,250 < $197,300). Deduction 20% = $14,840.",
        amount=14840,
        proconnect_default="Same - QBI comes from the 199A fields entered from Statement A.",
        proconnect_fix="S Corp Info (1120S K-1) > Qualified Business Income (199A): QBI 82,000; confirm the SE health insurance adjustment "
                       "reduces QBI to 74,200 (field per current release - verify).",
        efile_impact="None",
        affected_lines=["13a", "Form 8995"],
        procedure_section="QBI (QOFs, QROFs)"),
    exc("EVG1018-SX4", "13", "Basis/At-Risk/Passive", "Trust's final K-1: $18,400 suspended passive losses are a basis step-up, not a deduction",
        axcess_default="If the footnote's suspended PAL ($18,400) is keyed as a final-year deduction or a Schedule E loss on the K-1 (1041) "
                       "input, Axcess deducts it. Axcess has no field that adds it to the basis of the distributed condo - that basis lives "
                       "outside the return until the property is placed in service.",
        axcess_diagnostic="None - silent",
        manual_calc="Yes",
        axcess_fix="K-1 (Form 1041) input: enter only interest $420, dividends $1,380 ($1,100 qualified) and box 11 code E LT capital loss "
                   "carryover $3,200 (Schedule D line 14; $200 carries to 2026). No PAL deduction (IRC 469(j)(12)). Record condo basis "
                   "$222,546 + $18,400 = $240,946 in PERM; 2026 Rental input: continue trust's 27.5-yr schedule on carryover building "
                   "basis $174,546 and add the $14,431 increase as a new asset (assumption flagged).",
        amount=18400,
        proconnect_default="Same - suspended losses from a trust footnote are not deductible and must not be entered as a K-1 loss.",
        proconnect_fix="Trust K-1 (1041) input: no passive loss entry; Schedule D capital loss carryover 3,200 via the K-1 final-year field; "
                       "basis memo for the 2026 rental asset entries (screen/field per current release - verify).",
        efile_impact="None",
        affected_lines=["Schedule E (no loss)", "Schedule D line 14", "PERM basis record"],
        procedure_section="Schedules K-1 - trust final K-1",
        notes="Use only the FINAL K-1 (08/21/2026); the June DRAFT ($410 interest) is superseded."),
    exc("EVG1018-SX5", "2", "Other", "2% shareholder health insurance in W-2 box 14 - deduction needs its own input",
        axcess_default="W-2 box 14 text ('2% SH HLTH 7,800') is informational; nothing flows to Schedule 1 line 17 from it. Without the "
                       "separate self-employed health insurance entry linked to the S corp, the premiums stay taxed as wages.",
        axcess_diagnostic="None - silent",
        manual_calc="No",
        axcess_fix="Adjustments > Self-Employed Health Insurance: $7,800, linked to Bayline (more-than-2% shareholder; premiums in box 1, not "
                   "boxes 3/5 - confirmed). Limited to Bayline wages $90,000 (verify field path in current release).",
        amount=7800,
        proconnect_default="Same - box 14 amounts do not create the deduction by themselves.",
        proconnect_fix="Adjustments to Income > Self-employed health insurance: 7,800, linked to the S corporation (field per current "
                       "release - verify).",
        efile_impact="None",
        affected_lines=["10 (Schedule 1 line 17)"],
        procedure_section="Schedules K-1 - 2% shareholder fringe benefits",
        notes="Notice 2008-1."),
]

TABS = {
    "12": [{"A": "Elena Vasquez - Bayline Marine Services, Inc. (100%)", "B": 95000, "C": 0, "D": 83150, "E": 72000,
            "G": "Income 83,150 = box 1 82,000 (incl. 311(b) / 1245 gain 20,000) + interest 1,150 -> 178,150 before distributions. "
                 "Distributions at FMV: cash 40,000 + truck 32,000 = 72,000 -> no excess. Then nondeductible + charity -> ending 101,750."}],
    "13": [{"A": "Rosa M. Delgado Trust - Clearwater FL condo (Gulf Palms 12B) distributed 09/15/2025", "B": 222546, "C": 18400, "E": "Y",
            "F": "Final K-1 08/21/2026. Carryover basis (643(e), no 643(e)(3) election) + suspended PAL 18,400 (469(j)(12)) = 240,946. "
                 "Not deductible by anyone. Building basis 174,546 + increase 14,431 (assumption: new 27.5-yr asset from 2026)."}],
}

CHECKS = {
    "'12. S-Corp Dual Basis'!F15": 0,
    "'13. Trust Termination PAL'!D12": 240946,
}
