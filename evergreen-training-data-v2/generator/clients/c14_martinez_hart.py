"""EVG1014 - Sofia Martinez & Liam Hart (MFJ, Michigan - Ann Arbor). Newlyweds married 12/20/2025 -> married all year;
MFJ vs MFS simulation; SSA name mismatch -> e-file reject IND-031-04; first-year freelance Schedule C with 1099-K / 1099-NEC
double-reporting; home office Form 8829 vs simplified (part-year); de minimis laptop; unemployment; 2210 combined-PY safe harbor."""
from common import ClientBuild, gotcha, fmt
from docs import statement, scanned_pages, write_text, write_xlsx, write_csv
import forms as F
from tax2025 import Return1040, r, se_tax

C = ClientBuild("EVG1014", "Martinez-Hart", "Sofia Martinez & Liam Hart")
ADDR = ("611 S Division St Apt 4B", "Ann Arbor, MI 48104")
TP = {"name": "Sofia E. Martinez", "ssn": "XXX-XX-3057", "dob": "2000-04-09"}   # primary (name per SSA record)
SP = {"name": "Liam P. Hart", "ssn": "XXX-XX-8124", "dob": "1996-11-02"}
REC_T = [TP["name"], *ADDR, f"TIN: {TP['ssn']}"]
REC_S = [SP["name"], *ADDR, f"TIN: {SP['ssn']}"]

# ------------------------------------------------------------------ PERM
C.write_profile(f"""
# EVG1014 - Martinez, Sofia & Hart, Liam  (PERM)

*Synthetic client - Project Evergreen training data.*

| Item | Detail |
|---|---|
| Client ID | EVG1014 (originally Liam Hart, Single, client since 2022; Sofia added for TY2025 after marriage) |
| Taxpayer (primary on 2025 return) | **Sofia E. Martinez** - name on Social Security card / SSA record (name control **MART**). DOB 04/09/2000, SSN XXX-XX-3057. Freelance graphic designer from 04/2025 (laid off from Kerrytown Creative Agency 12/2024). |
| Spouse | Liam P. Hart, DOB 11/02/1996, SSN XXX-XX-8124, Software QA Engineer, Huron Valley Software Group LLC |
| Marriage | Married 12/20/2025, Washtenaw County, MI. Sofia uses "Sofia Hart" socially and signed the organizer that way but has **NOT** filed Form SS-5 with SSA (as of 09/2026). |
| Address | {ADDR[0]}, {ADDR[1]} - both Ann Arbor residents all of 2025 (lived together, lease in both names). **Ann Arbor has no city income tax.** |
| Contact | Liam preferred - liam.hart@example.com, (734) 555-0162; Sofia - sofia.designs@example.com; eSign OK |
| Engagement | Liam: basic W-2 tier since 2022. 2025: joint return + Schedule C (first year) - quote $1,650. |
| Health coverage 2025 | Liam - employer plan (self-only until 01/2026). Sofia - covered as a dependent on her father's employer plan (under age 26); no premiums paid by her. |
| Payment info | Joint checking - Univ. of Michigan Credit Union ****5580 (voided check on file 03/2026) |
""")
F.prior_year_summary(C.perm_file("2024_Form_1040_Return_Summary_Liam_Hart.pdf", "Prior-year return summary (Liam, Single)"),
    "Liam Hart", "EVG1014", "Single", [
        ["1a", "W-2 wages (Brightline QA Services Inc.)", 64000],
        ["2b", "Taxable interest - Capital One 360", 190],
        ["11", "AGI", 64190], ["12", "Standard deduction", 14600], ["15", "Taxable income", 49590],
        ["24", "Total tax", 5963], ["25a", "Federal withholding", 6420], ["35a", "Refund", 457],
        ["MI-1040", "MI AGI 64,190; exemption 5,600; MI tax 2,490", 2490]],
    notes="PY WP: Single, no dependents. Liam changed jobs 01/2025 (Huron Valley Software Group). Mentioned partner Sofia may "
          "start freelancing - send Schedule C organizer pages for 2025.")

# ------------------------------------------------------------------ PBC documents
EMP_L = {"name": "Huron Valley Software Group LLC", "addr1": "301 E Liberty St Ste 600", "addr2": "Ann Arbor, MI 48104", "ein": "00-6627310"}
EE_L = {"name": SP["name"], "addr1": ADDR[0], "addr2": ADDR[1], "ssn": SP["ssn"]}
w2_l = {"1": 88000.00, "2": 8900.00, "3": 92000.00, "4": 5704.00, "5": 92000.00, "6": 1334.00,
        "12": [("D", 4000.00), ("DD", 6480.00)], "13": ["Retirement plan: X"], "control": "HVSG-2025-0391",
        "state": [{"state": "MI", "id": "38-0662731", "wages": 88000.00, "tax": 3800.00}]}

F.organizer(C.pbc_file("01_2025_Organizer_Hart.pdf", "Client organizer", "2026-02-16"), "Liam Hart & Sofia Hart", "EVG1014",
    general=[("Did your marital status change during 2025?", "Yes", "Got married 12/20/2025!! (Sofia Hart - new name)"),
             ("Filing status preference?", "?", "Whatever is cheaper - married separately since we only married in December?"),
             ("Did you start a business or have self-employment income?", "Yes", "Sofia - freelance design since April"),
             ("Did you make payments that would require you to file Form(s) 1099?", "No", ""),
             ("Did you use part of your home for business?", "Yes", "Sofia's studio = 2nd bedroom (approx 150 sq ft)"),
             ("Did you receive unemployment compensation?", "Yes", "Sofia Jan-Mar"),
             ("Did you make estimated tax payments?", "No", ""),
             ("Did you receive, sell, exchange digital assets?", "No", "")],
    dependents=[],
    income_rows=[["Wages", "Huron Valley Software Group LLC (Liam)", "", "see W-2"],
                 ["Wages", "Brightline QA Services Inc. (Liam - PY employer)", 64000, "left job"],
                 ["Interest", "Capital One 360 (Liam)", 190, "208"],
                 ["Interest", "Ally Bank (Sofia)", "", "142"],
                 ["Unemployment", "State of Michigan UIA (Sofia)", "", "5,460"],
                 ["Self-employment", "Sofia - design clients", "", "see 1099s + my spreadsheet"]],
    deductions_rows=[["Rent", "Apartment - $1,950/mo", "", "23,400"],
                     ["Business expenses", "Sofia - see spreadsheet", "", "yes"]],
    signature_date="02/14/2026  /s/ Liam Hart   /s/ Sofia Hart")

