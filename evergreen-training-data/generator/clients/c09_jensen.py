"""EVG1009 - Harold Jensen and Eleanor Jensen (deceased 08/09/2025) (MFJ - year of death, Washington - Spokane).
Filing status in the year of death (MFJ, not QSS - the procedure's 'qualifying widower' wording is wrong for 2025);
community-property full basis step-up (sec. 1014(b)(6)) for the brokerage account (1099-B shows original/unadjusted
basis) and the marital home; home sale with 1099-S excluded under sec. 121 ($500k); decedent's final medical bills on
Schedule A; SSA-1099 benefit repaid (box 4); spousal IRA transfer (not a distribution); funeral costs not deductible;
senior deduction x2; WA capital gains excise not triggered; Form 706 portability flag."""
from common import ClientBuild, gotcha, fmt
from docs import statement, scanned_pages, write_text
import forms as F
from tax2025 import Return1040, r, taxable_ss

C = ClientBuild("EVG1009", "Jensen", "Harold Jensen & Eleanor Jensen (deceased)")
OLD_ADDR = ("3415 S Manito Blvd", "Spokane, WA 99203")
ADDR = ("1020 W Riverside Ave Apt 604", "Spokane, WA 99201")
T = {"name": "Harold L. Jensen", "ssn": "XXX-XX-6620", "dob": "1953-02-11"}
S = {"name": "Eleanor M. Jensen", "ssn": "XXX-XX-4318", "dob": "1955-06-23", "dod": "2025-08-09"}
REC_T = [T["name"], *ADDR, f"TIN: {T['ssn']}"]
REC_J = ["Harold L. Jensen", "Eleanor M. Jensen (deceased)", *ADDR, f"TIN: {T['ssn']}"]

# ================================================================== facts
SS_H_GROSS, SS_H_PARTB = 2600.00 * 12, 185.00 * 12
SS_E_GROSS, SS_E_REPAID, SS_E_PARTB = 1845.00 * 9, 1845.00, 185.00 * 8   # Aug benefit (paid Sep) returned - not entitled for month of death
SS_H_NET, SS_E_NET = SS_H_GROSS, SS_E_GROSS - SS_E_REPAID
PENSION, PENSION_WH = 28800.00, 2400.00
IRA_H, IRA_H_WH = 10000.00, 1000.00
ELEANOR_IRA_DOD, ELEANOR_IRA_XFER = 412340.18, 418902.66
INT_SCHWAB, DIV_ORD, DIV_QUAL = 1215.40, 6840.22, 5960.10
# brokerage sales (all inherited community property -> DOD FMV basis for BOTH halves; holding period LT under sec. 1223(9))
DOD_NOTE = "DOD 08/09/2025 (Sat) - mean of high/low averaged 08/08 & 08/11"
SALES = [  # id, desc, shares, sold, proceeds, reported basis (None = noncovered/not reported), original cost, DOD FMV
    ("1", "Vanguard 500 Index Admiral (VFIAX)", 400, "11/14/2025", 230000.00, None, 48200.00, 222048.00),
    ("2", "Microsoft Corp (MSFT)", 300, "10/06/2025", 153000.00, 13500.00, 13500.00, 156105.00),
    ("3", "Johnson & Johnson (JNJ)", 200, "10/06/2025", 37620.00, None, 11800.00, 31080.00),
]
trades = []
for sid, desc, sh, sold, proc, rep, orig, fmv in SALES:
    if rep is not None:   # covered - broker reported ORIGINAL basis to IRS (not updated) -> box D, code B adjustment
        trades.append({"box": "D", "id": sid, "desc": f"{sh} sh {desc} - INHERITED (community property)", "acq": "INHERITED", "sold": sold,
                       "proceeds": proc, "basis": rep, "adj": -(fmv - rep), "code": "B"})
    else:                 # noncovered - basis not reported -> box E, enter DOD FMV basis
        trades.append({"box": "E", "id": sid, "desc": f"{sh} sh {desc} - INHERITED (community property)", "acq": "INHERITED", "sold": sold,
                       "proceeds": proc, "basis": fmv})
STOCK_GAIN = sum(p - f for _, _, _, _, p, _, _, f in SALES)
NAIVE_GAIN = sum(p - o for _, _, _, _, p, _, o, _ in SALES)
HALF_STEP_GAIN = sum(p - (f + o) / 2 for _, _, _, _, p, _, o, f in SALES)
# home sale
HOME_PRICE = 685000.00
COMMISSION = round(HOME_PRICE * .055, 2)
REET = round(525000 * .011 + (HOME_PRICE - 525000) * .0128 + HOME_PRICE * .005, 2)   # WA state graduated REET + Spokane local 0.5%
TITLE_ESCROW = 2850.00
SELL_COSTS = COMMISSION + REET + TITLE_ESCROW
AMT_REALIZED = HOME_PRICE - SELL_COSTS
HOME_DOD_FMV = 615000.00
HOME_ORIG = 210000.00 + 85000.00          # 1998 purchase + improvements (irrelevant after step-up)
HOME_GAIN = r(AMT_REALIZED - HOME_DOD_FMV)
HOME_GAIN_NAIVE = r(AMT_REALIZED - HOME_ORIG)
trades.append({"box": "F", "id": "4", "desc": f"Principal residence {OLD_ADDR[0]}, Spokane WA (Form 1099-S) - sec. 121 exclusion",
               "acq": "INHERITED/1998", "sold": "12/12/2025", "proceeds": HOME_PRICE, "basis": HOME_DOD_FMV + r(SELL_COSTS),
               "adj": -HOME_GAIN, "code": "H"})   # col (d) = 1099-S gross; col (e) = DOD basis + selling expenses
# property tax 2025 on home (both halves paid by Harold); seller's share through 12/11/2025
PROP_TAX_2025 = 6820.00
PROP_TAX_DED = r(PROP_TAX_2025 * 345 / 365)
BUYER_CREDIT = round(PROP_TAX_2025 - PROP_TAX_2025 * 345 / 365, 2)
SALES_TAX_TABLE = 1480.00
# medical (paid by Harold in 2025 from joint account)
MED_ELEANOR = [("Providence Sacred Heart Medical Center - inpatient stay 05/2025, patient balance (MA plan max OOP + out-of-network)", 6850.00),
               ("Hospice House of Spokane - residential room & board 06/08-08/09/2025 (62 days x $300; not covered by Medicare hospice)", 18600.00),
               ("Evergreen Home Care Agency - certified nursing aide, chronically ill, plan of care by physician (sec. 7702B(c))", 12400.00)]
