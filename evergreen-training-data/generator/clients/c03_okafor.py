"""EVG1003 - Daniel "Danny" Okafor (Single, Nevada - Las Vegas). Casino bartender (W-2 with reported tips in box 1/7 and
ALLOCATED tips in box 8 not in box 1) + Uber rideshare driver (Schedule C, standard mileage). Handwritten daily tip log
(actual unreported tips < allocated -> Form 4137 on actual), handwritten mileage log that mixes in commuting miles,
OBBBA no-tax-on-tips (W-2 + 4137 + rideshare tips, $25,000 cap), QBI, SE tax, 2 of 4 estimates (Form 2210 check)."""
from common import ClientBuild, gotcha, fmt
from docs import statement, scanned_pages, write_text, write_csv
import forms as F
from tax2025 import Return1040, r, se_tax, MILEAGE_2025, SS_WAGE_BASE

C = ClientBuild("EVG1003", "Okafor", "Daniel Okafor")
ADDR = ("7720 W Oquendo Rd, Unit 2114", "Las Vegas, NV 89113")
T = {"name": "Daniel C. Okafor", "ssn": "XXX-XX-5082", "dob": "1991-11-02"}
REC_T = [T["name"], *ADDR, f"TIN: {T['ssn']}"]

# ------------------------------------------------------------------ PERM
C.write_profile(f"""
# EVG1003 - Okafor, Daniel "Danny"  (PERM)

*Synthetic client - Project Evergreen training data.*

| Item | Detail |
|---|---|
| Client ID | EVG1003 |
| Taxpayer | Daniel C. ("Danny") Okafor, DOB 11/02/1991, SSN XXX-XX-5082 |
| Occupations | Bartender - Ember Bar & Grill at Silver Sage Casino Resort (W-2, tipped); Uber rideshare driver since 09/2024 (Schedule C) |
| Filing status | Single, no dependents |
| Address | {ADDR[0]}, {ADDR[1]} (Clark County) - **Nevada: no individual income tax** |
| Contact | Text preferred (702) 555-0139; danny.okafor@example.com; eSign OK |
| Vehicle | 2021 Toyota Camry SE (owned, paid off 2024). First used for Uber 09/2024 - **standard mileage rate elected in first year (2024)** |
| Engagement | Client since 2025 (2024 return). Quote: W-2 + Schedule C tier $1,650 |
| Payment info | Voided check on file (Nevada State Bank ending 7765) |

**PY WP notes:** Casino W-2 reports tips from Form 4070 statements in boxes 1/7; employer shows ALLOCATED tips in box 8 (8% rule
shortfall allocation). Danny keeps a daily tip diary (started 2024 at our request - "adequate records"). Recommended 2025
quarterly estimates of $500 for the Uber income.
""")
F.prior_year_summary(C.perm_file("2024_Form_1040_Return_Summary.pdf", "Prior-year return summary"), "Daniel Okafor",
    "EVG1003", "Single", [
        ["1a", "W-2 wages incl. reported tips - Silver Sage Casino Resort", 36800],
        ["1c", "Unreported tips (Form 4137) - actual per tip diary (W-2 box 8 allocated $2,450 not used)", 1180],
        ["Sch 1-3", "Schedule C - Uber rideshare (09/2024-12/2024), standard mileage", 2150],
        ["10", "Adjustments - 1/2 SE tax", 152],
        ["11", "AGI", 39978], ["12", "Standard deduction", 14600], ["13", "QBI deduction", 400], ["15", "Taxable income", 24978],
        ["16", "Tax", 2765], ["Sch 2-4", "SE tax", 304], ["Sch 2-5", "Form 4137 SS/Medicare tax", 90],
        ["24", "Total tax", 3159], ["25a", "Federal withholding", 2700], ["37", "Balance due (paid 04/14/2025)", 459]],
    carryovers=[["Vehicle - standard mileage method elected 2024 (2021 Camry)", "Yes"],
                ["2024 total tax for 2025 Form 2210 safe harbor (100% - AGI < $150k)", 3159]],
    notes="Tip diary kept daily; 4137 on actual unreported cash tips. Uber: use gross 1099-K and deduct Uber fees; exclude commute "
          "to casino from mileage. 2025 estimates recommended $500/quarter (vouchers sent 04/2025).")

# ------------------------------------------------------------------ PBC documents
EMP = {"name": "Silver Sage Casino Resort LLC dba Ember Bar & Grill", "addr1": "3900 S Las Vegas Blvd",
       "addr2": "Las Vegas, NV 89109", "ein": "00-8812046"}
EE = {"name": T["name"], "addr1": ADDR[0], "addr2": ADDR[1], "ssn": T["ssn"]}
hourly = 19800.00
tips_reported = 24600.00
w2b = {"1": hourly + tips_reported, "2": 3150.00, "3": hourly, "4": round((hourly + tips_reported) * .062, 2),
       "5": hourly + tips_reported, "6": round((hourly + tips_reported) * .0145, 2), "7": tips_reported, "8": 2900.00,
       "14": [("TIPS RPTD (4070)", tips_reported), ("NV SUTA/UI", "n/a")], "13": [], "control": "SSC-25-08814"}

