"""EVG1004 - Robert & Linda Castellano (MFJ, Florida - Sarasota). Retirees: Robert 67 (US-born), Linda 64 (Canadian citizen,
US green card). SSA-1099 with Medicare premiums; pension; Schwab IRA distribution with $8,000 paid to church that the client
calls a "QCD" (Robert is under 70 1/2 -> NOT a QCD; corrected 1099-R issued); Canadian NR-4 employer pension (CAD -> USD at
1.398, FTC Form 1116 general category, carryforward); RBC chequing -> FBAR; consolidated 1099 with munis, Treasuries and
accrued interest paid at purchase; Schwab IRA statement (not reportable); taxable SS; standard vs itemized; senior deduction
for Robert only."""
from common import ClientBuild, gotcha, fmt
from docs import statement, scanned_pages, write_text, write_xlsx, info_form
import forms as F
from tax2025 import Return1040, r, taxable_ss

C = ClientBuild("EVG1004", "Castellano", "Robert & Linda Castellano")
ADDR = ("5127 Bayou Heron Ln", "Sarasota, FL 34231")
T = {"name": "Robert A. Castellano", "ssn": "XXX-XX-2847", "dob": "1958-05-14"}
S = {"name": "Linda M. Castellano", "ssn": "XXX-XX-6135", "dob": "1961-03-22"}
REC_T = [T["name"], *ADDR, f"TIN: {T['ssn']}"]
REC_S = [S["name"], *ADDR, f"TIN: {S['ssn']}"]
REC_J = ["Robert A. & Linda M. Castellano JT TEN", *ADDR, f"TIN: {T['ssn']}"]
CAD_AVG = 1.398          # IRS yearly average currency exchange rate 2025 (design spec)
CAD_FBAR = 1.371         # ASSUMED Treasury Reporting Rate of Exchange 12/31/2025 (Canada-Dollar) - verify

# ------------------------------------------------------------------ PERM
C.write_profile(f"""
# EVG1004 - Castellano, Robert & Linda  (PERM)

*Synthetic client - Project Evergreen training data.*

| Item | Detail |
|---|---|
| Client ID | EVG1004 |
| Taxpayer | Robert A. Castellano, DOB 05/14/1958 (age 67 at 12/31/2025), SSN XXX-XX-2847 - retired civil engineer, US citizen |
| Spouse | Linda M. Castellano, DOB 03/22/1961 (**age 64 at 12/31/2025; turns 65 on 03/22/2026**), SSN XXX-XX-6135 - Canadian citizen, US lawful permanent resident (green card since 2011) -> US tax resident |
| Address | {ADDR[0]}, {ADDR[1]} (Sarasota County, homestead) - **Florida: no individual income tax** |
| Retirement income | Robert: Social Security (Medicare B + D withheld); Gulf Coast Engineering Group pension; Schwab traditional IRA. Linda: Canadian employer pension (Nova Scotia Maritime Utilities Pension Plan, NR-4, 15% Canadian withholding under treaty Art. XVIII). Linda has no US Social Security. |
| Foreign accounts | Linda: RBC Royal Bank chequing (Halifax NS, acct ****4471) - FBAR filed every year by Linda (sole owner). No other foreign accounts, no RRSP/TFSA (closed 2019). |
| Health | Robert on Medicare. Linda (under 65) covered by Robert's retiree medical plan - premiums $330/mo deducted from his pension (after-tax). |
| Contact | Robert - email robert.castellano@example.com, (941) 555-0162. eSign OK. |
| Engagement | Client since 2021. Quote $1,950 (foreign pension/1116, FBAR, retiree). |
| Payment info | Voided check on file (Truist checking ending 3380) |

**PY WP notes:** Canadian pension converted at IRS yearly average rate; 1116 general-category limitation leaves an FTC carryforward
each year (Canada 15% > US average rate). FBAR: use Treasury Reporting Rates of Exchange at 12/31. Accrued interest on Schwab bond
purchases reversed on Schedule B. Standard deduction every year (itemized ~ $15-17k).
""")
F.prior_year_summary(C.perm_file("2024_Form_1040_Return_Summary.pdf", "Prior-year return summary"),
    "Robert & Linda Castellano", "EVG1004", "Married filing jointly", [
        ["2a", "Tax-exempt interest (Schwab munis)", 3020], ["2b", "Taxable interest (Schwab, RBC) net of accrued interest", 3410],
        ["3a / 3b", "Qualified / ordinary dividends", "5,010 / 5,960"],
        ["4a / 4b", "IRA distributions (Schwab) - taxable", "25,000 / 25,000"],
        ["5a / 5b", "Pensions: Gulf Coast Eng. $24,600 + Canadian pension CAD 23,400 @ 1.370 = $17,080", "41,680 / 41,680"],
        ["6a / 6b", "Social security (Robert) / taxable 85%", "37,200 / 31,620"],
        ["7", "Capital gain distributions", 690], ["11", "AGI", 108360],
        ["12", "Standard deduction (MFJ + 1 age-65 box)", 30750], ["15", "Taxable income", 77610],
        ["Sch 3-1", "Foreign tax credit (Form 1116 general category, limited)", 1140],
        ["24", "Total tax", 6430], ["26", "Estimates paid", 6000], ["25", "Withholding", 4610],
        ["34", "Overpayment - applied to 2025 estimated tax", 1150]],
    carryovers=[["Form 1116 general category FTC carryforward (2023 $1,210; 2024 $1,258)", 2468],
                ["2024 overpayment applied to 2025", 1150], ["Capital loss carryover", 0]],
    notes="FBAR 2024 filed 03/28/2025 by Linda (RBC max CAD 36,100). Linda turns 65 in March 2026 - senior items for her start 2026. "
          "Robert asked about QCDs for church giving - told him QCDs require age 70 1/2 (Nov 2028 for Robert).")