MED_PREMIUMS = [("Medicare Part B - Harold (SSA-1099 description)", SS_H_PARTB), ("Medicare Part B - Eleanor (SSA-1099 description)", SS_E_PARTB),
                ("Medigap Plan G + Part D - Harold (12 mo)", 3180.00), ("Medigap Plan G + Part D - Eleanor (Jan-Aug)", 2120.00)]
MED_OTHER = [("Harold - dental, prescriptions, hearing aid batteries, copays", 1860.00)]
MED_TOTAL = sum(a for _, a in MED_ELEANOR + MED_PREMIUMS + MED_OTHER)
FUNERAL = 14500.00
CHARITY = 2400.00 + 1000.00

# ================================================================== PERM
C.write_profile(f"""
# EVG1009 - Jensen, Harold (and Eleanor, deceased)  (PERM)

*Synthetic client - Project Evergreen training data.*

| Item | Detail |
|---|---|
| Client ID | EVG1009 |
| Taxpayer | Harold L. Jensen, DOB 02/11/1953, SSN XXX-XX-6620 - retired civil engineer (Spokane County; WA DRS PERS Plan 2 retiree) |
| Spouse | Eleanor M. Jensen, DOB 06/23/1955, SSN XXX-XX-4318 - retired teacher's librarian - **died 08/09/2025** (death certificate copy in PERM, received 09/2025) |
| Marriage | Married 1979. Washington residents since 1984 - **community property state**. Community Property Agreement (RCW 26.16.120) signed 2004 - all property community; vests in survivor at first death (copy in PERM). |
| Address | Through 12/12/2025: {OLD_ADDR[0]}, {OLD_ADDR[1]} (owned since 1998). **New address from 12/2025: {ADDR[0]}, {ADDR[1]}** (rental, senior community). Update static info. |
| Dependents | None. Adult son Mark Jensen (Portland OR) helps Harold with paperwork - authorized contact (Form 8821 not on file; Harold OK'd email cc). |
| Estate | No probate (community property agreement). Estate attorney: Linda Ferris, Ferris & Oakes PLLC. |
| Contact | Harold - (509) 555-0141 (prefers phone); Mark - mark.jensen@example.com (cc). Paper copy mailed to Harold; eSign by Harold. |
| Engagement | Client since 2016. Retiree tier ($950); 2025 quote $1,600 (year of death, home sale, inherited securities). |
""")
F.prior_year_summary(C.perm_file("2024_Form_1040_Return_Summary.pdf", "Prior-year return summary"), "Harold & Eleanor Jensen",
    "EVG1009", "Married filing jointly", [
        ["2b / 3b", "Interest / ordinary dividends (Schwab)", 7380],
        ["5b", "WA DRS pension - Harold", 28400],
        ["6a / 6b", "Social security (Harold 30,000; Eleanor 21,600) / taxable", 51600],
        ["", "   taxable social security", 29910],
        ["11", "AGI", 65690], ["12", "Standard deduction (MFJ 29,200 + 2 x 1,550)", 32300],
        ["15", "Taxable income", 33390], ["24", "Total tax", 2014], ["25", "Withholding (pension)", 2400], ["35a", "Refund", 386]],
    carryovers=[["None", 0]],
    notes="PY WP: Joint Schwab account held as community property with right of survivorship. Eleanor's traditional IRA at Vanguard "
          "(no RMDs yet - born 1955, RMD age 73 -> 2028 first year). Harold born 1953 -> first RMD year 2026 (age 73).")
statement(C.perm_file("Community_Property_Agreement_2004.pdf", "Legal agreement (community property)"),
    "COMMUNITY PROPERTY AGREEMENT (RCW 26.16.120)", [
        {"para": ["THIS AGREEMENT is made on March 4, 2004 at Spokane, Washington, between HAROLD L. JENSEN and ELEANOR M. JENSEN, "
                  "husband and wife, residents of Spokane County, Washington.",
                  "1. All property now owned by either or both of us, and all property hereafter acquired by either or both of us, "
                  "wherever situated and however titled, is and shall be our community property.",
                  "2. Upon the death of either of us, all community property shall vest immediately in the survivor, without probate.",
                  "3. This agreement does not apply to property that federal law requires to pass by beneficiary designation "
                  "(retirement accounts), which shall pass according to such designation.",
                  "Signed: /s/ Harold L. Jensen   /s/ Eleanor M. Jensen   Notarized: J. Whitcomb, Notary Public, State of Washington."]}])
statement(C.perm_file("Death_Certificate_Eleanor_Jensen_(summary).pdf", "Death certificate (copy - summary page)"),
    "Washington State Department of Health - Certificate of Death (copy - summary)", [
        {"table": [["Decedent", "Eleanor Marie Jensen"], ["Date of death", "08/09/2025"], ["Place", "Hospice House of Spokane, Spokane WA"],
                   ["Marital status", "Married - spouse Harold L. Jensen"], ["Residence", f"{OLD_ADDR[0]}, {OLD_ADDR[1]}"]],
         "left_align_cols": [0, 1]}])

# ================================================================== PBC
F.organizer(C.pbc_file("01_2025_Organizer_completed.pdf", "Client organizer", "2026-02-27", "Mailed (paper)"),
    "Harold & Eleanor Jensen", "EVG1009",
    general=[("Did your marital status change during 2025?", "Yes", "Eleanor passed away August 9. I guess I am a widower now - file as widower?"),
             ("Did you sell your home or other real estate?", "Yes", "Sold Manito house 12/12/25 - moved to apartment"),
             ("Did you sell stocks or other investments?", "Yes", "Sold some of the Schwab account for the medical bills + move"),
             ("Did you receive an inheritance?", "Yes", "Eleanor's IRA moved to my IRA at Vanguard; Schwab account now in my name"),
             ("Did you have large medical expenses?", "Yes", "Eleanor's hospital + hospice + home aide - list attached"),
             ("Did you make estimated tax payments?", "No", ""),
             ("Did you receive, sell, exchange digital assets?", "No", "")],
    dependents=[],
    income_rows=[["Pension", "WA Dept of Retirement Systems", 28400, "see 1099-R"],
                 ["IRA distribution", "Vanguard (Harold)", 0, "10,000 in Dec"],
                 ["Social security", "Harold", 30000, "31,200"],
                 ["Social security", "Eleanor", 21600, "see form"],
                 ["Interest / dividends", "Schwab", 7380, "see 1099"],
                 ["Home sale", OLD_ADDR[0], "", "685,000 (1099-S) - bought 1998 for 210,000"]],
    deductions_rows=[["Medical", "Eleanor's bills (list attached)", "", "about 38,000"],
                     ["Medical insurance", "Medigap/Part D", 5300, "5,300"],
                     ["Funeral", "Hennessey-Smith Funeral Home", "", "14,500"],
                     ["Property tax", "Spokane County (Manito house)", 6480, "6,820"],
                     ["Charitable", "Manito Lutheran; Hospice memorial gift", 2400, "3,400"]],
    signature_date="02/22/2026")
