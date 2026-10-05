"""EVG1020 - Ashley Turner (Single, Tennessee - Knoxville). ICU nurse W-2; Gatlinburg condo rented on Airbnb
(average stay <= 7 days -> not a "rental activity"; material participation -> nonpassive loss); first-year
capitalization/bonus depreciation; Airbnb 1099-K gross vs payouts; W-2G from a North Carolina casino (NC
nonresident return); gambling losses limited to winnings (100% in 2025); non-federally-declared casualty."""
import random
from datetime import date, timedelta

from common import ClientBuild, gotcha, fmt
from docs import statement, scanned_pages, write_text, write_csv, write_xlsx
import forms as F
from tax2025 import Return1040, r

C = ClientBuild("EVG1020", "Turner", "Ashley Turner")
ADDR = ("718 Kenesaw Ave", "Knoxville, TN 37919")
T = {"name": "Ashley N. Turner", "ssn": "XXX-XX-6318", "dob": "1986-05-19"}
REC = [T["name"], *ADDR, f"TIN: {T['ssn']}"]
CONDO = "1210 Ski Mountain Rd, Unit 407 (Laurel Ridge Condominiums), Gatlinburg, TN 37738"

# =================================================================== PERM
C.write_profile(f"""
# EVG1020 - Turner, Ashley  (PERM)

*Synthetic client - Project Evergreen training data.*

| Item | Detail |
|---|---|
| Client ID | EVG1020 |
| Taxpayer | Ashley N. Turner, DOB 05/19/1986, SSN XXX-XX-6318, ICU Registered Nurse (W-2) |
| Filing status history | Single (never married), no dependents |
| Residence | {ADDR[0]}, {ADDR[1]} (Knox County) - owned since 2019. **Tennessee: no individual income tax** |
| Other real estate | NEW 2025: Gatlinburg condo ({CONDO}) - closed 03/31/2025, short-term rental on Airbnb from 04/01/2025 |
| Contact | Email ashley.turner@example.com, cell (865) 555-0192 (texts OK). eSign OK |
| Referral | Co-worker Megan Doyle (EVG1016) |
| Engagement | Client since 2024 (2023 return). 2025 quote raised from $1,200 to $2,400 (new Schedule E short-term rental with depreciation set-up + NC nonresident return) |
| Payment info | Voided check on file (ORNL Federal Credit Union checking ending 5530) |
| Prior CPA | H&R Block (2022 and prior) |

## Notes from 01/20/2026 phone call (S. Kennedy)
- Bought the condo with a 20% down payment; manages it herself on Airbnb (listing, pricing, guest messaging, restocking, check-ins).
  Uses a local cleaner for turnovers. Told her to keep a log of hours - she has one on paper.
- Mentioned "a big slot win at the Cherokee casino" in June and a tree falling on her house in July (insurance claim).
- Asked her to send the Airbnb earnings CSV (not just the 1099-K), the closing statement and all furniture receipts.
""")
F.prior_year_summary(C.perm_file("2024_Form_1040_Return_Summary.pdf", "Prior-year return summary"), "Ashley Turner",
    "EVG1020", "Single", [
        ["1a", "W-2 wages - Tennessee Valley Regional Medical Center", 88410],
        ["2b", "Taxable interest - ORNL Federal Credit Union", 64],
        ["11", "AGI", 88474], ["12", "Standard deduction (itemized $10,380 < standard)", 14600],
        ["15", "Taxable income", 73874], ["24", "Total tax", 11195], ["25a", "Withholding", 11890], ["35a", "Refund", 695]],
    notes="PY WP: W-2 only; Knoxville home mortgage interest $8,145 + property tax $2,135 + sales tax; itemized < standard. "
          "No rental, no Schedule E, no gambling. Client does not make estimates.")

# =================================================================== PBC documents
EMP = {"name": "Tennessee Valley Regional Medical Center", "addr1": "1924 Alcoa Hwy", "addr2": "Knoxville, TN 37920",
       "ein": "00-5518203"}
EE = {"name": T["name"], "addr1": ADDR[0], "addr2": ADDR[1], "ssn": T["ssn"]}
w2b = {"1": 92180.00, "2": 10420.00, "3": 98680.00, "4": 6118.16, "5": 98680.00, "6": 1430.86,
       "12": [("D", 6500.00), ("DD", 8940.00)], "13": ["Retirement plan: X"], "control": "TVR-0418822"}

# ---- Airbnb reservations (deterministic synthetic data) ----------------------------------------------------
rnd = random.Random(2020)
NIGHT_RATE = {4: 185, 5: 195, 6: 225, 7: 240, 8: 215, 9: 205, 10: 255, 11: 210, 12: 245}
CLEAN_FEE, HOST_PCT, TAX_PCT = 125.00, .03, .1275
PERSONAL = (date(2025, 10, 12), 6)          # her own stay 10/12-10/18 (6 nights, no charge)
MAINT_DAYS = [date(2025, 8, 18), date(2025, 8, 19)]   # deep clean / caulking - working days, not personal use
pattern = [2, 4, 3, 2, 5, 3, 4, 2, 3, 3, 6, 2, 3, 4, 2, 3]
nights = [pattern[i % len(pattern)] for i in range(62)]
diff = 192 - sum(nights)
i = 0
while diff != 0:
    j = i % 62
    if diff > 0 and nights[j] < 6:
        nights[j] += 1; diff -= 1
    elif diff < 0 and nights[j] > 2:
        nights[j] -= 1; diff += 1
    i += 1
assert sum(nights) == 192 and max(nights) <= 7
d = date(2025, 4, 3)
res_rows = []
for k, n in enumerate(nights):
    # skip the personal-use week and maintenance days
    while (d < PERSONAL[0] + timedelta(days=PERSONAL[1]) and d + timedelta(days=n) > PERSONAL[0]) or \
            any(d <= m < d + timedelta(days=n) for m in MAINT_DAYS):
        d += timedelta(days=1)
    rate = NIGHT_RATE[d.month] + rnd.choice([-10, 0, 0, 5, 15])
    sub = round(rate * n, 2)
    gross = round(sub + CLEAN_FEE, 2)
    fee = round(gross * HOST_PCT, 2)
    occ = round(gross * TAX_PCT, 2)
    res_rows.append({"conf": f"HM{rnd.randint(10**7, 10**8 - 1)}", "in": d, "out": d + timedelta(days=n), "nights": n,
                     "guest": rnd.choice(["Jordan P.", "Kayla M.", "Brandon W.", "Priya S.", "Luis G.", "Hannah T.",
                                          "Marcus L.", "Emily R.", "Tyler B.", "Grace K.", "Devon H.", "Olivia C."]),
                     "nightly": sub, "clean": CLEAN_FEE, "gross": gross, "fee": fee, "occ": occ,
                     "payout": round(gross - fee, 2)})
    d = d + timedelta(days=n + rnd.choice([0, 0, 1, 1, 2]))
