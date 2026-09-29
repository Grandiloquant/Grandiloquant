"""EVG1015 - Rajesh & Anita Iyer (MFJ, Washington - Redmond). Indian-born US tax residents: NRE interest taxable in the US
(Indian fiscal-year certificates -> calendar year), NRO interest with 31.2% TDS -> FTC limited to the 15% treaty rate on
Form 1116 (de minimis election not available), FBAR, Form 8938, PFIC Form 8621 (Indian mutual funds), Form 3520 Part IV
(gift from nonresident-alien father), NRA parents are not dependents, Additional Medicare + NIIT. Extended return."""
from common import ClientBuild, gotcha, fmt
from docs import statement, scanned_pages, write_text, write_xlsx
import forms as F
from tax2025 import Return1040, r

C = ClientBuild("EVG1015", "Iyer", "Rajesh & Anita Iyer")
ADDR = ("16420 NE 95th St", "Redmond, WA 98052")
TP = {"name": "Rajesh V. Iyer", "ssn": "XXX-XX-2231", "dob": "1986-02-14"}
SP = {"name": "Anita K. Iyer", "ssn": "XXX-XX-7719", "dob": "1988-09-30"}
REC_T = [TP["name"], *ADDR, f"TIN: {TP['ssn']}"]
REC_S = [SP["name"], *ADDR, f"TIN: {SP['ssn']}"]
REC_J = ["Rajesh V. Iyer & Anita K. Iyer", *ADDR, f"TIN: {TP['ssn']}"]
FX_AVG = 87.147     # IRS yearly average currency exchange rate 2025 (INR per USD)
FX_YE = 89.870      # ASSUMED Treasury Reporting Rate of Exchange at 12/31/2025 (INR per USD) - verify against the published table
TREATY_RATE = .15   # US-India income tax treaty, Art. 11(2) - interest beneficially owned by a US resident (non-bank)

# ------------------------------------------------------------------ PERM
C.write_profile(f"""
# EVG1015 - Iyer, Rajesh & Anita  (PERM)

*Synthetic client - Project Evergreen training data.*

| Item | Detail |
|---|---|
| Client ID | EVG1015 (new client for TY2025; engaged 03/2026) |
| Taxpayer | Rajesh V. Iyer, DOB 02/14/1986, SSN XXX-XX-2231, citizen of India. US lawful permanent resident (green card) since 06/2022 (H-1B 2016-2022). Principal Software Engineer, Cascadia Cloud Systems Inc. |
| Spouse | Anita K. Iyer (nee Krishnan), DOB 09/30/1988, SSN XXX-XX-7719, citizen of India. Green card 06/2022 (H-4/H-1B before). Data Science Manager, Pinegrove Health Analytics LLC |
| US tax residency | Both resident aliens for all of 2025 (green card test); treaty tie-breaker not claimed - permanent home and all employment in the US |
| Dependent | Vikram R. Iyer, son, DOB 06/05/2019, SSN XXX-XX-4408, US citizen |
| Address | {ADDR[0]}, {ADDR[1]} (King County) - **Washington: no individual income tax** |
| Foreign | India (see FBAR schedule in WP): HDFC Bank NRE savings + NRE fixed deposits; SBI NRO savings + NRO FD; three Indian mutual funds (CAMS/KFintech folios, growth option) - all joint. PAN on file for both. |
| Parents (not dependents) | Anita's parents Srinivasan & Lakshmi Krishnan - Indian citizens/residents (Chennai), visited 04/05-09/28/2025 on B-2 visas |
| Contact | Rajesh preferred - rajesh.iyer@example.com, (425) 555-0133; eSign OK |
| Engagement | International tier - quote $3,400 (1040 + 1116 + 8938 + 3 x 8621 + 3520 + FBAR). PY returns self-prepared (TurboTax). |
| Payment info | Refunds to Chase checking ****2046 |
""")
F.prior_year_summary(C.perm_file("2024_Form_1040_Return_Summary_TurboTax.pdf", "Prior-year return summary (client self-prepared)"),
    "Rajesh & Anita Iyer", "EVG1015", "Married filing jointly", [
        ["1a", "W-2 wages (Cascadia Cloud; Pinegrove Health)", 318400],
        ["2b", "Taxable interest - Chase $212; 'India NRO interest' $2,020", 2232],
        ["11", "AGI", 320632], ["12", "Standard deduction", 29200], ["15", "Taxable income", 291432],
        ["19", "Child tax credit", 2000], ["Sch 3 1", "Foreign tax credit (claimed without Form 1116)", 628],
        ["Sch 2 11", "Additional Medicare Tax", 612], ["24", "Total tax", 55190], ["35a", "Refund", 2311],
        ["Sch B 7a", "Foreign account: Yes / FBAR: Yes / India", ""]],
    notes="Summary from client's TurboTax PDF (not prepared by Evergreen). Observed at intake: NRE interest NOT reported; FTC "
          "claimed at full 31.2% TDS; no Form 8938 or 8621 filed; FBAR filed (copy in PBC). Refer to signer re: prior-year "
          "exposure (amend 2023-2024 / consider streamlined domestic offshore procedures) - separate CONS project.")

# ------------------------------------------------------------------ PBC documents
EMP_T = {"name": "Cascadia Cloud Systems Inc.", "addr1": "15700 NE 39th St", "addr2": "Redmond, WA 98052", "ein": "00-9120447"}
EMP_S = {"name": "Pinegrove Health Analytics LLC", "addr1": "1201 3rd Ave Ste 2200", "addr2": "Seattle, WA 98101", "ein": "00-6618830"}
EE_T = {"name": TP["name"], "addr1": ADDR[0], "addr2": ADDR[1], "ssn": TP["ssn"]}
EE_S = {"name": SP["name"], "addr1": ADDR[0], "addr2": ADDR[1], "ssn": SP["ssn"]}
g_t, g_s = 213500.00, 173500.00
w2_t = {"1": g_t - 23500, "2": 36000.00, "3": 176100.00, "4": 10918.20, "5": g_t, "6": round(g_t * .0145 + (g_t - 200000) * .009, 2),
        "12": [("D", 23500.00), ("DD", 18240.00)], "13": ["Retirement plan: X"],
        "14": [("WA PFML", 1167.08), ("WA CARES", 1238.30)], "control": "CCS-77310"}
