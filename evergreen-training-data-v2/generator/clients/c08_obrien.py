"""EVG1008 - Kevin & Samantha O'Brien (MFJ, Pennsylvania - Lancaster). Long-term duplex rental (1098 for the rental
address that autoflow treats as personal; roof capitalized vs water heater de minimis vs window repair; passive loss
suspended at MAGI > $150k with a PY carryforward the organizer omits) + Poconos cabin used personally 21 days and
rented 62 days (sec. 280A vacation-home limitation, IRS day allocation, carryovers); freshman daughter AOTC in the
MAGI phase-out; ODC for an 18-year-old; PA-40 class rules (PA taxes 401(k)/403(b) deferrals; rent-class loss can't
offset compensation)."""
from common import ClientBuild, gotcha, fmt
from docs import statement, scanned_pages, write_text, write_xlsx, write_csv
import forms as F
from tax2025 import Return1040, r, macrs_residential

C = ClientBuild("EVG1008", "OBrien", "Kevin & Samantha O'Brien")
ADDR = ("86 Hawthorne Ridge Dr", "Lancaster, PA 17601")
T = {"name": "Kevin M. O'Brien", "ssn": "XXX-XX-2841", "dob": "1975-05-14"}
S = {"name": "Samantha J. O'Brien", "ssn": "XXX-XX-7719", "dob": "1977-09-30"}
REC_J = ["Kevin M. & Samantha J. O'Brien", *ADDR, f"TIN: {T['ssn']}"]
DUPLEX = "128-130 Chestnut Row, Lancaster, PA 17602"
CABIN = "27 Blue Heron Ln, Pocono Lake, PA 18347"

# ================================================================== facts / judgement calls
w2_k = {"1": 98500.00, "2": 11800.00, "3": 110500.00, "4": 110500 * .062, "5": 110500.00, "6": 110500 * .0145,
        "12": [("D", 12000.00), ("DD", 16240.00)], "13": ["Retirement plan: X"], "14": [("PA LST", 52.00)],
        "state": [{"state": "PA", "id": "8810-4471", "wages": 110500.00, "tax": round(110500 * .0307, 2)}],
        "local": [{"wages": 110500.00, "tax": 1105.00, "name": "MANHEIM TWP EIT (LCTCB)"}], "control": "CPC-2291"}
w2_s = {"1": 72800.00, "2": 7900.00, "3": 78800.00, "4": 78800 * .062, "5": 78800.00, "6": 78800 * .0145,
        "12": [("E", 6000.00), ("DD", 9880.00)], "13": ["Retirement plan: X"], "14": [("PA LST", 52.00)],
        "state": [{"state": "PA", "id": "3310-2208", "wages": 78800.00, "tax": round(78800 * .0307, 2)}],
        "local": [{"wages": 78800.00, "tax": 788.00, "name": "MANHEIM TWP EIT (LCTCB)"}], "control": "LRHS-10433"}
INT_FULTON = 382.10

# --- Rental #1: duplex (long-term, both units available all year)
RENT_A, RENT_B, LATE_FEES = 1350.00 * 12, 1295.00 * 10, 75.00      # unit B vacant Mar-Apr (advertised - still fair rental)
DUP_RENTS = RENT_A + RENT_B + LATE_FEES
DUP_1098_INT, DUP_RE_TAX = 9860.00, 5420.00
DUP_EXP = {  # Schedule E line: amount
    "5 Advertising": 85.00, "6 Auto and travel (380 mi x 70c)": 380 * .70, "7 Cleaning and maintenance (lawn/snow)": 600.00,
    "9 Insurance": 1640.00, "12 Mortgage interest paid to banks (Form 1098)": DUP_1098_INT,
    "14 Repairs (window 450, plumbing 780, misc 1,120)": 450.00 + 780.00 + 1120.00, "16 Taxes": DUP_RE_TAX,
    "17 Utilities (water/sewer/trash)": 1380.00, "19 Other - water heater (de minimis safe harbor)": 1900.00}
BLDG_BASIS, KITCHEN = 220000.00, 18000.00           # PERM: bought 04/2018 $265,000 (land $45,000); kitchen 09/2021
ROOF, ROOF_MONTH = 14000.00, 6                        # full tear-off replacement completed 06/2025 -> capitalize 27.5-yr
DEP_BLDG = r(BLDG_BASIS / 27.5)
DEP_KITCHEN = r(KITCHEN / 27.5)
DEP_ROOF = macrs_residential(ROOF, ROOF_MONTH, 1)
DUP_DEP = DEP_BLDG + DEP_KITCHEN + DEP_ROOF
DUP_EXP["18 Depreciation (Form 4562)"] = DUP_DEP
DUP_TOTAL_EXP = r(sum(DUP_EXP.values()))
DUP_NET = r(DUP_RENTS) - DUP_TOTAL_EXP
PY_SUSPENDED = 6200.00                                # Form 8582 carryover per PY return (organizer silent)

# --- Rental #2: Poconos cabin (sec. 280A(d) residence: personal days 21 > greater of 14 or 10% x 62)
RENT_DAYS, PERS_DAYS = 62, 21
USE_DAYS = RENT_DAYS + PERS_DAYS
FRAC = RENT_DAYS / USE_DAYS
CAB_GROSS = 14880.00
CAB_FEES = round(CAB_GROSS * .08, 2)                  # VRBO host fee 5% + payment processing 3%
CAB_CLEAN = 1240.00                                   # guest turnover cleaning (rental only)
CAB_INT, CAB_TAX = 8300.00, 3320.00
CAB_OPER = {"Utilities": 2490.00, "Insurance": 1660.00, "Repairs (deck boards, plumbing)": 830.00, "Supplies (linens, consumables)": 415.00}
CAB_BLDG = 250000.00                                  # bought 06/2020 $310,000 (land $60,000); FMV at conversion higher -> use basis
CAB_PIS_MONTH = 5                                     # first listed/available 05/01/2025
cab_dep_full = macrs_residential(CAB_BLDG, CAB_PIS_MONTH, 1)
CAB_DEP_RENTAL = r(cab_dep_full * FRAC)
# Worksheet 5-1 (Pub. 527) ordering
w_int, w_tax = r(CAB_INT * FRAC), r(CAB_TAX * FRAC)
w_direct = r(CAB_FEES + CAB_CLEAN)
tier1 = w_int + w_tax + w_direct
room1 = r(CAB_GROSS) - tier1
oper_rental = {k: r(a * FRAC) for k, a in CAB_OPER.items()}
oper_total = sum(oper_rental.values())
oper_allowed = min(oper_total, max(0, room1))
oper_co = oper_total - oper_allowed
room2 = max(0, room1 - oper_allowed)
dep_allowed = min(CAB_DEP_RENTAL, room2)
dep_co = CAB_DEP_RENTAL - dep_allowed
CAB_NET = r(CAB_GROSS) - tier1 - oper_allowed - dep_allowed
assert CAB_NET == 0
PERS_INT, PERS_TAX = r(CAB_INT - w_int), r(CAB_TAX - w_tax)

# --- passive loss (Form 8582)
MAGI_8582 = None  # set after AGI is known

# --- education
TUITION_BOX1, SCHOLARSHIP = 18400.00, 6000.00
QEE = TUITION_BOX1 - SCHOLARSHIP
# --- Schedule A items (comparison)
HOME_INT, HOME_RE, CHARITY = 7400.00, 6100.00, 2400.00

