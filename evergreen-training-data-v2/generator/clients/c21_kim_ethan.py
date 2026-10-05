"""EVG1021 - Ethan S. Kim (16, dependent of EVG1010 Daniel & Grace Kim), Washington. Separate child return required by the
Kid Taxes procedure: UTMA interest/dividends + a long-term gain from a fund sale + summer W-2 -> Form 8814 not available ->
Form 8615 (kiddie tax) computed with the PARENTS' final 2025 taxable income, filing status, qualified dividends and net
capital gain, imported from c10_kim (the parents' return is computed first)."""
from common import ClientBuild, gotcha, fmt
from docs import statement, write_text
import forms as F
from tax2025 import Return1040, r, KIDDIE_THRESH, DEP_STD_MIN, DEP_STD_EARNED_ADD, tax_with_prefs

import c10_kim as P   # parents' return (EVG1010) - computed first; supplies Form 8615 lines 6-10

C = ClientBuild("EVG1021", "Kim-Ethan", "Ethan S. Kim")
E = P.ETHAN
ADDR = P.ADDR

# ====================================================================== PERM
C.write_profile(f"""
# EVG1021 - Kim, Ethan S.  (PERM)

*Synthetic client - Project Evergreen training data.*

| Item | Detail |
|---|---|
| Client ID | EVG1021 - opened 02/23/2026 (Kid Taxes procedure: child with a separate filing requirement gets its own client ID and 1040 project code) |
| Related client | **EVG1010 - Kim, Daniel & Grace** (parents, MFJ). Ethan is their dependent - parents claim him (CTC). Parents' return must be finalized first (Form 8615) |
| Taxpayer | Ethan S. Kim, DOB 03/14/2009 (age 16 at 12/31/2025), SSN {E['ssn']}, high-school student; summer lifeguard |
| Address | {ADDR[0]}, {ADDR[1]} (lives with parents). Washington: no income tax |
| Accounts | Pioneer Square Brokerage UTMA/WA ****2270 - custodian Grace H. Kim (gifts from grandparents) |
| Prior years | No 2024 Form 1040 filed - Ethan's 2024 interest/dividends ($2,050) were reported on the parents' 2024 return via Form 8814 |
| Contact | Through parent: Grace Kim - grace.kim@example.com, (425) 555-0172. eSign: Ethan signs his own Form 8879 (Grace co-signs engagement as parent/guardian) |
| Engagement | Child return - flat fee $450 (engagement addendum signed 02/24/2026) |
| Payment | Any balance due is paid by the parents from their checking ****6630 (their choice) |
""")
F.prior_year_summary(C.perm_file("2024_Form_1040_Return_Summary.pdf", "Prior-year return summary"), "Ethan S. Kim", "EVG1021",
    "No 2024 return filed (dependent child)", [
        ["-", "No 2024 Form 1040 filed for Ethan", ""],
        ["Parents' 2024 Form 8814", "Ethan: interest $610 + ordinary dividends $1,440 (no sales, no wages)", 2050],
        ["Parents' 2024 Form 8814", "Tax on Ethan's income included on parents' 2024 Form 1040 line 16", 75]],
    notes="No 2024 tax liability of his own and no 2024 return -> 2025 Form 2210 not required (and 2025 balance due < $1,000).")

# ====================================================================== PBC
F.organizer(C.pbc_file("01_2025_Organizer_Ethan_BLANK.pdf", "Client organizer (blank)", "2026-02-24", "Evergreen - created at client setup"),
    "Ethan S. Kim", "EVG1021",
    general=[("Can anyone claim you as a dependent?", "", ""), ("Did you have a job in 2025?", "", ""),
             ("Did you sell any investments?", "", ""), ("Did you make estimated tax payments?", "", "")],
    dependents=[], income_rows=[["Wages", "", "", ""], ["Interest / dividends", "", "", ""]], blank=True, signature_date="")
P.render_ethan_docs(C, received="2026-02-24", source="Copied from EVG1010 Sharefile (parents' upload 02/09/2026)",
                    note="re-filed to new client ID", prefix="02")