UNREPORTED = [110, 95, 160, 120, 140, 150, 175, 130, 115, 125, 130, 150]        # per tip diary, by month
unreported_tips = sum(UNREPORTED)
assert unreported_tips == 1600
MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
REPORTED_M = [1880, 1760, 2050, 1990, 2110, 2020, 2240, 2150, 1980, 2020, 2090, 2310]
assert sum(REPORTED_M) == tips_reported

# Uber
fares, booking, other_fees, tolls, uber_tips = 32040.00, 2410.00, 1070.00, 340.00, 2860.00
k_gross = fares + booking + other_fees + tolls + uber_tips
nec = 1150.00
service_fee = 7660.00
online_miles, trip_miles = 15145, 10210
commute_miles = 4180          # home <-> casino: 190 shifts x 22 mi round trip - NOT business
k_months = [2410.10, 2655.25, 3120.40, 3302.85, 3288.70, 3044.30, 3561.15, 3390.90, 3128.60, 3355.00, 3468.45, 3994.30]
assert abs(sum(k_months) - k_gross) < .01

F.organizer(C.pbc_file("01_2025_Organizer_Okafor.pdf", "Client organizer", "2026-02-09"), "Daniel Okafor", "EVG1003",
    general=[("Did your marital status change during 2025?", "No", ""),
             ("Did you receive tips not reported to your employer?", "Yes", "see tip log - I wrote down everything"),
             ("Did you have a business or side job (1099)?", "Yes", "Uber - same as last year"),
             ("Did you use your vehicle for business?", "Yes", "see mileage log"),
             ("Did you make estimated tax payments?", "Yes", "April + June, $500 each - couldn't do Sept/Jan"),
             ("Did you receive, sell, exchange digital assets?", "No", ""),
             ("Health insurance through employer (1095-C)?", "Yes", "Culinary union plan")],
    dependents=[],
    income_rows=[["Wages", "Silver Sage Casino Resort", 36800, "see W-2"],
                 ["Unreported tips (Form 4137)", "cash tips - tip diary", 1180, ""],
                 ["Uber - Schedule C gross", "Uber (1099-K / 1099-NEC)", 12940, "about 28,700 deposited"]],
    deductions_rows=[["Business miles", "Uber (log)", 4880, "19,325"],
                     ["Gas", "Camry", 1310, "3,900"], ["Car insurance", "GEICO", 2140, "2,280"],
                     ["Oil changes / maintenance", "", 160, "310"], ["Car washes / water & mints for riders", "", 110, "380"],
                     ["Phone", "T-Mobile $85/mo", "60% business", "same"], ["Dash cam", "", "", "149"],
                     ["Estimated tax payments", "IRS Direct Pay", "", "1,000"]],
    signature_date="02/07/2026")
F.w2(C.pbc_file("02_W-2_Silver_Sage_Casino.pdf", "Form W-2", "2026-02-09"), EMP, EE, w2b)
F.f1099_k(C.pbc_file("03_1099-K_Uber.pdf", "Form 1099-K", "2026-02-09"),
          ["Uber Technologies, Inc.", "1725 3rd Street", "San Francisco, CA 94158", "TIN: 00-2647441"], REC_T,
          {"1a": k_gross, "1b": k_gross, "2": "4121", "3": 1463, "months": k_months})
F.f1099_nec(C.pbc_file("04_1099-NEC_Uber.pdf", "Form 1099-NEC", "2026-02-09"),
            ["Uber Technologies, Inc.", "1725 3rd Street", "San Francisco, CA 94158", "TIN: 00-2647441"], REC_T, {"1": nec})
statement(C.pbc_file("05_Uber_2025_Tax_Summary.pdf", "Platform annual tax summary", "2026-02-09"),
    "Uber - 2025 Tax Summary for Daniel Okafor (driver)", [
        {"para": "This summary is provided for informational purposes. It is not tax advice. Your 1099-K reports the gross amount "
                 "of payments from riders; Uber fees and other expenses listed below are not deducted in the 1099-K amount."},
        {"heading": "Gross earnings", "table": [["Item", "Amount"], ["Gross fares", fares], ["Booking fees", booking],
                                                ["Airport fees / other rider fees", other_fees], ["Tolls (rider reimbursed)", tolls],
                                                ["Tips", uber_tips], ["Total 1099-K gross payments", k_gross]], "total_row": True},
        {"heading": "Other income (1099-NEC)", "table": [["Item", "Amount"], ["Incentives / Quest promotions", 1030.00],
                                                         ["Referral bonuses", 120.00], ["Total 1099-NEC", nec]], "total_row": True},
        {"heading": "Potential tax deductions - fees and charges", "table": [["Item", "Amount"], ["Uber service fee", service_fee],
                                                                              ["Booking fees (passed to Uber)", booking],
                                                                              ["Airport / city / other fees", other_fees],
                                                                              ["Total fees", service_fee + booking + other_fees]],
         "total_row": True},
        {"heading": "Mileage", "table": [["Item", "Miles"], ["Online miles (waiting, en route to pickup, on trip)", online_miles],
                                         ["On-trip miles (included above)", trip_miles]],
         "note": "Online miles do not include miles driven while offline (e.g., commuting to your first trip from home)."},
        {"heading": "Net payouts to your bank (for reference)",
         "table": [["Item", "Amount"], ["Total deposits 2025", k_gross + nec - service_fee - booking - other_fees]]}])
