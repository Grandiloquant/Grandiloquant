"""EVG1006 - Carlos & Maria Mendoza (MFJ, Texas - San Antonio). Landscaping Schedule C kept in QuickBooks on the
accrual basis (convert to cash), book-tax differences (meals, gifts, club dues, personal items), de minimis safe harbor
(mower) vs bonus depreciation (used trailer), truck actual expenses on the PERM depreciation schedule, unfiled
1099-NECs for two helpers, prior-year prep-fee proration, SEP-IRA maximum, SE health insurance barred by the spouse's
subsidized employer plan, teacher's-aide educator expense, and Carlos' mother as a qualifying relative (ODC)."""
from common import ClientBuild, gotcha, fmt
from docs import statement, scanned_pages, write_text, write_xlsx
import forms as F
from tax2025 import Return1040, r, se_tax, MACRS_HY

C = ClientBuild("EVG1006", "Mendoza", "Carlos & Maria Mendoza")
ADDR = ("7318 Mesquite Bend", "San Antonio, TX 78250")
T = {"name": "Carlos A. Mendoza", "ssn": "XXX-XX-5208", "dob": "1983-07-19"}
S = {"name": "Maria L. Mendoza", "ssn": "XXX-XX-6634", "dob": "1985-02-26"}
REC_T = [T["name"], *ADDR, f"TIN: {T['ssn']}"]
REC_J = ["Carlos A. & Maria L. Mendoza", *ADDR, f"TIN: {T['ssn']}"]
BIZ = "Mendoza Lawn & Landscape LLC"
BIZ_EIN = "00-3381945"
REC_BIZ = [BIZ, "c/o Carlos A. Mendoza", *ADDR, f"TIN: {BIZ_EIN}"]

# ================================================================== key facts (all judgement calls here)
# --- QuickBooks (accrual) revenue -> cash receipts
REV_RES, REV_COM = 128650.00, 57750.00
BOOK_REV = REV_RES + REV_COM                      # 186,400 accrual revenue
AR_BEG, AR_END = 6200.00, 16000.00                # A/R 12/31/2024 and 12/31/2025 (A/P zero both dates)
CASH_REV = BOOK_REV - (AR_END - AR_BEG)           # 176,600 cash-basis gross receipts

# --- truck (2022 Ford F-250, >6,000 lb GVWR -> no 280F caps), 85% business per mileage log, MACRS 5-yr HY, no bonus
TRUCK_COST, TRUCK_BUS = 52000.00, 0.85
TRUCK_MILES_TOTAL, TRUCK_MILES_BUS = 18400, 15640
TRUCK_EXP = {"Fuel - truck": 6860.00, "Repairs - truck": 1920.00, "Insurance - truck": 2460.00, "Registration/inspection": 310.00}
truck_exp_total = sum(TRUCK_EXP.values())
truck_ded = r(truck_exp_total * TRUCK_BUS)
truck_basis = TRUCK_COST * TRUCK_BUS
truck_dep = [r(truck_basis * x) for x in MACRS_HY[5]]      # 2022..2027
TRUCK_DEP_2025 = truck_dep[3]
TRUCK_DEP_PRIOR = sum(truck_dep[:3])
TRAILER_COST = 6500.00                            # used 2019 trailer bought 03/22/2025 -> 100% bonus (acq. after 01/19/2025)
MOWER_COST = 2300.00                              # new zero-turn mower 05/06/2025 -> de minimis safe harbor (<= $2,500)
SMALL_TOOLS = 1240.00

# --- book expense accounts (as in QuickBooks)
BOOK = [  # (account, amount, tax treatment key)
    ("Advertising & marketing", 1480.00, "adv"),
    ("Bank & merchant fees (Square)", 1690.00, "oth_merchant"),
    ("Contract labor", 12500.00, "labor"),
    ("Dues & subscriptions - Oak Hills Country Club", 4200.00, "club"),
    ("Dues & subscriptions - TX Nursery & Landscape Assn", 250.00, "oth_dues"),
    ("Dues & subscriptions - Netflix", 275.88, "personal"),
    ("Equipment rental", 1350.00, "rent_eq"),
    ("Equipment repairs & maintenance", 3860.00, "repairs"),
    ("Fuel - mowers & equipment", 3420.00, "oth_fuel"),
    ("Gifts - customers (12 x $75 gift cards)", 900.00, "gifts"),
    ("Insurance - general liability", 3150.00, "ins"),
    ("Insurance - health (BCBS family PPO)", 14400.00, "health"),
    ("Legal & professional (bookkeeper year-end)", 900.00, "legal"),
    ("Meals", 3140.00, "meals"),
    ("Materials - plants, mulch, stone, fertilizer", 28400.00, "supplies"),
    ("Office & software (QuickBooks Online)", 920.00, "office"),
    ("Miscellaneous (Alamo Youth Soccer - kids)", 640.00, "personal"),
    ("Rent - storage yard (Leon Valley)", 4800.00, "rent_other"),
    ("Small tools & equipment - hand tools/trimmers", SMALL_TOOLS, "supplies"),
    ("Small tools & equipment - Exmark zero-turn mower", MOWER_COST, "deminimis"),
    ("Taxes & licenses (TX irrigator lic., COSA permits)", 385.00, "taxes"),
    ("Telephone - AT&T family plan (4 lines)", 2280.00, "phone"),
    ("Truck - fuel", TRUCK_EXP["Fuel - truck"], "truck"),
    ("Truck - repairs", TRUCK_EXP["Repairs - truck"], "truck"),
    ("Truck - insurance", TRUCK_EXP["Insurance - truck"], "truck"),
    ("Truck - registration/inspection", TRUCK_EXP["Registration/inspection"], "truck"),
    ("Uniforms & safety gear", 410.00, "oth_uniform"),
    ("Dump / disposal fees", 1120.00, "oth_dump"),
]
BOOK_EXP = sum(a for _, a, _ in BOOK)
BOOK_NET = BOOK_REV - BOOK_EXP
PHONE_BUS = 570.00           # Carlos' own line (1 of 4); the 3 family lines are personal
GIFT_ALLOWED = 12 * 25.00    # $25 per recipient per year (sec. 274(b))
PY_PREP_FEE = 1650.00        # 2024 return prep fee paid 04/2025 from joint personal checking (not in books)
PREP_SCH_C = r(PY_PREP_FEE / 3)   # time records: ~1 of 3 hours on Schedule C

tax_by = {}
def add(k, v):
    tax_by[k] = tax_by.get(k, 0) + v
for acct, amt, k in BOOK:
    if k in ("personal", "club", "health"):
        continue
    if k == "meals":
        add("meals", amt * 0.5)
    elif k == "gifts":
        add("oth_gifts", GIFT_ALLOWED)
    elif k == "phone":
        add("util", PHONE_BUS)
    elif k == "truck":
        continue
    else:
        add(k, amt)
add("legal", PREP_SCH_C)

SCH_C_LINES = [  # (line, description, amount)
    ("1", "Gross receipts (cash basis)", r(CASH_REV)),
    ("8", "Advertising", r(tax_by["adv"])),
    ("9", f"Car and truck expenses (actual; 85% business of ${truck_exp_total:,.0f})", truck_ded),
    ("11", "Contract labor", r(tax_by["labor"])),
    ("13", "Depreciation and section 179 (Form 4562)", TRUCK_DEP_2025 + r(TRAILER_COST)),
    ("15", "Insurance (other than health)", r(tax_by["ins"])),
    ("17", "Legal and professional services", r(tax_by["legal"])),
    ("18", "Office expense", r(tax_by["office"])),
    ("20a", "Rent - vehicles, machinery, and equipment", r(tax_by["rent_eq"])),
    ("20b", "Rent - other business property", r(tax_by["rent_other"])),
    ("21", "Repairs and maintenance", r(tax_by["repairs"])),
    ("22", "Supplies (landscape materials, small tools)", r(tax_by["supplies"])),
    ("23", "Taxes and licenses", r(tax_by["taxes"])),
    ("24b", "Deductible meals (50%)", r(tax_by["meals"])),
    ("25", "Utilities (Carlos' business cell line)", r(tax_by["util"])),
]
OTHER_C = [("Equipment fuel (mowers/trimmers)", r(tax_by["oth_fuel"])), ("Dump / disposal fees", r(tax_by["oth_dump"])),
           ("Merchant / card processing fees", r(tax_by["oth_merchant"])), ("Uniforms & safety gear", r(tax_by["oth_uniform"])),
           ("Business gifts (12 x $25 limit)", r(tax_by["oth_gifts"])), ("Trade association dues (TNLA)", r(tax_by["oth_dues"])),
           ("Small equipment - de minimis safe harbor (zero-turn mower)", r(tax_by["deminimis"]))]
other_c_total = sum(a for _, a in OTHER_C)
SCH_C_LINES.append(("27a", "Other expenses (Part V)", other_c_total))
sch_c_exp = sum(a for ln, _, a in SCH_C_LINES if ln != "1")
SCH_C_NET = r(CASH_REV) - sch_c_exp
SCH_C_LINES += [("28", "Total expenses", sch_c_exp), ("31", "Net profit", SCH_C_NET)]

