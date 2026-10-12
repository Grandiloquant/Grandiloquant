#!/usr/bin/env python3
"""Stand-in for the CCH Axcess calculation engine.

    python3 tools/compute_return.py <facts.json> <out_dir>

Reads the preparer's input facts (schema: .claude/skills/evergreen-prepare/references/facts_schema.md), runs the
TY2025 federal calculation, and writes:
  <out_dir>/return.json  - every form/line, the Form 1040 summary, refund/balance due, carryforwards, engine notes
  <out_dir>/return.md    - the same, human-readable (what a reviewer pages through)
  <out_dir>/diagnostics.json - input checks, like Axcess diagnostics: unknown fields, missing basics, sanity flags

The engine only does arithmetic. Every judgment (what is income, which deduction applies, basis fixes, limits that
need off-system workpapers) lives in the facts the preparer supplies - exactly as with real tax software.
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "taxcalc"))
from tax2025 import Return1040  # noqa: E402

KNOWN = {"status", "taxpayer", "spouse", "dependents", "w2", "interest", "dividends", "ira", "pension", "ssa", "trades",
         "k1_st", "k1_lt", "other_st", "other_lt", "cap_loss_co", "unrecaptured_1250", "g28_other", "sch1", "adjustments",
         "itemized", "force_itemize", "salt_magi_addback", "qbi", "sch1a", "se", "se_earned_T", "se_earned_S",
         "dependent_care", "education", "eic_eligible", "eic_kids", "eic_earned", "eic_invest_income", "ctc_magi_addback",
         "earned_income_8812", "se_net_for_8812", "ftc", "amt", "niit", "kiddie_8615", "form_8814_tax", "line16_other",
         "claimed_as_dependent", "earned_for_dep_std", "mfs_spouse_itemizes", "mfs_spouse_no_income", "hh_wages_no_w2",
         "unreported_tips", "unreported_tips_medicare", "form4137_tax", "form5329_tax", "schedule_h_tax", "excess_aptc",
         "net_ptc", "uncollected_fica_w2", "sch2_other", "sch3_ref_other", "other_nonref_credits", "res_clean_energy",
         "energy_home_improvement", "other_earned", "withholding_1099", "withholding_other", "estimated_payments",
         "extension_payment", "apply_to_2026", "es_penalty", "ss_taxable_override", "qd_elected_4952",
         "foreign_accounts", "foreign_account_country", "foreign_trust"}
META = {"_comment", "_notes", "client_id", "tax_year", "_sources"}


def diagnostics(f):
    d = []
    for k in f:
        if k not in KNOWN and k not in META:
            d.append({"severity": "WARNING", "msg": f"Unknown input field '{k}' - ignored by the engine (check facts_schema.md)"})
    if f.get("status") not in ("S", "MFJ", "MFS", "HOH", "QSS"):
        d.append({"severity": "E-FILE DISQUALIFYING", "msg": "Filing status missing/invalid (S, MFJ, MFS, HOH, QSS)"})
    if f.get("status") == "MFJ" and not f.get("spouse"):
        d.append({"severity": "WARNING", "msg": "MFJ without spouse block (age65/blind default to False)"})
    for i, w in enumerate(f.get("w2", [])):
        if w.get("box2", 0) > w.get("box1", 0) > 0:
            d.append({"severity": "WARNING", "msg": f"W-2 #{i+1}: federal withholding exceeds wages"})
        if not w.get("box5"):
            d.append({"severity": "CAUTION", "msg": f"W-2 #{i+1}: box 5 (Medicare wages) missing - Form 8959 may be understated"})
    for i, t in enumerate(f.get("trades", [])):
        if t.get("box") not in tuple("ABCDEFGHIJKL"):
            d.append({"severity": "WARNING", "msg": f"Trade #{i+1}: Form 8949 box '{t.get('box')}' invalid"})
    if f.get("itemized") and not f.get("itemized", {}).get("state_income_tax") and not f.get("itemized", {}).get("real_estate_tax"):
        d.append({"severity": "INFORMATIONAL", "msg": "Itemized block has no SALT entries"})
    return d


def to_md(R, cid):
    v = R.values
    out = [f"# {cid} - 2025 Form 1040 (computed)", "",
           f"Filing status: **{R.status}** | Deduction: **{v.get('deduction_type')}** | "
           f"{'Refund' if v.get('refund') else 'Balance due'}: **${(v.get('refund') or v.get('balance_due') or 0):,}**", ""]
    for form, lines in R.forms.items():
        out += [f"## {form}", "", "| Line | Description | Amount |", "|---|---|---:|"]
        for ln, desc, amt in lines:
            a = f"{amt:,}" if isinstance(amt, int) else str(amt)
            out.append(f"| {ln} | {str(desc).replace('|', '/')} | {a} |")
        out.append("")
    if R.notes:
        out += ["## Engine notes", ""] + [f"- {n}" for n in R.notes]
    return "\n".join(out) + "\n"


def main(facts_path, out_dir):
    f = json.load(open(facts_path))
    os.makedirs(out_dir, exist_ok=True)
    diag = diagnostics(f)
    clean = {k: v for k, v in f.items() if k in KNOWN}
    R = Return1040(clean).compute()
    cid = f.get("client_id", os.path.basename(os.path.dirname(os.path.abspath(facts_path))))
    data = {
        "client_id": cid, "filing_status": R.status, "form_1040_summary": R.summary(),
        "deduction_type": R.values.get("deduction_type"), "refund": R.values.get("refund"),
        "balance_due": R.values.get("balance_due"),
        "carryforwards_to_2026": {k: v for k, v in R.values.items()
                                  if "carryover" in k or "carryforward" in k or k.endswith("_unused")},
        "federal_forms": {form: [{"line": ln, "description": d, "amount": a} for ln, d, a in lines]
                          for form, lines in R.forms.items()},
        "engine_notes": R.notes,
    }
    json.dump(data, open(os.path.join(out_dir, "return.json"), "w"), indent=2, default=str)
    open(os.path.join(out_dir, "return.md"), "w").write(to_md(R, cid))
    json.dump(diag, open(os.path.join(out_dir, "diagnostics.json"), "w"), indent=2)
    s = R.summary()
    print(f"{cid}: AGI {s['11']:,} | TI {s['15']:,} | total tax {s['24']:,} | payments {s['33']:,} | "
          f"{'refund' if data['refund'] else 'due'} {(data['refund'] or data['balance_due'] or 0):,} | "
          f"{len(diag)} diagnostics")
    for x in diag:
        print(f"  [{x['severity']}] {x['msg']}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    main(sys.argv[1], sys.argv[2])
