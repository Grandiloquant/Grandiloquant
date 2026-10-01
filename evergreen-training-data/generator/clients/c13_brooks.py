"""EVG1013 - Nathan Brooks (Single, Illinois - Chicago). Startup employee: NSO same-day sale (1099-B basis = strike only),
ISO exercise-and-hold (AMT / Form 6251, Form 8801 credit carryforward), LATE 83(b) election on founder restricted stock
(Form 15620 mailed day 37 -> invalid), HSA excess contribution withdrawn before the extended due date. Extended return."""
from common import ClientBuild, gotcha, fmt
from docs import statement, scanned_pages, write_text, write_csv, info_form
import forms as F
from tax2025 import Return1040, r, AMT_EXEMPT, AMT_28_BREAK

C = ClientBuild("EVG1013", "Brooks", "Nathan Brooks")
ADDR = ("2250 W Belden Ave Apt 3R", "Chicago, IL 60647")
T = {"name": "Nathan J. Brooks", "ssn": "XXX-XX-6618", "dob": "1995-07-22"}
REC = [T["name"], *ADDR, f"TIN: {T['ssn']}"]

# ------------------------------------------------------------------ PERM
C.write_profile(f"""
# EVG1013 - Brooks, Nathan  (PERM)

*Synthetic client - Project Evergreen training data.*

| Item | Detail |
|---|---|
| Client ID | EVG1013 |
| Taxpayer | Nathan J. Brooks, DOB 07/22/1995, SSN XXX-XX-6618, Senior Robotics Software Engineer |
| Employer | Parallax Robotics, Inc. (Chicago; IPO on Nasdaq 05/2025, ticker "PLXR" - synthetic). Equity: ISOs + NSOs under 2020 Stock Plan, administered on E*TRADE (Morgan Stanley at Work) |
| Side venture | Co-founder / CTO of Loomwork AI, Inc. (Delaware C corp formed 10/2025; no payroll in 2025) |
| Address | {ADDR[0]}, {ADDR[1]} - Illinois resident all years. **Chicago has no city income tax.** |
| Filing status | Single, no dependents |
| Contact | Email nathan.brooks@example.com, (312) 555-0187; eSign OK; prefers email |
| Engagement | Client since 2022 (2021 return self-prepared). Equity-comp tier (quote $1,850 + $250 per additional equity event). |
| Health coverage | Parallax HDHP, **self-only**, all of 2025; HSA at Fidelity |
| Payment info | Refunds by direct deposit - Chase checking ****7730 (voided check on file) |
| Standing instructions | Always review Form 3921/3922 and E*TRADE supplements; client tends to over-contribute to HSA |
""")
F.prior_year_summary(C.perm_file("2024_Form_1040_Return_Summary.pdf", "Prior-year return summary"), "Nathan Brooks",
    "EVG1013", "Single", [
        ["1a", "W-2 wages (Parallax Robotics, Inc.)", 139880],
        ["2b", "Taxable interest - Wealthfront Cash", 1106],
        ["11", "AGI", 140986], ["12", "Standard deduction", 14600], ["15", "Taxable income", 126386],
        ["16", "Tax", 23526], ["17", "AMT (Form 6251)", 0], ["24", "Total tax", 23526],
        ["25a", "Federal withholding", 24410], ["35a", "Refund", 884],
        ["IL-1040", "IL base income 140,986; exemption 2,775; IL tax 6,842; refund 311", 6842]],
    carryovers=[["Minimum tax credit (Form 8801)", 0], ["Capital loss carryover", 0]],
    notes="PY WP: ISOs vesting (10,000-share grant 2021 at $1.50). Discussed AMT impact of any exercise-and-hold before "
          "year end; client said he would call us before exercising (he did not). HSA self-only; 2024 contributions within limit.")

# ------------------------------------------------------------------ PBC documents
EMP = {"name": "Parallax Robotics, Inc.", "addr1": "1045 W Fulton Market Ste 400", "addr2": "Chicago, IL 60607", "ein": "00-8814402"}
EE = {"name": T["name"], "addr1": ADDR[0], "addr2": ADDR[1], "ssn": T["ssn"]}
SALARY, NSO_INC, K401, HSA_PAYROLL, HSA_ER = 158000.00, 22000.00, 12000.00, 3300.00, 1000.00
box1 = SALARY + NSO_INC - K401 - HSA_PAYROLL
box3 = min(SALARY + NSO_INC - HSA_PAYROLL, 176100.00)
box5 = SALARY + NSO_INC - HSA_PAYROLL
w2b = {"1": box1, "2": 27600.00, "3": box3, "4": round(box3 * .062, 2), "5": box5, "6": round(box5 * .0145, 2),
       "12": [("D", K401), ("W", HSA_PAYROLL + HSA_ER), ("V", NSO_INC), ("DD", 7812.00)], "13": ["Retirement plan: X"],
       "control": "PLX-00417",
       "state": [{"state": "IL", "id": "0088-1440", "wages": box1, "tax": 8150.00}]}

