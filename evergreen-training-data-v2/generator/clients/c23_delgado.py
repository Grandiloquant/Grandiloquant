"""EVG1023 - Raymond & Carla Delgado (MFJ, North Carolina - Charlotte). NEW CLIENT (first year with Evergreen).
Raymond: (a) Catawba River Outfitters LLC - 40% general partner (member-manager), materially participates: guaranteed payments,
ordinary loss limited by basis (IRC 704(d)) and then by at-risk (IRC 465 - nonrecourse seller financing on equipment is not qualified
nonrecourse financing), SE income per box 14A, AMT box 17A adjustment that must NOT be added because the loss is limited (Form 6251
line 2n = 0); (b) Lakewood Partners LP - 10% limited partner: IRC 704(c)(1)(B) "mixing bowl" gain $250,000 disclosed only in a K-1
footnote + IRC 752(b) deemed distribution, passive loss suspended with new-client prior-year Regular vs AMT carryovers; (c) Baja Coastal
Ventures (Mexican entity taxed as a partnership) - $180,000 contribution -> Form 8865 Categories 3 and 4 + Form 8938.
Jointly owned rental duplex destroyed by fire 01/24/2025 - IRC 1033 election to defer the insurance gain (replacement deadline
12/31/2027) and Schedule E for January only. Carla: interior design Schedule C with 100% bonus depreciation (OBBBA, acquired after
01/19/2025) -> NC 85% bonus addback; SE tax; SEP; QBI. NC D-400; NIIT; estimates + extension."""
import datetime as dt

from common import ClientBuild, gotcha, fmt
from docs import statement, scanned_pages, write_text, write_xlsx
import forms as F
from tax2025 import Return1040, r, se_tax

C = ClientBuild("EVG1023", "Delgado", "Raymond & Carla Delgado")
ADDR = ("4708 Sardis Oaks Ct", "Charlotte, NC 28270")
T = {"name": "Raymond J. Delgado", "ssn": "XXX-XX-5127", "dob": "1971-10-03"}
S = {"name": "Carla S. Delgado", "ssn": "XXX-XX-8840", "dob": "1974-04-27"}
REC_T = [T["name"], *ADDR, f"TIN: {T['ssn']}"]
REC_S = [S["name"], *ADDR, f"TIN: {S['ssn']}"]
REC_J = ["Raymond J. & Carla S. Delgado", *ADDR, f"TIN: {T['ssn']}"]

# =================================================================== facts
# --- (a) Catawba River Outfitters LLC (equipment rental) - Raymond 40%, member-manager (general partner), material participation
CAT = {"name": "Catawba River Outfitters LLC", "ein": "00-3381204", "addr": "118 N Main St, Belmont, NC 28012",
       "gp": 95000, "box1": -52000, "box14a": 43000, "box17a": 6000, "beg_basis": 30000, "nonrecourse": 28000,
       "w2": 41000, "ubia": 612000}
assert CAT["box14a"] == CAT["gp"] + CAT["box1"]
CAT_BASIS_ALLOWED = min(-CAT["box1"], CAT["beg_basis"])                 # 30,000 (IRC 704(d))
CAT_BASIS_SUSP = -CAT["box1"] - CAT_BASIS_ALLOWED                       # 22,000
CAT_AT_RISK = CAT["beg_basis"] - CAT["nonrecourse"]                     # 2,000 (seller financing on equipment is not QNF)
CAT_ALLOWED = min(CAT_BASIS_ALLOWED, CAT_AT_RISK)                       # 2,000
CAT_ATRISK_SUSP = CAT_BASIS_ALLOWED - CAT_ALLOWED                       # 28,000
CAT_AMT_LOSS = -CAT["box1"] - CAT["box17a"]                             # 46,000 AMT loss before limits
CAT_AMT_ALLOWED = min(CAT_AMT_LOSS, CAT["beg_basis"], CAT_AT_RISK)      # 2,000
CAT_2N = (-CAT_AMT_ALLOWED) - (-CAT_ALLOWED)                            # 0
# --- (b) Lakewood Partners LP - Raymond 10% limited partner (real estate)
LAKE = {"name": "Lakewood Partners LP", "ein": "00-7724150", "addr": "200 Lakewood Pointe Dr, Mooresville, NC 28117",
        "box2": -14000, "box17a": 1200, "liab_beg": 180000, "liab_end": 95000, "beg_basis": 296000,
        "contrib_fmv": 400000, "contrib_basis": 150000, "contrib_date": "03/22/2021", "dist_date": "08/14/2025", "fmv_at_dist": 465000,
        "py_susp_reg": 31000, "py_susp_amt": 27500}
BIG = LAKE["contrib_fmv"] - LAKE["contrib_basis"]                       # 250,000
GAIN_704C = min(BIG, LAKE["fmv_at_dist"] - LAKE["contrib_basis"])       # 250,000
DEEMED_752 = LAKE["liab_beg"] - LAKE["liab_end"]                        # 85,000
LAKE_BASIS_BEFORE_LOSS = LAKE["beg_basis"] + GAIN_704C - DEEMED_752    # 461,000
LAKE_END_BASIS = LAKE_BASIS_BEFORE_LOSS + LAKE["box2"]                  # 447,000 (suspended passive losses still reduce basis)
LAKE_AMT_LOSS = -LAKE["box2"] - LAKE["box17a"]                          # 12,800
# --- (c) Baja Coastal Ventures S. de R.L. de C.V. (Mexico; Form 8832 partnership election 2019)
BAJA = {"name": "Baja Coastal Ventures, S. de R.L. de C.V.", "contrib": 180000, "pct": "15%", "date": "03/18/2025", "loss": -6000}
BAJA_END_BASIS = BAJA["contrib"] + BAJA["loss"]
# --- rental duplex destroyed by fire (jointly owned, active participation)
DUP = {"addr": "1407-1409 Thomas Ave, Charlotte, NC 28205", "pis": "05/10/2019", "bldg_cost": 290000, "land": 75000,
       "fire": dt.date(2025, 1, 24), "proceeds": 410000, "paid": "05/16/2025"}
ANNUAL = DUP["bldg_cost"] / 27.5
DEP_2019 = ANNUAL * 7.5 / 12
DEP_PRIOR = DEP_2019 + 5 * ANNUAL                                        # 2019-2024
DEP_2025 = round(ANNUAL * 0.5 / 12, 2)                                   # January (disposition month = half month)
ADJ_BASIS = r(DUP["bldg_cost"] - DEP_PRIOR - DEP_2025)
GAIN_1033 = DUP["proceeds"] - ADJ_BASIS
ACCUM_DEP = r(DEP_PRIOR + DEP_2025)
DEADLINE = "12/31/2027"
JAN = {"Rents received (2 units x $1,600 less refund of 01/24-01/31 rent to tenants $826)": 2374.00,
       "Taxes (Mecklenburg County 2025, January share 1/12 of $4,200)": -350.00,
       "Insurance (January share)": -200.00, "Utilities (water/sewer - landlord paid)": -140.00,
       "Repairs (unit B plumbing 01/08/2025)": -1260.00, "Management fee (10% of rents)": -237.40,
       "Depreciation (01/01-01/24/2025 - half month, 27.5-yr SL)": -DEP_2025}
DUP_NET = round(sum(JAN.values()), 2)
DUP_LAND_TAX = 4200.00 - 350.00                                          # rest of 2025 tax on the lot (held for rebuild) -> Sch A
# --- Carla - Schedule C (cash basis)
SCHC_INCOME = {"Design fees": 145000.00, "Furnishings sold to clients (resale)": 82500.00}
SCHC_GROSS = sum(SCHC_INCOME.values())
SCHC_COGS = 61200.00
ASSETS = [("Showroom furniture & display fixtures (7-yr)", "03/06/2025", 14200.00, 7),
          ("Design workstation + large-format plotter (5-yr)", "04/14/2025", 8600.00, 5),
          ("Sample-library shelving & display wall (7-yr)", "06/02/2025", 5200.00, 7)]
BONUS = sum(a[2] for a in ASSETS)
SCHC_EXP = {"8 Advertising": 3900.00, "9 Car (standard mileage 6,200 mi x $0.70)": 4340.00, "11 Contract labor": 8960.00,
            "13 Depreciation (Form 4562 - 100% bonus, OBBBA)": BONUS, "15 Insurance": 2850.00, "17 Legal & professional": 1900.00,
            "18 Office expense": 2240.00, "20b Rent - studio": 14400.00, "22 Supplies": 1810.00, "24a Travel": 2100.00,
            "24b Meals (50% of $1,280)": 640.00, "25 Utilities / phone": 1560.00, "27a Software subscriptions": 3600.00}
