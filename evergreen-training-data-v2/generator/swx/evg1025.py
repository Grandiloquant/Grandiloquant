"""EVG1025 Brennan-Ochoa - software exceptions (CCH Axcess workbook tabs 22, 24 + log items; ProConnect equivalents).
Amounts tie to the EVG1025 answer key: section 962 tax 2,286 on line 16 (tested income 400,000; gross-up 57,143; IRC 250 50%;
deemed-paid credit 45,714); IRC 356 boot gain 300,000; IRC 331 loss (35,000); IRC 1259 gain 150,000; Form 1042-S withholding 3,600
(line 25c, paper filing)."""
from software_exceptions import exc

CLIENT_ID, DISPLAY = "EVG1025", "Victor & Lena Brennan-Ochoa"
PREPARER, REVIEWER = "P. Nwosu (staff)", "D. Morgan (manager)"
INTRO = """
Three shareholder-level stock events that no broker statement computes correctly (merger boot, a corporate liquidation reported
only on a 1099-DIV, and a constructive sale with no 1099-B), a CFC whose GILTI is taxed under a section 962 election that both
packages handle only through an outside computation, and a Form 1042-S that forces a paper return. The ProConnect tier does not
matter here - the Advanced/Elite bundles have the same form coverage as the other tiers; they only change return counts and users.
"""

