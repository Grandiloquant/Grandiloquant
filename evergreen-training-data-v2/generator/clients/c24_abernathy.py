"""EVG1024 - Margaret "Peggy" Abernathy (Single, Florida - Naples).
Founder's stock in a dissolved C corp (IRC 1244 ordinary loss up to $50,000 + worthless-stock capital loss, IRC 165(g));
credit-card 1099-C excluded under the insolvency exception (Form 982) with IRC 108(b) attribute reduction of the capital
loss carryover; inherited IRA distribution with the IRC 691(c) deduction for estate tax on IRD; distribution from a foreign
non-grantor trust (Jersey) reported under the actual method from a Foreign Nongrantor Trust Beneficiary Statement, plus
Form 3520 Part III (filed separately) and Form 8938."""
from common import ClientBuild, gotcha, fmt
from docs import statement, scanned_pages, write_text, write_xlsx, info_form
import forms as F
from tax2025 import Return1040, r

C = ClientBuild("EVG1024", "Abernathy", "Margaret \"Peggy\" Abernathy")
ADDR = ("2180 Gulf Shore Blvd N, Unit 504", "Naples, FL 34102")
T = {"name": "Margaret A. Abernathy", "ssn": "XXX-XX-6318", "dob": "1979-05-27"}
REC_T = [T["name"], *ADDR, f"TIN: {T['ssn']}"]

# ------------------------------------------------------------------ key facts (single source of truth)
BRIGHTLINE_BASIS = 150000          # 1,500,000 founder shares issued 06/12/2019 for cash
S1244_LIMIT = 50000                # single filer
S1244_LOSS = min(BRIGHTLINE_BASIS, S1244_LIMIT)
WORTHLESS_CAP_LOSS = BRIGHTLINE_BASIS - S1244_LOSS          # 100,000 LT capital loss (8949 box F, sold 12/31/2025)
COD = 38000                        # Citibank 1099-C, identifiable event 03/18/2025
CARD_BALANCE = 52400               # balance immediately before settlement
SETTLEMENT_PAID = CARD_BALANCE - COD   # 14,400
ASSETS_BEFORE = [("Condominium, 2180 Gulf Shore Blvd N #504 (broker CMA 03/2025)", 288000),
                 ("Brightline Analytics, Inc. 401(k) - Fidelity (03/14/2025 statement) - INCLUDED (Carlson, 116 T.C. 87)", 62400),
                 ("Checking + savings - Gulf Coast Community Bank (03/17/2025)", 4350),
                 ("2019 Subaru Outback (KBB private-party value)", 14500),
                 ("Household furniture and furnishings (garage-sale value)", 5000),
                 ("Jewelry (appraisal 2023, rolled forward)", 2750),
                 ("Brightline Analytics, Inc. stock (operations ceased 01/2025; dissolution plan adopted 02/10/2025)", 0),
                 ("Discretionary interest - Hale Family Settlement (no enforceable right to distributions at 03/2025) - see note", 0)]
LIABS_BEFORE = [("Mortgage - Suncoast Home Lending (payoff statement 03/2025)", 274600),
                ("Citibank Double Cash ****7781 (the settled card)", CARD_BALANCE),
                ("American Express ****1009", 6100),
                ("Auto loan - Gulf Coast Community Bank (Subaru)", 21700),
                ("Federal student loans - MOHELA (MBA)", 38300),
                ("Loan from brother (Daniel Abernathy) - signed promissory note 2024", 12000),
                ("LightStream personal loan ($15,000) + NCH Healthcare medical bills ($4,900)", 19900)]
ASSETS = sum(a for _, a in ASSETS_BEFORE)
LIABS = sum(a for _, a in LIABS_BEFORE)
INSOLVENCY = max(0, LIABS - ASSETS)
EXCLUDED = min(COD, INSOLVENCY)
assert (ASSETS, LIABS, INSOLVENCY, EXCLUDED) == (377000, 425000, 48000, 38000)

# 691(c) - per estate attorney letter (federal estate tax only)
EST_TAX_WITH = 1764000
EST_TAX_WITHOUT = 804000
IRD_IN_ESTATE = 2400000            # father's IRA included in gross estate
IRA_WITHDRAWN = 150000
IRD_TAX = EST_TAX_WITH - EST_TAX_WITHOUT                 # 960,000
D691C = r(IRD_TAX * IRA_WITHDRAWN / IRD_IN_ESTATE)       # 60,000
assert D691C == 60000
WRONG_TAB18 = IRD_IN_ESTATE - EST_TAX_WITH               # 636,000 - original workbook formula (meaningless)
CT_ESTATE_TAX = 1131000            # Connecticut estate tax (not part of 691(c))

# Foreign trust (Hale Family Settlement, Jersey) - FNTBS actual method
FT_DIST = 120000
FT_INT, FT_QDIV, FT_LTCG = 15000, 40000, 30000
FT_DNI = FT_INT + FT_QDIV + FT_LTCG                       # 85,000
FT_CORPUS = FT_DIST - FT_DNI                              # 35,000
assert (FT_DNI, FT_CORPUS) == (85000, 35000)

BANK_INT = 41.18
ROLLOVER_401K = 63120.44
WH_IRA = 15000.00
EXT_PAY = 1500
MORT_INT = 14288.40
RE_TAX = 3914.62
SALES_TAX_TABLE = 1412             # IRS Sales Tax Deduction Calculator, FL, no local surtax (WP)
CHARITY = 1800 + 700

# ------------------------------------------------------------------ PERM
C.write_profile(f"""
# EVG1024 - Abernathy, Margaret "Peggy"  (PERM)

*Synthetic client - Project Evergreen training data.*

| Item | Detail |
|---|---|
| Client ID | EVG1024 |
| Taxpayer | Margaret ("Peggy") A. Abernathy, DOB 05/27/1979, SSN XXX-XX-6318 |
| Occupation | Director of Data Science, Paradigm Coastal Health Systems, Inc. (from 06/02/2025). Founder/CEO of Brightline Analytics, Inc. 2019-2025 |
| Address | {ADDR[0]}, {ADDR[1]} (Collier County) - owns condo since 2022; **Florida: no individual income tax return** |
| Filing status | Single, never married, no dependents |
| Contact | Peggy - email peggy.abernathy@example.com, (239) 555-0187; eSign OK |
| Family | Father Harold J. Abernathy (Greenwich, CT) **died 07/14/2025**; brother Daniel Abernathy (co-beneficiary, not a client). Late grandmother Eleanor Hale (UK) - settlor of the Hale Family Settlement (Jersey) |
| Engagement | Client since 2021 (2020-2024 returns). Complex individual tier (quote $2,600 for 2025 - foreign trust / estate items). |
| Brightline Analytics, Inc. | Delaware C corporation (EIN 00-8812045), SaaS analytics for clinics. Peggy bought 1,500,000 common shares at original issuance 06/12/2019 for **$150,000 cash** (stock purchase agreement + board resolution adopting a section 1244 plan in PERM). Capital received by the corporation at that time: $150,000 (Series Seed preferred $600,000 sold to outside investors in 2021 - total paid-in capital $750,000, never over $1M). Revenue from software subscriptions (active) every year. Ceased operations 01/2025 after an acquisition LOI collapsed; plan of dissolution 02/10/2025; certificate of dissolution filed in Delaware 08/22/2025; no distributions to stockholders. |
| Hale Family Settlement | Discretionary trust governed by Jersey law, created 1998 by Eleanor Hale (UK resident, died 2022). Trustee: Ravensworth Trust Company (Jersey) Limited. Foreign NON-grantor trust as to Peggy (settlor was a nonresident alien and is deceased). Peggy is one of five discretionary beneficiaries. First distribution to Peggy in 2025. |
| Prior CPA | Evergreen since 2021 |
""")
F.prior_year_summary(C.perm_file("2024_Form_1040_Return_Summary.pdf", "Prior-year return summary"), "Margaret A. Abernathy",
    "EVG1024", "Single", [
        ["1a", "W-2 wages - Brightline Analytics, Inc. (reduced founder salary)", 48000],
        ["2b", "Taxable interest - Gulf Coast Community Bank", 62],
        ["11", "AGI", 48062], ["12", "Standard deduction", 14600], ["15", "Taxable income", 33462],
        ["16", "Tax", 3785], ["24", "Total tax", 3785], ["35a", "Refund", 655]],
    carryovers=[["Capital loss carryover", 0], ["Charitable carryover", 0]],
    notes="PY WP: Brightline Analytics is struggling (founder salary cut to $48k; acquisition talks with a larger health-IT "
          "company in progress). Founder stock basis $150,000 - original issuance for cash 06/12/2019; 1244 plan adopted by "
          "the board (copies in PERM). If the company fails, test IRC 1244 (single limit $50,000) and the year of "
          "worthlessness. Condo mortgage ~$275k. No foreign accounts.")