SCHC_NET = SCHC_GROSS - SCHC_COGS - sum(SCHC_EXP.values())
assert SCHC_NET == 90000
BOOK_DEP = round(BONUS * .40 + 8600 * .6 * .20 + 19400 * .6 * .1429, 2)        # bookkeeper's 40% phase-down bonus + MACRS
NC_ADDBACK = r(BONUS * .85)                                                     # 23,800
NC_FUTURE = r(NC_ADDBACK / 5)                                                   # 4,760 per year 2026-2030
# --- other income / deductions / payments
ALLY_INT = 2840.12
MMF_DIV = 9612.40                       # Schwab Value Advantage Money Fund (insurance proceeds parked) - 1099-DIV, not interest
FID_DIV, FID_QDIV = 4200.00, 3600.00
NC_ES = [("04/15/2025", 3800.00), ("06/16/2025", 3800.00), ("09/15/2025", 3800.00), ("01/15/2026", 3800.00)]
NC_PY_BAL = 1150.00
HOME_RE_TAX, MORT_INT, CHARITY = 6140.00, 14380.00, 6500.00
FED_ES = [("04/15/2025", 16000.00), ("06/16/2025", 16000.00), ("09/15/2025", 16000.00), ("01/15/2026", 16000.00)]
FED_EXT, NC_EXT = 15000.00, 3000.00
PY = {"agi": 251300, "tax": 56400, "nc_tax": 10140}

# =================================================================== PERM
C.write_profile(f"""
# EVG1023 - Delgado, Raymond & Carla  (PERM)

*Synthetic client - Project Evergreen training data.*

| Item | Detail |
|---|---|
| Client ID | EVG1023 |
| Taxpayer | Raymond J. Delgado, DOB 10/03/1971, SSN XXX-XX-5127 - managing member, Catawba River Outfitters LLC; investor |
| Spouse | Carla S. Delgado, DOB 04/27/1974, SSN XXX-XX-8840 - owner, Carla Delgado Interiors (sole proprietor, Sch C) |
| Address | {ADDR[0]}, {ADDR[1]} (Mecklenburg County) - NC residents all years |
| Dependents | None (son Mateo, 24, independent) |
| Contact | Carla preferred - carla@example.com, (704) 555-0163; eSign OK |
| Engagement | **New client 2025** (prior preparer Queen City Tax Pros PLLC retired). Quote $5,500 (3 K-1s, Sch C, rental casualty, Form 8865) |
| Payment info | Voided check on file (Truist ****4421) |

## K-1 / activity carryforward schedule (from prior preparer's 2024 workpapers - verify)
| Activity | Character | Outside basis 12/31/2024 | Suspended losses c/f to 2025 |
|---|---|---|---|
| Catawba River Outfitters LLC (40%, member-manager) | Nonpassive (material participation) | 30,000 (incl. 28,000 share of nonrecourse seller note) | none |
| Lakewood Partners LP (10% LP; land contributed 03/22/2021) | Passive - limited partner | 296,000 (incl. 180,000 share of liabilities) | 8582: Regular 31,000 / AMT 27,500 |
| Baja Coastal Ventures (Mexico) | Passive | n/a - acquired 03/2025 | - |
| Rental duplex {DUP['addr']} (joint, active participation) | Passive rental | building cost 290,000 (PIS 05/10/2019), land 75,000 | none |
""")
F.prior_year_summary(C.perm_file("2024_Form_1040_Return_Summary.pdf", "Prior-year return summary (prior preparer)"),
    "Raymond & Carla Delgado", "EVG1023", "Married filing jointly", [
        ["Sch C", "Carla Delgado Interiors - net profit", 84200], ["Sch E", "Catawba GP 90,000 + ordinary income 8,400; duplex rental net 6,900; "
         "Lakewood (9,000) suspended", 105300], ["2b / 3b", "Interest / dividends", "1,900 / 4,000"],
        ["11", "AGI", PY["agi"]], ["12", "Itemized deductions", 38700], ["13", "QBI deduction", 16800],
        ["24", "Total tax (incl. SE tax)", PY["tax"]], ["NC D-400", "NC tax", PY["nc_tax"]], ["37", "Amount owed", 2410]],
    carryovers=[["Form 8582 - Lakewood Partners LP unallowed loss - Regular tax", 31000],
                ["Form 8582 - Lakewood Partners LP unallowed loss - AMT", 27500],
                ["Catawba River Outfitters - outside basis 12/31/2024 (prior preparer worksheet)", 30000],
                ["Capital loss carryover", 0]],
    notes="Copy of the 2024 return provided by Queen City Tax Pros PLLC. Their Form 8582 worksheet lists Lakewood's prior-year unallowed "
          "loss separately for regular tax and AMT (AMT depreciation is slower). Duplex depreciation schedule attached to the 2024 return.")
statement(C.perm_file("Lakewood_Partners_2021_Contribution_Agreement_excerpt.pdf", "Legal agreement (PERM)"),
    "Lakewood Partners LP - Contribution Agreement (excerpt) - 03/22/2021", [
        {"para": ["1. Contribution. Raymond J. Delgado (\"Contributor\") contributes to the Partnership all right, title and interest in the "
                  "unimproved parcel of approximately 6.1 acres at Mooresville Road, Iredell County, NC (PIN 4655-xx-xxxx) (the \"Parcel\").",
                  "2. Agreed value. The Parties agree the fair market value of the Parcel is $400,000. Contributor represents that his adjusted "
                  "tax basis in the Parcel is $150,000 (purchased 2009).",
                  "3. Interest. In exchange the Contributor receives a 10% limited partnership interest.",
                  "4. Section 704(c). Built-in gain on the Parcel shall be allocated to the Contributor in accordance with IRC Section 704(c) "
                  "using the traditional method. The General Partner shall notify the Contributor before any distribution of the Parcel "
                  "to another partner within seven years of this contribution.",
                  "5. The Partnership will hold the Parcel for investment pending a joint-venture decision."]}])
statement(C.perm_file("Catawba_River_Outfitters_seller_note_summary.pdf", "Loan summary (PERM)"),
    "Catawba River Outfitters LLC - Equipment Purchase - Seller Financing Summary", [
        {"table": [["Term", "Detail"], ["Seller / lender", "Foothills Marine & Outdoor Supply, Inc. (equipment dealer; seller of the equipment)"],
                   ["Original principal (11/2023)", 70000.00], ["Collateral", "Rafts, kayaks, trailers, shuttle vans (equipment only)"],
                   ["Recourse", "NONRECOURSE - lender's sole remedy is the collateral; no member guaranty"],
                   ["Terms", "Interest-only 8% through 12/2026, then 36-month amortization"],
                   ["Raymond's 40% share (K-1 item K, nonrecourse)", 28000.00]], "left_align_cols": [0, 1]},
        {"para": "Prior preparer's 2024 basis worksheet: capital 2,000 + share of nonrecourse liabilities 28,000 = outside basis 30,000. "
                 "No at-risk computation (Form 6198) was attached to the 2024 return (Catawba had income in 2024)."}])

# =================================================================== PBC
F.engagement_letter(C.pbc_file("00_Engagement_Letter_signed.pdf", "Engagement letter (signed)", "2026-02-03"), "Raymond & Carla Delgado",
    "EVG1023", "Quoted fee $5,500 for the 2025 federal and North Carolina returns including Form 8865 and Form 8938.", "02/03/2026",
    "2025 Form 1040, NC D-400, Forms 8865 and 8938, and the IRC 1033 election statement for the rental fire.")
F.organizer(C.pbc_file("01_2025_Organizer_completed.pdf", "Client organizer", "2026-02-18"), "Raymond & Carla Delgado", "EVG1023",
    general=[("Did your marital status change during 2025?", "No", ""),
             ("Did you receive any K-1s?", "Yes", "Catawba, Lakewood (late every year)"),
             ("Did you invest in or own any foreign business or account?", "Yes", "Baja Coastal - Mexico, put in $180k"),
             ("Did you sell, or lose to casualty, any property?", "Yes", "Thomas Ave duplex burned 1/24 - insurance paid in May"),
             ("Do you plan to replace the property?", "Yes", "rebuild or buy another rental - builder says 2027"),
             ("Did you buy business equipment?", "Yes", "Carla - $28,000 showroom/studio (see bookkeeper)"),
             ("Do you want to maximize retirement contributions?", "Yes", "Carla SEP - max"),
             ("Did you make estimated payments?", "Yes", "Fed 4 x 16,000; NC 4 x 3,800"),
             ("Did you receive, sell, exchange digital assets?", "No", "")],
    dependents=[],
    income_rows=[["Business income (Sch C)", "Carla Delgado Interiors", 84200, "~90k after equipment"],
                 ["K-1 Catawba River Outfitters", "guaranteed payments + share", 98400, "loss year"],
                 ["K-1 Lakewood Partners LP", "", -9000, ""],
                 ["Rental - Thomas Ave duplex", "", 6900, "January only - fire"],
                 ["Interest", "Ally Bank", 1900, "2,840"],
                 ["Dividends", "Fidelity / Schwab", 4000, "see 1099s"]],
    deductions_rows=[["Mortgage interest", "Truist Mortgage", 15100, "see 1098"],
                     ["Real estate taxes", "Mecklenburg County - home", 5900, "6,140"],
                     ["Real estate taxes", "Mecklenburg County - Thomas Ave", 4100, "4,200"],
                     ["Charitable", "St. Gabriel / Second Harvest", 6000, "6,500"]],
    signature_date="02/16/2026")