# handwritten tip diary (scanned)
jan_days = [("1/2", 92, 88, 4), ("1/3", 131, 120, 11), ("1/4", 164, 150, 14), ("1/8", 71, 71, 0), ("1/9", 88, 80, 8),
            ("1/10", 142, 130, 12), ("1/11", 158, 150, 8), ("1/15", 66, 60, 6), ("1/16", 95, 90, 5), ("1/17", 139, 125, 14),
            ("1/18", 170, 160, 10), ("1/22", 70, 66, 4), ("1/23", 84, 80, 4), ("1/24 ...", "", "", "")]
p1 = ["DANNY - TIP DIARY 2025  (Ember bar)     page 1", "date   total tips   told work(4070)   cash kept",
      *[f"{d:<7} {a!s:>6}        {b!s:>6}            {c!s:>4}" for d, a, b, c in jan_days],
      "   ... (daily pages Feb-Dec in my notebook, totals below)"]
p2 = ["TIP DIARY - MONTHLY TOTALS 2025", "month  told work   cash not reported   total tips"]
for m, rep, un in zip(MONTHS, REPORTED_M, UNREPORTED):
    p2.append(f"{m:<6} {rep:>7,}        {un:>5}              {rep + un:>6,}")
p2 += [f"TOTAL  {tips_reported:>7,.0f}        {unreported_tips:>5,}             {tips_reported + unreported_tips:>7,.0f}",
       "", "W-2 box 8 says allocated tips 2,900 ??  I only kept 1,600 extra", "all tips are from bar customers, no tip-outs rec'd"]
scanned_pages(C.pbc_file("06_Tip_diary_scan_2025.pdf", "Handwritten statement (scan)", "2026-02-09", "Sharefile upload",
                         "3 notebook pages scanned at FedEx"), [p1, p2,
    ["Tip-outs I GAVE to barbacks (cash, not on W-2):", "about $15/shift x 190 shifts = 2,850 ??",
     "(these come out of my 'told work' amount - is that deductible??)", "", "- Danny"]], handwritten=True, seed=31)
# handwritten mileage log (scanned)
UBER_M = [1010, 1090, 1260, 1310, 1290, 1220, 1420, 1340, 1240, 1290, 1300, 1375]
assert sum(UBER_M) == online_miles
COMM_M = [330, 330, 352, 352, 352, 352, 374, 352, 330, 352, 352, 352]
assert sum(COMM_M) == commute_miles
pm = ["MILES 2025 - Camry   (odometer 1/1: 48,210   12/31: 71,960)", "month   uber app   work (casino)   total biz"]
for m, a, b in zip(MONTHS, UBER_M, COMM_M):
    pm.append(f"{m:<7} {a:>6,}      {b:>5}          {a + b:>6,}")
pm += [f"TOTAL  {online_miles:>7,}     {commute_miles:>6,}         {online_miles + commute_miles:>7,}",
       "casino = drive to work + home 22 mi round trip, 190 shifts"]
scanned_pages(C.pbc_file("07_Mileage_log_scan_2025.pdf", "Handwritten statement (scan)", "2026-02-09", "Sharefile upload"),
              [pm], handwritten=True, seed=32, skew=-1.2)
statement(C.pbc_file("08_TMobile_2025_statement_summary.pdf", "Phone bill summary", "2026-02-09"),
    "T-Mobile - 2025 Account Statement Summary (1 line)", [
        {"table": [["Month", "Plan charges", "Taxes & fees", "Total"]] +
                  [[m, 76.00, 9.00, 85.00] for m in MONTHS] + [["Total", 912.00, 108.00, 1020.00]], "total_row": True}])
statement(C.pbc_file("09_IRS_Online_Account_Payment_History.pdf", "IRS online account printout", "2026-02-09"),
    "IRS Online Account - Payment Activity (printed 02/06/2026) - Tax period 12/31/2025", [
        {"table": [["Payment date", "Type", "Method", "Amount"], ["04/14/2025", "Estimated tax (1040-ES) 2025", "Direct Pay", 500.00],
                   ["04/14/2025", "Balance due 2024 Form 1040", "Direct Pay", 459.00],
                   ["06/16/2025", "Estimated tax (1040-ES) 2025", "Direct Pay", 500.00]]},
        {"para": "Total 2025 estimated tax payments: $1,000.00."}])
