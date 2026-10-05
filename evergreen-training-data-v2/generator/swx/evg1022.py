"""EVG1022 Whitfield - software exceptions (CCH Axcess workbook tabs 23, 7, 18, 17, 14, 10, 8 + log items; ProConnect equivalents).
Amounts tie to the EVG1022 answer key: MA-source wages 44,727 (410,000 x 18/165); PA Schedule G-L credit 1,373; NUA taxable
96,000 (box 6 544,000 deferred); wash sale code W 18,000; ABP 786.12 + accrued interest 2,981.94; carryover ST 26,000 / LT 12,000;
Form 2210 required annual payment 126,067 vs 137,769 paid (no penalty); PA net gains 47,000."""
from software_exceptions import exc

CLIENT_ID, DISPLAY = "EVG1022", "Gregory & Ellen Whitfield"
PREPARER, REVIEWER = "D. Moreau (senior staff)", "M. Osei (manager)"
INTRO = """
A new client with a retiring mobile executive. Almost everything here is **silent** in both packages: the software calculates
exactly what the documents say, and the documents are incomplete or misleading - a W-2 that codes 100% of wages to Pennsylvania,
a 1099-B that cannot see a spouse's IRA purchase, a 1099-R whose box 6 is easy to skip, a consolidated 1099 whose accrued interest
lives only on a supplemental page, and a prior preparer's capital loss carryover with the wrong character. Neither CCH Axcess nor
ProConnect has a prior-year proforma for a new client, so every carryover is a manual entry. ProConnect's higher bundles
(Advanced/Elite) have the same form coverage - the tier changes return counts and users only.
"""

