"""EVG1025 - Victor & Lena Brennan-Ochoa (MFJ, Texas - Houston).
Irish CFC with GILTI and an IRC 962 election (tax on line 16 per attached statement; 5471/8992/8993/pro-forma 1118);
A-reorganization with cash boot (IRC 356 - gain limited to boot, Clark test -> capital); US C-corp liquidation (IRC 331 loss
from a 1099-DIV box 9); short-against-the-box constructive sale (IRC 1259) with no 1099-B; Form 1042-S withholding on a US
citizen (stale W-8BEN) -> withholding credited, paper filing; FBAR for the CFC's Irish bank account; NIIT."""
from common import ClientBuild, gotcha, fmt
from docs import statement, scanned_pages, write_text, info_form
import forms as F
from tax2025 import Return1040, r, tax_with_prefs

C = ClientBuild("EVG1025", "Brennan-Ochoa", "Victor & Lena Brennan-Ochoa")
ADDR = ("5127 Bayou Laurel Ln", "Houston, TX 77019")
T = {"name": "Victor M. Brennan-Ochoa", "ssn": "XXX-XX-5590", "dob": "1975-08-19"}
S = {"name": "Lena K. Brennan-Ochoa", "ssn": "XXX-XX-2874", "dob": "1977-01-30"}
REC_T = [T["name"], *ADDR, f"TIN: {T['ssn']}"]
REC_S = [S["name"], *ADDR, f"TIN: {S['ssn']}"]
REC_J = ["Victor M. & Lena K. Brennan-Ochoa", *ADDR, f"TIN: {T['ssn']}"]

# ------------------------------------------------------------------ key facts
# CFC - Ochoa Engineering Ltd. (Ireland), 100% Victor; amounts in USD per the Irish accountants' US reporting package
CFC_PRETAX = 457143
IRISH_TAX = 57143                    # 12.5%
TESTED_INCOME = CFC_PRETAX - IRISH_TAX   # 400,000
QBAI = 0
GILTI = TESTED_INCOME - r(.10 * QBAI)    # 400,000 (inclusion percentage 100%)
GROSS_UP = IRISH_TAX                 # IRC 78 (tested foreign income taxes x inclusion percentage)
S962_BASE = GILTI + GROSS_UP         # 457,143
S250 = S962_BASE * .50               # 2025 IRC 250 deduction rate for GILTI
S962_TI = S962_BASE - S250           # 228,571.50
S962_TAX_PRE = S962_TI * .21         # 48,000.0
DEEMED_PAID = r(.80 * IRISH_TAX)     # 45,714 (IRC 960(d))
S962_TAX = r(S962_TAX_PRE) - DEEMED_PAID
assert (TESTED_INCOME, r(S962_TAX_PRE), DEEMED_PAID, S962_TAX) == (400000, 48000, 45714, 2286)

# Lena - Gulf Coast Dental Labs -> Meridian Dental Holdings (A reorg, 06/20/2025)
GCDL_BASIS = 200000
MDH_SHARES = 10000
MDH_FMV_PER = 90
STOCK_RECEIVED = MDH_SHARES * MDH_FMV_PER          # 900,000
BOOT = 300000
REALIZED = STOCK_RECEIVED + BOOT - GCDL_BASIS      # 1,000,000
RECOGNIZED = min(REALIZED, BOOT)                    # 300,000
NEW_BASIS = GCDL_BASIS - BOOT + RECOGNIZED          # 200,000
PER_SH = NEW_BASIS / MDH_SHARES                     # 20
assert (REALIZED, RECOGNIZED, NEW_BASIS, PER_SH) == (1000000, 300000, 200000, 20)
# VBO Holdings liquidation (IRC 331)
VBO_BASIS, VBO_DIST = 120000, 85000
VBO_LOSS = VBO_DIST - VBO_BASIS                     # -35,000
# Constructive sale 12/10/2025 (IRC 1259)
SHORT_SH, SHORT_PX = 2000, 95
CS_PROCEEDS = SHORT_SH * SHORT_PX                   # 190,000
CS_BASIS = SHORT_SH * PER_SH                        # 40,000
CS_GAIN = CS_PROCEEDS - CS_BASIS                    # 150,000
assert (CS_GAIN, VBO_LOSS) == (150000, -35000)
# 1042-S
DIV_1042S, WH_1042S = 12000.00, 3600.00
BANK_INT = 1850.22
EST_PAID = [("09/15/2025", 20000), ("01/15/2026", 20000)]
EXT_PAY = 25000

# ------------------------------------------------------------------ PERM
C.write_profile(f"""
# EVG1025 - Brennan-Ochoa, Victor & Lena  (PERM)

*Synthetic client - Project Evergreen training data.*

| Item | Detail |
|---|---|
| Client ID | EVG1025 |
| Taxpayer | Victor M. Brennan-Ochoa, DOB 08/19/1975, SSN XXX-XX-5590 - principal structural engineer (W-2, Sabine & Pike Engineering, Inc.) |
| Spouse | Lena K. Brennan-Ochoa, DOB 01/30/1977, SSN XXX-XX-2874 - former co-owner of Gulf Coast Dental Labs, Inc. (not employed in 2025). U.S. citizen; lived in Madrid 2014-2018 |
| Address | {ADDR[0]}, {ADDR[1]} (Harris County) - **Texas: no individual income tax return** |
| Dependents | None |
| Contact | Lena preferred - lena.bo@example.com, (713) 555-0162; Victor - victor.bo@example.com |
| Engagement | **New client 2025** (prior preparer Harold Fenn, CPA retired 12/2025). International tier quote $5,800 (5471/8992/8993/962, FBAR, reorg). |
| Ochoa Engineering Ltd. | Irish private company limited by shares (Cork), incorporated 03/2022, CRO no. 7XXXXX (synthetic). Victor owns 100% (U.S. shareholder; CFC). Four Irish-resident employee engineers provide design review services to Irish/EU clients. Victor is an unpaid director; signatory on the company's AIB business account. Irish accountants: Kinsale & Murphy, Chartered Accountants. **Section 962 election made every year since 2022** (prior preparer). No distributions ever paid. |
| VBO Holdings, Inc. | Texas C corporation formed 05/2016 by Victor ($120,000 cash for 100% of stock) - small real-estate consulting holding company; plan of liquidation adopted 09/2025, final distribution 11/14/2025. |
| Gulf Coast Dental Labs, Inc. | Lena bought 18% of the stock 03/2012 for $200,000 (stock purchase agreement in PERM). Merged into Meridian Dental Holdings, Inc. (NYSE: MDH) 06/20/2025. |
""")
F.prior_year_summary(C.perm_file("2024_Form_1040_Return_Summary_prior_preparer.pdf", "Prior-year return summary (prior preparer)"),
    "Victor & Lena Brennan-Ochoa", "EVG1025", "Married filing jointly", [
        ["1a", "W-2 wages - Sabine & Pike Engineering", 172000],
        ["2b", "Taxable interest", 1410], ["3a / 3b", "Qualified / ordinary dividends (Atlas Clearing 1099-DIV)", "11,020 / 11,020"],
        ["11", "AGI", 184430], ["12", "Standard deduction", 29200], ["15", "Taxable income", 155230],
        ["16", "Tax incl. section 962 tax $1,200 (statement)", 24072], ["24", "Total tax", 24072], ["35a", "Refund", 3528]],
    carryovers=[["Capital loss carryover", 0], ["Section 962 PTEP (Ochoa Engineering) - cumulative 2022-2024 (USD)", "618,400"]],
    notes="Prior preparer WP: 962 election statements 2022-2024 attached to returns (5471 Cat 4/5, 8992, 8993 prepared by Kinsale & "
          "Murphy's U.S. desk). Schedule B Part III line 7a answered NO and no FBAR filed for 2022-2024 (prior preparer did not ask "
          "about the company's Irish account).")