# ================================================================== PERM
C.write_profile(f"""
# EVG1008 - O'Brien, Kevin & Samantha  (PERM)

*Synthetic client - Project Evergreen training data.*

| Item | Detail |
|---|---|
| Client ID | EVG1008 |
| Taxpayer | Kevin M. O'Brien, DOB 05/14/1975, SSN XXX-XX-2841 - production manager, Conestoga Precision Components |
| Spouse | Samantha J. O'Brien, DOB 09/30/1977, SSN XXX-XX-7719 - RN care coordinator, Lancaster Regional Health System |
| Address | {ADDR[0]}, {ADDR[1]} (Manheim Township, Lancaster County) - PA full-year residents |
| Dependents | Emma O'Brien (DOB 03/18/2007) - started Penn State (University Park) fall 2025, full-time; Connor O'Brien (DOB 08/02/2011) |
| Rental #1 | Duplex {DUPLEX} - purchased 04/2018 ($265,000; land $45,000). Long-term tenants; self-managed. Mortgage with Susquehanna Valley Mortgage (in both names). |
| Rental #2 | Cabin {CABIN} (Monroe County) - purchased 06/2020 ($310,000; land $60,000), family vacation home. **Listed on VRBO starting 05/2025.** Mortgage with Pocono Community Bank. |
| Passive | Duplex losses suspended every year (MAGI > $150k) - see Form 8582 carryover on PY summary. |
| Local | Manheim Twp EIT withheld by both employers; annual local EIT final return filed separately with Lancaster County Tax Collection Bureau (LCTCB) - admin handles. |
| Contact | Samantha - sam.obrien@example.com, (717) 555-0129; eSign OK |
| Engagement | Client since 2018. Rental tier ($1,450 + $250 per additional rental). |
""")
F.prior_year_summary(C.perm_file("2024_Form_1040_Return_Summary.pdf", "Prior-year return summary"), "Kevin & Samantha O'Brien",
    "EVG1008", "Married filing jointly", [
        ["1a", "W-2 wages", 164900], ["2b", "Interest - Fulton Bank", 355],
        ["Sch E", f"Duplex {DUPLEX}: rents 28,400; net loss (3,050) - passive, fully suspended (Form 8582)", 0],
        ["11", "AGI", 165255], ["12", "Standard deduction (itemized 28,800 incl. cabin as 2nd home)", 29200],
        ["15", "Taxable income", 136055], ["19", "CTC (Connor) + ODC (Emma, age 17 -> CTC in 2024)", 4000],
        ["35a", "Refund", 1680]],
    carryovers=[["Form 8582 - prior-year unallowed passive loss, duplex (2023 3,150 + 2024 3,050)", PY_SUSPENDED],
                ["Sec. 280A carryover (cabin)", 0], ["Capital loss carryover", 0]],
    notes="PY WP: MAGI above $150k -> no $25k special allowance; carry the suspended duplex loss. Cabin was 100% personal in 2024 "
          "(second home - interest/taxes on Sch A worksheet, standard deduction still larger). Clients mentioned possibly renting the "
          "cabin in 2025 - if so, track rental and personal-use days. Emma starts college fall 2025 - get the 1098-T and bursar statement.")
statement(C.perm_file("Depreciation_Schedule_Rentals.pdf", "Depreciation schedule (rental)"),
    "O'Brien - Rental Depreciation Schedule (through 12/31/2024)", [
        {"table": [["Asset", "In service", "Basis", "Method", "Annual", "Accum. 12/31/2024"],
                   [f"Duplex building - {DUPLEX}", "04/2018", BLDG_BASIS, "27.5 SL MM", DEP_BLDG, r(BLDG_BASIS / 27.5 * 8.5 / 12) + DEP_BLDG * 6],
                   ["Land - duplex (not depreciable)", "04/2018", 45000.00, "-", 0, 0],
                   ["Unit A kitchen remodel", "09/2021", KITCHEN, "27.5 SL MM", DEP_KITCHEN, r(KITCHEN / 27.5 * 3.5 / 12) + DEP_KITCHEN * 3]],
         "left_align_cols": [0, 1, 3]},
        {"note": "Cabin (27 Blue Heron Ln) - personal use only through 2024 - not on schedule."}])

# ================================================================== PBC
EMP_K = {"name": "Conestoga Precision Components Inc", "addr1": "2400 Oregon Pike", "addr2": "Lancaster, PA 17601", "ein": "00-2238104"}
EMP_S = {"name": "Lancaster Regional Health System", "addr1": "555 N Duke St", "addr2": "Lancaster, PA 17602", "ein": "00-1104772"}
EE_K = {"name": T["name"], "addr1": ADDR[0], "addr2": ADDR[1], "ssn": T["ssn"]}
EE_S = {"name": S["name"], "addr1": ADDR[0], "addr2": ADDR[1], "ssn": S["ssn"]}
F.organizer(C.pbc_file("01_2025_Organizer_completed.pdf", "Client organizer", "2026-02-24"), "Kevin & Samantha O'Brien", "EVG1008",
    general=[("Did your marital status change during 2025?", "No", ""),
             ("Were there any changes in dependents?", "No", "Emma started Penn State in August"),
             ("Did you pay higher-education expenses?", "Yes", "1098-T + bursar statement"),
             ("Do you own rental property?", "Yes", "Duplex (see spreadsheet) + we started renting the cabin on VRBO in May"),
             ("Did you personally use any rental property?", "Yes", "Cabin - family used it a few weeks, see calendar"),
             ("Did you make improvements to a rental?", "Yes", "New roof on the duplex in June, water heater unit B"),
             ("Did you make estimated tax payments?", "No", ""),
             ("Did you receive, sell, exchange digital assets?", "No", "")],
    dependents=[["Emma O'Brien", "Daughter", "03/18/2007", "5540", "12 (at school Aug-Dec)", "Yes"],
                ["Connor O'Brien", "Son", "08/02/2011", "9021", "12", "No"]],
    income_rows=[["Wages", "Conestoga Precision Components", 93100, "see W-2"],
                 ["Wages", "Lancaster Regional Health System", 71800, "see W-2"],
                 ["Interest", "Fulton Bank", 355, "382"],
                 ["Rental - 128-130 Chestnut Row (duplex) - rents", "tenants", 28400, "see Excel"],
                 ["Rental - 128-130 Chestnut Row - net income (loss)", "", -3050, ""],
                 ["Rental - 27 Blue Heron Ln (cabin) - rents", "VRBO", "", "see VRBO 1099-K"]],
    deductions_rows=[["Mortgage interest", "Members 1st FCU (home)", 7710, "see 1098"],
                     ["Mortgage interest", "Pocono Community Bank (cabin)", 8500, "see 1098"],
                     ["Real estate tax", "Home - Manheim Twp", 5950, "6,100"],
                     ["Real estate tax", "Cabin - Tobyhanna Twp", 3250, "3,320"],
                     ["Charitable", "St. Anne Parish / United Way", 2600, "2,400"]],
    signature_date="02/21/2026")
F.w2(C.pbc_file("02_W-2_Conestoga_Precision_Kevin.pdf", "Form W-2", "2026-02-24"), EMP_K, EE_K, w2_k)
F.w2(C.pbc_file("03_W-2_Lancaster_Regional_Samantha.pdf", "Form W-2", "2026-02-24"), EMP_S, EE_S, w2_s)
F.f1099_int(C.pbc_file("04_1099-INT_Fulton_Bank.pdf", "Form 1099-INT", "2026-02-24"),
            ["Fulton Bank, N.A.", "One Penn Square", "Lancaster, PA 17602", "TIN: 00-0000052"], REC_J, {"1": INT_FULTON}, account="****3318")