# --- SE tax, SEP, QBI
SE = se_tax(SCH_C_NET, 0)
SEP_COMP = SCH_C_NET - SE["half"]                 # net earnings from SE for plan purposes (net profit - 1/2 SE tax)
SEP_MAX = min(r(SEP_COMP * 0.20), 70000)          # 25% of compensation = 20% of (net profit - 1/2 SE tax)
QBI_AMT = SCH_C_NET - SE["half"] - SEP_MAX        # QBI reduced by deductible 1/2 SE tax and SEP (Reg. 1.199A-3(b)(1)(vi))

# --- Maria W-2 (Mission Creek ISD - district does not participate in Social Security; TRS 414(h) pick-up)
w2_m = {"1": 29360.00, "2": 1380.00, "3": "", "4": "", "5": 32000.00, "6": 464.00,
        "14": [("TRS 414(h)", 2640.00), ("SEC125 MED", 1920.00)], "13": ["Retirement plan: X"], "control": "MCISD-04471"}
INT_FROST = 212.40
EDU_RECEIPTS = 410.00
HEALTH_PREM = 14400.00
OOP_MED = 2860.00
PROP_TAX, MORT_INT, CHARITY, SALES_TAX_TABLE = 6420.00, 8640.00, 2400.00, 2150.00
EST_PAID = [("04/15/2025", 2500.00), ("06/16/2025", 2500.00), ("09/15/2025", 2500.00), ("01/15/2026", 2500.00)]
EXT_PAY = 1500.00
ROSA_SS, ROSA_INT = 14200.00, 85.16

# ================================================================== PERM
C.write_profile(f"""
# EVG1006 - Mendoza, Carlos & Maria  (PERM)

*Synthetic client - Project Evergreen training data.*

| Item | Detail |
|---|---|
| Client ID | EVG1006 |
| Taxpayer | Carlos A. Mendoza, DOB 07/19/1983, SSN XXX-XX-5208 - owner, {BIZ} (single-member LLC, disregarded; EIN {BIZ_EIN}) |
| Spouse | Maria L. Mendoza, DOB 02/26/1985, SSN XXX-XX-6634 - instructional aide (teacher's aide), Mission Creek ISD (K-5), full-time |
| Address | {ADDR[0]}, {ADDR[1]} (Bexar County) - **Texas: no individual income tax** |
| Dependents (PY) | Sofia Mendoza (daughter, DOB 10/04/2013); Mateo Mendoza (son, DOB 05/22/2017) |
| Household | Carlos' mother **Rosa Mendoza** (DOB 12/01/1955, SSN XXX-XX-1187) moved in 09/2024 after Carlos' father died; her only income is her own Social Security. Not claimed in 2024 (lived with them < 12 months and we did not have a support worksheet) - revisit for 2025. |
| Business | Residential & HOA landscaping / lawn maintenance, NAICS 561730. Started 2016. **Books: QuickBooks Online, ACCRUAL basis** (bookkeeper: Delia Ruiz, Ruiz Bookkeeping). **Tax return: CASH basis** (method used since 2016 - no Form 3115). No employees - seasonal helpers paid as contractors. |
| Vehicles / assets | See `Depreciation_Schedule_Mendoza_Lawn.pdf` (2022 F-250 on MACRS, actual-expense method since 2022; 2023 Exmark mower expensed under sec. 179). |
| Contact | Carlos - carlos.mendoza@example.com, (210) 555-0187 (text OK). Maria for household docs - maria.mendoza@example.com. eSign OK. |
| Engagement | Client since 2019. Sch C tier (quote $1,650; PY actual $1,650 paid 04/2025). Time records: ~1/3 of prep time is Schedule C. |
| Retirement | SEP-IRA at Schwab (acct ****7120) opened 2020; Carlos contributes the maximum each year after we compute it. |
| Payment info | Voided check on file - Frost Bank joint checking ****4410 |
""")
F.prior_year_summary(C.perm_file("2024_Form_1040_Return_Summary.pdf", "Prior-year return summary"), "Carlos & Maria Mendoza",
    "EVG1006", "Married filing jointly", [
        ["1a", "W-2 wages (Mission Creek ISD - Maria)", 28410],
        ["2b", "Taxable interest - Frost Bank", 198],
        ["Sch C 31", f"Net profit - {BIZ} (cash basis)", 71320],
        ["Sch 1 11", "Educator expenses (Maria)", 300],
        ["Sch 1 15", "Deductible part of SE tax", 5038],
        ["Sch 1 16", "SEP-IRA (computed maximum; funded 04/10/2025)", 13256],
        ["11", "AGI", 81334], ["12", "Standard deduction", 29200], ["13", "QBI deduction", 10427],
        ["15", "Taxable income", 41707], ["19", "Child tax credit (2 children)", 4000],
        ["Sch 2 4", "Self-employment tax", 10077], ["24", "Total tax", 10620], ["25", "Withholding (Maria)", 1310],
        ["26", "2024 estimated tax payments", 9000], ["37", "Amount owed with return", 310]],
    carryovers=[["None", 0]],
    notes="PY WP: (1) QuickBooks is on the accrual basis - convert revenue to cash using the A/R aging each year "
          "(A/R 12/31/2024 per aging report $6,200; A/P nil). (2) Proposed AJE #1 sent to Ruiz Bookkeeping 04/08/2025: "
          "Dr Depreciation expense 8,486 / Cr Accumulated depreciation - F-250 8,486 (2024 depreciation per our schedule) - "
          "bookkeeper to post. (3) 2024: Carlos & kids were covered on Maria's district plan - no SE health insurance. "
          "(4) Carlos paid helpers < $600 each in 2024 - no 1099s needed. (5) Prep fee $1,650; 1/3 to Sch C next year when paid.")
statement(C.perm_file("Depreciation_Schedule_Mendoza_Lawn.pdf", "Fixed asset / depreciation schedule (tax)"),
    f"{BIZ} - Tax Depreciation Schedule (through 12/31/2024)", [
        {"table": [["Asset", "Placed in service", "Cost", "Bus. %", "Method / life", "Sec. 179 / bonus", "Prior depreciation", "Accum. 12/31/2024"],
                   ["2022 Ford F-250 XL (GVWR 10,000 lb) - VIN 1FT7W2BN5NEC20117", "03/14/2022", TRUCK_COST, "85%",
                    "MACRS 200DB HY 5-yr", "Elected out of bonus (2022)", f"2022 {truck_dep[0]:,}; 2023 {truck_dep[1]:,}; 2024 {truck_dep[2]:,}", TRUCK_DEP_PRIOR],
                   ["2023 Exmark Lazer Z 60in commercial mower", "04/03/2023", 11800.00, "100%", "Sec. 179", "179: 11,800", "2023 11,800", 11800.00]],
         "left_align_cols": [0, 1, 3, 4, 5, 6]},
        {"note": ["Truck: actual-expense method used since 2022 (MACRS claimed) - standard mileage rate may not be used for this vehicle "
                  "(Rev. Proc. 2019-46 sec. 4.05). Business % from annual mileage log. Listed property - Form 4562 Part V each year.",
                  "Remaining truck depreciation (85% basis 44,200): 2025 11.52%, 2026 11.52%, 2027 5.76%."]}])

# ================================================================== PBC documents
EMP_M = {"name": "Mission Creek Independent School District", "addr1": "5900 Evers Rd", "addr2": "San Antonio, TX 78238", "ein": "00-6002114"}
EE_M = {"name": S["name"], "addr1": ADDR[0], "addr2": ADDR[1], "ssn": S["ssn"]}