ITEMS = [
    exc("EVG1025-SX1", "24", "Other", "Section 962 election - GILTI tax computed outside the 1040 engine, $2,286 on line 16",
        axcess_default="If the Form 8992 GILTI inclusion ($400,000) is entered as income, Axcess taxes it at individual ordinary rates with no "
                       "section 250 deduction and no deemed-paid credit - about $125,391 more income tax. The 1040 engine does not "
                       "compute the corporate-rate 962 tax or the IRC 960(d) credit.",
        axcess_diagnostic="None - silent",
        manual_calc="Yes",
        axcess_fix="International specialist workpaper (workbook tab 24): (400,000 + 57,143 gross-up) - 50% IRC 250 = 228,571.50 x 21% = "
                   "48,000 - 80% deemed-paid credit 45,714 = 2,286. Do not carry the 951A inclusion to Schedule 1 (not in AGI under the "
                   "election - presentation assumption to verify). Enter 2,286 as additional tax included on Form 1040 line 16 with the "
                   "962 election statement and pro-forma 1120/1118 attached (Taxes > other tax / line 16 adjustment - verify field path "
                   "in current release); document the override amount.",
        amount=2286,
        proconnect_default="ProConnect does not compute the section 962 tax; Form 1118 is not available.",
        proconnect_fix="Practitioner workaround (verify): prepare the pro-forma 1120/1118/8992/8993 outside the software and enter the computed "
                       "962 tax on screen 45.3 (Other Taxes) through the 'Section 962 tax' adjustment. Community guidance describes it as a "
                       "NEGATIVE adjustment where the inclusion has been entered as income, so that net tax equals the 962 computation. For "
                       "this return the inclusion is not entered as income; confirm the sign convention so line 16 = regular tax 86,955 + "
                       "2,286 = 89,241 and attach the statement as a PDF.",
        proconnect_ref="Intuit Accountants Community thread on section 962 election / Form 8992 (practitioner workaround - verify)",
        efile_impact="Return is paper filed anyway (see SX6); statement and pro-forma forms attached to the paper return",
        affected_lines=["16", "Line 16 statement", "Form 8992", "Form 8993"],
        procedure_section="Foreign Corps",
        notes="Override amount documented per Intuit 'Using overrides and adjustments in ProConnect Tax'. Future PTEP distributions taxable "
              "under IRC 962(d) to the extent they exceed 962 tax paid."),
    exc("EVG1025-SX2", "24", "Other", "Form 5471 (Cat 4/5), Form 8992 / 8993 and pro-forma Form 1118 - specialist workpaper, not the 1040 engine",
        axcess_default="The 1040 module prepares the information returns only from what is keyed into the 5471/8992/8993 inputs; the GILTI "
                       "high-tax test, tested income, QBAI and the 962 deemed-paid credit (Form 1118 is a corporate form) are not "
                       "computed from the Irish accountants' package.",
        axcess_diagnostic="Completeness diagnostics only for keyed 5471/8992 inputs (gist - verify); the GILTI/962 amounts "
                          "themselves are not tested",
        manual_calc="Yes",
        axcess_fix="Key Form 5471 Categories 4 and 5 (Schedules C, E, F, H, I-1, J, P, Q, R, M) and Form 8992 Schedule A from the "
                   "re-performed Kinsale & Murphy package (tested income 400,000; QBAI 0; tested foreign income taxes 57,143). Form 8993 "
                   "and the pro-forma 1118 are part of the 962 statement (tab 24, row 2). No Form 926 (no 2025 transfers).",
        amount=400000,
        proconnect_default="Form 1118 is not available in ProConnect; practitioners prepare pro-forma 1120/1118/8992/8993 for the 962 election.",
        proconnect_fix="Prepare the 962 pro-forma set outside ProConnect; whether ProConnect's Form 5471 output is adequate for Categories 4/5 "
                       "is not relied on - verify in the current release or prepare 5471 in the firm's international software and attach "
                       "to the paper return.",
        proconnect_ref="Intuit Accountants Community thread on section 962 election / Form 8992",
        efile_impact="Attached to the paper return",
        affected_lines=["Form 5471", "Form 8992", "Form 8993", "Form 8938 Part IV"],
        procedure_section="Foreign Corps",
        notes="Form 8938 also filed: CFC stock is a specified foreign financial asset, excepted because reported on Form 5471."),
    exc("EVG1025-SX3", "22", "Capital Loss", "Merger cash boot - exchange agent 1099-B: $300,000 proceeds, no basis, no acquisition date",
        axcess_default="Axcess imports the 1099-B with blank basis and blank date acquired. Missing basis is treated as zero, so the gain is "
                       "$300,000 - numerically right only by coincidence - but with no acquisition date the term is not established and "
                       "the IRC 356 support is missing. The common manual 'fix' (basis 200,000 -> gain 100,000) is wrong.",
        axcess_diagnostic="Possibly an informational missing-basis / date-acquired message (gist - verify); the $300,000 gain itself "
                          "calculates without any IRC 356 check",
        manual_calc="Yes",
        axcess_fix="Workbook tab 22 (Reorg Boot row): realized 1,000,000; recognized = lesser of boot or realized = 300,000; Clark -> capital. "
                   "Capital Gains worksheet: date acquired 03/15/2012, basis 0 entered explicitly, long-term, box E, statement attached. "
                   "Record Meridian basis 200,000 ($20/share) in the client's basis schedule.",
        amount=300000,
        proconnect_default="Same - blank basis treated as zero; term needs the acquisition date.",
        proconnect_fix="Dispositions: enter the transaction with date acquired 03/15/2012, cost 0, long-term, box E, and attach the IRC 356 "
                       "statement (screen/field per current release - verify).",
        efile_impact="None (return paper filed for SX6)",
        affected_lines=["7", "Form 8949 box E"],
        procedure_section="Schedule D"),
    exc("EVG1025-SX4", "22", "Capital Loss", "VBO Holdings liquidation - 1099-DIV box 9 creates no Form 8949 line",
        axcess_default="Box 9 (cash liquidation distributions) is informational on the dividend input - Axcess cannot know Victor's stock "
                       "basis, so no gain/loss is computed. If keyed as box 1a it becomes an $85,000 dividend. Either way the $35,000 "
                       "IRC 331 loss is missing.",
        axcess_diagnostic="None - silent",
        manual_calc="Yes",
        axcess_fix="Workbook tab 22 (Liquidation row). Capital Gains worksheet: VBO Holdings, Inc., acquired 05/09/2016, sold 11/14/2025, "
                   "proceeds 85,000, cost 120,000 -> (35,000) LT, box F.",
        amount=-35000,
        proconnect_default="Same - the 1099-DIV box 9 entry does not create a disposition.",
        proconnect_fix="Dispositions: add the liquidation as a sale (proceeds 85,000, cost 120,000, LT, box F) (screen/field per current release "
                       "- verify).",
        efile_impact="None",
        affected_lines=["7", "Form 8949 box F"],
        procedure_section="Schedule D"),
    exc("EVG1025-SX5", "22", "Capital Loss", "Constructive sale (IRC 1259) - short against the box with no 2025 1099-B",
        axcess_default="Nothing is reported for 2025: the short sale is reported on a 1099-B only in 2026 when closed. Axcess has no "
                       "information that a constructive sale occurred - $150,000 of 2025 gain is omitted. In 2026 the 1099-B will show "
                       "unknown basis and the same gain would be taxed again.",
        axcess_diagnostic="None - silent",
        manual_calc="Yes",
        axcess_fix="Workbook tab 22 (Constructive Sale row). Capital Gains worksheet: Meridian 2,000 sh, acquired 03/15/2012 (tacked), "
                   "transaction date overridden to the constructive-sale date 12/10/2025, proceeds 190,000, cost 40,000 -> 150,000 LT, "
                   "box F. 2026 proforma note: basis of the 2,000 shares 190,000 (code B adjustment).",
        amount=150000,
        proconnect_default="Same - no 2025 document; nothing reported unless entered manually.",
        proconnect_fix="Dispositions: enter the deemed sale (date sold 12/10/2025, proceeds 190,000, cost 40,000, LT, box F) with an "
                       "explanatory statement; carry the $95/share basis to 2026 (screen/field per current release - verify).",
        efile_impact="None",
        affected_lines=["7", "Form 8949 box F"],
        procedure_section="Schedule D"),
    exc("EVG1025-SX6", "PC", "E-file Disqualifying", "Form 1042-S withholding on a U.S. citizen's 1040 - paper filing required",
        axcess_default="Axcess: verify MeF support for claiming Form 1042-S withholding on a Form 1040; firm policy is paper filing with "
                       "the 1042-S copy attached. The dividends must be keyed as ordinary/qualified dividends (no 1099-DIV was issued).",
        axcess_diagnostic="None - silent",
        manual_calc="No",
        axcess_fix="Dividends input: Atlas Clearing 12,000 ordinary / 12,000 qualified; withholding input: 3,600 federal tax withheld from "
                   "Form 1042-S -> line 25c (verify field path in current release). Mark the return for paper filing; attach the 1042-S.",
        amount=3600,
        proconnect_default="Form 1042-S is not supported in the e-file of Form 1040 (only 1040-NR supports 1042-S) - per Intuit, "
                           "returns claiming 1042-S withholding must be paper filed.",
        proconnect_fix="Enter the 1042-S dividends and withholding, suppress e-file and paper file the 1040 with a copy of the 1042-S attached. "
                       "Client to give the broker a Form W-9.",
        proconnect_ref="Intuit help: e-file diagnostic Ref 47040/47039/47310 for Form 1042-S",
        efile_impact="Paper filing required (ProConnect); firm policy paper in Axcess as well",
        affected_lines=["3a", "3b", "25c"],
        procedure_section="Paper Filing Returns"),
    exc("EVG1025-SX7", "2", "Other", "FBAR / Schedule B line 7a - CFC's Irish bank account (financial interest + signature authority)",
        axcess_default="Schedule B Part III and the FBAR are driven by the foreign-account questions and FBAR inputs; with no 1099 for the "
                       "account the software has nothing to trigger them. The proforma (prior preparer) answer 'No' carries forward.",
        axcess_diagnostic="None - silent",
        manual_calc="No",
        axcess_fix="General > foreign accounts question: Yes; country Ireland. FBAR (FinCEN 114) filed separately through BSA E-Filing - "
                   "AIB ****4471, max EUR 310,000, owner Ochoa Engineering Ltd. (Victor > 50% owner and signatory).",
        amount="EUR 310,000 max",
        proconnect_default="Same - question-driven; ProConnect does not file the FBAR.",
        proconnect_fix="Schedule B foreign account question = Yes / Ireland; FBAR filed through BSA E-Filing outside the return "
                       "(screen/field per current release - verify).",
        efile_impact="None (FBAR filed separately)",
        affected_lines=["Sch B line 7a/7b", "FinCEN 114"],
        procedure_section="FinCEN114/FBAR",
        notes="Prior-year (2022-2024) FBARs not filed by the prior preparer - delinquent FBAR procedures (separate engagement)."),
]

