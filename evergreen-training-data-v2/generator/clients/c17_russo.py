"""EVG1017 - Frank & Diane Russo (MFJ, Illinois - Hinsdale). High-net-worth investor: big Morgan Stanley consolidated
1099 (ORIGINAL + CORRECTED), accrued interest, market discount (code D), wash sale (code W), missing basis on a
noncovered lot, WHFIT/UIT section, REIT 199A dividends, nondividend distributions, foreign tax > $600 (Form 1116),
margin interest (Form 4952 / 8960); three K-1s: PTP (suspended loss), real-estate LP (passive loss released against
other passive income incl. PY suspended), and an operating LLC with a distribution in excess of outside basis
(IRC 731 gain) and a state matrix apportioning income to Pennsylvania -> PA-40 NR + IL Schedule CR."""
from common import ClientBuild, gotcha, fmt
from docs import statement, scanned_pages, write_text, write_xlsx
import forms as F
from tax2025 import Return1040, r

C = ClientBuild("EVG1017", "Russo", "Frank & Diane Russo")
ADDR = ("412 S Garfield St", "Hinsdale, IL 60521")
T = {"name": "Frank J. Russo", "ssn": "XXX-XX-3350", "dob": "1961-07-09"}
S = {"name": "Diane L. Russo", "ssn": "XXX-XX-8814", "dob": "1963-01-22"}
REC_J = ["Frank J. Russo & Diane L. Russo JTWROS", *ADDR, f"TIN: {T['ssn']}"]
REC_T = [T["name"], *ADDR, f"TIN: {T['ssn']}"]
MS = ["Morgan Stanley Smith Barney LLC", "1 New York Plaza", "New York, NY 10004", "TIN: 00-0000262"]
ACCT = "***-*4417-51"

# =================================================================== Morgan Stanley data (CORRECTED = correct)
DIV_DETAIL = [  # payer, ordinary 1a, qualified 1b, capgain 2a, nondividend 3, 199A 5, foreign tax 7
    ("Apple, JNJ, Microsoft, JPMorgan, PepsiCo, P&G common stock", 38000.00, 36400.00, 0, 0, 0, 0),
    ("Vanguard Total Intl Stock Index Adm (VTIAX)", 16200.00, 11800.00, 0, 0, 0, 820.00),
    ("Vanguard Real Estate Index Adm (VGSLX)", 9200.00, 0, 1400.00, 2150.00, 9200.00, 0),
    ("American Funds Growth Fund of America F2 (GFFFX)", 15000.00, 13000.00, 6500.00, 0, 0, 0),
]
DIV_ORIG = [DIV_DETAIL[0], DIV_DETAIL[1], ("Vanguard Real Estate Index Adm (VGSLX)", 10450.00, 0, 1400.00, 900.00, 8400.00, 0),
            DIV_DETAIL[3]]
def tot(rows, i): return round(sum(x[i] for x in rows), 2)
FOREIGN_SRC_INC = 14600.00          # VTIAX foreign-source income per fund's supplemental (RIC)
INT_DETAIL = [("Apple Inc 3.35% 02/09/2032 (bought 03/2025) - coupons", 3350.00),
              ("Ford Motor Credit 4.95% 05/28/2031 - coupon + accrued interest received at sale", 2860.00),
              ("Brokered CDs (Goldman Sachs Bank USA, Ally Bank)", 4100.00),
              ("Bank Deposit Program (sweep)", 3940.00)]
INT_BOX1 = round(sum(x[1] for x in INT_DETAIL), 2)
TSY_DETAIL = [("US Treasury Note 4.25% 06/30/2030 (bought 07/2025) - coupon", 3187.50), ("US Treasury Bills - discount at maturity", 6412.50)]
INT_BOX3 = round(sum(x[1] for x in TSY_DETAIL), 2)
MUNI = [("NY Dormitory Authority 5% 2034", 2500.00), ("California GO 4% 2037", 1400.00), ("Texas Water Dev Board 3% 2036", 900.00)]
INT_BOX8 = round(sum(x[1] for x in MUNI), 2)
ACCR_CORP, ACCR_TSY = 1240.00, 310.00
MD_DISC, MD_HELD, MD_TOTAL = 50000 - 45750, 1282, 3356
MARKET_DISC = r(MD_DISC * MD_HELD / MD_TOTAL)          # ratable accrual (no constant-yield election)
MARGIN_INT = 6400.00
# 1099-B (corrected). box: A=ST covered, D=LT covered, E=LT noncovered
TRADES = [
    dict(id="1", box="A", desc="300 sh Intel Corp (INTC)", acq="01/14/2025", sold="03/10/2025", proceeds=6030.00, basis=12230.00,
         code="W", adj=4100.00, note="Wash sale loss disallowed (1g) 4,100 - repurchased 03/28/2025"),
    dict(id="2", box="A", desc="150 sh Palantir Technologies (PLTR)", acq="02/03/2025", sold="07/21/2025", proceeds=22410.00, basis=12960.00),
    dict(id="3", box="A", desc="100 sh Advanced Micro Devices (AMD)", acq="04/08/2025", sold="11/18/2025", proceeds=14280.00, basis=9870.00),
    dict(id="4", box="A", desc="300 sh Intel Corp (INTC) - replacement lot", acq="03/28/2025", sold="10/06/2025", proceeds=11550.00,
         basis=11120.00, note="basis includes 4,100 disallowed wash-sale loss (broker-adjusted)"),
    dict(id="5", box="D", desc="400 sh Apple Inc (AAPL)", acq="06/12/2018", sold="05/15/2025", proceeds=84200.00, basis=18640.00),
    dict(id="6", box="D", desc="200 sh Johnson & Johnson (JNJ)", acq="09/17/2019", sold="08/11/2025", proceeds=31400.00, basis=27900.00),
    dict(id="7", box="D", desc="$50,000 Ford Motor Credit 4.95% 05/28/2031 (CUSIP 345397C35)", acq="03/08/2022", sold="09/10/2025",
         proceeds=49125.00, basis=45750.00, code="D", adj=-MARKET_DISC, note=f"Accrued market discount (1f) {MARKET_DISC:,}"),
    dict(id="8", box="D", desc="500 sh Verizon Communications (VZ)", acq="04/22/2016", sold="12/08/2025", proceeds=19850.00, basis=24600.00),
    dict(id="9", box="E", desc="300 sh Abbott Laboratories (ABT) - NONCOVERED, basis not reported", acq="11/16/2009", sold="12/02/2025",
         proceeds=36900.00, basis=14850.00, note="basis per client records (300 sh @ $49.50, old Schwab confirm)"),
]
WHFIT = {"name": "Invesco Unit Trust Series 2104 - Dividend Achievers Portfolio (WHFIT)", "div": 1380.00, "qdiv": 1210.00,
         "expenses": 95.00, "proceeds": 4820.00, "basis": 4310.00}
TRADES.append(dict(id="10", box="E", desc="WHFIT - Invesco UIT 2104: pro-rata sales of underlying securities (WHFIT statement)",
                   acq="03/2021", sold="VARIOUS 2025", proceeds=WHFIT["proceeds"], basis=WHFIT["basis"],
                   note="reported only in WHFIT section - not in 1099-B totals"))

# =================================================================== K-1s
PTP = {"name": "Permian Midstream Partners LP", "ein": "00-4829913", "box1": -2340, "dist": 3600, "ubti": -3100, "py_susp": 1150}
PTP_STATES = [("TX", -1120), ("OK", -410), ("LA", -295), ("NM", -188), ("CO", -97), ("ND", -61), ("WV", -52), ("KS", -38),
              ("WY", -27), ("MS", -19), ("AR", -12), ("UT", -9), ("MT", -6), ("AL", -4), ("OH", -2)]
assert sum(x[1] for x in PTP_STATES) == PTP["box1"]
OAK = {"name": "Oak Brook Industrial Partners LP", "ein": "00-6630128", "box2": -9600, "py_susp": 7300}
OAK_STATES = [("IL", -6200), ("IN", -2300), ("WI", -1100)]
RID = {"name": "Ridgeview Capital Partners LLC", "ein": "00-2217765", "box1": 58600, "box5": 400, "dist": 80000,
       "liab_beg": 18000, "liab_end": 14000, "beg_basis": 15500, "w2": 214000, "ubia": 1450000, "cap_beg": -2500}
