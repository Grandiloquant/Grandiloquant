"""EVG1007 - Dr. Aisha Rahman (Single, Illinois - Chicago). 100% owner of an S-corp pediatric practice (SSTB).
S-corp distributions exceed STOCK basis even though she has DEBT basis (shareholder loan) -> capital gain (Form 7203,
Form 8949/Sch D); IL PTE tax credit (not a Schedule A tax); 2% shareholder health insurance; QBI $0 (SSTB above range);
NIIT with sec. 1411(c)(4)-type exclusion of the excess-distribution gain; SALT cap phase-down (MAGI > $500k); DAF vs
GoFundMe vs used clothing FMV; IL refund tax-benefit rule; missed Q3 federal estimate -> Form 2210 penalty."""
from datetime import date

from common import ClientBuild, gotcha, fmt
from docs import statement, scanned_pages, write_text
import forms as F
from tax2025 import Return1040, r, schedule_tax

C = ClientBuild("EVG1007", "Rahman", "Dr. Aisha Rahman")
ADDR = ("2240 N Magnolia Ave", "Chicago, IL 60614")
T = {"name": "Aisha N. Rahman", "ssn": "XXX-XX-3057", "dob": "1981-11-02"}
REC_T = [T["name"], *ADDR, f"TIN: {T['ssn']}"]
CORP = "Lakeshore Pediatric Partners, S.C."
CORP_EIN = "00-4471822"
CORP_ADDR = ("1550 N Clybourn Ave Ste 300", "Chicago, IL 60642")

# ================================================================== facts / judgement calls
# W-2 from the S corp
SALARY, K401, SH_HEALTH = 240000.00, 23500.00, 8400.00        # 2% shareholder health premiums included in box 1 only
w2 = {"1": SALARY - K401 + SH_HEALTH, "2": 56000.00, "3": 176100.00, "4": 176100 * .062, "5": SALARY,
      "6": SALARY * .0145 + (SALARY - 200000) * .009,
      "12": [("D", K401)], "13": ["Retirement plan: X"], "14": [("2% SH HLTH", SH_HEALTH)],
      "state": [{"state": "IL", "id": "4471-8220", "wages": SALARY - K401 + SH_HEALTH, "tax": 10800.00}], "control": "LPP-0001"}
# K-1 (1120-S)
K1_ORD = 310000.00          # box 1, after the entity's deduction for the IL PTE tax
K1_INT = 640.00             # box 4
K1_CHAR = 2000.00           # box 12A (cash, 60%)
K1_NONDED = 3100.00         # box 16C (50% meals, penalties)
K1_DIST = 360000.00         # box 16D
PTE_TAX = r(.0495 * (K1_ORD + K1_INT - K1_CHAR) / (1 - .0495))   # IL PTE tax (entity base adds back the PTE tax itself)
ENTITY_W2, ENTITY_UBIA = 612000.00, 185000.00
# basis (Form 7203) - ordering per Reg. 1.1367-1(f): increases, distributions, nondeductible expenses, losses/deductions
STOCK_BEG, DEBT_BEG = 28000.00, 120000.00
stock_after_inc = STOCK_BEG + K1_ORD + K1_INT
EXCESS_DIST = max(0, K1_DIST - stock_after_inc)            # capital gain - LT (stock held since 2016)
stock_after_dist = max(0, stock_after_inc - K1_DIST)
# stock basis is zero -> nondeductible expenses and the charitable deduction reduce DEBT basis (not below zero)
debt_reduction = min(DEBT_BEG, K1_NONDED + K1_CHAR)
DEBT_END = DEBT_BEG - debt_reduction
STOCK_END = 0.0
# personal investments
INT_CHASE = 1850.00
DIV_ORD, DIV_QUAL = 2400.00, 2100.00
# itemized
IL_WH = w2["state"][0]["tax"]
IL_EST = [("04/15/2025", 2250.00), ("06/16/2025", 2250.00), ("09/15/2025", 2250.00), ("01/15/2026", 2250.00)]
IL_EST_PAID_2025 = sum(a for d, a in IL_EST if d.endswith("2025"))
PROP_TAX = [("03/03/2025", "2024 1st installment", 7980.00), ("12/15/2025", "2024 2nd installment", 6820.00)]
PROP_TAX_PAID = sum(a for _, _, a in PROP_TAX)
MORT_INT = 21600.00
DAF, GOFUNDME, CLOTHING_COST, CLOTHING_FMV = 25000.00, 1500.00, 600.00, 150.00
IL_REFUND_1099G = 2100.00
# federal estimates actually paid (IRS online account) vs client's statement (4 x 15,000)
FED_EST = [(date(2025, 4, 15), 15000.00), (date(2025, 6, 16), 15000.00), (date(2026, 1, 15), 15000.00)]
PY_TAX_2024 = 121500.00
PY_AGI_2024 = 508300.00

# ================================================================== PERM
C.write_profile(f"""
# EVG1007 - Rahman, Dr. Aisha  (PERM)

*Synthetic client - Project Evergreen training data.*

| Item | Detail |
|---|---|
| Client ID | EVG1007 |
| Taxpayer | Dr. Aisha N. Rahman, MD, DOB 11/02/1981, SSN XXX-XX-3057 - pediatrician |
| Address | {ADDR[0]}, {ADDR[1]} (Lincoln Park; Cook County) - owns home (purchased 2019); **Illinois full-year resident** |
| Filing status | Single, no dependents |
| Business | 100% shareholder of **{CORP}** (EIN {CORP_EIN}), IL service corporation, S election eff. 01/01/2016. Medical practice = **SSTB** (health). Materially participates (full-time). Entity return (1120-S / IL-1120-ST) prepared by Kessler & Park CPAs - K-1 received each March. |
| Entity elections | Corporation elects the **Illinois PTE tax** each year (since 2022). |
| Shareholder loan | Aisha lent the corporation $120,000 on 06/01/2021 (promissory note in PERM; 5% interest accrues, unpaid). **Debt basis** tracked separately from stock basis - see PY Form 7203. |
| Other | Fidelity taxable brokerage; Chase savings; Fidelity Charitable DAF opened 2025. |
| Contact | aisha.rahman@example.com (prefers email), (312) 555-0163. Practice manager for K-1 questions: Tom Brandt, (312) 555-0170. eSign OK. |
| Engagement | Client since 2021. Individual + K-1 tier ($2,400 quote). |
""")
F.prior_year_summary(C.perm_file("2024_Form_1040_Return_Summary.pdf", "Prior-year return summary"), "Dr. Aisha Rahman", "EVG1007",
    "Single", [
        ["1a", f"W-2 wages ({CORP})", 221300],
        ["2b / 3b", "Interest / ordinary dividends", 3900],
        ["Sch E", f"K-1 ordinary income - {CORP} (nonpassive)", 291400],
        ["Sch 1 17", "S corp 2% shareholder health insurance", 8300],
        ["11", "AGI", PY_AGI_2024],
        ["Sch A 5e", "State & local taxes paid $31,000 (IL income $16,400 + Cook County property $14,600) - LIMITED to $10,000 (2024 cap)", 10000],
        ["Sch A", "Mortgage interest $22,300; charitable $12,000", 34300],
        ["12", "Itemized deductions", 44300], ["13", "QBI deduction (SSTB, above phase-in range)", 0],
        ["15", "Taxable income", 464000], ["24", "Total tax", r(PY_TAX_2024)],
        ["26", "2024 estimated payments", 52000], ["37", "Amount owed with return", 11850]],
    carryovers=[["Stock basis 12/31/2024 (Form 7203)", STOCK_BEG], ["Debt basis 12/31/2024 (Form 7203)", DEBT_BEG],
                ["Capital loss carryover", 0], ["Charitable carryover", 0]],
    notes="PY WP: 2024 IL-1040 overpaid (entity PTE tax credit + estimates) - refund $2,100 expected in 2025; SALT was capped in 2024 "
          "so the refund will not be taxable (tax benefit rule - keep this worksheet). Stock basis is low because distributions "
          "have run close to income each year - watch for distributions in excess of STOCK basis (debt basis does not absorb "
          "distributions). 2026 planning: discussed a DAF 'bunching' contribution for 2025.")