assert res_rows[-1]["out"] <= date(2025, 12, 31), res_rows[-1]["out"]
DAYS_RENTED = sum(x["nights"] for x in res_rows)
GROSS = round(sum(x["gross"] for x in res_rows), 2)
HOST_FEES = round(sum(x["fee"] for x in res_rows), 2)
OCC = round(sum(x["occ"] for x in res_rows), 2)
PAYOUT = round(sum(x["payout"] for x in res_rows), 2)
CLEAN_COLLECTED = round(sum(x["clean"] for x in res_rows), 2)
AVG_STAY = DAYS_RENTED / len(res_rows)
months = [0.0] * 12
for x in res_rows:
    months[x["in"].month - 1] += x["gross"]
months = [round(m, 2) for m in months]
PERSONAL_DAYS = PERSONAL[1]
RATIO = DAYS_RENTED / (DAYS_RENTED + PERSONAL_DAYS)       # IRC 280A(e) allocation

# ---- Condo mortgage (Smoky Mountain FCU) - closed 03/31/2025, first payment 05/01/2025 -------------------------
LOAN, RATE = 308000.00, .06875
mr = RATE / 12
pmt = round(LOAN * mr / (1 - (1 + mr) ** -360), 2)
bal, int_paid = LOAN, round(LOAN * RATE / 365 * 1, 2)     # 1 day per-diem interest paid at closing (03/31)
for _ in range(8):                                          # May-Dec payments
    it = round(bal * mr, 2)
    int_paid += it
    bal = round(bal - (pmt - it), 2)
CONDO_INT = round(int_paid, 2)
# ---- closing statement / basis ----------------------------------------------------------------------------
PRICE = 385000.00
ACQ_COSTS = {"Owner's title insurance": 1650.00, "Recording fee - deed": 210.00, "Survey": 450.00,
             "Settlement / closing fee (attorney)": 1100.00}
LOAN_COSTS = {"Origination fee (1%)": 3080.00, "Appraisal": 650.00, "Lender's title policy": 780.00}
PROP_TAX_BILL = {"Sevier County 2025": 2140.00, "City of Gatlinburg 2025": 720.00}
TAX_BILL = sum(PROP_TAX_BILL.values())
SELLER_CREDIT = round(TAX_BILL * 89 / 365, 2)              # 01/01-03/30 = 89 days (seller's share, IRC 164(d))
TAX_HERS = round(TAX_BILL - SELLER_CREDIT, 2)
BASIS = PRICE + sum(ACQ_COSTS.values())
ASSESSOR_LAND, ASSESSOR_TOTAL = 49500, 330000
LAND = r(BASIS * ASSESSOR_LAND / ASSESSOR_TOTAL)
BLDG = r(BASIS) - LAND
BLDG_DEP = r(BLDG * .01819)                                 # 39-yr SL mid-month, placed in service April (Table A-7a)
FURN = [("Sofa sleeper + sectional (Ashley HomeStore)", "03/22/2025", 3420.00),
        ("King bed, queen bed, bunk bed + mattresses", "03/22/2025", 4860.00),
        ("Dining table + 6 chairs", "03/22/2025", 1480.00),
        ("65in + 2x 43in smart TVs, soundbar", "03/24/2025", 2310.00),
        ("Washer/dryer stack (replaced seller's units)", "03/27/2025", 1890.00),
        ("Hot tub (deck) - portable 6-person", "03/28/2025", 5400.00),
        ("Patio furniture, grill, fire pit", "03/29/2025", 1760.00),
        ("Linens, towels, cookware, small appliances (bulk)", "03/30/2025", 2140.00),
        ("Lamps, rugs, wall decor, blackout curtains", "03/30/2025", 1340.00)]
FURN_TOTAL = round(sum(x[2] for x in FURN), 2)
LOAN_AMORT = round(sum(LOAN_COSTS.values()) / 360 * 9, 2)

# ---- operating expenses ------------------------------------------------------------------------------------
TRIPS, MILES_RT = 24, 82
MILEAGE = round(TRIPS * MILES_RT * .70, 2)
DIRECT = {  # 100% rental (guest-related) - not allocated
    "Airbnb host service fees": HOST_FEES,
    "Turnover cleaning (Mountain Fresh Cleaning - 62 x $95)": 62 * 95.00,
    "Guest supplies / consumables": 1380.00,
    "Auto - rental trips (24 x 82 mi x $0.70)": MILEAGE,
    "Gatlinburg business license + Sevier County STR permit": 150.00,
    "Dynamic pricing software (PriceLabs, 9 mo)": 180.00,
}
SHARED = {  # allocated rental-days / total-days-used per IRC 280A(e)
    "Insurance (STR landlord policy 04/01/25-03/31/26)": 2160.00,
    "Mortgage interest (Form 1098)": CONDO_INT,
    "Repairs (plumber - disposal)": 265.00,
    "Taxes - her share of 2025 property tax": TAX_HERS,
    "Utilities (electric, water, internet/TV)": 3420.00,
    "HOA dues (9 x $385)": 9 * 385.00,
    "Depreciation - condo (39-yr, $%s x 1.819%%)" % f"{BLDG:,}": BLDG_DEP,
    "Depreciation - furniture/appliances (5-yr, 100% bonus)": FURN_TOTAL,
    "Amortization - loan costs (360 mo; 9 months)": LOAN_AMORT,
}

# ---- Organizer -----------------------------------------------------------------------------------------------
F.organizer(C.pbc_file("01_2025_Organizer_completed.pdf", "Client organizer", "2026-02-09"), "Ashley Turner", "EVG1020",
    general=[("Did your marital status change during 2025?", "No", ""),
             ("Did you buy, sell or refinance real estate?", "Yes", "Bought condo in Gatlinburg 3/31 - Airbnb"),
             ("Do you have rental property?", "Yes", "Airbnb - I do everything myself except cleaning"),
             ("Any gambling winnings?", "Yes", "Won 12k on slots but lost more than that overall so net loss"),
             ("Did you have a casualty or theft loss?", "Yes", "Tree fell on my house in July - see insurance letter"),
             ("Did you pay any individual $600+ for services (1099 required)?", "Yes", "Cleaner - did 1099 on Track1099"),
             ("Did you receive, sell, exchange digital assets?", "No", ""),
             ("Did you make estimated tax payments?", "No", "")],
    dependents=[],
    income_rows=[["Wages", "Tennessee Valley Regional Medical Center", 88410, "see W-2"],
                 ["Interest", "ORNL Federal Credit Union", 64, "71"],
                 ["Rental income", "Airbnb - Gatlinburg condo", "", f"{PAYOUT:,.2f} (what I actually got)"],
                 ["Gambling", "Cherokee casino", "", "net loss (-3,400)"]],
    deductions_rows=[["Mortgage interest", "Volunteer State Mortgage (home)", 8145, "see 1098"],
                     ["Mortgage interest", "Smoky Mountain FCU (condo)", "", "see 1098"],
                     ["Real estate tax", "Knox County / City of Knoxville", 2135, "in escrow"],
                     ["Charitable - cash", "Second Presbyterian Church", 300, "350"],
                     ["Casualty loss", "Tree / roof / fence", "", "deductible 1,000 + tree removal 2,400"]],
    signature_date="02/08/2026")

F.w2(C.pbc_file("02_W-2_TN_Valley_Regional_Medical_Center.pdf", "Form W-2", "2026-02-09"), EMP, EE, w2b)
F.f1099_int(C.pbc_file("03_1099-INT_ORNL_FCU.pdf", "Form 1099-INT", "2026-02-09"),
            ["ORNL Federal Credit Union", "PO Box 365", "Oak Ridge, TN 37831", "TIN: 00-0000071"], REC, {"1": 71.14},
            account="****5530")
