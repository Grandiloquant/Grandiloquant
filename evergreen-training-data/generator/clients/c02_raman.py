"""EVG1002 - Priya Raman (HOH, Illinois - Naperville). Low-income single mother: organizer says "Single" but she
qualifies for HOH; EITC + CTC/ACTC + Lifetime Learning Credit + Saver's credit; 1099-K for personal items sold at a
loss (report and zero out); 1099-G state refund not taxable (standard deduction in 2024); TreasuryDirect interest
(IL subtraction); child's father also claims the child -> IND-507 e-file reject -> paper file."""
from common import ClientBuild, gotcha, fmt
from docs import statement, scanned_pages, write_text, write_csv
import forms as F
from tax2025 import Return1040, r

C = ClientBuild("EVG1002", "Raman", "Priya Raman")
ADDR = ("1846 Wexford Ct, Apt 3B", "Naperville, IL 60565")
T = {"name": "Priya Raman", "ssn": "XXX-XX-3318", "dob": "1994-07-21"}
KID = {"name": "Arjun Raman", "ssn": "XXX-XX-6604", "dob": "2018-03-09"}
REC_T = [T["name"], *ADDR, f"TIN: {T['ssn']}"]


# ------------------------------------------------------------------ engine extension (local, no shared-module edit)
class RamanReturn(Return1040):
    """Adds the Retirement Savings Contributions Credit (Form 8880, Schedule 3 line 4).
    The shared engine has no saver's-credit input and orders `other_nonref_credits` AFTER the child tax credit.
    Schedule 8812 Credit Limit Worksheet A subtracts Schedule 3 lines 1-4 (FTC, 2441, education, 8880) BEFORE the CTC,
    so the saver's credit must be taken first - that pushes more of the CTC into the refundable ACTC."""

    def _schedule3_nonref(self, agi, l18):
        res = super()._schedule3_nonref(agi, l18)
        sv = self.f.get("saver")
        res["saver"] = 0
        if sv:
            base = min(sv["contributions"], 2000)
            tentative = r(base * sv["rate"])
            limit = max(0, l18 - res["before_ctc"])        # Form 8880 credit limit (tax less FTC/2441/education)
            res["saver"] = min(tentative, limit)
            self.line("Form 8880", "1-6", f"Elective deferrals (W-2 box 12 code D) {r(sv['contributions']):,}; eligible (max 2,000)", r(base))
            self.line("Form 8880", "9", f"Credit rate for AGI {r(agi):,} (HOH: 50% <= 35,625; 20% <= 38,250; 10% <= 59,250)", f"{sv['rate']:.0%}")
            self.line("Form 8880", "12", "Retirement savings contributions credit (to Schedule 3, line 4)", res["saver"])
            res["before_ctc"] += res["saver"]
        return res

    def _finish_schedule3_nonref(self, res, remaining):
        order = [("1", "Foreign tax credit", "ftc"), ("2", "Credit for child and dependent care expenses (Form 2441)", "care"),
                 ("3", "Education credits (Form 8863, line 19)", "edu"),
                 ("4", "Retirement savings contributions credit (Form 8880)", "saver"),
                 ("5a", "Residential clean energy credit (Form 5695)", "clean"),
                 ("5b", "Energy efficient home improvement credit (Form 5695)", "home_imp"),
                 ("6z", "Other nonrefundable credits", "other")]
        left, tot = remaining, 0
        for ln, d, k in order:
            v = res.get(k, 0)
            if not v:
                continue
            used = min(v, max(0, left))
            if used < v:
                self.values[f"{k}_unused"] = v - used
            self.line("Schedule 3", ln, d + (f" (limited from {v:,})" if used < v else ""), used)
            left -= used
            tot += used
        if tot:
            self.line("Schedule 3", "8", "Total nonrefundable credits (to Form 1040, line 20)", tot)
        return tot


# ------------------------------------------------------------------ PERM
C.write_profile(f"""
# EVG1002 - Raman, Priya  (PERM)

*Synthetic client - Project Evergreen training data.*

| Item | Detail |
|---|---|
| Client ID | EVG1002 |
| Taxpayer | Priya Raman, DOB 07/21/1994, SSN XXX-XX-3318, Medical Billing Specialist (DuPage Family Health Partners) |
| Marital status | Never married |
| Dependent | Arjun Raman (son, DOB 03/09/2018, SSN XXX-XX-6604) - lives with Priya full time (lease + school records on file) |
| Child's father | Rohan Mehta (not married to Priya, does not live with them; separate address in Aurora IL). No Form 8332 signed. |
| Address | {ADDR[0]}, {ADDR[1]} (DuPage County) - renter; IL full-year resident |
| Contact | Priya - text/phone preferred (630) 555-0187; email priya.raman@example.com; eSign OK |
| Referral | Online inquiry (VITA site referred her; outside VITA income/complexity window because of the 1098-T question) |
| Engagement | NEW client for 2025. Basic W-2 tier + IL ($1,200 + $250 state). 2023-2024 returns were self-prepared (FreeTaxUSA) as Single, no dependent. |
| Payment info | Voided check on file (Alliant Credit Union checking ending 4410) |
| Onboarding | Driver's license scanned; 2023 & 2024 returns received 01/28/2026 |

**Interview memo 01/28/2026 (transcribed):** Priya is not married; Arjun has lived with her every night of 2025 except a
few weekends with his father. His father "claims Arjun every year" and told her not to put Arjun on her return - she has
done that since 2022. She did not sign any IRS form releasing the exemption. She takes part-time evening classes at College
of DuPage (medical coding certificate). She sold a lot of old furniture and baby things on Facebook Marketplace (paid through
PayPal) after moving apartments in 2025 - "everything went for way less than I paid".
""")
F.prior_year_summary(C.perm_file("2024_Form_1040_Return_Summary.pdf", "Prior-year return summary (client self-prepared)"),
    "Priya Raman", "EVG1002", "Single (as filed - self-prepared)", [
        ["1a", "W-2 wages - DuPage Family Health Partners", 34960],
        ["2b", "Taxable interest - TreasuryDirect (I bond/T-bill) $188", 188],
        ["11", "AGI", 35148], ["12", "Standard deduction (Single)", 14600], ["15", "Taxable income", 20548],
        ["16", "Tax", 2227], ["19", "Child tax credit", 0], ["27", "EIC", 0],
        ["25a", "Federal withholding", 2410], ["35a", "Refund", 183],
        ["IL-1040", "IL base income $34,960 (TreasuryDirect interest subtracted); IL refund", 212]],
    carryovers=[["None", ""]],
    notes="PY return copy received at onboarding (self-prepared). No dependent claimed, no education credit. Standard deduction "
          "used - the 2024 IL refund ($212, received 2025) will not be taxable in 2025. Filing status/dependent claim to be "
          "revisited for 2025 (custodial parent) and possible 1040-X for 2023-2024.")

