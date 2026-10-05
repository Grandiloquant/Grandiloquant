"""EVG1005 - Jennifer Walsh (Single, Michigan: Detroit -> Royal Oak 07/01/2025). Two W-2 jobs (Detroit employer, then a
Southfield employer that kept withholding Detroit tax after the move); excess social security credit; Additional Medicare Tax
not withheld (Form 8959); backdoor Roth with a forgotten rollover IRA -> pro-rata rule (Form 8606); MI-1040; City of Detroit
part-year resident return (new local filing requirement triggered by the move)."""
from common import ClientBuild, gotcha, fmt
from docs import statement, write_text, write_csv
import forms as F
from tax2025 import Return1040, r, SS_WAGE_BASE

C = ClientBuild("EVG1005", "Walsh", "Jennifer Walsh")
OLD_ADDR = ("1440 Brush St, Apt 1207", "Detroit, MI 48226")
ADDR = ("418 W Fourth St", "Royal Oak, MI 48067")
T = {"name": "Jennifer L. Walsh", "ssn": "XXX-XX-7719", "dob": "1987-10-05"}
REC_T = [T["name"], *ADDR, f"TIN: {T['ssn']}"]

# ------------------------------------------------------------------ PERM
C.write_profile(f"""
# EVG1005 - Walsh, Jennifer  (PERM)

*Synthetic client - Project Evergreen training data.*

| Item | Detail |
|---|---|
| Client ID | EVG1005 |
| Taxpayer | Jennifer L. Walsh, DOB 10/05/1987, SSN XXX-XX-7719 - data science manager |
| Filing status | Single, no dependents |
| Residency history | Detroit ({OLD_ADDR[0]}) 2019 - 06/30/2025; **Royal Oak ({ADDR[0]}) from 07/01/2025**. Michigan full-year resident. |
| Local tax history | City of Detroit resident return (D-1040 resident) filed through 2024 |
| Retirement accounts | Fidelity **Rollover IRA** ****5530 (2019 rollover of former employer 401(k) - Quicken Loans-era job); Fidelity Roth IRA ****5531 (opened 2025); Fidelity traditional IRA ****5532 (backdoor contribution account, opened 2025) |
| Contact | Email jen.walsh@example.com, (313) 555-0175; eSign OK |
| Engagement | Client since 2022. Quote $1,400 (W-2, MI + city). |
| Payment info | Voided check on file (Chase checking ending 6621) |

**PY WP notes:** Rollover IRA 12/31/2024 value $56,880 (Fidelity). No Form 8606 on file - no nondeductible contributions through 2024.
Jennifer mentioned her financial planner suggested a "backdoor Roth" for 2025 - flagged: the rollover IRA balance will make most
of any conversion taxable (pro-rata) unless it is rolled into an employer 401(k) before 12/31 of the conversion year.
""")
F.prior_year_summary(C.perm_file("2024_Form_1040_Return_Summary.pdf", "Prior-year return summary"), "Jennifer Walsh", "EVG1005",
    "Single", [
        ["1a", "W-2 wages - Motor City Analytics LLC", 171400], ["2b", "Taxable interest - Ally Bank", 162],
        ["11", "AGI", 171562], ["12", "Standard deduction", 14600], ["15", "Taxable income", 156962],
        ["24", "Total tax", 31187], ["25a", "Withholding", 32050], ["35a", "Refund", 863],
        ["MI-1040", "MI tax 4.25% on 171,562 - 5,600 exemption; MI refund $118", 7053],
        ["Detroit D-1040(R)", "Resident: wages (box 18) 194,400 + interest 162 - 600 exemption x 2.4%; refund $22", 4655]],
    carryovers=[["Form 8606 basis (traditional IRAs)", 0], ["Rollover IRA (Fidelity ****5530) 12/31/2024 value", 56880]],
    notes="Standard deduction. 401(k) maxed. Detroit taxes 401(k) deferrals (box 18 = Medicare wages). No estimated payments.")

# ------------------------------------------------------------------ amounts
EMP1 = {"name": "Motor City Analytics LLC", "addr1": "1001 Woodward Ave, Suite 1400", "addr2": "Detroit, MI 48226",
        "ein": "00-6630918"}
EMP2 = {"name": "Lakeshore Robotics, Inc.", "addr1": "26555 Evergreen Rd, Suite 800", "addr2": "Southfield, MI 48076",
        "ein": "00-2295047"}
EE_OLD = {"name": T["name"], "addr1": OLD_ADDR[0], "addr2": OLD_ADDR[1], "ssn": T["ssn"]}
EE = {"name": T["name"], "addr1": ADDR[0], "addr2": ADDR[1], "ssn": T["ssn"]}