RID_STATES = [("PA", 38200), ("IL", 19000), ("WI", 1400)]
assert sum(x[1] for x in RID_STATES) == RID["box1"]
PA_SRC = RID_STATES[0][1]
PA_WH = r(PA_SRC * .0307)
DEEMED = RID["liab_beg"] - RID["liab_end"]
BASIS_BEFORE_DIST = RID["beg_basis"] + RID["box1"] + RID["box5"]
TOTAL_DIST = RID["dist"] + DEEMED
GAIN_731 = max(0, TOTAL_DIST - BASIS_BEFORE_DIST)
TRADES.append(dict(id="11", box="F", desc=f"{RID['name']} - distribution in excess of outside basis (IRC 731(a); no 751 property)",
                   acq="06/01/2017", sold="12/31/2025", proceeds=TOTAL_DIST, basis=BASIS_BEFORE_DIST))
OAK_ALLOWED = OAK["box2"] - OAK["py_susp"]          # passive income from Ridgeview absorbs it
SCH_E = RID["box1"] + OAK_ALLOWED                    # PTP loss suspended (separate PTP basket)
PTP_SUSP_CF = -(PTP["box1"]) + PTP["py_susp"]

# =================================================================== other facts
W2 = {"1": 85000.00, "2": 12800.00, "3": 97000.00, "4": 6014.00, "5": 97000.00, "6": 1406.50, "12": [("D", 12000.00), ("DD", 16200.00)],
      "13": ["Retirement plan: X"], "control": "MSG-2210", "state": [{"state": "IL", "id": "4418-2210", "wages": 85000.00, "tax": 4207.50}]}
BANK_INT = 1860.44
MORT_INT, RE_TAX, CHARITY = 9400.00, 18600.00, 12000.00
IL_WH = W2["state"][0]["tax"]
IL_ES = [("01/15/2025", 2600.00, "2024 Q4"), ("04/15/2025", 2800.00, "2025"), ("06/16/2025", 2800.00, "2025"),
         ("09/15/2025", 2800.00, "2025"), ("01/15/2026", 2800.00, "2025")]
IL_PAID_2025 = IL_WH + sum(a for d, a, y in IL_ES if d.endswith("2025"))
IL_ES_FOR_2025 = sum(a for d, a, y in IL_ES if y == "2025")
FED_ES, EXT_PAY = 4 * 6500.00, 4000.00

# =================================================================== PERM
C.write_profile(f"""
# EVG1017 - Russo, Frank & Diane  (PERM)

*Synthetic client - Project Evergreen training data.*

| Item | Detail |
|---|---|
| Client ID | EVG1017 |
| Taxpayer | Frank J. Russo, DOB 07/09/1961, SSN XXX-XX-3350 - retired (former CFO, industrial distributor; retired 2022). No wages |
| Spouse | Diane L. Russo, DOB 01/22/1963, SSN XXX-XX-8814 - strategy consultant, W-2 (Meridian Strategy Group LLC) |
| Address | {ADDR[0]}, {ADDR[1]} (DuPage County) - IL residents all years |
| Investments | Morgan Stanley joint account {ACCT} (margin enabled; FA: Tom Keane); Frank's MS rollover IRA (not reportable); 3 K-1 investments (see below) |
| K-1s | Permian Midstream Partners LP (PTP, 1,500 units since 2021); Oak Brook Industrial Partners LP (limited partner since 2020); Ridgeview Capital Partners LLC (non-managing member since 06/2017 - no participation) |
| Contact | Frank - frank.russo@example.com, (630) 555-0117; wants a call before filing; eSign OK |
| Engagement | Client since 2018. Quote $5,800 (complex investor + K-1s + IL; nonresident state returns billed separately) |
| Payment info | Voided check on file (Salt Creek Bank & Trust ****3008) |

## K-1 carryforward schedule (from 2024 WP)
| Activity | Passive? | 2024 suspended loss c/f | Outside basis 12/31/2024 |
|---|---|---|---|
| Permian Midstream Partners LP (PTP) | Passive - PTP basket (IRC 469(k)) | 1,150 | 21,400 |
| Oak Brook Industrial Partners LP | Passive (limited partner - no $25k allowance) | 7,300 | 38,900 |
| Ridgeview Capital Partners LLC | Passive (no material participation) | 0 | **15,500** (incl. $18,000 share of liabilities; tax capital -2,500) |
""")
F.prior_year_summary(C.perm_file("2024_Form_1040_Return_Summary.pdf", "Prior-year return summary"), "Frank & Diane Russo", "EVG1017",
    "Married filing jointly", [
        ["1a", "W-2 wages (Diane)", 82000], ["2b", "Taxable interest (net of accrued interest paid)", 21870],
        ["3a / 3b", "Qualified / ordinary dividends", "57,100 / 74,900"], ["7", "Capital gain", 61450],
        ["Sch E", "Ridgeview $4,900 passive income; Oak Brook ($12,200) allowed $4,900, suspended $7,300; PTP ($1,150) suspended", 0],
        ["11", "AGI", 240220], ["12", "Itemized (SALT capped $10,000)", 37900], ["Sch 3 line 1", "Foreign tax credit (Form 1116, RIC)", 760],
        ["Sch 2 line 12", "NIIT", 0], ["24", "Total tax", 34120], ["35a", "Refund", 410]],
    carryovers=[["Oak Brook Industrial Partners LP - suspended passive loss (Form 8582)", 7300],
                ["Permian Midstream Partners LP - suspended PTP loss", 1150],
                ["Ridgeview Capital Partners LLC - outside basis 12/31/2024", 15500], ["Capital loss carryover", 0]],
    notes="PY WP: PA-40 NR filed for 2024 (Ridgeview PA-source income $2,900; PA withholding $89). Consolidated 1099 had accrued interest paid ($620) - reversed on Sch B. Margin interest $4,100 -> 4952.")
statement(C.perm_file("Ridgeview_Outside_Basis_Worksheet_2017-2024.pdf", "K-1 basis worksheet (PY)"),
    "Ridgeview Capital Partners LLC - Frank J. Russo - Outside Basis Worksheet 2017-2024", [
        {"table": [["Year", "Beginning", "Contrib.", "Income", "Distributions", "Liability share change", "Ending"],
                   ["2017", 0, 50000, 3100, 0, 11000, 64100], ["2018-2021", 64100, 0, 61200, (-98000), 4000, 31300],
                   ["2022", 31300, 0, 8800, -20000, 2000, 22100], ["2023", 22100, 0, 6100, -12000, 1000, 17200],
                   ["2024", 17200, 0, 4900, -8000, 1400, 15500]]},
        {"para": "Ending 2024 = tax capital (2,500) + share of liabilities 18,000 = 15,500. Maintained by Evergreen (CCH Section 6 - apply limitation)."}])

