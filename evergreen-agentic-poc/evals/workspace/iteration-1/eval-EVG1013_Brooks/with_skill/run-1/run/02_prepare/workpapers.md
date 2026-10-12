# EVG1013 - Brooks - 2025 workpapers (off-system computations)

## WP-1 NSO exercise and same-day sale - basis correction (Form 8949 code B)
Source: W-2 box 12 V $22,000 (PBC/02); 1099-B (PBC/04); E*TRADE supplement (PBC/05).
| | Amount |
|---|---:|
| Shares | 2,000 |
| Exercise price $2.00 x 2,000 = cash basis (reported on 1099-B) | 4,000.00 |
| Compensation income FMV $13.00 - $2.00 = $11.00 x 2,000 (in W-2 box 1, code V) | 22,000.00 |
| Adjusted basis (Treas. Reg. 1.83-4(b), 1.6045-1(d)(6)) | **26,000.00** |
| Proceeds, net of $24.95 commission (1099-B 1d) | 25,975.05 |
| Gain/(loss) - short-term, box A, code B | **(24.95)** |
Effect: removes $22,000 of double-counted income vs. the 1099-B as reported.

## WP-2 ISO exercise-and-hold - AMT (Form 6251 line 2i)
Source: Form 3921 (PBC/03); supplement (PBC/05).
| | Amount |
|---|---:|
| 4,000 sh x (FMV $14.00 - exercise $1.50) | **50,000.00** |
| Regular-tax basis of ISO lot (4,000 x $1.50) | 6,000.00 |
| AMT basis of ISO lot (6,000 + 50,000) | 56,000.00 |
| 12/31/2025 value (4,000 x $11.35) | 45,400.00 |
No 2025 sale, so no disqualifying disposition and no same-year reversal (IRC 56(b)(3), 422). Holding period for qualifying
disposition: after 02/14/2026 (1 yr from exercise) and 03/15/2023 (2 yrs from grant) -> sales after 02/14/2026 qualify.

Form 6251 (engine): TI 150,209 + std ded 15,750 + ISO 50,000 = AMTI 215,959; exemption 88,100 (no phase-out; AMTI < 626,350);
26% x 127,859 = TMT 33,243; regular tax 28,897; **AMT 4,346**.

## WP-3 Minimum tax credit carryforward to 2026 (Form 8801 computation)
AMTI from exclusion items only = 150,209 + 15,750 = 165,959; less exemption 88,100 = 77,859 x 26% = 20,243 TMT on exclusion
items. 20,243 < regular tax 28,897 -> exclusion-item AMT = 0. Entire AMT is from the deferral item (ISO).
**MTC carryforward to 2026 = $4,346** (Form 8801 filed with the 2026 return; credit usable when regular tax > TMT,
typically in the year of sale). No 2024 MTC carryover (PY summary), so no Form 8801 for 2025.

## WP-4 HSA - Form 8889 and excess contribution
Source: W-2 code W (PBC/02); Fidelity history (PBC/08); 5498-SA (PBC/07); return-of-excess confirmation (PBC/13).
| | Amount |
|---|---:|
| Self-only HDHP, 12 months; age 30 -> limit (no catch-up) | 4,300.00 |
| Employer contributions incl. cafeteria payroll ($3,300 + $1,000 seed) = W-2 code W (8889 line 9) | 4,300.00 |
| Remaining room | 0.00 |
| Participant after-tax deposit 04/11/2025 | 1,000.00 = excess |
| Excess withdrawn 09/15/2026 with NIA $38 (before 10/15/2026 extended due date) | 1,038.00 |
Treatment (IRC 4973(g)/223(f)(3); Form 8889 instructions line 2): line 2 = $0 (excess withdrawn by due date is excluded),
line 13 HSA deduction = $0, no Form 5329 excise. $38 NIA is income in 2026, the year received (2026 1099-SA code 2).
No 2025 distributions (no 1099-SA for 2025).

## WP-5 Loomwork 83(b) timeliness
Source: RSA (PBC/09); Form 15620 + USPS receipt (PBC/10); cap table (PBC/14).
* Transfer date 11/03/2025 (RSA; Form 15620 line 7). 30-day deadline under IRC 83(b)(2) / Reg. 1.83-2(b): **12/03/2025**.
* Form 15620 signed 12/08/2025; USPS certified mail postmark **12/10/2025** (timely-mailing rule of IRC 7502 needs a
  postmark on or before the due date). Company copy received 12/08/2025.
* Conclusion: the election is untimely and invalid; no extension/9100 relief is available for a statutory deadline.
  Shares remain substantially nonvested property; **$0 income in 2025** (not the $8,000 on line 12). Compensation income
  = FMV at each vesting date (from 11/03/2026); any dividends before vesting would be compensation. Advice item for client.

## WP-6 Deduction choice
Itemized: IL withholding 8,150 (SALT under $40k cap) + charity 250 = 8,400 < standard 15,750 -> standard.

## WP-7 Payments and Form 2210
Withholding W-2 box 2 27,600 + extension payment 6,000 (Form 4868, 04/13/2026, receipt log) = 33,600.
Required annual payment = lesser of 90% x 33,243 = 29,919 or 100% of 2024 tax 23,526 (2024 AGI 140,986 <= 150k) = 23,526.
Withholding (treated as paid evenly) 27,600 >= 23,526 -> no penalty; Form 2210 not required.
2026 safe harbor: 2025 AGI > $150k -> 110% x 33,243 = $36,567.

## WP-8 Illinois IL-1040
Base income = federal AGI 165,959 (no subtractions: Wealthfront interest is bank interest, not US obligations; no
retirement/SS). Exemption 2,850 (AGI < $250k). Net income 163,109 x 4.95% = 8,073.90 -> 8,074. IL withholding 8,150
(W-2 box 17). **Refund 76.** No IL estimates / extension payment. Chicago: no city income tax.

## WP-9 Prior-year comparison
| | 2024 | 2025 | Why |
|---|---:|---:|---|
| Wages | 139,880 | 164,700 | raise + $22,000 NSO income |
| Interest | 1,106 | 1,284 | |
| AGI | 140,986 | 165,959 | |
| Total tax | 23,526 | 33,243 | higher income + AMT 4,346 (ISO) |
| Refund | 884 | 357 | AMT largely offset by $6,000 extension payment |