statement(C.perm_file("Brightline_2019_Stock_Purchase_Agreement_and_1244_resolution.pdf", "Legal document - stock issuance"),
    "Brightline Analytics, Inc. - Common Stock Purchase Agreement (06/12/2019) and Board Resolution (extract)", [
        {"table": [["Term", "Detail"], ["Issuer", "Brightline Analytics, Inc., a Delaware corporation (EIN 00-8812045)"],
                   ["Purchaser", "Margaret A. Abernathy"], ["Shares", "1,500,000 shares of Common Stock, $0.0001 par"],
                   ["Purchase price", "$0.10 per share - $150,000.00 paid by wire 06/12/2019"],
                   ["Original issuance?", "Yes - newly issued shares (not acquired from another holder)"],
                   ["Capital and paid-in surplus after issuance", "$150,000.00"]], "left_align_cols": [0, 1]},
        {"heading": "Board resolution (06/10/2019)",
         "para": "RESOLVED, that the Common Stock to be issued to the founder is intended to qualify as 'section 1244 stock' within the "
                 "meaning of Section 1244 of the Internal Revenue Code, and the officers are directed to maintain records sufficient "
                 "to establish such qualification (amount and type of consideration received, capitalization, gross receipts)."}])

# ------------------------------------------------------------------ PBC documents
EMP = {"name": "Paradigm Coastal Health Systems, Inc.", "addr1": "8800 Tamiami Trail N, Suite 300", "addr2": "Naples, FL 34108",
       "ein": "00-6630214"}
EE = {"name": T["name"], "addr1": ADDR[0], "addr2": ADDR[1], "ssn": T["ssn"]}
w2 = {"1": 70000.00, "2": 8200.00, "3": 74550.00, "4": 4622.10, "5": 74550.00, "6": 1080.98,
      "12": [("D", 4550.00), ("DD", 6840.00)], "13": ["Retirement plan: X"], "14": [("Start date", "06/02/2025")],
      "control": "PCHS-25-0412"}

F.organizer(C.pbc_file("01_2025_Organizer_completed.pdf", "Client organizer", "2026-02-23"), "Margaret A. Abernathy", "EVG1024",
    general=[("Did your marital status change during 2025?", "No", ""),
             ("Did you change jobs?", "Yes", "Brightline closed; started at Paradigm Coastal 6/2"),
             ("Did you have any debt forgiven or canceled?", "Yes", "Settled my Citi card in March - got a 1099-C, ugh"),
             ("Did you sell or have any stock become worthless?", "Yes", "Brightline is dissolved. Total loss."),
             ("Did you inherit property or receive an inheritance?", "Yes", "Dad passed in July. Took $150k from his IRA."),
             ("Did you receive a distribution from or have an interest in a foreign trust?", "?",
              "Grandma's trust in Jersey sent me money in Oct - it's an inheritance from England so not taxable?"),
             ("Do you have a foreign bank account?", "No", ""),
             ("Did you make estimated tax payments?", "No", "Fidelity withheld 10%"),
             ("Did you receive, sell, exchange digital assets?", "No", "")],
    dependents=[],
    income_rows=[["Wages", "Brightline Analytics, Inc.", 48000, "0 - no paychecks in 2025"],
                 ["Wages", "Paradigm Coastal Health Systems", "", "see W-2"],
                 ["Interest", "Gulf Coast Community Bank", 62, "41"],
                 ["Retirement distributions", "Fidelity", "", "inherited IRA + rolled my old 401k"],
                 ["Other income", "", "", "trust money $120,000 (not income?)"]],
    deductions_rows=[["Mortgage interest", "Suncoast Home Lending", 14710, "see 1098"],
                     ["Real estate taxes", "Collier County (escrow)", 3866, "see 1098"],
                     ["Charitable", "St. Ann Parish, Humane Society of Collier", 900, "2,500"]],
    signature_date="02/20/2026")

F.w2(C.pbc_file("02_W-2_Paradigm_Coastal_Health.pdf", "Form W-2", "2026-02-23"), EMP, EE, w2)
F.f1099_int(C.pbc_file("03_1099-INT_Gulf_Coast_Community_Bank.pdf", "Form 1099-INT", "2026-02-23"),
            ["Gulf Coast Community Bank", "4001 Tamiami Trail N", "Naples, FL 34103", "TIN: 00-5509917"], REC_T, {"1": BANK_INT},
            account="****2207")
CITI = ["Citibank, N.A.", "PO Box 6500", "Sioux Falls, SD 57117", "TIN: 00-0000031"]
c_boxes = [("1", "Date of identifiable event", "03/18/2025"), ("2", "Amount of debt discharged", float(COD)),
           ("3", "Interest, if included in box 2", ""), ("4", "Debt description", "Credit card - Citi Double Cash ****7781"),
           ("5", "Check here if the debtor was personally liable for repayment of the debt", "X"),
           ("6", "Identifiable event code", "F - by agreement"), ("7", "Fair market value of property", "")]
F.f1099(C.pbc_file("04_1099-C_Citibank.pdf", "Form 1099-C", "2026-02-23"), "1099-C", "Cancellation of Debt", CITI, REC_T,
        c_boxes, account="****7781", omb="OMB No. 1545-1424")
# duplicate phone photo of the 1099-C
scanned_pages(C.pbc_file("05_IMG_0331_citi_1099C.pdf", "Photo upload (image)", "2026-02-26", "Client email attachment",
                         "client emailed phone photo"),
    [["Form 1099-C   Cancellation of Debt   2025        Copy B",
      "CREDITOR: Citibank, N.A.  PO Box 6500  Sioux Falls SD 57117",
      "DEBTOR: Margaret A. Abernathy   XXX-XX-6318",
      "2180 Gulf Shore Blvd N Unit 504, Naples FL 34102",
      "Account ****7781",
      "",
      "1 Date of identifiable event      03/18/2025",
      "2 Amount of debt discharged        38000.00",
      "4 Credit card - Citi Double Cash",
      "5 Personally liable  [X]",
      "6 Identifiable event code   F"]], handwritten=False, skew=-2.1, seed=241)
statement(C.pbc_file("06_Citi_settlement_letter_2025-03-04.pdf", "Creditor letter", "2026-02-26"),
    "Citibank, N.A. - Settlement Offer Accepted (Account ending 7781)", [
        {"para": ["Dear Margaret Abernathy,",
                  f"This letter confirms our agreement to accept ${SETTLEMENT_PAID:,.2f} as settlement in full of your Citi Double Cash "
                  f"account ending 7781. Balance on 03/04/2025: ${CARD_BALANCE:,.2f}. Payment due by 03/17/2025.",
                  "Upon receipt of the settlement payment the remaining balance will be forgiven. The forgiven amount may be reported "
                  "to the IRS on Form 1099-C. Please consult your tax advisor."]},
        {"table": [["Item", "Amount"], ["Balance before settlement", float(CARD_BALANCE)], ["Settlement paid 03/17/2025", float(SETTLEMENT_PAID)],
                   ["Amount forgiven (03/18/2025)", float(COD)]], "total_row": True}])