# ------------------------------------------------------------------ amounts
ss_gross, med_b, med_d = 38400.00, 185.00 * 12, 38.50 * 12
pen_gross, pen_wh = 24600.00, 2460.00
ira_gross, ira_wh, ira_to_church = 30000.00, 2200.00, 8000.00
nr4_cad, nr4_tax_cad = 24000.00, 3600.00
nr4_usd, nr4_tax_usd = round(nr4_cad / CAD_AVG, 2), round(nr4_tax_cad / CAD_AVG, 2)
rbc_int_cad = 42.18
rbc_int_usd = round(rbc_int_cad / CAD_AVG, 2)
rbc_max_cad = 37912.44
# Home Depot 4.90% bond, $15,000 face, bought 07/08/2025: accrued 04/15-07/08 (83 days, 30/360) = 367.50 x 83/180 = 169.46
schwab_int, schwab_treas, schwab_muni, accrued = 2438.87, 1862.40, 3114.75, 169.46
div_ord, div_q, cgd = 6184.22, 5207.90, 812.00
prop_tax = 5840.36
retiree_health = 330.00 * 12
med_oop = {"Dental (Linda crowns)": 1850.00, "Rx copays": 640.00, "Eyeglasses": 420.00, "Doctor copays": 285.00}
church_envelope = 2600.00
es_paid = [1500.00] * 4
py_overpay = 1150.00

# ------------------------------------------------------------------ PBC documents
F.organizer(C.pbc_file("01_2025_Organizer_Castellano.pdf", "Client organizer", "2026-02-16"),
    "Robert & Linda Castellano", "EVG1004",
    general=[("Did your marital status change during 2025?", "No", ""),
             ("Were you or your spouse age 65 or older?", "Yes", "Both - Linda turns 65 in March"),
             ("Did you have any foreign bank accounts or foreign income?", "Yes", "Linda RBC account + Canadian pension (NR-4)"),
             ("Did you take any IRA distributions?", "Yes", "$30,000 - $8,000 went straight to church as a QCD"),
             ("Did you make estimated tax payments?", "Yes", "4 x $1,500 + last year's refund applied"),
             ("Medical expenses (incl. Medicare premiums)?", "Yes", "see spreadsheet"),
             ("Did you receive, sell, exchange digital assets?", "No", "")],
    dependents=[],
    income_rows=[["Social Security", "SSA (Robert)", 37200, "see SSA-1099"],
                 ["Pension", "Gulf Coast Engineering Group", 24600, "24,600"],
                 ["Foreign pension (Linda)", "Nova Scotia Maritime Utilities PP (NR-4)", "CAD 23,400", "CAD 24,000"],
                 ["IRA distributions", "Schwab IRA ****8812", 25000, "30,000 (8,000 QCD)"],
                 ["Interest / dividends", "Schwab joint ****3307", "see 1099", "see 1099"],
                 ["Foreign interest", "RBC chequing (Linda)", "CAD 38", ""],
                 ["Tax-exempt interest", "Schwab munis", 3020, "see 1099"]],
    deductions_rows=[["Real estate tax", "Sarasota County (homestead)", 5610, "5,840.36"],
                     ["Charitable - cash", "First Presbyterian Church", 2500, "2,600 + 8,000 QCD"],
                     ["Medical", "see spreadsheet", 8900, "see spreadsheet"],
                     ["Estimated payments", "4 x 1,500", 6000, "6,000"], ["PY overpayment applied", "", 950, "1,150"]],
    signature_date="02/12/2026")
F.ssa_1099(C.pbc_file("02_SSA-1099_Robert.pdf", "Form SSA-1099", "2026-02-16"), [T["name"], T["ssn"]],
           {"3": ss_gross, "4": 0, "5": ss_gross, "8": "XXX-XX-2847A",
            "desc": ["DESCRIPTION OF AMOUNT IN BOX 3: Paid by check or direct deposit $35,718.00; "
                     f"Medicare Part B premiums deducted from your benefits ${med_b:,.2f}; "
                     f"Medicare prescription drug (Part D) premiums deducted ${med_d:,.2f}. Total additions $38,400.00.",
                     "Benefits for 2025: $3,200.00 per month (after 2.5% COLA). No voluntary federal income tax withheld."]})
F.f1099_r(C.pbc_file("03_1099-R_Gulf_Coast_Engineering_Pension.pdf", "Form 1099-R", "2026-02-16"),
          ["Gulf Coast Engineering Group Retirement Plan", "c/o Principal Financial - 711 High St", "Des Moines, IA 50392",
           "TIN: 00-5528140"], REC_T, {"1": pen_gross, "2a": pen_gross, "4": pen_wh, "7": "7", "state": "FL / - / -"},
          notes=["Retiree medical premiums of $3,960.00 were deducted on an after-tax basis from your 2025 monthly benefit "
                 "($330.00/month - spouse coverage). These deductions do not reduce the amounts in box 1 or 2a."])
F.f1099_r(C.pbc_file("04_1099-R_Schwab_IRA.pdf", "Form 1099-R", "2026-02-16"),
          ["Charles Schwab & Co., Inc. - IRA Custodian", "PO Box 982600", "El Paso, TX 79998", "TIN: 00-1737782"], REC_T,
          {"1": ira_gross, "2a": ira_gross, "2b": "Total distribution: No", "4": ira_wh, "7": "7Y   IRA/SEP/SIMPLE: X",
           "13": "various"}, account="IRA ****8812",
          notes=["Distributions 2025: 06/10 $22,000 to owner (10% federal withholding $2,200); 12/05 $8,000 check payable to "
                 "First Presbyterian Church of Sarasota (owner-directed charitable distribution)."])