F.k1_generic(C.pbc_file("02_K-1_1065_Catawba_River_Outfitters.pdf", "Schedule K-1 (1065)", "2026-03-20"), "Form 1065", CAT["name"],
    [["EIN", CAT["ein"]], ["Name / address", f"{CAT['name']}, {CAT['addr']}"], ["IRS Center", "Ogden, UT"]],
    [["Partner", f"{T['name']}, {ADDR[0]}, {ADDR[1]} - TIN {T['ssn']}"],
     ["Type", "General partner or LLC member-manager: X;  Domestic partner"],
     ["J Profit / Loss / Capital (beginning & ending)", "40% / 40% / 40%"],
     ["K Share of liabilities - beginning / ending", "Nonrecourse 28,000 / 28,000; Qualified nonrecourse 0 / 0; Recourse 0 / 0"],
     ["L Capital account (tax basis)", "Beginning 2,000; contributed 0; current-year net income (loss) (52,000); withdrawals 0; ending (50,000)"],
     ["M Contributed property with built-in gain?", "No"]], [],
    [["1", "Ordinary business income (loss)", "", CAT["box1"]], ["4a", "Guaranteed payments for services", "", CAT["gp"]],
     ["4c", "Total guaranteed payments", "", CAT["gp"]], ["14", "Self-employment earnings (loss)", "A", CAT["box14a"]],
     ["17", "Alternative minimum tax (AMT) items", "A  Post-1986 depreciation adjustment", CAT["box17a"]],
     ["19", "Distributions", "A", 0], ["20", "Other information", "Z  Section 199A information", "STMT"]],
    supplemental=[{"heading": "Statement A - Section 199A information (Catawba River Outfitters LLC - not an SSTB)",
                   "table": [["Item", "Amount"], ["Ordinary business income (loss)", CAT["box1"]], ["W-2 wages", CAT["w2"]],
                             ["UBIA of qualified property", CAT["ubia"]], ["Guaranteed payments (not QBI)", CAT["gp"]]]},
                  {"heading": "Partner notes", "para": ["Loss for 2025 reflects first full year of depreciation on the 2023-2024 fleet and "
                   "lower rafting season revenue (drought). Partners are responsible for applying basis, at-risk and passive limitations. "
                   "The equipment seller note is nonrecourse (see item K).",
                   "NC: Partnership files NC D-403; NC-K-1 shows no NC adjustments for 2025 (no bonus depreciation claimed)."]}])
F.k1_generic(C.pbc_file("03_K-1_1065_Lakewood_Partners_LP.pdf", "Schedule K-1 (1065) package", "2026-08-21", note="received after extension"),
    "Form 1065", LAKE["name"],
    [["EIN", LAKE["ein"]], ["Name / address", f"{LAKE['name']}, {LAKE['addr']}"], ["General partner", "Lakewood GP LLC"]],
    [["Partner", f"{T['name']}, {ADDR[0]}, {ADDR[1]} - TIN {T['ssn']}"], ["Type", "Limited partner;  Domestic partner"],
     ["J Profit / Loss / Capital", "10% / 10% / 10%"],
     ["K Share of liabilities - beginning / ending", f"Qualified nonrecourse {LAKE['liab_beg']:,} / {LAKE['liab_end']:,}; other 0 / 0"],
     ["L Capital account (tax basis)", "Beginning 116,000; current-year net income (loss) (14,000); other increase 250,000 (see footnote 3); "
      "withdrawals 0; ending 352,000"],
     ["M Contributed property with built-in gain?", "Yes (see footnote 3)"]], [],
    [["2", "Net rental real estate income (loss)", "", LAKE["box2"]], ["9a", "Net long-term capital gain (loss)", "", 0],
     ["17", "Alternative minimum tax (AMT) items", "A  Post-1986 depreciation adjustment", LAKE["box17a"]],
     ["19", "Distributions", "A", 0], ["20", "Other information", "Z / footnotes", "STMT"]],
    supplemental=[{"heading": "Footnotes to Schedule K-1 (page 4 of 4)", "para": [
        "1. Rental activities: Mooresville Commons retail center (Iredell County, NC). Limited partners do not materially participate.",
        "2. The partnership refinanced its mortgage in 2025; principal reduced with operating reserves. Partner's share of qualified "
        "nonrecourse financing is shown in item K.",
        f"3. Section 704(c)(1)(B). On {LAKE['dist_date']} the Partnership distributed the Mooresville Road parcel (contributed by R. Delgado "
        f"on {LAKE['contrib_date']}) to partner Harbor Pointe Holdings LLC in partial redemption of its interest. Because the parcel was "
        "distributed to a partner other than the contributing partner within seven years of its contribution, the contributing partner "
        f"is treated as recognizing gain equal to the remaining built-in gain of ${GAIN_704C:,}. The parcel was held for investment. This "
        "gain is not included in box 9a. The contributing partner's basis in his partnership interest is increased by the gain recognized. "
        "Consult your tax advisor.",
        "4. State: all income/loss is North Carolina-source. NC withholding on nonresident partners: not applicable."]}])
statement(C.pbc_file("04_Baja_Coastal_capital_contribution_wire_and_receipt.pdf", "Wire confirmation + receipt", "2026-02-18"),
    "Truist Bank - Outgoing International Wire Confirmation / Baja Coastal Ventures Capital Receipt", [
        {"table": [["Field", "Value"], ["Date", BAJA["date"]], ["Originator", "Raymond J. Delgado - Truist ****4421"],
                   ["Beneficiary", f"{BAJA['name']} - BBVA Mexico, CLABE ****0117"], ["Amount (USD)", BAJA["contrib"]],
                   ["Purpose", "Aportacion de capital / capital contribution - 15% interest (partes sociales)"]], "left_align_cols": [0, 1]},
        {"para": "Recibo: Baja Coastal Ventures acknowledges receipt of USD 180,000 as a capital contribution by Raymond J. Delgado, "
                 "representing 15% of the partes sociales after the capital increase approved by the asamblea de socios on 03/12/2025."}])
scanned_pages(C.pbc_file("05_Baja_Coastal_Acta_de_Asamblea_2025-03-12_scan.pdf", "Scanned legal document (Spanish)", "2026-02-18"),
    [["ACTA DE ASAMBLEA GENERAL EXTRAORDINARIA DE SOCIOS",
      "BAJA COASTAL VENTURES, S. DE R.L. DE C.V.",
      "La Paz, Baja California Sur, a 12 de marzo de 2025",
      "",
      "PRIMERO. Se aprueba el aumento de capital social variable por",
      "la cantidad equivalente a USD 180,000.00 suscrito por el",
      "Sr. Raymond J. Delgado (residente de EE.UU.).",
      "SEGUNDO. Despues del aumento, la participacion del Sr. Delgado",
      "sera de 15% de las partes sociales.",
      "TERCERO. Los socios mexicanos (Grupo Pacifico Sur, 60%;",
      "Inmobiliaria Cabo Azul, 25%) conservan el control.",
      "",
      "Nota (traduccion del cliente): the company elected to be a",
      "partnership for US taxes in 2019 (Form 8832) - ask CPA"]], handwritten=False, skew=-1.3, seed=231)
statement(C.pbc_file("06_Baja_Coastal_2025_US_tax_information_letter.pdf", "Partner information letter", "2026-07-30", note="received after extension"),
    f"{BAJA['name']} - 2025 U.S. Tax Information for U.S. Partners", [
        {"para": ["Prepared by the company's U.S. tax adviser for U.S. members. The company is classified as a partnership for U.S. federal "
                  "tax purposes (Form 8832 effective 01/01/2019; IRS acceptance letter on file). The company does not file Form 1065 and "
                  "does not issue Schedules K-1; U.S. members who are required to file Form 8865 should report the information below.",
                  "Amounts translated from MXN using the IRS 2025 yearly average rate; U.S. tax principles applied."]},
        {"table": [["Item (Raymond J. Delgado - 15% from 03/18/2025)", "USD"], ["Capital contributed 03/18/2025", BAJA["contrib"]],
                   ["Share of ordinary business income (loss) - boutique hotel development/operation", BAJA["loss"]],
                   ["Distributions", 0], ["Share of liabilities (all nonrecourse, Mexican bank construction loan)", 0],
                   ["Foreign taxes paid or accrued", 0], ["Ending capital account (tax basis)", BAJA_END_BASIS]]},
        {"para": "Members do not participate in management (managed by Grupo Pacifico Sur). Mexican entity has no U.S. trade or business."}])
statement(C.pbc_file("07_Piedmont_Mutual_fire_claim_settlement_letter.pdf", "Insurance settlement letter", "2026-02-18"),
    "Piedmont Mutual Insurance Co. - Claim No. PM-25-008817 - Settlement Letter (05/12/2025)", [
        {"table": [["Item", "Amount"], ["Insured", "Raymond J. & Carla S. Delgado"], ["Property", DUP["addr"] + " (2-unit dwelling, rental)"],
                   ["Date of loss", "01/24/2025 - fire (electrical, unit B)"], ["Coverage A - Dwelling (replacement cost policy, actual cash value paid)", DUP["proceeds"]],
                   ["Debris removal (included in Coverage A)", "included"], ["Loss of rents (Coverage D)", "Not purchased"],
                   ["Payment date", DUP["paid"]]], "left_align_cols": [0]},
        {"para": "Replacement-cost holdback: none (policy settled at agreed value). Land is not covered. Structure declared a total loss by "
                 "the City of Charlotte (demolition permit 03/2025)."}])
