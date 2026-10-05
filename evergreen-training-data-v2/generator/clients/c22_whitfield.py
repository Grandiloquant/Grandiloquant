"""EVG1022 - Gregory & Ellen Whitfield (MFJ, Pennsylvania - West Chester). NEW CLIENT (first year with Evergreen).
Mobile sales executive retires 08/29/2025: single PA-coded W-2 but workdays in PA/NJ/MA/IL (calendar export) ->
NJ reciprocity (no NJ return), Illinois 30-day nonresident-employee threshold (no IL return), Massachusetts
nonresident Form 1-NR/PY on a workday allocation, PA resident credit (Schedule G-L) limited to PA tax on the MA wages;
401(k) lump-sum distribution with employer stock in kind (NUA - only cost basis taxable) + direct rollover of the rest;
cross-account wash sale (Gregory's taxable account -> Ellen's IRA, Rev. Rul. 2008-5: loss permanently disallowed);
bond premium (box 11/13) and accrued interest paid at purchase; prior preparer's capital loss carryover carried with the
wrong character (all long-term); SALT cap phase-down to the $10,000 floor; NIIT; Additional Medicare."""
import datetime as dt

from common import ClientBuild, gotcha, fmt
from docs import statement, scanned_pages, write_text, write_xlsx
import forms as F
from tax2025 import Return1040, r

C = ClientBuild("EVG1022", "Whitfield", "Gregory & Ellen Whitfield")
ADDR = ("1418 Brandywine Hunt Dr", "West Chester, PA 19382")
T = {"name": "Gregory A. Whitfield", "ssn": "XXX-XX-6618", "dob": "1967-06-21"}
S = {"name": "Ellen M. Whitfield", "ssn": "XXX-XX-2274", "dob": "1969-02-09"}
REC_T = [T["name"], *ADDR, f"TIN: {T['ssn']}"]
REC_S = [S["name"], *ADDR, f"TIN: {S['ssn']}"]
REC_J = ["Gregory A. Whitfield & Ellen M. Whitfield JTWROS", *ADDR, f"TIN: {T['ssn']}"]
SCHWAB = ["Charles Schwab & Co., Inc.", "211 Main St", "San Francisco, CA 94105", "TIN: 00-1737782"]
FID = ["Fidelity Management Trust Company, Trustee", "Keystone Medical Devices 401(k) Savings Plan", "245 Summer St, Boston, MA 02210",
       "TIN: 00-6110482"]

# =================================================================== facts (all amounts in one place)
# --- W-2s
G_W2 = {"1": 410000.00, "2": 98400.00, "3": 176100.00, "4": 10918.20, "5": 441000.00, "6": 8563.50,
        "12": [("D", 31000.00), ("C", 1242.00), ("DD", 22800.00)], "13": ["Retirement plan: X"],
        "14": [("PA UC", 308.70), ("SEVERANCE/PTO PAYOUT incl. box 1", 38500.00)], "control": "KMD-77104",
        "state": [{"state": "PA", "id": "00-6612480-PA", "wages": 441000.00, "tax": 13538.70}],
        "local": [{"wages": 441000.00, "tax": 4410.00, "name": "W CHESTER BORO EIT"}]}
E_W2 = {"1": 62000.00, "2": 5200.00, "3": 65000.00, "4": 4030.00, "5": 65000.00, "6": 942.50,
        "12": [("E", 3000.00), ("DD", 9600.00)], "13": ["Retirement plan: X"], "control": "BVSD-1187",
        "state": [{"state": "PA", "id": "00-2209177-PA", "wages": 65000.00, "tax": 1995.50}],
        "local": [{"wages": 65000.00, "tax": 650.00, "name": "W CHESTER BORO EIT"}]}
PA_COMP = G_W2["state"][0]["wages"] + E_W2["state"][0]["wages"]          # PA compensation includes 401(k)/403(b) deferrals
PA_WH = G_W2["state"][0]["tax"] + E_W2["state"][0]["tax"]

# --- workday log (calendar export). Holidays/PTO excluded from workdays.
HOLIDAYS = {dt.date(2025, 1, 1): "Company holiday - New Year's Day", dt.date(2025, 4, 18): "Company holiday - Good Friday",
            dt.date(2025, 5, 26): "Company holiday - Memorial Day", dt.date(2025, 7, 4): "Company holiday - Independence Day"}
PTO = {dt.date(2025, 3, 14): "PTO", dt.date(2025, 7, 3): "PTO", dt.date(2025, 7, 7): "PTO", dt.date(2025, 8, 15): "PTO - retirement paperwork"}
def _days(m, ds): return [dt.date(2025, m, x) for x in ds]
TRIPS = {
    "MA": [(_days(2, [11, 12, 13]), "Boston, MA", "Mass General Brigham - capital equipment review"),
           (_days(3, [25, 26, 27, 28]), "Boston / Burlington, MA", "New England region launch; Lahey Hospital"),
           (_days(5, [13, 14, 15]), "Worcester, MA", "UMass Memorial - contract negotiation"),
           (_days(6, [17, 18, 19]), "Boston, MA", "Boston Children's / Beth Israel QBRs"),
           (_days(7, [22, 23, 24, 25]), "Cambridge / Boston, MA", "New England sales team offsite + handoff to successor"),
           (_days(8, [6]), "Springfield, MA", "Baystate Health - final account handoff")],
    "IL": [(_days(1, [28, 29, 30]), "Chicago, IL", "National sales kickoff (McCormick Place)"),
           (_days(4, [8, 9, 10, 11]), "Chicago, IL", "AAMI-type trade conference booth + customer dinners"),
           (_days(6, [3, 4, 5]), "Chicago / Oak Brook, IL", "Midwest GPO contract renewal"),
           (_days(8, [19, 20, 21]), "Chicago, IL", "Transition meetings - Midwest accounts")],
    "NJ": [(_days(1, [9, 16, 23]) + _days(2, [6, 20, 27]) + _days(3, [6, 20]) + _days(4, [3, 24]) + _days(5, [1, 8, 22, 29]) +
            _days(6, [12, 26]) + _days(7, [10, 17, 31]) + _days(8, [7, 14, 28]), "New Brunswick / Princeton / Camden, NJ",
            "Day trip - NJ hospital system accounts (RWJBarnabas, Penn Medicine Princeton, Cooper)")],
}
LOG, COUNT = [], {"PA": 0, "NJ": 0, "MA": 0, "IL": 0}
day_state = {}
for st, trips in TRIPS.items():
    for ds, city, act in trips:
        for x in ds:
            day_state[x] = (st, city, act)
x = dt.date(2025, 1, 1)
while x <= dt.date(2025, 8, 29):
    if x.weekday() < 5:
        if x in HOLIDAYS or x in PTO:
            LOG.append([x.isoformat(), x.strftime("%a"), "", "", (HOLIDAYS.get(x) or PTO.get(x)), "No"])
        else:
            st, city, act = day_state.get(x, ("PA", "King of Prussia, PA (HQ) / home office West Chester",
                                              "Office / internal meetings / calls"))
            COUNT[st] += 1
            LOG.append([x.isoformat(), x.strftime("%a"), st, city, act, "Yes"])
    x += dt.timedelta(days=1)
TOT_WD = sum(COUNT.values())
assert (TOT_WD, COUNT["PA"], COUNT["NJ"], COUNT["MA"], COUNT["IL"]) == (165, 112, 22, 18, 13), (TOT_WD, COUNT)
MA_PCT = COUNT["MA"] / TOT_WD
MA_WAGES = r(G_W2["1"] * MA_PCT)                         # MA-source wages (830 CMR 62.5A.1 workday method)
IL_WAGES_IF_SOURCED = r(G_W2["1"] * COUNT["IL"] / TOT_WD)

# --- 401(k) lump-sum distribution (separation from service 08/29/2025, age 58)
NUA_SH, NUA_FMV_SH, NUA_COST_SH = 8000, 80.00, 12.00
NUA_BOX1 = NUA_SH * NUA_FMV_SH                  # 640,000
NUA_BOX2A = NUA_SH * NUA_COST_SH                # 96,000 (plan's cost basis of the employer stock)
NUA_BOX6 = NUA_BOX1 - NUA_BOX2A                 # 544,000
ROLLOVER = 780000.00

# --- interest / bonds (Schwab joint ****2207)
PFE_FACE, PFE_PRICE, PFE_CPN = 200000, 104.25, .0475
PFE_PREMIUM = r(PFE_FACE * (PFE_PRICE - 100) / 100)          # 8,500
ACCRUED_DAYS = 113                                            # 30/360: 11/19/2024 -> 03/12/2025
ACCRUED_PAID = round(PFE_FACE * PFE_CPN * ACCRUED_DAYS / 360, 2)   # 2,981.94
PFE_COUPONS = PFE_FACE * PFE_CPN                              # 9,500 (05/19 + 11/19)
SWEEP_INT = 3140.55
SCHWAB_BOX1 = round(PFE_COUPONS + SWEEP_INT, 2)
BOX11_ABP = 786.12
MUNI_FACE, MUNI_INT, BOX13_PREM = 150000, 7500.00, 1104.30
TAX_EXEMPT = round(MUNI_INT - BOX13_PREM, 2)
BFCU_INT = 212.40
# --- dividends
DIV_JOINT = [("Procter & Gamble Co (PG) - until 04/03 sale", 1680.00, 1680.00), ("Vanguard Total Stock Market ETF (VTI)", 2110.00, 2110.00),
             ("Vanguard Total International Stock ETF (VXUS)", 3960.00, 2310.00), ("Schwab US Dividend Equity ETF (SCHD)", 6500.00, 6500.00)]
