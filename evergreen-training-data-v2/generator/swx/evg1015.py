"""EVG1015 Iyer - software exceptions (CCH Axcess workbook tab 24 + log items; ProConnect equivalents).
Amounts tie to the EVG1015 answer key (Form 3520 Part IV gift 150,812.53; FTC 310 vs TDS 644; Indian interest
NRE 4,819 + NRO 2,065; FBAR aggregate max 202,648)."""
from software_exceptions import exc

CLIENT_ID, DISPLAY = "EVG1015", "Rajesh & Anita Iyer"
PREPARER, REVIEWER = "Staff preparer", "D. Morgan (senior)"
INTRO = """
Green-card holders with Indian accounts. Every number that matters here arrives in rupees on an April-March certificate,
so both packages are only as good as the USD amounts typed in: neither converts currency, splits an Indian fiscal year, or
knows the US-India treaty rate. The foreign tax credit is the most dangerous item - entering the TDS actually withheld
produces a larger credit with no diagnostic, and the de minimis shortcut can drop Form 1116 altogether. Form 3520 is a
separate paper filing outside the e-filed 1040 in both packages (and is not supported at all in ProConnect).
"""

ITEMS = [
    exc("EVG1015-SX1", "24", "Other", "Form 3520 Part IV - INR 1.3 crore gift from a nonresident-alien parent (separate paper filing)",
        axcess_default="Nothing on the 1040 inputs triggers Form 3520 - a gift is not income, so no amount is entered and no form or "
                       "diagnostic is produced. The 1040 e-files without it.",
        axcess_diagnostic="None - silent",
        manual_calc="Yes",
        axcess_fix="Prepare Form 3520 (Part IV, gift from a nonresident alien individual > $100,000) jointly for the MFJ filers: $150,812.53 "
                   "per the Chase wire credit 06/18/2025 (actual USD received). Form 3520 cannot be e-filed - mail separately to the IRS "
                   "(Ogden) by the extended 1040 due date 10/15/2026; certified mail 09/23/2026. Whether it is generated in Axcess or "
                   "prepared from the IRS PDF depends on the firm's Axcess form coverage (verify in current release).",
        amount=150812.53,
        proconnect_default="Form 3520 is not supported in ProConnect Tax.",
        proconnect_fix="Prepare Form 3520 outside ProConnect (IRS fillable PDF or other software) and mail it separately; it cannot be "
                       "e-filed in any case. The 1040 itself is still e-filed from ProConnect.",
        proconnect_ref="Intuit Accountants Community: 'Does ProConnect generate Form 3520...'",
        efile_impact="1040 e-filed; Form 3520 paper-filed separately (penalty up to 25% of the gift if missed)",
        affected_lines=["Form 3520 Part IV", "Schedule B line 8 (No - not a foreign trust)"],
        procedure_section="Foreign Trusts / Other Reportable Transactions",
        notes="The money sits in a US account (not a foreign account for FBAR/8938)."),
    exc("EVG1015-SX2", "2", "Other", "Foreign tax credit - TDS withheld at 31.2% but only the 15% treaty rate is creditable",
        axcess_default="Axcess credits whatever foreign tax is entered. Keying the SBI TDS actually withheld (INR 56,160 = $644) gives a $644 "
                       "credit; the software cannot know a treaty caps Indian tax on interest at 15% (Art. 11(2)) or that the excess is "
                       "refundable from India.",
        axcess_diagnostic="None - silent",
        manual_calc="Yes",
        axcess_fix="Foreign Tax Credit (1116) > passive category, India: foreign taxes paid = INR 27,000 (15% x NRO INR 180,000) / 87.147 = $310. "
                   "Excess INR 29,160 ($335) is not a compulsory payment (Reg. 1.901-2(e)(5)) - client to claim refund in India (ITR + "
                   "Form 10F/TRC).",
        amount=310,
        proconnect_default="Same - the credit is computed from the foreign tax amount entered.",
        proconnect_fix="Foreign Tax Credit (1116) input: foreign taxes paid = 310 (creditable amount only); document the treaty limitation "
                       "(screen/field per current release - verify).",
        efile_impact="None",
        affected_lines=["20 (Schedule 3 line 1)", "Form 1116"],
        procedure_section="Form 1116",
        notes="Limitation $1,220 >> $310, so the full creditable amount is allowed."),
    exc("EVG1015-SX3", "2", "Other", "De minimis FTC election is not available - Form 1116 must be produced",
        axcess_default="Foreign taxes under $600 (MFJ) on passive income can go straight to Schedule 3 line 1 without Form 1116 when the "
                       "de minimis election is made. If the election setting is on (firm template or preparer following the procedure's "
                       "'$600 MFJ - skip the 1116' shortcut), no 1116 prints and nothing flags it; the software cannot know the income is "
                       "not reported on a qualified payee statement.",
        axcess_diagnostic="None - silent",
        manual_calc="No",
        axcess_fix="Foreign Tax Credit input: do NOT elect the de minimis exception (force Form 1116). Indian bank certificates / Form 16A "
                   "are not qualified payee statements (1099/K-1/1042-S). Passive category, country India (verify field path in current release).",
        amount=310,
        proconnect_default="Same - the election to claim the credit without Form 1116 is an input choice; ProConnect does not test the "
                           "payee-statement requirement.",
        proconnect_fix="Foreign Tax Credit (1116): leave 'elect not to file Form 1116' unchecked / force Form 1116 (field per current release - verify).",
        efile_impact="None",
        affected_lines=["Form 1116", "Schedule 3 line 1"],
        procedure_section="Form 1116",
        notes="Procedure text '$600 MFJ - skip the 1116' is imprecise; IRC 904(j) also requires qualified payee statements."),
    exc("EVG1015-SX4", "2", "Other", "Indian interest on an April-March fiscal year in INR - calendar 2025 USD must be built by hand",
        axcess_default="Axcess has no currency conversion or fiscal-year split for foreign interest; it reports the USD amount typed in. "
                       "Keying the FY 2024-25 certificate totals (and omitting NRE interest because it is exempt in India) under-reports "
                       "2025 interest and NIIT with no diagnostic.",
        axcess_diagnostic="None - silent",
        manual_calc="Yes",
        axcess_fix="Income > Interest Income: HDFC NRE $4,819 (INR 420,000) and SBI NRO $2,065 (INR 180,000) - calendar 2025 = Jan-Mar from "
                   "FY 2024-25 + Apr-Dec from FY 2025-26 certificates, converted at the IRS 2025 yearly average 87.147. Mark as foreign "
                   "(India) so they source to Form 1116; they flow into Form 8960 NII automatically.",
        amount=6884,
        proconnect_default="Same - foreign interest is entered in USD; no FX or fiscal-year logic.",
        proconnect_fix="Income > Interest Income: two foreign-payer entries in USD (4,819 / 2,065), country India, linked to Form 1116 "
                       "(screen/field per current release - verify).",
        efile_impact="None",
        affected_lines=["2b", "Schedule B", "Form 1116", "Form 8960"],
        procedure_section="Foreign Transactions",
        notes="NRE interest is exempt in India (s.10(4)(ii)) but fully taxable in the US. 2023-2024 omissions referred to signer (CONS project)."),
    exc("EVG1015-SX5", "2", "Other", "FBAR maximum values - Treasury 12/31 rate, and the three mutual fund folios",
        axcess_default="If the FinCEN 114 is prepared from the tax software's FBAR input, it rolls last year's 4 bank accounts and converts "
                       "with whatever value is entered. Reusing the IRS average rate (87.147) used for income, or omitting the 3 mutual fund "
                       "folios ('other financial accounts'), is not flagged.",
        axcess_diagnostic="None - silent",
        manual_calc="Yes",
        axcess_fix="FBAR (FinCEN 114) input: 7 accounts (4 bank + 3 MF folios), maximum values converted at the Treasury Reporting Rate for "
                   "12/31/2025 (assumed INR 89.87 - verify to the published table); aggregate $202,648. One FBAR by Rajesh with Anita's Form "
                   "114a (all joint). Form 8938 is a separate requirement (year-end $194,843 > $100,000 MFJ), mutual funds listed as "
                   "excepted assets (3 Forms 8621).",
        amount=202648,
        proconnect_default="Same - FBAR values are entered by the preparer; no rate logic.",
        proconnect_fix="FBAR is filed through BSA E-Filing (from the software's FinCEN 114 input if used, or directly). Enter USD maximum values "
                       "at the Treasury 12/31 rate for all 7 accounts (screen per current release - verify).",
        efile_impact="FBAR filed separately via BSA E-Filing (09/22/2026); due 10/15/2026 automatic extension",
        affected_lines=["Schedule B line 7a", "FinCEN 114", "Form 8938"],
        procedure_section="FinCEN114/FBAR"),
]

TABS = {
    "24": [
        {"A": "Foreign gift - Form 3520 Part IV (gift > $100,000 from a nonresident alien individual)",
         "B": "Anita's father (Indian resident, NRA) wired INR 1.3 crore 06/18/2025 to the joint Chase account. Not income. Joint 3520 "
              "(MFJ). Due 10/15/2026 with the extended return; paper only.",
         "C": "PBC - Chase incoming wire advice 06/18/2025; WP Form 3520 + certified-mail receipt 09/23/2026",
         "D": 150812.53,
         "E": "No 1040 income input. Form 3520 prepared separately (Axcess form coverage per current release - verify); ProConnect: not supported",
         "F": "Staff preparer 09/2026 / D. Morgan"},
    ],
}

CHECKS = {  # tab 24 has no formulas - check the logged amount itself ties to the answer key
    "'24. Rare-Event Log'!D11": 150812.53,
}
