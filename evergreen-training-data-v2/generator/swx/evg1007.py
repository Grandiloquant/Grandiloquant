"""EVG1007 Rahman - software exceptions (CCH Axcess workbook tabs 8, 12 + log items; ProConnect equivalents).
Amounts tie to the EVG1007 answer key (Form 8949 box F 21,360; line 38 penalty 779; IL PTE credit 16,073)."""
from software_exceptions import exc

CLIENT_ID, DISPLAY = "EVG1007", "Dr. Aisha Rahman"
PREPARER, REVIEWER = "M. Novak (staff)", "L. Chen (senior)"
INTRO = """
Dr. Rahman's return hits two of the workbook's calculation tabs (S-corp dual basis and Form 2210) and four
"silent" software traps where neither package raises a diagnostic - the return simply calculates the wrong answer
from facially reasonable inputs. Those silent items are the most valuable eval cases.
"""

ITEMS = [
    exc("EVG1007-SX1", "12", "Basis/At-Risk/Passive", "S-corp distribution above STOCK basis (debt basis does not cover distributions)",
        axcess_default="If beginning basis is keyed as one blended figure ($28,000 stock + $120,000 shareholder loan = $148,000), "
                       "Axcess tests the $360,000 distribution against $148,000 + $310,640 of income = $458,640 and treats it as "
                       "fully tax-free. No capital gain is generated.",
        axcess_diagnostic="None - silent",
        manual_calc="Yes",
        axcess_fix="Income/Deductions > S Corporation Passthrough > Basis Limitation section: beginning STOCK basis $28,000 on the "
                   "stock-basis line; shareholder loan $120,000 entered only in the separate DEBT-basis lines. Recalculate - "
                   "$21,360 excess distribution flows to Form 8949 box F (LT; held since 2016). Form 7203 attached.",
        amount=21360,
        proconnect_default="ProConnect requires 'Stock basis at beginning of year' to produce Form 7203 (missing entry raises "
                           "diagnostic ref 56844). If the preparer types the blended $148,000 there, the same tax-free result occurs.",
        proconnect_fix="S Corp Info (1120S K-1) > Shareholder's Basis (7203): Stock basis at beginning of year = 28,000; Debt basis at "
                       "beginning of tax year = 120,000 (Shareholder Loan section). 7203 generates because a distribution was received; "
                       "the $21,360 gain flows to Schedule D.",
        proconnect_ref="Intuit help: 'How to complete Form 7203 and resolve diagnostic 56844 in ProConnect Tax'",
        efile_impact="None (Form 7203 required attachment when a distribution is received)",
        affected_lines=["7", "Form 8949 box F", "Form 7203"],
        procedure_section="Schedules K-1 - Debt Basis vs Stock Basis Distribution Trap",
        notes="Workbook tab 12 formula corrected to apply distributions before losses (Reg. 1.1367-1(f)); see Corrections Log."),
    exc("EVG1007-SX2", "8", "Est. Tax Penalty", "Form 2210 - organizer says 4 estimates, only 3 were paid",
        axcess_default="Axcess computes the underpayment penalty from whatever estimates are keyed. Keying the organizer "
                       "(4 x $15,000) shows no penalty; nothing compares the organizer to the IRS account transcript.",
        axcess_diagnostic="None - silent",
        manual_calc="Yes",
        axcess_fix="General > Payments: enter federal estimates by actual date paid (04/15, 06/16, 01/15/2026 = $15,000 each; Q3 $0). "
                   "Penalty section: regular method, no waiver; 110% prior-year safe harbor applies (2024 AGI $508,300 > $150,000). "
                   "Penalty $779 on line 38.",
        amount=779,
        proconnect_default="Same - ProConnect uses the estimate amounts/dates entered; no transcript check.",
        proconnect_fix="Payments, Penalties & Extensions: enter each 2025 federal estimate with its actual date paid (leave Q3 blank); let "
                       "the Form 2210 penalty compute (do not check 'suppress penalty').",
        proconnect_ref="Screen name per current release - verify",
        efile_impact="None",
        affected_lines=["26", "38"],
        procedure_section="Workpapers / Responding to Review Points",
        notes="Workbook tab 8 (corrected) shows required annual payment $120,006 vs payments $101,360 -> NOT met."),
    exc("EVG1007-SX3", "2", "Other", "SSTB flag missing from K-1 statement - QBI deduction would be ~$62,000",
        axcess_default="The K-1's Section 199A statement reports QBI, W-2 wages and UBIA but the corporation did not check the SSTB "
                       "box. Axcess applies the W-2 wage limit only and allows a ~$62,000 QBI deduction (20% x $310,000; wage limit "
                       "$120,000 and taxable-income limit $91,273 do not bind).",
        axcess_diagnostic="None - silent",
        manual_calc="No",
        axcess_fix="S Corporation Passthrough > Section 199A: check 'Specified service trade or business'. With taxable income before QBI "
                   "of $479,825 (> $247,300) the SSTB is fully phased out - QBI deduction $0.",
        amount=0,
        proconnect_default="Same - ProConnect relies on the SSTB indicator entered from the K-1 statement.",
        proconnect_fix="S Corp Info (1120S K-1) > Qualified Business Income (199A): 'Specified service trade or business' = Yes.",
        efile_impact="None",
        affected_lines=["13a", "Form 8995-A"],
        procedure_section="QBI (QOFs, QROFs)",
        notes="Pediatric medical practice is a health SSTB under 199A(d)(2)."),
    exc("EVG1007-SX4", "2", "Other", "NIIT - excess-distribution gain on active S-corp stock (Form 8960 line 5c)",
        axcess_default="The $21,360 Schedule D gain is treated as net investment income automatically (+$812 NIIT). Axcess cannot know the "
                       "corporation's assets are 100% used in a nonpassive trade or business.",
        axcess_diagnostic="None - silent",
        manual_calc="Yes",
        axcess_fix="Form 8960 input: line 5c adjustment (disposition of partnership interest or S-corp stock) = (21,360), supported by a "
                   "Reg. 1.1411-7 (proposed, may be relied on) statement. NIIT falls to $186.",
        amount=-21360,
        proconnect_default="Same - capital gain flows into NII.",
        proconnect_fix="Net Investment Income Tax (8960) screen: 'Adjustment for disposition of partnership interest or S corporation stock' = "
                       "-21,360; attach statement.",
        proconnect_ref="Field label per current release - verify",
        efile_impact="Statement attached as PDF",
        affected_lines=["Schedule 2 line 12", "Form 8960"],
        notes="Position flagged for signer (NIIT $812 higher if not taken)."),
    exc("EVG1007-SX5", "2", "Other", "State refund (1099-G $2,100) - tax benefit rule when PY SALT was capped",
        axcess_default="For a new client or when the 2024 Schedule A detail did not proforma, Axcess's state-refund worksheet has no PY "
                       "SALT/cap data and includes the full $2,100 on Schedule 1 line 1.",
        axcess_diagnostic="Informational: state and local refund worksheet requires prior-year itemized deduction information",
        manual_calc="Yes",
        axcess_fix="Income > State and local refund worksheet: enter 2024 state and local taxes paid ($31,000), SALT limitation $10,000, "
                   "2024 itemized total; worksheet computes $0 taxable (Rev. Rul. 2019-11).",
        amount=0,
        proconnect_default="Same - the taxable-refund worksheet needs prior-year itemized and SALT-limit data; otherwise the full refund is taxable.",
        proconnect_fix="Income > State and local tax refunds: complete the prior-year Schedule A / SALT limitation fields so the worksheet limits "
                       "the taxable amount to $0.",
        proconnect_ref="Verify field names in current release",
        efile_impact="None",
        affected_lines=["8 (Schedule 1 line 1)"],
        procedure_section="Schedule A - refunds of taxes itemized in a prior year"),
    exc("EVG1007-SX6", "2", "State Allocation", "Illinois PTE tax - federal Schedule A vs IL credit",
        axcess_default="If the K-1's 'state taxes paid by entity' footnote is keyed as an estimated state payment, Axcess both itemizes it "
                       "(federal) and credits it (IL) - double benefit. The tax was already deducted inside K-1 box 1.",
        axcess_diagnostic="None - silent",
        manual_calc="No",
        axcess_fix="Do not enter the PTE tax on the federal Taxes worksheet. Enter $16,073 only on the IL K-1-P passthrough credit input "
                   "(IL Schedule IL-E / PTE credit). IL exemption and property-tax credit are disallowed (AGI > $250,000).",
        amount=16073,
        proconnect_default="Same risk if entered under state estimated payments.",
        proconnect_fix="Illinois return > Pass-through entity credits: enter the IL K-1-P PTE tax credit $16,073; nothing on federal "
                       "Taxes (Schedule A).",
        efile_impact="IL return e-filed with K-1-P information",
        affected_lines=["Schedule A line 5a", "IL-1040 credits"],
        procedure_section="Schedules K-1 - PTE tax"),
]