statement(C.pbc_file("05_Schwab_2025_Consolidated_1099_Joint_3307.pdf", "Consolidated 1099 (brokerage)", "2026-02-16"),
    "Charles Schwab - 2025 Form 1099 Composite & Year-End Summary - Account ****3307 (JT TEN)", [
        {"para": "Robert A. & Linda M. Castellano JT TEN - Recipient TIN XXX-XX-2847. Payer: Charles Schwab & Co., Inc., TIN 00-1737782. "
                 "This is important tax information and is being furnished to the IRS."},
        {"heading": "Form 1099-DIV", "table": [["Box", "Description", "Amount"], ["1a", "Total ordinary dividends", div_ord],
                                              ["1b", "Qualified dividends", div_q], ["2a", "Total capital gain distributions", cgd],
                                              ["3", "Nondividend distributions", 0], ["4", "Federal income tax withheld", 0],
                                              ["5", "Section 199A dividends", 0], ["7", "Foreign tax paid", 0]]},
        {"heading": "Form 1099-INT", "table": [["Box", "Description", "Amount"], ["1", "Interest income", schwab_int],
                                              ["3", "Interest on U.S. Savings Bonds and Treasury obligations", schwab_treas],
                                              ["4", "Federal income tax withheld", 0], ["8", "Tax-exempt interest", schwab_muni],
                                              ["9", "Specified private activity bond interest", 0], ["11", "Bond premium", 0]]},
        {"heading": "Form 1099-B", "para": "No reportable sales or redemptions in 2025."},
        {"heading": "Detail of Interest Income (supplemental - not reported to IRS)", "pagebreak": True,
         "table": [["Security", "CUSIP", "Date", "Type", "Amount"],
                   ["JPMorgan Chase & Co 4.25% 10/01/2027", "46625HRL6", "04/01, 10/01", "Corporate interest", 1062.50],
                   ["Verizon Communications 3.875% 02/08/2029", "92343VEN0", "02/08, 08/08", "Corporate interest", 968.75],
                   ["Home Depot 4.90% 04/15/2029", "437076CV2", "10/15", "Corporate interest", 367.50],
                   ["Schwab Bank sweep", "", "monthly", "Bank interest", 40.12],
                   ["Subtotal box 1", "", "", "", schwab_int],
                   ["US Treasury Note 4.125% 11/15/2027", "91282CJK8", "05/15, 11/15", "Treasury interest", 1237.50],
                   ["US Treasury Bill 26-wk (matured 09/18/2025)", "912797KX4", "09/18", "Treasury discount", 624.90],
                   ["Subtotal box 3", "", "", "", schwab_treas],
                   ["Florida St Brd Ed Pub 5% 06/01/2031", "341271AD6", "06/01, 12/01", "Tax-exempt", 1250.00],
                   ["Sarasota Cnty Util Rev 4% 10/01/2034", "803296FP1", "04/01, 10/01", "Tax-exempt", 1000.00],
                   ["Tampa Bay Water Rev 3.5% 10/01/2036", "875464HD8", "04/01, 10/01", "Tax-exempt", 864.75],
                   ["Subtotal box 8", "", "", "", schwab_muni]], "left_align_cols": [0, 1, 2, 3]},
        {"heading": "Accrued Interest Paid on Purchases (supplemental)",
         "table": [["Security", "Trade date", "Accrued interest paid", "Note"],
                   ["Home Depot 4.90% 04/15/2029 ($15,000 face)", "07/08/2025", accrued,
                    "Paid to seller at purchase; included in the 10/15/2025 coupon reported in box 1"]],
         "note": "Accrued interest paid on purchases is not netted against box 1 interest. Consult your tax advisor."},
        {"heading": "Year-End Summary (not reported to IRS)", "table": [["Item", "Amount"], ["Margin interest paid", 0],
                                                                         ["Account value 12/31/2025", 612884.19]]}])
info_form(C.pbc_file("06_NR4_Nova_Scotia_Maritime_Utilities_Pension_Linda.pdf", "Canadian NR-4 slip", "2026-02-16",
                     "Sharefile upload", "Canadian tax slip"),
          "NR-4", "Statement of Amounts Paid or Credited to Non-Residents of Canada",
          payer=["Payer or agent (Payeur ou agent)", "Nova Scotia Maritime Utilities Pension Plan", "1894 Barrington St, Suite 1200",
                 "Halifax NS  B3J 2A8  CANADA", "Non-resident account no. NR0071 4471"],
          recipient=["Recipient (Beneficiaire)", "CASTELLANO, LINDA M.", ADDR[0], ADDR[1] + "  USA", "Foreign TIN: XXX-XX-6135"],
          boxes=[("10", "Year", "2025"), ("11", "Recipient code", "1 - Individual"), ("12", "Country code for tax purposes", "USA"),
                 ("13", "Foreign or Canadian tax ID", "XXX-XX-6135"), ("14", "Income code", "46"), ("15", "Currency code", "CAD"),
                 ("16", "Gross income", nr4_cad), ("17", "Non-resident tax withheld", nr4_tax_cad), ("18", "Exemption code", "")],
          copy_label="Copy for recipient - Canada Revenue Agency / Agence du revenu du Canada",
          notes=["Income code 46 = pension or superannuation. Tax withheld at the 15% treaty rate (Canada-United States Tax "
                 "Convention, Article XVIII). Amounts are in Canadian dollars."])
statement(C.pbc_file("07_RBC_Chequing_2025_statements_summary.pdf", "Foreign bank statements (summary)", "2026-02-16"),
    "RBC Royal Bank - Chequing Account ****4471 - 2025 Statement Summary (CAD)", [
        {"para": "Account holder: Linda M. Castellano (sole). Branch: Spring Garden Rd, Halifax NS. Currency: CAD."},
        {"table": [["Month", "Opening", "Deposits", "Withdrawals", "Closing", "Highest balance in month"],
                   ["Jan", 29844.10, 1850.00, 1210.40, 30483.70, 31102.55],
                   ["Mar", 30720.33, 2000.00, 1400.00, 31320.33, 32404.81],
                   ["Jun", 33115.20, 5210.00, 2890.00, 35435.20, rbc_max_cad],
                   ["Sep", 34101.62, 1850.00, 4400.00, 31551.62, 34988.10],
                   ["Dec", 31802.90, 1850.00, 2447.80, 31205.10, 32691.40]],
         "note": "Selected months shown by client. Maximum balance during 2025: CAD 37,912.44 (06/27/2025)."},
        {"table": [["Interest paid 2025 (CAD)", rbc_int_cad], ["Canadian tax withheld on interest", 0.00]]}])