statement(C.perm_file("2024_Form_7203_Shareholder_Basis.pdf", "PY Form 7203 (basis worksheet)"),
    f"Form 7203 (2024) - S Corporation Shareholder Stock and Debt Basis - {CORP}", [
        {"heading": "Part I - Shareholder Stock Basis (2024)", "table": [["Line", "Description", "Amount"],
            ["1", "Stock basis at beginning of year", 36600.00], ["3a", "Ordinary business income", 291400.00],
            ["3c", "Interest income", 520.00], ["5", "Stock basis before distributions", 328520.00],
            ["6", "Distributions (excluding dividend distributions)", 297000.00], ["7", "Stock basis after distributions", 31520.00],
            ["8a", "Nondeductible expenses", 2020.00], ["9", "Stock basis before loss and deduction items", 29500.00],
            ["10", "Allowable loss and deduction items (charitable)", 1500.00], ["15", "Stock basis at end of year", STOCK_BEG]],
         "left_align_cols": [0, 1]},
        {"heading": "Part II - Shareholder Debt Basis (2024)", "table": [["Debt", "Description", "Amount"],
            ["Debt 1", "Formal note 06/01/2021 - shareholder loan to corporation (5%, interest accrued unpaid)", "principal 120,000"],
            ["16", "Loan balance at beginning of year", 120000.00], ["20", "Debt basis at beginning of year", 120000.00],
            ["30", "Debt basis at end of year", DEBT_BEG], ["35", "Loan balance at end of year", 120000.00]], "left_align_cols": [0, 1]}])
statement(C.perm_file("Promissory_Note_Shareholder_Loan_2021.pdf", "Legal agreement (shareholder loan)"),
    "PROMISSORY NOTE", [
        {"para": [f"Principal amount: $120,000.00        Date: June 1, 2021        Chicago, Illinois",
                  f"FOR VALUE RECEIVED, {CORP}, an Illinois medical corporation (\"Borrower\"), promises to pay to the order of Aisha N. "
                  "Rahman (\"Lender\") the principal sum of One Hundred Twenty Thousand Dollars ($120,000.00), together with interest "
                  "on the unpaid principal at five percent (5%) per annum, compounded annually.",
                  "Principal and all accrued interest are due on demand, and in any event no later than June 1, 2031. Borrower may prepay "
                  "without penalty. This note is unsecured.",
                  "Purpose: purchase of clinical equipment and working capital for the Clybourn Avenue office build-out.",
                  f"BORROWER: {CORP}   By: /s/ Aisha N. Rahman, President      LENDER: /s/ Aisha N. Rahman"]}])

# ================================================================== PBC
EMP = {"name": CORP, "addr1": CORP_ADDR[0], "addr2": CORP_ADDR[1], "ein": CORP_EIN}
EE = {"name": T["name"], "addr1": ADDR[0], "addr2": ADDR[1], "ssn": T["ssn"]}
F.organizer(C.pbc_file("01_2025_Organizer_completed.pdf", "Client organizer", "2026-02-20"), "Dr. Aisha Rahman", "EVG1007",
    general=[("Did your marital status change during 2025?", "No", ""),
             ("Did you receive any Schedules K-1?", "Yes", "Lakeshore - Tom will send final K-1 in March"),
             ("Did you receive any Forms 1099-INT/DIV/B?", "Yes", "Chase, Fidelity"),
             ("Did you make estimated tax payments?", "Yes", "Federal 4 x $15,000; IL 4 x $2,250"),
             ("Did you receive a state tax refund?", "Yes", "IL refund $2,100 (1099-G)"),
             ("Did you make charitable contributions?", "Yes", "See list below"),
             ("Did you receive, sell, exchange digital assets?", "No", ""),
             ("Did you lend money to or receive repayment from your corporation?", "No", "No change - still $120k")],
    dependents=[],
    income_rows=[["Wages", CORP, 221300, "see W-2"],
                 ["Interest", "Chase Bank", 1480, "1,850"],
                 ["Dividends", "Fidelity", 1900, "see 1099"],
                 ["K-1 S corporation", CORP, 291400, "coming"],
                 ["State refund", "Illinois", 0, "2,100"]],
    deductions_rows=[["Estimated tax - federal", "1040-ES", 52000, "60,000 (4 x 15,000)"],
                     ["Estimated tax - Illinois", "IL-1040-ES", 8000, "9,000 (4 x 2,250)"],
                     ["Mortgage interest", "Wintrust Mortgage", 22300, "see 1098"],
                     ["Real estate tax", "Cook County", 14600, "14,800"],
                     ["Charitable - cash", "Fidelity Charitable (DAF)", 0, "25,000"],
                     ["Charitable - cash", "GoFundMe - Dr. Lee family (house fire)", 0, "1,500"],
                     ["Charitable - noncash", "Goodwill - 3 bags clothes (cost)", 400, "600"],
                     ["Charitable - cash", "Lurie Children's (PY)", 12000, ""]],
    signature_date="02/18/2026")
F.w2(C.pbc_file("02_W-2_Lakeshore_Pediatric_Partners.pdf", "Form W-2", "2026-02-20"), EMP, EE, w2)
F.f1099_int(C.pbc_file("03_1099-INT_Chase.pdf", "Form 1099-INT", "2026-02-20"),
            ["JPMorgan Chase Bank, N.A.", "PO Box 659754", "San Antonio, TX 78265", "TIN: 00-0000001"], REC_T, {"1": INT_CHASE}, account="****6620")
F.f1099_div(C.pbc_file("04_1099-DIV_Fidelity.pdf", "Form 1099-DIV", "2026-02-20"),
            ["Fidelity Brokerage Services LLC", "100 Salem St", "Smithfield, RI 02917", "TIN: 00-0000044"], REC_T,
            {"1a": DIV_ORD, "1b": DIV_QUAL}, account="Z71-448120")
F.f1098(C.pbc_file("05_1098_Wintrust_Mortgage.pdf", "Form 1098", "2026-02-20"),
        ["Wintrust Mortgage", "9700 W Higgins Rd Ste 300", "Rosemont, IL 60018", "TIN: 00-8811204"], REC_T,
        {"1": MORT_INT, "2": 598230.44, "3": "08/30/2019", "7": "Yes", "8": ADDR[0], "9": "1"})