# ------------------------------------------------------------------ PBC documents
EMP = {"name": "DuPage Family Health Partners, S.C.", "addr1": "2020 W Diehl Rd Ste 400", "addr2": "Naperville, IL 60563",
       "ein": "00-3867214"}
gross = 41600.00
k401 = 2496.00          # 6% elective deferral (code D)
s125 = 2964.00          # section 125 medical/dental premiums
w2b = {"1": round(gross - k401 - s125, 2), "3": round(gross - s125, 2), "5": round(gross - s125, 2)}
w2b.update({"2": 1210.00, "4": round(w2b["3"] * .062, 2), "6": round(w2b["5"] * .0145, 2)})
IL_WH = 1480.00

F.organizer(C.pbc_file("01_2025_Organizer_Priya.pdf", "Client organizer", "2026-02-05"), "Priya Raman", "EVG1002",
    general=[("Filing status for 2025", "Single", "same as last year"),
             ("Did your marital status change during 2025?", "No", ""),
             ("Can anyone claim you as a dependent?", "No", ""),
             ("Dependents you are claiming", "", "Arjun? his dad says he claims him every year - not sure"),
             ("Did you pay for education for yourself or a dependent?", "Yes", "College of DuPage coding classes"),
             ("Did you receive a Form 1099-K or sell items online?", "Yes", "sold old stuff on FB Marketplace"),
             ("Did you receive a state tax refund in 2025?", "Yes", "IL refund"),
             ("Did you contribute to a retirement plan?", "Yes", "401k at work"),
             ("Did you receive, sell, exchange digital assets?", "No", ""),
             ("Did you make estimated tax payments?", "No", "")],
    dependents=[["Arjun Raman", "Son", "03/09/2018", "6604", "", ""]],
    income_rows=[["Wages", "DuPage Family Health Partners", 34960, "see W-2 (photo)"],
                 ["Interest", "TreasuryDirect", 188, ""],
                 ["Interest", "Alliant Credit Union", "", ""],
                 ["Payment apps / 1099-K", "", "", "PayPal - not income?"],
                 ["State refund (1099-G)", "Illinois Dept. of Revenue", "", "212"]],
    deductions_rows=[["Tuition / fees", "College of DuPage", "", "see 1098-T + laptop receipt"],
                     ["Child care", "", "", ""],
                     ["Charitable", "", "", ""],
                     ["Rent paid (IL)", "Wexford Court Apartments", "", "1,640/mo"]],
    signature_date="02/03/2026")

# W-2: only a phone photo (glare, skewed)
scanned_pages(C.pbc_file("02_IMG_20260203_W2_photo.pdf", "Photo upload (image) - Form W-2", "2026-02-05",
                         "Sharefile upload (phone)", "only copy of W-2 provided"),
    [["Form W-2  Wage and Tax Statement      2025      Copy B - To Be Filed With Employee's FEDERAL Tax Return",
      f"b EIN 00-3867214     c DuPage Family Health Partners, S.C.",
      "     2020 W Diehl Rd Ste 400, Naperville IL 60563",
      f"a SSN XXX-XX-3318    e Priya Raman",
      f"     {ADDR[0]}, {ADDR[1]}",
      "",
      f"1  Wages, tips, other comp.       {w2b['1']:,.2f}      2  Federal income tax withheld   {w2b['2']:,.2f}",
      f"3  Social security wages          {w2b['3']:,.2f}      4  Social security tax withheld  {w2b['4']:,.2f}",
      f"5  Medicare wages and tips        {w2b['5']:,.2f}      6  Medicare tax withheld         {w2b['6']:,.2f}",
      "12a  D   2,496.00        12b  DD   8,412.00",
      "13  Retirement plan [X]",
      "14  SEC125  2,964.00",
      f"15 IL  00-3867214     16 {w2b['1']:,.2f}      17 {IL_WH:,.2f}",
      "",
      "   [glare across lower right corner - boxes 18-20 blank]"]],
    handwritten=False, skew=3.1, seed=21, faded=True)

F.f1099_int(C.pbc_file("03_1099-INT_TreasuryDirect.pdf", "Form 1099-INT", "2026-02-05"),
            ["U.S. Department of the Treasury - Bureau of the Fiscal Service", "TreasuryDirect", "Parkersburg, WV 26106",
             "TIN: 00-0000131"], REC_T, {"1": "", "3": 310.46},
            account="TD-****7730", notes=["Box 3 includes interest on Series I savings bonds redeemed 06/2025 ($214.80) and "
                                           "Treasury bills matured 2025 ($95.66)."])