w2_s = {"1": g_s - 23500, "2": 26500.00, "3": g_s, "4": round(g_s * .062, 2), "5": g_s, "6": round(g_s * .0145, 2),
        "12": [("D", 23500.00), ("DD", 16910.00)], "13": ["Retirement plan: X"],
        "14": [("WA PFML", 948.42), ("WA CARES", 1006.30)], "control": "PHA-4415"}

F.organizer(C.pbc_file("01_2025_Organizer_Iyer.pdf", "Client organizer", "2026-03-18"), "Rajesh & Anita Iyer", "EVG1015",
    general=[("Did your marital status change during 2025?", "No", ""),
             ("Did anyone else live with you / did you support anyone?", "Yes", "Anita's parents Apr-Sep - we paid everything"),
             ("Do you have foreign bank / investment accounts?", "Yes", "India - same as every year (we file FBAR)"),
             ("Did you receive a gift or inheritance from a foreign person?", "Yes", "Anita's dad sent money for our house fund"),
             ("Do you own foreign mutual funds or foreign stock?", "Yes", "Indian MFs from before we moved - no sales"),
             ("Did you pay foreign taxes?", "Yes", "TDS on NRO interest"),
             ("Did you make estimated tax payments?", "No", ""),
             ("Did you receive, sell, exchange digital assets?", "No", "")],
    dependents=[["Vikram R. Iyer", "Son", "06/05/2019", "4408", "12", "No"],
                ["Srinivasan Krishnan", "Father-in-law", "03/11/1956", "none (ITIN?)", "6", "No"],
                ["Lakshmi Krishnan", "Mother-in-law", "08/22/1959", "none (ITIN?)", "6", "No"]],
    income_rows=[["Wages", "Cascadia Cloud Systems Inc. (Rajesh)", 175600, "see W-2"],
                 ["Wages", "Pinegrove Health Analytics LLC (Anita)", 142800, "see W-2"],
                 ["Interest", "JPMorgan Chase Bank", 212, "1,642"],
                 ["Interest", "India - SBI NRO", 2020, "see certificate"],
                 ["Interest", "India - HDFC NRE", "", "tax free in India - not needed?"]],
    deductions_rows=[["Foreign tax paid", "TDS on NRO interest", 628, "see Form 16A"]],
    signature_date="03/15/2026")

F.w2(C.pbc_file("02_W-2_Cascadia_Cloud_Rajesh.pdf", "Form W-2", "2026-03-18"), EMP_T, EE_T, w2_t)
F.w2(C.pbc_file("03_W-2_Pinegrove_Health_Anita.pdf", "Form W-2", "2026-03-18"), EMP_S, EE_S, w2_s)
CHASE_INT = 1642.18
F.f1099_int(C.pbc_file("04_1099-INT_Chase.pdf", "Form 1099-INT", "2026-03-18"),
            ["JPMorgan Chase Bank, N.A.", "PO Box 659754", "San Antonio, TX 78265", "TIN: 00-0000001"], REC_T, {"1": CHASE_INT},
            account="Premier Savings ****8813")

# India - quarterly interest credits (INR). Indian certificates run on the Indian fiscal year (April-March).
NRE_Q = {"2024Q2": 98000, "2024Q3": 99500, "2024Q4": 100500, "2025Q1": 102000, "2025Q2": 104500, "2025Q3": 106000,
         "2025Q4": 107500, "2026Q1": 108000}
NRO_Q = {"2024Q2": 42500, "2024Q3": 43000, "2024Q4": 43500, "2025Q1": 44000, "2025Q2": 45000, "2025Q3": 45500,
         "2025Q4": 45500, "2026Q1": 46000}
TDS = .312
CY = ["2025Q1", "2025Q2", "2025Q3", "2025Q4"]
QLBL = {"2024Q2": "Apr-Jun 2024", "2024Q3": "Jul-Sep 2024", "2024Q4": "Oct-Dec 2024", "2025Q1": "Jan-Mar 2025",
        "2025Q2": "Apr-Jun 2025", "2025Q3": "Jul-Sep 2025", "2025Q4": "Oct-Dec 2025", "2026Q1": "Jan-Mar 2026"}
FY1 = ["2024Q2", "2024Q3", "2024Q4", "2025Q1"]
FY2 = ["2025Q2", "2025Q3", "2025Q4", "2026Q1"]
nre_cy_inr = sum(NRE_Q[q] for q in CY)
nro_cy_inr = sum(NRO_Q[q] for q in CY)
tds_cy_inr = sum(round(NRO_Q[q] * TDS) for q in CY)
nre_usd = nre_cy_inr / FX_AVG
nro_usd = nro_cy_inr / FX_AVG
tds_usd = tds_cy_inr / FX_AVG
treaty_tax_inr = nro_cy_inr * TREATY_RATE
ftc_usd = treaty_tax_inr / FX_AVG
excess_tds_inr = tds_cy_inr - treaty_tax_inr


def cert(fname, recv, bank, acct, kind, qs, fy, tds=False, note=""):
    rows = [["Quarter", "Interest credited (INR)"] + (["TDS deducted @31.2% (INR)"] if tds else [])]
    for q in qs:
        amt = (NRE_Q if kind == "NRE" else NRO_Q)[q]
        rows.append([QLBL[q], f"{amt:,.0f}"] + ([f"{round(amt * TDS):,.0f}"] if tds else []))
    tot = sum((NRE_Q if kind == "NRE" else NRO_Q)[q] for q in qs)
    rows.append(["Total FY " + fy, f"{tot:,.0f}"] + ([f"{sum(round((NRO_Q)[q] * TDS) for q in qs):,.0f}"] if tds else []))
    statement(C.pbc_file(fname, "Foreign bank interest certificate", recv, "Client email attachment" if recv > "2026-04" else "Sharefile upload"),
              f"{bank} - Interest Certificate - Financial Year {fy} (1 April - 31 March)", [
                  {"table": [["Field", "Detail"], ["Account holders", "Rajesh Venkat Iyer / Anita Krishnan Iyer (joint)"],
                             ["Account", acct], ["Account type", kind + (" (Non-Resident External - repatriable)" if kind == "NRE" else
                                                                         " (Non-Resident Ordinary)")],
                             ["PAN", "XXXXX1234X / XXXXX5678X"]], "left_align_cols": [0, 1]},
                  {"table": rows, "total_row": True},
                  {"para": note}])


