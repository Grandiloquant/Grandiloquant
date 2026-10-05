"""EVG1019 - Owen & Chloe Fitzgerald (MFJ, North Carolina - Raleigh). W-2 + consulting Schedule C with home office
(Form 8829 vs simplified; 8829 share must come off Schedule A); 2016 mortgage grandfathered at $1M (CCH default $750k
limit must be overridden); income tax vs sales tax (EV highway-use tax) for SALT; 25D solar credit; EV bought
10/15/2025 (no 30D; car-loan interest phased out); SEP-IRA maximum; Additional Medicare on combined wages + SE;
NC D-400 (NC itemized with $20k mortgage/property-tax cap, child deduction $0, no NC solar credit)."""
from common import ClientBuild, gotcha, fmt
from docs import statement, scanned_pages, write_text, write_xlsx
import forms as F
from tax2025 import Return1040, r, se_tax

C = ClientBuild("EVG1019", "Fitzgerald", "Owen & Chloe Fitzgerald")
ADDR = ("8416 Glenwood Ridge Ct", "Raleigh, NC 27612")
T = {"name": "Owen P. Fitzgerald", "ssn": "XXX-XX-5582", "dob": "1982-02-14"}
S = {"name": "Chloe A. Fitzgerald", "ssn": "XXX-XX-7719", "dob": "1984-11-02"}
REC_T = [T["name"], *ADDR, f"TIN: {T['ssn']}"]
REC_S = [S["name"], *ADDR, f"TIN: {S['ssn']}"]
REC_J = ["Owen P. & Chloe A. Fitzgerald", *ADDR, f"TIN: {T['ssn']}"]
BIZ = "Fitzgerald Advisory (Chloe A. Fitzgerald, sole proprietor) - management consulting, NAICS 541611"

# ------------------------------------------------------------------ home / mortgage facts
LOAN_ORIG, LOAN_BAL, LOAN_RATE = 960000, 872000, .0325     # 10/1 interest-only ARM, fixed 3.25% through 09/2026
MORT_INT = r(LOAN_BAL * LOAN_RATE)                           # interest-only; balance constant all year
RE_TAX, HOME_INS, UTIL, HVAC = 9840.00, 2460.00, 5160.00, 780.00
OFFICE_SQFT, HOME_SQFT = 300, 3000
PCT = OFFICE_SQFT / HOME_SQFT
HOME_COST, HOME_LAND = 1200000, 280000
OFFICE_BASIS = r((HOME_COST - HOME_LAND) * PCT)
OFFICE_DEP = r(OFFICE_BASIS * .02564)                        # 39-yr SL, office in use since 03/2019 (year 7)
PRIOR_OFFICE_DEP = r(OFFICE_BASIS * .02033) + 5 * OFFICE_DEP
LIMIT_750_PCT = 750000 / LOAN_BAL

# ------------------------------------------------------------------ Schedule C (cash basis)
NEC = [("Carolina HealthSystems Partners", "00-5102277", 64000.00), ("Piedmont Logistics Group LLC", "00-3371840", 36000.00),
       ("Blue Ridge Credit Union", "00-1128830", 22500.00)]
GROSS = sum(x[2] for x in NEC)
PREP_FEE_PY = 2700.00
SCH_C_EXP = [  # (Sch C line, description, amount allowed)
    ("8", "Advertising - website hosting/domain", 480.00),
    ("15", "Insurance - professional liability (E&O)", 1850.00),
    ("17", "Legal & professional - bookkeeper", 1200.00),
    ("17", "Legal & professional - 1/3 of 2024 tax prep fee paid 04/2025 ($2,700 x 1/3; Sch C time share)", round(PREP_FEE_PY / 3, 2)),
    ("18", "Office expense - postage, printing", 640.00),
    ("22", "Supplies - laptop (de minimis safe harbor election, $2,100 <= $2,500)", 2100.00),
    ("24a", "Travel - airfare, hotels (client sites)", 6850.00),
    ("24b", "Meals - $2,400 x 50%", 1200.00),
    ("27a", "Software & subscriptions", 2160.00),
    ("27a", "Continuing education / certification (PMP renewal, courses)", 895.00),
    ("27a", "Cell phone - Chloe's line $1,440 x 60% business", 864.00),
]
EXP_TOTAL = round(sum(x[2] for x in SCH_C_EXP), 2)
TENTATIVE = round(GROSS - EXP_TOTAL, 2)
F8829 = [("9", "Casualty losses", 0), ("10/11", "Mortgage interest (Form 1098; fully deductible - pre-12/16/2017 debt)", MORT_INT),
         ("11", "Real estate taxes", RE_TAX), ("18", "Insurance", HOME_INS), ("20", "Repairs and maintenance (HVAC)", HVAC),
         ("21", "Utilities", UTIL)]
IND = {k: round(v * PCT, 2) for _, k, v in F8829 if v}
HOME_OFFICE = r(sum(IND.values()) + OFFICE_DEP)
SIMPLIFIED = 5 * OFFICE_SQFT
NET_C = r(TENTATIVE - HOME_OFFICE)
SE = se_tax(NET_C, 0)
SEP = r(.20 * (NET_C - SE["half"]))

# ------------------------------------------------------------------ other facts
w2t = {"1": 168000.00, "2": 21800.00, "3": 176100.00, "4": 10918.20, "5": 191500.00, "6": 2776.75,
       "12": [("D", 23500.00), ("DD", 18400.00)], "13": ["Retirement plan: X"], "control": "TBA-44810",
       "state": [{"state": "NC", "id": "600118834", "wages": 168000.00, "tax": 7350.00}]}
NC_WH = w2t["state"][0]["tax"]
NC_ES = [("04/15/2025", 1000.00, 2025), ("06/16/2025", 1000.00, 2025), ("09/15/2025", 1000.00, 2025), ("01/15/2026", 1000.00, 2025),
         ("01/15/2025", 900.00, 2024), ("04/15/2025", 640.00, "2024 balance due")]
