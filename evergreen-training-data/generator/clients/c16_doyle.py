"""EVG1016 - Megan Doyle (HOH, Michigan - Grand Rapids). Separated (not divorced) at 12/31/2025 but "considered unmarried" ->
HOH; separation agreement (scanned legal agreement): post-2018 spousal support and child support not income; Form 8332 release
of Liam -> CTC for Nora only, but HOH and Form 2441 still use both children; QDRO distribution to alternate payee (1099-R code 1)
-> 10% additional tax exception (Form 5329 code 04); qualified overtime premium reported by employer; MI exemptions per
federal dependents; Grand Rapids resident city return."""
from common import ClientBuild, gotcha, fmt
from docs import statement, scanned_pages, write_text, write_xlsx
import forms as F
from tax2025 import Return1040, r

C = ClientBuild("EVG1016", "Doyle", "Megan Doyle")
ADDR = ("2217 Oakwood Ave NE", "Grand Rapids, MI 49505")
T = {"name": "Megan R. Doyle", "ssn": "XXX-XX-5190", "dob": "1989-05-17"}
REC = [T["name"], *ADDR, f"TIN: {T['ssn']}"]

# ------------------------------------------------------------------ PERM
C.write_profile(f"""
# EVG1016 - Doyle, Megan  (PERM)

*Synthetic client - Project Evergreen training data.*

| Item | Detail |
|---|---|
| Client ID | EVG1016 (Doyle household client since 2019 - MFJ with Brian T. Doyle through 2024) |
| Taxpayer | Megan R. Doyle, DOB 05/17/1989, SSN XXX-XX-5190, Registered Nurse (ICU), Grand River Health System |
| Spouse (separated) | Brian T. Doyle, SSN XXX-XX-6632 - moved out **03/01/2025** (now in Wyoming, MI). Separation Agreement signed 03/20/2025; interim QDRO order 07/22/2025; **Judgment of Divorce entered 02/10/2026** (Kent County Circuit Court, Family Division). Brian engaged another preparer for 2025 - **conflict check: Brian is no longer our client (engagement ended 2025).** |
| Children | Liam P. Doyle, DOB 03/08/2014, SSN XXX-XX-2287; Nora J. Doyle, DOB 10/21/2017, SSN XXX-XX-9054 - both lived with Megan all of 2025 (custodial parent) |
| Address | {ADDR[0]}, {ADDR[1]} - marital home, Megan remains (Grand Rapids resident all years -> **Grand Rapids resident city return GR-1040R**) |
| Contact | Email megan.doyle.rn@example.com, (616) 555-0119 - text OK after 7pm (night shifts). eSign OK |
| Engagement | 2025: individual HOH return + MI-1040 + GR-1040R, quote $1,150 (separate engagement letter signed 02/2026) |
| Payment info | Refund - Lake Michigan Credit Union checking ****3321 (new individual account; voided check 02/2026) |
""")
F.prior_year_summary(C.perm_file("2024_Form_1040_Return_Summary.pdf", "Prior-year return summary (joint)"),
    "Brian & Megan Doyle", "EVG1016", "Married filing jointly", [
        ["1a", "W-2 wages (Grand River Health - Megan $84,110; Lakeshore Industrial Supply - Brian $71,300)", 155410],
        ["2b", "Taxable interest - Lake Michigan CU", 58],
        ["11", "AGI", 155468], ["12", "Standard deduction", 29200], ["15", "Taxable income", 126268],
        ["19", "Child tax credit (Liam, Nora)", 4000], ["Sch 3 / 2441", "Dependent care credit ($4,900 x 20%)", 980],
        ["24", "Total tax", 11322], ["35a", "Refund", 1840],
        ["MI-1040", "Exemptions 4 x $5,600; MI tax 5,655", 5655], ["GR-1040R", "Grand Rapids resident, 4 exemptions x $600", 2295]],
    notes="PY WP: joint return. Kids' after-school program at Kent Kids Club. Megan asked (12/2025 call) whether she can file "
          "'single' for 2025 since the divorce will be final in February - told her we need the separation agreement.")

# ------------------------------------------------------------------ PBC documents
EMP = {"name": "Grand River Health System", "addr1": "100 Michigan St NE", "addr2": "Grand Rapids, MI 49503", "ein": "00-3811620"}
EE = {"name": T["name"], "addr1": ADDR[0], "addr2": ADDR[1], "ssn": T["ssn"]}
WAGES = 88600.00
OT_PREM = 4860.00
GR_EX = 600
w2b = {"1": WAGES, "2": 7800.00, "3": WAGES, "4": round(WAGES * .062, 2), "5": WAGES, "6": round(WAGES * .0145, 2),
       "12": [("DD", 9820.00)], "14": [("QUAL OT PREM", OT_PREM), ("UNION DUES", 742.00)], "control": "GRHS-118802",
       "state": [{"state": "MI", "id": "38-1181620", "wages": WAGES, "tax": 3450.00}],
       "local": [{"wages": WAGES, "tax": 1311.00, "name": "GRAND RAPIDS (resident)"}]}

