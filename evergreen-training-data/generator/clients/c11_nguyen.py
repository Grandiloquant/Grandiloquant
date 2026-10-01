"""EVG1011 - Thomas Nguyen (Single, Tennessee - Nashville). Left his W-2 job in March 2025; self-directed crypto/stock investor
(not a trader in securities - no Schedule C, no mark-to-market). Coinbase 1099-DA (2025: gross proceeds only, basis not
reported) vs CoinLedger all-wallet report (use CoinLedger detail, reconcile to 1099-DA, do not load both); self-transfers are not
sales; staking income (Kraken 1099-MISC is a subset of the CoinLedger income report); NFT digital art = collectible (28%);
no wash-sale rule for crypto but Robinhood stock wash sale (code W) applies; NIIT limited by MAGI excess; 1095-A with APTC
based on low projected income -> repay all APTC (>400% FPL, no cap); IP PIN (stale CP01A); extension + expedite fee."""
from common import ClientBuild, gotcha, fmt
from docs import statement, scanned_pages, write_text, write_csv
import forms as F
from tax2025 import Return1040, r

C = ClientBuild("EVG1011", "Nguyen", "Thomas Nguyen")
ADDR = ("1907 Eastland Ave Unit 3", "Nashville, TN 37206")
OLD_ADDR = ("410 Demonbreun St Apt 1208", "Nashville, TN 37203")
T = {"name": "Thomas Q. Nguyen", "ssn": "XXX-XX-2087", "dob": "1992-10-08"}
REC_T = [T["name"], *ADDR, f"TIN: {T['ssn']}"]

# ====================================================================== PERM
C.write_profile(f"""
# EVG1011 - Nguyen, Thomas  (PERM)

*Synthetic client - Project Evergreen training data.*

| Item | Detail |
|---|---|
| Client ID | EVG1011 |
| Taxpayer | Thomas Q. Nguyen, DOB 10/08/1992, SSN {T['ssn']}. Former product analyst (Harpeth Digital Media) - resigned 03/2025; now manages his own investments full time |
| Address | {ADDR[0]}, {ADDR[1]} since 06/2025 (previously {OLD_ADDR[0]}, {OLD_ADDR[1]}). **Form 8822 not filed with IRS** (IRS mail still goes to old address). Tennessee - no income tax (Hall tax repealed 2021) |
| Filing status | Single, no dependents |
| **IP PIN** | **Identity-theft victim (2023). Enrolled in the IP PIN program - a NEW 6-digit IP PIN is issued every calendar year (CP01A or IRS Online Account). The 2025 return (filed in 2026) needs the 2026 IP PIN.** |
| Investments | Coinbase, Kraken (staking), MetaMask self-custody wallet (DeFi/NFT), Robinhood (stocks). Uses CoinLedger to aggregate all wallets/exchanges |
| Trader status | Reviewed 2025: holding periods mostly months/years, ~20 trades/yr -> investor, not a trader in securities (no Sch C, no 475(f) election) |
| Health coverage | Employer plan Jan-Mar 2025; TN marketplace plan Apr-Dec 2025 (APTC based on projected income $36,000) |
| Contact | thomas.nguyen@example.com, (615) 555-0139 (text OK); eSign OK |
| Engagement | Client since 2022. Crypto/investor tier $1,600 + hourly for reconciliation. **Expedite fee (15%) applies to information received within 15 days of a deadline** |
| Payments | 2025 estimates via IRS Direct Pay; refund by direct deposit (checking ****5582) |
""")
F.prior_year_summary(C.perm_file("2024_Form_1040_Return_Summary.pdf", "Prior-year return summary"), "Thomas Nguyen",
    "EVG1011", "Single", [
        ["1a", "W-2 wages (Harpeth Digital Media)", 91250],
        ["2b", "Taxable interest", 1105],
        ["7", "Capital gain (crypto - CoinLedger report; Robinhood)", 11860],
        ["8 / Sch 1 8v", "Digital assets received as ordinary income (staking)", 740],
        ["11", "AGI", 104955], ["12", "Standard deduction", 14600], ["15", "Taxable income", 90355],
        ["24", "Total tax", 14212], ["25a", "Withholding", 12890], ["26", "Estimated payments", 2000],
        ["35a", "Refund", 678]],
    notes="PY WP: 2024 e-filed with IP PIN from CP01A dated 01/2024 (IRS issues a new IP PIN each year). CoinLedger report tied to "
          "exchange statements. 2025 estimates recommended (4 x $5,500) because he planned to leave his job and sell BTC. "
          "No health coverage issues in 2024 (employer plan all year).")

# ====================================================================== trades
FEE = 0.004
def cb(qty, asset, acq, cost, sold, gross, lt, tid, collectible=False):
    buy_fee = round(cost * FEE, 2)
    sale_fee = round(gross * FEE, 2)
    return {"id": tid, "asset": f"{qty} {asset}", "acq": acq, "sold": sold, "cost": cost, "buy_fee": buy_fee,
            "gross": gross, "sale_fee": sale_fee, "net": round(gross - sale_fee, 2), "basis": round(cost + buy_fee, 2), "lt": lt}

