"""EVG1024 Abernathy - software exceptions (CCH Axcess workbook tabs 10, 18, 20, 22, 24 + log items; ProConnect equivalents).
Amounts tie to the EVG1024 answer key: Form 982 exclusion 38,000 (insolvency 48,000); 2026 capital loss carryover 67,000 before /
29,000 after the IRC 108(b) reduction; IRC 1244 ordinary loss 50,000 + worthless-stock LT capital loss 100,000; IRC 691(c) 60,000;
foreign trust DNI 85,000 (interest 15,000 / qualified dividends 40,000 / LTCG 30,000) + corpus 35,000."""
from software_exceptions import exc

CLIENT_ID, DISPLAY = "EVG1024", "Margaret \"Peggy\" Abernathy"
PREPARER, REVIEWER = "T. Nguyen (staff)", "R. Patel (senior)"
INTRO = """
Peggy's return is built almost entirely from documents that neither package can interpret on its own: a 1099-C that is excluded
under the insolvency exception, the attribute reduction that exclusion forces on next year's capital loss carryover, founder stock
that is part IRC 1244 ordinary loss and part worthless-stock capital loss (no 1099-B), an estate-tax deduction (IRC 691(c)) that
depends on an attorney's letter, and a distribution from a foreign non-grantor trust that must be split by character from a
Foreign Nongrantor Trust Beneficiary Statement and reported on a Form 3520 that is filed on paper. Most of these are **silent** -
the software calculates a facially valid return from the 1099s. Same tax answer in both packages; only the mechanics differ.
"""