F.organizer(C.pbc_file("01_2025_Organizer_Brooks.pdf", "Client organizer", "2026-03-02"), "Nathan Brooks", "EVG1013",
    general=[("Did your marital status change during 2025?", "No", ""),
             ("Did you exercise, vest or sell any employer stock / options / RSUs?", "Yes",
              "Exercised ISOs in Feb (held), exercised+sold NSOs in Sept. Also got founder shares in my startup."),
             ("Did you receive any Form 3921 / 3922?", "Yes", "3921 attached"),
             ("Did you file a Section 83(b) election in 2025?", "Yes", "Mailed it in December - copy attached"),
             ("Did you have an HSA?", "Yes", "Fidelity - payroll + I added $1,000 in April"),
             ("Did you receive, sell, exchange digital assets?", "No", ""),
             ("Did you make estimated tax payments?", "No", ""),
             ("Do you want to extend?", "Yes", "waiting on Loomwork paperwork")],
    dependents=[],
    income_rows=[["Wages", "Parallax Robotics, Inc.", 139880, "see W-2"],
                 ["Interest", "Wealthfront Cash Account", 1106, "~1,300"],
                 ["Brokerage (1099-B)", "E*TRADE from Morgan Stanley", 0, "NSO sale - see 1099"],
                 ["Other income", "Loomwork AI founder stock", "", "8,000?? (83b)"]],
    deductions_rows=[["HSA contributions", "payroll + direct", 3850, "5,300"],
                     ["Charitable", "", 0, ""]],
    signature_date="02/27/2026")

F.w2(C.pbc_file("02_W-2_Parallax_Robotics.pdf", "Form W-2", "2026-03-02"), EMP, EE, w2b)
info_form(C.pbc_file("03_Form_3921_Parallax_ISO_exercise.pdf", "Form 3921", "2026-03-02"), "3921",
          "Exercise of an Incentive Stock Option Under Section 422(b)",
          payer=["TRANSFEROR'S name, street address, city, state, ZIP", EMP["name"], EMP["addr1"], EMP["addr2"], f"TIN: {EMP['ein']}"],
          recipient=["EMPLOYEE'S name, street address, city, state, ZIP", *REC],
          boxes=[("1", "Date option granted", "03/15/2021"), ("2", "Date option exercised", "02/14/2025"),
                 ("3", "Exercise price paid per share", 1.50), ("4", "Fair market value per share on exercise date", 14.00),
                 ("5", "No. of shares transferred", "4,000"), ("6", "If other than transferor, name/address of corp. whose stock transferred", "")],
          omb="OMB No. 1545-2129", account_no="Grant ISO-2021-0117",
          notes=["FMV per share on exercise date per Board-approved 409A valuation dated 01/31/2025 (pre-IPO).",
                 "Shares held in E*TRADE stock plan account - no shares sold in 2025."])

# E*TRADE 1099-B (consolidated) - basis = exercise price only
NSO_SH, NSO_STRIKE, NSO_FMV = 2000, 2.00, 13.00
commission = 24.95
proceeds = NSO_SH * NSO_FMV - commission
rep_basis = NSO_SH * NSO_STRIKE
statement(C.pbc_file("04_ETRADE_2025_Consolidated_1099.pdf", "Consolidated Form 1099 (broker)", "2026-03-02"),
    "E*TRADE from Morgan Stanley - 2025 Consolidated Form 1099 (Stock Plan Account ****4471)", [
        {"heading": "Summary", "table": [["Form", "Item", "Amount"],
                                         ["1099-DIV", "Total ordinary dividends", 0.00],
                                         ["1099-INT", "Interest income", 0.00],
                                         ["1099-B", "Total proceeds (short-term, covered - Box A)", proceeds],
                                         ["1099-B", "Total cost basis reported to IRS", rep_basis],
                                         ["1099-B", "Wash sale loss disallowed", 0.00]]},
        {"heading": "Form 1099-B - Short-term transactions for covered tax lots (Box 12: basis reported to the IRS) - Form 8949 Box A",
         "table": [["1a Description", "1b Acquired", "1c Sold", "1d Proceeds", "1e Cost basis", "1f/1g", "Gain/(loss)"],
                   ["PARALLAX ROBOTICS INC (PLXR) 2,000 sh - NSO exercise, same-day sale", "09/18/2025", "09/18/2025",
                    proceeds, rep_basis, "", proceeds - rep_basis]],
         "note": "Box 2: Short-term. Box 5: noncovered - not checked. Box 12: basis reported to IRS - checked. Box 4: federal withholding 0.00. "
                 "Proceeds are net of commissions and fees of $24.95."},
        {"heading": "Important information about cost basis for compensatory options",
         "para": "Beginning with securities acquired in 2014, brokers are required to report the cost basis of shares acquired "
                 "through a compensatory stock option as the amount paid for the shares (the exercise price) only. Cost basis "
                 "reported on this Form 1099-B does not include compensation income that may have been reported on your Form W-2. "
                 "See your Stock Plan Transactions Supplement for adjusted cost basis information. You may need to adjust "
                 "basis on Form 8949 (code B)."}])
