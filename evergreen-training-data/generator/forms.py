"""
Builders for specific tax documents, on top of docs.info_form / docs.statement.
Every builder takes a path and plain dict/keyword data so client scripts stay readable.
"""
from __future__ import annotations

from docs import info_form, statement, money

FIRM = "Evergreen Tax (synthetic CPA firm)"


def _p(name, addr1, addr2, tin_label="TIN", tin="", phone=None):
    out = [name, addr1, addr2]
    if phone:
        out.append(phone)
    out.append(f"{tin_label}: {tin}")
    return out


# ----------------------------------------------------------------- W-2
def w2(path, employer, employee, b, corrected=False, copy_label="Copy B - To Be Filed With Employee's FEDERAL Tax Return",
       watermark=None, notes=None):
    """employer: dict(name, addr1, addr2, ein, state_id); employee: dict(name, addr1, addr2, ssn);
    b: dict of boxes: 1..11, 12 (list of (code, amt)), 13 (list), 14 (list of (label, amt)), 15-20 state/local rows."""
    boxes = [
        ("1", "Wages, tips, other comp.", b.get("1", 0)), ("2", "Federal income tax withheld", b.get("2", 0)),
        ("3", "Social security wages", b.get("3", 0)), ("4", "Social security tax withheld", b.get("4", 0)),
        ("5", "Medicare wages and tips", b.get("5", 0)), ("6", "Medicare tax withheld", b.get("6", 0)),
        ("7", "Social security tips", b.get("7", "")), ("8", "Allocated tips", b.get("8", "")),
        ("9", "", ""), ("10", "Dependent care benefits", b.get("10", "")),
        ("11", "Nonqualified plans", b.get("11", "")), ("13", "Stat. emp / Ret. plan / 3rd-party sick",
                                                          " / ".join(b.get("13", [])) or ""),
    ]
    for code, amt in b.get("12", []):
        boxes.append(("12", f"Code {code}", f"{code}  {money(amt)}"))
    for lbl, amt in b.get("14", []):
        boxes.append(("14", f"Other: {lbl}", money(amt) if isinstance(amt, (int, float)) else amt))
    for row in b.get("state", []):
        boxes.append(("15", "State / Employer state ID", f"{row['state']}  {row.get('id','')}"))
        boxes.append(("16/17", "State wages / State income tax", f"{money(row.get('wages',''))} / {money(row.get('tax',''))}"))
    for row in b.get("local", []):
        boxes.append(("18/19", "Local wages / Local income tax", f"{money(row.get('wages',''))} / {money(row.get('tax',''))}"))
        boxes.append(("20", "Locality name", row.get("name", "")))
    info_form(path, "W-2", "Wage and Tax Statement", payer=[
        "c Employer's name, address, and ZIP code", employer["name"], employer["addr1"], employer["addr2"],
        f"b EIN: {employer['ein']}"],
        recipient=["e/f Employee's name, address, and ZIP code", employee["name"], employee["addr1"], employee["addr2"],
                   f"a SSN: {employee['ssn']}"],
        boxes=boxes, corrected=corrected, copy_label=copy_label, omb="OMB No. 1545-0008",
        watermark_dup=watermark, notes=notes, extra_left=[("d Control number", [b.get("control", "")])])


# ----------------------------------------------------------------- generic 1099
def f1099(path, form_no, title, payer, recipient, boxes, corrected=False, account=None, notes=None,
          copy_label="Copy B - For Recipient", watermark=None, omb=""):
    info_form(path, form_no, title,
              payer=["PAYER'S name, street address, city, state, ZIP, telephone"] + payer,
              recipient=["RECIPIENT'S name, street address, city, state, ZIP"] + recipient,
              boxes=boxes, corrected=corrected, account_no=account, notes=notes, copy_label=copy_label,
              watermark_dup=watermark, omb=omb)