F.f1099_k(C.pbc_file("04_1099-K_Airbnb_2025.pdf", "Form 1099-K", "2026-02-09"),
          ["Airbnb Payments, Inc.", "888 Brannan St", "San Francisco, CA 94103", "TIN: 00-0000911"], REC,
          {"1a": GROSS, "1b": GROSS, "2": "6513", "3": str(len(res_rows)), "months": months, "filer_type": "PSE"},
          account="Host ID 48817305",
          notes=["Gross amount reported is the total of reservation payments (nightly rates + cleaning fees) before host service "
                 "fees and adjustments. It does not include occupancy taxes collected and remitted by Airbnb.",
                 "Airbnb may issue Form 1099-K even if federal reporting thresholds are not met."])
write_csv(C.pbc_file("05_Airbnb_Transaction_History_2025.csv", "Airbnb earnings export (CSV)", "2026-02-09"),
    ["Confirmation code", "Guest", "Check-in", "Check-out", "Nights", "Accommodation subtotal", "Cleaning fee",
     "Gross earnings", "Host service fee", "Occupancy & sales taxes (collected/remitted by Airbnb)", "Payout"],
    [[x["conf"], x["guest"], x["in"].strftime("%m/%d/%Y"), x["out"].strftime("%m/%d/%Y"), x["nights"], f"{x['nightly']:.2f}",
      f"{x['clean']:.2f}", f"{x['gross']:.2f}", f"-{x['fee']:.2f}", f"{x['occ']:.2f}", f"{x['payout']:.2f}"]
     for x in res_rows] +
    [["TOTAL", "", "", "", DAYS_RENTED, f"{sum(x['nightly'] for x in res_rows):.2f}", f"{CLEAN_COLLECTED:.2f}",
      f"{GROSS:.2f}", f"-{HOST_FEES:.2f}", f"{OCC:.2f}", f"{PAYOUT:.2f}"]])
F.f1098(C.pbc_file("06_1098_Smoky_Mountain_FCU_condo.pdf", "Form 1098", "2026-02-09"),
        ["Smoky Mountain Federal Credit Union", "300 Parkway", "Sevierville, TN 37862", "TIN: 00-0000388"], REC,
        {"1": CONDO_INT, "2": LOAN, "3": "03/31/2025", "7": "No", "8": CONDO, "9": "1", "11": "03/31/2025"},
        account_no="Loan ****7702")
F.f1098(C.pbc_file("07_1098_Volunteer_State_Mortgage_home.pdf", "Form 1098", "2026-02-09"),
        ["Volunteer State Mortgage Co.", "4400 Papermill Dr", "Knoxville, TN 37909", "TIN: 00-0000290"], REC,
        {"1": 7912.44, "2": 214688.10, "3": "06/14/2019", "7": "Yes", "9": "1", "10": "RE tax 2,184.00"},
        account_no="Loan ****1180")
statement(C.pbc_file("08_Closing_Statement_Gatlinburg_Condo_03-31-2025.pdf", "Settlement statement (ALTA)", "2026-02-09"),
    "ALTA Settlement Statement - Buyer - Closing 03/31/2025", [
        {"para": f"Property: {CONDO}. Buyer: Ashley N. Turner. Seller: R&J Mountain Getaways LLC. "
                 "Settlement agent: Great Smokies Title & Escrow, Sevierville TN. File GST-25-0331-07."},
        {"heading": "Buyer charges", "table": [["Item", "Buyer debit", "Buyer credit"],
            ["Contract sales price", PRICE, ""],
            ["Deposit / earnest money", "", 5000.00],
            ["Loan amount - Smoky Mountain FCU", "", LOAN],
            *[[k, v, ""] for k, v in ACQ_COSTS.items()],
            *[[k + " (loan cost)", v, ""] for k, v in LOAN_COSTS.items()],
            ["Prepaid interest 03/31/2025-04/01/2025 (1 day)", round(LOAN * RATE / 365, 2), ""],
            ["County/city 2025 property taxes 01/01-03/30 (seller credit, taxes unpaid)", "", SELLER_CREDIT],
            ["HOA transfer fee", 250.00, ""],
            ["HOA dues April 2025 (prorated)", 385.00, ""]]},
        {"para": "Personal property: seller's furniture was NOT included in the sale (unit sold unfurnished). "
                 "2025 property taxes will be billed to buyer in October 2025 (due 02/28/2026)."}])
statement(C.pbc_file("09_Sevier_County_Gatlinburg_2025_Property_Tax_Receipts.pdf", "Property tax receipts", "2026-02-09"),
    "2025 Property Tax Receipts - Parcel 125K-A-012.07-407", [
        {"table": [["Jurisdiction", "Bill", "Paid", "Date paid"],
                   ["Sevier County Trustee - 2025", PROP_TAX_BILL["Sevier County 2025"], PROP_TAX_BILL["Sevier County 2025"], "12/04/2025"],
                   ["City of Gatlinburg - 2025", PROP_TAX_BILL["City of Gatlinburg 2025"], PROP_TAX_BILL["City of Gatlinburg 2025"], "12/04/2025"]]},
        {"heading": "Sevier County Property Assessor - 2025 appraisal",
         "table": [["Component", "Appraised value"], ["Land (share of common elements)", ASSESSOR_LAND],
                   ["Improvements", ASSESSOR_TOTAL - ASSESSOR_LAND], ["Total", ASSESSOR_TOTAL]], "total_row": True}])
write_xlsx(C.pbc_file("10_Condo_Expenses_2025_Ashley.xlsx", "Client expense spreadsheet (XLSX)", "2026-02-09"), {
    "Expenses": [["Date", "Vendor", "Category (Ashley)", "Amount", "Notes"],
                 ["03/31/2025", "Great Smokies Title", "Closing costs", round(sum(ACQ_COSTS.values()) + sum(LOAN_COSTS.values()), 2), "all closing costs"],
                 *[[dt, "various", "Furniture", amt, desc] for desc, dt, amt in FURN],
                 ["monthly", "Sevier Co. Electric / Gatlinburg Utilities / Spectrum", "Utilities", 3420.00, "Apr-Dec"],
                 ["monthly", "Laurel Ridge HOA", "HOA", 3465.00, "9 months"],
                 ["03/28/2025", "Proper Insurance", "Insurance", 2160.00, "12-month policy"],
                 ["various", "Mountain Fresh Cleaning (Rhonda Pierce)", "Cleaning", 5890.00, "62 turnovers x $95 - 1099-NEC filed"],
                 ["various", "Costco / Amazon", "Supplies", 1380.00, "coffee, toiletries, paper goods, batteries"],
                 ["07/09/2025", "Gatlinburg Plumbing", "Repairs", 265.00, "garbage disposal"],
                 ["04/02/2025", "City of Gatlinburg / Sevier Co.", "License", 150.00, "business license + STR permit"],
                 ["monthly", "PriceLabs", "Software", 180.00, ""],
                 ["various", "Gas", "Car", 612.40, "gas for trips to condo"],
                 ["04/15/2025", "Dollywood", "Guest perks?", 189.00, "season pass - I take guests' kids sometimes"],
                 ["various", "Airbnb", "Occupancy taxes", OCC, "from CSV - tax column"],
                 ["12/04/2025", "Sevier County Trustee / City", "Property tax", TAX_BILL, "full bill"]],
    "Trips": [["Date", "Purpose", "Round-trip miles"]] +
             [[(date(2025, 4, 1) + timedelta(days=11 * k)).strftime("%m/%d/%Y"),
               rnd.choice(["restock + inspect", "guest issue - hot tub", "meet plumber", "photos / listing refresh",
                           "deep clean check", "restock", "smoke detector batteries", "key lockbox reset"]), MILES_RT]
              for k in range(TRIPS)] + [["10/12/2025", "Our girls trip (personal - no guests)", MILES_RT]]})