statement(C.pbc_file("08_Charlotte_Fire_Dept_incident_report.pdf", "Incident report", "2026-02-18"),
    "Charlotte Fire Department - Incident Report 25-0011893 (public summary)", [
        {"para": ["Date/time: 01/24/2025 03:12. Address: 1409 Thomas Ave. Structure: 2-unit residential. Cause: electrical (undetermined "
                  "origin in wall cavity, unit B). Occupants evacuated - no injuries. Structure: total loss.",
                  "Not a federally declared disaster."]}])
scanned_pages(C.pbc_file("09_Carla_handwritten_duplex_January_ledger.pdf", "Handwritten ledger (scan)", "2026-02-18"),
    [["Thomas Ave - Jan 2025",
      "Rent unit A  1,600   (pd 1/2)",
      "Rent unit B  1,600   (pd 1/3)",
      "Refunded tenants 1/24-1/31:  A 413  B 413  = 826",
      "Plumber unit B 1/8  - 1,260",
      "Duke water/sewer   - 140",
      "Mgmt fee 10%   - 237.40",
      "Insurance + county tax - monthly share?",
      "FIRE 1/24 - insurance check 410k in May (Schwab MMF)",
      "Builder (Belk Homes) estimate to rebuild: ~$465k, 2026-27"]], handwritten=True, seed=232)
write_text(C.pbc_file("10_Email_Raymond_duplex_and_K-1s_2026-03-02.txt", "Client correspondence", "2026-03-02", "Email"),
"""From: Raymond Delgado <ray.delgado@example.com>
To: preparer@evergreentax.example
Date: Mon, 2 Mar 2026 07:58:31 -0500
Subject: Re: Delgado 2025 - open items

1) Duplex: we 100% plan to replace it - either rebuild on the same lot (Belk Homes quote attached separately, ~$465k,
   permits in 2026) or buy another rental if the numbers work. Our old CPA said we don't have to pay tax on the insurance
   if we reinvest - how long do we have? The insurance adjuster said "two years from the fire".
2) Lakewood K-1 always comes in August. Catawba's K-1 is uploaded.
3) Baja: I wired $180k last March for 15%. They don't do a K-1 - their US accountant sends a letter in the summer.
4) Carla's bookkeeper (Jen) did her depreciation in QuickBooks - Carla wants the SEP maxed again.
Ray
""")
write_xlsx(C.pbc_file("11_Carla_Delgado_Interiors_QuickBooks_PL_2025.xlsx", "Spreadsheet (QuickBooks export)", "2026-02-18"),
    {"Profit and Loss 2025": [["Account", "Amount"]] + [[k, v] for k, v in SCHC_INCOME.items()] +
        [["Total income", SCHC_GROSS], ["Cost of goods sold - client furnishings", -SCHC_COGS], ["Gross profit", SCHC_GROSS - SCHC_COGS]] +
        [[k.split(" ", 1)[1] if k[0].isdigit() else k, -(BOOK_DEP if "Depreciation" in k else v)] for k, v in SCHC_EXP.items()] +
        [["Net income (books)", SCHC_GROSS - SCHC_COGS - sum(SCHC_EXP.values()) + BONUS - BOOK_DEP]],
     "Fixed asset additions": [["Asset", "Placed in service", "Cost", "MACRS life", "Bookkeeper depreciation (40% bonus + MACRS)"]] +
        [[a, d, c, f"{life}-yr", round(c * .4 + c * .6 * (.20 if life == 5 else .1429), 2)] for a, d, c, life in ASSETS] +
        [["Note (Jen)", "", "", "", "Used 40% bonus per 2025 phase-down schedule"]],
     "Income by client": [["Client / channel", "Amount", "1099?"], ["Piedmont Custom Homes", 48000, "1099-NEC"],
                          ["Ballantyne Hospitality Group", 22500, "1099-NEC"], ["Square card payments", 61800, "1099-K"],
                          ["Checks / ACH - residential clients", 95200, "none"], ["Total", SCHC_GROSS, ""]]})
F.f1099_nec(C.pbc_file("12_1099-NEC_Piedmont_Custom_Homes.pdf", "Form 1099-NEC", "2026-02-18"),
            ["Piedmont Custom Homes LLC", "5960 Fairview Rd", "Charlotte, NC 28210", "TIN: 00-5527310"], REC_S, {"1": 48000.00})
F.f1099_nec(C.pbc_file("13_1099-NEC_Ballantyne_Hospitality.pdf", "Form 1099-NEC", "2026-02-18"),
            ["Ballantyne Hospitality Group Inc", "14801 Ballantyne Village Way", "Charlotte, NC 28277", "TIN: 00-3390416"], REC_S, {"1": 22500.00})
F.f1099_k(C.pbc_file("14_1099-K_Square_Carla.pdf", "Form 1099-K", "2026-02-18"),
          ["Block, Inc. (Square)", "1955 Broadway Ste 600", "Oakland, CA 94612", "TIN: 00-0429876"], REC_S,
          {"1a": 61800.00, "3": 74, "months": [3100, 4200, 6900, 5200, 4800, 7100, 3900, 5600, 6200, 5400, 4300, 5100],
           "filer_type": "Payment settlement entity"})
F.f1099_int(C.pbc_file("15_1099-INT_Ally_Bank.pdf", "Form 1099-INT", "2026-02-18"),
            ["Ally Bank", "PO Box 951", "Horsham, PA 19044", "TIN: 00-0000002"], REC_J, {"1": ALLY_INT}, account="****7310")
F.f1099_div(C.pbc_file("16_1099-DIV_Schwab_Value_Advantage_MMF.pdf", "Form 1099-DIV", "2026-02-18"),
            ["Charles Schwab & Co., Inc.", "211 Main St", "San Francisco, CA 94105", "TIN: 00-1737782"], REC_J,
            {"1a": MMF_DIV, "1b": 0.00}, account="****6650 (Schwab Value Advantage Money Fund - SWVXX)")
F.f1099_div(C.pbc_file("17_1099-DIV_Fidelity_joint.pdf", "Form 1099-DIV", "2026-02-18"),
            ["Fidelity Brokerage Services LLC", "900 Salem St", "Smithfield, RI 02917", "TIN: 00-2153912"], REC_J,
            {"1a": FID_DIV, "1b": FID_QDIV}, account="****2245")
F.f1098(C.pbc_file("18_1098_Truist_Mortgage.pdf", "Form 1098", "2026-02-18"),
        ["Truist Bank - Mortgage", "PO Box 2467", "Greensboro, NC 27420", "TIN: 00-0298860"], REC_J,
        {"1": MORT_INT, "2": 402118.70, "3": "08/20/2020", "7": "Yes", "9": "1"}, account="****9032")
statement(C.pbc_file("19_Mecklenburg_County_tax_bills_2025.pdf", "Property tax bills", "2026-02-18"), "Mecklenburg County - 2025 Property Tax Receipts", [
    {"table": [["Parcel", "Paid", "Amount"], ["4708 Sardis Oaks Ct (residence)", "12/18/2025", HOME_RE_TAX],
               ["1407-1409 Thomas Ave (duplex; building destroyed 01/24/2025 - 2025 bill on 01/01 valuation)", "12/18/2025", 4200.00]]}])
statement(C.pbc_file("20_Estimated_tax_payment_confirmations.pdf", "Payment confirmations", "2026-02-18"), "2025 Estimated Tax Payments (IRS Direct Pay / NCDOR)", [
    {"table": [["Date", "Federal 1040-ES", "NC NC-40"]] + [[a, b, c] for (a, b), (_, c) in zip(FED_ES, NC_ES)],
     "left_align_cols": [0]},
    {"para": f"Also paid 04/15/2025: NC 2024 D-400 balance ${NC_PY_BAL:,.2f}; federal 2024 balance $2,410.00."}])
write_text(C.pbc_file("21_Extension_confirmations_2026-04-15.txt", "Extension confirmation", "2026-04-15", "Evergreen e-file system"),
f"""Form 4868 - TY2025 - Raymond J. & Carla S. Delgado - transmitted 04/14/2026 - ACCEPTED 04/15/2026.
Payment with extension: ${FED_EXT:,.2f} (EFW Truist ****4421).  NC D-410 extension payment ${NC_EXT:,.2f} (04/15/2026).
Reason: Lakewood K-1 (expected August) and Baja Coastal partner information letter outstanding.
""")
write_text(C.pbc_file("22_Email_Carla_SEP_funded_2026-09-08.txt", "Client correspondence", "2026-09-08", "Email"),
"""From: Carla Delgado <carla@example.com>
To: preparer@evergreentax.example
Date: Tue, 8 Sep 2026 12:30:11 -0400
Subject: SEP done

Funded the SEP-IRA at Fidelity today with the amount you sent ($16,728) - designated for 2025. Confirmation attached.
""")