statement(C.perm_file("VBO_Holdings_2016_formation_and_stock_ledger.pdf", "Corporate document - basis support"),
    "VBO Holdings, Inc. - Certificate of Formation (Texas) and Stock Ledger (extract)", [
        {"table": [["Date", "Holder", "Shares", "Consideration"], ["05/09/2016", "Victor M. Brennan-Ochoa", "1,000", "$120,000.00 cash"]]},
        {"para": "No additional contributions or redemptions through 2025 (per corporate secretary)."}])
statement(C.perm_file("Gulf_Coast_Dental_Labs_2012_stock_purchase.pdf", "Legal document - basis support"),
    "Gulf Coast Dental Labs, Inc. - Stock Purchase Agreement (03/15/2012) - extract", [
        {"table": [["Term", "Detail"], ["Purchaser", "Lena K. Brennan-Ochoa (then Lena K. Brennan)"], ["Shares", "1,800 common (18%)"],
                   ["Price", "$200,000.00 cash"], ["Closing", "03/15/2012"]], "left_align_cols": [0, 1]}])

# ------------------------------------------------------------------ PBC
EMP = {"name": "Sabine & Pike Engineering, Inc.", "addr1": "1400 Smith St, Suite 2200", "addr2": "Houston, TX 77002", "ein": "00-4471862"}
EE = {"name": T["name"], "addr1": ADDR[0], "addr2": ADDR[1], "ssn": T["ssn"]}
w2 = {"1": 180000.00, "2": 32000.00, "3": 176100.00, "4": 10918.20, "5": 196000.00, "6": 2842.00,
      "12": [("D", 16000.00), ("DD", 14220.00)], "13": ["Retirement plan: X"], "control": "SPE-25-1187"}

F.organizer(C.pbc_file("01_2025_Organizer_completed.pdf", "Client organizer", "2026-02-27"), "Victor & Lena Brennan-Ochoa", "EVG1025",
    general=[("Did you sell stock or other investments?", "Yes", "Lena - dental lab merger (cash + Meridian stock)"),
             ("Did any corporation you own liquidate or dissolve?", "Yes", "VBO Holdings closed in November"),
             ("Do you own 10% or more of a foreign corporation?", "Yes", "Ochoa Engineering Ltd (Ireland) - Kinsale & Murphy sends the package"),
             ("Do you have a financial interest in or signature authority over a foreign account?", "No", "only the company's account"),
             ("Did you receive any Forms 1042-S?", "Yes", "Lena - Atlas sent a weird one"),
             ("Did you make estimated tax payments?", "Yes", "2 payments - see confirmations"),
             ("Did you receive, sell, exchange digital assets?", "No", "")],
    dependents=[],
    income_rows=[["Wages", "Sabine & Pike Engineering", "", "see W-2"],
                 ["Interest", "Bayou City Bank", "", "~1,800"],
                 ["Dividends", "Atlas Clearing (Lena)", "", "12,000 (1042-S??)"],
                 ["Brokerage", "Lone Star Trust Co. (exchange agent)", "", "300,000 cash from merger"],
                 ["Foreign corporation", "Ochoa Engineering Ltd.", "", "962 again please"]],
    deductions_rows=[["Mortgage interest", "Third Coast Mortgage", "", "see 1098"],
                     ["Property taxes", "Harris County / HISD", "", "14,800"],
                     ["Charitable", "Various", "", "6,000"],
                     ["Estimated tax", "IRS Direct Pay", "", "20,000 x 2"]],
    signature_date="02/25/2026")
F.w2(C.pbc_file("02_W-2_Sabine_Pike_Engineering_Victor.pdf", "Form W-2", "2026-02-27"), EMP, EE, w2)
F.f1099_int(C.pbc_file("03_1099-INT_Bayou_City_Bank.pdf", "Form 1099-INT", "2026-02-27"),
            ["Bayou City Bank", "2700 Post Oak Blvd", "Houston, TX 77056", "TIN: 00-3307714"], REC_J, {"1": BANK_INT}, account="****6631")
EXA = ["Lone Star Trust Company, N.A., as Exchange Agent", "PO Box 43078", "Houston, TX 77210", "TIN: 00-9900417"]
b_boxes = [("1a", "Description of property", "GCDL INC - MERGER CASH CONSIDERATION"),
           ("1b", "Date acquired", ""), ("1c", "Date sold or disposed", "06/20/2025"),
           ("1d", "Proceeds", float(BOOT)), ("1e", "Cost or other basis", ""),
           ("2", "Short-term / Long-term / Ordinary", "(blank)"), ("3", "Check if proceeds from collectibles / QOF", ""),
           ("4", "Federal income tax withheld", 0.0), ("5", "Check if noncovered security", "X"),
           ("6", "Reported to IRS: Gross proceeds / Net proceeds", "Gross proceeds"), ("12", "Basis reported to IRS", "")]
F.f1099(C.pbc_file("04_1099-B_Lone_Star_Trust_exchange_agent.pdf", "Form 1099-B", "2026-02-27"), "1099-B",
        "Proceeds From Broker and Barter Exchange Transactions", EXA, REC_S, b_boxes, account="GCDL-MRG-00412",
        omb="OMB No. 1545-0715", notes=["Cash paid in the merger of Gulf Coast Dental Labs, Inc. into Meridian Dental Holdings, Inc. "
                                         "Shares of Meridian stock delivered to your designated broker are not reported on this form."])
scanned_pages(C.pbc_file("05_IMG_7702_exchange_agent_1099B.pdf", "Photo upload (image)", "2026-03-03", "Client email attachment",
                         "client emailed phone photo"),
    [["Form 1099-B  2025   Lone Star Trust Company, N.A., as Exchange Agent",
      "RECIPIENT: Lena K. Brennan-Ochoa  XXX-XX-2874",
      "Account GCDL-MRG-00412",
      "1a GULF COAST DENTAL LABS INC - CASH CONSIDERATION (MERGER)",
      "1c Date sold 06/20/2025       1d Proceeds   300,000.00",
      "1e Cost basis  (blank)        5 Noncovered [X]",
      "",
      "  (Lena's note in pen:  is this all taxable?? we only paid 200k",
      "   for the whole thing)"]], handwritten=False, skew=1.7, seed=2505)