scanned_pages(C.pbc_file("11_STR_hours_log_handwritten.pdf", "Handwritten log (scan)", "2026-02-09"),
    [["Condo hours log 2025  -  Ashley  (Airbnb unit 407)",
      "Mar  - furnish/setup, photos, listing          34 hrs",
      "Apr  - msgs, 2 trips, restock                  17",
      "May  - msgs, pricing, 2 trips                  15",
      "Jun  - msgs, hot tub issue, 3 trips            19",
      "Jul  - msgs, plumber, 2 trips                  16",
      "Aug  - deep clean + caulk (2 days), msgs       22",
      "Sep  - msgs, 2 trips                           13",
      "Oct  - msgs, 2 trips (not our girls trip)      15",
      "Nov  - msgs, restock                           13",
      "Dec  - msgs, xmas decor, 2 trips               16",
      "                                     TOTAL  180 hrs",
      "Rhonda (cleaner) - her invoices = 62 turnovers ~1.5 hr",
      "   + 2 deep cleans  =  about 95 hrs",
      "Handyman (Aug) - 12 hrs.   Nobody else works on it."]], handwritten=True, seed=31)
F.w2g(C.pbc_file("12_W-2G_Harrahs_Cherokee_NC.pdf", "Form W-2G", "2026-02-09"),
      ["Harrah's Cherokee Casino Resort", "777 Casino Dr", "Cherokee, NC 28719", "TIN: 00-0000577"], REC,
      {"1": 12000.00, "2": "06/21/2025", "3": "Slots", "4": 0.00, "5": "Machine 14-2207", "8": "K. Wolfe",
       "9": T["ssn"], "10": "Cage 3", "state": "NC / 12,000.00 / 510.00"})
statement(C.pbc_file("13_Caesars_Rewards_Win-Loss_Statement_2025.pdf", "Casino win/loss statement", "2026-02-09"),
    "Caesars Rewards - 2025 Win/Loss Statement - Harrah's Cherokee Casino Resort", [
        {"para": "Player: Ashley N. Turner, Caesars Rewards #****88413. Statement period 01/01/2025-12/31/2025. "
                 "This statement reflects rated play only and is provided as a courtesy; it is not a substitute for the "
                 "patron's own records."},
        {"table": [["Game type", "Total wins (jackpots, W-2G)", "Total losses", "Net win/(loss)"],
                   ["Slots", 12000.00, 15400.00, -3400.00], ["Table games", 0, 0, 0], ["Total", 12000.00, 15400.00, -3400.00]],
         "total_row": True}])
scanned_pages(C.pbc_file("14_Gambling_session_log_phone_notes.pdf", "Handwritten log (scan)", "2026-02-09"),
    [["casino trips 2025 (Cherokee)",
      "2/15  slots   in 800   out 0          -800",
      "4/12  slots   -1450",
      "6/21  JACKPOT 12,000!! (W-2G, NC took 510)",
      "      then lost back ~5,200 same trip",
      "8/30  slots   -2,900",
      "11/8  slots   -3,050 (bday weekend)",
      "12/27 slots   -2,000",
      "total lost about 15,400 (matches Caesars stmt)"]], handwritten=True, seed=32, skew=-1.1)
statement(C.pbc_file("15_Volunteer_Mutual_Insurance_Claim_Letter.pdf", "Insurance correspondence", "2026-02-09"),
    "Volunteer Mutual Insurance Co. - Claim Settlement Letter", [
        {"para": ["Claim HO-25-118804 | Insured: Ashley N. Turner | Property: 718 Kenesaw Ave, Knoxville TN | "
                  "Date of loss: 07/18/2025 | Cause: windstorm - tree limb/trunk impact to roof and rear fence.",
                  "We have completed our review of your claim. Covered damages were estimated at $14,200.00 (roof decking, "
                  "shingles, gutter, fence panels). Less your wind/hail deductible of $1,000.00, we have issued payment of "
                  "$13,200.00. Debris/tree removal beyond the $500 policy sublimit ($2,400 invoiced) is not covered.",
                  "This loss was caused by a localized severe thunderstorm. No state or federal disaster declaration applies "
                  "to this event for Knox County."]}])
F.f1099_nec(C.pbc_file("16_1099-NEC_issued_to_cleaner_copy.pdf", "Copy of 1099-NEC client issued", "2026-02-09",
                       note="payer copy"),
            [T["name"], *ADDR, f"TIN: {T['ssn']}"],
            ["Rhonda Pierce dba Mountain Fresh Cleaning", "PO Box 1142", "Pigeon Forge, TN 37868", "TIN: XXX-XX-4410"],
            {"1": 5890.00}, copy_label="Copy C - For Payer")
statement(C.pbc_file("17_Fidelity_401k_Year-End_Statement.pdf", "Retirement plan statement", "2026-02-09"),
    "TVRMC 403(b)/401(k) Retirement Savings Plan - Year-End Statement 2025", [
        {"table": [["Item", "Amount"], ["Beginning balance 01/01/2025", 61840.22], ["Your contributions", 6500.00],
                   ["Employer match", 3250.00], ["Investment gain", 7910.44], ["Ending balance 12/31/2025", 79500.66]],
         "left_align_cols": [0]}])
write_text(C.pbc_file("18_Email_Ashley_2026-02-12.txt", "Client correspondence", "2026-02-12", "Email"),
"""From: Ashley Turner <ashley.turner@example.com>
To: preparer@evergreentax.example
Date: Thu, 12 Feb 2026 21:14:52 -0500
Subject: Turner taxes - couple questions

Hi! Everything should be uploaded now. A few questions:

1) For the Airbnb I put what actually hit my bank account ($%s) on the organizer. The 1099-K is higher - which
   one is right??
2) The casino - I won 12k on one machine but lost 15,400 over the year. So I shouldn't owe anything on that right?
   My friend said now you can only deduct 90%% of losses?
3) The tree - insurance covered most of it but I paid the $1,000 deductible and $2,400 for the tree removal company.
   Can I deduct that? There was a lot of damage around Knoxville that night.
4) The Cherokee casino took NC tax out of my jackpot. Do I get that back? I've never lived in NC.

Thanks!! Ashley
""" % f"{PAYOUT:,.2f}")

