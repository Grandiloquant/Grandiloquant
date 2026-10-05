"""EVG1010 - Daniel & Grace Kim (MFJ, Washington - Bellevue). Tech couple: RSU sell-to-cover / later sales with $0 broker
basis; nanny paid by Venmo and wrongly treated as a 1099 contractor (household employee -> Schedule H, W-2, EIN, WA ESD);
WA529 1099-Q used for K-12 tuition; kiddie tax: Ethan (16) has a stock sale -> cannot use Form 8814 -> separate client
EVG1021 (see c21_kim_ethan.py, which imports this module's return for Form 8615); Chloe (12) interest only -> Form 8814
election on the parents' return; CTC phase-out; Additional Medicare; NIIT; WA sales-tax election on Schedule A."""
from common import ClientBuild, gotcha, fmt
from docs import statement, scanned_pages, write_text, write_csv, write_xlsx, write_docx
import forms as F
from tax2025 import Return1040, r, tax_with_prefs

C = ClientBuild("EVG1010", "Kim", "Daniel & Grace Kim")
ADDR = ("2218 164th Ave NE", "Bellevue, WA 98008")
T = {"name": "Daniel J. Kim", "ssn": "XXX-XX-3318", "dob": "1984-07-22"}
S = {"name": "Grace H. Kim", "ssn": "XXX-XX-7742", "dob": "1986-11-05"}
ETHAN = {"name": "Ethan S. Kim", "ssn": "XXX-XX-5561", "dob": "2009-03-14"}
CHLOE = {"name": "Chloe M. Kim", "ssn": "XXX-XX-8420", "dob": "2013-06-02"}
REC_T = [T["name"], *ADDR, f"TIN: {T['ssn']}"]
REC_S = [S["name"], *ADDR, f"TIN: {S['ssn']}"]
REC_J = ["Daniel J. Kim & Grace H. Kim JTWROS", *ADDR, f"TIN: {T['ssn']}"]
REC_E = ["Grace H. Kim CUST Ethan S. Kim UTMA/WA", *ADDR, f"TIN: {ETHAN['ssn']}"]
REC_C = ["Chloe M. Kim (Grace H. Kim, custodian)", *ADDR, f"TIN: {CHLOE['ssn']}"]

# ====================================================================== PERM
C.write_profile(f"""
# EVG1010 - Kim, Daniel & Grace  (PERM)

*Synthetic client - Project Evergreen training data.*

| Item | Detail |
|---|---|
| Client ID | EVG1010 (parents). **Related client: EVG1021 - Kim, Ethan** (child's separate 1040 opened 02/2026 - see Kid Taxes procedure) |
| Taxpayer | Daniel J. Kim, DOB 07/22/1984, SSN {T['ssn']}, Principal Software Engineer, Northshore Cloud Systems, Inc. (RSUs vest quarterly) |
| Spouse | Grace H. Kim, DOB 11/05/1986, SSN {S['ssn']}, Clinical Pharmacist, Eastlake Medical Center (dependent-care FSA) |
| Address | {ADDR[0]}, {ADDR[1]} (King County) - resident since 2019. **Washington: no individual income tax**; WA capital gains excise - check annually |
| Dependents | Ethan S. Kim (son, DOB 03/14/2009, SSN {ETHAN['ssn']}); Chloe M. Kim (daughter, DOB 06/02/2013, SSN {CHLOE['ssn']}) |
| Kids' accounts | Ethan: UTMA brokerage (Pioneer Square Brokerage, Grace custodian). Chloe: savings/CDs at Cascade Federal Credit Union. **2024: both kids' interest/dividends reported on parents' return via Form 8814** |
| Household help | Nanny (Maria Lopez) since 09/2024 - after-school care for Chloe + household. Clients' 2024 return: nothing reported (hired late 2024; 2024 cash pay $6,240 - see open note below) |
| Home | Purchased 08/2019, mortgage Evergreen Coast Mortgage (orig. $712,000, < $750k limit). Property tax paid through escrow |
| 529 | WA529 account for Chloe (owner Grace) - pays part of Chloe's private-school tuition (Lakeside Hills Academy, grade 7) |
| Contact | Grace preferred - grace.kim@example.com, (425) 555-0172; eSign OK. Daniel: daniel.kim@example.com |
| Engagement | Client since 2021. "Complex W-2 / equity comp" tier, quote $2,400 (parents) + child return quoted separately |
| Payment info | Direct deposit/debit: BECU-style checking ending 6630 (voided check on file) |
""")
F.prior_year_summary(C.perm_file("2024_Form_1040_Return_Summary.pdf", "Prior-year return summary"), "Daniel & Grace Kim",
    "EVG1010", "Married filing jointly", [
        ["1a", "W-2 wages (Northshore Cloud incl. RSU $71,250; Eastlake Medical Center)", 386410],
        ["2b", "Taxable interest (Rainier Securities joint)", 1310],
        ["3a / 3b", "Qualified / ordinary dividends (Rainier Securities joint)", "5,240 / 6,120"],
        ["7", "Capital gain (RSU sell-to-cover, basis adjusted to FMV at vest; CG distributions)", 8040],
        ["11", "AGI", 401880], ["12", "Itemized deductions (property tax, WA sales tax table, mortgage interest, charity)", 44130],
        ["15", "Taxable income", 357750], ["16", "Tax (incl. Form 8814 tax for 2 children $115)", 74932],
        ["19", "Child tax credit (2 children; phase-out $100)", 3900],
        ["23", "Other taxes (Form 8959 $1,227; Form 8960 $538)", 1765],
        ["24", "Total tax", 72797], ["25", "Withholding", 74037], ["35a", "Refund", 1240],
        ["8814", "Form 8814 (2024 base $1,300) - Ethan: interest $610 + ordinary dividends $1,440 = $2,050 (tax $75); Chloe: interest $1,700 (tax $40)", 115]],
    notes="PY WP: Kids' income small and only interest/dividends -> Form 8814 elected for both (nothing added to parents' income "
          "since each child < $2,700). RSU shares: Northshore's broker reports $0 basis - always use FMV at vest from the "
          "equity supplemental statement. WA - no state return; WA capital gains excise not triggered. "
          "FYI: Grace mentioned hiring a nanny in Sept 2024 - ask about payment method / household employment in 2025 interview.")

# ====================================================================== PBC data
EMP_T = {"name": "Northshore Cloud Systems, Inc.", "addr1": "500 108th Ave NE", "addr2": "Bellevue, WA 98004", "ein": "00-6120447"}
EMP_S = {"name": "Eastlake Medical Center", "addr1": "1135 116th Ave NE", "addr2": "Bellevue, WA 98004", "ein": "00-2291806"}
EE_T = {"name": T["name"], "addr1": ADDR[0], "addr2": ADDR[1], "ssn": T["ssn"]}
EE_S = {"name": S["name"], "addr1": ADDR[0], "addr2": ADDR[1], "ssn": S["ssn"]}

RSU_TOTAL = 86400.00
w2_t = {"1": 309850.00, "2": 66420.00, "3": 176100.00, "4": 10918.20, "5": 333350.00, "6": 6033.73,
        "12": [("C", 552.00), ("D", 23500.00), ("DD", 22860.00)], "13": ["Retirement plan: X"],
        "14": [("RSU", RSU_TOTAL), ("WA PFML", 1157.19)], "control": "NCS-25-004417",
        "state": [{"state": "WA", "id": "(no state income tax)", "wages": "", "tax": ""}]}
w2_s = {"1": 120000.00, "2": 19860.00, "3": 130000.00, "4": 8060.00, "5": 130000.00, "6": 1885.00, "10": 5000.00,
        "12": [("D", 10000.00), ("DD", 19240.00)], "13": ["Retirement plan: X"],
        "14": [("WA PFML", 854.26), ("DCAP FSA", 5000.00)], "control": "EMC-0098812"}