F.organizer(C.pbc_file("01_2025_Organizer_completed.pdf", "Client organizer", "2026-03-09"), "Carlos & Maria Mendoza", "EVG1006",
    general=[("Did your marital status change during 2025?", "No", ""),
             ("Were there any changes in dependents or household members?", "Yes", "My mom Rosa lives with us full time (since 9/2024). Her only income is her social security (form attached)"),
             ("Did you receive any Forms 1099-INT/DIV/B?", "Yes", "Frost Bank"),
             ("Do you operate a business (Schedule C)?", "Yes", "Mendoza Lawn &amp; Landscape - QuickBooks P&amp;L sent by Delia (bookkeeper)"),
             ("Did you make any payments in 2025 that would require you to file Form(s) 1099?", "Yes", "Paid Jose and Luis to help in spring/summer"),
             ("If yes, did you or will you file all required Forms 1099?", "No", "Didnt know I had to - I paid them by Zelle"),
             ("Did you buy or sell business equipment or vehicles?", "Yes", "New Exmark zero turn (May) and a used trailer (March)"),
             ("Did you pay health insurance premiums?", "Yes", "BCBS family PPO for me + kids $1,200/mo. Maria is on her school plan"),
             ("Do you want to make the maximum SEP-IRA contribution?", "Yes", "Max again - tell me the number"),
             ("Did you make estimated tax payments?", "Yes", "4 x $2,500 federal"),
             ("Did you receive, sell, exchange digital assets?", "No", ""),
             ("Educator expenses (K-12 teacher, aide, counselor)?", "Yes", "Maria - classroom supplies $410 receipts"),
             ("Would you like to file an extension?", "Yes", "Need more time for books")],
    dependents=[["Sofia Mendoza", "Daughter", "10/04/2013", "3390", "12", "No"],
                ["Mateo Mendoza", "Son", "05/22/2017", "8812", "12", "No"],
                ["Rosa Mendoza", "Mother (Carlos)", "12/01/1955", "1187", "12", "No"]],
    income_rows=[["Wages", "Mission Creek ISD (Maria)", 28410, "see W-2"],
                 ["Interest", "Frost Bank", 198, "212.40"],
                 ["Business income", BIZ, 71320, "see P&L from QuickBooks"],
                 ["Social security", "Rosa (mother)", "", "14,200 (hers)"]],
    deductions_rows=[["Estimated tax", "Federal 2025", 9000, "10,000"],
                     ["SEP-IRA", "Schwab ****7120", 13256, "max"],
                     ["Health insurance", "BCBS family PPO (Carlos + kids)", "", "14,400"],
                     ["Medical / dental out of pocket", "Sofia braces etc.", 1150, "2,860"],
                     ["Mortgage interest", "Lone Oak Mortgage", 8910, "see 1098"],
                     ["Real estate tax", "Bexar County", 6180, "6,420"],
                     ["Charitable - cash", "St. Brigid Parish", 2200, "2,400"],
                     ["Tax preparation fee", "Evergreen Tax (paid 04/2025)", "", "1,650"]],
    signature_date="03/07/2026")
F.w2(C.pbc_file("02_W-2_Mission_Creek_ISD_Maria.pdf", "Form W-2", "2026-03-09"), EMP_M, EE_M, w2_m,
     notes=["Box 3/4: District does not participate in Social Security (TRS member). Box 14 TRS 414(h) = employee "
            "Teacher Retirement System contribution picked up under IRC 414(h)(2)."])
F.f1099_int(C.pbc_file("03_1099-INT_Frost_Bank.pdf", "Form 1099-INT", "2026-03-09"),
            ["Frost Bank", "PO Box 1600", "San Antonio, TX 78296", "TIN: 00-0000013"], REC_J, {"1": INT_FROST}, account="****4410")
F.f1099_k(C.pbc_file("04_1099-K_Square_Mendoza_Lawn.pdf", "Form 1099-K", "2026-03-09"),
          ["Block, Inc. (Square)", "1955 Broadway, Suite 600", "Oakland, CA 94612", "TIN: 00-0000029"], REC_BIZ,
          {"1a": 61240.18, "1b": 8310.00, "2": "0780", "3": 318,
           "months": [1820.00, 2460.50, 5230.00, 6480.25, 7120.00, 6940.40, 6310.00, 6015.63, 5630.00, 5480.40, 4090.00, 3663.00]},
          account="SQ-MLL-2291")
F.f1099_nec(C.pbc_file("05_1099-NEC_Stone_Oak_HOA.pdf", "Form 1099-NEC", "2026-03-09"),
            ["Stone Oak Ranch Homeowners Association", "c/o Brightline Community Mgmt", "20626 Stone Oak Pkwy, San Antonio, TX 78258",
             "TIN: 00-7120094"], REC_BIZ, {"1": 24000.00})
F.f1099_nec(C.pbc_file("06_1099-NEC_Alamo_Property_Mgmt.pdf", "Form 1099-NEC", "2026-03-09"),
            ["Alamo Heights Property Management LLC", "5150 Broadway St Ste 400", "San Antonio, TX 78209", "TIN: 00-5581320"],
            REC_T, {"1": 18500.00})

# QuickBooks export (accrual)
pl_rows = [["Mendoza Lawn & Landscape LLC - Profit and Loss - January through December 2025 - ACCRUAL BASIS", ""],
           ["Income", ""], ["  Landscaping services - residential", REV_RES], ["  Commercial / HOA maintenance contracts", REV_COM],
           ["Total Income", BOOK_REV], ["Expenses", ""]]
for acct, amt, _ in BOOK:
    pl_rows.append([f"  {acct}", amt])
pl_rows += [["  Depreciation expense", 0.00], ["Total Expenses", round(BOOK_EXP, 2)], ["Net Income", round(BOOK_NET, 2)]]
gl = [["Date", "Type", "Num", "Name", "Memo", "Account", "Debit", "Credit"]]
gl_items = [
    ("01/10/2025", "Check", "EFT", "Oak Hills Country Club", "Annual dues - family membership", "Dues & subscriptions - Oak Hills Country Club", 4200.00),
    ("Monthly", "Expense", "ACH", "Netflix", "Streaming 22.99 x 12", "Dues & subscriptions - Netflix", 275.88),
    ("02/03/2025", "Check", "1188", "Alamo Youth Soccer Assn", "Spring + fall registration Sofia & Mateo", "Miscellaneous (Alamo Youth Soccer - kids)", 640.00),
    ("Monthly", "Expense", "ACH", "AT&T Mobility", "Family plan 4 lines 190.00 x 12", "Telephone - AT&T family plan (4 lines)", 2280.00),
    ("Monthly", "Expense", "ACH", "Blue Cross Blue Shield of TX", "Family PPO - Carlos, Sofia, Mateo 1,200 x 12", "Insurance - health (BCBS family PPO)", 14400.00),
    ("03/22/2025", "Check", "1204", "Ray Delgado", "Used 16ft tandem landscape trailer (2019 Big Tex)", "Fixed assets - Trailer", 6500.00),
    ("05/06/2025", "Expense", "Visa", "Alamo Power Equipment", "Exmark Radius S 52in zero-turn - inv 55120", "Small tools & equipment - Exmark zero-turn mower", MOWER_COST),
    ("Various", "Zelle", "", "Jose Ramirez", "Helper - 32 days spring/summer (Zelle)", "Contract labor", 8000.00),
    ("Various", "Zelle", "", "Luis Garza", "Helper - Jun-Sep (Zelle/cash)", "Contract labor", 4500.00),
    ("12/2025", "Expense", "Visa", "H-E-B / Amazon", "12 x $75 gift cards - HOA managers & top customers", "Gifts - customers (12 x $75 gift cards)", 900.00),
    ("Various", "Expense", "Visa", "Various restaurants", "Client lunches / crew lunches", "Meals", 3140.00),
    ("12/31/2025", "Invoice", "2025-311", "Stone Oak Ranch HOA", "December maintenance (paid 01/09/2026)", "Accounts Receivable", 9000.00),
]
for d, ty, num, nm, memo, acct, amt in gl_items:
    col = (amt, "") if acct != "Accounts Receivable" else (amt, "")
    gl.append([d, ty, num, nm, memo, acct, *col])
bs = [["Balance Sheet as of", "12/31/2024 (per QB)", "12/31/2025 (per QB)"],
      ["Frost Bank - business checking ****8830", 11840.22, 14215.60],
      ["Accounts Receivable", AR_BEG, AR_END],
      ["Fixed assets - 2022 F-250", TRUCK_COST, TRUCK_COST],
      ["Fixed assets - 2023 Exmark mower", 11800.00, 11800.00],
      ["Fixed assets - Trailer", 0.00, TRAILER_COST],
      ["Accumulated depreciation", -(truck_dep[0] + truck_dep[1] + 11800), -(truck_dep[0] + truck_dep[1] + 11800)],
      ["Accounts Payable", 0.00, 0.00],
      ["Owner's equity - Retained earnings (QB)", "see note", "see note"],
      ["NOTE (bookkeeper)", "Accum. depr. still excludes 2024 depreciation 8,486 - AJE #1 not posted", ""]]
aging = [["Customer", "Current", "1-30", "31-60", "61-90", ">90", "Total 12/31/2025"],
         ["Stone Oak Ranch HOA", 9000.00, 0, 0, 0, 0, 9000.00],
         ["Alamo Heights Property Mgmt", 4200.00, 0, 0, 0, 0, 4200.00],
         ["Residential - various (14)", 1650.00, 850.00, 300.00, 0, 0, 2800.00],
         ["TOTAL", 14850.00, 850.00, 300.00, 0, 0, AR_END],
         ["A/R at 12/31/2024 per PY aging", "", "", "", "", "", AR_BEG]]
write_xlsx(C.pbc_file("07_QuickBooks_PL_GL_2025_Mendoza_Lawn.xlsx", "QuickBooks export (P&L, GL detail, balance sheet, A/R aging)",
                      "2026-03-09", "Email from bookkeeper (Ruiz Bookkeeping)"),
           {"P&L 2025 (Accrual)": pl_rows, "GL Detail (selected)": gl, "Balance Sheet": bs, "AR Aging 12-31-2025": aging})
