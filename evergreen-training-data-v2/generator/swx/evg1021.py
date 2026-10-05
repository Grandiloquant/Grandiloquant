"""EVG1021 Kim (Ethan) - software exceptions (CCH Axcess Diagnostics Log items; ProConnect equivalents).
Amounts tie to the EVG1021 answer key (parents' 2025 TI 402,319 / tax 80,830 from EVG1010; Form 8615 tax 642; dependent
standard deduction 3,650; unearned income 6,400)."""
from software_exceptions import exc

CLIENT_ID, DISPLAY = "EVG1021", "Ethan S. Kim"
PREPARER, REVIEWER = "Staff preparer", "M. Okafor (senior)"
INTRO = """
A simple kiddie-tax return whose only real risk is stale or missing parent data. Form 8615 is computed from the parents'
taxable income and tax, which live on a different return (EVG1010). Whatever parent figures are in the child's return
when it is calculated are used without question - the draft used the parents' 2024 numbers. In ProConnect the parent's
information is always a manual entry (no Family Link - that is a Lacerte feature).
"""

ITEMS = [
    exc("EVG1021-SX1", "2", "Other", "Form 8615 parent figures - stale 2024 data / manual entry; must match the FINAL EVG1010 return",
        axcess_default="Form 8615 uses the parent's taxable income, filing status and tax entered on the child's return. The first draft "
                       "carried the parents' 2024 taxable income ($357,750) because EVG1010 was not final; the calculation runs without a "
                       "diagnostic once any parent figure is present. Entering the parents' line 16 including the $55 Form 8814 tax for "
                       "Chloe also overstates line 10.",
        axcess_diagnostic="None - silent",
        manual_calc="Yes",
        axcess_fix="Form 8615 (Kiddie tax) input: parents Daniel & Grace Kim, MFJ, 2025 taxable income $402,319, qualified dividends $5,904, "
                   "net capital gain $9,877, tax $80,830 (excluding the $55 Form 8814 tax); no other children's NUI (Chloe is on Form 8814). "
                   "Result: tax on NUI $628 + $14 = $642 (line 16). Release only after EVG1010 is locked/accepted (verify field names in "
                   "current release).",
        amount=402319,
        proconnect_default="ProConnect has no Family Link (that is a Lacerte feature); the parent's information is not pulled from the "
                           "parents' return. Without it, diagnostic ref 826 ('Form 8615 must be filed') appears and the tax cannot be "
                           "computed correctly.",
        proconnect_fix="Taxes > Children Under 18 (8615) > Parent's Information: enter the parents' names/SSN, filing status MFJ, taxable "
                       "income 402,319, tax 80,830, and the qualified dividend / capital gain figures; update manually if EVG1010 changes.",
        proconnect_ref="Intuit help: 'How do you generate Form 8615 in ProConnect Tax'; 'resolve diagnostic Ref 826'",
        efile_impact="None (transmit after EVG1010 is accepted - duplicate-dependent reject risk otherwise)",
        affected_lines=["16", "Form 8615"],
        procedure_section="Kid Taxes and Filings",
        notes="If EVG1010 is ever amended, Ethan's Form 8615 must be recomputed and his return amended."),
    exc("EVG1021-SX2", "2", "Other", "'Can be claimed as a dependent' box - dependent standard deduction $3,650",
        axcess_default="Unless the 'can be claimed as a dependent' indicator is checked on the child's return, Axcess gives the full single "
                       "standard deduction ($15,750) -> taxable income $0 and Form 8615 has nothing to tax.",
        axcess_diagnostic="None - silent",
        manual_calc="No",
        axcess_fix="General > Basic Data: check 'Taxpayer can be claimed as a dependent'. Standard deduction = greater of $1,350 or earned "
                   "income $3,200 + $450 = $3,650; taxable income $5,950.",
        amount=3650,
        proconnect_default="Same - the dependent standard deduction applies only when the 'can be claimed as a dependent' box is checked.",
        proconnect_fix="General > Taxpayer information: 'Can be claimed as a dependent on another return' = Yes (field per current release - verify).",
        efile_impact="None",
        affected_lines=["12e", "15"],
        procedure_section="Kid Taxes and Filings"),
    exc("EVG1021-SX3", "2", "Other", "Form 8814 rolled forward on the parents' return although Ethan no longer qualifies",
        axcess_default="The parents' 2024 return reported Ethan's UTMA income on Form 8814; proforma carries that 8814 input into EVG1010 for "
                       "2025. Nothing tests the 8814 eligibility rules (only interest/dividends, gross income < $13,500, no estimates/"
                       "withholding) against the capital-gain sale and summer wages, so his income could be reported on the wrong return.",
        axcess_diagnostic="None - silent",
        manual_calc="No",
        axcess_fix="EVG1010: delete Ethan's Form 8814 input (keep Chloe's). Set up EVG1021 as its own client/return: unearned income $6,400 "
                   "(interest $900 + dividends $2,400 + LTCG $3,100) > $2,700 -> Form 8615 on Ethan's own 1040.",
        amount=6400,
        proconnect_default="Same - a Form 8814 entry carried forward on the parents' return is not tested against the child's other income.",
        proconnect_fix="Parents' return: remove Ethan's 8814 entry (Taxes > Children's Interest and Dividends, screen per current release - "
                       "verify); prepare Ethan's own 1040 with Form 8615.",
        efile_impact="None",
        affected_lines=["Entire return", "EVG1010 Form 8814"],
        procedure_section="Kid Taxes and Filings"),
]

TABS = {}   # log-only items - no calculation tab applies
CHECKS = {}
