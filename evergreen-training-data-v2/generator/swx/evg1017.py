"""EVG1017 Russo - software exceptions (CCH Axcess workbook tabs 3, 5, 7, 11, 14 + log items; ProConnect equivalents).
Amounts tie to the EVG1017 answer key (Ridgeview 731(a) gain 9,500; Sch E 41,700; PTP carryforward 3,490; Sch B 26,184;
accrued interest -1,550; market discount 1,624; ABT basis 14,850; IL Sch CR 1,173; IL Treasury subtraction 9,290)."""
from software_exceptions import exc

CLIENT_ID, DISPLAY = "EVG1017", "Frank & Diane Russo"
PREPARER, REVIEWER = "Staff preparer", "M. Osei (senior)"
INTRO = """
A large brokerage-plus-K-1 return where the software's imports are complete-looking but wrong in quiet ways: two
consolidated 1099s for the same account, a broker statement whose accrued-interest and WHFIT sections sit outside the
form totals, a noncovered lot with no basis, and a partnership distribution that exceeds basis only once the 752(b)
deemed distribution is counted. All seven items are silent. Workbook tabs 3/11 (Ridgeview basis and 752(b)),
5 (passive and PTP baskets), 7 (PA credit) and 14 (bond interest) carry the supporting numbers.
"""