# =================================================================== PBC
def consolidated(path, corrected, div_rows, md_box, issue_date):
    ord_, q, cg, nd, s199, ft = (tot(div_rows, i) for i in range(1, 7))
    secs = [
        {"heading": "Summary of 2025 Tax Information", "table": [["Form", "Box", "Description", "Amount"],
            ["1099-DIV", "1a", "Total ordinary dividends", ord_], ["1099-DIV", "1b", "Qualified dividends", q],
            ["1099-DIV", "2a", "Total capital gain distributions", cg], ["1099-DIV", "3", "Nondividend distributions", nd],
            ["1099-DIV", "5", "Section 199A dividends", s199], ["1099-DIV", "7", "Foreign tax paid", ft],
            ["1099-DIV", "8", "Foreign country", "RIC / VARIOUS"],
            ["1099-INT", "1", "Interest income", INT_BOX1], ["1099-INT", "3", "Interest on US Savings Bonds & Treasury obligations", INT_BOX3],
            ["1099-INT", "8", "Tax-exempt interest", INT_BOX8], ["1099-INT", "4", "Federal income tax withheld", 0],
            ["1099-B", "", "Short-term covered (Box A) - proceeds / cost / wash sale", "54,270.00 / 46,180.00 / 4,100.00"],
            ["1099-B", "", "Long-term covered (Box D) - proceeds / cost", "184,575.00 / 116,890.00"],
            ["1099-B", "", "Long-term noncovered (Box E) - proceeds (cost not reported)", "36,900.00 / --"],
            ["1099-B", "1f", "Accrued market discount", md_box if md_box else "0.00"]], "left_align_cols": [0, 1, 2]},
        {"heading": "1099-DIV detail by security", "table": [["Security", "1a Ordinary", "1b Qualified", "2a Cap gain", "3 Nondividend", "5 Sec. 199A", "7 Foreign tax"]] +
            [[x[0], *x[1:]] for x in div_rows], "pagebreak": True},
        {"heading": "1099-INT detail", "table": [["Security", "Box", "Amount"]] + [[a, "1", b] for a, b in INT_DETAIL] +
            [[a, "3", b] for a, b in TSY_DETAIL] + [[a, "8", b] for a, b in MUNI]},
        {"heading": "1099-B - Short-term transactions for which basis is reported to the IRS (Box A)",
         "table": [["Description", "Acquired", "Sold", "1d Proceeds", "1e Cost", "1g Wash sale loss disallowed", "Gain/(loss)"]] +
            [[t["desc"], t["acq"], t["sold"], t["proceeds"], t["basis"], t.get("adj", "") if t.get("code") == "W" else "",
              round(t["proceeds"] - t["basis"] + (t.get("adj", 0) if t.get("code") == "W" else 0), 2)] for t in TRADES if t["box"] == "A"],
         "pagebreak": True},
        {"heading": "1099-B - Long-term transactions for which basis is reported to the IRS (Box D)",
         "table": [["Description", "Acquired", "Sold", "1d Proceeds", "1e Cost", "1f Accrued market discount", "Gain/(loss)"]] +
            [[t["desc"], t["acq"], t["sold"], t["proceeds"], t["basis"], (md_box if t.get("code") == "D" else ""),
              round(t["proceeds"] - t["basis"], 2)] for t in TRADES if t["box"] == "D"]},
        {"heading": "1099-B - Long-term transactions for which basis is NOT reported to the IRS (Box E) - noncovered",
         "table": [["Description", "Acquired", "Sold", "1d Proceeds", "1e Cost", "Gain/(loss)"],
                   ["300 sh Abbott Laboratories (ABT)", "11/16/2009", "12/02/2025", 36900.00, "NOT PROVIDED", "--"]],
         "note": "Cost basis for noncovered securities is not reported to the IRS and may not be available. You are responsible for determining basis."},
        {"heading": "Supplemental information (not reported to the IRS)", "pagebreak": True, "table": [["Item", "Detail", "Amount"],
            ["Accrued interest paid on purchases", "Apple Inc 3.35% 2032 - purchased 03/11/2025", ACCR_CORP],
            ["Accrued interest paid on purchases", "US Treasury Note 4.25% 2030 - purchased 07/15/2025", ACCR_TSY],
            ["Margin interest charged", "Margin account - 2025", MARGIN_INT],
            ["Foreign source income (RIC pass-through)", "Vanguard Total Intl Stock Index Adm - included in box 1a", FOREIGN_SRC_INC],
            ["Advisory fees charged", "Portfolio management fee (not deductible 2018-2025)", 11850.00],
            ["State tax information", "US government obligations % of 1099-INT box 3 interest", "100%"],
            ["State tax information", "Box 8 tax-exempt interest by state", "NY 2,500.00; CA 1,400.00; TX 900.00"],
            ["Nondividend distributions (box 3)", "VGSLX return of capital - reduces cost basis of shares held", nd]]},
        {"heading": "Widely Held Fixed Investment Trust (WHFIT) Information - NOT included in the 1099 totals above",
         "table": [["WHFIT", "Item", "Amount"], [WHFIT["name"], "Ordinary dividends", WHFIT["div"]],
                   ["", "Qualified dividends", WHFIT["qdiv"]], ["", "Trust expenses (non-interest)", WHFIT["expenses"]],
                   ["", "Gross proceeds - pro-rata sales of trust assets", WHFIT["proceeds"]],
                   ["", "Your cost of assets sold (per cost factor)", WHFIT["basis"]], ["", "Holding period", "Long-term (units bought 03/2021)"]],
         "note": "WHFIT income is reported to you under Treas. Reg. 1.671-5. Report these items on your return as if you held the underlying assets directly."},
    ]
    statement(path, f"Morgan Stanley - 2025 Consolidated Form 1099 {'(CORRECTED)' if corrected else '(ORIGINAL)'} - Account {ACCT}", secs,
              subtitle=f"{'CORRECTED ' if corrected else ''}Tax Information Statement - Frank J. Russo & Diane L. Russo JTWROS - Date issued {issue_date}",
              header_lines=[f"Payer: {MS[0]}, {MS[1]}, {MS[2]} ({MS[3]})",
                            "Recipient: Frank J. Russo & Diane L. Russo JTWROS, 412 S Garfield St, Hinsdale IL 60521 - TIN XXX-XX-3350"]
                           + (["<b>CORRECTED:</b> reclassification of Vanguard Real Estate Index distributions (box 1a/3/5) and addition of "
                               "accrued market discount (box 1f) on the Ford Motor Credit sale. This statement replaces the statement dated 02/13/2026."]
                              if corrected else []))

F.organizer(C.pbc_file("01_2025_Organizer_completed.pdf", "Client organizer", "2026-02-20"), "Frank & Diane Russo", "EVG1017",
    general=[("Did your marital status change during 2025?", "No", ""),
             ("Did you receive any K-1s?", "Yes", "Permian, Oak Brook, Ridgeview (late as usual)"),
             ("Did you have foreign accounts or pay foreign tax?", "No", "only through mutual funds"),
             ("Did you receive distributions from partnerships?", "Yes", "Ridgeview $80k - return of our money?"),
             ("Did you make estimated payments?", "Yes", "Fed 4 x 6,500; IL 4 x 2,800"),
             ("Did you sell any securities?", "Yes", "see MS 1099 - Abbott basis on the yellow sticky"),
             ("Did you receive, sell, exchange digital assets?", "No", "")],
    dependents=[],
    income_rows=[["Wages", "Meridian Strategy Group (Diane)", 82000, "see W-2"],
                 ["Interest/dividends/sales", "Morgan Stanley JT", "see PY", "see 1099"],
                 ["Interest", "Salt Creek Bank & Trust", 1640, "1,860"],
                 ["K-1 Permian Midstream (PTP)", "", -1150, "small loss"],
                 ["K-1 Oak Brook Industrial", "", -12200, "loss again"],
                 ["K-1 Ridgeview Capital", "", 4900, "big year"],
                 ["Suspended passive losses c/f", "Oak Brook / Permian", "7,300 / 1,150", ""]],
    deductions_rows=[["Mortgage interest", "Chase", 10100, "see 1098"], ["Real estate tax", "DuPage County", 17900, "18,600"],
                     ["Charitable", "St. Isaac Jogues / Hinsdale Humane Society", 10000, "12,000"],
                     ["Margin interest", "Morgan Stanley", 4100, "on statement"], ["Investment advisory fees", "Morgan Stanley", 11200, "11,850"]],
    signature_date="02/18/2026")
EMP = {"name": "Meridian Strategy Group LLC", "addr1": "71 S Wacker Dr Ste 2400", "addr2": "Chicago, IL 60606", "ein": "00-2290417"}
F.w2(C.pbc_file("02_W-2_Meridian_Strategy_Group_Diane.pdf", "Form W-2", "2026-02-20"), EMP,
     {"name": S["name"], "addr1": ADDR[0], "addr2": ADDR[1], "ssn": S["ssn"]}, W2)
consolidated(C.pbc_file("03_Morgan_Stanley_Consolidated_1099_2025_ORIGINAL.pdf", "Consolidated 1099 (original)", "2026-02-20"),
             False, DIV_ORIG, None, "02/13/2026")
consolidated(C.pbc_file("04_Morgan_Stanley_Consolidated_1099_2025_CORRECTED.pdf", "Consolidated 1099 (corrected)", "2026-03-16"),
             True, DIV_DETAIL, float(MARKET_DISC), "03/12/2026")
F.f1099_int(C.pbc_file("05_1099-INT_Salt_Creek_Bank.pdf", "Form 1099-INT", "2026-02-20"),
            ["Salt Creek Bank & Trust", "25 E First St", "Hinsdale, IL 60521", "TIN: 00-0000630"], REC_J, {"1": BANK_INT}, account="****3008")
F.f1098(C.pbc_file("06_1098_Chase_Mortgage.pdf", "Form 1098", "2026-02-20"),
        ["JPMorgan Chase Bank, N.A.", "PO Box 78420", "Phoenix, AZ 85062", "TIN: 00-0000001"], REC_J,
        {"1": MORT_INT, "2": 262410.77, "3": "04/02/2012", "7": "Yes", "9": "1"}, account_no="****0442")
statement(C.pbc_file("07_DuPage_County_Property_Tax_Receipts_2025.pdf", "Property tax receipts", "2026-02-20"),
    "DuPage County Treasurer - Tax Year 2024 Bills Payable in 2025 - PIN 09-12-203-0XX", [
        {"table": [["Installment", "Due", "Paid", "Amount"], ["1st", "06/02/2025", "05/28/2025", 9300.00], ["2nd", "09/02/2025", "08/25/2025", 9300.00],
                   ["Total paid in 2025", "", "", RE_TAX]], "total_row": True}])
ptp_boxes = [["1", "Ordinary business income (loss)", "", PTP["box1"]], ["19", "Distributions - cash", "A", PTP["dist"]],
             ["20", "Section 199A information (PTP)", "Z", "STMT"], ["20", "UBTI (for tax-exempt partners)", "V", PTP["ubti"]],
             ["20", "Other information", "AH", "STMT"]]
