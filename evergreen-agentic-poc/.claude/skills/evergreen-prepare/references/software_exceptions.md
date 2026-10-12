# Software exception log (CCH Axcess + Intuit ProConnect)

The firm files in CCH Axcess; some partner firms use ProConnect. Real tax software calculates from what is keyed in and
cannot know facts that live outside a single form. Log every place this return needs a manual calculation, override, special
input or alternate filing path - **especially "silent" ones where no diagnostic fires** and the wrong answer just calculates.

## What belongs in the log (and what doesn't)
Log an item when the **software's default handling of the documents/inputs would produce a wrong return** or needs a
special input, override, attachment or alternate filing path. Include:
* **Silent input traps** - duplicate or corrected forms the scanner would load twice; amounts the software takes at face
  value but which must be adjusted (equity-comp basis, accrued interest, wash sales across accounts, QCD/rollover codes).
* **Manual-calc inputs** - items you computed off-system that need specific entries for the software to agree (prior-year
  tax/AGI for the 2210 safe harbor, 8606 year-end balances, K-1 stock vs debt basis, carryovers for a new client).
* **State and local module defaults** - wage bases the state module pulls from the wrong box, exemptions it takes from the
  federal dependent screen, credits for other-state tax, city returns.
* **"Negative" exceptions** - returns or forms the software would generate that must be suppressed (a nonresident state
  under a reciprocity/de minimis rule, a duplicate dependent claim) and forms it can't produce (filed separately / paper).
* When one source causes two problems (a rental 1098 routed to Schedule A AND its escrow statement importing as a second
  1098), log both halves.
Don't pad the log with pure tax judgments the software has no default for (e.g. "newborn is a dependent") - those belong in
the prep notes. Amounts must be the corrected amount you entered, not the raw form figure.

## Format (software_exceptions.md)
| ID | Workbook tab | Exception | Silent? | Amount | Axcess fix (input/override location) | ProConnect fix | E-file impact |
Then one short paragraph per item: what the software does by default, why that's wrong here, the calc.

## The firm's CCH Axcess Exception Workbook - calculation tabs
3 K-1 basis limitation · 4 At-risk (6198) · 5 Passive (8582, $25k allowance) · 6 Depreciation federal vs state/AMT ·
7 Multi-state allocation & resident credit · 8 Form 2210 safe harbor · 9 AMT line 2n loss limits · 10 Capital loss carryover
(new clients) · 11 §751(b)/§704(c)/§737/§752(b) · 12 S-corp stock vs debt basis · 13 Trust termination suspended PAL ·
14 Bond accrued interest & premium · 15 Mortgage interest limit · 16 Vacation home allocation · 17 Equity comp basis &
cross-account wash sales · 18 NUA & IRD (§691(c)) · 19 Crypto income & basis · 20 Insolvency (982) · 21 §1033 replacement ·
22 Reorg boot/§331/§1259/§1244 · 23 Multi-state W-2 workdays · 24 Rare events (throwback, foreign trust, §962...).
Items with no tab (SSTB checkbox, NIIT 5c adjustment, state-refund worksheet, PTE routing, IP PIN, unsupported forms) are
"log-only" (tab 2, Diagnostics Log).

## Rules for describing software behaviour
* **Never invent CCH Axcess diagnostic numbers** - they vary by release. Describe the message gist or write "None - silent".
  Describe input locations the way the workbook does ("Income/Deductions > S Corporation Passthrough > Basis Limitation") and
  add "verify field path in current release" when unsure.
* ProConnect behaviours documented by Intuit (safe to state):
  - Form 3520 is not supported - prepare outside; it's mailed separately anyway.
  - Form 8865 is not available in ProConnect or Lacerte.
  - Form 8615 has no Family Link in ProConnect (Lacerte feature) - parent information keyed manually (diagnostic ref 826).
  - Form 7203 needs "Stock basis at beginning of year" (diagnostic ref 56844); debt basis entered separately; 7203 produced
    only with a loss, distribution, disposition or loan repayment.
  - Section 962 election is a manual practitioner workaround (computed 962 tax entered as an adjustment on the other-taxes
    screen); Form 1118 isn't available.
  - Form 8949 summary reporting: attach the detail PDF (Form 8949 Exception Reporting Statement) to suppress Form 8453
    (diagnostic ref 10322).
  - Form 1042-S withholding can't be e-filed on a Form 1040 - paper file.
  - New-client prior-year passive losses: enter Regular AND AMT amounts separately.
  - 1099-C insolvency worksheet flows to Form 982; attribute reduction still needs review.
  For anything else say "screen/field per current release - verify".
* ProConnect tiers (incl. the top bundles) have the same form coverage; tiers only change return counts/users.