statement(C.pbc_file("08_BCBS_TX_2025_Premium_Statement.pdf", "Insurance premium statement", "2026-03-09"),
    "Blue Cross Blue Shield of Texas - 2025 Premium Payment Summary (Individual & Family PPO - off-Marketplace)", [
        {"table": [["Field", "Value"], ["Subscriber", "Carlos A. Mendoza"], ["Covered members", "Carlos, Sofia, Mateo"],
                   ["Plan", "Blue Choice PPO Silver 2500 (purchased directly - not through HealthCare.gov; no APTC)"],
                   ["Coverage period", "01/01/2025 - 12/31/2025"], ["Monthly premium", 1200.00], ["Total premiums paid 2025", HEALTH_PREM],
                   ["Paid by", "Autodraft - Frost Bank ****8830 (Mendoza Lawn & Landscape LLC)"]], "left_align_cols": [0, 1]},
        {"para": "No Form 1095-A will be issued (off-exchange policy). Form 1095-B available on request."}])
statement(C.pbc_file("09_Mission_Creek_ISD_2025_Benefits_Enrollment_Maria.pdf", "Employer benefits confirmation", "2026-03-09"),
    "Mission Creek ISD - 2025 Benefits Confirmation Statement - Maria L. Mendoza (Employee ID 44710)", [
        {"table": [["Benefit", "Coverage tier elected", "Employee cost / month", "District contribution / month"],
                   ["TRS-ActiveCare Primary medical", "Employee only", 160.00, 450.00],
                   ["Dental (Delta)", "Employee only", 22.40, 0.00], ["Vision", "Employee only", 6.10, 0.00]],
         "left_align_cols": [0, 1]},
        {"heading": "2025 medical premium grid (all tiers available to eligible employees)",
         "table": [["Tier", "Total premium", "District contribution", "Employee cost"],
                   ["Employee only", 610.00, 450.00, 160.00], ["Employee + spouse", 1450.00, 450.00, 1000.00],
                   ["Employee + children", 1090.00, 450.00, 640.00], ["Employee + family", 1860.00, 450.00, 1410.00]]},
        {"para": "Eligible dependents: legal spouse and children under 26. Open enrollment 08/2024 for plan year 01/01/2025-12/31/2025. "
                 "Employee declined spouse and child coverage. Mid-year changes only for qualifying life events."}])
F.f1098(C.pbc_file("10_1098_Lone_Oak_Mortgage.pdf", "Form 1098", "2026-03-09"),
        ["Lone Oak Mortgage Company", "PO Box 790041", "Fort Worth, TX 76179", "TIN: 00-8124460"], REC_J,
        {"1": MORT_INT, "2": 236412.10, "3": "06/12/2019", "7": "Yes", "8": ADDR[0], "9": "1", "10": f"RE taxes paid from escrow {PROP_TAX:,.2f}"})
F.ssa_1099(C.pbc_file("11_SSA-1099_Rosa_Mendoza.pdf", "Form SSA-1099", "2026-03-09", note="beneficiary: Rosa Mendoza"),
           ["Rosa Mendoza", "XXX-XX-1187"], {"3": ROSA_SS, "4": 0, "5": ROSA_SS, "7": "7318 Mesquite Bend, San Antonio TX 78250",
           "desc": ["Description of amount in box 3: Paid by check or direct deposit $12,977.20; Medicare Part B premiums deducted "
                    "from your benefits $1,222.80. Total additions $14,200.00."]})
F.f1099_int(C.pbc_file("12_1099-INT_Rosa_Mendoza_Broadway_Bank.pdf", "Form 1099-INT", "2026-03-09"),
            ["Broadway National Bank", "PO Box 17001", "San Antonio, TX 78217", "TIN: 00-0000031"],
            ["Rosa Mendoza", *ADDR, "TIN: XXX-XX-1187"], {"1": ROSA_INT}, account="****0615")
scanned_pages(C.pbc_file("13_Rosa_support_worksheet_handwritten.pdf", "Handwritten worksheet (scan)", "2026-03-09"),
    [["Rosa (mom) - 2025 support - Maria's figures",
      "",
      "Her room - we figured fair rent $800/mo x 12 = 9,600",
      "Food share approx  350/mo = 4,200",
      "Her medical (copays, rx, dentist) = 3,400",
      "  (Medicare B taken out of her SS - 1,223 incl. above)",
      "Clothes, phone, church, misc = 2,600",
      "TOTAL her support ~ 19,800",
      "",
      "She paid from her SS:  her medical 3,400 + clothes/misc 2,600",
      "   + gives us 300/mo sometimes (~?)  -> call it 6,300 total",
      "Rest of her SS goes to her savings at Broadway Bank",
      "We paid the rest  ~ 13,500",
      "",
      "She has no other income. No pension.  - M."]], handwritten=True, seed=61)
scanned_pages(C.pbc_file("14_Trailer_bill_of_sale_photo.pdf", "Phone photo (image)", "2026-03-09"),
    [["BILL OF SALE - TRAILER",
      "",
      "Date: March 22, 2025",
      "Seller: Raymond Delgado, 1123 W Mulberry, San Antonio TX",
      "Buyer: Carlos Mendoza / Mendoza Lawn & Landscape",
      "Description: 2019 Big Tex 35SA 16ft tandem axle",
      "  utility/landscape trailer, VIN 16VAX1622K5000918",
      "  (used - one prior owner)",
      "Price: $6,500.00   Paid by check #1204",
      "Sold AS IS.",
      "",
      "Seller signature: R. Delgado      Buyer: C. Mendoza"]], handwritten=True, seed=62, skew=-2.1)
statement(C.pbc_file("15_Alamo_Power_Equipment_Invoice_55120.pdf", "Vendor invoice", "2026-03-09"),
    "Alamo Power Equipment - Invoice 55120", [
        {"table": [["Item", "Qty", "Price"], ["Exmark Radius S-Series 52in zero-turn mower (new) S/N 412077810", "1", 2199.00],
                   ["Delivery / setup", "1", 101.00], ["Invoice total (sales tax exempt - TX ag/timber no. n/a; taxable sale, tax incl.)", "", MOWER_COST]],
         "left_align_cols": [0]},
        {"para": "Sold to: Mendoza Lawn & Landscape LLC, 7318 Mesquite Bend, San Antonio TX. Date 05/06/2025. Paid Visa ****2231."}])
statement(C.pbc_file("16_Mileage_log_summary_F-250_2025.pdf", "Mileage log summary (client-prepared)", "2026-03-09"),
    "2025 Truck Mileage Log Summary - 2022 Ford F-250 (from MileIQ export)", [
        {"table": [["Month", "Business miles", "Personal / commuting miles", "Total"],
                   *[[m, b, p, b + p] for m, b, p in [("Jan", 980, 210), ("Feb", 1040, 190), ("Mar", 1390, 230), ("Apr", 1520, 240),
                                                      ("May", 1560, 250), ("Jun", 1480, 260), ("Jul", 1410, 240), ("Aug", 1390, 230),
                                                      ("Sep", 1370, 220), ("Oct", 1330, 220), ("Nov", 1180, 240), ("Dec", 990, 230)]],
                   ["Total", TRUCK_MILES_BUS, TRUCK_MILES_TOTAL - TRUCK_MILES_BUS, TRUCK_MILES_TOTAL]], "total_row": True},
        {"para": f"Odometer 01/01/2025 41,207; 12/31/2025 {41207 + TRUCK_MILES_TOTAL:,}. Business use {TRUCK_MILES_BUS / TRUCK_MILES_TOTAL:.0%}. "
                 "Truck garaged at home; trips to storage yard and job sites are business. Maria's Honda used for family."}])
statement(C.pbc_file("17_Educator_expense_receipts_Maria.pdf", "Receipts (compiled)", "2026-03-09"),
    "Maria - classroom supplies receipts 2025 (compiled)", [
        {"table": [["Date", "Vendor", "Items", "Amount"],
                   ["01/18/2025", "Lakeshore Learning", "Phonics cards, readers", 96.40], ["03/02/2025", "Target", "Markers, folders, glue", 58.12],
                   ["08/09/2025", "Amazon", "Headphones for listening center (6)", 119.94], ["08/16/2025", "Walmart", "Back-to-school supplies", 84.61],
                   ["10/11/2025", "Teachers Pay Teachers", "Math centers (digital)", 50.93], ["Total", "", "", EDU_RECEIPTS]], "total_row": True,
         "left_align_cols": [0, 1, 2]},
        {"para": "Maria works 7:30-3:45 in a 2nd-grade classroom (instructional aide) - approx. 1,260 hours in 2025. Not reimbursed."}])
statement(C.pbc_file("18_EFTPS_payment_history_2025.pdf", "EFTPS payment history", "2026-03-09"),
    "EFTPS - Payment History - Form 1040ES - Tax Period 2025 - SSN ***-**-5208", [
        {"table": [["Settlement date", "Tax form", "Tax period", "Amount", "EFT #"]] +
                  [[d, "1040-ES", "12/2025", a, f"27055{i}0418"] for i, (d, a) in enumerate(EST_PAID, 1)]}])