F.f1098(C.pbc_file("05_1098_Susquehanna_Valley_Mortgage.pdf", "Form 1098", "2026-02-24"),
        ["Susquehanna Valley Mortgage Co.", "PO Box 4410", "Harrisburg, PA 17111", "TIN: 00-6120044"], REC_J,
        {"1": DUP_1098_INT, "2": 176402.33, "3": "04/20/2018", "7": "No", "8": DUPLEX, "9": "1",
         "10": f"Property taxes disbursed from escrow {DUP_RE_TAX:,.2f}"})
F.f1098(C.pbc_file("06_1098_Members_1st_FCU_Home.pdf", "Form 1098", "2026-02-24"),
        ["Members 1st Federal Credit Union", "5000 Louise Dr", "Mechanicsburg, PA 17055", "TIN: 00-8770321"], REC_J,
        {"1": HOME_INT, "2": 208110.05, "3": "10/15/2012", "7": "Yes", "8": ADDR[0], "9": "1", "10": f"RE taxes {HOME_RE:,.2f}"})
F.f1098(C.pbc_file("07_1098_Pocono_Community_Bank_Cabin.pdf", "Form 1098", "2026-02-24"),
        ["Pocono Community Bank", "559 Main St", "Stroudsburg, PA 18360", "TIN: 00-4410982"], REC_J,
        {"1": CAB_INT, "2": 238990.71, "3": "06/26/2020", "7": "No", "8": CABIN, "9": "1", "10": f"RE taxes {CAB_TAX:,.2f}"})
statement(C.pbc_file("08_Susquehanna_Valley_Escrow_Annual_Statement_Duplex.pdf", "Lender annual escrow statement", "2026-02-24"),
    "Susquehanna Valley Mortgage Co. - Annual Escrow Account Disclosure / Year-End Summary 2025", [
        {"table": [["Item", "Amount"], ["Loan", "****7751 - " + DUPLEX], ["Principal paid 2025", 7118.40], ["Interest paid 2025", DUP_1098_INT],
                   ["Escrow disbursements - Lancaster City/County/School taxes", DUP_RE_TAX], ["Escrow disbursements - hazard insurance", 1640.00]],
         "left_align_cols": [0]},
        {"para": "This statement is for your records. Your Form 1098 has been mailed separately."}])
F.f1098_t(C.pbc_file("09_1098-T_Penn_State_Emma.pdf", "Form 1098-T", "2026-02-24"),
          ["The Pennsylvania State University", "Bursar - 103 Shields Bldg", "University Park, PA 16802", "TIN: 00-6003624"],
          ["Emma O'Brien", *ADDR, "TIN: XXX-XX-5540"], {"1": TUITION_BOX1, "5": SCHOLARSHIP, "7": "X", "8": "X"})
statement(C.pbc_file("10_Penn_State_LionPATH_Account_Activity_2025.pdf", "Bursar account statement", "2026-02-24"),
    "Penn State LionPATH - Student Account Activity - Emma O'Brien - 2025", [
        {"table": [["Date", "Description", "Charges", "Credits"],
                   ["07/15/2025", "Tuition - Fall 2025 (in-state, lower division)", 9200.00, ""], ["07/15/2025", "Student activity/facility/tech fees - Fall", 610.00, ""],
                   ["07/15/2025", "Room & board - East Halls, Fall", 7420.00, ""], ["08/01/2025", "Provost Award (scholarship) - Fall", "", 3000.00],
                   ["08/12/2025", "Payment - parent (e-check)", "", 14230.00],
                   ["11/20/2025", "Tuition - Spring 2026", 8000.00, ""], ["11/20/2025", "Fees - Spring 2026", 590.00, ""],
                   ["11/20/2025", "Room & board - Spring 2026", 7420.00, ""], ["12/01/2025", "Provost Award (scholarship) - Spring", "", 3000.00],
                   ["12/15/2025", "Payment - parent (checking)", "", 13010.00]], "left_align_cols": [0, 1]},
        {"para": "Required course materials purchased separately (Barnes & Noble, not shown). Qualified tuition & required fees paid in 2025: "
                 "$18,400 (box 1 of Form 1098-T). Scholarships $6,000 (box 5) - restricted to tuition."}])
# rental ledger (Excel)
duplex_rows = [["Date", "Unit", "Payee / payer", "Category", "Income", "Expense", "Memo"]]
for m in range(1, 13):
    duplex_rows.append([f"{m:02d}/01/2025", "A", "Tenant - R. Alvarez", "Rent", 1350.00, "", ""])
    if m not in (3, 4):
        duplex_rows.append([f"{m:02d}/01/2025", "B", "Tenant - J. Kline / (new tenant T. Moyer from 05/2025)", "Rent", 1295.00, "", ""])
duplex_rows += [["03/2025", "B", "Zillow Rentals", "Advertising", "", 85.00, "Unit B vacant Mar-Apr - listed"],
                ["06/03/2025", "A", "Kline - late fee", "Rent", LATE_FEES, "", "late fee Feb"],
                ["02/11/2025", "B", "Weaver Plumbing & Heating", "Repairs", "", 1900.00, "50 gal gas water heater replaced - inv 88710"],
                ["06/20/2025", "Both", "Keystone Roofing LLC", "Repairs", "", ROOF, "New roof - full tear off"],
                ["09/08/2025", "A", "Lancaster Glass Co.", "Repairs", "", 450.00, "Broken window - bedroom"],
                ["Various", "Both", "Weaver Plumbing / Home Depot", "Repairs", "", 780.00 + 1120.00, "plumbing 780; misc 1,120"],
                ["Various", "Both", "Lancaster City Water/Sewer; Penn Waste", "Utilities", "", 1380.00, ""],
                ["Various", "Both", "Green Acres Lawn / snow", "Maintenance", "", 600.00, ""],
                ["Escrow", "Both", "Susquehanna Valley Mortgage", "Insurance", "", 1640.00, "escrow"],
                ["Escrow", "Both", "Susquehanna Valley Mortgage", "Taxes", "", DUP_RE_TAX, "escrow"],
                ["Monthly", "Both", "Susquehanna Valley Mortgage", "Mortgage payment (P&I)", "", DUP_1098_INT + 7118.40, "P&I total - see 1098"],
                ["Various", "Both", "Mileage (Kevin) 380 mi", "Auto", "", "", "trips to duplex"]]
cabin_rows = [["Month", "Nights booked (VRBO)", "Gross bookings", "VRBO fees", "Payout", "Cleaning (guest turnover)"]]
cab_months = [("May", 6, 1440), ("Jun", 11, 2640), ("Jul", 9, 2250), ("Aug", 12, 2940), ("Sep", 8, 1880), ("Oct", 10, 2380), ("Nov", 3, 690), ("Dec", 3, 660)]
assert sum(n for _, n, _ in cab_months) == RENT_DAYS and sum(g for _, _, g in cab_months) == CAB_GROSS
for mth, n, g in cab_months:
    cabin_rows.append([mth, n, float(g), round(g * .08, 2), round(g * .92, 2), round(CAB_CLEAN * n / RENT_DAYS, 2)])
cabin_rows += [["TOTAL", RENT_DAYS, CAB_GROSS, CAB_FEES, round(CAB_GROSS - CAB_FEES, 2), CAB_CLEAN],
               ["", "", "", "", "", ""], ["Cabin annual costs (whole year)", "", "", "", "", ""]]