F.ssa_1099(C.pbc_file("02_SSA-1099_Harold_Jensen.pdf", "Form SSA-1099", "2026-02-27", "Mailed (paper)"),
           [T["name"], T["ssn"]], {"3": SS_H_GROSS, "4": 0, "5": SS_H_NET, "7": f"{OLD_ADDR[0]}, {OLD_ADDR[1]}",
           "desc": [f"Description of amount in box 3: Paid by direct deposit {SS_H_GROSS - SS_H_PARTB:,.2f}; Medicare Part B premiums "
                    f"deducted from your benefits {SS_H_PARTB:,.2f}. Total additions {SS_H_GROSS:,.2f}."]})
F.ssa_1099(C.pbc_file("03_SSA-1099_Eleanor_Jensen.pdf", "Form SSA-1099", "2026-02-27", "Mailed (paper)"),
           [S["name"], S["ssn"]], {"3": SS_E_GROSS, "4": SS_E_REPAID, "5": SS_E_NET, "7": f"{OLD_ADDR[0]}, {OLD_ADDR[1]}",
           "desc": [f"Description of amount in box 3: Paid by direct deposit {SS_E_GROSS - SS_E_PARTB:,.2f}; Medicare Part B premiums "
                    f"deducted {SS_E_PARTB:,.2f}. Description of amount in box 4: Benefits for August 2025 paid 09/10/2025 returned "
                    f"by bank 10/2025 {SS_E_REPAID:,.2f} (beneficiary deceased 08/09/2025 - not due for month of death)."]})
F.f1099_r(C.pbc_file("04_1099-R_WA_DRS_Pension.pdf", "Form 1099-R", "2026-02-27", "Mailed (paper)"),
          ["Washington State Department of Retirement Systems", "PO Box 48380", "Olympia, WA 98504", "TIN: 00-6001234"], REC_T,
          {"1": PENSION, "2a": PENSION, "4": PENSION_WH, "7": "7", "9a": "100%"}, account="PERS2-44120")
F.f1099_r(C.pbc_file("05_1099-R_Vanguard_IRA_Harold.pdf", "Form 1099-R", "2026-02-27", "Mailed (paper)"),
          ["Vanguard Fiduciary Trust Company", "PO Box 2600", "Valley Forge, PA 19482", "TIN: 00-0000071"], REC_T,
          {"1": IRA_H, "2a": IRA_H, "2b": "Taxable amount not determined", "4": IRA_H_WH, "7": "7  IRA/SEP/SIMPLE: X", "13": "12/05/2025"},
          account="IRA ****6620")
statement(C.pbc_file("06_Vanguard_Spousal_Beneficiary_Transfer_Confirmation.pdf", "Custodian letter + statement", "2026-02-27", "Mailed (paper)"),
    "Vanguard - Beneficiary Transfer Confirmation - Account of Eleanor M. Jensen (deceased) Traditional IRA ****2208", [
        {"para": ["Dear Mr. Jensen,",
                  "As sole primary beneficiary and surviving spouse, you elected to treat your late wife's IRA as your own. On 10/20/2025 "
                  f"the assets (${ELEANOR_IRA_XFER:,.2f}) were transferred directly to your Vanguard Traditional IRA ****6620.",
                  "Because this was a direct trustee-to-trustee transfer to a spousal beneficiary, it is not a distribution and no Form "
                  "1099-R will be issued. The transferred amount will not appear in box 2 of Form 5498 for your IRA.",
                  "Future required minimum distributions will be based on your own age (your first RMD year is 2026)."]},
        {"table": [["Eleanor's IRA ****2208", "Amount"], ["Value 08/09/2025 (date of death)", ELEANOR_IRA_DOD],
                   ["Transfer to spouse IRA ****6620 on 10/20/2025", ELEANOR_IRA_XFER], ["Balance 12/31/2025", 0.00]], "left_align_cols": [0]}])
statement(C.pbc_file("07_Vanguard_IRA_Harold_Year-End_Statement.pdf", "IRA statement", "2026-02-27", "Mailed (paper)"),
    "Vanguard - Traditional IRA ****6620 (Harold L. Jensen) - 2025 Year-End Summary", [
        {"table": [["Item", "Amount"], ["Beginning value 01/01/2025", 356210.40], ["Spousal beneficiary transfer in 10/20/2025", ELEANOR_IRA_XFER],
                   ["Withdrawal 12/05/2025 (10% federal withholding)", -IRA_H], ["Dividends & capital gains reinvested", 24880.16],
                   ["Market change", 31004.72], ["Ending value 12/31/2025 (Form 5498 box 5)", 820997.94]], "left_align_cols": [0]}])
# Schwab consolidated 1099 (unadjusted basis)
b_rows = [["Box 1a Description", "Shares", "1b Acquired", "1c Sold", "1d Proceeds", "1e Cost basis", "Gain/loss", "Box 2 term", "Box 12 basis reported"]]
for sid, desc, sh, sold, proc, rep, orig, fmv in SALES:
    b_rows.append([desc, sh, "VARIOUS" if rep is None else "03/12/2015", sold, proc, rep if rep is not None else "(not reported)",
                   (proc - rep) if rep is not None else "", "Long-term", "Yes" if rep is not None else "No - noncovered"])