def f1099_int(path, payer, recipient, b, **kw):
    boxes = [("1", "Interest income", b.get("1", 0)), ("2", "Early withdrawal penalty", b.get("2", "")),
             ("3", "Interest on U.S. Savings Bonds and Treas. obligations", b.get("3", "")),
             ("4", "Federal income tax withheld", b.get("4", "")), ("5", "Investment expenses", b.get("5", "")),
             ("6", "Foreign tax paid", b.get("6", "")), ("7", "Foreign country or U.S. possession", b.get("7", "")),
             ("8", "Tax-exempt interest", b.get("8", "")), ("9", "Specified private activity bond interest", b.get("9", "")),
             ("10", "Market discount", b.get("10", "")), ("11", "Bond premium", b.get("11", "")),
             ("12", "Bond premium on Treasury obligations", b.get("12", "")),
             ("13", "Bond premium on tax-exempt bond", b.get("13", "")), ("14", "Tax-exempt and tax credit bond CUSIP no.", b.get("14", "")),
             ("15-17", "State / State ID / State tax withheld", b.get("state", ""))]
    f1099(path, "1099-INT", "Interest Income", payer, recipient, boxes, omb="OMB No. 1545-0112", **kw)


def f1099_div(path, payer, recipient, b, **kw):
    boxes = [("1a", "Total ordinary dividends", b.get("1a", 0)), ("1b", "Qualified dividends", b.get("1b", 0)),
             ("2a", "Total capital gain distr.", b.get("2a", "")), ("2b", "Unrecap. Sec. 1250 gain", b.get("2b", "")),
             ("2c", "Section 1202 gain", b.get("2c", "")), ("2d", "Collectibles (28%) gain", b.get("2d", "")),
             ("2e", "Section 897 ordinary dividends", b.get("2e", "")), ("2f", "Section 897 capital gain", b.get("2f", "")),
             ("3", "Nondividend distributions", b.get("3", "")), ("4", "Federal income tax withheld", b.get("4", "")),
             ("5", "Section 199A dividends", b.get("5", "")), ("6", "Investment expenses", b.get("6", "")),
             ("7", "Foreign tax paid", b.get("7", "")), ("8", "Foreign country or U.S. possession", b.get("8", "")),
             ("12", "Exempt-interest dividends", b.get("12", "")), ("13", "Specified private activity bond interest dividends", b.get("13", ""))]
    f1099(path, "1099-DIV", "Dividends and Distributions", payer, recipient, boxes, omb="OMB No. 1545-0110", **kw)


def f1099_r(path, payer, recipient, b, **kw):
    boxes = [("1", "Gross distribution", b.get("1", 0)), ("2a", "Taxable amount", b.get("2a", "")),
             ("2b", "Taxable amount not determined / Total distribution", b.get("2b", "")),
             ("3", "Capital gain (included in box 2a)", b.get("3", "")), ("4", "Federal income tax withheld", b.get("4", "")),
             ("5", "Employee contributions / Designated Roth contrib. / insurance premiums", b.get("5", "")),
             ("6", "Net unrealized appreciation", b.get("6", "")), ("7", "Distribution code(s) / IRA/SEP/SIMPLE", b.get("7", "")),
             ("8", "Other", b.get("8", "")), ("9a", "Your percentage of total distribution", b.get("9a", "")),
             ("10", "Amount allocable to IRR within 5 years", b.get("10", "")), ("11", "1st year of desig. Roth contrib.", b.get("11", "")),
             ("12", "FATCA filing requirement", b.get("12", "")), ("13", "Date of payment", b.get("13", "")),
             ("14-16", "State tax withheld / State / State distribution", b.get("state", ""))]
    f1099(path, "1099-R", "Distributions From Pensions, Annuities, Retirement or Profit-Sharing Plans, IRAs, Insurance Contracts, etc.",
          payer, recipient, boxes, omb="OMB No. 1545-0119", **kw)