statement(C.pbc_file("06_Meridian_GCDL_merger_election_and_Form_8937.pdf", "Corporate action documents", "2026-02-27"),
    "Meridian Dental Holdings, Inc. / Gulf Coast Dental Labs, Inc. - Letter of Transmittal Confirmation and Form 8937 (extract)", [
        {"heading": "Exchange confirmation - Lena K. Brennan-Ochoa (1,800 GCDL shares surrendered)",
         "table": [["Consideration", "Amount"], ["Meridian common stock (10,000 shares; NYSE close 06/20/2025 $90.00)", float(STOCK_RECEIVED)],
                   ["Cash consideration", float(BOOT)], ["Total", float(STOCK_RECEIVED + BOOT)]], "total_row": True},
        {"heading": "Form 8937 - Report of Organizational Actions Affecting Basis of Securities (Meridian, filed 07/2025) - Part II",
         "para": ["Line 14: On 06/20/2025 Gulf Coast Dental Labs, Inc. merged with and into Meridian Merger Sub LLC, a wholly owned "
                  "subsidiary of Meridian, in a transaction intended to qualify as a reorganization under IRC 368(a)(1)(A).",
                  "Line 15-16: A GCDL holder who received Meridian stock and cash recognizes gain (but not loss) equal to the lesser of "
                  "(i) the cash received or (ii) the gain realized. The aggregate basis of Meridian stock received equals the basis of "
                  "GCDL stock surrendered, decreased by the cash received and increased by the gain recognized. Holding period of the "
                  "Meridian stock includes the holding period of the GCDL stock.",
                  "Line 18: Whether cash is treated as a dividend under IRC 356(a)(2) depends on each holder's facts (Commissioner v. "
                  "Clark, 489 U.S. 726 (1989)). Holders should consult their tax advisors."]}])
F.f1099_div(C.pbc_file("07_1099-DIV_VBO_Holdings_liquidation.pdf", "Form 1099-DIV", "2026-02-27"),
            ["VBO Holdings, Inc. (in liquidation)", "5127 Bayou Laurel Ln", "Houston, TX 77019", "TIN: 00-8016452"], REC_T,
            {"1a": 0.0, "1b": 0.0, "9": float(VBO_DIST)},
            notes=["Box 9 Cash liquidation distributions: 85,000.00 (final distribution 11/14/2025 - plan of complete liquidation "
                   "adopted 09/02/2025). Box 10 Noncash liquidation distributions: 0.00"])
statement(C.pbc_file("08_VBO_Holdings_plan_of_liquidation_and_certificate_of_termination.pdf", "Corporate documents", "2026-02-27"),
    "VBO Holdings, Inc. - Plan of Complete Liquidation (09/02/2025) and Certificate of Termination (Texas SOS, 11/24/2025)", [
        {"para": ["Final distribution of all remaining cash ($85,000.00) to the sole shareholder on 11/14/2025 in complete "
                  "liquidation (IRC 331/336). Form 966 filed by the corporation 09/18/2025."]}])
statement(C.pbc_file("09_Bayside_Securities_Dec_2025_statement_Lena.pdf", "Brokerage statement", "2026-02-27"),
    "Bayside Securities LLC - Lena K. Brennan-Ochoa - Individual Margin Account ****3318 - December 2025 (extract)", [
        {"heading": "Positions at 12/31/2025",
         "table": [["Security", "Quantity", "Price 12/31", "Market value", "Cost basis (broker)"],
                   ["Meridian Dental Holdings (MDH) - long", "10,000", 93.40, 934000.00, "Unknown - transferred in 06/2025"],
                   ["Meridian Dental Holdings (MDH) - SHORT", "(2,000)", 93.40, -186800.00, "Short proceeds 190,000.00"]]},
        {"heading": "Activity - December 2025",
         "table": [["Date", "Activity", "Security", "Quantity", "Price", "Amount"],
                   ["12/10/2025", "Sell short", "MDH", "2,000", 95.00, 190000.00]]},
        {"para": "Short positions are reported on Form 1099-B in the year the position is closed."}])
statement(C.pbc_file("10_Bayside_Securities_Mar_2026_statement_Lena.pdf", "Brokerage statement", "2026-04-08",
                     note="client upload after organizer"),
    "Bayside Securities LLC - Lena K. Brennan-Ochoa - Account ****3318 - March 2026 (extract)", [
        {"table": [["Date", "Activity", "Security", "Quantity", "Detail"],
                   ["03/15/2026", "Cover short by delivery of long shares (versus purchase)", "MDH", "2,000",
                    "Short closed - long shares delivered; broker basis 'unknown'"]]}])
scanned_pages(C.pbc_file("11_Lena_note_about_Meridian_hedge.pdf", "Handwritten note (scan)", "2026-02-27"),
    [["Lena - notes for CPA",
      "",
      "Meridian shares (10,000) came in June from the merger.",
      "Dec 10 - my advisor had me 'short against the box'",
      "  2,000 sh @ $95 to lock in the price. He said no",
      "  tax until I close it, so nothing for 2025.",
      "Closed it in March by delivering the shares.",
      "",
      "Also - why did Atlas take 30% of my dividends?!",
      "I haven't lived in Spain since 2018."]], handwritten=True, seed=2511)
info_form(C.pbc_file("12_Form_1042-S_Atlas_Clearing_Lena.pdf", "Form 1042-S", "2026-03-16"), "1042-S",
          "Foreign Person's U.S. Source Income Subject to Withholding",
          payer=["Withholding agent's name / address / EIN", "Atlas Clearing Corp.", "One Liberty Plaza, 22nd Fl", "New York, NY 10006",
                 "EIN: 00-2290415"],
          recipient=["13a-13c Recipient's name / country / address", "Lena K. Brennan", "Calle de Velazquez 88 (on file)",
                     "Madrid 28006, Spain", "13b Country code: SP"],
          boxes=[("1", "Income code (06 = U.S. corp. dividends)", "06"), ("2", "Gross income", DIV_1042S),
                 ("3", "Chapter indicator", "3"), ("3a", "Exemption code", "00"), ("3b", "Tax rate", "30.00"),
                 ("7a", "Federal tax withheld", WH_1042S), ("10", "Total withholding credit", WH_1042S),
                 ("13e", "Recipient's U.S. TIN", "XXX-XX-2874"), ("13f", "Ch. 3 status code", "16 - Individual"),
                 ("13j", "LOB code", ""), ("13l", "Recipient's foreign tax identification number", "X1234567Z (expired)")],
          account_no="Atlas acct ****0957", copy_label="Copy B - For Recipient",
          notes=["Account migrated from Iberia Capital Markets 01/2025. Documentation on file: Form W-8BEN dated 06/2017."])