statement(C.pbc_file("05_ETRADE_Stock_Plan_Transactions_Supplement_2025.pdf", "Broker supplemental statement", "2026-03-02"),
    "E*TRADE from Morgan Stanley - 2025 Stock Plan Transactions Supplement (not a tax form)", [
        {"para": "This supplement is provided for informational purposes to help you reconcile your Form 1099-B. It is not filed "
                 "with the IRS. Transactions shown here are the SAME transactions reported on your 2025 Form 1099-B."},
        {"heading": "Nonqualified Stock Option (NSO) - Exercise and Same-Day Sale",
         "table": [["Grant", "Exercise / sale date", "Shares", "Exercise price", "FMV at exercise", "Ordinary income (on W-2)",
                    "Proceeds (net)", "Adjusted cost basis", "Adjusted gain/(loss)"],
                   ["NSO-2022-0288", "09/18/2025", NSO_SH, NSO_STRIKE, NSO_FMV, NSO_SH * (NSO_FMV - NSO_STRIKE), proceeds,
                    NSO_SH * NSO_FMV, proceeds - NSO_SH * NSO_FMV]]},
        {"heading": "Incentive Stock Option (ISO) - Exercise and Hold (no sale)",
         "table": [["Grant", "Exercise date", "Shares", "Exercise price", "FMV at exercise", "Bargain element (AMT)", "Shares held 12/31/2025"],
                   ["ISO-2021-0117", "02/14/2025", 4000, 1.50, 14.00, 50000.00, 4000]],
         "note": "ISO exercise is not reported on Form W-2 or Form 1099-B. See Form 3921 issued by your employer."},
        {"heading": "Holdings at 12/31/2025", "table": [["Security", "Shares", "Price 12/31/2025", "Market value"],
                                                        ["PLXR (ISO lot 02/14/2025)", 4000, 11.35, 45400.00]]}])
F.f1099_int(C.pbc_file("06_1099-INT_Wealthfront.pdf", "Form 1099-INT", "2026-03-02"),
            ["Wealthfront Brokerage LLC (Cash Account program banks)", "261 Hamilton Ave", "Palo Alto, CA 94301", "TIN: 00-3350097"],
            REC, {"1": 1284.37}, account="WF-****2091")
F.f5498_sa(C.pbc_file("07_5498-SA_Fidelity_HSA.pdf", "Form 5498-SA", "2026-05-28", "Client email attachment", "arrived after main batch"),
           ["Fidelity Management Trust Co.", "PO Box 770001", "Cincinnati, OH 45277", "TIN: 00-2297021"], REC,
           {"2": 5300.00, "5": 14870.12})
statement(C.pbc_file("08_Fidelity_HSA_Contribution_History_2025.pdf", "HSA contribution history", "2026-03-02"),
    "Fidelity HSA - Contribution History - Account ****5512 - Calendar Year 2025", [
        {"table": [["Date", "Source", "Tax year", "Amount"],
                   ["Jan-Dec (26 pay periods)", "Payroll - employee pre-tax (Parallax cafeteria plan)", "2025", 3300.00],
                   ["01/10/2025", "Employer seed contribution (Parallax)", "2025", 1000.00],
                   ["04/11/2025", "Participant - online transfer from Chase ****7730 (after-tax)", "2025", 1000.00],
                   ["Total", "", "", 5300.00]], "total_row": True, "left_align_cols": [0, 1]},
        {"para": "Coverage type on file: SELF-ONLY HDHP. 2025 IRS contribution limit for self-only coverage: $4,300 "
                 "(age 55+ catch-up: not applicable)."}])
# Loomwork founder stock - legal agreement + late 83(b)
statement(C.pbc_file("09_Loomwork_AI_Restricted_Stock_Agreement.pdf", "Legal agreement (restricted stock)", "2026-03-02"),
    "Loomwork AI, Inc. - Founder Restricted Stock Agreement (excerpt)", [
        {"para": ["This Restricted Stock Agreement is entered into as of <b>November 3, 2025</b> (the \"Grant Date\") between "
                  "Loomwork AI, Inc., a Delaware corporation (the \"Company\"), and Nathan J. Brooks (the \"Founder\").",
                  "<b>1. Issuance.</b> In consideration of services rendered and to be rendered, the Company issues to Founder "
                  "20,000 shares of Common Stock (the \"Shares\"). No cash purchase price is payable. The Board has determined the fair "
                  "market value of the Common Stock on the Grant Date to be $0.40 per share (aggregate $8,000).",
                  "<b>2. Vesting.</b> 25% of the Shares vest on the first anniversary of the Grant Date (11/03/2026); the balance vests in "
                  "36 equal monthly installments thereafter, subject to Founder's continuous service. Unvested Shares are subject to "
                  "forfeiture on termination of service.",
                  "<b>3. Section 83(b) Election.</b> Founder understands that he may elect under Section 83(b) of the Internal Revenue Code "
                  "to be taxed currently on the fair market value of the Shares. <b>Such election must be filed with the IRS within "
                  "thirty (30) days after the Grant Date.</b> Founder acknowledges that it is Founder's sole responsibility, and not the "
                  "Company's, to timely file the election.",
                  "Signed: Priya Ramaswamy, CEO, Loomwork AI, Inc. / Nathan J. Brooks, Founder - 11/03/2025"]}])