DIV_GREG = [("iShares Core S&P 500 ETF (IVV) - until 11/10 sale", 2870.00, 2020.00),
            ("Keystone Medical Devices Inc (KMDV) - NUA shares, Q4 dividend", 1280.00, 1280.00)]
def tot(rows, i): return round(sum(x[i] for x in rows), 2)
# --- sales
TRADES = [
    dict(id="1", box="A", desc="120 sh Eli Lilly & Co (LLY) [Gregory ****4410]", acq="01/22/2025", sold="06/30/2025", proceeds=95400.00,
         basis=90400.00),
    dict(id="2", box="A", desc="400 sh iShares Core S&P 500 ETF (IVV) [Gregory ****4410]", acq="02/19/2025", sold="11/10/2025",
         proceeds=227000.00, basis=245000.00, code="W", adj=18000.00,
         note="Wash sale - 420 sh IVV bought 11/20/2025 in Ellen's Schwab IRA ****8831 (Rev. Rul. 2008-5; spouse - Pub. 550). "
              "Not flagged by Schwab (box 1g blank)."),
    dict(id="3", box="D", desc="400 sh Procter & Gamble Co (PG) [joint ****2207]", acq="05/14/2014", sold="04/03/2025", proceeds=66400.00,
         basis=31200.00),
    dict(id="4", box="D", desc="300 sh Vanguard Total Stock Market ETF (VTI) [joint ****2207]", acq="03/09/2017", sold="09/22/2025",
         proceeds=92100.00, basis=67300.00),
]
WASH_LOSS = 18000.00
IRA_BUY_SH, IRA_BUY_PX = 420, 571.20
# --- prior year (2024, prior preparer) and carryover
PY = {"agi": 669300, "tax": 164982, "st": -29000, "lt": -12000, "l16": -41000, "l21": -3000}
CO_WRONG = {"st": 0, "lt": 38000}
CO_RIGHT = {"st": 26000, "lt": 12000}          # ST absorbs the $3,000 first (Capital Loss Carryover Worksheet)
assert CO_RIGHT["st"] == -PY["st"] - 3000 and CO_RIGHT["lt"] == -PY["lt"]
# --- itemized / payments
PA_PY_BAL = 410.00                       # 2024 PA-40 balance paid 04/15/2025
LOCAL_EIT = G_W2["local"][0]["tax"] + E_W2["local"][0]["tax"]
RE_TAX = {"Chester County + West Goshen Twp 2025": 2350.00, "West Chester Area School District 2025-26": 7480.00}
MORT_INT = 11240.00
CHARITY = [("Church of the Holy Trinity, West Chester", 9000.00), ("Chester County Food Bank", 4000.00),
           ("Penn State Brandywine - scholarship fund", 2000.00)]
FED_ES = [("04/15/2025", 8000.00), ("06/16/2025", 8000.00), ("09/15/2025", 8000.00), ("01/15/2026", 8000.00)]
FED_EXT = 3000.00
PA_EXT, MA_EXT = 1000.00, 2300.00

# =================================================================== PERM
C.write_profile(f"""
# EVG1022 - Whitfield, Gregory & Ellen  (PERM)

*Synthetic client - Project Evergreen training data.*

| Item | Detail |
|---|---|
| Client ID | EVG1022 |
| Taxpayer | Gregory A. Whitfield, DOB 06/21/1967, SSN XXX-XX-6618 - SVP Sales, Keystone Medical Devices, Inc. (HQ King of Prussia PA); **retired 08/29/2025** (age 58) |
| Spouse | Ellen M. Whitfield, DOB 02/09/1969, SSN XXX-XX-2274 - school nurse, Brandywine Valley School District (W-2) |
| Address | {ADDR[0]}, {ADDR[1]} (Chester County; West Goshen Twp / West Chester Area SD) - PA residents all years |
| Dependents | None (two adult children, independent) |
| Contact | Gregory - greg.whitfield@example.com, (610) 555-0182; prefers email + one call before filing; eSign OK |
| Engagement | **New client 2025** (referred by Keystone's CFO, existing client). Quote $4,800 (complex - NUA, multi-state, investments); MA nonresident return $450 |
| Prior preparer | Brandywine Tax Services (2019-2024) - copies of 2024 federal/PA returns provided at intake (PERM) |
| Payment info | Voided check on file (PNC checking ****7720) |

## Intake notes (new-client interview 02/10/2026)
- Gregory covered the Mid-Atlantic, then also New England (from 01/2025) and Midwest key accounts; heavy travel Jan-Aug 2025.
  Keystone payroll coded 100% of wages to PA. He keeps his work calendar in Outlook - asked for an export by state.
- Retired 08/29/2025; took his whole 401(k) in September: company stock "in kind" to Schwab, the rest rolled to a Fidelity IRA
  (Fidelity's retirement planner recommended the "NUA strategy"). Has not sold any of the company stock.
- No MA/IL/NJ returns ever filed. MA travel started with the New England assignment in 01/2025 (none in 2024 per Gregory).
- Prior preparer's 2024 return shows a capital loss carryover - copy of their carryover worksheet in PERM.
""")
F.prior_year_summary(C.perm_file("2024_Form_1040_Return_Summary.pdf", "Prior-year return summary (prior preparer)"),
    "Gregory & Ellen Whitfield", "EVG1022", "Married filing jointly", [
        ["1a", "W-2 wages (Keystone Medical Devices $590,000; Brandywine Valley SD $61,000)", 651000],
        ["2b", "Taxable interest (Schwab, BFCU)", 5200], ["3a / 3b", "Qualified / ordinary dividends", "14,000 / 16,100"],
        ["7", "Capital loss (Sch D line 21) - line 16 net loss (41,000): ST (29,000) / LT (12,000)", PY["l21"]],
        ["11", "AGI", PY["agi"]], ["12", "Itemized deductions (SALT limited to $10,000)", 33800], ["15", "Taxable income", 635500],
        ["24", "Total tax (incl. Additional Medicare and NIIT)", PY["tax"]], ["35a", "Refund", 2210]],
    carryovers=[["Capital loss carryover to 2025 - per prior preparer's worksheet ('long-term')", 38000],
                ["Charitable contribution carryover", 0], ["PA-40 2024: PA tax / withholding / balance due", "19,986 / 19,576 / 410"]],
    notes="Prepared from the copy of the 2024 return Brandywine Tax Services provided. The prior preparer's Capital Loss Carryover "
          "Worksheet is reproduced separately in PERM (scan). Evergreen has not yet verified any carryover.")
scanned_pages(C.perm_file("2024_Prior_Preparer_Sch_D_and_Carryover_Worksheet_scan.pdf", "Prior preparer workpaper (scan)"),
    [["Brandywine Tax Services            2024 Form 1040 - Schedule D (excerpt)",
      "Client: Gregory A. & Ellen M. Whitfield          MFJ",
      "",
      "Part I  Short-term",
      "  1b  Box A totals    proceeds 184,220   cost 213,220      (29,000)",
      "  7   Net short-term capital gain or (loss) ............ (29,000)",
      "Part II Long-term",
      "  8b  Box D totals    proceeds  61,400   cost  73,400      (12,000)",
      "  15  Net long-term capital gain or (loss) ............. (12,000)",
      "Part III",
      "  16  Combine lines 7 and 15 ............................ (41,000)",
      "  21  Loss allowed (smaller of line 16 or $3,000) ........  (3,000)",
      "",
      "CAPITAL LOSS CARRYOVER WORKSHEET - to 2025",
      "  Total loss (41,000) less allowed (3,000) = 38,000",
      "  Carryover to 2025:   Short-term ______0______",
      "                       Long-term   ___38,000___",
      "  Prepared by: K.L.  03/28/2025"]], handwritten=False, skew=1.1, seed=221)

# =================================================================== PBC
F.engagement_letter(C.pbc_file("00_Engagement_Letter_signed.pdf", "Engagement letter (signed)", "2026-02-10"), "Gregory & Ellen Whitfield",
    "EVG1022", "Quoted fee $4,800 for the federal and Pennsylvania returns; $450 for each nonresident state return.", "02/10/2026",
    "2025 Form 1040, PA-40, and any nonresident state returns required by Gregory's 2025 work travel.")