statement(C.pbc_file("06_Cook_County_Property_Tax_Payments_2025.pdf", "Property tax bills / payment history", "2026-02-20"),
    "Cook County Treasurer - Payment History - PIN 14-32-118-022-0000 (2240 N Magnolia Ave)", [
        {"table": [["Paid on", "Tax year / installment", "Amount"]] + [[d, t, a] for d, t, a in PROP_TAX] +
                  [["Total paid in calendar 2025", "", PROP_TAX_PAID]], "total_row": True, "left_align_cols": [0, 1]}])
F.f1099_g(C.pbc_file("07_1099-G_Illinois_Refund.pdf", "Form 1099-G", "2026-02-20"),
          ["Illinois Department of Revenue", "PO Box 19044", "Springfield, IL 62794", "TIN: 00-6000001"], REC_T,
          {"2": IL_REFUND_1099G, "3": "2024"})
statement(C.pbc_file("08_MyTax_Illinois_Estimated_Payments.pdf", "State payment history", "2026-02-20"),
    "MyTax Illinois - Individual Income Tax - Estimated Payments - Tax Year 2025", [
        {"table": [["Payment date", "Type", "Amount", "Status"]] + [[d, "IL-1040-ES", a, "Posted"] for d, a in IL_EST]}])
statement(C.pbc_file("09_Fidelity_Charitable_Contribution_Acknowledgment.pdf", "Charity acknowledgment", "2026-02-20"),
    "Fidelity Charitable - Contribution Acknowledgment", [
        {"para": ["Dear Dr. Rahman,", "Thank you for your contribution to your Giving Account (Rahman Family Giving Fund, #G-2291044).",
                  "Date received: 12/12/2025.   Amount: $25,000.00 (cash, via ACH).",
                  "Fidelity Charitable is a public charity described in section 170(b)(1)(A)(vi). No goods or services were provided in "
                  "exchange for this contribution. Fidelity Charitable has exclusive legal control over the contributed assets.",
                  "Grant recommendations made from your Giving Account are not additional deductible contributions."]}])
write_text(C.pbc_file("10_GoFundMe_receipt_email.txt", "Email receipt", "2026-02-20", "Client email forward"),
"""From: GoFundMe <receipts@gofundme.example.com>
To: aisha.rahman@example.com
Date: Sat, 14 Jun 2025 09:12:44 -0500
Subject: Thank you for your donation to "Help the Lee Family Rebuild"

Hi Aisha, thank you for donating $1,500.00 to "Help the Lee Family Rebuild" organized by Karen Wu.
Beneficiary: Dr. Michael Lee and family (Evanston, IL).
Please note: Donations to personal fundraisers are generally not tax-deductible. This is not a tax receipt.

---- forwarded by Aisha: "can we deduct this? - A"
""")
scanned_pages(C.pbc_file("11_Goodwill_donation_receipt_photo.pdf", "Phone photo (image)", "2026-02-20"),
    [["GOODWILL INDUSTRIES OF METROPOLITAN CHICAGO",
      "Donation Receipt - Clybourn Ave Donation Center",
      "",
      "Date: 10/04/2025",
      "Donor: A. Rahman",
      "Items: [X] Clothing  3 bags   [ ] Household  [ ] Electronics",
      "Goodwill did not provide goods or services for this donation.",
      "Value of items to be determined by donor.",
      "",
      "(handwritten by client:)  women's work clothes, shoes, coats",
      "   paid ~$600 new, most 4-6 yrs old, good condition",
      "   thrift value?? - Goodwill site says ~$5-8/item x ~25 items"]], handwritten=False, seed=71, skew=1.7)
# draft K-1 (preliminary, superseded)
k1_entity = [["A - Corporation EIN", CORP_EIN], ["B - Name/address", f"{CORP}, {CORP_ADDR[0]}, {CORP_ADDR[1]}"],
             ["C - IRS Center", "e-file"], ["D - Shares outstanding BOY / EOY", "1,000 / 1,000"]]
k1_sh = [["E - Shareholder SSN", T["ssn"]], ["F - Name/address", f"{T['name']}, {ADDR[0]}, {ADDR[1]}"],
         ["G - Ownership % for tax year", "100%"], ["H - Shares BOY / EOY", "1,000 / 1,000"],
         ["I - Loans from shareholder BOY / EOY", "120,000 / 120,000"]]
F.k1_generic(C.pbc_file("12_DRAFT_K-1_1120-S_Lakeshore_(preliminary).pdf", "Schedule K-1 (draft)", "2026-02-20",
                        "Client email forward", "marked DRAFT by entity CPA"),
    "1120-S", CORP + " - DRAFT (subject to change)", k1_entity, k1_sh, [],
    [["1", "Ordinary business income (loss)", "", 326100.00], ["4", "Interest income", "", 640.00],
     ["12", "Charitable contributions", "A", 2000.00], ["16", "Items affecting shareholder basis - distributions", "D", 360000.00]],
    notes=["DRAFT - prepared 02/06/2026 before the 2025 IL PTE tax was finalized. Do not file. Final K-1 to follow."])
F.k1_generic(C.pbc_file("13_K-1_1120-S_Lakeshore_Pediatric_Partners_FINAL.pdf", "Schedule K-1 (1120-S) package", "2026-03-11",
                        "Email from entity CPA (Kessler & Park)"),
    "1120-S", CORP, k1_entity, k1_sh, [],
    [["1", "Ordinary business income (loss)", "", K1_ORD], ["4", "Interest income", "", K1_INT],
     ["12", "Charitable contributions (60% cash)", "A", K1_CHAR],
     ["16", "Nondeductible expenses", "C", K1_NONDED], ["16", "Distributions", "D", K1_DIST],
     ["17", "Section 199A information - see Statement A", "V", "STMT"]],
    supplemental=[
        {"heading": "Statement A - QBI Pass-through Entity Reporting (sec. 199A)",
         "table": [["Item", "Trade or business: Pediatric medical practice"], ["Specified service trade or business (SSTB)?", "YES - health"],
                   ["QBI - ordinary business income", K1_ORD], ["W-2 wages", ENTITY_W2], ["UBIA of qualified property", ENTITY_UBIA]],
         "left_align_cols": [0]},
        {"heading": "Illinois Schedule K-1-P (2025) - Shareholder's share",
         "table": [["Item", "Amount"], ["Share of IL base income (apportionment 100%)", K1_ORD + K1_INT],
                   ["Pass-through entity tax credit (PTE tax paid by the corporation, 35 ILCS 5/201(p))", PTE_TAX],
                   ["Replacement tax (1.5%) - paid by corporation, not a shareholder credit", "n/a"]], "left_align_cols": [0]},
        {"heading": "Shareholder basis",
         "para": "The corporation does not track shareholder stock or debt basis. Shareholders must attach Form 7203 when "
                 "receiving a distribution. Shareholder loan balance per corporate books 12/31/2025: $120,000 principal "
                 "(accrued interest payable $26,153 not paid)."}],
    notes=["Ordinary income is net of the corporation's deduction for the 2025 Illinois pass-through entity tax."])
