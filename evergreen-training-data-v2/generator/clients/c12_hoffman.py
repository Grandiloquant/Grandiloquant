"""EVG1012 - Walter & June Hoffman (MFJ, North Carolina - Asheville). Retirees; 2024 seller-financed sale of 22 acres of
unimproved land -> Form 6252 installment method (gross profit % from the 2024 6252 in PERM). 2025: principal/interest from a
HANDWRITTEN payment ledger + amortization schedule; December 2025 payment received 01/06/2026 (cash basis -> 2026); interest
to Schedule B with buyer's name/SSN/address; organizer line blank though PY had the down payment. Senior deduction x2 with
MAGI phase-out; taxable SS; NC D-400 with Bailey-settlement exclusion for June's TSERS pension and SS subtraction."""
import math
from common import ClientBuild, gotcha, fmt
from docs import statement, scanned_pages, write_text, write_xlsx
import forms as F
from tax2025 import Return1040, r

C = ClientBuild("EVG1012", "Hoffman", "Walter & June Hoffman")
ADDR = ("47 Laurel Knob Rd", "Asheville, NC 28804")
T = {"name": "Walter E. Hoffman", "ssn": "XXX-XX-1180", "dob": "1952-05-19"}
S = {"name": "June A. Hoffman", "ssn": "XXX-XX-6437", "dob": "1954-09-02"}
REC_T = [T["name"], *ADDR, f"TIN: {T['ssn']}"]
REC_S = [S["name"], *ADDR, f"TIN: {S['ssn']}"]
REC_J = ["Walter E. & June A. Hoffman", *ADDR, f"TIN: {T['ssn']}"]
BUYER = {"names": "Aaron M. Caldwell & Beth L. Caldwell", "ssn": "XXX-XX-6641", "addr": "912 Sugar Hollow Rd, Fairview, NC 28730"}

# ====================================================================== installment sale facts (2024 Form 6252 in PERM)
PRICE, BASIS, SELL_EXP, DOWN = 420000, 95000, 18000, 84000
NOTE, RATE, N = 336000, 0.06, 120
GROSS_PROFIT = PRICE - BASIS - SELL_EXP
CONTRACT_PRICE = PRICE
GP = GROSS_PROFIT / CONTRACT_PRICE
assert GROSS_PROFIT == 307000 and abs(GP - 0.730952) < 1e-6
GAIN_2024 = r(DOWN * GP)
i = RATE / 12
PMT = round(NOTE * i / (1 - (1 + i) ** -N), 2)
sched = []
bal = NOTE
for k in range(1, N + 1):
    intr = round(bal * i, 2)
    prin = round(PMT - intr, 2) if k < N else bal
    bal = round(bal - prin, 2)
    y, m = 2025 + (k - 1) // 12, (k - 1) % 12 + 1
    sched.append({"n": k, "due": f"{m:02d}/15/{y}", "pmt": PMT, "int": intr, "prin": prin, "bal": bal})
# received dates per June's ledger (payment 7 late with $75 late charge; payment 12 (Dec 2025) arrived 01/06/2026)
RECEIVED = {1: "01/14/2025", 2: "02/14/2025", 3: "03/17/2025", 4: "04/15/2025", 5: "05/15/2025", 6: "06/13/2025",
            7: "07/22/2025", 8: "08/15/2025", 9: "09/15/2025", 10: "10/15/2025", 11: "11/14/2025", 12: "01/06/2026"}
LATE_FEE = 75.00
pay25 = [s for s in sched[:12] if RECEIVED[s["n"]].endswith("2025")]
assert len(pay25) == 11
PRIN_25 = round(sum(s["prin"] for s in pay25), 2)
INT_25 = round(sum(s["int"] for s in pay25), 2)
GAIN_25 = r(PRIN_25 * GP)
DEC = sched[11]
naive_gain_12 = r((PRIN_25 + DEC["prin"]) * GP)