write_text(C.pbc_file("13_Email_thread_Lena_Atlas_W-9_2026-03-18.txt", "Client correspondence", "2026-03-18", "Email"),
"""From: preparer@evergreentax.example
To: Lena Brennan-Ochoa
Date: Tue, 17 Mar 2026 09:41:00 -0500
Subject: Brennan-Ochoa 2025 - the 1042-S

Lena - Atlas still has the W-8BEN you signed in Madrid in 2017, so it treated you as a foreign person and withheld 30% on your
dividends. You are a U.S. citizen: the dividends are taxable on your 1040 as usual and the $3,600 is credited against your tax like
any other withholding. Please send Atlas a Form W-9 now so 2026 dividends are paid in full (we attached a blank W-9).
One consequence: our software cannot e-file a Form 1040 that claims Form 1042-S withholding, so your 2025 return will be paper
filed with a copy of the 1042-S attached.

From: Lena Brennan-Ochoa <lena.bo@example.com>
Date: Wed, 18 Mar 2026 07:12:30 -0500
Subject: RE: Brennan-Ochoa 2025 - the 1042-S

Done - W-9 uploaded to Atlas this morning. Paper is fine.
Lena
""")
statement(C.pbc_file("14_Kinsale_Murphy_US_reporting_package_Ochoa_Engineering_2025.pdf", "CFC reporting package", "2026-06-24",
                     "Email attachment", "received after extension"),
    "Ochoa Engineering Ltd. (Ireland) - U.S. Shareholder Reporting Package - Year ended 31 December 2025", [
        {"para": "Prepared by Kinsale & Murphy, Chartered Accountants (U.S. tax desk) for Victor M. Brennan-Ochoa (100% U.S. "
                 "shareholder). Amounts translated to USD at the average exchange rate for the year (IRC 989(b)); balance sheet "
                 "amounts at the year-end spot rate."},
        {"heading": "Tested income (Treas. Reg. 1.951A-2)",
         "table": [["Item", "USD"], ["Gross income - engineering design-review services (performed in Ireland for unrelated clients)", 1388400.00],
                   ["Less: salaries, rent, professional fees and other allocable deductions", -931257.00],
                   ["Taxable income before tax (US tax principles)", float(CFC_PRETAX)],
                   ["Irish corporation tax at 12.5% (trading rate) - paid", -float(IRISH_TAX)],
                   ["Tested income", float(TESTED_INCOME)],
                   ["Qualified business asset investment (QBAI) - all equipment leased; no specified tangible property", float(QBAI)],
                   ["Subpart F income (FBCSI: services performed in Ireland - none)", 0.0],
                   ["Effective foreign tax rate 12.5% < 18.9% -> GILTI high-tax exclusion not available", ""]]},
        {"heading": "Section 962 election computation (provided for information - preparer to verify)",
         "table": [["Line", "USD"], ["GILTI inclusion (inclusion percentage 100%)", float(GILTI)], ["Section 78 gross-up", float(GROSS_UP)],
                   ["Total", float(S962_BASE)], ["Section 250 deduction 50%", -S250], ["Taxable at 21%", S962_TI],
                   ["Tax at 21%", S962_TAX_PRE], ["Deemed-paid credit 80% x 57,143", -float(DEEMED_PAID)], ["Section 962 tax", float(S962_TAX)]]},
        {"heading": "Earnings & profits / PTEP and distributions",
         "table": [["Item", "USD"], ["Distributions to shareholder in 2025", 0.0],
                   ["Section 962 PTEP (cumulative, after 2025 inclusion)", 1018400.0]]},
        {"heading": "Bank accounts held by the company",
         "table": [["Institution", "Account", "Max balance 2025 (EUR)", "Signatories"],
                   ["Allied Irish Banks plc, Cork", "Business current ****4471", "310,000", "V. Brennan-Ochoa (director); S. Hennessy (financial controller)"]]}])
write_text(C.pbc_file("15_Email_Victor_962_2026-06-24.txt", "Client correspondence", "2026-06-24", "Email"),
"""From: Victor Brennan-Ochoa <victor.bo@example.com>
To: preparer@evergreentax.example
Date: Wed, 24 Jun 2026 18:03:12 -0500
Subject: Ochoa Engineering package

Kinsale & Murphy's package is attached. Harold always did the "962 election" - please do the same. The Irish account is the
company's money, not mine, so I assume there's no FBAR - Harold never filed one. I'm a signer on it though.
Victor
""")
statement(C.pbc_file("16_IRS_Direct_Pay_confirmations.pdf", "Payment confirmations", "2026-02-27"), "IRS Direct Pay - payment confirmations", [
    {"table": [["Date", "Type", "Tax year", "Amount", "Confirmation"]] +
              [[d, "Estimated tax (1040-ES)", "2025", float(a), f"DP-{i}84Q-{i}1X"] for i, (d, a) in enumerate(EST_PAID, 1)] +
              [["04/14/2026", "Extension (Form 4868)", "2025", float(EXT_PAY), "DP-3T7Z-55A"]]}])
statement(C.pbc_file("17_1098_Third_Coast_Mortgage.pdf", "Form 1098", "2026-02-27"), "Form 1098 - Mortgage Interest Statement 2025", [
    {"table": [["Box", "Description", "Amount"], ["1", "Mortgage interest received", 9612.55], ["2", "Outstanding principal", 238400.00],
               ["3", "Origination date", "08/12/2019"], ["10", "Property tax paid from escrow (Harris County + HISD)", 14800.00]],
     "left_align_cols": [0, 1]}])

# ------------------------------------------------------------------ RETURN
trades = [
    {"box": "E", "id": "1", "desc": "Gulf Coast Dental Labs, Inc. 1,800 sh - cash boot in IRC 368(a)(1)(A) merger into Meridian; "
     f"gain recognized = lesser of boot {BOOT:,} or realized gain {REALIZED:,} (IRC 356(a)(1)); statement attached",
     "acq": "03/15/2012", "sold": "06/20/2025", "proceeds": BOOT, "basis": 0},
    {"box": "F", "id": "2", "desc": "VBO Holdings, Inc. 1,000 sh - complete liquidation (IRC 331) - 1099-DIV box 9",
     "acq": "05/09/2016", "sold": "11/14/2025", "proceeds": VBO_DIST, "basis": VBO_BASIS},
    {"box": "F", "id": "3", "desc": "Meridian Dental Holdings 2,000 sh - CONSTRUCTIVE SALE (IRC 1259) - short against the box "
     "12/10/2025 @ $95; holding period includes GCDL (2012)", "acq": "03/15/2012", "sold": "12/10/2025",
     "proceeds": CS_PROCEEDS, "basis": CS_BASIS},
]
facts = {
    "status": "MFJ",
    "taxpayer": {}, "spouse": {},
    "w2": [{"who": "T", "box1": w2["1"], "box2": w2["2"], "box3": w2["3"], "box4": w2["4"], "box5": w2["5"], "box6": w2["6"]}],
    "interest": [{"payer": "Bayou City Bank", "amount": BANK_INT}],
    "dividends": [{"payer": "Atlas Clearing Corp. - reported on Form 1042-S (income code 06; U.S. citizen - see statement)",
                   "ordinary": DIV_1042S, "qualified": DIV_1042S}],
    "foreign_accounts": True, "foreign_account_country": "Ireland",
    "trades": trades,
    "itemized": {"state_income_tax": 0, "real_estate_tax": 14800, "mortgage_interest_1098": 9612.55, "charity_cash": 6000},
    "line16_other": [("Section 962 election tax (Ochoa Engineering Ltd.) - statement attached", S962_TAX)],
    "withholding_other": WH_1042S,
    "estimated_payments": sum(a for _, a in EST_PAID),
    "extension_payment": EXT_PAY,
}
nii = r(BANK_INT) + DIV_1042S + BOOT + VBO_LOSS + CS_GAIN
facts["niit"] = {"nii": nii, "gross": nii}
R = Return1040(facts).compute()
v = R.values
sd = v["sch_d"]
assert sd["net_lt"] == 415000

