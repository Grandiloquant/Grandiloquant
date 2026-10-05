"""EVG1001 - Marcus & Tanya Bell (MFJ, Texas). W-2 family; OBBBA overtime + car-loan deductions; newborn;
duplicate W-2; recurring 1099-INT missing from PBC; dependent-care FSA offset on Form 2441."""
from common import ClientBuild, gotcha, fmt
from docs import statement, scanned_pages, write_text
import forms as F
from tax2025 import Return1040, r

C = ClientBuild("EVG1001", "Bell", "Marcus & Tanya Bell")
ADDR = ("4417 Pecan Hollow Dr", "Round Rock, TX 78665")
T = {"name": "Marcus D. Bell", "ssn": "XXX-XX-4471", "dob": "1988-04-12"}
S = {"name": "Tanya R. Bell", "ssn": "XXX-XX-9023", "dob": "1990-09-03"}
REC_T = [T["name"], *ADDR, f"TIN: {T['ssn']}"]
REC_S = [S["name"], *ADDR, f"TIN: {S['ssn']}"]
REC_J = ["Marcus D. & Tanya R. Bell", *ADDR, f"TIN: {T['ssn']}"]

# ------------------------------------------------------------------ PERM
C.write_profile(f"""
# EVG1001 - Bell, Marcus & Tanya  (PERM)

*Synthetic client - Project Evergreen training data.*

| Item | Detail |
|---|---|
| Client ID | EVG1001 |
| Taxpayer | Marcus D. Bell, DOB 04/12/1988, SSN XXX-XX-4471, Warehouse Operations Supervisor (hourly, non-exempt) |
| Spouse | Tanya R. Bell, DOB 09/03/1990, SSN XXX-XX-9023, Dental Hygienist |
| Address | {ADDR[0]}, {ADDR[1]} (Williamson County) - resident all years; **Texas: no individual income tax return** |
| Dependents (per PY return) | Jaylen Bell (son, DOB 06/20/2015), Maya Bell (daughter, DOB 02/11/2019) |
| Contact | Tanya preferred - email tanya.bell@example.com, (512) 555-0144; eSign OK |
| Referral | Referred by existing client Oscar Diaz (EVG0874), co-worker of Marcus |
| Engagement | Client since 2023. Basic W-2 return tier (quote $1,200). |
| Payment info | Voided check on file (Ally checking ending 2210) - refunds by direct deposit |
| Prior CPA | TurboTax self-prepared through 2022 |
""")
F.prior_year_summary(C.perm_file("2024_Form_1040_Return_Summary.pdf", "Prior-year return summary"), "Marcus & Tanya Bell",
    "EVG1001", "Married filing jointly", [
        ["1a", "W-2 wages (Lone Star Distribution; Brightsmile Dental)", 101240],
        ["2b", "Taxable interest - Ally Bank (savings 5591) $980; Chase $31", 1011],
        ["11", "AGI", 102251], ["12", "Standard deduction", 29200], ["15", "Taxable income", 73051],
        ["19", "Child tax credit (2 children)", 4000], ["Sch 3 / 2441", "Dependent care credit (after $5,000 FSA exclusion)", 200],
        ["35a", "Refund", 3902]],
    notes="PY WP: Ally Bank savings interest is recurring (HYSA ~$25k balance). Tanya has a dependent-care FSA each year. "
          "HSA through Marcus' employer (family HDHP).")

# ------------------------------------------------------------------ PBC documents
EMP_T = {"name": "Lone Star Distribution LLC", "addr1": "1200 Logistics Pkwy", "addr2": "Austin, TX 78744", "ein": "00-4417290"}
EMP_S = {"name": "Brightsmile Dental PLLC", "addr1": "880 University Blvd Ste 110", "addr2": "Round Rock, TX 78665", "ein": "00-7730215"}
EE_T = {"name": T["name"], "addr1": ADDR[0], "addr2": ADDR[1], "ssn": T["ssn"]}
EE_S = {"name": S["name"], "addr1": ADDR[0], "addr2": ADDR[1], "ssn": S["ssn"]}