cabin_rows += [[k, "", "", "", "", a] for k, a in CAB_OPER.items()]
cabin_rows += [["Mortgage interest (1098)", "", "", "", "", CAB_INT], ["Real estate tax (Tobyhanna Twp / Pocono Mtn SD)", "", "", "", "", CAB_TAX]]
write_xlsx(C.pbc_file("11_OBrien_Rental_Ledger_2025.xlsx", "Client spreadsheet (rental ledger)", "2026-02-24"),
           {"Duplex 2025": duplex_rows, "Cabin 2025": cabin_rows})
F.f1099_k(C.pbc_file("12_1099-K_VRBO_Cabin.pdf", "Form 1099-K", "2026-02-24"),
          ["Expedia / VRBO (HomeAway.com, Inc.)", "1111 Expedia Group Way W", "Seattle, WA 98119", "TIN: 00-0000061"],
          ["Kevin M. O'Brien", *ADDR, f"TIN: {T['ssn']}"],
          {"1a": CAB_GROSS, "1b": CAB_GROSS, "2": "6513", "3": 14,
           "months": [0, 0, 0, 0, 1440.00, 2640.00, 2250.00, 2940.00, 1880.00, 2380.00, 690.00, 660.00]}, account="VRBO-4471902")
write_csv(C.pbc_file("13_VRBO_Payout_Report_2025.csv", "Platform export (CSV)", "2026-02-24"),
          ["Reservation", "Check-in", "Nights", "Gross booking (excl. taxes remitted by VRBO)", "Host service fee", "Payment processing", "Payout"],
          [[f"HA-{8840 + i}", f"2025-{m}", n, g, round(g * .05, 2), round(g * .03, 2), round(g * .92, 2)]
           for i, (m, n, g) in enumerate([("05-09", 3, 720), ("05-23", 3, 720), ("06-06", 4, 960), ("06-20", 7, 1680), ("07-18", 4, 1000),
                                           ("07-25", 5, 1250), ("08-01", 5, 1225), ("08-22", 7, 1715), ("09-05", 4, 940), ("09-26", 4, 940),
                                           ("10-03", 5, 1190), ("10-17", 5, 1190), ("11-07", 3, 690), ("12-05", 3, 660)])] +
          [["TOTAL", "", RENT_DAYS, CAB_GROSS, round(CAB_GROSS * .05, 2), round(CAB_GROSS * .03, 2), round(CAB_GROSS * .92, 2)]])
statement(C.pbc_file("14_Keystone_Roofing_Invoice_2025-0619.pdf", "Contractor invoice", "2026-02-24"),
    "Keystone Roofing LLC - Invoice 2025-0619", [
        {"table": [["Description", "Amount"],
                   [f"Complete tear-off of existing roof (2 layers) and replacement - {DUPLEX} (both units): ice & water shield, "
                    "synthetic underlayment, 30-yr architectural shingles, new ridge vent, flashing, 28 squares", 13150.00],
                   ["Replace rotted decking (6 sheets)", 520.00], ["Dumpster / disposal", 330.00], ["TOTAL (paid in full 06/20/2025)", ROOF]],
         "left_align_cols": [0]},
        {"para": "Work completed 06/18/2025. 10-year workmanship warranty."}])
statement(C.pbc_file("15_Weaver_Plumbing_Invoice_88710.pdf", "Contractor invoice", "2026-02-24"),
    "Weaver Plumbing & Heating - Invoice 88710", [
        {"table": [["Description", "Amount"], ["Remove failed 40-gal gas water heater (unit 130 / B)", 180.00],
                   ["Install new Bradford White 50-gal gas water heater, expansion tank, venting to code", 1720.00], ["TOTAL", 1900.00]],
         "left_align_cols": [0]}])
scanned_pages(C.pbc_file("16_IMG_2207_window_receipt.pdf", "Phone photo (image)", "2026-02-24"),
    [["LANCASTER GLASS CO.  -  Service Receipt",
      "Date 09/08/2025   Job: 128 Chestnut Row (unit A, 2nd fl bedroom)",
      "Replace broken double-hung sash glass (IGU) - 1",
      "  Labor 1.5 hr ........................ 165.00",
      "  Insulated glass unit 30x28 .......... 285.00",
      "  TOTAL PAID (check 3310) ............. 450.00",
      "",
      "Cause: tenant reported baseball through window"]], handwritten=False, seed=81, skew=-1.4)
scanned_pages(C.pbc_file("17_Cabin_2025_calendar_Samantha.pdf", "Handwritten calendar (scan)", "2026-02-24"),
    [["CABIN 2025 - who used it  (Sam)",
      "Jan-Apr: closed up, we went up 2x to check pipes (day trips)",
      "May 1 - listed on VRBO!",
      "Jul 3 - Jul 9   us (4th of July week)       7",
      "Aug 10 - Aug 16  us + Emma before college    7",
      "Sep 19 - 21   Pat (Kev's brother) + family  3",
      "     (free - he's family, doesn't count?)",
      "Oct 11-12  Kevin + Connor - rebuilt deck",
      "     stairs, worked all day both days",
      "Nov 26 - 29  Thanksgiving us                4",
      "",
      "VRBO guests: 62 nights (see report)",
      "So we used it about 18 days not counting Pat",
      "and the deck weekend."]], handwritten=True, seed=82)
write_text(C.pbc_file("18_Email_Samantha_cabin_roof_2026-03-10.txt", "Client correspondence", "2026-03-10", "Email"),
"""From: preparer@evergreentax.example
To: Samantha O'Brien <sam.obrien@example.com>
Date: Tue, 3 Mar 2026 09:40:00 -0500
Subject: O'Brien 2025 - cabin and duplex questions

Hi Sam - a few questions: (1) Was the cabin available for rent all of May-December, and were any VRBO guests
relatives or friends who paid less than market rate? (2) On the deck weekend in October, did Kevin work on the
cabin substantially full time both days? (3) Was the roof a full replacement (tear-off) or a patch? (4) The
organizer's 2024 column shows a duplex loss but nothing for 'suspended losses' - that is fine, we have it from
last year's return.

-----
From: Samantha O'Brien
Date: Tue, 10 Mar 2026 21:15:06 -0500
Subject: RE: O'Brien 2025 - cabin and duplex questions

1) yes available May-Dec, all VRBO guests were strangers at the normal rate. 2) yes Kevin and Connor worked 8-5 both
days on the deck stairs, didn't do anything else. 3) Full tear off, the old roof was original from the 90s.
Also Emma's books were $640 from the campus store, receipt attached. Thanks!
""")
statement(C.pbc_file("19_Lancaster_County_2025_Reassessment_Notice.pdf", "County notice (informational)", "2026-02-24"),
    "Lancaster County Assessment Office - 2025 Assessment Notice (informational)", [
        {"table": [["Parcel", "Address", "Assessed value 2025"], ["390-11752-0-0000", ADDR[0], 311400.00]], "left_align_cols": [0, 1]},
        {"para": "This notice is not a tax bill."}])

# ================================================================== RETURN
w2_facts = [{"who": "T", "box1": w2_k["1"], "box2": w2_k["2"], "box3": w2_k["3"], "box4": w2_k["4"], "box5": w2_k["5"], "box6": w2_k["6"]},
            {"who": "S", "box1": w2_s["1"], "box2": w2_s["2"], "box3": w2_s["3"], "box4": w2_s["4"], "box5": w2_s["5"], "box6": w2_s["6"]}]