g1, k1 = 128400.00, 12000.00           # Jan 1 - Jun 13: salary $86,000 + 2024 bonus paid 03/14 $34,200 + PTO payout $8,200
g2_first = round(180000 / 260 * 6, 2)  # 06/23-06/30 prorated salary, paid 06/30 (while still a Detroit resident)
g2 = round(g2_first + 12 * 7500.00, 2) # + 12 semi-monthly paychecks 07/15-12/31
k2 = 11500.00
det2_wages = round(g2_first + 5 * 7500.00, 2)     # Detroit withheld through 09/15 payroll (HR address not updated)
w2_1 = {"1": g1 - k1, "2": 24180.00, "3": g1, "4": round(g1 * .062, 2), "5": g1, "6": round(g1 * .0145, 2),
        "12": [("D", k1), ("DD", 7340.00)], "13": ["Retirement plan: X"],
        "state": [{"state": "MI", "id": "00-6630918", "wages": g1 - k1, "tax": 4826.30}],
        "local": [{"wages": g1, "tax": round(g1 * .024, 2), "name": "DETROIT (R)"}], "control": "MCA-2025-0417"}
w2_2 = {"1": round(g2 - k2, 2), "2": 15400.00, "3": g2, "4": round(g2 * .062, 2), "5": g2, "6": round(g2 * .0145, 2),
        "12": [("D", k2), ("DD", 4120.00)], "13": ["Retirement plan: X"],
        "state": [{"state": "MI", "id": "00-2295047", "wages": round(g2 - k2, 2), "tax": 3425.00}],
        "local": [{"wages": det2_wages, "tax": round(det2_wages * .024, 2), "name": "DETROIT"}], "control": "LRI-W2-2025-1188"}
assert k1 + k2 <= 23500
conv = 7012.00
contrib = 7000.00
rollover_fmv = 63412.77
ally_int, ally_int_res = 186.40, 91.20      # full year / Jan-Jun (resident period)

# ------------------------------------------------------------------ PBC documents
F.organizer(C.pbc_file("01_2025_Organizer_Walsh.pdf", "Client organizer", "2026-02-11"), "Jennifer Walsh", "EVG1005",
    general=[("Did your marital status change during 2025?", "No", ""),
             ("Did you move during 2025?", "Yes", "Detroit -> Royal Oak on 7/1"),
             ("Did you change jobs?", "Yes", "left Motor City Analytics 6/13, started Lakeshore Robotics 6/23"),
             ("Did you make IRA contributions or conversions?", "Yes", "backdoor Roth - $7,000 contributed and converted in Feb"),
             ("Do you have any other traditional, SEP, SIMPLE or rollover IRAs?", "No", ""),
             ("Did you make estimated tax payments?", "No", ""),
             ("Do you live or work in a city with an income tax?", "Yes", "Detroit until June"),
             ("Did you receive, sell, exchange digital assets?", "No", "")],
    dependents=[],
    income_rows=[["Wages", "Motor City Analytics LLC", 171400, "see W-2"],
                 ["Wages", "Lakeshore Robotics, Inc.", "", "see W-2"],
                 ["Interest", "Ally Bank", 162, "186"],
                 ["IRA / Roth conversion", "Fidelity", "", "7,012 (should be nontaxable - backdoor)"]],
    deductions_rows=[["IRA contribution (nondeductible)", "Fidelity traditional IRA", "", "7,000"],
                     ["Moving expenses", "Two Men and a Truck", "", "1,850"]],
    signature_date="02/09/2026")
F.w2(C.pbc_file("02_W-2_Motor_City_Analytics.pdf", "Form W-2", "2026-02-11"), EMP1, EE_OLD, w2_1)
F.w2(C.pbc_file("03_W-2_Lakeshore_Robotics.pdf", "Form W-2", "2026-02-11"), EMP2, EE, w2_2)
F.f1099_r(C.pbc_file("04_1099-R_Fidelity_Traditional_IRA_5532.pdf", "Form 1099-R", "2026-02-11"),
          ["Fidelity Management Trust Company, Custodian", "PO Box 770001", "Cincinnati, OH 45277", "TIN: 00-2227113"],
          REC_T, {"1": conv, "2a": conv, "2b": "Taxable amount not determined: X   Total distribution: X", "4": 0,
                  "7": "2   IRA/SEP/SIMPLE: X", "13": "02/18/2025"}, account="****5532",
          notes=["Distribution: conversion to Fidelity Roth IRA ****5531 on 02/18/2025."])
F.f1099_int(C.pbc_file("05_1099-INT_Ally_Bank.pdf", "Form 1099-INT", "2026-02-11"),
            ["Ally Bank", "PO Box 951", "Horsham, PA 19044", "TIN: 00-0000002"], REC_T, {"1": ally_int}, account="****8840")
statement(C.pbc_file("06_Fidelity_2025_Year-End_Investment_Report.pdf", "Brokerage/IRA year-end statement", "2026-02-11"),
    "Fidelity Investments - 2025 Year-End Investment Report - Jennifer L. Walsh", [
        {"heading": "Account summary (values as of 12/31/2025)",
         "table": [["Account", "Type", "Value 12/31/2024", "Value 12/31/2025"],
                   ["****5530", "Rollover IRA", 56880.14, rollover_fmv],
                   ["****5531", "Roth IRA", 0.00, 7688.12],
                   ["****5532", "Traditional IRA", 0.00, 0.00],
                   ["Total", "", 56880.14, rollover_fmv + 7688.12]], "total_row": True},
        {"heading": "Traditional IRA ****5532 activity", "table": [["Date", "Activity", "Amount"],
                   ["02/03/2025", "Contribution - 2025 tax year", contrib], ["02/10/2025", "Interest (core position)", 12.00],
                   ["02/18/2025", "Conversion to Roth IRA ****5531", -conv]]},
        {"heading": "Rollover IRA ****5530 activity", "table": [["Item", "Amount"], ["Dividends / cap gains (reinvested)", 1822.40],
                                                                 ["Change in market value", 4710.23], ["Distributions", 0.00]],
         "note": "Income earned in IRAs is not reported on Form 1099."}])