statement(C.pbc_file("14_Fidelity_401k_2025_Year-End_Statement.pdf", "Retirement plan statement", "2026-03-02"),
    f"Fidelity NetBenefits - {CORP} 401(k) Plan - Year-End Statement 12/31/2025", [
        {"table": [["Item", "Amount"], ["Beginning balance 01/01/2025", 612440.18], ["Employee deferrals (pre-tax)", K401],
                   ["Employer profit-sharing (entity deduction)", 46500.00], ["Dividends / capital gains reinvested", 21904.66],
                   ["Change in market value", 48110.02], ["Ending balance 12/31/2025", 752454.86]], "left_align_cols": [0]},
        {"para": "Earnings inside the plan are tax-deferred and are not reported on your individual return."}])
write_text(C.pbc_file("15_Email_Aisha_estimates_2026-03-18.txt", "Client correspondence", "2026-03-18", "Email"),
"""From: preparer@evergreentax.example
To: Aisha Rahman <aisha.rahman@example.com>
Date: Wed, 18 Mar 2026 10:21:00 -0500
Subject: Rahman 2025 - estimated payments

Dr. Rahman - the organizer shows four federal estimates of $15,000. Could you download your payment history from
your IRS online account (irs.gov/account > Payments) so we can match dates to the return? A missing payment is a
common e-file / notice issue.

-----
From: Aisha Rahman
Date: Fri, 20 Mar 2026 22:04:51 -0500
Subject: RE: Rahman 2025 - estimated payments

Attached. I thought I did all four through Direct Pay - I was at a conference in September, maybe I missed it?
""")
statement(C.pbc_file("16_IRS_Online_Account_Payment_History.pdf", "IRS online account printout", "2026-03-20", "Client email attachment"),
    "IRS Online Account - Payment Activity - Tax Year 2025 (Form 1040)", [
        {"table": [["Payment date", "Method", "Type", "Amount", "Status"]] +
                  [[d.strftime("%m/%d/%Y"), "Direct Pay", "Estimated tax (1040ES)", a, "Completed"] for d, a in FED_EST],
         "left_align_cols": [0, 1, 2]},
        {"para": "No other payments are posted for tax year 2025."}])

# ================================================================== RETURN
SALT_PAID = IL_WH + IL_EST_PAID_2025 + PROP_TAX_PAID
itemized = {"state_income_tax": IL_WH + IL_EST_PAID_2025, "real_estate_tax": PROP_TAX_PAID,
            "mortgage_interest_1098": MORT_INT, "charity_cash": DAF + K1_CHAR, "charity_noncash": CLOTHING_FMV}
nii_items = INT_CHASE + K1_INT + DIV_ORD           # line 8 after the line 5c adjustment removes the excess-distribution gain
facts = {
    "status": "S", "taxpayer": {"age65": False},
    "w2": [{"who": "T", "box1": w2["1"], "box2": w2["2"], "box3": w2["3"], "box4": w2["4"], "box5": w2["5"], "box6": w2["6"]}],
    "interest": [{"payer": "JPMorgan Chase Bank", "amount": INT_CHASE}, {"payer": f"{CORP} (Schedule K-1 box 4)", "amount": K1_INT}],
    "dividends": [{"payer": "Fidelity Brokerage Services", "ordinary": DIV_ORD, "qualified": DIV_QUAL}],
    "trades": [{"box": "F", "id": "1", "desc": f"{CORP} - S corp distribution in excess of stock basis (sec. 1368(b)(2); Form 7203)",
                "acq": "01/01/2016", "sold": "12/31/2025", "proceeds": EXCESS_DIST, "basis": 0}],
    "sch1": {"sch_e": K1_ORD},
    "adjustments": {"se_health": SH_HEALTH},
    "itemized": itemized,
    "qbi": {"businesses": [{"name": CORP, "qbi": K1_ORD, "w2_wages": ENTITY_W2, "ubia": ENTITY_UBIA, "sstb": True}]},
    "niit": {"nii": nii_items, "gross": nii_items},
    "estimated_payments": sum(a for _, a in FED_EST),
}
R0 = Return1040(facts).compute()           # pass 1 - tax before the 2210 penalty


def form_2210(total_tax_for_2210, withholding, payments, py_tax, rate=.07):
    """Form 2210 regular method (Part IV). Withholding treated as paid 25% on each due date. Payments applied to the
    earliest unpaid required installment. Single rate assumed for every period. Returns (penalty, detail rows)."""
    due = [date(2025, 4, 15), date(2025, 6, 16), date(2025, 9, 15), date(2026, 1, 15)]
    rap = min(.90 * total_tax_for_2210, 1.10 * py_tax)
    inst = rap / 4
    pays = sorted([(d, withholding / 4) for d in due] + list(payments))
    open_u = []   # [due_date, amount]
    rows = []
    pen = 0.0
    credit = 0.0
    pi = 0
    end = date(2026, 4, 15)

    def apply(amount, on):
        nonlocal pen
        while amount > 0.005 and open_u:
            dd, amt = open_u[0]
            use = min(amt, amount)
            p = use * rate * (on - dd).days / 365
            pen += p
            rows.append([f"Underpayment due {dd:%m/%d/%Y} of {use:,.2f} paid {on:%m/%d/%Y}", (on - dd).days, round(p, 2)])
            open_u[0][1] -= use
            amount -= use
            if open_u[0][1] <= 0.005:
                open_u.pop(0)
        return amount
    for dd in due:
        while pi < len(pays) and pays[pi][0] <= dd:
            left = apply(pays[pi][1], pays[pi][0])
            credit += left
            pi += 1
        use = min(credit, inst)
        credit -= use
        short = inst - use
        if short > 0.005:
            open_u.append([dd, short])
    while pi < len(pays):
        apply(pays[pi][1], pays[pi][0])
        pi += 1
    for dd, amt in list(open_u):
        p = amt * rate * (end - dd).days / 365
        pen += p
        rows.append([f"Underpayment due {dd:%m/%d/%Y} of {amt:,.2f} paid with return 04/15/2026", (end - dd).days, round(p, 2)])
    return r(pen), rap, inst, rows


TAX_FOR_2210 = R0.values["24"]              # no refundable credits
PEN, RAP, INST, PEN_ROWS = form_2210(TAX_FOR_2210, R0.values["25d"], FED_EST, PY_TAX_2024)
R = Return1040(dict(facts, es_penalty=PEN)).compute()
v = R.values
assert v["deduction_type"].startswith("Itemized")
# AMT check (not owed)
R_amt = Return1040(dict(facts, amt={"other": 0})).compute()
AMT_TMT = R_amt.values["amt_tmt"]
assert R_amt.forms_value("Form 6251", "11") == 0