NC_PAID_2025 = NC_WH + sum(a for d, a, y in NC_ES if d.endswith("2025"))
NC_ES_FOR_2025 = sum(a for d, a, y in NC_ES if y == 2025)
FED_ES = 4 * 3500.00
SOLAR = 31500.00
EV_PRICE, HUT = 52000.00, round(52000.00 * .03, 2)
EV_INT = 438.12
SALES_TAX_TABLE = 2640            # IRS Sales Tax Deduction Calculator - Wake County 7.25%, 4 exemptions (assumption)
CHARITY = 6000.00
BANK_INT = 382.16

# ------------------------------------------------------------------ PERM
C.write_profile(f"""
# EVG1019 - Fitzgerald, Owen & Chloe  (PERM)

*Synthetic client - Project Evergreen training data.*

| Item | Detail |
|---|---|
| Client ID | EVG1019 |
| Taxpayer | Owen P. Fitzgerald, DOB 02/14/1982, SSN XXX-XX-5582 - Director, Clinical Data, Triangle BioAnalytics (W-2) |
| Spouse | Chloe A. Fitzgerald, DOB 11/02/1984, SSN XXX-XX-7719 - independent management consultant (Schedule C since 03/2019) |
| Dependents | Harper Fitzgerald (daughter, DOB 06/11/2016), Declan Fitzgerald (son, DOB 09/24/2019) |
| Address | {ADDR[0]}, {ADDR[1]} (Wake County) - purchased 08/19/2016 for $1,200,000 (land $280,000 per Wake County) |
| Mortgage | Oak City Mortgage Co. - **originated 08/19/2016, $960,000 acquisition debt** (10/1 interest-only ARM, 3.25% fixed to 09/2026). Grandfathered $1,000,000 limit (debt incurred before 12/16/2017). Principal curtailments 2019-2024 $88,000 -> balance $872,000 |
| Home office | 300 sq ft dedicated office / 3,000 sq ft home = 10%; in use since 03/2019; 8829 depreciation basis $92,000 (39-yr) |
| Contact | Chloe preferred - chloe@fitzgeraldadvisory.example, (919) 555-0148; eSign OK |
| Engagement | Client since 2019. Quote $3,200 (1040 + Sch C/8829 + NC) |
| Payment info | Voided check on file (First Citizens ****6620) |
""")
F.prior_year_summary(C.perm_file("2024_Form_1040_Return_Summary.pdf", "Prior-year return summary"), "Owen & Chloe Fitzgerald",
    "EVG1019", "Married filing jointly", [
        ["1a", "W-2 wages - Triangle BioAnalytics (Owen)", 161200],
        ["Sch C line 31", "Fitzgerald Advisory - net profit (after Form 8829 $6,904)", 91450],
        ["Sch 1 line 16", "SEP-IRA (max)", 17040], ["11", "AGI", 229320],
        ["Sch A", "Itemized: NC income tax 11,210 (SALT cap $10,000) + mortgage interest 90% 25,506 + charity 5,500", 41006],
        ["13", "QBI deduction", 13320], ["19", "Child tax credit (2)", 4000], ["24", "Total tax", 44290], ["35a", "Refund", 1180]],
    carryovers=[["Form 8829 depreciation claimed 2019-2024 (office basis $92,000)", PRIOR_OFFICE_DEP],
                ["Form 8829 carryover of operating expenses / excess casualty & depreciation", 0]],
    notes="PY WP: Mortgage interest - OVERRIDE of Axcess $750k limitation (2016 acquisition debt, grandfathered $1M; calc tape in "
          "PY WP 14). 8829 share of mortgage interest and real estate tax removed from Sch A. SEP computed at max each year.")

# ------------------------------------------------------------------ PBC
EMP = {"name": "Triangle BioAnalytics, Inc.", "addr1": "5000 Centregreen Way Ste 300", "addr2": "Cary, NC 27513", "ein": "00-6402217"}
EE = {"name": T["name"], "addr1": ADDR[0], "addr2": ADDR[1], "ssn": T["ssn"]}
F.organizer(C.pbc_file("01_2025_Organizer_completed.pdf", "Client organizer", "2026-03-10"), "Owen & Chloe Fitzgerald", "EVG1019",
    general=[("Did your marital status change during 2025?", "No", ""),
             ("Did you buy a vehicle?", "Yes", "Hyundai Ioniq 5 in October - EV credit?"),
             ("Did you make energy improvements to your home?", "Yes", "Solar panels July - $31,500"),
             ("Do you have a home office?", "Yes", "same office - use $5/sq ft this year, easier?"),
             ("Do you want to maximize the SEP contribution?", "Yes", "Yes - tell us the number"),
             ("Did you make estimated tax payments?", "Yes", "Fed 4 x 3,500; NC 4 x 1,000"),
             ("Did you receive, sell, exchange digital assets?", "No", "")],
    dependents=[["Harper Fitzgerald", "Daughter", "06/11/2016", "3310", "12", "No"],
                ["Declan Fitzgerald", "Son", "09/24/2019", "8127", "12", "No"]],
    income_rows=[["Wages", "Triangle BioAnalytics", 161200, "see W-2"],
                 ["Self-employment", "Fitzgerald Advisory", 91450, "see P&L"],
                 ["Interest", "First Citizens Bank", 355, "382"]],
    deductions_rows=[["Mortgage interest", "Oak City Mortgage", 28340, "see 1098"],
                     ["Real estate tax", "Wake County (escrow)", 9610, "see 1098"],
                     ["Charitable - cash", "St. Raphael / Food Bank", 5500, "6,000"],
                     ["Tax prep fee", "Evergreen (2024 return)", 2600, "2,700"]],
    signature_date="03/08/2026")
F.w2(C.pbc_file("02_W-2_Triangle_BioAnalytics_Owen.pdf", "Form W-2", "2026-03-10"), EMP, EE, w2t)
for i, (payer, ein, amt) in enumerate(NEC):
    corrected = payer.startswith("Carolina")
    F.f1099_nec(C.pbc_file(f"0{3 + i}_1099-NEC_{payer.split()[0]}{'_CORRECTED' if corrected else ''}.pdf",
                           "Form 1099-NEC" + (" (corrected)" if corrected else ""), "2026-03-10"),
                [payer, "(address on file)", "North Carolina", f"TIN: {ein}"], REC_S, {"1": amt}, corrected=corrected)