F.w2(C.pbc_file("02_W-2_Huron_Valley_Software_Liam.pdf", "Form W-2", "2026-02-16"), EMP_L, EE_L, w2_l)
F.f1099_g(C.pbc_file("03_1099-G_Michigan_UIA_Sofia.pdf", "Form 1099-G", "2026-02-16"),
          ["State of Michigan - Unemployment Insurance Agency", "3024 W Grand Blvd", "Detroit, MI 48202", "TIN: 00-6000134"],
          REC_T, {"1": 5460.00, "4": 546.00, "state": "MI / 00-6000134 / 232.05"}, account="UIA claim ****7810")
UC, UC_FWH, UC_MIWH = 5460.00, 546.00, 232.05
NEC_A, NEC_B = 18000.00, 9500.00
F.f1099_nec(C.pbc_file("04_1099-NEC_Kerrytown_Creative.pdf", "Form 1099-NEC", "2026-02-16"),
            ["Kerrytown Creative Agency LLC", "210 Kerrytown Ct", "Ann Arbor, MI 48104", "TIN: 00-4481026"], REC_T, {"1": NEC_A})
F.f1099_nec(C.pbc_file("05_1099-NEC_Arbor_Brewing_Collective.pdf", "Form 1099-NEC", "2026-02-16"),
            ["Arbor Brewing Collective Inc.", "114 E Washington St", "Ann Arbor, MI 48104", "TIN: 00-7719350"], REC_T, {"1": NEC_B},
            notes=["Payer note: amounts paid to vendor during 2025 (invoices LMD-103, 104, 107, 108, 109, 111, 115)."])
stripe_months = [0, 0, 0, 1200.00, 2350.00, 1500.00, 2400.00, 900.00, 1650.00, 1100.00, 800.00, 500.00]
STRIPE_GROSS = sum(stripe_months)
# Stripe payout export - shows the Arbor Brewing invoices were paid by card through Stripe
stripe_rows = []
arbor = [("2025-05-14", "LMD-104", 2350.00), ("2025-07-09", "LMD-107", 1500.00), ("2025-07-30", "LMD-108", 900.00),
         ("2025-09-03", "LMD-111", 1650.00), ("2025-10-22", "LMD-115", 1100.00), ("2025-06-02", "LMD-103", 1500.00),
         ("2025-08-06", "LMD-109", 500.00)]
others = [("2025-04-18", "Huron Pilates Studio", "LMD-101", 1200.00), ("2025-08-20", "Sparrow Books", "LMD-110", 400.00),
          ("2025-11-12", "Washtenaw Yoga Collective", "LMD-117", 800.00), ("2025-12-05", "Sparrow Books", "LMD-119", 500.00)]
assert abs(sum(a[2] for a in arbor) - NEC_B) < .01
assert abs(sum(a[2] for a in arbor) + sum(o[3] for o in others) - STRIPE_GROSS) < .01
charges = sorted([(d, "Arbor Brewing Collective Inc.", inv, amt) for d, inv, amt in arbor] + others)
fee_total = 0.0
for d, cust, inv, amt in charges:
    fee = round(amt * .029 + .30, 2)
    fee_total += fee
    stripe_rows.append([d, "charge", cust, inv, f"{amt:.2f}", f"{fee:.2f}", f"{amt - fee:.2f}", "paid out"])
N_CHARGES = len(charges)
STRIPE_FEES = round(fee_total, 2)
F.f1099_k(C.pbc_file("06_1099-K_Stripe.pdf", "Form 1099-K", "2026-02-16"),
          ["Stripe, Inc.", "354 Oyster Point Blvd", "South San Francisco, CA 94080", "TIN: 00-2330271"], REC_T,
          {"1a": STRIPE_GROSS, "1b": STRIPE_GROSS, "2": "7333", "3": N_CHARGES, "months": stripe_months,
           "filer_type": "Payment settlement entity (PSE) - payment card"},
          notes=["Gross amount is the total dollar amount of payment transactions, without adjustment for fees, refunds or chargebacks."])

F.f1099_int(C.pbc_file("07_1099-INT_Capital_One_Liam.pdf", "Form 1099-INT", "2026-02-16"),
            ["Capital One, N.A.", "PO Box 85123", "Richmond, VA 23285", "TIN: 00-0000013"], REC_S, {"1": 208.44}, account="360 ****4410")
F.f1099_int(C.pbc_file("08_1099-INT_Ally_Sofia.pdf", "Form 1099-INT", "2026-02-16"),
            ["Ally Bank", "PO Box 951", "Horsham, PA 19044", "TIN: 00-0000002"], REC_T, {"1": 141.87}, account="****9023")

write_csv(C.pbc_file("09_Stripe_balance_history_2025.csv", "Spreadsheet (CSV)", "2026-02-16"),
          ["created (UTC)", "type", "customer", "description / invoice", "amount", "fee", "net", "status"], stripe_rows)
