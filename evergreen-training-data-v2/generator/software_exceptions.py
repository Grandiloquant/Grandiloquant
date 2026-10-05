"""
Software-exception layer (v2).

For each client this writes:
  2025/<ID>_2025_Software_Exception_Workbook.xlsx  - the firm's (corrected) CCH Axcess Exception Workbook, with the
        Diagnostics Log and every relevant calculation tab filled in for this client, plus a "ProConnect Exceptions" tab
  2025/<ID>_2025_Software_Exceptions.md            - plain-English walkthrough: what each package does by default,
        why that is wrong for this client, the manual calc, and where the override goes (Axcess and ProConnect)
  ...and merges a "software_exceptions" rubric array into <ID>_2025_Answer_Key.json.

Usage from a swx data module (generator/swx/evgNNNN.py):

    ITEMS = [exc(...), ...]          # one per exception
    TABS = {"12": [{"A": "...", "B": 28000, ...}], "8": {"B12": 133340, ...}, ...}
    PC_ONLY = [...]                  # optional extra ProConnect-only rows (same exc() shape, tab="PC")

Tab keys are the workbook tab numbers ("3".."24"); "3b" is the lower 'Allowed vs. Suspended' block of tab 3.
Row-style tabs take a list of {column_letter: value}; cell-style tabs take {cell: value}: "5cells" -> {"E23": MAGI};
"8" -> E12 CY tax, E14 PY AGI, E15 PY tax, E19 payments, C25:C28 paid, D25:D28 timely, F25:F28 notes;
"10" -> D10 PY allowable loss, D11 PY ST loss, D12 PY LT loss.
Formula cells are never overwritten unless the column is listed in ALLOW_OVERWRITE for that tab.
"""
from __future__ import annotations

import json
import os
import warnings

from openpyxl import load_workbook
from openpyxl.styles import Alignment, Font, PatternFill

warnings.filterwarnings("ignore")
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, ".."))
TEMPLATE = os.path.join(ROOT, "reference", "CCH_Axcess_1040_Exception_Workbook_v2_CORRECTED.xlsx")

TAB_NAMES = {
    "2": "2. Diagnostics Log", "3": "3. K-1 Basis Limitation", "3b": "3. K-1 Basis Limitation",
    "4": "4. At-Risk (Form 6198)", "5": "5. Passive Activity (8582)", "6": "6. Depreciation Overrides",
    "7": "7. Multi-State Allocation", "8": "8. Est. Tax Penalty (2210)", "9": "9. AMT Adjustments (6251)",
    "10": "10. Capital Loss Carryover", "11": "11. Hot Assets & Mixing Bowl", "12": "12. S-Corp Dual Basis",
    "13": "13. Trust Termination PAL", "14": "14. Bond Interest & Premium", "15": "15. Mortgage Interest Limit",
    "16": "16. Vacation Home Allocation", "17": "17. Equity Comp & Wash Sales", "18": "18. NUA & IRD Deduction",
    "19": "19. Crypto Income & Basis", "20": "20. Insolvency (Form 982)", "21": "21. Involuntary Conv. 1033",
    "22": "22. Reorg, Liquidation, 1244", "23": "23. Multi-State W-2 Days", "24": "24. Rare-Event Log",
}
# first data row and max rows for row-style tabs
ROW_LAYOUT = {"2": (14, 40), "3": (13, 8), "3b": (24, 8), "4": (13, 8), "5": (13, 8), "6": (13, 10), "7": (12, 8),
              "9": (13, 8), "11": (16, 8), "12": (15, 8), "13": (12, 6), "14": (11, 8), "15": (12, 6), "16": (12, 6),
              "17": (12, 8), "18": (11, 6), "19": (13, 10), "20": (11, 6), "21": (12, 6), "22": (15, 8), "23": (11, 8),
              "24": (11, 10)}
CELL_TABS = {"5", "8", "10"}  # tab 5 also accepts rows; its MAGI goes in via {"B23": x} under key "5cells"
ALLOW_OVERWRITE = {"18": {"E"}}  # IRD rows: 691(c) deduction typed over the NUA formula (see Corrections Log)