F.f1099_nec(C.pbc_file("06_1099-NEC_Carolina_HealthSystems_original.pdf", "Form 1099-NEC", "2026-03-10"),
            [NEC[0][0], "(address on file)", "North Carolina", f"TIN: {NEC[0][1]}"], REC_S, {"1": 63000.00})
write_xlsx(C.pbc_file("07_Fitzgerald_Advisory_2025_PnL_Chloe.xlsx", "Client P&L (XLSX)", "2026-03-10"), {
    "P&L 2025": [["Account", "Amount", "Chloe's note"],
                 ["Consulting revenue - Carolina HealthSystems", 64000.00, "Dec invoice paid 12/29"],
                 ["Consulting revenue - Piedmont Logistics", 36000.00, ""],
                 ["Consulting revenue - Blue Ridge CU", 22500.00, ""],
                 ["Total revenue", GROSS, ""],
                 ["Website", 480.00, ""], ["E&O insurance", 1850.00, ""], ["Bookkeeper", 1200.00, ""],
                 ["Postage / printing", 640.00, ""], ["Laptop (MacBook Pro)", 2100.00, "bought 02/03/2025"],
                 ["Travel", 6850.00, ""], ["Meals", 2400.00, "client meals + travel meals"],
                 ["Software", 2160.00, ""], ["PMP / courses", 895.00, ""], ["Cell phone", 1440.00, "my line only - maybe 60% biz"],
                 ["Home office", SIMPLIFIED, "300 sq ft x $5"],
                 ["Net income", GROSS - 480 - 1850 - 1200 - 640 - 2100 - 6850 - 2400 - 2160 - 895 - 1440 - SIMPLIFIED, ""]]})
F.f1098(C.pbc_file("08_1098_Oak_City_Mortgage.pdf", "Form 1098", "2026-03-10"),
        ["Oak City Mortgage Co.", "150 Fayetteville St Ste 900", "Raleigh, NC 27601", "TIN: 00-0000915"], REC_J,
        {"1": MORT_INT, "2": LOAN_BAL, "3": "08/19/2016", "7": "Yes", "9": "1", "10": f"RE tax {RE_TAX:,.2f}",
         "11": "08/19/2016"}, account_no="Loan ****2291",
        notes=["Loan type: 10/1 interest-only ARM. Original principal $960,000. Principal curtailments received 2019-2024: $88,000. "
               "No principal payments or advances in 2025. Balance 01/01/2025 and 12/31/2025: $872,000.00."])
statement(C.pbc_file("09_Home_expenses_2025_summary.pdf", "Client summary", "2026-03-10"),
    "Fitzgerald household - 2025 home costs (compiled by Chloe)", [
        {"table": [["Item", "Vendor", "2025 paid"], ["Homeowners insurance", "NC Farm Bureau (escrow)", HOME_INS],
                   ["Electric", "Duke Energy Progress", 3380.00], ["Natural gas", "PSNC Energy", 1060.00], ["Water/sewer", "City of Raleigh", 720.00],
                   ["HVAC service + repair", "Pro-Air Heating & Cooling", HVAC], ["Kitchen remodel (not office)", "Triangle Kitchen & Bath", 38400.00]],
         "left_align_cols": [0, 1]},
        {"para": "Office: 300 sq ft (15 x 20 ft room over garage), used only for Fitzgerald Advisory. House 3,000 sq ft heated."}])
statement(C.pbc_file("10_Sunstream_Solar_Invoice_and_PTO.pdf", "Contractor invoice + utility letter", "2026-03-10"),
    "Sunstream Solar of NC LLC - Final Invoice #SS-25-0719 / Duke Energy Permission to Operate", [
        {"table": [["Item", "Amount"], ["11.2 kW roof-mounted PV system (28 panels, microinverters)", 28900.00],
                   ["Labor, permitting, interconnection", 2600.00], ["Total paid (financed via cash - paid in full 07/22/2025)", SOLAR]],
         "left_align_cols": [0]},
        {"para": ["Installation complete 07/22/2025. Duke Energy Progress Permission to Operate issued 08/05/2025.",
                  "Property: 8416 Glenwood Ridge Ct, Raleigh NC (primary residence). No battery storage. No utility rebate received."]}])
statement(C.pbc_file("11_Hyundai_Buyers_Order_Ioniq5_2025-10-15.pdf", "Vehicle purchase agreement", "2026-03-10"),
    "Capital Hyundai of Raleigh - Retail Buyer's Order", [
        {"table": [["Item", "Value"], ["Date of agreement / delivery", "10/15/2025 / 10/15/2025"],
                   ["Vehicle", "NEW 2025 Hyundai IONIQ 5 SEL AWD, VIN KM8KRDDF2SU10XXXX (final assembly: Ellabell, GA, USA)"],
                   ["Buyers", "Owen P. Fitzgerald, Chloe A. Fitzgerald"], ["Cash price", EV_PRICE],
                   ["NC Highway Use Tax (3%)", HUT], ["Title / plate / registration", 118.00],
                   ["Down payment (10/15/2025)", 8678.00], ["Amount financed - Hyundai Motor Finance", 45000.00],
                   ["Clean vehicle credit seller report (Form 15400) / transfer election", "NOT AVAILABLE - vehicle acquired after 09/30/2025"]],
         "left_align_cols": [0, 1]},
        {"para": "No deposit or binding agreement prior to 10/15/2025. Purchaser intends personal use."}])
statement(C.pbc_file("12_Hyundai_Motor_Finance_2025_Interest.pdf", "Lender interest statement", "2026-03-10"),
    "Hyundai Motor Finance - 2025 Year-End Account Summary", [
        {"table": [["Field", "Value"], ["Account", "****7715"], ["Contract date", "10/15/2025"], ["APR", "5.99%"],
                   ["Interest paid 2025", EV_INT], ["Principal balance 12/31/2025", 44102.55]], "left_align_cols": [0, 1]}])