cert("05_HDFC_NRE_Interest_Certificate_FY2024-25.pdf", "2026-03-18", "HDFC Bank Ltd (synthetic)", "NRE SB ****1180 + NRE FDs ****1180-FD01/02",
     "NRE", FY1, "2024-25", note="Interest on NRE deposits is exempt from Indian income tax under section 10(4)(ii) of the Income-tax "
                                 "Act, 1961. No TDS deducted.")
cert("06_SBI_NRO_Interest_Certificate_and_Form16A_FY2024-25.pdf", "2026-03-18", "State Bank of India (synthetic)",
     "NRO SB ****0457 + NRO FD ****0457-FD1", "NRO", FY1, "2024-25", tds=True,
     note="TDS under section 195 at 30% + 4% Health & Education Cess = 31.2% (no Form 10F / Tax Residency Certificate on file for "
          "treaty rate). Form 16A certificates for Q1-Q4 FY 2024-25 attached (TAN XXXX12345X).")
mf = [("Sahyadri Bluechip Equity Fund - Direct Plan - Growth", "SBE/88104512", "2017-08-10", 41250.110, 69.82, 2950000),
      ("Narmada Flexi Cap Fund - Regular Plan - Growth", "NFC/40517733", "2018-02-19", 30012.448, 84.63, 2610000),
      ("Kaveri Short Duration Debt Fund - Direct - Growth", "KSD/77120918", "2019-01-07", 36860.071, 29.30, 1160000)]
mf_rows = [["Scheme", "Folio", "First purchase", "Units 31-Dec-2025", "NAV 31-Dec-2025 (INR)", "Market value (INR)", "Transactions 2025"]]
MF_YE_INR = 0
for n, fo, acq, u, nav, mx in mf:
    val = round(u * nav)
    MF_YE_INR += val
    mf_rows.append([n, fo, acq, f"{u:,.3f}", f"{nav:,.2f}", f"{val:,.0f}", "None (no purchase / redemption / dividend)"])
mf_rows.append(["Total", "", "", "", "", f"{MF_YE_INR:,.0f}", ""])
statement(C.pbc_file("07_CAMS_KFintech_Consolidated_Account_Statement_Dec2025.pdf", "Foreign investment statement", "2026-03-18"),
    "Consolidated Account Statement (CAS) - Mutual Fund Holdings - 01-Jan-2025 to 31-Dec-2025 (synthetic)", [
        {"para": "Investor: Rajesh Venkat Iyer (first holder) / Anita Krishnan Iyer (joint holder). Mode of holding: Joint. "
                 "Option: Growth (no IDCW / dividend payouts)."},
        {"table": mf_rows, "total_row": True},
        {"para": "Capital gains statement for the period: NIL redemptions."}], landscape_mode=True)
GIFT_INR, GIFT_USD, GIFT_DATE = 13000000, 150812.53, "06/18/2025"
statement(C.pbc_file("08_Chase_Incoming_Wire_Advice_2025-06-18.pdf", "Bank wire advice", "2026-03-18"),
    "JPMorgan Chase Bank - Incoming International Wire - Advice of Credit", [
        {"table": [["Field", "Detail"], ["Value date", GIFT_DATE], ["Beneficiary", "Rajesh V. Iyer / Anita K. Iyer (joint) - Premier Savings ****8813"],
                   ["Ordering customer", "SRINIVASAN KRISHNAN, CHENNAI 600020 INDIA"],
                   ["Ordering bank", "STATE BANK OF INDIA, ADYAR BRANCH (SBININBB)"],
                   ["Original amount", "INR 13,000,000.00"], ["Exchange rate applied", "86.2000"],
                   ["USD credited", GIFT_USD], ["Remittance info", "GIFT TO DAUGHTER - FAMILY MAINTENANCE / HOUSE"],
                   ["Purpose code (India LRS)", "S1301 - remittance for family maintenance"]], "left_align_cols": [0, 1]}])
scanned_pages(C.pbc_file("09_Gift_letter_from_S_Krishnan.pdf", "Handwritten letter (scan)", "2026-03-18"),
    [["Chennai, 2 June 2025",
      "",
      "To whom it may concern,",
      "",
      "I, Srinivasan Krishnan, resident of Chennai, India,",
      "am sending Rs. 1,30,00,000 (One crore thirty lakh)",
      "to my daughter Anita as a GIFT out of love and",
      "affection, for purchase of a home. This is not a",
      "loan and need not be repaid. No trust is created.",
      "",
      "Funds are from my own savings (SBI Adyar).",
      "",
      "             - S. Krishnan   (signature)",
      "  Passport no. Z-XXXXXX1   PAN XXXXX9911X"]], handwritten=True, seed=1515)
write_text(C.pbc_file("10_Email_Rajesh_2026-03-18.txt", "Client correspondence", "2026-03-18", "Email"),
"""From: Rajesh Iyer <rajesh.iyer@example.com>
To: preparer@evergreentax.example
Date: Wed, 18 Mar 2026 22:47:19 -0700
Subject: Iyer 2025 - documents

Hello, thank you for taking us on. A few notes:
- NRE interest is tax free in India so I don't think it goes on the US return (we never reported it before).
- NRO interest - bank deducts 31.2% TDS, please claim full credit like last year.
- Anita's father gifted us Rs 1.3 crore in June for our house down payment. Gifts are not taxable, right?
  Do we need to show it anywhere?
- Anita's parents stayed with us April to end of September. We paid all their expenses (flights, medical,
  food). Can we claim them as dependents? They don't have SSNs - can we get ITINs?
- Indian mutual funds: no sales, just holding. Value is about Rs 65 lakh.
We will need an extension - the FY 2025-26 bank certificates only come in April/May.
Regards, Rajesh
""")
scanned_pages(C.pbc_file("11_Krishnan_I-94_travel_history.pdf", "Scanned travel record", "2026-03-18"),
    [["U.S. Customs and Border Protection - I-94 Travel History (printout)",
      "Name: KRISHNAN, SRINIVASAN   Country of citizenship: INDIA",
      "  Date        Type       Location",
      "  2025-09-28  Departure  SEA",
      "  2025-04-05  Arrival    SEA   Class of admission: B2",
      "  (no prior U.S. travel in 2023 or 2024)",
      "",
      "Name: KRISHNAN, LAKSHMI     Country of citizenship: INDIA",
      "  2025-09-28  Departure  SEA",
      "  2025-04-05  Arrival    SEA   Class of admission: B2",
      "  (no prior U.S. travel in 2023 or 2024)"]], handwritten=False, seed=1516)