F.organizer(C.pbc_file("01_2025_Organizer_Doyle_Megan.pdf", "Client organizer", "2026-02-19"), "Megan Doyle", "EVG1016",
    general=[("Did your marital status change during 2025?", "Yes", "Separated March 2025, divorce final 2/10/2026 - file SINGLE?"),
             ("Were there any changes in dependents?", "Yes", "Brian gets Liam in odd years (agreement) - signed 8332"),
             ("Did you pay or receive alimony / spousal support?", "Yes", "Received $1,500/mo from April + $900/mo child support"),
             ("Did you receive distributions from a retirement plan?", "Yes", "From Brian's 401k thru the court order ($30k)"),
             ("Did you pay for childcare?", "Yes", "Kent Kids Club after school - both kids"),
             ("Did you have an FSA / dependent care benefits?", "No", ""),
             ("Did you make estimated tax payments?", "No", ""),
             ("Did you receive, sell, exchange digital assets?", "No", "")],
    dependents=[["Liam P. Doyle", "Son", "03/08/2014", "2287", "12", "No"],
                ["Nora J. Doyle", "Daughter", "10/21/2017", "9054", "12", "No"]],
    income_rows=[["Wages", "Grand River Health System (Megan)", 84110, "see W-2"],
                 ["Wages", "Lakeshore Industrial Supply Co. (Brian)", 71300, "N/A - separated"],
                 ["Interest", "Lake Michigan Credit Union", 58, "62"],
                 ["Alimony received", "Brian Doyle", "", "13,500"],
                 ["Retirement distribution", "Lakeshore 401(k) (QDRO)", "", "30,000"]],
    deductions_rows=[["Dependent care", "Kent Kids Club", 4900, "5,200"],
                     ["Mortgage interest", "Lake Michigan CU mortgage", 8410, "see 1098"],
                     ["Property tax", "City of Grand Rapids", 4210, "4,330"]],
    signature_date="02/17/2026")
F.w2(C.pbc_file("02_W-2_Grand_River_Health_Megan.pdf", "Form W-2", "2026-02-19"), EMP, EE, w2b)
QDRO_AMT, QDRO_WH, QDRO_MI = 30000.00, 6000.00, 1275.00
F.f1099_r(C.pbc_file("03_1099-R_Lakeshore_401k_QDRO_alternate_payee.pdf", "Form 1099-R", "2026-02-19"),
          ["Lakeshore Industrial Supply Co. 401(k) Savings Plan", "c/o Midwest Retirement Recordkeeping", "PO Box 4410, Troy, MI 48099",
           "TIN: 00-2270451"], REC,
          {"1": QDRO_AMT, "2a": QDRO_AMT, "2b": "Total distribution: No", "4": QDRO_WH, "7": "1", "13": "08/14/2025",
           "state": f"{QDRO_MI:,.2f} / MI / {QDRO_AMT:,.2f}"}, account="Alt payee ****0451-AP",
          notes=["Distribution to alternate payee pursuant to Qualified Domestic Relations Order (participant: Brian T. Doyle)."])
F.f1099_int(C.pbc_file("04_1099-INT_Lake_Michigan_CU.pdf", "Form 1099-INT", "2026-02-19"),
            ["Lake Michigan Credit Union", "PO Box 2848", "Grand Rapids, MI 49501", "TIN: 00-0000021"], REC, {"1": 61.88},
            account="****3321")
F.f1098(C.pbc_file("05_1098_Lake_Michigan_CU_mortgage.pdf", "Form 1098", "2026-02-19"),
        ["Lake Michigan Credit Union", "PO Box 2848", "Grand Rapids, MI 49501", "TIN: 00-0000021"],
        ["Brian T. Doyle / Megan R. Doyle", *ADDR, f"TIN: {T['ssn']}"],
        {"1": 8120.44, "2": 212480.00, "3": "05/28/2016", "7": "Yes", "10": "RE tax paid from escrow 4,330.12", "11": ""})