ITEMS = [
    exc("EVG1017-SX1", "2", "Other", "Original AND corrected Morgan Stanley consolidated 1099 both imported",
        axcess_default="Autoflow treated the 02/13 original and the 03/12 CORRECTED consolidated 1099s as two payer documents: dividends "
                       "~$158k, interest and sales doubled. The original also had box 3 nondividend $900 (vs $2,150), box 5 $8,400 "
                       "(vs $9,200) and no box 1f market discount.",
        axcess_diagnostic="None - silent",
        manual_calc="No",
        axcess_fix="Delete the original statement's import (bookmark 'superseded'); keep only the CORRECTED 03/12/2026 statement: box 1a "
                   "$78,400 (+ WHFIT $1,380 = Sch B $79,780), box 3 return of capital $2,150 (reduces VGSLX basis - not income), box 5 "
                   "$9,200, box 1f $1,624.",
        amount=78400,
        proconnect_default="Same - an imported/entered second consolidated 1099 is additive; ProConnect does not know one supersedes the other.",
        proconnect_fix="Delete the original 1099 entries; import/key the corrected statement only (screen per current release - verify).",
        efile_impact="None",
        affected_lines=["2b", "3a", "3b", "7", "13a"],
        procedure_section="Scan - consolidated 1099 (corrected statements)"),
    exc("EVG1017-SX2", "14", "Other", "Accrued interest paid at purchase and accrued market discount - not netted by the broker",
        axcess_default="The 1099-INT import reports box 1 $14,250 + box 3 $9,600 gross. The $1,240 (Apple bond) and $310 (Treasury note) of "
                       "accrued interest Frank PAID sellers is only on the supplemental page, and the Ford bond's accrued market discount "
                       "(1099-B box 1f, $1,624) stays inside the capital gain unless code D is entered.",
        axcess_diagnostic="None - silent",
        manual_calc="Yes",
        axcess_fix="Income > Interest Income: add negative lines 'Accrued interest' -1,240 (corporate) and -310 (US obligation, so the IL "
                   "subtraction is also reduced); add $1,624 market discount as interest. Gains and Losses: Ford row box D, code D, "
                   "adjustment -1,624. Schedule B line 2b = $26,184.",
        amount=-1550,
        proconnect_default="Same - accrued interest paid and market discount must be entered as separate adjustments.",
        proconnect_fix="Interest income input: 'Accrued interest paid' / negative adjustment lines (-1,240 and -310, the latter flagged as US "
                       "obligation interest); Dispositions: Ford sale code D -1,624 with the $1,624 reported as interest "
                       "(screen/field per current release - verify).",
        efile_impact="None",
        affected_lines=["2b", "Schedule B", "Form 8949 box D", "IL Schedule M"],
        procedure_section="Schedule B - accrued interest / state exemption"),
    exc("EVG1017-SX3", "2", "Capital Loss", "Noncovered Abbott lot imports with $0 basis; WHFIT section outside the 1099 totals",
        axcess_default="(1) The ABT sale (box E, noncovered) imports with blank basis -> $36,900 gain. (2) The Invesco UIT (WHFIT) "
                       "dividends $1,380 and pro-rata sales are reported in a separate statement section that is not in the 1099-DIV/B "
                       "summary the import reads, so they are omitted. Neither is flagged.",
        axcess_diagnostic="None - silent",
        manual_calc="Yes",
        axcess_fix="Gains and Losses: ABT row basis $14,850 (2009 Schwab confirm) -> gain $22,050. Add WHFIT: dividends $1,380 ($1,210 qualified) "
                   "on Schedule B; pro-rata sales on 8949 box E proceeds $4,820 / basis $4,310 (+$510); trust expenses $95 not deductible.",
        amount=14850,
        proconnect_default="Same - noncovered basis must be keyed; WHFIT items are not part of a 1099 import.",
        proconnect_fix="Dispositions: enter ABT cost basis 14,850; add WHFIT dividends and pro-rata sale lines manually (screen per current "
                       "release - verify).",
        efile_impact="None",
        affected_lines=["3a", "3b", "7"],
        procedure_section="Schedule D - missing cost basis"),
    exc("EVG1017-SX4", "3", "Basis/At-Risk/Passive", "Ridgeview distribution exceeds outside basis once the 752(b) deemed distribution is counted",
        axcess_default="Without the Section 6 basis limitation applied (beginning basis blank), Axcess treats the $80,000 box 19 distribution as "
                       "tax-free. Even with basis entered, the $4,000 decrease in his share of liabilities (K-1 item K: 18,000 -> 14,000) is "
                       "not a box 19 amount, so it is not counted as a distribution.",
        axcess_diagnostic="None - silent",
        manual_calc="Yes",
        axcess_fix="Income/Deductions > Partnership Passthrough > Section 6 (Basis Limitation): beginning basis $15,500 (tax capital -2,500 + "
                   "liabilities 18,000); income +$59,000; distributions $80,000 cash + $4,000 752(b) deemed = $84,000 -> excess $9,500 "
                   "IRC 731(a) LTCG on Form 8949 box F (held since 2017; footnote: no 751 property). Ending basis $0.",
        amount=9500,
        proconnect_default="Same - ProConnect does not compute partner outside basis from the K-1; a liability-share decrease must be "
                           "entered as a deemed distribution.",
        proconnect_fix="Partnership K-1 > basis worksheet / Dispositions: enter the $9,500 excess distribution as a long-term capital gain "
                       "(8949 box F) and document basis (screen/field per current release - verify).",
        efile_impact="None",
        affected_lines=["7", "Form 8949 box F"],
        procedure_section="Schedules K-1",
        notes="Supporting rows on tab 3 (basis) and tab 11 (752(b) liability shift)."),
    exc("EVG1017-SX5", "5", "Basis/At-Risk/Passive", "Passive baskets - Oak Brook LP loss + omitted PY carryover vs PTP isolation",
        axcess_default="(1) The organizer's PY column left the Oak Brook suspended loss ($7,300) blank, so Form 8582 shows no prior-year "
                       "unallowed loss. (2) Unless the Permian K-1 is flagged as a PTP, its ($2,340) loss nets against Ridgeview's passive "
                       "income and enters QBI.",
        axcess_diagnostic="None - silent",
        manual_calc="Yes",
        axcess_fix="Partnership Passthrough: Oak Brook prior-year unallowed loss $7,300 (from PY 8582 / PERM); Permian: check 'Publicly traded "
                   "partnership' so 469(k) isolates it (PY suspended $1,150). Result: Oak Brook $9,600 + $7,300 allowed against Ridgeview "
                   "$58,600 -> Schedule E $41,700; PTP $3,490 suspended (excluded from QBI). LP -> no $25k allowance.",
        amount=41700,
        proconnect_default="Same - prior-year unallowed losses and the PTP indicator are inputs.",
        proconnect_fix="Partnership K-1 > Passive Losses tab: prior-year unallowed Regular (and AMT) = 7,300 for Oak Brook; Permian: PTP = "
                       "Yes with PY unallowed 1,150. Form 8582 can be forced (1=when applicable, 2=force) if needed.",
        proconnect_ref="Intuit help: 'How to generate Form 8582 ... ProConnect Tax' (prior years' unallowed losses)",
        efile_impact="None",
        affected_lines=["8 (Schedule 1 line 5)", "Schedule E line 41", "Form 8582", "13a"],
        procedure_section="Schedules K-1"),
    exc("EVG1017-SX6", "7", "State Allocation", "PA-source K-1 income - PA-40 NR and IL Schedule CR not generated from the K-1 matrix",
        axcess_default="The Ridgeview state matrix ($38,200 PA) is a K-1 footnote; unless the PA amount is entered as PA-source and a PA "
                       "nonresident return is added, no PA-40 NR is produced and IL Schedule CR has no tax paid to another state to credit.",
        axcess_diagnostic="None - silent",
        manual_calc="Yes",
        axcess_fix="Partnership Passthrough > state allocation: PA $38,200 (IL $19,000; WI $1,400 under WI's $2,000 threshold). Add PA-40 NR: "
                   "tax $1,173 = NRK-1 withholding $1,173. IL Schedule CR: lesser of PA tax $1,173 or IL tax on PA income "
                   "(16,864 x 38,200/346,385 = $1,860) -> $1,173. 731 gain treated as non-PA-source (assumption, flagged for signer).",
        amount=1173,
        proconnect_default="Same - nonresident state returns and the resident credit depend on state-source amounts entered per K-1.",
        proconnect_fix="Partnership K-1 > State: PA-source 38,200; activate PA nonresident return; IL credit for tax paid to PA = 1,173 "
                       "(screen/field per current release - verify).",
        efile_impact="PA-40 NR e-filed with the IL-1040",
        affected_lines=["IL-1040 Schedule CR", "PA-40 NR"],
        procedure_section="SALT Implications - New State Filing Requirements"),
    exc("EVG1017-SX7", "2", "State Allocation", "IL subtraction for US Treasury interest must be net of accrued interest paid; muni add-back",
        axcess_default="The IL subtraction for US obligation interest pulls 1099-INT box 3 ($9,600) in full; the $310 accrued interest paid "
                       "on the Treasury note, entered as a separate negative line, is not tied to it unless flagged as US obligation "
                       "interest. Out-of-state muni interest $4,800 must be identified as non-IL to be added back.",
        axcess_diagnostic="None - silent",
        manual_calc="Yes",
        axcess_fix="Illinois > Schedule M: US obligation subtraction $9,290 (9,600 - 310); tax-exempt interest add-back $4,800 (NY/CA/TX "
                   "issuers). IL base income $346,385.",
        amount=9290,
        proconnect_default="Same - the state US-obligation subtraction follows the amounts flagged as US obligation interest.",
        proconnect_fix="Illinois return > subtractions: US obligation interest 9,290; additions: out-of-state tax-exempt interest 4,800 "
                       "(screen/field per current release - verify).",
        efile_impact="None",
        affected_lines=["IL-1040 lines 2/5", "IL Schedule M"],
        procedure_section="SALT Implications"),
]