F.engagement_letter(C.pbc_file("03_Engagement_Letter_Addendum_Ethan_signed.pdf", "Engagement letter (signed)", "2026-02-24", "DocuSign"),
    "Ethan S. Kim (Grace H. Kim, parent/guardian)", "EVG1021", "Flat fee $450 for the 2025 Form 1040 with Form 8615.",
    "02/24/2026", "2025 federal Form 1040 for a dependent child, including Form 8615 (tax for certain children who have unearned income). "
                  "No state return (Washington). Return will be prepared after the parents' return (EVG1010) is final.")
write_text(C.pbc_file("04_Email_Grace_re_Ethan_return_2026-02-23.txt", "Client correspondence", "2026-02-23", "Email"),
"""From: preparer@evergreentax.example
To: Grace Kim <grace.kim@example.com>
Date: Mon, 23 Feb 2026 11:20:04 -0800
Subject: Kim 2025 - Ethan needs his own return

Hi Grace,

Following up on Friday's call. Last year we reported Ethan's and Chloe's investment income on your return (Form 8814).
That election is only available when a child's income is ONLY interest and dividends. In 2025 Ethan sold part of his
index fund in July (a $3,100 capital gain) and also had his lifeguard W-2, so he has to file his own 2025 return.
Because his investment income is over $2,700, part of it is taxed at your tax rate (the "kiddie tax", Form 8615).
We will set him up as his own client and finish his return right after yours, since his tax depends on your final
taxable income. Estimated tax on his return is a few hundred dollars. Chloe can stay on your return (Form 8814).

Please sign the short engagement addendum for Ethan's return (DocuSign to follow).

-----
From: Grace Kim
Date: Mon, 23 Feb 2026 20:02:37 -0800
Subject: RE: Kim 2025 - Ethan needs his own return

Makes sense - go ahead. We'll pay whatever he owes. He can sign his own e-file form, he's 16 :)
""")

# ====================================================================== RETURN
unearned = r(P.ETHAN_INT) + r(P.ETHAN_ORD) + r(P.ETHAN_SALE["proceeds"] - P.ETHAN_SALE["basis"])
earned = r(P.ETHAN_W2["1"])
dep_std = min(15750, max(DEP_STD_MIN, earned + DEP_STD_EARNED_ADD))
agi_expected = earned + unearned
ti_expected = agi_expected - dep_std
line2 = 2 * DEP_STD_MIN                     # $2,700 (no itemized deductions)
assert line2 == KIDDIE_THRESH
line3 = unearned - line2
nui = min(line3, ti_expected)               # Form 8615 line 5
ratio = nui / unearned                      # share of QD / capital gain included in NUI (8615 line 9 instructions)
ltcg = P.ETHAN_SALE["proceeds"] - P.ETHAN_SALE["basis"]
qd_share = round(P.ETHAN_QUAL * ratio, 2)
cg_share = round(ltcg * ratio, 2)
k = P.PARENT_8615
facts = {
    "status": "S",
    "claimed_as_dependent": True, "earned_for_dep_std": earned,
    "taxpayer": {"age65": False},
    "w2": [{"who": "T", "box1": P.ETHAN_W2["1"], "box2": P.ETHAN_W2["2"], "box3": P.ETHAN_W2["3"], "box4": P.ETHAN_W2["4"],
            "box5": P.ETHAN_W2["5"], "box6": P.ETHAN_W2["6"]}],
    "interest": [{"payer": "Pioneer Square Brokerage (UTMA ****2270)", "amount": P.ETHAN_INT}],
    "dividends": [{"payer": "Pioneer Square Brokerage (UTMA ****2270)", "ordinary": P.ETHAN_ORD, "qualified": P.ETHAN_QUAL}],
    "trades": [{"box": "D", "id": "1", "desc": P.ETHAN_SALE["desc"], "acq": P.ETHAN_SALE["acq"], "sold": P.ETHAN_SALE["sold"],
                "proceeds": P.ETHAN_SALE["proceeds"], "basis": P.ETHAN_SALE["basis"]}],
    "kiddie_8615": {"net_unearned": nui, "parent_ti": k["parent_ti"], "parent_status": k["parent_status"],
                    "parent_qd": k["parent_qd"], "parent_ncg": k["parent_ncg"], "other_children_nui": 0,
                    "child_qd_nui_share": qd_share, "child_ncg_nui_share": cg_share},
}
R = Return1040(facts).compute()
v = R.values
det = R.tax_detail
assert v["11"] == agi_expected and v["12e"] == dep_std and v["15"] == ti_expected, (v["11"], v["12e"], v["15"])
assert det["parent_tax_without"] == k["parent_tax_line16_ex_8814"]   # 8615 line 10 ties to parents' 1040 line 16 less 8814 tax
# hand check of the slice taxed at the parents' rates. The parents' TI is in the 32% bracket, but their ORDINARY income
# (TI less QD and net capital gain) is in the 24% bracket; QD/CG are stacked on top at 15%. Adding the child's NUI adds its
# ordinary part at 24% (still below $394,600) and its QD/CG part at 15%.
p_ord = k["parent_ti"] - k["parent_qd"] - k["parent_ncg"]
nui_ord = nui - qd_share - cg_share
assert 206700 < p_ord and p_ord + nui_ord < 394600 and k["parent_ti"] + nui < 600050
hand = nui_ord * 0.24 + (qd_share + cg_share) * 0.15
assert abs(det["line13_tentative_tax_on_nui"] - hand) <= 1, (det, hand)
naive_32 = r(nui * 0.32)            # common error: all NUI at the parents' top bracket
plain, _ = tax_with_prefs(v["15"], "S", v["3a"], v["sch_d"]["ncg"])