# =================================================================== RETURN - Schedule E computation
direct_total = round(sum(DIRECT.values()), 2)
shared_alloc = {k: r(v * RATIO) for k, v in SHARED.items()}
shared_personal = {k: r(v) - shared_alloc[k] for k, v in SHARED.items()}
exp_total = r(direct_total) + sum(shared_alloc.values())
SCH_E_NET = r(GROSS) - exp_total
PERS_TAX = shared_personal["Taxes - her share of 2025 property tax"]
PERS_INT = shared_personal["Mortgage interest (Form 1098)"]

SALES_TAX = 1480            # IRS Sales Tax Deduction Calculator (TN 7% + Knox Co 2.25%), no large items - assumption
HOME_RE_TAX = 2184.00
HOME_INT = 7912.44
CHARITY = 350.00
GAMBLING_WIN, GAMBLING_LOSS = 12000.00, 15400.00

facts = {
    "status": "S",
    "taxpayer": {"age65": False},
    "w2": [{"who": "T", "box1": w2b["1"], "box2": w2b["2"], "box3": w2b["3"], "box4": w2b["4"], "box5": w2b["5"],
            "box6": w2b["6"]}],
    "interest": [{"payer": "ORNL Federal Credit Union", "amount": 71.14}],
    "sch1": {"sch_e": SCH_E_NET, "other": [("8b", "Gambling winnings (Form W-2G - Harrah's Cherokee, NC)", GAMBLING_WIN)]},
    "itemized": {"state_income_tax": SALES_TAX, "use_sales_tax": True, "real_estate_tax": HOME_RE_TAX + PERS_TAX,
                 "mortgage_interest_1098": HOME_INT, "charity_cash": CHARITY,
                 "other_itemized": min(GAMBLING_LOSS, GAMBLING_WIN),
                 "other_itemized_desc": "Gambling losses (limited to gambling winnings of $12,000; 100% for 2025)"},
    "qbi": {"businesses": [{"name": "Gatlinburg STR (Sch E) - trade or business", "qbi": SCH_E_NET}]},
}
R = Return1040(facts).compute()
v = R.values
R.values["qbi_loss_carryforward_2026"] = -SCH_E_NET if SCH_E_NET < 0 else 0

# itemized vs standard comparison (for notes/attachments)
item_no_gamble = v["itemized_total_computed"] - r(min(GAMBLING_LOSS, GAMBLING_WIN))

# ---- NC nonresident D-400 / Schedule PN
NC_STD = 12750
nc_agi = v["11"]
nc_ti_full = max(0, nc_agi - NC_STD)
nc_pct = round(GAMBLING_WIN / nc_agi, 4)
nc_ti = r(nc_ti_full * nc_pct)
nc_tax = r(nc_ti * .0425)
NC_WH = 510.00
nc_refund = r(NC_WH) - nc_tax

sch_e_rows = [["Schedule E, Part I - Property A: " + CONDO + " (type 3 - short-term rental)", "Total expense", "Rental portion", "Sch E"],
              ["Line 2: fair rental days / personal use days / QJV", f"{DAYS_RENTED} / {PERSONAL_DAYS} / No", "", ""],
              ["Line 3 Rents received (Form 1099-K gross = CSV gross earnings)", r(GROSS), "100%", r(GROSS)]]
for k, val in DIRECT.items():
    sch_e_rows.append([k + " (direct - 100%)", r(val), "100%", r(val)])
for k, val in SHARED.items():
    sch_e_rows.append([k + f" (x {DAYS_RENTED}/{DAYS_RENTED + PERSONAL_DAYS})", r(val), f"{RATIO:.4%}", shared_alloc[k]])
sch_e_rows += [["Line 20 Total expenses", "", "", exp_total],
               ["Line 21/26 Net income (loss) - NONPASSIVE (not a rental activity; material participation)", "", "", SCH_E_NET]]
recon = [["Airbnb reconciliation (CSV -> 1099-K -> bank)", "Amount"],
         ["Accommodation subtotal (nightly rates)", r(GROSS - CLEAN_COLLECTED)],
         ["Cleaning fees charged to guests", r(CLEAN_COLLECTED)],
         ["Gross earnings = Form 1099-K box 1a (Sch E line 3)", r(GROSS)],
         ["Less host service fees (3%) - deducted as commissions", -r(HOST_FEES)],
         ["Payouts deposited (client's organizer figure)", r(PAYOUT)],
         ["Occupancy & sales taxes collected/remitted by Airbnb - NOT income, NOT deductible", r(OCC)],
         [f"Reservations {len(res_rows)}; nights {DAYS_RENTED}; average stay {AVG_STAY:.2f} nights (<= 7 -> not a rental activity)", ""]]
f4562 = [["Form 4562 (Sch E - Gatlinburg condo)", "Basis", "Method", "2025 deduction (before 280A allocation)"],
         [f"Condo building (price {PRICE:,.0f} + acquisition costs {sum(ACQ_COSTS.values()):,.0f} = {BASIS:,.0f}; land "
          f"{LAND:,} per assessor ratio {ASSESSOR_LAND:,}/{ASSESSOR_TOTAL:,})", BLDG, "39-yr SL MM (transient use), PIS 04/2025", BLDG_DEP],
         ["Furniture, appliances, hot tub, TVs, linens (9 invoices, acquired 03/22-03/30/2025)", r(FURN_TOTAL),
          "5-yr, 100% special depreciation allowance (acquired after 01/19/2025)", r(FURN_TOTAL)],
         ["Loan costs (origination, appraisal, lender title) - amortized over 360 months", r(sum(LOAN_COSTS.values())), "SL 30 yrs", r(LOAN_AMORT)],
         ["Land (not depreciable)", LAND, "-", 0]]
mp = [["Material participation / passive analysis", "Result"],
      ["Average period of customer use (Reg. 1.469-1T(e)(3)(ii)(A))", f"{AVG_STAY:.2f} days <= 7 -> NOT a rental activity"],
      ["Significant/extraordinary personal services?", "No (no meals, daily cleaning, concierge) -> Schedule E, not Schedule C; no SE tax"],
      ["Test 3 - Reg. 1.469-5T(a)(3): > 100 hours and not less than any other individual", "Ashley 180 hrs vs cleaner ~95, handyman 12 -> MET"],
      ["Result", "Material participation -> nonpassive; loss offsets W-2 wages; Form 8582 not used"],
      ["IRC 280A(d) residence test: personal days vs greater of 14 or 10% of rental days",
       f"{PERSONAL_DAYS} vs {max(14, DAYS_RENTED * .1):.1f} -> not a residence; no 280A(c)(5) income limit"],
      ["IRC 280A(e) allocation of shared expenses", f"{DAYS_RENTED}/{DAYS_RENTED + PERSONAL_DAYS} = {RATIO:.4%}; "
       "maintenance days (08/18-08/19) are not personal use"]]
comp = [["Standard vs itemized", "Amount"], ["Standard deduction (single, OBBBA)", v["standard_deduction_available"]],
        ["Itemized WITHOUT gambling losses", item_no_gamble], ["Itemized WITH gambling losses (used)", v["itemized_total_computed"]]]