# client-prepared insolvency sheet - WRONG date (12/31/2025), omits 401(k), includes inherited IRA
write_xlsx(C.pbc_file("07_Peggy_insolvency_worksheet_DRAFT.xlsx", "Spreadsheet (client-prepared)", "2026-02-26",
                      "Client email attachment"),
    {"What I own vs owe 12-31-25": [
        ["Item", "Value / balance at 12/31/2025", "Peggy's note"],
        ["Condo", 291000, "Zillow"], ["Inherited IRA (my half of Dad's)", 1048300, "Fidelity Dec stmt"],
        ["Checking/savings", 31200, ""], ["Subaru", 13800, ""], ["401k", "", "left out - can't touch it til 59 1/2"],
        ["Mortgage", -271900, ""], ["Citi card", 0, "settled!"], ["Amex", -2300, ""], ["Car loan", -17400, ""],
        ["Student loans", -36900, ""], ["Daniel loan", -12000, ""], ["LightStream", -11200, ""],
        ["NET", 1022600, "not insolvent :( so I owe tax on the $38k?"]]})
scanned_pages(C.pbc_file("08_Handwritten_list_of_debts_March_2025.pdf", "Handwritten note (scan)", "2026-03-09",
                         "Sharefile upload", "requested by preparer 03/02"),
    [["Peggy - what I owed right before Citi settled (from March stmts)",
      "",
      "Mortgage (Suncoast payoff ltr)      274,600",
      "Citi Double Cash                     52,400",
      "Amex                                  6,100",
      "Subaru loan                          21,700",
      "MOHELA student loans                 38,300",
      "Daniel (promissory note '24)         12,000",
      "LightStream                          15,000",
      "NCH hospital bills                    4,900",
      "",
      "Assets: condo ~288k (Jen's CMA 3/25), 401k 62,400 (3/14 stmt)",
      "  bank 4,350  Subaru 14,500 (KBB)  furniture ~5k  jewelry 2,750",
      "  Brightline stock = 0 (board voted to dissolve 2/10)",
      "Grandma's trust - nothing promised, trustees decide"]], handwritten=True, seed=2408)
statement(C.pbc_file("09_Brightline_dissolution_documents.pdf", "Corporate documents", "2026-02-23"),
    "Brightline Analytics, Inc. - Plan of Dissolution, Certificate of Dissolution and Final Stockholder Notice", [
        {"heading": "Unanimous written consent of the Board and stockholders (02/10/2025)",
         "para": "Approved a plan of complete dissolution and liquidation under DGCL Sections 275 and 281(b). The corporation ceased "
                 "operations on 01/31/2025 following termination of the letter of intent with HealthGrid Holdings."},
        {"heading": "Certificate of Dissolution - filed with the Delaware Secretary of State 08/22/2025", "para": "File No. 7XXXXXX (synthetic)."},
        {"heading": "Final notice to stockholders - Hartley & Rowe LLP, company counsel (12/05/2025)",
         "para": ["The corporation's remaining assets (customer contracts and IP sold for $210,000) were insufficient to satisfy its "
                  "creditors (bank line of credit, landlord, vendors). Series Seed preferred stockholders received no liquidation "
                  "preference payment. **No distribution was made or will be made to holders of Common Stock.** Stock certificates "
                  "are cancelled.",
                  "Stockholders should consult their tax advisors concerning a worthless-stock deduction for 2025."]}])
F.f1099_r(C.pbc_file("10_1099-R_Fidelity_Inherited_IRA.pdf", "Form 1099-R", "2026-02-23"),
          ["Fidelity Management Trust Company", "PO Box 770001", "Cincinnati, OH 45277", "TIN: 00-0000044"],
          ["Margaret A. Abernathy, BENE of", "Harold J. Abernathy (Decd 07/14/2025) Inherited IRA", *ADDR, f"TIN: {T['ssn']}"],
          {"1": float(IRA_WITHDRAWN), "2a": float(IRA_WITHDRAWN), "4": WH_IRA, "7": "4   IRA/SEP/SIMPLE [X]"},
          account="Z70-****551")
F.f1099_r(C.pbc_file("11_1099-R_Fidelity_Brightline_401k_rollover.pdf", "Form 1099-R", "2026-02-23"),
          ["Fidelity Investments Institutional Operations Co.", "PO Box 770003", "Cincinnati, OH 45277", "TIN: 00-0000045"],
          REC_T, {"1": ROLLOVER_401K, "2a": 0.00, "7": "G", "13": "09/22/2025"}, account="Brightline Analytics 401(k) Plan - 61190")
statement(C.pbc_file("12_Fidelity_Inherited_IRA_Dec_2025_statement.pdf", "Account statement", "2026-02-23"),
    "Fidelity - Inherited IRA FBO Margaret A. Abernathy, BENE of Harold J. Abernathy - December 2025 statement (extract)", [
        {"table": [["Item", "Amount"], ["Transfer in from decedent's IRA (50% share) 09/30/2025", 1202640.18],
                   ["Dividends and interest (reinvested inside IRA)", 9811.37], ["Withdrawal 11/12/2025 (gross)", -150000.00],
                   ["Federal withholding 10%", "(15,000.00) - included in gross"], ["Change in value", -14151.55],
                   ["Ending value 12/31/2025", 1048300.00]]},
        {"para": "Note: income earned inside the inherited IRA is not reported to you on Form 1099. Required minimum distributions: "
                 "see the enclosed RMD notice for 2026."}])
statement(C.pbc_file("13_Fidelity_letter_decedent_2025_RMD_satisfied.pdf", "Custodian letter", "2026-03-09",
                     note="requested by preparer 03/02"),
    "Fidelity - Confirmation of 2025 Required Minimum Distribution - Harold J. Abernathy IRA (deceased 07/14/2025)", [
        {"para": ["To the beneficiaries: our records show the account owner (DOB 03/02/1946) satisfied his 2025 required minimum "
                  "distribution in full on 02/14/2025 ($88,640.00). No year-of-death RMD remains for 2025.",
                  "Because the account owner had reached his required beginning date, each designated beneficiary must take annual RMDs "
                  "beginning in 2026 (based on the beneficiary's single life expectancy) and must empty the account by 12/31/2035 "
                  "(10-year rule, Treas. Reg. 1.401(a)(9)-5)."]}])
statement(C.pbc_file("14_1098_Suncoast_Home_Lending.pdf", "Form 1098", "2026-02-23"),
    "Form 1098 - Mortgage Interest Statement 2025 - Suncoast Home Lending", [
        {"table": [["Box", "Description", "Amount"], ["1", "Mortgage interest received", MORT_INT],
                   ["2", "Outstanding mortgage principal (01/01/2025)", 276212.08], ["3", "Mortgage origination date", "04/29/2022"],
                   ["8", "Property address", f"{ADDR[0]}, {ADDR[1]}"], ["10", "Real estate taxes paid from escrow (Collier County, paid 11/2025)", RE_TAX]],
         "left_align_cols": [0, 1]}])
statement(C.pbc_file("15_Charitable_receipts_2025.pdf", "Donation receipts", "2026-02-23"), "2025 charitable contribution receipts", [
    {"table": [["Organization", "Date(s)", "Amount", "Goods/services received"],
               ["St. Ann Catholic Parish, Naples (weekly giving statement)", "2025", 1800.00, "None (intangible religious benefits only)"],
               ["Humane Society of Collier County", "12/01/2025", 700.00, "None"]]}])