# =================================================================== RETURN
se_r, se_c = se_tax(CAT["box14a"]), se_tax(SCHC_NET)
SEP = r((SCHC_NET - se_c["half"]) * .20)
SCH_E = CAT["gp"] - CAT_ALLOWED                       # GP 95,000 nonpassive + allowed loss (2,000); passive losses suspended
QBI_C = SCHC_NET - se_c["half"] - SEP
QBI_CAT = -CAT_ALLOWED - se_r["half"]                 # GP is not QBI; half-SE allocated here (conservative assumption)
SALT_INC = sum(a for d, a in NC_ES if d.endswith("2025")) + NC_PY_BAL
facts = {
    "status": "MFJ", "taxpayer": {"age65": False}, "spouse": {"age65": False},
    "interest": [{"payer": "Ally Bank", "amount": ALLY_INT}],
    "dividends": [{"payer": "Schwab Value Advantage Money Fund (insurance proceeds)", "ordinary": MMF_DIV, "qualified": 0},
                  {"payer": "Fidelity Brokerage - joint", "ordinary": FID_DIV, "qualified": FID_QDIV}],
    "k1_lt": GAIN_704C,
    "sch1": {"sch_c": SCHC_NET, "sch_e": SCH_E},
    "se": [{"who": "T", "net_profit": CAT["box14a"]}, {"who": "S", "net_profit": SCHC_NET}],
    "se_earned_T": CAT["box14a"], "se_earned_S": SCHC_NET,
    "adjustments": {"sep": SEP},
    "itemized": {"state_income_tax": SALT_INC, "real_estate_tax": HOME_RE_TAX + DUP_LAND_TAX, "mortgage_interest_1098": MORT_INT,
                 "charity_cash": CHARITY},
    "qbi": {"businesses": [{"name": "Carla Delgado Interiors (Sch C)", "qbi": QBI_C},
                           {"name": "Catawba River Outfitters LLC (allowed loss)", "qbi": QBI_CAT}]},
    "amt": {"check": True},
    "estimated_payments": sum(a for _, a in FED_ES), "extension_payment": FED_EXT,
}
pre = Return1040(dict(facts)).compute()
NII = GAIN_704C + pre.values["2b"] + pre.values["3b"]
facts["niit"] = {"nii": NII}
R = Return1040(facts).compute()
v = R.values
# what-ifs for the rubric
fx = dict(facts); fx["sch1"] = {"sch_c": SCHC_NET, "sch_e": CAT["gp"] + CAT["box1"]}
fx["qbi"] = {"businesses": [{"name": "c", "qbi": QBI_C}, {"name": "cat", "qbi": CAT["box1"] - se_r["half"]}]}
RX = Return1040(fx).compute()
LOSS_LIMIT_EFFECT = RX.values["24"] - v["24"]          # negative: tax understated if full loss taken
fg = dict(facts); fg["k1_lt"] = 0; fg["niit"] = {"nii": NII - GAIN_704C}
RG = Return1040(fg).compute()
GAIN_EFFECT = v["24"] - RG.values["24"]
REPLACEMENT_BASIS_NOTE = f"replacement cost less deferred gain {GAIN_1033:,}"

# --- NC D-400
NC_AGI = v["11"]
NC_ITEM = min(20000, MORT_INT + HOME_RE_TAX) + CHARITY
NC_STD = 25500
NC_DED = max(NC_ITEM, NC_STD)
NC_TI = NC_AGI + NC_ADDBACK - NC_DED
NC_TAX = r(NC_TI * .0425)
NC_PAY = sum(a for _, a in NC_ES) + NC_EXT
NC_REFUND = NC_PAY - NC_TAX
assert sum(a for _, a in NC_ES) >= PY["nc_tax"]          # NC estimates >= 100% of 2024 NC tax -> no NC-40 penalty

# =================================================================== return PDF attachments
k1_att = [["K-1 basis / at-risk / passive (Raymond)", "Catawba River Outfitters", "Lakewood Partners LP", "Baja Coastal (8865)"],
          ["Beginning outside basis", CAT["beg_basis"], LAKE["beg_basis"], 0],
          ["Contributions", 0, 0, BAJA["contrib"]],
          ["IRC 704(c)(1)(B) gain recognized (basis increase)", 0, GAIN_704C, 0],
          ["IRC 752(b) deemed distribution (liability share decrease)", 0, -DEEMED_752, 0],
          ["Basis before current-year loss", CAT["beg_basis"], LAKE_BASIS_BEFORE_LOSS, BAJA["contrib"]],
          ["Current-year loss", CAT["box1"], LAKE["box2"], BAJA["loss"]],
          ["Allowed by basis (704(d)) / suspended", f"{CAT_BASIS_ALLOWED:,} / {CAT_BASIS_SUSP:,}", f"{-LAKE['box2']:,} / 0", f"{-BAJA['loss']:,} / 0"],
          ["At-risk amount (Form 6198) / allowed", f"{CAT_AT_RISK:,} / {CAT_ALLOWED:,}", "QNF counts - not limited", "not limited"],
          ["Suspended by at-risk (carryforward)", CAT_ATRISK_SUSP, 0, 0],
          ["Passive?", "No - material participation", "Yes - limited partner", "Yes"],
          ["Allowed on Schedule E (2025)", -CAT_ALLOWED, 0, 0],
          ["Ending outside basis", 0, LAKE_END_BASIS, BAJA_END_BASIS]]
f8582 = [["Form 8582 - passive activities (all suspended)", "2025 loss", "PY unallowed", "Regular c/f to 2026", "AMT c/f to 2026"],
         ["Lakewood Partners LP (limited partner - no $25,000 allowance)", LAKE["box2"], -LAKE["py_susp_reg"],
          LAKE["box2"] - LAKE["py_susp_reg"], -(LAKE_AMT_LOSS + LAKE["py_susp_amt"])],
         ["Baja Coastal Ventures (foreign partnership)", BAJA["loss"], 0, BAJA["loss"], BAJA["loss"]],
         ["Duplex - Thomas Ave (active participation; MAGI > $150,000 -> $0 allowance)", DUP_NET, 0, DUP_NET, DUP_NET],
         ["Passive income", 0, "", "", ""],
         ["Note", "704(c)(1)(B) gain is portfolio (land held for investment) - not passive income; fire + IRC 1033 deferral is not a fully "
                  "taxable disposition - duplex loss not released (IRC 469(g))", "", "", ""]]
f6251 = [["Form 6251 - loss-limited K-1 AMT items", "Regular allowed", "AMT allowed", "Line 2n"],
         ["Catawba: box 17A +6,000 -> AMT loss 46,000, limited to the same $2,000 at-risk", -CAT_ALLOWED, -CAT_AMT_ALLOWED, CAT_2N],
         ["Lakewood: box 17A +1,200 -> loss suspended (passive) for both systems", 0, 0, 0],
         ["Line 2l (depreciation) - box 17A amounts NOT reported (loss limited)", "", "", 0]]
f1033 = [["IRC 1033 election statement (attached; Form 4684 Section B)", "Amount"],
         [f"Property: {DUP['addr']} - 2-unit residential rental building, PIS {DUP['pis']}", ""],
         ["Involuntary conversion: destroyed by fire 01/24/2025; insurance proceeds received " + DUP["paid"], DUP["proceeds"]],
         [f"Adjusted basis of building (cost {DUP['bldg_cost']:,} less depreciation {ACCUM_DEP:,} through 01/24/2025)", ADJ_BASIS],
         ["Gain realized (incl. depreciation that would be unrecaptured 1250 gain)", GAIN_1033],
         ["Gain postponed - taxpayers elect IRC 1033(a)(2); intend to rebuild/replace with similar-use rental property", GAIN_1033],
         ["Gain recognized in 2025", 0],
         [f"Replacement period ends {DEADLINE} (2 years after the close of 2025, the first year gain was realized)", ""],
         ["Taxpayers will report replacement details (or recognize gain by amended return) when replaced or the period expires", ""]]
schc = [["Schedule C - Carla Delgado Interiors (NAICS 541410; cash method)", "Amount"],
        ["1 Gross receipts (1099-NEC 70,500 + 1099-K 61,800 + checks/ACH 95,200)", SCHC_GROSS], ["4 Cost of goods sold", SCHC_COGS],
        ["7 Gross income", SCHC_GROSS - SCHC_COGS]] + [[k, v_] for k, v_ in SCHC_EXP.items()] + [["31 Net profit", SCHC_NET]]
f4562 = [["Form 4562 - 2025 additions (acquired and placed in service after 01/19/2025)", "Cost", "100% bonus (IRC 168(k), OBBBA)"]] + \
        [[f"{a} - PIS {d}", c, c] for a, d, c, _ in ASSETS] + [["Total", BONUS, BONUS],
        ["Bookkeeper's QuickBooks depreciation (40% bonus phase-down + MACRS) - not used", "", BOOK_DEP]]
sep_att = [["SEP-IRA maximum (Carla)", "Amount"], ["Net profit", SCHC_NET], ["Less deductible half of SE tax", -se_c["half"]],
           ["Net earnings for plan", SCHC_NET - se_c["half"]], ["x 20% (25% plan rate, self-employed)", SEP],
           ["Funded 09/08/2026 (before extended due date), designated 2025", SEP]]
qbi_att = [["Form 8995 support", "QBI"], ["Carla Delgado Interiors: 90,000 - half SE - SEP", QBI_C],
           ["Catawba River Outfitters: allowed loss (2,000) - half SE (assumption); GP excluded (IRC 199A(c)(4))", QBI_CAT],
           ["Suspended Catawba losses (22,000 basis + 28,000 at-risk) - QBI loss carryforward when allowed", ""],
           ["Passive suspended losses - excluded until allowed", ""]]