statement(C.pbc_file("10_GEICO_auto_declarations.pdf", "Insurance declarations", "2026-02-09"),
    "GEICO - Auto Policy Declarations (policy period 03/01/2025 - 03/01/2026)", [
        {"table": [["Vehicle", "Coverage", "Premium"], ["2021 Toyota Camry SE  VIN 4T1G11AK5MU0XXXXX", "Liability/Collision/Comp + TNC rideshare endorsement", 2280.00]]}])
F.f1099_k(C.pbc_file("11_1099-K_Uber (1).pdf", "Form 1099-K", "2026-02-12", note="client uploaded again"),
          ["Uber Technologies, Inc.", "1725 3rd Street", "San Francisco, CA 94158", "TIN: 00-2647441"], REC_T,
          {"1a": k_gross, "1b": k_gross, "2": "4121", "3": 1463, "months": k_months})
write_text(C.pbc_file("12_Email_thread_tips_miles_2026-02-18.txt", "Client correspondence", "2026-02-18", "Email",
                      "reply to preparer questions"),
"""From: preparer@evergreentax.example
To: Danny Okafor <danny.okafor@example.com>
Date: Mon, 16 Feb 2026 14:02:00 -0800
Subject: Okafor 2025 - tip diary and mileage

Hi Danny - thanks, the diary is great. Three questions:
1. Your W-2 shows $2,900 of "allocated tips" (box 8). Your diary shows $1,600 of cash tips you did not report to the bar.
   Is the diary complete for every shift you worked (you kept it daily, at the end of each shift)?
2. The tip-outs you paid to barbacks - were those already subtracted before you reported tips to the bar on your 4070s?
3. Your mileage log adds 4,180 "casino" miles to your Uber miles. Is that your drive to and from the bar job?

-----
From: Danny Okafor
Date: Wed, 18 Feb 2026 01:47:33 -0800
Subject: RE: Okafor 2025 - tip diary and mileage

1. yes every shift, I write it on my break or right after close. Same as last year
2. yes I report my tips after tip-out to the barbacks (bar manager says that's how everyone does it)
3. yes thats going to work at the casino. I usually go online on Uber from home not from work.
""")
scanned_pages(C.pbc_file("13_IMG_odometer_photos.pdf", "Photo upload (image)", "2026-02-20", "Text message",
                         "follow-up requested by preparer"),
    [["[photo] Camry dashboard  01/01/2025  ODO 048210", "", "[photo] Camry dashboard  12/31/2025  ODO 071960"]],
    handwritten=False, seed=33, skew=1.9, faded=True)

# ------------------------------------------------------------------ SCHEDULE C (preparer computation)
biz_miles = online_miles                          # commuting miles excluded
std_mileage = biz_miles * MILEAGE_2025
car_line9 = r(std_mileage + tolls)                # standard mileage + tolls (parking none)
fees_line10 = r(service_fee + booking + other_fees)
supplies = r(380 + 149)
phone = r(1020 * .60)
gross_receipts = r(k_gross + nec)
sch_c_exp = car_line9 + fees_line10 + supplies + phone
sch_c_net = gross_receipts - sch_c_exp
se = se_tax(sch_c_net, w2b["3"] + w2b["7"] + unreported_tips)
qbi_amt = sch_c_net - se["half"]

# Form 4137 on ACTUAL unreported tips (adequate records) instead of allocated tips
f4137_line10 = min(unreported_tips, SS_WAGE_BASE - (w2b["3"] + w2b["7"]))
f4137_ss = round(f4137_line10 * .062, 2)
f4137_med = round(unreported_tips * .0145, 2)
f4137_tax = r(f4137_ss + f4137_med)

qualified_tips = w2b["7"] + unreported_tips + uber_tips
assert uber_tips <= sch_c_net     # SE tips limited to net income from the tipped trade

facts = {
    "status": "S", "taxpayer": {"age65": False},
    "w2": [{"who": "T", "box1": w2b["1"], "box2": w2b["2"], "box3": w2b["3"], "box4": w2b["4"], "box5": w2b["5"],
            "box6": w2b["6"]}],
    "unreported_tips": unreported_tips, "unreported_tips_medicare": unreported_tips, "form4137_tax": f4137_tax,
    "sch1": {"sch_c": sch_c_net},
    "se": [{"who": "T", "net_profit": sch_c_net, "w2_ss_wages": w2b["3"] + w2b["7"] + unreported_tips}],
    "qbi": {"businesses": [{"name": "Uber rideshare (Sch C)", "qbi": qbi_amt}]},
    "sch1a": {"tips": qualified_tips, "tip_occupation": "Bartenders (W-2) / Rideshare drivers (Sch C)"},
    "estimated_payments": 1000,
}
R = Return1040(facts).compute()
v = R.values