w2_t = {"1": 58477.50, "2": 3960.00, "3": 61850.00, "4": 3834.70, "5": 61850.00, "6": 896.83,
        "12": [("D", 3372.50), ("W", 3000.00), ("DD", 14812.00)], "13": ["Retirement plan: X"],
        "14": [("OVERTIME", 9450.00), ("SEC125", 3600.00)], "control": "LSD-000871"}
w2_s = {"1": 47000.00, "2": 2810.00, "3": 47000.00, "4": 2914.00, "5": 47000.00, "6": 681.50, "10": 5000.00,
        "12": [("AA", 2600.00), ("DD", 7200.00)], "13": ["Retirement plan: X"], "control": "BSD-22-014"}

F.organizer(C.pbc_file("01_2025_Organizer_completed.pdf", "Client organizer", "2026-02-02"), "Marcus & Tanya Bell", "EVG1001",
    general=[("Did your marital status change during 2025?", "No", ""),
             ("Were there any changes in dependents?", "No", ""),
             ("Did you receive any Forms 1099-INT/DIV/B?", "Yes", "Chase checking"),
             ("Did you buy a vehicle in 2025?", "Yes", "New truck in March - loan statement attached"),
             ("Did you pay for childcare?", "Yes", "After-school + camps (receipts attached)"),
             ("Did you have an HSA?", "Yes", "Through Marcus' job"),
             ("Did you receive, sell, exchange digital assets?", "No", ""),
             ("Did you make estimated tax payments?", "No", "")],
    dependents=[["Jaylen Bell", "Son", "06/20/2015", "7781", "12", "No"],
                ["Maya Bell", "Daughter", "02/11/2019", "6120", "12", "No"]],
    income_rows=[["Wages", "Lone Star Distribution LLC", 55890, "see W-2"],
                 ["Wages", "Brightsmile Dental PLLC", 45350, "see W-2"],
                 ["Interest", "Ally Bank", 980, ""],
                 ["Interest", "JPMorgan Chase Bank", 31, "38"]],
    deductions_rows=[["Dependent care", "Kids Kampus / camps", 5400, "see receipts"],
                     ["HSA contributions", "via payroll", 3000, "same"]],
    signature_date="01/30/2026")

F.w2(C.pbc_file("02_W-2_Lone_Star_Distribution_Marcus.pdf", "Form W-2", "2026-02-02"), EMP_T, EE_T, w2_t)
F.w2(C.pbc_file("03_W-2_Brightsmile_Dental_Tanya.pdf", "Form W-2", "2026-02-02"), EMP_S, EE_S, w2_s)
# duplicate - phone photo of the same W-2 uploaded again a week later
scanned_pages(C.pbc_file("04_IMG_4471_tanya_w2.pdf", "Photo upload (image)", "2026-02-09", "Client email attachment",
                         "client emailed phone photo"),
    [["Form W-2  Wage and Tax Statement   2025          Copy B",
      "Employer: Brightsmile Dental PLLC   EIN 00-7730215",
      "880 University Blvd Ste 110, Round Rock TX 78665",
      "Employee: Tanya R. Bell   SSN XXX-XX-9023",
      "4417 Pecan Hollow Dr, Round Rock TX 78665",
      "",
      "1 Wages, tips, other comp      47000.00",
      "2 Federal income tax withheld   2810.00",
      "3 Social security wages        47000.00",
      "4 Social security tax withheld  2914.00",
      "5 Medicare wages and tips      47000.00",
      "6 Medicare tax withheld          681.50",
      "10 Dependent care benefits      5000.00",
      "12a AA 2600.00     12b DD 7200.00",
      "13 Retirement plan [X]",
      "Control no. BSD-22-014"]], handwritten=False, skew=2.3, seed=11)