F.f1099_int(C.pbc_file("04_1099-INT_Alliant_CU.pdf", "Form 1099-INT", "2026-02-05"),
            ["Alliant Credit Union", "11545 W Touhy Ave", "Chicago, IL 60666", "TIN: 00-1170442"], REC_T, {"1": 12.30},
            account="****4410-S1")
F.f1099_k(C.pbc_file("05_1099-K_PayPal.pdf", "Form 1099-K", "2026-02-05"),
          ["PayPal, Inc.", "2211 North First Street", "San Jose, CA 95131", "TIN: 00-2645331"], REC_T,
          {"1a": 6812.40, "1b": 6812.40, "2": "5399", "3": 41,
           "months": [0, 0, 0, 385.00, 1420.00, 2915.40, 1560.00, 312.00, 220.00, 0, 0, 0]})
F.f1099_g(C.pbc_file("06_1099-G_IL_refund.pdf", "Form 1099-G", "2026-02-05"),
          ["Illinois Department of Revenue", "PO Box 19044", "Springfield, IL 62794", "TIN: 00-6000003"], REC_T,
          {"2": 212.00, "3": "2024"})
F.f1098_t(C.pbc_file("07_1098-T_College_of_DuPage.pdf", "Form 1098-T", "2026-02-05"),
          ["College of DuPage (Community College District 502)", "425 Fawell Blvd", "Glen Ellyn, IL 60137",
           "TIN: 00-2033110", "(630) 555-2000"], REC_T, {"1": 2388.00, "8": "", "9": ""},
          notes=["Box 8 (at least half-time) not checked - student enrolled 6 credit hours Spring and 5 Fall 2025 in the "
                 "Medical Coding & Billing Certificate program."])
statement(C.pbc_file("08_BestBuy_receipt_laptop.pdf", "Receipt", "2026-02-05"), "Best Buy - Order Receipt #BBY01-8841273", [
    {"table": [["Item", "Qty", "Price"], ["Lenovo IdeaPad 5 15.6\" laptop", 1, 849.99], ["Sales tax (Naperville)", "", 60.56],
               ["Total charged Visa ****2291 on 01/12/2025", "", 910.55]], "total_row": True},
    {"para": "Priya's note on upload: 'laptop for my coding class - COD said we need one but didn't sell it'."}])
write_csv(C.pbc_file("09_PayPal_activity_export_2025.csv", "Payment app export (CSV)", "2026-02-05"),
          ["Date", "Buyer (Marketplace)", "Item", "Gross", "Fee", "Net", "Client note - what I paid"],
          [["2025-04-19", "Marketplace buyer #1", "Graco 4Ever car seat", 85.00, 0, 85.00, "~300 (2019)"],
           ["2025-04-26", "Marketplace buyer #2", "Crib + mattress", 300.00, 0, 300.00, "~650 (2018)"],
           ["2025-05-03", "Marketplace buyer #3", "Sofa (sectional)", 750.00, 0, 750.00, "2,100 (2020)"],
           ["2025-05-17", "Marketplace buyer #4", "Kids bike + toys lot", 120.00, 0, 120.00, "~400"],
           ["2025-05-24", "Marketplace buyer #5", "Dining table + 4 chairs", 550.00, 0, 550.00, "1,300 (2019)"],
           ["2025-06-07", "Marketplace buyer #6", "Bedroom dresser + nightstands", 900.00, 0, 900.00, "2,400 (2020)"],
           ["2025-06-14", "Marketplace buyer #7", "TV 55in", 260.00, 0, 260.00, "680 (2021)"],
           ["2025-06-21", "various (14 buyers)", "baby clothes / stroller / high chair / misc", 1755.40, 0, 1755.40, "way more"],
           ["2025-07-12", "various (9 buyers)", "household items (move)", 1560.00, 0, 1560.00, "way more"],
           ["2025-08-09", "various (6 buyers)", "books / toys", 312.00, 0, 312.00, ""],
           ["2025-09-13", "various (4 buyers)", "old desk, lamps", 220.00, 0, 220.00, "~500"],
           ["TOTAL", "", "", 6812.40, 0, 6812.40, "all personal stuff - sold at a loss"]])
F.f1099_int(C.pbc_file("10_1099-INT_TreasuryDirect_copy.pdf", "Form 1099-INT", "2026-02-05", note="second upload"),
            ["U.S. Department of the Treasury - Bureau of the Fiscal Service", "TreasuryDirect", "Parkersburg, WV 26106",
             "TIN: 00-0000131"], REC_T, {"1": "", "3": 310.46}, account="TD-****7730",
            notes=["Box 3 includes interest on Series I savings bonds redeemed 06/2025 ($214.80) and "
                   "Treasury bills matured 2025 ($95.66)."], watermark="REPRINT")
statement(C.pbc_file("11_Naperville_CUSD203_school_fees.pdf", "School fee receipt", "2026-02-05"),
    "Naperville Community Unit School District 203 - 2025 Fee Payment History (Arjun Raman, Grade 2)", [
        {"table": [["Date", "Description", "Amount"], ["08/05/2025", "Registration / instructional materials fee", 115.00],
                   ["08/05/2025", "Chromebook technology fee", 50.00], ["09/12/2025", "Field trip (Morton Arboretum)", 12.00],
                   ["Total", "", 177.00]], "total_row": True}])