# ---- Form 2210 check (regular installment method, withholding treated as paid evenly)
py_tax = 3159
cy_tax = v["24"]
req_annual = min(round(.90 * cy_tax, 2), py_tax)
inst = req_annual / 4
wh_q = v["25d"] / 4
es_paid = [500, 500, 0, 0]
rows_2210 = [["Form 2210 Part IV - installment", "Due date", "Required (cumulative)", "Paid (cumulative)", "Underpaid?"]]
cum_req = cum_paid = 0
underpaid_any = False
for i, due in enumerate(["04/15/2025", "06/16/2025", "09/15/2025", "01/15/2026"]):
    cum_req += inst
    cum_paid += wh_q + es_paid[i]
    under = cum_paid + 0.005 < cum_req
    underpaid_any |= under
    rows_2210.append([f"Q{i + 1}", due, r(cum_req), r(cum_paid), "Yes" if under else "No"])
assert not underpaid_any
# $1,000 test: total tax less withholding
owe_after_wh = cy_tax - v["25d"]

schc = [["Schedule C - Uber rideshare (NAICS 485310), cash method, Nevada", "Amount"],
        ["Line 1 Gross receipts: 1099-K $38,720 (fares, booking/airport fees, tolls, tips) + 1099-NEC $1,150", gross_receipts],
        ["Line 9 Car and truck: 15,145 business miles x $0.70 + tolls $340 (commute 4,180 mi excluded)", car_line9],
        ["Line 10 Commissions and fees: Uber service fee $7,660 + booking fees $2,410 + airport/other $1,070", fees_line10],
        ["Line 22 Supplies: car washes, rider water/mints $380; dash cam $149", supplies],
        ["Line 25 Utilities: phone $1,020 x 60% business", phone],
        ["Line 28 Total expenses", sch_c_exp], ["Line 31 Net profit", sch_c_net],
        ["Not deducted: gas $3,900, insurance $2,280, oil changes $310 (included in standard mileage rate)", 0]]
car = [["Form 4562 Part V / Sch C Part IV - vehicle information", "Detail"],
       ["Vehicle / placed in service for business", "2021 Toyota Camry SE / 09/2024 (standard mileage elected 2024)"],
       ["Total miles 2025 (odometer 48,210 -> 71,960)", "23,750"], ["Business miles (Uber online miles)", f"{biz_miles:,}"],
       ["Commuting miles (home <-> casino bartending job)", f"{commute_miles:,}"],
       ["Other personal miles", f"{23750 - biz_miles - commute_miles:,}"], ["Evidence (written)?", "Yes - app report + log"],
       ["Another vehicle for personal use?", "No"]]
f4137 = [["Form 4137 - Social Security and Medicare Tax on Unreported Tip Income", "Amount"],
         ["1(c) Total cash and charge tips received (tip diary) - Silver Sage Casino Resort EIN 00-8812046", tips_reported + unreported_tips],
         ["1(d) Tips reported to employer (Forms 4070 = W-2 box 7)", tips_reported],
         ["4 Unreported tips (actual per diary; allocated tips box 8 $2,900 NOT used - adequate records)", unreported_tips],
         ["5 Tips not required to be reported (< $20/month)", 0], ["6 Unreported tips subject to Medicare", unreported_tips],
         ["8 SS wages + SS tips (W-2 boxes 3 + 7)", r(w2b["3"] + w2b["7"])], ["10 Subject to SS tax", r(f4137_line10)],
         ["11 x 6.2%", f4137_ss], ["12 x 1.45%", f4137_med], ["13 Total (to Schedule 2 line 5)", f4137_tax]]
tips1a = [["Schedule 1-A Part II - qualified tips", "Amount"],
          ["W-2 box 7 social security tips (bartender - listed occupation)", r(w2b["7"])],
          ["Form 4137 line 4 unreported tips (bartender)", unreported_tips],
          ["Rideshare rider tips (Sch C; rideshare driver - listed occupation; limited to Sch C net)", r(uber_tips)],
          ["Total qualified tips", r(qualified_tips)], ["Limited to $25,000 (MAGI below $150,000 - no phase-out)", 25000],
          ["Not qualified: W-2 box 8 allocated tips not reported; tip-outs paid", "-"]]
qbi_att = [["Form 8995 - QBI", "Amount"], ["Schedule C net profit", sch_c_net], ["Less deductible 1/2 SE tax", -se["half"]],
           ["QBI", r(qbi_amt)], ["20% component", r(.2 * qbi_amt)],
           ["Income limit: 20% x taxable income before QBI (AGI - std ded - Sch 1-A tips) " +
            f"{v['11'] - v['12e'] - v['13b']:,}", r(.2 * (v['11'] - v['12e'] - v['13b']))],
           ["QBI deduction (smaller)", v["13a"]]]
