# Evergreen Tax - Agentic Tax-Filing Proof of Concept

An agentic system that takes an individual tax client from **intake -> preparation -> review -> filing**, built as
Claude Code **agent skills** that encode the firm's SOP (*Project Evergreen Draft (Pre-AI)*, v2). It is tested and tuned
against the synthetic client data set in `../evergreen-training-data-v2/` (25 clients with answer keys).

> Synthetic data only. Nothing is transmitted to the IRS; the "filing" stage produces the package a human signer approves.

## Architecture

```
            client PBC folder (PDFs, scans, spreadsheets, emails, PY return)
                               |
  1. evergreen-intake    scan -> classify -> extract -> PY compare -> filing screen -> open items
                               |   01_intake/intake.json, intake_memo.md, open_items_email.md
  2. evergreen-prepare   SOP checklist by area -> off-system workpapers -> facts.json -> calc engine
                               |   02_prepare/return.json, workpapers.md, state_returns.json,
                               |   software_exceptions.md (CCH Axcess / ProConnect overrides), prep_notes.md
  3. evergreen-review    independent re-derivation (fresh agent) -> review points -> corrections
                               |   03_review/review_points.md, review.json  ->  final/return.json
  4. evergreen-file      filing list + methods + due dates, e-file blockers, 8879, client letter, invoice
                               |   04_file/filing_package.json, signer_handoff.md, client_letter.md, invoice.md
  evergreen-pipeline    runs 1-4 with stage gates; writes run_summary.md
```

* **Skills** live in `.claude/skills/<name>/SKILL.md` with `references/` loaded on demand (progressive disclosure):
  intake document guide + schema; prep checklist (the SOP turned into questions), engine input schema, software-exception
  rules; review checklist; filing rules.
* **Tools** (`tools/`) are deterministic stand-ins for the firm's tech stack: `extract_docs.py` ~ ProSystem fx Scan, and
  `compute_return.py` ~ the Axcess calculation engine (TY2025 federal math incl. OBBBA). The agent makes every judgment;
  the engine only does arithmetic - the same split as a human preparer keying Axcess.
* **Separation of duties:** the review stage is meant to run in a *fresh* agent that has not seen the preparer's
  reasoning, mirroring the SOP's preparer/reviewer/signer colours.

## Running it

In Claude Code, opened at this folder (so `.claude/skills` loads):
```
> Run the evergreen pipeline on runs/smith-2025   (folder containing input/PERM and input/PBC)
```
Headless / batch (Claude Code CLI):
```bash
claude -p "Use the evergreen-pipeline skill on the client in runs/smith-2025" --permission-mode acceptEdits
```
Set up a sandboxed run from the synthetic data set (inputs only - answer keys are never copied):
```bash
python3 evals/make_run.py ../evergreen-training-data-v2 EVG1001 runs/EVG1001
```

## Evaluation loop

`evals/` implements the loop the brief asked for - "loop through test data to fine-tune each skill and identify gaps":
1. `setup_iteration.py` builds `evals/workspace/iteration-N/eval-<client>/{with_skill,without_skill}/run-1/`
   (with-skill = full pipeline; without-skill baseline = same tools and documents, no skills/SOP).
2. Each run is executed by an independent agent.
3. `score_run.py` compares the final return to the answer key line by line (30 key Form 1040 lines, filing status,
   refund/balance due) and measures what review added (pre- vs post-review).
4. An LLM grader (`grader.md`) scores every gotcha, software exception and required filing in the answer key, and writes
   root-cause "weaknesses".
5. Weaknesses are generalised into skill changes; the next iteration reruns the dev clients plus held-out clients the
   skills were never tuned on.
Results and the change log: [`evals/EVAL_LOG.md`](evals/EVAL_LOG.md).