f8615 = [["Form 8615 - Tax for Certain Children Who Have Unearned Income", "Amount"],
         ["Parent: " + k["parent_name"] + " (MFJ) - SSN " + k["parent_ssn"] + " - client EVG1010", ""],
         ["Line 1 Child's unearned income (interest $900 + dividends $2,400 + capital gain $3,100)", unearned],
         ["Line 2 $2,700 (child did not itemize)", line2],
         ["Line 3 Subtract line 2 from line 1", line3],
         ["Line 4 Child's taxable income (Form 1040 line 15)", v["15"]],
         ["Line 5 Net unearned income - smaller of line 3 or line 4", nui],
         ["Line 6 Parent's taxable income (EVG1010 Form 1040 line 15)", k["parent_ti"]],
         ["Line 7 Net unearned income of other children of the parent (Chloe is on Form 8814 - not included)", 0],
         ["Line 8 Add lines 5, 6 and 7", k["parent_ti"] + nui],
         ["Line 9 Tax on line 8 at parent's rates (QDCG worksheet incl. child's QD/CG share)", det["parent_tax_with_nui"]],
         ["Line 10 Parent's tax (Form 1040 line 16, excluding Form 8814 tax)", det["parent_tax_without"]],
         ["Line 11 Subtract line 10 from line 9", det["line13_tentative_tax_on_nui"]],
         ["Line 12a/12b Only child with NUI -> 1.000", 1],
         ["Line 13 Multiply line 11 by line 12b", det["child_share"]],
         ["Line 14 Subtract line 5 from line 4", v["15"] - nui],
         ["Line 15 Tax on line 14 at child's own rates (QDCG worksheet, remaining QD/CG)", det["tax_on_child_TI_less_NUI"]],
         ["Line 16 Add lines 13 and 15", det["line15"]],
         ["Line 17 Tax on line 4 at child's own rates", det["tax_as_if_no_8615"]],
         ["Line 18 Larger of line 16 or line 17 (to Form 1040 line 16, Form 8615 box checked)", det["line18_tax"]],
         [f"Memo: QD / capital gain included in NUI = line 5 / line 1 ({nui:,}/{unearned:,}) x QD $1,900 and x LTCG $3,100", f"{qd_share:,.2f} / {cg_share:,.2f}"]]
std_rows = [["Standard deduction - dependent (Form 1040 instructions worksheet)", "Amount"],
            ["Earned income (W-2 box 1) + $450", earned + DEP_STD_EARNED_ADD], ["Minimum", DEP_STD_MIN],
            ["Larger of the two, not more than $15,750", dep_std],
            ["'Someone can claim you as a dependent' box checked; no CTC/ODC/EITC; not eligible for Schedule 1-A senior items", ""]]