C.write_return(R, [
    ("Taxpayer", "Daniel C. Okafor (XXX-XX-5082)"),
    ("Address", ", ".join(ADDR)),
    ("Filing status", "Single"),
    ("Digital assets question", "No"),
    ("Forms included", "1040; Sch 1, 1-A, 2, C, SE; Forms 4137, 8995 (2210 not required)"),
    ("State", "None - Nevada has no individual income tax"),
    ("Filing method", "E-file (8879 signed 03/10/2026); balance due by Direct Pay 04/15/2026"),
], attachments=[("Schedule C detail", schc), ("Vehicle information (Schedule C Part IV)", car), ("Form 4137 detail", f4137),
                ("Schedule 1-A Part II - no tax on tips", tips1a), ("Form 8995 detail", qbi_att),
                ("Form 2210 underpayment check (workpaper only)", rows_2210 +
                 [["Required annual payment = smaller of 90% x 2025 tax or 100% x 2024 tax", "", r(req_annual), "", ""]])])

gotchas = [
    gotcha("EVG1003-G1", "Scan - Unstructured PBC (handwritten statements)", "Allocated tips (W-2 box 8) vs actual tip diary",
           "Add W-2 box 8 allocated tips $2,900 to wages (line 1c) and Form 4137, or ignore unreported tips entirely.",
           "Allocated tips are not in box 1. With adequate daily records (contemporaneous tip diary) the taxpayer reports ACTUAL "
           "unreported tips - $1,600 - on line 1c and Form 4137 instead of the $2,900 allocation. Document the judgment in the WP.",
           "Line 1c $1,600 (not $2,900 or $0)", ["1c", "Form 4137"], "hard"),
    gotcha("EVG1003-G2", "Return - Form 4137 / Schedule 2", "SS/Medicare on unreported tips",
           "Report the $1,600 as wages without Form 4137 (no FICA) or compute SE tax on it.",
           f"Form 4137: 6.2% + 1.45% on $1,600 = {fmt(f4137_tax)} on Schedule 2 line 5; tips also count toward the SS wage base on Schedule SE line 8b.",
           f"Schedule 2 line 5 {fmt(f4137_tax)}", ["23", "Sch 2 line 5"], "medium"),
    gotcha("EVG1003-G3", "Scan - Unstructured PBC (Schedule C records / handwritten mileage log)", "Commuting miles in the mileage log",
           "Use the client's 19,325 'total biz' miles (includes 4,180 miles driving to the casino bartending job).",
           f"Driving between home and the W-2 job is commuting. Business miles = Uber online miles 15,145 x $0.70 = {fmt(r(std_mileage))} + tolls.",
           "Car expense overstated $2,926", ["Sch C line 9"], "medium"),
    gotcha("EVG1003-G4", "Return - Schedule C (1099-K gross vs net)", "Rideshare 1099-K gross includes Uber fees and tips",
           "Report net deposits ($28,730) as gross receipts, or report the 1099-K gross without deducting the Uber service/booking fees; "
           "or omit the 1099-NEC incentives / count the duplicate 1099-K twice.",
           f"Gross receipts = 1099-K $38,720 + 1099-NEC $1,150 = {fmt(gross_receipts)}; deduct Uber service fee, booking and airport fees "
           f"({fmt(fees_line10)}) on line 10. Second 1099-K upload is a duplicate.",
           "Schedule C net", ["Sch C line 1", "Sch C line 10"], "medium"),
    gotcha("EVG1003-G5", "Return - OBBBA no tax on tips (Schedule 1-A Part II)", "Qualified tips from W-2, 4137 and Schedule C",
           "Deduct only W-2 box 7 (or include allocated tips), and exceed the $25,000 cap.",
           f"Qualified tips = box 7 $24,600 + Form 4137 $1,600 + rider tips $2,860 (rideshare driver is a listed occupation; SE tips "
           f"limited to Schedule C net) = {fmt(r(qualified_tips))}, capped at $25,000. Unreported allocated tips never qualify.",
           "Line 13b $25,000", ["13b"], "hard"),
    gotcha("EVG1003-G6", "Return - Schedule C / standard mileage", "Actual car costs claimed on top of standard mileage",
           "Deduct gas, insurance and oil changes from the organizer in addition to 70 cents/mile.",
           "Standard mileage rate replaces operating costs (gas, insurance, maintenance, depreciation); only tolls/parking added. "
           "Standard mileage was elected in the first business-use year (2024), so it may continue.",
           "Schedule C overstated $6,490", ["Sch C line 9"], "easy"),
    gotcha("EVG1003-G7", "Return - Schedule SE / QBI", "SE tax and QBI on rideshare profit",
           "Skip SE tax because the W-2 already has FICA, or compute QBI on net profit without the 1/2 SE tax reduction.",
           f"SE tax on {fmt(sch_c_net)} x 92.35% = {fmt(se['se_tax'])} (SS base not reached); QBI = net - 1/2 SE = {fmt(r(qbi_amt))} -> "
           f"{fmt(v['13a'])} deduction.",
           "Schedule 2 line 4 / line 13a", ["23", "13a", "10"], "medium"),
    gotcha("EVG1003-G8", "Return - Form 2210 (estimated tax)", "Only 2 of 4 estimated payments made",
           "Compute an underpayment penalty for the missed September and January installments, or skip the 2210 analysis.",
           f"Required annual payment = smaller of 90% of 2025 tax ({fmt(r(.9 * cy_tax))}) or 100% of 2024 tax ({fmt(py_tax)}) = {fmt(r(req_annual))}. "
           "Withholding is treated as paid evenly; with the April and June $500 payments every cumulative installment is covered -> "
           "no penalty, Form 2210 not required.",
           "Line 38 $0", ["38"], "medium"),
]
C.write_answer_key(R, {"residence": "NV - Las Vegas (no state return)", "complexity": "W-2 tipped + Schedule C rideshare"},
                   gotchas, filings=[{"form": "Form 1040 (federal)", "method": "e-file", "due": "2026-04-15", "filed": "2026-03-11"}],
                   extra={"form_2210": {"required_annual_payment": r(req_annual), "penalty": 0,
                                        "tax_after_withholding": owe_after_wh}})