C.write_return(R, [
    ("Taxpayer", "Ashley N. Turner (XXX-XX-6318), DOB 05/19/1986"),
    ("Address", ", ".join(ADDR)),
    ("Filing status", "Single"),
    ("Digital assets question", "No"),
    ("Forms included", "1040, Schedules 1, A, B, E, Form 4562, Form 8995 (QBI loss carryforward); NC D-400 + Schedule PN (nonresident)"),
    ("State", "Tennessee - no individual income tax. North Carolina nonresident return (NC-source gambling winnings)"),
    ("Filing method", "E-file federal and NC (Form 8879 signed 04/08/2026); direct deposit ORNL FCU ****5530"),
], state_summary=[{
    "title": "North Carolina Form D-400 (nonresident) with Schedule PN - 2025",
    "lines": [("6", "Federal adjusted gross income", nc_agi), ("9-10", "NC additions / deductions", 0),
              ("11", "NC standard deduction (single) - NC itemized limited to mortgage int./property tax/charity/medical; "
                     "gambling losses not allowed by NC", NC_STD),
              ("12b", "Income after deductions", nc_ti_full),
              ("13", f"Taxable percentage (Sch PN: NC-source {GAMBLING_WIN:,.0f} / total {nc_agi:,})", f"{nc_pct:.4f}"),
              ("14", "North Carolina taxable income", nc_ti), ("15", "NC income tax (4.25%)", nc_tax),
              ("20a", "NC tax withheld (Form W-2G)", r(NC_WH)),
              ("28/34", "Refund" if nc_refund >= 0 else "Tax due", abs(nc_refund))],
    "note": "Filing required: nonresident with NC-source income whose total gross income exceeds the NC filing threshold. "
            "Tennessee has no income tax (no credit for tax paid to NC is available anywhere)."}],
    attachments=[("Schedule E - Part I detail (Gatlinburg condo)", sch_e_rows),
                 ("Airbnb 1099-K reconciliation", recon), ("Form 4562 - depreciation and amortization", f4562),
                 ("Passive activity / IRC 280A analysis", mp), ("Deduction comparison", comp)])

gotchas = [
    gotcha("EVG1020-G1", "Schedule E / Rental Properties; Scan - Schedule E records (hours log)",
           "Short-term rental: not a 'rental activity'; material participation",
           "Treat the Airbnb condo as a passive rental: loss suspended on Form 8582 (MAGI < $100k -> maybe $25k allowance) "
           "or move it to Schedule C with SE tax.",
           f"Average stay {AVG_STAY:.2f} nights (<= 7) -> not a rental activity (Reg. 1.469-1T(e)(3)(ii)(A)); no substantial "
           "services -> stays on Schedule E (no SE tax). Handwritten log: 180 hours, more than any other individual (cleaner ~95) "
           f"-> material participation test 3 -> nonpassive. Loss {fmt(SCH_E_NET)} offsets wages; no Form 8582.",
           f"Sch 1 line 5 {fmt(SCH_E_NET)}; tax effect ~22% of the loss", ["Sch 1 line 5", "11"], "hard"),
    gotcha("EVG1020-G2", "Scan - Schedule E/Rental Income records", "Airbnb 1099-K gross vs payouts vs occupancy taxes",
           f"Report the organizer's payout figure {fmt(PAYOUT)} (and still deduct host fees = double deduction), or treat the "
           "occupancy/sales tax column as income and a deduction.",
           f"Rents = 1099-K gross {fmt(GROSS)} (nightly + cleaning fees), host fees {fmt(HOST_FEES)} deducted once; "
           f"occupancy/sales taxes {fmt(OCC)} collected and remitted by Airbnb are neither income nor deductible. Reconciled CSV to 1099-K.",
           "Sch E line 3 / expense lines", ["Sch E line 3", "Sch E line 8"], "medium"),
    gotcha("EVG1020-G3", "Schedule E / Rental Properties - personal use days",
           "Personal-use days: 280A allocation, not the vacation-home limit",
           "Ignore the girls' trip (deduct 100% of all expenses) or treat the condo as a vacation home and limit expenses to income.",
           f"{PERSONAL_DAYS} personal days < greater of 14 / 10% of {DAYS_RENTED} -> not a residence; shared expenses x "
           f"{DAYS_RENTED}/{DAYS_RENTED + PERSONAL_DAYS}. Personal share of property tax ({fmt(PERS_TAX)}) to Sch A; personal "
           f"share of mortgage interest ({fmt(PERS_INT)}) is nondeductible personal interest (condo not a qualified residence). "
           "Maintenance days are not personal days.", "Sch E expenses; Sch A line 5b", ["Sch E", "Sch A 5b"], "medium"),
    gotcha("EVG1020-G4", "Schedule E / Rental Properties - capitalization of repairs; Scan - spreadsheet",
           "Client spreadsheet expenses closing costs, furniture and personal items",
           "Deduct the spreadsheet as-is: closing costs, $24.6k furniture as 'supplies', full property-tax bill, occupancy "
           "taxes, Dollywood pass, gas receipts.",
           f"Capitalize acquisition costs into basis ({fmt(BASIS)}; land {fmt(LAND)} per assessor ratio); building 39-yr MM "
           "(unit used on a transient basis is not a 'dwelling unit' for 27.5-yr); furniture 5-yr with 100% bonus (acquired after "
           f"01/19/2025) on Form 4562; loan costs amortized; property tax limited to her post-closing share {fmt(TAX_HERS)} "
           "(IRC 164(d)); mileage at 70c replaces gas; Dollywood pass is personal.",
           "Sch E lines 16/18/19; Form 4562", ["Sch E", "4562"], "hard"),
    gotcha("EVG1020-G5", "Schedule A - Gambling Winnings/Losses (OBBBA timing)", "Gambling: gross winnings, losses capped, 2025 = 100%",
           "Net the jackpot against losses and report nothing (client's view), or deduct $15,400, or apply the OBBBA 90% limit "
           "(procedure text says 'in effect for 2026').",
           f"Report {fmt(GAMBLING_WIN)} W-2G winnings on Sch 1 line 8b; losses deductible only as an itemized deduction (Sch A line 16) "
           f"limited to winnings = {fmt(GAMBLING_WIN)}. The 90% limit applies to tax years beginning after 12/31/2025 - not 2025. "
           "Procedure wording is imprecise; law followed.", "Sch 1 line 8b; Sch A line 16", ["8", "12e"], "medium"),
    gotcha("EVG1020-G6", "Schedule A - itemize vs standard / sales tax", "Itemizing only works because of the gambling losses",
           "Take the standard deduction (as in 2024) - losing the gambling-loss deduction and taxing $12,000 of winnings in full.",
           f"Itemized {fmt(v['itemized_total_computed'])} (sales tax - TN has no income tax - + real estate tax + home mortgage "
           f"+ charity + gambling) vs standard {fmt(v['standard_deduction_available'])}; without gambling itemized would be "
           f"{fmt(item_no_gamble)}.", "Line 12e", ["12e"], "medium"),
    gotcha("EVG1020-G7", "Schedule A - Disaster Losses (federally declared only)", "Windstorm tree damage is not deductible",
           "Deduct the $1,000 deductible and $2,400 tree removal as a casualty loss.",
           "Personal casualty losses for 2025 are deductible only if attributable to a federally declared disaster (Form 4684); the "
           "07/18/2025 storm had no declaration (insurer letter). Expansion to state-declared disasters starts 2026. $0; no gain "
           "because reimbursement did not exceed basis.", "Sch A line 15 = 0", ["Sch A 15"], "easy"),
    gotcha("EVG1020-G8", "SALT - New State Filing Requirements", "NC nonresident return for NC-casino winnings",
           "No state return because Tennessee has no income tax; the $510 NC withholding is lost (or claimed on the 1040).",
           f"Winnings from a North Carolina casino are NC-source; file D-400 as nonresident with Schedule PN: NC taxable income x "
           f"{nc_pct:.4f} -> tax {fmt(nc_tax)} vs withholding $510 -> refund {fmt(nc_refund)}. NC does not allow gambling losses.",
           "NC D-400", ["NC D-400"], "medium"),
]
C.write_answer_key(R, {"residence": "TN (no state income tax); NC nonresident return", "complexity":
                       "W-2 + short-term rental Schedule E + gambling + NC nonresident"}, gotchas,
                   state=[{"jurisdiction": "NC D-400 (nonresident, Sch PN)", "nc_agi": nc_agi, "nc_std": NC_STD,
                           "taxable_pct": nc_pct, "nc_taxable_income": nc_ti, "tax": nc_tax, "withholding": r(NC_WH),
                           "refund": nc_refund}],
                   filings=[{"form": "Form 1040", "method": "e-file", "due": "2026-04-15", "filed": "2026-04-09"},
                            {"form": "NC D-400 nonresident", "method": "e-file", "due": "2026-04-15", "filed": "2026-04-09"}],
                   extra={"schedule_e": {"rents": r(GROSS), "expenses": exp_total, "net": SCH_E_NET, "fair_rental_days": DAYS_RENTED,
                                         "personal_days": PERSONAL_DAYS, "allocation_ratio": round(RATIO, 6),
                                         "average_stay_nights": round(AVG_STAY, 2), "nonpassive": True},
                          "condo_basis": {"total": r(BASIS), "land": LAND, "building": BLDG,
                                          "building_depr_2025": BLDG_DEP, "furniture_bonus": r(FURN_TOTAL)}})