scanned_pages(C.pbc_file("06_Separation_Agreement_Doyle_executed_2025-03-20.pdf", "Legal agreement (scan)", "2026-02-19"),
    [["SEPARATION AND PROPERTY SETTLEMENT AGREEMENT",
      "Brian T. Doyle (\"Husband\") and Megan R. Doyle (\"Wife\")",
      "Executed March 20, 2025 - Kent County, Michigan",
      "",
      "Recitals: The parties were married 06/11/2011. They separated",
      "on March 1, 2025, when Husband moved from the marital home at",
      "2217 Oakwood Ave NE, Grand Rapids. A complaint for divorce has",
      "been filed (Case No. 25-XXXX-DM). Until entry of a Judgment of",
      "Divorce the parties remain married.",
      "",
      "Art. 3 CUSTODY. Wife shall have sole physical custody of the",
      "minor children Liam (DOB 3/8/2014) and Nora (DOB 10/21/2017).",
      "Husband parenting time: alternate weekends, Wed dinners.",
      "",
      "Art. 4 CHILD SUPPORT. Husband pays $900.00 per month beginning",
      "April 1, 2025 per MI Child Support Formula.",
      "",
      "Art. 5 SPOUSAL SUPPORT. Husband pays Wife $1,500.00 per month",
      "beginning April 1, 2025 for 36 months. Payments terminate on",
      "Wife's death or remarriage."],
     ["Art. 7 RETIREMENT. Wife is awarded $30,000.00 from Husband's",
      "Lakeshore Industrial Supply 401(k) Savings Plan, to be paid",
      "pursuant to a Qualified Domestic Relations Order. Wife may",
      "elect a cash distribution.",
      "",
      "Art. 9 TAX MATTERS.",
      " 9.1 For tax year 2025 the parties shall file SEPARATE returns.",
      " 9.2 Dependency exemption / child tax credit: Husband may",
      "     claim LIAM in ODD-numbered tax years (2025, 2027...) and",
      "     Wife claims Liam in EVEN years. Wife claims NORA every",
      "     year. Wife shall sign IRS Form 8332 for each odd year by",
      "     January 31 of the following year, provided Husband is",
      "     current on child support.",
      " 9.3 Wife is entitled to the home mortgage interest and property",
      "     tax deductions for the marital home from 3/1/2025.",
      "",
      "Signed: /s/ Brian T. Doyle  3/20/2025   /s/ Megan R. Doyle  3/20/2025",
      "Notary: K. Vander Molen, Kent County (synthetic)"]], handwritten=False, skew=.9, seed=1616)
scanned_pages(C.pbc_file("07_Interim_QDRO_Order_2025-07-22.pdf", "Legal document (scan)", "2026-02-19"),
    [["STATE OF MICHIGAN - 17TH CIRCUIT COURT - FAMILY DIVISION",
      "Doyle v. Doyle   Case No. 25-XXXX-DM",
      "",
      "STIPULATED INTERIM ORDER / QUALIFIED DOMESTIC RELATIONS ORDER",
      "",
      "Participant: Brian T. Doyle   Alternate Payee: Megan R. Doyle",
      "Plan: Lakeshore Industrial Supply Co. 401(k) Savings Plan",
      "Assigned amount: $30,000.00 as of the date of segregation.",
      "This Order is entered pursuant to MCL 552.1 et seq. and",
      "relates to the marital property rights of the Alternate Payee",
      "as spouse of the Participant.",
      "",
      "Entered: July 22, 2025   /s/ Hon. D. Brink, Circuit Judge",
      "",
      "Plan Administrator determination 08/04/2025: QUALIFIED."]], handwritten=False, skew=-.7, seed=1617)
scanned_pages(C.pbc_file("08_Form_8332_signed_Liam_2025.pdf", "IRS form (scan)", "2026-02-19"),
    [["Form 8332 (Rev. Oct 2018)  Release/Revocation of Release of Claim",
      "to Exemption for Child by Custodial Parent",
      "",
      "Name of noncustodial parent: Brian T. Doyle   SSN XXX-XX-6632",
      "Name(s) of child(ren): Liam P. Doyle",
      "",
      "Part I  Release of Claim to Exemption for Current Year",
      "I agree not to claim an exemption for the above child for the",
      "tax year 2025.",
      "",
      "Signature of custodial parent: /s/ Megan R. Doyle",
      "SSN XXX-XX-5190        Date: 01/28/2026",
      "",
      "(Original given to Brian's attorney 01/28/2026 - Megan)"]], handwritten=False, skew=1.2, seed=1618)
statement(C.pbc_file("09_Kent_Kids_Club_2025_statement.pdf", "Provider statement", "2026-02-19"),
    "Kent Kids Club - 2025 Annual Payment Statement (EIN 00-4471208)", [
        {"table": [["Child", "Program", "Amount paid 2025"], ["Liam Doyle", "After-school care Jan-May, Sep-Dec", 2600.00],
                   ["Nora Doyle", "After-school care Jan-May, Sep-Dec", 2600.00], ["Total", "", 5200.00]], "total_row": True},
        {"para": "Kent Kids Club, 1530 Plainfield Ave NE, Grand Rapids MI 49505. Payments by Megan Doyle (LMCU ****3321)."}])
HOME_COSTS = [("Mortgage interest (escrowed payments)", 8120.00, 1370.00), ("Real estate taxes (escrow)", 4330.00, 722.00),
              ("Homeowners insurance (escrow)", 1380.00, 230.00), ("Utilities (Consumers Energy, water, internet)", 5160.00, 860.00),
              ("Home repairs (furnace service, gutter)", 940.00, 0.00), ("Groceries / food eaten at home", 10400.00, 1600.00)]
