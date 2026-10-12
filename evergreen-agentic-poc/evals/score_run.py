#!/usr/bin/env python3
"""Deterministic scorer: compare an agent's final return with the dataset answer key.

    python3 evals/score_run.py <run_dir> <answer_key.json> [--out <dir>]

Reads <run_dir>/final/return.json (falls back to 02_prepare/return.json) and, if present, the preparer's pre-review
return (02_prepare/return.json) so the value added by review can be measured. Writes score.json + scorecard.md.

Scoring
* line_accuracy: share of the key Form 1040 lines that match the answer key within $2 (rounding tolerance)
* bottom_line: refund / balance due within $5 of the answer key  (the number the client actually sees)
* status_ok, deduction_type_ok
* For each line: expected, got, diff - so misses are easy to trace.
"""
import json
import os
import sys

LINES = [("1z", "Wages etc."), ("2a", "Tax-exempt interest"), ("2b", "Taxable interest"), ("3a", "Qualified dividends"),
         ("3b", "Ordinary dividends"), ("4b", "IRA taxable"), ("5b", "Pensions taxable"), ("6b", "SS taxable"),
         ("7", "Capital gain/loss"), ("8", "Schedule 1 income"), ("9", "Total income"), ("10", "Adjustments"),
         ("11", "AGI"), ("12e", "Deduction"), ("13a", "QBI deduction"), ("13b", "Schedule 1-A"), ("15", "Taxable income"),
         ("16", "Tax"), ("17", "Schedule 2 Part I (AMT, APTC)"), ("19", "CTC/ODC"), ("20", "Schedule 3 credits"),
         ("23", "Other taxes"), ("24", "Total tax"), ("25d", "Withholding"), ("26", "Estimated payments"),
         ("27a", "EIC"), ("28", "ACTC"), ("29", "AOTC refundable"), ("31", "Schedule 3 payments"), ("33", "Total payments")]
TOL = 2


def bottom(d):
    return (d.get("refund") or 0) - (d.get("balance_due") or 0)


def compare(ret, key):
    rs, ks = ret.get("form_1040_summary", {}), key.get("form_1040_summary", {})
    rows, hit = [], 0
    for ln, desc in LINES:
        e, g = ks.get(ln, 0) or 0, rs.get(ln, 0) or 0
        ok = abs(g - e) <= TOL
        hit += ok
        rows.append({"line": ln, "desc": desc, "expected": e, "got": g, "diff": g - e, "ok": ok})
    b_e, b_g = bottom(key), bottom(ret)
    return {"line_accuracy": round(hit / len(LINES), 3), "lines_matched": hit, "lines_total": len(LINES),
            "bottom_line_expected": b_e, "bottom_line_got": b_g, "bottom_line_ok": abs(b_e - b_g) <= 5,
            "bottom_line_error": b_g - b_e,
            "status_expected": key.get("filing_status"), "status_got": ret.get("filing_status"),
            "status_ok": key.get("filing_status") == ret.get("filing_status"),
            "deduction_type_ok": (key.get("deduction_type") or "")[:8] == (ret.get("deduction_type") or "")[:8],
            "lines": rows}


def main(run_dir, key_path, out_dir=None):
    key = json.load(open(key_path))
    out_dir = out_dir or run_dir
    final = os.path.join(run_dir, "final", "return.json")
    prep = os.path.join(run_dir, "02_prepare", "return.json")
    res = {"client_id": key["client_id"]}
    if os.path.exists(final):
        res["final"] = compare(json.load(open(final)), key)
    elif os.path.exists(prep):
        res["final"] = compare(json.load(open(prep)), key)
        res["final"]["note"] = "no final/return.json - scored the preparer's return"
    else:
        res["final"] = None
    if os.path.exists(prep):
        res["pre_review"] = compare(json.load(open(prep)), key)
    stages = {s: os.path.exists(os.path.join(run_dir, p)) for s, p in
              [("intake", "01_intake/intake.json"), ("prepare", "02_prepare/return.json"),
               ("review", "03_review/review.json"), ("final", "final/return.json"), ("file", "04_file/filing_package.json")]}
    res["stages_completed"] = stages
    os.makedirs(out_dir, exist_ok=True)
    json.dump(res, open(os.path.join(out_dir, "score.json"), "w"), indent=2)
    f = res["final"]
    md = [f"# Scorecard - {key['client_id']} {key.get('client','')}", ""]
    if f:
        md += [f"* Filing status: expected **{f['status_expected']}**, got **{f['status_got']}** {'OK' if f['status_ok'] else 'MISS'}",
               f"* Line accuracy (final): **{f['lines_matched']}/{f['lines_total']}** ({f['line_accuracy']:.0%})" +
               (f"  |  pre-review: {res['pre_review']['lines_matched']}/{f['lines_total']}" if res.get("pre_review") else ""),
               f"* Bottom line (refund + / due -): expected **{f['bottom_line_expected']:,}**, got **{f['bottom_line_got']:,}** "
               f"(error {f['bottom_line_error']:+,}) {'OK' if f['bottom_line_ok'] else 'MISS'}",
               f"* Stages completed: {', '.join(k for k, v in stages.items() if v)}", "",
               "| Line | Description | Expected | Got | Diff |", "|---|---|---:|---:|---:|"]
        for r in f["lines"]:
            if not r["ok"]:
                md.append(f"| {r['line']} | {r['desc']} | {r['expected']:,} | {r['got']:,} | {r['diff']:+,} |")
        if all(r["ok"] for r in f["lines"]):
            md.append("| - | all key lines match | | | |")
    else:
        md.append("No return produced.")
    open(os.path.join(out_dir, "scorecard.md"), "w").write("\n".join(md) + "\n")
    print("\n".join(md[:6]))
    return res


if __name__ == "__main__":
    argv = sys.argv[1:]
    out = None
    if "--out" in argv:
        i = argv.index("--out")
        out = argv[i + 1]
        argv = argv[:i] + argv[i + 2:]
    args = argv
    if len(args) < 2:
        sys.exit(__doc__)
    main(args[0], args[1], out)