scanned_pages(C.pbc_file("10_Form_15620_83b_election_and_USPS_receipt.pdf", "Scanned form + mailing receipt", "2026-03-02"),
    [["Form 15620 (Rev. 12-2024)   Section 83(b) Election          OMB 1545-xxxx",
      "Part I  Taxpayer: Nathan J. Brooks   SSN XXX-XX-6618",
      "        2250 W Belden Ave Apt 3R, Chicago IL 60647",
      "Part II Service recipient: Loomwork AI, Inc.  EIN 00-5520871",
      "Part III Property: 20,000 sh Common Stock, Loomwork AI, Inc.",
      "  Line 7  Date property transferred:      11/03/2025",
      "  Line 8  Tax year for which election made: 2025",
      "  Line 9  Restrictions: forfeiture on termination; 4-yr vesting",
      "  Line 10 FMV at transfer ........................  $8,000.00",
      "  Line 11 Amount paid ...........................       $0.00",
      "  Line 12 Amount includible in income .............  $8,000.00",
      "Signature: /s/ Nathan J. Brooks      Date: 12/08/2025",
      "",
      "Copy furnished to service recipient: yes (emailed P. Ramaswamy 12/08)"],
     ["USPS Certified Mail Receipt  PS Form 3800",
      "Article no. 9589 0710 5270 0XXX XXXX 17",
      "Postage $0.73  Certified fee $4.85  Return receipt $4.10",
      "Sent to: Department of the Treasury, IRS",
      "         Ogden, UT 84201-0002 (per Form 15620 instr.)",
      "",
      "Postmark:  CHICAGO IL 60647   DEC 10 2025",
      "",
      "(handwritten on receipt:) 83b - Loomwork - mailed!"]], handwritten=False, skew=-1.4, seed=1313)
write_text(C.pbc_file("11_Email_Nathan_2026-03-02.txt", "Client correspondence", "2026-03-02", "Email"),
"""From: Nathan Brooks <nathan.brooks@example.com>
To: preparer@evergreentax.example
Date: Mon, 2 Mar 2026 21:14:05 -0600
Subject: 2025 docs + a few questions

Hi - everything is uploaded to Sharefile. A few things:

1. I exercised 4,000 ISOs in February (before the IPO) and still hold them. I know you warned me about AMT... sorry.
2. In September I exercised and immediately sold 2,000 NSOs. E*TRADE shows a gain of like $22k on the 1099-B but
   that was already on my W-2?? Please don't make me pay tax twice on it.
3. I co-founded a startup (Loomwork) in November and got 20,000 founder shares. A friend told me to do an 83(b)
   so I mailed it in December. Do I report $8,000 of income for 2025? The form says "amount includible in income 8,000".
4. I put an extra $1,000 into my HSA in April because I thought the limit was higher. Is that ok?

Go ahead and extend - Loomwork's lawyer is still sending me paperwork.
Thanks, Nathan
""")
statement(C.pbc_file("12_Chicago_Public_Library_Foundation_receipt.pdf", "Donation receipt", "2026-03-02", note="client included"),
    "Chicago Public Library Foundation - Thank you!", [
        {"para": ["Dear Nathan, thank you for your gift of $250.00 received 11/28/2025 (Giving Tuesday). No goods or services were "
                  "provided in exchange for your contribution. EIN 00-3611982."]}])
write_text(C.pbc_file("13_Email_thread_HSA_excess_2026-09-16.txt", "Client correspondence + doc", "2026-09-16", "Email",
                      "requested by preparer 08/27"),
"""From: preparer@evergreentax.example
To: Nathan Brooks
Date: Thu, 27 Aug 2026 09:40:00 -0500
Subject: Brooks 2025 - HSA excess contribution (action needed before 10/15)

Hi Nathan - your 2025 HSA contributions were $5,300 ($4,300 through Parallax payroll/employer, which already equals the
2025 self-only limit, plus your $1,000 transfer in April). The $1,000 is an excess contribution. If you withdraw the
$1,000 plus the earnings on it before 10/15/2026 (the extended due date of your return), there is no 6% excise tax.
Please ask Fidelity for a "return of excess contribution" for tax year 2025 and send us the confirmation.

-----
From: Nathan Brooks
Date: Wed, 16 Sep 2026 07:58:31 -0500
Subject: RE: Brooks 2025 - HSA excess contribution (action needed before 10/15)

Done - Fidelity processed it yesterday. Confirmation attached. They said I'll get a 1099-SA for 2026.

  Fidelity HSA - Return of Excess Contribution - Confirmation
  Request date 09/14/2026   Processed 09/15/2026
  Tax year of contribution: 2025
  Excess contribution returned:   $1,000.00
  Net income attributable (NIA):     $38.00
  Total distributed to Chase ****7730: $1,038.00
  (Will be reported on 2026 Form 1099-SA, distribution code 2)
""")
write_csv(C.pbc_file("14_Loomwork_cap_table_export.csv", "Spreadsheet (CSV)", "2026-09-10", "Client email attachment",
                     "from Loomwork counsel"),
          ["Holder", "Security", "Shares", "Issue date", "Price paid", "Vesting start", "83(b) received by company"],
          [["Priya Ramaswamy", "Common (founder RSA)", 40000, "2025-11-03", 0, "2025-11-03", "Yes - 11/21/2025"],
           ["Nathan J. Brooks", "Common (founder RSA)", 20000, "2025-11-03", 0, "2025-11-03", "Copy received 12/08/2025"],
           ["Marco Feliz", "Common (founder RSA)", 20000, "2025-11-03", 0, "2025-11-03", "Yes - 11/26/2025"],
           ["2025 Equity Incentive Plan pool", "Reserved", 20000, "2025-11-03", "", "", ""]])