F.f1099_int(C.pbc_file("05_1099-INT_Chase.pdf", "Form 1099-INT", "2026-02-02"),
            ["JPMorgan Chase Bank, N.A.", "PO Box 659754", "San Antonio, TX 78265", "TIN: 00-0000001"], REC_T, {"1": 38.42},
            account="****8812")
F.f1099_sa(C.pbc_file("06_1099-SA_HSA_Bank.pdf", "Form 1099-SA", "2026-02-02"),
           ["HSA Bank", "605 N 8th St", "Sheboygan, WI 53081", "TIN: 00-3920118"], REC_T, {"1": 1150.00, "3": "1"}, account="HSA-****3310")
F.f5498_sa(C.pbc_file("07_5498-SA_HSA_Bank.pdf", "Form 5498-SA", "2026-05-20", note="arrived after main batch"),
           ["HSA Bank", "605 N 8th St", "Sheboygan, WI 53081", "TIN: 00-3920118"], REC_T, {"2": 3000.00, "5": 6842.55})
statement(C.pbc_file("08_Ford_Credit_2025_Interest_Statement_F150.pdf", "Lender interest statement", "2026-02-02"),
    "Ford Motor Credit Company LLC - 2025 Annual Interest Statement", [
        {"table": [["Field", "Value"], ["Borrower(s)", "Marcus D. Bell; Tanya R. Bell"], ["Account", "****5518"],
                   ["Vehicle", "2025 Ford F-150 XLT SuperCrew 4x4 (NEW)"], ["VIN", "1FTFW1E58SFA10393"],
                   ["Contract / purchase date", "03/08/2025"], ["Original amount financed", 48250.00],
                   ["Lien", "First lien on vehicle"], ["Interest paid 01/01/2025 - 12/31/2025", 2452.18],
                   ["Principal balance 12/31/2025", 42106.77]], "left_align_cols": [0, 1]},
        {"para": "This statement is provided for informational purposes to assist borrowers who may claim the deduction for "
                 "qualified passenger vehicle loan interest. Final assembly location per Monroney label: Dearborn, Michigan, USA."}])
statement(C.pbc_file("09_Honda_Financial_2025_Interest_Statement_CRV.pdf", "Lender interest statement", "2026-02-02"),
    "American Honda Finance Corporation - 2025 Year-End Statement", [
        {"table": [["Field", "Value"], ["Borrower", "Tanya R. Bell"], ["Account", "****0937"],
                   ["Vehicle", "2022 Honda CR-V EX (pre-owned)"], ["VIN", "7FARW2H56NE00417"],
                   ["Contract date", "06/14/2024"], ["Interest paid in 2025", 1104.77], ["Balance 12/31/2025", 16203.40]],
         "left_align_cols": [0, 1]}])
statement(C.pbc_file("10_Childcare_receipts_2025.pdf", "Provider statements", "2026-02-02"),
    "2025 Child Care / Camp Payment Statements (compiled by client)", [
        {"heading": "Kids Kampus After-School Program  (EIN 00-6618204, 1800 Gattis School Rd, Round Rock TX)",
         "table": [["Child", "Period", "Amount paid"], ["Maya Bell", "Jan-May, Aug-Dec 2025 (after-school)", 4200.00]]},
        {"heading": "Camp Cedar Ridge (EIN 00-5512093, Georgetown TX)",
         "table": [["Child / Program", "Dates", "Amount paid"],
                   ["Jaylen - Summer Day Camp (8:00-5:30)", "06/09-07/03/2025", 1300.00],
                   ["Maya - Summer Day Camp (8:00-5:30)", "06/09-07/03/2025", 1300.00],
                   ["Jaylen - Adventure Week (overnight, 6 nights)", "07/13-07/19/2025", 1400.00],
                   ["Total", "", 5400.00]], "total_row": True},
        {"para": "Tanya's note: 'FSA reimbursed $5,000 of this. Total we paid was $9,600.'"}])