F.organizer(C.pbc_file("01_2025_Organizer_completed.pdf", "Client organizer", "2026-02-24"), "Gregory & Ellen Whitfield", "EVG1022",
    general=[("Did your marital status change during 2025?", "No", ""),
             ("Did you work in any state other than your home state?", "Yes", "Travelled a lot - NJ, Boston, Chicago. Employer withheld PA only"),
             ("Did you retire or change jobs?", "Yes", "Greg retired 8/29/2025"),
             ("Did you receive distributions from retirement plans?", "Yes", "401k - stock to Schwab, rest rolled to Fidelity IRA"),
             ("Did you sell any securities?", "Yes", "See Schwab"),
             ("Did you buy or sell bonds?", "Yes", "Pfizer bond in March"),
             ("Do you have capital loss carryovers?", "Yes", "Per last year's return ($38,000)"),
             ("Did you make estimated tax payments?", "Yes", "Fed 4 x 8,000"),
             ("Did you receive, sell, exchange digital assets?", "No", ""),
             ("Foreign accounts / foreign trusts?", "No", "")],
    dependents=[],
    income_rows=[["Wages", "Keystone Medical Devices (Gregory)", 590000, "see W-2"],
                 ["Wages", "Brandywine Valley SD (Ellen)", 61000, "see W-2"],
                 ["Interest", "Charles Schwab - joint", 4990, "see 1099"],
                 ["Interest", "Brandywine Federal Credit Union", 210, "212"],
                 ["Dividends", "Charles Schwab", 16100, "see 1099"],
                 ["Retirement distributions", "", 0, "Fidelity 401k - see 1099-R"],
                 ["Capital gains/losses", "Charles Schwab", -41000, "gains this year"]],
    deductions_rows=[["Mortgage interest", "PNC Mortgage", 12100, "see 1098"],
                     ["Real estate taxes", "County/twp + school", 9500, "9,830"],
                     ["Charitable contributions", "Church, food bank, PSU", 13500, "15,000"],
                     ["Federal estimated payments", "", 0, "32,000"]],
    signature_date="02/22/2026")

EMP_G = {"name": "Keystone Medical Devices, Inc.", "addr1": "1000 First Ave", "addr2": "King of Prussia, PA 19406", "ein": "00-6612480"}
EMP_E = {"name": "Brandywine Valley School District", "addr1": "200 Lenape Rd", "addr2": "West Chester, PA 19382", "ein": "00-2209177"}
EE_G = {"name": T["name"], "addr1": ADDR[0], "addr2": ADDR[1], "ssn": T["ssn"]}
EE_E = {"name": S["name"], "addr1": ADDR[0], "addr2": ADDR[1], "ssn": S["ssn"]}
F.w2(C.pbc_file("02_W-2_Keystone_Medical_Devices_Gregory.pdf", "Form W-2", "2026-02-24"), EMP_G, EE_G, G_W2)
F.w2(C.pbc_file("03_W-2_Brandywine_Valley_SD_Ellen.pdf", "Form W-2", "2026-02-24"), EMP_E, EE_E, E_W2)
write_xlsx(C.pbc_file("04_Outlook_calendar_export_2025_work_locations.xlsx", "Spreadsheet (calendar export)", "2026-03-09", "Email",
                      "requested at intake"),
    {"Calendar 2025": [["Date", "Day", "Work state", "Location", "Calendar subject / activity", "Workday?"]] + LOG,
     "Gregory notes": [["Note"],
                       ["Exported from Outlook by my assistant (Dana). Weekends left out - I didn't work client meetings on weekends."],
                       ["Travel days: I put the state where I spent most of the working day (e.g. flew to Boston at 7am = MA)."],
                       ["Company holidays and my PTO days are marked - I did not work those days."],
                       ["Last day 8/29/2025. I think it's roughly 20 days in Massachusetts and maybe 15 in Chicago - you count."]]})
F.f1099_r(C.pbc_file("05_1099-R_Fidelity_401k_KMD_stock_in_kind.pdf", "Form 1099-R", "2026-02-24"), FID, REC_T,
          {"1": NUA_BOX1, "2a": NUA_BOX2A, "2b": "Total distribution: X", "4": 0.00, "6": NUA_BOX6, "7": "2",
           "9a": "100%", "13": "09/10/2025"}, account="KMD401K-****0712")
F.f1099_r(C.pbc_file("06_1099-R_Fidelity_401k_direct_rollover.pdf", "Form 1099-R", "2026-02-24"), FID, REC_T,
          {"1": ROLLOVER, "2a": 0.00, "2b": "Total distribution: X", "4": 0.00, "7": "G", "13": "09/10/2025"}, account="KMD401K-****0712")
statement(C.pbc_file("07_Fidelity_401k_distribution_confirmation_NUA.pdf", "Plan distribution confirmation", "2026-02-24"),
    "Fidelity NetBenefits - Keystone Medical Devices 401(k) Savings Plan - Distribution Confirmation", [
        {"table": [["Field", "Value"], ["Participant", "Gregory A. Whitfield"], ["Plan account", "****0712"],
                   ["Distribution reason", "Separation from service 08/29/2025 (age 58)"], ["Distribution date", "09/10/2025"],
                   ["Type", "Lump-sum distribution of entire vested balance"]], "left_align_cols": [0, 1]},
        {"heading": "Distribution detail", "table": [["Component", "Shares", "Value", "Disposition"],
            ["Keystone Medical Devices common (KMDV) - in kind", NUA_SH, NUA_BOX1, "Transferred to Schwab brokerage ****4410 (participant)"],
            ["Plan cost basis of employer securities ($12.00/sh)", "", NUA_BOX2A, "Taxable amount (box 2a)"],
            ["Net unrealized appreciation (box 6)", "", NUA_BOX6, "Not taxable until shares are sold"],
            ["All other plan assets (mutual funds, stable value)", "", ROLLOVER, "Direct rollover to Fidelity Rollover IRA ****5519 (code G)"],
            ["Total distribution", "", NUA_BOX1 + ROLLOVER, ""]], "left_align_cols": [0, 3]},
        {"para": ["Federal withholding: none. The distribution to you consisted solely of employer securities, and mandatory 20% "
                  "withholding cannot exceed the cash and property other than employer securities distributed to you.",
                  "Because the distribution was made after separation from service in or after the year you reached age 55, the 10% "
                  "additional tax does not apply (code 2).",
                  "Schwab has been sent a cost-basis letter showing $12.00 per share. Fair market value at distribution: $80.00 per share."]}])
statement(C.pbc_file("08_Fidelity_NetBenefits_2025_year_end_summary.pdf", "Account summary (not a tax form)", "2026-02-24"),
    "Fidelity - 2025 Year-End Retirement Summary - Gregory A. Whitfield", [
        {"table": [["Account", "12/31/2024 value", "Contributions", "Distributions", "12/31/2025 value"],
                   ["Keystone 401(k) Savings Plan ****0712", 1215400.00, 31000.00 + 15500.00, -(NUA_BOX1 + ROLLOVER), 0.00],
                   ["Fidelity Rollover IRA ****5519 (opened 09/2025)", 0.00, ROLLOVER, 0.00, 803114.27]]},
        {"para": "This summary is provided for information only. See Forms 1099-R for tax reporting. Income earned inside the IRA is "
                 "not reported on your tax return until withdrawn."}])

def schwab_1099(path, acct, owner, divs, int_box1, int_box8, box11, box13, trades, supp, issue):
    secs = [{"heading": "Summary", "table": [["Form", "Box", "Description", "Amount"],
                ["1099-DIV", "1a", "Total ordinary dividends", tot(divs, 1)], ["1099-DIV", "1b", "Qualified dividends", tot(divs, 2)],
                ["1099-INT", "1", "Interest income", int_box1], ["1099-INT", "8", "Tax-exempt interest", int_box8],
                ["1099-INT", "11", "Bond premium", box11], ["1099-INT", "13", "Bond premium on tax-exempt bond", box13],
                ["1099-B", "", "Total proceeds / cost basis (all covered)",
                 f"{sum(t['proceeds'] for t in trades):,.2f} / {sum(t['basis'] for t in trades):,.2f}"]], "left_align_cols": [0, 1, 2]},
            {"heading": "1099-DIV detail", "table": [["Security", "1a Ordinary", "1b Qualified"]] + [list(x) for x in divs]}]
    if trades:
        secs.append({"heading": "1099-B detail - covered securities (basis reported to the IRS)",
                     "table": [["Description", "Acquired", "Sold", "1d Proceeds", "1e Cost", "1g Wash sale loss disallowed", "Gain/(loss)", "ST/LT"]] +
                     [[t["desc"].split(" [")[0], t["acq"], t["sold"], t["proceeds"], t["basis"], "", round(t["proceeds"] - t["basis"], 2),
                       "Short" if t["box"] == "A" else "Long"] for t in trades]})
    secs.append({"heading": "Supplemental information (not reported to the IRS)", "table": [["Item", "Detail", "Amount"]] + supp})
    statement(path, f"Charles Schwab - 2025 Form 1099 Composite & Year-End Summary - {acct}", secs,
              subtitle=f"Account owner(s): {owner} - Date prepared {issue}",
              header_lines=[f"Payer: {SCHWAB[0]}, {SCHWAB[1]}, {SCHWAB[2]} ({SCHWAB[3]})"])