# RSU vests (from Northshore equity supplemental statement) - FMV at vest is the tax basis (included in W-2 box 1)
VESTS = [("02/15/2025", 120, 180.00), ("05/15/2025", 120, 172.50), ("08/15/2025", 120, 185.00), ("11/15/2025", 120, 182.50)]
assert abs(sum(n * p for _, n, p in VESTS) - RSU_TOTAL) < 0.01
STC = [("02/18/2025", 38, 179.40), ("05/15/2025", 38, 172.35), ("08/15/2025", 38, 185.30), ("11/17/2025", 38, 181.90)]
# broker 1099-B rows: (id, desc, acq, sold, shares, price, fmv_basis, lt)
RSU_SALES = []
for i, ((vd, n, fmv), (sd, q, px)) in enumerate(zip(VESTS, STC), 1):
    RSU_SALES.append((f"STC{i}", f"{q} sh NSCS (RSU sell-to-cover)", vd, sd, q, px, round(q * fmv, 2), False))
RSU_SALES.append(("S5", "82 sh NSCS (RSU 02/15/2025 lot)", "02/15/2025", "12/05/2025", 82, 190.10, round(82 * 180.00, 2), False))
RSU_SALES.append(("S6", "150 sh NSCS (RSU 03/15/2023 lot, FMV 118.40)", "03/15/2023", "06/10/2025", 150, 176.20,
                  round(150 * 118.40, 2), True))

trades = []
for tid, desc, acq, sold, q, px, basis, lt in RSU_SALES:
    proceeds = round(q * px, 2)
    trades.append({"box": "E" if lt else "B", "id": tid, "desc": desc, "acq": acq, "sold": sold, "proceeds": proceeds,
                   "basis": 0.0, "adj": -basis, "code": "B"})
rsu_st_gain = sum(t["proceeds"] + t["adj"] for t in trades if t["box"] == "B")
rsu_lt_gain = sum(t["proceeds"] + t["adj"] for t in trades if t["box"] == "E")
rsu_proceeds = sum(t["proceeds"] for t in trades)

# joint Rainier Securities account (no sales in 2025)
J_INT, J_ORD, J_QUAL, J_CGD = 1452.18, 6811.40, 5904.22, 1206.55
# Nanny
NANNY = {"name": "Maria Lopez", "ssn": "XXX-XX-6093", "addr": "15820 NE 8th St Apt 214, Bellevue, WA 98008"}
NANNY_WEEKS = 50
NANNY_WEEKLY = 560.00
NANNY_CASH = NANNY_WEEKS * NANNY_WEEKLY
assert NANNY_CASH == 28000
SS_MED_RATE, FUTA_NET, FUTA_BASE = 0.153, 0.006, 7000
sch_h_fica = r(NANNY_CASH * 0.124) + r(NANNY_CASH * 0.029)
sch_h_futa = r(FUTA_BASE * FUTA_NET)
sch_h_total = sch_h_fica + sch_h_futa
ee_share_paid = round(NANNY_CASH * 0.0765, 2)          # employee share paid by the Kims (not withheld)

# Chloe (Form 8814)
CHLOE_INT = 1900.00
f8814_line4 = r(CHLOE_INT)
f8814_base = 2700
f8814_line6_income = max(0, f8814_line4 - f8814_base)
f8814_tax = r(0.10 * max(0, min(f8814_line4, 2700) - 1350))

# Ethan's documents (rendered here in the parents' PBC as uploaded; c21 re-renders copies into EVG1021)
ETHAN_W2 = {"1": 3200.00, "2": 0.00, "3": 3200.00, "4": 198.40, "5": 3200.00, "6": 46.40,
            "14": [("WA PFML", 21.03)], "control": "EAC-2025-117"}
ETHAN_EMP = {"name": "Eastside Aquatics Club", "addr1": "14509 SE Newport Way", "addr2": "Bellevue, WA 98006", "ein": "00-4038821"}
ETHAN_INT, ETHAN_ORD, ETHAN_QUAL = 900.00, 2400.00, 1900.00
ETHAN_SALE = {"desc": "74 sh Pioneer Total Market Index Fund Admiral", "acq": "06/03/2019", "sold": "07/21/2025",
              "proceeds": 8214.00, "basis": 5114.00}
PSB = ["Pioneer Square Brokerage LLC", "1201 Third Ave Ste 3000", "Seattle, WA 98101", "TIN: 00-8830126"]


def render_ethan_docs(build, received="2026-02-09", source="Sharefile upload", note="", prefix=""):
    """Ethan's PBC documents. Called by this script (parents' upload) and by c21 (copies in the child's own folder)."""
    ee = {"name": ETHAN["name"], "addr1": ADDR[0], "addr2": ADDR[1], "ssn": ETHAN["ssn"]}
    F.w2(build.pbc_file(f"{prefix}a_W-2_Eastside_Aquatics_Ethan.pdf", "Form W-2 (child)", received, source, note), ETHAN_EMP, ee, ETHAN_W2)
    statement(build.pbc_file(f"{prefix}b_Pioneer_Square_UTMA_Ethan_2025_Consolidated_1099.pdf", "Consolidated 1099 (child UTMA)",
                             received, source, note),
        "Pioneer Square Brokerage - 2025 Consolidated Form 1099 - Account ****2270 (UTMA/WA)", [
            {"table": [["Recipient", "Grace H. Kim CUST Ethan S. Kim UTMA/WA - TIN " + ETHAN["ssn"]],
                       ["Payer", "Pioneer Square Brokerage LLC, 1201 Third Ave Ste 3000, Seattle WA 98101 - TIN 00-8830126"],
                       ["Statement date", "02/13/2026 (original)"]], "left_align_cols": [0, 1], "header": False},
            {"heading": "Form 1099-INT", "table": [["Box", "Description", "Amount"], ["1", "Interest income (money market / Treasury MMF)", ETHAN_INT],
                                                   ["3", "Interest on U.S. Savings Bonds and Treasury obligations", 0.00],
                                                   ["4", "Federal income tax withheld", 0.00]]},
            {"heading": "Form 1099-DIV", "table": [["Box", "Description", "Amount"], ["1a", "Total ordinary dividends", ETHAN_ORD],
                                                   ["1b", "Qualified dividends", ETHAN_QUAL], ["2a", "Total capital gain distributions", 0.00],
                                                   ["4", "Federal income tax withheld", 0.00]]},
            {"heading": "Form 1099-B - Short-term / Long-term transactions",
             "table": [["Description", "Date acquired", "Date sold", "1d Proceeds", "1e Cost basis", "Gain/(loss)", "Term / box"],
                       [ETHAN_SALE["desc"], ETHAN_SALE["acq"], ETHAN_SALE["sold"], ETHAN_SALE["proceeds"], ETHAN_SALE["basis"],
                        ETHAN_SALE["proceeds"] - ETHAN_SALE["basis"], "Long-term, covered (box D) - basis reported to IRS"]]},
            {"note": "Custodial (UTMA) account income is taxable to the minor, reported under the minor's TIN."}])