statement(C.pbc_file("12_Lease_Wexford_Court_2025.pdf", "Residential lease (excerpt)", "2026-02-05"),
    "Wexford Court Apartments - Residential Lease Agreement (excerpt)", [
        {"table": [["Term", "Detail"], ["Premises", f"{ADDR[0]}, {ADDR[1]}"], ["Lease term", "02/01/2025 - 01/31/2026"],
                   ["Tenant", "Priya Raman"], ["Authorized occupants", "Priya Raman; Arjun Raman (minor child)"],
                   ["Monthly rent", 1640.00]], "left_align_cols": [0, 1]},
        {"para": "Prior address 01/2025: 612 Iroquois Ave Unit 2, Naperville IL 60563 (Priya and Arjun)."}])
statement(C.pbc_file("13_1095-C_DuPage_Family_Health.pdf", "Form 1095-C", "2026-02-05"),
    "Form 1095-C Employer-Provided Health Insurance Offer and Coverage - 2025", [
        {"table": [["Line", "All 12 months"], ["14 Offer of coverage", "1E"], ["15 Employee required contribution", 96.00],
                   ["16 Section 4980H safe harbor", "2C"]]},
        {"heading": "Part III - Covered individuals", "table": [["Name", "SSN", "Covered all 12 months"],
                                                               ["Priya Raman", "XXX-XX-3318", "X"], ["Arjun Raman", "XXX-XX-6604", "X"]]}])
write_text(C.pbc_file("14_Text_screenshot_transcript_Rohan.txt", "Client correspondence (text message transcript)",
                      "2026-02-05", "Sharefile upload (phone)"),
"""[Transcribed from screenshot uploaded by client - iMessage, 01/30/2026]

Rohan: hey reminder I'm doing my taxes this weekend, I'm putting Arjun on mine like always. don't put him on yours
       or we'll both get audited lol
Priya: ok... my tax lady asked about it. he lives with me tho
Rohan: I pay child support so I get to claim him. that's how it works
Priya: ok whatever
""")
write_text(C.pbc_file("15_Email_thread_custody_2026-02-12.txt", "Client correspondence", "2026-02-12", "Email",
                      "reply to preparer questions"),
"""From: preparer@evergreentax.example
To: Priya Raman <priya.raman@example.com>
Date: Tue, 10 Feb 2026 11:20:00 -0600
Subject: Raman 2025 - a few questions (Arjun / filing status)

Hi Priya - thanks for the documents. A few questions so we can file correctly:
1. How many nights in 2025 did Arjun sleep at your home vs. at his father's?
2. Did you ever sign IRS Form 8332 (Release of Claim to Exemption) or any similar written release for Rohan?
3. Does a court order say who may claim Arjun?
4. Did you pay more than half the cost of keeping up your apartment (rent, utilities, groceries)?
Based on what you told us, you are likely the custodial parent and may file as Head of Household with Arjun as your
qualifying child. If his father also claims him, our e-filed return may be rejected; if so, we would paper-file.

-----
From: Priya Raman
Date: Thu, 12 Feb 2026 21:03:17 -0600
Subject: RE: Raman 2025 - a few questions (Arjun / filing status)

1. he was with his dad maybe 2 weekends a month, so like 50 nights? rest with me
2. no never signed anything
3. no court order, we were never married. child support is through IL HFS
4. yes I pay everything, rent + ComEd + Nicor + food. Rohan pays $350/mo child support
Thanks!! I had no idea.
""")
write_text(C.pbc_file("16_Email_IRS_reject_notice_2026-02-20.txt", "Firm e-file reject notice (saved to WP)", "2026-02-20",
                      "CCH e-file status report"),
"""CCH Axcess ELF Status - Rejected
Return: EVG1002 Raman, Priya   TY2025 Form 1040   Submission ID 0048912026051xxxxxxx
Transmitted: 02/19/2026 16:42   Status: REJECTED 02/20/2026 06:15

Rule IND-507-01: 'Qualifying Child SSN' in the Earned Income Credit Schedule (Schedule EIC) and/or
Dependent SSN on Form 1040 was used as a Dependent SSN or Qualifying Child SSN on another return
for the same tax period.

Dependent SSN: XXX-XX-6604 (ARJUN RAMAN)
""")
statement(C.pbc_file("17_COD_attendance_and_School_letter.pdf", "Residency support (school letter)", "2026-02-24",
                     "Email attachment", "requested by preparer after e-file reject"),
    "Naperville CUSD 203 - Ellsworth Elementary - Enrollment Verification", [
        {"para": ["To whom it may concern: This letter verifies that Arjun Raman (DOB 03/09/2018) was enrolled at Ellsworth "
                  "Elementary for the 2024-25 and 2025-26 school years. The parent/guardian of record and address on file for "
                  f"the entire 2025 calendar year is Priya Raman, 612 Iroquois Ave Unit 2 (through 01/31/2025) and {ADDR[0]}, "
                  "Naperville (from 02/01/2025).", "Signed: Office of the Principal (synthetic)"]}])

# ------------------------------------------------------------------ RETURN
interest_td = 310.46
interest_cu = 12.30
paypal = 6812.40
coll_qualified = 2388.00       # 1098-T box 1; laptop NOT a qualified LLC expense (not paid to the institution)
facts = {
    "status": "HOH",
    "taxpayer": {"age65": False},
    "dependents": [{"name": "Arjun Raman", "ctc": True}],
    "w2": [{"who": "T", "box1": w2b["1"], "box2": w2b["2"], "box3": w2b["3"], "box4": w2b["4"], "box5": w2b["5"],
            "box6": w2b["6"]}],
    "interest": [{"payer": "U.S. Treasury - TreasuryDirect (box 3, U.S. obligations)", "amount": interest_td},
                 {"payer": "Alliant Credit Union", "amount": interest_cu}],
    # IRS FAQ / 2025 Sch 1 instructions: personal items sold at a loss reported on 1099-K -> 8z and offset on 24z
    "sch1": {"other": [("8z", "Form 1099-K personal items sold at a loss (PayPal)", paypal)]},
    "adjustments": {"other": [("24z", "Form 1099-K personal items sold at a loss (PayPal)", paypal)]},
    "education": [{"name": "Priya Raman (College of DuPage)", "type": "LLC", "qualified_expenses": coll_qualified}],
    "saver": {"contributions": k401, "rate": .20},
    "eic_eligible": True, "eic_kids": 1, "eic_invest_income": interest_td + interest_cu,
}
R = RamanReturn(facts).compute()
v = R.values
assert 35625 < v["11"] <= 38250, "AGI must stay in the 20% saver's-credit tier"