statement(C.pbc_file("13_Estimated_Tax_Payment_Confirmations.pdf", "Payment confirmations", "2026-03-10"),
    "IRS Direct Pay / NCDOR ePayment confirmations (printed by client)", [
        {"heading": "IRS - Form 1040-ES (2025)", "table": [["Date", "Amount", "Tax year"],
            ["04/15/2025", 3500.00, 2025], ["06/16/2025", 3500.00, 2025], ["09/15/2025", 3500.00, 2025], ["01/15/2026", 3500.00, 2025]]},
        {"heading": "NC Department of Revenue - NC-40 / D-400V", "table": [["Date", "Amount", "Tax year / type"]] +
            [[d, a, str(y)] for d, a, y in NC_ES]}])
statement(C.pbc_file("14_Charitable_Receipts_2025.pdf", "Charity receipts", "2026-03-10"),
    "2025 Contribution Acknowledgements", [
        {"table": [["Organization", "Date(s)", "Amount"], ["St. Raphael Catholic Church (cash, weekly)", "2025", 4800.00],
                   ["Food Bank of Central & Eastern NC", "11/28/2025", 1200.00], ["Total", "", CHARITY]], "total_row": True,
         "note": "No goods or services were provided in exchange for these contributions."}])
statement(C.pbc_file("15_NC529_Statement_Harper_Declan.pdf", "529 plan statement", "2026-03-10"),
    "NC 529 Plan - 2025 Annual Statement", [
        {"table": [["Beneficiary", "Contributions 2025", "Balance 12/31/2025"], ["Harper Fitzgerald", 3000.00, 31408.12],
                   ["Declan Fitzgerald", 3000.00, 19870.55]]},
        {"para": "No withdrawals in 2025."}])
write_text(C.pbc_file("16_Email_Chloe_2026-03-12.txt", "Client correspondence", "2026-03-12", "Email"),
"""From: Chloe Fitzgerald <chloe@fitzgeraldadvisory.example>
To: preparer@evergreentax.example
Date: Thu, 12 Mar 2026 13:02:44 -0400
Subject: Fitzgerald 2025 - questions

Hi,
1) We bought the Ioniq 5 on Oct 15. The dealer said the point-of-sale credit was gone but that we could still
   claim the $7,500 on our return. Is that right? Also I read car loan interest is deductible now?
2) I put the home office at $5/sq ft on my P&L because it's simpler. Is that OK?
3) Solar - we get 30% back, right? Can NC give us anything too?
4) Please tell us the max SEP amount - I'll fund it before you file. We're traveling in April; please extend.
Thanks! Chloe
""")
write_text(C.pbc_file("17_Email_Chloe_SEP_funded_2026-09-18.txt", "Client correspondence", "2026-09-18", "Email",
                      "follow-up"),
f"""From: Chloe Fitzgerald
Date: Fri, 18 Sep 2026 09:15:10 -0400
Subject: RE: SEP amount

Funded ${SEP:,} to my Fidelity SEP-IRA today (confirmation attached - designated as a 2025 contribution).
""")

# ------------------------------------------------------------------ RETURN
sch_a_mort = r(MORT_INT * (1 - PCT))
sch_a_re = r(RE_TAX * (1 - PCT))
facts = {
    "status": "MFJ",
    "taxpayer": {"age65": False}, "spouse": {"age65": False},
    "dependents": [{"name": "Harper Fitzgerald", "ctc": True}, {"name": "Declan Fitzgerald", "ctc": True}],
    "w2": [{"who": "T", "box1": w2t["1"], "box2": w2t["2"], "box3": w2t["3"], "box4": w2t["4"], "box5": w2t["5"], "box6": w2t["6"]}],
    "interest": [{"payer": "First Citizens Bank", "amount": BANK_INT}],
    "sch1": {"sch_c": NET_C},
    "se": [{"who": "S", "net_profit": NET_C, "w2_ss_wages": 0}],
    "se_earned_S": NET_C,
    "adjustments": {"sep": SEP},
    "itemized": {"state_income_tax": NC_PAID_2025, "real_estate_tax": sch_a_re, "mortgage_interest_1098": sch_a_mort,
                 "charity_cash": CHARITY},
    "qbi": {"businesses": [{"name": "Fitzgerald Advisory (SSTB - consulting; below threshold)",
                            "qbi": NET_C - SE["half"] - SEP, "sstb": True}]},
    "sch1a": {"car_interest": EV_INT, "vin": "KM8KRDDF2SU10XXXX"},
    "res_clean_energy": r(SOLAR * .30),
    "amt": {"other": 0},          # Form 6251 check only (no preference items)
    "estimated_payments": FED_ES,
}
R = Return1040(facts).compute()
v = R.values
AGI = v["11"]
# CCH default ($750k) comparison
cch_default_int = r(MORT_INT * LIMIT_750_PCT * (1 - PCT))

# NC D-400
NC_STD = 25500
nc_mort_re = min(20000, sch_a_mort + sch_a_re)
nc_item = nc_mort_re + r(CHARITY)
nc_ded = max(NC_STD, nc_item)
nc_child = 0                                   # NC child deduction: $0 for MFJ AGI > $140,000
nc_ti = AGI - nc_ded - nc_child
nc_tax = r(nc_ti * .0425)
nc_paid = r(NC_WH + NC_ES_FOR_2025)
nc_refund = nc_paid - nc_tax

sch_c_rows = [["Schedule C - " + BIZ, "Line", "Amount"],
              ["Gross receipts (3 x 1099-NEC; Carolina HealthSystems CORRECTED $64,000 used - original $63,000 superseded)", "1", r(GROSS)]] + \
             [[d, ln, r(a)] for ln, d, a in SCH_C_EXP] + \
             [["Total expenses before home office", "28", r(EXP_TOTAL)], ["Tentative profit", "29", r(TENTATIVE)],
              ["Business use of home (Form 8829) - NOT simplified $1,500", "30", HOME_OFFICE], ["Net profit", "31", NET_C],
              ["Method: cash; material participation: Yes; started/acquired in 2025: No", "F/G/H", ""],
              ["Payments requiring Form 1099: No (no contractors)", "I/J", ""]]