PA_WH = w2_k["state"][0]["tax"] + w2_s["state"][0]["tax"]
EIT_WH = w2_k["local"][0]["tax"] + w2_s["local"][0]["tax"]
itemized = {"state_income_tax": PA_WH + EIT_WH, "real_estate_tax": HOME_RE + PERS_TAX,
            "mortgage_interest_1098": HOME_INT + PERS_INT, "charity_cash": CHARITY}
facts = {
    "status": "MFJ", "taxpayer": {"age65": False}, "spouse": {"age65": False},
    "dependents": [{"name": "Emma O'Brien (18, full-time student)", "odc": True}, {"name": "Connor O'Brien", "ctc": True}],
    "w2": w2_facts,
    "interest": [{"payer": "Fulton Bank", "amount": INT_FULTON}],
    "sch1": {"sch_e": 0},
    "education": [{"name": "Emma O'Brien", "type": "AOTC", "qualified_expenses": QEE}],
}
R_cmp = Return1040(dict(facts, itemized=itemized)).compute()
ITEMIZED = R_cmp.values["itemized_total_computed"]
assert R_cmp.values["deduction_type"] == "Standard"
# the trap: rental 1098 + escrow taxes put on Schedule A (and removed from Sch E)
R_trap = Return1040(dict(facts, itemized=dict(itemized, mortgage_interest_1098=itemized["mortgage_interest_1098"] + DUP_1098_INT,
                                              real_estate_tax=itemized["real_estate_tax"] + DUP_RE_TAX))).compute()
ITEMIZED_TRAP = R_trap.values["itemized_total_computed"]
R = Return1040(facts).compute()
v = R.values
R.notes.append(f"Itemized deductions ${ITEMIZED:,} < standard ${v['12e']:,} - standard used.")
MAGI_8582 = v["11"]
ALLOW = max(0, 25000 - max(0, MAGI_8582 - 100000) * .5)
assert ALLOW == 0
SUSP_TOTAL = r(PY_SUSPENDED - DUP_NET)

# ---------------- PA-40
PA_COMP = w2_k["state"][0]["wages"] + w2_s["state"][0]["wages"]
PA_TI = r(PA_COMP) + r(INT_FULTON)
PA_TAX = r(PA_TI * .0307)
PA_WH_R = r(PA_WH)
PA_BAL = PA_TAX - PA_WH_R
PA_RENTS = DUP_NET + (r(CAB_GROSS) - tier1 - oper_total - CAB_DEP_RENTAL)   # PA: assume no sec. 280A limit (loss class anyway)
state = [{"title": "Pennsylvania PA-40 (2025) - full-year residents (joint)",
          "lines": [("1a", "Gross compensation (W-2 box 16 - includes 401(k)/403(b) elective deferrals, taxable for PA)", r(PA_COMP)),
                    ("1b", "Unreimbursed employee business expenses", 0), ("1c", "Net compensation", r(PA_COMP)),
                    ("2", "Interest income", r(INT_FULTON)), ("3", "Dividend and capital gains distributions", 0),
                    ("6", f"Net income (loss) from rents - Schedule E: duplex {DUP_NET:,}; cabin (PA - no sec. 280A limit assumed) "
                          f"{r(CAB_GROSS) - tier1 - oper_total - CAB_DEP_RENTAL:,} = LOSS {PA_RENTS:,} (not netted against other classes)", "(LOSS)"),
                    ("9", "Total PA taxable income (positive classes only)", PA_TI), ("12", "PA tax liability (3.07%)", PA_TAX),
                    ("13", "Total PA tax withheld (W-2 box 17)", PA_WH_R), ("18", "Tax forgiveness (Schedule SP) - not eligible (income too high)", 0),
                    ("28", "Tax due", max(0, PA_BAL)), ("29", "Overpayment", max(0, -PA_BAL))],
          "note": "PA does not apply the federal passive-loss rules or carry rental losses forward; a loss in the rents class simply "
                  "cannot offset compensation. PA depreciation = federal here (no bonus). Local: Manheim Township EIT withheld "
                  f"({fmt(r(EIT_WH))} total, W-2 box 19); the annual local EIT final return is filed separately with LCTCB (no balance expected)."}]

# ---------------- attachments
sch_e_a = [["Schedule E Part I - Property A: " + DUPLEX + " (2-unit residential, type 2)", "Amount"],
           ["Fair rental days 365 / personal use days 0 / QJV no", ""],
           ["3 Rents received (unit A 16,200; unit B 12,950 - vacant Mar-Apr, advertised; late fees 75)", r(DUP_RENTS)]] + \
          [[k, r(a)] for k, a in DUP_EXP.items()] + \
          [["20 Total expenses", DUP_TOTAL_EXP], ["21 Income (loss)", DUP_NET],
           ["22 Deductible rental real estate loss after limitation (Form 8582)", 0]]
sch_e_b = [["Schedule E Part I - Property B: " + CABIN + " (vacation/short-term, type 1) - sec. 280A(c)(5) limited", "Amount"],
           [f"Fair rental days {RENT_DAYS} / personal use days {PERS_DAYS} (family 18 + brother's free stay 3; deck-repair weekend "
            "10/11-10/12 excluded - substantially full-time repair work)", ""],
           ["3 Rents received (VRBO gross - 1099-K)", r(CAB_GROSS)],
           [f"Rental share of expenses = {RENT_DAYS}/{USE_DAYS} = {FRAC:.4%} (IRS method: total rental days / total days used)", ""],
           ["12 Mortgage interest - rental portion (8,300 x 62/83)", w_int], ["16 Taxes - rental portion (3,320 x 62/83)", w_tax],
           ["19 Other - VRBO host & processing fees (direct, 100%)", r(CAB_FEES)], ["7 Cleaning - guest turnovers (direct, 100%)", r(CAB_CLEAN)]] + \
          [[f"{k} - rental portion {r(CAB_OPER[k]):,} x 62/83 = {a:,}; allowed (limited)", ""] for k, a in oper_rental.items()] + \
          [["Operating expenses allowed (limited to remaining income)", oper_allowed],
           ["18 Depreciation allowed (limited)", dep_allowed], ["21 Net income", CAB_NET]]
ws51 = [["Pub. 527 Worksheet 5-1 - dwelling unit used as a home (IRS method)", "Amount"],
        ["1 Rental income", r(CAB_GROSS)],
        ["2a Rental portion of mortgage interest", w_int], ["2b Rental portion of real estate taxes", w_tax],
        ["2d Direct rental expenses (VRBO fees + guest cleaning)", w_direct], ["2e Fully deductible rental expenses", tier1],
        ["3 Remaining rental income (1 - 2e)", room1],
        ["4 Rental portion of operating expenses (utilities, insurance, repairs, supplies)", oper_total],
        ["5 Operating expenses allowed", oper_allowed], ["Carryover of operating expenses to 2026", oper_co],
        [f"6 Rental portion of depreciation ({cab_dep_full:,} MACRS 27.5-yr, placed in service 05/2025, x 62/83)", CAB_DEP_RENTAL],
        ["Depreciation allowed", dep_allowed], ["Carryover of depreciation to 2026 (sec. 280A(c)(5))", dep_co],
        [f"Personal portion to Schedule A worksheet: interest {PERS_INT:,}; taxes {PERS_TAX:,} (cabin is a qualified second home)", ""],
        ["Not a passive activity (sec. 469(j)(10)) - no Form 8582 for the cabin", ""]]