ITEMS = [
    exc("EVG1024-SX1", "20", "Other", "1099-C $38,000 - insolvency exclusion (Form 982) must be built and elected manually",
        axcess_default="The 1099-C input flows the $38,000 to Schedule 1 line 8c as cancellation-of-debt income. Axcess has no balance "
                       "sheet and cannot test insolvency, so the return simply taxes the COD (about $10,191 of extra tax including NIIT).",
        axcess_diagnostic="None - silent",
        manual_calc="Yes",
        axcess_fix="Workbook tab 20: assets 377,000 / liabilities 425,000 immediately before the 03/18/2025 discharge (incl. the 401(k); "
                   "excl. the July inheritance) -> insolvency 48,000 -> excludable 38,000. Then Income > Cancellation of debt / Form 982 "
                   "input: check 'Discharge of indebtedness to the extent insolvent' (line 1b) and enter 38,000 as the excluded amount; "
                   "confirm Schedule 1 line 8c drops to $0 (verify field path in current release).",
        amount=38000,
        proconnect_default="Same - the 1099-C amount is taxable unless the insolvency section is completed.",
        proconnect_fix="Income > 1099-C > Canceled Debt Worksheet: complete the Insolvency section (total liabilities 425,000 and total "
                       "assets 377,000 immediately before the cancellation); the excluded $38,000 flows to Form 982 line 1b/line 2. "
                       "Attribute reduction still requires manual review (see SX2).",
        proconnect_ref="Intuit help: 'Entering a Form 1099-C with insolvency (Form 982)'",
        efile_impact="None (Form 982 is e-filed with the 1040)",
        affected_lines=["8 (Sch 1 line 8c)", "Form 982 lines 1b, 2"],
        procedure_section="Return - Form 982 (insolvency)",
        notes="Client's own worksheet used 12/31/2025 balances, counted the inherited IRA and omitted the 401(k) - all three wrong."),
    exc("EVG1024-SX2", "10", "Capital Loss", "IRC 108(b) attribute reduction - 2026 capital loss carryover must be overridden (67,000 -> 29,000)",
        axcess_default="Axcess computes the 2025 Capital Loss Carryover Worksheet (LT 67,000) and proformas it to 2026. Completing Form 982 "
                       "Part II does not reduce the carryover that rolls forward - the 2026 return would deduct losses that were "
                       "eliminated by the excluded COD.",
        axcess_diagnostic="None - silent",
        manual_calc="Yes",
        axcess_fix="Form 982 Part II line 9 (net capital loss / carryovers; verify line number in current revision) = 38,000. Workbook tab 10 "
                   "documents the pre-reduction carryover (ST 0 / LT 67,000); attach the reduction statement. In the 2026 proforma: "
                   "Income > Capital Gains and Losses > Carryovers: override LT capital loss carryover to 29,000 (ST 0).",
        amount=29000,
        proconnect_default="Same - ProConnect carries the unreduced 67,000 forward; the 982 attribute-reduction lines are informational "
                           "for the carryover.",
        proconnect_fix="Form 982 Part II line 9 = 38,000 (Canceled Debt / 982 inputs); in the 2026 return override the prior-year long-term "
                       "capital loss carryover to 29,000 on the Schedule D carryover input (screen/field per current release - verify).",
        proconnect_ref="Intuit help: 'Entering a Form 1099-C with insolvency (Form 982)' - attribute reduction requires manual review",
        efile_impact="None",
        affected_lines=["Form 982 line 9", "2026 Schedule D lines 6/14"],
        procedure_section="Return - Form 982 Part II (attribute reduction)",
        notes="Reduction is made after the 2025 tax is determined (IRC 108(b)(4)(A)); the 2025 $3,000 deduction is unaffected. Tab 10 "
              "inputs here are the 2025 (year-of-discharge) Schedule D figures, used to compute the 2025->2026 carryover."),
    exc("EVG1024-SX3", "22", "Capital Loss", "Brightline founder stock - IRC 1244 ordinary loss + worthless-stock capital loss (no 1099-B)",
        axcess_default="There is no 1099-B for worthless stock. If the preparer keys the $150,000 on the Capital Gains worksheet with "
                       "default 'Capital' character, Axcess reports a $150,000 LT capital loss and allows $3,000 - the $50,000 ordinary "
                       "loss is lost. Axcess cannot know the stock qualifies under IRC 1244.",
        axcess_diagnostic="None - silent",
        manual_calc="Yes",
        axcess_fix="Workbook tab 22 (two rows). Capital Gains and Losses worksheet: line 1 - Brightline Analytics common, acquired 06/12/2019, "
                   "sold 12/31/2025 (IRC 165(g) deemed date), proceeds 0, cost 50,000, category changed from 'Capital' to 'Section 1244 "
                   "Ordinary Loss' -> Form 4797 Part II line 10 (Schedule 1 line 4: -50,000). Line 2 - same stock, cost 100,000, "
                   "'Worthless', long-term, Form 8949 box F.",
        amount=-50000,
        proconnect_default="Same - a disposition entered without the section 1244 indicator is a capital loss.",
        proconnect_fix="Dispositions (Schedule D/4797): enter two lines - $50,000 marked as section 1244 / ordinary (flows to Form 4797 Part II) "
                       "and $100,000 as a long-term worthless-security capital loss with date sold 12/31/2025, box F (screen/field per "
                       "current release - verify).",
        efile_impact="None",
        affected_lines=["Sch 1 line 4", "Form 4797 line 10", "Form 8949 box F", "7"],
        procedure_section="Schedule D",
        notes="1244 limit $50,000 single; original issuance for cash; capitalization $750,000 <= $1M; active receipts. Worthless in 2025 "
              "(plan of dissolution, no stockholder distributions)."),
    exc("EVG1024-SX4", "18", "Other", "IRC 691(c) deduction on inherited IRA distribution - not derived from the 1099-R",
        axcess_default="The 1099-R (code 4) flows $150,000 to line 4b. Axcess computes no IRC 691(c) deduction - it has no estate-tax data. "
                       "The firm workbook's ORIGINAL tab 18 formula (IRA value - estate tax = 2,400,000 - 1,764,000 = 636,000) would "
                       "have produced a meaningless figure.",
        axcess_diagnostic="None - silent",
        manual_calc="Yes",
        axcess_fix="Workbook tab 18 (IRD row - column E typed over per the Corrections Log): (1,764,000 - 804,000) x 150,000 / 2,400,000 = "
                   "60,000. Enter on Itemized Deductions > Miscellaneous Deductions > Income in Respect of a Decedent (Schedule A line 16, "
                   "no 2% floor); attach the computation statement.",
        amount=60000,
        proconnect_default="Same - the 1099-R entry produces no 691(c) deduction.",
        proconnect_fix="Itemized Deductions > Other itemized deductions: 'Federal estate tax on income in respect of a decedent' = 60,000 "
                       "(screen/field per current release - verify); statement attached.",
        efile_impact="None",
        affected_lines=["12e", "Schedule A line 16"],
        procedure_section="Estate Implications",
        notes="Federal estate tax only - Connecticut estate tax excluded. Remaining 691(c) pool for Peggy's future withdrawals 420,000."),
    exc("EVG1024-SX5", "24", "Other", "Foreign non-grantor trust distribution - actual method character split from the FNTBS",
        axcess_default="Axcess has no input that reads a Foreign Nongrantor Trust Beneficiary Statement. Keyed as one $120,000 'other income' "
                       "amount it is all ordinary (and the $35,000 of corpus is taxed); left out because the client calls it an "
                       "inheritance, $85,000 of income is omitted. The software also cannot know undistributed net income is $0.",
        axcess_diagnostic="None - silent",
        manual_calc="Yes",
        axcess_fix="Workbook tab 24 (rare-event log, FNTBS as the workpaper). Enter by character: Interest input - 'Hale Family Settlement "
                   "(foreign trust)' 15,000; Dividends input - 40,000 ordinary / 40,000 qualified; Capital Gains - Schedule D line 12 "
                   "(estates and trusts) 30,000 LT. Corpus 35,000 not entered. No accumulation distribution -> no Form 4970 / Form 3520 "
                   "interest-charge override.",
        amount=85000,
        proconnect_default="Same - ProConnect has no FNTBS import; amounts are taxed as entered.",
        proconnect_fix="Enter the three income items on the Interest, Dividends and Dispositions/Schedule D screens with the trust as payer; "
                       "do not enter the 35,000 corpus (screen/field per current release - verify).",
        efile_impact="None for the 1040 (Form 3520 - see SX6)",
        affected_lines=["2b", "3a", "3b", "7", "Sch B Part III line 8"],
        procedure_section="Foreign Trusts",
        notes="Actual method allowed: trustee appointed a U.S. agent and issued the FNTBS. Default method / throwback would be wrong."),
    exc("EVG1024-SX6", "PC", "E-file Disqualifying", "Form 3520 Part III - not supported in ProConnect; separate paper filing",
        axcess_default="Form 3520 is not part of the 1040 e-file in any package. Per the workbook's tab 24 guidance Axcess has a Form 3520 / "
                       "Miscellaneous Taxes input; whether the current release produces a complete Part III is not relied on - firm "
                       "practice: prepare Form 3520 separately and mail it.",
        axcess_diagnostic="None - silent",
        manual_calc="No",
        axcess_fix="Prepare Form 3520 Part III (lines 24-33, FNTBS attached, actual method) outside the 1040 e-file; mail to IRS Ogden by "
                   "10/15/2026 (extended due date), certified. Log on workbook tab 24.",
        amount=120000,
        proconnect_default="ProConnect does not generate Form 3520.",
        proconnect_fix="Prepare Form 3520 outside ProConnect (IRS fillable PDF) and mail it separately to the IRS (it cannot be e-filed). "
                       "In ProConnect answer the Schedule B Part III foreign-trust question 'Yes' so line 8 prints.",
        proconnect_ref="Intuit Accountants Community: 'Does ProConnect generate Form 3520...'",
        efile_impact="1040 e-filed; Form 3520 paper-filed separately (IRS Ogden)",
        affected_lines=["Form 3520", "Sch B line 8"],
        procedure_section="Foreign Trusts / Paper Filing Returns",
        notes="Penalty for failure to file: greater of $10,000 or 35% of the distribution ($42,000)."),
    exc("EVG1024-SX7", "2", "Other", "Schedule B Part III line 8 and Form 8938 - foreign trust interest (excepted asset)",
        axcess_default="Schedule B line 8 (distribution from a foreign trust) is answered from the general foreign-trust question - it "
                       "defaults to No. Form 8938 is only produced from 8938 inputs; nothing tells the software that a beneficial "
                       "interest in a foreign trust (value = distributions received $120,000) crosses the $75,000 any-time threshold.",
        axcess_diagnostic="None - silent",
        manual_calc="No",
        axcess_fix="General / Foreign accounts and trusts input: 'received a distribution from a foreign trust' = Yes. Form 8938 input: "
                   "Part IV excepted specified foreign financial assets - number of Forms 3520 = 1 (verify field path in current release).",
        amount=120000,
        proconnect_default="Same - question-driven; Form 8938 only if 8938 inputs are completed.",
        proconnect_fix="Schedule B foreign trust question = Yes; Foreign Reporting > Form 8938: list the excepted asset (Form 3520 count 1) "
                       "(screen/field per current release - verify).",
        efile_impact="None",
        affected_lines=["Sch B line 8", "Form 8938"],
        procedure_section="Foreign Trusts",
        notes="No FBAR - no foreign financial account; discretionary beneficiary does not report the trust's accounts."),
]