statement(C.pbc_file("08_Schwab_IRA_8812_Year-End_Statement.pdf", "IRA year-end statement", "2026-02-16"),
    "Charles Schwab - Traditional IRA ****8812 - 2025 Year-End Summary (Robert A. Castellano)", [
        {"table": [["Item", "Amount"], ["Value 12/31/2024", 486220.14], ["Dividends (inside IRA)", 9812.40],
                   ["Interest (inside IRA)", 3104.66], ["Realized gains (inside IRA)", 14280.00], ["Distributions", -ira_gross],
                   ["Federal tax withheld", -ira_wh], ["Change in value", 21002.80], ["Value 12/31/2025", 502020.00]]},
        {"para": "Income earned in your IRA is tax-deferred and is not reported on Form 1099-DIV/INT/B. Required minimum distribution: "
                 "none required for 2025 (your RMD age is 73). Fair market value reported to the IRS on Form 5498."}])
statement(C.pbc_file("09_Sarasota_County_2025_Property_Tax_Receipt.pdf", "Property tax receipt", "2026-02-16"),
    "Sarasota County Tax Collector - 2025 Real Estate Tax Receipt", [
        {"table": [["Item", "Detail"], ["Parcel", "0081-12-0047"], ["Situs", ADDR[0]], ["Homestead exemption", "Yes"],
                   ["Gross tax", 6083.71], ["Paid 11/24/2025 (4% discount)", prop_tax]], "left_align_cols": [0, 1]}])
write_xlsx(C.pbc_file("10_Medical_expenses_2025.xlsx", "Client spreadsheet (XLSX)", "2026-02-16"),
    {"Medical 2025": [["Date", "Provider / payee", "Who", "Description", "Amount"],
                      ["monthly", "Gulf Coast Eng. retiree plan", "Linda", "Health premium (from pension)", retiree_health],
                      ["06/2025", "Sarasota Family Dental", "Linda", "Crowns x2", med_oop["Dental (Linda crowns)"]],
                      ["various", "Publix Pharmacy", "Both", "Rx copays", med_oop["Rx copays"]],
                      ["09/2025", "Costco Optical", "Robert", "Eyeglasses", med_oop["Eyeglasses"]],
                      ["various", "Sarasota Memorial", "Both", "Doctor copays", med_oop["Doctor copays"]],
                      ["", "", "", "(Medicare B/D - see SSA form)", ""],
                      ["", "", "", "TOTAL", retiree_health + sum(med_oop.values())]]})
statement(C.pbc_file("11_First_Presbyterian_2025_Giving_Statement.pdf", "Charitable acknowledgment", "2026-02-16"),
    "First Presbyterian Church of Sarasota - 2025 Contribution Statement", [
        {"para": "Robert & Linda Castellano - Envelope #214. First Presbyterian Church of Sarasota is a 501(c)(3) organization "
                 "(EIN 00-0612203)."},
        {"table": [["Date", "Description", "Amount"], ["2025 weekly", "Offering envelopes (52)", church_envelope],
                   ["12/08/2025", "Check #0041178 from Charles Schwab & Co. FBO Robert Castellano IRA", ira_to_church],
                   ["Total", "", church_envelope + ira_to_church]], "total_row": True},
        {"para": "No goods or services were provided in exchange for these contributions other than intangible religious benefits."}])
write_text(C.pbc_file("12_Email_Robert_2026-02-14.txt", "Client correspondence", "2026-02-14", "Email"),
"""From: Robert Castellano <robert.castellano@example.com>
To: preparer@evergreentax.example
Date: Sat, 14 Feb 2026 09:31:22 -0500
Subject: Castellano 2025 docs uploaded

Good morning - all our documents are on Sharefile. A few notes:
- This year I did the QCD you and I talked about - $8,000 of my IRA withdrawal went directly from Schwab to the church
  in December, so only $22,000 should be taxable. The church statement shows it.
- Linda's pension slip is in Canadian dollars as usual.
- Estimated payments: $1,500 on 4/14, 6/13, 9/12 and 1/13, plus the $1,150 from last year.
- Linda is 65 this year for the extra deduction, right? (She turns 65 on March 22.)
Thanks - Bob
""")
F.f1099_r(C.pbc_file("13_1099-R_Schwab_IRA_CORRECTED.pdf", "Form 1099-R (CORRECTED)", "2026-03-02", "Mail (client scanned)",
                     "corrected form"),
          ["Charles Schwab & Co., Inc. - IRA Custodian", "PO Box 982600", "El Paso, TX 79998", "TIN: 00-1737782"], REC_T,
          {"1": ira_gross, "2a": ira_gross, "2b": "Total distribution: No", "4": ira_wh, "7": "7   IRA/SEP/SIMPLE: X",
           "13": "various"}, account="IRA ****8812", corrected=True,
          notes=["CORRECTED: distribution code Y (qualified charitable distribution) removed. The account owner had not attained "
                 "age 70 1/2 on the 12/05/2025 distribution date; the $8,000 charitable check is reported as a normal distribution.",
                 "Distributions 2025: 06/10 $22,000 to owner; 12/05 $8,000 check payable to First Presbyterian Church of Sarasota."])
statement(C.pbc_file("14_IRS_Direct_Pay_confirmations.pdf", "Payment confirmations", "2026-02-16"),
    "IRS Direct Pay - Payment Confirmations (printed by client)", [
        {"table": [["Confirmation #", "Date", "Type", "Tax period", "Amount"],
                   ["2QX-114-8829-07", "04/14/2025", "Estimated tax", "2025", 1500.00],
                   ["2QX-164-1180-44", "06/13/2025", "Estimated tax", "2025", 1500.00],
                   ["2QX-255-3071-19", "09/12/2025", "Estimated tax", "2025", 1500.00],
                   ["2QX-013-9920-62", "01/13/2026", "Estimated tax", "2025", 1500.00]]}])

# ------------------------------------------------------------------ RETURN (two passes: FTC limitation needs TI)
interest = [{"payer": "Charles Schwab ****3307 - interest (corporate bonds / sweep)", "amount": schwab_int,
             "tax_exempt": schwab_muni},
            {"payer": "Charles Schwab ****3307 - U.S. Treasury interest", "amount": schwab_treas},
            {"payer": "Royal Bank of Canada ****4471 (CAD 42.18 @ 1.398) - foreign", "amount": rbc_int_usd},
            {"payer": "Accrued interest paid on purchase - Home Depot 4.90% 2029 (Schwab)", "amount": -accrued}]