COINBASE = [
    cb("0.50000000", "BTC", "12/16/2024", 53000.00, "04/07/2025", 38500.00, False, "CB1"),
    cb("40.0000", "SOL", "04/09/2025", 4480.00, "09/18/2025", 9800.00, False, "CB2"),
    cb("6.00000000", "ETH", "04/22/2025", 10680.00, "08/22/2025", 28200.00, False, "CB3"),
    cb("0.50000000", "BTC", "04/18/2025", 42250.00, "10/06/2025", 62000.00, False, "CB4"),
    cb("1.25000000", "BTC", "03/02/2021", 60625.00, "07/14/2025", 150000.00, True, "CB5"),
    cb("0.60000000", "BTC", "11/10/2022", 10200.00, "10/06/2025", 74400.00, True, "CB6"),
    cb("2.00000000", "ETH", "06/20/2022", 2300.00, "08/22/2025", 9400.00, True, "CB7"),
]
# 8.0 ETH bought 04/22/2025 @1,780 on Coinbase: 6.0 sold on Coinbase (CB3); 2.0 sent to MetaMask 08/23/2025 (NOT a sale), swapped 08/24
ETH_LOT_BASIS_2 = round((14240.00 + round(14240.00 * FEE, 2)) * 2 / 8, 2)
COINBASE[2]["cost"], COINBASE[2]["buy_fee"] = 10680.00, round(round(14240.00 * FEE, 2) * 6 / 8, 2)
COINBASE[2]["basis"] = round(COINBASE[2]["cost"] + COINBASE[2]["buy_fee"], 2)
METAMASK = [
    {"id": "MM1", "asset": "2.0 ETH -> 8,900 USDC (Uniswap swap)", "acq": "04/22/2025", "sold": "08/24/2025",
     "gross": 8900.00, "sale_fee": 14.20, "net": 8885.80, "basis": ETH_LOT_BASIS_2, "lt": False, "collectible": False},
    {"id": "MM2", "asset": "NFT 'Chromatic Drift #214' (digital art) sold for 3.9 ETH", "acq": "02/05/2023", "sold": "11/12/2025",
     "gross": 12285.00, "sale_fee": round(12285 * 0.025, 2) + 9.10, "basis": 2970.00 + 22.40, "lt": True, "collectible": True},
]
METAMASK[1]["net"] = round(METAMASK[1]["gross"] - METAMASK[1]["sale_fee"], 2)
ROBINHOOD = [
    {"id": "RH1", "desc": "20 sh TSLA", "acq": "01/21/2025", "sold": "03/10/2025", "proceeds": 4440.00, "basis": 8400.00, "wash": 3960.00, "box": "A"},
    {"id": "RH2", "desc": "20 sh TSLA (replacement shares; basis incl. wash-sale adj.)", "acq": "03/24/2025", "sold": "06/30/2025",
     "proceeds": 6340.00, "basis": 8680.00, "wash": 0.0, "box": "A"},
    {"id": "RH3", "desc": "25 sh VTI", "acq": "02/11/2020", "sold": "09/15/2025", "proceeds": 8050.00, "basis": 4000.00, "wash": 0.0, "box": "D"},
]
DA_TOTAL = round(sum(x["net"] for x in COINBASE), 2)
CL_CB_GROSS = round(sum(x["gross"] for x in COINBASE), 2)
CB_SALE_FEES = round(sum(x["sale_fee"] for x in COINBASE), 2)
assert abs(CL_CB_GROSS - CB_SALE_FEES - DA_TOTAL) < 0.01

trades = []
for x in COINBASE:
    trades.append({"box": "K" if x["lt"] else "H", "id": x["id"], "desc": x["asset"] + " (Coinbase)", "acq": x["acq"], "sold": x["sold"],
                   "proceeds": x["net"], "basis": x["basis"]})
for x in METAMASK:
    trades.append({"box": "L" if x["lt"] else "I", "id": x["id"], "desc": x["asset"] + " (MetaMask - no 1099-DA)", "acq": x["acq"],
                   "sold": x["sold"], "proceeds": x["net"], "basis": x["basis"], "code": "C" if x["collectible"] else "",
                   "collectible": x["collectible"]})
for x in ROBINHOOD:
    trades.append({"box": x["box"], "id": x["id"], "desc": x["desc"] + " (Robinhood)", "acq": x["acq"], "sold": x["sold"],
                   "proceeds": x["proceeds"], "basis": x["basis"], "adj": x["wash"], "code": "W" if x["wash"] else ""})
g = lambda t: t["proceeds"] - t["basis"] + t.get("adj", 0)
ST = round(sum(g(t) for t in trades if t["box"] in "ABCGHI"), 2)
LT = round(sum(g(t) for t in trades if t["box"] in "DEFJKL"), 2)
NFT_GAIN = round(g(trades[len(COINBASE) + 1]), 2)
BTC_LOSS = round(g(trades[0]), 2)
naive_double = DA_TOTAL  # loading 1099-DA with $0 basis on top of CoinLedger = proceeds counted again as gain

KRAKEN_MISC = 1240.00
ONCHAIN_STAKE = 860.44
STAKING = round(KRAKEN_MISC + ONCHAIN_STAKE, 2)
INT = 1850.12
W2 = {"1": 21400.00, "2": 2568.00, "3": 21400.00, "4": 1326.80, "5": 21400.00, "6": 310.30,
      "12": [("DD", 1650.00)], "14": [("PTO PAYOUT", 3900.00)], "control": "HDM-25-0331",
      "state": [{"state": "TN", "id": "(no state income tax)"}]}
EST = [("04/15/2025", 5500.00), ("06/16/2025", 5500.00), ("09/15/2025", 5500.00), ("01/15/2026", 5500.00)]
EXT_PAY = 12000.00
# 1095-A Apr-Dec
M_PREM, M_SLCSP, M_APTC = 468.00, 441.00, 392.00
months = [(0, 0, 0)] * 3 + [(M_PREM, M_SLCSP, M_APTC)] * 9
APTC_TOTAL = round(M_APTC * 9, 2)

# ====================================================================== PBC
F.engagement_letter(C.pbc_file("01_Engagement_Letter_2025_signed.pdf", "Engagement letter (signed)", "2026-01-20", "DocuSign"),
    "Thomas Q. Nguyen", "EVG1011", "Crypto / investor tier $1,600 plus hourly reconciliation time.", "01/20/2026",
    "2025 federal Form 1040 and related schedules (Tennessee has no individual income tax return).")
F.organizer(C.pbc_file("02_2025_Organizer_Nguyen.pdf", "Client organizer", "2026-03-30"), "Thomas Nguyen", "EVG1011",
    general=[("Did your address change during 2025?", "Yes", "Moved to East Nashville June 2025"),
             ("Did you receive, sell, exchange or otherwise dispose of digital assets?", "Yes", "Coinbase/Kraken/MetaMask - CoinLedger report to follow"),
             ("Did you have health coverage through the Marketplace (Form 1095-A)?", "Yes", "Apr-Dec after I quit"),
             ("Do you have an Identity Protection PIN?", "Yes", "Attached my letter"),
             ("Did you make estimated tax payments?", "Yes", "4 x 5,500"),
             ("Are you in the business of trading securities?", "No", "Just investing")],
    dependents=[],
    income_rows=[["Wages", "Harpeth Digital Media", 91250, "see W-2"],
                 ["Interest", "Harpeth Online Bank", 1105, "1,850"],
                 ["Crypto gains", "CoinLedger report", 11860, "coming"],
                 ["Staking income", "Kraken", 740, "see 1099-MISC"],
                 ["Stock sales", "Robinhood", "", "see 1099"]],
    deductions_rows=[["Estimated payments", "IRS Direct Pay", 2000, "22,000"],
                     ["Crypto software / hardware wallet", "CoinLedger sub + Ledger", "", "449"]],
    signature_date="03/28/2026")