write_text(C.pbc_file("16_Email_Peggy_trust_and_IRA_2026-03-02.txt", "Client correspondence", "2026-03-02", "Email"),
"""From: Peggy Abernathy <peggy.abernathy@example.com>
To: preparer@evergreentax.example
Date: Mon, 2 Mar 2026 21:14:55 -0500
Subject: Re: Abernathy 2025 - open items

Hi - answers to your list:

1. Grandma's trust (the Hale Family Settlement in Jersey) wired me $120,000 on Oct 8. The trustees said a "beneficiary
   statement" would come after their year end (they close the books in March). Isn't this just an inheritance from
   England? I didn't think it was taxable. My cousins in London said they pay UK tax on theirs.
2. Dad's estate - the attorney (Whitaker & Lowe in Stamford) says the estate tax return is due in April and they'll send
   us "691(c) information" afterward. My brother Daniel and I split the IRA 50/50. I took $150k out in November to pay
   off stuff.
3. I'll dig up the March balances for the insolvency thing you asked about. My spreadsheet was at year end, sorry.

Should we extend? I'm fine with that.
Peggy
""")
# ---- documents received after the extension
statement(C.pbc_file("17_Hale_Family_Settlement_Foreign_Nongrantor_Trust_Beneficiary_Statement_2025.pdf",
                     "Foreign trust beneficiary statement", "2026-06-19", "Courier (DHL) - scanned by Admin"),
    "Foreign Nongrantor Trust Beneficiary Statement - Tax Year 2025 - The Hale Family Settlement", [
        {"para": "Prepared by the trustee in the format required by the Instructions for Form 3520 (Part III, lines 31-33) for "
                 "U.S. beneficiaries. Amounts stated in U.S. dollars translated at the spot rate on the date of each item (trustee's "
                 "U.S. tax adviser)."},
        {"table": [["Item", "Detail"], ["Trust", "The Hale Family Settlement (settled 14 May 1998), Jersey, Channel Islands"],
                   ["Trustee", "Ravensworth Trust Company (Jersey) Limited, 12 Esplanade, St Helier JE2 3QA"],
                   ["Trust EIN / reference", "None / RTC-HFS-1998"],
                   ["Grantor (settlor)", "Eleanor M. Hale (UK resident; deceased 2022) - trust is a foreign NON-grantor trust"],
                   ["U.S. beneficiary", "Margaret A. Abernathy (XXX-XX-6318)"],
                   ["U.S. agent", "Yes - Hollis & Crane LLP, 30 Rockefeller Plaza, New York NY (agent agreement dated 04/01/2025 attached)"],
                   ["Method", "ACTUAL method - trust books and records available to the IRS through the U.S. agent"]],
         "left_align_cols": [0, 1]},
        {"heading": "Distribution to the beneficiary during the trust's 2025 tax year (calendar year)",
         "table": [["Date", "Description", "Amount (USD)"], ["10/06/2025", "Cash (GBP 89,552.24 wired; USD received)", float(FT_DIST)]]},
        {"heading": "Character of the distribution (Treas. Reg. 1.643/IRC 661-662 tier rules; IRC 643(a)(6) foreign trust DNI)",
         "table": [["Item", "Amount (USD)"],
                   ["Interest income (Jersey bank deposits; gilts) - foreign source", float(FT_INT)],
                   ["Dividends - UK resident companies (qualified foreign corporations - US-UK treaty); holding periods met", float(FT_QDIV)],
                   ["Net long-term capital gain (included in foreign trust DNI - IRC 643(a)(6)(C))", float(FT_LTCG)],
                   ["Total distributable net income (current year) distributed", float(FT_DNI)],
                   ["Distribution of corpus (principal) - not taxable", float(FT_CORPUS)],
                   ["Accumulation distribution (throwback) - undistributed net income at 12/31/2024 = $0", 0.0],
                   ["Total distribution", float(FT_DIST)]], "total_row": True},
        {"heading": "Foreign taxes", "para": "No foreign income tax was withheld or paid on the distributed income (Jersey does not tax "
                                             "non-resident beneficiaries; UK dividends carry no withholding)."},
        {"heading": "Statement of trustee",
         "para": "The trust has no undistributed net income from prior years because all distributable net income for 2022-2024 was "
                 "distributed currently to the UK-resident beneficiaries. This statement may be relied on by the beneficiary for the "
                 "actual (non-default) method on Form 3520."}],
    footer="Ravensworth Trust Company (Jersey) Limited - Director signature on file - 12 June 2026")
statement(C.pbc_file("18_Gulf_Coast_Community_Bank_incoming_wire_advice.pdf", "Bank advice", "2026-06-19"),
    "Gulf Coast Community Bank - Incoming International Wire Advice", [
        {"table": [["Field", "Value"], ["Credit date", "10/08/2025"], ["Beneficiary", "Margaret A. Abernathy ****2207"],
                   ["Ordering customer", "RAVENSWORTH TRUST CO (JERSEY) LTD RE HALE SETTLEMENT"], ["Original amount", "GBP 89,552.24"],
                   ["USD credited", "120,000.00"], ["Reference", "BENEFICIARY DISTRIBUTION"]], "left_align_cols": [0, 1]}])
statement(C.pbc_file("19_Whitaker_Lowe_estate_tax_691c_letter_2026-07-10.pdf", "Estate attorney letter", "2026-07-13", "Email attachment"),
    "Whitaker & Lowe LLP - Estate of Harold J. Abernathy - Information for Beneficiaries (IRC 691(c))", [
        {"para": ["Dear Ms. Abernathy and Mr. Abernathy,",
                  "The federal estate tax return (Form 706) for the Estate of Harold J. Abernathy (date of death 07/14/2025) was filed on "
                  "04/10/2026 and the tax shown was paid. The following information is provided so that you may compute the deduction "
                  "for estate tax attributable to income in respect of a decedent (IRC 691(c)) when you receive distributions from the "
                  "inherited IRA."]},
        {"table": [["Item", "Amount"], ["Federal estate tax (Form 706, after credits)", float(EST_TAX_WITH)],
                   ["Federal estate tax recomputed excluding the IRA (net value of IRD items)", float(EST_TAX_WITHOUT)],
                   ["Federal estate tax attributable to IRD", float(IRD_TAX)],
                   ["IRD included in gross estate - Fidelity IRA (date-of-death value)", float(IRD_IN_ESTATE)],
                   ["Connecticut estate tax paid (separate; deducted under IRC 2058 on Form 706)", float(CT_ESTATE_TAX)]]},
        {"para": "Each beneficiary owns 50% of the IRA. The deduction is allowed in the year IRD is included in your income, in "
                 "proportion to the IRD you include over the total IRD. Only the federal estate tax enters the computation. "
                 "Please share this letter with your tax preparer."}])