schwab_1099(C.pbc_file("09_Schwab_1099_Composite_Joint_2207.pdf", "Consolidated Form 1099", "2026-02-24"), "Brokerage ****2207",
    "Gregory A. Whitfield & Ellen M. Whitfield JTWROS", DIV_JOINT, SCHWAB_BOX1, MUNI_INT, BOX11_ABP, BOX13_PREM,
    [t for t in TRADES if "joint" in t["desc"]],
    [["1099-INT detail", "Pfizer Investment Enterprises 4.75% 05/19/2033 (CUSIP 716973AE2) - coupons 05/19, 11/19", PFE_COUPONS],
     ["1099-INT detail", "Schwab Bank sweep / Schwab Value Advantage cash", SWEEP_INT],
     ["1099-INT detail (box 8)", "Pennsylvania Turnpike Commission 5.00% 12/01/2038 (PA issuer)", MUNI_INT],
     ["Accrued interest paid on purchases", "Pfizer 4.75% 2033 - bought 03/12/2025 $200,000 face @ 104.250 (113 days accrued)", ACCRUED_PAID],
     ["Bond premium amortization (box 11)", "Pfizer 4.75% 2033 - constant yield, from purchase date", BOX11_ABP],
     ["Bond premium amortization (box 13)", "PA Turnpike 5% 2038 - tax-exempt, reduces box 8 interest", BOX13_PREM],
     ["Gross proceeds summary", "All lots held long-term / covered", ""]], "02/13/2026")
schwab_1099(C.pbc_file("10_Schwab_1099_Composite_Gregory_4410.pdf", "Consolidated Form 1099", "2026-02-24"), "Brokerage ****4410",
    "Gregory A. Whitfield (individual)", DIV_GREG, 0.00, 0.00, 0.00, 0.00, [t for t in TRADES if "4410" in t["desc"]],
    [["Transfer in (09/12/2025)", f"{NUA_SH:,} sh KMDV from Fidelity 401(k) - cost basis per plan letter $12.00/sh (noncovered transfer)",
      NUA_BOX2A],
     ["Unrealized gain/loss 12/31/2025", "KMDV 8,000 sh @ 83.15", 8000 * 83.15 - NUA_BOX2A],
     ["Wash sale tracking", "Schwab tracks wash sales for identical CUSIPs within this account only", ""]], "02/13/2026")
F.f1099_int(C.pbc_file("11_1099-INT_Brandywine_FCU_Ellen.pdf", "Form 1099-INT", "2026-02-24"),
            ["Brandywine Federal Credit Union", "15 S High St", "West Chester, PA 19382", "TIN: 00-2318840"], REC_S, {"1": BFCU_INT},
            account="****0391")
statement(C.pbc_file("12_Schwab_IRA_Ellen_8831_Q4_2025_statement.pdf", "IRA statement", "2026-02-24"),
    "Charles Schwab - Traditional IRA ****8831 - Ellen M. Whitfield - Statement Period 10/01/2025 - 12/31/2025", [
        {"heading": "Account value", "table": [["", "Amount"], ["Beginning value 10/01/2025", 268411.36], ["Ending value 12/31/2025", 281906.04]]},
        {"heading": "Transaction detail", "table": [["Date", "Activity", "Description", "Quantity", "Price", "Amount"],
            ["10/31/2025", "Dividend", "Schwab Short-Term US Treasury ETF (SCHO)", "", "", 812.40],
            ["11/18/2025", "Sell", "Schwab Short-Term US Treasury ETF (SCHO)", -9800, 24.48, 239904.00],
            ["11/20/2025", "Buy", "iShares Core S&P 500 ETF (IVV)", IRA_BUY_SH, IRA_BUY_PX, -round(IRA_BUY_SH * IRA_BUY_PX, 2)],
            ["12/17/2025", "Dividend", "iShares Core S&P 500 ETF (IVV)", "", "", 798.00]], "left_align_cols": [0, 1, 2]},
        {"para": "Income and gains in an IRA are tax-deferred and are not reported on Form 1099. Form 5498 (FMV 12/31/2025 $281,906.04) "
                 "will be mailed by 05/31/2026."}])
write_text(C.pbc_file("13_Email_Ellen_IRA_and_docs_2026-02-24.txt", "Client correspondence", "2026-02-24", "Email"),
"""From: Ellen Whitfield <ellen.whitfield@example.com>
To: preparer@evergreentax.example
Date: Tue, 24 Feb 2026 21:14:02 -0500
Subject: Whitfield - documents uploaded

Hi - everything Greg and I have is uploaded now. A few notes:
- I also uploaded my IRA statement, I know you said you don't need it but Greg said to send everything. In November
  I moved the bond fund money in my IRA into the S&P 500 fund (same one Greg had) because Greg said the market dipped
  and it was a good time to buy.
- Greg's calendar export is coming - his old assistant is pulling it.
- The bond Greg bought in March came with a confirmation that showed a big "accrued interest" charge. Is that deductible?
Thanks! Ellen
""")
statement(C.pbc_file("14_Schwab_trade_confirmation_Pfizer_bond_2025-03-12.pdf", "Trade confirmation", "2026-02-24"),
    "Charles Schwab - Trade Confirmation - Account ****2207", [
        {"table": [["Field", "Value"], ["Trade date / settlement", "03/12/2025 / 03/13/2025"], ["Action", "BUY"],
                   ["Security", "Pfizer Investment Enterprises Pte 4.75% due 05/19/2033, CUSIP 716973AE2"],
                   ["Face amount", PFE_FACE], ["Price", "104.250"], ["Principal", PFE_FACE * PFE_PRICE / 100],
                   ["Accrued interest (113 days, 30/360)", ACCRUED_PAID], ["Total amount due", round(PFE_FACE * PFE_PRICE / 100 + ACCRUED_PAID, 2)],
                   ["Yield to maturity", "4.098%"]], "left_align_cols": [0, 1]}])
F.f1098(C.pbc_file("15_1098_PNC_Mortgage.pdf", "Form 1098", "2026-02-24"),
        ["PNC Mortgage, a division of PNC Bank NA", "3232 Newmark Dr", "Miamisburg, OH 45342", "TIN: 00-1201890"], REC_J,
        {"1": MORT_INT, "2": 318420.55, "3": "06/11/2019", "7": "Yes", "9": "1", "10": "Escrow: RE taxes 9,830.00"}, account="****6604")
statement(C.pbc_file("16_Real_estate_tax_receipts_2025.pdf", "Tax bills / receipts", "2026-02-24"), "2025 Real Estate Tax Receipts - 1418 Brandywine Hunt Dr", [
    {"table": [["Bill", "Paid", "Amount"]] + [[k, "via PNC escrow", v] for k, v in RE_TAX.items()] + [["Total", "", sum(RE_TAX.values())]],
     "total_row": True}])
statement(C.pbc_file("17_Charitable_acknowledgments_2025.pdf", "Donation acknowledgments", "2026-02-24"), "2025 Contribution Acknowledgments", [
    {"table": [["Organization", "Type", "Amount"]] + [[a, "Cash/check - written acknowledgment, no goods or services", b] for a, b in CHARITY]}])
scanned_pages(C.pbc_file("18_Gregory_handwritten_ES_payments_note.pdf", "Handwritten note (scan)", "2026-02-24"),
    [["Estimated taxes 2025 - Federal (IRS Direct Pay)",
      "  4/15/25    8,000",
      "  6/16/25    8,000",
      "  9/15/25    8,000",
      "  1/15/26    8,000",
      "PA - none (withholding covers it?)",
      "",
      "Greg - remember to ask about Boston + Chicago",
      "and the Schwab 'cost basis' on the KMD stock = 640k??"]], handwritten=True, seed=224)
write_xlsx(C.pbc_file("04b_Outlook_calendar_export_DUPLICATE_upload.xlsx", "Spreadsheet (calendar export)", "2026-03-10", "Sharefile upload",
                      "second upload of item 04"),
    {"Calendar 2025": [["Date", "Day", "Work state", "Location", "Calendar subject / activity", "Workday?"]] + LOG})
write_text(C.pbc_file("19_Form_4868_and_extension_payments_confirmation.txt", "Extension confirmation", "2026-04-15", "Evergreen e-file system"),
f"""Form 4868 - Application for Automatic Extension - TY2025 - Gregory A. & Ellen M. Whitfield
Transmitted 04/14/2026 - ACCEPTED 04/15/2026. Payment with extension: ${FED_EXT:,.2f} (EFW, PNC ****7720, settle 04/15/2026)
PA: REV-276 extension payment ${PA_EXT:,.2f} (04/15/2026). MA: Form M-4868 payment ${MA_EXT:,.2f} (04/15/2026, MassTaxConnect).
Reason: awaiting work-location calendar export / multi-state allocation; capital loss carryover verification.
""")

# =================================================================== RETURN
sch_b_interest = [{"payer": "Charles Schwab & Co. - joint brokerage ****2207 (1099-INT box 1)", "amount": SCHWAB_BOX1,
                   "tax_exempt": TAX_EXEMPT},
                  {"payer": "Brandywine Federal Credit Union", "amount": BFCU_INT},
                  {"payer": "ABP Adjustment - Pfizer 4.75% 2033 (1099-INT box 11)", "amount": -BOX11_ABP},
                  {"payer": "Accrued interest paid on purchase - Pfizer 4.75% 2033 (03/12/2025 confirm)", "amount": -ACCRUED_PAID}]