statement(C.pbc_file("12_FBAR_2024_filed_copy.pdf", "Prior-year FBAR (client filed)", "2026-03-18"),
    "FinCEN Form 114 - Calendar Year 2024 - BSA E-Filing confirmation (client filed 04/12/2025)", [
        {"table": [["Part", "Financial institution", "Account", "Type", "Max value (USD) reported"],
                   ["III (joint)", "HDFC Bank Ltd", "****1180", "Bank", 38100], ["III (joint)", "HDFC Bank Ltd", "****1180-FD01/02", "Bank", 59800],
                   ["III (joint)", "State Bank of India", "****0457", "Bank", 6900], ["III (joint)", "State Bank of India", "****0457-FD1", "Bank", 28700]],
         "left_align_cols": [0, 1, 2, 3]},
        {"para": "Note: 2024 FBAR did not list the mutual fund folios (CAMS/KFintech)."}])
statement(C.pbc_file("13_UIDAI_Aadhaar_PAN_link_confirmation.pdf", "Other document", "2026-03-18", note="included in upload"),
    "Income Tax Department (India) - Aadhaar-PAN Link Status (printout)", [
        {"para": "Your PAN XXXXX1234X is already linked to given Aadhaar XXXX XXXX 5521. (Printout supplied by client - no tax data.)"}])
# follow-up docs after extension
cert("14_HDFC_NRE_Interest_Certificate_FY2025-26.pdf", "2026-08-11", "HDFC Bank Ltd (synthetic)", "NRE SB ****1180 + NRE FDs ****1180-FD01/02",
     "NRE", FY2, "2025-26", note="Interest on NRE deposits is exempt from Indian income tax under section 10(4)(ii). No TDS deducted.")
cert("15_SBI_NRO_Interest_Certificate_and_Form16A_FY2025-26.pdf", "2026-08-11", "State Bank of India (synthetic)",
     "NRO SB ****0457 + NRO FD ****0457-FD1", "NRO", FY2, "2025-26", tds=True,
     note="TDS under section 195 at 30% + 4% cess = 31.2%. Form 16A certificates Q1-Q4 FY 2025-26 attached.")
fbar_accts = [  # institution, acct, type, max INR, 12/31 INR
    ("HDFC Bank Ltd, Mumbai", "NRE SB ****1180", "Bank", 3480000, 3212000),
    ("HDFC Bank Ltd, Mumbai", "NRE FD ****1180-FD01/02", "Bank", 5000000, 5000000),
    ("State Bank of India, Chennai", "NRO SB ****0457", "Bank", 612000, 398500),
    ("State Bank of India, Chennai", "NRO FD ****0457-FD1", "Bank", 2400000, 2400000),
] + [(f"{n.split(' - ')[0]} (AMC; RTA CAMS/KFintech)", f"Folio {fo}", "Securities/Other (mutual fund)", mx, round(u * nav))
     for n, fo, acq, u, nav, mx in mf]
write_xlsx(C.pbc_file("16_Rajesh_India_accounts_max_balances_2025.xlsx", "Spreadsheet (client-prepared)", "2026-08-11",
                      "Client email attachment", "requested by preparer 07/28"),
           {"Max balances 2025": [["Institution", "Account", "Type", "Max balance 2025 (INR)", "Balance 31-Dec-2025 (INR)"]] +
                                 [[a, b, c, d, e] for a, b, c, d, e in fbar_accts]})

# ------------------------------------------------------------------ RETURN
wages_total = w2_t["1"] + w2_s["1"]
facts = {
    "status": "MFJ",
    "taxpayer": {}, "spouse": {},
    "dependents": [{"name": "Vikram R. Iyer", "ctc": True}],
    "w2": [{"who": "T", "box1": w2_t["1"], "box2": w2_t["2"], "box3": w2_t["3"], "box4": w2_t["4"], "box5": w2_t["5"], "box6": w2_t["6"]},
           {"who": "S", "box1": w2_s["1"], "box2": w2_s["2"], "box3": w2_s["3"], "box4": w2_s["4"], "box5": w2_s["5"], "box6": w2_s["6"]}],
    "interest": [{"payer": "JPMorgan Chase Bank, N.A.", "amount": CHASE_INT},
                 {"payer": f"HDFC Bank Ltd, India - NRE deposits (INR {nre_cy_inr:,} / {FX_AVG})", "amount": nre_usd},
                 {"payer": f"State Bank of India - NRO deposits (INR {nro_cy_inr:,} / {FX_AVG})", "amount": nro_usd}],
    "foreign_accounts": True, "foreign_account_country": "India",
    "niit": {},
    "extension_payment": 0,
}
total_int = CHASE_INT + nre_usd + nro_usd
facts["niit"] = {"nii": total_int, "gross": total_int}
# Form 1116 (passive): foreign-source gross income less apportioned standard deduction
foreign_gross = nre_usd + nro_usd
gross_all = wages_total + total_int
std_apportioned = 31500 * foreign_gross / gross_all
fsti = foreign_gross - std_apportioned
facts["ftc"] = {"method": "1116", "taxes": ftc_usd, "foreign_source_ti": fsti, "category": "passive"}
R = Return1040(facts).compute()
v = R.values
f1116_limit = v["16"] * fsti / v["15"]