f8829 = [["Form 8829 - 300 / 3,000 sq ft = 10.00%", "Total (indirect)", "Business 10%"]] + \
        [[f"Line {ln} {k}", r(val), r(IND[k])] for ln, k, val in F8829 if val] + \
        [[f"Line 42 Depreciation: basis {HOME_COST - HOME_LAND:,} x 10% = {OFFICE_BASIS:,}; 39-yr SL x 2.564% (in use since 03/2019)", "", OFFICE_DEP],
         ["Line 36 Allowable (gross-income limit not reached)", "", HOME_OFFICE],
         [f"Simplified method alternative: {OFFICE_SQFT} sq ft x $5", "", SIMPLIFIED],
         ["Line 16 excess mortgage interest", "", "None - debt grandfathered under $1,000,000"],
         [f"Prior depreciation 2019-2024: {PRIOR_OFFICE_DEP:,}; accumulated after 2025: {PRIOR_OFFICE_DEP + OFFICE_DEP:,} (IRC 1250 recapture on sale)", "", ""]]
mort = [["Mortgage interest limitation (manual override of Axcess default)", "Amount"],
        ["Acquisition debt incurred 08/19/2016 (before 12/16/2017) -> $1,000,000 limit (IRC 163(h)(3)(F)(iii))", LOAN_ORIG],
        ["Average balance 2025 (interest-only; no principal activity)", LOAN_BAL],
        ["Interest paid (Form 1098 box 1)", MORT_INT],
        ["Less home office share on Form 8829 (10%)", -r(MORT_INT * PCT)],
        ["Schedule A line 8a - 100% of personal share (balance < $1M)", sch_a_mort],
        [f"Axcess default at $750,000 ({LIMIT_750_PCT:.2%} of interest) - WRONG", cch_default_int],
        ["Understatement avoided", sch_a_mort - cch_default_int]]
salt = [["SALT - income tax vs sales tax (Schedule A line 5a)", "Amount"],
        ["NC withholding (W-2 box 17)", r(NC_WH)],
        ["NC estimates paid in 2025 for 2025 (04/15, 06/16, 09/15)", 3000],
        ["NC 2024 Q4 estimate paid 01/15/2025", 900], ["NC 2024 balance due paid 04/15/2025", 640],
        ["(NC 2025 Q4 paid 01/15/2026 - deductible in 2026, not 2025)", ""],
        ["State income taxes paid in 2025", r(NC_PAID_2025)],
        [f"General sales tax: IRS table/calculator ${SALES_TAX_TABLE:,} + NC Highway Use Tax on Ioniq 5 ${HUT:,.0f} (rate <= general rate)",
         r(SALES_TAX_TABLE + HUT)],
        ["Elected: income taxes (larger); real estate tax 90% after 8829 share", sch_a_re],
        [f"Total SALT {r(NC_PAID_2025) + sch_a_re:,} < $40,000 cap (MAGI < $500,000)", ""]]
sep_ws = [["SEP-IRA maximum (self-employed rate 20%)", "Amount"], ["Schedule C net profit", NET_C],
          ["Less deductible half of SE tax", -SE["half"]], ["Net earnings for plan", NET_C - SE["half"]],
          ["x 20% = maximum SEP contribution (funded 09/18/2026, before extended due date)", SEP]]
energy = [["Credits / vehicle", "Amount"], ["Form 5695 Part I - solar PV $31,500 x 30% (expenditure 07/2025; residence; office use 10% <= 20% -> no reduction)", r(SOLAR * .30)],
          ["Form 5695 line 14 limitation - tax after other credits", "Credit fully used (no carryforward)" if not v.get("res_clean_energy_carryforward") else f"carryforward {v['res_clean_energy_carryforward']:,}"],
          ["Form 8936 clean vehicle credit - Ioniq 5 acquired 10/15/2025 (after 09/30/2025 termination)", 0],
          [f"Schedule 1-A Part IV car-loan interest ${EV_INT:,.2f} - MAGI {AGI:,} exceeds $200,000 by enough to phase out fully", v.get("13b", 0)]]
C.write_return(R, [
    ("Taxpayer / Spouse", "Owen P. Fitzgerald (XXX-XX-5582) / Chloe A. Fitzgerald (XXX-XX-7719)"),
    ("Address", ", ".join(ADDR)),
    ("Filing status", "Married filing jointly"),
    ("Dependents", "Harper (daughter, 2016) - CTC; Declan (son, 2019) - CTC"),
    ("Digital assets question", "No"),
    ("Forms included", "1040, Schedules 1, 1-A, 2, 3, 8812, A, B, C, SE; Forms 5695, 6251 (check), 8829, 8959, 8995; NC D-400"),
    ("Extension", "Form 4868 + NC D-410 filed 04/14/2026 (no payment - overpayment expected)"),
    ("Filing method", "E-file federal + NC (Form 8879 signed 09/24/2026); direct deposit First Citizens ****6620"),
], state_summary=[{
    "title": "North Carolina Form D-400 (full-year residents, MFJ) - 2025",
    "lines": [("6", "Federal adjusted gross income", AGI), ("7-10", "NC additions / deductions", 0),
              ("10b", "Child deduction (MFJ, AGI > $140,000)", nc_child),
              ("11", f"NC itemized: mortgage interest + property tax {sch_a_mort + sch_a_re:,} capped at 20,000 + charity {r(CHARITY):,} "
                     f"= {nc_item:,} vs NC standard {NC_STD:,}", nc_ded),
              ("14", "North Carolina taxable income", nc_ti), ("15", "NC income tax (4.25%)", nc_tax),
              ("16", "Tax credits (NC has no residential solar/energy credit)", 0),
              ("20a", "NC tax withheld (Owen W-2)", r(NC_WH)), ("21a", "2025 NC estimated payments (incl. 01/15/2026)", r(NC_ES_FOR_2025)),
              ("26/34", "Refund" if nc_refund >= 0 else "Tax due", abs(nc_refund))],
    "note": "NC-3/D-410 extension filed 04/14/2026. Consider NC-40 for 2026 - reduce Chloe's NC estimates (overpaid)."}],
    attachments=[("Schedule C detail", sch_c_rows), ("Form 8829 detail", f8829), ("Mortgage interest - $1M grandfathered limit", mort),
                 ("Schedule A - SALT election", salt), ("SEP-IRA computation", sep_ws), ("Energy / vehicle items", energy),
                 ("De minimis safe harbor election (Reg. 1.263(a)-1(f))",
                  "Chloe A. Fitzgerald, SSN XXX-XX-7719, Fitzgerald Advisory: the taxpayer is making the de minimis safe harbor election "
                  "under Treas. Reg. 1.263(a)-1(f) for the tax year beginning 01/01/2025.")])

