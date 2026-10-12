# Grader instructions (LLM grader for one client run)

You grade one agent run against the dataset answer key. You may read the answer key - the agent under test could not.

## Inputs (paths given in your prompt)
* `run_dir` - the agent's run folder (01_intake ... 04_file, final/)
* `answer_key` - `<ID>_2025_Answer_Key.json` (fields: `form_1040_summary`, `federal_forms`, `state_and_local`,
  `required_filings`, `gotchas` [id, title, trap, correct_treatment, affected_lines], `software_exceptions` [id, title,
  axcess_default_behavior, axcess_override, override_amount, proconnect_fix])
* `score.json` - the deterministic line comparison already done for you (don't redo arithmetic comparisons)
* The client's preparer notes / review points in the dataset folder may help you understand the intended treatment.

## What to grade
1. **Each gotcha** in `gotchas`: did the run's FINAL return and notes apply the `correct_treatment` and avoid the `trap`?
   - `passed: true` only if the treatment is right in the final return (or correctly not applicable) AND the run shows it
     understood why (notes, workpapers, review points). Right number for the wrong reason -> false, explain.
   - If the preparer missed it but the reviewer caught and fixed it, it passes - note "caught in review".
   - Evidence: quote/point to the file and line (e.g. `02_prepare/prep_notes.md` item 4; `final/return.json` line 13b = 3150).
2. **Each software exception** in `software_exceptions` (v2 dataset): did `software_exceptions.md` (prepare or review)
   identify the issue, the right fix/override location in substance, and the amount (within $5 or clearly equivalent)?
   Wording and exact field paths don't need to match.
3. **Filing completeness**: compare `04_file/filing_package.json` with the key's `state_and_local` and `required_filings`
   (and filings implied by gotchas, e.g. FBAR, 3520, nonresident states, city returns, paper-filing triggers). One
   expectation per required filing: listed with a correct method? Also one expectation "no required filing missing and no
   unnecessary return filed".
4. **Open items**: one expectation - did intake/prep identify the open items/conflicts a careful preparer would (missing
   recurring documents, organizer conflicts), and avoid inventing facts?

## Output - write `grading.json` (exact field names; the viewer depends on them)
```json
{"expectations": [
   {"text": "[gotcha EVG1001-G4] Overtime deduction uses premium only ($3,150)", "passed": true, "evidence": "..."},
   {"text": "[swx EVG1007-SX1] S-corp distribution above stock basis identified ($21,360)", "passed": false, "evidence": "..."},
   {"text": "[filing] MA 1-NR/PY nonresident return listed (e-file)", "passed": true, "evidence": "..."},
   {"text": "[line accuracy] 30/30 key 1040 lines within $2", "passed": true, "evidence": "score.json"},
   {"text": "[bottom line] refund/due within $5 (expected 5,686, got 5,686)", "passed": true, "evidence": "score.json"}],
 "summary": {"passed": 0, "failed": 0, "total": 0, "pass_rate": 0.0},
 "by_category": {"gotcha": [p, t], "swx": [p, t], "filing": [p, t], "lines": [p, t]},
 "weaknesses": ["short, generalisable descriptions of what the skills got wrong and why (root cause), e.g. 'intake read only the summary page of the consolidated 1099 and missed the accrued-interest supplemental page'"],
 "eval_feedback": {"overall": "anything about the test case itself that seems wrong or ambiguous"}}
```
Include the two `score.json` expectations (line accuracy = passed only if 100% of lines match; bottom line) as written.
Be strict but fair: a defensible alternative position documented as such (and flagged for the signer) can pass if the
answer key itself calls the item a judgment call.
