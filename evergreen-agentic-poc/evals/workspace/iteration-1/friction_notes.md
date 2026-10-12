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