# comparison: no section 962 election (GILTI taxed at individual ordinary rates; no IRC 250 deduction, no deemed-paid credit)
qd, ncg = v["3a"], sd["ncg"]
tax_no962, _ = tax_with_prefs(v["15"] + GILTI, "MFJ", qd, ncg)
tax_with962 = v["16"]
saving_962 = tax_no962 - tax_with962
regular_only = v["16"] - S962_TAX
payments = v["33"]

s962 = [["Section 962 election - tax computation (Reg. 1.962-1; election statement per Reg. 1.962-2)", "Amount"],
        ["Tested income - Ochoa Engineering Ltd. (CFC, 100%)", TESTED_INCOME], ["Less 10% of QBAI ($0)", 0],
        ["GILTI inclusion - Form 8992 (not included in AGI under the 962 election)", GILTI],
        ["Section 78 gross-up (tested foreign income taxes x inclusion %)", GROSS_UP],
        ["Total section 962 income", S962_BASE], ["Section 250 deduction (50% for 2025) - Form 8993", -r(S250)],
        ["Taxable at corporate rate", r(S962_TI)], ["Tax at 21%", r(S962_TAX_PRE)],
        ["Deemed-paid credit IRC 960(d): 80% x 57,143 (pro-forma Form 1118, GILTI basket; limitation 48,000)", -DEEMED_PAID],
        ["Section 962 tax - included on Form 1040 line 16 (see Line 16 statement)", S962_TAX],
        ["Comparison - no election: income tax on TI + 400,000 GILTI at individual rates", tax_no962],
        ["Comparison - with election: line 16 (regular tax + 962 tax)", tax_with962],
        ["Federal income tax saved by the election (before NIIT)", saving_962],
        ["Presentation assumption: 962 tax reported on line 16 with an attached statement and the 951A inclusion excluded from "
         "AGI - verify against the current Form 1040 line 16 instructions", ""],
        ["Future distributions of this PTEP: taxable under IRC 962(d) to the extent they exceed the 962 tax paid", ""]]
intl = [["International information returns attached to Form 1040", "Detail"],
        ["Form 5471 - Ochoa Engineering Ltd. (Categories 4 and 5)", "Schedules C, E, F, H, I-1, J, P, Q, R, M; Victor 100%"],
        ["Form 8992 - GILTI (Schedule A)", f"Net CFC tested income {GILTI:,}"],
        ["Form 8993 - section 250 deduction", f"{r(S250):,} (computed for the 962 election)"],
        ["Pro-forma Form 1118 / Form 1120 computations", "Attached as part of the 962 statement (not separately filed)"],
        ["Form 926", "Not required - no transfers to the CFC in 2025"],
        ["Form 8938 (MFJ living in U.S.: > $100,000 year end / > $150,000 any time)",
         "Required - stock of Ochoa Engineering Ltd. (excepted - reported on Form 5471, Part IV: 1 Form 5471)"],
        ["Schedule B Part III", "Line 7a Yes (financial interest via > 50% owned company + signature authority); 7b Ireland"]]
fbar = [["FinCEN Form 114 (FBAR) 2025 - filed separately via BSA E-Filing", "Detail"],
        ["Filer", "Victor M. Brennan-Ochoa"],
        ["Account", "Allied Irish Banks plc, Cork - business current ****4471 (owned by Ochoa Engineering Ltd.)"],
        ["Basis for filing", "Financial interest (owns > 50% of the account owner, 31 CFR 1010.350(e)(2)(ii)) and signature authority"],
        ["Maximum value", "EUR 310,000 - converted at the Treasury 12/31/2025 reporting rate (verify published rate)"],
        ["Due", "04/15/2026, automatic extension to 10/15/2026"],
        ["Prior years 2022-2024", "Not filed by prior preparer - delinquent FBAR submission procedures recommended (separate engagement)"]]
reorg = [["IRC 356 statement - Gulf Coast Dental Labs / Meridian merger (Lena)", "Amount"],
         ["Meridian stock received (10,000 sh x $90)", STOCK_RECEIVED], ["Cash boot received", BOOT],
         ["Amount realized", STOCK_RECEIVED + BOOT], ["Basis of GCDL stock surrendered (2012)", GCDL_BASIS],
         ["Gain realized", REALIZED], ["Gain recognized = lesser of boot or realized gain (LTCG - Clark: no dividend equivalence; "
          "Lena's 18% interest became < 1% of Meridian - hypothetical redemption is not essentially equivalent to a dividend)", RECOGNIZED],
         ["Basis of Meridian stock: 200,000 - 300,000 cash + 300,000 gain", NEW_BASIS], ["Per share ($ / 10,000 sh)", PER_SH],
         ["Holding period of Meridian shares tacks to 03/15/2012", ""]]
cs = [["IRC 1259 constructive sale statement (Lena - Meridian, short against the box)", "Amount"],
      ["Short sale 12/10/2025: 2,000 sh x $95 (deemed sale of 2,000 long shares at FMV)", CS_PROCEEDS],
      ["Basis of 2,000 long shares ($20/sh)", CS_BASIS], ["Long-term gain recognized in 2025 (no 1099-B)", CS_GAIN],
      ["Exception IRC 1259(c)(3) not met - short not closed within 30 days after year end (closed 03/15/2026)", ""],
      ["New basis of the 2,000 shares $95 ($190,000); new holding period from 12/10/2025 - 2026 1099-B will show unknown basis: "
       "report basis 190,000 (code B) so the 150,000 is not taxed twice", ""]]
w1042 = [["Form 1042-S (Atlas Clearing) - U.S. citizen recipient", "Amount"],
         ["Income code 06 dividends - included on Schedule B / line 3b (qualified: shares held since 2019)", DIV_1042S],
         ["Chapter 3 withholding 30% - credited on Form 1040 line 25c (copy of 1042-S attached)", WH_1042S],
         ["Cause: stale 2017 Form W-8BEN; Form W-9 provided to Atlas 03/18/2026", ""],
         ["Filing method: PAPER (software cannot e-file a 1040 claiming Form 1042-S withholding)", ""]]