# ====================================================================== PERM
C.write_profile(f"""
# EVG1012 - Hoffman, Walter & June  (PERM)

*Synthetic client - Project Evergreen training data.*

| Item | Detail |
|---|---|
| Client ID | EVG1012 |
| Taxpayer | Walter E. Hoffman, DOB 05/19/1952 (73), SSN {T['ssn']} - retired paper-mill engineer (private pension + IRA) |
| Spouse | June A. Hoffman, DOB 09/02/1954 (71), SSN {S['ssn']} - retired Buncombe County Schools teacher (1976-2011). **NC TSERS member with 13 years of creditable service as of 08/12/1989 -> "Bailey" vested - TSERS benefits exempt from NC tax** |
| Address | {ADDR[0]}, {ADDR[1]} (Buncombe County), resident 30+ years |
| Land sale | 22 acres unimproved land, Sugar Hollow Rd, Fairview NC (bought 1998, basis $95,000). Sold 12/13/2024 to {BUYER['names']} for ${PRICE:,}; selling costs ${SELL_EXP:,}; **seller-financed**: ${DOWN:,} down, note ${NOTE:,} at 6% for 10 years, ${PMT:,.2f}/month due the 15th starting 01/15/2025. Buyers built their home on the land (moved in 08/2025). Buyer SSN (on note): {BUYER['ssn']}. Gross profit % **{GP*100:.4f}%** (2024 Form 6252 in PERM) |
| Records | June keeps a handwritten payment ledger; closing attorney's amortization schedule and the promissory note/deed of trust are in PERM |
| Contact | June preferred - (828) 555-0163 (landline), june.hoffman@example.com (checks email weekly). Paper copies mailed. eSign: no - wet-signed 8879 |
| Engagement | Client since 2016. Retiree tier $950 + installment sale schedule |
| Payments | 2025 federal and NC estimates by check; refund by direct deposit (checking ****0915) |
""")
F.prior_year_summary(C.perm_file("2024_Form_1040_Return_Summary.pdf", "Prior-year return summary"), "Walter & June Hoffman",
    "EVG1012", "Married filing jointly", [
        ["2b", "Taxable interest (Blue Ridge Savings Bank CDs)", 2410],
        ["3a / 3b", "Qualified / ordinary dividends (Blue Ridge Growth Fund)", "2,480 / 2,960"],
        ["4b", "IRA distribution (Walter) - none in 2024 (first RMD year is 2025)", 0],
        ["5b", "Pensions (Walter - Pisgah Paper pension; June - NC TSERS)", 57940],
        ["6a / 6b", "Social security benefits / taxable", "54,780 / 46,563"],
        ["7", "Capital gain - Form 6252 installment sale of land (down payment $84,000 x 73.0952%)", GAIN_2024],
        ["11", "AGI", 171273], ["12", "Standard deduction (MFJ + 2 x 65+)", 32300], ["15", "Taxable income", 138973],
        ["24", "Total tax", 20486], ["26", "Estimated payments", 12000], ["35a", "Refund", 214],
        ["D-400", "NC: SS and Bailey TSERS deducted on Schedule S; NC tax on installment gain", ""]],
    carryovers=[["Installment note balance 12/31/2024 (principal)", NOTE], ["Gross profit percentage (Form 6252 line 19)", f"{GP*100:.4f}%"],
                ["Payments received in prior years (6252 line 23 for 2025)", DOWN]],
    notes="PY WP: 2024 Form 6252 Part I computed from closing statement; gain on down payment only. Future years: principal received x "
          f"{GP*100:.4f}% = LTCG (Sch D line 11); interest to Sch B line 1 with buyer name/SSN/address (buyers' residence). "
          "Recommended estimates for 2025 (fed 4 x $1,500; NC 4 x $300).")
statement(C.perm_file("2024_Form_6252_Installment_Sale.pdf", "Prior-year Form 6252"),
    "2024 Form 6252 - Installment Sale Income - Walter & June Hoffman (filed with 2024 return)", [
        {"table": [["Line", "Description", "Amount"],
                   ["1", "Description of property", "22 acres unimproved land, Sugar Hollow Rd, Fairview NC (PIN 9654-22-1180)"],
                   ["2a / 2b", "Date acquired / Date sold", "04/1998 / 12/13/2024"], ["3", "Sold to a related party?", "No"],
                   ["5", "Selling price", PRICE], ["6", "Mortgages/debts buyer assumed", 0], ["7", "Subtract line 6 from line 5", PRICE],
                   ["8", "Cost or other basis", BASIS], ["9", "Depreciation allowed", 0], ["10", "Adjusted basis", BASIS],
                   ["11", "Commissions and other expenses of sale", SELL_EXP], ["12", "Income recapture", 0],
                   ["13", "Add lines 10, 11 and 12", BASIS + SELL_EXP], ["14", "Subtract line 13 from line 5 (gross profit)", GROSS_PROFIT],
                   ["16", "Gross profit", GROSS_PROFIT], ["17", "Subtract line 13 from line 6", 0], ["18", "Contract price", CONTRACT_PRICE],
                   ["19", "Gross profit percentage", f"{GP*100:.4f}%"], ["20", "Payments received in 2024 (down payment)", DOWN],
                   ["22", "Payments received in 2024", DOWN], ["24", "Installment sale income (to Schedule D line 11, long-term)", GAIN_2024]],
         "left_align_cols": [0, 1]}])
statement(C.perm_file("Promissory_Note_and_Deed_of_Trust_Caldwell_2024.pdf", "Legal agreement"),
    "PROMISSORY NOTE (secured by Deed of Trust) - Buncombe County, North Carolina", [
        {"para": [f"<b>Principal amount:</b> ${NOTE:,}.00     <b>Date:</b> December 13, 2024     <b>Place:</b> Asheville, North Carolina",
                  f"FOR VALUE RECEIVED, the undersigned, {BUYER['names']} (\"Borrowers\"), of {BUYER['addr']}, jointly and severally "
                  f"promise to pay to the order of Walter E. Hoffman and June A. Hoffman (\"Holders\") the principal sum of Three Hundred "
                  f"Thirty-Six Thousand and 00/100 Dollars (${NOTE:,}.00), with interest from December 15, 2024 on the unpaid principal "
                  "at the rate of six percent (6.00%) per annum.",
                  f"<b>Payments.</b> Principal and interest shall be payable in 120 consecutive monthly installments of ${PMT:,.2f}, "
                  "due on the fifteenth (15th) day of each month beginning January 15, 2025, until paid in full; the final installment "
                  "due December 15, 2034. Payments shall be applied first to accrued interest and then to principal.",
                  "<b>Late charge.</b> If any installment is not received within ten (10) days after its due date, Borrowers shall pay a late "
                  "charge of Seventy-Five Dollars ($75.00).",
                  "<b>Prepayment.</b> Borrowers may prepay all or part of the principal at any time without penalty.",
                  "<b>Security.</b> This Note is secured by a Deed of Trust of even date on approximately 22 acres, Sugar Hollow Road, "
                  "Fairview, Buncombe County, NC (PIN 9654-22-1180), recorded in Book 6621, Page 418.",
                  f"<b>Borrowers' taxpayer identification:</b> Aaron M. Caldwell {BUYER['ssn']}. Holders' TIN: {T['ssn']}.",
                  "<b>Default; acceleration; governing law</b> - North Carolina. [standard clauses omitted in synthetic copy]",
                  "Signed: Aaron M. Caldwell /s/   Beth L. Caldwell /s/     Witness: R. Delaney, Attorney at Law"]}])