gotchas = [
    gotcha("EVG1019-G1", "Schedule A - pre-2017 mortgages ($1M threshold) - manual override", "Grandfathered 2016 mortgage limited to $750k by default",
           f"Accept Axcess default: interest x 750,000/{LOAN_BAL:,} -> Schedule A {fmt(cch_default_int)}.",
           f"Acquisition debt incurred 08/19/2016 (before 12/16/2017) keeps the $1,000,000 limit; balance {fmt(LOAN_BAL)} -> 100% deductible. "
           f"Override: Schedule A line 8a {fmt(sch_a_mort)} (90% personal share).", f"Sch A understated {fmt(sch_a_mort - cch_default_int)}",
           ["Sch A 8a", "12e"], "medium"),
    gotcha("EVG1019-G2", "Schedule A / Schedule C - home office double count", "8829 share of mortgage interest and property tax left on Schedule A",
           "Deduct 10% of interest and real estate tax on Form 8829 AND 100% on Schedule A.",
           f"Schedule A gets only the 90% personal share: mortgage {fmt(sch_a_mort)}, real estate tax {fmt(sch_a_re)}; 8829 gets "
           f"{fmt(r(MORT_INT * PCT))} + {fmt(r(RE_TAX * PCT))}.", "Sch A overstated ~$3,800 if missed", ["Sch A 5b", "Sch A 8a"], "medium"),
    gotcha("EVG1019-G3", "Schedule C - Home Office Deduction (simplified vs 8829)", "Client used $5/sq ft on her P&L",
           f"Use the P&L's simplified {fmt(SIMPLIFIED)}.",
           f"Compare: Form 8829 actual {fmt(HOME_OFFICE)} (incl. depreciation {fmt(OFFICE_DEP)}) vs simplified {fmt(SIMPLIFIED)} -> use 8829. "
           "Kitchen remodel is not an office expense.", f"Sch C understated deduction {fmt(HOME_OFFICE - SIMPLIFIED)}", ["Sch C 30", "Sch 1 line 3"], "medium"),
    gotcha("EVG1019-G4", "Schedule A - income vs sales tax; large-item sales tax; refunds/timing", "SALT election and the January 2026 NC estimate",
           "Claim both NC income tax and the EV highway-use tax, or deduct all four 2025 NC estimates incl. the one paid 01/15/2026.",
           f"Income OR sales tax, not both. Income tax paid in 2025 {fmt(r(NC_PAID_2025))} (W-2 + three 2025 estimates + 2024 Q4 + 2024 "
           f"balance) > sales tax {fmt(r(SALES_TAX_TABLE + HUT))} (table + HUT as large item) -> income tax. The 01/15/2026 payment is a 2026 deduction.",
           "Sch A line 5a", ["Sch A 5a"], "medium"),
    gotcha("EVG1019-G5", "Other traps - 25D residential clean energy", "Solar credit 30%, residence with a home office",
           "Reduce the credit by the 10% home-office share, or skip it assuming it expired, or claim an NC credit.",
           f"Form 5695: $31,500 x 30% = {fmt(r(SOLAR * .30))}; business use <= 20% -> no reduction; expenditure before 12/31/2025 "
           "termination; fully usable against tax (no carryforward). NC has no solar credit. Reduce home basis by the credit.",
           "Sch 3 line 5a", ["20"], "medium"),
    gotcha("EVG1019-G6", "Other traps - clean vehicle credit termination / Schedule 1-A", "EV bought 10/15/2025",
           "Claim $7,500 Form 8936 (dealer's advice) and deduct the car-loan interest on Schedule 1-A.",
           f"30D terminated for vehicles acquired after 09/30/2025 (no binding contract/payment before) -> $0. Car-loan interest {fmt(r(EV_INT))} "
           f"qualifies in principle (new, US assembly) but MAGI {fmt(AGI)} > $200,000: reduction $200 per $1,000 -> $0.",
           "Credit overstated $7,500 if missed", ["20", "13b"], "easy"),
    gotcha("EVG1019-G7", "Schedule C - SEP IRA (compute maximum)", "SEP maximum for a sole proprietor",
           "Use 25% of net profit, or 20% of net profit without the half-SE-tax reduction.",
           f"Max = 20% x (net profit {fmt(NET_C)} - half SE tax {fmt(SE['half'])}) = {fmt(SEP)}; funded 09/18/2026 before the extended due date.",
           "Sch 1 line 16", ["10"], "medium"),
    gotcha("EVG1019-G8", "Other traps - Form 8959", "Additional Medicare on combined wages + SE earnings (MFJ)",
           "No 8959 because Owen's Medicare wages ($191,500) are under $250,000 and the employer withheld none.",
           f"MFJ threshold $250,000 applies to combined Medicare wages {fmt(r(w2t['5']))} + Chloe's SE earnings {fmt(SE['net_earnings'])} "
           f"-> 0.9% x excess = {fmt(R.forms_value('Schedule 2', '11'))}.", "Sch 2 line 11", ["23"], "medium"),
    gotcha("EVG1019-G9", "SALT - NC return", "NC itemized deduction rules and child deduction",
           "Use federal itemized total (or ignore NC's cap) and claim the NC child deduction; claim an NC solar credit.",
           f"NC itemized = mortgage + property tax capped at $20,000 + charity = {fmt(nc_item)} > NC standard $25,500; child deduction $0 "
           f"(MFJ AGI > $140,000); no NC energy credit. NC tax {fmt(nc_tax)}, refund {fmt(nc_refund)}.", "NC D-400", ["NC D-400"], "medium"),
]
C.write_answer_key(R, {"residence": "NC (Raleigh)", "complexity": "W-2 + Sch C/8829 + itemized + energy credits + NC"}, gotchas,
                   state=[{"jurisdiction": "NC D-400 (resident, MFJ)", "nc_agi": AGI, "deduction": nc_ded, "deduction_type": "NC itemized",
                           "child_deduction": nc_child, "nc_taxable_income": nc_ti, "tax": nc_tax, "payments": nc_paid,
                           "refund": nc_refund}],
                   filings=[{"form": "Form 4868 / NC D-410", "filed": "2026-04-14", "payment": 0},
                            {"form": "Form 1040", "method": "e-file", "due": "2026-10-15", "filed": "2026-09-25"},
                            {"form": "NC D-400", "method": "e-file", "due": "2026-10-15", "filed": "2026-09-25"}],
                   extra={"schedule_c": {"gross": r(GROSS), "expenses_before_8829": r(EXP_TOTAL), "form_8829": HOME_OFFICE, "net": NET_C},
                          "sep_max": SEP, "mortgage_interest_sch_a": sch_a_mort, "cch_default_750k_would_allow": cch_default_int})

