# Evaluation log - Evergreen agentic tax-filing PoC

Each iteration: run the pipeline (with skills) and a no-skill baseline on test clients in sandboxed folders (inputs only), score
the final return against the answer key (`score_run.py`), have an independent LLM grader mark every gotcha, software
exception, required filing and open-item check (`grader.md`), then turn root causes into skill changes.

Baseline = same documents and tools (scanner, calc engine and its input schema) but **no skills, SOP, firm reference or
CLAUDE.md**. The baseline wasn't asked to produce a software-exception log, so compare categories, not just the headline rate.

---

## Iteration 1 - dev set (6 clients), skills v1

Clients: EVG1001 Bell, EVG1003 Okafor, EVG1008 O'Brien, EVG1013 Brooks, EVG1016 Doyle, EVG1022 Whitfield.
Viewer: `workspace/iteration-1/review.html` · benchmark: `workspace/iteration-1/benchmark.md`

| Category (graded checks) | With skills | Baseline |
|---|---:|---:|
| Gotchas (tax traps in the answer key) | 46/47 | 44/47 |
| Required filings (state/local/separate, methods) | 21/21 | 20/21 |
| Key 1040 lines + bottom line (all lines exact / refund within $5) | 10/12 | 8/12 |
| State amounts | 0/2 | 1/2 |
| Open items identified | 6/6 | 6/6 |
| Software exceptions (Axcess/ProConnect log) | 23/29 | 0/29 (not produced) |
| **All checks** | **91.5%** | **70.1%** |

Cost: with skills ~142k tokens / 6.1 min per client vs baseline ~84k / 1.9 min.

### What we learned
* **The base model is already strong** on clean federal mechanics - both configurations got the federal bottom line right on
  most clients. The skills' value showed up in state/local filing discipline (the baseline filed an unnecessary Illinois
  nonresident return for Whitfield), prior-year checks (the skills run caught a 2024 child-tax-credit over-claim on O'Brien
  that isn't even in the answer key), the review trail, and the software-exception log.
* **Answer-key defects found by the agents** (fixed in the data set):
  * Whitfield: the key ignored Form 8960 line 9b (state income tax allocable to investment income). The skills run applied it
    correctly -> key corrected (refund $717).
  * Okafor: the key deducted car washes on top of standard mileage and a dash cam at 100%; the organizer lumped car washes with
    rider supplies -> source data split and key corrected (balance due $262).
  * O'Brien: 39-year (transient use) vs 27.5-year life for a short-stay cabin - both defensible; noted.
* **Skill weaknesses (root causes)** and the fixes made for iteration 2:
  | Weakness | Fix |
  |---|---|
  | Applied a remembered Michigan 2025 overtime subtraction (it actually starts 2026); review rubber-stamped it | CLAUDE.md rule "don't apply law you can't support"; reviewer must decide every "verify" item; MI fact added to reference |
  | Review not independent (sub-agents can't start agents) | Harness now runs stages 1-2 and 3-4 as separate agents; pipeline skill documents this |
  | Wrong state wage base (box 16 PA base incl. 401(k) deferrals used for MA) | Reference + checklist: reconcile each state's wage base before workday allocation |
  | Software-exception log padded with tax judgments; missed state-module defaults, manual-calc inputs and "negative" exceptions | Defined what belongs in the log (4 categories) and what doesn't |
  | Lumped organizer items deducted in full | Checklist E0: split / estimate / ask - never deduct the whole lump |
  | Agents flagged every return as late (machine date Oct 2026) | "As-of" engagement date rule |
  | Gaps: tips composition, SE wage base, NIIT 9b, AMT credit, timely mailing, HSA excess, vacation-home details | Added to the 2025 reference / facts schema; `supporting_forms` so Sch C/E, 8889, 8582 detail shows on the return |