divs = [{"payer": "Charles Schwab - joint ****2207", "ordinary": tot(DIV_JOINT, 1), "qualified": tot(DIV_JOINT, 2)},
        {"payer": "Charles Schwab - Gregory ****4410", "ordinary": tot(DIV_GREG, 1), "qualified": tot(DIV_GREG, 2)}]
SALT_INCOME = PA_WH + LOCAL_EIT + PA_PY_BAL
facts = {
    "status": "MFJ", "taxpayer": {"age65": False}, "spouse": {"age65": False},
    "w2": [{"who": "T", "box1": G_W2["1"], "box2": G_W2["2"], "box3": G_W2["3"], "box4": G_W2["4"], "box5": G_W2["5"], "box6": G_W2["6"]},
           {"who": "S", "box1": E_W2["1"], "box2": E_W2["2"], "box3": E_W2["3"], "box4": E_W2["4"], "box5": E_W2["5"], "box6": E_W2["6"]}],
    "interest": sch_b_interest, "dividends": divs,
    "pension": [{"gross": NUA_BOX1, "taxable": NUA_BOX2A}, {"gross": ROLLOVER, "taxable": 0}],
    "trades": [{k: t[k] for k in ("id", "box", "desc", "acq", "sold", "proceeds", "basis", "code", "adj") if k in t} for t in TRADES],
    "cap_loss_co": CO_RIGHT,
    "itemized": {"state_income_tax": SALT_INCOME, "real_estate_tax": sum(RE_TAX.values()), "mortgage_interest_1098": MORT_INT,
                 "charity_cash": sum(a for _, a in CHARITY)},
    "amt": {"check": True},
    "estimated_payments": sum(a for _, a in FED_ES), "extension_payment": FED_EXT,
}
# NIIT: interest + dividends + net capital gain (qualified-plan distribution and muni interest excluded)
pre = Return1040(dict(facts)).compute()
NII = pre.values["2b"] + pre.values["3b"] + pre.values["7"]
facts["niit"] = {"nii": NII}
R = Return1040(facts).compute()
v = R.values
sd = v["sch_d"]
TOTAL_TAX = v["24"]

# what-if: prior preparer's all-long-term carryover (character error) - same net, different character
fw = dict(facts); fw["cap_loss_co"] = CO_WRONG
RW = Return1040(fw).compute()
CHAR_DIFF = RW.values["24"] - v["24"]
# what-if: NUA ignored (full $640,000 taxed) - shows magnitude for the rubric
fn = dict(facts); fn["pension"] = [{"gross": NUA_BOX1, "taxable": NUA_BOX1}, {"gross": ROLLOVER, "taxable": 0}]
RN = Return1040(fn).compute()
NUA_DIFF = RN.values["24"] - v["24"]

# --- Form 2210 safe-harbor check (tab 8)
WH_TOTAL = v["25d"]
ES_TIMELY = sum(a for _, a in FED_ES)
REQ_90 = TOTAL_TAX * .90
PY_110 = PY["tax"] * 1.10
REQ_ANNUAL = min(REQ_90, PY_110)
QTR_WH = WH_TOTAL / 4
assert WH_TOTAL + ES_TIMELY >= REQ_ANNUAL and QTR_WH + 8000 >= REQ_ANNUAL / 4

# =================================================================== STATE: MA nonresident, PA resident
# MA Form 1-NR/PY. Ratio = MA-source income / income from all sources (MA basis, approximated - see notes).
MA_ALL_SOURCES = v["1a"] + v["2b"] + r(TAX_EXEMPT) + v["3b"] + v["7"] + v["5b"]
MA_RATIO = round(MA_WAGES / MA_ALL_SOURCES, 4)
MA_EXEMPT = r(8800 * MA_RATIO)
MA_SSMED = r(2 * 2000 * MA_RATIO)
MA_TI = MA_WAGES - MA_SSMED - MA_EXEMPT
MA_TAX = r(MA_TI * .05)
MA_REFUND = MA_EXT - MA_TAX
# PA-40 (resident). PA compensation includes 401(k)/403(b) deferrals; 401(k) distribution after retirement not taxable.
PA_INT, PA_DIV = v["2b"], v["3b"]
PA_GAINS = r(sum(t["proceeds"] - t["basis"] for t in TRADES))          # no IRC 1091 disallowance and no carryover in PA (see notes)
PA_TI = r(PA_COMP) + PA_INT + PA_DIV + PA_GAINS
PA_TAX = r(PA_TI * .0307)
PA_TAX_ON_MA = r(MA_WAGES * .0307)
PA_CREDIT = min(MA_TAX, PA_TAX_ON_MA)
PA_AFTER = PA_TAX - PA_CREDIT
PA_PAY = PA_WH + PA_EXT
PA_REFUND = round(PA_PAY - PA_AFTER, 2)
PA_WASH_EFFECT = r(WASH_LOSS * .0307)
PA_90 = PA_AFTER * .9
assert PA_WH >= PA_90            # PA underpayment safe harbor (withholding >= 90% of current-year tax)
IL_TAX_IF_FILED = r(IL_WAGES_IF_SOURCED * .0495)

# =================================================================== return PDF
wd_table = [["Form W-2 workday allocation - Gregory (Keystone; box 1 $410,000)", "Workdays", "Allocation %", "Allocated wages", "Treatment"],
            ["Pennsylvania (resident)", COUNT["PA"], f"{COUNT['PA']/TOT_WD:.4%}", r(G_W2['1'] * COUNT['PA'] / TOT_WD), "Resident - all wages taxed by PA"],
            ["New Jersey", COUNT["NJ"], f"{COUNT['NJ']/TOT_WD:.4%}", r(G_W2['1'] * COUNT['NJ'] / TOT_WD), "PA-NJ reciprocal agreement - taxed only by PA; no NJ-1040NR"],
            ["Massachusetts", COUNT["MA"], f"{MA_PCT:.4%}", MA_WAGES, "MA-source - Form 1-NR/PY"],
            ["Illinois", COUNT["IL"], f"{COUNT['IL']/TOT_WD:.4%}", IL_WAGES_IF_SOURCED, "30 or fewer IL workdays - not IL-source (assumption - verify)"],
            ["Total workdays (holidays 4, PTO 4 excluded)", TOT_WD, "100.0000%", r(G_W2["1"]), ""]]
nua_att = [["Form 1099-R / NUA (Fidelity - Keystone 401(k), lump-sum after separation 08/29/2025, age 58)", "Amount"],
           ["Distribution 1 - employer stock in kind: box 1 (8,000 sh KMDV @ $80.00)", NUA_BOX1],
           ["Box 6 net unrealized appreciation - excluded from income until sale (IRC 402(e)(4)(B))", NUA_BOX6],
           ["Box 2a taxable = plan cost basis ($12.00/sh) - Form 1040 line 5b", NUA_BOX2A],
           ["Distribution 2 - direct rollover to Fidelity IRA (code G) - line 5a only, 'Rollover'", ROLLOVER],
           ["10% additional tax (code 2 - separation in/after year turned 55)", 0],
           ["Basis of KMDV shares going forward: $96,000 cost; NUA $544,000 is LTCG when sold; post-distribution appreciation "
            "LT/ST by holding period from 09/11/2025", ""]]
bond_att = [["Schedule B - bond adjustments", "Amount"],
            ["Schwab 1099-INT box 1 (Pfizer coupons 9,500 + sweep 3,140.55)", SCHWAB_BOX1],
            ["ABP Adjustment - box 11 bond premium amortization (Pfizer, taxable bond, IRC 171 election)", -BOX11_ABP],
            ["Accrued interest paid at purchase 03/12/2025 (trade confirm; supplemental page)", -ACCRUED_PAID],
            ["Tax-exempt interest: box 8 7,500.00 less box 13 premium 1,104.30 (Form 1040 line 2a)", TAX_EXEMPT]]
wash_att = [["Form 8949 box A - code W (cross-account wash sale)", "Amount"],
            ["IVV 400 sh sold 11/10/2025 in Gregory ****4410: proceeds 227,000 - basis 245,000", -WASH_LOSS],
            ["Ellen's Schwab IRA ****8831 bought 420 sh IVV 11/20/2025 (within 30 days)", ""],
            ["Code W adjustment - loss disallowed; NOT added to the IRA's basis (Rev. Rul. 2008-5)", WASH_LOSS],
            ["Net reported gain/(loss)", 0]]
co_att = [["Capital loss carryover from 2024 (recomputed - prior preparer's worksheet was wrong)", "Short-term", "Long-term"],
          ["2024 Sch D line 7 / line 15", PY["st"], PY["lt"]],
          ["2024 line 21 allowed loss ($3,000) absorbs short-term first", 3000, 0],
          ["Correct carryover to 2025 (Sch D lines 6 and 14)", CO_RIGHT["st"], CO_RIGHT["lt"]],
          ["Prior preparer's carryover (all long-term)", CO_WRONG["st"], CO_WRONG["lt"]]]