# ====================================================================== PBC data
SSA_T = {"3": 35640.00, "4": 0.0, "5": 35640.00, "desc": ["Description of amount in box 3: Paid by check or direct deposit $33,420.00; "
         "Medicare Part B premiums deducted from your benefit $2,220.00. Total additions $35,640.00"]}
SSA_S = {"3": 22380.00, "4": 0.0, "5": 22380.00, "desc": ["Description of amount in box 3: Paid by direct deposit $20,160.00; "
         "Medicare Part B premiums deducted from your benefit $2,220.00. Total additions $22,380.00"]}
PEN_T = {"1": 28400.00, "2a": 28400.00, "4": 2800.00, "7": "7", "state": "NC 1,100.00 / 00-4412290 / 28,400.00"}
TSERS = {"1": 31200.00, "2a": 30788.00, "4": 3120.00, "5": 412.00, "7": "7", "state": "NC 0.00"}
IRA_T = {"1": 8600.00, "2a": 8600.00, "4": 860.00, "7": "7", "state": "NC 0.00", "2b": "Taxable amount not determined: [ ]"}
BANK_INT = 2338.61
DIV_ORD, DIV_QUAL, DIV_CGD = 3104.20, 2612.75, 0.0
EST_FED = [("04/15/2025", 1500.00), ("06/16/2025", 1500.00), ("09/15/2025", 1500.00), ("01/15/2026", 1500.00)]
EST_NC = [("04/15/2025", 300.00), ("06/16/2025", 300.00), ("09/15/2025", 300.00), ("01/15/2026", 300.00)]

F.organizer(C.pbc_file("01_2025_Organizer_Hoffman.pdf", "Client organizer", "2026-02-16", "US mail", "paper organizer mailed in"),
    "Walter & June Hoffman", "EVG1012",
    general=[("Did your marital status change during 2025?", "No", ""),
             ("Did you sell, exchange or receive payments on property sold in a prior year (installment sale)?", "", ""),
             ("Did you receive Social Security or pension payments?", "Yes", "same as always"),
             ("Did you make estimated tax payments?", "Yes", "Fed and NC, see list"),
             ("Did you purchase items out of state without paying NC sales tax (use tax)?", "No", ""),
             ("Did you receive, sell, exchange digital assets?", "No", "")],
    dependents=[],
    income_rows=[["Interest", "Blue Ridge Savings Bank", 2410, "2,338.61"],
                 ["Dividends", "Blue Ridge Growth Fund", 2960, "see 1099"],
                 ["Installment sale - Caldwell land note", "Down payment received 12/2024", DOWN, ""],
                 ["Pension", "Pisgah Paper Co. Retirement Plan", 28000, "28,400"],
                 ["Pension", "NC TSERS (June)", 29940, "31,200"],
                 ["IRA distribution", "Walter IRA (first RMD)", "", "8,600"],
                 ["Social Security", "Walter / June", "54,780", "see SSA-1099s"]],
    deductions_rows=[["Medical", "Medigap (both) + Rx + dental", 7900, "8,140"],
                     ["Property tax", "Buncombe County", 3980, "4,120"],
                     ["Charitable", "church + Manna Food Bank", 3100, "3,300"],
                     ["Estimated tax - federal", "4 x $1,500", 12000, "6,000"],
                     ["Estimated tax - NC", "4 x $300", 2400, "1,200"]],
    signature_date="02/10/2026")
F.ssa_1099(C.pbc_file("02_SSA-1099_Walter.pdf", "Form SSA-1099", "2026-02-16", "US mail"), [T["name"], T["ssn"], *ADDR], SSA_T)
F.ssa_1099(C.pbc_file("03_SSA-1099_June.pdf", "Form SSA-1099", "2026-02-16", "US mail"), [S["name"], S["ssn"], *ADDR], SSA_S)
F.f1099_r(C.pbc_file("04_1099-R_Pisgah_Paper_Pension_Walter.pdf", "Form 1099-R", "2026-02-16", "US mail"),
          ["Pisgah Paper Co. Retirement Plan - synthetic", "c/o Plan Administrator, PO Box 1450", "Canton, NC 28716", "TIN: 00-4412290"],
          REC_T, PEN_T, account="PEN-****2201")
F.f1099_r(C.pbc_file("05_1099-R_NC_TSERS_June.pdf", "Form 1099-R", "2026-02-16", "US mail"),
          ["NC Teachers' and State Employees' Retirement System (synthetic)", "3200 Atlantic Ave", "Raleigh, NC 27604", "TIN: 00-6000469"],
          REC_S, TSERS, account="TSERS-****7730",
          notes=["Box 5: recovery of after-tax employee contributions (Simplified Method).",
                 "Retirement benefits may be exempt from North Carolina income tax if you had 5 or more years of creditable service as of "
                 "August 12, 1989 (Bailey v. State of North Carolina). See the D-400 instructions."])