statement(C.pbc_file("07_Form_5498_Fidelity_Rollover_IRA_5530.pdf", "Form 5498 (FMV statement)", "2026-02-11"),
    "Form 5498 IRA Contribution Information - 2025 (FMV statement furnished by 01/31/2026)", [
        {"table": [["Box", "Description", "Amount"], ["", "Trustee", "Fidelity Management Trust Company (TIN 00-2227113)"],
                   ["", "Participant", "Jennifer L. Walsh XXX-XX-7719 - account ****5530 (Rollover IRA)"],
                   ["1", "IRA contributions", 0.00], ["2", "Rollover contributions", 0.00],
                   ["3", "Roth IRA conversion amount", 0.00], ["5", "Fair market value of account (12/31/2025)", rollover_fmv],
                   ["7", "IRA / SEP / SIMPLE / Roth", "IRA"], ["11", "RMD for 2026", "No"]], "left_align_cols": [0, 1]}])
write_text(C.pbc_file("08_Email_Jennifer_2026-02-10.txt", "Client correspondence", "2026-02-10", "Email"),
"""From: Jennifer Walsh <jen.walsh@example.com>
To: preparer@evergreentax.example
Date: Tue, 10 Feb 2026 20:14:51 -0500
Subject: Walsh 2025 - docs + questions

Hi - everything is uploaded. Notes:
1) Backdoor Roth: my planner had me put $7,000 into a new traditional IRA on 2/3 and convert it on 2/18. He said it is
   "tax-free because it's after-tax money". The 1099-R shows $7,012 - the $12 was interest before the conversion.
2) I moved to Royal Oak on July 1. Royal Oak doesn't have a city tax, right? Lakeshore kept taking Detroit tax out of my
   paychecks until I noticed in September and fixed my address with HR. Can I get that back?
3) Neither job took out the extra 0.9% Medicare - is that a problem?
4) Can I deduct my moving costs ($1,850)?
Thanks, Jen
""")
write_csv(C.pbc_file("09_Ally_interest_by_month_2025.csv", "Bank export (CSV)", "2026-02-18", "Email",
                     "requested by preparer"),
          ["Month", "Interest credited"],
          [["2025-01", 15.30], ["2025-02", 14.10], ["2025-03", 15.60], ["2025-04", 15.20], ["2025-05", 15.70], ["2025-06", 15.30],
           ["2025-07", 15.80], ["2025-08", 15.90], ["2025-09", 15.40], ["2025-10", 16.00], ["2025-11", 15.80], ["2025-12", 16.30],
           ["Total", ally_int]])
statement(C.pbc_file("10_Lakeshore_Robotics_offer_letter_and_HR_change.pdf", "Employment documents", "2026-02-18", "Email",
                     "requested by preparer"),
    "Lakeshore Robotics, Inc. - Offer Letter (excerpt) and HR Address Change Confirmation", [
        {"heading": "Offer letter - 05/28/2025 (excerpt)",
         "para": ["Position: Senior Manager, Data Science. Start date: Monday, June 23, 2025. Base salary: $180,000 per year, paid "
                  "semi-monthly on the 15th and last business day. Work location: Southfield headquarters (hybrid - remote days "
                  "from home). Your first paycheck on 06/30/2025 will include prorated salary for 06/23-06/30 ($4,153.85).",
                  "Lakeshore Robotics maintains a sales office in Detroit and is registered as a City of Detroit withholding agent."]},
        {"heading": "Workday - personal information change (confirmation)",
         "table": [["Field", "Old", "New", "Effective"], ["Home address", "1440 Brush St Apt 1207, Detroit MI 48226",
                                                         "418 W Fourth St, Royal Oak MI 48067", "Entered 09/16/2025"],
                   ["Local tax (resident)", "DETROIT 2.4%", "None", "Payroll 09/30/2025"]], "left_align_cols": [0, 1, 2, 3]},
        {"para": "Employee note: 'I never worked in the Detroit office - Southfield or home in Royal Oak only after I moved.'"}])
statement(C.pbc_file("11_Leases_Detroit_move-out_and_Royal_Oak.pdf", "Residency documents", "2026-02-18", "Email",
                     "requested by preparer"),
    "Residency Support - Lease Termination (Detroit) and New Lease (Royal Oak)", [
        {"table": [["Document", "Detail"],
                   ["The Brush Park Lofts - notice of lease end", "Tenant J. Walsh, 1440 Brush St #1207, Detroit; move-out 06/30/2025; keys returned 06/30"],
                   ["Royal Oak lease", "418 W Fourth St, Royal Oak MI 48067; term 07/01/2025 - 06/30/2026; tenant J. Walsh"],
                   ["Michigan driver's license", "Address updated to Royal Oak 07/14/2025"]], "left_align_cols": [0, 1]}])