def build(ira_taxable, fs_ti):
    f = {
        "status": "MFJ", "taxpayer": {"age65": True}, "spouse": {"age65": False},
        "ssa": [{"who": "T", "net_benefits": ss_gross}],
        "pension": [{"payer": "Gulf Coast Engineering Group Retirement Plan", "gross": pen_gross, "taxable": pen_gross},
                    {"payer": "Nova Scotia Maritime Utilities PP (NR-4, CAD 24,000 @ 1.398)", "gross": nr4_usd, "taxable": nr4_usd}],
        "ira": [{"payer": "Charles Schwab IRA ****8812 (CORRECTED 1099-R)", "gross": ira_gross, "taxable": ira_taxable}],
        "interest": interest,
        "dividends": [{"payer": "Charles Schwab ****3307", "ordinary": div_ord, "qualified": div_q, "capgain_dist": cgd}],
        "foreign_accounts": True, "foreign_account_country": "Canada",
        "withholding_1099": pen_wh + ira_wh,
        "sch1a": {"seniors": 1},
        "ftc": {"taxes": nr4_tax_usd, "foreign_source_ti": fs_ti, "category": "general (pension)"},
        "estimated_payments": sum(es_paid) + py_overpay,
    }
    return Return1040(f).compute()


def fs_taxable_income(R0):
    v0 = R0.values
    deds = v0["12e"] + v0["13b"]
    return nr4_usd - deds * nr4_usd / v0["9"]      # Form 1116 line 3 apportionment by gross income


R0 = build(ira_gross, nr4_usd)
fs_ti = fs_taxable_income(R0)
R = build(ira_gross, fs_ti)
assert abs(fs_taxable_income(R) - fs_ti) < 1
v = R.values
# what the client expected (QCD excluded) - for the notes
Rq0 = build(ira_gross - ira_to_church, nr4_usd)
Rq = build(ira_gross - ira_to_church, fs_taxable_income(Rq0))
qcd_cost = Rq.values["refund"] - v["refund"] if v["refund"] else None

ftc_used = R.forms_value("Schedule 3", "1")
# Schedule A comparison (computed here, Schedule A not filed)
med_total = r(med_b + med_d + retiree_health + sum(med_oop.values()))
med_floor = r(v["11"] * .075)
med_ded = max(0, med_total - med_floor)
itemized_total = med_ded + r(prop_tax) + r(church_envelope + ira_to_church)
std_total = v["12e"]
assert itemized_total < std_total
ftc_limit = r(v["16"] * fs_ti / v["15"])
ftc_cf_2025 = r(nr4_tax_usd) - ftc_used
ftc_cf_total = 2468 + ftc_cf_2025

# SS worksheet detail
exempt = r(schwab_muni)
other_inc = v["1z"] + v["2b"] + v["3b"] + v["4b"] + v["5b"] + v["7"] + v["8"]
ssw = [["Social Security Benefits Worksheet (MFJ)", "Amount"], ["1 Box 5 of SSA-1099 (Robert)", r(ss_gross)],
       ["2 50% of line 1", r(ss_gross / 2)],
       ["3 Lines 1z, 2b, 3b, 4b, 5b (incl. Canadian pension), 7, 8", other_inc], ["4 Tax-exempt interest (line 2a)", exempt],
       ["5 Provisional income (2 + 3 + 4)", r(ss_gross / 2) + other_inc + exempt], ["8 Base amount (MFJ)", 32000],
       ["10 Additional amount", 12000], ["18 Taxable social security (85% maximum reached)", v["6b"]]]
itemize = [["Itemized vs standard", "Amount"],
           ["Medical: Medicare B $2,220 + D $462 (SSA-1099) + retiree premium $3,960 + dental/Rx/eyewear/copays $3,195",
            med_total],
           ["Less 7.5% of AGI", -med_floor], ["Deductible medical", med_ded],
           ["Real estate tax (SALT cap $40,000 not reached)", r(prop_tax)],
           ["Charitable: envelopes $2,600 + $8,000 IRA check (not a QCD)", r(church_envelope + ira_to_church)],
           ["Total itemized", itemized_total],
           ["Standard deduction MFJ $31,500 + $1,600 (Robert 65+; Linda 64 - no)", std_total],
           ["Senior deduction (Robert only) - allowed with either", v["13b"]], ["Use", "Standard"]]
f1116 = [["Form 1116 - General category income (Canada)", "Amount"],
         ["1a Gross foreign-source income: NR-4 pension CAD 24,000 / 1.398", r(nr4_usd)],
         ["3a Standard deduction + senior deduction (not definitely related)", v["12e"] + v["13b"]],
         ["3d/3e Gross foreign income / gross income all sources (line 9)", f"{r(nr4_usd):,} / {v['9']:,}"],
         ["6 Apportioned deductions", r(nr4_usd - fs_ti)], ["7 Net foreign-source taxable income", r(fs_ti)],
         ["8 Foreign taxes paid: CAD 3,600 / 1.398 (15% treaty rate; paid basis)", r(nr4_tax_usd)],
         ["10 Carryover from prior years (2023-2024)", 2468],
         ["18 Worldwide taxable income (adjustment exception - no foreign QD/CG)", v["15"]],
         ["20 US tax (1040 line 16)", v["16"]], ["21 Limitation = line 20 x line 17 / line 18", ftc_limit],
         ["24 Foreign tax credit (to Schedule 3 line 1)", ftc_used],
         ["Carryforward to 2026 (general category): 2023 $1,210 + 2024 $1,258 + 2025 " + f"{ftc_cf_2025:,}", ftc_cf_total]]
fbar = [["FinCEN Form 114 (FBAR) - 2025 - filer: Linda M. Castellano", "Detail"],
        ["Financial institution", "Royal Bank of Canada, 1505 Barrington St, Halifax NS (chequing ****4471), sole owner"],
        ["Maximum value (CAD)", "37,912.44 (06/27/2025)"],
        ["Rate: Treasury Reporting Rates of Exchange 12/31/2025 (Canada-Dollar) - assumed", f"{CAD_FBAR}"],
        ["Maximum value (USD)", f"{r(rbc_max_cad / CAD_FBAR):,}"],
        ["Aggregate > $10,000 -> FBAR required", "Yes"],
        ["Due 04/15/2026 (automatic extension to 10/15/2026) - BSA E-Filing", "Filed 03/27/2026"],
        ["Form 8938 (MFJ, US residents: > $100,000 year-end / $150,000 any time)", "Not required"]]