F.w2(C.pbc_file("03_W-2_Harpeth_Digital_Media.pdf", "Form W-2", "2026-02-11"),
     {"name": "Harpeth Digital Media, LLC", "addr1": "300 Rep. John Lewis Way N", "addr2": "Nashville, TN 37219", "ein": "00-5091377"},
     {"name": T["name"], "addr1": OLD_ADDR[0], "addr2": OLD_ADDR[1], "ssn": T["ssn"]}, W2)
F.f1099_int(C.pbc_file("04_1099-INT_Harpeth_Online_Bank.pdf", "Form 1099-INT", "2026-02-11"),
            ["Harpeth Online Bank - synthetic", "PO Box 40218", "Nashville, TN 37204", "TIN: 00-0661204"], REC_T, {"1": INT},
            account="HYSA ****7741")
# Coinbase 1099-DA composite
da_rows = [["Sale", "Asset / units (box 1a-1c)", "Date acquired", "Date sold (1e)", "1f Gross proceeds (net of transaction costs)", "1g Cost basis", "Term (box 2)", "Basis reported?"]]
for x in COINBASE:
    da_rows.append([x["id"], x["asset"], "Not reported", x["sold"], x["net"], "Not reported", "Long" if x["lt"] else "Short", "No (2025)"])
da_rows.append(["Total", "", "", "", DA_TOTAL, "", "", ""])
statement(C.pbc_file("05_Coinbase_2025_Form_1099-DA.pdf", "Form 1099-DA (composite)", "2026-02-17"),
    "Coinbase, Inc. - 2025 Form 1099-DA - Digital Asset Proceeds From Broker Transactions (composite statement)", [
        {"table": [["Recipient", f"{T['name']} - TIN {T['ssn']} - {OLD_ADDR[0]}, {OLD_ADDR[1]}"],
                   ["Broker", "Coinbase, Inc. - TIN 00-2804112 (synthetic)"], ["Account", "****c19e"]], "left_align_cols": [0, 1], "header": False},
        {"heading": "Sales and exchanges of digital assets", "table": da_rows, "total_row": True},
        {"note": ["For 2025 brokers report gross proceeds only; cost basis and acquisition dates are not reported to the IRS. "
                  "Gross proceeds are reported net of digital asset transaction costs (fees).",
                  "Transfers of digital assets to wallets or accounts you control ('Sends') are not sales and are not reported on Form 1099-DA.",
                  "Federal income tax withheld (box 4): 0.00"]}])
# Coinbase transaction history CSV (includes Sends)
cb_csv = [["2024-12-16T15:02:11Z", "Buy", "BTC", "0.50000000", "106000.00", "53000.00", "53212.00", "212.00", "Bought 0.5 BTC"]]
for x in COINBASE:
    if x["acq"].endswith("2025"):
        mm, dd, yy = x["acq"].split("/")
        cb_csv.append([f"{yy}-{mm}-{dd}T14:31:40Z", "Buy", x["asset"].split()[1], x["asset"].split()[0], "", f"{x['cost']:.2f}",
                       f"{x['basis']:.2f}", f"{x['buy_fee']:.2f}", "Bought"])
cb_csv[-2] = ["2025-04-22T14:31:40Z", "Buy", "ETH", "8.00000000", "1780.00", "14240.00", f"{14240 + round(14240 * FEE, 2):.2f}",
              f"{round(14240 * FEE, 2):.2f}", "Bought 8 ETH"]
for x in COINBASE:
    mm, dd, yy = x["sold"].split("/")
    cb_csv.append([f"{yy}-{mm}-{dd}T16:05:12Z", "Sell", x["asset"].split()[1], x["asset"].split()[0], "", f"{x['gross']:.2f}",
                   f"{x['net']:.2f}", f"{x['sale_fee']:.2f}", "Sold"])
cb_csv += [["2025-08-23T02:14:55Z", "Send", "ETH", "2.00000000", "", "", "", "0.00", "Sent 2 ETH to 0x7c3a...91be"],
           ["2025-11-02T19:40:03Z", "Send", "ETH", "1.50000000", "", "", "", "0.00", "Sent 1.5 ETH to 0x7c3a...91be"],
           ["2025-05-09T12:00:00Z", "Receive", "ETH", "0.21400000", "", "", "", "0.00", "Received from Kraken (staking rewards withdrawn)"],
           ["2025-12-30T21:10:44Z", "Withdrawal", "USD", "", "", "25000.00", "", "0.00", "Withdrawal to bank ****5582"]]
cb_csv.sort(key=lambda row: row[0])
write_csv(C.pbc_file("06_Coinbase_transaction_history_2025.csv", "Exchange transaction export (CSV)", "2026-02-17"),
          ["Timestamp", "Transaction Type", "Asset", "Quantity", "Spot price (USD)", "Subtotal (USD)", "Total incl. fees (USD)", "Fees (USD)", "Notes"], cb_csv)
F.f1099_misc(C.pbc_file("07_Kraken_2025_Form_1099-MISC.pdf", "Form 1099-MISC", "2026-02-17"),
             ["Payward Interactive, Inc. (Kraken) - synthetic", "PO Box 3048", "Cheyenne, WY 82003", "TIN: 00-4418872"],
             [T["name"], *OLD_ADDR, f"TIN: {T['ssn']}"], {"3": KRAKEN_MISC},
             notes=["Box 3: staking rewards (ETH, SOL) credited to your account in 2025, valued at USD fair market value when credited."])
# Robinhood consolidated
rh_rows = [["Box", "Description", "1b Acquired", "1c Sold", "1d Proceeds", "1e Cost basis", "1g Wash sale loss disallowed", "Gain/(loss)"]]
for x in ROBINHOOD:
    rh_rows.append(["A (ST covered)" if x["box"] == "A" else "D (LT covered)", x["desc"], x["acq"], x["sold"], x["proceeds"], x["basis"],
                    x["wash"] or "", x["proceeds"] - x["basis"] + x["wash"]])