F.f1099_r(C.pbc_file("06_1099-R_IRA_RMD_Walter.pdf", "Form 1099-R", "2026-02-16", "US mail"),
          ["Blue Ridge Growth Fund IRA Custodian - synthetic", "PO Box 9022", "Charlotte, NC 28201", "TIN: 00-3350187"],
          REC_T, IRA_T, account="IRA-****6604", notes=["Box 7: IRA/SEP/SIMPLE [X]. Distribution 12/05/2025 (required minimum distribution)."])
F.f1099_int(C.pbc_file("07_1099-INT_Blue_Ridge_Savings_Bank.pdf", "Form 1099-INT", "2026-02-16", "US mail"),
            ["Blue Ridge Savings Bank - synthetic", "25 Patton Ave", "Asheville, NC 28801", "TIN: 00-0567112"], REC_J, {"1": BANK_INT},
            account="CD ****1180")
F.f1099_div(C.pbc_file("08_1099-DIV_Blue_Ridge_Growth_Fund.pdf", "Form 1099-DIV", "2026-02-16", "US mail"),
            ["Blue Ridge Growth Fund - synthetic", "PO Box 9022", "Charlotte, NC 28201", "TIN: 00-3350190"], REC_J,
            {"1a": DIV_ORD, "1b": DIV_QUAL}, account="****4471")
# June's handwritten ledger (scanned) - one mis-split row (she wrote March as all principal) and the Jan 6 note
led = ["CALDWELL NOTE - payments rec'd 2025   (pmt $3,730.29)", "", "date      ck#    amount     int    prin"]
for s in pay25:
    amt = s["pmt"] + (LATE_FEE if s["n"] == 7 else 0)
    if s["n"] == 3:
        led.append(f"{RECEIVED[s['n']]}  {1100 + s['n']}  {amt:,.2f}    --    {amt:,.2f} ?")
    else:
        led.append(f"{RECEIVED[s['n']]}  {1100 + s['n']}  {amt:,.2f}  {s['int']:,.2f}  {s['prin']:,.2f}"
                   + ("  (late! +$75)" if s["n"] == 7 else ""))
led += ["", "Dec pmt - came Jan 6 2026 (ck 1112) - holiday mail", "", "total rec'd 2025 = 41,108.19 ?? check w/ Walter"]
scanned_pages(C.pbc_file("09_June_handwritten_payment_ledger_2025.pdf", "Handwritten ledger (scan)", "2026-02-16", "US mail",
                         "handwritten pages"), [led], handwritten=True, seed=12, skew=0.9)
# amortization schedule from closing attorney (PDF) - payments 1-24
statement(C.pbc_file("10_Amortization_Schedule_Caldwell_Note.pdf", "Amortization schedule", "2026-02-16", "US mail",
                     "photocopy of attorney schedule"),
    "Amortization Schedule - $336,000 at 6.00% - 120 monthly payments - Caldwell to Hoffman (prepared by R. Delaney, Attorney)", [
        {"table": [["#", "Due date", "Payment", "Interest", "Principal", "Balance"]] +
                  [[s["n"], s["due"], s["pmt"], s["int"], s["prin"], s["bal"]] for s in sched[:24]]},
        {"note": f"Schedule continues through payment 120 (12/15/2034). Total interest over the life of the note: "
                 f"${round(PMT * (N - 1) + sched[-1]['prin'] + sched[-1]['int'] - NOTE, 2):,.2f} (assumes all payments on due dates)."}])
write_text(C.pbc_file("11_Estimated_payments_list.txt", "Client list (typed by June)", "2026-02-16", "US mail"),
    "2025 ESTIMATED TAX PAYMENTS (checks)\n\nFederal (1040-ES):\n" +
    "\n".join(f"  {d}  ${a:,.2f}" for d, a in EST_FED) + "\n\nNC (NC-40):\n" + "\n".join(f"  {d}  ${a:,.2f}" for d, a in EST_NC) + "\n")
statement(C.pbc_file("12_Medical_and_property_tax_receipts.pdf", "Deduction receipts", "2026-02-16", "US mail"),
    "2025 Medical / Property Tax / Charitable receipts (compiled by June)", [
        {"table": [["Item", "Amount"], ["Medigap Plan G premiums - Walter", 2580.00], ["Medigap Plan G premiums - June", 2580.00],
                   ["Part D premiums (both)", 780.00], ["Prescriptions / dental / eyeglasses", 2200.00], ["Total medical per June", 8140.00],
                   ["Buncombe County property tax 2025 (paid 12/2025)", 4120.00], ["Church + Manna Food Bank", 3300.00]],
         "left_align_cols": [0]}])
write_text(C.pbc_file("13_Phone_note_June_2026-03-04.txt", "Client correspondence (phone note)", "2026-03-04", "Phone"),
"""[Phone note - K. Walsh (preparer), 03/04/2026 10:40]
Called June re: organizer - installment sale question left blank and no amount entered on the Caldwell note line
(PY shows the $84,000 down payment). June: "Oh - the Caldwells pay us every month, I sent my notebook page and the
lawyer's schedule. I didn't know where to put it on the form." Confirmed: 11 checks received in 2025; the December
check arrived January 6 (holiday mail) and was deposited 01/07/2026. July check was late - they added the $75 late fee.
The Caldwells finished their house and moved in over the summer (August 2025).
No prepayments of principal. Nothing else sold in 2025.
""")

