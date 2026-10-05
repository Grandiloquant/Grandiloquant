"""EVG1012 Hoffman - software exceptions (CCH Axcess workbook tab 8 + log items; ProConnect equivalents).
Amounts tie to the EVG1012 answer key (Form 6252 gain 16,904; seller-financed interest 17,983; NC Bailey deduction 30,788;
total tax 12,817; payments 12,780; 2024 tax 20,486 / AGI 171,273)."""
from software_exceptions import exc

CLIENT_ID, DISPLAY = "EVG1012", "Walter & June Hoffman"
PREPARER, REVIEWER = "Staff preparer", "L. Chen (senior)"
INTRO = """
A retiree return where the software's carry-forward data is necessary but not sufficient. The installment note proformas
from 2024, but Axcess cannot know what was actually received in 2025, so a blank organizer line silently produces no
gain and no interest. The NC Bailey exclusion depends on a fact (June's 1989 vesting) that is nowhere on the 1099-R.
The Form 2210 item documents why no penalty override is needed and flags the 2026 voucher amount.
"""

ITEMS = [
    exc("EVG1012-SX1", "2", "Other", "Installment sale year 2 - proforma'd Form 6252 computes $0 when 2025 payments are blank",
        axcess_default="The 2024 Form 6252 rolls forward with the contract price, gross profit % (73.0952%) and note balance, but the "
                       "current-year 'payments received' fields are blank because the organizer line was blank. Axcess computes $0 "
                       "installment gain and the note interest never reaches Schedule B. If the attorney's amortization schedule is keyed "
                       "instead of actual receipts, it picks up 12 payments (the December check was received 01/06/2026).",
        axcess_diagnostic="None - silent",
        manual_calc="Yes",
        axcess_fix="Gains and Losses > Installment Sales (Form 6252), Caldwell land note: 2025 principal received $23,126 (11 payments, "
                   "amortization-schedule split - interest first). Gain = 23,126 x 73.0952% = $16,904 LT (Schedule D line 11). "
                   "No 1250/1245 recapture (unimproved land). Payment 12 (received 01/06/2026) goes to 2026.",
        amount=16904,
        proconnect_default="Same - the installment sale carries forward from the prior year, but the current-year payment must be entered; "
                           "blank = no gain.",
        proconnect_fix="Dispositions > Installment Sale (6252): enter 2025 payments received (principal) $23,126; confirm gross profit % 73.0952% "
                       "carried from 2024 and line 26 gain $16,904 (field names per current release - verify).",
        efile_impact="None",
        affected_lines=["7", "Form 6252 line 21/26", "Schedule D line 11"],
        procedure_section="Return - General Return Prep Notes (blank organizer line is not zero) / Installment Sales",
        notes="Cash-basis: payments count when received. PERM note balance 12/31/2025 $312,874."),
    exc("EVG1012-SX2", "2", "Other", "Seller-financed mortgage interest - buyer's name, SSN and address must print first on Schedule B",
        axcess_default="Note interest keyed as an ordinary interest payer (or lumped with the bank CD) prints as a plain Schedule B line; "
                       "the seller-financed disclosure (buyer name/SSN/address, listed first) is only produced when the interest is "
                       "flagged as seller-financed mortgage interest. Nothing prompts for it.",
        axcess_diagnostic="None - silent",
        manual_calc="Yes",
        axcess_fix="Income > Interest Income: payer 'Aaron M. & Beth L. Caldwell', mark as seller-financed mortgage (buyer used property as a "
                   "personal residence), enter buyer SSN XXX-XX-6641 and address; amount $17,983 = amortization-schedule interest on 11 "
                   "payments $17,908 + $75 late charge (verify field path in current release).",
        amount=17983,
        proconnect_default="Same - the seller-financed indicator and buyer information must be entered on the interest input.",
        proconnect_fix="Income > Interest Income (1099-INT, 1099-OID): enter the Caldwell note as a separate payer with the 'seller-financed "
                       "mortgage' option and the buyer's SSN/address (screen/field per current release - verify).",
        efile_impact="None ($50 penalty for omitting the buyer SSN)",
        affected_lines=["2b", "Schedule B line 1"],
        procedure_section="Schedule B"),
    exc("EVG1012-SX3", "2", "State Allocation", "NC Bailey settlement - June's TSERS pension taxed by default",
        axcess_default="The NC return taxes every 1099-R that is taxable federally unless the distribution is identified as a "
                       "Bailey-qualifying government retirement benefit. The 1099-R itself carries no Bailey indicator, and Walter's "
                       "private pension and IRA must stay taxable - so the result depends entirely on a per-1099-R state input.",
        axcess_diagnostic="None - silent",
        manual_calc="No",
        axcess_fix="North Carolina > Retirement/Schedule S deductions: mark June's TSERS 1099-R as Bailey-exempt (5+ years creditable service "
                   "as of 08/12/1989 - PERM). Schedule S: SS $49,317 + Bailey $30,788. Leave Walter's pension and IRA taxable. NC taxable "
                   "income $51,829; tax $2,203 (verify field path in current release).",
        amount=30788,
        proconnect_default="Same - the Bailey deduction is driven by a state-specific input per 1099-R.",
        proconnect_fix="North Carolina return > retirement benefits (Bailey) input for June's TSERS 1099-R = $30,788 (screen/field per current "
                       "release - verify).",
        efile_impact="NC D-400 e-filed",
        affected_lines=["NC D-400 Schedule S"],
        procedure_section="SALT Implications"),
    exc("EVG1012-SX4", "8", "Est. Tax Penalty", "Form 2210 - 110% prior-year safe harbor missed, 90% current-year test met; 2026 vouchers",
        axcess_default="Axcess correctly computes the lesser of 90% of 2025 tax and 110% of 2024 tax (2024 AGI $171,273) - no penalty. "
                       "The trap is a manual one: forcing a penalty because the 110% test failed, or (for 2026) hand-setting vouchers at "
                       "4 x $1,500 using the 100% rule. 2025 AGI is $157,434 (> $150,000), so the 2026 prior-year safe harbor "
                       "is 110% of $12,817 = $14,099; withholding at the 2025 level + 4 x $1,500 = $12,780 falls short of it by $1,319.",
        axcess_diagnostic="None - silent",
        manual_calc="Yes",
        axcess_fix="Penalties and Interest: no override, no waiver - regular method; required annual payment $11,535 (90% of 2025 tax) is met "
                   "every quarter. Estimates input for 2026: let the 110% method compute vouchers (or document a 90%-of-2026 projection if "
                   "the clients prefer $1,500/quarter).",
        amount=0,
        proconnect_default="Same calculation - ProConnect uses the lesser of the 90% / 110% tests from the prior-year data entered.",
        proconnect_fix="Payments, Penalties & Extensions: confirm 2024 tax $20,486 and AGI $171,273 are entered; no penalty override. 2026 "
                       "estimate vouchers: 110% method (screen per current release - verify).",
        efile_impact="None",
        affected_lines=["38", "2026 Form 1040-ES"],
        procedure_section="Workpapers / Estimated tax",
        notes="Caught in v2 review: the draft open item applied the 100% rule (2025 AGI $157,434 > $150,000). Preparer Notes now "
              "recommend 4 x $1,830 federal estimates for 2026."),
]

TABS = {
    "8": {"E12": 12817, "E14": 171273, "E15": 20486, "E19": 12780,
          "C25": 3195, "C26": 3195, "C27": 3195, "C28": 3195,
          "D25": "Y", "D26": "Y", "D27": "Y", "D28": "Y",
          "F25": "1099-R withholding 6,780 treated as paid evenly (1,695/qtr) + 1,500 estimate 04/15/2025",
          "F26": "1,695 + 1,500 estimate 06/16/2025", "F27": "1,695 + 1,500 estimate 09/15/2025",
          "F28": "1,695 + 1,500 estimate paid 01/15/2026 (timely for 2025)"},
}

CHECKS = {
    "'8. Est. Tax Penalty (2210)'!E17": 22535,
    "'8. Est. Tax Penalty (2210)'!E18": 11535,
    "'8. Est. Tax Penalty (2210)'!E20": 0,
    "'8. Est. Tax Penalty (2210)'!E28": 0,
}