# Sofia's own income & expense workbook
VENMO = 350.00
income_rows = [["Date", "Client", "Invoice", "Paid via", "Amount", "Notes"]]
income_rows += [["2025-04-30", "Kerrytown Creative Agency LLC", "LMD-100", "ACH", 4500.00, "retainer Apr-May"],
                ["2025-06-30", "Kerrytown Creative Agency LLC", "LMD-102", "ACH", 4500.00, ""],
                ["2025-09-30", "Kerrytown Creative Agency LLC", "LMD-112", "ACH", 4500.00, ""],
                ["2025-12-15", "Kerrytown Creative Agency LLC", "LMD-118", "ACH", 4500.00, "1099-NEC"]]
income_rows += [[d, c, inv, "Stripe (card)", amt, "1099-NEC too" if c.startswith("Arbor") else ""] for d, c, inv, amt in charges]
income_rows += [["2025-07-19", "Jess M. (friend) - logo for her Etsy shop", "-", "Venmo", VENMO, "no form"]]
GROSS = NEC_A + STRIPE_GROSS + VENMO
assert abs(sum(x[4] for x in income_rows[1:]) - GROSS) < .01
income_rows += [["", "TOTAL", "", "", GROSS, ""]]

exp = [  # (date, vendor, category, amount, business %, deductible?, note)
    ("2025-04-05", "Apple Store - MacBook Pro 14in", "Equipment", 1899.00, 1.0, True, "de minimis"),
    ("2025-04-07", "Wacom - Intuos Pro tablet", "Equipment", 379.00, 1.0, True, "de minimis"),
    ("Apr-Dec", "Adobe Creative Cloud (9 x 59.99)", "Software", 539.91, 1.0, True, ""),
    ("Apr-Dec", "Figma Professional (9 x 15.00)", "Software", 135.00, 1.0, True, ""),
    ("various", "Adobe Stock / Envato fonts & images", "Supplies", 385.00, 1.0, True, ""),
    ("2025-04-02", "Squarespace - portfolio site + domain", "Advertising", 276.00, 1.0, True, ""),
    ("2025-04-10", "Dribbble Pro", "Advertising", 96.00, 1.0, True, ""),
    ("2025-05-01", "MOO - business cards", "Advertising", 118.00, 1.0, True, ""),
    ("Apr-Dec", "Verizon - my phone (9 x 70.00)", "Utilities", 630.00, .5, True, "50% business"),
    ("various", "Coffee w/ clients (Sweetwaters, Literati)", "Meals", 164.00, .5, True, "50% limit"),
    ("Apr-Dec", "Spotify Premium (music while I work)", "Software", 99.00, 0.0, False, "personal"),
    ("2025-10-14", "Print Ann Arbor - our wedding invitations", "Printing", 640.00, 0.0, False, "personal - own wedding"),
]
EXP_ALLOWED = round(sum(a * p for _, _, _, a, p, ok, _ in exp if ok), 2)
exp_rows = [["Date", "Vendor", "Category", "Amount", "Business %", "Client note"]] + \
           [[d, vnd, cat, a, f"{int(p*100)}%" if ok else "100%", n] for d, vnd, cat, a, p, ok, n in exp]
write_xlsx(C.pbc_file("10_Sofia_Design_Income_Expenses_2025.xlsx", "Spreadsheet (client-prepared books)", "2026-02-16"),
           {"Income": income_rows, "Expenses": exp_rows,
            "Home studio": [["Item", "Monthly", "Months (Apr-Dec)", "Total"],
                            ["Rent - 611 S Division Apt 4B (900 sq ft)", 1950.00, 9, 17550.00],
                            ["DTE Energy (electric + gas) avg", 96.00, 9, 864.00],
                            ["AT&T Fiber internet", 75.00, 9, 675.00],
                            ["Lemonade renters insurance", 16.00, 9, 144.00],
                            ["Studio = 2nd bedroom, ~150 sq ft, used only for design work", "", "", ""]]})
statement(C.pbc_file("11_Lease_611_S_Division_Apt4B.pdf", "Lease (excerpt)", "2026-02-16"),
    "Residential Lease Agreement - 611 S Division St, Apt 4B, Ann Arbor MI 48104 (excerpt)", [
        {"table": [["Term", "Detail"], ["Tenants", "Liam P. Hart; Sofia E. Martinez"], ["Landlord", "Division Street Flats LLC"],
                   ["Lease term", "08/01/2024 - 07/31/2026"], ["Monthly rent", 1950.00],
                   ["Unit", "2 bedroom / 1 bath, approx. 900 sq ft"], ["Utilities", "Tenant pays DTE and internet"]],
         "left_align_cols": [0, 1]}])
# Sofia's 2024 return (self-prepared)
statement(C.pbc_file("12_Sofia_2024_TurboTax_return_summary.pdf", "Prior-year return (other preparer)", "2026-02-16"),
    "2024 Form 1040 - Sofia E. Martinez - TurboTax Tax Summary (client copy)", [
        {"table": [["Line", "Item", "Amount"], ["Filing status", "Single", ""], ["1a", "Wages - Kerrytown Creative Agency LLC", 41000],
                   ["2b", "Taxable interest", 95], ["11", "AGI", 41095], ["12", "Standard deduction", 14600],
                   ["15", "Taxable income", 26495], ["24", "Total tax", 2947], ["25a", "Withholding", 3310], ["35a", "Refund", 363],
                   ["MI-1040", "MI tax (41,095 - 5,600) x 4.25%", 1509]], "left_align_cols": [0, 1]}])