# ====================================================================== RETURN
ssa_net = SSA_T["5"] + SSA_S["5"]
medicare_prem = 2220 * 2
facts = {
    "status": "MFJ",
    "taxpayer": {"age65": True}, "spouse": {"age65": True},
    "interest": [{"payer": "Blue Ridge Savings Bank", "amount": BANK_INT},
                 {"payer": f"Seller-financed mortgage interest - {BUYER['names']}, SSN {BUYER['ssn']}, {BUYER['addr']} "
                           f"(incl. ${LATE_FEE:.0f} late charge)", "amount": round(INT_25 + LATE_FEE, 2)}],
    "dividends": [{"payer": "Blue Ridge Growth Fund", "ordinary": DIV_ORD, "qualified": DIV_QUAL}],
    "ira": [{"gross": IRA_T["1"], "taxable": IRA_T["2a"]}],
    "pension": [{"gross": PEN_T["1"], "taxable": PEN_T["2a"]}, {"gross": TSERS["1"], "taxable": TSERS["2a"]}],
    "ssa": [{"net_benefits": SSA_T["5"]}, {"net_benefits": SSA_S["5"]}],
    "other_lt": GAIN_25,
    "withholding_1099": PEN_T["4"] + TSERS["4"] + IRA_T["4"],
    "estimated_payments": sum(a for _, a in EST_FED),
    "itemized": {"medical": 8140 + medicare_prem, "real_estate_tax": 4120, "charity_cash": 3300},
    "sch1a": {"seniors": 2},
}
R = Return1040(facts).compute()
v = R.values
assert v["deduction_type"] == "Standard" and v["12e"] == 31500 + 2 * 1600
magi = v["11"]
per_senior = max(0, 6000 - 0.06 * max(0, magi - 150000))
assert v["13b"] == r(2 * per_senior)
assert v["6b"] == r(0.85 * ssa_net)   # provisional income far above $44,000 -> 85% cap
# 2210: 2024 AGI > $150k -> 110% PY safe harbor not met, but 90% of 2025 tax is (installments timely)
req_90 = 0.90 * v["24"]
paid = v["25d"] + v["26"]
assert paid >= req_90 and (v["25d"] / 4 + 1500) >= req_90 / 4

# ---------------------------------------------------------------- NC D-400
nc_ss = v["6b"]
nc_bailey = TSERS["2a"]
nc_std = 25500
nc_ti = max(0, v["11"] - nc_ss - nc_bailey - nc_std)
nc_tax = r(nc_ti * 0.0425)
nc_wh = 1100
nc_est = sum(a for _, a in EST_NC)
nc_bal = nc_tax - nc_wh - nc_est
nc = {"title": "North Carolina Form D-400 (2025) - Resident - MFJ", "lines": [
    ("6", "Federal adjusted gross income", v["11"]), ("7", "Additions to federal AGI (Schedule S Part A)", 0),
    ("9", "Deductions from federal AGI (Schedule S Part B)", nc_ss + nc_bailey),
    ("S-B", f"  - Taxable social security included in federal AGI", nc_ss),
    ("S-B", f"  - Bailey settlement: June's NC TSERS benefits (vested 5+ yrs as of 08/12/1989) included in federal AGI", nc_bailey),
    ("S-B", "  - Walter's private pension and IRA RMD: NOT exempt (no NC general retirement exclusion)", 0),
    ("10", "Child deduction", 0), ("11", "NC standard deduction (MFJ - no additional amount for age in NC)", nc_std),
    ("14", "North Carolina taxable income", nc_ti), ("15", "North Carolina income tax (4.25%)", nc_tax),
    ("16-17", "Tax credits", 0), ("18", "Consumer use tax (client: none)", 0), ("19", "Add lines 17 and 18", nc_tax),
    ("20a", "NC income tax withheld (Pisgah Paper pension 1099-R)", nc_wh), ("21a", "2025 NC estimated tax payments", nc_est),
    ("25/28", "Refund" if nc_bal < 0 else "Tax due", abs(nc_bal))],
    "note": "Installment-sale gain and seller-financed interest are taxable in NC (included in federal AGI, no NC subtraction)."}

f6252 = [["Form 6252 (2025) - Part II (year after the year of sale) - Caldwell land note", "Amount"],
         ["Line 1 Property: 22 acres unimproved land, Sugar Hollow Rd, Fairview NC; acquired 04/1998; sold 12/13/2024; not related party", ""],
         ["Line 19 Gross profit percentage (from 2024 Form 6252: 307,000 / 420,000)", f"{GP*100:.4f}%"],
         ["Line 21 Payments received during 2025 - principal portion of 11 installments (payments 1-11)", PRIN_25],
         ["Line 22 Add lines 20 and 21", PRIN_25],
         ["Line 23 Payments received in prior years (2024 down payment)", DOWN],
         ["Line 24 Installment sale income (line 22 x line 19)", GAIN_25],
         ["Line 25 Ordinary income recapture", 0],
         ["Line 26 Subtract line 25 from line 24 - long-term (to Schedule D line 11)", GAIN_25],
         ["Note: payment 12 (due 12/15/2025) received 01/06/2026 -> 2026 (cash basis) - principal", DEC["prin"]],
         ["Principal balance 12/31/2025 (after payment 11)", sched[10]["bal"]]]
pay_rows = [["#", "Due", "Received", "Check amount", "Interest (amortization)", "Principal", "Year"]]
for s in sched[:12]:
    amt = s["pmt"] + (LATE_FEE if s["n"] == 7 else 0)
    pay_rows.append([s["n"], s["due"], RECEIVED[s["n"]], amt, s["int"], s["prin"], RECEIVED[s["n"]][-4:]])