F.w2(C.pbc_file("12_W-2_Motor_City_Analytics_ADP_reprint.pdf", "Form W-2", "2026-02-18", note="client uploaded again"),
     EMP1, EE_OLD, w2_1, watermark="REPRINT")
statement(C.pbc_file("13_Two_Men_and_a_Truck_invoice.pdf", "Receipt", "2026-02-11"), "Two Men and a Truck - Detroit Metro - Invoice #DM-55182", [
    {"table": [["Date", "Service", "Amount"], ["06/30/2025", "Local move Detroit -> Royal Oak, 3 movers, 5 hours", 1850.00]]}])

# ------------------------------------------------------------------ Form 8606 (Part I + Part II)
l1, l2 = contrib, 0
l3 = l1 + l2
l5 = l3
l6 = r(rollover_fmv)                # all traditional/SEP/SIMPLE IRAs at 12/31/2025 (conversion account is $0)
l7 = 0
l8 = conv
l9 = l6 + l7 + l8
l10 = round(l5 / l9, 5)
l11 = r(l8 * l10)
l12 = r(l7 * l10)
l13 = l11 + l12
l14 = l3 - l13
l16, l17 = conv, l11
l18 = r(l16 - l17)

wages = [{"who": "T", "box1": w2_1["1"], "box2": w2_1["2"], "box3": w2_1["3"], "box4": w2_1["4"], "box5": w2_1["5"],
          "box6": w2_1["6"]},
         {"who": "T", "box1": w2_2["1"], "box2": w2_2["2"], "box3": w2_2["3"], "box4": w2_2["4"], "box5": w2_2["5"],
          "box6": w2_2["6"]}]
facts = {
    "status": "S", "taxpayer": {"age65": False},
    "w2": wages,
    "interest": [{"payer": "Ally Bank", "amount": ally_int}],
    "ira": [{"payer": "Fidelity traditional IRA ****5532 - Roth conversion (Form 8606)", "gross": conv, "taxable": l18}],
    "niit": {"nii": ally_int},     # interest only; the Roth conversion is not NII (but raises MAGI)
}
R = Return1040(facts).compute()
v = R.values
# naive draft: conversion treated as nontaxable (organizer "no other IRAs")
naive = Return1040(dict(facts, ira=[{"payer": "Fidelity", "gross": conv, "taxable": conv - contrib}])).compute()

# excess SS check
ss_withheld = w2_1["4"] + w2_2["4"]
excess_ss = r(ss_withheld - SS_WAGE_BASE * .062)
assert excess_ss == v["excess_ss"]
med_wages = w2_1["5"] + w2_2["5"]

# ------------------------------------------------------------------ Michigan MI-1040
mi_agi = v["11"]
mi_exempt = 5800
mi_ti = mi_agi - mi_exempt
mi_tax = r(mi_ti * .0425)
mi_wh = r(w2_1["state"][0]["tax"] + w2_2["state"][0]["tax"])
mi_bal = mi_tax - mi_wh
# ------------------------------------------------------------------ City of Detroit part-year resident return
det_res_wages1 = g1                 # box 18 (Detroit taxes 401(k) deferrals - Medicare wages)
det_res_wages2 = g2_first           # Lakeshore paycheck 06/30 (earned 06/23-06/30 while a resident; taxable wherever earned)
det_res_int = ally_int_res
det_nonres_wages2 = det2_wages - g2_first   # 07/01-09/15 wages with Detroit withholding: nonresident, earned outside Detroit
det_nonres_taxable = 0
det_res_total = r(det_res_wages1 + det_res_wages2 + det_res_int)
det_exempt_res = 600               # all taxable income is resident-period income -> full exemption allocated to resident portion
det_taxable = det_res_total - det_exempt_res
det_tax = r(det_taxable * .024)
det_wh = round(w2_1["local"][0]["tax"] + w2_2["local"][0]["tax"], 2)
det_refund = r(det_wh) - det_tax