ITEMS = [
    exc("EVG1022-SX1", "23", "State Allocation", "Single PA-coded W-2 for a mobile executive - MA workday allocation",
        axcess_default="The W-2 worksheet carries box 15/16 exactly as keyed: one PA row with $441,000 of state wages. Axcess has no work "
                       "location data, so it produces only the PA resident return - no Massachusetts nonresident return and no MA-source "
                       "wages.",
        axcess_diagnostic="None - silent",
        manual_calc="Yes",
        axcess_fix="Wages, Salaries, Tips (W-2) worksheet > state/local section: add a multi-state allocation row - MA wages $44,727 "
                   "(410,000 x 18/165 workdays) - and activate the MA nonresident return (Form 1-NR/PY). Keep the PA row at box 16 "
                   "($441,000; PA taxes residents on all compensation). Verify field path in current release.",
        amount=44727,
        proconnect_default="Same - the W-2 screen's state section reflects only what is keyed; with one PA row only PA is generated.",
        proconnect_fix="Wages, Salaries, Tips > W-2 > State and local information: add a second state line for MA with state wages $44,727 "
                       "(state withholding 0) and generate the MA nonresident return (screen/field per current release - verify).",
        efile_impact="None - PA and MA both e-filed",
        affected_lines=["MA 1-NR/PY (MA-source wages)", "PA-40 Schedule G-L"],
        procedure_section="SALT Implications - New State Filing Requirements",
        notes="Workdays from the Outlook export: PA 112, NJ 22, MA 18, IL 13 = 165 (4 holidays + 4 PTO excluded). Massachusetts uses the "
              "working-day ratio for nonresident employees."),
    exc("EVG1022-SX2", "2", "State Allocation", "NJ reciprocity and Illinois 30-day threshold - do NOT generate NJ/IL returns",
        axcess_default="If the preparer allocates by days to every state on the log (adds NJ and IL W-2 state rows), Axcess generates an "
                       "NJ-1040NR and an IL-1040 with Schedule NR and pushes resident credits to the PA return. Nothing in the software "
                       "knows the PA-NJ reciprocal agreement or the Illinois 30-working-day nonresident employee threshold.",
        axcess_diagnostic="None - silent",
        manual_calc="No",
        axcess_fix="No NJ or IL state rows on the W-2 worksheet; leave the NJ/IL returns inactive. Document on the Diagnostics Log and tab 23 "
                   "notes: NJ 22 days - reciprocity (PA only); IL 13 days <= 30 - not IL-source (assumption to verify; IL tax at stake "
                   "about $1,599).",
        amount=0,
        proconnect_default="Same - any state line keyed on the W-2 generates that state's nonresident return.",
        proconnect_fix="Do not add NJ/IL lines on the W-2 screen; if a state was activated, delete it in the state return list "
                       "(screen per current release - verify).",
        efile_impact="Avoids two unnecessary nonresident filings",
        affected_lines=["PA-40 Schedule G-L"],
        procedure_section="SALT Implications - New State Filing Requirements",
        notes="Workbook tab 23 note column records both rules."),
    exc("EVG1022-SX3", "7", "State Allocation", "PA resident credit (Schedule G-L) for MA tax - limited to PA tax on the MA income",
        axcess_default="When the MA tax paid is keyed as the 'tax paid to other state' on the PA credit input without the MA income, or the "
                       "credit is overridden to the MA tax, the full $2,191 is credited. PA limits the credit to the PA tax on the income "
                       "taxed by MA.",
        axcess_diagnostic="None - silent",
        manual_calc="Yes",
        axcess_fix="PA return > Resident credit (Schedule G-L) input: income taxed by MA $44,727, MA tax $2,191; credit = MIN(2,191, "
                   "44,727 x 3.07% = 1,373) = $1,373 (override if the default differs). Tab 7 column G = PA tax before credit $17,821; "
                   "column B = PA taxable income $580,485 so G x D = PA tax on the MA income. Verify field path in current release.",
        amount=1373,
        proconnect_default="Same - the PA credit for taxes paid to other states uses the income and tax entered for the other state.",
        proconnect_fix="Pennsylvania return > Credits > Credit for taxes paid to other states (Schedule G-L): MA income 44,727, MA tax "
                       "2,191; confirm the computed credit is $1,373 (screen/field per current release - verify).",
        efile_impact="None",
        affected_lines=["PA-40 line 22", "Schedule G-L"],
        procedure_section="SALT Implications",
        notes="Used the income MA actually taxed (box 1 based) rather than PA-measured wages incl. 401(k) deferrals - conservative."),
    exc("EVG1022-SX4", "18", "Other", "401(k) lump sum with employer stock in kind - NUA (only cost basis taxable)",
        axcess_default="Axcess taxes the 1099-R box 2a amount keyed. If the stock distribution is keyed with box 2a = box 1 ($640,000) or "
                       "'taxable amount not determined', and box 6 is skipped, the whole $640,000 is taxed on line 5b. With box 2a $96,000 "
                       "keyed correctly the federal result is right - the risk is purely input.",
        axcess_diagnostic="None - silent",
        manual_calc="Yes",
        axcess_fix="Income > Pensions, IRAs (1099-R) worksheet: distribution 1 - gross $640,000, taxable $96,000, box 6 NUA $544,000, code 2, "
                   "total distribution; distribution 2 - gross $780,000, taxable $0, code G (rollover). Tab 18: Box 1 - Box 6 = $96,000. "
                   "Set up the 8,000 KMDV shares in the client's basis records at $12.00/share. PA: mark the 1099-R as not PA-taxable "
                   "(retirement distribution after retirement) on the PA 1099-R input - verify field path in current release.",
        amount=96000,
        proconnect_default="Same - ProConnect taxes the taxable amount keyed; box 6 must be entered for the NUA to be carried.",
        proconnect_fix="Income > Pensions, Annuities (1099-R): enter both 1099-Rs - box 2a $96,000 and box 6 net unrealized appreciation "
                       "$544,000 on the stock distribution, code 2; the code G rollover with taxable $0 (field labels per current release - "
                       "verify). PA: exclude from PA income on the PA 1099-R/retirement income input.",
        efile_impact="None",
        affected_lines=["5a", "5b", "PA-40"],
        procedure_section="Client IRAs / retirement distributions",
        notes="Code 2 (separation from service in/after the year he turned 55) - no 10% tax, no Form 5329. Taxing the full FMV would cost "
              "$199,260 of additional federal tax (answer key what-if)."),
    exc("EVG1022-SX5", "17", "Capital Loss", "Cross-account wash sale - spouse's IRA bought the same ETF (Rev. Rul. 2008-5)",
        axcess_default="Schwab's 1099-B for Gregory's account shows the IVV sale with box 1g blank (the repurchase was in Ellen's IRA - a "
                       "different owner and account). Autoflow/keying the 1099-B as reported deducts the $18,000 loss.",
        axcess_diagnostic="None - silent",
        manual_calc="Yes",
        axcess_fix="Gains and Losses > Capital Gains and Losses (Form 8949) - IVV line: adjustment code W, adjustment amount +$18,000 "
                   "(loss disallowed). Do NOT increase any basis (IRA purchase - the loss is permanently lost).",
        amount=18000,
        proconnect_default="Same - the disposition is imported/keyed as reported; nothing cross-matches other accounts or a spouse's IRA.",
        proconnect_fix="Dispositions (Schedule D/4797) > the IVV transaction: adjustment code W, adjustment +18,000 (field labels per "
                       "current release - verify). No basis entry elsewhere.",
        efile_impact="None (four transactions - no 8949 summary/PDF attachment needed)",
        affected_lines=["7", "Form 8949 box A"],
        procedure_section="Schedule D - adjustment code W",
        notes="Evidence: Ellen's 02/24 email + Schwab IRA ****8831 Q4 statement (buy 420 sh IVV 11/20/2025)."),
    exc("EVG1022-SX6", "14", "Other", "Bond premium (box 11/13) and accrued interest paid at purchase",
        axcess_default="Scan/autoflow of the composite 1099 picks up box 1 ($12,640.55) and box 8 ($7,500). The accrued interest paid "
                       "($2,981.94) appears only on Schwab's supplemental page and the trade confirm - no 1099 box - so it is never "
                       "reversed. If box 11/13 are not captured in their fields, no ABP adjustment is made and line 2a stays at $7,500.",
        axcess_diagnostic="None - silent",
        manual_calc="Yes",
        axcess_fix="Interest Income (1099-INT) worksheet: box 11 bond premium $786.12 and box 13 $1,104.30 in their fields (ABP adjustment "
                   "line on Schedule B; line 2a $6,396); add a separate line 'Accrued interest' -$2,981.94. Line 2b $9,085.",
        amount=3768,
        proconnect_default="Same - the accrued interest is not on a 1099 box; box 11/13 must be keyed to be netted.",
        proconnect_fix="Income > Interest Income (1099-INT): enter box 11 and box 13 premium amounts in their fields and the accrued "
                       "interest as an adjustment line/'Accrued interest' (screen/field per current release - verify).",
        efile_impact="None",
        affected_lines=["2a", "2b"],
        procedure_section="Schedule B - accrued interest; Scan - consolidated 1099",
        notes="Override amount = 786.12 + 2,981.94 reduction of taxable interest."),
    exc("EVG1022-SX7", "10", "Capital Loss", "New client - prior preparer's capital loss carryover had the wrong character",
        axcess_default="No proforma for a new client. Keying the prior preparer's worksheet ($38,000 long-term) is accepted without question; "
                       "Axcess then nets the $5,000 short-term gain as ordinary income.",
        axcess_diagnostic="None - silent",
        manual_calc="Yes",
        axcess_fix="Gains and Losses > Capital Loss Carryovers: short-term $26,000, long-term $12,000 (recomputed from the 2024 Schedule D: "
                   "ST (29,000), LT (12,000), $3,000 allowed absorbs ST first). Tax $1,000 lower than the all-LT version.",
        amount=26000,
        proconnect_default="Same - carryovers for a new client are manual entries; ProConnect uses whatever character is keyed.",
        proconnect_fix="Schedule D input > Capital loss carryover: short-term 26,000, long-term 12,000 (screen/field per current release - "
                       "verify).",
        efile_impact="None",
        affected_lines=["7", "16", "Schedule D lines 6/14"],
        procedure_section="General Return Prep Notes",
        notes="Workbook tab 10 (corrected formulas): D16 26,000 / D17 12,000."),
    exc("EVG1022-SX8", "8", "Est. Tax Penalty", "Form 2210 for a new client - prior-year tax not proforma'd",
        axcess_default="Axcess computes Form 2210 from the prior-year tax and AGI it has. For a new client those fields are blank unless keyed, "
                       "so the 110%-of-prior-year safe harbor is not available to the calculation; front-loaded withholding is treated as "
                       "paid evenly by default.",
        axcess_diagnostic="Penalty/2210 informational message may appear for missing prior-year data - verify; otherwise silent",
        manual_calc="Yes",
        axcess_fix="General > Payments > Penalties and Interest (Form 2210): 2024 tax $164,982, 2024 AGI $669,300; estimates by date "
                   "(4 x $8,000 timely). Required annual payment = lesser of 90% of 2025 tax $126,067 or 110% of 2024 tax $181,480 -> "
                   "$126,067; paid $137,769 (each quarter covered) -> no penalty, no override.",
        amount=0,
        proconnect_default="Same - prior-year tax/AGI for Form 2210 must be entered for a new client.",
        proconnect_fix="Payments, Penalties & Extensions > Underpayment penalty (2210): enter prior-year tax and AGI; estimates with dates "
                       "(screen/field per current release - verify).",
        efile_impact="None",
        affected_lines=["38"],
        procedure_section="Workpapers / Responding to Review Points"),
    exc("EVG1022-SX9", "2", "State Allocation", "PA-40 classes differ from federal: box 16 compensation, no carryover, no wash-sale rule",
        axcess_default="The PA return starts from federal data. Unless PA adjustments are made: compensation may be pulled from federal box 1 "
                       "instead of box 16 (PA taxes 401(k)/403(b) deferrals); the federal capital loss carryover and the code W "
                       "disallowance can flow into PA net gains; the $96,000 taxable 1099-R can be treated as PA income.",
        axcess_diagnostic="None - silent",
        manual_calc="Yes",
        axcess_fix="PA return inputs: compensation = W-2 box 16 ($506,000); PA net gains = 2025 sales only $47,000 (no PA carryover; IVV loss "
                   "allowed - PA has no wash-sale provision, verify); 1099-R marked non-PA-taxable (retirement). PA taxable income "
                   "$580,485, tax $17,821. Verify field paths in current release.",
        amount=47000,
        proconnect_default="Same risk - PA adjustments to federal amounts are separate state inputs.",
        proconnect_fix="Pennsylvania return > income class adjustments: PA compensation from box 16; PA gains adjustment to remove the "
                       "carryover and the code W adjustment; 1099-R PA exclusion (screen/field per current release - verify).",
        efile_impact="None",
        affected_lines=["PA-40 lines 1a, 5"],
        procedure_section="SALT Implications",
        notes="PA wash-sale treatment is an assumption flagged for the signer (PA tax effect $553)."),
]