# client follow-ups
write_text(C.pbc_file("11_Email_from_Tanya_2026-02-11.txt", "Client correspondence", "2026-02-11", "Email"),
"""From: Tanya Bell <tanya.bell@example.com>
To: preparer@evergreentax.example
Date: Wed, 11 Feb 2026 19:42:10 -0600
Subject: Re: Bell 2025 taxes - one more thing!!

Hi! Sorry, I forgot to put this on the organizer - we had our baby boy in December!! Noah James Bell,
born 12/18/2025 at St. David's Round Rock. His social security card came last week (attached).
SSN ends in 3386.

Also I sent my W-2 twice I think, sorry about that. Let me know if you need anything else.
Tanya
[attachment: Noah_SS_card.jpg - retained in PERM, not reproduced]
""")
write_text(C.pbc_file("12_Email_thread_Ally_1099-INT_2026-03-04.txt", "Client correspondence + doc", "2026-03-04", "Email",
                      "requested by preparer 02/24"),
"""From: preparer@evergreentax.example
To: Tanya Bell
Date: Tue, 24 Feb 2026 10:05:00 -0600
Subject: Bell 2025 - open item

Hi Tanya - your 2024 return included interest from your Ally Bank savings account (ending 5591), but we did not
receive a 2025 Form 1099-INT from Ally and the organizer line was left blank. Did the account still earn interest in
2025? If so, please download the 1099-INT from Ally's Documents tab and upload it to Sharefile.

-----
From: Tanya Bell
Date: Wed, 4 Mar 2026 08:12:44 -0600
Subject: RE: Bell 2025 - open item

Yes still have it! Uploaded. It says $1,246.19.
""")
F.f1099_int(C.pbc_file("13_1099-INT_Ally_Bank.pdf", "Form 1099-INT", "2026-03-04"),
            ["Ally Bank", "PO Box 951", "Horsham, PA 19044", "TIN: 00-0000002"], REC_T, {"1": 1246.19}, account="****5591")

# ------------------------------------------------------------------ RETURN
facts = {
    "status": "MFJ",
    "taxpayer": {"age65": False}, "spouse": {"age65": False},
    "dependents": [{"name": "Jaylen Bell", "ctc": True}, {"name": "Maya Bell", "ctc": True},
                   {"name": "Noah Bell", "ctc": True}],
    "w2": [{"who": "T", "box1": w2_t["1"], "box2": w2_t["2"], "box3": w2_t["3"], "box4": w2_t["4"], "box5": w2_t["5"], "box6": w2_t["6"]},
           {"who": "S", "box1": w2_s["1"], "box2": w2_s["2"], "box3": w2_s["3"], "box4": w2_s["4"], "box5": w2_s["5"], "box6": w2_s["6"],
            "box10": w2_s["10"]}],
    "interest": [{"payer": "Ally Bank", "amount": 1246.19}, {"payer": "JPMorgan Chase Bank", "amount": 38.42}],
    "dependent_care": {"expenses": 4200 + 1300 + 1300, "n_qual": 2},
    "sch1a": {"overtime": 9450 / 3, "car_interest": 2452.18, "vin": "1FTFW1E58SFA10393"},
}
R = Return1040(facts).compute()
v = R.values

hsa_8889 = [["Form 8889 (Marcus - family HDHP coverage all 12 months)", "Amount"],
            ["Line 2 HSA contributions you made (not through employer)", 0],
            ["Line 3 Limitation (family, under 55)", 8550],
            ["Line 9 Employer contributions (W-2 box 12 code W, incl. pre-tax payroll)", 3000],
            ["Line 13 HSA deduction", 0],
            ["Line 14a Total distributions (1099-SA)", 1150], ["Line 15 Qualified medical expenses paid", 1150],
            ["Line 16 Taxable HSA distributions", 0]]