f8582 = [["Form 8582 - passive activity loss limitation", "Amount"],
         ["1a Activities with active participation - current year net loss (duplex)", DUP_NET],
         ["1c Prior-year unallowed losses (PY Form 8582 - organizer did not list it)", -r(PY_SUSPENDED)],
         ["1d Combined", DUP_NET - r(PY_SUSPENDED)],
         [f"Special allowance: 25,000 - 50% x (MAGI {MAGI_8582:,} - 100,000) -> fully phased out at MAGI >= 150,000", 0],
         ["Total losses allowed 2025", 0],
         ["Unallowed loss carried to 2026 (duplex)", -SUSP_TOTAL]]
f4562 = [["Form 4562 / depreciation", "Placed in service", "Basis", "Method", "2025"],
         ["Duplex building (PERM)", "04/2018", r(BLDG_BASIS), "27.5 SL MM", DEP_BLDG],
         ["Unit A kitchen remodel (PERM)", "09/2021", r(KITCHEN), "27.5 SL MM", DEP_KITCHEN],
         ["NEW - duplex roof replacement (Keystone Roofing) - improvement (restoration of the roof system), capitalized", "06/2025",
          r(ROOF), "27.5 SL MM (Part III line 19h)", DEP_ROOF],
         ["Cabin building - rental use (62/83) - converted to rental use 05/2025", "05/2025", r(CAB_BLDG), "27.5 SL MM x 62/83",
          CAB_DEP_RENTAL],
         ["Cabin depreciation allowed after sec. 280A limitation (carryover 4,244)", "", "", "", dep_allowed]]
dem = ("<b>Section 1.263(a)-1(f) de minimis safe harbor election.</b> Kevin M. and Samantha J. O'Brien, SSN XXX-XX-2841, " +
       ADDR[0] + ", " + ADDR[1] + ". The taxpayers are making the de minimis safe harbor election under Treas. Reg. sec. 1.263(a)-1(f) "
       "for the taxable year ending 12/31/2025 (applies to the rental activities; no applicable financial statement; items of $2,500 "
       "or less per invoice/item expensed). Roof replacement ($14,000) is capitalized; small-taxpayer safe harbor (Reg. 1.263(a)-3(h)) "
       f"not available because 2025 repairs + improvements on the duplex exceed 2% of its unadjusted basis ($265,000 x 2% = $5,300).")
edu = [["Form 8863 - American opportunity credit - Emma O'Brien (1st year, full-time, Penn State; no felony drug conviction)", "Amount"],
       ["1098-T box 1 tuition & required fees paid 2025 (incl. spring 2026 term billed & paid Dec 2025 - box 7)", r(TUITION_BOX1)],
       ["Less tax-free scholarship (box 5) - restricted to tuition", -r(SCHOLARSHIP)],
       ["Adjusted qualified expenses (room & board excluded; $640 books also qualify but not needed)", r(QEE)],
       ["Tentative AOTC: 100% x 2,000 + 25% x 2,000 (expenses capped at 4,000)", 2500],
       [f"MAGI {v['11']:,}: phase-out (180,000 - MAGI) / 20,000 = {R.forms_value('Form 8863', 'phase')}", ""],
       ["AOTC allowed", r(v.get('aotc_refundable', 0) / .40) if v.get('aotc_refundable') else 0],
       ["40% refundable (Form 1040 line 29)", v.get("aotc_refundable", 0)],
       ["Nonrefundable (Schedule 3 line 3)", R.forms_value("Form 8863", "19")]]
cmp_tbl = [["Standard vs itemized", "Correct", "If rental 1098 left on Sch A (trap)"],
           ["Taxes: PA + local EIT withheld, home RE, cabin RE personal portion (+ duplex escrow taxes in trap)", r(itemized['state_income_tax'] + itemized['real_estate_tax']), r(itemized['state_income_tax'] + itemized['real_estate_tax'] + DUP_RE_TAX)],
           ["Mortgage interest: home + cabin personal portion (+ duplex 1098 in trap)", r(itemized['mortgage_interest_1098']), r(itemized['mortgage_interest_1098'] + DUP_1098_INT)],
           ["Charity", r(CHARITY), r(CHARITY)],
           ["Total itemized", ITEMIZED, ITEMIZED_TRAP], ["Standard deduction", v["12e"], v["12e"]],
           ["Deduction used", "Standard", "Itemized (wrong) - and the duplex would show a $" + f"{DUP_NET + r(DUP_1098_INT + DUP_RE_TAX):,}" + " profit"]]
C.write_return(R, [
    ("Taxpayer / Spouse", "Kevin M. O'Brien (XXX-XX-2841) / Samantha J. O'Brien (XXX-XX-7719)"), ("Address", ", ".join(ADDR)),
    ("Filing status", "Married filing jointly"),
    ("Dependents", "Emma (daughter, 2007, full-time student) - ODC + AOTC; Connor (son, 2011) - CTC"),
    ("Forms included", "1040, Sch 1, Sch 3, Sch 8812, Sch E, Form 4562, Form 8582, Form 8863, de minimis election; PA-40 (Sch E, W-2S)"),
    ("Digital assets question", "No"),
    ("State / local", "PA-40 resident (e-file); Manheim Twp local EIT final return filed separately with LCTCB"),
    ("Filing method", "E-file 04/08/2026 (Form 8879 signed 04/06/2026); federal refund direct deposit Fulton ****3318; PA balance due paid via ACH"),
], state_summary=state, attachments=[("Schedule E - Property A (duplex)", sch_e_a), ("Schedule E - Property B (cabin)", sch_e_b),
                                     ("Vacation home limitation worksheet", ws51), ("Form 8582 summary", f8582),
                                     ("Depreciation detail (Form 4562)", f4562), ("Election statement", dem),
                                     ("Form 8863 detail", edu), ("Standard vs itemized comparison", cmp_tbl)])