CATEGORIES = ["Basis/At-Risk/Passive", "Depreciation", "State Allocation", "Est. Tax Penalty", "AMT", "Capital Loss",
              "E-file Disqualifying", "Other"]


def exc(xid, tab, category, title, axcess_default, axcess_diagnostic, manual_calc, axcess_fix, amount,
        proconnect_default, proconnect_fix, efile_impact="None", proconnect_ref="", status="Signed Off",
        affected_lines=None, procedure_section="", notes=""):
    """One software exception.
    tab: workbook tab number as str ("3".."24") or "PC" for a ProConnect-only exception or "2" for log-only.
    axcess_default / proconnect_default: what the package does on its own (the trap).
    axcess_fix / proconnect_fix: exact input/override and where it goes.
    axcess_diagnostic: diagnostic text the preparer sees, or 'None - silent' when nothing fires (the dangerous case).
    """
    assert category in CATEGORIES, category
    return {"id": xid, "workbook_tab": TAB_NAMES.get(tab, "ProConnect-only" if tab == "PC" else tab), "tab_key": tab,
            "category": category, "title": title, "axcess_default_behavior": axcess_default,
            "axcess_diagnostic": axcess_diagnostic, "manual_calc_required": manual_calc, "axcess_override": axcess_fix,
            "override_amount": amount, "proconnect_default_behavior": proconnect_default,
            "proconnect_fix": proconnect_fix, "proconnect_reference": proconnect_ref, "efile_impact": efile_impact,
            "status": status, "affected_lines": affected_lines or [], "procedure_section": procedure_section,
            "notes": notes}


def _fill_rows(ws, key, rows):
    start, mx = ROW_LAYOUT[key]
    assert len(rows) <= mx, f"tab {key}: {len(rows)} rows > {mx}"
    allow = ALLOW_OVERWRITE.get(key, set())
    for i, row in enumerate(rows):
        r = start + i
        for col, val in row.items():
            cell = ws[f"{col}{r}"]
            if isinstance(cell.value, str) and cell.value.startswith("=") and col not in allow:
                raise ValueError(f"{ws.title}!{col}{r} is a formula ({cell.value}); refusing to overwrite")
            cell.value = val


def _fill_cells(ws, cells):
    for ref, val in cells.items():
        cur = ws[ref].value
        if isinstance(cur, str) and cur.startswith("="):
            raise ValueError(f"{ws.title}!{ref} is a formula; refusing to overwrite")
        ws[ref].value = val