pay_rows.append(["2025 total", "", "", round(sum(s["pmt"] for s in pay25) + LATE_FEE, 2), INT_25, PRIN_25, ""])
comp_a = [["Standard vs itemized", "Amount"], ["Medical: Medicare Part B from SSA-1099s (4,440) + Medigap/Part D/out-of-pocket (8,140)", 8140 + medicare_prem],
          ["Less 7.5% of AGI", -r(0.075 * v["11"])], ["Deductible medical", max(0, 8140 + medicare_prem - r(0.075 * v["11"]))],
          ["Property tax", 4120], ["Charitable", 3300], ["Total itemized", v["itemized_total_computed"]],
          ["Standard deduction MFJ $31,500 + 2 x $1,600 (both 65+)", v["12e"]]]
sen = [["Schedule 1-A Part V - Enhanced deduction for seniors", "Amount"], ["Modified AGI", magi], ["Threshold (MFJ)", 150000],
       ["Excess x 6%", r(0.06 * max(0, magi - 150000))], ["Walter (73): $6,000 less reduction", r(per_senior)],
       ["June (71): $6,000 less reduction", r(per_senior)], ["Total (Form 1040 line 13b)", v["13b"]]]
C.write_return(R, [
    ("Taxpayer / Spouse", f"{T['name']} ({T['ssn']}) / {S['name']} ({S['ssn']}) - both 65 or older"),
    ("Address", ", ".join(ADDR)),
    ("Filing status", "Married filing jointly"),
    ("Digital assets question", "No"),
    ("Forms included", "1040, Schedule 1-A, Schedule B, Schedule D, Form 6252; NC D-400 with Schedule S"),
    ("State", "North Carolina D-400 (resident)"),
    ("Filing method", "E-file federal and NC (Form 8879 / NC e-file authorization wet-signed 04/06/2026); " + (f"federal balance due ${v['balance_due']:,} by check with Form 1040-V" if v["balance_due"] else "federal refund by direct deposit ****0915") + ("; NC refund by direct deposit ****0915" if nc_bal < 0 else "; NC balance due by check")),
], state_summary=[nc], attachments=[("Form 6252 - Installment Sale Income (2025)", f6252),
                                     ("Installment payment schedule - 2025 (from ledger + amortization schedule)", pay_rows),
                                     ("Senior deduction phase-out", sen), ("Itemized vs standard deduction", comp_a)])

# ====================================================================== ANSWER KEY
gotchas = [
    gotcha("EVG1012-G1", "General Return Prep Notes - blank organizer line with PY amount", "Installment payments missing from the organizer",
           "Organizer installment-sale question and the Caldwell note line are blank -> no 2025 installment income or note interest reported.",
           "PY return and PERM show a 2024 installment sale with a 10-year note. Blank line is not zero: called June (03/04) and used her "
           "ledger + amortization schedule. Report 2025 principal x GP% on Form 6252 and the interest on Schedule B.",
           f"Omits {fmt(GAIN_25)} LTCG and {fmt(INT_25 + LATE_FEE)} interest", ["2b", "7"], "medium"),
    gotcha("EVG1012-G2", "Installment Sales (Form 6252)", "Recognize gain only on principal received",
           f"Report the full {fmt(GROSS_PROFIT - GAIN_2024)} remaining gain in 2025, or apply GP% to the total checks (principal + interest).",
           f"Gain = principal received in 2025 {fmt(PRIN_25)} x {GP*100:.4f}% (GP% from the 2024 6252) = {fmt(GAIN_25)}, long-term (land held "
           "since 1998) -> Schedule D line 11. Interest is not a payment on the selling price.",
           "Line 7", ["7"], "medium"),
    gotcha("EVG1012-G3", "Installment Sales - review the payment schedule dates", "December payment received in January 2026",
           "Use the amortization schedule's 12 scheduled payments for 2025.",
           f"Cash-basis taxpayers report payments when received. Payment 12 (due 12/15/2025) was received 01/06/2026 -> 2026. 2025 = 11 payments: "
           f"principal {fmt(PRIN_25)}, interest {fmt(INT_25)}.",
           f"Gain overstated {fmt(naive_gain_12 - GAIN_25)} and interest {fmt(DEC['int'])} if 12 payments used", ["2b", "7"], "hard"),
    gotcha("EVG1012-G4", "Scan - handwritten statements / legal agreements", "June's ledger mis-splits a payment; late fee",
           "Key the handwritten ledger as-is (March check all 'principal'; total 'rec'd 2025' includes interest).",
           "Use the attorney amortization schedule for the interest/principal split (payments apply to interest first per the note). The $75 July "
           "late charge is additional interest income (Sch B).",
           "Split between line 2b and line 7", ["2b", "7"], "medium"),
    gotcha("EVG1012-G5", "Schedule B - seller-financed mortgage", "Buyer name, SSN and address required",
           "Lump the note interest with bank interest or list only 'Caldwell note'.",
           "Interest on a seller-financed mortgage where the buyer uses the property as a personal residence is listed first on Schedule B line 1 "
           "with the buyer's name, address and SSN ($50 penalty for omission).",
           "Disclosure", ["2b"], "easy"),
    gotcha("EVG1012-G6", "Schedule 1-A - senior deduction (OBBBA)", "Senior deduction phase-out",
           "Take $12,000 (2 x $6,000) without the MAGI test, or skip it because they take the additional standard deduction.",
           f"Both 65+ -> $6,000 each, reduced by 6% of MAGI over $150,000 ({fmt(magi - 150000)} x 6% = {fmt(r(0.06 * (magi - 150000)))} each) "
           f"-> {fmt(v['13b'])}. It is in addition to the standard deduction (incl. 2 x $1,600 age add-ons).",
           "Line 13b", ["13b"], "medium"),
    gotcha("EVG1012-G7", "SALT - NC D-400 (Bailey / Social Security)", "NC exclusions for Bailey-vested TSERS and Social Security",
           "Tax June's TSERS pension in NC (or exempt Walter's private pension too); forget the SS subtraction.",
           f"Schedule S: deduct taxable SS {fmt(nc_ss)} and June's TSERS benefits {fmt(nc_bailey)} (5+ years creditable service as of 08/12/1989). "
           f"Walter's private pension and IRA are taxable in NC. NC taxable income {fmt(nc_ti)} x 4.25% = {fmt(nc_tax)}.",
           "NC tax", [], "medium"),
    gotcha("EVG1012-G8", "Schedule A - Medicare premiums from SSA-1099", "Itemized vs standard for seniors",
           "Itemize using the organizer medical total only, or ignore Medicare Part B shown on the SSA-1099s.",
           f"Add Medicare Part B {fmt(medicare_prem)} from the SSA-1099 descriptions to medical; still, itemized {fmt(v['itemized_total_computed'])} "
           f"< standard {fmt(v['12e'])} -> standard deduction.",
           "Line 12e", ["12e"], "easy"),
]
C.write_answer_key(R, {"residence": "NC (resident D-400)", "complexity": "Retirees + installment sale"}, gotchas,
                   state=[{"jurisdiction": "North Carolina", "form": "D-400", "federal_agi": v["11"], "ss_deduction": nc_ss,
                           "bailey_deduction": nc_bailey, "nc_standard_deduction": nc_std, "nc_taxable_income": nc_ti, "nc_tax": nc_tax,
                           "withholding": nc_wh, "estimated_payments": nc_est,
                           "refund": max(0, -nc_bal), "balance_due": max(0, nc_bal)}],
                   filings=[{"form": "Form 1040 (federal)", "method": "e-file", "due": "2026-04-15", "filed": "2026-04-08"},
                            {"form": "NC D-400", "method": "e-file", "due": "2026-04-15", "filed": "2026-04-08"}],
                   extra={"installment_2025": {"principal": PRIN_25, "interest": INT_25, "late_fee": LATE_FEE, "gain": GAIN_25,
                                               "gp_pct": round(GP, 6), "balance_12_31_2025": sched[10]["bal"]}})