statement(C.pbc_file("08_Schwab_2025_Consolidated_1099_Jensen.pdf", "Consolidated Form 1099 (brokerage)", "2026-02-27", "Mailed (paper)"),
    "Charles Schwab & Co., Inc. - 2025 Form 1099 Composite & Year-End Summary - Account ****5519", [
        {"para": "Account title: HAROLD L. JENSEN (formerly Harold L. & Eleanor M. Jensen, Community Property with Right of Survivorship - "
                 "retitled 09/15/2025). Recipient TIN XXX-XX-6620."},
        {"heading": "Form 1099-DIV", "table": [["Box", "Amount"], ["1a Total ordinary dividends", DIV_ORD], ["1b Qualified dividends", DIV_QUAL],
                                               ["2a Capital gain distributions", 0.00]]},
        {"heading": "Form 1099-INT", "table": [["Box", "Amount"], ["1 Interest income (Schwab bank sweep)", INT_SCHWAB]]},
        {"heading": "Form 1099-B - Long-term transactions", "table": b_rows, "left_align_cols": [0]},
        {"note": ["Cost basis shown is the original purchase cost from our records. Schwab has NOT adjusted cost basis for the 08/2025 "
                  "account retitling. If these securities were inherited, the basis may be different - consult your tax advisor. "
                  "Noncovered lots: VFIAX original cost $48,200; JNJ original cost $11,800 (not reported to the IRS)."]}])
statement(C.pbc_file("09_Schwab_Date_of_Death_Valuation_Report.pdf", "Date-of-death valuation", "2026-03-06", "Email from son (Mark)",
                     "received after open-item request"),
    "Charles Schwab - Date of Death Valuation Report - Decedent: Eleanor M. Jensen - Account ****5519", [
        {"para": f"Valuation date: 08/09/2025. {DOD_NOTE} (Treas. Reg. 20.2031-2(b)). Account held as community property - "
                 "report shows 100% of each position."},
        {"table": [["Security", "Shares", "Value per share", "Total DOD value", "Decedent 1/2", "Survivor 1/2"]] +
                  [[d, sh, round(f / sh, 4), f, f / 2, f / 2] for _, d, sh, _, _, _, _, f in SALES] +
                  [["Schwab bank sweep (cash)", "", "", 81220.18, 40610.09, 40610.09]], "left_align_cols": [0]}])
F.f1099_s(C.pbc_file("10_1099-S_Manito_Blvd_Sale.pdf", "Form 1099-S", "2026-02-27", "Mailed (paper)"),
          ["Inland Northwest Title & Escrow", "601 W 1st Ave Ste 1400", "Spokane, WA 99201", "TIN: 00-9120447"],
          [T["name"], *ADDR, f"TIN: {T['ssn']}"],
          {"1": "12/12/2025", "2": HOME_PRICE, "3": f"{OLD_ADDR[0]}, Spokane WA 99203 (parcel 35294.1102)", "6": ""})
statement(C.pbc_file("11_Seller_Final_Settlement_Statement.pdf", "Closing statement (seller)", "2026-02-27", "Mailed (paper)"),
    "Inland Northwest Title & Escrow - Seller's Final Settlement Statement - Escrow 25-11874", [
        {"table": [["Item", "Debit (seller)", "Credit (seller)"], ["Contract sales price", "", HOME_PRICE],
                   ["Real estate commission 5.5% (Windermere / Coldwell)", COMMISSION, ""],
                   ["WA real estate excise tax (state graduated + local 0.5%)", REET, ""],
                   ["Owner's title policy, escrow fee, recording", TITLE_ESCROW, ""],
                   ["County taxes 01/01/25-12/11/25 (seller paid full year; buyer credit)", "", BUYER_CREDIT],
                   ["Payoff of existing loans", 0.00, ""], ["Net proceeds to seller (wired 12/12/2025)", "", round(HOME_PRICE - SELL_COSTS + BUYER_CREDIT, 2)]],
         "left_align_cols": [0]}])
statement(C.pbc_file("12_Retrospective_Appraisal_Summary_08-09-2025.pdf", "Appraisal (summary letter)", "2026-03-06", "Email from son (Mark)",
                     "received after open-item request"),
    "Spokane Valuation Group - Retrospective Appraisal - Summary Letter", [
        {"para": [f"Subject: {OLD_ADDR[0]}, Spokane, WA 99203 - single-family residence, 2,640 sf, built 1928.",
                  "Client: Estate of Eleanor M. Jensen / Harold L. Jensen. Purpose: establish fair market value as of the date of death "
                  "for basis (IRC sec. 1014).",
                  f"Effective date of value: 08/09/2025.   Opinion of market value: ${HOME_DOD_FMV:,.0f}.",
                  "Approach: sales comparison (5 comparable sales 03/2025-09/2025). Report date 10/28/2025. Appraiser: R. Delacroix, "
                  "WA Certified Residential Appraiser 1102441."]}])
scanned_pages(C.pbc_file("13_Medical_bills_list_Harold_handwritten.pdf", "Handwritten list (scan) + bills", "2026-02-27", "Mailed (paper)"),
    [["Medical 2025 - what I paid (H.J.)",
      "",
      "Sacred Heart hospital (Ellie, May)       6,850",
      "Hospice House - room + board 62 days    18,600",
      "  (June 8 - Aug 9, Medicare paid hospice care",
      "   but not the room)",
      "Evergreen Home Care - aide for Ellie   12,400",
      "  (Mar-June, Dr. Patel care plan)",
      "                                   --------",
      "                                    37,850",
      "",
      "Medigap + Part D  me 3,180  Ellie 2,120",
      "My dentist / drugs / etc about 1,860",
      "Funeral - Hennessey-Smith 14,500 (can I take this?)",
      "all paid from our checking at Numerica CU"]], handwritten=True, seed=91)
statement(C.pbc_file("14_Hennessey-Smith_Funeral_Home_Invoice.pdf", "Invoice", "2026-02-27", "Mailed (paper)"),
    "Hennessey-Smith Funeral Home - Statement of Funeral Goods and Services Selected", [
        {"table": [["Item", "Amount"], ["Professional services / facilities", 5200.00], ["Casket", 4800.00], ["Cemetery (Greenwood) - plot & opening", 3600.00],
                   ["Obituary, certificates, flowers", 900.00], ["TOTAL - paid 08/20/2025 by Harold L. Jensen", FUNERAL]], "left_align_cols": [0]}])