def f1099_nec(path, payer, recipient, b, **kw):
    boxes = [("1", "Nonemployee compensation", b.get("1", 0)), ("2", "Payer made direct sales totaling $5,000 or more", b.get("2", "")),
             ("3", "Excess golden parachute payments", ""), ("4", "Federal income tax withheld", b.get("4", "")),
             ("5-7", "State tax withheld / State / State income", b.get("state", ""))]
    f1099(path, "1099-NEC", "Nonemployee Compensation", payer, recipient, boxes, omb="OMB No. 1545-0116", **kw)


def f1099_misc(path, payer, recipient, b, **kw):
    boxes = [("1", "Rents", b.get("1", "")), ("2", "Royalties", b.get("2", "")), ("3", "Other income", b.get("3", "")),
             ("4", "Federal income tax withheld", b.get("4", "")), ("6", "Medical and health care payments", b.get("6", "")),
             ("8", "Substitute payments in lieu of dividends", b.get("8", "")), ("10", "Gross proceeds paid to an attorney", b.get("10", "")),
             ("15-17", "State", b.get("state", ""))]
    f1099(path, "1099-MISC", "Miscellaneous Information", payer, recipient, boxes, omb="OMB No. 1545-0115", **kw)


def f1099_g(path, payer, recipient, b, **kw):
    boxes = [("1", "Unemployment compensation", b.get("1", "")), ("2", "State or local income tax refunds, credits, or offsets", b.get("2", "")),
             ("3", "Box 2 amount is for tax year", b.get("3", "")), ("4", "Federal income tax withheld", b.get("4", "")),
             ("5", "RTAA payments", ""), ("6", "Taxable grants", ""), ("7", "Agriculture payments", ""),
             ("8", "Box 2 is trade or business income", b.get("8", "")), ("10a-11", "State / State ID / State tax withheld", b.get("state", ""))]
    f1099(path, "1099-G", "Certain Government Payments", payer, recipient, boxes, omb="OMB No. 1545-0120", **kw)


def f1099_k(path, filer, payee, b, **kw):
    months = b.get("months", [0] * 12)
    boxes = [("1a", "Gross amount of payment card/third party network transactions", b.get("1a", 0)),
             ("1b", "Card Not Present transactions", b.get("1b", "")), ("2", "Merchant category code", b.get("2", "")),
             ("3", "Number of payment transactions", b.get("3", "")), ("4", "Federal income tax withheld", b.get("4", ""))]
    mn = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    for i, m in enumerate(mn):
        boxes.append((f"5{chr(97+i)}", m, months[i]))
    boxes.append(("1a filer type", "PSE / Electronic Payment Facilitator / Other third party", b.get("filer_type", "Third party settlement organization")))
    f1099(path, "1099-K", "Payment Card and Third Party Network Transactions", filer, payee, boxes, omb="OMB No. 1545-2205", **kw)


def f1099_sa(path, payer, recipient, b, **kw):
    boxes = [("1", "Gross distribution", b.get("1", 0)), ("2", "Earnings on excess cont.", b.get("2", "")),
             ("3", "Distribution code", b.get("3", "1")), ("4", "FMV on date of death", b.get("4", "")),
             ("5", "HSA / Archer MSA / MA MSA", b.get("5", "HSA"))]
    f1099(path, "1099-SA", "Distributions From an HSA, Archer MSA, or Medicare Advantage MSA", payer, recipient, boxes, **kw)


def f5498_sa(path, trustee, participant, b, **kw):
    boxes = [("1", "Employee or self-employed person's Archer MSA contributions", ""),
             ("2", "Total contributions made in 2025", b.get("2", 0)), ("3", "Total HSA or Archer MSA contributions made in 2026 for 2025", b.get("3", "")),
             ("4", "Rollover contributions", ""), ("5", "Fair market value of HSA, Archer MSA, or MA MSA", b.get("5", "")),
             ("6", "HSA / Archer MSA / MA MSA", "HSA")]
    info_form(path, "5498-SA", "HSA, Archer MSA, or Medicare Advantage MSA Information",
              payer=["TRUSTEE'S name, street address, city, state, ZIP"] + trustee,
              recipient=["PARTICIPANT'S name, street address, city, state, ZIP"] + participant, boxes=boxes, **kw)