# Naive first-draft comparison (Single, no dependent, no saver ordering) for review points
# (isolates the filing-status/dependent error: Single, no dependent, no EIC child; everything else the same)
naive_f = dict(facts, status="S", dependents=[], eic_kids=0, saver={"contributions": k401, "rate": .10})
naive = RamanReturn(naive_f).compute()

# ------------------------------------------------------------------ Illinois IL-1040
il_sub_treasury = r(interest_td)
il_base = v["11"] - il_sub_treasury
il_exempt = 2 * 2850
il_net = il_base - il_exempt
il_tax = r(il_net * .0495)
il_eic = r(v["27a"] * .20)
il_ctc = r(il_eic * .40)       # ASSUMPTION: IL child tax credit = 40% of IL EIC for 2025 (child under 12)
il_pay = r(IL_WH) + il_eic + il_ctc
il_refund = il_pay - il_tax
state = [{"title": "Illinois Form IL-1040 (full-year resident) - summary", "lines": [
    ("1", "Federal adjusted gross income", v["11"]),
    ("5-7", "Subtractions - Schedule M: U.S. Treasury obligation interest (TreasuryDirect 1099-INT box 3)", -il_sub_treasury),
    ("-", "IL refund on 1099-G: not in federal AGI -> no IL subtraction needed", 0),
    ("9", "Illinois base income", il_base),
    ("10", "Exemption allowance: 2 x $2,850 (Priya + Arjun)", il_exempt),
    ("11", "Net income", il_net),
    ("12", "Tax at 4.95%", il_tax),
    ("-", "K-12 education expense credit (Sch ICR): qualified fees $165 do not exceed $250 floor", 0),
    ("-", "Property tax credit: renter - not eligible", 0),
    ("Sch IL-E/EIC", "Illinois earned income credit = 20% x federal EIC " + f"{v['27a']:,}", il_eic),
    ("Sch IL-E/EIC", "Illinois child tax credit = 40% x IL EIC (child under 12) - see assumption", il_ctc),
    ("-", "IL income tax withheld (W-2 box 17)", r(IL_WH)),
    ("-", "Total payments and refundable credits", il_pay),
    ("-", "REFUND", il_refund)],
    "note": "IL-1040 transmitted as a state-only (unlinked) e-file 02/24/2026 and accepted 02/25/2026. ASSUMPTION: IL child "
            "tax credit for 2025 computed at 40% of the IL EIC for a qualifying child under age 12 - "
            "verify rate against final 2025 Schedule IL-E/EIC instructions."}]

# ------------------------------------------------------------------ attachments
f8867 = [["Form 8867 - Paid Preparer's Due Diligence Checklist (EIC, CTC/ACTC, AOTC, HOH)", "Response"],
         ["Credits/status claimed", "EIC, CTC/ACTC, HOH (LLC is not a due-diligence credit)"],
         ["Interview: residency of child > 1/2 year", "Yes - ~315 nights with Priya; lease + school enrollment letter (WP 17)"],
         ["Relationship / age / SSN", "Son, age 7, valid SSN XXX-XX-6604"],
         ["Other person may claim the child (tie-breaker / noncustodial)?", "Father may claim - but Priya is the custodial "
          "parent, no Form 8332 signed, no decree -> Priya has the right to claim"],
         ["HOH: paid > 1/2 cost of keeping up home; unmarried", "Yes - rent $1,640/mo, utilities, food (client email 02/12)"],
         ["Documents reviewed / retained", "Lease, school letter, text message transcript, custody interview notes"],
         ["Knowledge requirement documented", "Yes - reject IND-507 resolved by paper filing with explanation retained"]]
sch_eic = [["Schedule EIC - qualifying child", "Detail"], ["Name", "Arjun Raman"], ["SSN", "XXX-XX-6604"],
           ["Year of birth", "2018"], ["Relationship", "Son"], ["Months lived with taxpayer in U.S.", "12"],
           ["Student / disabled", "No / No"]]
k1099 = [["Form 1099-K reconciliation (PayPal)", "Amount"], ["1099-K box 1a gross", paypal],
         ["Items sold: used personal furniture, baby gear, household goods (CSV export WP 9)", ""],
         ["Client's cost of items (estimates; all sold below cost)", "~$9,300+"],
         ["Reported on Schedule 1 line 8z", r(paypal)], ["Offset on Schedule 1 line 24z", -r(paypal)],
         ["Net effect on AGI", 0]]