f8865 = [["Form 8865 (Baja Coastal Ventures, S. de R.L. de C.V.) - Raymond", "Detail"],
         ["Filer categories", "Category 3 (IRC 6038B - contributed $180,000 cash, > $100,000 in 12 months) and Category 4 (IRC 6046A - "
                              "acquired a 10%+ interest)"],
         ["Schedule O - transfer of property", "Cash $180,000 on 03/18/2025 for 15%"], ["Schedule P - acquisition", "15% interest acquired 03/18/2025"],
         ["Share of loss (passive, suspended on Form 8582)", BAJA["loss"]], ["Filed with Form 1040 (due with the extended return)", "Yes"]]
f8938 = [["Form 8938 - MFJ living in the US (thresholds: > $100,000 year-end or > $150,000 any time)", "Amount"],
         ["Interest in Baja Coastal Ventures - maximum value 2025 (contribution)", BAJA["contrib"]],
         ["Year-end value (capital account; no appraisal)", BAJA_END_BASIS],
         ["Part IV - excepted specified foreign financial asset: reported on Form 8865 (counts toward the threshold)", "Form 8865"],
         ["FBAR (FinCEN 114)", "Not required - a partnership interest is not a financial account; no signature authority"]]
C.write_return(R, [
    ("Taxpayer / Spouse", "Raymond J. Delgado (XXX-XX-5127) / Carla S. Delgado (XXX-XX-8840)"),
    ("Address", ", ".join(ADDR)),
    ("Filing status", "Married filing jointly (no dependents)"),
    ("Digital assets question", "No"),
    ("Forms included", "1040; Schedules 1, 2, 3, A, B, C, D, E, SE (x2); Forms 4562, 4684 (Sec. B) + IRC 1033 statement, 6198, 6251, 8582, "
                       "8865 (Cat. 3 & 4), 8938, 8960, 8995; K-1 basis worksheets; 704(c)(1)(B) statement; NC D-400"),
    ("Extension", f"Form 4868 accepted 04/15/2026 (${FED_EXT:,.0f} paid); NC D-410 ${NC_EXT:,.0f}"),
    ("Filing method", "E-file federal (incl. Form 8865 in Axcess) and NC (8879 / NC-8879 signed 09/25/2026); refunds direct deposit Truist ****4421"),
], state_summary=[
    {"title": "North Carolina Form D-400 (full-year residents) - 2025",
     "lines": [("6", "Federal adjusted gross income", NC_AGI),
               ("7 / D-400 Sch S", "Addition: 85% of federal bonus depreciation (Carla, $28,000)", NC_ADDBACK),
               ("9", "Deductions from federal AGI", 0),
               ("11", f"NC itemized: mortgage interest + home RE tax capped at $20,000 + charity {CHARITY:,.0f} (> NC standard $25,500)", NC_DED),
               ("14", "NC taxable income", NC_TI), ("15", "NC income tax 4.25%", NC_TAX),
               ("--", "2025 NC estimated payments (4 x 3,800)", sum(a for _, a in NC_ES)), ("--", "Paid with D-410 extension", NC_EXT),
               ("--", "Refund" if NC_REFUND >= 0 else "Tax due", abs(NC_REFUND))],
     "note": f"NC bonus addback recovered as a deduction of 20% ({NC_FUTURE:,}) in each of 2026-2030 (tracking schedule in PERM). "
             "Assumption: NC addback computed on the bonus actually taken federally - verify NC's IRC conformity for OBBBA's 100% bonus."}],
    attachments=[("Schedule C", schc), ("Form 4562", f4562), ("SEP-IRA computation", sep_att),
                 ("K-1 basis / at-risk / passive worksheet", k1_att), ("Form 8582 summary", f8582), ("Form 6251 line 2n support", f6251),
                 ("Schedule E - duplex (January 2025 only)", [["Item", "Amount"]] + [[k, v_] for k, v_ in JAN.items()] +
                  [["Net (passive - suspended on Form 8582)", DUP_NET]]),
                 ("IRC 1033 election / Form 4684", f1033), ("Form 8995 support", qbi_att), ("Form 8865 summary", f8865),
                 ("Form 8938 summary", f8938)])

# =================================================================== ANSWER KEY
cfwd = {"catawba_704d_suspended_loss": CAT_BASIS_SUSP, "catawba_465_at_risk_suspended_loss": CAT_ATRISK_SUSP,
        "passive_regular_suspended_total": -(LAKE["box2"] - LAKE["py_susp_reg"] + BAJA["loss"] + DUP_NET),
        "passive_amt_suspended_total": LAKE_AMT_LOSS + LAKE["py_susp_amt"] - BAJA["loss"] - DUP_NET,
        "lakewood_outside_basis": LAKE_END_BASIS, "catawba_outside_basis": 0, "baja_outside_basis": BAJA_END_BASIS,
        "deferred_1033_gain": GAIN_1033, "nc_bonus_addback_deduction_per_year_2026_2030": NC_FUTURE}
for k, val in cfwd.items():
    R.values[f"{k}_carryforward_2026"] = val