# ---------------- Illinois
IL_BASE = v["11"]                            # no additions/subtractions (PTE income already in federal AGI)
IL_EXEMPT = 0 if v["11"] > 250000 else 2850
IL_NET = IL_BASE - IL_EXEMPT
IL_TAX = r(IL_NET * .0495)
IL_PAY = IL_WH + sum(a for _, a in IL_EST)
IL_OVER = r(PTE_TAX + IL_PAY - IL_TAX)
state = [{"title": "Illinois Form IL-1040 (2025) - full-year resident",
          "lines": [("1", "Federal adjusted gross income", v["11"]),
                    ("", "Additions / subtractions (PTE income is already in federal AGI; no US-obligation interest)", 0),
                    ("9", "Illinois base income", IL_BASE),
                    ("10", "Exemption allowance ($2,850 - not allowed: federal AGI > $250,000)", IL_EXEMPT),
                    ("11", "Net income", IL_NET), ("12", "Income tax (4.95%)", IL_TAX),
                    ("", "Illinois property tax credit (5% of property tax) - NOT allowed: federal AGI > $250,000", 0),
                    ("", f"Pass-through entity tax credit - Schedule K-1-P from {CORP}", PTE_TAX),
                    ("", "Illinois income tax withheld (W-2 box 17)", r(IL_WH)),
                    ("", "Estimated payments (4 x $2,250, incl. 01/15/2026)", r(sum(a for _, a in IL_EST))),
                    ("", "Total payments and refundable credits", PTE_TAX + r(IL_PAY)),
                    ("", "Overpayment - refund (direct deposit)", IL_OVER)],
          "note": "Chicago has no municipal income tax. The 2025 IL refund will be a 2026 Form 1099-G item: only the part that "
                  "produced a 2025 federal tax benefit is taxable in 2026 (SALT was capped in 2025) - see preparer notes."}]

# ---------------- attachments
f7203 = [["Form 7203 (2025) - " + CORP + " (EIN " + CORP_EIN + ")", "Amount"],
         ["Part I line 1 - Stock basis at beginning of year", r(STOCK_BEG)],
         ["3a Ordinary business income", r(K1_ORD)], ["3c Interest income", r(K1_INT)],
         ["5 Stock basis before distributions", r(stock_after_inc)],
         ["6 Distributions (K-1 box 16D)", r(K1_DIST)],
         ["7 Stock basis after distributions (not below zero)", 0],
         ["Distributions in excess of stock basis -> capital gain (Form 8949 Part II box F, LT - held since 2016)", r(EXCESS_DIST)],
         ["8a Nondeductible expenses (box 16C) - stock basis is zero -> reduce DEBT basis", 0],
         ["15 Stock basis at end of year", 0],
         ["Part II line 20 - Debt basis at beginning of year (formal note 06/01/2021)", r(DEBT_BEG)],
         ["Debt basis is NOT reduced by distributions; it absorbs only losses/deductions and nondeductible expenses", ""],
         ["Nondeductible expenses 3,100 + charitable deduction 2,000 applied against debt basis", -r(debt_reduction)],
         ["30 Debt basis at end of year (restored first by future net increases)", r(DEBT_END)],
         ["35 Loan balance at end of year (no repayment -> no gain on repayment)", 120000],
         ["Part III - all K-1 loss/deduction items allowed (charitable 2,000 allowed via debt basis)", r(K1_CHAR)]]
f8960 = [["Form 8960 - Net investment income tax", "Amount"],
         ["1 Taxable interest (Chase 1,850 + K-1 box 4 640)", r(INT_CHASE + K1_INT)],
         ["2 Ordinary dividends", r(DIV_ORD)],
         ["4a/4b K-1 ordinary income - nonpassive trade or business (material participation) - excluded", 0],
         ["5a Net gain (Schedule D) - excess S-corp distribution", r(EXCESS_DIST)],
         ["5c Adjustment - gain attributable to S-corp stock of a nonpassive active trade or business (sec. 1411(c)(4); "
          "Prop. Reg. 1.1411-7 - all corporate assets used in the practice)", -r(EXCESS_DIST)],
         ["8 Total investment income", r(nii_items)],
         ["12 Net investment income", r(nii_items)],
         ["13-16 MAGI " + f"{v['11']:,}" + " less threshold 200,000", v["11"] - 200000],
         ["17 NIIT 3.8% x smaller of line 12 or line 16", v.get("niit", 0)],
         ["Alternative (if gain treated as NII): additional NIIT", r(EXCESS_DIST * .038)]]
tbr = [["State refund worksheet (tax benefit rule, Rev. Rul. 2019-11) - 2024 IL refund $2,100", "Amount"],
       ["2024 state & local taxes paid (IL income 16,400 + property 14,600)", 31000],
       ["2024 SALT deduction allowed (cap)", 10000],
       ["Taxes paid less refund (31,000 - 2,100)", 28900],
       ["SALT that would have been allowed had only 28,900 been paid (still capped)", 10000],
       ["Tax benefit from the overpaid tax (10,000 - 10,000)", 0],
       ["Taxable refund - Schedule 1 line 1", 0]]
sa_detail = [["Schedule A support", "Amount"],
             ["5a State income tax: IL withholding 10,800 + IL estimates paid in 2025 (04/15, 06/16, 09/15) 6,750. "
              "01/15/2026 payment is a 2026 deduction. IL PTE tax is NOT included (deducted by the corporation).", r(IL_WH + IL_EST_PAID_2025)],
             ["5b Real estate tax paid in 2025 (Cook County)", r(PROP_TAX_PAID)],
             ["5d Total state & local taxes", r(SALT_PAID)],
             [f"5e SALT limit: 40,000 - 30% x (MAGI {v['11']:,} - 500,000) = {v['salt_cap_applied']:,} (floor 10,000)", v["salt_cap_applied"]],
             ["8a Mortgage interest (Wintrust 1098; acquisition debt < $750,000)", r(MORT_INT)],
             ["11 Cash: Fidelity Charitable DAF 25,000 (written acknowledgment) + K-1 box 12A 2,000", r(DAF + K1_CHAR)],
             ["GoFundMe 'Help the Lee Family Rebuild' $1,500 - gift to individuals, NOT deductible", 0],
             ["12 Noncash: used clothing, FMV (thrift value ~25 items x $6) - under $500, no Form 8283", r(CLOTHING_FMV)],
             ["Note: 2026+ itemized deductions are subject to the OBBBA 2/37 limitation and 0.5%-of-AGI charitable floor - not 2025", ""]]
p2210 = [["Form 2210 - regular method (Part IV) - Short Method not allowed (payments not all timely/equal)", "Days", "Penalty"],
         [f"2025 tax for 2210 {TAX_FOR_2210:,} x 90% = {r(.9 * TAX_FOR_2210):,}; 2024 tax {r(PY_TAX_2024):,} x 110% (AGI > $150k) = "
          f"{r(1.1 * PY_TAX_2024):,}; required annual payment {r(RAP):,}; each installment {INST:,.2f}", "", ""],
         [f"Withholding {v['25d']:,} (incl. 8959 line 24) treated as paid 1/4 on each due date; estimates paid 04/15/2025, 06/16/2025, "
          "01/15/2026 (Q3 09/15/2025 NOT paid)", "", ""]] + PEN_ROWS + \
        [["Rate assumed 7% per year for all periods (IRS underpayment rate 2025 Q1-Q4 and 2026 Q1)", "", ""],
         ["Penalty (Form 1040 line 38)", "", PEN]]
qbi_note = ("QBI: " + CORP + " is a specified service trade or business (health). Taxable income before QBI " +
            f"{v['11'] - v['12e']:,}" + " exceeds the $247,300 top of the 2025 phase-in range ($197,300 + $50,000), so the "
            "applicable percentage is 0% and the QBI deduction is $0 (Form 8995-A Schedule A).")