C.write_return(R, [
    ("Taxpayer", "Priya Raman (XXX-XX-3318)"),
    ("Address", ", ".join(ADDR)),
    ("Filing status", "Head of household (qualifying person: Arjun Raman, son)"),
    ("Dependents", "Arjun Raman (son, DOB 03/09/2018) - CTC, EIC qualifying child"),
    ("Digital assets question", "No"),
    ("Forms included", "1040; Sch 1, 3, 8812, EIC; Forms 8863, 8880; Form 8867 (preparer)"),
    ("State", "Illinois IL-1040 with Schedule M and Schedule IL-E/EIC"),
    ("Filing method", "PAPER-FILED 03/04/2026 after e-file reject IND-507-01 (02/20/2026)"),
], state_summary=state,
   attachments=[("Filing / mailing detail", [["Item", "Detail"],
                 ["E-file", "Transmitted 02/19/2026; rejected 02/20/2026 - IND-507-01 (dependent SSN XXX-XX-6604 used on another return)"],
                 ["Paper return", "Government copy wet-signed 03/03/2026; mailed 03/04/2026 to the IRS Kansas City, MO processing center "
                                  "(address per 2025 Form 1040 instructions - Illinois, no payment enclosed)"],
                 ["Tracking", "USPS Certified 9407 1118 9876 5432 1098 76"],
                 ["Illinois", "IL-1040 state-only e-file 02/24/2026, accepted 02/25/2026"]]),
                ("Schedule EIC", sch_eic), ("Form 1099-K - personal items sold at a loss", k1099),
                ("Form 8867 (preparer due diligence - retained, filed with return)", f8867)])

gotchas = [
    gotcha("EVG1002-G1", "Review - Filing Status (Single vs HOH)", "Organizer says 'Single' but client qualifies for HOH",
           "Carry forward the organizer / PY filing status (Single, no dependent) - standard deduction $15,750, Single brackets, no EIC/CTC.",
           "Unmarried, paid > 1/2 the cost of keeping up the home, qualifying child (son, 7) lived with her > 1/2 the year -> "
           "Head of household: standard deduction $23,625, HOH brackets; claim Arjun as dependent.",
           f"Refund {fmt(v['refund'])} vs balance due {fmt(naive.values['balance_due'])} on a naive Single/no-dependent return", ["filing status", "12e", "16"], "easy"),
    gotcha("EVG1002-G2", "Post-Submission Exceptions - E-File Rejects / Paper Filing Returns",
           "Child's father also claims the child -> IND-507-01 reject",
           "Remove Arjun (or switch back to Single) to get the e-file accepted because 'dad claims him every year'.",
           "Priya is the custodial parent (child lived with her the greater number of nights), no Form 8332 / written release signed, "
           "so only she may claim Arjun (dependency, CTC, EIC, HOH). Document the reject, paper-file the same return with the "
           "school/lease support retained; IRS will resolve the duplicate with the father (CP87A).",
           "EIC + CTC + HOH benefit preserved", ["filing method", "27a", "28", "19"], "medium"),
    gotcha("EVG1002-G3", "Scan - Unstructured PBC / 1099-K", "1099-K for personal items sold at a loss",
           "Treat PayPal 1099-K gross $6,812 as Schedule C gross receipts (SE tax) or other income, or ignore it (CP2000 risk).",
           "Personal-use property sold below cost is not income and the loss is not deductible. Report $6,812 on Schedule 1 line 8z "
           "and the same amount on line 24z ('Form 1099-K personal items sold at a loss') so the 1099-K is matched and AGI is unaffected.",
           "Avoids $6,812 of phantom income (+ SE tax) and preserves EIC", ["Sch 1 8z", "Sch 1 24z", "11"], "medium"),
    gotcha("EVG1002-G4", "Return - Schedule A (state refunds of taxes previously itemized)", "1099-G IL refund $212",
           "Include the $212 state refund on Schedule 1 line 1.",
           "2024 return used the standard deduction -> no tax benefit from the IL tax -> refund not taxable (tax benefit rule). Not reported.",
           "Line 8 overstated $212", ["Sch 1 1"], "easy"),
    gotcha("EVG1002-G5", "Return - Form 8863 education credits", "Lifetime Learning Credit - qualified expenses",
           "Add the $850 laptop to the 1098-T tuition, or skip the credit because box 8 (half-time) is unchecked.",
           "LLC has no half-time requirement (one course is enough). Qualified expenses = tuition & fees paid to the school "
           f"$2,388; the laptop was not required to be purchased from the institution -> not qualified for LLC. LLC = 20% = {fmt(R.forms_value('Form 8863', '19'))}.",
           "LLC", ["Sch 3 line 3"], "medium"),
    gotcha("EVG1002-G6", "Return - credit ordering (Form 8880 / Schedule 8812)", "Saver's credit missed / ordered after CTC",
           "Ignore Form 8880 (401k deferrals code D) or apply it after the CTC so it is wiped out.",
           f"Part-time student (not full-time) with $2,496 elective deferrals and AGI {fmt(v['11'])} (HOH 20% tier) -> saver's credit "
           f"{fmt(R.forms_value('Form 8880', '12'))}. It is subtracted before the CTC on Credit Limit Worksheet A, so more of the "
           f"$2,200 CTC becomes refundable ACTC ({fmt(v['28'])}, capped at $1,700).",
           "ACTC / refund", ["20", "19", "28"], "hard"),
    gotcha("EVG1002-G7", "Return - Schedule B (federal obligations exempt at state level)", "TreasuryDirect interest",
           "Treat I-bond/T-bill interest as tax-exempt federally, or forget the IL subtraction; also the organizer line was blank.",
           "Box 3 interest is taxable federally (line 2b); subtract $310 on IL Schedule M (U.S. obligations). The duplicate 'REPRINT' "
           "1099-INT is the same form - count once.",
           "IL tax on $310 (~$15); federal 2b", ["2b", "IL Sch M"], "easy"),
    gotcha("EVG1002-G8", "SALT Implications - Illinois credits", "IL EIC and IL child tax credit",
           "Stop at IL tax less withholding; miss the refundable IL EIC (20% of federal) and IL child tax credit; or claim the "
           "K-12 education expense credit for $165 of school fees.",
           f"IL EIC {fmt(il_eic)} + IL child tax credit {fmt(il_ctc)} (assumed 40% of IL EIC for 2025); school fees are below the "
           "$250 floor for the K-12 credit.",
           f"IL refund {fmt(il_refund)}", ["IL-1040"], "medium"),
]
C.write_answer_key(R, {"residence": "IL - Naperville (full-year)", "complexity": "Basic W-2 tier + IL; low-income credits",
                       "new_client": True}, gotchas,
    state=state,
    filings=[{"form": "Form 1040 (federal)", "method": "paper (after e-file reject IND-507-01)", "due": "2026-04-15",
              "filed": "2026-03-04"},
             {"form": "IL-1040", "method": "e-file (state-only)", "due": "2026-04-15", "filed": "2026-02-24"}],
    extra={"assumptions": ["IL child tax credit 2025 = 40% of IL EIC (child under 12)",
                           "Saver's credit HOH 20% tier AGI $35,626-$38,250 (Notice 2024-80)"],
           "naive_single_no_dependent_balance_due": naive.values["balance_due"]})