# ------------------------------------------------------------------ RETURN
ISO_SH, ISO_STRIKE, ISO_FMV = 4000, 1.50, 14.00
iso_adj = ISO_SH * (ISO_FMV - ISO_STRIKE)
facts = {
    "status": "S",
    "taxpayer": {"age65": False},
    "w2": [{"who": "T", "box1": w2b["1"], "box2": w2b["2"], "box3": w2b["3"], "box4": w2b["4"], "box5": w2b["5"], "box6": w2b["6"]}],
    "interest": [{"payer": "Wealthfront Brokerage LLC", "amount": 1284.37}],
    "trades": [{"box": "A", "id": "1", "desc": "2,000 sh Parallax Robotics (PLXR) - NSO same-day sale", "acq": "09/18/2025",
                "sold": "09/18/2025", "proceeds": proceeds, "basis": rep_basis, "adj": -NSO_INC, "code": "B"}],
    "amt": {"iso": iso_adj},
    "extension_payment": 6000,
}
R = Return1040(facts).compute()
v = R.values

# Form 8801 carryforward: AMT attributable to deferral items (ISO) is creditable in later years.
amti_excl = v["15"] + v["12e"]          # exclusion items only (standard deduction add-back)
tmt_excl = r(max(0, amti_excl - AMT_EXEMPT["S"]) * .26)
min_tax_excl = max(0, tmt_excl - v["16"])
mtc_cf = v["17"] - min_tax_excl
v["minimum_tax_credit_carryforward"] = mtc_cf
ra_tax = v["16"]
amt_amt = v["17"]

# Illinois
IL_EXEMPT = 2850
il_base = v["11"]
il_net = il_base - IL_EXEMPT
il_tax = r(il_net * .0495)
il_wh = 8150
il_refund = il_wh - il_tax

hsa_8889 = [["Form 8889 - Nathan (self-only HDHP all 12 months)", "Amount"],
            ["Line 2 HSA contributions you made for 2025 (not through employer) - per 5498-SA less code W", 1000],
            ["Line 3 Limitation - self-only", 4300],
            ["Line 6 Limitation after Archer MSA", 4300],
            ["Line 9 Employer contributions (W-2 box 12 code W: $3,300 cafeteria-plan + $1,000 employer seed)", 4300],
            ["Line 10 Qualified HSA funding distributions", 0],
            ["Line 12 Line 8 less lines 9-11", 0],
            ["Line 13 HSA deduction (smaller of line 2 or line 12)", 0],
            ["Excess contribution $1,000 + earnings $38 withdrawn 09/15/2026 (before 10/15/2026 extended due date) - "
             "not an excess contribution for Form 5329; $38 earnings taxable in 2026 (year received, 1099-SA code 2)", 0],
            ["Line 14a Distributions in 2025", 0]]
f8949_detail = [["Form 8949 Box A", "Proceeds (d)", "Cost basis per 1099-B (e)", "Code (f)", "Adjustment (g)", "Gain/(loss) (h)"],
                ["2,000 sh PLXR - acquired 09/18/2025 (NSO exercise) / sold 09/18/2025", r(proceeds), r(rep_basis), "B", -r(NSO_INC),
                 r(proceeds - rep_basis - NSO_INC)],
                ["Adjusted basis = exercise price $4,000 + compensation in W-2 box 1 (box 12 code V) $22,000 = $26,000", "", "", "", "", ""]]
amt_detail = [["Form 6251 support / Form 8801 carryforward", "Amount"],
              ["ISO exercise 02/14/2025: 4,000 sh x (FMV $14.00 - strike $1.50) (Form 3921) - line 2i", r(iso_adj)],
              ["AMT basis of ISO shares carried forward (4,000 x $14.00) vs regular basis ($6,000)", 56000],
              ["Tentative minimum tax (AMTI less $88,100 exemption x 26%)", v["amt_tmt"]],
              ["Regular tax (line 16)", ra_tax],
              ["AMT (Schedule 2 line 1)", amt_amt],
              [f"TMT on exclusion items only (AMTI {r(amti_excl):,} - exemption) x 26% = {tmt_excl:,} < regular tax -> "
               "minimum tax on exclusion items", min_tax_excl],
              ["Minimum tax credit carryforward to 2026 (Form 8801) - all attributable to the ISO deferral item", mtc_cf]]
rs_memo = ("Loomwork AI, Inc. founder restricted stock (20,000 sh, granted 11/03/2025, FMV $0.40, $0 paid). Form 15620 was signed "
           "12/08/2025 and postmarked 12/10/2025 - 37 days after transfer. Section 83(b)(2) requires filing within 30 days "
           "(deadline 12/03/2025); no extension/9100 relief is available. The election is invalid: NO income is reported for 2025, "
           "and the stock is not 'transferred' for tax purposes until it vests. Compensation income will be recognized at each "
           "vesting date equal to FMV at vesting (first 5,000 sh on 11/03/2026). Election copy NOT attached to this return.")