# ------------------------------------------------------------------ RETURN
facts = {
    "status": "S",
    "taxpayer": {"age65": False},
    "w2": [{"who": "T", "box1": w2["1"], "box2": w2["2"], "box3": w2["3"], "box4": w2["4"], "box5": w2["5"], "box6": w2["6"]}],
    "interest": [{"payer": "Gulf Coast Community Bank", "amount": BANK_INT},
                 {"payer": "Hale Family Settlement (Jersey foreign trust) - interest per Foreign Nongrantor Trust Beneficiary Statement",
                  "amount": FT_INT}],
    "dividends": [{"payer": "Hale Family Settlement (Jersey foreign trust) - UK-company dividends per FNTBS (qualified)",
                   "ordinary": FT_QDIV, "qualified": FT_QDIV}],
    "foreign_trust": True,
    "ira": [{"gross": IRA_WITHDRAWN, "taxable": IRA_WITHDRAWN}],
    "pension": [{"gross": ROLLOVER_401K, "taxable": 0}],
    "trades": [{"box": "F", "id": "1", "desc": "Brightline Analytics, Inc. - 1,500,000 sh common - WORTHLESS (IRC 165(g)(1)); "
                "cost 150,000 less 50,000 claimed as IRC 1244 ordinary loss on Form 4797",
                "acq": "06/12/2019", "sold": "12/31/2025", "proceeds": 0, "basis": WORTHLESS_CAP_LOSS}],
    "k1_lt": FT_LTCG,   # foreign trust net LT capital gain per FNTBS (Schedule D line 12 - estates/trusts)
    "sch1": {"f4797": -S1244_LOSS},
    "itemized": {"state_income_tax": SALES_TAX_TABLE, "use_sales_tax": True, "real_estate_tax": RE_TAX,
                 "mortgage_interest_1098": MORT_INT, "charity_cash": CHARITY, "other_itemized": D691C,
                 "other_itemized_desc": "Federal estate tax on income in respect of a decedent (IRC 691(c)) - statement attached"},
    "withholding_1099": WH_IRA,
    "extension_payment": EXT_PAY,
}
# NIIT: interest + dividends + net gain (Form 8960 line 5: net capital loss limited to the 1211(b) $3,000; the 1244 ordinary
# loss is not allowed to take net gain below zero - Reg. 1.1411-4(d)(2); conservative position flagged to signer)
nii = r(BANK_INT + FT_INT) + FT_QDIV - 3000
facts["niit"] = {"nii": nii, "gross": nii}
R = Return1040(facts).compute()
v = R.values
sd = v["sch_d"]
co_before = v["capital_loss_carryover_2026"]
co_after_lt = max(0, co_before["lt"] - EXCLUDED)
assert co_before == {"st": 0, "lt": 67000, "total": 67000} and co_after_lt == 29000
magi_excess = v["11"] - 200000
niit_alt = r(min(max(0, nii - S1244_LOSS), magi_excess) * .038)   # if the 1244 loss reduced NII
# tax if the 1099-C had been left in income (for the notes)
R_cod = Return1040({**facts, "sch1": {**facts["sch1"], "other": [("8c", "Cancellation of debt", COD)]}}).compute()
cod_tax = R_cod.values["24"] - v["24"]

f4797 = [["Form 4797 Part II - Ordinary gains and losses (line 10)", "Amount"],
         ["Brightline Analytics, Inc. common stock - IRC 1244 loss (acquired 06/12/2019 at original issuance for cash; "
          "worthless 2025 - dissolved, no distributions)", -S1244_LOSS],
         ["Limit: $50,000 (single). Corporation was a domestic small business corporation (capital received <= $1,000,000 when "
          "issued); > 50% of gross receipts from active software subscriptions for the 5 years before the loss", ""],
         ["Excess of basis over the 1244 limit -> Form 8949 box F (capital) - see Schedule D", WORTHLESS_CAP_LOSS],
         ["Line 18b / Schedule 1 line 4", -S1244_LOSS]]
f982 = [["Form 982 - Reduction of Tax Attributes Due to Discharge of Indebtedness", "Amount"],
        ["Line 1b - Discharge of indebtedness to the extent insolvent (not in a title 11 case)", "X"],
        ["Line 2 - Total amount of discharged indebtedness excluded from gross income (Citibank 1099-C)", EXCLUDED],
        ["Line 9 - Applied to reduce net capital loss for 2025 and capital loss carryovers to 2025 (verify line number "
         "in current revision)", EXCLUDED],
        ["All other Part II lines (NOL, credits, basis, passive, FTC)", 0],
        ["Reduction is made AFTER the 2025 tax is determined (IRC 108(b)(4)(A)): the 2025 $3,000 capital loss deduction is "
         "unaffected; the 2026 carryover falls from " + f"{co_before['total']:,} to {co_after_lt:,}", ""]]
insolv = [["Insolvency worksheet - immediately before discharge (03/17/2025)", "FMV / balance"]] + \
         [[d, a] for d, a in ASSETS_BEFORE] + [["Total assets", ASSETS]] + [[d, a] for d, a in LIABS_BEFORE] + \
         [["Total liabilities", LIABS], ["Insolvency (liabilities - assets)", INSOLVENCY],
          ["1099-C amount", COD], ["Excluded (lesser of COD or insolvency)", EXCLUDED], ["Taxable COD income", COD - EXCLUDED],
          ["Not counted: inherited IRA (father died 07/14/2025 - after the discharge); balances at 12/31/2025 (client draft) are "
           "the wrong date", ""]]
d691 = [["IRC 691(c) deduction - Schedule A line 16", "Amount"],
        ["Federal estate tax (Form 706)", EST_TAX_WITH], ["Federal estate tax without the IRA", EST_TAX_WITHOUT],
        ["Estate tax attributable to IRD", IRD_TAX], ["Total IRD in the estate (IRA)", IRD_IN_ESTATE],
        ["IRD included in Peggy's 2025 income (1099-R code 4)", IRA_WITHDRAWN],
        [f"Deduction = {IRD_TAX:,} x {IRA_WITHDRAWN:,} / {IRD_IN_ESTATE:,}", D691C],
        ["Connecticut estate tax - not included (IRC 691(c) uses federal estate tax only)", 0],
        ["Not a miscellaneous itemized deduction (IRC 67(b)(7)) - no 2% floor / not suspended", ""],
        ["Remaining 691(c) pool for Peggy's future withdrawals: 960,000 x 50% - 60,000", r(IRD_TAX * .5) - D691C]]
f3520 = [["Form 3520 Part III - distributions to a U.S. person from a foreign trust (filed separately)", "Detail"],
         ["Trust", "The Hale Family Settlement, Jersey - foreign non-grantor trust; U.S. agent appointed (Hollis & Crane LLP)"],
         ["Line 24 - cash distribution 10/06/2025", f"${FT_DIST:,}"],
         ["Lines 31-33 - Foreign Nongrantor Trust Beneficiary Statement received; ACTUAL method",
          f"DNI ${FT_DNI:,} (interest {FT_INT:,}; qualified dividends {FT_QDIV:,}; net LTCG {FT_LTCG:,}); corpus ${FT_CORPUS:,}"],
         ["Accumulation distribution / Form 4970 / interest charge", "None - undistributed net income $0 (no throwback)"],
         ["Due / filing", "Due 10/15/2026 (with the extended 1040); paper only - mailed separately to IRS Ogden (certified mail)"],
         ["Penalty if not filed", "Greater of $10,000 or 35% of the distribution (IRC 6677) - i.e. $42,000"]]
f8938 = [["Form 8938 (single, living in the U.S.: > $50,000 at year end or > $75,000 at any time)", "Detail"],
         ["Specified foreign financial asset", "Beneficial interest in the Hale Family Settlement (foreign trust)"],
         ["Value for threshold (Reg. 1.6038D-5(f)): distributions received in 2025 (no mandatory interest)", f"${FT_DIST:,}"],
         ["Part IV - excepted (duplicative reporting, Reg. 1.6038D-7): reported on Form 3520", "Number of Forms 3520: 1"],
         ["FBAR", "Not required - no foreign financial account; a discretionary beneficiary does not report the trust's accounts"]]
co_stmt = [["Capital loss carryover to 2026 (after IRC 108(b) reduction)", "ST", "LT", "Total"],
           ["Schedule D 2025: net ST / net LT", sd["net_st"], sd["net_lt"], sd["line16"]],
           ["Allowed in 2025 (line 21)", 0, -3000, -3000],
           ["Carryover before attribute reduction (Capital Loss Carryover Worksheet)", co_before["st"], co_before["lt"], co_before["total"]],
           ["Form 982 line 9 reduction", 0, -EXCLUDED, -EXCLUDED],
           ["Carryover to 2026 - enter as override in 2026 proforma", 0, co_after_lt, co_after_lt]]