C.write_receipt_log("EVG1012-1040-2025", "K. Walsh (staff)", "L. Chen (senior)", "S. Kennedy, CPA", "2026-02-16")
over = v["refund"] or v["balance_due"]
C.write_notes(f"""
# EVG1012 - Hoffman, Walter & June - 2025 Form 1040 / NC D-400 - Preparer Notes

*Synthetic client - Project Evergreen. Return status: **signed off, e-filed 04/08/2026 (federal + NC), accepted.***

## Return summary
| | |
|---|---|
| Filing status | Married filing jointly (both 65+) |
| AGI (line 11) | {fmt(v['11'])} |
| Deductions | Standard {fmt(v['12e'])} + senior deduction {fmt(v['13b'])} |
| Taxable income | {fmt(v['15'])} |
| Total tax (line 24) | {fmt(v['24'])} |
| Payments | 1099-R withholding {fmt(v['25d'])} + estimates {fmt(v['26'])} |
| **Federal {'refund' if v['refund'] else 'balance due'}** | **{fmt(over)}** |
| NC D-400 | NC taxable income {fmt(nc_ti)}; tax {fmt(nc_tax)}; **{'refund' if nc_bal < 0 else 'balance due'} {fmt(abs(nc_bal))}** |

## What I did and why (plain English)
1. **Installment sale (Form 6252, year 2 of 10).** The organizer left the installment question and the Caldwell note line blank, but the
   2024 return and PERM show the 12/13/2024 land sale with a $336,000 seller-financed note. Per the Return Prep Notes procedure I did not
   assume zero - called June (03/04) and used her handwritten ledger plus the attorney's amortization schedule.
   - Gross profit % from the 2024 Form 6252: ($420,000 - $95,000 basis - $18,000 selling costs) / $420,000 contract price = **{GP*100:.4f}%**.
   - Only **11** payments were received in 2025: the December check arrived **01/06/2026**, so it is 2026 income (cash basis) - the
     schedule shows 12 payments due in 2025.
   - Principal received {fmt(PRIN_25)} x {GP*100:.4f}% = **{fmt(GAIN_25)} long-term gain** (land held since 1998) -> Form 6252 line 26 ->
     Schedule D line 11. No depreciation recapture (unimproved land).
   - June's ledger shows the March check as all principal and adds interest into her total - I used the amortization schedule split
     (the note applies payments to interest first).
2. **Interest.** Seller-financed interest {fmt(INT_25)} + the $75 July late charge (treated as interest) = {fmt(INT_25 + LATE_FEE)}, listed first on
   Schedule B line 1 with the buyers' names, SSN and address (they moved into their new house on the land in 08/2025 - personal residence).
   Bank CD interest {fmt(BANK_INT)}. Dividends {fmt(DIV_ORD)} (qualified {fmt(DIV_QUAL)}).
3. **Retirement income.** Walter's pension {fmt(PEN_T['1'])} (code 7) and his first IRA RMD {fmt(IRA_T['1'])} (born 1952 -> RMD age 73 in 2025;
   taken 12/05/2025). June's TSERS {fmt(TSERS['1'])} gross, taxable {fmt(TSERS['2a'])} (box 5 after-tax contribution recovery $412).
4. **Social security.** Net benefits {fmt(ssa_net)}; provisional income is far above $44,000, so the taxable amount hits the 85% cap:
   {fmt(v['6b'])}. Medicare Part B premiums ($2,220 each) are shown in the SSA-1099 description boxes - picked up for the Schedule A test.
5. **Deductions.** Standard {fmt(v['12e'])} ($31,500 + 2 x $1,600 for age) vs itemized {fmt(v['itemized_total_computed'])} (medical over
   7.5% of AGI + property tax + charity) -> standard. **Senior deduction:** both 65+; MAGI {fmt(magi)} is {fmt(magi - 150000)} over $150,000 ->
   each $6,000 reduced by 6% x excess ({fmt(r(0.06 * (magi - 150000)))}) -> {fmt(v['13b'])}. (We apply the reduction to each spouse's $6,000,
   consistent with the published "fully phased out at $250,000 MFJ" design.)
6. **Tax.** Qualified dividends and the installment gain use the QDCG worksheet: {fmt(v['16'])}.
7. **Estimated tax penalty.** 2024 AGI $171,273 > $150,000, so the prior-year safe harbor would be 110% of 2024 tax ($22,535), which they
   did not pay (2025 estimates were reduced to $1,500/quarter). But withholding + timely estimates ({fmt(paid)}) exceed **90% of 2025 tax**
   ({fmt(r(req_90))}) with each quarter's required installment met -> no Form 2210 penalty (the small balance due is also under $1,000).
8. **North Carolina D-400.** Start with federal AGI {fmt(v['11'])}; Schedule S deductions: taxable social security {fmt(nc_ss)} and June's TSERS
   benefits {fmt(nc_bailey)} (Bailey settlement - she had 13 years of creditable service at 08/12/1989, confirmed in PERM). Walter's
   private pension and IRA are taxable in NC; the installment gain and note interest are taxable in NC. NC standard deduction $25,500
   (NC has no extra amount for age). NC taxable income {fmt(nc_ti)} x 4.25% = {fmt(nc_tax)}; withholding {fmt(nc_wh)} + estimates {fmt(nc_est)}.

## Open items / client communication
- None open. Letter to June: keep logging the Caldwell checks with dates; the January 2026 check counts in 2026. Consider using
  Form 1098-style annual statement to buyers (they need the interest amount and our SSN for their Schedule A).
- 2026 estimates: 2025 AGI is $157,434 (> $150,000), so the 2026 prior-year safe harbor is 110% of 2025 tax = $14,099. Withholding at the 2025 level + 4 x $1,500 = $12,780 falls $1,319 short -> recommended federal estimates 4 x $1,830; NC 4 x $300.

## Hand-off to signer / routing
- [x] Return locked; Accountant's copy saved as *reviewed*
- [x] Federal 1040 - e-file; NC D-400 - e-file; no FBAR
- [x] Due dates 04/15/2026 populated for both
- [x] Wet-signed 8879 + NC authorization (clients do not use eSign); paper copies mailed per preference; June by landline
- [x] PERM updated: note balance 12/31/2025 {fmt(sched[10]['bal'])}; GP% carries forward; payment 12 goes to 2026
- Billing: retiree tier $950 + 1.0 hr installment schedule (client chargeable). Nothing to W/O.
""")
C.write_review_points(f"""
# Review Points - EVG1012 - 2025 - Form 1040

*Reviewer: L. Chen (blue). Preparer responses in red. Synthetic.*

1. **Form 6252 / Schedule D** - First draft had no installment income: organizer line blank. PY shows the Caldwell note ($336,000).
   - Do not treat as zero. Get the 2025 payment history (WP 9-10).
   - *Preparer: Called June 03/04 (WP 13). Ledger + amortization schedule entered.*
2. **Form 6252 line 21** - Draft used 12 payments from the amortization schedule. Payment 12 was received 01/06/2026 -> 2026.
   - *Preparer: Corrected to 11 payments - principal {fmt(PRIN_25)}, gain {fmt(GAIN_25)}.*
3. **Schedule B** - Split each check per the amortization schedule, not June's ledger (March row). Add the $75 late charge. List the buyer's name,
   SSN and address first on line 1.
   - *Preparer: Done - {fmt(INT_25 + LATE_FEE)}.*
4. **Schedule 1-A** - Senior deduction: MAGI is over $150,000 - apply the 6% reduction.
   - *Preparer: {fmt(v['13b'])}; worksheet attached.*
5. **NC D-400 Schedule S** - Draft deducted SS only. June is Bailey-vested (PERM) - deduct TSERS {fmt(nc_bailey)}. Do NOT deduct Walter's private pension.
   - *Preparer: Done. NC tax {fmt(nc_tax)}.*
6. FYI - 2210: 110% PY safe harbor not met, but 90% of current-year tax is covered by withholding + timely estimates. No penalty.
""")
print("EVG1012 done", R.summary()["24"], v["refund"], v["balance_due"], "AGI", v["11"], "NC", nc_tax, nc_bal)