scanned_pages(C.pbc_file("13_IMG_2291_marriage_certificate.pdf", "Photo upload (image)", "2026-02-16", "Client email attachment"),
    [["STATE OF MICHIGAN - CERTIFICATE OF MARRIAGE",
      "County of Washtenaw        Local file no. 2025-xxxx",
      "",
      "Party A: Liam Patrick Hart      Age 29   Ann Arbor, MI",
      "Party B: Sofia Elena Martinez   Age 25   Ann Arbor, MI",
      "",
      "Date of marriage: December 20, 2025",
      "Place: Ann Arbor, Washtenaw County",
      "Officiant: Hon. R. Delgado (synthetic)",
      "",
      "Surname after marriage - Party B: HART"]], handwritten=False, skew=1.8, seed=1414)
write_text(C.pbc_file("14_Email_Liam_2026-02-16.txt", "Client correspondence", "2026-02-16", "Email"),
"""From: Liam Hart <liam.hart@example.com>
To: preparer@evergreentax.example
Date: Mon, 16 Feb 2026 20:31:12 -0500
Subject: Hart 2025 - uploaded everything

Hi! Big year - Sofia and I got married in December (certificate attached) so this year it's both of us.
Please put her down as Sofia Hart. We'd like whichever is cheaper - joint or separate. Somebody at work said
since we only got married on Dec 20 we have to file single for 2025?

Sofia started freelancing in April after unemployment ran out. Her spreadsheet has everything. Stripe sent a
1099-K AND Arbor Brewing sent a 1099-NEC - she thinks they're for the same money, not sure.

We didn't make any estimated payments - hope that's ok.
Liam
""")
statement(C.pbc_file("15_Ann_Arbor_Art_Fair_booth_flyer.pdf", "Other document", "2026-02-16", note="included in upload"),
    "Ann Arbor Summer Art Fair 2026 - Artist Booth Application (flyer)", [
        {"para": "Booth applications for the July 2026 fair open March 1. Jury fee $45. (Client included this flyer in her upload.)"}])
write_text(C.pbc_file("16_Email_thread_eFile_reject_2026-04-09.txt", "Client correspondence", "2026-04-09", "Email",
                      "e-file reject follow-up"),
"""From: preparer@evergreentax.example
To: Liam Hart; Sofia Martinez
Cc: L. Chen
Date: Thu, 9 Apr 2026 08:15:00 -0400
Subject: Hart/Martinez 2025 - IRS rejected e-file (name mismatch) - quick question

Hi Sofia and Liam - the IRS rejected the e-filed return last night with code IND-031-04: the primary taxpayer's
name control ("HART") does not match the SSN in the IRS/SSA database. Has Sofia filed Form SS-5 with Social
Security to change her name to Hart yet?

-----
From: Sofia Martinez <sofia.designs@example.com>
Date: Thu, 9 Apr 2026 10:02:47 -0400

Oh no - no, I haven't done the Social Security name change yet. My card still says Martinez.
Should I use Martinez?
""")

# ------------------------------------------------------------------ SCHEDULE C / 8829 computations
SQFT, HOME_SQFT, MONTHS = 150, 900, 9
BUS_PCT = SQFT / HOME_SQFT
rent, dte, net, ins = 1950.00 * MONTHS, 96.00 * MONTHS, 75.00 * MONTHS, 16.00 * MONTHS
indirect = rent + dte + net + ins
OFFICE_8829 = r(indirect * BUS_PCT)
SIMPLIFIED = r(5 * SQFT * MONTHS / 12)          # Rev. Proc. 2013-13 average monthly allowable square footage
gross_receipts = GROSS
exp_total = EXP_ALLOWED + STRIPE_FEES
tentative = gross_receipts - exp_total
SCH_C = r(tentative - OFFICE_8829)
se = se_tax(SCH_C, 0)
QBI = SCH_C - se["half"]

TAX_2024 = {"Liam": 5963, "Sofia": 2947}
PY_SAFE = sum(TAX_2024.values())


def facts_for(status, who=None):
    w2 = [{"who": "S", "box1": w2_l["1"], "box2": w2_l["2"], "box3": w2_l["3"], "box4": w2_l["4"], "box5": w2_l["5"], "box6": w2_l["6"]}]
    sofia = {"interest": [{"payer": "Ally Bank (Sofia)", "amount": 141.87}],
             "sch1": {"sch_c": SCH_C, "unemployment": UC}, "se": [{"who": "T", "net_profit": SCH_C, "w2_ss_wages": 0}],
             "qbi": {"businesses": [{"name": "Sofia Martinez Design (Sch C)", "qbi": QBI}]}, "withholding_1099": UC_FWH}
    if status == "MFJ":
        f = {"status": "MFJ", "taxpayer": {}, "spouse": {}, "w2": w2,
             "interest": [{"payer": "Ally Bank", "amount": 141.87}, {"payer": "Capital One, N.A.", "amount": 208.44}],
             "sch1": sofia["sch1"], "se": sofia["se"], "qbi": sofia["qbi"], "withholding_1099": UC_FWH}
        return f
    if who == "Sofia":
        return dict(status="MFS", taxpayer={}, **sofia)
    w2[0]["who"] = "T"
    return {"status": "MFS", "taxpayer": {}, "w2": w2, "interest": [{"payer": "Capital One, N.A.", "amount": 208.44}]}


R = Return1040(facts_for("MFJ")).compute()
v = R.values
Rs = Return1040(facts_for("MFS", "Sofia")).compute()
Rl = Return1040(facts_for("MFS", "Liam")).compute()
mfs_tax = Rs.values["24"] + Rl.values["24"]
mfs_net = (Rs.values["refund"] - Rs.values["balance_due"]) + (Rl.values["refund"] - Rl.values["balance_due"])
mfj_net = v["refund"] - v["balance_due"]
savings = mfs_tax - v["24"]
wh_total = v["25d"]
req_90 = r(.9 * v["24"])