statement(C.pbc_file("08_Robinhood_2025_Consolidated_1099.pdf", "Consolidated 1099 (brokerage)", "2026-02-19"),
    "Robinhood Securities, LLC - 2025 Consolidated Form 1099 - Account ****3316", [
        {"heading": "Form 1099-B - covered securities (basis reported to IRS)", "table": rh_rows},
        {"heading": "Form 1099-DIV / 1099-INT", "para": "Total ordinary dividends 0.00; interest 0.00 (below $10 reporting threshold)."},
        {"note": "Wash sale: 20 sh TSLA sold 03/10/2025 at a loss; 20 sh TSLA purchased 03/24/2025 (within 30 days). The disallowed loss "
                 "($3,960.00) was added to the basis of the replacement shares sold 06/30/2025."}])
F.f1095_a(C.pbc_file("09_Form_1095-A_Marketplace.pdf", "Form 1095-A", "2026-02-03"),
          ["Health Insurance Marketplace (HealthCare.gov) - Tennessee", "Marketplace ID 47-FFM", "Issuer: Volunteer State Health Plan (synthetic)"],
          [T["name"], f"SSN {T['ssn']}", f"DOB {T['dob']}", *OLD_ADDR, "Coverage start 04/01/2025 - end 12/31/2025"], months,
          policy="VSHP-2025-883104")
# CP01A letter (January 2025) - scanned, stale
scanned_pages(C.pbc_file("10_IRS_CP01A_letter_scan.pdf", "IRS notice (scan)", "2026-03-30", "Sharefile upload", "client scan"),
    [["Department of the Treasury  Internal Revenue Service", "", "Notice CP01A          Notice date: January 6, 2025",
      "Tax year: 2024", "", f"THOMAS Q NGUYEN", f"{OLD_ADDR[0].upper()}", f"{OLD_ADDR[1].upper()}", "",
      "Your Identity Protection Personal Identification Number (IP PIN)", "", "Your IP PIN is: 4 8 1 9 3 X",
      "", "Use this IP PIN when filing your 2024 federal tax return during calendar year 2025.",
      "You will receive a new IP PIN each year by mail or you can retrieve it", "in your IRS Online Account.",
      "If you e-file without the correct IP PIN, your return will be rejected.", "", "(synthetic - digits partially masked)"]],
    handwritten=False, skew=-1.1, seed=31)
scanned_pages(C.pbc_file("11_Sticky_note_wallets_photo.pdf", "Photo of handwritten note", "2026-03-30", "Sharefile upload"),
    [["wallets for Coinledger:", "- Coinbase (API linked)", "- Kraken (API) - staking only, no sells",
      "- MetaMask 0x7c3a...91be  <- NOT linked yet!!", "   (uniswap swap Aug, sold the NFT Nov)",
      "", "sold .5 BTC in April at a loss then bought back", "  11 days later -> wash sale?? ask Priya",
      "", "moved 3.5 ETH coinbase -> metamask (my own wallet)"]], handwritten=True, seed=32)
write_text(C.pbc_file("12_IRS_Direct_Pay_confirmations.txt", "Payment confirmations", "2026-03-30"),
    "IRS Direct Pay - payment confirmations (copied from emails)\n\n" +
    "\n".join(f"{d}  Estimated tax (1040ES) tax year 2025  ${a:,.2f}  confirmation EFT-2025-{i:05d}" for i, (d, a) in enumerate(EST, 88100)) +
    f"\n04/14/2026  Extension (Form 4868) payment tax year 2025  ${EXT_PAY:,.2f}  confirmation EFT-2026-04412\n")
write_text(C.pbc_file("13_Email_extension_and_CoinLedger_status_2026-04-10.txt", "Client correspondence", "2026-04-10", "Email"),
"""From: preparer@evergreentax.example
To: Thomas Nguyen <thomas.nguyen@example.com>
Date: Fri, 10 Apr 2026 09:15:22 -0500
Subject: Nguyen 2025 - extension

Thomas - we don't have your final CoinLedger report yet (MetaMask wallet not connected), so we are filing Form 4868.
Based on your preliminary numbers we recommend paying $12,000 with the extension by 04/15/2026 via Direct Pay.
Please send the final CoinLedger Form 8949 (CSV + PDF) and income report once MetaMask is imported.

-----
From: Thomas Nguyen
Date: Mon, 13 Apr 2026 22:47:10 -0500
Subject: RE: Nguyen 2025 - extension

Paying tomorrow. Will get the MetaMask stuff done over the summer, sorry!
""")
# CoinLedger preliminary (Coinbase + Kraken only) - superseded
statement(C.pbc_file("14_CoinLedger_2025_Tax_Report_PRELIMINARY_2026-08-14.pdf", "Crypto tax report (preliminary)", "2026-08-14"),
    "CoinLedger - 2025 Tax Report (PRELIMINARY) - generated 08/14/2026", [
        {"para": "Connected sources: Coinbase (API), Kraken (API). <b>Warning: 2 incoming transfers with missing cost basis; "
                 "1 wallet address referenced in transfers is not connected (0x7c3a...91be).</b>"},
        {"table": [["Summary", "Proceeds", "Cost basis", "Gain/(loss)"],
                   ["Short-term", round(sum(x["gross"] for x in COINBASE if not x["lt"]), 2), round(sum(x["basis"] + x["sale_fee"] for x in COINBASE if not x["lt"]), 2),
                    round(sum(x["net"] - x["basis"] for x in COINBASE if not x["lt"]), 2)],
                   ["Long-term", round(sum(x["gross"] for x in COINBASE if x["lt"]), 2), round(sum(x["basis"] + x["sale_fee"] for x in COINBASE if x["lt"]), 2),
                    round(sum(x["net"] - x["basis"] for x in COINBASE if x["lt"]), 2)],
                   ["Income (staking)", "", "", KRAKEN_MISC]]}])
# CoinLedger FINAL (all wallets) - CSV + PDF + income report, received 09/26/2026
cl_rows = []
for x in COINBASE + METAMASK:
    cl_rows.append([x["asset"].split(" (")[0], x["acq"], x["sold"], f"{x['gross']:.2f}", f"{x['basis'] + x['sale_fee']:.2f}",
                    f"{x['net'] - x['basis']:.2f}", "Long-term" if x["lt"] else "Short-term",
                    "Coinbase" if x["id"].startswith("CB") else "MetaMask (0x7c3a...91be)", "Collectible (NFT)" if x.get("collectible") else ""])
write_csv(C.pbc_file("15_CoinLedger_2025_Form_8949_FINAL.csv", "Crypto tax report - Form 8949 export (CSV)", "2026-09-26", "Sharefile upload",
                     "received 09/26/2026"),
          ["Description", "Date Acquired", "Date Sold", "Proceeds (USD)", "Cost Basis (USD)", "Gain/Loss (USD)", "Holding Period", "Source", "Notes"], cl_rows)