F.k1_generic(C.pbc_file("08_K-1_1065_Permian_Midstream_Partners_PTP.pdf", "Schedule K-1 (1065) - PTP package", "2026-03-20", "Mail (scanned)"),
    "1065", PTP["name"],
    [["A Partnership EIN", PTP["ein"]], ["B Partnership", f"{PTP['name']}, 1300 Main St, Houston TX 77002"], ["D Publicly traded partnership", "X  Yes"]],
    [["E Partner TIN", T["ssn"]], ["F Partner", "Frank J. Russo"], ["G / I1", "Limited partner / Individual"]],
    [["J Partner's share of profit/loss/capital", "0.0012% / 0.0012% / 0.0012%"], ["K Share of liabilities (nonrecourse / QNR / recourse)", "410 / 7,880 / 0"],
     ["Units held 12/31/2025", "1,500"]],
    ptp_boxes,
    supplemental=[
        {"heading": "Section 199A statement (box 20 code Z) - publicly traded partnership", "table": [["Item", "Amount"],
            ["Qualified PTP items: ordinary business income (loss)", PTP["box1"]], ["Section 751 gain (on disposition - none)", 0]]},
        {"heading": "State schedule - partner's share of ordinary income (loss) by state", "table": [["State", "Amount"]] + [[a, b] for a, b in PTP_STATES],
         "note": "Amounts are provided for informational purposes. Consult your tax advisor regarding state filing requirements."},
        {"heading": "Unit sales schedule", "para": "No units were sold in 2025. (Sales schedule is provided only in the year of disposition.)"}],
    notes=["Tax package prepared by PTP tax services provider (synthetic)."])
F.k1_generic(C.pbc_file("09_K-1_1065_Oak_Brook_Industrial_Partners_LP.pdf", "Schedule K-1 (1065)", "2026-04-02", "Email from sponsor"),
    "1065", OAK["name"],
    [["A Partnership EIN", OAK["ein"]], ["B Partnership", f"{OAK['name']}, 2001 Spring Rd Ste 400, Oak Brook IL 60523"],
     ["D Publicly traded partnership", "No"]],
    [["E Partner TIN", T["ssn"]], ["F Partner", "Frank J. Russo"], ["G / I1", "LIMITED partner / Individual"]],
    [["J Share of profit/loss/capital", "1.85%"], ["K Share of liabilities (qualified nonrecourse)", "61,200"]],
    [["2", "Net rental real estate income (loss)", "", OAK["box2"]], ["19", "Distributions - cash", "A", 0],
     ["20", "Section 199A information", "Z", "STMT"]],
    supplemental=[{"heading": "Section 199A statement", "table": [["Item", "Amount"], ["Rental real estate - trade or business (QBI)", OAK["box2"]],
                                                                  ["W-2 wages", 0], ["UBIA", 1840000]]},
                  {"heading": "State apportionment", "table": [["State", "Net rental income (loss)"]] + [[a, b] for a, b in OAK_STATES]}])
F.k1_generic(C.pbc_file("10_K-1_1065_Ridgeview_Capital_Partners_LLC.pdf", "Schedule K-1 (1065)", "2026-09-08", "Email from sponsor",
                        "received after extension"),
    "1065", RID["name"],
    [["A Partnership EIN", RID["ein"]], ["B Partnership", f"{RID['name']}, 1100 Liberty Ave, Pittsburgh PA 15222"],
     ["D Publicly traded partnership", "No"]],
    [["E Partner TIN", T["ssn"]], ["F Partner", "Frank J. Russo"], ["G / I1", "LLC member - other (non-manager) / Individual"]],
    [["J Share of profit/loss/capital", "4.20% / 4.20% / 3.90%"],
     ["K Share of liabilities: nonrecourse beginning / ending", f"{RID['liab_beg']:,} / {RID['liab_end']:,}"],
     ["L Capital account (tax basis): beginning / income / distributions / ending",
      f"{RID['cap_beg']:,} / {RID['box1'] + RID['box5']:,} / ({RID['dist']:,}) / {RID['cap_beg'] + RID['box1'] + RID['box5'] - RID['dist']:,}"],
     ["N Share of net unrecognized 704(c) gain", "0 / 0"]],
    [["1", "Ordinary business income (loss)", "", RID["box1"]], ["5", "Interest income", "", RID["box5"]],
     ["19", "Distributions - cash and marketable securities", "A", RID["dist"]], ["20", "Section 199A information", "Z", "STMT"]],
    supplemental=[
        {"heading": "Section 199A statement (non-SSTB - precision machining)", "table": [["Item", "Amount"], ["QBI - ordinary business income", RID["box1"]],
                                                                                        ["W-2 wages", RID["w2"]], ["UBIA", RID["ubia"]]]},
        {"heading": "State apportionment matrix - partner's share", "table": [["State", "Apportioned business income", "State withholding / composite"]] +
            [["PA", PA_SRC, f"PA nonresident withholding 3.07% remitted: {PA_WH:,.2f} (PA-65 Schedule NRK-1 attached)"],
             ["IL", RID_STATES[1][1], "none (resident)"], ["WI", RID_STATES[2][1], "none"]]},
        {"heading": "Footnotes", "para": [
            "Box 19A includes the Pennsylvania nonresident withholding paid on the partner's behalf.",
            "Distributions did not include section 751 property and did not change the partner's share of unrealized receivables or inventory.",
            "The partnership does not track partner outside basis. Partners should consult their tax advisor if distributions exceed basis.",
            f"PA-65 Schedule NRK-1: PA-source income (loss) from business {PA_SRC:,}; PA tax withheld {PA_WH:,.2f}."]}])
write_xlsx(C.pbc_file("11_Frank_cost_basis_records.xlsx", "Client basis records (XLSX)", "2026-02-20"), {
    "Lots": [["Security", "Shares", "Trade date", "Price", "Cost", "Source", "Notes"],
             ["Abbott Laboratories (ABT)", 300, "11/16/2009", 49.50, 14850.00, "Schwab confirm (old account)", "moved to MS 2014 - no basis transferred"],
             ["Invesco UIT 2104", 400, "03/10/2021", 25.00, 10000.00, "MS", "WHFIT"],
             ["Vanguard Real Estate Index (VGSLX)", 612.4, "various", "", 61200.00, "MS", "reduce for return of capital"]]})
scanned_pages(C.pbc_file("12_Sticky_note_Abbott_basis.pdf", "Handwritten note (scan)", "2026-02-20"),
    [["Abbott - 300 sh", "bought Nov 16 2009 @ 49.50", "(Schwab - see spreadsheet)", "sold Dec '25 thru Tom @ MS", "  - Frank"]],
    handwritten=True, seed=17, skew=2.5)
statement(C.pbc_file("13_Estimated_Payments_Federal_and_IL.pdf", "Payment confirmations", "2026-02-20"),
    "2025 Estimated Tax Payments - Federal (EFTPS) and Illinois (MyTax Illinois)", [
        {"heading": "Federal 1040-ES (2025)", "table": [["Date", "Amount"], ["04/15/2025", 6500.00], ["06/16/2025", 6500.00],
                                                        ["09/15/2025", 6500.00], ["01/15/2026", 6500.00]]},
        {"heading": "Illinois IL-1040-ES", "table": [["Date", "Amount", "Tax year"]] + [[d, a, y] for d, a, y in IL_ES]}])
statement(C.pbc_file("14_Charitable_Receipts_2025.pdf", "Charity receipts", "2026-02-20"), "2025 Contribution Receipts", [
    {"table": [["Organization", "Amount"], ["St. Isaac Jogues Parish", 8000.00], ["Hinsdale Humane Society", 4000.00], ["Total", CHARITY]],
     "total_row": True, "note": "No goods or services provided."}])
statement(C.pbc_file("15_Morgan_Stanley_IRA_Year-End_Statement_Frank.pdf", "IRA statement (informational)", "2026-02-20"),
    "Morgan Stanley - Rollover IRA (Frank J. Russo) - 2025 Year-End Summary", [
        {"table": [["Item", "Amount"], ["Beginning value", 1284400.18], ["Dividends & interest (inside IRA)", 31220.40],
                   ["Realized gains (inside IRA)", 44810.00], ["Distributions", 0], ["Ending value 12/31/2025", 1411927.55]],
         "left_align_cols": [0]},
        {"para": "No Form 1099-R issued for 2025 (no distributions). RMDs begin at age 75 (born 1961)."}])
statement(C.pbc_file("16_Form_4868_Extension_Confirmation.pdf", "Extension confirmation", "2026-04-15", "Internal", "e-filed by firm"),
    "Form 4868 - Acknowledgement / IL-505-I", [
        {"table": [["Item", "Value"], ["Federal 4868 accepted", "04/15/2026 - $4,000 paid (EFTPS)"],
                   ["Illinois IL-505-I", "Automatic 6-month extension; no payment (overpayment expected)"],
                   ["PA", "Automatic via federal extension (REV-276 not required - no payment)"], ["Extended due date", "10/15/2026"]],
         "left_align_cols": [0, 1]}])