C.write_receipt_log("EVG1002-1040-2025", "A. Novak (staff)", "L. Chen (senior)", "S. Kennedy, CPA", "2026-02-05",
                    extra="Post-filing: e-file reject 02/20/2026 (IND-507-01) logged; paper return mailed 03/04/2026 USPS certified.")

tax16 = v["16"]
C.write_notes(f"""
# EVG1002 - Raman, Priya - 2025 Form 1040 - Preparer Notes

*Synthetic client - Project Evergreen. Return status: **signed off; e-file rejected 02/20/2026 (IND-507-01); paper-filed
03/04/2026 (USPS certified). IL-1040 e-filed state-only 02/24/2026, accepted.***

## Return summary
| | |
|---|---|
| Filing status | **Head of household** (organizer said Single) |
| AGI (line 11) | {fmt(v['11'])} |
| Standard deduction (HOH) | {fmt(v['12e'])} |
| Taxable income | {fmt(v['15'])} |
| Tax (HOH tax table) | {fmt(tax16)} |
| Nonrefundable credits | LLC {fmt(R.forms_value('Form 8863', '19'))} + saver's {fmt(R.forms_value('Form 8880', '12'))} + CTC {fmt(v['19'])} |
| Total tax (line 24) | {fmt(v['24'])} |
| Withholding | {fmt(v['25d'])} |
| EIC (1 child) | {fmt(v['27a'])} |
| ACTC | {fmt(v['28'])} |
| **Federal refund** | **{fmt(v['refund'])}** |
| **IL refund** | **{fmt(il_refund)}** |

## What I did and why (plain English)
1. **Filing status - Head of household.** Priya checked "Single" (her self-prepared 2023/2024 returns were Single with no
   dependent). She is unmarried, pays all the rent/utilities/food (email 02/12) and Arjun lived with her ~315 nights in 2025,
   so she qualifies for HOH - bigger standard deduction ($23,625) and HOH brackets. A Single/no-dependent draft would show a
   balance due of {fmt(naive.values['balance_due'])} instead of a {fmt(v['refund'])} refund.
2. **Arjun - custodial parent rule.** His father says he "claims Arjun every year" because he pays child support. Paying support
   does not matter: the custodial parent (more nights) claims the child unless she signs Form 8332. She never signed anything and
   there is no decree. Priya claims Arjun for dependency, CTC, EIC and HOH. Form 8867 due-diligence questions documented.
3. **E-file reject -> paper file.** Transmitted 02/19; rejected 02/20 with IND-507-01 (Arjun's SSN already used - Rohan filed first).
   Per the procedure (*Paper Filing Returns - dependent already claimed but rightfully claimable*), we documented the reject,
   obtained the school enrollment letter (WP 17), printed the government copy and mailed it 03/04/2026 (certified). Priya was told
   to expect a longer processing time and possibly an IRS letter asking for proof of residency (keep the lease + school letter).
4. **Wages (phone photo W-2).** Only a photo was provided; all boxes were legible except 18-20 (blank - no local tax). Box 1
   {fmt(r(w2b['1']))} = gross less 401(k) (code D $2,496) and Section 125 premiums ($2,964). Box 1 ties to 41,600 - 2,496 - 2,964.
5. **Interest.** TreasuryDirect box 3 $310.46 (I bonds redeemed + T-bills) is federally taxable; the organizer line was blank but the
   1099-INT was in the PBC (a second "REPRINT" copy was the same form - counted once). Alliant CU $12.30. Total {fmt(v['2b'])}.
6. **PayPal 1099-K ($6,812).** Facebook Marketplace sales of her own used furniture and baby gear, all sold well below what she
   paid (CSV WP 9). No gain -> not income; a loss on personal items is not deductible. Reported on Schedule 1 line 8z and
   backed out on line 24z so the IRS matching program sees the 1099-K. Not a business -> no Schedule C / SE tax. (The 2025 1099-K
   threshold is $20,000 and 200 transactions - PayPal issued the form anyway.)
7. **1099-G IL refund $212.** Not taxable - she took the standard deduction in 2024 (no tax benefit).
8. **Lifetime Learning Credit.** College of DuPage 1098-T box 1 $2,388 (part-time; LLC does not need half-time). The laptop was not
   purchased from the college as a condition of enrollment, so it is **not** an LLC expense. LLC 20% x $2,388 = {fmt(R.forms_value('Form 8863', '19'))}.
9. **Saver's credit (Form 8880).** She is not a full-time student, is 31, and deferred $2,496 into her 401(k). AGI {fmt(v['11'])}
   falls in the HOH 20% tier -> {fmt(R.forms_value('Form 8880', '12'))}. Schedule 8812 Credit Limit Worksheet A subtracts the 8880 credit
   (with the LLC) before the CTC, which leaves only {fmt(v['19'])} of tax for the nonrefundable CTC; the rest of the $2,200 is ACTC
   {fmt(v['28'])} (refundable cap $1,700; 15% x (earned income - $2,500) is not limiting). Net CTC benefit {fmt(v['19'] + v['28'])}.
10. **EIC.** 1 qualifying child; earned income {fmt(r(w2b['1']))}, AGI {fmt(v['11'])} - both in the phase-out range; the smaller
   table amount (AGI) applies -> {fmt(v['27a'])}. Investment income ${r(interest_td + interest_cu)} is far below $11,950.
   Refund will not be released before mid-February (PATH Act) - moot given paper filing.
11. **Illinois.** Base income = federal AGI less the U.S. Treasury interest ($310, Schedule M). Exemptions 2 x $2,850. Tax 4.95%
   = {fmt(il_tax)}. Refundable IL EIC 20% of federal = {fmt(il_eic)}; IL child tax credit {fmt(il_ctc)} (**assumption:** 40% of IL EIC
   for 2025, child under 12 - verify on final Schedule IL-E/EIC). K-12 education credit: $165 of qualifying fees (field trip not
   qualified) is below the $250 floor -> $0. Renter -> no property tax credit. IL refund {fmt(il_refund)}. The IL-1040 was transmitted
   separately as a state-only (unlinked) e-file and was accepted.

## Open items / client communication
- **Offer 1040-X for 2023 and 2024** (HOH + EIC + CTC were missed on her self-prepared returns). Refund statute: 2022 claim window
  closes 04/18/2026, 2023 04/15/2027, 2024 04/15/2028. Quoted separately (new 1040-X project codes) - client considering; likely to
  trigger a dispute with the father's returns, explained to her.
- Priya to keep the lease, school letter and custody notes; if IRS sends a Letter 4800C / audit of the EIC, bring it to us
  (separate NOTICE project).
- Suggest she tell Rohan he cannot claim Arjun without a signed Form 8332.

## Hand-off to signer / routing
- [x] Return locked; Accountant's copy saved as *reviewed*
- [x] Federal 1040 - **PAPER** (after IND-507-01 reject) - government copy printed, signed by client 03/03, mailed 03/04 certified
- [x] IL-1040 - e-file state-only, accepted 02/25/2026
- [x] No FBAR; due date 04/15/2026 met
- [x] Form 8879 (IL) eSign; federal paper return wet-signed at our office
- [x] Contact: text/phone (630) 555-0187
- Billing: basic W-2 tier $1,200 + IL $250 + paper-filing/reject handling 0.5 hr (client-chargeable - external reason: another
  person claimed the dependent). 1040-X quotes to go in a separate MISC/1040-X project. Consider courtesy discount (VITA referral).
""")
C.write_review_points(f"""
# Review Points - EVG1002 - 2025 - Form 1040

*Reviewer: L. Chen (blue). Preparer responses in red. Synthetic.*

1. **Filing status / Organizer** - First draft was Single with no dependent (copied from the organizer and her PY return).
   - She is unmarried, pays the household costs and Arjun lived with her all year - HOH with Arjun as qualifying child. Get the
     residency facts in writing (nights, who pays rent) and complete Form 8867.
   - *Preparer: Emailed 02/10; answers received 02/12 (WP 15). Changed to HOH, added Arjun, 8867 completed.*
2. **Dependent claimed by father** - Text from Rohan (WP 14) says he will claim Arjun. Supporting the child financially does not
   give him the claim - custodial parent rule, no 8332. Keep Arjun on our return. If e-file rejects, follow *Paper Filing Returns*.
   - *Preparer: Rejected 02/20 (IND-507-01). School letter obtained 02/24; paper return mailed 03/04. Reject documented in WP.*
3. **Schedule 1 / 1099-K** - Draft put the PayPal $6,812 on Schedule 1 line 3 as business income (autoflow default) with SE tax.
   - These are personal items sold at a loss (CSV WP 9). Report on line 8z and offset on line 24z; no Schedule C.
   - *Preparer: Done - AGI now {fmt(v['11'])}; SE tax removed; EIC recomputed.*
4. **Form 8863** - Draft included the $850 laptop in LLC expenses. Not paid to the institution as a condition of enrollment -
   remove. Box 8 unchecked does not matter for LLC.
   - *Preparer: Removed; qualified expenses $2,388.*
5. **Form 8880 / 8812** - Saver's credit was missing (401k code D $2,496). Add it and check the credit ordering - 8880 comes
   before the CTC on Credit Limit Worksheet A, so ACTC should go up.
   - *Preparer: Added {fmt(R.forms_value('Form 8880', '12'))}; ACTC now {fmt(v['28'])}.*
6. **Schedule 1 line 1** - Draft picked up the IL 1099-G $212. PY standard deduction - not taxable. Remove.
   - *Preparer: Removed.*
7. **IL-1040** - Add Schedule M subtraction for the TreasuryDirect interest ($310) and the IL EIC / IL child tax credit. Document
   the 40% IL CTC assumption in the WP. Do not claim the K-12 credit (under $250).
   - *Preparer: Done - IL refund {fmt(il_refund)}.*
8. FYI - Offer 1040-X for 2023-2024 in a separate project; note the 2022 window closes 04/18/2026.
""")
print("EVG1002 done", R.summary()["24"], v["refund"], "IL refund", il_refund)
