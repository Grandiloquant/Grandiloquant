# EVG1013 - Brooks, Nathan - 2025 Form 1040 - Preparer Notes

*Synthetic client - Project Evergreen. Return status: **signed off, extended return e-filed 09/25/2026 (federal + IL).***

## Return summary
| | |
|---|---|
| Filing status | Single |
| AGI (line 11) | $165,959 |
| Deduction | Standard $15,750 (no itemizing - $250 charity only) |
| Taxable income | $150,209 |
| Regular tax (line 16) | $28,897 |
| AMT (Schedule 2 line 1 / Form 6251) | $4,346 |
| Total tax | $33,243 |
| Withholding / extension payment | $27,600 / $6,000 |
| **Refund** | **$357** (direct deposit) |
| Illinois | tax $8,074, withheld $8,150, refund $76 |
| Carryforward | Minimum tax credit (Form 8801) $4,346; ISO AMT basis $56,000 (regular basis $6,000) |

## What I did and why (plain English)
1. **W-2.** Box 1 $164,700 already includes the $22,000 NSO spread (box 12 code V). Box 12 D (401k) and W (HSA) are
   pre-tax. Medicare wages are under $200,000, so no Additional Medicare Tax.
2. **NSO same-day sale (Form 8949 box A, code B).** E*TRADE reported cost basis of $4,000 (exercise price only - required
   broker reporting for compensatory options). The $22,000 spread was taxed on the W-2, so real basis is $26,000. I kept the
   1099-B basis in column (e) and entered a ($22,000) code B adjustment -> a ($25) loss (the commission). Without this, the
   same $22,000 would have been taxed twice. The Stock Plan Transactions Supplement is the same sale (informational only) -
   bookmarked DUP/support, not entered.
3. **ISO exercise-and-hold (Form 6251).** Form 3921: 4,000 shares, strike $1.50, FMV $14.00 on 02/14/2025 -> $50,000
   bargain element. Not regular income (no sale; ISO rules), but it is an AMT adjustment (line 2i). AMTI $215,959
   less the $88,100 exemption x 26% = tentative minimum tax $33,243 vs regular tax $28,897 ->
   **AMT $4,346**. Because the ISO is a *deferral* item, the whole AMT becomes a **minimum tax credit carryforward
   ($4,346, Form 8801)** usable in future years when regular tax exceeds TMT (e.g. the year he sells the shares).
   AMT basis in the shares is $56,000 vs regular basis $6,000 - recorded in PERM for the eventual sale (a sale after
   02/14/2026 is a qualifying disposition: more than 1 year after exercise and more than 2 years after the 03/15/2021 grant).
4. **Loomwork founder shares - late 83(b).** Grant date 11/03/2025; Form 15620 signed 12/08 and USPS postmark 12/10/2025 =
   37 days. Section 83(b) requires filing within 30 days of transfer (by 12/03/2025) and the IRS cannot extend it. The
   election is **invalid**, so nothing is reported for 2025 (the $8,000 "amount includible" on his form is not income) and
   the copy is not attached. Consequence: ordinary compensation income at each vesting date equal to FMV then (first
   5,000 shares on 11/03/2026), and capital-gain holding period starts at vesting. Client emailed with this explanation;
   suggested he ask Loomwork's counsel about cancelling and re-granting the shares with a new, timely 83(b).
5. **HSA (Form 8889).** Self-only HDHP all year; limit $4,300. Code W $4,300 ($3,300 his pre-tax payroll + $1,000
   employer seed) already uses the full limit, so his $1,000 April transfer is an excess contribution and deduction is $0.
   He withdrew $1,000 + $38 earnings on 09/15/2026, before the 10/15/2026 extended due date -> **no 6% excise / no Form 5329**.
   The $38 is taxable in **2026** (1099-SA code 2 next year) - noted in PERM for the 2026 return.
6. **Interest.** Wealthfront $1,284 (under $1,500, so Schedule B is not required; it prints for reference only).
7. **Estimated tax penalty.** Balance before extension payment was ~$5,643 because of AMT. Withholding
   $27,600 exceeds 100% of 2024 tax ($23,526; 2024 AGI under $150,000), so the prior-year safe harbor is met - no Form 2210.
   The $6,000 extension payment made 04/13/2026 covers the balance, so there is no late-payment penalty or interest.
8. **Illinois.** IL-1040 starts from federal AGI (NSO income in IL wages; IL has no AMT, so no ISO adjustment). Exemption
   $2,850 (AGI under $250,000). Tax $8,074 vs withholding $8,150 -> refund $76. IL gives an automatic
   6-month extension; nothing was owed so no IL-505-I payment. **Chicago has no city income tax.**
9. **Charity.** $250 Chicago Public Library Foundation - no benefit (standard deduction; the non-itemizer charitable deduction
   starts in 2026, so it will matter next year).

## Open items / client communication
- None open. HSA excess corrected 09/15/2026 (confirmation in PBC #13).
- Advised (email 09/18): (a) AMT credit carryforward $4,346 will be recovered in later years - keep records;
  (b) any 2026 sale of the ISO shares is a qualifying disposition (after 02/14/2026); the AMT/regular basis difference
  reverses on Form 6251 in the sale year and frees up the credit - projection offered (PROJ project); (c) Loomwork vesting income starts 11/2026 -
  plan withholding/estimates; (d) cap HSA at payroll only for 2026 (limit $4,400 self-only).

## Hand-off to signer / routing
- [x] Return locked; Accountant's copy saved as *reviewed*
- [x] Federal 1040 - e-file; due 10/15/2026 (extended; 4868 filed 04/13/2026 with $6,000)
- [x] IL-1040 - e-file; due 10/15/2026 (automatic extension)
- [x] No FBAR / no foreign filings
- [x] eSign (8879 + IL-8453 equivalent) - email preferred, nathan.brooks@example.com
- [x] Special instructions: do NOT attach Form 15620 copy; PERM updated with ISO AMT basis, MTC carryforward, 2026 HSA $38
- Billing: equity-comp tier $1,850 + 2 equity events ($500) + HSA excess follow-up 0.5 hr. PBC items were complete, so
  no chargeable client-caused rework; the 83(b) research memo (1 hr) billed under MISC as a consultation.