statement(C.pbc_file("16_CoinLedger_2025_Tax_Report_FINAL.pdf", "Crypto tax report (final)", "2026-09-26", "Sharefile upload", "received 09/26/2026"),
    "CoinLedger - 2025 Tax Report (FINAL) - generated 09/25/2026", [
        {"para": "Connected sources: Coinbase (API), Kraken (API), MetaMask 0x7c3a...91be (Ethereum mainnet). No missing cost basis. "
                 "Internal transfers between your own wallets are excluded from gains (Coinbase -> MetaMask: 3.5 ETH). "
                 "In this report, proceeds are shown before the sale fee and the sale fee is included in the cost basis column."},
        {"heading": "Capital gains summary", "table": [["Term", "Proceeds", "Cost basis (incl. fees)", "Gain/(loss)"],
            ["Short-term", round(sum(x["gross"] for x in COINBASE + METAMASK if not x["lt"]), 2),
             round(sum(x["basis"] + x["sale_fee"] for x in COINBASE + METAMASK if not x["lt"]), 2),
             round(sum(x["net"] - x["basis"] for x in COINBASE + METAMASK if not x["lt"]), 2)],
            ["Long-term", round(sum(x["gross"] for x in COINBASE + METAMASK if x["lt"]), 2),
             round(sum(x["basis"] + x["sale_fee"] for x in COINBASE + METAMASK if x["lt"]), 2),
             round(sum(x["net"] - x["basis"] for x in COINBASE + METAMASK if x["lt"]), 2)]]},
        {"heading": "Income report", "table": [["Category", "Source", "USD value at receipt"],
            ["Staking", "Kraken (ETH, SOL)", KRAKEN_MISC], ["Staking", "On-chain ETH staking rewards - MetaMask", ONCHAIN_STAKE],
            ["Total income", "", STAKING]], "total_row": True},
        {"heading": "Wash sales", "para": "Crypto: no wash-sale adjustments applied (report setting: disabled)."},
        {"note": "Stocks held at Robinhood are not included in this report."}])
write_text(C.pbc_file("17_Email_Thomas_final_report_2026-09-26.txt", "Client correspondence", "2026-09-26", "Email"),
"""From: Thomas Nguyen <thomas.nguyen@example.com>
To: preparer@evergreentax.example
Date: Sat, 26 Sep 2026 11:02:48 -0500
Subject: FINAL coinledger report uploaded

Finally got MetaMask imported - final CoinLedger CSV + PDF are on Sharefile. Sorry it's so late.
Also I didn't get a new IP PIN letter this year?? The only one I have is the one I scanned (from last January).
""")
write_text(C.pbc_file("18_Email_IP_PIN_retrieved_2026-09-28.txt", "Client correspondence", "2026-09-28", "Email / phone",
                      "follow-up received"),
"""From: preparer@evergreentax.example
To: Thomas Nguyen
Date: Mon, 28 Sep 2026 08:40:00 -0500
Subject: Re: FINAL coinledger report uploaded

Thomas - the CP01A you scanned is from January 2025 and was for your 2024 return. IP PINs change every year, and the
IRS mailed your 2026 CP01A to your old Demonbreun St address (no Form 8822 on file). Please log in to your IRS Online
Account (Get an IP PIN) and text or call us with the current 6-digit IP PIN - do not email it.
We'll also file Form 8822 with your new address.

-----
[Phone note - P. Anand, 09/28/2026 14:12] Client read current IP PIN from IRS Online Account (stored in Axcess e-file
screen, masked ****27). Form 8822 prepared for client signature.
""")
statement(C.pbc_file("19_Ledger_hardware_wallet_receipt.pdf", "Purchase receipt", "2026-03-30"),
    "Order confirmation - hardware wallet (synthetic)", [
        {"table": [["Item", "Date", "Amount"], ["Hardware wallet + shipping", "05/02/2025", 150.00],
                   ["CoinLedger annual plan (receipt forwarded)", "08/14/2026", 299.00]]}])

# ====================================================================== RETURN
nii = r(INT) + r(STAKING) + r(ST + LT)
facts = {
    "status": "S", "taxpayer": {"age65": False},
    "w2": [{"who": "T", "box1": W2["1"], "box2": W2["2"], "box3": W2["3"], "box4": W2["4"], "box5": W2["5"], "box6": W2["6"]}],
    "interest": [{"payer": "Harpeth Online Bank", "amount": INT}],
    "trades": trades,
    "sch1": {"other": [("8v", f"Digital assets received as ordinary income not reported elsewhere (staking: Kraken 1099-MISC ${KRAKEN_MISC:,.2f} "
                              f"+ on-chain ${ONCHAIN_STAKE:,.2f})", STAKING)]},
    "niit": {"nii": nii, "gross": nii},
    "estimated_payments": sum(a for _, a in EST),
    "extension_payment": EXT_PAY,
}
R0 = Return1040(facts).compute()
# Form 8962: household income = MAGI (AGI; no tax-exempt interest / foreign exclusions / nontaxable SS)
FPL_2024_1 = 15060
magi = R0.values["11"]
fpl_pct = magi / FPL_2024_1
assert fpl_pct >= 4.0
app_fig = 0.085
annual_contrib = r(magi * app_fig)
monthly_contrib = round(annual_contrib / 12, 2)
ptc_months = [max(0.0, min(p, s - monthly_contrib)) if p else 0.0 for p, s, a in months]
PTC_ALLOWED = r(sum(ptc_months))
EXCESS = r(APTC_TOTAL - PTC_ALLOWED)
assert PTC_ALLOWED == 0 and EXCESS == r(APTC_TOTAL)
facts["excess_aptc"] = EXCESS
R = Return1040(facts).compute()
v = R.values
assert v["11"] == magi
sdd = v["sch_d"]
assert v["niit"] == r(0.038 * min(nii, v["11"] - 200000))
assert sdd["g28"] == r(NFT_GAIN)