write_text(C.pbc_file("17_Email_Frank_2026-09-09.txt", "Client correspondence", "2026-09-09", "Email"),
"""From: Frank Russo <frank.russo@example.com>
To: preparer@evergreentax.example
Date: Wed, 9 Sep 2026 08:31:05 -0500
Subject: Ridgeview K-1 finally

Attached. Big year at Ridgeview - they distributed $80,000. That's just getting my money back out, so no tax on
that part, right? Also Oak Brook shows another loss - I assume that's still "suspended" like last year.

The sticky note has my Abbott cost. Morgan Stanley sent a corrected 1099 in March - please make sure you use it.
Call me before you file. - Frank
""")

# =================================================================== RETURN
div_facts = [{"payer": f"Morgan Stanley - {x[0]}", "ordinary": x[1], "qualified": x[2], "capgain_dist": x[3]} for x in DIV_DETAIL]
div_facts.append({"payer": f"Morgan Stanley WHFIT - {WHFIT['name']}", "ordinary": WHFIT["div"], "qualified": WHFIT["qdiv"]})
int_facts = [{"payer": "Morgan Stanley - interest (1099-INT box 1)", "amount": INT_BOX1},
             {"payer": "Morgan Stanley - US Treasury interest (box 3)", "amount": INT_BOX3},
             {"payer": "Morgan Stanley - accrued market discount (Ford Motor Credit bond, 1099-B box 1f)", "amount": MARKET_DISC},
             {"payer": "Salt Creek Bank & Trust", "amount": BANK_INT},
             {"payer": f"{RID['name']} (K-1 box 5)", "amount": RID["box5"]},
             {"payer": "Accrued interest paid on purchases - Apple 3.35% 2032 (Morgan Stanley)", "amount": -ACCR_CORP},
             {"payer": "Accrued interest paid on purchases - US Treasury 4.25% 2030 (Morgan Stanley)", "amount": -ACCR_TSY},
             {"payer": "Tax-exempt interest (1099-INT box 8) - memo", "amount": 0, "tax_exempt": INT_BOX8}]
taxable_int = r(sum(x["amount"] for x in int_facts))
ord_div = r(sum(x["ordinary"] for x in div_facts))
qual_div = r(sum(x["qualified"] for x in div_facts))
itemized = {"state_income_tax": IL_PAID_2025, "real_estate_tax": RE_TAX, "mortgage_interest_1098": MORT_INT,
            "investment_interest": MARGIN_INT, "charity_cash": CHARITY}

def build(foreign_ti):
    facts = {
        "status": "MFJ", "taxpayer": {"age65": False}, "spouse": {"age65": False},
        "w2": [{"who": "S", "box1": W2["1"], "box2": W2["2"], "box3": W2["3"], "box4": W2["4"], "box5": W2["5"], "box6": W2["6"]}],
        "interest": int_facts, "dividends": div_facts, "trades": TRADES,
        "sch1": {"sch_e": SCH_E},
        "itemized": itemized,
        "qbi": {"businesses": [{"name": RID["name"], "qbi": RID["box1"], "w2_wages": RID["w2"], "ubia": RID["ubia"]},
                               {"name": OAK["name"] + " (current + PY suspended loss allowed)", "qbi": OAK_ALLOWED}],
                "reit": tot(DIV_DETAIL, 5), "ptp": 0},
        "ftc": {"method": "1116", "taxes": tot(DIV_DETAIL, 6), "foreign_source_ti": foreign_ti, "category": "passive (RIC)"},
        "amt": {"other": 0},
        "estimated_payments": FED_ES, "extension_payment": EXT_PAY,
    }
    return facts

# pass 1 to get line 9 / itemized for the 1116 apportionment, then final
R0 = Return1040(build(FOREIGN_SRC_INC)).compute()
ratio_1116 = FOREIGN_SRC_INC / R0.values["9"]
apport = r(ratio_1116 * R0.values["12e"])
FOREIGN_TI = r(FOREIGN_SRC_INC - apport)
facts = build(FOREIGN_TI)
R = Return1040(facts).compute()
v = R.values
sd = v["sch_d"]
NII_GROSS = v["2b"] + v["3b"] + v["7"] + SCH_E
NII = NII_GROSS - r(MARGIN_INT)
facts["niit"] = {"nii": NII, "gross": NII_GROSS, "deductions": r(MARGIN_INT)}
R = Return1040(facts).compute()
v = R.values
assert R.values["9"] == R0.values["9"]
inv_income_4952 = v["2b"] + (v["3b"] - v["3a"])

# ---- Illinois
il_add = r(INT_BOX8)
il_sub = r(INT_BOX3 - ACCR_TSY)
il_base = v["11"] + il_add - il_sub
il_exempt = 2 * 2850 if v["11"] <= 500000 else 0
il_net = il_base - il_exempt
il_tax = r(il_net * .0495)
il_cr_limit = r(il_tax * PA_SRC / il_base)
pa_tax = r(PA_SRC * .0307)
il_cr = min(pa_tax, il_cr_limit)
il_ptc = r(RE_TAX * .05) if v["11"] <= 500000 else 0
il_after = il_tax - il_cr - il_ptc
il_pay = r(IL_WH + IL_ES_FOR_2025)
il_refund = il_pay - il_after

# ---- attachments
sched_b_note = [["Schedule B support (tape on consolidated 1099 page)", "Amount"],
                ["MS 1099-INT box 1 (corrected)", r(INT_BOX1)], ["MS 1099-INT box 3 US Treasury", r(INT_BOX3)],
                [f"Accrued market discount - Ford Motor Credit sale (1099-B 1f; ratable {MD_DISC:,} x {MD_HELD}/{MD_TOTAL} days)", MARKET_DISC],
                ["Salt Creek Bank", r(BANK_INT)], ["Ridgeview K-1 box 5", RID["box5"]],
                ["Less: 'Accrued interest' paid on purchases (Apple bond 1,240; Treasury note 310)", -r(ACCR_CORP + ACCR_TSY)],
                ["Schedule B line 4 / Form 1040 line 2b", v["2b"]],
                ["Tax-exempt interest line 2a (NY/CA/TX munis - added back for IL)", v["2a"]],
                ["WHFIT dividends added (not in 1099-DIV totals): ordinary / qualified", f"{WHFIT['div']:,.0f} / {WHFIT['qdiv']:,.0f}"],
                ["Nondividend distributions box 3 (not income - reduce VGSLX basis)", r(tot(DIV_DETAIL, 4))],
                ["WHFIT trust expenses / advisory fees (miscellaneous itemized - not deductible)", f"{WHFIT['expenses']:,.0f} / 11,850"]]
basis_ws = [["Ridgeview Capital Partners LLC - outside basis (CCH Section 6 - limitation applied)", "Amount"],
            ["Beginning outside basis 01/01/2025 (tax capital -2,500 + liabilities 18,000)", RID["beg_basis"]],
            ["+ Ordinary income (box 1)", RID["box1"]], ["+ Interest (box 5)", RID["box5"]],
            ["= Basis before distributions", BASIS_BEFORE_DIST],
            ["- Cash distributions box 19A (incl. PA withholding paid for partner)", -RID["dist"]],
            [f"- Deemed distribution: decrease in share of liabilities {RID['liab_beg']:,} -> {RID['liab_end']:,} (IRC 752(b))", -DEEMED],
            ["= Excess distribution -> IRC 731(a) capital gain, long-term (held since 2017), Form 8949 box F", GAIN_731],
            ["Ending outside basis 12/31/2025", 0]]
f8582 = [["Form 8582 / passive activity summary", "Current", "PY suspended", "Allowed 2025", "Carryforward"],
         [RID["name"] + " (passive income)", RID["box1"], 0, RID["box1"], 0],
         [OAK["name"] + " (limited partner - no $25k allowance)", OAK["box2"], -OAK["py_susp"], OAK_ALLOWED, 0],
         [PTP["name"] + " (PTP - own basket, IRC 469(k); not on 8582)", PTP["box1"], -PTP["py_susp"], 0, -PTP_SUSP_CF],
         ["Schedule E line 41", "", "", SCH_E, ""]]