def f1099_s(path, filer, transferor, b, **kw):
    boxes = [("1", "Date of closing", b.get("1", "")), ("2", "Gross proceeds", b.get("2", 0)),
             ("3", "Address (including city, state, ZIP) or legal description", b.get("3", "")),
             ("4", "Transferor received or will receive property or services as part of consideration", b.get("4", "")),
             ("5", "Check here if the transferor is a foreign person", b.get("5", "")),
             ("6", "Buyer's part of real estate tax", b.get("6", ""))]
    info_form(path, "1099-S", "Proceeds From Real Estate Transactions",
              payer=["FILER'S name, street address, city, state, ZIP, telephone"] + filer,
              recipient=["TRANSFEROR'S name, street address, city, state, ZIP"] + transferor, boxes=boxes, **kw)


def f1099_q(path, payer, recipient, b, **kw):
    boxes = [("1", "Gross distribution", b.get("1", 0)), ("2", "Earnings", b.get("2", "")), ("3", "Basis", b.get("3", "")),
             ("4", "Trustee-to-trustee transfer", b.get("4", "")), ("5", "Private / State / Coverdell", b.get("5", "")),
             ("6", "Recipient is not the designated beneficiary", b.get("6", ""))]
    f1099(path, "1099-Q", "Payments From Qualified Education Programs", payer, recipient, boxes, **kw)


def f1098(path, lender, borrower, b, **kw):
    boxes = [("1", "Mortgage interest received from payer(s)/borrower(s)", b.get("1", 0)),
             ("2", "Outstanding mortgage principal", b.get("2", "")), ("3", "Mortgage origination date", b.get("3", "")),
             ("4", "Refund of overpaid interest", b.get("4", "")), ("5", "Mortgage insurance premiums", b.get("5", "")),
             ("6", "Points paid on purchase of principal residence", b.get("6", "")),
             ("7", "Is address of property securing mortgage same as payer's/borrower's address?", b.get("7", "")),
             ("8", "Address or description of property securing mortgage", b.get("8", "")),
             ("9", "Number of properties securing the mortgage", b.get("9", "")), ("10", "Other (real estate taxes / escrow)", b.get("10", "")),
             ("11", "Mortgage acquisition date", b.get("11", ""))]
    info_form(path, "1098", "Mortgage Interest Statement",
              payer=["RECIPIENT'S/LENDER'S name, street address, city, state, ZIP, telephone"] + lender,
              recipient=["PAYER'S/BORROWER'S name, street address, city, state, ZIP"] + borrower, boxes=boxes,
              omb="OMB No. 1545-1380", **kw)


def f1098_t(path, school, student, b, **kw):
    boxes = [("1", "Payments received for qualified tuition and related expenses", b.get("1", 0)),
             ("4", "Adjustments made for a prior year", b.get("4", "")), ("5", "Scholarships or grants", b.get("5", "")),
             ("6", "Adjustments to scholarships or grants for a prior year", b.get("6", "")),
             ("7", "Includes amounts for an academic period beginning Jan-Mar 2026", b.get("7", "")),
             ("8", "At least half-time student", b.get("8", "")), ("9", "Graduate student", b.get("9", "")),
             ("10", "Ins. contract reimb./refund", b.get("10", ""))]
    info_form(path, "1098-T", "Tuition Statement",
              payer=["FILER'S name, street address, city, state, ZIP, telephone"] + school,
              recipient=["STUDENT'S name, street address, city, state, ZIP"] + student, boxes=boxes, **kw)