seh = [["Self-employed health insurance - 2% S corporation shareholder (Form 7206)", "Amount"],
       ["Premiums paid by the S corp and included in W-2 box 1 (box 14 '2% SH HLTH'); not in boxes 3/5", r(SH_HEALTH)],
       ["Limit: W-2 wages from the S corporation", r(w2["1"])],
       ["Not eligible for any other subsidized employer plan (single; the S corp plan is her own)", ""],
       ["Schedule 1 line 17", r(SH_HEALTH)]]
C.write_return(R, [
    ("Taxpayer", "Dr. Aisha N. Rahman (XXX-XX-3057)"), ("Address", ", ".join(ADDR)), ("Filing status", "Single"),
    ("Digital assets question", "No"),
    ("Forms included", "1040, Sch 1, Sch 2, Sch A, Sch B, Sch D, Form 8949, Sch E (Part II), Form 7203, Form 8959, Form 8960, "
                       "Form 8995-A, Form 7206, Form 2210, IL-1040 with Schedule K-1-P credit"),
    ("K-1", f"{CORP} (EIN {CORP_EIN}) - nonpassive, SSTB, Form 7203 attached"),
    ("State", "Illinois IL-1040 (resident)"),
    ("Filing method", "E-file 04/13/2026 (Form 8879 signed 04/11/2026). Balance due by direct debit 04/15/2026 (Chase ****6620); IL refund direct deposit"),
], state_summary=state, attachments=[("Form 7203 - S corporation shareholder stock and debt basis", f7203),
                                     ("Form 8960 detail", f8960), ("Schedule A detail", sa_detail),
                                     ("State refund - tax benefit rule worksheet", tbr),
                                     ("Form 2210 - underpayment of estimated tax penalty", p2210),
                                     ("Form 7206 - SE health insurance (2% shareholder)", seh),
                                     ("Form 8995-A statement", qbi_note)])

# ---------------- answer key
tax_16_exact = v["16"]
gotchas = [
    gotcha("EVG1007-G1", "Schedules K-1 - Debt Basis vs Stock Basis Distribution Trap", "Distributions exceed STOCK basis; debt basis is positive",
           f"Look at total basis (stock {fmt(stock_after_inc)} + debt {fmt(DEBT_BEG)}) and treat the {fmt(K1_DIST)} distribution as tax-free.",
           f"Distributions reduce stock basis only. Stock basis before distributions {fmt(stock_after_inc)} -> {fmt(EXCESS_DIST)} "
           "is gain from the sale of stock (sec. 1368(b)(2)) - Form 8949 Part II box F, long-term; Form 7203 attached. Debt basis "
           f"absorbs only the nondeductible expenses/charitable items (debt basis EOY {fmt(DEBT_END)}).",
           f"Sch D +{fmt(EXCESS_DIST)} LTCG (~{fmt(EXCESS_DIST * .15)} tax)", ["7", "Sch D", "Form 8949", "Form 7203"], "hard"),
    gotcha("EVG1007-G2", "Schedules K-1 - PTE tax credit", "IL PTE tax on the K-1-P",
           f"Add the {fmt(PTE_TAX)} PTE tax paid by the corporation to Schedule A line 5a as state income tax, and/or ignore the IL credit.",
           "The PTE tax was deducted by the corporation (ordinary income is already net of it) - it is not the shareholder's "
           f"itemized tax. Claim the {fmt(PTE_TAX)} credit on the IL-1040 (Schedule K-1-P); no IL subtraction.",
           "Sch A overstated / IL refund understated", ["Sch A 5a", "IL-1040"], "medium"),
    gotcha("EVG1007-G3", "Schedule A - itemizing SALT (refund of taxes itemized in the prior year)", "1099-G $2,100 IL refund",
           "Report the $2,100 on Schedule 1 line 1 because she itemized in 2024.",
           "2024 SALT was capped at $10,000 with $31,000 paid; without the overpayment she would still have been capped -> no tax "
           "benefit -> $0 taxable (tax benefit rule, Rev. Rul. 2019-11). Keep the worksheet.", "Line 8 +$2,100 if wrong", ["Sch 1 1"], "medium"),
    gotcha("EVG1007-G4", "Schedule A - SALT cap (OBBBA phase-down)", "MAGI above $500,000",
           f"Deduct the full $40,000 cap (or {fmt(SALT_PAID)} paid), and include the 01/15/2026 IL estimate.",
           f"Cap = 40,000 - 30% x ({fmt(v['11'])} - 500,000) = {fmt(v['salt_cap_applied'])}. Only IL payments made in 2025 count "
           f"(withholding + 3 estimates); total paid {fmt(SALT_PAID)} -> limited to {fmt(v['salt_cap_applied'])}.",
           f"Sch A line 5e {fmt(v['salt_cap_applied'])}", ["Sch A 5e", "12e"], "medium"),
    gotcha("EVG1007-G5", "Schedule A - Charitable Contributions (DAF vs GoFundMe; noncash clothing)", "Three kinds of 'donations'",
           f"Deduct GoFundMe $1,500 and value clothing at 3x cost per the procedure ($1,800) or at cost ($600).",
           f"DAF $25,000 deductible in 2025 (public charity, written acknowledgment). GoFundMe for a colleague's family is a gift to "
           f"individuals - not deductible. Used clothing is limited to FMV (thrift value) ~{fmt(CLOTHING_FMV)} - the procedure's 3x-cost "
           "rule conflicts with sec. 170 (FMV of used clothing cannot exceed its cost) and is not followed.",
           "Sch A line 11/12 overstated $3,150 if wrong", ["Sch A 11", "Sch A 12"], "easy"),
    gotcha("EVG1007-G6", "Review - Hand-off / estimated payments (organizer vs. confirmation)", "Organizer says 4 x $15,000 federal estimates",
           "Enter $60,000 on line 26 from the organizer -> understated balance due, IRS math-error notice, no 2210.",
           f"IRS account shows 3 payments ($45,000; Q3 missed). Line 26 = $45,000. 90% of 2025 tax < 110% of 2024 tax -> required "
           f"annual payment {fmt(RAP)}; Form 2210 regular method penalty {fmt(PEN)} (line 38).",
           f"Balance due {fmt(v['balance_due'])} (not {fmt(v['balance_due'] - 15000 - PEN)})", ["26", "37", "38"], "medium"),
    gotcha("EVG1007-G7", "QBI (limitations) - SSTB", "Medical practice S corp with $612k of W-2 wages",
           "Claim 20% x $310,000 = $62,000 because the W-2 wage limit is met.",
           "Health is an SSTB; taxable income before QBI is above $247,300 (single) -> applicable percentage 0% -> QBI deduction $0.",
           "Line 13a $0", ["13a"], "easy"),
    gotcha("EVG1007-G8", "NIIT", "Excess-distribution gain and K-1 income on Form 8960",
           f"Include the K-1 ordinary income and/or the {fmt(EXCESS_DIST)} excess-distribution gain in NII.",
           "K-1 income is nonpassive trade/business income (material participation) - not NII. The excess-distribution gain is "
           "treated as gain on S-corp stock and removed on line 5c to the extent attributable to the active business (sec. 1411(c)(4), "
           f"Prop. Reg. 1.1411-7; all corporate assets used in the practice). NII = interest + dividends {fmt(nii_items)} -> NIIT {fmt(v.get('niit', 0))}.",
           f"NIIT {fmt(v.get('niit', 0))} (vs {fmt(v.get('niit', 0) + r(EXCESS_DIST * .038))} if gain included)", ["Sch 2 12", "Form 8960"], "hard"),
    gotcha("EVG1007-G9", "Scan - duplicate documents (draft vs final K-1)", "DRAFT K-1 received before the final",
           "Autoflow both K-1s, or use the draft ($326,100 box 1 - before the PTE tax deduction).",
           f"Use only the FINAL K-1 (box 1 {fmt(K1_ORD)}); bookmark the draft as superseded.", "Sch E overstated $16,100 or doubled", ["Sch E", "Sch 1 5"], "easy"),
]
C.write_answer_key(R, {"residence": "IL (Chicago) - full-year resident", "complexity": "S-corp owner, K-1 basis, high income"}, gotchas,
    state=[{"return": "IL-1040", "base_income": IL_BASE, "exemption": IL_EXEMPT, "tax": IL_TAX, "pte_credit": PTE_TAX,
            "withholding": r(IL_WH), "estimates": r(sum(a for _, a in IL_EST)), "refund": IL_OVER}],
    filings=[{"form": "Form 1040", "method": "e-file", "due": "2026-04-15", "filed": "2026-04-13"},
             {"form": "IL-1040", "method": "e-file", "due": "2026-04-15", "filed": "2026-04-13"}],
    extra={"form_7203": {"stock_basis_boy": STOCK_BEG, "stock_before_distributions": stock_after_inc, "distributions": K1_DIST,
                         "excess_distribution_gain": EXCESS_DIST, "stock_basis_eoy": STOCK_END, "debt_basis_boy": DEBT_BEG,
                         "debt_basis_eoy": DEBT_END},
           "form_2210": {"required_annual_payment": r(RAP), "penalty": PEN, "rate_assumed": 0.07},
           "amt_check": {"tentative_minimum_tax": AMT_TMT, "regular_tax": v["16"], "amt": 0}})