f1116 = [["Form 1116 - passive category, country RIC (mutual fund)", "Amount"],
         ["Line 1a gross foreign-source income (VTIAX)", r(FOREIGN_SRC_INC)],
         [f"Lines 3a-3g apportioned deductions: itemized {R0.values['12e']:,} x {FOREIGN_SRC_INC:,.0f}/{R0.values['9']:,} ({ratio_1116:.4%})", -apport],
         ["Line 7 net foreign-source taxable income", FOREIGN_TI],
         ["Qualified dividend adjustment", "Not required - adjustment exception (foreign QD < $20,000; no 20%/28%/25% rate income)"],
         ["Line 8 foreign taxes paid (1099-DIV box 7)", r(tot(DIV_DETAIL, 6))],
         ["Why 1116: $820 exceeds the $600 MFJ de minimis election limit", ""],
         ["Credit allowed (Schedule 3 line 1)", v.get("ftc", 0)]]
f4952 = [["Form 4952 - investment interest expense", "Amount"], ["Line 1 margin interest paid 2025", r(MARGIN_INT)],
         ["Line 4a gross investment income: taxable interest + nonqualified dividends", inv_income_4952],
         ["Line 4g election to include QD/net capital gain", "None needed"], ["Line 8 deduction (Schedule A line 9)", r(MARGIN_INT)],
         ["Tracing: margin draws used to buy taxable equities (not munis - IRC 265)", ""]]
qbi_att = [["Form 8995 support", "Amount"], [RID["name"] + " QBI (W-2 wages 214,000; UBIA 1,450,000)", RID["box1"]],
           [OAK["name"] + " QBI loss (2025 loss + 2024 suspended loss allowed in 2025)", OAK_ALLOWED],
           ["Qualified REIT dividends (1099-DIV box 5, corrected)", r(tot(DIV_DETAIL, 5))],
           [PTP["name"] + " - PTP loss suspended under 469 -> excluded until allowed", 0]]
C.write_return(R, [
    ("Taxpayer / Spouse", "Frank J. Russo (XXX-XX-3350) / Diane L. Russo (XXX-XX-8814)"),
    ("Address", ", ".join(ADDR)),
    ("Filing status", "Married filing jointly"),
    ("Digital assets question", "No"),
    ("Forms included", "1040; Schedules 1, 2, 3, A, B, D, E; Forms 1116, 4952, 6251 (check), 8582, 8949, 8960, 8995; K-1 basis worksheet; IL-1040 "
                       "(Sch M, CR, ICR); PA-40 NR"),
    ("Extension", "Federal 4868 04/15/2026 ($4,000); IL-505-I automatic; PA automatic"),
    ("Filing method", "E-file federal, IL and PA (8879/IL-8453/PA-8879 signed 09/23/2026); refunds by direct deposit Salt Creek ****3008"),
], state_summary=[
    {"title": "Illinois Form IL-1040 (full-year residents) - 2025",
     "lines": [("1", "Federal AGI", v["11"]), ("2", "Federally tax-exempt interest (NY/CA/TX munis)", il_add),
               ("5 / Sch M", "US Treasury interest subtraction (box 3 9,600 less accrued interest paid 310)", -il_sub),
               ("9", "Base income", il_base), ("10", "Exemption allowance 2 x $2,850 (AGI <= $500,000)", -il_exempt),
               ("11", "Net income", il_net), ("12/14", "Tax 4.95%", il_tax),
               ("15 / Sch CR", f"Credit for tax paid to PA: lesser of PA tax {pa_tax:,} or IL tax x {PA_SRC:,}/{il_base:,} = {il_cr_limit:,}", -il_cr),
               ("16 / Sch ICR", "Property tax credit 5% x 18,600 (AGI <= $500,000)", -il_ptc),
               ("24", "Total tax", il_after), ("25", "IL withholding (W-2)", r(IL_WH)),
               ("26", "2025 IL estimated payments (incl. 01/15/2026)", r(IL_ES_FOR_2025)),
               ("36/40", "Refund" if il_refund >= 0 else "Tax due", abs(il_refund))],
     "note": "Muni interest from other states is taxable to IL. PTP and Oak Brook state amounts are losses/immaterial - no other state filings."},
    {"title": "Pennsylvania PA-40 NR (nonresident, joint) - 2025",
     "lines": [("4", "Net income from business - Ridgeview Capital Partners LLC (PA-65 Schedule NRK-1, PA-source)", PA_SRC),
               ("9", "Total PA taxable income (Frank)", PA_SRC), ("12", "PA tax 3.07%", pa_tax),
               ("13", "PA nonresident withholding (Schedule NRK-1)", PA_WH), ("26-28", "Tax due / (refund)", pa_tax - PA_WH)],
     "note": "Filing required - nonresident with PA-source income over $33. IRC 731 gain on the partnership interest treated as non-PA-source "
             "(intangible; assumption - see notes). Diane has no PA-source income."}],
    attachments=[("Schedule B support", sched_b_note), ("K-1 outside basis worksheet - Ridgeview", basis_ws),
                 ("Passive activities (Form 8582 / PTP)", f8582), ("Form 1116 detail", f1116), ("Form 4952", f4952),
                 ("Form 8995 support", qbi_att)])

cf = {"permian_ptp_suspended_loss": PTP_SUSP_CF, "oak_brook_suspended_loss": 0, "ridgeview_outside_basis": 0}
for k, val in cf.items():
    R.values[f"{k}_carryforward_2026"] = val