def f1098_e(path, lender, borrower, b, **kw):
    boxes = [("1", "Student loan interest received by lender", b.get("1", 0)),
             ("2", "If checked, box 1 does not include loan origination fees and/or capitalized interest", b.get("2", ""))]
    info_form(path, "1098-E", "Student Loan Interest Statement",
              payer=["RECIPIENT'S/LENDER'S name, address, telephone"] + lender,
              recipient=["BORROWER'S name, address"] + borrower, boxes=boxes, **kw)


def ssa_1099(path, beneficiary, b, **kw):
    boxes = [("3", "Benefits paid in 2025", b.get("3", 0)), ("4", "Benefits repaid to SSA in 2025", b.get("4", 0)),
             ("5", "Net benefits for 2025 (Box 3 minus Box 4)", b.get("5", 0)),
             ("6", "Voluntary federal income tax withheld", b.get("6", "")),
             ("7", "Address", b.get("7", "")), ("8", "Claim number", b.get("8", ""))]
    desc = b.get("desc", [])
    info_form(path, "SSA-1099", "Social Security Benefit Statement",
              payer=["Social Security Administration", "(synthetic)", "", "", ""],
              recipient=["Box 1 Name / Box 2 Beneficiary's SSN"] + beneficiary, boxes=boxes, notes=desc,
              copy_label="Form SSA-1099 - Social Security Benefit Statement", **kw)


def w2g(path, payer, winner, b, **kw):
    boxes = [("1", "Reportable winnings", b.get("1", 0)), ("2", "Date won", b.get("2", "")),
             ("3", "Type of wager", b.get("3", "")), ("4", "Federal income tax withheld", b.get("4", "")),
             ("5", "Transaction", b.get("5", "")), ("6", "Race", ""), ("7", "Winnings from identical wagers", ""),
             ("8", "Cashier", b.get("8", "")), ("9", "Winner's taxpayer identification no.", b.get("9", "")),
             ("10", "Window", b.get("10", "")), ("13-15", "State / State winnings / State tax withheld", b.get("state", ""))]
    info_form(path, "W-2G", "Certain Gambling Winnings",
              payer=["PAYER'S name, street address, city, state, ZIP, telephone"] + payer,
              recipient=["WINNER'S name, street address, city, state, ZIP"] + winner, boxes=boxes, **kw)


def f1095_a(path, marketplace, recipient, months, policy="", **kw):
    """months: list of 12 tuples (premium, slcsp, aptc)."""
    boxes = []
    mn = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
    tot = [0, 0, 0]
    for i, (a, bb, c) in enumerate(months):
        boxes.append((str(21 + i), f"{mn[i]}: A premium / B SLCSP / C APTC", f"{money(a)} / {money(bb)} / {money(c)}"))
        tot[0] += a; tot[1] += bb; tot[2] += c
    boxes.append(("33", "Annual totals A / B / C", f"{money(tot[0])} / {money(tot[1])} / {money(tot[2])}"))
    info_form(path, "1095-A", "Health Insurance Marketplace Statement",
              payer=["Part I - Marketplace / Policy"] + marketplace + [f"Policy number: {policy}"],
              recipient=["Recipient"] + recipient, boxes=boxes, box_cols=1, **kw)


# ----------------------------------------------------------------- K-1s
def k1_generic(path, form, title, entity, partner, part_ii, boxes, supplemental=None, final=False, amended=False,
               notes=None):
    """Renders a K-1 face page plus supplemental statement pages (as a statement PDF)."""
    sec = [{"heading": "Part I - Information About the Entity", "table": [["Item", "Value"]] + entity, "left_align_cols": [0, 1]},
           {"heading": "Part II - Information About the Partner / Shareholder / Beneficiary",
            "table": [["Item", "Value"]] + partner + part_ii, "left_align_cols": [0, 1]},
           {"heading": "Part III - Share of Current Year Income, Deductions, Credits, and Other Items",
            "table": [["Box", "Description", "Code", "Amount"]] + boxes, "left_align_cols": [0, 1, 2]}]
    flags = []
    if final:
        flags.append("X FINAL K-1")
    if amended:
        flags.append("X AMENDED K-1")
    for s in supplemental or []:
        sec.append(s)
    statement(path, f"Schedule K-1 ({form}) 2025 - {title}", sec,
              subtitle=("  ".join(flags) + "   " if flags else "") + "For calendar year 2025", footer="; ".join(notes or []))