C.write_receipt_log("EVG1019-1040-2025", "J. Ortiz (staff)", "L. Chen (senior)", "S. Kennedy, CPA", "2026-03-10",
                    extension="Federal 4868 + NC D-410 e-filed 04/14/2026, accepted; no payment")
C.write_notes(f"""
# EVG1019 - Fitzgerald, Owen & Chloe - 2025 Form 1040 - Preparer Notes

*Synthetic client - Project Evergreen. Return status: **signed off; federal + NC e-filed 09/25/2026 (extended), accepted.***

## Return summary
| | |
|---|---|
| Filing status | Married filing jointly (2 children) |
| Wages (Owen) | {fmt(v['1a'])} |
| Schedule C - Fitzgerald Advisory (after 8829) | {fmt(NET_C)} |
| Adjustments (half SE tax {fmt(SE['half'])} + SEP {fmt(SEP)}) | {fmt(v['10'])} |
| AGI (line 11) | {fmt(AGI)} |
| Itemized deductions | {fmt(v['12e'])} |
| QBI deduction | {fmt(v['13a'])} |
| Taxable income | {fmt(v['15'])} |
| Tax / CTC / solar credit | {fmt(v['16'])} / {fmt(v['19'])} / {fmt(v['20'])} |
| SE tax + Additional Medicare | {fmt(v['23'])} |
| Total tax | {fmt(v['24'])} |
| Payments (withholding {fmt(v['25d'])} + estimates {fmt(v['26'])}) | {fmt(v['33'])} |
| **Federal refund** | **{fmt(v['refund'])}** |
| NC D-400 | tax {fmt(nc_tax)}; paid {fmt(nc_paid)}; **refund {fmt(nc_refund)}** |

## What I did and why (plain English)
1. **Schedule C.** Gross receipts {fmt(r(GROSS))} = the three 1099-NECs using Carolina HealthSystems' CORRECTED form ($64,000 - the
   original $63,000 missed the December payment; ties to Chloe's P&L). Book-to-tax changes to her P&L: meals 50%; cell phone 60% of her
   line; laptop expensed under the **de minimis safe harbor election** (statement attached); added **1/3 of the 2024 prep fee** we billed
   ($900 - Sch C is about a third of the return time; the other 2/3 is a nondeductible personal expense); replaced her $5/sq ft home
   office with Form 8829.
2. **Home office - Form 8829 vs simplified.** Office 300/3,000 sq ft = 10%. Actual method: 10% of mortgage interest, real estate tax,
   insurance, utilities and HVAC repair + depreciation {fmt(OFFICE_DEP)} (39-yr, basis $92,000) = **{fmt(HOME_OFFICE)}** vs simplified
   {fmt(SIMPLIFIED)} -> used 8829. The kitchen remodel has nothing to do with the office. Future sale: {fmt(PRIOR_OFFICE_DEP + OFFICE_DEP)}
   accumulated office depreciation will be taxed as unrecaptured 1250 gain (not excludable under 121).
3. **No double counting.** Because 10% of the interest and property tax is on 8829, Schedule A only gets the 90% personal share
   (mortgage {fmt(sch_a_mort)}, real estate tax {fmt(sch_a_re)}).
4. **Mortgage interest - $1M grandfathered limit.** The loan is $960,000 acquisition debt from 08/19/2016 (before 12/16/2017), so the old
   $1,000,000 limit applies. It is interest-only; the balance was $872,000 all year (under $1M) -> 100% deductible. Axcess defaults to the
   $750,000 limit (would allow {fmt(cch_default_int)}); I **overrode** the limitation with the manual computation (tape in WP 14) -
   {fmt(sch_a_mort - cch_default_int)} more deduction. Heads-up for 2026: the loan resets to amortizing in 10/2026 - no new debt, still grandfathered.
5. **SALT.** NC income tax actually paid in 2025 = {fmt(r(NC_PAID_2025))} (W-2 withholding $7,350 + 2025 estimates paid 04/15, 06/16,
   09/15 + the 2024 Q4 estimate paid 01/15/2025 + the 2024 balance paid 04/15/2025). The 2025 Q4 estimate paid 01/15/2026 is a 2026
   deduction. Sales tax alternative = IRS calculator ${SALES_TAX_TABLE:,} (*assumption: calculator figure, Wake County 7.25%*) + the 3% NC
   Highway Use Tax on the Ioniq 5 ${HUT:,.0f} (a motor-vehicle tax at a rate not above the general rate counts as a large-item addition)
   = {fmt(r(SALES_TAX_TABLE + HUT))} -> income tax is larger. You can't take both. Total SALT {fmt(r(NC_PAID_2025) + sch_a_re)} is under the
   $40,000 cap (MAGI under $500,000).
6. **Solar (Form 5695).** $31,500 system on the main home, installed/paid 07/22/2025 -> 30% = **{fmt(r(SOLAR * .30))}**. The office is only
   10% of the home (20% or less business use -> no reduction). 25D ends for expenditures after 12/31/2025, but this one qualifies; the
   credit is fully absorbed by their tax, so no carryforward. NC has no solar credit (answered Chloe's email). Home basis +$31,500 - $9,450.
7. **EV - no credit.** Ioniq 5 buyer's order dated 10/15/2025 with no prior binding contract or payment -> acquired after 09/30/2025 ->
   clean vehicle credit terminated ($0) even though it is a new, US-assembled car; the dealer's comment was wrong. The new car-loan interest
   deduction ({fmt(r(EV_INT))}) is fully phased out at MAGI {fmt(AGI)} ($200 per $1,000 over $200,000 MFJ) - shown on Schedule 1-A as $0.
8. **SEP-IRA.** Chloe wanted the maximum: 20% x (net profit {fmt(NET_C)} - half SE tax {fmt(SE['half'])}) = **{fmt(SEP)}**; she funded it
   09/18/2026, before the 10/15/2026 extended due date.
9. **QBI.** Consulting is an SSTB, but taxable income before QBI is below $394,600 (MFJ), so the SSTB rule doesn't bite: 20% x
   (net profit - half SE - SEP = {fmt(NET_C - SE['half'] - SEP)}) = {fmt(v['13a'])}.
10. **Additional Medicare (Form 8959).** MFJ threshold $250,000 is applied to Owen's Medicare wages ($191,500) plus Chloe's SE earnings
    ({fmt(SE['net_earnings'])}) -> 0.9% of the excess = {fmt(R.forms_value('Schedule 2', '11'))}. Owen's employer withheld none (his wages < $200k).
11. **CTC.** Two children under 17 -> $4,400; AGI far below $400,000.
12. **AMT** checked on Form 6251 - none.
13. **NC D-400.** NC starts from federal AGI (no adjustments). NC itemized = mortgage interest + property tax **capped at $20,000** +
    charity = {fmt(nc_item)} vs NC standard $25,500 -> NC itemized. NC child deduction is $0 at AGI over $140,000 (MFJ). No NC credit for
    solar. Tax 4.25% = {fmt(nc_tax)}; NC withholding + 2025 estimates (including the 01/15/2026 one - it counts for the 2025 NC return)
    {fmt(nc_paid)} -> refund {fmt(nc_refund)}. The NC 529 statement is informational (NC has no 529 deduction).

## Hand-verification
- SE tax: {NET_C:,} x 92.35% = {SE['net_earnings']:,} x 15.3% = {SE['se_tax']:,}; half = {SE['half']:,}.
- Tax on {fmt(v['15'])} (MFJ, schedule) = {fmt(v['16'])}; less CTC {fmt(v['19'])} and solar {fmt(v['20'])}; + SE/8959 {fmt(v['23'])} = {fmt(v['24'])}.

## Open items / client communication
- None open. Suggested reducing Chloe's NC estimates for 2026 (NC overpaid) and noted the mortgage will begin amortizing 10/2026.

## Hand-off to signer / routing
- [x] Return locked; Accountant's Copy saved as *reviewed*
- [x] Federal 1040 (extended) - e-file; due 10/15/2026
- [x] NC D-400 (extended via D-410) - e-file; due 10/15/2026
- [x] No FBAR; SEP contribution confirmation in WP
- [x] eSign (8879 + NC-8879) - Chloe, chloe@fitzgeraldadvisory.example
- [x] Direct deposit First Citizens ****6620
- Billing: quote $3,200; actual in line. No W/O.
""")
C.write_review_points(f"""
# Review Points - EVG1019 - 2025 - Form 1040

*Reviewer: L. Chen (blue). Preparer responses in red. Synthetic.*

1. **Schedule A line 8a** - Axcess applied the $750,000 limit (interest {fmt(cch_default_int)}). 2016 acquisition debt - $1M grandfathered.
   Override with the manual calc; tape the calc on the 1098 page.
   - *Preparer: Overridden to {fmt(sch_a_mort)}; tape added (WP 14).*
2. **Form 8829 / Schedule A** - Draft left 100% of mortgage interest and real estate tax on Schedule A while 10% is on 8829. Remove the 8829 share.
   - *Preparer: Done - Sch A shows 90%.*
3. **Schedule C line 30** - Draft used Chloe's $1,500 simplified figure. Compare with 8829 per procedure.
   - *Preparer: 8829 {fmt(HOME_OFFICE)} > $1,500 - switched.*
4. **Schedule A line 5a** - Draft included the 01/15/2026 NC estimate and ALSO added the EV highway-use tax. Pick income OR sales tax; cash-basis timing.
   - *Preparer: Income tax {fmt(r(NC_PAID_2025))}; HUT removed (used only in the comparison).*
5. **Form 8936** - Remove the $7,500 clean vehicle credit (acquired 10/15/2025). Show Sch 1-A car interest phased out.
   - *Preparer: Removed; Sch 1-A = $0.*
6. **Schedule 1 line 16** - SEP draft used 25% of net profit. Use the self-employed rate (20% of net profit less half SE).
   - *Preparer: {fmt(SEP)}; Chloe funded 09/18.*
7. **Form 8959** - Missing. Combine SE earnings with Owen's wages for the $250k MFJ threshold.
   - *Preparer: Added ({fmt(R.forms_value('Schedule 2', '11'))}).*
8. **NC D-400** - Draft used federal itemized total. NC caps mortgage + property tax at $20,000; child deduction $0 at this AGI.
   - *Preparer: Fixed; NC itemized {fmt(nc_item)}.*
9. FYI - Prep fee proration: 1/3 to Sch C per procedure; laptop via de minimis election (statement attached).
""")
print("EVG1019 done", AGI, v["15"], v["24"], v["refund"], v["balance_due"], "NC", nc_tax, nc_refund)