C.write_return(R, [
    ("Taxpayer", "Nathan J. Brooks (XXX-XX-6618)"),
    ("Address", ", ".join(ADDR)),
    ("Filing status", "Single"),
    ("Dependents", "None"),
    ("Digital assets question", "No"),
    ("Forms included", "1040, Schedule 2, Schedule 3, Schedule B, Schedule D, Form 8949, Form 6251, Form 8889; IL-1040"),
    ("Extension", "Form 4868 filed 04/13/2026 with $6,000 payment; IL automatic extension (no IL balance due)"),
    ("State / local", "Illinois IL-1040 (resident). Chicago - no city income tax."),
    ("Filing method", "E-file (Form 8879 signed 09/24/2026); direct deposit to Chase ****7730"),
], state_summary=[{"title": "Illinois Form IL-1040 (resident) - summary", "lines": [
        ("1", "Federal adjusted gross income", il_base),
        ("2-4", "Additions (none) / federally tax-exempt interest (none)", 0),
        ("9", "Base income", il_base),
        ("10", "Exemption allowance (1 x $2,850; federal AGI under $250,000)", IL_EXEMPT),
        ("11", "Net income", il_net),
        ("12", "Income tax (4.95%)", il_tax),
        ("14-16", "Credits (none) / Illinois has no AMT or ISO adjustment", 0),
        ("25", "Illinois income tax withheld (W-2 box 17)", il_wh),
        ("36", "Overpayment - refund", il_refund)],
        "note": "NSO compensation ($22,000) is in IL wages (box 16). ISO spread is not IL income (IL starts from federal AGI; no "
                "IL minimum tax). Chicago/Cook County impose no individual income tax."}],
    attachments=[("Form 8949 detail - NSO basis adjustment (code B)", f8949_detail),
                 ("Form 6251 / Form 8801 support - ISO exercise", amt_detail),
                 ("Form 8889 - Health Savings Accounts", hsa_8889),
                 ("Statement - restricted stock / Section 83(b) (not filed; preparer memo for the file)", rs_memo)])

gotchas = [
    gotcha("EVG1013-G1", "Restricted Stock (Section 83(b) / Form 15620 within 30 days)", "83(b) election mailed 37 days after grant",
           "Accept the client's Form 15620 at face value: report $8,000 of compensation income for 2025 (Sch 1 / line 1h) and "
           "attach the election copy.",
           "Grant 11/03/2025 -> 30-day deadline 12/03/2025; USPS postmark 12/10/2025. Election is invalid (no relief under "
           "Reg. 1.83-2 / no 9100 relief). No 2025 income; income is recognized at each vesting at FMV then. Advise client in "
           "writing (and Loomwork counsel re: possible cancel-and-regrant with a new timely election).",
           "Income overstated $8,000 (tax ~$1,920) if reported; future vesting income ignored", ["1h", "8"], "hard"),
    gotcha("EVG1013-G2", "Schedule D (missing / incorrect cost basis on consolidated 1099)",
           "NSO same-day sale: 1099-B basis = exercise price only",
           "Autoflow the 1099-B as reported: $4,000 basis -> $21,975 short-term gain on top of the $22,000 already in W-2 box 1.",
           "Form 8949 box A, report 1099-B basis $4,000 in col (e), code B, adjustment ($22,000) -> loss ($25) (commission).",
           "Taxable income overstated $22,000 (~$5,280 tax)", ["7", "Form 8949"], "medium"),
    gotcha("EVG1013-G3", "Scan - duplicate documents", "E*TRADE Stock Plan Transactions Supplement repeats the 1099-B sale",
           "Enter both the 1099-B and the supplement's 'adjusted gain' line as separate sales (double-counting proceeds).",
           "The supplement is informational (same transaction). Use it only to support the code B basis adjustment.",
           "Proceeds double-counted $25,975", ["7"], "easy"),
    gotcha("EVG1013-G4", "Form 6251 (AMT) - ISO exercise and hold", "ISO spread is an AMT adjustment, not regular income",
           "Either (a) ignore Form 3921 (no W-2/1099 income -> no AMT), or (b) add the $50,000 spread to wages.",
           f"Regular tax: nothing. Form 6251 line 2i $50,000 -> AMT {fmt(amt_amt)}. Track AMT basis $56,000 vs regular $6,000; "
           f"Form 8801 minimum tax credit carryforward {fmt(mtc_cf)} to 2026 (deferral item).",
           f"Tax understated {fmt(amt_amt)} (a) or overstated ~$12,000 (b)", ["17", "Form 6251"], "hard"),
    gotcha("EVG1013-G5", "W-2 box 12 codes / Form 8889", "HSA code W already equals the self-only limit; extra $1,000 is excess",
           "Deduct the $1,000 direct contribution on Schedule 1 line 13 (or deduct $5,300 per 5498-SA).",
           "Limit $4,300 - code W $4,300 = $0 deduction. Excess $1,000 + $38 earnings withdrawn 09/15/2026, before the 10/15/2026 "
           "extended due date -> no 6% excise (no Form 5329); $38 earnings taxable in 2026, not 2025. File 8889.",
           "Adjustments overstated $1,000; or $60 excise wrongly assessed", ["10", "Form 8889"], "medium"),
    gotcha("EVG1013-G6", "General Return Prep Notes / estimated tax (Form 2210)", "AMT creates a balance due - is there a penalty?",
           "Compute a Form 2210 penalty because withholding < 90% of 2025 tax.",
           "Withholding $27,600 >= 100% of 2024 tax $23,526 (2024 AGI under $150,000) -> safe harbor met, no penalty. Extension "
           "payment $6,000 (Sch 3 line 10) avoids late-payment interest.", "Line 38 should be $0", ["38", "31"], "medium"),
    gotcha("EVG1013-G7", "SALT Implications (state conformity)", "Illinois has no AMT and taxes the NSO income as wages",
           "Add an IL adjustment for the ISO spread or subtract the NSO income as 'already taxed on 1099-B'.",
           f"IL base income = federal AGI {fmt(il_base)}; exemption $2,850; tax 4.95% = {fmt(il_tax)}; refund {fmt(il_refund)}. "
           "Chicago has no city income tax.", "IL-1040 lines 1-12", ["IL-1040"], "easy"),
]
C.write_answer_key(R, {"residence": "IL - Chicago (IL-1040; no city income tax)", "complexity": "Equity-compensation tier; AMT"},
                   gotchas,
                   state=[{"jurisdiction": "Illinois", "form": "IL-1040", "base_income": il_base, "exemption": IL_EXEMPT,
                           "net_income": il_net, "tax": il_tax, "withholding": il_wh, "refund": il_refund}],
                   filings=[{"form": "Form 4868 (extension)", "filed": "2026-04-13", "payment": 6000},
                            {"form": "Form 1040 (federal)", "method": "e-file", "due": "2026-10-15", "filed": "2026-09-25"},
                            {"form": "IL-1040", "method": "e-file", "due": "2026-10-15", "filed": "2026-09-25"}],
                   extra={"minimum_tax_credit_carryforward_2026": mtc_cf, "iso_amt_basis_carryforward": 56000,
                          "restricted_stock_83b": "invalid (late) - no 2025 income",
                          "hsa_excess_2025": {"excess": 1000, "withdrawn": "2026-09-15", "earnings_taxable_2026": 38}})