# ----------------------------------------------------------------- Organizer
def organizer(path, client_name, client_id, general, dependents, income_rows, deductions_rows=None, blank=False,
              signature_date=""):
    """income_rows: list of (description, payer, PY 2024 amount, CY 2025 client entry or '')."""
    secs = []
    if blank:
        secs.append({"heading": "BLANK ORGANIZER", "para": "Client opted out of completing the organizer. <b>Blank Organizer</b>"})
    secs.append({"heading": "Beginning Checklist / General Questions (client answers)",
                 "table": [["#", "Question", "Answer", "Client explanation"]] + [[i + 1, q, a, e] for i, (q, a, e) in enumerate(general)],
                 "col_widths": [22, 300, 45, 160], "left_align_cols": [1, 2, 3]})
    secs.append({"heading": "Dependents", "table": [["Name", "Relationship", "DOB", "SSN (last 4)", "Months in home", "Full-time student"]] + dependents,
                 "left_align_cols": [0, 1, 2, 3, 4, 5]})
    secs.append({"heading": "Income - Prior year amounts pre-printed by Evergreen Tax; client to enter 2025",
                 "table": [["Income item", "Payer", "2024 (prior year)", "2025 (client entry)"]] + income_rows,
                 "left_align_cols": [0, 1]})
    if deductions_rows:
        secs.append({"heading": "Deductions / Adjustments / Payments",
                     "table": [["Item", "Detail", "2024 (prior year)", "2025 (client entry)"]] + deductions_rows,
                     "left_align_cols": [0, 1]})
    secs.append({"heading": "Signature", "para": f"Client signature on file: {client_name}   Date: {signature_date}"})
    statement(path, f"2025 Client Tax Organizer - {client_name} ({client_id})", secs,
              subtitle="Prepared from CCH Axcess organizer export (synthetic). Amounts in the 2024 column are from your prior year return.")


def engagement_letter(path, client_name, client_id, fee_text, signed_date, services):
    secs = [{"para": [f"Dear {client_name},",
                      "This letter confirms the terms of our engagement to prepare your 2025 federal and state income tax returns. "
                      "We will prepare the returns from information you furnish to us. We will not audit or otherwise verify the data "
                      "you submit, although we may ask for clarification of some information.",
                      f"<b>Services:</b> {services}",
                      f"<b>Fees:</b> {fee_text} Final billing is based on actual time incurred at the standard hourly rates of the "
                      "staff assigned. Information received within 15 days of a filing deadline is subject to a 15% expedited processing fee.",
                      "You are responsible for the completeness and accuracy of the information provided and for maintaining records "
                      "supporting the returns. Returns will be e-filed unless an exception requires paper filing.",
                      f"Signed and returned by client: <b>{client_name}</b>  Date: <b>{signed_date}</b>"]}]
    statement(path, f"Engagement Letter - Tax Year 2025 - {client_id}", secs, subtitle=FIRM)


def prior_year_summary(path, client_name, client_id, status, rows, carryovers=None, notes=None):
    secs = [{"heading": "2024 Form 1040 - key lines (from filed return)", "table": [["Line", "Description", "Amount"]] + rows,
             "left_align_cols": [0, 1]}]
    if carryovers:
        secs.append({"heading": "Carryovers to 2025", "table": [["Item", "Amount"]] + carryovers, "left_align_cols": [0]})
    if notes:
        secs.append({"heading": "Prior-year preparer notes (PY WP)", "para": notes})
    statement(path, f"2024 Return Summary - {client_name} ({client_id})", secs, subtitle=f"Filing status: {status}")