statement(C.pbc_file("15_Spokane_County_2025_Property_Tax_Receipts.pdf", "Property tax receipts", "2026-02-27", "Mailed (paper)"),
    "Spokane County Treasurer - 2025 Property Tax Receipts - Parcel 35294.1102", [
        {"table": [["Paid", "Half", "Amount"], ["04/28/2025", "1st half 2025", PROP_TAX_2025 / 2], ["10/30/2025", "2nd half 2025", PROP_TAX_2025 / 2],
                   ["Total", "", PROP_TAX_2025]], "left_align_cols": [0, 1], "total_row": True}])
write_text(C.pbc_file("16_Email_Mark_Jensen_2026-03-06.txt", "Client correspondence (authorized family member)", "2026-03-06", "Email"),
"""From: Mark Jensen <mark.jensen@example.com>
To: preparer@evergreentax.example
Cc: (Harold - by phone)
Date: Fri, 6 Mar 2026 16:22:09 -0800
Subject: Jensen taxes - docs you asked for

Hi - attached are the Schwab date-of-death valuation and the appraisal the estate lawyer ordered on the house.
Dad asked me to pass along two questions:
 1) He read online that he should file as a "qualifying widower" this year - is that right? He wants to do whatever
    gives the lower tax. He has not remarried (!) and I'm not a dependent.
 2) Mom's last Social Security check in September was taken back by SSA. Is that a problem?
Also - Ms. Ferris (estate attorney) said something about a "portability" election for Mom's estate tax exemption and
asked whether you handle that. The estate is not large, everything went to Dad.
Thanks, Mark
""")
statement(C.pbc_file("17_Premera_Medigap_PartD_2025_Premium_Statements.pdf", "Insurance premium statements", "2026-02-27", "Mailed (paper)"),
    "Premera Blue Cross Medicare Supplement Plan G / SilverScript Part D - 2025 Premiums Paid", [
        {"table": [["Insured", "Coverage", "Months", "Premiums paid"], ["Harold L. Jensen", "Plan G + Part D", "Jan-Dec", 3180.00],
                   ["Eleanor M. Jensen", "Plan G + Part D", "Jan-Aug (terminated at death)", 2120.00]], "left_align_cols": [0, 1, 2]}])

# ================================================================== RETURN
itemized = {"medical": MED_TOTAL, "state_income_tax": SALES_TAX_TABLE, "use_sales_tax": True, "real_estate_tax": PROP_TAX_DED,
            "charity_cash": CHARITY}
facts = {
    "status": "MFJ", "taxpayer": {"age65": True}, "spouse": {"age65": True},
    "ssa": [{"who": "T", "net_benefits": SS_H_NET}, {"who": "S", "net_benefits": SS_E_NET}],
    "pension": [{"payer": "WA DRS (PERS 2)", "gross": PENSION, "taxable": PENSION}],
    "ira": [{"payer": "Vanguard IRA (Harold)", "gross": IRA_H, "taxable": IRA_H}],
    "interest": [{"payer": "Charles Schwab & Co.", "amount": INT_SCHWAB}],
    "dividends": [{"payer": "Charles Schwab & Co.", "ordinary": DIV_ORD, "qualified": DIV_QUAL}],
    "trades": trades,
    "itemized": itemized,
    "sch1a": {"seniors": 2},
    "withholding_1099": PENSION_WH + IRA_H_WH,
}
R = Return1040(facts).compute()
v = R.values
assert v["deduction_type"].startswith("Itemized")
STD_AVAIL = v["standard_deduction_available"]
other_inc = v["1z"] + v["2b"] + v["3b"] + v["4b"] + v["5b"] + v["7"] + v["8"]
ss_tot = v["6a"]

# SS worksheet detail
l2 = ss_tot / 2
l3 = other_inc
l5 = l2 + l3
l9 = l5 - 32000
l11 = max(0, l9 - 12000)
ssw = [["Social Security Benefits Worksheet (MFJ)", "Amount"],
       ["1 Net benefits (Harold 31,200 + Eleanor 16,605 paid - 1,845 repaid = 14,760)", r(ss_tot)],
       ["2 One-half of line 1", r(l2)], ["3 Other income (lines 1z, 2b, 3b, 4b, 5b, 7, 8)", r(l3)],
       ["4-5 Tax-exempt interest 0; adjustments 0 -> combined income", r(l5)], ["6 Base amount MFJ", 32000],
       ["9 Excess over base", r(l9)], ["11 Excess over 44,000", r(l11)],
       ["16 Taxable (lesser of 85% of benefits or worksheet)", v["6b"]]]
basis_tbl = [["Inherited securities - basis (sec. 1014(b)(6) community property: BOTH halves to DOD FMV)", "Original cost", "1099-B basis", "DOD FMV (correct basis)", "Proceeds", "Gain"]]
for sid, desc, sh, sold, proc, rep, orig, fmv in SALES:
    basis_tbl.append([f"{sh} sh {desc} sold {sold}", orig, rep if rep is not None else "not reported", fmv, proc, r(proc - fmv)])
basis_tbl += [["Total", sum(x[6] for x in SALES), "", sum(x[7] for x in SALES), sum(x[4] for x in SALES), r(STOCK_GAIN)],
              [f"Wrong: original cost -> gain {NAIVE_GAIN:,.0f}; half step-up only (common-law rule) -> gain {HALF_STEP_GAIN:,.0f}", "", "", "", "", ""]]
home_tbl = [["Sale of home - " + OLD_ADDR[0] + " (Form 1099-S) - Form 8949 Part II box F, code H", "Amount"],
            ["Gross sales price (1099-S box 2)", r(HOME_PRICE)],
            ["Less selling expenses: commission " + f"{COMMISSION:,.0f}" + ", WA REET " + f"{REET:,.0f}" + ", title/escrow " + f"{TITLE_ESCROW:,.0f}", -r(SELL_COSTS)],
            ["Amount realized", r(AMT_REALIZED)],
            ["Basis: 100% stepped up to DOD FMV (community property - appraisal 08/09/2025); original cost + improvements $295,000 irrelevant", r(HOME_DOD_FMV)],
            ["Gain", HOME_GAIN],
            ["Form 8949: column (d) gross proceeds 685,000 (ties to 1099-S); column (e) basis 615,000 + selling expenses " + f"{r(SELL_COSTS):,}" + "; column (g) code H", ""],
            ["Sec. 121 exclusion (owned & used 2 of 5 years; MFJ in year of death -> $500,000; also available to an unmarried surviving "
             "spouse for sales within 2 years of death, sec. 121(b)(4))", -HOME_GAIN],
            ["Taxable gain", 0],
            [f"Without step-up and with a $250,000 single exclusion (two errors): {HOME_GAIN_NAIVE:,} - 250,000 = {HOME_GAIN_NAIVE - 250000:,} taxable", ""]]