TABS = {
    "3": [{"A": "Ridgeview Capital Partners LLC (Frank, passive)", "B": 15500, "C": 59000, "D": 84000,
           "F": "Beg basis = tax capital (2,500) + liabilities 18,000. Income = box 1 58,600 + box 5 400. Decreases = cash 80,000 + "
                "752(b) deemed 4,000. NEGATIVE ending basis (9,500) = distribution in excess of basis -> 731(a) LTCG 8949 box F."}],
    "3b": [{"C": 0, "F": "No loss in 2025 - limitation not needed for losses; excess distribution gain 9,500 instead (see tab 11)."}],
    "11": [{"A": "Frank Russo - Ridgeview Capital Partners LLC", "B": "752b", "C": 74500, "D": 0, "E": 18000, "F": 14000, "G": 9500,
            "H": "Liability share 18,000 -> 14,000 = 4,000 deemed cash distribution (752(b)). Basis after income 74,500 < cash 80,000 + "
                 "4,000 -> 9,500 gain (731(a)); footnote confirms no 751 hot assets. Not a 704(c)/737 event."}],
    "5": [{"A": "Oak Brook Industrial Partners LP (limited partner)", "B": "N - LP, no $25k allowance", "C": 16900, "D": 58600,
           "F": "2025 loss 9,600 + PY suspended 7,300 vs Ridgeview passive income 58,600 -> all allowed; net passive income 41,700 = Sch E line 41."},
          {"A": "Permian Midstream Partners LP (PTP)", "B": "N - PTP (469(k) separate basket)", "C": 3490, "D": 0,
           "F": "2025 loss 2,340 + PY 1,150; no income from the same PTP -> 3,490 suspended to 2026; excluded from QBI."}],
    "5cells": {"E23": 350875},
    "7": [{"A": "PA (nonresident) - credit on IL-1040 Sch CR", "B": 346385, "C": 38200, "E": 1173, "G": 16864}],
    "14": [{"A": "Apple Inc 3.35% 02/09/2032 (bought 03/11/2025)", "B": 3350, "C": -1240,
            "F": "Taxable. Accrued interest paid to seller at purchase - negative Sch B line."},
           {"A": "US Treasury Note 4.25% 06/30/2030 (bought 07/15/2025)", "B": 3187.50, "C": -310,
            "F": "Taxable federal / exempt IL: IL subtraction = box 3 9,600 - 310 = 9,290."},
           {"A": "Ford Motor Credit 4.95% 2031 - accrued market discount (1099-B box 1f)", "B": 1624,
            "F": "Not 1099-INT: ratable accrual 4,250 x 1,282/3,356 days = 1,624 -> Sch B interest; 8949 code D (1,624)."}],
}

CHECKS = {
    "'3. K-1 Basis Limitation'!E13": -9500,
    "'3. K-1 Basis Limitation'!D24": 0,
    "'5. Passive Activity (8582)'!E13": -41700,
    "'5. Passive Activity (8582)'!E14": 3490,
    "'5. Passive Activity (8582)'!E28": 0,
    "'7. Multi-State Allocation'!F12": 1173,
    "'14. Bond Interest & Premium'!C19": -1550,
    "'14. Bond Interest & Premium'!B19": 8161.5,
    "'11. Hot Assets & Mixing Bowl'!G16": 9500,
}