# ====================================================================== PBC documents (parents)
F.organizer(C.pbc_file("01_2025_Organizer_Kim.pdf", "Client organizer", "2026-02-09"), "Daniel & Grace Kim", "EVG1010",
    general=[("Did your marital status change during 2025?", "No", ""),
             ("Were there any changes in dependents?", "No", ""),
             ("Did you pay any individual (e.g. nanny, housekeeper) to work in or around your home?", "No",
              "Our nanny Maria is a contractor - we sent her a 1099"),
             ("Did you pay for child care so you could work?", "Yes", "Maria (nanny) - Grace's FSA reimbursed $5k"),
             ("Did you receive a distribution from a 529 plan or Coverdell?", "Yes", "WA529 paid Chloe's school"),
             ("Did you sell stock or other securities?", "Yes", "RSUs (sell to cover) + one sale in June"),
             ("Do your children have investment income?", "Yes", "Same as last year - please do Form 8814 again"),
             ("Did you receive, sell, exchange digital assets?", "No", ""),
             ("Did you make estimated tax payments?", "No", "")],
    dependents=[["Ethan S. Kim", "Son", "03/14/2009", "5561", "12", "No"],
                ["Chloe M. Kim", "Daughter", "06/02/2013", "8420", "12", "No"]],
    income_rows=[["Wages", "Northshore Cloud Systems (Daniel)", 293680, "see W-2"],
                 ["Wages", "Eastlake Medical Center (Grace)", 92730, "see W-2"],
                 ["Interest / dividends", "Rainier Securities (joint)", "1,310 / 6,120", "see 1099"],
                 ["Stock sales", "Summit Shareworks (RSU)", 7296, "see 1099-B"],
                 ["Child income (8814)", "Ethan - Pioneer Square UTMA", 2050, "see 1099 (sold a fund)"],
                 ["Child income (8814)", "Chloe - Cascade FCU", 1700, "1,900"]],
    deductions_rows=[["Mortgage interest", "Evergreen Coast Mortgage", 25140, "see 1098"],
                     ["Property tax", "King County (escrow)", 13880, "see 1098"],
                     ["Charitable - cash", "Eastside Food Bank, church", 3800, "4,000"],
                     ["Child care provider", "Maria Lopez", "", "28,000"]],
    signature_date="02/07/2026")

F.w2(C.pbc_file("02_W-2_Northshore_Cloud_Daniel.pdf", "Form W-2", "2026-02-09"), EMP_T, EE_T, w2_t)
F.w2(C.pbc_file("03_W-2_Eastlake_Medical_Grace.pdf", "Form W-2", "2026-02-09"), EMP_S, EE_S, w2_s)

# Summit Shareworks 1099-B (RSU account) - basis shown as $0.00, box 12 NOT checked
rows_b = [["Description (box 1a)", "1b Acquired", "1c Sold", "1d Proceeds", "1e Cost basis", "1f/1g", "Box 12 basis reported to IRS?", "Term"]]
for tid, desc, acq, sold, q, px, basis, lt in RSU_SALES:
    rows_b.append([desc, acq, sold, round(q * px, 2), 0.00, "", "NO", "Long" if lt else "Short"])
rows_b.append(["Total", "", "", round(rsu_proceeds, 2), 0.00, "", "", ""])
statement(C.pbc_file("04_Summit_Shareworks_2025_Form_1099-B_Daniel.pdf", "Form 1099-B (RSU account)", "2026-02-09"),
    "Summit Shareworks Brokerage LLC - 2025 Form 1099-B - Account ****9102 (Northshore equity plan)", [
        {"table": [["Recipient", f"{T['name']} - TIN {T['ssn']}"], ["Payer", "Summit Shareworks Brokerage LLC, 40 Wall St Fl 22, New York NY 10005 - TIN 00-7715320"]],
         "left_align_cols": [0, 1], "header": False},
        {"heading": "Proceeds from Broker Transactions - NONCOVERED / basis not reported to the IRS (Form 8949 box B / box E)",
         "table": rows_b, "total_row": True},
        {"note": ["Cost basis for shares acquired through an employee equity plan may not include amounts included in your wages. "
                  "Refer to your Supplemental Information statement for the fair market value at vest.",
                  "Federal income tax withheld (box 4): 0.00. Taxes on vesting were withheld through payroll (sell-to-cover)."]}])
statement(C.pbc_file("05_Summit_Shareworks_2025_Supplemental_Equity_Statement.pdf", "Equity supplemental statement", "2026-02-09"),
    "Summit Shareworks - 2025 Supplemental Information (not filed with the IRS) - Daniel J. Kim", [
        {"heading": "RSU releases (ordinary income reported on your Form W-2)",
         "table": [["Release date", "Shares released", "FMV per share", "Taxable income (in W-2 box 1 / box 14 'RSU')", "Shares sold to cover", "Net shares deposited"]] +
                  [[vd, n, fmv, round(n * fmv, 2), 38, n - 38] for vd, n, fmv in VESTS] +
                  [["Total", 480, "", RSU_TOTAL, 152, 328]], "total_row": True},
        {"heading": "Adjusted cost basis for 2025 sales",
         "table": [["Sale", "Date sold", "Shares", "Lot / release date", "FMV at release (adjusted basis)", "Broker 1099-B basis"]] +
                  [[tid, sold, q, acq, basis, 0.00] for tid, desc, acq, sold, q, px, basis, lt in RSU_SALES]},
        {"note": "Lot S6 was released 03/15/2023 at $118.40/share (included in your 2023 Form W-2)."}])
statement(C.pbc_file("06_Rainier_Securities_2025_Consolidated_1099_Joint.pdf", "Consolidated 1099 (joint)", "2026-02-19",
                     note="uploaded separately"),
    "Rainier Securities - 2025 Consolidated Form 1099 - Joint Account ****4418", [
        {"table": [["Recipient", "Daniel J. Kim & Grace H. Kim JTWROS - TIN " + T["ssn"]],
                   ["Payer", "Rainier Securities Inc., 999 Third Ave, Seattle WA 98104 - TIN 00-3304719"]], "left_align_cols": [0, 1], "header": False},
        {"heading": "1099-INT", "table": [["Box", "Description", "Amount"], ["1", "Interest income", J_INT], ["3", "U.S. Treasury obligations", 0.0]]},
        {"heading": "1099-DIV", "table": [["Box", "Description", "Amount"], ["1a", "Total ordinary dividends", J_ORD],
                                          ["1b", "Qualified dividends", J_QUAL], ["2a", "Total capital gain distributions", J_CGD],
                                          ["7", "Foreign tax paid", 0.0]]},
        {"heading": "1099-B", "para": "No sales or redemptions in 2025."}])
F.f1099_q(C.pbc_file("07_1099-Q_WA529_Chloe.pdf", "Form 1099-Q", "2026-02-09"),
          ["Washington College Savings Plan (WA529) - synthetic", "PO Box 7211", "Olympia, WA 98507", "TIN: 00-9912004"],
          ["Chloe M. Kim", *ADDR, f"TIN: {CHLOE['ssn']}"],
          {"1": 10000.00, "2": 3122.61, "3": 6877.39, "5": "State (qualified tuition program)"}, account="WA529-****5510",
          notes=["Distribution paid 08/12/2025 directly to Lakeside Hills Academy (payee) for the benefit of the beneficiary."])
statement(C.pbc_file("08_Lakeside_Hills_Academy_2025-26_Tuition_Statement.pdf", "School tuition statement", "2026-02-09"),
    "Lakeside Hills Academy (private K-12, Bellevue WA) - Tuition Account Statement - Chloe Kim, Grade 7", [
        {"table": [["Date", "Description", "Charges", "Payments"],
                   ["07/01/2025", "2025-26 tuition (grade 7)", 24800.00, ""],
                   ["08/12/2025", "Payment - WA529 plan", "", 10000.00],
                   ["08/15/2025", "Payment - Kim family (check 3391)", "", 7400.00],
                   ["01/10/2026", "Payment - Kim family", "", 7400.00],
                   ["", "Balance", 0.00, ""]], "left_align_cols": [0, 1]}])
F.f1099_int(C.pbc_file("09_1099-INT_Cascade_FCU_Chloe.pdf", "Form 1099-INT (child)", "2026-02-09"),
            ["Cascade Federal Credit Union - synthetic", "18020 80th Pl S", "Kent, WA 98032", "TIN: 00-1167045"], REC_C,
            {"1": CHLOE_INT}, account="****0457 (share certificates)")