TABS = {
    "20": [{"A": "Citibank, N.A. - Double Cash ****7781 (1099-C, event 03/18/2025, code F)", "B": 377000, "C": 425000, "D": 38000,
            "E": "Balance sheet immediately before discharge (03/17/2025): assets incl. 401(k) 62,400 (Carlson); liabilities incl. "
                 "full card balance 52,400; inherited IRA NOT counted (father died 07/14/2025, after discharge). Insolvent 48,000 >= "
                 "38,000 -> all excluded; taxable COD 0. Attribute reduction: capital loss carryover (Form 982 line 9) 38,000 - see tab 10."}],
    "10": {"D10": 3000, "D11": 0, "D12": 70000},
    "22": [{"A": "Brightline Analytics, Inc. common (1,500,000 sh) - section 1244 portion", "B": "§1244", "C": "12/31/2025",
            "D": 50000, "E": 50000, "F": -50000, "G": "Ordinary - Form 4797 Part II line 10 (single limit $50,000)",
            "H": "Original issuance 06/12/2019 for $150,000 cash; capital <= $1M; active SaaS receipts; worthless 2025 (dissolved, no "
                 "stockholder distributions). Deemed sold 12/31/2025 (IRC 165(g))."},
           {"A": "Brightline Analytics, Inc. common - excess over 1244 limit (worthless security)", "B": "Worthless stock (§165(g))",
            "C": "12/31/2025", "D": 100000, "E": 0, "F": -100000, "G": "Capital - long-term (held since 2019), Form 8949 box F",
            "H": "Nets with trust LTCG 30,000 -> Sch D line 16 (70,000); 3,000 allowed; carryover 67,000 before Form 982 reduction."}],
    "18": [{"A": "Fidelity Inherited IRA - Peggy (50% beneficiary of Harold J. Abernathy, d. 07/14/2025)", "B": 2400000, "C": 1764000,
            "D": 0.0625, "E": 60000,
            "F": "IRD (691(c)): federal estate tax 1,764,000 - tax without IRA 804,000 = 960,000 attributable to IRD x IRD received "
                 "150,000 / total IRD 2,400,000 (6.25%) = 60,000. Column E typed over (original formula B-C = 636,000 is meaningless - "
                 "Corrections Log). CT estate tax excluded. Sch A line 16."}],
    "24": [{"A": "Foreign trust distribution (Form 3520 Part III)", "B": "Hale Family Settlement (Jersey, foreign non-grantor trust; U.S. "
            "agent appointed). Distribution 10/06/2025 $120,000: DNI 85,000 (interest 15,000; UK qualified dividends 40,000; net LTCG "
            "30,000) + corpus 35,000. UNI $0 -> no accumulation distribution / no throwback.",
            "C": "PBC/17_Hale_Family_Settlement_Foreign_Nongrantor_Trust_Beneficiary_Statement_2025.pdf; WP 3520",
            "D": 85000, "E": "Interest / Dividends / Schedule D line 12 inputs by character; Form 3520 prepared outside the e-file",
            "F": "T. Nguyen 09/14/2026 / R. Patel"},
           {"A": "Default method / Form 4970 interest charge - NOT applicable", "B": "Actual-method statement received; trust's UNI at "
            "12/31/2024 = $0 -> no accumulation distribution, no section 668 interest charge.", "C": "Same FNTBS", "D": 0,
            "E": "None (no Form 3520 / Miscellaneous Taxes override)", "F": "T. Nguyen 09/14/2026 / R. Patel"}],
}

CHECKS = {
    "'20. Insolvency (Form 982)'!F11": 48000,
    "'20. Insolvency (Form 982)'!G11": 38000,
    "'10. Capital Loss Carryover'!D16": 0,
    "'10. Capital Loss Carryover'!D17": 67000,
    "'18. NUA & IRD Deduction'!E11": 60000,
}