TABS = {
    "12": [{"A": "Dr. Aisha Rahman - Lakeshore Pediatric Partners, S.C. (100%)", "B": 28000, "C": 120000, "D": 310640,
            "E": 360000,
            "G": "Stock 28,000 + income 310,640 (box 1 310,000 + box 4 640) = 338,640 < distributions 360,000 -> 21,360 LTCG "
                 "(8949 box F). Debt basis 120,000 NOT available for distributions; nondeductible exp 3,100 + charity 2,000 "
                 "then reduce DEBT basis -> 114,900 carryforward."}],
    "8": {"E12": 133340, "E14": 508300, "E15": 121500, "E19": 101360,
          "C25": 29090, "C26": 29090, "C27": 14090, "C28": 29090,
          "D25": "Y", "D26": "Y", "D27": "N - no estimate", "D28": "Y",
          "F25": "W-2 withholding 56,360 treated as paid evenly (14,090/qtr) + 15,000 estimate",
          "F27": "Q3 estimate never paid (IRS account transcript) - organizer wrong",
          "F28": "Q4 estimate paid 01/15/2026 (timely for 2025)"},
}

# Workbook formula results that must tie to the return (verified with pycel at build time)
CHECKS = {
    "'12. S-Corp Dual Basis'!F15": 21360,
    "'8. Est. Tax Penalty (2210)'!E18": 120006,
    "'8. Est. Tax Penalty (2210)'!E20": 18646,
}