state = [
    {"title": "Michigan MI-1040 (full-year resident) - summary", "lines": [
        ("AGI", "Federal AGI", mi_agi), ("Sch 1", "Additions / subtractions (Roth conversion taxable in MI; no retirement "
                                                "subtraction for a conversion; no U.S. obligation interest)", 0),
        ("-", "Income subject to tax", mi_agi), ("-", "Exemption allowance (1 x $5,800)", mi_exempt),
        ("-", "Taxable income", mi_ti), ("-", "Tax at 4.25%", mi_tax),
        ("-", "City income tax paid (Detroit) - no MI credit or deduction", 0),
        ("-", "Michigan income tax withheld (W-2 box 17: 4,826.30 + 3,425.00)", mi_wh),
        ("-", "TAX DUE" if mi_bal > 0 else "REFUND", abs(mi_bal))],
     "note": "MI-1040 e-filed with the federal return. Balance due paid by ACH debit 04/15/2026."},
    {"title": "City of Detroit Income Tax - PART-YEAR RESIDENT return (resident 01/01-06/30/2025) - summary", "lines": [
        ("R-1", "Resident period: Motor City Analytics wages (W-2 box 18 = Medicare wages; Detroit taxes 401(k) deferrals)", r(det_res_wages1)),
        ("R-2", "Resident period: Lakeshore Robotics wages earned & paid 06/23-06/30 (resident - taxable although earned in Southfield)", r(det_res_wages2)),
        ("R-3", "Resident period: interest (Ally, Jan-Jun per bank export)", r(det_res_int)),
        ("R-4", "Resident period: Roth conversion 02/2025 - IRA distribution, excluded from city income (see assumption)", 0),
        ("NR-1", "Nonresident period 07/01-12/31: Lakeshore wages 07/01-09/15 shown in box 18 but earned outside Detroit - not taxable", 0),
        ("NR-2", f"(memo: Lakeshore Detroit box 18 wages {det2_wages:,.2f} less resident-period {g2_first:,.2f} = {det_nonres_wages2:,.2f} excluded)", 0),
        ("-", "Total income subject to Detroit tax", det_res_total),
        ("-", "Exemption $600 (apportioned to resident income - no Detroit-taxable nonresident income)", det_exempt_res),
        ("-", "Taxable income (resident rate 2.4%)", det_taxable), ("-", "Detroit income tax", det_tax),
        ("-", "Detroit tax withheld: Motor City Analytics 3,081.60 + Lakeshore Robotics " + f"{w2_2['local'][0]['tax']:,.2f}", r(det_wh)),
        ("-", "REFUND", det_refund)],
     "note": "NEW for 2025: part-year resident return replaces the prior-year Detroit resident return (move to Royal Oak 07/01/2025). "
             "Royal Oak and Southfield do not levy a city income tax -> no other local return. Detroit return filed through MI Treasury "
             "e-file with the MI-1040. ASSUMPTION: the Roth conversion is treated as an excluded IRA distribution under the Uniform City "
             "Income Tax Ordinance (retirement/IRA distributions not city income); verify against current Detroit part-year instructions."}]

f8606 = [["Form 8606 - Nondeductible IRAs (2025)", "Amount"],
         ["1 Nondeductible contributions for 2025 (02/03/2025)", l1], ["2 Basis from prior years", l2], ["3 Total basis", l3],
         ["5", l5], ["6 Value of ALL traditional, SEP, SIMPLE IRAs at 12/31/2025 (Fidelity Rollover IRA ****5530)", l6],
         ["7 Distributions (other than conversions)", l7], ["8 Net amount converted to Roth in 2025", r(l8)], ["9 Add lines 6-8", r(l9)],
         ["10 Nontaxable ratio (line 5 / line 9)", f"{l10:.5f}"], ["11 Nontaxable portion of conversion", l11],
         ["13 Nontaxable portion - total", l13], ["14 Basis carried to 2026", l14],
         ["16 Amount converted", r(l16)], ["17 Basis in amount converted", l17], ["18 Taxable amount of conversion (to 1040 line 4b)", l18]]
local_ss = [["Excess social security (two employers)", "Amount"], ["Motor City Analytics box 4", w2_1["4"]],
            ["Lakeshore Robotics box 4", w2_2["4"]], ["Total SS withheld", round(ss_withheld, 2)],
            ["Maximum (6.2% x $176,100)", round(SS_WAGE_BASE * .062, 2)], ["Excess - Schedule 3 line 11", excess_ss]]
f8959 = [["Form 8959", "Amount"], ["Medicare wages (box 5) - both W-2s", round(med_wages, 2)], ["Threshold (Single)", 200000],
         ["Excess x 0.9%", R.forms_value("Form 8959", "7/13")], ["Additional Medicare withheld (box 6 over 1.45%)", 0]]
C.write_return(R, [
    ("Taxpayer", "Jennifer L. Walsh (XXX-XX-7719)"),
    ("Address", f"{', '.join(ADDR)} (from 07/01/2025; Detroit before)"),
    ("Filing status", "Single"),
    ("Digital assets question", "No"),
    ("Forms included", "1040; Sch 2, 3, B; Forms 8606, 8959, 8960"),
    ("State / local", "MI-1040 (full-year resident); City of Detroit part-year resident"),
    ("Filing method", "E-file federal + MI + Detroit (8879 / MI-8453 signed 03/18/2026)"),
], state_summary=state,
   attachments=[("Form 8606 (pro-rata rule)", f8606), ("Excess social security tax withheld", local_ss),
                ("Form 8959 - Additional Medicare Tax", f8959)])