# ---------------- answer key
aotc_total = r(v.get("aotc_refundable", 0)) + R.forms_value("Form 8863", "19")
gotchas = [
    gotcha("EVG1008-G1", "Schedule E - Rental Properties (Form 1098 treated as personal)", "1098 for the duplex address autoflows to Schedule A",
           f"Put the {fmt(DUP_1098_INT)} rental mortgage interest (and {fmt(DUP_RE_TAX)} escrow taxes) on Schedule A -> itemize "
           f"({fmt(ITEMIZED_TRAP)}) and show a duplex profit.",
           "1098 box 8 = rental address (box 7 'No'): interest and escrowed taxes are Schedule E expenses of the duplex. Correct "
           f"itemized total {fmt(ITEMIZED)} < standard {fmt(v['12e'])} -> standard deduction; duplex shows a {fmt(DUP_NET)} loss (suspended).",
           "Deduction type flips; passive income/loss misstated", ["12e", "Sch E 12", "Sch E 16"], "medium"),
    gotcha("EVG1008-G2", "Schedule E - capitalization of repairs vs improvements; de minimis election", "Roof, water heater, window",
           f"Expense the {fmt(ROOF)} roof as a repair (ledger coded it 'Repairs'), or capitalize everything.",
           f"Roof: full tear-off replacement = restoration of a building system -> capitalize, 27.5-yr SL mid-month from 06/2025 ({fmt(DEP_ROOF)} "
           "for 2025); small-taxpayer safe harbor fails (> 2% of UBB). Water heater $1,900: de minimis safe harbor (<= $2,500 per invoice) "
           "with the election statement attached. Window $450: repair.", "Sch E line 14 overstated $14,000 (loss suspended anyway, but basis/carryforward wrong)",
           ["Sch E 14", "Sch E 18", "Form 4562"], "medium"),
    gotcha("EVG1008-G3", "Schedule E - personal use days (sec. 280A)", "Cabin rented 62 days, used personally 21 days",
           "Report the cabin as a regular rental with a full-year loss (or count only 18 personal days, excluding the brother's free stay).",
           f"Use by a family member (brother) is personal use even if he paid nothing; the deck-repair weekend is not personal use. 21 personal days "
           f"> 14 and > 10% of 62 -> the cabin is a residence: expenses allocated {RENT_DAYS}/{USE_DAYS} and limited to rental income "
           f"(Worksheet 5-1). Net $0; carry forward operating {fmt(oper_co)} + depreciation {fmt(dep_co)}; personal share of interest/taxes to "
           "Sch A worksheet.", "Avoids an improper ~$7,000 loss", ["Sch E line 2", "Sch E 21"], "hard"),
    gotcha("EVG1008-G4", "General Return Prep Notes - blank organizer line with PY amount (suspended passive loss)", "PY suspended loss not on the organizer",
           "Start Form 8582 at zero - the $6,200 carryforward is lost.",
           f"Pull the {fmt(PY_SUSPENDED)} unallowed loss from the PY return/PERM. MAGI {fmt(MAGI_8582)} > $150k -> $25k special allowance fully "
           f"phased out; 2025 loss {fmt(DUP_NET)} also suspended -> carry {fmt(SUSP_TOTAL)} to 2026.", "Carryforward understated $6,200",
           ["Form 8582", "Sch E 22"], "medium"),
    gotcha("EVG1008-G5", "Education credits / dependents", "AOTC in the MAGI phase-out; 18-year-old dependent",
           "Claim the full $2,500 AOTC on the $18,400 box 1 (ignoring the scholarship) and a $2,200 CTC for Emma.",
           f"Qualified expenses = 18,400 - 6,000 scholarship = {fmt(QEE)} (>= $4,000 -> $2,500 tentative). MAGI {fmt(v['11'])} is in the "
           f"$160k-$180k range -> allowed {fmt(aotc_total)} ({fmt(v.get('aotc_refundable', 0))} refundable on line 29). Emma is 18 -> $500 ODC, "
           "Connor $2,200 CTC.", "Credits overstated ~$3,100 if wrong", ["19", "29", "Sch 3 3"], "medium"),
    gotcha("EVG1008-G6", "Scan - duplicate documents", "Lender escrow statement repeats the 1098 interest and taxes",
           "Autoflow the escrow year-end summary as a second 1098 -> duplex interest/taxes doubled.",
           "Escrow statement is support only; use Form 1098 once (Sch E line 12 9,860; line 16 5,420).", "Sch E expenses doubled",
           ["Sch E 12", "Sch E 16"], "easy"),
    gotcha("EVG1008-G7", "SALT Implications - PA class rules", "PA-40 prepared from federal numbers",
           "Use federal wages (box 1) and net the rental loss against compensation.",
           f"PA compensation = W-2 box 16 {fmt(r(PA_COMP))} (401(k)/403(b) deferrals are PA-taxable). The rents class is a loss and cannot "
           f"offset other classes (no carryforward). PA tax 3.07% x {fmt(PA_TI)} = {fmt(PA_TAX)}; local EIT final return filed separately.",
           f"PA tax {fmt(PA_TAX)}", ["PA-40 1a", "PA-40 6", "PA-40 12"], "medium"),
]
C.write_answer_key(R, {"residence": "PA (Lancaster - Manheim Twp)", "complexity": "Rental tier - 2 rentals incl. vacation home, college student"},
    gotchas, state=[{"return": "PA-40", "compensation": r(PA_COMP), "interest": r(INT_FULTON), "rents_class": PA_RENTS,
                     "taxable_income": PA_TI, "tax": PA_TAX, "withheld": PA_WH_R, "balance_due": max(0, PA_BAL)},
                    {"return": "Manheim Twp EIT (LCTCB)", "withheld": r(EIT_WH), "note": "filed separately"}],
    filings=[{"form": "Form 1040", "method": "e-file", "due": "2026-04-15", "filed": "2026-04-08"},
             {"form": "PA-40", "method": "e-file", "due": "2026-04-15", "filed": "2026-04-08"}],
    extra={"schedule_e": {"duplex": {"rents": r(DUP_RENTS), "expenses": DUP_TOTAL_EXP, "net": DUP_NET, "allowed": 0},
                          "cabin": {"rents": r(CAB_GROSS), "rental_days": RENT_DAYS, "personal_days": PERS_DAYS, "net": CAB_NET,
                                    "sec280A_carryover_operating": oper_co, "sec280A_carryover_depreciation": dep_co}},
           "passive_loss_carryforward_to_2026": SUSP_TOTAL, "itemized_not_used": ITEMIZED})
C.write_receipt_log("EVG1008-1040-2025", "A. Brennan (staff)", "L. Chen (senior)", "S. Kennedy, CPA", "2026-02-24")