render_ethan_docs(C, prefix="10")
F.f1098(C.pbc_file("11_1098_Evergreen_Coast_Mortgage.pdf", "Form 1098", "2026-02-09"),
        ["Evergreen Coast Mortgage LLC - synthetic", "2200 Western Ave", "Seattle, WA 98121", "TIN: 00-5528190"], REC_J,
        {"1": 24310.55, "2": 648212.40, "3": "08/23/2019", "7": "Yes", "9": "1", "10": "Property tax paid from escrow 14,236.40",
         "11": ""}, account_no="****7719")
statement(C.pbc_file("12_King_County_2025_Property_Tax_Receipt.pdf", "Property tax receipt", "2026-02-09"),
    "King County Treasury - 2025 Property Tax Receipt (synthetic)", [
        {"table": [["Parcel", "Owner", "1st half paid", "2nd half paid", "Total 2025"],
                   ["1545800-0215", "KIM DANIEL J+GRACE H", 7118.20, 7118.20, 14236.40]]},
        {"note": "Paid by Evergreen Coast Mortgage (escrow) 04/28/2025 and 10/29/2025."}])
statement(C.pbc_file("13_Charitable_receipts_2025.pdf", "Charity acknowledgments", "2026-02-09"),
    "2025 Charitable Contribution Acknowledgments (compiled by Grace)", [
        {"table": [["Organization", "Date", "Amount", "Goods/services received?"],
                   ["Eastside Food Bank (501(c)(3), EIN 00-9134402)", "12/15/2025", 2500.00, "None"],
                   ["Bellevue Korean Presbyterian Church (EIN 00-7710093)", "monthly 2025", 1500.00, "None - intangible religious benefits only"],
                   ["Total", "", 4000.00, ""]], "total_row": True}])

# Venmo export (nanny) - weekly Friday payments, 2 unpaid weeks
import datetime as _dt
d0 = _dt.date(2025, 1, 3)
ven = []
skip = {_dt.date(2025, 7, 4), _dt.date(2025, 12, 26)}
d = d0
while d.year == 2025:
    if d not in skip:
        ven.append([f"{d:%Y-%m-%d}T17:{10 + d.day % 40:02d}:00", "Payment", "Complete", "Grace Kim", "Maria Lopez",
                    "nanny week " + f"{d:%m/%d}" + (" + groceries" if d.month == 3 and d.day < 8 else ""), f"-{NANNY_WEEKLY:.2f}", "Venmo balance"])
    d += _dt.timedelta(days=7)
assert len(ven) == NANNY_WEEKS, len(ven)
ven.insert(9, ["2025-03-11T09:02:00", "Payment", "Complete", "Grace Kim", "Tom Reyes", "soccer carpool gas", "-40.00", "Venmo balance"])
ven.insert(30, ["2025-07-19T12:44:00", "Payment", "Complete", "Grace Kim", "Jin Park", "BBQ split", "-62.50", "Venmo balance"])
write_csv(C.pbc_file("14_Venmo_statement_2025_Grace.csv", "Payment app export (CSV)", "2026-02-20", "Client email attachment",
                     "requested at interview"),
          ["Datetime", "Type", "Status", "From", "To", "Note", "Amount (total)", "Funding source"], ven)
F.f1099_nec(C.pbc_file("15_1099-NEC_issued_to_Maria_Lopez_copy.pdf", "Form 1099-NEC (issued BY client)", "2026-02-20",
                       "Client email attachment"),
            ["Grace Kim", *ADDR, f"TIN: {S['ssn']}"],
            [NANNY["name"], "15820 NE 8th St Apt 214", "Bellevue, WA 98008", f"TIN: {NANNY['ssn']}"], {"1": NANNY_CASH},
            copy_label="Copy B - For Recipient (payer's file copy)",
            notes=["Filed by payer 01/27/2026 via an online 1099 filing service (confirmation IRIS-2026-5530071)."])
write_text(C.pbc_file("16_Email_Grace_nanny_details_2026-02-20.txt", "Client correspondence", "2026-02-20", "Email"),
"""From: Grace Kim <grace.kim@example.com>
To: preparer@evergreentax.example
Cc: Daniel Kim <daniel.kim@example.com>
Date: Fri, 20 Feb 2026 21:14:33 -0800
Subject: Re: Kim 2025 - nanny questions from today's call

Hi Priya,

Answers to your questions from the call:

- Maria works Mon-Fri, 12:30pm to 6:30pm at our house. She picks Chloe up from school, helps with homework,
  does kid laundry and starts dinner. Some days she takes Ethan to practice.
- We set the schedule and tell her what we need done. She uses our car for pickups. We pay $560/week by Venmo,
  every Friday. We gave her 2 paid holidays but skipped 2 weeks when we were on vacation (July 4th week and Christmas week).
- She doesn't work for any other family. She doesn't have a business name or insurance.
- We had her fill out a W-9 last year and I sent her a 1099-NEC in January through an online site.
  My friend said that's how you do it for a nanny?
- She started in September 2024. We paid her $6,240 in 2024 (didn't do anything for that year).
- My FSA reimbursed me $5,000 for her pay (I used her SSN on the FSA claim form).

Venmo export attached. Let us know what we need to do!

Grace
""")
write_docx(C.pbc_file("17_Interview_Memo_2026-02-20.docx", "Client interview memo (firm)", "2026-02-20", "Evergreen - prepared by staff",
                      "bookmark as client correspondence"),
    "Client Interview Memo - EVG1010 Kim - Tax Year 2025", [
        ("h", "Attendees / date"), "Grace Kim (client), P. Anand (preparer) - phone, 02/20/2026, 25 min.",
        ("h", "Topics"),
        ("b", ["Nanny (Maria Lopez): works in clients' home, clients set hours/duties, uses clients' car, paid weekly, no other clients -> "
               "common-law employee (household employee) - NOT an independent contractor. Clients issued a 1099-NEC ($28,000).",
               "Need: EIN (SS-4) for household employer, Schedule H, W-2/W-3 for Maria, corrected (zeroed) 1099-NEC, WA ESD registration; "
               "2024 cash wages $6,240 >= 2024 $2,700 threshold -> 2024 Schedule H also required (separate MISC project - amended 2024 return).",
               "Kids: Ethan sold part of his UTMA fund in July -> capital gain. Grace asked for Form 8814 again 'like last year'. "
               "Explained 8814 is not available when the child has capital gains from a sale (or wages) -> Ethan must file his own return. "
               "Need new client ID + project code for Ethan (EVG1021). Chloe: interest only -> 8814 OK.",
               "WA529 $10,000 paid to Lakeside Hills Academy (K-12 tuition) - qualified; no taxable portion.",
               "No estimated payments. Clients understand balance may be due because nanny taxes were not withheld/paid in 2025."]),
        ("h", "Follow-ups"),
        ("b", ["Email engagement addendum for EVG1021 (child return) and MISC household-employer project.",
               "Send client the household employer checklist (SS-4, W-4 for 2026, WA ESD, L&I and WA PFML guidance to be confirmed with payroll provider)."])])