gotchas = [
    gotcha("EVG1005-G1", "Return - Schedule 3 (excess social security)", "Two employers -> excess SS withheld",
           "Ignore the excess because each W-2 is correct on its own.",
           f"SS withheld {ss_withheld:,.2f} exceeds $10,918.20 (6.2% x $176,100) -> {fmt(excess_ss)} refundable credit on Schedule 3 line 11.",
           f"Refund understated {fmt(excess_ss)}", ["31", "Sch 3 line 11"], "easy"),
    gotcha("EVG1005-G2", "Return - Form 8959 / NIIT", "Additional Medicare Tax not withheld by either employer",
           "No Form 8959 because neither W-2 shows extra Medicare withholding (each employer paid < $200k).",
           f"Combined Medicare wages {med_wages:,.2f} - $200,000 = excess x 0.9% = {fmt(R.forms_value('Form 8959', '7/13'))} on Schedule 2. "
           f"Also NIIT on the Ally interest ({fmt(v.get('niit', 0))}) since MAGI > $200,000 (the conversion is not NII but raises MAGI).",
           "Schedule 2 lines 11-12", ["23"], "medium"),
    gotcha("EVG1005-G3", "Review - Client IRAs / General Return Prep Notes (organizer answers vs PY WP)",
           "Backdoor Roth with an existing rollover IRA - pro-rata rule",
           "Accept the organizer answer 'no other IRAs' and the planner's 'tax-free' comment: taxable conversion = $12 (earnings only).",
           f"The Fidelity year-end report / 5498 (and the PY WP) show a Rollover IRA worth {rollover_fmv:,.2f} at 12/31/2025. Form 8606 "
           f"line 6 includes it: nontaxable ratio {l10} -> taxable conversion {fmt(l18)} (line 4b), basis {fmt(l14)} carried forward.",
           f"4b {fmt(l18)} vs $12 - tax difference {fmt(v['24'] - naive.values['24'])}", ["4a", "4b", "Form 8606"], "hard"),
    gotcha("EVG1005-G4", "Return - Form 8606 basis tracking", "Remaining IRA basis must be carried forward",
           "Report 8606 Part II only and lose the unrecovered basis.",
           f"File Form 8606 Part I: 2026 basis {fmt(l14)}. Advise rolling the Rollover IRA into Lakeshore's 401(k) (if the plan accepts "
           "roll-ins) before 12/31/2026 to make future backdoor conversions clean.",
           "Future double taxation of $6,303", ["Form 8606 line 14"], "medium"),
    gotcha("EVG1005-G5", "SALT Implications - Local Filing Requirements", "Move Detroit -> Royal Oak creates a part-year Detroit return",
           "File a Detroit resident return as in the prior year (full-year wages at 2.4%), or file nothing because she now lives in Royal Oak.",
           "Change in residence mid-year -> City of Detroit PART-YEAR resident return: resident-period income at 2.4%; nonresident period "
           "only Detroit-source income (none). Royal Oak/Southfield have no city income tax.",
           f"Detroit refund {fmt(det_refund)}", ["Detroit return"], "medium"),
    gotcha("EVG1005-G6", "SALT Implications - Local Filing Requirements (W-2 box 18-20)", "Detroit withholding on job-2 wages after the move",
           "Treat Lakeshore's W-2 box 18 Detroit wages ($41,654) as Detroit-taxable, or ignore the Lakeshore box 19 withholding.",
           "Wages earned 07/01-09/15 as a nonresident working in Southfield/home are not Detroit income; the Detroit tax withheld on them "
           "is claimed as a payment on the part-year return and refunded.",
           "Detroit tax overstated ~$900 if included", ["Detroit return"], "hard"),
    gotcha("EVG1005-G7", "SALT Implications - Local Filing Requirements (part-year allocation)", "Job-2 wages earned while still a Detroit resident",
           "Exclude all Lakeshore wages from Detroit because the job is in Southfield.",
           f"The 06/23-06/30 paycheck ({g2_first:,.2f}, paid 06/30) was earned and received while a Detroit resident -> taxable at the "
           "resident rate regardless of work location.",
           "Detroit tax ~$100", ["Detroit return"], "hard"),
    gotcha("EVG1005-G8", "SALT Implications - Michigan", "MI-1040 treatment",
           "Subtract the Roth conversion (retirement subtraction) or deduct/credit the Detroit tax; or deduct moving expenses.",
           f"MI starts from federal AGI; conversion taxable in MI; exemption $5,800; tax 4.25% = {fmt(mi_tax)}; no credit for city tax. "
           "Moving expenses are not deductible (suspended except Armed Forces).",
           f"MI {'balance due' if mi_bal > 0 else 'refund'} {fmt(abs(mi_bal))}", ["MI-1040"], "medium"),
    gotcha("EVG1005-G9", "Scan - Duplicate documents", "ADP reprint of the job-1 W-2",
           "Autoflow both copies of the Motor City Analytics W-2 (wages, withholding and the excess-SS computation all doubled).",
           "Same control number / amounts - mark DUP; one W-2 per employer.", "Line 1a overstated $116,400", ["1a", "25a"], "easy"),
]
C.write_answer_key(R, {"residence": "MI - Detroit (01/01-06/30) -> Royal Oak (07/01-12/31)",
                       "complexity": "W-2 x2, 8606, MI + Detroit part-year"}, gotchas, state=state,
    filings=[{"form": "Form 1040 (federal)", "method": "e-file", "due": "2026-04-15", "filed": "2026-03-19"},
             {"form": "MI-1040", "method": "e-file", "due": "2026-04-15", "filed": "2026-03-19"},
             {"form": "City of Detroit part-year resident income tax return", "method": "e-file (MI Treasury)", "due": "2026-04-15",
              "filed": "2026-03-19"}],
    extra={"form_8606": {"line6": l6, "line10": l10, "line18_taxable": l18, "line14_basis_2026": l14},
           "assumptions": ["Detroit: Roth conversion excluded as an IRA distribution under the UCITO",
                           "Detroit: 401(k) deferrals taxable (box 18 = Medicare wages)",
                           "Detroit exemption fully allocated to resident-period income (no Detroit-taxable nonresident income)"]})