# FBAR / 8938 values at the 12/31/2025 Treasury rate
fbar_rows = [["#", "Financial institution (India)", "Account", "Type", "Max value 2025 (INR)", "Max value (USD @ 89.870)", "12/31/2025 (USD)"]]
fbar_max_usd = 0
ye_usd = 0
for i, (inst, acct, typ, mx, ye) in enumerate(fbar_accts, 1):
    fbar_rows.append([str(i), inst, acct, typ, f"{mx:,.0f}", r(mx / FX_YE), r(ye / FX_YE)])
    fbar_max_usd += mx / FX_YE
    ye_usd += ye / FX_YE
fbar_rows.append(["", "Aggregate (all jointly owned - one FBAR by Rajesh; Anita signs Form 114a)", "", "", "", r(fbar_max_usd), r(ye_usd)])
mf_ye_usd = MF_YE_INR / FX_YE
f8621 = [["Form 8621 (one per fund) - Part I, section 1291 fund, no elections", "Folio", "Acquired", "Units", "Value 12/31/2025 (USD)", "Line 2 box"]]
for n, fo, acq, u, nav, mx in mf:
    f8621.append([n, fo, acq, f"{u:,.3f}", r(u * nav / FX_YE), "(a) $0-50,000"])
f8621.append([f"Aggregate PFIC value {fmt(mf_ye_usd)} > $50,000 (MFJ annual-filing exemption, Reg. 1.1298-1(c)(2)(i)(A)) -> "
              "Part I filing required for each fund. Part V: no distributions, no dispositions -> no excess distribution, no "
              "section 1291 tax or interest. No QEF (no PFIC Annual Information Statement) / no MTM election made (see notes).",
              "", "", "", "", ""])
f8938 = [["Form 8938 - MFJ living in US: threshold $100,000 at year end or $150,000 at any time", "Amount (USD)"],
         ["Part V - 4 deposit accounts (HDFC NRE SB, NRE FD; SBI NRO SB, NRO FD) - max value", r(sum(a[3] for a in fbar_accts[:4]) / FX_YE)],
         ["Part VI / Part IV - 3 mutual fund holdings (PFICs; reported on Form 8621 - counted toward threshold, "
          "excepted from duplicate detail: 'Number of Forms 8621: 3')", r(sum(a[3] for a in fbar_accts[4:]) / FX_YE)],
         ["Total value at 12/31/2025 (all specified foreign financial assets)", r(ye_usd)],
         ["Part III - income from these assets: interest (Sch B) - NRE + NRO", r(foreign_gross)],
         ["Part III - foreign tax credited (Form 1116)", r(ftc_usd)],
         ["Exchange rate: Treasury Reporting Rate 12/31/2025, INR 89.870 per USD (assumed - see notes)", ""]]
f1116 = [["Form 1116 - passive category income - India", "INR", "USD"],
         [f"NRE interest - calendar 2025 (Q1 from FY24-25 cert + Q2-Q4 from FY25-26 cert) @ {FX_AVG}", f"{nre_cy_inr:,}", r(nre_usd)],
         [f"NRO interest - calendar 2025 @ {FX_AVG}", f"{nro_cy_inr:,}", r(nro_usd)],
         ["Line 1a gross foreign-source income", "", r(foreign_gross)],
         [f"Line 3a standard deduction apportioned: 31,500 x {r(foreign_gross):,} / {r(gross_all):,} gross income", "", r(std_apportioned)],
         ["Line 7 net foreign-source taxable income", "", r(fsti)],
         ["TDS actually withheld on NRO interest @ 31.2% (Form 16A)", f"{tds_cy_inr:,}", r(tds_usd)],
         ["Creditable: limited to US-India treaty rate 15% (Art. 11(2)) - Reg. 1.901-2(e)(5)", f"{r(treaty_tax_inr):,}", r(ftc_usd)],
         ["Excess TDS (not a creditable tax - refund claim in India via ITR / Form 10F + TRC)", f"{r(excess_tds_inr):,}", r(excess_tds_inr / FX_AVG)],
         ["Line 21 limitation: US tax x (FSTI / taxable income)", "", r(f1116_limit)],
         ["Line 33 / Schedule 3 line 1 foreign tax credit", "", v.get("ftc", 0)],
         ["De minimis election (no Form 1116) NOT available: Indian bank income is not reported on a qualified payee statement", "", ""]]
f3520 = [["Form 3520 Part IV - gifts from a nonresident alien individual (lines 54-55)", "Detail"],
         ["Filer", "Anita K. Iyer, jointly with spouse Rajesh V. Iyer (joint 1040 filers)"],
         ["Line 54 date / description / FMV", f"{GIFT_DATE} - cash wire INR 13,000,000 from father (Srinivasan Krishnan, India) - "
                                             f"${GIFT_USD:,.2f} (USD actually credited)"],
         ["Threshold", "More than $100,000 from a nonresident alien individual -> reporting required (not income)"],
         ["Due date / filing", "Due with the 2025 income tax return including extensions (10/15/2026); mailed separately to IRS Ogden "
                               "(not part of the e-file) - certified mail 09/23/2026"],
         ["Penalty if not filed", "5% of the gift per month, up to 25% (IRC 6039F)"]]
C.write_return(R, [
    ("Taxpayer / Spouse", "Rajesh V. Iyer (XXX-XX-2231) / Anita K. Iyer (XXX-XX-7719) - resident aliens (green card)"),
    ("Address", ", ".join(ADDR)),
    ("Filing status", "Married filing jointly"),
    ("Dependents", "Vikram R. Iyer (son, 2019) - CTC. Anita's parents NOT dependents (nonresident aliens, not US/Canada/Mexico residents)"),
    ("Digital assets question", "No"),
    ("Forms included", "1040, Schedules 2, 3, B (Part III: Yes / India), 8812, Form 1116 (passive), Form 8938, Form 8621 x 3, "
                       "Form 8959, Form 8960. Separately: Form 3520 (mail), FinCEN 114 (BSA E-Filing)"),
    ("Extension", "Form 4868 filed 04/10/2026 (no payment - refund expected)"),
    ("State", "None - Washington has no individual income tax (no WA capital gains excise - no sales)"),
    ("Filing method", "E-file 1040 (8879 signed 09/21/2026), accepted 09/23/2026; direct deposit Chase ****2046"),
], attachments=[("Form 1116 detail - foreign tax credit (passive, India)", f1116),
                ("FinCEN Form 114 (FBAR) - 2025 - accounts and maximum values", fbar_rows),
                ("Form 8938 - Statement of Specified Foreign Financial Assets", f8938),
                ("Form 8621 - PFIC annual information (3 Indian mutual funds)", f8621),
                ("Form 3520 - Part IV foreign gift (filed separately)", f3520)])