statement(C.pbc_file("19_Oak_Hills_CC_2025_Dues_Statement.pdf", "Club statement", "2026-03-09"),
    "Oak Hills Country Club - 2025 Annual Family Membership Dues", [
        {"table": [["Member", "Carlos Mendoza (Family - golf & pool)"], ["Annual dues", 4200.00], ["Paid", "01/10/2025 (Mendoza Lawn & Landscape LLC)"]],
         "left_align_cols": [0, 1]},
        {"para": "Carlos' note on upload: 'I meet HOA board people here - some jobs came from it. Delia put it in the books.'"}])
statement(C.pbc_file("20_Bexar_County_2025_Property_Tax_Receipt.pdf", "Property tax receipt", "2026-03-09"),
    "Bexar County Tax Assessor-Collector - 2025 Tax Receipt", [
        {"table": [["Account", "07318-440-0120"], ["Property", ADDR[0]], ["2025 levy (county, city, ISD, ACCD, UHS)", PROP_TAX],
                   ["Paid", "12/19/2025 - Lone Oak Mortgage (escrow)"]], "left_align_cols": [0, 1]}])
write_text(C.pbc_file("21_Email_Carlos_1099_question_2026-03-16.txt", "Client correspondence", "2026-03-16", "Email"),
"""From: preparer@evergreentax.example
To: Carlos Mendoza <carlos.mendoza@example.com>
Date: Mon, 16 Mar 2026 11:02:00 -0500
Subject: Mendoza 2025 - helpers / Forms 1099-NEC

Hi Carlos - your QuickBooks shows Zelle/cash payments of $8,000 to Jose Ramirez and $4,500 to Luis Garza. Payments of
$600 or more to a non-employee for services in the course of your business require Form 1099-NEC (due 01/31/2026).
Because they were paid by Zelle (not by card/PayPal), no one else reported these payments. Schedule C asks whether you
made payments requiring 1099s (Yes) and whether you filed them - please send us completed Forms W-9 (name, address, SSN)
for both so we can prepare late 1099-NECs. Late-filing penalties apply but are much smaller than leaving them unfiled.

Also - who else is on the BCBS policy, and did Maria's district offer family coverage?

-----
From: Carlos Mendoza
Date: Tue, 24 Mar 2026 20:15:31 -0500
Subject: RE: Mendoza 2025 - helpers / Forms 1099-NEC

Ok. Jose gave me his W9, Luis is in Mexico until summer I'll get it when he is back. Me and the kids are on BCBS. Maria's
school has family coverage but it was expensive ($1,410 a month for family) and we wanted Sofia's orthodontist in network.
Just file the extension for now.
""")
write_text(C.pbc_file("22_Email_Carlos_W-9s_and_SEP_2026-08-27.txt", "Client correspondence + docs", "2026-08-27", "Email",
                      "W-9s attached"),
"""From: Carlos Mendoza <carlos.mendoza@example.com>
To: preparer@evergreentax.example
Date: Thu, 27 Aug 2026 07:48:02 -0500
Subject: W9s + how much SEP

Here are both W9s (Jose Ramirez SSN ends 7731, Luis Garza SSN ends 2045). How much do I put in the SEP this year? I want
the max like always. I will send it from Schwab when you tell me.
[attachments: W-9_Ramirez.pdf, W-9_Garza.pdf - retained in 1099 workpaper, not reproduced]
""")
statement(C.pbc_file("23_Schwab_SEP-IRA_Contribution_Confirmation.pdf", "Contribution confirmation", "2026-09-23",
                     note="received after SEP funded"),
    "Charles Schwab & Co. - SEP-IRA Contribution Confirmation", [
        {"table": [["Account", "SEP-IRA ****7120 - Carlos A. Mendoza"], ["Contribution date", "09/22/2026"],
                   ["Contribution type", "Employer SEP contribution - designated for tax year 2025"], ["Amount", float(SEP_MAX)]],
         "left_align_cols": [0, 1]}])
statement(C.pbc_file("24_IRIS_1099-NEC_Late_Filing_Acknowledgment.pdf", "IRS IRIS acknowledgment", "2026-09-18",
                     "Evergreen Tax (filed on client's behalf)"),
    "IRS Information Returns Intake System (IRIS) - Submission Acknowledgment", [
        {"table": [["Field", "Value"], ["Payer", f"{BIZ} (EIN {BIZ_EIN})"], ["Form type", "1099-NEC (tax year 2025) - 2 returns"],
                   ["Submission date", "09/18/2026"], ["Status", "Accepted"], ["Payees", "Jose Ramirez $8,000.00; Luis Garza $4,500.00"],
                   ["Payee copies", "Mailed 09/18/2026"]], "left_align_cols": [0, 1]}])

# ================================================================== RETURN
itemized = {"medical": HEALTH_PREM + OOP_MED, "state_income_tax": SALES_TAX_TABLE, "use_sales_tax": True,
            "real_estate_tax": PROP_TAX, "mortgage_interest_1098": MORT_INT, "charity_cash": CHARITY}
facts = {
    "status": "MFJ",
    "taxpayer": {"age65": False}, "spouse": {"age65": False},
    "dependents": [{"name": "Sofia Mendoza", "ctc": True}, {"name": "Mateo Mendoza", "ctc": True},
                   {"name": "Rosa Mendoza", "odc": True}],
    "w2": [{"who": "S", "box1": w2_m["1"], "box2": w2_m["2"], "box3": 0, "box4": 0, "box5": w2_m["5"], "box6": w2_m["6"]}],
    "interest": [{"payer": "Frost Bank", "amount": INT_FROST}],
    "sch1": {"sch_c": SCH_C_NET},
    "se": [{"who": "T", "net_profit": SCH_C_NET, "w2_ss_wages": 0}],
    "adjustments": {"educator": min(300, EDU_RECEIPTS), "sep": SEP_MAX},
    "qbi": {"businesses": [{"name": BIZ, "qbi": QBI_AMT}]},
    "estimated_payments": sum(a for _, a in EST_PAID),
    "extension_payment": EXT_PAY,
}
# itemized vs standard comparison run (Schedule A is not filed - kept out of the final return forms)
R_cmp = Return1040(dict(facts, itemized=itemized)).compute()
ITEMIZED = R_cmp.values["itemized_total_computed"]
assert R_cmp.values["deduction_type"] == "Standard"
R = Return1040(facts).compute()
v = R.values
R.notes.append(f"Itemized deductions ${ITEMIZED:,} (medical over 7.5% floor, sales tax + real estate tax, mortgage interest, charity) "
               f"< standard deduction ${v['12e']:,}; standard deduction used.")

# ---------------- attachments
sch_c_tbl = [["Schedule C line", "Description", "Amount"]] + [[a, b, c] for a, b, c in SCH_C_LINES]
part_v = [["Schedule C Part V - Other expenses", "Amount"]] + [[a, b] for a, b in OTHER_C] + [["Total (line 27a)", other_c_total]]
recon = [["Book-to-tax reconciliation (QuickBooks accrual -> Schedule C cash)", "Amount"],
         ["Net income per QuickBooks P&amp;L (accrual)", r(BOOK_NET)],
         ["Less: increase in accounts receivable (16,000 - 6,200) - accrual -> cash", -r(AR_END - AR_BEG)],
         ["Add back: country club dues (sec. 274(a)(3) - no deduction for club dues)", r(4200)],
         ["Add back: Netflix (personal)", r(275.88)],
         ["Add back: kids' soccer registration (personal)", r(640)],
         ["Add back: AT&amp;T family plan - 3 of 4 lines personal (keep Carlos' line $570)", r(2280 - PHONE_BUS)],
         ["Add back: health insurance - owner's family premiums are never a Sch C expense (see SE health worksheet)", r(HEALTH_PREM)],
         ["Add back: 50% of meals (sec. 274(n))", r(3140 * .5)],
         ["Add back: business gifts over $25 per recipient (12 x $50)", r(900 - GIFT_ALLOWED)],
         ["Less: truck - 15% personal use of actual expenses", -r(truck_exp_total - truck_ded)],
         ["Less: tax depreciation (Form 4562) - books recorded none", -(TRUCK_DEP_2025 + r(TRAILER_COST))],
         ["Less: 1/3 of 2024 return prep fee paid 04/2025 from personal account (legal & professional)", -PREP_SCH_C],
         ["Rounding", SCH_C_NET - (r(BOOK_NET) - r(AR_END - AR_BEG) + 4200 + 276 + 640 + r(2280 - PHONE_BUS) + r(HEALTH_PREM)
                                   + 1570 + 600 - r(truck_exp_total - truck_ded) - TRUCK_DEP_2025 - r(TRAILER_COST) - PREP_SCH_C)],
         ["Schedule C line 31 net profit (cash basis)", SCH_C_NET]]