C.write_receipt_log("EVG1013-1040-2025", "P. Nwosu (staff)", "L. Chen (senior)", "S. Kennedy, CPA", "2026-03-02",
                    extension="Filed 04/13/2026 (client requested; Loomwork documents outstanding) - $6,000 paid via EFTPS/Direct Pay")
C.write_notes(f"""
# EVG1013 - Brooks, Nathan - 2025 Form 1040 - Preparer Notes

*Synthetic client - Project Evergreen. Return status: **signed off, extended return e-filed 09/25/2026 (federal + IL).***

## Return summary
| | |
|---|---|
| Filing status | Single |
| AGI (line 11) | {fmt(v['11'])} |
| Deduction | Standard {fmt(v['12e'])} (no itemizing - $250 charity only) |
| Taxable income | {fmt(v['15'])} |
| Regular tax (line 16) | {fmt(v['16'])} |
| AMT (Schedule 2 line 1 / Form 6251) | {fmt(v['17'])} |
| Total tax | {fmt(v['24'])} |
| Withholding / extension payment | {fmt(v['25d'])} / {fmt(v['31'])} |
| **Refund** | **{fmt(v['refund'])}** (direct deposit) |
| Illinois | tax {fmt(il_tax)}, withheld {fmt(il_wh)}, refund {fmt(il_refund)} |
| Carryforward | Minimum tax credit (Form 8801) {fmt(mtc_cf)}; ISO AMT basis $56,000 (regular basis $6,000) |

## What I did and why (plain English)
1. **W-2.** Box 1 {fmt(w2b['1'])} already includes the $22,000 NSO spread (box 12 code V). Box 12 D (401k) and W (HSA) are
   pre-tax. Medicare wages are under $200,000, so no Additional Medicare Tax.
2. **NSO same-day sale (Form 8949 box A, code B).** E*TRADE reported cost basis of $4,000 (exercise price only - required
   broker reporting for compensatory options). The $22,000 spread was taxed on the W-2, so real basis is $26,000. I kept the
   1099-B basis in column (e) and entered a ($22,000) code B adjustment -> a ($25) loss (the commission). Without this, the
   same $22,000 would have been taxed twice. The Stock Plan Transactions Supplement is the same sale (informational only) -
   bookmarked DUP/support, not entered.
3. **ISO exercise-and-hold (Form 6251).** Form 3921: 4,000 shares, strike $1.50, FMV $14.00 on 02/14/2025 -> $50,000
   bargain element. Not regular income (no sale; ISO rules), but it is an AMT adjustment (line 2i). AMTI {fmt(v['15'] + v['12e'] + iso_adj)}
   less the $88,100 exemption x 26% = tentative minimum tax {fmt(v['amt_tmt'])} vs regular tax {fmt(v['16'])} ->
   **AMT {fmt(v['17'])}**. Because the ISO is a *deferral* item, the whole AMT becomes a **minimum tax credit carryforward
   ({fmt(mtc_cf)}, Form 8801)** usable in future years when regular tax exceeds TMT (e.g. the year he sells the shares).
   AMT basis in the shares is $56,000 vs regular basis $6,000 - recorded in PERM for the eventual sale (a sale after
   02/14/2026 is a qualifying disposition: more than 1 year after exercise and more than 2 years after the 03/15/2021 grant).
4. **Loomwork founder shares - late 83(b).** Grant date 11/03/2025; Form 15620 signed 12/08 and USPS postmark 12/10/2025 =
   37 days. Section 83(b) requires filing within 30 days of transfer (by 12/03/2025) and the IRS cannot extend it. The
   election is **invalid**, so nothing is reported for 2025 (the $8,000 "amount includible" on his form is not income) and
   the copy is not attached. Consequence: ordinary compensation income at each vesting date equal to FMV then (first
   5,000 shares on 11/03/2026), and capital-gain holding period starts at vesting. Client emailed with this explanation;
   suggested he ask Loomwork's counsel about cancelling and re-granting the shares with a new, timely 83(b).
5. **HSA (Form 8889).** Self-only HDHP all year; limit $4,300. Code W $4,300 ($3,300 his pre-tax payroll + $1,000
   employer seed) already uses the full limit, so his $1,000 April transfer is an excess contribution and deduction is $0.
   He withdrew $1,000 + $38 earnings on 09/15/2026, before the 10/15/2026 extended due date -> **no 6% excise / no Form 5329**.
   The $38 is taxable in **2026** (1099-SA code 2 next year) - noted in PERM for the 2026 return.
6. **Interest.** Wealthfront $1,284 (under $1,500, so Schedule B is not required; it prints for reference only).
7. **Estimated tax penalty.** Balance before extension payment was ~{fmt(v['24'] - v['25d'])} because of AMT. Withholding
   $27,600 exceeds 100% of 2024 tax ($23,526; 2024 AGI under $150,000), so the prior-year safe harbor is met - no Form 2210.
   The $6,000 extension payment made 04/13/2026 covers the balance, so there is no late-payment penalty or interest.
8. **Illinois.** IL-1040 starts from federal AGI (NSO income in IL wages; IL has no AMT, so no ISO adjustment). Exemption
   $2,850 (AGI under $250,000). Tax {fmt(il_tax)} vs withholding {fmt(il_wh)} -> refund {fmt(il_refund)}. IL gives an automatic
   6-month extension; nothing was owed so no IL-505-I payment. **Chicago has no city income tax.**
9. **Charity.** $250 Chicago Public Library Foundation - no benefit (standard deduction; the non-itemizer charitable deduction
   starts in 2026, so it will matter next year).

## Open items / client communication
- None open. HSA excess corrected 09/15/2026 (confirmation in PBC #13).
- Advised (email 09/18): (a) AMT credit carryforward {fmt(mtc_cf)} will be recovered in later years - keep records;
  (b) any 2026 sale of the ISO shares is a qualifying disposition (after 02/14/2026); the AMT/regular basis difference
  reverses on Form 6251 in the sale year and frees up the credit - projection offered (PROJ project); (c) Loomwork vesting income starts 11/2026 -
  plan withholding/estimates; (d) cap HSA at payroll only for 2026 (limit $4,400 self-only).

## Hand-off to signer / routing
- [x] Return locked; Accountant's copy saved as *reviewed*
- [x] Federal 1040 - e-file; due 10/15/2026 (extended; 4868 filed 04/13/2026 with $6,000)
- [x] IL-1040 - e-file; due 10/15/2026 (automatic extension)
- [x] No FBAR / no foreign filings
- [x] eSign (8879 + IL-8453 equivalent) - email preferred, nathan.brooks@example.com
- [x] Special instructions: do NOT attach Form 15620 copy; PERM updated with ISO AMT basis, MTC carryforward, 2026 HSA $38
- Billing: equity-comp tier $1,850 + 2 equity events ($500) + HSA excess follow-up 0.5 hr. PBC items were complete, so
  no chargeable client-caused rework; the 83(b) research memo (1 hr) billed under MISC as a consultation.
""")
C.write_review_points(f"""
# Review Points - EVG1013 - 2025 - Form 1040

*Reviewer: L. Chen (blue). Preparer responses in red. Synthetic.*

1. **WP 4 / Form 8949** - Draft took the E*TRADE 1099-B basis of $4,000 -> $21,975 ST gain. The $22,000 is already in W-2 box 1
   (code V).
   - Enter code B adjustment of ($22,000); net should be a ($25) loss. Tie to the Stock Plan Supplement (WP 5).
   - *Preparer: Done. Supplement bookmarked as support / DUP - not a second sale.*
2. **WP 9-10 / Other income** - Draft included $8,000 on Schedule 1 line 8z for the Loomwork 83(b) election.
   - Check the dates: grant 11/03/2025, postmark 12/10/2025. That is outside 30 days - the election is invalid.
   - Remove the income; write the client memo (procedure: Restricted Stock).
   - *Preparer: Removed. Memo added to the return package (not attached to the e-file); client emailed 09/18.*
3. **WP 3 / Form 6251** - Form 3921 was not picked up by autoflow (no dollar box it recognizes). ISO spread $50,000 must go on line 2i.
   - *Preparer: Entered. AMT {fmt(amt_amt)}; Form 8801 carryforward {fmt(mtc_cf)} added to PERM and carryforward report.*
4. **Form 8889** - Draft deducted $1,000 on Schedule 1 line 13. Code W includes his payroll deferral; limit already used.
   - Deduction should be $0. Confirm the excess (plus earnings) is withdrawn before 10/15 or we need Form 5329 (6% = $60).
   - *Preparer: Deduction removed. Client withdrew $1,038 on 09/15/2026 (WP 13). No 5329. $38 flagged for 2026.*
5. **Form 2210** - Software generated an estimated tax penalty. Prior-year safe harbor: 2024 tax $23,526 vs withholding $27,600.
   - *Preparer: 2210 box for prior-year safe harbor - penalty $0.*
6. FYI - IL-1040: no AMT/ISO add-back; confirm IL withholding $8,150 from W-2 box 17. Chicago has no local return.
   - *Preparer: Confirmed; IL refund {fmt(il_refund)}.*
""")
print("EVG1013 done", R.summary()["24"], v["refund"], v["balance_due"])