C.write_return(R, [
    ("Taxpayer / Spouse", "Victor M. Brennan-Ochoa (XXX-XX-5590) / Lena K. Brennan-Ochoa (XXX-XX-2874)"),
    ("Address", ", ".join(ADDR)),
    ("Filing status", "Married filing jointly"),
    ("Dependents", "None"),
    ("Digital assets question", "No"),
    ("Forms included", "1040, Schedules 2, 3, B (Part III: Yes - Ireland), D, Form 8949, Form 8960, Form 5471 (Cat 4/5), Form 8992, "
                       "Form 8993, Form 8938, section 962 election statement + pro-forma 1118/1120, IRC 356 and IRC 1259 statements, "
                       "copy of Form 1042-S. Separately: FinCEN 114 (BSA E-Filing)"),
    ("Extension", f"Form 4868 filed 04/14/2026 with ${EXT_PAY:,} payment"),
    ("State", "None - Texas has no individual income tax"),
    ("Filing method", "PAPER - Form 1042-S withholding claimed; mailed 09/24/2026 by certified mail to the IRS address for Texas "
                      "filers per the Form 1040 'Where To File' table; balance due paid by IRS Direct Pay 09/24/2026"),
], attachments=[("Section 962 election - statement and computation", s962),
                ("International forms summary", intl),
                ("FBAR summary", fbar),
                ("IRC 356 reorganization statement", reorg),
                ("IRC 1259 constructive sale statement", cs),
                ("Form 1042-S withholding statement", w1042)])

gotchas = [
    gotcha("EVG1025-G1", "Foreign Corps (GILTI / section 962)", "Section 962 tax computation and line 16 presentation",
           "Add the $400,000 GILTI to AGI and tax it at ordinary rates (no election); or apply 21% to $400,000 with no gross-up / "
           "no section 250 deduction / no deemed-paid credit; or add the 962 tax on Schedule 2.",
           f"962 election: (400,000 + 57,143 gross-up) - 50% IRC 250 deduction = {r(S962_TI):,} x 21% = 48,000 - 80% deemed-paid "
           f"credit {DEEMED_PAID:,} = {fmt(S962_TAX)}, on line 16 with a statement; inclusion not in AGI (presentation stated as an "
           "assumption to verify). Election statement + Forms 5471/8992/8993 + pro-forma 1118.",
           f"Without the election federal income tax is {fmt(saving_962)} higher", ["16", "Form 8992", "Form 8993"], "hard"),
    gotcha("EVG1025-G2", "Foreign Corps (Form 5471 / 926)", "CFC information returns",
           "Only attach the 962 statement; or file Form 926 for the Irish company.",
           "Victor is a 100% U.S. shareholder of a CFC -> Form 5471 Categories 4 and 5 (Schedules incl. I-1, J, P, Q, R), Form 8992, "
           "Form 8993. No transfers to the CFC in 2025 -> no Form 926. Form 8938 also required (CFC stock is a specified foreign "
           "financial asset - excepted, reported on 5471).", "$10,000 per-form penalty exposure", ["Form 5471", "Form 8938"], "medium"),
    gotcha("EVG1025-G3", "FinCEN114/FBAR", "Company's Irish bank account - 'not my money'",
           "No FBAR and Schedule B 7a 'No' (as the prior preparer did), because the account is owned by the company.",
           "A U.S. person who owns > 50% of a corporation has a financial interest in its foreign accounts, and Victor also has signature "
           "authority -> FBAR required (max EUR 310,000), Schedule B line 7a Yes / Ireland. 2022-2024 FBARs missing - delinquent FBAR "
           "procedures (separate engagement).", "Penalty exposure", ["Sch B 7a", "FBAR"], "medium"),
    gotcha("EVG1025-G4", "Schedule D (reorganization boot)", "Merger cash boot - 1099-B shows $300,000 proceeds, no basis",
           "Report $1.2M amount realized (gain $1,000,000); or offset the $200,000 basis against the cash (gain $100,000); or treat the "
           "boot as a dividend.",
           f"IRC 356(a)(1): gain recognized = lesser of boot {fmt(BOOT)} or realized gain {fmt(REALIZED)} = {fmt(RECOGNIZED)} LTCG "
           "(basis 0 on 8949 box E with statement). Clark: hypothetical redemption of Meridian stock is a meaningful reduction -> capital, "
           f"not dividend. Meridian basis {fmt(NEW_BASIS)} ($20/sh), holding period from 2012.",
           "Gain over/understated $200,000-$700,000", ["7", "Form 8949 box E"], "hard"),
    gotcha("EVG1025-G5", "Schedule D", "Liquidating distribution on Form 1099-DIV box 9",
           "Report $85,000 as a dividend, or ignore box 9 (no 1099-B) and miss the loss.",
           f"Box 9 is a liquidating distribution - IRC 331 exchange treatment: 85,000 - basis 120,000 = {fmt(VBO_LOSS)} long-term capital "
           "loss (held since 2016), Form 8949 box F.", "$35,000 loss omitted", ["7", "Form 8949 box F"], "medium"),
    gotcha("EVG1025-G6", "Schedule D (constructive sale)", "Short against the box - IRC 1259",
           "Nothing in 2025 (no 1099-B; advisor said no tax until closed); report the gain in 2026.",
           f"Shorting substantially identical stock against an appreciated long position is a constructive sale on 12/10/2025; the "
           f"30-day closing exception is not met (closed 03/15/2026). LTCG 2,000 x ($95 - $20) = {fmt(CS_GAIN)} in 2025 (holding period "
           "tacks). New basis $95/share - adjust the 2026 1099-B so the gain is not taxed twice.",
           f"Gain understated {fmt(CS_GAIN)}", ["7", "Form 8949 box F"], "hard"),
    gotcha("EVG1025-G7", "Paper Filing Returns / E-File Rejects", "Form 1042-S issued to a U.S. citizen",
           "Ignore the 1042-S (dividends 'already taxed') or omit the $3,600 credit; or try to e-file anyway.",
           f"Dividends {fmt(DIV_1042S)} taxable on Schedule B / line 3 (qualified - long-held domestic stock); 30% withholding {fmt(WH_1042S)} "
           "credited on line 25c. A 1040 claiming 1042-S withholding can't be e-filed in ProConnect (firm policy: paper file in either "
           "package) -> paper return with the 1042-S copy attached; W-9 to the broker.", "$3,600 credit; e-file rejection", ["3b", "25c"], "medium"),
    gotcha("EVG1025-G8", "NIIT", "Net investment income - gains, 962 inclusion, MAGI limb",
           "Include the $400,000 GILTI in NII/MAGI; or skip NIIT because the gains are 'reorganization' gains.",
           f"NII = interest + dividends + net gains {fmt(sd['line16'])} = {fmt(nii)}; MAGI {fmt(v['11'])} - 250,000 = "
           f"{fmt(v['11'] - 250000)} is smaller -> NIIT {fmt(v['niit'])}. The 962 inclusion is not NII and not in AGI (Reg. 1.1411-10; "
           "no (g) election).", f"NIIT {fmt(v['niit'])}", ["23", "Form 8960"], "medium"),
    gotcha("EVG1025-G9", "Schedule A (SALT cap phase-down)", "Itemize vs standard with MAGI > $500,000",
           "Itemize using $14,800 property tax + mortgage + charity (> $31,500 if the SALT cap is taken as $40,000).",
           f"MAGI {fmt(v['11'])} > $500,000 -> SALT cap 40,000 - 30% x excess, floored at $10,000. Itemized = 10,000 + 9,613 + 6,000 = "
           f"{fmt(v['itemized_total_computed'])} < standard $31,500 -> standard deduction.", "Deduction", ["12e"], "easy"),
]
C.write_answer_key(R, {"residence": "TX - Houston (no state income tax)", "complexity": "International tier - CFC/962, reorg, 1259"},
                   gotchas,
                   filings=[{"form": "Form 4868", "filed": "2026-04-14", "payment": EXT_PAY},
                            {"form": "Form 1040 incl. 5471, 8992, 8993, 8938, 8960, 962 statement, 1042-S copy", "method": "paper - certified mail (Where To File address for TX)",
                             "due": "2026-10-15", "filed": "2026-09-24"},
                            {"form": "FinCEN 114 (FBAR)", "method": "BSA E-Filing", "due": "2026-10-15 (automatic extension)", "filed": "2026-09-22"}],
                   extra={"section_962": {"tested_income": TESTED_INCOME, "gilti": GILTI, "gross_up": GROSS_UP, "s250": r(S250),
                                          "taxable": r(S962_TI), "tax_21pct": r(S962_TAX_PRE), "deemed_paid_credit": DEEMED_PAID,
                                          "s962_tax": S962_TAX, "income_tax_without_election": tax_no962, "saving": saving_962},
                          "reorg_356": {"realized": REALIZED, "recognized": RECOGNIZED, "new_basis": NEW_BASIS, "per_share": PER_SH},
                          "liquidation_331": VBO_LOSS, "constructive_sale_1259": CS_GAIN,
                          "form_1042s": {"dividends": DIV_1042S, "withholding_25c": WH_1042S},
                          "carryforwards_to_2026": {"meridian_basis_2000_sh_after_1259": CS_PROCEEDS,
                                                    "meridian_basis_8000_sh": r(8000 * PER_SH),
                                                    "section_962_ptep_usd": 1018400},
                          "assumptions": ["Form 1040 line 16 presentation of the section 962 tax with the inclusion excluded from AGI - verify "
                                          "against current instructions",
                                          "Atlas dividends treated as qualified (domestic C-corp stock held since 2019)",
                                          "2025 section 250 deduction rate for GILTI 50%"]})