f4562 = [["Form 4562 - " + BIZ, "Placed in service", "Cost / basis", "Bus. %", "Method", "2025 deduction"],
         ["Part II - Special depreciation allowance: 2019 Big Tex 16ft trailer (used, acquired 03/22/2025 - after 01/19/2025), 5-yr", "03/22/2025", r(TRAILER_COST), "100%", "Bonus 100% (sec. 168(k) as amended by OBBBA)", r(TRAILER_COST)],
         ["Part V listed property: 2022 Ford F-250 (GVWR > 6,000 lb)", "03/14/2022", r(TRUCK_COST), "85%", "MACRS 200DB HY 5-yr, year 4 (11.52%)", TRUCK_DEP_2025],
         ["2023 Exmark mower", "04/03/2023", 11800, "100%", "Sec. 179 (2023) - fully expensed", 0],
         ["Zero-turn mower $2,300 - NOT on Form 4562 (de minimis safe harbor election - expensed on Sch C line 27a)", "05/06/2025", r(MOWER_COST), "100%", "Reg. 1.263(a)-1(f)", 0],
         ["Total Form 4562 line 22 (to Schedule C line 13)", "", "", "", "", TRUCK_DEP_2025 + r(TRAILER_COST)],
         ["Part V line 30-36: truck total miles " + f"{TRUCK_MILES_TOTAL:,}" + "; business " + f"{TRUCK_MILES_BUS:,}" + "; commuting 0 (home is principal place of business); other personal " + f"{TRUCK_MILES_TOTAL - TRUCK_MILES_BUS:,}" + "; written evidence: Yes", "", "", "", "", ""]]
deminimis = ("<b>Section 1.263(a)-1(f) de minimis safe harbor election.</b> Carlos A. Mendoza, SSN XXX-XX-5208, " + BIZ + ", " +
             ADDR[0] + ", " + ADDR[1] + ". The taxpayer is making the de minimis safe harbor election under Treas. Reg. "
             "sec. 1.263(a)-1(f) for the taxable year ending 12/31/2025. (Taxpayer has no applicable financial statement; "
             "amounts of $2,500 or less per invoice/item are expensed on the books under the business's accounting procedure.)")
sep_ws = [["SEP-IRA maximum contribution worksheet (self-employed - Pub. 560 rate table / worksheet)", "Amount"],
          ["1. Schedule C net profit (line 31)", SCH_C_NET],
          ["2. Deductible part of SE tax (Schedule 1 line 15)", SE["half"]],
          ["3. Net earnings from self-employment for plan purposes (1 - 2)", SEP_COMP],
          ["4. Plan contribution rate 25% -> self-employed reduced rate 0.25 / 1.25 = 20%", "20%"],
          ["5. Maximum contribution (3 x 20%), limited to $70,000 (2025) and $350,000 comp. cap", SEP_MAX],
          ["6. Funded 09/22/2026 (before extended due date 10/15/2026) - Schwab confirmation in PBC", SEP_MAX],
          ["First draft used 25% x net profit = " + f"{r(SCH_C_NET * .25):,}" + " - excess contribution of " + f"{r(SCH_C_NET * .25) - SEP_MAX:,}" + " avoided", ""]]
seh = [["Self-employed health insurance (Form 7206) - eligibility", "Result"],
       ["Premiums paid (BCBS family PPO, Carlos + 2 children, 12 months)", r(HEALTH_PREM)],
       ["Was Carlos eligible to participate in a subsidized health plan maintained by his spouse's employer (Mission Creek ISD - "
        "district pays $450/mo toward every tier, spouse & family tiers offered) in any month?", "Yes - all 12 months"],
       ["Sec. 162(l)(2)(B): no deduction for any month the self-employed person is eligible for a subsidized employer plan "
        "(own or spouse's), even if coverage is declined", "Deduction $0"],
       ["Premiums -> Schedule A medical (see comparison; standard deduction larger)", r(HEALTH_PREM)]]
sa_cmp = [["Itemized vs standard (Schedule A not filed)", "Amount"],
          ["Medical: BCBS premiums 14,400 + out-of-pocket 2,860 = " + f"{r(HEALTH_PREM + OOP_MED):,}" + " less 7.5% of AGI " + f"{r(v['11'] * .075):,}",
           max(0, r(HEALTH_PREM + OOP_MED) - r(v['11'] * .075))],
          ["State & local: general sales tax (IRS table, TX + Bexar local 8.25%) + real estate tax 6,420 (no income tax in TX)", r(SALES_TAX_TABLE + PROP_TAX)],
          ["Home mortgage interest (Form 1098 - Lone Oak Mortgage)", r(MORT_INT)],
          ["Charitable - cash (St. Brigid Parish)", r(CHARITY)],
          ["Total itemized", ITEMIZED], ["Standard deduction MFJ (OBBBA)", v["12e"]],
          ["Result", "Standard deduction"]]
rosa = [["Qualifying relative test - Rosa Mendoza (mother of Carlos)", "Result"],
        ["Relationship: parent (need not live with taxpayer; she did all 12 months)", "Met"],
        ["Gross income test: < $5,200 (2025). Social Security is excluded from gross income here because none of it is "
         "taxable (her only other income is $85 interest; provisional income far below $25,000)", "Met - gross income $85"],
        ["Support test: total support $19,800; Rosa's own funds used for her support ~$6,300; Mendozas provided ~$13,500 (68%)", "Met"],
        ["Not a qualifying child of anyone; US citizen; not filing a joint return", "Met"],
        ["Credit for other dependents (Schedule 8812)", 500],
        ["Rosa's SSA-1099 and 1099-INT are HER documents - not reported on the Mendozas' return; Rosa has no filing requirement", ""]]
C.write_return(R, [
    ("Taxpayer / Spouse", "Carlos A. Mendoza (XXX-XX-5208) / Maria L. Mendoza (XXX-XX-6634)"),
    ("Address", ", ".join(ADDR)),
    ("Filing status", "Married filing jointly"),
    ("Dependents", "Sofia (daughter, 2013) - CTC; Mateo (son, 2017) - CTC; Rosa Mendoza (mother, 1955) - ODC (qualifying relative)"),
    ("Schedule C", f"{BIZ}, NAICS 561730, EIN {BIZ_EIN}, cash method; line I (payments requiring 1099) YES; line J (filed) YES - "
                   "late 1099-NECs filed 09/18/2026"),
    ("Digital assets question", "No"),
    ("Forms included", "1040, Sch 1, Sch 2, Sch 3, Sch 8812, Sch C, Sch SE, Form 4562, Form 8995, de minimis election statement"),
    ("Extension", f"Form 4868 filed 04/13/2026 with ${EXT_PAY:,.0f} payment; return due 10/15/2026"),
    ("State", "None - Texas has no individual income tax"),
    ("Filing method", "E-file (Form 8879 signed 09/25/2026); refund by direct deposit Frost ****4410"),
], attachments=[("Schedule C - Profit or Loss From Business (" + BIZ + ")", sch_c_tbl), ("Schedule C Part V", part_v),
                ("Book-to-tax reconciliation", recon), ("Form 4562 detail", f4562),
                ("Election statement", deminimis), ("SEP-IRA contribution computation", sep_ws),
                ("SE health insurance - not deductible", seh), ("Standard vs itemized comparison", sa_cmp),
                ("Dependent - qualifying relative worksheet", rosa)])