C.write_receipt_log("EVG1007-1040-2025", "M. Novak (staff)", "L. Chen (senior)", "S. Kennedy, CPA", "2026-02-20")

# ---------------- notes
naive_bal = v["balance_due"] - 15000 - PEN
il_refund_benefit = max(0, r(v["salt_cap_applied"] - (SALT_PAID - IL_OVER)))
C.write_notes(f"""
# EVG1007 - Rahman, Dr. Aisha - 2025 Form 1040 / IL-1040 - Preparer Notes

*Synthetic client - Project Evergreen. Return status: **signed off, e-filed 04/13/2026 (federal + IL), accepted.***

## Return summary
| | |
|---|---|
| Filing status | Single |
| AGI (line 11) | {fmt(v['11'])} |
| Deduction | Itemized {fmt(v['12e'])} |
| QBI deduction | $0 (SSTB above phase-in range) |
| Taxable income | {fmt(v['15'])} |
| Income tax (line 16) | {fmt(v['16'])} |
| NIIT / Additional Medicare | {fmt(v.get('niit', 0))} / {fmt(R.forms_value('Form 8959', '7/13'))} (Addl Medicare fully withheld by employer - credit on line 25c) |
| Total tax | {fmt(v['24'])} |
| Payments | withholding {fmt(v['25d'])} + estimates {fmt(v['26'])} |
| Form 2210 penalty (line 38) | {fmt(PEN)} |
| **Balance due** | **{fmt(v['balance_due'])}** (direct debit 04/15/2026) |
| Illinois | tax {fmt(IL_TAX)}; PTE credit {fmt(PTE_TAX)} + payments {fmt(r(IL_PAY))} -> **refund {fmt(IL_OVER)}** |

## What I did and why (plain English)
1. **K-1 - use the final.** Tom sent a DRAFT K-1 in February (box 1 $326,100, before the IL PTE tax was booked). The final K-1
   (03/11) shows box 1 {fmt(K1_ORD)} - net of the corporation's PTE tax deduction. Draft bookmarked "superseded".
2. **Distributions vs stock basis (Form 7203).** Beginning stock basis was only {fmt(STOCK_BEG)} (PY 7203). Add 2025 income
   ({fmt(K1_ORD)} + {fmt(K1_INT)} interest) = {fmt(stock_after_inc)} available for distributions. She took {fmt(K1_DIST)}, so
   **{fmt(EXCESS_DIST)} is taxable as long-term capital gain** (stock held since 2016) on Form 8949 Part II (box F - no 1099-B).
   Her $120,000 shareholder loan gives her **debt basis, but debt basis never covers distributions** - it only absorbs losses and
   deductions. This is exactly the "debt vs stock basis" trap in our procedure: in Axcess the K-1 basis section must have stock and
   debt entered separately (stock basis line 2 = {fmt(STOCK_BEG)}; debt basis section = 120,000) or the software nets them and lets
   the distribution through tax-free. After the distribution, the nondeductible expenses ({fmt(K1_NONDED)}) and the charitable item
   ({fmt(K1_CHAR)}) reduce debt basis to {fmt(DEBT_END)}; future net income restores debt basis first. The loan was not repaid, so no
   gain on repayment. Advised Aisha: in 2026 keep distributions below stock basis (or repay part of the loan instead) - we will
   send the practice manager a mid-year basis estimate.
3. **QBI = $0.** Pediatrics is a health SSTB; taxable income before QBI ({fmt(v['11'] - v['12e'])}) is above $247,300, so none of
   the K-1 income qualifies even though the W-2 wage limit would be met.
4. **Health insurance.** The S corp paid her $8,400 of health premiums and correctly put them in W-2 box 1 (not boxes 3/5) -
   deducted on Schedule 1 line 17 (Form 7206). Not eligible for any other subsidized plan.
5. **NIIT.** K-1 ordinary income is from a business she materially participates in - not investment income. For the
   excess-distribution gain I followed the sec. 1411(c)(4) approach (proposed Reg. 1.1411-7, which taxpayers may rely on): the gain
   on S-corp stock is excluded to the extent the corporation's assets are used in a nonpassive trade or business (here 100%), shown as
   a line 5c adjustment. NII is just interest and dividends ({fmt(nii_items)}) -> NIIT {fmt(v.get('niit', 0))}. (If the gain were treated
   as NII the NIIT would be {fmt(r(EXCESS_DIST * .038))} higher - flagged for the signer; we consider our position well supported.)
6. **Additional Medicare.** Medicare wages {fmt(r(w2['5']))} -> 0.9% x $40,000 = $360; the corporation withheld exactly $360, which is
   claimed back on line 25c - net zero.
7. **Schedule A.**
   - *SALT:* IL withholding {fmt(r(IL_WH))} + IL estimates **paid in 2025** {fmt(r(IL_EST_PAID_2025))} (the 01/15/2026 payment is a 2026
     deduction) + Cook County property tax paid in 2025 {fmt(r(PROP_TAX_PAID))} = {fmt(r(SALT_PAID))}. MAGI is over $500,000, so the new
     $40,000 cap shrinks by 30% of the excess: 40,000 - 30% x {fmt(v['11'] - 500000)} = **{fmt(v['salt_cap_applied'])}**. The PTE tax
     the corporation paid is *not* hers to itemize - it is already deducted inside the K-1 and is claimed as a credit in Illinois.
   - *Mortgage interest* {fmt(r(MORT_INT))} (Wintrust; balance under $750k).
   - *Charity:* the $25,000 Fidelity Charitable DAF gift counts in 2025 (the year given, not when grants go out) + the K-1 box 12A
     {fmt(r(K1_CHAR))}. The $1,500 GoFundMe for Dr. Lee's family is a gift to individuals - **not deductible** (told Aisha). Used clothing:
     our procedure says to use 3x cost, but the law limits used clothing to its fair market (thrift) value, which can't exceed what she
     paid; Goodwill's guide gives ~$6 per item x ~25 items = **{fmt(CLOTHING_FMV)}**. I did not follow the 3x rule (would have been $1,800).
8. **IL refund 1099-G $2,100 - not taxable.** In 2024 she paid $31,000 of state/local taxes and could only deduct $10,000. Even without
   the $2,100 overpayment she would still have hit the cap, so the refund gave no tax benefit (Rev. Rul. 2019-11) -> $0 on Schedule 1.
9. **Estimated payments - only three were made.** The organizer says 4 x $15,000, but her IRS online account shows no September
   payment. Line 26 = {fmt(v['26'])}. She did not meet a safe harbor (90% of 2025 tax = {fmt(r(.9 * TAX_FOR_2210))}; 110% of 2024 tax =
   {fmt(r(1.1 * PY_TAX_2024))}; paid {fmt(v['25d'] + v['26'])}), so I computed the Form 2210 penalty (regular method, 7% rate assumed for
   every period) = **{fmt(PEN)}** and included it on line 38 rather than waiting for an IRS bill.
10. **AMT check.** Tentative minimum tax {fmt(AMT_TMT)} < regular tax {fmt(v['16'])} -> no AMT (Form 6251 not required).
11. **Illinois.** Base income = federal AGI {fmt(IL_BASE)} (no subtraction for the S-corp income; the PTE tax add-back happens at the
    entity). No exemption and no 5% property-tax credit because AGI is over $250,000. Tax {fmt(IL_TAX)} less PTE credit {fmt(PTE_TAX)},
    withholding and 4 estimates -> refund {fmt(IL_OVER)}.

## Open items / advice
- 2026 federal estimates: 110% of 2025 tax = {fmt(r(1.1 * v['24']))} -> {fmt(r(1.1 * v['24'] / 4 / 100) * 100)} per quarter (less
  withholding). Suggested increasing W-2 withholding from the S corp instead (withholding counts as paid evenly).
- 2026 note for next year's preparer: the 2025 IL refund ({fmt(IL_OVER)}) will be taxable on the 2026 return only to the extent it
  produced a 2025 benefit - 2025 SALT paid {fmt(r(SALT_PAID))} less refund = {fmt(r(SALT_PAID - IL_OVER))} vs 2025 cap
  {fmt(v['salt_cap_applied'])} -> about {fmt(il_refund_benefit)} taxable.
- Form 706/estate items: n/a. Portability n/a. Consider repaying part of the shareholder loan in 2026 (tax-free return of debt basis
  only to the extent of remaining debt basis {fmt(DEBT_END)} - the rest would be gain) - coordinate with Kessler & Park.

## Hand-off to signer / routing
- [x] Return locked; Accountant's copy saved as *reviewed*
- [x] Federal 1040 - e-file; IL-1040 - e-file; no FBAR
- [x] Due date 04/15/2026 (no extension); balance due by direct debit 04/15/2026 incl. 2210 penalty
- [x] eSign (Form 8879 / IL-8453) - email preferred
- [x] Special: signer to review NIIT line 5c position (item 5)
- Billing: K-1 tier $2,400 + 1.0 hr Form 7203/basis + 0.5 hr 2210 = standard rates; nothing to W/O.
""")
C.write_review_points(f"""
# Review Points - EVG1007 - 2025 - Form 1040

*Reviewer: L. Chen (blue). Preparer responses in red. Synthetic.*

1. **WP 12/13 - K-1s** - Autoflow picked up both the DRAFT and FINAL K-1 (Sch E showed $636,100). Use the final only.
   - *Preparer: Draft bookmarked superseded; Sch E {fmt(K1_ORD)}.*
2. **K-1 basis / Form 7203** - Draft return showed no gain on the $360,000 distribution. Axcess netted stock + debt basis (blended).
   - Split: stock basis line 2 {fmt(STOCK_BEG)}; debt basis entered separately (note 06/01/2021). Distributions only reduce stock basis.
   - *Preparer: Done - {fmt(EXCESS_DIST)} LTCG on 8949 box F; Form 7203 attached; debt basis EOY {fmt(DEBT_END)}.*
3. **Sch A line 5a** - Draft included the IL PTE tax ({fmt(PTE_TAX)}) and the 01/15/2026 IL estimate. Neither belongs in 2025 Sch A.
   - *Preparer: Removed. Sch A 5a = withholding + 3 estimates paid in 2025.*
4. **Sch A line 5e** - Cap shown at $40,000. MAGI > $500k - apply the 30% phase-down.
   - *Preparer: Cap {fmt(v['salt_cap_applied'])}.*
5. **Sch 1 line 1** - Draft picked up the $2,100 1099-G. PY SALT was capped - run the tax benefit worksheet.
   - *Preparer: Worksheet shows $0 benefit; removed and worksheet attached.*
6. **Sch A charity** - GoFundMe $1,500 included; clothing at $1,800 (3x cost per procedure).
   - Personal fundraisers are not charities. Clothing is FMV; the 3x rule does not hold up (FMV can't exceed cost for used clothing).
   - *Preparer: GoFundMe removed; clothing {fmt(CLOTHING_FMV)} FMV per Goodwill valuation guide; noted in WP.*
7. **Line 26** - Estimates entered as $60,000 per the organizer. IRS account shows three payments.
   - Use $45,000; compute 2210 (110% PY safe harbor not met).
   - *Preparer: Line 26 {fmt(v['26'])}; 2210 penalty {fmt(PEN)} on line 38.*
8. **Form 8995-A** - Draft took 20% of K-1 income. SSTB above the range -> $0.
   - *Preparer: Corrected; SSTB box checked.*
9. **Form 8960** - Draft included the K-1 ordinary income in NII (Axcess default "passive"). She materially participates.
   - Also document the line 5c position for the excess-distribution gain for signer review.
   - *Preparer: Activity set to nonpassive; 5c adjustment documented; NIIT {fmt(v.get('niit', 0))}.*
10. FYI - W-2 box 14 2% SH health correctly in box 1 -> Form 7206 deduction {fmt(r(SH_HEALTH))}. Additional Medicare withheld -> 8959 credit.
""")
print("EVG1007 done", dict(R.summary()), v["refund"], v["balance_due"], "pen", PEN, "IL", IL_TAX, IL_OVER, "PTE", PTE_TAX)