gotchas = [
    gotcha("EVG1023-G1", "Schedules K-1 - partnership loss limitations (Section 6 - apply the limitation)",
           "Catawba ordinary loss: basis first, then at-risk",
           "Deduct the full $52,000 K-1 loss (Axcess default without basis/at-risk inputs), or stop at the basis limit ($30,000).",
           f"Basis {fmt(CAT['beg_basis'])} -> {fmt(CAT_BASIS_ALLOWED)} passes 704(d), {fmt(CAT_BASIS_SUSP)} suspended. At-risk: the $28,000 share of "
           f"the equipment seller's NONRECOURSE note is not at risk (qualified nonrecourse financing is only for real property) -> at-risk "
           f"{fmt(CAT_AT_RISK)}; allowed {fmt(CAT_ALLOWED)}, {fmt(CAT_ATRISK_SUSP)} suspended on Form 6198. Tax effect of taking the full loss: "
           f"{fmt(-LOSS_LIMIT_EFFECT)} understated.", f"Sch E overstated loss {fmt(-CAT['box1'] - CAT_ALLOWED)}", ["8", "13a", "24"], "hard"),
    gotcha("EVG1023-G2", "Schedules K-1 - guaranteed payments / SE", "Guaranteed payments, SE income and basis",
           "Add the $95,000 guaranteed payment to outside basis (so the loss is fully allowed) or compute SE on $95,000 only.",
           f"Guaranteed payments are ordinary income (Sch E nonpassive) and do not increase basis. SE income per K-1 box 14A = GP 95,000 + "
           f"loss share (52,000) = {fmt(CAT['box14a'])} (assumption: the 704(d)/465 limits do not limit SE earnings - follow box 14A). "
           f"SE tax {fmt(se_r['se_tax'])}.", "Sch SE / basis", ["23"], "medium"),
    gotcha("EVG1023-G3", "Form 6251 - K-1 AMT items on limited losses", "Box 17A +6,000 when the loss is limited",
           "Carry the +$6,000 K-1 AMT adjustment to Form 6251 line 2l.",
           "AMT loss (46,000) is subject to the same basis/at-risk limits -> AMT allowed loss $2,000 = regular allowed loss -> line 2n "
           "adjustment $0 and nothing on 2l. Lakewood's +1,200 likewise has no current effect (loss suspended). No AMT in 2025.",
           "AMTI overstated $6,000 (no AMT this year; AMT carryforwards distorted)", ["Form 6251"], "medium"),
    gotcha("EVG1023-G4", "Schedules K-1 - mixing bowl (IRC 704(c)(1)(B)) / footnotes", "Precontribution gain disclosed only in a K-1 footnote",
           "Key boxes 2 and 9a only (box 9a = 0) and miss the gain.",
           f"Land contributed 03/2021 (FMV 400,000, basis 150,000) distributed to another partner 08/14/2025 (< 7 years) -> Raymond recognizes "
           f"{fmt(GAIN_704C)} LTCG (land held for investment; Sch D line 12 with statement) and outside basis +{GAIN_704C:,}. It is NII "
           f"(NIIT applies) and portfolio income - it cannot free passive losses. Tax effect {fmt(GAIN_EFFECT)}.",
           f"Line 7 understated {fmt(GAIN_704C)}", ["7", "23"], "hard"),
    gotcha("EVG1023-G5", "Schedules K-1 - IRC 752(b) deemed distribution", "Liability share dropped 180,000 -> 95,000",
           "Ignore item K changes (basis overstated) or treat the $85,000 decrease as gain.",
           f"Deemed cash distribution {fmt(DEEMED_752)} reduces basis; basis {fmt(LAKE['beg_basis'] + GAIN_704C)} is sufficient -> no IRC 731 gain. "
           f"Ending basis {fmt(LAKE_END_BASIS)}.", "Basis tracking", ["K-1 worksheet"], "medium"),
    gotcha("EVG1023-G6", "Schedules K-1 - passive activities (new client carryovers)", "Prior-year unallowed losses - Regular vs AMT",
           "Enter one PY carryover ($31,000) for both regular and AMT, or omit it (new client - no proforma); or allow the $25,000 "
           "special allowance for the LP and the duplex.",
           f"Limited partner -> no $25,000 allowance; MAGI {fmt(v['11'])} > $150,000 anyway. All passive losses suspended: regular "
           f"{fmt(cfwd['passive_regular_suspended_total'])}, AMT {fmt(cfwd['passive_amt_suspended_total'])} carried to 2026.",
           "Form 8582 carryforwards", ["8", "Form 8582"], "medium"),
    gotcha("EVG1023-G7", "Involuntary conversion (IRC 1033) / Schedule E", "Fire-destroyed rental: deferral election and replacement deadline",
           f"Report the {fmt(GAIN_1033)} gain (Form 4684/4797) or calculate the deadline as 2 years after the fire (01/24/2027 - adjuster's view / "
           "original workbook formula); or treat the fire as a disposition that frees the duplex's passive loss.",
           f"Elect IRC 1033 - postpone the entire gain (statement attached); replacement period ends {DEADLINE} (2 years after the close of the "
           "first tax year the gain was realized). Basis of replacement = cost less deferred gain. Schedule E for January only: rents net of "
           f"refunds, expenses and half-month depreciation -> {fmt(DUP_NET)} (passive, suspended - not a fully taxable disposition).",
           f"Line 7/8 overstated {fmt(GAIN_1033)} if not elected", ["7", "8", "Form 4684"], "hard"),
    gotcha("EVG1023-G8", "Foreign Transactions - foreign partnership (Form 8865) / Form 8938 / FBAR", "Cash contribution to a Mexican partnership",
           "Report the Baja loss and nothing else; or file Form 926 / FBAR.",
           "Form 8865 Category 3 (6038B: > $100,000 contributed) and Category 4 (6046A: 10%+ acquired), Schedules O and P; passive loss "
           "suspended. Form 8938 required (MFJ thresholds); interest listed as excepted asset reported on 8865. No FBAR (not a financial "
           "account). ProConnect cannot produce 8865 -> paper filing if prepared there (firm e-filed from Axcess).",
           "Penalties $10,000+ per form if omitted", ["Form 8865", "Form 8938"], "hard"),
    gotcha("EVG1023-G9", "Schedule C - depreciation (OBBBA) / SALT state conformity", "Bonus rate and NC addback",
           f"Use the bookkeeper's 40% bonus ({fmt(BOOK_DEP)} depreciation) and/or forget the NC addback.",
           f"Assets acquired 03-06/2025 (after 01/19/2025) -> 100% bonus ({fmt(BONUS)}). NC: add back 85% = {fmt(NC_ADDBACK)} on D-400 "
           f"Schedule S; deduct {fmt(NC_FUTURE)} in each of 2026-2030. SEP max {fmt(SEP)} funded 09/08/2026.",
           "Sch C / NC taxable income", ["8", "10", "NC D-400"], "medium"),
]
C.write_answer_key(R, {"residence": "NC (Charlotte)", "new_client": True,
                       "complexity": "3 partnerships (basis/at-risk/passive/704(c)/752), Form 8865, IRC 1033, Sch C"}, gotchas,
                   state=[{"jurisdiction": "NC D-400", "federal_agi": NC_AGI, "bonus_addback": NC_ADDBACK, "deduction": NC_DED,
                           "deduction_type": "NC itemized" if NC_ITEM > NC_STD else "NC standard", "taxable_income": NC_TI, "tax": NC_TAX,
                           "payments": NC_PAY, "refund": NC_REFUND}],
                   filings=[{"form": "Form 4868", "filed": "2026-04-15", "payment": FED_EXT},
                            {"form": "Form 1040 (with Forms 8865, 8938, 1033 statement)", "method": "e-file (Axcess)", "due": "2026-10-15",
                             "filed": "2026-09-28"},
                            {"form": "NC D-400", "method": "e-file", "due": "2026-10-15", "filed": "2026-09-28"},
                            {"form": "FinCEN 114", "method": "not required"}],
                   extra={"gain_704c1b": GAIN_704C, "deemed_distribution_752b": DEEMED_752, "catawba": {"basis_allowed": CAT_BASIS_ALLOWED,
                          "at_risk": CAT_AT_RISK, "allowed": CAT_ALLOWED, "basis_suspended": CAT_BASIS_SUSP, "at_risk_suspended": CAT_ATRISK_SUSP,
                          "amt_line_2n": CAT_2N}, "duplex_1033": {"proceeds": DUP["proceeds"], "adjusted_basis": ADJ_BASIS, "gain_deferred": GAIN_1033,
                          "deadline": DEADLINE}, "nii": NII, "sep": SEP, "nc_bonus_addback": NC_ADDBACK})

C.write_receipt_log("EVG1023-1040-2025", "T. Alvarez (senior staff)", "M. Osei (manager)", "S. Kennedy, CPA", "2026-02-03",
                    extension="Federal 4868 e-filed 04/14/2026, accepted 04/15/2026, $15,000 paid; NC D-410 $3,000")