# Michigan
MI_EX = 5800
mi_agi = v["11"]
mi_taxable = mi_agi - 2 * MI_EX
mi_tax = r(mi_taxable * .0425)
mi_wh = r(w2_l["state"][0]["tax"] + UC_MIWH)
mi_due = mi_tax - mi_wh

sch_c_tbl = [["Schedule C - Sofia Martinez Design (sole proprietor) - code 541430, cash method", "Amount"],
             ["Line F accounting method: Cash.  Line G materially participated: Yes", ""],
             ["Line H: STARTED OR ACQUIRED this business during 2025 - X (started 04/01/2025)", ""],
             ["Line I: Did you make any payments in 2025 that would require you to file Form(s) 1099? - No", ""],
             [f"1 Gross receipts: 1099-NEC Kerrytown {NEC_A:,.0f} + Stripe 1099-K {STRIPE_GROSS:,.0f} (includes Arbor Brewing "
              f"card payments {NEC_B:,.0f} also on its 1099-NEC - counted once) + Venmo (no form) {VENMO:,.0f}", r(gross_receipts)],
             ["8 Advertising (website, Dribbble, business cards)", r(276 + 96 + 118)],
             ["10 Commissions and fees (Stripe processing fees per balance history)", r(STRIPE_FEES)],
             ["18 Office expense / 22 Supplies (fonts, stock images)", 385],
             ["22 Supplies - laptop $1,899 + tablet $379 (de minimis safe harbor election, Reg. 1.263(a)-1(f))", r(1899 + 379)],
             ["24b Deductible meals (50% of $164)", 82],
             ["25 Utilities - cell phone 50% business", 315],
             ["27a Other - software subscriptions (Adobe CC, Figma)", r(539.91 + 135)],
             ["28 Total expenses before home office", r(exp_total)],
             ["29 Tentative profit", r(tentative)],
             ["30 Business use of home (Form 8829)", OFFICE_8829],
             ["31 Net profit (to Schedule 1 line 3 and Schedule SE)", SCH_C],
             ["Not deducted: Spotify $99 (personal), wedding invitations $640 (personal - own wedding)", ""]]
f8829 = [["Form 8829 - 611 S Division Apt 4B (rented)", "Amount"],
         ["1 Area used regularly and exclusively for business (2nd bedroom)", "150 sq ft"],
         ["2 Total area of home", "900 sq ft"], ["7 Business percentage", f"{BUS_PCT*100:.2f}%"],
         ["Months used for business: April - December 2025 (only expenses for those months included)", "9"],
         ["18 Rent (9 x $1,950) - indirect", r(rent)], ["20 Utilities DTE + AT&T Fiber - indirect", r(dte + net)],
         ["17 Insurance (renters) - indirect", r(ins)], ["Total indirect expenses", r(indirect)],
         ["Allowable (x 16.67%) - within gross income limitation", OFFICE_8829],
         ["Comparison: simplified method $5 x average monthly sq ft (150 x 9 / 12 = 112.5) - NOT elected", SIMPLIFIED]]
se_tbl = [["Schedule SE - Sofia", "Amount"], ["Net profit", SCH_C], ["x 92.35%", se["net_earnings"]],
          ["SE tax (15.3%)", se["se_tax"]], ["Deductible half (Sch 1 line 15)", se["half"]],
          ["QBI (net profit - 1/2 SE tax)", r(QBI)]]
sim_tbl = [["MFJ vs MFS simulation (projection tool)", "MFJ", "MFS - Sofia", "MFS - Liam", "MFS combined"],
           ["AGI", v["11"], Rs.values["11"], Rl.values["11"], Rs.values["11"] + Rl.values["11"]],
           ["Taxable income", v["15"], Rs.values["15"], Rl.values["15"], Rs.values["15"] + Rl.values["15"]],
           ["Income tax (line 16)", v["16"], Rs.values["16"], Rl.values["16"], Rs.values["16"] + Rl.values["16"]],
           ["SE tax", v["23"], Rs.values["23"], Rl.values["23"], Rs.values["23"] + Rl.values["23"]],
           ["Total tax (line 24)", v["24"], Rs.values["24"], Rl.values["24"], mfs_tax],
           ["Refund / (balance due)", mfj_net, Rs.values["refund"] - Rs.values["balance_due"],
            Rl.values["refund"] - Rl.values["balance_due"], mfs_net],
           [f"MFJ saves {fmt(savings)} federal. Michigan is a flat 4.25% with the same exemptions either way (no MI difference).", "", "", "", ""]]
p2210 = [["Form 2210 check (no estimates; first-year business)", "Amount"],
         ["2025 total tax (MFJ)", v["24"]], ["90% of 2025 tax", req_90],
         ["2024 tax - Liam (Single, filed by us)", TAX_2024["Liam"]], ["2024 tax - Sofia (Single, TurboTax)", TAX_2024["Sofia"]],
         ["Prior-year safe harbor: MFJ in 2025 but separate in 2024 -> SUM of both 2024 taxes (combined 2024 AGI under $150,000 -> 100%)", PY_SAFE],
         ["Required annual payment (smaller)", min(req_90, PY_SAFE)],
         ["Withholding (W-2 + 1099-G), treated as paid evenly", wh_total],
         ["Penalty", 0]]