TABS = {
    "23": [{"A": "Pennsylvania (resident; HQ King of Prussia / home office)", "B": 112, "C": 165, "D": 410000,
            "G": "Resident - PA taxes all compensation (box 16 $441,000 incl. 401(k) deferrals)"},
           {"A": "New Jersey", "B": 22, "C": 165, "D": 410000,
            "G": "PA-NJ reciprocal agreement - NJ wages of a PA resident taxed only by PA; NO NJ-1040NR"},
           {"A": "Massachusetts", "B": 18, "C": 165, "D": 410000,
            "G": "No day threshold - MA Form 1-NR/PY; allocated wages = MA-source wages (enter as MA state wage row)"},
           {"A": "Illinois", "B": 13, "C": 165, "D": 410000,
            "G": "<= 30 IL working days - nonresident employee compensation not IL-source (rule eff. 2020); no IL-1040 (assumption - verify)"}],
    "7": [{"A": "Massachusetts (nonresident) -> PA-40 Schedule G-L credit", "B": 580485, "C": 44727, "E": 2191, "G": 17821}],
    "18": [{"A": "Gregory - Keystone 401(k) KMDV stock in kind (Fidelity 1099-R, code 2)", "B": 640000, "C": 544000,
            "D": "Box 2a 96,000 = 8,000 sh x $12.00 plan cost",
            "F": "NUA - lump-sum after separation 08/29/2025; box 6 deferred until sale (LTCG). Separate 1099-R $780,000 code G rollover - "
                 "nontaxable. PA: not taxable (retirement)."}],
    "17": [{"A": "IVV 400 sh - Gregory Schwab ****4410, sold 11/10/2025 (acq 02/19/2025)", "B": 245000, "C": 0,
            "E": "YES - Ellen's Schwab IRA ****8831 bought 420 sh IVV 11/20/2025", "F": 18000,
            "G": "Rev. Rul. 2008-5 / Pub. 550 (spouse): loss disallowed permanently (code W); no basis added to the IRA. 1099-B box 1g blank."}],
    "14": [{"A": "Pfizer Inv. Ent. 4.75% 05/19/2033 (CUSIP 716973AE2) - bought 03/12/2025", "B": 9500, "C": -2981.94, "D": 8500,
            "E": 786.12, "F": "Taxable - box 11 ABP (constant yield, broker-computed) on Sch B 'ABP Adjustment'; accrued interest 113 days "
                              "reversed as 'Accrued interest'"},
           {"A": "Pennsylvania Turnpike Commission 5% 12/01/2038", "B": 7500, "C": 0, "D": 6750, "E": 1104.30,
            "F": "Tax-exempt - box 13 premium reduces line 2a to 6,396; not deductible; PA obligation exempt for PA"}],
    "10": {"D10": 3000, "D11": 29000, "D12": 12000},
    "8": {"E12": 140074, "E14": 669300, "E15": 164982, "E19": 137769,
          "C25": 34442.25, "C26": 34442.25, "C27": 34442.25, "C28": 34442.25,
          "D25": "Y", "D26": "Y", "D27": "Y", "D28": "Y",
          "F25": "W-2 withholding 105,769 (incl. 2,169 addl Medicare) treated as paid evenly 26,442.25 + 8,000 estimate",
          "F28": "Q4 estimate paid 01/15/2026 (timely for 2025); 3,000 paid with 4868 not counted"},
}

CHECKS = {
    "'23. Multi-State W-2 Days'!F13": 44727.27,
    "'23. Multi-State W-2 Days'!F14": 32303.03,
    "'7. Multi-State Allocation'!F12": 1373,
    "'18. NUA & IRD Deduction'!E11": 96000,
    "'17. Equity Comp & Wash Sales'!D12": 245000,
    "'14. Bond Interest & Premium'!C19": -2981.94,
    "'10. Capital Loss Carryover'!D16": 26000,
    "'10. Capital Loss Carryover'!D17": 12000,
    "'8. Est. Tax Penalty (2210)'!E18": 126066.6,
    "'8. Est. Tax Penalty (2210)'!E20": 0,
}
