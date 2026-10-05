"""Produce the CORRECTED copy of the firm's CCH Axcess 1040 Exception Workbook (v2).

The original workbook (reference/..._ORIGINAL.xlsx) has several formula-reference errors: on four tabs the
labels and calculated cells sit in column E while the formulas read empty column-B cells, so those tabs
silently return the wrong answer. This script copies the original, fixes the formulas, and adds a
"Corrections Log" sheet. The per-client exception workbooks are filled from the corrected copy.

Run: python3 fix_workbook.py
"""
import os

from openpyxl import load_workbook
from openpyxl.styles import Alignment, Font, PatternFill

HERE = os.path.dirname(os.path.abspath(__file__))
REF = os.path.join(HERE, "..", "reference")
SRC = os.path.join(REF, "CCH_Axcess_1040_Exception_Workbook_v2_ORIGINAL.xlsx")
DST = os.path.join(REF, "CCH_Axcess_1040_Exception_Workbook_v2_CORRECTED.xlsx")

FIXES = []


def fix(ws, cell, new, why):
    old = ws[cell].value
    ws[cell].value = new
    FIXES.append((ws.title, cell, str(old), new, why))


def main():
    import warnings
    warnings.filterwarnings("ignore")
    wb = load_workbook(SRC)

    # Tab 5 - $25,000 special allowance. The formulas read B23/B24/B26/B27, but B23:B28 sit INSIDE merged label ranges
    # (A23:D23 ... A28:D28) - nothing can be typed there - and the threshold/results live in column E.
    ws = wb["5. Passive Activity (8582)"]
    why5 = ("Formulas pointed at B-column cells that are inside merged label ranges (A:D), so MAGI could never be entered and "
            "the tab always showed the full $25,000 allowance. MAGI is now entered in E23 (input cell).")
    fix(ws, "E26", "=MAX(0,E23-E24)", why5)
    fix(ws, "E27", "=MIN(25000,ROUND(E26*0.5,0))", why5)
    fix(ws, "E28", "=MAX(0,25000-E27)", why5)

    # Tab 8 - Form 2210 safe harbor. Same defect: inputs referenced in B12/B14/B15/B19 are inside merged ranges A:D;
    # the tan input cells are E12, E14, E15, E19.
    ws = wb["8. Est. Tax Penalty (2210)"]
    why8 = ("Formulas referenced B12/B13/B14/B15/B16/B17/B18/B19 - all inside merged label ranges (A:D) - so every result was 0 "
            "and the tab always said 'YES - no penalty override needed'. Inputs are now E12 (CY tax), E14 (PY AGI), "
            "E15 (PY tax), E19 (payments).")
    fix(ws, "E13", "=E12*0.9", why8)
    fix(ws, "E16", "=IF(E14>150000,1.1,1)", why8 + " (MFS threshold is $75,000 - override E16 for MFS.)")
    fix(ws, "E17", "=E15*E16", why8)
    fix(ws, "E18", "=MIN(E13,E17)", why8)
    fix(ws, "E20", "=MAX(0,E18-E19)", why8)
    fix(ws, "E21", '=IF(E20=0,"YES — no penalty override needed","NO — compute penalty or consider annualized method")', why8)
    for r in range(25, 29):
        fix(ws, f"B{r}", "=$E$18*0.25", why8 + " Quarterly installments now use the required annual payment in E18.")

    # Tab 10 - capital loss carryover. Labels merged A:C; formulas in column D read B10/B11/B12 (inside the merge).
    ws = wb["10. Capital Loss Carryover"]
    why10 = ("Formulas read B10-B12 and B14/B15, which are inside merged label ranges (A:C), so every carryover was 0 (and, "
             "had inputs been possible, the $3,000 deduction was never subtracted). Inputs are now D10 (PY line 21 allowable "
             "loss), D11 (PY ST net loss), D12 (PY LT net loss).")
    fix(ws, "D13", "=D11+D12", why10)
    fix(ws, "D14", "=MIN(D11,D10)", why10)
    fix(ws, "D15", "=MAX(0,D10-D14)", why10)
    fix(ws, "D16", "=MAX(0,D11-D14)", why10)
    fix(ws, "D17", "=MAX(0,D12-D15)", why10)

    # Tab 7 - resident credit limitation multiplied the allocation % by INCOME, not by resident-state TAX.
    ws = wb["7. Multi-State Allocation"]
    ws["G11"].value = "Resident-State Tax Before Credit (input)"
    ws["G11"].font = Font(bold=True)
    why7 = ("Credit limit was MIN(tax paid, alloc % x total federal income) - that is state-source INCOME, not tax. "
            "Added input column G (resident-state tax before credit); limit = MIN(tax paid, G x alloc %).")
    for r in range(12, 20):
        fix(ws, f"F{r}", f"=MIN(E{r},G{r}*D{r})", why7)

    # Tab 12 - S corp: losses were netted against basis before distributions (Reg. 1.1367-1(f) ordering).
    ws = wb["12. S-Corp Dual Basis"]
    why12 = ("Distributions reduce stock basis BEFORE nondeductible expenses and losses (Treas. Reg. 1.1367-1(f)). "
             "The original formula subtracted a current-year loss first, overstating the taxable distribution. "
             "Only current-year income now increases the basis tested against distributions.")
    for r in range(15, 23):
        fix(ws, f"F{r}", f"=MAX(0,E{r}-(B{r}+MAX(0,D{r})))", why12)

    # Tab 21 - 1033 replacement deadline counted from the conversion DATE; the statute counts from the close of
    # the first tax year in which any part of the gain is realized.
    ws = wb["21. Involuntary Conv. 1033"]
    why21 = ("IRC 1033(a)(2)(B): the replacement period ends 2 years (3 for condemned business/investment real "
             "property; 4 for a principal residence in a federally declared disaster area) after the close of the "
             "first tax year in which any part of the gain is realized - not 2 x 365 days after the event. Formula "
             "assumes the gain is realized in the conversion year (insurance paid that year); override if not.")
    for r in range(12, 18):
        fix(ws, f"I{r}", f'=IF(AND(B{r}<>"",E{r}<>""),DATE(YEAR(B{r})+E{r},12,31),"")', why21)

    # Tab 13 - citation
    ws = wb["13. Trust Termination PAL"]
    ws["A1"].value = "TRUST TERMINATION — SUSPENDED PASSIVE LOSS BASIS STEP-UP TRACKER (§469(j)(12) / §643(e))"
    FIXES.append((ws.title, "A1", "...(§643(e) / §469(g))", ws["A1"].value,
                  "A trust's distribution of a passive activity is governed by IRC 469(j)(12) (suspended losses added to "
                  "basis, not deductible); 469(g) covers fully taxable dispositions, where losses ARE deductible."))

    # Tab 18 - IRD rows reuse the NUA formula (Box 1 - Box 6) which is meaningless for IRD.
    ws = wb["18. NUA & IRD Deduction"]
    FIXES.append((ws.title, "E11:E16", "=B-C (all rows)", "unchanged for NUA rows; IRD rows are overwritten with a value",
                  "The 691(c) deduction is the federal estate tax WITH the IRD minus estate tax WITHOUT it, times the "
                  "beneficiary's share of the IRD received this year - it cannot be computed as IRA value - estate tax. "
                  "Compute it off-tab (or in Notes) and type the result into column E for IRD rows."))

    log = wb.create_sheet("Corrections Log", 1)
    log.append(["Tab", "Cell(s)", "Original", "Corrected", "Why"])
    for c in log[1]:
        c.font = Font(bold=True, color="FFFFFF")
        c.fill = PatternFill("solid", fgColor="1F5C3A")
    for row in FIXES:
        log.append(list(row))
    for col, w in zip("ABCDE", (26, 12, 34, 40, 110)):
        log.column_dimensions[col].width = w
    for row in log.iter_rows(min_row=2):
        for c in row:
            c.alignment = Alignment(wrap_text=True, vertical="top")
    wb.calculation.fullCalcOnLoad = True
    wb.save(DST)
    print(f"wrote {DST} with {len(FIXES)} corrections")
    return FIXES


if __name__ == "__main__":
    main()