# ---------------- answer key
naive_sep = r(SCH_C_NET * .25)
gotchas = [
    gotcha("EVG1006-G1", "Schedule C - Accrual Basis books that should be on cash basis; AJEs", "QuickBooks P&L is accrual; PY AJE never posted",
           f"Enter QuickBooks revenue {fmt(BOOK_REV)} as gross receipts (includes the {fmt(AR_END - AR_BEG)} A/R increase, e.g. the "
           "December HOA invoice collected 01/2026); or 'fix' tax depreciation to match the unposted books.",
           f"Tax return is cash basis (method used since 2016): gross receipts = revenue - increase in A/R = {fmt(CASH_REV)} "
           "(A/P nil). PY AJE #1 (2024 depreciation 8,486) was not posted, so QB retained earnings/accumulated depreciation do not "
           "roll to our PY workpaper - no return impact (tax depreciation comes from our Form 4562 schedule); re-send AJE to bookkeeper.",
           f"Gross receipts overstated {fmt(AR_END - AR_BEG)} -> ~{fmt((AR_END - AR_BEG) * .9235 * .153 + (AR_END - AR_BEG) * .12 * .7)} tax", ["Sch C 1", "Sch C 31"], "medium"),
    gotcha("EVG1006-G2", "Schedule C - Book-Tax Differences (meals, personal expenses, club dues, gifts)", "Personal and limited items buried in the books",
           "Take the QuickBooks expense accounts at face value.",
           "Remove country club dues $4,200 (sec. 274(a)(3)), Netflix $276, kids' soccer $640, 3 of 4 family phone lines $1,710; "
           "meals 50% ($1,570 allowed); gifts limited to $25 x 12 recipients = $300 (sec. 274(b)); truck expenses 85% business.",
           "Sch C expenses overstated ~$10,000 if missed", ["Sch C 24b", "Sch C 25", "Sch C 27a", "Sch C 31"], "medium"),
    gotcha("EVG1006-G3", "Schedule C - De-Minimis Safe Harbor Election", "Mower under $2,500 vs used trailer",
           "Capitalize the $2,300 mower on Form 4562 (or expense it without the election statement); expense the $6,500 trailer as a "
           "'small tool', or depreciate it over 5 years without bonus.",
           "Mower: de minimis safe harbor (Reg. 1.263(a)-1(f)) - expense on Sch C and attach the annual election statement. Trailer: "
           "used 5-year property acquired 03/22/2025 (after 01/19/2025) -> 100% bonus depreciation (automatic; chosen over sec. 179, "
           "which needs an election and is income-limited) on Form 4562 Part II. Truck: remaining MACRS from PERM schedule at 85%.",
           "Timing; missing election statement = no safe harbor", ["Sch C 13", "Sch C 27a", "Form 4562"], "medium"),
    gotcha("EVG1006-G4", "Schedule C - Checking the top of Schedule C boxes (Form 1099 filed?)", "Helpers paid $8,000 and $4,500 by Zelle",
           "Answer line I 'Yes' and line J 'No' (red flag) or 'Yes' without filing; ignore the filing obligation.",
           "Advise client, obtain W-9s, file late 1099-NECs (filed via IRIS 09/18/2026; penalty exposure up to $340 per form under "
           "sec. 6721 plus $340 per payee statement under sec. 6722 for 2026-due returns - Rev. Proc. 2024-40 amounts), then answer I Yes / J Yes.",
           "Compliance / penalty exposure; audit flag", ["Sch C I", "Sch C J"], "easy"),
    gotcha("EVG1006-G5", "Schedule C - Tax Prep Fees", "PY prep fee paid personally in 2025",
           "Omit it (not in the books) or deduct the full $1,650 on Schedule C.",
           f"Prorate by time: 1 of 3 hours on Sch C -> {fmt(PREP_SCH_C)} to Sch C line 17 legal & professional; the personal 2/3 is "
           "nondeductible (misc. itemized deductions eliminated).", f"Sch C line 17 +{fmt(PREP_SCH_C)}", ["Sch C 17"], "easy"),
    gotcha("EVG1006-G6", "Schedule C - SEP IRA (compute maximum amount)", "SEP computed at 25% of net profit",
           f"Deduct 25% x net profit = {fmt(naive_sep)} (the employee rate) - creates an excess contribution.",
           f"Self-employed rate is 20% of (net profit - 1/2 SE tax): 20% x {fmt(SEP_COMP)} = {fmt(SEP_MAX)}; funded 09/22/2026 "
           "before the extended due date. QBI is reduced by the SEP deduction and 1/2 SE tax.",
           f"Sch 1 line 16 {fmt(SEP_MAX)} (not {fmt(naive_sep)})", ["Sch 1 16", "13a"], "medium"),
    gotcha("EVG1006-G7", "Schedule C - S/E Health Insurance Deduction", "Spouse's employer offers subsidized family coverage",
           "Deduct the $14,400 BCBS premiums on Sch 1 line 17 (or leave them in Sch C expenses as QuickBooks shows).",
           "Carlos was eligible to participate in Mission Creek ISD's subsidized plan through Maria (district contributes to every "
           "tier) -> sec. 162(l)(2)(B) bars the deduction for all 12 months even though he declined. Premiums go to Schedule A medical, "
           f"but itemized ({fmt(ITEMIZED)}) < standard ({fmt(v['12e'])}) -> no benefit.",
           "AGI understated $14,400 if deducted", ["Sch 1 17", "Sch C 15", "12e"], "hard"),
    gotcha("EVG1006-G8", "Scan - documents belonging to someone else; Dependents (qualifying relative)", "Rosa's SSA-1099 and 1099-INT in the PBC",
           "Autoflow adds Rosa's $14,200 SSA-1099 and $85 interest to the Mendozas' return; or omit Rosa as a dependent because "
           "'her SS is more than $5,200'.",
           "Remove Rosa's documents from the return. Rosa is a qualifying relative: nontaxable Social Security is not gross income "
           "(gross income $85 < $5,200), Mendozas provide ~68% of support -> $500 credit for other dependents.",
           "ODC $500; line 6a/6b wrongly populated", ["6a", "6b", "19"], "medium"),
    gotcha("EVG1006-G9", "Schedule 1 - Educator expenses", "Teacher's aide with $410 of receipts",
           "Deduct $410, or deny because she is 'not a teacher'.",
           "K-12 instructional aide with 900+ hours qualifies (sec. 62(d)(1)); deduction limited to $300.",
           "Sch 1 line 11 $300", ["Sch 1 11"], "easy"),
]
C.write_answer_key(R, {"residence": "TX (no state return)", "complexity": "Schedule C tier - accrual books, depreciation, SEP"},
    gotchas, filings=[{"form": "Form 4868", "filed": "2026-04-13", "payment": EXT_PAY},
                      {"form": "Form 1040 (federal)", "method": "e-file", "due": "2026-10-15", "filed": "2026-09-28"},
                      {"form": "Forms 1099-NEC (2) - late", "method": "IRIS", "filed": "2026-09-18"}],
    extra={"schedule_c": {ln: {"description": d, "amount": a} for ln, d, a in SCH_C_LINES},
           "schedule_c_other_expenses": dict(OTHER_C),
           "sep_ira": {"computation_base": SEP_COMP, "max_contribution": SEP_MAX, "funded": "2026-09-22"},
           "qbi_input": QBI_AMT, "itemized_not_used": ITEMIZED,
           "depreciation_2025": {"truck_macrs": TRUCK_DEP_2025, "trailer_bonus": r(TRAILER_COST), "mower_de_minimis_expensed": r(MOWER_COST)}})

C.write_receipt_log("EVG1006-1040-2025", "R. Salazar (staff)", "L. Chen (senior)", "S. Kennedy, CPA", "2026-03-09",
                    extension="Filed 04/13/2026 with $1,500 payment (client request - books not final)")