C.write_return(R, [
    ("Taxpayer", f"{E['name']} ({E['ssn']}), DOB 03/14/2009 - dependent of parents (EVG1010)"),
    ("Address", ", ".join(ADDR)),
    ("Filing status", "Single - 'Someone can claim you as a dependent' checked"),
    ("Digital assets question", "No"),
    ("Forms included", "1040, Schedule B (not required - under $1,500 each), Schedule D, Form 8949 (box D), Form 8615"),
    ("Parent information (Form 8615)", f"{k['parent_name']}, MFJ, SSN {k['parent_ssn']} - parents' 2025 taxable income {fmt(k['parent_ti'])}"),
    ("State", "None - Washington has no individual income tax"),
    ("Filing method", "E-file (Form 8879 signed by Ethan 04/12/2026); balance due paid by parents' direct debit 04/15/2026"),
], attachments=[("Form 8615 - line by line", f8615), ("Dependent standard deduction", std_rows)])

gotchas = [
    gotcha("EVG1021-G1", "Review - Kid Taxes and Filings (separate client ID / project code)", "Child needs his own return",
           "Report Ethan's income on the parents' Form 8814 like 2024, or skip his return because 'he's a dependent'.",
           "Capital gain from a sale + wages -> Form 8814 not allowed. Unearned income $6,400 > $1,350 filing threshold and > $2,700 kiddie "
           "threshold -> separate Form 1040 with Form 8615, under its own client ID (EVG1021) and 1040 project code, after discussing with parents.",
           "Entire return", ["16"], "medium"),
    gotcha("EVG1021-G2", "Kid Taxes - Form 8615 using parents' return", "Parents' rate from the FINAL parents' return",
           "Tax all of Ethan's income at his own 10%/0% rates, or use an estimated/prior-year parent taxable income.",
           f"Form 8615 line 6 = parents' 2025 taxable income {fmt(k['parent_ti'])} (EVG1010, MFJ); line 10 = parents' tax {fmt(det['parent_tax_without'])} "
           f"excluding the $55 Form 8814 tax. NUI {fmt(nui)} taxed at the parents' marginal rates -> {fmt(det['line13_tentative_tax_on_nui'])}. "
           "If the parents' return changes (amended), Ethan's return must be amended too.",
           f"Tax {fmt(v['16'])} vs {fmt(plain)} without Form 8615", ["16"], "hard"),
    gotcha("EVG1021-G3", "Kid Taxes - Form 8615 (QD / capital gain)", "Preferential rates keep applying inside Form 8615",
           "Tax the whole $3,700 of NUI at the parents' top bracket (their taxable income is in the 32% bracket).",
           f"The share of qualified dividends ({qd_share:,.2f}) and capital gain ({cg_share:,.2f}) included in NUI (line 5 / line 1) is taxed at "
           "the parents' 15% capital gain rate on line 9. The ordinary part is taxed at 24%, not 32%: the parents' ORDINARY income "
           f"(TI less QD/CG = {fmt(p_ord)}) is in the 24% bracket because the QDCG worksheet stacks QD/CG on top. The rest of the child's QD/CG is taxed at his "
           "own 0% rate on line 15.",
           f"Line 11 {fmt(det['line13_tentative_tax_on_nui'])} vs {fmt(naive_32)} if all NUI at 32%", ["16"], "hard"),
    gotcha("EVG1021-G4", "Standard deduction - dependent", "Dependent standard deduction",
           "Use the full $15,750 single standard deduction (-> $0 taxable income), or the $1,350 minimum ignoring wages.",
           f"Dependent: greater of $1,350 or earned income + $450 = {fmt(dep_std)} (capped at $15,750). Taxable income {fmt(v['15'])}.",
           "Taxable income", ["12e", "15"], "easy"),
    gotcha("EVG1021-G5", "Kid Taxes - Form 8615 line 1", "Only unearned income is subject to kiddie tax",
           "Include the $3,200 lifeguard wages in Form 8615 line 1.",
           "Line 1 = unearned income only ($900 + $2,400 + $3,100 = $6,400). Wages are taxed at the child's own rates (line 14/15).",
           "Line 16", ["16"], "medium"),
    gotcha("EVG1021-G6", "Filing - dependent return", "Dependent checkbox / no credits for the child",
           "Leave the 'can be claimed as a dependent' box unchecked, or claim his own personal credits.",
           "Check the box on page 1 (the parents claim him and the CTC). No CTC/EITC on his return; Form 8615 lists the parent's name/SSN. "
           f"Balance due {fmt(v['balance_due'])} < $1,000 and no 2024 liability -> no Form 2210.",
           "E-file consistency with EVG1010 (duplicate-dependent rejects)", ["19"], "easy"),
]
C.write_answer_key(R, {"residence": "WA (no state income tax return)", "complexity": "Dependent child - Form 8615",
                       "related_clients": ["EVG1010 (parents - Form 8615 parent data)"]}, gotchas,
                   filings=[{"form": "Form 1040 with Form 8615 (federal)", "method": "e-file", "due": "2026-04-15", "filed": "2026-04-14"}],
                   extra={"form_8615_parent_data_used": k,
                          "form_8615_child_shares": {"nui": nui, "qd_in_nui": qd_share, "ltcg_in_nui": cg_share}})
