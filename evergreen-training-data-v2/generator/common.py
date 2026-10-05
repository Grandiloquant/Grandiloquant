"""
Shared scaffolding for building one synthetic client:
folder structure (per Project Evergreen procedure "Folder Structures"), document
registry / receipt log, and writers for the answer key, notes, and rubric.

Folder layout produced for each client:

clients/<ClientID>_<Surname>/
    PERM/                                   permanent info (profile, prior-year return summary, legal docs)
    2025/
        PBC/                                source documents exactly as received from the client
        Deliverables/                       final return (client-ready) + vouchers / filing instructions
        <ID>_2025_PBC_Receipt_Log.md        admin intake log (what came in, when) - neutral, no hints
        <ID>_2025_Preparer_Notes.md         plain-English notes on the completed return (signed-off)
        <ID>_2025_Review_Points.md          reviewer points raised on the first draft and how resolved
        <ID>_2025_Answer_Key.json           machine-readable expected return + gotcha rubric (eval use)
"""
from __future__ import annotations

import json
import os
from datetime import date

from docs import return_pdf, write_text

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
CLIENTS_DIR = os.path.join(ROOT, "clients")
TAX_YEAR = 2025


class ClientBuild:
    def __init__(self, client_id: str, folder_name: str, display_name: str):
        self.id = client_id
        self.display = display_name
        self.root = os.path.join(CLIENTS_DIR, f"{client_id}_{folder_name}")
        self.perm = os.path.join(self.root, "PERM")
        self.year = os.path.join(self.root, str(TAX_YEAR))
        self.pbc = os.path.join(self.year, "PBC")
        self.deliv = os.path.join(self.year, "Deliverables")
        for p in (self.perm, self.pbc, self.deliv):
            os.makedirs(p, exist_ok=True)
        self.docs = []
        self.perm_docs = []

    # ---------------------------------------------------------------- paths
    def pbc_file(self, name, doc_type, received, source="Sharefile upload", note=""):
        """Register a PBC doc and return its path. `note` is the neutral admin note (no hints)."""
        self.docs.append({"file": name, "type": doc_type, "received": received, "source": source, "admin_note": note})
        return os.path.join(self.pbc, name)

    def perm_file(self, name, doc_type):
        self.perm_docs.append({"file": name, "type": doc_type})
        return os.path.join(self.perm, name)

    def year_file(self, name):
        return os.path.join(self.year, name)

    def deliv_file(self, name):
        return os.path.join(self.deliv, name)

    # ---------------------------------------------------------------- writers
    def write_receipt_log(self, project_code, preparer, reviewer, signer, actual_start, extension=None, extra=""):
        lines = [f"# {self.id} - {self.display} - 2025 PBC Receipt Log", "",
                 f"*Synthetic training data - Project Evergreen.*", "",
                 f"| Field | Value |", "|---|---|",
                 f"| Client ID | {self.id} |", f"| Project code | {project_code} |",
                 f"| Signer / Reviewer / Preparer | {signer} / {reviewer} / {preparer} |",
                 f"| Actual Start Date (first PBC received) | {actual_start} |"]
        if extension:
            lines.append(f"| Extension (Form 4868) | {extension} |")
        lines += ["", "## Documents received (in order logged by Admin)", "",
                  "| # | File | Document type | Date received | Source | Admin note |", "|---|---|---|---|---|---|"]
        for i, d in enumerate(self.docs, 1):
            lines.append(f"| {i} | `{d['file']}` | {d['type']} | {d['received']} | {d['source']} | {d['admin_note']} |")
        if self.perm_docs:
            lines += ["", "## PERM folder contents", "", "| File | Type |", "|---|---|"]
            for d in self.perm_docs:
                lines.append(f"| `{d['file']}` | {d['type']} |")
        if extra:
            lines += ["", extra]
        write_text(self.year_file(f"{self.id}_2025_PBC_Receipt_Log.md"), "\n".join(lines) + "\n")

    def write_return(self, ret, header_info, state_summary=None, attachments=None):
        header = {"title": f"{self.id} - {self.display} - 2025 Form 1040", "info": header_info}
        return_pdf(self.deliv_file(f"{self.id}_2025_Form_1040_Client_Copy.pdf"), header, ret, state_summary,
                   attachments, copy_label="CLIENT COPY - FINAL (signed off)")

    def write_answer_key(self, ret, facts_summary: dict, gotchas: list, state=None, filings=None, extra=None):
        forms = {form: [{"line": ln, "description": d, "amount": a} for ln, d, a in lines]
                 for form, lines in ret.forms.items()}
        data = {
            "client_id": self.id,
            "client": self.display,
            "tax_year": TAX_YEAR,
            "synthetic": True,
            "facts_summary": facts_summary,
            "filing_status": ret.status,
            "form_1040_summary": ret.summary(),
            "deduction_type": ret.values.get("deduction_type"),
            "refund": ret.values.get("refund"),
            "balance_due": ret.values.get("balance_due"),
            "carryforwards_to_2026": {k: v for k, v in ret.values.items()
                                      if "carryover" in k or "carryforward" in k or k.endswith("_unused")},
            "federal_forms": forms,
            "state_and_local": state or [],
            "required_filings": filings or [],
            "gotchas": gotchas,
            "engine_notes": ret.notes,
        }
        if extra:
            data.update(extra)
        write_text(self.year_file(f"{self.id}_2025_Answer_Key.json"), json.dumps(data, indent=2, default=str) + "\n")

    def write_notes(self, md):
        write_text(self.year_file(f"{self.id}_2025_Preparer_Notes.md"), md.strip() + "\n")

    def write_review_points(self, md):
        write_text(self.year_file(f"{self.id}_2025_Review_Points.md"), md.strip() + "\n")

    def write_profile(self, md):
        write_text(self.perm_file("Client_Profile.md", "Client static info / PERM notes"), md.strip() + "\n")


def gotcha(gid, procedure_section, title, trap, correct_treatment, impact, lines=None, difficulty="medium"):
    """One rubric item. `trap` = what a naive preparer/AI would do; `correct_treatment` = expected handling."""
    return {"id": gid, "procedure_section": procedure_section, "title": title, "trap": trap,
            "correct_treatment": correct_treatment, "impact": impact, "affected_lines": lines or [],
            "difficulty": difficulty}


def fmt(n):
    return f"${n:,.0f}" if n >= 0 else f"(${-n:,.0f})"