gotchas = [
    gotcha("EVG1017-G1", "Scan - duplicate documents (original + CORRECTED consolidated 1099)", "Corrected Morgan Stanley 1099 replaces the original",
           "Autoflow both consolidated 1099s (dividends ~$158k), or only the original (box 1a $79,650, box 3 $900, box 5 $8,400, no market discount).",
           f"Use the CORRECTED 03/12/2026 statement only: 1a {fmt(tot(DIV_DETAIL, 1))}, box 3 nondividend {fmt(tot(DIV_DETAIL, 4))} (return of "
           f"capital - not income, reduces VGSLX basis), box 5 199A {fmt(tot(DIV_DETAIL, 5))}, box 1f {fmt(MARKET_DISC)}. Bookmark original as superseded.",
           "Lines 2b/3a/3b/7/13a", ["3b", "13a"], "easy"),
    gotcha("EVG1017-G2", "Schedule B - accrued interest / state exemption; Scan - consolidated 1099 (accrued interest, state exemptions)",
           "Accrued interest paid and Treasury interest for IL",
           "Report box 1 + box 3 interest without reversing $1,550 accrued interest paid; subtract all $9,600 Treasury interest on IL; forget the muni add-back.",
           f"Schedule B: negative 'Accrued interest' lines (1,240 corporate, 310 Treasury) -> line 2b {fmt(v['2b'])}. IL Schedule M subtraction = Treasury "
           f"interest net of its accrued interest = {fmt(il_sub)}; add back out-of-state muni interest {fmt(il_add)}.",
           "Line 2b; IL base income", ["2b", "IL-1040"], "medium"),
    gotcha("EVG1017-G3", "Schedule D - adjustment codes D and W; missing cost basis", "Market discount, wash sale and a noncovered lot with no basis",
           f"Leave market discount inside capital gain; add the wash-sale loss back twice; let the ABT lot flow with $0 basis ({fmt(36900)} gain).",
           f"Ford bond: 8949 box D code D adjustment -{MARKET_DISC:,} and the {fmt(MARKET_DISC)} reported as interest on Sch B. INTC: code W +4,100 "
           "(replacement lot basis already includes it - no second adjustment). ABT box E basis $14,850 from client's Schwab records (gain $22,050).",
           "Line 7 overstated ~$16,500 if ABT basis missed; character shift for market discount", ["7", "2b"], "medium"),
    gotcha("EVG1017-G4", "Scan - consolidated 1099 (UITs / WHFITs)", "WHFIT section is outside the 1099 totals",
           "Import only the 1099-DIV/B summary -> WHFIT dividends ($1,380) and pro-rata sale ($510 LT gain) omitted; or deduct WHFIT expenses.",
           "Report WHFIT items as if held directly: dividends 1,380 (1,210 qualified) on Sch B; pro-rata sales on 8949 box E (4,820 / 4,310); "
           "trust expenses $95 are miscellaneous itemized deductions - not deductible.", "Lines 3a/3b/7", ["3b", "7"], "medium"),
    gotcha("EVG1017-G5", "Foreign Transactions - Form 1116 ($600 MFJ de minimis; RIC)", "Foreign tax $820 exceeds the MFJ de minimis",
           "Claim $820 directly on Schedule 3 without Form 1116 (de minimis election) or deduct it on Schedule A.",
           f"$820 > $600 MFJ -> Form 1116, passive category, country 'RIC'. Foreign-source income {fmt(FOREIGN_SRC_INC)} less apportioned "
           f"deductions = {fmt(FOREIGN_TI)}; limitation exceeds tax -> credit {fmt(v.get('ftc', 0))}.", "Sch 3 line 1 / Form 1116", ["20"], "medium"),
    gotcha("EVG1017-G6", "NIIT - margin interest allocable; Scan - margin interest", "Margin interest -> Form 4952 and Form 8960",
           "Ignore the $6,400 margin interest (not on a 1099 form) or deduct it with the advisory fees.",
           f"Form 4952: investment income {fmt(inv_income_4952)} > $6,400 -> fully deductible on Sch A line 9 (no QD election). Form 8960 line 9a "
           f"allocates it against NII (NII {fmt(NII)}). This year NIIT is on MAGI over $250k ({fmt(v['11'] - 250000)}) because that is smaller, so "
           "the 8960 allocation has no dollar effect - still required. Advisory fees remain nondeductible.", "Sch A line 9; Form 8960", ["12e", "23"], "medium"),
    gotcha("EVG1017-G7", "Schedules K-1 - partnership distribution in excess of outside basis (Section 6 - apply the limitation)",
           "Ridgeview $80,000 distribution exceeds outside basis",
           "Treat the distribution as a tax-free return of capital (client's view; Axcess default without basis limitation).",
           f"Basis 15,500 + income {RID['box1'] + RID['box5']:,} = {BASIS_BEFORE_DIST:,}; distributions 80,000 + IRC 752(b) deemed distribution "
           f"{DEEMED:,} (liability share decrease) = {TOTAL_DIST:,} -> IRC 731(a) LT capital gain {fmt(GAIN_731)} (8949 box F). No 751 property.",
           f"Line 7 understated {fmt(GAIN_731)}", ["7"], "hard"),
    gotcha("EVG1017-G8", "Schedules K-1 - passive activities / PTP; QBI (REIT, PTP)", "LP rental loss vs other passive income; PTP basket",
           "Suspend the Oak Brook loss again (client's assumption) and ignore the $7,300 PY suspended loss (organizer PY line blank); or net the PTP "
           "loss against Ridgeview; or include PTP loss in QBI.",
           f"Limited partner: no $25k allowance, but passive losses offset passive income: Ridgeview {fmt(RID['box1'])} absorbs Oak Brook 2025 "
           f"{fmt(OAK['box2'])} + PY {fmt(-OAK['py_susp'])} (all allowed; enters QBI). PTP loss usable only against the same PTP -> {fmt(PTP_SUSP_CF)} "
           f"suspended, excluded from QBI. QBI: 20% x ({RID['box1']:,} {OAK_ALLOWED:,}) + 20% x REIT {tot(DIV_DETAIL, 5):,.0f} = {fmt(v['13a'])}.",
           "Sch E line 41; line 13a", ["8", "13a"], "hard"),
    gotcha("EVG1017-G9", "SALT - New State Filing Requirements (K-1 state matrix)", "K-1 state matrices: PA filing required; losses don't trigger filings",
           "File nothing outside IL (or file in every state on the PTP schedule).",
           f"Ridgeview apportions {fmt(PA_SRC)} to PA -> PA-40 NR required (PA-source income > $33): tax {fmt(pa_tax)} = withholding. IL Schedule CR "
           f"credit {fmt(il_cr)}. WI $1,400 < WI $2,000 filing threshold. PTP and Oak Brook matrices are all losses -> no filing.",
           "PA-40 NR; IL Sch CR", ["IL-1040", "PA-40"], "medium"),
]
C.write_answer_key(R, {"residence": "IL (Hinsdale); PA nonresident", "complexity": "HNW investor - consolidated 1099 + 3 K-1s + IL + PA"}, gotchas,
                   state=[{"jurisdiction": "IL-1040", "base_income": il_base, "exemptions": il_exempt, "net_income": il_net, "tax": il_tax,
                           "sch_cr_credit": il_cr, "property_tax_credit": il_ptc, "total_tax": il_after, "payments": il_pay, "refund": il_refund},
                          {"jurisdiction": "PA-40 NR", "pa_source_income": PA_SRC, "tax": pa_tax, "withholding": PA_WH, "due": pa_tax - PA_WH}],
                   filings=[{"form": "Form 4868", "filed": "2026-04-15", "payment": EXT_PAY},
                            {"form": "Form 1040", "method": "e-file", "due": "2026-10-15", "filed": "2026-09-24"},
                            {"form": "IL-1040", "method": "e-file", "due": "2026-10-15", "filed": "2026-09-24"},
                            {"form": "PA-40 NR", "method": "e-file", "due": "2026-10-15", "filed": "2026-09-24"}],
                   extra={"ridgeview_731_gain": GAIN_731, "nii": NII, "form_1116_foreign_source_ti": FOREIGN_TI,
                          "form_4952_investment_income": inv_income_4952})

C.write_receipt_log("EVG1017-1040-2025", "A. Brennan (senior staff)", "M. Osei (manager)", "S. Kennedy, CPA", "2026-02-20",
                    extension="Federal 4868 e-filed 04/15/2026, accepted, $4,000 paid; IL/PA automatic")