gotchas = [
    gotcha("EVG1015-G1", "Foreign Transactions (foreign income / FX conversion)", "NRE interest is tax-free in India - client never reported it",
           "Omit NRE interest (organizer says 'tax free in India').",
           f"US residents are taxed on worldwide income; the Indian section 10(4)(ii) exemption is irrelevant. Report INR {nre_cy_inr:,} "
           f"/ {FX_AVG} = {fmt(nre_usd)} on Schedule B. Flag 2024 omission to signer (amend / streamlined).",
           f"Interest understated {fmt(nre_usd)}", ["2b", "Sch B"], "medium"),
    gotcha("EVG1015-G2", "Foreign Transactions (use IRS rates; foreign-currency amounts)", "Indian certificates are on the April-March fiscal year",
           "Use the FY 2024-25 certificate totals (INR 400,000 NRE / 173,000 NRO) as 2025 income.",
           "Build calendar-2025 interest from quarterly credits: Q1 from the FY24-25 certificate + Q2-Q4 from the FY25-26 certificate "
           f"(NRE INR {nre_cy_inr:,}; NRO INR {nro_cy_inr:,}; TDS INR {tds_cy_inr:,}). Convert at the IRS 2025 average {FX_AVG}.",
           "Wrong income and FTC amounts", ["2b", "Form 1116"], "hard"),
    gotcha("EVG1015-G3", "Foreign Transactions - Form 1116", "TDS withheld at 31.2% but treaty rate on interest is 15%",
           f"Claim the full TDS {fmt(tds_usd)} as a credit (as the client did in 2024).",
           f"Only the tax legally owed under the US-India treaty (15%) is a compulsory, creditable tax (Reg. 1.901-2(e)(5)): "
           f"INR {r(treaty_tax_inr):,} = {fmt(ftc_usd)}. Excess INR {r(excess_tds_inr):,} is refundable from India (ITR + Form 10F/TRC) - not creditable.",
           f"FTC overstated {fmt(tds_usd - ftc_usd)}", ["20", "Sch 3 1"], "hard"),
    gotcha("EVG1015-G4", "Foreign Transactions - Form 1116 (procedure's $600 MFJ print-skip)", "De minimis election is not available",
           "Foreign tax under $600 MFJ -> claim directly on Schedule 3 without Form 1116 (procedure shortcut).",
           "The election also requires all foreign income to be passive AND reported on a qualified payee statement (1099-INT/DIV, K-1). "
           "Indian bank certificates / Form 16A are not -> Form 1116 (passive) required. Procedure imprecise - law followed.",
           "Form 1116 missing", ["Form 1116"], "medium"),
    gotcha("EVG1015-G5", "FinCEN114/FBAR", "Mutual fund folios omitted; wrong exchange rate",
           "Repeat the 2024 FBAR (4 bank accounts) and convert at the IRS yearly average rate.",
           f"Report all 7 accounts (incl. 3 mutual fund folios - 'other financial accounts') at maximum value converted at the "
           f"Treasury 12/31/2025 rate (INR {FX_YE}). Aggregate max {fmt(fbar_max_usd)}. Joint accounts -> one FBAR + Form 114a. Due 10/15/2026 (automatic).",
           "Non-willful FBAR penalty exposure", ["FBAR"], "medium"),
    gotcha("EVG1015-G6", "Foreign Transactions (Form 8938)", "FBAR filed so 8938 'not needed'",
           "Skip Form 8938 because the FBAR covers the accounts.",
           f"Separate requirement. MFJ living in US: year-end value {fmt(ye_usd)} > $100,000 -> Form 8938 attached to the 1040; "
           "PFIC holdings counted toward the threshold and listed as excepted (3 Forms 8621).", "$10,000 penalty exposure", ["Form 8938"], "medium"),
    gotcha("EVG1015-G7", "PFICs (Form 8621)", "Indian mutual funds (growth option, no sales) are PFICs",
           "No income, no sale -> nothing to report.",
           f"Each fund is a PFIC. Aggregate value {fmt(mf_ye_usd)} > $50,000 MFJ exemption -> annual Form 8621 (Part I, section 1291 fund, "
           "no excess distribution) for each of the 3 funds. Recommend MTM (section 1296) discussion; QEF not available.",
           "Unfiled 8621s keep the statute open (6501(c)(8))", ["Form 8621"], "hard"),
    gotcha("EVG1015-G8", "Foreign Trusts (Form 3520)", "INR 1.3 crore gift from a nonresident-alien parent",
           "Either report it as income, or ignore it because gifts are not taxable.",
           f"Not income, but gifts > $100,000 from a nonresident alien individual require Form 3520 Part IV (${GIFT_USD:,.0f} credited "
           "06/18/2025). Due 10/15/2026 with the extension; mailed separately. Penalty up to 25% of the gift.",
           "Up to ~$37,700 penalty", ["Form 3520"], "medium"),
    gotcha("EVG1015-G9", "Review - dependents / Filing Status", "Parents lived with them 6 months, fully supported",
           "Claim both parents as qualifying relatives ($500 ODC each) and apply for ITINs.",
           "Dependents must be US citizens, nationals, or residents of the US, Canada or Mexico. Parents are Indian residents; 177 days "
           "in the US on B-2 (< 183, no prior-year days) -> nonresident aliens. No ODC. (Additional Medicare {} and NIIT {} also apply - "
           "combined wages > $250,000; NII = all interest incl. foreign.)".format(fmt(v['23'] - v.get('niit', 0)), fmt(v.get('niit', 0))),
           "ODC overstated $1,000", ["19"], "easy"),
]
C.write_answer_key(R, {"residence": "WA - Redmond (no state income tax)", "complexity": "International tier"}, gotchas,
                   filings=[{"form": "Form 4868", "filed": "2026-04-10", "payment": 0},
                            {"form": "Form 1040 incl. 1116, 8938, 8621 x3", "method": "e-file", "due": "2026-10-15", "filed": "2026-09-22"},
                            {"form": "Form 3520 (Part IV)", "method": "paper - IRS Ogden, certified mail", "due": "2026-10-15", "filed": "2026-09-23"},
                            {"form": "FinCEN 114 (FBAR) + Form 114a", "method": "BSA E-Filing", "due": "2026-10-15 (automatic extension)", "filed": "2026-09-22"}],
                   extra={"fx": {"irs_2025_average_inr": FX_AVG, "treasury_12_31_2025_inr_assumed": FX_YE},
                          "foreign_income_usd": {"nre": r(nre_usd), "nro": r(nro_usd)},
                          "ftc": {"tds_withheld_usd": r(tds_usd), "treaty_limited_usd": r(ftc_usd)},
                          "fbar_aggregate_max_usd": r(fbar_max_usd), "form8938_year_end_usd": r(ye_usd),
                          "pfic_aggregate_usd": r(mf_ye_usd), "gift_3520_usd": GIFT_USD})