C.write_receipt_log("EVG1021-1040-2025", "P. Anand (staff)", "M. Okafor (senior)", "S. Kennedy, CPA", "2026-02-24",
                    extra="Client ID created 02/23/2026 from EVG1010 per Kid Taxes procedure. Source documents were uploaded by the "
                          "parents to the EVG1010 Sharefile on 02/09/2026 and copied here by Admin.")
C.write_notes(f"""
# EVG1021 - Kim, Ethan S. - 2025 Form 1040 - Preparer Notes

*Synthetic client - Project Evergreen. Return status: **signed off, e-filed 04/14/2026 (after parents' EVG1010 return, e-filed 04/13), accepted.***

## Return summary
| | |
|---|---|
| Filing status | Single, can be claimed as a dependent (parents Daniel & Grace Kim, EVG1010) |
| Income | Wages {fmt(earned)} + interest {fmt(v['2b'])} + dividends {fmt(v['3b'])} (qualified {fmt(v['3a'])}) + LT capital gain {fmt(v['7'])} |
| AGI (line 11) | {fmt(v['11'])} |
| Standard deduction (dependent) | {fmt(v['12e'])} |
| Taxable income (line 15) | {fmt(v['15'])} |
| Tax (line 16, Form 8615) | {fmt(v['16'])} |
| Total tax (line 24) | {fmt(v['24'])} |
| Withholding | {fmt(v['25d'])} |
| **Balance due** | **{fmt(v['balance_due'])}** (parents paying by direct debit 04/15/2026) |

## What I did and why (plain English)
1. **Why Ethan files his own return.** In 2024 his UTMA interest/dividends went on his parents' return (Form 8814). That election
   requires the child's income to be only interest and dividends. In 2025 he sold 74 shares of his index fund ($3,100 long-term gain)
   and had a summer W-2, so 8814 is not available. His unearned income ($6,400) is over the $1,350 filing threshold and the $2,700
   kiddie-tax threshold -> his own Form 1040 with **Form 8615**. Per the Kid Taxes procedure I discussed it with Grace (02/20 and
   02/23 email) and set him up as client **EVG1021** with its own project code.
2. **Standard deduction.** As a dependent, his standard deduction is the larger of $1,350 or earned income + $450 = {fmt(dep_std)}.
   Taxable income {fmt(v['15'])}.
3. **Form 8615.** Net unearned income = $6,400 - $2,700 = {fmt(line3)}, limited to taxable income -> **{fmt(nui)}**. The parents' figures
   come straight from the final EVG1010 return: taxable income {fmt(k['parent_ti'])}, MFJ, qualified dividends {fmt(k['parent_qd'])},
   net capital gain {fmt(k['parent_ncg'])}, tax {fmt(det['parent_tax_without'])} (line 16 without the $55 Form 8814 tax for Chloe).
   - Parents' tax with Ethan's NUI added: {fmt(det['parent_tax_with_nui'])} -> difference **{fmt(det['line13_tentative_tax_on_nui'])}**. Of the NUI,
     {qd_share:,.2f} of qualified dividends and {cg_share:,.2f} of capital gain (line 5 / line 1 of each) keep the 15% rate; the ordinary part
     ({nui - qd_share - cg_share:,.2f}) is taxed at 24% - the parents' taxable income is in the 32% bracket, but their ordinary income after stacking QD/CG on top
     ({fmt(p_ord)}) is in the 24% bracket. Hand check: {nui_ord:,.2f} x 24% + {qd_share + cg_share:,.2f} x 15% = {hand:,.2f}.
   - Tax on the rest of his taxable income ({fmt(v['15'] - nui)}) at his own rates: {fmt(det['tax_on_child_TI_less_NUI'])} (mostly 0% qualified
     dividends / capital gain).
   - Line 16 {fmt(det['line15'])} vs line 17 (all at his own rates) {fmt(det['tax_as_if_no_8615'])} -> larger = **{fmt(det['line18_tax'])}**.
   - Chloe is not "another child" on line 7 - her income is on the parents' Form 8814, not a Form 8615.
4. **Wages.** Lifeguard W-2 $3,200 - no federal withholding (he claimed exempt on his W-4). Earned income is never kiddie-taxed.
5. **No NIIT / credits.** MAGI far below $200,000. No CTC on his return (his parents claim it), no EITC (dependent / under 25 with no children).
6. **Penalty.** Balance due {fmt(v['balance_due'])} is under $1,000 and he had no 2024 tax liability -> no Form 2210.
7. **State.** Washington - none.

## Open items / client communication
- None. Reminder in parents' letter: if EVG1010 is ever amended (e.g. taxable income changes), Ethan's Form 8615 must be recomputed.
- 2026: Ethan turns 17 - still subject to kiddie tax (under 18 at year-end); if he sells more fund shares, gains stay kiddie-taxed.

## Hand-off to signer / routing
- [x] Return locked; Accountant's copy saved as *reviewed*
- [x] Federal 1040 + Form 8615 - e-file; no state; no FBAR
- [x] Due date 04/15/2026 - e-filed 04/14/2026, released only after EVG1010 was accepted (dependent claimed on parents' return)
- [x] eSign: Ethan signed Form 8879; contact is Grace (email)
- Billing: flat $450 on EVG1021-1040-2025. Nothing to W/O.
""")
C.write_review_points(f"""
# Review Points - EVG1021 - 2025 - Form 1040

*Reviewer: M. Okafor (blue). Preparer responses in red. Synthetic.*

1. **Form 8615 line 6** - First draft used the parents' **2024** taxable income ($357,750) because EVG1010 wasn't final yet.
   - Must use the 2025 figures from the final EVG1010 return. Do not release until the parents' return is locked.
   - *Preparer: Updated to {fmt(k['parent_ti'])} after EVG1010 was locked 04/11. Tax now {fmt(v['16'])}.*
2. **Form 8615 line 9** - Draft taxed all $3,700 of NUI at 32% (the parents' top bracket) = {fmt(naive_32)}. Allocate the qualified dividend and capital gain portions (line 5 / line 1)
   so they keep the parents' 15% rate.
   - *Preparer: Done - QD {qd_share:,.2f} / CG {cg_share:,.2f}; line 11 now {fmt(det['line13_tentative_tax_on_nui'])}.*
3. **Line 12e** - Draft used $15,750. Dependent standard deduction = earned + $450 = {fmt(dep_std)}.
   - *Preparer: Corrected; 'can be claimed as a dependent' box checked.*
4. FYI - Line 7 of 8615: Chloe's income is on the parents' Form 8814, so it is not "other children's NUI". OK as $0.
5. FYI - Transmit only after EVG1010 is accepted; confirm the parents' SSN on Form 8615 matches EVG1010.
""")
print("EVG1021 done", R.summary()["24"], v["refund"], v["balance_due"], det)