C.write_receipt_log("EVG1005-1040-2025", "A. Novak (staff)", "D. Whitfield (senior)", "S. Kennedy, CPA", "2026-02-11")

C.write_notes(f"""
# EVG1005 - Walsh, Jennifer - 2025 Form 1040 - Preparer Notes

*Synthetic client - Project Evergreen. Return status: **signed off; federal, MI-1040 and Detroit part-year return e-filed
03/19/2026 - all accepted.***

## Return summary
| | |
|---|---|
| Filing status | Single |
| Wages (2 W-2s) | {fmt(v['1a'])} |
| Interest | {fmt(v['2b'])} |
| Roth conversion 4a / 4b (Form 8606) | {fmt(v['4a'])} / {fmt(v['4b'])} |
| AGI | {fmt(v['11'])} |
| Standard deduction | {fmt(v['12e'])} |
| Taxable income | {fmt(v['15'])} |
| Income tax (line 16) | {fmt(v['16'])} |
| Additional Medicare (8959) + NIIT (8960) | {fmt(R.forms_value('Form 8959', '7/13'))} + {fmt(v.get('niit', 0))} |
| Total tax | {fmt(v['24'])} |
| Withholding + excess SS credit | {fmt(v['25d'])} + {fmt(v['excess_ss'])} |
| **Federal refund** | **{fmt(v['refund'])}** |
| MI-1040 | tax {fmt(mi_tax)} - withheld {fmt(mi_wh)} = **{'balance due ' + fmt(mi_bal) if mi_bal > 0 else 'refund ' + fmt(-mi_bal)}** |
| Detroit part-year | tax {fmt(det_tax)} - withheld {fmt(r(det_wh))} = **refund {fmt(det_refund)}** |

## What I did and why (plain English)
1. **Two W-2s.** Motor City Analytics (Detroit, 01/01-06/13) and Lakeshore Robotics (Southfield, from 06/23). The ADP "REPRINT"
   of the first W-2 is the same form (control MCA-2025-0417) - marked DUP. 401(k) deferrals total $23,500 - exactly the 2025 limit,
   no excess deferral.
2. **Excess social security.** Each employer withheld 6.2% up to its own wage count; combined SS wages {g1 + g2:,.2f} exceed the
   $176,100 wage base. SS withheld {ss_withheld:,.2f} - $10,918.20 = **{fmt(excess_ss)}** credited on Schedule 3 line 11.
3. **Additional Medicare Tax.** Neither employer paid her more than $200,000, so neither withheld the 0.9%. Combined Medicare wages
   {med_wages:,.2f} exceed the $200,000 single threshold -> Form 8959 {fmt(R.forms_value('Form 8959', '7/13'))}. (Answer to her question 3:
   not a problem, it is just owed with the return.) NIIT: MAGI > $200,000, so 3.8% applies to the lesser of NII ($186 interest)
   or the excess MAGI -> {fmt(v.get('niit', 0))}. The Roth conversion is not investment income.
4. **Backdoor Roth - pro-rata rule (the big one).** She contributed $7,000 nondeductible to a new traditional IRA (her MAGI is far
   above the deduction phase-out, so it's nondeductible) and converted $7,012 on 02/18. The organizer says she has no other IRAs,
   but the Fidelity year-end report, the rollover-IRA Form 5498 (FMV {rollover_fmv:,.2f}) and our PY notes all show a 2019
   **Rollover IRA**. All traditional IRAs are aggregated at 12/31/2025 (Form 8606 line 6), so only
   {l10:.5f} of the conversion is basis: nontaxable {fmt(l11)}, **taxable {fmt(l18)}** on line 4b. The remaining basis
   {fmt(l14)} carries to 2026 on Form 8606 line 14. No 10% penalty (conversion, code 2). The planner's "tax-free" comment would
   have been right only without the rollover IRA; the tax cost of the pro-rata rule this year is about
   {fmt(v['24'] - naive.values['24'])}.
5. **Tax.** Taxable income {fmt(v['15'])} - Tax Computation Worksheet (24% bracket) {fmt(v['16'])}.
6. **Moving expenses.** Not deductible (suspended for non-military) - federal or MI.
7. **Michigan.** Full-year MI resident (both addresses in MI) - MI-1040 only. AGI includes the taxable conversion; no MI retirement
   subtraction for a Roth conversion. Exemption $5,800. Tax 4.25% = {fmt(mi_tax)}; withheld {fmt(mi_wh)} ->
   {'balance due ' + fmt(mi_bal) if mi_bal > 0 else 'refund ' + fmt(-mi_bal)} (conversion had no withholding).
8. **City of Detroit - new part-year filing (procedure: Local Filing Requirements).** Last year she filed as a Detroit resident. The
   07/01 move to Royal Oak (no city income tax; Southfield has none either) means a **part-year resident** Detroit return for 2025:
   - Resident period (01/01-06/30): all income wherever earned at 2.4% - Motor City Analytics wages per box 18 ($128,400 - Detroit
     taxes 401(k) deferrals, so box 18 = Medicare wages), the Lakeshore paycheck for 06/23-06/30 ({g2_first:,.2f}, earned and paid while
     still a resident - not on any Detroit W-2 line as resident wages), and Jan-Jun Ally interest ($91.20 from the bank export).
     The February Roth conversion is excluded as an IRA distribution (**assumption** - UCITO excludes IRA/pension distributions; verify).
   - Nonresident period (07/01-12/31): only Detroit-source income is taxable (1.2% rate) - she never worked in Detroit after the move
     (Lakeshore offer letter / HR note), so $0. **Lakeshore kept withholding Detroit resident tax until her address change on 09/16**
     (box 18 {det2_wages:,.2f}, box 19 {w2_2['local'][0]['tax']:,.2f}) - those wages are not Detroit income; the withholding is refunded.
   - Exemption $600 (all of it applies to resident income). Taxable {fmt(det_taxable)} x 2.4% = {fmt(det_tax)}; withheld {fmt(r(det_wh))};
     **refund {fmt(det_refund)}**.
   - 2026: no Detroit return needed unless she has Detroit-source income.

## Open items / client communication
- Recommend rolling the Fidelity Rollover IRA into the Lakeshore 401(k) (plan accepts roll-ins - confirm with HR) before 12/31/2026
  so a 2026 backdoor conversion is almost fully nontaxable; alternatively skip the backdoor. Sent summary to Jennifer and her planner.
- W-4: add ~$150/paycheck extra federal withholding (Additional Medicare, conversion) - or accept small balance.
- Confirm Lakeshore stopped Detroit withholding (09/30 payroll) - yes per HR confirmation.

## Hand-off to signer / routing
- [x] Return locked; Accountant's copy saved as *reviewed*
- [x] Federal 1040 - e-file; refund direct deposit Chase ****6621
- [x] MI-1040 - e-file; balance due ACH debit 04/15/2026
- [x] **City of Detroit part-year resident return - e-file** (new routing line this year - update PERM residency: Royal Oak from 07/01/2025)
- [x] No FBAR; due dates 04/15/2026
- [x] eSign (8879 + MI-8453) by email
- Billing: $1,400 quote + 1.0 hr for 8606 pro-rata analysis and Detroit part-year allocation (in scope - bill); PERM static data
  update (address) not billable.
""")
C.write_review_points(f"""
# Review Points - EVG1005 - 2025 - Form 1040

*Reviewer: D. Whitfield (blue). Preparer responses in red. Synthetic.*

1. **WP 2 / WP 12 - W-2s** - The ADP reprint of the Motor City Analytics W-2 was autoflowed as a third W-2. Remove.
   - *Preparer: Marked DUP.*
2. **Form 8606** - First draft entered the 1099-R as a nontaxable backdoor Roth (taxable $12) with line 6 = $0 per the organizer.
   The Fidelity year-end report (WP 6) and PY WP show a Rollover IRA - 5498 FMV {rollover_fmv:,.2f} goes on line 6. Recompute.
   - *Preparer: Done. Taxable conversion {fmt(l18)}; basis carryforward {fmt(l14)}. Emailed Jennifer re: the organizer answer.*
3. **Schedule 3 line 11** - Excess SS credit missing (two employers). Please check CCH picked up both W-2s under the taxpayer.
   - *Preparer: Now {fmt(excess_ss)}.*
4. **Form 8959** - Medicare wages combined exceed $200k; employers withheld none. Add 8959. Also run 8960 for the interest.
   - *Preparer: 8959 {fmt(R.forms_value('Form 8959', '7/13'))}; NIIT {fmt(v.get('niit', 0))}.*
5. **Local - Detroit** - Draft carried the PY Detroit **resident** return forward and picked up both W-2 box 18 amounts at 2.4%.
   - She moved 07/01. Prepare a part-year resident return. Resident period only + Detroit-source nonresident income (none).
   - The Lakeshore box 18 wages after 07/01 are not Detroit income - claim the withholding as a payment.
   - Don't forget the 06/30 Lakeshore paycheck earned while she was a resident.
   - *Preparer: Part-year return prepared - tax {fmt(det_tax)}, refund {fmt(det_refund)}. Residency documents in WP 10-11.*
6. **MI-1040** - Draft took a retirement subtraction for the conversion. Not eligible - remove. Confirm moving expenses not deducted.
   - *Preparer: Removed; MI {'due' if mi_bal > 0 else 'refund'} {fmt(abs(mi_bal))}.*
7. FYI - document the Detroit IRA-distribution exclusion and 401(k) treatment assumptions in the WP.
""")
print("EVG1005 done", R.summary()["24"], v["refund"], "MI", mi_bal, "Detroit refund", det_refund, "8606 taxable", l18)