f2210 = [["Form 2210 safe-harbor check (no penalty)", "Amount"], ["2025 total tax (line 24)", TOTAL_TAX], ["90% of 2025 tax", r(REQ_90)],
         ["110% of 2024 tax (2024 AGI > $150,000)", r(PY_110)], ["Required annual payment (smaller)", r(REQ_ANNUAL)],
         ["Withholding (treated as paid evenly) + timely estimates", r(WH_TOTAL + ES_TIMELY)],
         ["Each quarter: withholding/4 + 8,000 estimate vs 25% of required", f"{r(QTR_WH + 8000):,} vs {r(REQ_ANNUAL/4):,}"]]
C.write_return(R, [
    ("Taxpayer / Spouse", "Gregory A. Whitfield (XXX-XX-6618) / Ellen M. Whitfield (XXX-XX-2274)"),
    ("Address", ", ".join(ADDR)),
    ("Filing status", "Married filing jointly (no dependents)"),
    ("Digital assets question", "No"),
    ("Forms included", "1040; Schedules 1-3 (as needed), A, B, D; Forms 8949, 8959, 8960, 6251 (check); NUA/1099-R statement; "
                       "PA-40 with Schedule G-L; MA Form 1-NR/PY"),
    ("Extension", f"Form 4868 accepted 04/15/2026 (${FED_EXT:,.0f} paid); PA REV-276 ${PA_EXT:,.0f}; MA M-4868 ${MA_EXT:,.0f}"),
    ("Filing method", "E-file federal, PA-40 and MA 1-NR/PY (8879, PA-8879, M-8453 signed 09/16/2026); refunds direct deposit PNC ****7720"),
], state_summary=[
    {"title": "Pennsylvania PA-40 (full-year residents, joint) - 2025",
     "lines": [("1a/1c", "Compensation - Gregory 441,000 + Ellen 65,000 (W-2 box 16; includes 401(k)/403(b) deferrals)", r(PA_COMP)),
               ("2", "Interest (federal Schedule B net; PA Turnpike bond exempt)", PA_INT),
               ("3", "Dividends", PA_DIV),
               ("5", "Net gains - 2025 sales only; no PA carryover of 2024 losses; IVV loss allowed (no PA wash-sale rule - verify)", PA_GAINS),
               ("--", "401(k) distribution after retirement / NUA stock - not PA taxable", 0),
               ("9/11", "Total PA taxable income", PA_TI), ("12", "PA tax 3.07%", PA_TAX),
               ("22 / Sch G-L", f"Resident credit - MA: lesser of MA tax {MA_TAX:,} or PA tax on MA wages {MA_WAGES:,} x 3.07% = {PA_TAX_ON_MA:,}", -PA_CREDIT),
               ("13", "PA withholding (W-2 box 17)", round(PA_WH, 2)), ("14", "Extension payment (REV-276)", PA_EXT),
               ("29/30", "Refund" if PA_REFUND >= 0 else "Tax due", abs(PA_REFUND))],
     "note": "No PA underpayment penalty - withholding exceeds 90% of PA tax. West Chester local EIT final return is filed separately "
             "(Keystone Collections) - outside this deliverable."},
    {"title": "Massachusetts Form 1-NR/PY (nonresidents, joint) - 2025",
     "lines": [("--", f"MA-source wages: 410,000 x {COUNT['MA']}/{TOT_WD} MA workdays", MA_WAGES),
               ("--", f"Nonresident deduction & exemption ratio = {MA_WAGES:,} / {MA_ALL_SOURCES:,} (income from all sources, MA basis - approx.)", MA_RATIO),
               ("--", "Social Security/Medicare deduction 2 x $2,000 x ratio (assumption - see notes)", -MA_SSMED),
               ("--", "Personal exemption MFJ $8,800 x ratio", -MA_EXEMPT),
               ("--", "5.0% income after deductions and exemptions", MA_TI), ("--", "Tax 5.0% (no 4% surtax - income below threshold)", MA_TAX),
               ("--", "MA withholding", 0), ("--", "Extension payment (M-4868)", MA_EXT),
               ("--", "Refund" if MA_REFUND >= 0 else "Tax due", abs(MA_REFUND))],
     "note": "No M-2210 penalty assumed: no 2024 MA tax liability (MA work began 01/2025) - verify exception. NJ: no return (PA-NJ "
             "reciprocity). IL: no return (13 IL workdays <= 30-day nonresident employee threshold - verify)."}],
    attachments=[("Multi-state W-2 workday allocation", wd_table), ("Form 1099-R / NUA statement", nua_att),
                 ("Schedule B bond premium & accrued interest", bond_att), ("Form 8949 wash sale (code W)", wash_att),
                 ("Capital loss carryover recomputation", co_att), ("Form 2210 - safe harbor met (not filed)", f2210)])

# =================================================================== ANSWER KEY
gotchas = [
    gotcha("EVG1022-G1", "SALT - New State Filing Requirements", "Single PA-coded W-2 for a mobile executive -> MA nonresident return",
           "Accept W-2 box 15/16 (100% PA) and file only PA-40; or allocate by days to every state including NJ and IL.",
           f"Use the calendar export: {TOT_WD} workdays (PA {COUNT['PA']}, NJ {COUNT['NJ']}, MA {COUNT['MA']}, IL {COUNT['IL']}). MA has no "
           f"day threshold -> Form 1-NR/PY with MA-source wages 410,000 x {COUNT['MA']}/{TOT_WD} = {fmt(MA_WAGES)}; MA tax {fmt(MA_TAX)}.",
           f"MA return omitted (tax {fmt(MA_TAX)} + penalties/interest)", ["MA 1-NR/PY"], "hard"),
    gotcha("EVG1022-G2", "SALT - New State Filing Requirements (reciprocity / thresholds)", "NJ reciprocity and the Illinois 30-day rule",
           "File NJ-1040NR for the 22 NJ days and IL-1040 for the 13 IL days (and claim PA credits for them).",
           f"PA-NJ reciprocal agreement: NJ wages of a PA resident are taxed only by PA - no NJ return. Illinois: a nonresident employee "
           f"present 30 or fewer working days is not taxed on that compensation (effective 2020) - no IL return (assumption - verify no "
           f"exception applies; IL tax at stake {fmt(IL_TAX_IF_FILED)}).", "Unneeded NJ/IL returns; overstated PA credit", ["PA-40 Sch G-L"], "medium"),
    gotcha("EVG1022-G3", "SALT - resident credit (Schedule G-L)", "PA credit for MA tax is limited",
           f"Credit the full MA tax ({fmt(MA_TAX)}) against PA tax.",
           f"PA credit = lesser of MA tax or PA tax on the income taxed by MA: {fmt(MA_WAGES)} x 3.07% = {fmt(PA_TAX_ON_MA)} -> {fmt(PA_CREDIT)}.",
           f"PA overstated credit {fmt(MA_TAX - PA_CREDIT)}", ["PA-40 line 22"], "medium"),
    gotcha("EVG1022-G4", "Client IRAs / retirement distributions (Form 1099-R) - NUA", "Lump-sum distribution with employer stock in kind",
           "Tax the full $640,000 FMV (or the full $1,420,000), or apply the 10% early-distribution tax (age 58).",
           f"Only box 2a cost basis {fmt(NUA_BOX2A)} is taxable (line 5b); NUA {fmt(NUA_BOX6)} deferred until sale (LTCG). Direct rollover "
           f"{fmt(ROLLOVER)} (code G) nontaxable. Code 2 - separation in/after the year he turned 55 - no 10% tax. Total tax effect of "
           f"ignoring NUA: {fmt(NUA_DIFF)}.", f"Line 5b overstated up to {fmt(NUA_BOX6)}", ["5a", "5b", "16"], "hard"),
    gotcha("EVG1022-G5", "Schedule D - adjustment code W (wash sales)", "Cross-account wash sale into spouse's IRA",
           "Report the $18,000 IVV loss as shown on Schwab's 1099-B (box 1g blank), or disallow it but add $18,000 to the IRA's basis.",
           "Ellen's IRA bought 420 sh IVV 10 days after Gregory's loss sale -> wash sale (spouse; IRA). Form 8949 code W +18,000; the loss is "
           "permanently lost - IRA has no basis step-up (Rev. Rul. 2008-5).", "Sch D ST gain understated $18,000", ["7"], "hard"),
    gotcha("EVG1022-G6", "Schedule B - accrued interest / bond premium (Scan - consolidated 1099)", "Box 11/13 premium and accrued interest paid",
           "Report box 1 $12,641 gross with no ABP adjustment or accrued-interest reversal; report box 8 $7,500 as tax-exempt.",
           f"Sch B: 'ABP Adjustment' -{BOX11_ABP:,.2f} and 'Accrued interest' -{ACCRUED_PAID:,.2f} (from the trade confirm/supplemental page) "
           f"-> line 2b {fmt(v['2b'])}. Line 2a = 7,500 - 1,104.30 box 13 = {fmt(r(TAX_EXEMPT))}.", "Line 2b overstated $3,768", ["2a", "2b"], "medium"),
    gotcha("EVG1022-G7", "General Return Prep Notes - prior-year carryovers (new client)", "Prior preparer's carryover had the wrong character",
           "Enter the prior preparer's $38,000 long-term carryover as given.",
           f"2024: ST (29,000), LT (12,000), $3,000 allowed -> carryover ST {fmt(CO_RIGHT['st'])} / LT {fmt(CO_RIGHT['lt'])} (ST absorbed first). "
           f"2025 net ST {fmt(sd['net_st'])}, net LT {fmt(sd['net_lt'])}; tax {fmt(CHAR_DIFF)} lower than with the all-LT carryover "
           "(ST gain of $5,000 would otherwise be taxed at 35%).", f"Tax overstated {fmt(CHAR_DIFF)}", ["7", "16"], "hard"),
    gotcha("EVG1022-G8", "Schedule A - SALT (OBBBA cap phase-down)", "MAGI over $500,000 reduces the SALT cap to the $10,000 floor",
           f"Deduct SALT up to $40,000 (PA/local tax {fmt(r(SALT_INCOME))} + RE tax {fmt(r(sum(RE_TAX.values())))}).",
           f"Cap = 40,000 - 30% x (MAGI {fmt(v['11'])} - 500,000) -> below floor -> $10,000. Itemized {fmt(v['12e'])} still beats standard.",
           "Sch A line 5e", ["12e"], "medium"),
    gotcha("EVG1022-G9", "SALT - PA compensation and retirement income", "PA taxes 401(k)/403(b) deferrals; PA exempts the retirement distribution",
           "Use federal box 1 wages ($472,000) as PA compensation and/or tax the $96,000 NUA cost basis (or $640,000) on the PA-40; "
           "carry the federal capital loss carryover/code W to PA.",
           f"PA compensation = W-2 box 16 {fmt(r(PA_COMP))}. 401(k) distribution after retirement not PA-taxable. PA net gains {fmt(PA_GAINS)} "
           "(2025 sales only; PA has no carryover; IVV loss allowed - no PA wash-sale rule, verify). PA tax "
           f"{fmt(PA_TAX)}.", "PA-40 lines 1a/5", ["PA-40"], "medium"),
]
C.write_answer_key(R, {"residence": "PA (West Chester) resident; MA nonresident", "new_client": True,
                       "complexity": "Retiring executive - NUA, multi-state W-2 days, investments"}, gotchas,
                   state=[{"jurisdiction": "PA-40", "compensation": r(PA_COMP), "interest": PA_INT, "dividends": PA_DIV, "net_gains": PA_GAINS,
                           "taxable_income": PA_TI, "tax": PA_TAX, "sch_gl_credit_ma": PA_CREDIT, "tax_after_credit": PA_AFTER,
                           "payments": round(PA_PAY, 2), "refund": PA_REFUND},
                          {"jurisdiction": "MA Form 1-NR/PY", "ma_source_wages": MA_WAGES, "workdays_ma_total": [COUNT["MA"], TOT_WD],
                           "ratio": MA_RATIO, "deductions": MA_SSMED, "exemption": MA_EXEMPT, "taxable": MA_TI, "tax": MA_TAX,
                           "payments": MA_EXT, "refund": MA_REFUND},
                          {"jurisdiction": "NJ", "filing": "none - PA/NJ reciprocity"},
                          {"jurisdiction": "IL", "filing": "none - 13 workdays <= 30 (assumption, verify)"}],
                   filings=[{"form": "Form 4868", "filed": "2026-04-15", "payment": FED_EXT},
                            {"form": "Form 1040", "method": "e-file", "due": "2026-10-15", "filed": "2026-09-17"},
                            {"form": "PA-40", "method": "e-file", "due": "2026-10-15", "filed": "2026-09-17"},
                            {"form": "MA Form 1-NR/PY", "method": "e-file", "due": "2026-10-15", "filed": "2026-09-17"}],
                   extra={"workdays": COUNT, "total_workdays": TOT_WD, "ma_source_wages": MA_WAGES, "nua": {"box1": NUA_BOX1,
                          "box2a": NUA_BOX2A, "box6": NUA_BOX6, "rollover": ROLLOVER}, "nii": NII,
                          "capital_loss_carryover_used": CO_RIGHT, "tax_difference_wrong_carryover_character": CHAR_DIFF,
                          "form_2210": {"required_annual_payment": r(REQ_ANNUAL), "paid_timely": r(WH_TOTAL + ES_TIMELY), "penalty": 0}})