C.write_receipt_log("EVG1025-1040-2025", "P. Nwosu (staff)", "D. Morgan (manager)", "S. Kennedy, CPA", "2026-02-27",
                    extension=f"Filed 04/14/2026 with ${EXT_PAY:,} payment - CFC reporting package (Kinsale & Murphy) outstanding")
C.write_notes(f"""
# EVG1025 - Brennan-Ochoa, Victor & Lena - 2025 Form 1040 - Preparer Notes

*Synthetic client - Project Evergreen (new client 2025). Return status: **signed off; extended return PAPER filed 09/24/2026
(certified mail); FBAR e-filed 09/22/2026.***

## Return summary
| | |
|---|---|
| Filing status | Married filing jointly |
| Wages | {fmt(v['1a'])} (Victor) |
| Interest / dividends | {fmt(v['2b'])} / {fmt(v['3b'])} (1042-S dividends; qualified {fmt(v['3a'])}) |
| Capital gains (line 7) | {fmt(v['7'])} = boot {fmt(RECOGNIZED)} + constructive sale {fmt(CS_GAIN)} + liquidation loss {fmt(VBO_LOSS)} |
| AGI (line 11) | {fmt(v['11'])} (GILTI not included - section 962 election) |
| Deduction | Standard {fmt(v['12e'])} (itemized only {fmt(v['itemized_total_computed'])} after the SALT cap phase-down to $10,000) |
| Taxable income | {fmt(v['15'])} |
| Tax (line 16) | {fmt(v['16'])} = regular tax {fmt(regular_only)} + section 962 tax {fmt(S962_TAX)} |
| NIIT | {fmt(v['niit'])} |
| Total tax | {fmt(v['24'])} |
| Payments | W-2 {fmt(v['25a'])} + 1042-S {fmt(v['25c'])} + estimates {fmt(v['26'])} + extension {fmt(EXT_PAY)} = {fmt(payments)} |
| **Balance due** | **{fmt(v['balance_due'])}** (paid by IRS Direct Pay 09/24/2026; IRS will bill interest from 04/15/2026) |

## What I did and why (plain English)
1. **Ochoa Engineering Ltd. - GILTI and the section 962 election.** Victor owns 100% of an Irish company -> CFC. Its tested income is
   {fmt(TESTED_INCOME)} after 12.5% Irish tax ({fmt(IRISH_TAX)}); no QBAI, no subpart F (services performed in Ireland), and 12.5% is
   below the 18.9% high-tax threshold -> GILTI inclusion {fmt(GILTI)}. Without an election, an individual is taxed on GILTI at ordinary
   rates with no section 250 deduction and no foreign tax credit for the company's Irish tax. Under the **section 962 election** (made
   every year since 2022) Victor is taxed as if a corporation: (400,000 + 57,143 section 78 gross-up) less the 50% section 250
   deduction = {fmt(r(S962_TI))} x 21% = {fmt(r(S962_TAX_PRE))}, less the 80% deemed-paid credit {fmt(DEEMED_PAID)} = **{fmt(S962_TAX)}**.
   The tax goes on **line 16** with an attached statement (election statement, pro-forma 1120 / 1118 computations, Forms 8992 and
   8993); the inclusion itself is not added to AGI. *Presentation is stated as an assumption to verify against the current Form 1040
   line 16 instructions.* Election saves {fmt(saving_962)} of 2025 federal income tax (without it, tax on line 16 would be
   {fmt(tax_no962)}). Trade-off: when the company eventually distributes this PTEP, the distribution is taxable to the extent it exceeds
   the 962 tax paid (IRC 962(d)) - as a qualified dividend if Ireland treaty requirements are met. Kinsale & Murphy's package (received
   06/24/2026 - main reason for the extension) was re-performed, not just copied.
2. **Form 5471 / 8938 / FBAR.** Form 5471 Categories 4 and 5, Forms 8992 and 8993 attached. No Form 926 (no transfers to the CFC in
   2025). Form 8938 required (CFC stock is a specified foreign financial asset - listed as excepted, reported on 5471). The company's
   AIB account: Victor owns more than 50% of the account owner (financial interest) and is a signer -> **FBAR required** and
   Schedule B line 7a **Yes / Ireland**. The prior preparer answered "No" and filed no FBARs for 2022-2024 - flagged to signer
   (delinquent FBAR submission procedures; separate engagement).
3. **Lena - merger boot (IRC 356).** 1,800 GCDL shares (basis $200,000, 2012) were exchanged in an A reorganization for 10,000 Meridian
   shares (FMV {fmt(STOCK_RECEIVED)}) plus {fmt(BOOT)} cash. Realized gain {fmt(REALIZED)}; recognized = lesser of the boot or the
   realized gain = **{fmt(RECOGNIZED)}**. Under Clark the boot is tested as a hypothetical redemption of Meridian stock: Lena's
   interest in Meridian is tiny and the hypothetical redemption is a meaningful reduction -> capital gain, not a dividend. Long-term
   (GCDL held since 2012). The exchange agent's 1099-B shows proceeds $300,000 and no basis: reported on 8949 box E with basis $0
   and a statement (not $1.2M proceeds, and not $300,000 less $200,000). Meridian basis = 200,000 - 300,000 + 300,000 = **$200,000
   ($20/share)**, holding period tacks.
4. **VBO Holdings liquidation (IRC 331).** 1099-DIV box 9 shows an $85,000 cash liquidating distribution - not a dividend. Exchange
   treatment against Victor's $120,000 basis -> **{fmt(VBO_LOSS)}** long-term capital loss (8949 box F).
5. **Constructive sale (IRC 1259).** On 12/10/2025 Lena sold short 2,000 Meridian shares at $95 while holding 10,000 long shares -
   "short against the box". That is a constructive sale of 2,000 long shares on 12/10/2025. The exception for a short closed within
   30 days after year end does not apply (closed 03/15/2026). Gain 2,000 x ($95 - $20) = **{fmt(CS_GAIN)}** long-term in 2025 - no
   1099-B exists for 2025. Those 2,000 shares now have a $95 basis and a new holding period; when the 2026 1099-B reports the
   March close with unknown basis, report basis $190,000 so the gain isn't taxed twice (2026 diary note).
6. **Form 1042-S.** Atlas Clearing still had Lena's 2017 W-8BEN (Madrid) and withheld 30% on {fmt(DIV_1042S)} of dividends. She is a
   U.S. citizen: the dividends are taxable normally (qualified - domestic stock held since 2019) and the {fmt(WH_1042S)} is credited
   as withholding on line 25c. Per Intuit, a Form 1040 claiming 1042-S withholding cannot be e-filed in ProConnect; firm policy is the
   same in Axcess -> **paper return** with a copy of the 1042-S attached. Lena gave Atlas a W-9 on 03/18/2026.
7. **NIIT.** NII = interest + dividends + net gains = {fmt(nii)}; MAGI over $250,000 = {fmt(v['11'] - 250000)} is smaller ->
   NIIT **{fmt(v['niit'])}**. The 962 inclusion is not NII. No Additional Medicare tax (Medicare wages $196,000 < $250,000 MFJ).
8. **Deduction.** MAGI over $500,000 phases the SALT cap down to the $10,000 floor; itemized would be {fmt(v['itemized_total_computed'])}
   -> standard deduction $31,500.
9. **Payments / penalties.** 2024 tax $24,072 (AGI > $150,000 -> 110% = $26,479); withholding alone ({fmt(v['25d'])}) exceeds it ->
   no Form 2210 penalty. Extension payment + estimates covered > 90% of the tax by 04/15/2026, so no late-payment penalty for the
   extension period; IRS will bill interest on the {fmt(v['balance_due'])} balance.

## Open items / client communication
- FBAR 2022-2024 and Schedule B 7a for those years: delinquent FBAR submission procedures - engagement letter to be sent (CONS).
- 2026: Meridian 2,000-share basis $95 (code B adjustment on the 2026 1099-B); 8,000 remaining shares $20 basis.
- 2026 GILTI: section 250 deduction for GILTI changes to 40% (OBBBA) and the deemed-paid credit to 90% - re-run the 962 comparison.

## Hand-off to signer / routing
- [x] Return locked; Accountant's copy saved as *reviewed*
- [x] Federal 1040 - **PAPER** (1042-S withholding); government copy + 1042-S copy + statements; certified mail 09/24/2026 (tracking in WP)
- [x] **FinCEN 114** - BSA E-Filing 09/22/2026 (Victor; financial interest + signature authority)
- [x] No state (TX)
- [x] Signature: wet-signed jurat (paper return) - both spouses
- Billing: international tier $5,800 (+ $600 constructive-sale / reorg research). Prior-year FBAR remediation -> separate CONS project.
""")
C.write_review_points(f"""
# Review Points - EVG1025 - 2025 - Form 1040

*Reviewer: D. Morgan (blue). Preparer responses in red. Synthetic.*

1. **Line 16 / 962** - First draft added the $400,000 GILTI to Schedule 1 and taxed it at ordinary rates (organizer says "962 again").
   - Make the election (statement + pro-forma 1118); compute tax with the 78 gross-up, 50% section 250, 80% deemed-paid credit.
   - *Preparer: 962 tax {fmt(S962_TAX)} on line 16; inclusion removed from AGI; savings {fmt(saving_962)} documented.*
2. **Form 8949 - merger** - Draft reported proceeds $300,000 less basis $200,000 = $100,000.
   - Boot rule: gain = lesser of boot or realized gain. Basis stays with the Meridian shares.
   - *Preparer: {fmt(RECOGNIZED)} LTCG; statement attached; Meridian basis $20/share recorded in PERM.*
3. **Constructive sale** - Lena's note and the December statement show a short against the box. Nothing in the draft.
   - IRC 1259 - recognize in 2025; 30-day exception not met.
   - *Preparer: {fmt(CS_GAIN)} LTCG on 8949 box F, sold date 12/10/2025; 2026 basis note set.*
4. **1099-DIV box 9** - Draft showed $85,000 as ordinary dividends.
   - Liquidating distribution -> capital loss vs $120,000 basis.
   - *Preparer: {fmt(VBO_LOSS)} LT loss.*
5. **1042-S** - Draft omitted the dividends and the $3,600 credit ("already taxed").
   - US citizen - include and credit on 25c. Paper file. W-9 to broker.
   - *Preparer: Done; return will be paper filed.*
6. **FBAR / Sch B 7a** - Draft answered No (followed prior preparer). Victor owns 100% of the account owner and signs on the account.
   - *Preparer: FBAR filed; Sch B Yes/Ireland; prior-year exposure memo to S. Kennedy.*
7. FYI - NIIT should not include the GILTI inclusion; MAGI limb binds. Itemizing does not beat standard after the SALT phase-down.
   - *Preparer: Confirmed - NIIT {fmt(v['niit'])}; standard deduction.*
""")
print("EVG1025 done", R.summary()["24"], "refund", v["refund"], "due", v["balance_due"], "AGI", v["11"], "TI", v["15"],
      "16", v["16"], "niit", v["niit"], "no962", tax_no962, "save", saving_962)