write_text(C.pbc_file("18_Email_thread_EIN_W-2_ESD_2026-03-12.txt", "Client correspondence", "2026-03-12", "Email"),
"""From: preparer@evergreentax.example
To: Grace Kim
Date: Tue, 3 Mar 2026 10:12:00 -0800
Subject: Kim - household employer items

Hi Grace - as discussed, your EIN as a household employer was assigned today (00-9087731, online SS-4). Next steps:
1) We prepared Maria's 2025 Form W-2 (box 1 $30,142.00 - includes the $2,142 employee share of social security/
   Medicare that you are paying on her behalf; boxes 3 and 5 $28,000.00) and Form W-3 for e-filing with SSA.
2) We will file a CORRECTED 1099-NEC showing $0 to replace the one you sent.
3) Please register with Washington ESD for unemployment insurance as a household employer and pay the 2025 contributions
   BEFORE April 15, 2026 (this keeps the federal unemployment (FUTA) rate at 0.6% on Schedule H).

-----
From: Grace Kim
Date: Thu, 12 Mar 2026 19:40:51 -0800
Subject: RE: Kim - household employer items

Done! Registered with ESD today. They'll send a bill for Q1-Q4 2025 - I will pay it as soon as it comes.
Also gave Maria her W-2. She said thank you (she wasn't sure how to do her taxes with the 1099).
""")
write_text(C.pbc_file("19_Email_Grace_ESD_paid_2026-04-07.txt", "Client correspondence", "2026-04-07", "Email",
                      "follow-up received"),
"""From: Grace Kim <grace.kim@example.com>
To: preparer@evergreentax.example
Date: Tue, 7 Apr 2026 08:03:12 -0700
Subject: ESD paid

Paid the Washington ESD unemployment bill for 2025 yesterday (04/06/2026) - confirmation ESD-UI-8812046.
Ready to sign whenever the returns are done.
""")
# irrelevant: 401(k) statement
statement(C.pbc_file("20_Northshore_401k_Q4_2025_Statement_Daniel.pdf", "Retirement plan statement", "2026-02-09"),
    "Northshore Cloud Systems 401(k) Plan - Quarterly Statement 10/01/2025-12/31/2025 - Daniel J. Kim", [
        {"table": [["Item", "Amount"], ["Beginning balance", 612440.18], ["Employee pre-tax deferrals", 5875.00],
                   ["Employer match", 2937.50], ["Dividends / gains", 18204.66], ["Ending balance", 639457.34]],
         "left_align_cols": [0]},
        {"note": "Earnings inside the plan are tax-deferred. This statement is for your records."}])

# ====================================================================== RETURN
parent_niit_gross = r(J_INT) + r(J_ORD) + r(J_CGD) + r(rsu_st_gain) + r(rsu_lt_gain)
facts = {
    "status": "MFJ",
    "taxpayer": {"age65": False}, "spouse": {"age65": False},
    "dependents": [{"name": "Ethan S. Kim", "ctc": True}, {"name": "Chloe M. Kim", "ctc": True}],
    "w2": [{"who": "T", "box1": w2_t["1"], "box2": w2_t["2"], "box3": w2_t["3"], "box4": w2_t["4"], "box5": w2_t["5"], "box6": w2_t["6"]},
           {"who": "S", "box1": w2_s["1"], "box2": w2_s["2"], "box3": w2_s["3"], "box4": w2_s["4"], "box5": w2_s["5"], "box6": w2_s["6"],
            "box10": w2_s["10"]}],
    "interest": [{"payer": "Rainier Securities (joint ****4418)", "amount": J_INT}],
    "dividends": [{"payer": "Rainier Securities (joint ****4418)", "ordinary": J_ORD, "qualified": J_QUAL, "capgain_dist": J_CGD}],
    "trades": trades,
    "dependent_care": {"expenses": NANNY_CASH, "n_qual": 1},
    "itemized": {"state_income_tax": 3912, "use_sales_tax": True, "real_estate_tax": 14236.40,
                 "mortgage_interest_1098": 24310.55, "charity_cash": 4000},
    "form_8814_tax": f8814_tax,
    "schedule_h_tax": sch_h_total,
    "niit": {"nii": parent_niit_gross, "gross": parent_niit_gross},
}
R = Return1040(facts).compute()
v = R.values
sd = v["sch_d"]
# export for Form 8615 (EVG1021)
PARENT_8615 = {"parent_ti": v["15"], "parent_status": "MFJ", "parent_qd": v["3a"], "parent_ncg": sd["ncg"],
               "parent_tax_line16_ex_8814": v["16"] - f8814_tax, "parent_name": "Daniel J. Kim & Grace H. Kim",
               "parent_ssn": T["ssn"]}