C.write_notes(f"""
# EVG1023 - Delgado, Raymond & Carla - 2025 Form 1040 - Preparer Notes

*Synthetic client - Project Evergreen. NEW CLIENT. Return status: **signed off; federal (with Forms 8865/8938) and NC D-400 e-filed 09/28/2026 (extended), accepted.***

## Return summary
| | |
|---|---|
| Filing status | Married filing jointly |
| Schedule C (Carla) | {fmt(SCHC_NET)} |
| Schedule E | {fmt(SCH_E)} (Catawba guaranteed payments {fmt(CAT['gp'])} less allowed loss {fmt(CAT_ALLOWED)}; all passive losses suspended) |
| Capital gain (line 7) | {fmt(v['7'])} (IRC 704(c)(1)(B) gain - Lakewood) |
| Interest / dividends | {fmt(v['2b'])} / {fmt(v['3b'])} |
| Adjustments | half SE {fmt(se_r['half'] + se_c['half'])} + SEP {fmt(SEP)} |
| AGI | {fmt(v['11'])} |
| Itemized deductions | {fmt(v['12e'])} |
| QBI deduction | {fmt(v['13a'])} |
| Taxable income | {fmt(v['15'])} |
| Tax / SE tax / NIIT | {fmt(v['16'])} / {fmt(se_r['se_tax'] + se_c['se_tax'])} / {fmt(v.get('niit', 0))} |
| Total tax | {fmt(v['24'])} |
| Payments (estimates {fmt(v['26'])} + extension {fmt(FED_EXT)}) | {fmt(v['33'])} |
| **Federal {'refund' if v['refund'] else 'balance due'}** | **{fmt(v['refund'] or v['balance_due'])}** |
| NC D-400 | tax {fmt(NC_TAX)}; **{'refund' if NC_REFUND >= 0 else 'due'} {fmt(abs(NC_REFUND))}** |

## What I did and why (plain English)
1. **Catawba River Outfitters (Raymond, 40% member-manager).** He works in the business (material participation) - nonpassive.
   The K-1 shows guaranteed payments {fmt(CAT['gp'])} and an ordinary loss {fmt(CAT['box1'])}. Three tests, in order:
   - *Basis (IRC 704(d)):* beginning basis {fmt(CAT['beg_basis'])} (prior preparer's worksheet: capital 2,000 + 40% share of the equipment
     seller note 28,000). Guaranteed payments do **not** add to basis - they're paid to him in cash. Allowed {fmt(CAT_BASIS_ALLOWED)};
     **{fmt(CAT_BASIS_SUSP)} suspended** for basis.
   - *At-risk (IRC 465, Form 6198):* the seller note is nonrecourse and secured only by equipment. Only *real-property* financing can be
     "qualified nonrecourse financing", so the $28,000 is not at risk. At-risk = {fmt(CAT_AT_RISK)} -> allowed **{fmt(CAT_ALLOWED)}**,
     {fmt(CAT_ATRISK_SUSP)} suspended under 465 (basis is still reduced by the full {fmt(CAT_BASIS_ALLOWED)} -> ending basis $0).
   - *Passive:* not applicable (material participation).
   Schedule E: {fmt(CAT['gp'])} - {fmt(CAT_ALLOWED)} = {fmt(SCH_E)}. Taking the whole loss would have understated tax by {fmt(-LOSS_LIMIT_EFFECT)}.
2. **SE tax - Raymond.** Box 14A {fmt(CAT['box14a'])} (= GP + loss share). *Position/assumption:* SE earnings follow the distributive share as
   reported (IRC 1402(a) refers to the 702(a)(8) share; the 704(d)/465 limits apply to income tax) - we followed box 14A. SE tax {fmt(se_r['se_tax'])}.
3. **AMT (box 17A +$6,000).** The AMT loss would be 46,000, but the same basis/at-risk limits apply under AMT -> AMT allowed loss is also
   {fmt(CAT_AMT_ALLOWED)}, so Form 6251 line 2n = **$0** and the 17A amount is not carried to line 2l. Same for Lakewood's 17A (loss suspended).
   Form 6251: no AMT.
4. **Lakewood Partners (10% limited partner).** The K-1 face shows only the rental loss. **Footnote 3** says the parcel Raymond contributed in
   03/2021 (FMV $400,000, basis $150,000) was distributed to another partner on 08/14/2025 - within 7 years -> IRC 704(c)(1)(B): Raymond
   recognizes the remaining built-in gain **{fmt(GAIN_704C)}** as long-term capital gain (land held for investment; Sch D line 12 with a
   statement) and adds it to his outside basis. His share of the partnership's debt fell 180,000 -> 95,000: a **{fmt(DEEMED_752)} deemed
   distribution** (IRC 752(b)), covered by basis -> no gain. Ending basis {fmt(LAKE_END_BASIS)}.
5. **Passive losses (new client).** Lakewood is a limited partnership interest: no $25,000 rental allowance - and MAGI is far over $150,000.
   The prior preparer's 8582 shows Lakewood unallowed losses **Regular $31,000 / AMT $27,500** - entered separately. The 704(c) gain is
   portfolio income (investment land), not passive income, so it does not free any losses. Baja's loss {fmt(BAJA['loss'])} and the duplex's
   January loss {fmt(DUP_NET)} are passive too. Everything is suspended: Regular {fmt(cfwd['passive_regular_suspended_total'])}, AMT
   {fmt(cfwd['passive_amt_suspended_total'])} carried to 2026.
6. **Duplex fire (IRC 1033).** Building destroyed 01/24/2025; insurance {fmt(DUP['proceeds'])} received 05/16/2025. Adjusted basis
   {fmt(ADJ_BASIS)} (cost $290,000 less depreciation {fmt(ACCUM_DEP)} incl. a half month in January) -> realized gain **{fmt(GAIN_1033)}**.
   Raymond confirmed they will rebuild (Belk Homes quote ~$465,000) or buy another rental -> election to postpone the whole gain; statement
   attached to Form 4684. **Deadline 12/31/2027** - two years after the close of 2025, the first year any gain was realized (not "two
   years from the fire" as the adjuster said; not three years - that is for condemnations). If they spend less than $410,000 the
   shortfall is taxable (amend 2025); replacement basis = cost less the deferred gain. Schedule E covers January only (rent less the
   refund to tenants, expenses, half-month depreciation = {fmt(DUP_NET)}); the fire with a 1033 deferral is not a fully taxable
   disposition, so the passive loss stays suspended. The rest of the 2025 county tax on the lot ({fmt(DUP_LAND_TAX)}) is a Schedule A tax
   (land held for the rebuild).
7. **Baja Coastal Ventures (Mexico).** Elected partnership (Form 8832, 2019). Raymond wired $180,000 for 15% -> **Form 8865 Category 3**
   (cash contribution > $100,000) **and Category 4** (acquired 10%+), Schedules O and P. Share of loss {fmt(BAJA['loss'])} per Baja's U.S.
   adviser letter - passive, suspended. **Form 8938** required (MFJ: > $100,000 at year-end or > $150,000 at any time); the interest is
   listed in Part IV as reported on Form 8865. No FBAR - a partnership interest is not a financial account and Raymond has no signature
   authority. Firm decision: prepared and e-filed in Axcess with Form 8865 included (ProConnect cannot produce Form 8865 - would have
   required paper filing with the 8865 prepared outside).
8. **Carla - Schedule C.** Gross receipts {fmt(SCHC_GROSS)} (reconciled: 1099-NECs + Square 1099-K + checks), COGS {fmt(SCHC_COGS)}. Jen
   (bookkeeper) used 40% bonus - that phase-down rate only applies to property acquired before 01/20/2025. All three purchases were
   made 03-06/2025 -> **100% bonus** {fmt(BONUS)} (OBBBA). Net profit {fmt(SCHC_NET)}; SE tax {fmt(se_c['se_tax'])}; SEP max {fmt(SEP)} (20% of net
   earnings after half SE tax) funded 09/08/2026.
9. **QBI.** Taxable income before QBI is under $394,600 -> 20% x QBI: Carla {fmt(QBI_C)} (after half SE and SEP); Catawba {fmt(QBI_CAT)} (allowed
   loss less half of Raymond's SE tax - conservative assumption; guaranteed payments are never QBI) -> {fmt(v['13a'])}.
10. **NIIT.** NII = 704(c) gain + interest + dividends = {fmt(NII)}; MAGI over $250,000 is smaller ({fmt(v['11'] - 250000)}) -> NIIT {fmt(v.get('niit', 0))}.
11. **Itemized.** NC income tax paid in 2025 {fmt(SALT_INC)} (3 estimates + 2024 balance) + home RE tax {fmt(HOME_RE_TAX)} + lot tax
    {fmt(DUP_LAND_TAX)} = SALT under the $40,000 cap (MAGI < $500,000); mortgage {fmt(MORT_INT)}; charity {fmt(CHARITY)} -> {fmt(v['12e'])}.
12. **Estimates.** 4 x $16,000 = $64,000 >= 110% of 2024 tax ({fmt(r(PY['tax'] * 1.1))}) paid evenly -> no Form 2210 penalty.
13. **North Carolina.** AGI + 85% bonus addback {fmt(NC_ADDBACK)} - NC itemized {fmt(NC_DED)} (mortgage + home property tax capped at $20,000
    + charity; beats the $25,500 NC standard deduction) = {fmt(NC_TI)} x 4.25% = {fmt(NC_TAX)}. NC deductions of {fmt(NC_FUTURE)}/year 2026-2030 set up
    in PERM. *Assumption:* NC addback measured on the bonus taken federally - confirm NC's conformity to OBBBA's 100% bonus.

## Open items / carryforwards to 2026
- Catawba: 704(d) suspended {fmt(CAT_BASIS_SUSP)}; 465 suspended {fmt(CAT_ATRISK_SUSP)}; basis $0, at-risk $0. Any 2026 recourse debt guaranty or
  contribution would change this - ask Raymond.
- Passive suspended: Regular {fmt(cfwd['passive_regular_suspended_total'])} / AMT {fmt(cfwd['passive_amt_suspended_total'])} (by activity in WP).
- **1033 tickler: replacement by 12/31/2027** - calendar reminder set; track cost vs $410,000.
- Form 8865 again for 2026 if Category 3/4 events occur; Category 3 continues for contributed property only in the year of transfer.
- NC bonus addback recovery schedule 2026-2030 ({fmt(NC_FUTURE)}/yr).

## Hand-off to signer / routing
- [x] Return locked; Accountant's Copy saved as *reviewed*
- [x] Federal 1040 (extended) incl. Forms 8865 and 8938 - e-file (Axcess); due 10/15/2026
- [x] NC D-400 (extended) - e-file; due 10/15/2026
- [x] FBAR: not required (documented)
- [x] eSign (8879 / NC-8879) - Carla preferred contact
- Billing: quote $5,500; Lakewood K-1 arrived 08/21/2026 and Baja letter 07/30/2026 - both more than 15 days before 10/15, no expedite fee.
  Extra 2 hrs for the 704(c)(1)(B) footnote research (client-chargeable).
""")
C.write_review_points(f"""
# Review Points - EVG1023 - 2025 - Form 1040

*Reviewer: M. Osei (blue). Preparer responses in red. Synthetic.*

1. **K-1 Catawba** - Draft deducted the full ($52,000). Apply Section 6 basis limitation and Form 6198.
   - *Preparer: Basis allows 30,000; seller note is nonrecourse equipment debt (not QNF) -> at-risk 2,000. Allowed {fmt(CAT_ALLOWED)}.*
   - 1a. Don't add the guaranteed payments to basis.
   - *Preparer: Removed - basis worksheet attached.*
2. **Form 6251** - Line 2l shows +6,000 from box 17A. The loss is limited - recompute under AMT (line 2n).
   - *Preparer: AMT allowed loss also 2,000 -> 2n = 0; 2l removed.*
3. **K-1 Lakewood - footnote 3** - 704(c)(1)(B) gain of $250,000 is missing. Also item K: liabilities dropped $85,000.
   - *Preparer: Added to Sch D line 12 with statement; basis +250,000 and 752(b) deemed distribution 85,000 - no gain.*
4. **Form 8582** - Draft had no PY carryover (new client) and gave the duplex a $25k allowance. Enter Regular 31,000 / AMT 27,500.
   - *Preparer: Done; MAGI > $150k - $0 allowance; all suspended.*
5. **Form 4797/4684** - Draft recognized the duplex gain and checked "disposed of activity". Client is replacing - elect 1033;
   confirm the deadline.
   - *Preparer: 1033 statement attached; deadline 12/31/2027 (tab 21 corrected formula); disposal box unchecked.*
6. **Foreign** - Baja: 8865 Cat 3 & 4 and 8938. Confirm FBAR position.
   - *Preparer: Prepared in Axcess; no FBAR (not a financial account). Documented ProConnect limitation in the workbook.*
7. **Schedule C / 4562** - Bookkeeper's 40% bonus - assets acquired after 01/19/2025 get 100%. NC addback?
   - *Preparer: 100% bonus {fmt(BONUS)}; NC addback {fmt(NC_ADDBACK)} (tab 6).*
8. FYI - SEP amount confirmed with Carla before funding (09/08).
""")
print("EVG1023 done", v["11"], v["15"], v["24"], v["refund"], v["balance_due"], "NC", NC_TAX, NC_REFUND, "gain", GAIN_1033, ADJ_BASIS)