C.write_return(R, [
    ("Taxpayer / Spouse", "Sofia E. Martinez (XXX-XX-3057) / Liam P. Hart (XXX-XX-8124)"),
    ("Name control", "MART - primary taxpayer's last name exactly as on Social Security card (SSA record not yet updated)"),
    ("Address", ", ".join(ADDR)),
    ("Filing status", "Married filing jointly (married 12/20/2025 - married for all of 2025)"),
    ("Dependents", "None"),
    ("Digital assets question", "No"),
    ("Forms included", "1040, Schedules 1, 2, B, C, SE, Form 8829, Form 8995; MI-1040"),
    ("State / local", "Michigan MI-1040 (resident). Ann Arbor - no city income tax."),
    ("Filing method", "E-file. 1st transmission 04/08/2026 rejected IND-031-04 (name control HART); corrected to Martinez, "
                      "retransmitted 04/09/2026, accepted 04/10/2026. Balance due paid by direct debit 04/15/2026."),
], state_summary=[{"title": "Michigan MI-1040 (resident, joint) - summary", "lines": [
        ("10", "Federal AGI (includes unemployment compensation - taxable in Michigan)", mi_agi),
        ("12-14", "Additions / subtractions (none)", 0),
        ("15", "Income subject to tax", mi_agi),
        ("9 / 16", "Exemption allowance: 2 x $5,800", 2 * MI_EX),
        ("17", "Taxable income", mi_taxable),
        ("18", "Tax at 4.25%", mi_tax),
        ("30", "Michigan tax withheld (Liam W-2 $3,800 + UIA 1099-G $232)", mi_wh),
        ("35", "Tax due", mi_due)],
        "note": "Balance due under $500 -> no Michigan estimated payments were required (no MI-2210 penalty). Ann Arbor does not "
                "levy a city income tax (unlike Detroit, Grand Rapids, Lansing)."}],
    attachments=[("Schedule C - Profit or Loss From Business (Sofia)", sch_c_tbl),
                 ("Form 8829 - Expenses for Business Use of Your Home", f8829),
                 ("Schedule SE / QBI support", se_tbl),
                 ("Filing status simulation - MFJ vs MFS", sim_tbl),
                 ("Form 2210 - underpayment penalty check", p2210)])

gotchas = [
    gotcha("EVG1014-G1", "Filing Status (married by year end)", "Married 12/20/2025 - co-worker says file Single",
           "File two Single returns because they were married for only 11 days.",
           "Marital status is determined on 12/31: married for the entire year -> MFJ or MFS only.",
           "Single returns would be invalid", ["Filing status"], "easy"),
    gotcha("EVG1014-G2", "Projections (simulations - MFJ vs MFS)", "Client asks for the cheaper of joint / separate",
           "Pick MFS because 'we only just got married', or pick MFJ without modeling.",
           f"Model both: MFJ total tax {fmt(v['24'])} vs MFS combined {fmt(mfs_tax)} -> MFJ saves {fmt(savings)}. MI flat tax - no difference. "
           "Document the simulation and reconcile to the compliance return.", f"{fmt(savings)} federal", ["24"], "medium"),
    gotcha("EVG1014-G3", "E-File Rejects (name control / SSN mismatch)", "Organizer signed 'Sofia Hart'; SSA still shows Martinez",
           "Enter the primary taxpayer as 'Sofia Hart' per the organizer / client email.",
           "Use the name on the SSA record (Sofia E. Martinez, name control MART) until she files Form SS-5. Actual history: "
           "rejected IND-031-04 on 04/08; document reason, save corrected version, retransmit 04/09, monitor to acceptance 04/10.",
           "E-file reject; possible late filing if not monitored", ["Header"], "medium"),
    gotcha("EVG1014-G4", "Scan - duplicate documents / Schedule C records", "1099-K (Stripe) includes the $9,500 on the Arbor Brewing 1099-NEC",
           "Gross receipts = 18,000 + 9,500 + 12,400 = $39,900 (all information returns added).",
           f"Reconcile Stripe balance history: $9,500 of the $12,400 is Arbor Brewing card payments. Unique receipts = "
           f"{fmt(NEC_A)} + {fmt(STRIPE_GROSS)} + Venmo {fmt(VENMO)} (no form - still income) = {fmt(GROSS)}. Keep the reconciliation in the WP.",
           "Sch C overstated $9,500 (~$2,900 income + SE tax) or Venmo omitted", ["Sch C 1", "Sch 1 3"], "medium"),
    gotcha("EVG1014-G5", "Schedule C - Home Office Deduction (8829 vs simplified)", "Part-year home office in a rented apartment",
           "Use simplified $5 x 150 = $750, or 8829 with 12 months of rent.",
           f"8829 actual: 16.67% x Apr-Dec rent/utilities/insurance {fmt(indirect)} = {fmt(OFFICE_8829)} vs simplified "
           f"{fmt(SIMPLIFIED)} (average monthly footage 112.5) -> 8829.", f"Deduction {fmt(OFFICE_8829)}", ["Sch C 30"], "medium"),
    gotcha("EVG1014-G6", "Schedule C - checking the top-of-form boxes / De-Minimis Safe Harbor / personal expenses",
           "First-year business boxes and personal items in client books",
           "Leave line H blank; depreciate the laptop over 5 years; deduct the wedding invitations and Spotify from the spreadsheet.",
           "Check line H (started 2025); line I 'No' (no payments requiring 1099s). Attach the de minimis safe harbor election "
           "statement (laptop $1,899, tablet $379 <= $2,500). Remove personal items ($739).", "Sch C", ["Sch C H", "Sch C 22"], "easy"),
    gotcha("EVG1014-G7", "General Return Prep Notes / Form 2210", "No estimates on a first-year Schedule C; balance due > $1,000",
           f"Assess a 2210 penalty because withholding {fmt(wh_total)} < 90% of 2025 tax {fmt(req_90)}.",
           f"MFJ in 2025 but separate in 2024 -> prior-year safe harbor = Liam {fmt(TAX_2024['Liam'])} + Sofia {fmt(TAX_2024['Sofia'])} = "
           f"{fmt(PY_SAFE)} <= withholding -> no penalty. Advise 2026 estimates.", "Line 38 $0", ["38"], "hard"),
    gotcha("EVG1014-G8", "Scan - information returns", "Unemployment 1099-G with federal and MI withholding",
           "Omit unemployment (client thinks it was 'already taxed') or omit the $546 box 4 withholding.",
           "Sch 1 line 7 $5,460 (taxable federal and MI); $546 on line 25b; $232 MI withholding on MI-1040.", "Line 8 / 25b",
           ["8", "25b"], "easy"),
]
C.write_answer_key(R, {"residence": "MI - Ann Arbor (MI-1040; no city tax)", "complexity": "Joint + first-year Schedule C"},
                   gotchas,
                   state=[{"jurisdiction": "Michigan", "form": "MI-1040", "agi": mi_agi, "exemptions": 2 * MI_EX,
                           "taxable_income": mi_taxable, "tax": mi_tax, "withholding": mi_wh, "balance_due": mi_due}],
                   filings=[{"form": "Form 1040 (federal)", "method": "e-file", "due": "2026-04-15",
                             "history": "rejected 2026-04-08 IND-031-04; retransmitted 2026-04-09; accepted 2026-04-10"},
                            {"form": "MI-1040", "method": "e-file", "due": "2026-04-15", "filed": "2026-04-09"}],
                   extra={"mfs_simulation": {"sofia_mfs_total_tax": Rs.values["24"], "liam_mfs_total_tax": Rl.values["24"],
                                             "mfs_combined": mfs_tax, "mfj": v["24"], "mfj_savings": savings},
                          "schedule_c": {"gross_receipts": r(GROSS), "expenses_before_8829": r(exp_total), "form_8829": OFFICE_8829,
                                         "simplified_alternative": SIMPLIFIED, "net_profit": SCH_C, "se_tax": se["se_tax"]},
                          "name_control": "MART"})