# self-check: engine's own tax on parents' TI = line 16 less 8814 tax
_chk, _ = tax_with_prefs(v["15"], "MFJ", v["3a"], sd["ncg"])
assert _chk == PARENT_8615["parent_tax_line16_ex_8814"], (_chk, v["16"])
# hand checks
assert v["1a"] == r(w2_t["1"] + w2_s["1"])
ctc_red = 50 * -(-(v["11"] - 400000) // 1000)
assert v["19"] == 4400 - ctc_red
assert v["20"] == 0  # 2441 credit fully displaced by FSA exclusion
assert v["niit"] == r(0.038 * parent_niit_gross)
f8959 = r(0.009 * (w2_t["5"] + w2_s["5"] - 250000))

# ---------------------------------------------------------------- attachments
basis_rows = [["Sale", "Form 8949 box", "Date acquired", "Date sold", "Proceeds", "1099-B basis", "Adj. basis (FMV at vest)", "Code", "Col (g) adj.", "Gain/(loss)"]]
for t, (tid, desc, acq, sold, q, px, basis, lt) in zip(trades, RSU_SALES):
    basis_rows.append([tid, t["box"], acq, sold, t["proceeds"], 0, basis, "B", t["adj"], t["proceeds"] + t["adj"]])
basis_rows.append(["Total", "", "", "", rsu_proceeds, 0, "", "", sum(t["adj"] for t in trades), rsu_st_gain + rsu_lt_gain])
sch_h_rows = [["Schedule H (Form 1040) - Household Employment Taxes - employer EIN 00-9087731", "Amount"],
              ["A. Paid any one household employee cash wages of $2,800 or more in 2025? (Maria Lopez)", "Yes"],
              ["Line 1 Total cash wages subject to social security tax", NANNY_CASH],
              ["Line 2 Social security tax (x 12.4%)", r(NANNY_CASH * 0.124)],
              ["Line 3 Total cash wages subject to Medicare tax", NANNY_CASH],
              ["Line 4 Medicare tax (x 2.9%)", r(NANNY_CASH * 0.029)],
              ["Line 5/6 Additional Medicare Tax withholding / federal income tax withheld", 0],
              ["Line 8 Total social security, Medicare and income taxes", sch_h_fica],
              ["C. Total cash wages of $1,000 or more in any calendar quarter of 2024 or 2025?", "Yes -> Part II (FUTA)"],
              ["Line 13 Paid unemployment contributions to only one state (WA)?", "Yes"],
              ["Line 14 Paid all state unemployment contributions for 2025 by April 15, 2026? (ESD paid 04/06/2026)", "Yes"],
              ["Line 15 Were all wages that are taxable for FUTA also taxable for state unemployment?", "Yes"],
              ["Line 16 Total cash wages subject to FUTA (first $7,000)", FUTA_BASE],
              ["Line 17 FUTA tax (x 0.6%)", sch_h_futa],
              ["Line 26 Total household employment taxes (to Schedule 2, line 9)", sch_h_total],
              ["Memo: employee share of FICA paid by employer (not withheld) - included in Maria's W-2 box 1 only", ee_share_paid]]
f8814_rows = [["Form 8814 - Parents' Election To Report Child's Interest and Dividends - Chloe M. Kim (" + CHLOE["ssn"] + ")", "Amount"],
              ["Line 1a Child's taxable interest (Cascade FCU)", CHLOE_INT], ["Line 2a Ordinary dividends", 0],
              ["Line 3 Capital gain distributions", 0], ["Line 4 Total", f8814_line4], ["Line 5 Base amount", f8814_base],
              ["Line 6 Subtract line 5 from line 4 (amount included in parents' income - Sch 1 line 8z)", f8814_line6_income],
              ["Line 7-8 Tax computation: smaller of line 4 or $2,700, less $1,350", max(0, min(f8814_line4, 2700) - 1350)],
              ["Line 9/10 Tax (10%) - to Form 1040 line 16 (box 1 checked - Form 8814)", f8814_tax],
              ["Ethan S. Kim - NOT eligible (capital gain from a sale + wages) - files own return, client EVG1021 (Form 8615)", ""]]
a_compare = [["Schedule A - SALT election (WA has no income tax)", "Amount"],
             ["Option 1 - state/local income taxes: WA PFML employee premiums (W-2 box 14) treated as income taxes per Rev. Rul. 2025-4", r(1157.19 + 854.26)],
             ["Option 2 - general sales tax: IRS Sales Tax Deduction Calculator (ZIP 98008, family of 4, income per worksheet; 10.1% combined rate)", 3912],
             ["Elected: general sales tax (line 5a, box 5a checked)", 3912],
             ["Real estate tax (King County, per 1098 box 10 / receipt)", r(14236.40)],
             ["SALT total vs cap $40,000 (MAGI < $500,000 - no phase-down)", 3912 + r(14236.40)],
             ["Mortgage interest (acquisition debt $648k < $750k post-2017 limit - fully deductible)", r(24310.55)],
             ["Charitable cash", 4000], ["Total itemized", v["itemized_total_computed"]], ["Standard deduction MFJ", 31500]]
q_rows = [["Form 1099-Q review - WA529 (beneficiary Chloe)", "Amount"],
          ["Gross distribution 08/12/2025 (paid to Lakeside Hills Academy)", 10000], ["Earnings (box 2)", 3122.61],
          ["Qualified K-12 tuition (limit $10,000 per beneficiary for 2025)", 10000],
          ["Adjusted qualified education expenses >= distribution -> taxable earnings", 0],
          ["No AOTC/LLC claimed for the same expenses (K-12 is not eligible for education credits)", ""]]
C.write_return(R, [
    ("Taxpayer / Spouse", f"{T['name']} ({T['ssn']}) / {S['name']} ({S['ssn']})"),
    ("Address", ", ".join(ADDR)),
    ("Filing status", "Married filing jointly"),
    ("Dependents", "Ethan S. Kim (son, 2009) - CTC; Chloe M. Kim (daughter, 2013) - CTC. Ethan files his own 2025 return (EVG1021) and checks 'can be claimed as a dependent'."),
    ("Digital assets question", "No"),
    ("Forms included", "1040, Schedules 1 (none), 2, 3 (none), A, B, D, H, 8812, Forms 8949, 8814 (Chloe), 2441, 8959, 8960"),
    ("Household employer", "EIN 00-9087731 (obtained 03/03/2026); Form W-2/W-3 for Maria Lopez filed with SSA 03/10/2026; corrected 1099-NEC ($0) filed"),
    ("State", "None - Washington has no individual income tax. WA capital gains excise: not required (long-term gains far below WA standard deduction)."),
    ("Filing method", "E-file (Form 8879 signed 04/11/2026); refund by direct deposit to checking ****6630"),
], attachments=[("Schedule H - Household Employment Taxes", sch_h_rows),
                ("Form 8814 - Chloe (parents' election)", f8814_rows),
                ("RSU cost-basis adjustment (Form 8949 code B)", basis_rows),
                ("Schedule A - sales tax vs income tax and itemized vs standard", a_compare),
                ("Form 1099-Q - K-12 tuition (not taxable)", q_rows)])

# ====================================================================== ANSWER KEY
gotchas = [
    gotcha("EVG1010-G1", "Review - Kid Taxes and Filings (separate client ID / project code)", "Ethan cannot go on Form 8814",
           "Follow the client's request / PY return and report Ethan's $6,400 UTMA income on the parents' return via Form 8814.",
           "Form 8814 is available only if the child's income is solely interest and dividends (incl. capital gain distributions) "
           "and < $13,500. Ethan has a $3,100 capital gain from a fund SALE and $3,200 of wages -> not eligible. Unearned income "
           "$6,400 > $2,700 -> Form 8615 on Ethan's own return. Separate client ID EVG1021 and 1040 project code opened.",
           "Parents' return must show nothing for Ethan; Ethan's return EVG1021 carries the kiddie tax", ["16"], "hard"),
    gotcha("EVG1010-G2", "Review - Kid Taxes and Filings (Form 8814)", "Chloe's $1,900 interest - Form 8814 election",
           "Either ignore Chloe's 1099-INT (below $2,700 so 'nothing to report') or add $1,900 to the parents' interest income.",
           "Chloe must file (unearned > $1,350) unless parents elect Form 8814. Elected: line 4 $1,900 < $2,700 base -> $0 added to parents' "
           f"income; tax 10% x ($1,900 - $1,350) = ${f8814_tax} added to Form 1040 line 16. Trade-off: identical tax to a separate return "
           "for Chloe, one fewer return and fee; no AGI-based items of the parents are affected because $0 is included.",
           f"Line 16 +${f8814_tax}", ["16"], "medium"),
    gotcha("EVG1010-G3", "Schedule D - missing cost basis on Consolidated 1099 (equity comp)", "RSU shares reported with $0 basis",
           f"Autoflow takes the 1099-B basis of $0 -> {fmt(rsu_proceeds)} of proceeds taxed as gain (the $86,400 of 2025 vest income and the "
           "2023 lot income were already taxed as W-2 wages).",
           "Form 8949 box B (short-term) / box E (long-term) - basis not reported to IRS; enter 1099-B basis $0, code B, and a negative "
           f"column (g) adjustment equal to FMV at vest from the supplemental statement. Net RSU gain {fmt(rsu_st_gain + rsu_lt_gain)} "
           f"(ST {fmt(rsu_st_gain)}, LT {fmt(rsu_lt_gain)}).",
           f"Line 7 overstated by ~{fmt(rsu_proceeds - rsu_st_gain - rsu_lt_gain)} if missed", ["7"], "medium"),
    gotcha("EVG1010-G4", "Scan - unstructured documents / Payment-app export (household employee)", "Nanny treated as a 1099 contractor",
           "Accept the client's 1099-NEC treatment (or ignore it - 'not our client's income') and file with no Schedule H.",
           "Maria is a household employee (family controls when/how the work is done, in their home, their car, weekly pay, no other clients). "
           f"Cash wages $28,000 >= $2,800 (2025) -> Schedule H: SS/Medicare 15.3% = ${sch_h_fica:,}; FUTA 0.6% x $7,000 = ${sch_h_futa} "
           f"(WA ESD contributions paid by 04/15/2026) -> ${sch_h_total:,} on Schedule 2 line 9. Obtain EIN, file W-2/W-3 (box 1 includes the "
           "$2,142 employee share paid by the employer), file corrected $0 1099-NEC, register with WA ESD; 2024 wages $6,240 also exceeded the "
           "2024 $2,700 threshold -> amend 2024 (separate project).",
           f"Total tax understated ${sch_h_total:,}", ["23", "24"], "hard"),
    gotcha("EVG1010-G5", "Form 2441 / W-2 box 10", "Dependent-care FSA displaces the credit",
           "Claim a $600 credit (20% x $3,000) for Chloe's nanny costs in addition to the $5,000 FSA exclusion.",
           "Only Chloe (under 13) is a qualifying person (Ethan is 16). With one qualifying person the credit base is $3,000 - $5,000 "
           "excluded FSA benefits = $0. Form 2441 is still required (Part III) to support the $5,000 exclusion and list the provider (Maria, SSN).",
           "Credit $0, not $600", ["20"], "medium"),
    gotcha("EVG1010-G6", "Form 1099-Q", "529 distribution for private K-12 tuition",
           "Treat the $3,123 earnings in box 2 as taxable (no 1098-T), or claim an education credit for the tuition.",
           "Up to $10,000 per year per beneficiary of K-12 tuition is a qualified expense for 2025 (the $20,000 limit starts 2026). "
           "Distribution $10,000 = qualified tuition -> $0 taxable; nothing on the 1040. K-12 tuition is not eligible for AOTC/LLC.",
           "Avoids $3,123 of phantom income", ["8"], "easy"),
    gotcha("EVG1010-G7", "Schedule 8812 / Form 8959 / Form 8960", "High-income phase-outs and surtaxes",
           "Full $4,400 CTC; skip Form 8959 because the employer 'already withheld Additional Medicare'; skip NIIT.",
           f"CTC reduced $50 per $1,000 of MAGI over $400,000 -> ${v['19']:,}. Form 8959: combined Medicare wages "
           f"{fmt(w2_t['5'] + w2_s['5'])} - $250,000 MFJ threshold x 0.9% = ${f8959:,}; employer withheld only ${v['addl_medicare_withheld']:,} "
           f"(on Daniel's wages over $200,000) - credited on line 25c. NIIT 3.8% x NII {fmt(parent_niit_gross)} = ${v['niit']:,}.",
           "Several thousand dollars of tax", ["19", "23", "25c"], "medium"),
    gotcha("EVG1010-G8", "Schedule A - sales tax vs income tax (no-income-tax state)", "WA residents: general sales tax election",
           "Enter $0 on line 5a (no state income tax), or add both PFML premiums and sales tax.",
           "Elect general sales taxes (IRS calculator / Axcess blended-rate option): $3,912 > PFML premiums treated as income tax. "
           "Only one of income or sales tax may be itemized. Itemized total exceeds the $31,500 standard deduction.",
           "Schedule A line 5a", ["12e"], "easy"),
]
C.write_answer_key(R, {"residence": "WA (no state income tax return)", "complexity": "Equity comp + household employer + kiddie tax",
                       "related_clients": ["EVG1021 (Ethan - Form 8615 uses this return's taxable income)"]}, gotchas,
                   state=[{"jurisdiction": "Washington", "return": "None (no personal income tax)",
                           "note": "WA capital gains excise (RCW 82.87) - long-term gains far below the WA standard deduction; no return. "
                                   "Household employer: WA ESD unemployment registration/contributions (outside 1040)."}],
                   filings=[{"form": "Form 1040 (federal) incl. Schedule H", "method": "e-file", "due": "2026-04-15", "filed": "2026-04-13"},
                            {"form": "Form W-2 / W-3 (Maria Lopez)", "method": "SSA e-file", "due": "2026-02-02", "filed": "2026-03-10 (late)"},
                            {"form": "Corrected Form 1099-NEC ($0)", "method": "IRIS", "filed": "2026-03-10"},
                            {"form": "EVG1021 - Ethan Kim Form 1040 with Form 8615", "method": "e-file", "due": "2026-04-15", "filed": "2026-04-14"},
                            {"form": "2024 Form 1040-X with Schedule H (2024 nanny wages $6,240)", "method": "separate MISC project", "status": "in WIP"}],
                   extra={"form_8615_parent_data_exported": PARENT_8615})

C.write_receipt_log("EVG1010-1040-2025", "P. Anand (staff)", "M. Okafor (senior)", "S. Kennedy, CPA", "2026-02-09",
                    extra="Related project codes opened 02/23/2026: **EVG1021-1040-2025** (Ethan Kim - separate client ID) and "
                          "**EVG1010-MISC-2025** (household employer setup, 2024 amended return).")
C.write_notes(f"""
# EVG1010 - Kim, Daniel & Grace - 2025 Form 1040 - Preparer Notes

*Synthetic client - Project Evergreen. Return status: **signed off, e-filed 04/13/2026, accepted.***

## Return summary
| | |
|---|---|
| Filing status | Married filing jointly |
| AGI (line 11) | {fmt(v['11'])} |
| Deduction | Itemized {fmt(v['12e'])} (standard would be $31,500) |
| Taxable income (line 15) | {fmt(v['15'])} - **exported to EVG1021 (Ethan) Form 8615 line 6** |
| Tax (line 16) | {fmt(v['16'])} (includes Form 8814 tax on Chloe's interest {fmt(f8814_tax)}) |
| Child tax credit | {fmt(v['19'])} (2 x $2,200 less phase-out {fmt(ctc_red)}) |
| Other taxes (line 23) | {fmt(v['23'])} = Schedule H {fmt(sch_h_total)} + Form 8959 {fmt(f8959)} + NIIT {fmt(v['niit'])} |
| Total tax (line 24) | {fmt(v['24'])} |
| Payments | W-2 withholding {fmt(v['25a'])} + Additional Medicare withheld {fmt(v['25c'])} |
| **{'Refund' if v['refund'] else 'Balance due'}** | **{fmt(v['refund'] or v['balance_due'])}** |

## What I did and why (plain English)
1. **Wages.** Daniel {fmt(w2_t['1'])} (includes RSU vest income $86,400 shown in box 14) and Grace {fmt(w2_s['1'])}. Box 12 C (group-term
   life over $50k) is already in box 1; D and DD need no entry. WA PFML in box 14 is informational (see #8).
2. **RSU stock sales (Form 8949).** Summit Shareworks reported 6 sales with **$0 basis** and "basis not reported to IRS". The supplemental
   statement gives the FMV at release, which was already taxed as wages. I reported each sale in box B (short-term: the four sell-to-cover
   sales and the 12/05 sale) or box E (long-term: 150 shares from the 03/15/2023 release), entered the 1099-B basis $0, code **B**, and a
   negative column (g) adjustment equal to the FMV basis. Net result: ST {fmt(rsu_st_gain)}, LT {fmt(rsu_lt_gain)} instead of
   {fmt(rsu_proceeds)} of phantom gain. Joint Rainier account: interest {fmt(J_INT)}, dividends {fmt(J_ORD)} (qualified {fmt(J_QUAL)}),
   capital gain distributions {fmt(J_CGD)} (Sch D line 13). Schedule D line 16 {fmt(sd['line16'])}.
3. **Nanny = household employee (Schedule H).** The organizer said "no household employees" and the clients sent Maria a 1099-NEC,
   but the facts (their home, their schedule and duties, their car, weekly pay, no other clients) make her a common-law employee.
   Nannies are the classic household employee (Pub. 926). 2025 cash wages {fmt(NANNY_CASH)} >= $2,800, so:
   - Social security 12.4% + Medicare 2.9% on $28,000 = {fmt(sch_h_fica)}. The Kims did not withhold Maria's share, and chose to pay it
     rather than recover it from her; the {fmt(ee_share_paid)} employee share they pay is extra **wages for income tax only** (W-2 box 1
     $30,142.00; boxes 3/5 stay $28,000).
   - FUTA: wages of $1,000+ in a quarter -> 0.6% x $7,000 = {fmt(sch_h_futa)}. The 0.6% net rate assumes full state credit, which
     requires the WA ESD contributions to be paid by 04/15/2026 - Grace paid them 04/06/2026 (Schedule H line 14 "Yes").
   - Schedule H total {fmt(sch_h_total)} -> Schedule 2 line 9. Paid with the return (no penalty - see #9).
   - Admin items done outside the 1040: EIN obtained 03/03/2026; W-2/W-3 filed 03/10/2026 (after the 02/02/2026 due date - possible
     late-filing penalty; we will request first-time/reasonable-cause relief if a notice arrives); corrected $0 1099-NEC filed; WA ESD
     registration 03/12/2026. WA L&I and WA PFML/WA Cares obligations for household employers referred to a payroll provider (not a 1040 item).
   - **2024:** Maria was paid $6,240 in Sept-Dec 2024, over the 2024 $2,700 threshold - a 2024 Schedule H (1040-X) is needed.
     Opened as a separate MISC project (in WIP, billed separately).
4. **Form 2441.** Chloe (12) is the only qualifying person - Ethan is 16. Grace's $5,000 dependent-care FSA (W-2 box 10) is excluded;
   with one qualifying person the credit base is $3,000 less the $5,000 exclusion = **$0 credit**. Form 2441 is still filed (provider:
   Maria Lopez, SSN on file) to support the exclusion - taxable benefits $0.
5. **Kids' investment income (Kid Taxes procedure).**
   - **Ethan (16):** UTMA interest $900 + dividends $2,400 (qualified $1,900) + a $3,100 long-term gain from selling part of his index fund,
     plus a $3,200 summer W-2. Grace asked for Form 8814 again, but 8814 only works when the child's income is only interest and dividends -
     the fund **sale** (and the wages) disqualify him. Unearned income $6,400 > $2,700 -> kiddie tax on **his own return with Form 8615**.
     Per procedure, discussed with Grace (02/20) and opened a separate client ID **EVG1021** with its own 1040 project code. His return was
     finished after this one because Form 8615 needs our taxable income ({fmt(v['15'])}), tax, qualified dividends {fmt(v['3a'])} and net
     capital gain {fmt(sd['ncg'])}.
   - **Chloe (12):** only $1,900 of credit-union interest. She must file (unearned > $1,350) unless we elect Form 8814. Election made:
     nothing added to our income (under $2,700); tax = 10% x ($1,900 - $1,350) = **{fmt(f8814_tax)}** on line 16. Trade-off explained
     to Grace: the tax is the same $55 either way; 8814 saves a return and a fee. (If the parents' AGI mattered for any credit or
     deduction, including the child's income could hurt - not the case here since $0 is included.)
6. **WA529 1099-Q ($10,000).** Paid directly to Lakeside Hills Academy for grade-7 tuition. K-12 tuition up to $10,000 per beneficiary
   per year is a qualified expense in 2025 -> not taxable; nothing reported.
7. **CTC, Additional Medicare, NIIT.** Two children under 17 -> $4,400 before phase-out; MAGI {fmt(v['11'])} exceeds $400,000 by
   {fmt(v['11'] - 400000)} -> reduction {fmt(ctc_red)} -> CTC {fmt(v['19'])} (nonrefundable, fully used). Form 8959: Medicare wages
   {fmt(w2_t['5'] + w2_s['5'])} - $250,000 x 0.9% = {fmt(f8959)}; Northshore withheld {fmt(v['addl_medicare_withheld'])} (0.9% over $200,000
   of Daniel's wages), claimed on line 25c. NIIT: NII {fmt(parent_niit_gross)} (interest, dividends, CG distributions, net RSU gains)
   x 3.8% = {fmt(v['niit'])} (MAGI is far over $250,000, so the full NII is taxed).
8. **Itemized deductions.** WA has no income tax, so I elected **general sales tax** ($3,912 per the IRS calculator - Axcess blended-rate
   option). Even if the WA PFML employee premiums are treated as state income taxes (Rev. Rul. 2025-4), that option is only
   ${r(1157.19 + 854.26):,}. SALT {fmt(3912 + r(14236.40))} (well under the $40,000 cap; MAGI < $500,000). Mortgage interest $24,311
   (post-2017 loan, balance $648k < $750k - no limitation), charity $4,000. Total {fmt(v['12e'])} vs $31,500 standard -> itemize.
9. **Estimated tax penalty.** None. 2025 withholding {fmt(v['25d'])} exceeds 110% of 2024 total tax (110% x $72,797 = $80,077), and
   Schedule H taxes are included in the 2210 computation and covered by that safe harbor.
10. **Washington.** No income tax return. WA capital gains excise applies only to long-term gains above the WA standard deduction
    (~$278,000 for 2025) - LT gains here are ~{fmt(sd['net_lt'])}; not required.

## Open items / client communication
- None for the 2025 return. MISC project: 2024 amended return with Schedule H (Maria's 2024 wages) - in WIP.
- Advised clients: for 2026 either withhold Maria's income tax / FICA through a household payroll service or increase W-4 withholding
  to cover Schedule H; give Maria a 2026 W-4; calendar the 01/31 W-2 deadline.
- Next year Ethan will be 17: no CTC for him (ODC $500 instead), and kiddie tax still applies.

## Hand-off to signer / routing
- [x] Return locked; Accountant's copy saved as *reviewed*
- [x] Federal 1040 incl. Schedule H - e-file; no state return; no FBAR
- [x] Due date 04/15/2026 - filed 04/13/2026 (no extension)
- [x] Related filings routed: EVG1021 Ethan 1040 (e-filed 04/14/2026); W-2/W-3 (SSA, filed 03/10/2026); corrected 1099-NEC
- [x] eSign (Form 8879) - Grace preferred contact via email; refund by direct deposit (voided check on file)
- Billing: tier $2,400 + household-employer setup (EIN, W-2/W-3, corrected 1099, ESD guidance) 3.0 hrs billed on EVG1010-MISC-2025 (client
  chargeable - external reason: client-provided treatment was wrong). Ethan's return billed on its own project code. Nothing to W/O.
""")
C.write_review_points(f"""
# Review Points - EVG1010 - 2025 - Form 1040

*Reviewer: M. Okafor (blue). Preparer responses in red. Synthetic.*

1. **WP 4 / Form 8949** - Autoflow imported the Summit Shareworks 1099-B with $0 basis: Schedule D showed {fmt(rsu_proceeds + J_CGD)} of gain.
   - Pull FMV at release from the supplemental statement (WP 5); box B/E, code B, negative adjustment. Tie to W-2 box 14 RSU $86,400.
   - *Preparer: Done - net RSU gain now {fmt(rsu_st_gain + rsu_lt_gain)}; tape on WP 5.*
2. **Kid Taxes** - First draft put Ethan's UTMA income on Form 8814 per the client's request ("same as last year").
   - He sold fund shares ($3,100 LTCG) and has wages -> not eligible for 8814. Remove from our return; per procedure open a separate client
     ID and 1040 project code for Ethan; discuss with Grace first.
   - *Preparer: Removed. Grace agreed 02/23; EVG1021 created; Form 8615 prepared from this return's final TI.*
3. **Form 8814 (Chloe)** - OK to elect. Confirm $0 is added to income (under $2,700) and $55 tax is on line 16 with the 8814 box.
   - *Preparer: Confirmed.*
4. **Nanny** - WP 14/15: Venmo shows $560 every week to Maria Lopez and the clients issued her a 1099-NEC. Organizer says no household
   employee. Based on the 02/20 interview she is a household employee - Schedule H required, not a 1099.
   - Compute SS/Medicare on cash wages and FUTA; confirm WA ESD paid before 04/15 for the 0.6% rate; EIN, W-2/W-3, corrected 1099-NEC.
   - Also check 2024 - $6,240 paid Sept-Dec 2024 exceeds the 2024 threshold.
   - *Preparer: Schedule H {fmt(sch_h_total)} added. EIN/W-2/W-3/corrected 1099-NEC done 03/03-03/10. ESD paid 04/06 (WP 19). 2024 1040-X set up as MISC project.*
5. **Form 2441** - Draft claimed $600 credit. The FSA exclusion ($5,000) exceeds the $3,000 one-child limit -> $0. Ethan is not a
   qualifying person (16).
   - *Preparer: Corrected; 2441 kept for the exclusion.*
6. **1099-Q** - Draft picked up box 2 earnings $3,123 as other income. K-12 tuition up to $10,000 is qualified for 2025 - remove.
   - *Preparer: Removed; tuition statement on WP 8.*
7. **Schedule A** - Line 5a was blank. Use the sales tax table (WA has no income tax). Don't add PFML on top of it.
   - *Preparer: Sales tax $3,912 entered; comparison on WP.*
8. FYI - Form 8959: employer withheld 0.9% on Daniel's wages over $200k, but the MFJ threshold is $250k on combined wages - tax
   {fmt(f8959)}, withholding credit {fmt(v['addl_medicare_withheld'])} on line 25c. CTC phase-out and NIIT look right.
""")
print("EVG1010 done", R.summary()["24"], v["refund"], v["balance_due"], "TI", v["15"])