car_detail = [["Schedule 1-A Part IV - vehicle loans reviewed", "Interest", "Qualifies?"],
              ["2025 Ford F-150 XLT, VIN 1FTFW1E58SFA10393, new, purchased 03/08/2025, US final assembly (Dearborn MI)", 2452, "Yes"],
              ["2022 Honda CR-V EX, VIN 7FARW2H56NE00417, pre-owned, loan 06/14/2024", 1105, "No - used vehicle / pre-2025 debt"]]
C.write_return(R, [
    ("Taxpayer / Spouse", "Marcus D. Bell (XXX-XX-4471) / Tanya R. Bell (XXX-XX-9023)"),
    ("Address", ", ".join(ADDR)),
    ("Filing status", "Married filing jointly"),
    ("Dependents", "Jaylen (son, 2015) - CTC; Maya (daughter, 2019) - CTC; Noah (son, born 12/18/2025) - CTC"),
    ("Digital assets question", "No"),
    ("Forms included", "1040, Schedule 1-A, Schedule 8812, Schedule 3, Form 2441, Form 8889"),
    ("State", "None - Texas has no individual income tax"),
    ("Filing method", "E-file (Form 8879 signed 04/03/2026); direct deposit to Ally checking ****2210"),
], attachments=[("Form 8889 - Health Savings Accounts", hsa_8889), ("Vehicle loan interest detail", car_detail)])

gotchas = [
    gotcha("EVG1001-G1", "Scan - duplicate documents", "Tanya's W-2 uploaded twice (PDF + phone photo)",
           "Autoflow picks up both documents -> $47,000 wages and $2,810 withholding counted twice.",
           "Mark photo upload as DUP (same EIN, control no., amounts). One W-2 for Brightsmile Dental.",
           "Line 1a overstated $47,000 if missed", ["1a", "25a"], "easy"),
    gotcha("EVG1001-G2", "General Return Prep Notes - blank organizer line with PY amount", "Ally Bank 1099-INT not in initial PBC",
           "Organizer line blank; preparer assumes zero and omits $1,246 of interest (recurring, $980 in 2024).",
           "Open item emailed to client 02/24; 1099-INT received 03/04 and included on line 2b.",
           "Line 2b understated $1,246 -> CP2000 exposure", ["2b"], "medium"),
    gotcha("EVG1001-G3", "Client Interview / dependents", "Newborn not on organizer",
           "Organizer lists 2 dependents; baby born 12/18/2025 only disclosed in a later email.",
           "Add Noah as dependent (child born during the year is treated as living with the taxpayer all year; SSN issued before due date). Third $2,200 CTC.",
           "CTC understated $2,200", ["19"], "medium"),
    gotcha("EVG1001-G4", "OBBBA - no tax on overtime (Schedule 1-A Part III)", "W-2 box 14 shows TOTAL overtime pay",
           "Deduct the full $9,450 box 14 overtime amount.",
           "Only the FLSA premium ('half' of time-and-a-half) qualifies. Box 14 = total OT paid at 1.5x -> premium = 9,450 / 3 = $3,150.",
           "Line 13b overstated by $6,300", ["13b"], "hard"),
    gotcha("EVG1001-G5", "OBBBA - car loan interest (Schedule 1-A Part IV)", "Two vehicle loans, only one qualifies",
           "Deduct both loans ($3,557) or neither.",
           "F-150: new, 2025 purchase, US final assembly, personal use, VIN reported -> $2,452 deductible. CR-V: used vehicle, 2024 loan -> not qualified.",
           "Line 13b", ["13b"], "medium"),
    gotcha("EVG1001-G6", "Form 2441", "Dependent care FSA and overnight camp",
           "Claim credit on $6,000 of expenses ignoring the $5,000 W-2 box 10 exclusion and including overnight camp.",
           "Exclude $5,000 FSA (box 10) first; credit base = $6,000 cap - $5,000 = $1,000; overnight camp ($1,400) is not a qualified expense. Credit 20% x $1,000 = $200.",
           "Sch 3 line 2: $200 not $1,200", ["20"], "medium"),
    gotcha("EVG1001-G7", "W-2 box 12 codes", "HSA code W includes employee pre-tax payroll deferrals",
           "Take an additional HSA deduction on Schedule 1 line 13 for the $2,000 Marcus 'contributed'.",
           "Code W = employer + cafeteria-plan contributions, already excluded from wages. No Sch 1 deduction. 1099-SA used for qualified medical - nontaxable; Form 8889 still required.",
           "Sch 1 line 13 overstated $2,000-3,000", ["10"], "easy"),
    gotcha("EVG1001-G8", "W-2 box 12 codes", "Roth 401(k) (code AA) is not pre-tax",
           "Subtract $2,600 code AA from wages.", "Code AA is already included in box 1. No adjustment.", "Line 1a", ["1a"], "easy"),
]
C.write_answer_key(R, {"residence": "TX (no state return)", "complexity": "Basic W-2 tier + OBBBA deductions"}, gotchas,
                   filings=[{"form": "Form 1040 (federal)", "method": "e-file", "due": "2026-04-15", "filed": "2026-04-06"}])