HOME_TOTAL = sum(b for _, b, _ in HOME_COSTS)
HOME_BRIAN = sum(c for _, _, c in HOME_COSTS)
HOME_MEGAN = HOME_TOTAL - HOME_BRIAN
write_xlsx(C.pbc_file("10_Megan_household_costs_and_support_2025.xlsx", "Spreadsheet (client-prepared)", "2026-02-19",
                      note="requested by preparer 02/10 (PY WP note)"),
    {"Home costs 2025": [["Cost of keeping up home", "Total 2025", "Paid by Brian (Jan-Feb)", "Paid by Megan"]] +
                        [[a, b, c, b - c] for a, b, c in HOME_COSTS] +
                        [["Total", HOME_TOTAL, HOME_BRIAN, HOME_MEGAN],
                         ["(Mortgage PRINCIPAL 2025 $12,680 - excluded, not a cost of keeping up the home per Pub. 501)", "", "", ""]],
     "Support received": [["Month", "Spousal support", "Child support", "Paid via"]] +
                         [[m, 1500.00, 900.00, "MiSDU"] for m in ["Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]] +
                         [["Total", 13500.00, 8100.00, ""]]})
write_text(C.pbc_file("11_Email_Megan_2026-02-19.txt", "Client correspondence", "2026-02-19", "Email"),
"""From: Megan Doyle <megan.doyle.rn@example.com>
To: preparer@evergreentax.example
Date: Thu, 19 Feb 2026 06:48:02 -0500
Subject: Doyle 2025 - my docs (Megan only)

Hi, uploading everything after my shift. Divorce was finalized on Feb 10 (finally). So I'm single now -
I assume I file Single for 2025? The agreement says we file "separate" returns.

Brian gets to claim Liam this year (odd year), I signed the 8332 for him. I still pay for both kids'
after-school though.

I got the $30k from his 401k in August - they took 20% out. My friend said there's a 10% penalty
because I'm under 59 1/2?? Also do I have to pay tax on the $1,500/mo he pays me?

Also - is it still true Grand Rapids needs its own return? Brian says his city (Wyoming) doesn't have one.
Thanks! Megan
""")
statement(C.pbc_file("12_Grand_River_Health_OT_premium_letter.pdf", "Employer letter", "2026-02-19"),
    "Grand River Health System - Payroll - Qualified Overtime Compensation Statement (2025)", [
        {"para": ["Employee: Megan R. Doyle   Employee ID 118802",
                  "Box 14 of your 2025 Form W-2 ('QUAL OT PREM') reports the premium portion only (the amount in excess of your "
                  "regular rate) of overtime required under section 7 of the Fair Labor Standards Act, as described in the "
                  "Schedule 1-A instructions. Total overtime hours 2025: 162.0. Regular rate $60.00/hr; FLSA premium $30.00/hr x 162.0 = $4,860.00.",
                  "Shift differentials and holiday premiums not required under the FLSA are excluded."]}])
statement(C.pbc_file("13_Brian_Doyle_W-2_2025_copy.pdf", "Document for other taxpayer", "2026-02-19",
                     note="client uploaded - belongs to spouse"),
    "Copy - Form W-2 2025 - Brian T. Doyle - Lakeshore Industrial Supply Co. (uploaded by Megan)", [
        {"table": [["Box", "Amount"], ["1 Wages", 73850.00], ["2 Federal withholding", 7120.00], ["16 MI wages", 73850.00]]},
        {"para": "(Megan: 'in case you need this for joint??')"}])

# ------------------------------------------------------------------ RETURN
facts = {
    "status": "HOH",
    "taxpayer": {"age65": False},
    "dependents": [{"name": "Nora J. Doyle", "ctc": True}],       # Liam released to Brian via Form 8332
    "w2": [{"who": "T", "box1": w2b["1"], "box2": w2b["2"], "box3": w2b["3"], "box4": w2b["4"], "box5": w2b["5"], "box6": w2b["6"]}],
    "interest": [{"payer": "Lake Michigan Credit Union", "amount": 61.88}],
    "pension": [{"payer": "Lakeshore Industrial Supply 401(k) - QDRO alternate payee", "gross": QDRO_AMT, "taxable": QDRO_AMT}],
    "withholding_1099": QDRO_WH,
    "dependent_care": {"expenses": 5200.00, "n_qual": 2},
    "sch1a": {"overtime": OT_PREM},
    "itemized": {"mortgage_interest_1098": 8120.44, "real_estate_tax": 4330.12, "state_income_tax": 3450.00 + QDRO_MI + 1311.00},
}
R = Return1040(facts).compute()
v = R.values

# Michigan (exemptions follow federal: taxpayer + dependents claimed on the federal return)
MI_EX = 5800
mi_n = 2
mi_agi = v["11"]
mi_taxable = mi_agi - mi_n * MI_EX
mi_tax = r(mi_taxable * .0425)
mi_wh = r(w2b["state"][0]["tax"] + QDRO_MI)
mi_refund = mi_wh - mi_tax
# Grand Rapids resident (1.5%; $600 per exemption)
gr_income = WAGES + 61.88 + QDRO_AMT
gr_ex = 2 * GR_EX
gr_taxable = gr_income - gr_ex
gr_tax = r(gr_taxable * .015)
gr_wh = 1311
gr_due = gr_tax - gr_wh

hoh_tbl = [["Head of household - 'considered unmarried' test (IRC 7703(b) / Pub. 501)", "Result"],
           ["Married at 12/31/2025? (divorce judgment entered 02/10/2026; separation agreement is not a decree)", "Yes - married"],
           ["1. Files a separate return", "Yes"],
           [f"2. Paid more than half the cost of keeping up the home: Megan {fmt(HOME_MEGAN)} of {fmt(HOME_TOTAL)} "
            f"({HOME_MEGAN / HOME_TOTAL:.0%}; mortgage principal excluded) - even excluding the "
            "$13,500 spousal support received, her wages alone cover it", "Yes"],
           ["3. Spouse not a member of household during the last 6 months of 2025 (moved out 03/01/2025)", "Yes"],
           ["4. Home was the main home of her child for more than half the year (Liam and Nora - 12 months)", "Yes"],
           ["5. She can claim the child as a dependent - met for Nora; for Liam met except for the Form 8332 release (allowed)", "Yes"],
           ["Conclusion: 'considered unmarried' -> Head of household (not Single, not required to use MFS)", "HOH"]]
f5329 = [["Form 5329 Part I - Additional tax on early distributions", "Amount"],
         ["Line 1 Early distributions included in income (1099-R code 1, Lakeshore 401(k))", r(QDRO_AMT)],
         ["Line 2 Distributions excepted - exception number 04 (payment to alternate payee under a QDRO, IRC 72(t)(2)(C))", r(QDRO_AMT)],
         ["Line 3 Amount subject to additional tax", 0], ["Line 4 Additional tax (10%)", 0]]
f2441 = [["Form 2441 support", "Amount"],
         ["Qualifying persons: Liam (11) and Nora (8) - custodial parent may treat Liam as a qualifying person even though released on Form 8332", 2],
         ["Kent Kids Club after-school (EIN 00-4471208)", 5200],
         ["Dependent care benefits (W-2 box 10)", 0],
         ["Limit for 2 qualifying persons", 6000],
         [f"Credit 20% (AGI over $43,000)", v["form2441"]["credit"]]]
sch_a_cmp = [["Standard vs itemized (not itemizing)", "Amount"],
             ["Mortgage interest (1098 - Megan entitled from 03/2025 per agreement; she paid all 2025 escrow payments after Feb)", 8120],
             ["Real estate tax (escrow)", 4330],
             ["State + city income tax withheld", r(3450.00 + QDRO_MI + 1311.00)],
             ["Itemized total (upper bound - before splitting Jan-Feb payments made by Brian)", v["itemized_total_computed"]],
             ["HOH standard deduction", v["standard_deduction_available"]]]
C.write_return(R, [
    ("Taxpayer", "Megan R. Doyle (XXX-XX-5190)"),
    ("Address", ", ".join(ADDR)),
    ("Filing status", "Head of household - married, considered unmarried (spouse Brian T. Doyle XXX-XX-6632 not in home after 03/01/2025)"),
    ("Dependents", "Nora J. Doyle (daughter, 2017) - CTC. Liam P. Doyle (son, 2014) released to noncustodial parent on Form 8332 for "
                   "2025 - not claimed; still HOH qualifying person and Form 2441 qualifying person"),
    ("Digital assets question", "No"),
    ("Forms included", "1040, Schedule 1-A, Schedule 8812, Schedule 3, Form 2441, Form 5329, Schedule B (not required); MI-1040; GR-1040R"),
    ("State / local", "Michigan MI-1040 (resident); City of Grand Rapids GR-1040R (resident)"),
    ("Filing method", "E-file federal + MI (8879 signed 03/24/2026); GR-1040R e-filed 03/26/2026; refunds by direct deposit LMCU ****3321"),
], state_summary=[
    {"title": "Michigan MI-1040 (resident) - summary", "lines": [
        ("10", "Federal AGI", mi_agi),
        ("12-14", "Additions / subtractions - none (QDRO distribution at age 36 is not a 'retirement or pension benefit' eligible for "
                  "the MI retirement subtraction)", 0),
        ("9", f"Exemptions: {mi_n} x $5,800 (Megan + Nora - MI exemptions follow the dependents claimed on the federal return; "
              "Liam is claimed by Brian)", mi_n * MI_EX),
        ("17", "Taxable income", mi_taxable),
        ("18", "Tax at 4.25%", mi_tax),
        ("30", "MI withholding (W-2 $3,450 + 1099-R $1,275)", mi_wh),
        ("34", "Refund", mi_refund)],
     "note": "Homestead property tax credit not available (total household resources, which include spousal and child support "
             "received, exceed the limit)."},
    {"title": "City of Grand Rapids GR-1040R (resident) - summary", "lines": [
        ("1", "Wages (W-2 box 18)", r(WAGES)),
        ("2-3", "Interest", r(61.88)),
        ("5", "Retirement plan distribution - 1099-R code 1 (premature distribution; treated as taxable - see note)", r(QDRO_AMT)),
        ("-", "Spousal support / child support - not taxable", 0),
        ("8", "Total income", r(gr_income)),
        ("9", "Exemptions: 2 x $600", gr_ex),
        ("10", "Taxable income", r(gr_taxable)),
        ("11", "Tax - resident rate 1.5%", gr_tax),
        ("12", "Grand Rapids tax withheld (W-2 box 19)", gr_wh),
        ("14", "Tax due (paid with return)", gr_due)],
     "note": "Resident rate 1.5% / nonresident 0.75%. Pensions and annuities are exempt from Grand Rapids tax, but premature "
             "(code 1) plan distributions are taxable; the federal 72(t) QDRO exception does not change city taxability "
             "(reviewer confirmed with GR-1040 instructions). City return due 04/30/2026."}],
    attachments=[("Filing status determination - considered unmarried", hoh_tbl),
                 ("Form 5329 - exception to 10% additional tax", f5329),
                 ("Form 2441 - Child and dependent care expenses", f2441),
                 ("Schedule A comparison (standard deduction used)", sch_a_cmp)])

gotchas = [
    gotcha("EVG1016-G1", "Filing Status (separations are not divorces)", "Divorce final 02/10/2026; client wants 'Single'",
           "File Single because the divorce is final when the return is prepared, or MFS because the agreement says 'separate returns'.",
           "Marital status is tested at 12/31/2025 - still married. But she is 'considered unmarried' (separate return, paid > half "
           "of home costs, child lived with her > half year, spouse out of home last 6 months) -> HOH, which also satisfies the "
           "agreement's 'separate returns' clause.", "HOH vs MFS: std deduction $23,625 vs $15,750 + brackets + credits",
           ["Filing status", "12e", "16"], "hard"),
    gotcha("EVG1016-G2", "Scan - legal agreements (tax-reportable amounts)", "Separation agreement: spousal support + child support",
           "Report $13,500 spousal support as alimony income (Sch 1 line 2a) and/or child support as income.",
           "Instrument executed 03/20/2025 (after 2018) -> alimony is neither income to her nor deductible by Brian. Child support "
           "is never income. Nothing reported.", "Income overstated $13,500-$21,600", ["8", "Sch 1 2a"], "medium"),
    gotcha("EVG1016-G3", "Review - dependents (Form 8332 release)", "Liam released to Brian for 2025 (odd year)",
           "Claim both children for CTC ($4,400), or drop Liam from HOH / Form 2441 as well.",
           "Form 8332 releases only the dependency-related credits (CTC/ODC). Megan claims CTC for Nora only ($2,200); she remains "
           "custodial parent: Liam still counts for HOH and as a Form 2441 qualifying person (and EIC, though not eligible here).",
           "CTC overstated $2,200 / 2441 limit understated", ["19", "Form 2441"], "medium"),
    gotcha("EVG1016-G4", "Client IRAs / retirement distributions (1099-R code 1)", "QDRO distribution to alternate payee, age 36",
           "Report on line 4 (IRA) and/or assess the 10% additional tax ($3,000) because code 1 is shown.",
           "Taxable $30,000 on line 5a/5b (qualified plan). File Form 5329 with exception 04 (72(t)(2)(C) - payment to alternate payee "
           "under a QDRO) -> $0 additional tax. $6,000 (20%) withheld on line 25b.", "$3,000 additional tax avoided",
           ["5b", "25b", "Form 5329"], "medium"),
    gotcha("EVG1016-G5", "OBBBA - no tax on overtime (Schedule 1-A Part III)", "Employer reported the FLSA premium itself",
           "Divide the box 14 amount by 3 (as for total-OT W-2s like EVG1001), deducting only $1,620.",
           "Box 14 'QUAL OT PREM' and the employer letter show the premium portion only -> full $4,860 qualifies. Considered-unmarried "
           "HOH is not 'married' for 7703 purposes, so the joint-return requirement does not bar the deduction.",
           "Line 13b understated $3,240", ["13b"], "medium"),
    gotcha("EVG1016-G6", "SALT Implications (state exemptions)", "Michigan exemptions after Form 8332 release",
           "Claim 3 MI exemptions (Megan + both kids) as in the organizer.",
           "MI personal exemptions follow the dependents claimed on the federal return: Megan + Nora = 2 x $5,800 (assumption stated: "
           "Brian claims Liam's MI exemption).", f"MI tax understated {fmt(r(MI_EX * .0425))} if 3 exemptions", ["MI-1040 9"], "medium"),
    gotcha("EVG1016-G7", "Local Filing Requirements", "Grand Rapids resident city return",
           "No city return (client's ex-spouse's city has none) or omit the QDRO distribution from city income.",
           f"Grand Rapids resident (1.5%) GR-1040R required; premature distribution taxable to the city; tax {fmt(gr_tax)} vs "
           f"withheld {fmt(gr_wh)} -> {fmt(gr_due)} due 04/30/2026.", f"{fmt(gr_due)} city balance due", ["GR-1040R"], "medium"),
    gotcha("EVG1016-G8", "Scan - documents for another taxpayer", "Brian's W-2 uploaded by Megan",
           "Add Brian's W-2 to her return (or prepare a joint return).",
           "Separate return - Brian's W-2 is not hers; do not import. Keep out of her WP (confidentiality; Brian is not our client).",
           "Wages overstated $73,850", ["1a"], "easy"),
]
C.write_answer_key(R, {"residence": "MI - Grand Rapids (MI-1040 + GR-1040R)", "complexity": "Basic W-2 tier + separation items"},
                   gotchas,
                   state=[{"jurisdiction": "Michigan", "form": "MI-1040", "agi": mi_agi, "exemptions": mi_n * MI_EX,
                           "taxable_income": mi_taxable, "tax": mi_tax, "withholding": mi_wh, "refund": mi_refund},
                          {"jurisdiction": "Grand Rapids (resident)", "form": "GR-1040R", "total_income": r(gr_income),
                           "exemptions": gr_ex, "taxable_income": r(gr_taxable), "tax": gr_tax, "withholding": gr_wh,
                           "balance_due": gr_due, "due": "2026-04-30"}],
                   filings=[{"form": "Form 1040 (federal) - HOH", "method": "e-file", "due": "2026-04-15", "filed": "2026-03-25"},
                            {"form": "MI-1040", "method": "e-file", "due": "2026-04-15", "filed": "2026-03-25"},
                            {"form": "GR-1040R", "method": "e-file", "due": "2026-04-30", "filed": "2026-03-26"}])

C.write_receipt_log("EVG1016-1040-2025", "J. Ortiz (staff)", "L. Chen (senior)", "S. Kennedy, CPA", "2026-02-19")
C.write_notes(f"""
# EVG1016 - Doyle, Megan - 2025 Form 1040 - Preparer Notes

*Synthetic client - Project Evergreen. Return status: **signed off; federal + MI e-filed 03/25/2026 (accepted); GR-1040R e-filed 03/26/2026.***

## Return summary
| | |
|---|---|
| Filing status | Head of household (married, considered unmarried) |
| Income | Wages {fmt(v['1a'])}; QDRO distribution {fmt(v['5b'])} (line 5b); interest {fmt(v['2b'])} |
| AGI (line 11) | {fmt(v['11'])} |
| Deductions | Standard {fmt(v['12e'])} + Schedule 1-A overtime premium {fmt(v['13b'])} |
| Taxable income | {fmt(v['15'])} |
| Tax | {fmt(v['16'])} |
| Credits | CTC {fmt(v['19'])} (Nora) + dependent care {fmt(v['20'])} |
| Total tax | {fmt(v['24'])} |
| Withholding (W-2 + 1099-R) | {fmt(v['25d'])} |
| **Refund** | **{fmt(v['refund'])}** |
| Michigan | tax {fmt(mi_tax)}, withheld {fmt(mi_wh)}, refund {fmt(mi_refund)} |
| Grand Rapids | tax {fmt(gr_tax)}, withheld {fmt(gr_wh)}, **due {fmt(gr_due)}** |

## What I did and why (plain English)
1. **Filing status.** Megan asked to file Single because her divorce became final on 02/10/2026. Status is determined on
   12/31/2025, when she was still married (a separation agreement is not a divorce or separate-maintenance decree). She is,
   however, **"considered unmarried"**: separate return; she paid {HOME_MEGAN / HOME_TOTAL:.0%} of the cost of keeping up the home ({fmt(HOME_MEGAN)} of {fmt(HOME_TOTAL)};
   interest, taxes, insurance, utilities, repairs and food - not mortgage principal - per Pub. 501; her wages alone exceed the full cost, so it doesn't matter whether spousal support counts as her money); Brian did not
   live there after 03/01/2025 (last 6 months test met); both kids lived with her all year. -> **Head of household.** This is
   consistent with the agreement's "separate returns" clause (HOH is a separate return). Brian must file MFS.
2. **Children / Form 8332.** Agreement Art. 9.2: Brian claims Liam in odd years; Megan signed Form 8332 (Part I, 2025 only)
   on 01/28/2026. The release moves only the child tax credit: Megan claims **CTC for Nora only ({fmt(v['19'])})**. As the
   custodial parent she still uses Liam for HOH and Form 2441.
3. **Spousal and child support.** $1,500/month spousal support (Apr-Dec = $13,500) under an instrument executed in 2025 ->
   **not income** (TCJA rule for post-2018 instruments; also not deductible by Brian). Child support ($8,100) is never income.
4. **QDRO distribution.** Megan received $30,000 from Brian's 401(k) as alternate payee under the interim QDRO (plan
   administrator qualified it 08/04/2025). Taxable to her (not Brian) on **line 5a/5b** (qualified plan, not an IRA). The
   1099-R shows code 1, so **Form 5329** is filed claiming **exception 04** (72(t)(2)(C) - payments to an alternate payee under a
   QDRO) -> no 10% additional tax (her friend was wrong, but only because of the QDRO; had she rolled it to an IRA first and
   then withdrawn, the exception would have been lost). 20% withheld ($6,000) on line 25b.
5. **Overtime.** Box 14 "QUAL OT PREM 4,860" plus the employer's letter show the FLSA premium already isolated (162 OT
   hours x $30 half-time) -> the **full $4,860** is deductible on Schedule 1-A (contrast EVG1001, where box 14 was total OT
   pay and had to be divided by 3). MAGI {fmt(v['11'])} is under the $150,000 phase-out. The "must file jointly if married"
   rule refers to marital status under section 7703, and a considered-unmarried HOH is treated as not married - deduction allowed.
6. **Dependent care (Form 2441).** Kent Kids Club $5,200 for both kids, no FSA. Two qualifying persons ($6,000 limit) ->
   20% x $5,200 = **{fmt(v['20'])}**.
7. **Itemizing?** Mortgage interest $8,120 + property tax $4,330 + state/city tax ~$6,036 < HOH standard deduction $23,625 ->
   standard. (Even as an upper bound, before splitting the Jan-Feb payments Brian made.)
8. **Michigan.** MI-1040 from federal AGI {fmt(mi_agi)}; no retirement subtraction (a premature QDRO cash-out at 36 is not a
   retirement benefit). **Exemptions: 2 x $5,800** - assumption: MI personal exemptions follow the dependents claimed on the
   federal return, so Liam's MI exemption goes with Brian's federal claim. Tax {fmt(mi_tax)}; withholding {fmt(mi_wh)};
   refund {fmt(mi_refund)}. Homestead property tax credit - not eligible (household resources over the limit).
9. **Grand Rapids (Local Filing Requirements).** Still a Grand Rapids resident -> GR-1040R at 1.5% with $600 exemptions (2).
   Income: wages, interest and the QDRO distribution (premature distribution - taxable for the city even though exempt from
   the federal 10% tax). Support payments are not taxable. Tax {fmt(gr_tax)} vs withheld {fmt(gr_wh)} -> **{fmt(gr_due)} due**
   with the city return by 04/30/2026 (paid by direct debit). Brian's new city (Wyoming, MI) has no income tax - not our concern.
10. **Brian's W-2** was uploaded by Megan - not used; removed from her WP. Brian is no longer our client (conflict note in PERM).

## Open items / client communication
- None open. Advised Megan (email 03/20): 2026 filing status Single or HOH (divorced 02/10/2026 - HOH if kids live with her);
  2026 is an even year - she claims Liam; she should update her W-4 (HOH) and GR-W4 exemptions.

## Hand-off to signer / routing
- [x] Return locked; Accountant's copy saved as *reviewed*
- [x] Federal 1040 (HOH) - e-file; due 04/15/2026
- [x] MI-1040 - e-file; due 04/15/2026
- [x] GR-1040R - e-file; **due 04/30/2026**; balance {fmt(gr_due)} by direct debit
- [x] No FBAR
- [x] eSign 8879 / MI-8453 - email; text OK after 7pm
- [x] Special: do not attach Form 8332 (noncustodial parent attaches it); separation agreement kept in PERM
- Billing: $1,150 quote + 0.5 hr filing-status research memo; nothing to W/O.
""")
C.write_review_points(f"""
# Review Points - EVG1016 - 2025 - Form 1040

*Reviewer: L. Chen (blue). Preparer responses in red. Synthetic.*

1. **Filing status** - Draft was Single (organizer + client email). She was married on 12/31/2025 - divorce entered 02/10/2026.
   - Run the considered-unmarried test (WP 10 home-cost sheet; agreement recitals show Brian left 03/01/2025). Should be HOH.
   - *Preparer: Changed to HOH; test documented in the return statement.*
2. **Schedule 1 / WP 6** - Draft picked up $13,500 alimony (line 2a) from the organizer.
   - Agreement executed 03/20/2025 - post-2018 instrument. Remove.
   - *Preparer: Removed. Child support also not income.*
3. **Schedule 8812** - Draft claimed CTC for both kids. 8332 signed for Liam (2025).
   - Nora only. Keep Liam on 2441 and as HOH qualifying person.
   - *Preparer: Done - CTC {fmt(v['19'])}; 2441 still 2 qualifying persons.*
4. **1099-R** - Autoflow put the QDRO distribution on line 4a/4b and generated a $3,000 10% additional tax.
   - It is a 401(k) -> line 5a/5b. Form 5329 exception 04 (alternate payee under QDRO).
   - *Preparer: Moved to line 5; 5329 line 2 = $30,000, code 04; additional tax $0.*
5. **Schedule 1-A** - Draft took 1/3 of box 14 (copied the Bell method). Read the employer letter - premium already isolated.
   - *Preparer: Full $4,860.*
6. **MI-1040** - Draft had 3 exemptions. Liam's exemption follows the federal claim.
   - *Preparer: 2 exemptions; assumption documented in notes.*
7. **GR-1040R** - Draft excluded the 1099-R as a "pension". Code 1 premature distribution is taxable to the city. Due 04/30.
   - *Preparer: Included; GR balance due {fmt(gr_due)}.*
8. FYI - Brian's W-2 in the PBC (#13) - do not use; remove from the WP and do not share.
   - *Preparer: Removed from combined WP.*
""")
print("EVG1016 done", R.summary()["24"], v["refund"], v["balance_due"], "MI", mi_tax, mi_refund, "GR", gr_tax, gr_due)