C.write_notes(f"""
# EVG1017 - Russo, Frank & Diane - 2025 Form 1040 - Preparer Notes

*Synthetic client - Project Evergreen. Return status: **signed off; federal, IL-1040 and PA-40 NR e-filed 09/24/2026 (extended), accepted.***

## Return summary
| | |
|---|---|
| Filing status | Married filing jointly (Frank 64, Diane 62 - no senior items) |
| Wages (Diane) | {fmt(v['1a'])} |
| Taxable interest / tax-exempt interest | {fmt(v['2b'])} / {fmt(v['2a'])} |
| Ordinary / qualified dividends | {fmt(v['3b'])} / {fmt(v['3a'])} |
| Capital gain (Sch D line 16) | {fmt(v['7'])} (ST {fmt(sd['net_st'])}; LT {fmt(sd['net_lt'])}) |
| Schedule E (K-1s) | {fmt(SCH_E)} |
| AGI | {fmt(v['11'])} |
| Itemized deductions | {fmt(v['12e'])} |
| QBI deduction | {fmt(v['13a'])} |
| Taxable income | {fmt(v['15'])} |
| Tax (QD/CG worksheet) / FTC | {fmt(v['16'])} / {fmt(v.get('ftc', 0))} |
| NIIT | {fmt(v.get('niit', 0))} |
| Total tax | {fmt(v['24'])} |
| Payments (withholding {fmt(v['25d'])} + estimates {fmt(v['26'])} + extension {fmt(EXT_PAY)}) | {fmt(v['33'])} |
| **Federal {'refund' if v['refund'] else 'balance due'}** | **{fmt(v['refund'] or v['balance_due'])}** |
| IL-1040 | tax after credits {fmt(il_after)}; **{'refund' if il_refund >= 0 else 'due'} {fmt(abs(il_refund))}** |
| PA-40 NR | tax {fmt(pa_tax)} = withholding {fmt(PA_WH)}; $0 due |

## What I did and why (plain English)
1. **Which Morgan Stanley 1099.** Two consolidated 1099s are in the PBC - the original (02/13) and a CORRECTED one (03/12). Only the corrected
   statement is used. It reclassified $1,250 of the REIT fund's distributions to box 3 (return of capital - not income, it lowers the fund's
   basis), raised box 5 (199A) to $9,200 and added the Ford bond's accrued market discount.
2. **Interest (Schedule B).** Box 1 {fmt(r(INT_BOX1))} + Treasury box 3 {fmt(r(INT_BOX3))} + market discount {fmt(MARKET_DISC)} + bank + Ridgeview box 5,
   then two negative "Accrued interest" lines for interest Frank *paid* the sellers when he bought the Apple bond ($1,240) and the Treasury
   note ($310) - the broker doesn't net these. Line 2b {fmt(v['2b'])}. Muni interest {fmt(v['2a'])} on line 2a (NY/CA/TX issuers).
3. **Capital gains (8949 / Schedule D).**
   - INTC wash sale: the $4,100 disallowed loss is added back (code W) on the March sale; the replacement lot's basis already carries it.
   - Ford Motor Credit bond: bought at a market discount in 2022; the ratably accrued discount {fmt(MARKET_DISC)} is ordinary interest - code D
     adjustment out of the gain and onto Schedule B.
   - Abbott (noncovered, box E): MS reported no basis. Frank's records (2009 Schwab confirm, sticky note) show $14,850 -> gain $22,050, not $36,900.
   - WHFIT (Invesco UIT): its section is outside the 1099 totals; pro-rata sales added (box E) and WHFIT dividends added to Schedule B.
   - Capital gain distributions {fmt(r(tot(DIV_DETAIL, 3)))} on Sch D line 13.
   - Ridgeview excess distribution gain {fmt(GAIN_731)} (below).
4. **Ridgeview - distribution in excess of basis.** Outside basis 01/01 $15,500 (from our worksheet; includes $18,000 share of liabilities)
   + income $59,000 = {fmt(BASIS_BEFORE_DIST)}. Distributions: $80,000 cash (includes PA withholding paid for him) + $4,000 deemed distribution
   from the drop in his share of partnership liabilities (IRC 752(b)) = {fmt(TOTAL_DIST)}. The excess **{fmt(GAIN_731)}** is long-term capital gain
   under IRC 731(a) (interest held since 2017), reported on 8949 box F. Footnote confirms no 751 hot-asset shift. Ending basis $0. Frank's
   "return of my money" view is right only up to basis - told him on our 09/22 call.
5. **Passive activities.** All three K-1s are passive (Frank doesn't work in any of them).
   - Oak Brook (limited partner): no $25,000 rental allowance for LPs, **but** passive losses can offset passive income - Ridgeview's
     {fmt(RID['box1'])} is passive income. So the 2025 loss {fmt(OAK['box2'])} **and** the 2024 suspended loss {fmt(-OAK['py_susp'])} (organizer PY
     column left the carryforward line blank - picked up from PERM/PY 8582) are fully allowed.
   - Permian Midstream (PTP): a PTP's loss can only offset income from the same PTP (IRC 469(k)) -> {fmt(PTP['box1'])} suspended; total PTP
     carryforward {fmt(PTP_SUSP_CF)}. UBTI (box 20V) is irrelevant for an individual taxable account. Distributions $3,600 < basis.
   - Schedule E line 41 = {fmt(SCH_E)}.
6. **QBI (Form 8995).** Taxable income before QBI is under $394,600: 20% x (Ridgeview {RID['box1']:,} + Oak Brook allowed loss {OAK_ALLOWED:,})
   + 20% x REIT dividends {tot(DIV_DETAIL, 5):,.0f} = {fmt(v['13a'])}. The suspended PTP loss is left out until it is allowed.
7. **Foreign tax credit.** $820 of foreign tax from the international index fund exceeds the $600 MFJ de minimis limit, so Form 1116 is
   required (passive category, country "RIC"). Foreign-source income $14,600 less apportioned deductions = {fmt(FOREIGN_TI)}; the limitation is
   well above $820 -> full credit. Qualified-dividend adjustment not needed (adjustment exception).
8. **Margin interest.** $6,400 from the MS supplemental page (not on any 1099 box). Form 4952: investment income {fmt(inv_income_4952)} (taxable
   interest + nonqualified dividends) exceeds it -> fully deductible on Schedule A line 9 without electing to treat qualified dividends/gains
   as investment income. Margin draws were used for equities (no IRC 265 muni allocation). Advisory fees ($11,850) remain nondeductible.
9. **NIIT (Form 8960).** NII = interest + dividends + net gain + passive K-1 income (Ridgeview less Oak Brook) - investment interest $6,400 =
   {fmt(NII)}. Tax is 3.8% of the smaller of NII or MAGI over $250,000 ({fmt(v['11'] - 250000)}) = {fmt(v.get('niit', 0))}. (The margin interest
   allocation doesn't change the dollars this year, but it is on the form.)
10. **Itemized.** IL income tax paid in 2025 {fmt(r(IL_PAID_2025))} (W-2 + three 2025 estimates + 2024 Q4 paid 01/15/2025; the 01/15/2026
    payment is a 2026 deduction) + DuPage property tax $18,600 = SALT {fmt(r(IL_PAID_2025 + RE_TAX))} under the $40,000 cap (MAGI < $500,000);
    mortgage $9,400; investment interest $6,400; charity $12,000. AMT checked (Form 6251) - none.
11. **Illinois.** Base income = AGI + out-of-state muni interest {fmt(il_add)} - US Treasury interest {fmt(il_sub)} (net of the accrued interest
    Frank paid on the Treasury note). Exemptions 2 x $2,850 (AGI under $500k). Tax 4.95% {fmt(il_tax)}; Schedule CR credit for PA tax {fmt(il_cr)}
    (lesser of PA tax or IL tax on the PA income); property tax credit 5% {fmt(il_ptc)}. Payments {fmt(il_pay)} -> refund {fmt(il_refund)}.
12. **State filing review (K-1 matrices).** Ridgeview apportions {fmt(PA_SRC)} to Pennsylvania -> **PA-40 NR** required (nonresident with more than
    $33 of PA-source income). PA tax {fmt(pa_tax)}; Ridgeview already withheld {fmt(PA_WH)} (NRK-1) -> $0 due. The IRC 731 gain is treated as
    non-PA-source (gain on an intangible partnership interest of a nonresident - *assumption; Ridgeview has no PA real property per footnote;
    flagged for signer*). Wisconsin $1,400 is below WI's $2,000 nonresident filing threshold. Oak Brook and the PTP apportion only losses -> no
    new filing requirements.
13. **Not reportable:** Frank's Morgan Stanley rollover IRA statement (income inside the IRA; no distributions).

## Hand-verification
- Ordinary portion of TI = {fmt(v['15'])} - (QD {fmt(v['3a'])} + net capital gain {fmt(sd['ncg'])}) taxed at MFJ rates; preferential portion at 15%
  (no 0% room; below $600,050) -> line 16 {fmt(v['16'])}.
- NIIT = 3.8% x {fmt(v['11'] - 250000)} = {fmt(v.get('niit', 0))}.

## Open items / client communication
- Carryforwards to 2026: PTP suspended loss {fmt(PTP_SUSP_CF)}; Ridgeview outside basis $0 (next distribution is gain unless income/liabilities increase).
- Reduce VGSLX basis by the $2,150 return of capital in the lot records (told Tom Keane at MS).
- Frank asked for a 2026 projection (large Ridgeview distributions continuing) - separate PROJ project code.

## Hand-off to signer / routing
- [x] Return locked; Accountant's Copy saved as *reviewed*
- [x] Federal 1040 (extended) - e-file; due 10/15/2026
- [x] IL-1040 (extended) - e-file; due 10/15/2026
- [x] PA-40 NR (extended) - e-file; due 10/15/2026
- [x] No FBAR (no foreign accounts - foreign tax only via RIC)
- [x] eSign (8879, IL-8453, PA-8879); Frank wants a call before release - done 09/22
- Billing: quote $5,800 + PA-40 NR $350 + 2.5 hrs for Ridgeview basis/matrix after late K-1 (external). K-1 received 09/08 - more than 15 days before
  10/15, so no expedite fee.
""")
C.write_review_points(f"""
# Review Points - EVG1017 - 2025 - Form 1040

*Reviewer: M. Osei (blue). Preparer responses in red. Synthetic.*

1. **WP 4 / Consolidated 1099** - Autoflow picked up both the original and CORRECTED Morgan Stanley 1099s. Delete the original.
   - *Preparer: Done - original bookmarked "superseded".*
2. **Schedule B** - Accrued interest paid ($1,240 + $310) not reversed; market discount $0 in draft. Tape on the 1099 page.
   - *Preparer: Reversed; market discount {fmt(MARKET_DISC)} added from corrected 1f.*
3. **Form 8949** - Ford bond needs code D adjustment; ABT flowed with $0 basis - use Frank's records.
   - *Preparer: Code D -{MARKET_DISC:,}; ABT basis $14,850 per Schwab confirm (copy requested and received).*
4. **WHFIT** - Invesco UIT section not in the draft. Add income and pro-rata sales.
   - *Preparer: Added.*
5. **Schedule 3 line 1** - Draft took $820 as de minimis. MFJ limit is $600 - Form 1116 required (RIC).
   - *Preparer: 1116 prepared; full credit.*
6. **Schedule A line 9 / Form 8960** - Margin interest missing. 4952 + allocate to NII.
   - *Preparer: Added; no QD election needed.*
7. **K-1 Ridgeview** - Draft had no basis limitation; distribution passed as tax-free. Apply Section 6 limitation, include the 752(b) deemed
   distribution.
   - *Preparer: Gain {fmt(GAIN_731)} on 8949 box F; worksheet attached.*
8. **Form 8582** - Draft suspended Oak Brook again and omitted the $7,300 PY carryforward. Ridgeview passive income absorbs both. Keep the PTP separate.
   - *Preparer: Corrected; PTP carryforward {fmt(PTP_SUSP_CF)}.*
9. **SALT** - Ridgeview matrix shows PA $38,200. Add PA-40 NR and IL Schedule CR. Confirm no other state thresholds met.
   - *Preparer: PA-40 NR added ($0 due after NRK-1 withholding); IL CR {fmt(il_cr)}; WI under threshold; PTP/Oak Brook losses only.*
10. **IL-1040** - Treasury subtraction should be net of accrued interest paid on the Treasury note; add back muni interest.
    - *Preparer: Done.*
""")
print("EVG1017 done", v["11"], v["15"], v["24"], v["refund"], v["balance_due"], "IL", il_after, il_refund, "PA", pa_tax - PA_WH)