f8962 = [["Form 8962 - Premium Tax Credit (Apr-Dec marketplace coverage)", "Amount"],
         ["Line 1 Tax family size", 1], ["Line 2a Modified AGI", magi], ["Line 3 Household income", magi],
         ["Line 4 Federal poverty line (2024 guideline, 1 person, 48 states)", FPL_2024_1],
         ["Line 5 Household income as % of FPL", f"{fpl_pct*100:,.0f}%"],
         ["Line 7 Applicable figure (400% FPL and above - 2025 enhanced PTC)", "0.0850"],
         ["Line 8a Annual contribution for health care", annual_contrib], ["Line 8b Monthly contribution", monthly_contrib],
         ["Lines 12-23 (Apr-Dec): monthly premium / SLCSP / APTC", f"{M_PREM:,.2f} / {M_SLCSP:,.2f} / {M_APTC:,.2f}"],
         ["Lines 12-23 column (e): SLCSP less monthly contribution -> PTC allowed each month", 0],
         ["Line 24 Total premium tax credit", PTC_ALLOWED], ["Line 25 Advance payments of PTC (1095-A)", APTC_TOTAL],
         ["Line 27 Excess advance premium tax credit", EXCESS],
         ["Line 28 Repayment limitation (household income >= 400% FPL - no limit)", "N/A"],
         ["Line 29 Excess APTC repayment (to Schedule 2, line 2)", EXCESS]]
recon = [["1099-DA reconciliation (Coinbase) - CoinLedger vs broker", "Amount"],
         ["CoinLedger Coinbase proceeds (before sale fees)", CL_CB_GROSS],
         ["Less: sale fees (CoinLedger includes them in cost basis)", -CB_SALE_FEES],
         ["= Coinbase 1099-DA gross proceeds (net of transaction costs) - reported on 8949 boxes H/K", DA_TOTAL],
         ["Difference", 0],
         ["MetaMask disposals (no 1099-DA) - 8949 boxes I/L", round(sum(x["net"] for x in METAMASK), 2)],
         ["Coinbase 'Send' 3.5 ETH to own MetaMask wallet (08/23, 11/02) - self-transfer, not a disposition", 0],
         ["Coinbase 'Receive' from Kraken (own account) - not income (rewards already counted when credited)", 0],
         ["Draft error avoided: 1099-DA + CoinLedger both loaded -> proceeds double-counted (1099-DA basis blank = $0)", naive_double]]
C.write_return(R, [
    ("Taxpayer", f"{T['name']} ({T['ssn']}), DOB 10/08/1992"),
    ("Address", ", ".join(ADDR) + " (Form 8822 change of address filed with return package)"),
    ("Filing status", "Single"),
    ("Digital assets question", "YES"),
    ("Forms included", "1040, Schedules 1, 2, 3, B (no), D, Forms 8949 (boxes A, D, H, I, K, L), 8960, 8962"),
    ("Identity Protection PIN", "Entered - current IP PIN retrieved from IRS Online Account 09/28/2026 (stale 01/2025 CP01A not used)"),
    ("State", "None - Tennessee has no individual income tax"),
    ("Extension", "Form 4868 filed 04/14/2026 with $12,000 payment; extended due date 10/15/2026"),
    ("Filing method", "E-file (Form 8879 signed 09/28/2026; transmitted 09/29/2026 after 24-hour hold); refund by direct deposit ****5582"),
], attachments=[("Form 8962 - Premium Tax Credit", f8962), ("Digital asset reconciliation (1099-DA vs CoinLedger)", recon)])

# ====================================================================== ANSWER KEY
gotchas = [
    gotcha("EVG1011-G1", "Schedule D - CoinLedger-provided Forms 8949 vs Consolidated 1099 / 1099-DA", "1099-DA and CoinLedger both loaded",
           f"Autoflow imports the Coinbase 1099-DA (basis blank -> $0) AND the CoinLedger 8949 -> Coinbase sales counted twice, "
           f"~{fmt(naive_double)} of extra gain.",
           "Use the CoinLedger detail (all wallets) as the 8949 source; do not load the 1099-DA separately. Reconcile CoinLedger's Coinbase "
           f"proceeds {fmt(CL_CB_GROSS)} less sale fees {fmt(CB_SALE_FEES)} = 1099-DA {fmt(DA_TOTAL)}; report Coinbase sales in 8949 box H/K "
           "(1099-DA received, basis not reported) and MetaMask disposals in box I/L (no 1099-DA).",
           "Line 7 overstated by the 1099-DA proceeds", ["7"], "hard"),
    gotcha("EVG1011-G2", "E-File Rejects - IP PIN changes every year", "Stale IP PIN",
           "Enter the IP PIN from the January 2025 CP01A in the PBC (for the 2024 return).",
           "IP PINs are valid for one calendar year. The 2026 CP01A went to his old address; the current IP PIN was retrieved from the IRS "
           "Online Account (09/28/2026). Using the old PIN rejects the e-file (IP PIN mismatch reject - IND-181/IND-183 family). Also file Form 8822.",
           "E-file reject; late filing if not caught before 10/15", [], "medium"),
    gotcha("EVG1011-G3", "Scan - exchange CSV exports (self-transfers)", "Coinbase 'Send' rows treated as sales",
           "Treat the 3.5 ETH sent to MetaMask as dispositions (or as withdrawals of income).",
           "Transfers between wallets the taxpayer controls are not taxable; basis and holding period carry over (CoinLedger tracks the 2.0 ETH "
           "later swapped on Uniswap with its 04/22/2025 basis).", "Line 7", ["7"], "easy"),
    gotcha("EVG1011-G4", "Sch 1 line 8v - staking income", "Kraken 1099-MISC double-counted",
           f"Report the $1,240 1099-MISC AND the CoinLedger income total ${STAKING:,.2f} -> ${KRAKEN_MISC + STAKING:,.2f}.",
           f"CoinLedger's staking total already includes the Kraken rewards. Report ${STAKING:,.2f} once on Schedule 1 line 8v (ordinary income "
           "at FMV when received - Rev. Rul. 2023-14; not SE income for an investor). It is also net investment income.",
           f"Line 8 overstated ${KRAKEN_MISC:,.0f} if missed", ["8"], "medium"),
    gotcha("EVG1011-G5", "Schedule D - adjustment codes (C collectibles, W wash sale)", "Wash sale rule and crypto; NFT collectible",
           f"Disallow the {fmt(-BTC_LOSS)} BTC loss (repurchased 11 days later) as a wash sale; or treat the NFT gain as ordinary 15%/20% LTCG; "
           "or ignore Robinhood's 1g wash-sale amount.",
           "Section 1091 applies to stock or securities - not to digital assets in 2025 -> BTC loss fully allowed. The Robinhood TSLA wash sale "
           "(code W, $3,960) IS applied as reported. The NFT is digital art -> collectible (Notice 2023-27 look-through) -> 28% rate gain "
           f"{fmt(NFT_GAIN)} (8949 code C; Sch D line 18).", "Line 16 tax", ["7", "16"], "hard"),
    gotcha("EVG1011-G6", "Form 8962 - excess APTC", "Advance PTC based on $36k projected income",
           "Omit Form 8962 (no 1095-A input) or cap repayment at the table amount.",
           f"Household income {fmt(magi)} = {fpl_pct*100:,.0f}% of FPL. At 8.5% the monthly contribution {fmt(monthly_contrib)} exceeds the SLCSP "
           f"(${M_SLCSP:,.0f}) -> PTC $0 every month; repay ALL APTC {fmt(EXCESS)} (no repayment cap at/above 400% FPL) on Schedule 2 line 2.",
           f"Tax understated {fmt(EXCESS)}", ["17"], "medium"),
    gotcha("EVG1011-G7", "NIIT", "NIIT limited by MAGI over threshold",
           f"3.8% x all net investment income {fmt(nii)} = {fmt(r(nii * 0.038))}; or no NIIT because wages are low.",
           f"NIIT = 3.8% x lesser of NII {fmt(nii)} or MAGI over $200,000 ({fmt(v['11'] - 200000)}) = {fmt(v['niit'])}.",
           "Schedule 2 line 12", ["23"], "easy"),
    gotcha("EVG1011-G8", "Billing - expedite fee / Investor vs trader", "Late documents and non-deductible investor costs",
           "Deduct CoinLedger subscription / hardware wallet on Schedule C or Schedule A; skip the 15% expedite fee.",
           "Investor (not a trader): no Schedule C; investment expenses are miscellaneous itemized deductions - suspended (permanently after OBBBA). "
           "Final CoinLedger report received 09/26/2026, within 15 days of 10/15/2026 -> 15% expedited processing fee per engagement letter.",
           "Billing / deductions", [], "easy"),
]
C.write_answer_key(R, {"residence": "TN (no state income tax return)", "complexity": "Crypto investor, 1099-DA, PTC repayment, IP PIN"},
                   gotchas, state=[{"jurisdiction": "Tennessee", "return": "None (no individual income tax; Hall tax repealed 2021)"}],
                   filings=[{"form": "Form 4868", "filed": "2026-04-14", "payment": EXT_PAY},
                            {"form": "Form 1040 (federal)", "method": "e-file with IP PIN", "due": "2026-10-15 (extended)",
                             "filed": "2026-09-29 (transmitted; acknowledgment pending)"},
                            {"form": "Form 8822 (change of address)", "method": "paper (mail)", "filed": "2026-09-29"}])