# ---------------- notes
naive_c_net = r(BOOK_REV) - (sch_c_exp - PREP_SCH_C)  # e.g. accrual receipts, no prep fee
C.write_notes(f"""
# EVG1006 - Mendoza, Carlos & Maria - 2025 Form 1040 - Preparer Notes

*Synthetic client - Project Evergreen. Return status: **signed off, e-filed 09/28/2026 (extended), accepted.***

## Return summary
| | |
|---|---|
| Filing status | Married filing jointly |
| Schedule C net profit | {fmt(SCH_C_NET)} (cash basis) |
| AGI (line 11) | {fmt(v['11'])} |
| Deduction | Standard {fmt(v['12e'])} (itemized would be {fmt(ITEMIZED)}) |
| QBI deduction (line 13a) | {fmt(v['13a'])} (20% of QBI {fmt(QBI_AMT)} = {fmt(r(QBI_AMT * .2))}, limited to 20% of taxable income before QBI) |
| Taxable income | {fmt(v['15'])} |
| Income tax / credits | {fmt(v['16'])} less CTC/ODC {fmt(v['19'])} |
| SE tax (Sch 2 line 4) | {fmt(SE['se_tax'])} |
| Total tax | {fmt(v['24'])} |
| Payments | withholding {fmt(v['25d'])} + estimates {fmt(v['26'])} + extension {fmt(r(EXT_PAY))} |
| **Refund** | **{fmt(v['refund'])}** (direct deposit) |

## What I did and why (plain English)
1. **Accrual books -> cash return.** Delia keeps QuickBooks on the accrual basis; the return has always been cash basis. QB revenue
   {fmt(BOOK_REV)} includes customer invoices not collected by year end. A/R went from {fmt(AR_BEG)} to {fmt(AR_END)} (aging report -
   the big item is the December Stone Oak HOA invoice paid 01/09/2026), so cash receipts = {fmt(CASH_REV)}. A/P was zero at both
   dates so no expense adjustment. The Square 1099-K ($61,240) and two 1099-NECs ($24,000 + $18,500) are all part of these receipts
   ($103,740 reported vs {fmt(CASH_REV)} total) - no double counting.
2. **Book-tax differences** (full reconciliation attached to the return): club dues ($4,200) are never deductible even if Carlos gets
   leads there; Netflix and the kids' soccer are personal; AT&T family plan - kept Carlos' own line ($570) and removed the other three
   lines; meals 50%; customer gift cards limited to $25 per person (12 people -> $300); the $14,400 BCBS premiums came out of Sch C
   (an owner's own health insurance is never a Schedule C expense - see item 7).
3. **Truck.** 2022 F-250 has been on the actual-expense method with MACRS since 2022, so the standard mileage rate is not an option
   (15,640 business miles x 70c = $10,948 anyway, less than actual). 85% business use from the MileIQ log. 2025 actual expenses
   {fmt(truck_exp_total)} x 85% = {fmt(truck_ded)} on line 9; MACRS year 4 on the 85% basis = {fmt(TRUCK_DEP_2025)}. Heavy truck
   (GVWR > 6,000 lb) - no sec. 280F luxury caps. Listed property section of Form 4562 completed.
4. **New equipment.** Zero-turn mower $2,300 (one invoice, under $2,500): expensed under the **de minimis safe harbor**; the election
   statement is attached to the return (it must be attached every year it is used). Used 2019 trailer $6,500 (bought 03/22/2025 from
   a private seller): 5-year property; I took **100% bonus depreciation** (OBBBA restored 100% for property acquired after 01/19/2025;
   used property qualifies since Carlos never used it before). I chose bonus over sec. 179 because bonus is automatic, not limited to
   business income, and there is no reason to elect out; result is the same {fmt(r(TRAILER_COST))} deduction this year.
5. **Helpers / Forms 1099-NEC.** Jose ($8,000) and Luis ($4,500) were paid by Zelle - so no 1099-K covers them and Carlos had to
   issue 1099-NECs by 01/31/2026. Organizer answered "Yes" (payments requiring 1099) / "No" (filed). We got W-9s on 08/27 and
   filed both late through IRIS on 09/18/2026 (payee copies mailed), so lines I and J are both **Yes**. Told Carlos to expect IRS penalty
   notices: up to $340 per form for filing after August 1 plus up to $340 per late payee statement (Rev. Proc. 2024-40 amounts) -
   max exposure $1,360; we will respond with reasonable-cause language if a notice comes (MISC project, billed separately).
6. **Prep fee.** The $1,650 we billed for the 2024 return was paid 04/2025 from the personal account (not in QB). Our time records
   show about 1/3 on the Schedule C, so {fmt(PREP_SCH_C)} goes on line 17 legal & professional; the rest is personal and not deductible.
7. **SE health insurance - not allowed.** Carlos bought a BCBS family PPO for himself and the kids ($14,400). Maria's district
   offers spouse/family coverage and pays $450/month toward every tier, so Carlos was *eligible to participate in a subsidized plan
   of his spouse's employer* every month - sec. 162(l)(2)(B) disallows the deduction even though they declined (cost/network reasons).
   The premiums are a Schedule A medical expense instead, but itemizing ({fmt(ITEMIZED)}) does not beat the standard deduction.
   Advised Carlos that the rule looks at eligibility, not enrollment.
8. **SEP-IRA maximum.** Carlos wants the max. For a self-employed person the 25% plan rate becomes 20% of net earnings after the
   deductible half of SE tax: ({fmt(SCH_C_NET)} - {fmt(SE['half'])}) x 20% = **{fmt(SEP_MAX)}**. Told him the amount on 09/21; funded
   09/22/2026 at Schwab (confirmation in PBC) - before the 10/15/2026 extended due date, so it counts for 2025.
9. **QBI.** QBI = net profit - 1/2 SE tax - SEP = {fmt(QBI_AMT)}; 20% = {fmt(r(QBI_AMT * .2))} but the deduction is limited to 20%
   of taxable income before QBI ({fmt(v['11'] - v['12e'])}) = {fmt(v['13a'])}. Well below the $394,600 threshold (landscaping is not an SSTB anyway).
10. **Maria.** W-2 from Mission Creek ISD - the district is a TRS (non-Social Security) employer, so boxes 3/4 are blank; box 14
    TRS 414(h) is already excluded from box 1. Educator expense: she is a K-12 instructional aide with ~1,260 hours -> qualifies;
    receipts $410, limited to **$300**.
11. **Rosa (Carlos' mother).** Lived with them all year; her only income is Social Security ($14,200) and $85 of bank interest. None
    of her SS is taxable, so her *gross income* is only $85 - under the $5,200 limit. Maria's support worksheet shows the family
    provided about $13,500 of her $19,800 total support. She is a **qualifying relative -> $500 credit for other dependents**. Her
    SSA-1099 and 1099-INT were in the upload - they are *her* documents, bookmarked "not for this return" and excluded from autoflow.
    She has no filing requirement.
12. **Estimates / penalty.** 2025 estimates 4 x $2,500 plus Maria's withholding = $11,380 >= 100% of 2024 tax ($10,620; AGI under
    $150k), paid evenly -> no Form 2210 penalty. Extension payment $1,500 on 04/13/2026.
13. **State.** Texas - none.

## Open items / advice
- Re-sent PY AJE #1 (2024 depreciation 8,486) plus 2025 AJE #1 (depreciation {fmt(TRUCK_DEP_2025 + r(TRAILER_COST))}) and AJE #2
  (reclass club dues/personal items to owner draws) to Ruiz Bookkeeping - until posted, QB retained earnings will not tie to our workpaper.
- 2026: issue 1099-NECs by 01/31/2027 (collect W-9s before first payment); consider paying helpers via payroll if they work regular schedules.
- 2026 estimates: {fmt(r(v['24'] / 4 / 50) * 50)} per quarter suggested (100% of 2025 tax).

## Hand-off to signer / routing
- [x] Return locked; Accountant's copy saved as *reviewed*
- [x] Federal 1040 - e-file; no state; no FBAR
- [x] Extended due date 10/15/2026 (Form 4868 on file); 1099-NECs filed 09/18/2026 (IRIS ack in PBC)
- [x] eSign (Form 8879) - Carlos by text/email
- [x] Direct deposit verified (Frost ****4410)
- Billing: Schedule C tier $1,650 + 1.5 hrs accrual->cash conversion and book-tax reconciliation + 1099-NEC late filing (2 forms)
  billed under MISC project; nothing to W/O.
""")
C.write_review_points(f"""
# Review Points - EVG1006 - 2025 - Form 1040

*Reviewer: L. Chen (blue). Preparer responses in red. Synthetic.*

1. **Sch C / WP 7 (QuickBooks P&L)** - Gross receipts entered at {fmt(BOOK_REV)} straight from the accrual P&L. Books are accrual, return is cash.
   - Back out the A/R increase per the aging ({fmt(AR_END - AR_BEG)}). Tie 1099-K/1099-NECs to receipts.
   - *Preparer: Done - gross receipts {fmt(CASH_REV)}; tie-out on WP 7.*
2. **Sch C / book-tax** - Club dues, Netflix, soccer, family phone plan and BCBS premiums are all in expenses; meals at 100%; gifts at $75 each.
   - Club dues are nondeductible even with a business purpose. Gifts $25/recipient.
   - *Preparer: Removed; reconciliation schedule attached to the return.*
3. **Sch 1 line 17** - Draft moved the $14,400 BCBS premiums to SE health insurance. See WP 9 - Maria's district offers subsidized family coverage.
   - Sec. 162(l)(2)(B) - eligibility (not enrollment) bars the deduction. Move to Sch A medical and re-run the itemized comparison.
   - *Preparer: Removed; Sch A {fmt(ITEMIZED)} < standard {fmt(v['12e'])} - standard stays.*
4. **Form 4562** - Mower $2,300 capitalized as 7-year property; trailer $6,500 depreciated over 5 years with no bonus.
   - Mower: de minimis safe harbor + election statement. Trailer: acquired after 01/19/2025 -> 100% bonus (used property OK).
   - *Preparer: Done; election statement added.*
5. **Sch C lines I/J** - Draft answered I "Yes", J "No". Do not file it that way.
   - Talk to Carlos about late 1099-NECs; we can file through IRIS once we have W-9s. Change J to Yes once filed.
   - *Preparer: W-9s received 08/27; filed 09/18 (ack in PBC). Both boxes Yes.*
6. **Sch C line 17** - PY prep fee not picked up (paid personally). Prorate 1/3 per time records.
   - *Preparer: Added {fmt(PREP_SCH_C)}.*
7. **Sch 1 line 16 (SEP)** - Draft used 25% of net profit ({fmt(naive_sep)}). Self-employed rate is 20% of net profit less 1/2 SE tax.
   Tell Carlos the number before he funds it.
   - *Preparer: Recomputed {fmt(SEP_MAX)}; client funded 09/22/2026 - confirmation in PBC.*
8. **Dependents / WP 11-12** - Autoflow picked up Rosa's SSA-1099 ($14,200) on line 6a and her $85 interest. These are hers.
   - Also - she is a qualifying relative (nontaxable SS is not gross income). Add ODC; keep the support worksheet in the file.
   - *Preparer: Rosa's docs excluded; ODC added (8812 now $4,900).*
9. **Sch 1 line 11** - Educator expense entered at $410; limit $300.
   - *Preparer: Corrected.*
10. FYI - PY AJE for 2024 depreciation still not posted by the bookkeeper (QB balance sheet). No return impact since we use our own
    depreciation schedule, but RE will not roll - please re-send AJEs with the client copy.
    - *Preparer: Sent to Ruiz Bookkeeping 09/28 with 2025 AJEs.*
""")
print("EVG1006 done", dict(R.summary()), v["refund"], v["balance_due"])