med_tbl = [["Schedule A line 1 - medical and dental (paid in 2025 by Harold; decedent's expenses paid for his spouse)", "Amount"]] + \
          [[d, a] for d, a in MED_ELEANOR + MED_PREMIUMS + MED_OTHER] + \
          [["Total medical (line 1)", r(MED_TOTAL)], ["Less 7.5% of AGI", -r(v['11'] * .075)],
           ["Deductible medical (line 4)", max(0, r(MED_TOTAL) - r(v['11'] * .075))],
           ["Funeral / burial $14,500 - NOT deductible on Form 1040 (Form 706 only)", 0]]
cmp_tbl = [["Deduction comparison", "Amount"],
           ["Standard: MFJ 31,500 + 2 x 1,600 (both 65+; a spouse who dies is 65+ if 65 on the date of death)", STD_AVAIL],
           ["Itemized: medical over floor + taxes (property tax through 12/11/2025 " + f"{PROP_TAX_DED:,}" + " + WA sales tax table " + f"{SALES_TAX_TABLE:,.0f}" + ") + charity", v["12e"]],
           ["Result", "Itemize"],
           ["Schedule 1-A senior deduction (both spouses 65+; MAGI " + f"{v['11']:,}" + " < $150,000) - allowed whether or not itemizing", v["13b"]]]
fs_note = ("<b>Filing status.</b> Eleanor died 08/09/2025. A surviving spouse may file a joint return for the year of death if he has "
           "not remarried by year end (sec. 6013(a)(2)); MFJ is the correct status for 2025 - not qualifying surviving spouse (QSS "
           "requires a dependent child and applies only to the two years AFTER the year of death). Harold has no dependent, so from 2026 he "
           "files Single. Return is signed 'Harold L. Jensen' and 'Filing as surviving spouse' in Eleanor's signature space; 'DECEASED "
           "Eleanor M. Jensen 08/09/2025' is shown next to her name. No executor/administrator appointed; Form 1310 is not required "
           "for a surviving spouse filing a joint return.")
wa_tbl = [["Washington capital gains excise tax check (RCW 82.87)", "Amount"],
          ["Long-term capital gains from stocks (real estate is exempt from the WA excise)", r(STOCK_GAIN)],
          ["2025 standard deduction (indexed)", 278000],
          ["WA excise tax due", 0],
          [f"If basis were NOT stepped up: LTCG {NAIVE_GAIN:,.0f} - 278,000 = {NAIVE_GAIN - 278000:,.0f} x 7% -> WA return required", ""]]
C.write_return(R, [
    ("Taxpayer / Spouse", "Harold L. Jensen (XXX-XX-6620) / Eleanor M. Jensen (XXX-XX-4318) - DECEASED 08/09/2025"),
    ("Address", ", ".join(ADDR) + " (new address - home sold 12/12/2025)"),
    ("Filing status", "Married filing jointly (year of spouse's death) - 'Filing as surviving spouse'"),
    ("Dependents", "None"),
    ("Digital assets question", "No"),
    ("Forms included", "1040, Sch 1-A (seniors), Sch A, Sch B, Sch D, Form 8949 (boxes D, E, F)"),
    ("State", "None - Washington has no income tax; WA capital gains excise not triggered"),
    ("Filing method", "E-file 04/09/2026 (Form 8879 signed by Harold as surviving spouse 04/07/2026); refund direct deposit Numerica CU ****0415 (joint/Harold)"),
], attachments=[("Filing status - year of death", fs_note), ("Social security benefits worksheet", ssw),
                ("Basis of inherited securities (Form 8949 support)", basis_tbl), ("Sale of main home - sec. 121", home_tbl),
                ("Schedule A - medical detail", med_tbl), ("Standard vs itemized", cmp_tbl), ("Washington capital gains excise", wa_tbl)])