C.write_receipt_log("EVG1020-1040-2025", "D. Alvarez (staff)", "L. Chen (senior)", "S. Kennedy, CPA", "2026-02-09")
C.write_notes(f"""
# EVG1020 - Turner, Ashley - 2025 Form 1040 - Preparer Notes

*Synthetic client - Project Evergreen. Return status: **signed off; federal and NC e-filed 04/09/2026, both accepted.***

## Return summary
| | |
|---|---|
| Filing status | Single |
| Wages | {fmt(v['1a'])} |
| Schedule E - Gatlinburg short-term rental (nonpassive) | {fmt(SCH_E_NET)} |
| Gambling winnings (Sch 1 line 8b) | {fmt(GAMBLING_WIN)} |
| AGI (line 11) | {fmt(v['11'])} |
| Itemized deductions (Schedule A) | {fmt(v['12e'])} (standard would be {fmt(v['standard_deduction_available'])}) |
| QBI deduction | {fmt(v['13a'])} (STR net loss -> QBI loss carryforward {fmt(-SCH_E_NET)}) |
| Taxable income | {fmt(v['15'])} |
| Total tax | {fmt(v['24'])} |
| Withholding | {fmt(v['25d'])} |
| **Federal refund** | **{fmt(v['refund'])}** |
| NC D-400 (nonresident) | tax {fmt(nc_tax)}, withheld $510 -> **refund {fmt(nc_refund)}** |

## What I did and why (plain English)
1. **W-2.** One W-2 (TVRMC): box 1 {fmt(v['1a'])}; 401(k) code D already excluded. The Fidelity plan statement in the PBC is
   informational only (income inside the plan is not reportable). 1099-INT ORNL FCU $71.
2. **Is the condo a "rental activity"?** The Airbnb CSV shows {len(res_rows)} stays / {DAYS_RENTED} nights = average
   **{AVG_STAY:.2f} nights**. With an average customer stay of 7 days or less, the condo is *not* a rental activity for the
   passive-loss rules (Reg. 1.469-1T(e)(3)(ii)(A)), so the $25,000 rental allowance and the "rentals are per se passive" rule do
   not apply. Ashley provides no substantial services (no meals, no daily housekeeping), so it stays on **Schedule E** (property
   type 3) and is not subject to SE tax.
3. **Material participation.** Her handwritten log shows 180 hours (setup, listing/pricing, guest messaging, 24 trips) vs. the
   cleaner (~95 hours per invoices) and a handyman (12 hours). More than 100 hours and not less than anyone else = test 3 of
   Reg. 1.469-5T(a)(3). Even excluding the 34 March set-up hours (before the unit was available for rent), she has 146 hours -
   still more than 100 and more than anyone else. The loss is **nonpassive** and offsets her wages. Log is contemporaneous-ish (monthly); advised her to keep
   a dated log in 2026 (she is audit-exposed on this position).
4. **Rents.** I used the 1099-K gross ({fmt(GROSS)}) - the nightly rates plus cleaning fees guests paid - not the payouts she wrote
   on the organizer ({fmt(PAYOUT)}). The difference is the 3% host service fee ({fmt(HOST_FEES)}), which is deducted as a commission.
   The occupancy/sales tax column ({fmt(OCC)}) is collected and remitted by Airbnb; it is not her income or expense. The 1099-K
   was issued even though she had fewer than 200 transactions - rental income is reportable either way.
5. **Personal use.** She stayed 10/12-10/18 (6 days, no rent). That is under the greater of 14 days or 10% of rental days, so the
   condo is not treated as a residence (no income limitation). Shared expenses are allocated {DAYS_RENTED}/{DAYS_RENTED + PERSONAL_DAYS}
   = {RATIO:.2%} (IRC 280A(e)); the two August deep-clean/caulking days were working days, not personal days. Guest-only costs
   (host fees, turnover cleaning, supplies, mileage, permit, pricing software) are 100% rental. Personal share of property tax
   ({fmt(PERS_TAX)}) goes to Schedule A; the personal share of mortgage interest ({fmt(PERS_INT)}) is nondeductible because the
   condo is not a qualified residence.
6. **Capitalization and depreciation (Form 4562).** Her spreadsheet expensed closing costs and furniture. Corrected:
   - Basis = price {fmt(PRICE)} + title/recording/survey/settlement {fmt(sum(ACQ_COSTS.values()))} = {fmt(r(BASIS))}; land
     {fmt(LAND)} using the assessor's land/total ratio ({ASSESSOR_LAND:,}/{ASSESSOR_TOTAL:,}); building {fmt(BLDG)}.
   - Building: **39-year** nonresidential (a unit used predominantly on a transient basis is not a "dwelling unit" under
     IRC 168(e)(2)(A)), mid-month, placed in service 04/2025 -> 1.819% = {fmt(BLDG_DEP)}. (27.5 years would be the aggressive
     alternative; flagged for signer - we took the conservative reading.)
   - Furniture/appliances/hot tub/TVs/linens {fmt(r(FURN_TOTAL))}: 5-year property acquired after 01/19/2025 -> 100% special
     depreciation allowance (OBBBA). (De minimis safe harbor would have covered most items too; bonus is simpler and complete.)
   - Loan costs {fmt(r(sum(LOAN_COSTS.values())))} amortized over the 30-year loan: {fmt(r(LOAN_AMORT))} for 9 months.
   - Property tax: the 2025 bills total {fmt(r(TAX_BILL))} but the seller credited her {fmt(r(SELLER_CREDIT))} at closing for
     01/01-03/30 - under IRC 164(d) she deducts only her {fmt(r(TAX_HERS))}.
   - Removed: occupancy taxes, Dollywood season pass (personal), gas receipts (replaced by 24 trips x 82 miles x $0.70 = {fmt(r(MILEAGE))};
     the girls' trip excluded).
   - Result: Schedule E net **{fmt(SCH_E_NET)}**.
7. **1099 question (Sch E line A/B).** She paid the cleaner $5,890 and issued a 1099-NEC (copy in PBC) -> Yes / Yes.
8. **QBI.** Treated the self-managed STR as a section 162 trade or business (regular, continuous involvement). The net loss
   produces no 2025 deduction and a **QBI loss carryforward of {fmt(-SCH_E_NET)}** that will reduce 2026 QBI (Form 8995).
9. **Gambling.** W-2G $12,000 (slots, 06/21/2025) reported gross on Sch 1 line 8b. Losses per the Caesars win/loss statement and her
   session notes = $15,400, deductible only as an itemized deduction and only up to winnings -> $12,000 (Sch A line 16). The new
   OBBBA 90% limitation applies to tax years beginning after 12/31/2025, so 2025 is still 100%. (Our procedure text says to apply
   "the new rules ... in effect for 2026" - for 2025 returns that means *not* applying the 90% cap. Law followed.)
10. **Itemize vs standard.** Itemized {fmt(v['itemized_total_computed'])}: general sales tax ${SALES_TAX:,} (Tennessee has no income
    tax; IRS sales tax calculator, Knox County 9.25% combined rate, no large purchases - *assumption: calculator figure as run at
    prep*) + real estate tax {fmt(HOME_RE_TAX + PERS_TAX)} (home escrow $2,184 + condo personal share) + home mortgage interest
    $7,912 + church $350 + gambling $12,000. Without the gambling losses she would take the {fmt(v['standard_deduction_available'])}
    standard deduction ({fmt(item_no_gamble)} itemized).
11. **Casualty.** The tree/windstorm damage (07/18/2025) was not in a federally declared disaster area (insurer letter says no
    declaration). For 2025 a personal casualty loss is deductible only for federally declared disasters -> $0. No gain either
    (insurance $13,200 < basis in the house). The state-declared expansion begins in 2026.
12. **North Carolina.** The jackpot came from a casino in Cherokee, NC -> NC-source income. As a nonresident whose gross income
    exceeds the NC filing threshold, she must file a **D-400 with Schedule PN**: NC taxable income {fmt(nc_ti_full)} x
    {nc_pct:.4f} = {fmt(nc_ti)} x 4.25% = {fmt(nc_tax)}; withheld $510 -> refund {fmt(nc_refund)}. NC does not allow gambling
    losses as an itemized deduction and NC itemized (mortgage interest + property tax + charity) < NC standard $12,750.
    Tennessee has no income tax, so there is no resident credit to claim.

## Hand-verification
- Tax on {fmt(v['15'])} (single, tax table) = {fmt(v['16'])}; no credits; total tax {fmt(v['24'])}; withholding {fmt(v['25d'])}
  -> refund {fmt(v['refund'])}.
- Sch E: rents {fmt(r(GROSS))} - direct {fmt(r(direct_total))} - allocated shared {fmt(sum(shared_alloc.values()))} = {fmt(SCH_E_NET)}.

## Open items / client communication
- Replied to Ashley's 02/12 email (payout vs 1099-K; gambling; casualty; NC refund). All answered - no open items.
- Advised: keep a dated hours log for 2026; the average-stay test is annual - if average stays creep above 7 days, the condo
  becomes a rental activity and the loss would be passive.
- 2026 planning: gambling losses will be limited to 90% starting 2026 (she would owe tax on 10% of winnings even with equal losses).

## Hand-off to signer / routing
- [x] Return locked; Accountant's Copy saved as *reviewed*
- [x] Federal 1040 - e-file; due 04/15/2026
- [x] NC D-400 nonresident (Schedule PN) - e-file; due 04/15/2026
- [x] No FBAR; no TN return
- [x] eSign (8879 + NC-8879) - email ashley.turner@example.com / text (865) 555-0192
- [x] Refunds by direct deposit (ORNL FCU ****5530)
- Billing: quote $2,400 (Sch E set-up, depreciation, NC nonresident). Actual time over by ~1.5 hrs sorting the expense
  spreadsheet (client records -> external reason, chargeable). Bill $2,400 + 1 hr; 0.5 hr W/O courtesy.
""")
C.write_review_points(f"""
# Review Points - EVG1020 - 2025 - Form 1040

*Reviewer: L. Chen (blue). Preparer responses in red. Synthetic.*

1. **Schedule E / Form 8582** - First draft treated the condo as a passive rental and suspended the loss (MAGI < $100k so the draft
   actually allowed it under the $25k allowance, but for the wrong reason). Average stay is {AVG_STAY:.2f} nights -> not a rental
   activity; the $25k allowance doesn't apply. Document material participation (hours log, cleaner invoices) and remove Form 8582.
   - *Preparer: Done - Test 3 memo added to WP 6 with the log and cleaner's invoice count.*
2. **Schedule E line 3** - Draft used the organizer payout {fmt(PAYOUT)} AND deducted host fees. Use 1099-K gross; tie to CSV.
   - *Preparer: Corrected to {fmt(r(GROSS))}; reconciliation tape on the CSV page.*
3. **Schedule E expenses** - Closing costs, furniture and the full property tax bill were expensed from the client spreadsheet;
   occupancy taxes and the Dollywood pass also included. Capitalize/depreciate, use her post-closing share of property tax, remove
   personal items.
   - *Preparer: Done. 4562 added (39-yr building, 100% bonus furniture, loan-cost amortization).*
4. **Personal-use days** - The 10/12-10/18 girls' trip is in the Trips tab. Enter 6 personal days so shared expenses are prorated;
   personal share of property tax to Sch A.
   - *Preparer: Done - {DAYS_RENTED} fair rental / {PERSONAL_DAYS} personal.*
5. **Schedule A** - Draft took the standard deduction and netted gambling to zero. Winnings are gross income; losses only as an
   itemized deduction, capped at winnings. 2025 = 100% (not 90%).
   - *Preparer: Corrected; itemizing now saves tax. Sales tax option used (no state income tax).*
6. **Schedule A line 15** - Remove the casualty entry. Not a federally declared disaster.
   - *Preparer: Removed; explained to client.*
7. **State** - W-2G shows NC withholding. Add NC nonresident D-400 (Sch PN).
   - *Preparer: Added; refund {fmt(nc_refund)}.*
8. FYI - Consider whether the building should be 27.5 or 39 years. We went with 39 (transient use). Signer to confirm.
   - *Signer (green): Agree 39-year.*
""")
print("EVG1020 done", R.summary()["11"], R.summary()["15"], R.summary()["24"], v["refund"], v["balance_due"], "NC", nc_tax, nc_refund)