C.write_receipt_log("EVG1001-1040-2025", "J. Ortiz (staff)", "L. Chen (senior)", "S. Kennedy, CPA", "2026-02-02")
C.write_notes(f"""
# EVG1001 - Bell, Marcus & Tanya - 2025 Form 1040 - Preparer Notes

*Synthetic client - Project Evergreen. Return status: **signed off, e-filed 04/06/2026, accepted.***

## Return summary
| | |
|---|---|
| Filing status | Married filing jointly |
| AGI (line 11) | {fmt(v['11'])} |
| Deduction | Standard {fmt(v['12e'])} + Schedule 1-A {fmt(v['13b'])} (overtime premium $3,150 + car-loan interest $2,452) |
| Taxable income | {fmt(v['15'])} |
| Tax before credits | {fmt(v['16'])} |
| Credits | CTC {fmt(v['19'])} (3 children) + dependent care {fmt(v['20'])} |
| Total tax | {fmt(v['24'])} |
| Withholding | {fmt(v['25d'])} |
| **Refund** | **{fmt(v['refund'])}** (direct deposit) |

## What I did and why (plain English)
1. **Wages.** Two W-2s: Marcus (Lone Star Distribution) and Tanya (Brightsmile Dental). Tanya also emailed a phone photo of the
   same W-2 (same EIN, control number and amounts) - marked **DUP** and excluded from the autoflow. Box 12 codes reviewed:
   D (401k pre-tax) and W (HSA) are already out of box 1; Tanya's AA (Roth 401k) and both DD amounts need no entry.
2. **Interest.** Chase $38 was in the PBC. The organizer left the Ally Bank line blank, but the PY return had $980 from the same
   HYSA, so I did **not** assume zero - sent an open-item email 02/24; Tanya uploaded the Ally 1099-INT ($1,246.19) on 03/04.
   Total interest $1,285 (under $1,500, Schedule B not required).
3. **New baby.** Noah was born 12/18/2025 and was not on the organizer (Tanya's 02/11 email). A child born during the year counts
   as living with the parents for the entire year; SSN was issued before the return due date, so he is a qualifying child for the
   $2,200 CTC. Three qualifying children -> $6,600, all nonrefundable (no ACTC needed). AGI is far below the $400,000 phase-out.
4. **No tax on overtime (new for 2025, Schedule 1-A Part III).** Marcus' box 14 shows "OVERTIME 9,450.00" - that is total OT pay
   at time-and-a-half. Only the FLSA *premium* (the extra half) qualifies, so deduction = $9,450 / 3 = **$3,150**. For 2025 the IRS
   allows this reasonable-method computation because employers were not required to separately report it. Tanya had no OT.
   MAGI {fmt(v['11'])} is below the $300,000 MFJ phase-out.
5. **Car-loan interest (Schedule 1-A Part IV).** Ford Credit statement: new 2025 F-150, bought 03/08/2025, personal use, first lien,
   final assembly Dearborn MI, VIN reported on Schedule 1-A -> **$2,452** deductible. The Honda CR-V loan is on a *used* vehicle
   financed in 2024 -> not eligible (interest is personal and non-deductible).
6. **Dependent care (Form 2441).** Tanya's W-2 box 10 shows $5,000 FSA - excluded first (no taxable benefits since qualified
   expenses exceed $5,000). Qualified expenses: after-school $4,200 + day camps $2,600 = $6,800; the $1,400 overnight "Adventure
   Week" is **not** a qualified expense. Credit base = $6,000 (2 children) - $5,000 exclusion = $1,000 x 20% = **$200**.
7. **HSA (Form 8889).** Code W $3,000 includes Marcus' own pre-tax payroll deferrals - no additional Schedule 1 deduction.
   1099-SA $1,150 used for medical (code 1) - nontaxable. 5498-SA arrived in May and ties to the $3,000.
8. **Standard vs itemized.** No mortgage (renters), no significant charity - standard deduction $31,500 (OBBBA amount).
9. **State.** Texas - no individual income tax return.

## Open items / client communication
- All open items cleared (Ally 1099-INT received 03/04; Noah SSN received 02/11).
- Reminder sent: if Marcus' employer reports "qualified overtime" separately on 2026 W-2 (box 12 code TT), use that figure next year.

## Hand-off to signer / routing
- [x] Return locked; Accountant's copy saved as *reviewed*
- [x] Federal 1040 - e-file; no state; no FBAR
- [x] Due date 04/15/2026 (no extension needed)
- [x] eSign (Form 8879) - Tanya preferred contact via email
- [x] Direct deposit verified against voided check on file
- Billing: basic tier $1,200 + 0.5 hr for new dependent / OBBBA schedule; nothing to W/O.
""")
C.write_review_points(f"""
# Review Points - EVG1001 - 2025 - Form 1040

*Reviewer: L. Chen (blue). Preparer responses in red. Synthetic.*

1. **WP 3 / W-2s** - Autoflow imported 3 W-2s. Two are the same Brightsmile Dental W-2 (PDF + phone photo, control no. BSD-22-014).
   - Remove the duplicate; wages should be $105,478, withholding $6,770.
   - *Preparer: Done - photo bookmarked DUP.*
2. **Schedule B / Organizer** - PY had Ally Bank interest $980. Organizer blank, no 1099 in PBC. Do not assume $0.
   - *Preparer: Open-item email sent 02/24; 1099-INT $1,246.19 received 03/04 and entered.*
3. **Dependents** - Tanya's 02/11 email: baby born 12/18/2025. Add Noah (SSN on file) and recompute Schedule 8812.
   - *Preparer: Done - CTC now $6,600.*
4. **Schedule 1-A Part III** - First draft deducted $9,450 (full box 14 OT). Only the premium portion qualifies.
   - $9,450 is paid at 1.5x -> premium $3,150. Please document the computation on the W-2 page (calculator tape).
   - *Preparer: Corrected to $3,150; tape added to WP 3.*
5. **Schedule 1-A Part IV** - Draft included Honda CR-V interest. Used vehicle / 2024 loan - not qualified. Keep F-150 only; confirm VIN entered.
   - *Preparer: Removed Honda; VIN entered.*
6. **Form 2441** - Draft credit $1,200 ignored the $5,000 box 10 FSA and included the overnight camp. Recompute.
   - *Preparer: Credit now $200.*
7. FYI - Code W includes the employee's cafeteria-plan HSA deferral; no Schedule 1 line 13 deduction. Form 8889 still required.
""")
print("EVG1001 done", R.summary()["24"], v["refund"])