# ---------------- answer key
tax_diff_naive = r((NAIVE_GAIN - STOCK_GAIN) * .15)
gotchas = [
    gotcha("EVG1009-G1", "Review - Filing Status (spouse deceased)", "Client and procedure say 'qualifying widower'",
           "File 2025 as Qualifying Surviving Spouse (procedure wording) or Single.",
           "In the year of death the survivor files MFJ (sec. 6013(a)(2)); QSS needs a dependent child and only applies to the 2 following "
           "years. Harold has no dependent -> 2026 onward Single. Sign as surviving spouse; no Form 1310. Procedure is imprecise - follow the law.",
           "Filing status / std deduction / brackets", ["Filing status", "12e"], "medium"),
    gotcha("EVG1009-G2", "Estate Implications - step-up in basis (community property)", "Schwab 1099-B shows original cost; noncovered lots show no basis",
           f"Use the 1099-B/original cost (gain {fmt(NAIVE_GAIN)}), zero basis on noncovered lots, or step up only Eleanor's half "
           f"(gain {fmt(HALF_STEP_GAIN)}).",
           f"Washington community property: BOTH halves get a date-of-death basis (sec. 1014(b)(6)); holding period long-term. Use the Schwab "
           f"DOD valuation (weekend DOD - mean of adjacent trading days). Box D with code B adjustment for the covered MSFT lot; box E with "
           f"DOD basis for noncovered lots. Gain {fmt(STOCK_GAIN)}.", f"Sch D overstated {fmt(NAIVE_GAIN - STOCK_GAIN)} (~{fmt(tax_diff_naive)}+ tax and a WA excise filing)",
           ["7", "Form 8949", "Sch D"], "hard"),
    gotcha("EVG1009-G3", "Estate Implications - sale of a home received from an estate; Schedule D code H", "1099-S $685,000 on the marital home",
           f"Compute gain from the 1998 cost ({fmt(HOME_GAIN_NAIVE)}) and apply a $250,000 single exclusion -> {fmt(HOME_GAIN_NAIVE - 250000)} taxable; "
           "or omit the sale because it is excluded.",
           f"Full community-property step-up to the $615,000 appraisal -> gain {fmt(HOME_GAIN)}; excluded under sec. 121 ($500,000 - MFJ "
           "in year of death; sec. 121(b)(4) would also give $500k within 2 years of death). A 1099-S was issued, so report on Form 8949 "
           "box F with code H and the exclusion as a negative adjustment.", "Up to ~$99k of gain wrongly taxed", ["Form 8949 box F", "7"], "medium"),
    gotcha("EVG1009-G4", "Schedule A - medical; decedent's expenses; funeral", "Final medical bills and funeral costs",
           "Skip itemizing (standard + 65 add-ons looks 'normal' for retirees), deduct the funeral, or miss the Medicare premiums on the SSA-1099s.",
           f"Medical {fmt(r(MED_TOTAL))} (hospital, residential hospice room & board, licensed home aide under a plan of care, Medicare Part B from "
           f"both SSA-1099s, Medigap/Part D) less 7.5% floor -> itemized {fmt(v['12e'])} > standard {fmt(STD_AVAIL)}. Funeral is never a 1040 deduction.",
           f"Deduction {fmt(v['12e'])} vs {fmt(STD_AVAIL)}", ["12e", "Sch A 1-4"], "medium"),
    gotcha("EVG1009-G5", "Social security - benefits repaid (SSA-1099 box 4)", "Eleanor's August benefit returned",
           f"Enter box 3 gross benefits ({fmt(SS_E_GROSS)}) for Eleanor.",
           f"Use box 5 net benefits ({fmt(SS_E_NET)}) - the repayment is netted in the same year (no sec. 1341 claim needed). Total line 6a {fmt(r(ss_tot))}.",
           "Line 6b overstated ~$1,570", ["6a", "6b"], "easy"),
    gotcha("EVG1009-G6", "Client IRAs / inherited IRA", "Vanguard statement shows a $418,903 'transfer out' of Eleanor's IRA",
           "Report the spousal transfer as an IRA distribution on line 4a/4b.",
           "Direct trustee-to-trustee transfer by the surviving spouse who elected to treat the IRA as his own - not a distribution, no 1099-R, "
           "nothing on line 4. Only Harold's own $10,000 withdrawal is taxable.", "Line 4b overstated $418,903", ["4a", "4b"], "easy"),
    gotcha("EVG1009-G7", "OBBBA - senior deduction (Schedule 1-A Part V)", "Deceased spouse and the new $6,000 senior deduction",
           "Claim only one senior deduction (Harold) because Eleanor died, or skip it because they itemize.",
           f"Both spouses were 65+ and the deduction is allowed whether or not itemizing; MAGI {fmt(v['11'])} < $150,000 -> 2 x $6,000 = {fmt(v['13b'])}.",
           "Line 13b", ["13b"], "easy"),
    gotcha("EVG1009-G8", "Estate Implications / SALT - WA capital gains excise; Form 706 portability", "Items outside the 1040",
           "Ignore; or file a WA capital gains excise return based on unadjusted gains.",
           f"With stepped-up basis, 2025 LTCG {fmt(STOCK_GAIN)} is far below the ~$278,000 WA standard deduction (home sale exempt) - no WA "
           "filing. Flag to signer: a portability-only Form 706 (DSUE election) for Eleanor's estate - due 05/09/2026 (+6 months with Form 4768) "
           "or late under Rev. Proc. 2022-32 until 08/09/2030. Engagement for the 706 is a separate project.", "Compliance / planning", [], "medium"),
]
C.write_answer_key(R, {"residence": "WA (no income tax)", "complexity": "Year of death, inherited property, home sale"}, gotchas,
    state=[{"return": "WA capital gains excise", "required": False, "ltcg": r(STOCK_GAIN)}],
    filings=[{"form": "Form 1040 (MFJ - surviving spouse)", "method": "e-file", "due": "2026-04-15", "filed": "2026-04-09"},
             {"form": "Form 706 (portability only) - estate of Eleanor", "method": "paper", "due": "2026-05-09 or Rev. Proc. 2022-32 by 2030-08-09",
              "filed": "separate engagement - pending client decision"}],
    extra={"basis_step_up": {"stock_gain_correct": r(STOCK_GAIN), "stock_gain_original_cost": r(NAIVE_GAIN), "stock_gain_half_step_up": r(HALF_STEP_GAIN)},
           "home_sale": {"amount_realized": r(AMT_REALIZED), "basis_dod": HOME_DOD_FMV, "gain": HOME_GAIN, "sec121_excluded": HOME_GAIN},
           "filing_status_2026": "Single"})
C.write_receipt_log("EVG1009-1040-2025", "T. Nguyen (staff)", "L. Chen (senior)", "S. Kennedy, CPA", "2026-02-27")