C.write_receipt_log("EVG1011-1040-2025", "P. Anand (staff)", "L. Chen (senior)", "S. Kennedy, CPA", "2026-01-20",
                    extension="Filed 04/14/2026 with $12,000 payment (extended due date 10/15/2026)",
                    extra="Final CoinLedger report received 09/26/2026 - within 15 days of the 10/15/2026 extended deadline.")
tot_fee = 1600 + 4 * 185
C.write_notes(f"""
# EVG1011 - Nguyen, Thomas - 2025 Form 1040 - Preparer Notes

*Synthetic client - Project Evergreen. Return status: **signed off 09/28/2026; transmitted 09/29/2026 (acknowledgment pending).***

## Return summary
| | |
|---|---|
| Filing status | Single |
| Wages / interest / staking | {fmt(W2['1'])} / {fmt(v['2b'])} / {fmt(STAKING)} (Sch 1 line 8v) |
| Capital gains (line 7) | {fmt(v['7'])} = ST {fmt(sdd['net_st'])} + LT {fmt(sdd['net_lt'])} (incl. 28% collectible NFT gain {fmt(sdd['g28'])}) |
| AGI (line 11) | {fmt(v['11'])} |
| Standard deduction | {fmt(v['12e'])} |
| Taxable income | {fmt(v['15'])} |
| Tax (line 16) | {fmt(v['16'])} |
| Excess APTC repayment (Sch 2 line 2) | {fmt(EXCESS)} |
| NIIT (Sch 2 line 12) | {fmt(v['niit'])} |
| Total tax (line 24) | {fmt(v['24'])} |
| Payments | withholding {fmt(v['25d'])} + estimates {fmt(v['26'])} + extension {fmt(EXT_PAY)} |
| **{'Refund' if v['refund'] else 'Balance due'}** | **{fmt(v['refund'] or v['balance_due'])}** |

## What I did and why (plain English)
1. **Investor, not trader.** Thomas made ~12 disposals across the year and held most positions for months or years; no business
   activity -> investor. Everything goes on Form 8949 / Schedule D; no Schedule C, no 475(f) mark-to-market. His CoinLedger subscription
   and hardware wallet are investment expenses (miscellaneous itemized deductions) - not deductible.
2. **Which crypto source to use.** The Coinbase 1099-DA reports gross proceeds only (no basis in 2025). The final CoinLedger report
   covers Coinbase, Kraken and his MetaMask wallet with full basis. I used **only the CoinLedger detail** and did not load the 1099-DA
   (loading both would count {fmt(DA_TOTAL)} of Coinbase proceeds twice, the second time with $0 basis). Reconciliation: CoinLedger's
   Coinbase proceeds {fmt(CL_CB_GROSS)} are before sale fees and it puts the {fmt(CB_SALE_FEES)} of fees in cost basis; the 1099-DA
   reports proceeds net of fees. Same gain either way; I reported the 1099-DA proceeds figures so the IRS match ties.
   - Coinbase sales -> 8949 **box H** (short-term) / **box K** (long-term): "reported on Form 1099-DA, basis not reported".
   - MetaMask disposals (Uniswap swap, NFT sale) -> **box I / box L**: no 1099-DA.
   - Robinhood stock sales -> box A / box D (covered, basis reported).
3. **Self-transfers.** Coinbase shows "Send" 2.0 ETH (08/23) and 1.5 ETH (11/02) to 0x7c3a...91be - that is his own MetaMask wallet
   (per his note and the CoinLedger wallet list). Not sales. The 2.0 ETH swapped for USDC on 08/24 keeps its 04/22/2025 Coinbase
   basis ({fmt(ETH_LOT_BASIS_2)}).
4. **BTC loss and "wash sale".** He sold 0.5 BTC at a {fmt(-BTC_LOSS)} loss on 04/07 and rebought 0.5 BTC on 04/18. The wash-sale rule
   (sec. 1091) covers stock and securities; crypto is property, not a security, for 2025 -> **loss allowed**. His Robinhood TSLA sale on
   03/10 IS a wash sale (replacement bought 03/24): Robinhood disallowed $3,960 (box 1g) and added it to the replacement shares'
   basis - reported with code W as the broker did.
5. **NFT = collectible.** The NFT is digital art; under Notice 2023-27's look-through approach an NFT whose associated asset is a
   work of art is a collectible. Held > 1 year -> 28%-rate gain {fmt(NFT_GAIN)} (8949 code C, Schedule D line 18).
6. **Staking.** Kraken 1099-MISC box 3 $1,240.00 is part of CoinLedger's income report ($1,240.00 Kraken + $860.44 on-chain =
   {fmt(STAKING)}). Reported once on Schedule 1 line 8v at FMV when received (Rev. Rul. 2023-14). Not self-employment income.
7. **NIIT.** Net investment income {fmt(nii)} (interest, staking, net gains) but MAGI exceeds $200,000 by only {fmt(v['11'] - 200000)}
   -> 3.8% x {fmt(v['11'] - 200000)} = {fmt(v['niit'])}.
8. **Premium tax credit (Form 8962).** Marketplace plan Apr-Dec with APTC {fmt(APTC_TOTAL)} based on the $36,000 income he projected
   when he quit. Actual household income {fmt(magi)} = {fpl_pct*100:,.0f}% of the 2024 FPL ($15,060). 2025 still has the enhanced PTC
   (no 400% cliff), but at 8.5% his monthly contribution ({fmt(monthly_contrib)}) exceeds the benchmark plan ($441) -> PTC $0 each month.
   Above 400% FPL there is no repayment cap -> repay all {fmt(EXCESS)} (Schedule 2 line 2).
9. **IP PIN.** He is in the IP PIN program. The CP01A he scanned is dated 01/06/2025 - that PIN was for the 2024 return. The 2026 letter
   was mailed to his old address. He retrieved the current PIN from his IRS Online Account on 09/28 (phone, not email). Entered on the
   e-file screen. Using the stale PIN would reject the return. Form 8822 prepared for his new address.
10. **Estimated tax / extension.** Estimates {fmt(v['26'])} (4 x $5,500, timely) + extension payment $12,000 (04/14/2026). Form 2210:
    2024 AGI $104,955 (< $150,000) -> safe harbor is 100% of 2024 tax $14,212; timely withholding + estimates exceed $3,553 per quarter
    -> no penalty. Refund results; no late-payment penalty or interest since the full tax was paid by 04/15/2026.
11. **Tennessee.** No individual income tax (Hall tax on interest/dividends repealed from 2021) - no state return.

## Open items / client communication
- Acknowledgment for the 09/29/2026 transmission pending - monitor; if rejected, follow E-File Rejects procedure (document reason,
  save updated return, retransmit before 10/15/2026).
- Form 8822 mailed with his signature. Remind him: new IP PIN each January (Online Account).
- 2026: brokers start reporting crypto cost basis on 1099-DA for covered assets - keep CoinLedger connected to all wallets.

## Hand-off to signer / routing
- [x] Return locked; Accountant's copy saved as *reviewed*
- [x] Federal 1040 - e-file with current IP PIN; no state; no FBAR (no foreign accounts - Kraken/Coinbase are US entities)
- [x] Extended due date 10/15/2026 populated
- [x] eSign (Form 8879) - client prefers text/email; 24-hour ELF hold observed before transmission
- [x] Form 8822 (paper) - special processing instruction for Admin
- Billing: crypto tier $1,600 + 4.0 hrs reconciliation (1099-DA / CoinLedger / Robinhood) = ${tot_fee:,}; **15% expedite fee** (final
  CoinLedger report received 09/26/2026, within 15 days of 10/15) = ${r(tot_fee * 0.15):,}; total ${r(tot_fee * 1.15):,}. Time spent
  chasing the missing MetaMask import is client-chargeable (external reason).
""")
C.write_review_points(f"""
# Review Points - EVG1011 - 2025 - Form 1040

*Reviewer: L. Chen (blue). Preparer responses in red. Synthetic.*

1. **Form 8949** - Autoflow loaded the Coinbase 1099-DA ({fmt(DA_TOTAL)}, basis blank) AND the CoinLedger 8949 -> Schedule D gain overstated
   by the full 1099-DA proceeds.
   - Delete the 1099-DA import; use CoinLedger detail only. Tie CoinLedger Coinbase proceeds to the 1099-DA (fees).
   - Boxes: Coinbase = H/K, MetaMask = I/L. Draft had everything in box C/F.
   - *Preparer: Done - reconciliation attached to the return; difference = sale fees {fmt(CB_SALE_FEES)}.*
2. **Form 8949 / CoinLedger preliminary report** - Draft still had the 08/14 PRELIMINARY report (no MetaMask). Replace with FINAL (09/26).
   - *Preparer: Replaced; MetaMask swap and NFT now included.*
3. **Schedule 1 line 8v** - Draft had $1,240 (1099-MISC) + {fmt(STAKING)} (CoinLedger). Kraken is inside the CoinLedger total.
   - *Preparer: Corrected to {fmt(STAKING)}.*
4. **Wash sale** - Draft disallowed the April BTC loss ({fmt(-BTC_LOSS)}). Crypto is not subject to sec. 1091 in 2025 - allow it. Keep the Robinhood W adjustment.
   - *Preparer: Loss allowed.*
5. **Schedule D line 18** - NFT digital art is a collectible - 28% rate gain. Confirm code C.
   - *Preparer: Code C entered; line 18 {fmt(sdd['g28'])}.*
6. **Form 8962** - 1095-A was not entered in the draft. Household income > 400% FPL -> full repayment, no cap.
   - *Preparer: 8962 added; excess APTC {fmt(EXCESS)}.*
7. **E-file / IP PIN** - The CP01A in the PBC is for the 2024 return. Get the 2026 IP PIN before transmitting (IND-181/183 rejects).
   Do not accept it by email.
   - *Preparer: Retrieved by phone 09/28; entered; Form 8822 prepared.*
8. FYI - Expedite fee applies (final docs 09/26). Note in billing.
""")
print("EVG1011 done", R.summary()["24"], v["refund"], v["balance_due"], "AGI", v["11"])
