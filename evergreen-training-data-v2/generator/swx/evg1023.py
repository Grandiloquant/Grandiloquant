"""EVG1023 Delgado - software exceptions (CCH Axcess workbook tabs 3, 4, 5, 6, 9, 11, 21 + log item; ProConnect equivalents incl.
Form 8865 not supported and new-client Form 8582 Regular/AMT carryovers).
Amounts tie to the EVG1023 answer key: Catawba basis-allowed 30,000 / suspended 22,000, at-risk allowed 2,000 / suspended 28,000,
line 2n 0; Lakewood 704(c)(1)(B) gain 250,000, 752(b) deemed distribution 85,000, basis 461,000 before loss; passive suspended
Regular 51,253 / AMT 46,553; NC bonus addback 23,800; duplex 1033 gain 179,758 deferred, deadline 12/31/2027; AGI 423,527."""
import datetime as dt

from software_exceptions import exc

CLIENT_ID, DISPLAY = "EVG1023", "Raymond & Carla Delgado"
PREPARER, REVIEWER = "T. Alvarez (senior staff)", "M. Osei (manager)"
INTRO = """
Three partnerships, a rental fire and a foreign partnership - and a new client, so neither package has a proforma of basis,
at-risk or passive carryovers. Every limitation here is input-driven: CCH Axcess and ProConnect apply basis, at-risk and passive
rules only to the extent the preparer supplies beginning basis, the at-risk character of each liability, and prior-year unallowed
losses (separately for regular tax and AMT). Two items have no input at all - the IRC 704(c)(1)(B) gain hidden in a K-1 footnote and
the IRC 1033 replacement deadline - and must be calculated off-system (workbook tabs 11 and 21). Form 8865 cannot be produced in
ProConnect at any subscription tier (Advanced/Elite bundles change return counts and users, not form coverage).
"""