TABS = {
    "22": [{"A": "Gulf Coast Dental Labs, Inc. -> Meridian Dental Holdings (Lena, 1,800 sh)", "B": "Reorg Boot", "C": "06/20/2025",
            "D": 200000, "E": 300000, "F": 300000, "G": "Capital (LT) - Clark: not dividend-equivalent",
            "H": "Realized 1,000,000 (900,000 stock + 300,000 cash - 200,000 basis); recognized = boot 300,000. Meridian basis 200,000 "
                 "($20/sh); holding period from 03/15/2012. 1099-B shows proceeds only."},
           {"A": "VBO Holdings, Inc. (Victor, 100%)", "B": "Liquidation", "C": "11/14/2025", "D": 120000, "E": 85000, "F": -35000,
            "G": "Capital (LT) - held since 05/2016", "H": "1099-DIV box 9 cash liquidation distribution 85,000; IRC 331 exchange."},
           {"A": "Meridian Dental Holdings - short against the box (Lena, 2,000 sh)", "B": "Constructive Sale", "C": "12/10/2025",
            "D": 40000, "E": 190000, "F": 150000, "G": "Capital (LT) - holding period tacks to 2012",
            "H": "Short 2,000 @ $95 vs long basis $20; closed 03/15/2026 (> 30 days after year end) -> IRC 1259 applies. New basis $95."}],
    "24": [{"A": "GILTI - section 962 election (Ochoa Engineering Ltd., Ireland, CFC 100%)",
            "B": "Tested income 400,000 (Irish tax 57,143 at 12.5%); QBAI 0; GILTI 400,000 + 78 gross-up 57,143 = 457,143 - 50% IRC 250 = "
                 "228,571.50 x 21% = 48,000 - 80% deemed-paid credit 45,714 = 2,286. Inclusion not in AGI.",
            "C": "WP 962 (pro-forma 1120/1118/8992/8993); PBC/14 Kinsale & Murphy package", "D": 2286,
            "E": "Line 16 additional tax (962) with statement - verify field path", "F": "P. Nwosu 09/18/2026 / D. Morgan"},
           {"A": "Form 5471 Cat 4/5 + 8992 + 8993 (information returns)",
            "B": "Keyed from the re-performed package; no Form 926 (no 2025 transfers); Form 8938 Part IV lists 1 Form 5471.",
            "C": "WP 5471", "D": 400000, "E": "Form 5471 / 8992 / 8993 inputs", "F": "P. Nwosu 09/18/2026 / D. Morgan"}],
}

CHECKS = {
    "'22. Reorg, Liquidation, 1244'!F15": 300000,
    "'22. Reorg, Liquidation, 1244'!F16": -35000,
    "'22. Reorg, Liquidation, 1244'!F17": 150000,
    "'24. Rare-Event Log'!D11": 2286,
}