C.write_receipt_log("EVG1022-1040-2025", "D. Moreau (senior staff)", "M. Osei (manager)", "S. Kennedy, CPA", "2026-02-10",
                    extension="Federal 4868 e-filed 04/14/2026, accepted 04/15/2026, $3,000 paid; PA REV-276 $1,000; MA M-4868 $2,300")

C.write_notes(f"""
# EVG1022 - Whitfield, Gregory & Ellen - 2025 Form 1040 - Preparer Notes

*Synthetic client - Project Evergreen. NEW CLIENT. Return status: **signed off; federal, PA-40 and MA 1-NR/PY e-filed 09/17/2026 (extended), accepted.***

## Return summary
| | |
|---|---|
| Filing status | Married filing jointly (Gregory 58, Ellen 56) |
| Wages (line 1a) | {fmt(v['1a'])} |
| Taxable / tax-exempt interest | {fmt(v['2b'])} / {fmt(v['2a'])} |
| Ordinary / qualified dividends | {fmt(v['3b'])} / {fmt(v['3a'])} |
| Pensions (5a / 5b) | {fmt(v['5a'])} / {fmt(v['5b'])} (NUA cost basis only) |
| Capital gain (line 7) | {fmt(v['7'])} (net ST {fmt(sd['net_st'])}; net LT {fmt(sd['net_lt'])}) |
| AGI | {fmt(v['11'])} |
| Itemized deductions | {fmt(v['12e'])} (SALT limited to {fmt(v['salt_cap_applied'])}) |
| Taxable income | {fmt(v['15'])} |
| Tax (QD & CG worksheet) | {fmt(v['16'])} |
| Additional Medicare / NIIT | {fmt(R.forms_value('Schedule 2', '11'))} / {fmt(v.get('niit', 0))} |
| Total tax | {fmt(v['24'])} |
| Payments (withholding {fmt(v['25d'])} + estimates {fmt(v['26'])} + extension {fmt(FED_EXT)}) | {fmt(v['33'])} |
| **Federal {'refund' if v['refund'] else 'balance due'}** | **{fmt(v['refund'] or v['balance_due'])}** |
| PA-40 | tax {fmt(PA_TAX)} - MA credit {fmt(PA_CREDIT)} = {fmt(PA_AFTER)}; **{'refund' if PA_REFUND >= 0 else 'due'} {fmt(abs(PA_REFUND))}** |
| MA 1-NR/PY | tax {fmt(MA_TAX)}; **{'refund' if MA_REFUND >= 0 else 'due'} {fmt(abs(MA_REFUND))}** |

## What I did and why (plain English)
1. **Where Gregory worked (multi-state W-2).** Keystone coded all of Gregory's wages to PA (box 15/16). His Outlook export (uploaded twice -
   item 04b marked DUP) shows {TOT_WD} workdays from 01/02 to his last day 08/29 after removing 4 company holidays and 4 PTO days:
   PA {COUNT['PA']}, NJ {COUNT['NJ']}, MA {COUNT['MA']}, IL {COUNT['IL']}. (His own guess of "about 20 MA / 15 IL" was close but not usable.)
   - **New Jersey** - PA and NJ have a reciprocal agreement for employee compensation: a PA resident's NJ-earned wages are taxed only by PA.
     No NJ-1040NR; nothing to credit.
   - **Illinois** - Illinois does not tax a nonresident employee's compensation when he is present in IL performing services for 30 or
     fewer working days in the year (rule effective 2020). 13 days -> no IL return. *Assumption to verify:* no exception applies to
     Gregory's role; if IL-source, IL tax would be about {fmt(IL_TAX_IF_FILED)}.
   - **Massachusetts** - no day threshold for nonresident employees. MA-source wages = box 1 $410,000 x {COUNT['MA']}/{TOT_WD} =
     **{fmt(MA_WAGES)}** (workday method; box 14 severance/PTO payout is in box 1 and allocated with the rest - it relates to 2025 service).
2. **MA Form 1-NR/PY.** Joint nonresident return. Nonresident deduction & exemption ratio = MA-source income / income from all sources
   ({fmt(MA_WAGES)} / {fmt(MA_ALL_SOURCES)} = {MA_RATIO}). The denominator is approximated from the federal return (wages, interest incl. the
   PA Turnpike bond - MA taxes other states' munis -, dividends, capital gain, taxable 401(k) amount); it only drives the prorated
   exemption ($8,800 x ratio = {fmt(MA_EXEMPT)}) and the Social Security/Medicare deduction (2 x $2,000 x ratio = {fmt(MA_SSMED)} -
   *assumption: prorated for nonresidents*). Tax 5% x {fmt(MA_TI)} = **{fmt(MA_TAX)}**; no 4% surtax (far below the ~$1.08M threshold).
   No MA withholding; the $2,300 M-4868 payment covers it. No M-2210 penalty assumed - no MA tax in 2024 (New England territory started
   01/2025) - *verify the exception*.
3. **PA-40 and the credit for MA tax.** PA compensation is W-2 box 16 (**includes** the $31,000 401(k) and Ellen's $3,000 403(b) deferrals):
   {fmt(r(PA_COMP))}. Interest {fmt(PA_INT)} (PA Turnpike bond is a PA obligation - exempt; *assumption: PA interest = federal net of the
   ABP and accrued-interest reversals*), dividends {fmt(PA_DIV)}, net gains {fmt(PA_GAINS)} (2025 sales only - PA has no capital loss
   carryover - and the IVV loss is allowed because PA has no wash-sale rule; *verify*; effect {fmt(PA_WASH_EFFECT)} of PA tax). The 401(k)
   distribution after retirement is not PA income. PA tax 3.07% x {fmt(PA_TI)} = {fmt(PA_TAX)}. Schedule G-L credit = lesser of MA tax
   {fmt(MA_TAX)} or PA tax on the income MA taxed ({fmt(MA_WAGES)} x 3.07% = {fmt(PA_TAX_ON_MA)}) -> **{fmt(PA_CREDIT)}**. I used the MA-taxed
   wages (box 1 based, without the 401(k) deferral portion that MA did not tax) - conservative.
4. **401(k) lump sum - NUA.** Gregory separated from service 08/29/2025 at 58 and Fidelity distributed the **entire** balance in one tax year
   (lump-sum distribution): 8,000 KMDV shares in kind (FMV {fmt(NUA_BOX1)}) and a direct rollover of {fmt(ROLLOVER)} to a Fidelity IRA.
   Only the plan's cost basis of the stock, **{fmt(NUA_BOX2A)}**, is taxable now (1099-R box 2a; line 5b). The NUA of {fmt(NUA_BOX6)} is not taxed
   until the shares are sold and will be long-term capital gain whenever sold. Rollover: line 5a only, marked "Rollover". Code 2 = the
   age-55 separation exception - no 10% tax, no Form 5329. No withholding (stock-only distribution). Taxing the full FMV would have
   overstated tax by {fmt(NUA_DIFF)}.
5. **Wash sale across accounts.** Gregory sold 400 IVV at an $18,000 loss on 11/10 (his account). Ellen's email and IRA statement show her IRA
   bought 420 IVV on 11/20 - within 30 days. A purchase by a spouse or in an IRA counts (Pub. 550; Rev. Rul. 2008-5). Schwab's 1099-B
   can't see it (different owner/account). Form 8949 code W, +$18,000: the loss is **permanently** disallowed - the IRA gets no basis step-up.
6. **Bonds (Schedule B).** Pfizer 4.75% 2033 bought 03/12 at 104.25 with $2,981.94 of accrued interest paid to the seller (trade confirm +
   Schwab supplemental page). Schwab reports the full coupons in box 1 and the premium amortization in box 11. Schedule B: gross box 1, then
   "ABP Adjustment" (-{BOX11_ABP:,.2f}) and "Accrued interest" (-{ACCRUED_PAID:,.2f}) lines -> taxable interest {fmt(v['2b'])}. PA Turnpike muni:
   box 8 $7,500 less box 13 premium $1,104.30 = {fmt(r(TAX_EXEMPT))} on line 2a (premium on a tax-exempt bond is not deductible; it just
   reduces the exempt interest and basis). Ellen asked if the accrued interest is "deductible" - it's a reduction of interest income, done.
7. **Capital loss carryover (new client).** The prior preparer's worksheet carried the whole $38,000 as long-term. Their own 2024 Schedule D
   shows ST (29,000) and LT (12,000); the $3,000 allowed loss uses short-term first -> correct carryover **ST {fmt(CO_RIGHT['st'])} / LT
   {fmt(CO_RIGHT['lt'])}**. 2025: ST gains $5,000 - 26,000 = {fmt(sd['net_st'])}; LT 60,000 - 12,000 = {fmt(sd['net_lt'])}; net {fmt(v['7'])} - all
   taxed at 15%. With the wrong character the $5,000 ST gain would be taxed at 35% -> **{fmt(CHAR_DIFF)}** more tax. Nothing carries to 2026.
8. **Itemized / SALT.** PA withholding + local EIT + 2024 PA balance paid = {fmt(r(SALT_INCOME))}, real estate tax {fmt(r(sum(RE_TAX.values())))}.
   MAGI {fmt(v['11'])} is over $500,000 -> SALT cap = $40,000 - 30% of the excess = below the floor -> **$10,000**. Mortgage $11,240 +
   charity $15,000 -> itemized {fmt(v['12e'])} > standard $31,500. AMT checked - none (tentative minimum tax below regular tax).
9. **Additional Medicare / NIIT.** Medicare wages $506,000 - $250,000 = $256,000 x 0.9% = {fmt(R.forms_value('Schedule 2', '11'))}; Keystone withheld
   0.9% over $200,000 ($2,169 - Form 8959 line 24, included on line 25c). NII = interest + dividends + net capital gain = {fmt(NII)} (the 401(k)
   distribution and muni interest are excluded) -> NIIT {fmt(v.get('niit', 0))}.
10. **Estimated tax penalty.** None - 4 x $8,000 timely estimates plus withholding (treated as paid evenly) meet 25% of the required annual
    payment each quarter (90% of 2025 tax {fmt(r(REQ_90))} is less than 110% of 2024 tax {fmt(r(PY_110))}). Workbook tab 8.

## Open items / client communication
- **KMDV shares (NUA):** basis is $12.00/share ($96,000) - Schwab shows $80.00 in its unrealized gain report. Gregory's handwritten note asked
  about this. Do NOT let a future 1099-B basis of $640,000 through. When sold: NUA portion LTCG regardless of holding period. Recommended
  he talk to us before selling (and before any PA-basis question arises).
- Ellen's IRA and Gregory's taxable account: told them to avoid buying the same fund in either account within 30 days of a loss sale.
- 2026: Gregory no longer has wages - 2026 estimates (federal/PA) sent; no MA/IL filings expected.

## Hand-off to signer / routing
- [x] Return locked; Accountant's Copy saved as *reviewed*
- [x] Federal 1040 (extended) - e-file; due 10/15/2026
- [x] PA-40 (extended) - e-file; due 10/15/2026
- [x] MA Form 1-NR/PY (extended) - e-file; due 10/15/2026
- [x] No NJ or IL returns (reciprocity / 30-day rule - documented on workbook tab 23)
- [x] No FBAR / no foreign items
- [x] eSign (8879, PA-8879, M-8453); call with Gregory held 09/14/2026
- Billing: quote $4,800 + MA $450 + 1.5 hrs re-creating the capital loss carryover from the prior preparer's return (new-client setup).
  Calendar export received 03/09 - no expedite fee.
""")
C.write_review_points(f"""
# Review Points - EVG1022 - 2025 - Form 1040

*Reviewer: M. Osei (blue). Preparer responses in red. Synthetic.*

1. **WP 3 / W-2 (Gregory)** - Draft followed box 15/16 (100% PA) and had no other states. Gregory travelled - use the calendar export.
   - *Preparer: Day count {COUNT['PA']}/{COUNT['NJ']}/{COUNT['MA']}/{COUNT['IL']} of {TOT_WD}. MA 1-NR/PY added ({fmt(MA_WAGES)} MA wages). Tab 23.*
   - 1a. Don't add NJ (reciprocity) or IL (30-day threshold) - document both in the workbook.
   - *Preparer: Done - notes on tab 23 and tab 2.*
2. **PA Schedule G-L** - Draft credited the full MA tax. Limit to PA tax on the MA income.
   - *Preparer: Credit {fmt(PA_CREDIT)} (tab 7).*
3. **Form 1099-R (stock in kind)** - Draft line 5b showed $640,000 (box 2a keyed as box 1). NUA - box 2a is $96,000.
   - *Preparer: Corrected; 1099-R input box 6 entered; NUA statement attached; PA: excluded as retirement distribution.*
4. **Form 8949** - The IVV loss is a wash sale (Ellen's IRA purchase 11/20 - see her email). Code W, no basis adjustment anywhere.
   - *Preparer: Done - $18,000 disallowed.*
5. **Schedule B** - Accrued interest ($2,981.94) and box 11 premium not reversed; line 2a showed $7,500.
   - *Preparer: ABP and accrued interest lines added; 2a now {fmt(r(TAX_EXEMPT))}.*
6. **Schedule D carryover** - Draft used the prior preparer's $38,000 LT. Recompute from their Schedule D: ST 26,000 / LT 12,000.
   - *Preparer: Recomputed (tab 10); tax {fmt(CHAR_DIFF)} lower.*
7. FYI - SALT cap is $10,000 at this MAGI; confirm the draft didn't take $40,000.
   - *Preparer: Confirmed $10,000.*
8. **PA-40 line 1a** - Use box 16 (includes deferrals), not federal box 1.
   - *Preparer: Done - {fmt(r(PA_COMP))}.*
""")
print("EVG1022 done", v["11"], v["15"], v["24"], v["refund"], v["balance_due"], "PA", PA_TAX, PA_CREDIT, PA_REFUND, "MA", MA_TAX, MA_REFUND)