C.write_notes(f"""
# EVG1009 - Jensen, Harold (and Eleanor, deceased) - 2025 Form 1040 - Preparer Notes

*Synthetic client - Project Evergreen. Return status: **signed off, e-filed 04/09/2026, accepted.***

## Return summary
| | |
|---|---|
| Filing status | **Married filing jointly** (Eleanor died 08/09/2025) - signed by Harold as surviving spouse |
| AGI (line 11) | {fmt(v['11'])} |
| Deduction | Itemized {fmt(v['12e'])} (standard would be {fmt(STD_AVAIL)}) + senior deduction {fmt(v['13b'])} |
| Taxable income | {fmt(v['15'])} |
| Total tax | {fmt(v['24'])} |
| Withholding | {fmt(v['25d'])} (pension + IRA) |
| **Refund** | **{fmt(v['refund'])}** |

## What I did and why (plain English)
1. **Filing status - MFJ, not "qualifying widower".** Harold asked (and our procedure says) to treat him as a qualifying widower. That's
   not right for 2025: in the year a spouse dies, the survivor can still file a *joint* return with the deceased spouse if he hasn't
   remarried, which gives the same MFJ brackets and standard deduction. "Qualifying surviving spouse" is a separate status for the two
   years *after* the death and only if you have a dependent child - Harold has none, so from **2026 he files Single** (told Mark; bigger tax
   bite next year - adjust pension withholding). Signature: "Harold L. Jensen" plus "Filing as surviving spouse"; no Form 1310 needed.
2. **Social Security.** Harold {fmt(r(SS_H_NET))}; Eleanor's SSA-1099 shows {fmt(r(SS_E_GROSS))} paid and {fmt(r(SS_E_REPAID))} repaid (her August
   check - SSA doesn't pay for the month of death) -> used box 5 net {fmt(r(SS_E_NET))}. Taxable portion per the worksheet: {fmt(v['6b'])}.
   Medicare Part B from both SSA-1099s went to Schedule A medical.
3. **Eleanor's IRA** was moved directly into Harold's own IRA (spousal "treat as own" transfer) - not a distribution, no 1099-R, nothing
   reported. Harold's own $10,000 December withdrawal is taxable (10% withheld). His first RMD year is 2026 (born 1953, age 73) - and
   the RMD will now include the former inherited balance.
4. **Inherited Schwab account - basis step-up.** Washington is a community property state and they had a community property agreement, so
   **both halves** of every community asset get a new basis equal to the date-of-death value (sec. 1014(b)(6)) - not just Eleanor's half.
   Schwab's 1099-B still shows the original cost for the covered MSFT lot and no basis for the older noncovered lots. From Schwab's
   date-of-death valuation (DOD was a Saturday, so values are the average of Friday and Monday), the correct basis is {fmt(sum(x[7] for x in SALES))};
   gain is only **{fmt(STOCK_GAIN)}**, all long-term (inherited property is automatically long-term). Form 8949 box D with code B for MSFT
   (broker-reported basis wrong) and box E for the noncovered lots. Using the 1099-B numbers would have shown {fmt(NAIVE_GAIN)} of gain.
5. **Home sale.** Sold 12/12/2025 for {fmt(HOME_PRICE)} (1099-S). Selling costs {fmt(SELL_COSTS)} (commission, WA excise tax, title/escrow).
   Basis = the retrospective appraisal as of the date of death, {fmt(HOME_DOD_FMV)} (full step-up again - community property), not the 1998
   cost. Gain {fmt(HOME_GAIN)} is completely excluded under sec. 121 (lived there since 1998; $500,000 exclusion on the joint return).
   Because a 1099-S was issued, the sale is still reported on Form 8949 (box F, code H) with the exclusion as an adjustment - otherwise
   the IRS matching program would flag it.
6. **Medical - itemizing.** Harold paid Eleanor's final bills: hospital $6,850, hospice house room & board $18,600 (Medicare's hospice
   benefit doesn't cover room & board), licensed home aide $12,400 (under Dr. Patel's plan of care for a chronically ill person - qualified
   long-term care services = medical). Plus Medicare Part B, Medigap/Part D and Harold's own costs = {fmt(r(MED_TOTAL))}. After the 7.5%
   floor and with property tax (through the 12/11 sale date, {fmt(PROP_TAX_DED)}), WA sales tax per the IRS table, and charity, itemized
   deductions are {fmt(v['12e'])} vs the {fmt(STD_AVAIL)} standard deduction (incl. two 65+ add-ons). **Funeral costs ($14,500) are not
   deductible on a 1040** (only on an estate tax return) - explained to Mark.
7. **Senior deduction.** Both were 65+; MAGI {fmt(v['11'])} is under $150,000 -> 2 x $6,000 = {fmt(v['13b'])}, on top of itemizing.
8. **Washington.** No income tax. Capital gains excise: only {fmt(STOCK_GAIN)} of stock gains (the house is exempt real estate) vs a
   ~$278,000 standard deduction -> nothing to file.

## Open items / flags for signer
- **Form 706 portability (DSUE).** Everything passed to Harold (no estate tax), but electing portability preserves Eleanor's unused
  federal exemption for Harold's estate. Normal due date 05/09/2026 (6-month extension via Form 4768 if filed by then); otherwise
  Rev. Proc. 2022-32 allows a portability-only 706 up to 5 years after death (by 08/09/2030). Recommend a separate engagement (MISC/estate
  project code) - coordinate with Ms. Ferris. WA estate tax: estate is below the WA filing threshold - attorney to confirm.
- Update static info (new address; Eleanor deceased; 2026 status Single). Suggest Harold increase W-4P withholding for 2026.

## Hand-off to signer / routing
- [x] Return locked; Accountant's copy saved as *reviewed*
- [x] Federal 1040 MFJ (surviving spouse) - e-file; no state; no FBAR
- [x] Due 04/15/2026; filed 04/09/2026
- [x] eSign by Harold; paper copy mailed to new address; cc Mark by email (Harold's OK on file)
- Billing: $1,600 quote (year of death, home sale, basis step-up schedule); 706 portability quoted separately.
""")
C.write_review_points(f"""
# Review Points - EVG1009 - 2025 - Form 1040

*Reviewer: L. Chen (blue). Preparer responses in red. Synthetic.*

1. **Filing status** - Draft set to QSS per the organizer/procedure note. Year of death = MFJ (no dependent, so no QSS in 2026-27 either).
   - Update signature block (surviving spouse) and the 2026 status in PERM.
   - *Preparer: Changed to MFJ; PERM updated (2026 Single).*
2. **Form 8949 / WP 8** - Autoflow used Schwab's cost basis ({fmt(NAIVE_GAIN)} gain; noncovered lots at $0 basis).
   - Community property -> full step-up. Use the DOD report (WP 9); code B on the covered lot.
   - *Preparer: Done - gain {fmt(STOCK_GAIN)}; step-up schedule attached.*
3. **Home sale** - Draft omitted the sale ("excluded"). 1099-S was issued - report it with code H. Use the DOD appraisal as basis.
   - *Preparer: Added on 8949 box F; gain {fmt(HOME_GAIN)} fully excluded.*
4. **Line 6a** - Eleanor's gross benefits used; SSA-1099 box 4 shows the repaid August check.
   - *Preparer: Box 5 net used.*
5. **Line 4a/4b** - Draft picked up the $418,903 spousal transfer from the Vanguard statement.
   - *Preparer: Removed - trustee-to-trustee transfer, no 1099-R.*
6. **Sch A** - Funeral home $14,500 included in medical; Medicare Part B from the SSA-1099s missing.
   - *Preparer: Funeral removed; Part B added for both. Still itemizing ({fmt(v['12e'])} vs {fmt(STD_AVAIL)}).*
7. **Sch 1-A** - Senior deduction taken for Harold only.
   - *Preparer: Both spouses were 65+; {fmt(v['13b'])}.*
8. FYI - raise Form 706 portability with the signer; separate project code if the client proceeds.
""")
print("EVG1009 done", dict(R.summary()), v["refund"], "stock", STOCK_GAIN, "home", HOME_GAIN, "itm", v["12e"], STD_AVAIL)