C.write_return(R, [
    ("Taxpayer", "Margaret A. Abernathy (XXX-XX-6318)"),
    ("Address", ", ".join(ADDR)),
    ("Filing status", "Single"),
    ("Dependents", "None"),
    ("Digital assets question", "No"),
    ("Forms included", "1040, Schedules 1, 2, A, B (Part III line 8: Yes - distribution from a foreign trust), D, Form 8949, "
                       "Form 4797, Form 982, Form 8960, Form 8938; statements: IRC 691(c), worthless stock / 1244, foreign trust "
                       "character. Separately: Form 3520 (paper, IRS Ogden)"),
    ("Extension", f"Form 4868 filed 04/13/2026 with ${EXT_PAY:,} payment"),
    ("State", "None - Florida has no individual income tax"),
    ("Filing method", "E-file 1040 (8879 signed 09/16/2026), accepted 09/18/2026; Form 3520 mailed 09/21/2026 (certified); "
                      "refund by direct deposit Gulf Coast Community Bank ****2207"),
], attachments=[("Form 4797 Part II - IRC 1244 ordinary loss", f4797),
                ("Insolvency worksheet (Form 982 support)", insolv),
                ("Form 982 - exclusion and attribute reduction", f982),
                ("Statement - capital loss carryover after attribute reduction", co_stmt),
                ("Statement - IRC 691(c) deduction (Schedule A line 16)", d691),
                ("Form 8938 - Statement of Specified Foreign Financial Assets", f8938),
                ("Form 3520 Part III - foreign trust distribution (filed separately, not part of e-file)", f3520)])

gotchas = [
    gotcha("EVG1024-G1", "Schedule D (worthless stock / IRC 1244)", "Founder stock in a dissolved C corp - 1244 split",
           "Report the full $150,000 as a capital loss (only $3,000 usable) - or the full $150,000 as ordinary.",
           f"Original-issue stock for cash in a qualifying small business corporation -> IRC 1244 ordinary loss up to $50,000 (single) "
           f"on Form 4797 Part II line 10 (Schedule 1 line 4: {fmt(-S1244_LOSS)}); the excess $100,000 is a long-term capital loss "
           "on Form 8949 box F.", "Ordinary deduction understated $47,000 if all treated as capital", ["8", "Sch 1 line 4", "Form 4797"], "medium"),
    gotcha("EVG1024-G2", "Schedule D", "Worthless security - timing, holding period and the $3,000 limit",
           "No 1099-B -> nothing reported; or report as a 2026 loss (final notice dated 12/05/2025); or short-term.",
           "Stock became wholly worthless in 2025 (dissolution, no stockholder distributions); IRC 165(g) treats it as sold on "
           f"12/31/2025 -> long-term (held since 2019), box F. Nets with the trust's $30,000 LTCG: Schedule D line 16 {fmt(sd['line16'])}, "
           "deduction limited to $3,000.", "Loss year/character", ["7", "Sch D", "Form 8949"], "medium"),
    gotcha("EVG1024-G3", "Return - Form 982 (insolvency)", "1099-C $38,000 - insolvency measured immediately before the discharge",
           "Include $38,000 on Schedule 1 line 8c (client's year-end worksheet shows she is solvent once the inherited IRA is counted), "
           "or exclude it without a balance sheet; or leave the 401(k) out of assets.",
           f"Insolvency is tested immediately before the 03/18/2025 discharge: assets {fmt(ASSETS)} (incl. the 401(k) - Carlson) vs "
           f"liabilities {fmt(LIABS)} (incl. the full card balance) -> insolvent {fmt(INSOLVENCY)} >= $38,000 -> exclude all of it "
           "(Form 982 line 1b/2). The July inheritance is irrelevant (after the discharge).",
           f"Tax overstated ~{fmt(cod_tax)} if included", ["8", "Form 982"], "hard"),
    gotcha("EVG1024-G4", "Return - Form 982 Part II (attribute reduction)", "Excluded COD reduces the capital loss carryover",
           "Exclude the $38,000 and carry the full capital loss forward (software proformas $67,000).",
           f"IRC 108(b)(2): no NOL or credit carryovers, so the excluded amount reduces the 2025 net capital loss / carryover - after the "
           f"2025 tax is computed. 2026 LT carryover = {fmt(co_before['total'])} - {fmt(EXCLUDED)} = {fmt(co_after_lt)}. Manual "
           "override in the 2026 proforma; Form 982 line 9.", "2026 carryover overstated $38,000", ["Form 982", "Sch D carryover"], "hard"),
    gotcha("EVG1024-G5", "Estate Implications (IRC 691(c) - income in respect of a decedent)", "Estate tax deduction on inherited IRA withdrawals",
           f"Miss the deduction; or deduct the full $960,000; or use the workbook's original IRA value - estate tax formula "
           f"({fmt(WRONG_TAB18)}); or include Connecticut estate tax.",
           f"691(c) = federal estate tax attributable to IRD x IRD received / total IRD = 960,000 x 150,000 / 2,400,000 = {fmt(D691C)}, "
           "Schedule A line 16 (not subject to the 2% floor - IRC 67(b)(7)). Federal estate tax only.",
           f"Itemized deductions understated {fmt(D691C)}", ["12e", "Sch A line 16"], "hard"),
    gotcha("EVG1024-G6", "Client IRAs (inherited IRA)", "Inherited IRA distribution - code 4, RMD rules",
           "Apply the 10% early-distribution tax (she is 46); or treat the 2025 withdrawal as a required RMD; or ignore the 10-year rule.",
           "Code 4 (death) - no 10% additional tax. Father died after his required beginning date and took his 2025 RMD (Fidelity letter) -> "
           "no year-of-death RMD; annual RMDs required 2026-2034 and the account must be emptied by 12/31/2035. The 401(k) direct "
           "rollover (code G) is nontaxable (5a 63,120 / 5b 0).", "Sch 2 / planning", ["4b", "5b"], "medium"),
    gotcha("EVG1024-G7", "Foreign Trusts", "Foreign trust distribution taxed under the ACTUAL method",
           "Treat the $120,000 as a nontaxable foreign inheritance (client's view); or tax all $120,000 as ordinary income; or apply the "
           "default method / throwback (Form 4970 interest charge).",
           f"A Foreign Nongrantor Trust Beneficiary Statement (with a U.S. agent) supports the actual method: DNI {fmt(FT_DNI)} keeps its "
           f"character - interest {fmt(FT_INT)} (Sch B), UK qualified dividends {fmt(FT_QDIV)} (3a/3b), net LTCG {fmt(FT_LTCG)} (foreign "
           f"trust DNI includes capital gains) to Schedule D; corpus {fmt(FT_CORPUS)} not taxable. UNI $0 -> no accumulation "
           "distribution, no interest charge.", "Income and rate character", ["2b", "3a", "3b", "7"], "hard"),
    gotcha("EVG1024-G8", "Foreign Trusts / Paper Filing Returns", "Form 3520, Schedule B Part III and Form 8938",
           "Skip Form 3520 (income already on the 1040) or try to e-file it with the 1040; answer Schedule B line 8 'No'; skip Form 8938.",
           "Form 3520 Part III is required for any distribution from a foreign trust (penalty greater of $10,000 or 35%); it is a separate "
           "paper filing to IRS Ogden due 10/15/2026 with the extended return. Schedule B Part III line 8 = Yes. Form 8938: value of the "
           "beneficial interest = distributions received $120,000 > $75,000 -> file, Part IV excepted (reported on Form 3520). The 1040 itself "
           "can still be e-filed.", "Penalty exposure $42,000", ["Sch B line 8", "Form 3520", "Form 8938"], "medium"),
    gotcha("EVG1024-G9", "NIIT", "Net investment income - MAGI limb binds",
           "No NIIT because the 1244 loss and capital loss wipe out investment income; or NIIT on all $55,041 of trust and bank income.",
           f"NII = interest {fmt(r(BANK_INT + FT_INT))} + dividends {fmt(FT_QDIV)} + net gain limited to the $3,000 capital loss = "
           f"{fmt(nii)} (position: the 1244 ordinary loss cannot take Form 8960 net gain below zero - Reg. 1.1411-4(d)(2)). MAGI excess "
           f"{fmt(magi_excess)} is smaller -> NIIT {fmt(v['niit'])}. The IRA distribution is not NII.",
           f"NIIT {fmt(v['niit'])} (alternative position {fmt(niit_alt)})", ["23", "Form 8960"], "medium"),
]
C.write_answer_key(R, {"residence": "FL - Naples (no state income tax)", "complexity": "Complex individual - estate / foreign trust / COD"},
                   gotchas,
                   filings=[{"form": "Form 4868", "filed": "2026-04-13", "payment": EXT_PAY},
                            {"form": "Form 1040 incl. 4797, 982, 8938, 8960", "method": "e-file", "due": "2026-10-15", "filed": "2026-09-18"},
                            {"form": "Form 3520 (Part III)", "method": "paper - IRS Ogden, certified mail", "due": "2026-10-15", "filed": "2026-09-21"}],
                   extra={"carryforwards_to_2026": {"capital_loss_carryover_2026": {"st": 0, "lt": co_after_lt, "total": co_after_lt},
                                                    "capital_loss_carryover_before_form_982_reduction": co_before,
                                                    "form_982_attribute_reduction": EXCLUDED,
                                                    "irc_691c_remaining_pool_for_future_ird": r(IRD_TAX * .5) - D691C},
                          "insolvency": {"assets": ASSETS, "liabilities": LIABS, "insolvency": INSOLVENCY, "cod": COD, "excluded": EXCLUDED},
                          "irc_1244": {"basis": BRIGHTLINE_BASIS, "ordinary_4797": -S1244_LOSS, "capital_8949": -WORTHLESS_CAP_LOSS},
                          "irc_691c": {"estate_tax_with": EST_TAX_WITH, "estate_tax_without": EST_TAX_WITHOUT, "ird_total": IRD_IN_ESTATE,
                                       "ird_received": IRA_WITHDRAWN, "deduction": D691C},
                          "foreign_trust": {"distribution": FT_DIST, "dni": FT_DNI, "interest": FT_INT, "qualified_dividends": FT_QDIV,
                                            "net_ltcg": FT_LTCG, "corpus": FT_CORPUS, "method": "actual", "accumulation_distribution": 0},
                          "assumptions": ["Form 8960: 1244 ordinary loss does not reduce net gain below zero (Reg. 1.1411-4(d)(2)); "
                                          f"alternative NIIT {niit_alt}",
                                          "Discretionary interest in the Hale Family Settlement valued at $0 for insolvency (no enforceable "
                                          "right at 03/2025); even a $10,000 value leaves her insolvent by $38,000",
                                          "Form 982 Part II capital-loss line cited as line 9 - verify against current revision",
                                          "Father satisfied his 2025 RMD (Fidelity letter)"]})