def build_pack(C, items, tabs, preparer="Preparer", reviewer="Reviewer", intro=""):
    """C: common.ClientBuild. items: list of exc(). tabs: dict tab_key -> rows/cells."""
    wb = load_workbook(TEMPLATE)
    # ---- Diagnostics log
    log_rows = []
    for it in items:
        if it["tab_key"] == "PC":
            continue
        log_rows.append({"A": C.id, "B": 2025, "C": "— (varies by release)" if it["axcess_diagnostic"] != "None - silent" else "none fired",
                         "D": it["axcess_diagnostic"] if it["axcess_diagnostic"] != "None - silent" else
                         f"[No diagnostic - logged by preparer] {it['title']}",
                         "E": it["category"], "F": it["manual_calc_required"], "G": it["axcess_override"],
                         "H": it["override_amount"], "I": it["status"], "J": preparer, "K": reviewer,
                         "L": f"{it['id']} | Workbook tab {it['workbook_tab']} | {it['notes']}".strip(" |")})
    _fill_rows(wb[TAB_NAMES["2"]], "2", log_rows)
    # ---- calc tabs
    for key, data in tabs.items():
        if key == "5cells":
            _fill_cells(wb[TAB_NAMES["5"]], data)
        elif key in ("8", "10"):
            _fill_cells(wb[TAB_NAMES[key]], data)
        else:
            _fill_rows(wb[TAB_NAMES[key]], key, data)
    # ---- ProConnect tab
    ws = wb.create_sheet("ProConnect Exceptions", 2)
    hdr = ["ID", "Workbook tab (Axcess equivalent)", "Exception", "ProConnect default behavior", "ProConnect fix / input",
           "ProConnect reference", "E-file impact", "Override / calc amount"]
    ws.append([f"{C.id} - {C.display} - Intuit ProConnect Tax handling of the same exceptions (synthetic training data)"])
    ws["A1"].font = Font(bold=True, size=12)
    ws.append(["ProConnect field names/screens follow Intuit help articles where cited; confirm against the current "
               "release before relying on a screen path. Same tax answer either way - only the mechanics differ."])
    ws.append(hdr)
    for c in ws[3]:
        c.font = Font(bold=True, color="FFFFFF")
        c.fill = PatternFill("solid", fgColor="1F5C3A")
    for it in items:
        ws.append([it["id"], it["workbook_tab"], it["title"], it["proconnect_default_behavior"], it["proconnect_fix"],
                   it["proconnect_reference"], it["efile_impact"], it["override_amount"]])
    for col, w in zip("ABCDEFGH", (14, 26, 36, 48, 60, 34, 26, 16)):
        ws.column_dimensions[col].width = w
    for row in ws.iter_rows(min_row=4):
        for c in row:
            c.alignment = Alignment(wrap_text=True, vertical="top")
    wb.calculation.fullCalcOnLoad = True
    out = C.year_file(f"{C.id}_2025_Software_Exception_Workbook.xlsx")
    wb.save(out)

    # ---- markdown
    used_tabs = sorted({it["workbook_tab"] for it in items}, key=lambda s: (len(s.split(".")[0]), s))
    md = [f"# {C.id} - {C.display} - 2025 Software Exceptions (CCH Axcess & Intuit ProConnect)", "",
          "*Synthetic training data - Project Evergreen v2. Companion workbook: "
          f"`{C.id}_2025_Software_Exception_Workbook.xlsx` (firm's corrected CCH Axcess Exception Workbook, filled in).*", ""]
    if intro:
        md += [intro.strip(), ""]
    md += ["| ID | Workbook tab | Exception | Axcess diagnostic? | Override amount | E-file impact |", "|---|---|---|---|---:|---|"]
    for it in items:
        amt = it["override_amount"]
        amt = f"{amt:,.0f}" if isinstance(amt, (int, float)) else (amt or "")
        diag = "**silent** (no diagnostic)" if it["axcess_diagnostic"] == "None - silent" else "yes"
        md.append(f"| {it['id']} | {it['workbook_tab']} | {it['title']} | {diag} | {amt} | {it['efile_impact']} |")
    md.append("")
    for it in items:
        amt = it["override_amount"]
        amt_s = f"${amt:,.0f}" if isinstance(amt, (int, float)) else str(amt or "-")
        md += [f"## {it['id']} - {it['title']}", "",
               f"*Workbook tab:* {it['workbook_tab']}  |  *Category:* {it['category']}  |  *Manual calc:* "
               f"{it['manual_calc_required']}  |  *Amount:* {amt_s}" +
               (f"  |  *Procedure doc:* {it['procedure_section']}" if it['procedure_section'] else ""), "",
               f"- **CCH Axcess by default:** {it['axcess_default_behavior']}",
               f"- **Axcess diagnostic:** {it['axcess_diagnostic']}",
               f"- **Axcess fix:** {it['axcess_override']}",
               f"- **ProConnect by default:** {it['proconnect_default_behavior']}",
               f"- **ProConnect fix:** {it['proconnect_fix']}" +
               (f" *(ref: {it['proconnect_reference']})*" if it["proconnect_reference"] else ""),
               f"- **E-file impact:** {it['efile_impact']}"]
        if it["affected_lines"]:
            md.append(f"- **Return lines affected:** {', '.join(it['affected_lines'])}")
        if it["notes"]:
            md.append(f"- **Notes:** {it['notes']}")
        md.append("")
    with open(C.year_file(f"{C.id}_2025_Software_Exceptions.md"), "w") as fh:
        fh.write("\n".join(md) + "\n")

    # ---- merge into answer key
    ak = C.year_file(f"{C.id}_2025_Answer_Key.json")
    if os.path.exists(ak):
        d = json.load(open(ak))
        d["software_exceptions"] = items
        d["software_exception_tabs_used"] = used_tabs
        with open(ak, "w") as fh:
            fh.write(json.dumps(d, indent=2, default=str) + "\n")
    return out