ITEMS = [
    exc("EVG1023-SX1", "3", "Basis/At-Risk/Passive", "Catawba River Outfitters - loss exceeds outside basis (guaranteed payments don't add basis)",
        axcess_default="Without Section 6 (Basis Limitation) inputs, Axcess allows the full ($52,000) K-1 loss. If the preparer keys basis but "
                       "adds the $95,000 guaranteed payment as an 'other increase', basis looks sufficient and the full loss is still allowed.",
        axcess_diagnostic="None - silent",
        manual_calc="Yes",
        axcess_fix="Income/Deductions > Partnership Passthrough > Catawba > Section 6 Basis Limitation: check 'apply the limitation'; "
                   "beginning basis $30,000 (capital 2,000 + nonrecourse share 28,000); no increase for guaranteed payments. Allowed by "
                   "basis $30,000; $22,000 suspended (704(d) carryover). Verify field path in current release.",
        amount=30000,
        proconnect_default="Same - ProConnect applies the partner basis limitation only when basis information is entered on the K-1 "
                           "screen's basis worksheet.",
        proconnect_fix="Partnership Information > Schedule K-1 (1065) > Basis Limitations / Partner's basis worksheet: beginning basis "
                       "30,000; enforce limitation (screen/field per current release - verify). Suspended 22,000 carries in the 704(d) "
                       "carryover field.",
        efile_impact="None",
        affected_lines=["8 (Sch E line 28)", "Sch E Part II"],
        procedure_section="Schedules K-1 - partnership distributions/losses in excess of basis (Section 6 - apply the limitation)",
        notes="Tab 3 also documents Lakewood: 296,000 + 250,000 (704(c)) - 85,000 (752(b)) = 461,000 before the 14,000 loss."),
    exc("EVG1023-SX2", "4", "Basis/At-Risk/Passive", "At-risk: nonrecourse seller financing on equipment is not qualified nonrecourse financing",
        axcess_default="Unless 'subject to at-risk limitation' is checked and the liability character is entered, Axcess treats the $30,000 "
                       "that cleared basis as fully allowed. K-1 item K reports the $28,000 as 'nonrecourse' - Axcess cannot know it is "
                       "equipment seller financing rather than qualified (real property) nonrecourse financing.",
        axcess_diagnostic="None - silent",
        manual_calc="Yes",
        axcess_fix="Partnership Passthrough > Catawba > Section 6 / At-Risk: check 'subject this entity to the at-risk limitation'; amount at "
                   "risk $2,000 (basis 30,000 less nonrecourse non-QNF 28,000). Form 6198 allows $2,000; $28,000 suspended (Form 6198 "
                   "carryover). Verify field path in current release.",
        amount=-2000,
        proconnect_default="Same - Form 6198 is produced only when the at-risk box and at-risk amounts are entered.",
        proconnect_fix="Schedule K-1 (1065) > At-Risk (6198) section: some investment is not at risk = Yes; amount at risk 2,000 "
                       "(screen/field per current release - verify).",
        efile_impact="None (Form 6198 attached)",
        affected_lines=["8", "Form 6198", "13a"],
        procedure_section="Schedules K-1",
        notes="IRC 465(b)(6) QNF is limited to the activity of holding real property; this is equipment. Tax effect of skipping tabs 3-4: "
              "$11,804."),
    exc("EVG1023-SX3", "9", "AMT", "K-1 box 17A +$6,000 on a loss that is limited by basis/at-risk - Form 6251 line 2n = 0",
        axcess_default="Axcess carries the K-1 box 17A post-1986 depreciation adjustment to Form 6251 line 2l (+6,000) even though only "
                       "$2,000 of the regular loss is allowed - unless the AMT basis/at-risk amounts are entered so the AMT allowed loss "
                       "is recomputed.",
        axcess_diagnostic="None - silent",
        manual_calc="Yes",
        axcess_fix="AMT input for the Catawba K-1: AMT basis 30,000 and AMT at-risk 2,000 (AMT columns of the basis/at-risk worksheet); "
                   "if the line still shows +6,000, use the 'Loss limits (Force)' line 2n override so the net AMT adjustment is $0 "
                   "(regular allowed 2,000 = AMT allowed 2,000). Lakewood's +1,200 also nets to $0 (loss suspended). Verify field names.",
        amount=0,
        proconnect_default="Same risk - AMT K-1 items flow to 6251 unless AMT limitation amounts are entered.",
        proconnect_fix="Schedule K-1 (1065) > AMT / Basis and at-risk AMT amounts: enter AMT basis and AMT at-risk; confirm Form 6251 shows "
                       "no net adjustment (screen/field per current release - verify).",
        efile_impact="None",
        affected_lines=["Form 6251 lines 2l/2n"],
        procedure_section="Schedules K-1",
        notes="No AMT in 2025 either way, but the AMT suspended amounts carried forward depend on it."),
    exc("EVG1023-SX4", "11", "Basis/At-Risk/Passive", "IRC 704(c)(1)(B) mixing-bowl gain disclosed only in a K-1 footnote",
        axcess_default="Axcess reads the K-1 boxes: box 9a = 0, box 2 (14,000). The $250,000 precontribution gain in footnote 3 is not in any "
                       "box, so nothing is reported and outside basis is understated.",
        axcess_diagnostic="None - silent",
        manual_calc="Yes",
        axcess_fix="Partnership Passthrough > Lakewood: add $250,000 net long-term capital gain (K-1 Section 3 direct entry / box 9a "
                   "override) with a statement explaining IRC 704(c)(1)(B); Section 6 Basis: other increase +250,000. Gain is NII and "
                   "portfolio (not passive) income. Verify field path in current release.",
        amount=250000,
        proconnect_default="Same - ProConnect imports/keys K-1 boxes; a footnote amount must be entered manually.",
        proconnect_fix="Schedule K-1 (1065) > Lakewood > Net long-term capital gain: 250,000 (adjusted from K-1 with explanation statement); "
                       "basis worksheet other increase 250,000; ensure the gain is not treated as passive income (screen/field per "
                       "current release - verify).",
        efile_impact="Explanation statement attached (PDF)",
        affected_lines=["7", "Sch D line 12", "Form 8960"],
        procedure_section="Schedules K-1 - hot assets / disproportionate distributions (mixing bowl)",
        notes="Contributed 03/22/2021 (FMV 400,000, basis 150,000); distributed to another partner 08/14/2025 (< 7 years). Tax effect $44,094."),
    exc("EVG1023-SX5", "11", "Basis/At-Risk/Passive", "IRC 752(b) deemed distribution - liability share 180,000 -> 95,000",
        axcess_default="If only the K-1 boxes are keyed, Axcess's basis worksheet does not reflect the $85,000 decrease in the partner's "
                       "share of liabilities (item K) - basis is overstated going forward (no gain this year because basis is sufficient).",
        axcess_diagnostic="None - silent",
        manual_calc="Yes",
        axcess_fix="Section 6 Basis: beginning share of liabilities 180,000, ending 95,000 (or 'other decrease' 85,000 as a deemed cash "
                   "distribution). Basis before loss 461,000; ending 447,000. No IRC 731 gain.",
        amount=-85000,
        proconnect_default="Same - liability changes must be entered on the basis worksheet.",
        proconnect_fix="Schedule K-1 (1065) > Partner's basis worksheet: beginning/ending liabilities (screen/field per current release - verify).",
        efile_impact="None",
        affected_lines=["K-1 basis worksheet"],
        procedure_section="Schedules K-1"),
    exc("EVG1023-SX6", "5", "Basis/At-Risk/Passive", "New client - Form 8582 prior-year unallowed losses (Regular vs AMT); LP gets no $25,000",
        axcess_default="No proforma: Axcess shows no prior-year unallowed loss for Lakewood unless keyed, and a single amount keyed only in the "
                       "regular column leaves the AMT carryover blank (or equal to regular). The duplex is flagged active participation, "
                       "but MAGI > $150,000 removes the allowance; if 'disposed of activity' is checked for the fire, Axcess releases the "
                       "duplex loss although the IRC 1033 deferral means no fully taxable disposition.",
        axcess_diagnostic="None - silent",
        manual_calc="Yes",
        axcess_fix="Partnership Passthrough > Lakewood > Passive Activity carryovers: prior-year unallowed ordinary loss Regular 31,000, AMT "
                   "27,500; limited partner. Duplex rental: active participation, do NOT check disposed. Result: all passive losses suspended "
                   "- Regular 51,253 / AMT 46,553 carried to 2026.",
        amount=51253,
        proconnect_default="ProConnect also has no prior-year data for a new client; prior-year unallowed losses must be entered per activity, "
                           "with regular and AMT (operating) amounts entered separately; Form 8582 can be forced (1 = when applicable, "
                           "2 = force).",
        proconnect_fix="Partnership K-1 (and Rental) > Passive Losses tab / prior years' unallowed losses: Regular 31,000 and AMT 27,500 "
                       "for Lakewood; no disposition for the duplex; Form 8582 'when applicable'.",
        proconnect_ref="Intuit help: 'How to generate Form 8582 ... in ProConnect Tax'; Intuit Accountants Community thread on prior years' "
                       "unallowed losses",
        efile_impact="None",
        affected_lines=["8", "Form 8582"],
        procedure_section="Schedules K-1 / Schedule E",
        notes="Tab 5 MAGI 423,527 -> special allowance $0 (corrected formulas)."),
    exc("EVG1023-SX7", "6", "Depreciation", "NC decouples from bonus depreciation - 85% addback on Carla's $28,000",
        axcess_default="Carla's bookkeeper's asset list is keyed on the Sch C as a summary depreciation figure (not in the Depreciation module), "
                       "so no NC asset-level difference is computed and the D-400 shows no bonus addback.",
        axcess_diagnostic="None - silent",
        manual_calc="Yes",
        axcess_fix="Enter the three assets in the Depreciation module with NC treatment, or key the NC addition directly: NC > Additions > "
                   "Bonus depreciation $23,800 (85% of 28,000); set up the 20% ($4,760) deduction for 2026-2030. Verify field path in "
                   "current release; verify NC conformity for OBBBA 100% bonus.",
        amount=23800,
        proconnect_default="Same - the NC addback is computed only from asset entries with state depreciation; summary entries need a manual "
                           "NC adjustment.",
        proconnect_fix="Depreciation (4562) asset entries with state (NC) bonus treatment, or North Carolina > Additions > bonus depreciation "
                       "23,800 (screen/field per current release - verify).",
        efile_impact="None",
        affected_lines=["NC D-400 Schedule S", "Form 4562"],
        procedure_section="SALT Implications",
        notes="Federal: 100% bonus (assets acquired 03-06/2025, after 01/19/2025) - bookkeeper's 40% replaced."),
    exc("EVG1023-SX8", "21", "Other", "Rental duplex destroyed by fire - IRC 1033 election and replacement deadline",
        axcess_default="Entering the casualty on Form 4684 Section B with proceeds $410,000 and basis $230,242 recognizes the $179,758 gain "
                       "(Form 4797) unless the postponement election is made. Axcess keeps no multi-year ledger of the replacement deadline. "
                       "The firm workbook's ORIGINAL formula (event date + 2 x 365) would show 01/24/2027 - wrong.",
        axcess_diagnostic="None - silent",
        manual_calc="Yes",
        axcess_fix="Gains and Losses > Casualties and Thefts (Form 4684 Section B): enter the conversion; election to postpone gain under IRC "
                   "1033 / gain postponed 179,758; attach election statement (property, date, proceeds, basis, intent to replace, "
                   "deadline 12/31/2027). Tab 21 (corrected formula) tracks the deadline and replacement cost. Verify field path in current "
                   "release.",
        amount=179758,
        proconnect_default="Same - the postponement must be elected on the casualty/disposition input; no deadline tracking.",
        proconnect_fix="Dispositions > Casualties and Thefts (4684): business property, election to postpone gain (1033), amount postponed "
                       "179,758; attach the 1033 statement (screen/field per current release - verify).",
        efile_impact="Election statement attached (PDF)",
        affected_lines=["Form 4684", "Form 4797", "7"],
        procedure_section="Rare events / Tax Research",
        notes="Replacement period = 2 years after the close of the first tax year in which any part of the gain is realized (2025) -> "
              "12/31/2027; 3 years applies only to condemned real property."),
    exc("EVG1023-SX9", "PC", "E-file Disqualifying", "Form 8865 (Baja Coastal - Categories 3 and 4) is not available in ProConnect",
        axcess_default="Form 8865 prepared in the Axcess 1040 foreign forms (verify availability in the firm's current release and license) "
                       "and e-filed with the return.",
        axcess_diagnostic="None - silent",
        manual_calc="No",
        axcess_fix="n/a (firm e-filed from Axcess with Form 8865 Schedules O and P included).",
        amount=0,
        proconnect_default="Form 8865 is not available in ProConnect Tax (or Lacerte). The software cannot generate it or include it in the "
                           "1040 e-file.",
        proconnect_fix="Prepare Form 8865 outside ProConnect (IRS fillable PDF or software that supports it). Firm policy: when the 1040 is "
                       "prepared in ProConnect, paper-file the complete return with Form 8865 attached (an e-filed return cannot carry the "
                       "form). Report the Baja loss on Sch E/8582 as a passive partnership activity and list the interest on Form 8938 Part IV "
                       "as reported on Form 8865.",
        proconnect_ref="Intuit Accountants Community / product discussions: Form 8865 is not available in Lacerte or ProConnect Tax",
        efile_impact="ProConnect: paper filing required (firm decision); Axcess: e-file",
        affected_lines=["Form 8865", "Form 8938"],
        procedure_section="E-Filing / Paper Filing Returns; Foreign Transactions",
        notes="Penalty for failure to file Form 8865: $10,000 per form."),
    exc("EVG1023-SX10", "2", "Other", "Form 8938 - foreign partnership interest reported on Form 8865 still counts (excepted asset)",
        axcess_default="Nothing triggers Form 8938 from a Form 8865 entry; if 8938 is not opened, it is not produced. If it is opened, the "
                       "preparer must list the 8865 interest as an excepted asset in Part IV rather than in Part VI.",
        axcess_diagnostic="None - silent",
        manual_calc="No",
        axcess_fix="Foreign > Form 8938: MFJ living in the US; Part IV - number of Forms 8865 = 1 (asset counted toward the threshold: max "
                   "value $180,000, year-end $174,000 -> filing required). No FBAR. Verify field path in current release.",
        amount=180000,
        proconnect_default="ProConnect supports Form 8938 entry, but with no 8865 in the file nothing prompts it.",
        proconnect_fix="Foreign Reporting > Form 8938: enter the excepted-asset information (screen/field per current release - verify).",
        efile_impact="None (Axcess); paper with the return if prepared in ProConnect",
        affected_lines=["Form 8938", "Schedule B Part III"],
        procedure_section="Foreign Transactions - FinCEN114/FBAR"),
]