schb3 = [["Schedule B Part III", "Answer"], ["7a Financial interest in / signature authority over a foreign account?", "Yes"],
         ["7a Required to file FinCEN Form 114?", "Yes"], ["7b Country", "Canada"], ["8 Foreign trust", "No"]]
C.write_return(R, [
    ("Taxpayer", "Robert A. Castellano (XXX-XX-2847), age 67"),
    ("Spouse", "Linda M. Castellano (XXX-XX-6135), age 64"),
    ("Address", ", ".join(ADDR)),
    ("Filing status", "Married filing jointly"),
    ("Age 65+ boxes", "Robert - checked; Linda (born 03/22/1961) - NOT checked"),
    ("Digital assets question", "No"),
    ("Forms included", "1040; Sch 1-A, 3, B (Part III), D; Form 1116 (general category)"),
    ("Other filings", "FinCEN 114 (FBAR) - Linda - BSA E-Filing 03/27/2026"),
    ("State", "None - Florida has no individual income tax"),
    ("Filing method", "E-file (8879 signed 03/25/2026); direct deposit Truist ****3380"),
], attachments=[("Social Security benefits worksheet", ssw), ("Standard vs itemized comparison (Schedule A not filed)", itemize),
                ("Form 1116 detail (general category)", f1116), ("Schedule B Part III / FBAR summary", schb3 + fbar[1:]),
                ("Foreign currency translation",
                 [["Item", "CAD", "Rate", "USD"], ["NR-4 gross pension (IRS 2025 yearly average)", nr4_cad, "1.398", r(nr4_usd)],
                  ["NR-4 tax withheld", nr4_tax_cad, "1.398", r(nr4_tax_usd)], ["RBC interest", rbc_int_cad, "1.398", r(rbc_int_usd)],
                  ["RBC max balance (FBAR - Treasury 12/31 rate, assumed)", rbc_max_cad, str(CAD_FBAR), r(rbc_max_cad / CAD_FBAR)]])])

gotchas = [
    gotcha("EVG1004-G1", "Return - Schedule A (Medicare premiums from SSA-1099)", "Medicare Part B/D premiums in the SSA-1099 description",
           "Ignore the Medicare premiums (and Linda's after-tax retiree premiums) when testing itemized deductions, or use net benefits "
           "($35,718) as box 5.",
           "Box 5 is gross $38,400 (premiums are included in benefits). Medicare B $2,220 + D $462 and the $3,960 after-tax retiree premium "
           "go to medical on the Schedule A comparison; after the 7.5% floor, itemized total still < standard deduction -> standard.",
           "6a/6b and itemize decision", ["6a", "12e"], "easy"),
    gotcha("EVG1004-G2", "Foreign Transactions - Form 1116 (Canadian NR-4 pension)", "Canadian pension in CAD",
           "Enter CAD 24,000 as USD, omit it (thinking the treaty/Canadian tax covers it), or leave it out of the taxable SS computation.",
           f"Convert at the IRS 2025 yearly average (1.398): {fmt(r(nr4_usd))} on lines 5a/5b; it is included in provisional income for "
           "taxable SS (85% maximum reached).",
           "5a/5b and 6b", ["5a", "5b", "6b"], "medium"),
    gotcha("EVG1004-G3", "Foreign Transactions - Form 1116", "FTC on the Canadian pension: general category, no de minimis election",
           "Claim the $2,575 directly on Schedule 3 without Form 1116, or classify as passive.",
           f"Pension is general-category income and not 'qualified passive income' reported on a payee statement, and $2,575 > $600 -> "
           f"Form 1116 required. Limitation {fmt(ftc_limit)}; credit {fmt(ftc_used)}; {fmt(ftc_cf_2025)} added to the carryforward "
           f"(total {fmt(ftc_cf_total)}).",
           "Sch 3 line 1", ["20", "Sch 3 line 1"], "hard"),
    gotcha("EVG1004-G4", "Foreign Transactions - FinCEN114/FBAR", "RBC chequing account -> FBAR + Schedule B Part III",
           "Answer Schedule B line 7a 'No' (the interest is tiny) and skip FBAR, or file Form 8938.",
           f"Max value CAD 37,912 = ~{fmt(r(rbc_max_cad / CAD_FBAR))} (Treasury 12/31 rate) > $10,000 -> FinCEN 114 by Linda (due 4/15, "
           "auto-extended to 10/15); Schedule B Part III Yes / Canada; RBC interest is taxable. Form 8938 not required (below MFJ thresholds).",
           "FBAR penalty exposure", ["Sch B Part III", "FBAR"], "medium"),
    gotcha("EVG1004-G5", "Return - Schedule B (accrued interest reversal)", "Accrued interest paid at purchase",
           f"Report box 1 interest as shown ({fmt(r(schwab_int))}), or treat tax-exempt interest as taxable / omit it.",
           f"Subtract {fmt(r(accrued))} 'Accrued interest' on Schedule B (bond bought between coupon dates). Muni interest $3,115 on line 2a "
           "(not taxable, but counts in SS provisional income).",
           f"2b overstated {fmt(r(accrued))}", ["2a", "2b"], "medium"),
    gotcha("EVG1004-G6", "Review - Client IRAs", "Schwab IRA year-end statement in the PBC",
           "Autoflow the IRA's dividends ($9,812), interest ($3,105) and gains ($14,280) onto Schedules B/D.",
           "Income inside a traditional IRA is not reported; only distributions (1099-R) are taxable.",
           "Would overstate income ~$27,000", ["2b", "3b", "7"], "easy"),
    gotcha("EVG1004-G7", "Scan - Duplicate documents (corrected 1099-R) / QCD age test", "'QCD' by a 67-year-old; corrected 1099-R",
           "Use both 1099-Rs (double count $30,000) and/or exclude $8,000 as a QCD per the client and the original code Y.",
           "Use the CORRECTED 1099-R only. A QCD requires the owner to be 70 1/2 on the distribution date (Robert: 11/14/2028). The full "
           "$30,000 is taxable (4b); the $8,000 is a cash charitable contribution usable only if itemizing (it isn't beneficial). "
           "No RMD was required (RMD age 73).",
           f"4b $30,000 not $22,000 (refund {'lower by ' + fmt(qcd_cost) if qcd_cost is not None else 'affected'})", ["4a", "4b"], "hard"),
    gotcha("EVG1004-G8", "Return - Schedule 1-A senior deduction / standard deduction age test", "Linda is 64 at 12/31/2025",
           "Check both age-65 boxes (+$3,200) and claim the $6,000 senior deduction for both spouses (client says 'Linda is 65 this year').",
           "Linda turns 65 on 03/22/2026 -> only Robert gets the $1,600 additional standard deduction and the $6,000 senior deduction "
           f"(MAGI {fmt(v['11'])} < $150,000, no phase-out).",
           "12e / 13b overstated $7,600", ["12e", "13b"], "easy"),
    gotcha("EVG1004-G9", "Return - estimated payments", "Estimates + prior-year overpayment",
           "Enter only the four $1,500 payments (or the organizer's $950 PY figure).",
           "Line 26 = 4 x $1,500 + $1,150 2024 overpayment applied (per PY return) = $7,150.",
           "Line 26", ["26"], "easy"),
]
C.write_answer_key(R, {"residence": "FL - Sarasota (no state return)", "complexity": "Retiree, foreign pension, FBAR"}, gotchas,
                   filings=[{"form": "Form 1040 (federal)", "method": "e-file", "due": "2026-04-15", "filed": "2026-03-27"},
                            {"form": "FinCEN Form 114 (FBAR) - Linda", "method": "BSA E-Filing", "due": "2026-04-15 (auto-ext 2026-10-15)",
                             "filed": "2026-03-27"}],
                   extra={"assumptions": [f"FBAR Treasury 12/31/2025 CAD rate assumed {CAD_FBAR}",
                                          "1116 line 3 apportionment includes the Sch 1-A senior deduction with the standard deduction",
                                          "Canadian employer pension non-contributory -> no US investment in the contract",
                                          "QD/CG adjustment exception applies for Form 1116 (no foreign-source QD/CG)"],
                          "ftc_carryforward_general_total": ftc_cf_total,
                          "client_expected_qcd_refund": Rq.values["refund"]})