C.write_receipt_log("EVG1014-1040-2025", "R. Alvarez (staff)", "L. Chen (senior)", "S. Kennedy, CPA", "2026-02-16")
C.write_notes(f"""
# EVG1014 - Martinez, Sofia & Hart, Liam - 2025 Form 1040 - Preparer Notes

*Synthetic client - Project Evergreen. Return status: **signed off; e-filed 04/08/2026 (rejected IND-031-04), corrected and
retransmitted 04/09/2026, accepted 04/10/2026.***

## Return summary
| | |
|---|---|
| Filing status | Married filing jointly (primary: Sofia E. Martinez) |
| AGI (line 11) | {fmt(v['11'])} |
| Deduction | Standard {fmt(v['12e'])}; QBI {fmt(v['13a'])} |
| Taxable income | {fmt(v['15'])} |
| Income tax / SE tax | {fmt(v['16'])} / {fmt(v['23'])} |
| Total tax | {fmt(v['24'])} |
| Withholding (W-2 + 1099-G) | {fmt(v['25d'])} |
| **Balance due** | **{fmt(v['balance_due'])}** (paid by direct debit 04/15/2026; no 2210 penalty) |
| Michigan | tax {fmt(mi_tax)}, withheld {fmt(mi_wh)}, balance due {fmt(mi_due)} |

## What I did and why (plain English)
1. **Filing status.** They married 12/20/2025. You are married for the whole year if married on 12/31, so Single is not
   an option (answering the co-worker's advice in Liam's email). Per the Projections procedure I ran both MFJ and MFS:
   MFJ total tax {fmt(v['24'])} vs MFS {fmt(Rs.values['24'])} (Sofia) + {fmt(Rl.values['24'])} (Liam) = {fmt(mfs_tax)} ->
   **MFJ saves {fmt(savings)}**, mainly because Liam's income in the MFS 22% bracket drops to 12% on a joint return.
   Michigan is a flat 4.25% with the same exemptions either way, so no state difference. Clients chose MFJ.
2. **Names / e-file.** The organizer and Liam's email said "Sofia Hart", and the first transmission used Hart. It was
   rejected on 04/08 with **IND-031-04** (primary name control does not match SSA). Sofia confirmed she has not filed an
   SS-5, so the return must use **Sofia E. Martinez / name control MART**. Per the E-File Rejects procedure: reject reason
   documented, corrected version saved (v2), retransmitted 04/09, monitored - accepted 04/10. Told Sofia to file Form SS-5
   with SSA (and update her Stripe/1099 W-9s) before switching to Hart on the 2026 return.
3. **Schedule C - gross receipts.** Information returns total $18,000 + $9,500 + $12,400 = $39,900, but the Stripe balance
   history shows the Arbor Brewing invoices ($9,500) were paid by card through Stripe, so the same money is on both the
   Arbor 1099-NEC and the Stripe 1099-K. Unique receipts: Kerrytown {fmt(NEC_A)} + Stripe {fmt(STRIPE_GROSS)} + a Venmo
   logo job {fmt(VENMO)} with no form (still income) = **{fmt(GROSS)}**. Reconciliation (client spreadsheet vs 1099s vs
   Stripe CSV) is in WP 9-10. If the IRS AUR matches the 1099-NEC and 1099-K separately we have the support.
4. **Schedule C - expenses.** From her workbook: Stripe fees {fmt(STRIPE_FEES)} (from the CSV, not her estimate), software,
   fonts, website, cards, phone at 50%, meals at 50%. Laptop ($1,899) and tablet ($379) are each under $2,500 -> expensed
   under the **de minimis safe harbor election** (statement attached to the return). Removed personal items: Spotify ($99)
   and **their own wedding invitations** ($640). Top-of-form boxes: **line H checked (started 04/2025)**; line I "No"
   (she paid no contractors). Net profit {fmt(SCH_C)}.
5. **Home office.** Second bedroom, 150 of 900 sq ft (16.67%), used regularly and exclusively for design since April.
   Form 8829 with only April-December rent, DTE, internet and renters insurance ({fmt(indirect)}) -> **{fmt(OFFICE_8829)}**.
   Simplified method would be only {fmt(SIMPLIFIED)} ($5 x average monthly 112.5 sq ft for a 9-month year), so 8829 used.
   They rent - no depreciation/recapture issue.
6. **SE tax and QBI.** SE tax {fmt(se['se_tax'])} (half = {fmt(se['half'])} on Sch 1 line 15). QBI = net profit less
   half SE tax = {fmt(QBI)} -> 20% deduction {fmt(v['13a'])} (well below the $394,600 threshold). No SE health insurance
   (Sofia was on her father's plan and paid no premiums).
7. **Unemployment.** 1099-G $5,460 (Jan-Mar) on Schedule 1 line 7; $546 federal withholding on line 25b; $232 MI withholding.
   Taxable for Michigan too.
8. **Estimated tax penalty (Form 2210).** No estimates were made and the balance due exceeds $1,000. 90% of 2025 tax is
   {fmt(req_90)}, more than withholding {fmt(wh_total)}. But the prior-year safe harbor for a couple filing jointly in 2025
   who filed separately in 2024 uses the **sum of both 2024 taxes**: Liam {fmt(TAX_2024['Liam'])} + Sofia {fmt(TAX_2024['Sofia'])}
   = {fmt(PY_SAFE)} (combined 2024 AGI under $150,000, so 100%). Withholding exceeds that -> **no penalty**.
9. **Michigan.** MI-1040 joint: federal AGI {fmt(mi_agi)} less 2 x $5,800 exemptions = {fmt(mi_taxable)} x 4.25% = {fmt(mi_tax)};
   withholding {fmt(mi_wh)}; due {fmt(mi_due)} (under $500 - no MI estimate penalty). Ann Arbor has no city income tax, so
   no local return (checked per Local Filing Requirements).

## Open items / client communication
- Closed: name issue (04/09 email). Sofia to file SS-5; update PERM once SSA confirms.
- 2026 planning email sent 04/10: quarterly estimates for Sofia's business (suggested $1,300/quarter federal, $350 MI) or
  increase Liam's W-4 using the MFJ checkbox; keep a mileage log if she starts client visits; consider a Solo 401(k)/SEP.

## Hand-off to signer / routing
- [x] Return locked; Accountant's copy saved as *reviewed* (v2 after reject)
- [x] Federal 1040 - e-file; due 04/15/2026 - accepted 04/10/2026
- [x] MI-1040 - e-file; due 04/15/2026 - accepted
- [x] No FBAR; no local return (Ann Arbor)
- [x] eSign 8879 + MI-8453 - both spouses signed; contact Liam by email
- [x] Balance due: direct debit 04/15/2026 from UMCU ****5580
- Billing: joint + first-year Sch C $1,650 + home office 0.5 hr + MFJ/MFS simulation 0.5 hr. The e-file reject rework
  (0.3 hr) is an **external** reason (client-provided name) - chargeable per Updating Returns procedure; signer elected to W/O as goodwill.
""")
C.write_review_points(f"""
# Review Points - EVG1014 - 2025 - Form 1040

*Reviewer: L. Chen (blue). Preparer responses in red. Synthetic.*

1. **Schedule C line 1 / WP 4-6** - Draft gross receipts $39,900 = both 1099-NECs + the full Stripe 1099-K.
   - Tie the Stripe CSV to the 1099-K and the client spreadsheet. The Arbor Brewing $9,500 appears on both.
   - Also - client spreadsheet shows a $350 Venmo job with no 1099. Include it.
   - *Preparer: Corrected to {fmt(GROSS)}. Reconciliation tape added to WP 10.*
2. **Schedule C top boxes** - Line H (started business in 2025) not checked; line I left blank.
   - *Preparer: H checked; I = No (no contractors paid).*
3. **Schedule C expenses** - Draft depreciated the MacBook (5-yr MACRS) and included the wedding invitations and Spotify.
   - Use the de minimis safe harbor election (attach statement); remove personal items.
   - *Preparer: Done - $1,899 + $379 expensed; $739 personal removed.*
4. **Form 8829** - Draft used 12 months of rent. Business use started in April.
   - Only include April-December. Show the simplified-method comparison on the WP.
   - *Preparer: 8829 now {fmt(OFFICE_8829)} vs simplified {fmt(SIMPLIFIED)}.*
5. **Filing status** - Please run the MFS comparison in the projection tool (client asked) and save it to the WP.
   - *Preparer: MFJ {fmt(v['24'])} vs MFS {fmt(mfs_tax)}. Clients approved MFJ 04/03.*
6. **Form 2210** - Software computed a penalty: the 2024 tax field only rolled Liam's return from our system and the
   2210 input was left on "90% of current year".
   - For MFJ after separate 2024 returns, the prior-year amount is the sum of both 2024 taxes ({fmt(PY_SAFE)}). Enter
     Sofia's 2024 tax manually and confirm combined 2024 AGI < $150k.
   - *Preparer: Confirmed - Sofia's 2024 TurboTax summary in PBC #12. No penalty.*
7. **Post-transmission (signer)** - IRS reject IND-031-04. Primary name must match SSA (Martinez). Nobody caught that the
   organizer name differs from the 1099s/SS card. Add to the Filing Status review checklist for newlyweds.
   - *Preparer: Corrected, v2 saved, retransmitted 04/09, accepted 04/10. PERM updated with name-control note.*
""")
print("EVG1014 done", R.summary()["24"], v["refund"], v["balance_due"], "MFS", mfs_tax, "sch c", SCH_C, OFFICE_8829, SIMPLIFIED)