C.write_receipt_log("EVG1015-1040-2025", "P. Nwosu (staff)", "D. Morgan (manager)", "S. Kennedy, CPA", "2026-03-18",
                    extension="Filed 04/10/2026 - FY 2025-26 Indian interest certificates outstanding; no payment (refund expected)")
C.write_notes(f"""
# EVG1015 - Iyer, Rajesh & Anita - 2025 Form 1040 - Preparer Notes

*Synthetic client - Project Evergreen. Return status: **signed off; extended return e-filed 09/22/2026 (accepted 09/23);
Form 3520 mailed 09/23/2026; FBAR filed 09/22/2026.***

## Return summary
| | |
|---|---|
| Filing status | Married filing jointly (both resident aliens - green card) |
| Wages | {fmt(v['1a'])} |
| Interest | {fmt(v['2b'])} (Chase {fmt(CHASE_INT)}, NRE {fmt(nre_usd)}, NRO {fmt(nro_usd)}) |
| AGI (line 11) | {fmt(v['11'])} |
| Deduction | Standard {fmt(v['12e'])} |
| Taxable income | {fmt(v['15'])} |
| Tax (line 16) | {fmt(v['16'])} |
| Credits | CTC {fmt(v['19'])} (Vikram) + foreign tax credit {fmt(v.get('ftc', 0))} |
| Other taxes | Additional Medicare + NIIT {fmt(v['23'])} (NIIT {fmt(v.get('niit', 0))}) |
| Total tax | {fmt(v['24'])} |
| Withholding (incl. 8959 line 24) | {fmt(v['25d'])} |
| **Refund** | **{fmt(v['refund'])}** |

## What I did and why (plain English)
1. **Residency.** Both have green cards (since 2022) -> US residents taxed on worldwide income. No treaty tie-breaker
   position (home, jobs, child all in the US).
2. **Indian interest - calendar year, not Indian FY.** Indian certificates run April-March. I took Jan-Mar 2025 from the
   FY 2024-25 certificates and Apr-Dec 2025 from the FY 2025-26 certificates (received 08/11/2026 - main reason for the
   extension). Calendar 2025: NRE INR {nre_cy_inr:,}; NRO INR {nro_cy_inr:,}; TDS INR {tds_cy_inr:,}. Converted at the
   IRS 2025 yearly average rate **{FX_AVG} INR/USD**: NRE {fmt(nre_usd)}, NRO {fmt(nro_usd)}.
3. **NRE interest is taxable in the US.** It is exempt in India (s.10(4)(ii)), but that has no effect on US tax. It was left off
   the 2024 (and earlier) self-prepared returns - flagged to signer below.
4. **Foreign tax credit (Form 1116, passive).** SBI withheld TDS at 31.2% because no Form 10F/TRC was given. Under the US-India
   treaty (Art. 11(2)) India may tax interest paid to a US resident at no more than 15%. Tax paid above the treaty rate is not a
   compulsory payment (Reg. 1.901-2(e)(5)) and is not creditable - it should be reclaimed from India. Creditable tax =
   15% x INR {nro_cy_inr:,} = INR {r(treaty_tax_inr):,} = **{fmt(ftc_usd)}**; excess INR {r(excess_tds_inr):,} ({fmt(excess_tds_inr / FX_AVG)})
   is a refund claim in India. *Translation note:* TDS was withheld quarterly; I used the yearly average rate as a reasonable
   approximation of the payment-date rates (difference is a few dollars). **Form 1116 is required** even though the credit
   is under $600: the de minimis election needs all foreign income to be reported on a qualified payee statement
   (1099/K-1), which Indian certificates are not. (The procedure's "$600 MFJ - skip the 1116" shortcut is imprecise; the
   law was followed.) Limitation {fmt(f1116_limit)} >> credit, so the full {fmt(ftc_usd)} is allowed.
5. **Gift from Anita's father (Form 3520 Part IV).** INR 1.3 crore wired 06/18/2025 - Chase credited **${GIFT_USD:,.2f}** (the
   actual USD received is the value). A gift is not income, but gifts over $100,000 from a nonresident alien individual must
   be reported on Form 3520 Part IV. Filed jointly (joint 1040 filers), due with the extended return 10/15/2026, **mailed
   separately to IRS Ogden** by certified mail on 09/23/2026 (it cannot be e-filed with the 1040). The money sits in a US
   account, so it is not a foreign account.
6. **FBAR.** Aggregate balances far exceed $10,000. Reported all **7** accounts - the 4 bank accounts from the 2024 FBAR plus the
   3 mutual fund folios (mutual fund accounts are "other financial accounts" - the 2024 FBAR missed them). Maximum values
   converted at the Treasury Reporting Rate for 12/31/2025, **assumed INR {FX_YE}/USD** (verify against the published
   Treasury table; the FBAR rule is the 12/31 Treasury rate, not the IRS average). Aggregate max {fmt(fbar_max_usd)}. All
   accounts are joint, so Rajesh filed one FBAR with Anita's Form 114a. Due 04/15 with automatic extension to 10/15/2026.
7. **Form 8938.** MFJ living in the US: threshold $100,000 at year end / $150,000 at any time. Year-end value {fmt(ye_usd)}
   -> required. The FBAR does not satisfy 8938. Mutual funds count toward the threshold but are listed as excepted assets
   (3 Forms 8621).
8. **PFICs (Form 8621 x 3).** Indian mutual funds are foreign corporations with passive income -> PFICs. Growth option, no
   distributions, no redemptions in 2025 -> no excess distribution and no tax, but aggregate PFIC value {fmt(mf_ye_usd)}
   exceeds the $50,000 MFJ exemption, so an annual Part I filing is required for each fund (section 1291 funds). When they
   redeem, gains are taxed under the excess-distribution regime (top rate + interest charge back to 2019-2022 when their
   holding periods as US persons began). **Recommend a planning call on the section 1296 mark-to-market election** (funds have
   a published daily NAV and are redeemable - treated as marketable) vs. an orderly exit; QEF is not practical (Indian AMCs do
   not issue PFIC Annual Information Statements).
9. **Parents are not dependents.** Organizer listed them and Rajesh asked about ITINs. A dependent must be a US citizen/national
   or a resident of the US, Canada or Mexico. They are Indian residents; I-94 shows 177 days in the US (04/05-09/28) with no
   2023/2024 presence -> substantial presence test not met -> nonresident aliens. No ODC, no ITIN applications.
10. **Additional Medicare / NIIT.** Neither W-2 alone passes $200,000 for full withholding; combined Medicare wages {fmt(g_t + g_s)}
    exceed the $250,000 MFJ threshold -> Form 8959 tax {fmt(r((g_t + g_s - 250000) * .009))} less Cascadia's $122 withheld
    (line 25c). MAGI {fmt(v['11'])} > $250,000 -> NIIT 3.8% on all interest (foreign interest included) = {fmt(v.get('niit', 0))}.
    The FTC cannot offset NIIT.
11. **CTC.** Vikram (6) -> $2,200; AGI below $400,000, no phase-out. No child care expenses claimed.
12. **Washington.** No individual income tax; no capital gains excise (no sales). WA PFML / WA Cares in box 14 are not deductible.

## Open items / client communication
- **Prior years (signer decision - CONS project opened):** 2023-2024 returns omitted NRE interest (~$4,500/yr), over-claimed FTC,
  and omitted Forms 8938/8621; 2024 FBAR omitted MF folios. Options: amend 2022-2024 + late 8938/8621/FBAR with reasonable-cause
  statements, or Streamlined Domestic Offshore Procedures (5% miscellaneous offshore penalty). Engagement letter for the
  remediation to be sent separately; not included in this bill.
- Client to file an Indian ITR for FY 2025-26 claiming refund of excess TDS, and give SBI Form 10F + US Form 6166 (TRC) so
  2026 TDS is withheld at 15%. If India refunds the excess later, no US adjustment needed (it was never credited).
- PFIC MTM election discussion scheduled (must be made on a timely filed 2026 return if elected).

## Hand-off to signer / routing
- [x] Return locked; Accountant's copy saved as *reviewed*
- [x] Federal 1040 (with 1116, 8938, 8621 x 3) - e-file; due 10/15/2026 (extended) - accepted 09/23/2026
- [x] **Form 3520** - paper, mailed separately to IRS Ogden 09/23/2026, certified mail (tracking in WP); due 10/15/2026
- [x] **FinCEN 114 (FBAR)** - BSA E-Filing 09/22/2026 with Form 114a; due 10/15/2026 (automatic extension)
- [x] No state return (WA)
- [x] eSign 8879 - Rajesh by email
- Billing: international tier $3,400 (1040, 1116, 8938, 8621 x 3, 3520, FBAR). Prior-year remediation -> separate CONS
  project / MISC, time left in WIP.
""")
C.write_review_points(f"""
# Review Points - EVG1015 - 2025 - Form 1040

*Reviewer: D. Morgan (blue). Preparer responses in red. Synthetic.*

1. **Schedule B / WP 5-6** - Draft used the FY 2024-25 certificate totals (Apr 2024-Mar 2025) and left out NRE interest.
   - Rebuild calendar 2025 from the quarterly credits (need FY 2025-26 certificates - request from client).
   - NRE interest is US-taxable. Convert at the IRS 2025 average ({FX_AVG}).
   - *Preparer: FY 2025-26 certificates received 08/11. NRE {fmt(nre_usd)} + NRO {fmt(nro_usd)} now on Sch B.*
2. **Schedule 3 line 1** - Draft claimed {fmt(tds_usd)} with no Form 1116 (following the $600 MFJ procedure shortcut).
   - Two problems: (a) de minimis election not available - no qualified payee statement; (b) credit limited to 15% treaty rate.
   - *Preparer: Form 1116 (passive) prepared; credit {fmt(ftc_usd)}. Excess TDS noted as India refund claim.*
3. **Dependents** - Draft had both parents as ODC dependents with "ITIN pending".
   - Not US/Canada/Mexico residents - remove. Keep the I-94 printout in the WP.
   - *Preparer: Removed.*
4. **FBAR** - Draft FBAR copied the 2024 list and used 87.147. Mutual fund folios are reportable; use the 12/31 Treasury rate.
   - *Preparer: 7 accounts; rate {FX_YE} (documented as assumption pending tie-out to the Treasury table).*
5. **Form 8938 / 8621** - Not in draft. Year-end foreign assets {fmt(ye_usd)}; PFIC aggregate {fmt(mf_ye_usd)}.
   - *Preparer: 8938 and three 8621s added (Part I only; no elections).*
6. **Form 3520** - Gift of INR 1.3 crore - need Part IV; confirm USD amount from the wire advice, not the average rate.
   - *Preparer: ${GIFT_USD:,.2f} per Chase advice. Paper-filed separately.*
7. FYI - Additional Medicare: make sure 8959 picks up Cascadia's $122 withheld (line 24 -> 1040 line 25c). NIIT includes foreign interest.
   - *Preparer: Confirmed.*
8. **Signer note** - prior-year exposure memo drafted for S. Kennedy (see Preparer Notes open items).
   - *Preparer: Memo saved to CONS folder; client meeting to be scheduled after filing.*
""")
print("EVG1015 done", R.summary()["24"], v["refund"], v["balance_due"], "ftc", v.get("ftc"), "niit", v.get("niit"))