C.write_notes(f"""
# EVG1008 - O'Brien, Kevin & Samantha - 2025 Form 1040 / PA-40 - Preparer Notes

*Synthetic client - Project Evergreen. Return status: **signed off, e-filed 04/08/2026 (federal + PA), accepted.***

## Return summary
| | |
|---|---|
| Filing status | Married filing jointly |
| AGI (line 11) | {fmt(v['11'])} |
| Deduction | Standard {fmt(v['12e'])} (itemized would be {fmt(ITEMIZED)}) |
| Taxable income | {fmt(v['15'])} |
| Tax / credits | {fmt(v['16'])} less CTC+ODC {fmt(v['19'])} and AOTC {fmt(v['20'])} (nonrefundable) |
| Total tax | {fmt(v['24'])} |
| Payments | withholding {fmt(v['25d'])} + refundable AOTC {fmt(v['29'])} |
| **Federal refund** | **{fmt(v['refund'])}** |
| PA-40 | tax {fmt(PA_TAX)}, withheld {fmt(PA_WH_R)} -> {'balance due ' + fmt(PA_BAL) if PA_BAL > 0 else 'refund ' + fmt(-PA_BAL)} |
| Passive loss carried to 2026 | {fmt(SUSP_TOTAL)} (duplex) |
| Sec. 280A carryover to 2026 (cabin) | operating {fmt(oper_co)} + depreciation {fmt(dep_co)} |

## What I did and why (plain English)
1. **Duplex 1098.** The Susquehanna Valley 1098 is in both names, but box 8 is the Chestnut Row duplex address and box 7 says "No"
   (not their home). Autoflow dropped it on Schedule A. Moved the interest ({fmt(DUP_1098_INT)}) and the escrowed property taxes
   ({fmt(DUP_RE_TAX)}) to Schedule E. The lender's escrow year-end summary repeats the same numbers - support only, not a second 1098.
2. **Roof vs repairs.** The ledger coded the $14,000 roof as "repairs". A full tear-off/replacement of the roof is a restoration of a
   building system, so it is capitalized: 27.5-year straight line, mid-month, placed in service 06/2025 -> {fmt(DEP_ROOF)} this year.
   (The small-taxpayer safe harbor doesn't work: repairs + improvements on the duplex are over 2% of its $265,000 unadjusted basis.)
   The $1,900 water heater (one invoice, under $2,500) is expensed under the **de minimis safe harbor** - election statement attached
   (it has to be attached each year). If the water heater were instead treated as a plumbing-system restoration the difference would be
   ~$1,840 of 2025 deduction - immaterial here because the whole duplex loss is suspended. The $450 window is an ordinary repair.
3. **Duplex result and passive loss.** Rents {fmt(r(DUP_RENTS))} (unit B vacant March-April while advertised - still "fair rental"
   all 365 days) less expenses {fmt(DUP_TOTAL_EXP)} (incl. depreciation {fmt(DUP_DEP)} from the PERM schedule) = **{fmt(DUP_NET)} loss**.
   They actively participate, but MAGI {fmt(MAGI_8582)} is over $150,000 so the $25,000 allowance is completely phased out. The organizer
   didn't list last year's **suspended loss of {fmt(PY_SUSPENDED)}** - I took it from the PY return (PERM). Total suspended to 2026 =
   **{fmt(SUSP_TOTAL)}**; it will be released when income allows or when they sell the duplex.
4. **Cabin = vacation home (sec. 280A).** VRBO guests 62 nights at market rates. Personal use 21 days: the family's 18 days plus Kevin's
   brother Pat's 3 free nights - *any* use by a family member counts as personal use even if they "don't count" in Sam's mind. The
   October deck weekend was substantially full-time repair work (Sam's email) so those 2 days are **not** personal. 21 days is more than
   both 14 days and 10% of 62, so the cabin is treated as a residence: expenses are split {RENT_DAYS}/{USE_DAYS} = {FRAC:.2%} (IRS method)
   and rental deductions can't exceed rental income. Order: rental share of interest {fmt(w_int)} and taxes {fmt(w_tax)} plus 100% of the
   VRBO fees and guest cleaning ({fmt(w_direct)}) -> operating costs {fmt(oper_allowed)} of {fmt(oper_total)} -> depreciation $0 of
   {fmt(CAB_DEP_RENTAL)}. Net **$0**. Carry forward {fmt(oper_co)} operating + {fmt(dep_co)} depreciation. (Courts also allow the "Bolton"
   method - interest/taxes x 62/365 - which would free up more operating expenses; I used the IRS method as our procedure/brief requires,
   no 2025 tax difference because standard deduction applies.) The personal share of cabin interest ({fmt(PERS_INT)}) and taxes
   ({fmt(PERS_TAX)}) would go on Schedule A as second-home interest - but they don't itemize.
   Depreciation basis: cabin cost $310,000 less land $60,000 = $250,000 (lower than FMV at conversion), placed in service 05/2025.
5. **Standard vs itemized.** Correctly: PA + local tax withheld + home and cabin-personal property tax + home and cabin-personal mortgage
   interest + charity = {fmt(ITEMIZED)} < {fmt(v['12e'])}. (With the duplex 1098 wrongly on Sch A it would have been {fmt(ITEMIZED_TRAP)}.)
6. **Emma - AOTC.** First year at Penn State, full-time. 1098-T box 1 $18,400 (fall 2025 + spring 2026 billed and paid in 2025 - box 7
   checked, allowed in 2025) less $6,000 tax-free scholarship = {fmt(QEE)} -> the $4,000 maximum counts -> $2,500 tentative. MAGI
   {fmt(v['11'])} is inside the $160k-$180k joint phase-out -> **{fmt(aotc_total)}** allowed ({fmt(v['29'])} refundable, {fmt(v['20'])}
   nonrefundable). Emma is 18 so she gets the $500 other-dependent credit, not the CTC; Connor (14) gets $2,200.
7. **Pennsylvania.** PA taxes 401(k) and 403(b) deferrals, so PA compensation is W-2 box 16 ({fmt(r(PA_COMP))}), not box 1. The rents
   class is a loss (duplex {fmt(DUP_NET)}; for PA I assumed the cabin is not limited by sec. 280A - either way the class is a loss) and PA
   does not let a loss in one class offset another, so PA taxable income = compensation + interest = {fmt(PA_TI)} x 3.07% = {fmt(PA_TAX)}.
   Local Manheim Township EIT was withheld by both employers - the annual local return is filed separately with LCTCB.

## Open items / advice
- Keep the cabin calendar every year - if personal use is kept to 14 days or less (or 10% of rental days), the cabin becomes a regular
  rental (then passive, and with ~4-night average stays probably not a "rental activity" at all - revisit).
- Next year: sec. 280A carryovers ({fmt(oper_co)} / {fmt(dep_co)}) and passive carryforward ({fmt(SUSP_TOTAL)}) are in the Answer Key and PERM.

## Hand-off to signer / routing
- [x] Return locked; Accountant's copy saved as *reviewed*
- [x] Federal 1040 - e-file; PA-40 - e-file; local EIT final return - admin (LCTCB); no FBAR
- [x] Due 04/15/2026; filed 04/08/2026
- [x] eSign (8879 / PA-8879) - Samantha by email
- Billing: rental tier $1,450 + $250 second rental + 0.75 hr vacation-home allocation; nothing to W/O.
""")
C.write_review_points(f"""
# Review Points - EVG1008 - 2025 - Form 1040

*Reviewer: L. Chen (blue). Preparer responses in red. Synthetic.*

1. **Sch A / WP 5** - Autoflow put the Susquehanna Valley 1098 on Sch A (return showed itemized {fmt(ITEMIZED_TRAP)}). Box 8 is the duplex.
   - Move interest and escrow taxes to Sch E Property A. Re-run standard vs itemized.
   - *Preparer: Done - standard deduction now wins ({fmt(ITEMIZED)} itemized).*
2. **WP 8** - Escrow year-end summary was also imported as a 1098. Duplicate.
   - *Preparer: Removed, bookmarked as support.*
3. **Sch E Property A** - $14,000 roof expensed as a repair.
   - Full replacement - capitalize 27.5 yrs (mid-month 06/2025). Water heater: de minimis + attach election. Window OK as repair.
   - *Preparer: Done; election statement added; depreciation {fmt(DEP_ROOF)}.*
4. **Form 8582** - Prior-year unallowed loss missing (organizer silent). PY return shows {fmt(PY_SUSPENDED)}.
   - *Preparer: Added; carryforward {fmt(SUSP_TOTAL)}.*
5. **Sch E Property B** - Cabin entered as a regular rental with 18 personal days and a $7k loss. Pat's stay is personal use (family member).
   - 21 days -> sec. 280A residence; use the vacation-home worksheet; confirm the deck weekend with the client.
   - *Preparer: Sam confirmed full-time repair work; 21 personal days; worksheet attached; net $0 with carryovers.*
6. **Form 8863** - Draft used $18,400 without the scholarship and ignored the MAGI phase-out.
   - *Preparer: Qualified expenses {fmt(QEE)}; AOTC {fmt(aotc_total)} after phase-out.*
7. **Sch 8812** - Emma is 18 at year end -> ODC, not CTC.
   - *Preparer: Corrected.*
8. **PA-40** - Compensation entered from box 1; rental loss netted against wages.
   - PA box 16 includes 401(k)/403(b). Rents loss stays in its class.
   - *Preparer: Fixed; PA tax {fmt(PA_TAX)}.*
""")
print("EVG1008 done", dict(R.summary()), v["refund"], "PA", PA_TAX, PA_BAL, "dup", DUP_NET, "cab", oper_co, dep_co, "itm", ITEMIZED, ITEMIZED_TRAP)
