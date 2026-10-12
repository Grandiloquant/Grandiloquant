# Evergreen Tax - agentic tax-filing proof of concept

You are working inside a synthetic CPA firm, **Evergreen Tax**, that prepares individual (Form 1040) returns. Tax year
**2025** (filed during 2026) under current law including the One Big Beautiful Bill Act. All clients here are synthetic.

## How the work is organised
Four skills mirror the firm SOP (`docs/Project_Evergreen_SOP_v2.txt`): `evergreen-intake` -> `evergreen-prepare` ->
`evergreen-review` -> `evergreen-file`, chained by `evergreen-pipeline`. Shared tools:
* `tools/extract_docs.py` - scanner stand-in (PDF/XLSX/DOCX -> text, image pages -> PNG)
* `tools/compute_return.py` - calculation-engine stand-in (facts.json -> return.json); arithmetic only, no judgment
* `docs/tax_year_2025_reference.md` - 2025 figures and the rules the engine can't apply for you

## Run-folder contract
```
<run>/input/            client documents (read-only): PERM/, PBC/ (or 2025/PBC/), receipt log
<run>/01_intake/        intake.json, intake_memo.md, open_items_email.md, extracted/
<run>/02_prepare/       facts.json, return.json, return.md, diagnostics.json, workpapers.md, state_returns.json,
                        software_exceptions.md, prep_notes.md
<run>/03_review/        review_points.md, review.json, [facts_reviewed.json + engine output]
<run>/final/            return.json, state_returns.json   (what is filed)
<run>/04_file/          filing_package.json, signer_handoff.md, client_letter.md, invoice.md
<run>/run_summary.md
```

## Firm rules
* Work only from the run folder's `input/` documents and what earlier stages wrote. Do not open other client folders,
  answer keys, preparer notes or review files from any dataset - using them would invalidate the evaluation.
* Every number traces to a source document; every judgment gets a one-line reason (and authority when not obvious).
* Never invent facts. Missing information becomes an open item with the assumption you used.
* Communication to clients is drafted for internal approval first, never "sent".
* Where the SOP and the law disagree, follow the law and note it. Known cases: in the year of a spouse's death the
  survivor files MFJ (QSS is for the next two years with a dependent child); used-clothing donations are limited to thrift
  FMV (the SOP's "3x cost" can't be used); the FTC de minimis election requires all foreign income to be qualified passive
  income on payee statements; a separated taxpayer can still qualify for HOH; 2025 gambling losses are 100% (90% starts 2026).
* Describe tax software behaviour honestly: never invent CCH Axcess diagnostic numbers; state ProConnect behaviour only
  where documented (list in `evergreen-prepare/references/software_exceptions.md`).