C.write_receipt_log("EVG1024-1040-2025", "T. Nguyen (staff)", "R. Patel (senior)", "S. Kennedy, CPA", "2026-02-23",
                    extension=f"Filed 04/13/2026 with ${EXT_PAY:,} payment - foreign trust beneficiary statement and estate "
                              "691(c) information outstanding")
C.write_notes(f"""
# EVG1024 - Abernathy, Margaret "Peggy" - 2025 Form 1040 - Preparer Notes

*Synthetic client - Project Evergreen. Return status: **signed off; extended return e-filed 09/18/2026 (accepted);
Form 3520 mailed separately 09/21/2026 (certified mail).***

## Return summary
| | |
|---|---|
| Filing status | Single |
| Wages | {fmt(v['1a'])} (Paradigm Coastal, from 06/02/2025) |
| Interest / dividends | {fmt(v['2b'])} / {fmt(v['3b'])} (qualified {fmt(v['3a'])}) - mostly the foreign trust |
| IRA distributions (4b) | {fmt(v['4b'])} (inherited IRA, code 4); 401(k) rollover 5a {fmt(v['5a'])} / 5b {fmt(v['5b'])} |
| Capital gain or (loss) (line 7) | {fmt(v['7'])} (Schedule D line 16 {fmt(sd['line16'])}) |
| Schedule 1 line 4 (Form 4797) | {fmt(-S1244_LOSS)} - IRC 1244 ordinary loss |
| AGI (line 11) | {fmt(v['11'])} |
| Itemized deductions | {fmt(v['12e'])} (incl. IRC 691(c) {fmt(D691C)}) vs standard $15,750 |
| Taxable income | {fmt(v['15'])} |
| Tax (line 16) | {fmt(v['16'])} |
| NIIT | {fmt(v['niit'])} |
| Total tax | {fmt(v['24'])} |
| Payments | W-2 {fmt(v['25a'])} + 1099-R {fmt(v['25b'])} + extension {fmt(EXT_PAY)} = {fmt(v['33'])} |
| **Refund** | **{fmt(v['refund'])}** |
| Capital loss carryover to 2026 | **{fmt(co_after_lt)} LT** (after Form 982 reduction of {fmt(EXCLUDED)}) |

## What I did and why (plain English)
1. **Brightline stock - IRC 1244 + worthless stock.** Peggy bought 1,500,000 founder shares at original issuance for $150,000 cash
   (2019 SPA and 1244 board resolution in PERM). The company never had more than $750,000 of paid-in capital and earned its
   receipts from software subscriptions - a qualifying small business corporation. It stopped operating in January, adopted a plan
   of dissolution 02/10/2025, filed its Delaware certificate of dissolution 08/22/2025, and counsel's final notice confirms common
   holders get nothing - the stock became wholly worthless in 2025 (it still had value in 2024 while the acquisition was pending).
   Worthless stock is treated as sold on the last day of the year (IRC 165(g)) -> 12/31/2025, long-term. The first **$50,000**
   (single limit) is an ordinary loss under IRC 1244 on Form 4797 Part II; the other **$100,000** is a long-term capital loss on
   Form 8949 box F (no 1099-B).
2. **Foreign trust distribution (actual method).** Peggy's view was "foreign inheritance - not taxable." The $120,000 came from a
   foreign NON-grantor trust (Jersey; settlor was her UK grandmother, now deceased), so it is taxable to the extent of DNI. The trustee's
   Foreign Nongrantor Trust Beneficiary Statement (received 06/19/2026 - main reason for the extension) supports the **actual method**
   (U.S. agent appointed): interest {fmt(FT_INT)} (Schedule B), UK dividends {fmt(FT_QDIV)} - qualified (UK companies are qualified
   foreign corporations under the treaty; character passes through the trust), net long-term gain {fmt(FT_LTCG)} (a foreign trust's
   DNI includes capital gains - IRC 643(a)(6)(C)) on Schedule D line 12, and {fmt(FT_CORPUS)} of corpus, which is not taxable.
   Undistributed net income from prior years is $0, so there is **no accumulation distribution, no throwback and no Form 4970 /
   interest charge**. Using the default method would have been wrong (and costly) once an actual-method statement exists.
3. **Form 3520 / Schedule B / Form 8938.** Form 3520 Part III reports the distribution (penalty for not filing: greater of $10,000 or
   35% = $42,000). Form 3520 is never part of the e-file - mailed separately to IRS Ogden on 09/21/2026, certified, with the FNTBS.
   Schedule B Part III line 8 answered **Yes**. Form 8938: a beneficiary's interest in a foreign trust is a specified foreign financial
   asset; its value is the distributions received ($120,000) > $75,000 any-time threshold (single, living in the U.S.) -> filed, with
   the trust listed as an excepted asset in Part IV (reported on Form 3520). No FBAR - she has no foreign account and a discretionary
   beneficiary does not report the trust's accounts. The 1040 itself was e-filed.
4. **1099-C - insolvency exclusion (Form 982).** Citi forgave {fmt(COD)} on 03/18/2025. Peggy's own spreadsheet used 12/31/2025
   balances, counted her half of Dad's IRA and left out her 401(k) - wrong on all three counts. Insolvency is measured **immediately
   before the discharge**: from her March statements (handwritten list received 03/09) assets {fmt(ASSETS)} including the 401(k)
   (retirement accounts count - Carlson v. Commissioner) and liabilities {fmt(LIABS)} including the full {fmt(CARD_BALANCE)} card
   balance -> insolvent by **{fmt(INSOLVENCY)}**, so the whole {fmt(COD)} is excluded (Form 982 line 1b / line 2). The inheritance
   (July) came after the discharge and does not matter. Her discretionary interest in the Jersey trust was valued at $0 - she had no
   enforceable right to anything in March 2025; even a $10,000 value would leave her insolvent by more than $38,000. Including the
   COD in income would have cost about {fmt(cod_tax)} of tax.
5. **Attribute reduction (IRC 108(b)).** The excluded amount must reduce tax attributes in order: no NOL, no credits -> the 2025 net
   capital loss / carryover. The reduction is made after the 2025 tax is figured, so the $3,000 deduction stays. 2026 carryover:
   {fmt(co_before['total'])} (Capital Loss Carryover Worksheet) - {fmt(EXCLUDED)} = **{fmt(co_after_lt)} long-term** (Form 982 line 9).
   Both packages proforma the unreduced {fmt(co_before['total'])} - override in the 2026 proforma (diary note set).
6. **Inherited IRA and IRC 691(c).** Peggy (50% beneficiary) withdrew $150,000 (1099-R code 4 - no 10% tax; 10% withheld). Dad had
   reached his required beginning date and took his 2025 RMD on 02/14/2025 (Fidelity letter), so nothing more was required for 2025.
   From 2026 she must take annual RMDs over her single life expectancy and empty the account by 12/31/2035. The estate paid federal
   estate tax; the attorney's letter gives the "with and without" computation: 1,764,000 - 804,000 = **960,000** attributable to the
   $2,400,000 IRA. Deduction = 960,000 x 150,000 / 2,400,000 = **{fmt(D691C)}**, Schedule A line 16 (IRC 67(b)(7) - not a
   miscellaneous itemized deduction, no floor). Connecticut estate tax is not part of the computation. Remaining pool for her future
   withdrawals: {fmt(r(IRD_TAX * .5) - D691C)}. (The firm workbook's original tab 18 formula - IRA value minus estate tax =
   {fmt(WRONG_TAB18)} - is meaningless; the corrected tab is typed over per the Corrections Log.)
7. **Itemized deductions.** 691(c) {fmt(D691C)} + mortgage interest {fmt(r(MORT_INT))} + Collier property tax {fmt(r(RE_TAX))} +
   Florida sales tax (IRS table, no state income tax) {fmt(SALES_TAX_TABLE)} + charity {fmt(CHARITY)} = {fmt(v['12e'])}.
8. **NIIT.** MAGI {fmt(v['11'])} > $200,000. Net investment income = interest + dividends + net gain, where the net capital loss
   counts only to the $3,000 limit = {fmt(nii)}; I did **not** let the 1244 ordinary loss push Form 8960 net gain below zero
   (Reg. 1.1411-4(d)(2)) - conservative position flagged for the signer (if the 1244 loss were allowed, NIIT would be
   {fmt(niit_alt)} instead of {fmt(v['niit'])}). The MAGI excess ({fmt(magi_excess)}) is the smaller amount, so NIIT = {fmt(v['niit'])}.
9. **Estimated tax penalty.** None: 2024 tax was $3,785 and 2025 withholding alone was {fmt(v['25d'])} (withholding is treated as
   paid evenly).

## Open items / client communication
- 2026 planning letter: annual inherited-IRA RMDs start 2026 (10-year deadline 12/31/2035); claim 691(c) on every future withdrawal
  ({fmt(r(IRD_TAX * .5) - D691C)} pool left); expect a 2026 FNTBS from the trustee for any further distributions.
- Capital loss carryover to 2026 = {fmt(co_after_lt)} LT (NOT the {fmt(co_before['total'])} the software proformas).
- If the estate's Form 706 is examined and the estate tax changes, the 691(c) deduction must be recomputed (amend).

## Hand-off to signer / routing
- [x] Return locked; Accountant's copy saved as *reviewed*
- [x] Federal 1040 - e-file (Form 3520 is not part of the e-file); due 10/15/2026 (extended)
- [x] **Form 3520** - paper, mailed separately to IRS Ogden 09/21/2026 (certified; tracking in WP), FNTBS attached
- [x] Form 8938 included in e-file; no FBAR (no foreign account)
- [x] No state (FL)
- [x] eSign 8879 by email; refund by direct deposit
- Billing: complex individual tier $2,600 + 3520 ($450). Extension-period time is client-driven (documents from trustee and estate).
""")
C.write_review_points(f"""
# Review Points - EVG1024 - 2025 - Form 1040

*Reviewer: R. Patel (blue). Preparer responses in red. Synthetic.*

1. **Schedule 1 line 8c** - First draft included the $38,000 1099-C as income (based on the client's year-end spreadsheet).
   - Wrong date and wrong asset list. Rebuild the balance sheet immediately before 03/18/2025, include the 401(k), exclude the
     inherited IRA (July). Get her March balances.
   - *Preparer: Handwritten list + statements received 03/09. Insolvent {fmt(INSOLVENCY)}; Form 982 excludes all {fmt(COD)}.*
2. **Form 982 Part II** - Draft excluded the COD but left the capital loss carryover at {fmt(co_before['total'])}.
   - Excluded COD must reduce attributes - capital loss carryover here. Document the 2026 override.
   - *Preparer: Line 9 = {fmt(EXCLUDED)}; 2026 carryover {fmt(co_after_lt)}; statement attached and 2026 diary note set.*
3. **Brightline stock** - Draft showed a $150,000 LT capital loss on 8949 only.
   - Check 1244 - SPA and board resolution are in PERM. Single limit $50,000 to Form 4797 Part II.
   - *Preparer: Split done - {fmt(-S1244_LOSS)} ordinary / {fmt(-WORTHLESS_CAP_LOSS)} capital; sold date 12/31/2025.*
4. **Foreign trust** - Draft (prepared before the FNTBS arrived) had the $120,000 as Schedule 1 "other income".
   - Wait for the beneficiary statement - actual method gives character; corpus is not income. Confirm UNI = 0 (no throwback).
   - *Preparer: FNTBS received 06/19. Interest / qualified dividends / LTCG / corpus split; UNI $0; U.S. agent appointed.*
5. **Form 3520 / 8938 / Sch B line 8** - Need 3520 Part III (separate mailing), Schedule B line 8 = Yes, and test Form 8938.
   - *Preparer: 3520 prepared and mailed 09/21; Sch B updated; 8938 filed with Part IV excepted asset (value = distributions $120,000).*
6. **Schedule A** - 691(c) missing in draft. Use the attorney's letter (federal tax only - not CT). Do not use the old workbook formula.
   - *Preparer: {fmt(D691C)} on line 16; tab 18 overridden per Corrections Log.*
7. **Form 8960** - Draft showed $0 NIIT (1244 loss netted against investment income). Take the conservative position and flag it.
   - *Preparer: NIIT {fmt(v['niit'])}; alternative {fmt(niit_alt)} noted for S. Kennedy.*
8. FYI - Inherited IRA: confirm Dad's 2025 RMD was taken (otherwise beneficiaries must take it by 12/31/2025).
   - *Preparer: Fidelity letter in PBC - taken 02/14/2025.*
""")
print("EVG1024 done", R.summary()["24"], "refund", v["refund"], "due", v["balance_due"], "AGI", v["11"], "TI", v["15"],
      "niit", v["niit"], "co", co_before, "->", co_after_lt)
