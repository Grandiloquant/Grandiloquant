# Iteration 1 - executor friction reports (with_skill runs)

## EVG1001 Bell
- Subagents have no Agent tool -> "fresh reviewer subagent" impossible; self-review fallback weak. (Fix: harness runs review as a separate agent.)
- Overtime: no default when box 14 just says "OVERTIME" -> premium vs total ambiguity.
- Engine: no HSA/8889 input (workpaper only); Schedule B prints under $1,500; 2441/Sch 1-A lines show raw dict keys.
- File skill: no guidance for filing after 04/15 with unknown extension status.
- Intake schema: no dependent age / refund method fields. Copy list missing signer_handoff + invoice.
- Duplicate detection for photos relies on reading the image (no tool help).

## EVG1013 Brooks
- Same: no Agent tool -> self-review.
- Engine: no Form 8889 input/output; no Form 8801 MTC carryforward or AMT basis tracking (done by hand).
- facts_schema: no guidance for a timely-corrected HSA excess contribution.
- 2025 reference: missing 8801/MTC guidance, IL extension/payment rule, timely-mailing (§7502) rule for 83(b).
- Billing ambiguity in client fee schedule (base fee vs per-event).
- filing_package.json: no carryforwards field; unclear source for final/return.md.

## EVG1003 Okafor
- Same: no Agent tool -> self-review.
- No "as-of date" for the run: sandbox date (Oct 2026) is after 04/15 while the scenario reads as a filing-season engagement -> agents flag lateness. (Fix: harness/skill should state the engagement date or tell agents to read it from the receipt log.)
- extract_docs keeps spaces in filenames (e.g. "(1).pdf.txt") - breaks naive shell loops.
- Reference gap: car washes are covered by the standard mileage rate; rider supplies are not.
- facts_schema gaps: Sch 1-A tips = W-2 + 4137 + SE tips combined? SE tips limited to Sch C net; se.w2_ss_wages should include box 7 tips + 4137 tips (Sch SE 8a/8b).
- Engine: Schedule C detail only lives in workpapers (net profit input only).

## EVG1016 Doyle
- Same: no Agent tool -> self-review.
- Agent applied a Michigan 2025 overtime subtraction "from memory" (MI refund 381 vs key 175) - unverified law applied from recall; skill should require state positions not in the reference to be flagged, not applied.
- Reference gaps: MI tips/overtime + retirement subtraction, Grand Rapids treatment of retirement distributions and due date, city exemptions vs 8332 release.
- facts_schema: no field for 5329 exception codes, HOH qualifying person, 2441 lived-apart rule.
- Separation cases: Sch 1-A "married must file jointly" vs considered-unmarried HOH; splitting a joint 1098.
- Run date after 04/15 again (no as-of date).

## EVG1008 O'Brien
- Same: no Agent tool -> self-review.
- Engine: no Sch E detail / 8582 / 280A carryforward inputs -> carryforwards only in workpapers (return.json carryforwards block empty).
- Reference gaps: vacation-home details (pre-conversion costs, guest supplies, conversion basis = lower of FMV/basis), firm default IRS vs Bolton; PA specifics (PA vs §280A, extension form, local EIT).
- Scanner truncated 1098 box 10 ("5,4") - long values in form boxes get clipped.
- SOP text still says gambling follows 2026 rules (conflicts with CLAUDE.md) - CLAUDE.md wins.
- Notable catch: agent spotted a likely 2024 CTC over-claim (Emma 17 at end of 2024) in the PY summary.