C.write_receipt_log("EVG1004-1040-2025", "J. Ortiz (staff)", "R. Patel (senior)", "S. Kennedy, CPA", "2026-02-16")

C.write_notes(f"""
# EVG1004 - Castellano, Robert & Linda - 2025 Form 1040 - Preparer Notes

*Synthetic client - Project Evergreen. Return status: **signed off, e-filed 03/27/2026, accepted. FBAR filed 03/27/2026.***

## Return summary
| | |
|---|---|
| Filing status | Married filing jointly |
| Tax-exempt interest (2a) | {fmt(v['2a'])} |
| Taxable interest / ordinary dividends | {fmt(v['2b'])} / {fmt(v['3b'])} |
| IRA distributions (4a / 4b) | {fmt(v['4a'])} / {fmt(v['4b'])} |
| Pensions incl. Canadian (5a / 5b) | {fmt(v['5a'])} / {fmt(v['5b'])} |
| Social security (6a / 6b) | {fmt(v['6a'])} / {fmt(v['6b'])} |
| AGI | {fmt(v['11'])} |
| Standard deduction (1 age-65 box) + senior deduction (Robert) | {fmt(v['12e'])} + {fmt(v['13b'])} |
| Taxable income | {fmt(v['15'])} |
| Tax / foreign tax credit | {fmt(v['16'])} / {fmt(ftc_used)} |
| Total tax (line 24) | {fmt(v['24'])} |
| Withholding (1099-R) + estimates/PY overpayment | {fmt(v['25d'])} + {fmt(v['26'])} |
| **Refund** | **{fmt(v['refund'])}** |

## What I did and why (plain English)
1. **The "QCD" is not a QCD.** Robert asked Schwab to send $8,000 of his IRA to First Presbyterian in December and calls it a QCD.
   A qualified charitable distribution is only available once the IRA owner is **70 1/2** (Robert: 11/14/2028). Schwab caught
   this and issued a **CORRECTED 1099-R** (received 03/02) removing code Y. We used the corrected form only (the original is a
   superseded duplicate). The full $30,000 is taxable on line 4b. The $8,000 is still a charitable gift, but it only helps if they
   itemize - they don't (see comparison). Compared with what Robert expected, the refund is {fmt(qcd_cost) if qcd_cost is not None else 'n/a'} lower.
   No RMD was required in 2025 (RMD age 73). Discussed with Robert by phone 03/04 - he understood; plan QCDs starting 11/2028.
2. **Linda is 64.** She turns 65 on 03/22/2026, so for 2025 only Robert gets the extra $1,600 standard deduction and the new
   $6,000 senior deduction (MAGI {fmt(v['11'])} is under $150,000, no phase-out). Robert's email assumed both - corrected.
3. **Social Security.** Box 5 $38,400 is the gross benefit - the Medicare Part B ($2,220) and Part D ($462) premiums were deducted
   from it but are still income. Taxable SS worksheet: provisional income includes the Canadian pension and the $3,115 muni
   interest; 85% maximum reached -> {fmt(v['6b'])}.
4. **Canadian pension (NR-4).** Linda's CAD 24,000 employer pension is taxable in the US (treaty Art. XVIII lets Canada withhold
   15%, the US taxes as residence country). Converted at the IRS 2025 yearly average CAD 1.398 = {fmt(r(nr4_usd))} on line 5a/5b.
   Plan is non-contributory, so no US basis. Canadian tax CAD 3,600 = {fmt(r(nr4_tax_usd))}.
5. **Foreign tax credit (Form 1116, general category).** Not passive, not on a US payee statement and > $600, so no de minimis
   election - Form 1116 required. Foreign-source taxable income {fmt(r(fs_ti))} (after apportioning the standard + senior deduction
   by gross income). Limitation {fmt(v['16'])} x {r(fs_ti):,} / {v['15']:,} = {fmt(ftc_limit)}; credit {fmt(ftc_used)}. The rest
   ({fmt(ftc_cf_2025)}) joins the carryforward (total general-category carryforward {fmt(ftc_cf_total)}; 10-year life). Their US
   average rate is below Canada's 15%, so this carryforward will keep growing - no action possible other than tracking it.
   QD/CG adjustment exception applies (no foreign-source dividends or gains).
6. **Schwab consolidated 1099.** Interest {fmt(r(schwab_int))} less **{fmt(r(accrued))} accrued interest** paid when they bought the Home Depot bond in July
   (shown as a separate "Accrued interest" subtraction on Schedule B). Treasury interest $1,862 (federal taxable; no state return, so
   no state subtraction matters). Muni interest $3,115 on line 2a. Qualified dividends $5,208 and capital gain distributions $812 - all
   in the 0% bracket.
7. **Schwab IRA statement** - income earned inside the IRA ($27k of dividends/interest/gains) is not reported; only the 1099-R.
8. **RBC account / FBAR.** Linda's RBC chequing peaked at CAD 37,912 (~{fmt(r(rbc_max_cad / CAD_FBAR))} at the Treasury 12/31/2025 rate
   - **assumed {CAD_FBAR}; verify against the published table**). FBAR required; filed by Linda (sole owner) via BSA E-Filing 03/27.
   Schedule B Part III: Yes / Canada. RBC interest CAD 42 = ${r(rbc_int_usd)} included. Form 8938 not required (foreign assets well under
   $100k/$150k MFJ thresholds).
9. **Itemized vs standard.** Medical {fmt(med_total)} less 7.5% of AGI ({fmt(med_floor)}) leaves {fmt(med_ded)}; property tax
   $5,840 (well under the $40,000 SALT cap); charity $10,600 -> {fmt(itemized_total)} vs standard {fmt(std_total)}. **Standard.**
10. **Payments.** Four $1,500 estimates (confirmations in PBC) + $1,150 2024 overpayment applied (PY return; the organizer PY column
   showed $950, which was the 2023 figure) = {fmt(v['26'])}. Withholding: pension $2,460 + IRA $2,200 (corrected 1099-R).
11. **Florida.** No state income tax return.

## Open items / client communication
- 2026: Linda turns 65 (both senior items); remind Linda of her Medicare initial enrollment period (around 03/2026); her Medicare premiums will then replace the retiree-plan premium withheld from Robert's pension.
- 2026 estimates: $1,500/quarter continues to be sufficient (2025 tax {fmt(v['24'])}).
- Robert to tell Schwab in future to process charitable checks as QCDs only from 11/14/2028.

## Hand-off to signer / routing
- [x] Return locked; Accountant's copy saved as *reviewed*
- [x] Federal 1040 - e-file; no state
- [x] **FBAR (FinCEN 114) - Linda - filed 03/27/2026** (due 04/15/2026, auto-extension 10/15/2026)
- [x] Form 1116 carryforward schedule updated in PERM
- [x] eSign (8879) - Robert by email; refund direct deposit Truist ****3380
- Billing: $1,950 quote (1116 + FBAR + retiree) + 0.5 hr for the QCD / corrected 1099-R discussion (client-chargeable, external).
""")
C.write_review_points(f"""
# Review Points - EVG1004 - 2025 - Form 1040

*Reviewer: R. Patel (blue). Preparer responses in red. Synthetic.*

1. **WP 4 / WP 13 - 1099-R Schwab IRA** - Both the original (code 7Y) and the CORRECTED 1099-R autoflowed -> $60,000 of IRA
   distributions and $4,400 withholding. Use the corrected form only.
   - *Preparer: Original bookmarked "superseded"; one 1099-R remains.*
2. **Line 4b / QCD** - Draft excluded $8,000 as a QCD per Robert's email. Robert is 67 - QCD requires age 70 1/2. The corrected
   1099-R removed code Y. Make 4b $30,000 and remove the "QCD" notation. Call Robert before we send it.
   - *Preparer: Done. Spoke with Robert 03/04 (call memo in WP). Refund decreases {fmt(qcd_cost) if qcd_cost is not None else ''}.*
3. **Standard deduction / Schedule 1-A** - Draft checked the age-65 box for Linda and claimed 2 x $6,000 senior deduction.
   Linda's DOB is 03/22/1961 - she is 64 at 12/31/2025. Robert only.
   - *Preparer: Corrected - std {fmt(v['12e'])}, senior {fmt(v['13b'])}.*
4. **Schedule B** - Accrued interest ({fmt(r(accrued))}, Schwab supplemental page) not reversed. Add as a negative "Accrued interest" line.
   RBC interest missing - add (converted at 1.398).
   - *Preparer: Done.*
5. **Line 5a/5b / Form 1116** - Draft entered the NR-4 at CAD face value (24,000) and claimed the Canadian tax as a direct credit.
   Convert at 1.398 and run Form 1116 general category with the PY carryforward; no de minimis.
   - *Preparer: 5b now includes {fmt(r(nr4_usd))}; 1116 credit {fmt(ftc_used)}; carryforward {fmt(ftc_cf_total)}.*
6. **WP 8 - Schwab IRA statement** - Autoflow picked up the IRA's dividends/gains as 1099 income. Delete - income inside the IRA is
   not reportable.
   - *Preparer: Removed; page tickmarked "IRA - info only".*
7. **FBAR / Sch B Part III** - Mark Part III Yes / Canada and put FBAR on the routing sheet with its due date. Document the 12/31
   Treasury rate used.
   - *Preparer: Done; rate source noted in WP (assumed rate flagged for verification).*
8. FYI - line 26 should include the $1,150 PY overpayment (organizer PY column shows $950 - that is 2023). Medicare premiums
   reviewed for Schedule A - still standard.
""")
print("EVG1004 done", R.summary()["24"], v["refund"], "FTC", ftc_used, "cf", ftc_cf_total, "qcd_cost", qcd_cost)