TABS = {
    "3": [{"A": "Catawba River Outfitters LLC (40% member-manager; material participation)", "B": 30000, "C": 0, "D": 0,
           "F": "Begin = capital 2,000 + nonrecourse seller-note share 28,000. Guaranteed payments 95,000 NOT a basis increase."},
          {"A": "Lakewood Partners LP (10% limited partner)", "B": 296000, "C": 250000, "D": 85000,
           "F": "C = IRC 704(c)(1)(B) gain (footnote 3); D = IRC 752(b) deemed distribution (liabilities 180,000 -> 95,000)."}],
    "3b": [{"C": 52000, "F": "Yes - basis allowed 30,000; 22,000 704(d) carryover; then tab 4 at-risk"},
           {"C": 14000, "F": "Basis OK - loss passes; then tab 5 (passive - suspended)"}],
    "4": [{"A": "Catawba River Outfitters LLC - equipment rental", "B": 30000, "C": 2000}],
    "5": [{"A": "Lakewood Partners LP (LP) - 2025 loss 14,000 + PY unallowed 31,000", "B": "N", "C": 45000, "D": 0,
           "F": "Limited partner - no $25k allowance. AMT: 12,800 + PY 27,500 = 40,300. 704(c) gain is portfolio, not passive income."},
          {"A": "Baja Coastal Ventures (foreign partnership, 15%)", "B": "N", "C": 6000, "D": 0, "F": "Passive; Form 8865 activity"},
          {"A": "Duplex 1407-1409 Thomas Ave - January 2025", "B": "Y", "C": 252.79, "D": 0,
           "F": "Active participation but MAGI > 150k -> 0 allowance; fire + 1033 deferral is not a fully taxable disposition (469(g))"}],
    "5cells": {"E23": 423527},
    "6": [{"A": "Carla Sch C 2025 additions - furniture/fixtures 19,400 (7-yr) + workstation/plotter 8,600 (5-yr)", "B": 28000, "C": 4200,
           "E": 28000, "G": "100% bonus federal (acquired after 01/19/2025); NC adds back 85% = 23,800, deducts 4,760/yr 2026-2030; AMT "
                           "allows bonus (no AMT difference). Verify NC OBBBA conformity."}],
    "9": [{"A": "Catawba River Outfitters LLC (K-1 box 17A +6,000)", "B": -2000, "C": -2000,
           "F": "AMT loss 46,000 limited by same basis 30,000 / at-risk 2,000 -> 2,000; do NOT put 6,000 on line 2l"},
          {"A": "Lakewood Partners LP (K-1 box 17A +1,200)", "B": 0, "C": 0,
           "F": "Loss suspended (passive) for both systems; AMT suspended carryover tracked separately"}],
    "11": [{"A": "Raymond - Lakewood Partners LP (Mooresville Road parcel)", "B": "704c-737", "C": 250000, "D": 465000, "G": 250000,
            "H": "C = built-in gain at contribution 03/22/2021 (FMV 400,000 - basis 150,000); D = FMV at distribution 08/14/2025 to Harbor "
                 "Pointe Holdings LLC (< 7 yrs). Gain = min(250,000, 465,000 - 150,000). LTCG (investment land) -> Sch D line 12; "
                 "basis +250,000. K-1 box 9a omits it (footnote 3)."},
           {"A": "Raymond - Lakewood Partners LP", "B": "752b", "C": 546000, "D": 461000, "E": 180000, "F": 95000, "G": 0,
            "H": "Deemed distribution 85,000 < basis 546,000 -> no IRC 731 gain"}],
    "21": [{"A": "Duplex building - 1407-1409 Thomas Ave, Charlotte (rental)", "B": dt.datetime(2025, 1, 24), "C": 410000, "D": 230242,
            "E": 2, "G": "Fire 01/24/2025; insurance paid 05/16/2025 (gain realized 2025). IRC 1033 election - intend to rebuild (~$465k quote). "
                         "Accum. depreciation 59,758 (would be unrecaptured 1250). Replacement cost not yet incurred."}],
}

CHECKS = {
    "'3. K-1 Basis Limitation'!E14": 461000,
    "'3. K-1 Basis Limitation'!D24": -30000,
    "'3. K-1 Basis Limitation'!E24": 22000,
    "'3. K-1 Basis Limitation'!E25": 0,
    "'4. At-Risk (Form 6198)'!E13": -2000,
    "'5. Passive Activity (8582)'!E28": 0,
    "'6. Depreciation Overrides'!D13": -23800,
    "'6. Depreciation Overrides'!F13": 0,
    "'9. AMT Adjustments (6251)'!D21": 0,
    "'21. Involuntary Conv. 1033'!H12": 179758,
    "'21. Involuntary Conv. 1033'!I12": 46752,
    "'21. Involuntary Conv. 1033'!K12": 0,
}