C.write_receipt_log("EVG1003-1040-2025", "M. Alvarez (staff)", "R. Patel (senior)", "S. Kennedy, CPA", "2026-02-09")

C.write_notes(f"""
# EVG1003 - Okafor, Daniel - 2025 Form 1040 - Preparer Notes

*Synthetic client - Project Evergreen. Return status: **signed off, e-filed 03/11/2026, accepted 03/12/2026.***

## Return summary
| | |
|---|---|
| Filing status | Single |
| Wages incl. reported tips (1a) | {fmt(v['1a'])} |
| Unreported tips - Form 4137 (1c) | {fmt(v['1c'])} |
| Schedule C net profit (Uber) | {fmt(sch_c_net)} |
| AGI (line 11) | {fmt(v['11'])} |
| Standard deduction | {fmt(v['12e'])} |
| QBI deduction | {fmt(v['13a'])} |
| No tax on tips (Sch 1-A) | {fmt(v['13b'])} |
| Taxable income | {fmt(v['15'])} |
| Income tax (line 16) | {fmt(v['16'])} |
| SE tax + Form 4137 tax | {fmt(se['se_tax'])} + {fmt(f4137_tax)} |
| Total tax (line 24) | {fmt(v['24'])} |
| Withholding + estimates | {fmt(v['25d'])} + {fmt(v['26'])} |
| **Balance due** | **{fmt(v['balance_due'])}** (no Form 2210 penalty) |

## What I did and why (plain English)
1. **W-2 and tips.** Box 1 {fmt(v['1a'])} already includes the $24,600 of tips Danny reported to the bar on Forms 4070 (box 7).
   Box 8 shows **$2,900 of allocated tips** - these are NOT in box 1. Allocated tips must be reported unless the employee has
   adequate records of actual tips. Danny kept a contemporaneous daily tip diary (WP 6, confirmed in his 02/18 email: written each
   shift), showing $1,600 of cash tips he kept and never reported. With adequate records we report the **actual $1,600** on line 1c and
   Form 4137, not the $2,900 allocation. The diary is retained in the WP in case of exam.
2. **Form 4137.** $1,600 x 7.65% = {fmt(f4137_tax)} of employee SS/Medicare on Schedule 2 line 5. Tip-outs paid to barbacks were
   already netted before his 4070 reports (he reports after tip-out), so no separate deduction.
3. **Uber (Schedule C).** Gross receipts = the gross 1099-K ($38,720 - fares, booking/airport fees, tolls and rider tips) plus the
   1099-NEC incentives ($1,150) = {fmt(gross_receipts)}. The 1099-K is gross, so Uber's service fee and the pass-through fees
   ({fmt(fees_line10)}) are deducted on line 10. The second 1099-K upload is the same form (duplicate, excluded). Bank deposits
   ($28,730) tie to gross less fees.
4. **Mileage.** His log adds 4,180 "casino" miles (home to the bar job and back) to the Uber miles. That is commuting - excluded.
   Business miles = Uber online miles 15,145 (he goes online from home; miles while offline are not counted) x 70 cents =
   {fmt(r(std_mileage))} + tolls $340. Gas, insurance and oil changes listed on the organizer are covered by the standard mileage
   rate - not deducted. Standard mileage was elected in 2024 (first year), so it can continue. Odometer photos support 23,750 total miles.
5. **Phone.** 60% business use (client estimate - Uber app runs whenever he drives; reasonable vs. 64% vehicle business use) -> {fmt(phone)}.
6. **SE tax / QBI.** SE tax {fmt(se['se_tax'])} (half deducted {fmt(se['half'])}). QBI = {fmt(sch_c_net)} - {fmt(se['half'])} =
   {fmt(r(qbi_amt))}; 20% = {fmt(v['13a'])} (well below the 20%-of-taxable-income limit).
7. **No tax on tips (new for 2025, Schedule 1-A Part II).** Bartenders and rideshare drivers are both on Treasury's tipped-occupation
   list. Qualified tips: W-2 box 7 $24,600 + Form 4137 $1,600 + Uber rider tips $2,860 = {fmt(r(qualified_tips))}. The rideshare
   tips are limited to the Schedule C net profit ({fmt(sch_c_net)}) - not limiting. Total capped at **$25,000**. MAGI {fmt(v['11'])}
   is under $150,000 - no phase-out. The 2025 W-2 did not have to separately report qualified tips, so box 7 is used (transition relief).
   Note: the deduction reduces income tax only - SE tax and the 4137 FICA still apply.
8. **Estimated payments / Form 2210.** Danny paid only the April and June $500 estimates. 2025 tax {fmt(cy_tax)}; tax after
   withholding {fmt(owe_after_wh)} (over $1,000, so the small-balance exception doesn't apply). Required annual payment = smaller of
   90% of 2025 tax ({fmt(r(.9 * cy_tax))}) or 100% of 2024 tax ({fmt(py_tax)}; 2024 AGI under $150k) = **{fmt(r(req_annual))}**
   ({inst:,.2f} per quarter) - the prior-year safe harbor is the lower one.
   Withholding ({fmt(v['25d'])}) is treated as paid evenly; with the two $500 payments every cumulative installment is met -> **no
   penalty; Form 2210 not filed.**
9. **Tax.** Taxable income {fmt(v['15'])} -> Single tax table {fmt(v['16'])}.
10. **Nevada.** No individual income tax - no state return.

## Open items / client communication
- 2026 estimates: recommend $300/quarter (the tips deduction lowered his income tax); vouchers + Direct Pay instructions sent.
- Keep the tip diary going in 2026 (needed for both the allocated-tips position and the tips deduction).
- Reminder: from 2026 the employer should report qualified tips and the occupation code separately on the W-2.

## Hand-off to signer / routing
- [x] Return locked; Accountant's copy saved as *reviewed*
- [x] Federal 1040 - e-file; no state; no FBAR
- [x] Due date 04/15/2026; balance due {fmt(v['balance_due'])} - Direct Pay debit 04/15/2026 authorized on 8879
- [x] eSign (8879) - text/email contact confirmed
- Billing: W-2 + Schedule C tier $1,650; +0.5 hr for tip-diary / 4137 analysis (in scope). Nothing to W/O.
""")
C.write_review_points(f"""
# Review Points - EVG1003 - 2025 - Form 1040

*Reviewer: R. Patel (blue). Preparer responses in red. Synthetic.*

1. **WP 2 / W-2 box 8** - First draft added the $2,900 allocated tips to line 1c and Form 4137 (CCH default for box 8).
   - Danny keeps a daily diary (WP 6) showing $1,600 of unreported cash tips. With adequate records, report actual tips. Confirm
     with the client that the diary was kept every shift and document the judgment.
   - *Preparer: Confirmed by email 02/18 (WP 12). Line 1c and 4137 now $1,600.*
2. **Schedule C line 9** - Draft used 19,325 miles from the handwritten log. 4,180 of those are home <-> casino commuting. Use the
   Uber online miles.
   - *Preparer: Changed to 15,145 miles; commute listed on Part IV as commuting miles.*
3. **Schedule C expenses** - Draft deducted gas ($3,900) and GEICO insurance ($2,280) and oil changes in addition to standard mileage.
   Remove - standard rate covers operating costs.
   - *Preparer: Removed.*
4. **Schedule C line 1** - Duplicate 1099-K (WP 11 - "(1)" download) was also autoflowed; gross receipts doubled. Remove the duplicate;
   confirm 1099-NEC incentives are included.
   - *Preparer: Duplicate marked DUP; gross receipts {fmt(gross_receipts)}.*
5. **Schedule 1-A** - Draft tips deduction used box 7 only ($24,600). Add the 4137 tips and the Uber rider tips (rideshare drivers are
   listed), then apply the $25,000 cap.
   - *Preparer: Total qualified tips {fmt(r(qualified_tips))} -> $25,000.*
6. **Form 2210** - Client skipped Q3/Q4 estimates. Run the installment check against 100% of PY tax ({fmt(py_tax)}).
   - *Preparer: All installments met with withholding + April/June payments - no penalty (WP 2210 tape).*
7. FYI - tip-outs paid to barbacks: he reports after tip-out, so nothing further to deduct. OK as is.
""")
print("EVG1003 done", R.summary()["24"], v["balance_due"], "SchC", sch_c_net)
