# EVG1007 - Rahman, Dr. Aisha - 2025 Form 1040 / IL-1040 - Preparer Notes

*Synthetic client - Project Evergreen. Return status: **signed off, e-filed 04/13/2026 (federal + IL), accepted.***

## Return summary
| | |
|---|---|
| Filing status | Single |
| AGI (line 11) | $552,750 |
| Deduction | Itemized $72,925 |
| QBI deduction | $0 (SSTB above phase-in range) |
| Taxable income | $479,825 |
| Income tax (line 16) | $132,794 |
| NIIT / Additional Medicare | $186 / $360 (Addl Medicare fully withheld by employer - credit on line 25c) |
| Total tax | $133,340 |
| Payments | withholding $56,360 + estimates $45,000 |
| Form 2210 penalty (line 38) | $779 |
| **Balance due** | **$32,759** (direct debit 04/15/2026) |
| Illinois | tax $27,361; PTE credit $16,073 + payments $19,800 -> **refund $8,512** |

## What I did and why (plain English)
1. **K-1 - use the final.** Tom sent a DRAFT K-1 in February (box 1 $326,100, before the IL PTE tax was booked). The final K-1
   (03/11) shows box 1 $310,000 - net of the corporation's PTE tax deduction. Draft bookmarked "superseded".
2. **Distributions vs stock basis (Form 7203).** Beginning stock basis was only $28,000 (PY 7203). Add 2025 income
   ($310,000 + $640 interest) = $338,640 available for distributions. She took $360,000, so
   **$21,360 is taxable as long-term capital gain** (stock held since 2016) on Form 8949 Part II (box F - no 1099-B).
   Her $120,000 shareholder loan gives her **debt basis, but debt basis never covers distributions** - it only absorbs losses and
   deductions. This is exactly the "debt vs stock basis" trap in our procedure: in Axcess the K-1 basis section must have stock and
   debt entered separately (stock basis line 2 = $28,000; debt basis section = 120,000) or the software nets them and lets
   the distribution through tax-free. After the distribution, the nondeductible expenses ($3,100) and the charitable item
   ($2,000) reduce debt basis to $114,900; future net income restores debt basis first. The loan was not repaid, so no
   gain on repayment. Advised Aisha: in 2026 keep distributions below stock basis (or repay part of the loan instead) - we will
   send the practice manager a mid-year basis estimate.
3. **QBI = $0.** Pediatrics is a health SSTB; taxable income before QBI ($479,825) is above $247,300, so none of
   the K-1 income qualifies even though the W-2 wage limit would be met.
4. **Health insurance.** The S corp paid her $8,400 of health premiums and correctly put them in W-2 box 1 (not boxes 3/5) -
   deducted on Schedule 1 line 17 (Form 7206). Not eligible for any other subsidized plan.
5. **NIIT.** K-1 ordinary income is from a business she materially participates in - not investment income. For the
   excess-distribution gain I followed the sec. 1411(c)(4) approach (proposed Reg. 1.1411-7, which taxpayers may rely on): the gain
   on S-corp stock is excluded to the extent the corporation's assets are used in a nonpassive trade or business (here 100%), shown as
   a line 5c adjustment. NII is just interest and dividends ($4,890) -> NIIT $186. (If the gain were treated
   as NII the NIIT would be $812 higher - flagged for the signer; we consider our position well supported.)
6. **Additional Medicare.** Medicare wages $240,000 -> 0.9% x $40,000 = $360; the corporation withheld exactly $360, which is
   claimed back on line 25c - net zero.
7. **Schedule A.**
   - *SALT:* IL withholding $10,800 + IL estimates **paid in 2025** $6,750 (the 01/15/2026 payment is a 2026
     deduction) + Cook County property tax paid in 2025 $14,800 = $32,350. MAGI is over $500,000, so the new
     $40,000 cap shrinks by 30% of the excess: 40,000 - 30% x $52,750 = **$24,175**. The PTE tax
     the corporation paid is *not* hers to itemize - it is already deducted inside the K-1 and is claimed as a credit in Illinois.
   - *Mortgage interest* $21,600 (Wintrust; balance under $750k).
   - *Charity:* the $25,000 Fidelity Charitable DAF gift counts in 2025 (the year given, not when grants go out) + the K-1 box 12A
     $2,000. The $1,500 GoFundMe for Dr. Lee's family is a gift to individuals - **not deductible** (told Aisha). Used clothing:
     our procedure says to use 3x cost, but the law limits used clothing to its fair market (thrift) value, which can't exceed what she
     paid; Goodwill's guide gives ~$6 per item x ~25 items = **$150**. I did not follow the 3x rule (would have been $1,800).
8. **IL refund 1099-G $2,100 - not taxable.** In 2024 she paid $31,000 of state/local taxes and could only deduct $10,000. Even without
   the $2,100 overpayment she would still have hit the cap, so the refund gave no tax benefit (Rev. Rul. 2019-11) -> $0 on Schedule 1.
9. **Estimated payments - only three were made.** The organizer says 4 x $15,000, but her IRS online account shows no September
   payment. Line 26 = $45,000. She did not meet a safe harbor (90% of 2025 tax = $120,006; 110% of 2024 tax =
   $133,650; paid $101,360), so I computed the Form 2210 penalty (regular method, 7% rate assumed for
   every period) = **$779** and included it on line 38 rather than waiting for an IRS bill.
10. **AMT check.** Tentative minimum tax $108,620 < regular tax $132,794 -> no AMT (Form 6251 not required).
11. **Illinois.** Base income = federal AGI $552,750 (no subtraction for the S-corp income; the PTE tax add-back happens at the
    entity). No exemption and no 5% property-tax credit because AGI is over $250,000. Tax $27,361 less PTE credit $16,073,
    withholding and 4 estimates -> refund $8,512.

## Open items / advice
- 2026 federal estimates: 110% of 2025 tax = $146,674 -> $36,700 per quarter (less
  withholding). Suggested increasing W-2 withholding from the S corp instead (withholding counts as paid evenly).
- 2026 note for next year's preparer: the 2025 IL refund ($8,512) will be taxable on the 2026 return only to the extent it
  produced a 2025 benefit - 2025 SALT paid $32,350 less refund = $23,838 vs 2025 cap
  $24,175 -> about $337 taxable.
- Form 706/estate items: n/a. Portability n/a. Consider repaying part of the shareholder loan in 2026 (tax-free return of debt basis
  only to the extent of remaining debt basis $114,900 - the rest would be gain) - coordinate with Kessler & Park.

## Hand-off to signer / routing
- [x] Return locked; Accountant's copy saved as *reviewed*
- [x] Federal 1040 - e-file; IL-1040 - e-file; no FBAR
- [x] Due date 04/15/2026 (no extension); balance due by direct debit 04/15/2026 incl. 2210 penalty
- [x] eSign (Form 8879 / IL-8453) - email preferred
- [x] Special: signer to review NIIT line 5c position (item 5)
- Billing: K-1 tier $2,400 + 1.0 hr Form 7203/basis + 0.5 hr 2210 = standard rates; nothing to W/O.
