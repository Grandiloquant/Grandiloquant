# EVG1018 - Vasquez, Elena - 2025 Form 1040 - Preparer Notes

*Synthetic client - Project Evergreen. Return status: **signed off; e-filed 09/15/2026 (extended), accepted.***

## Return summary
| | |
|---|---|
| Filing status | Single |
| Wages (Bayline W-2) | $90,000 |
| S corp K-1 ordinary income (as corrected) | $82,000 (K-1 $62,000 + 311(b) gain $20,000) |
| Capital loss (trust carryover, limited) | ($3,000) |
| AGI (line 11) | $165,000 |
| Standard deduction | $15,750 |
| QBI deduction | $14,840 |
| Taxable income | $134,410 |
| Total tax | $24,960 |
| Payments (withholding $11,400 + estimates $12,800 + extension $2,000) | $26,200 |
| **Refund** | **$1,240** |

## What I did and why (plain English)
1. **The truck (IRC 311(b)).** Bayline gave Elena its 2021 F-250 on 08/29/2025. When an S corp distributes property that is worth
   more than its tax basis, the *corporation* is treated as if it sold it at fair market value. FMV $32,000 (dealer appraisal) -
   adjusted basis $12,000 = **$20,000 gain**. Because the truck had $33,000 of depreciation, the whole gain is IRC 1245 recapture ->
   ordinary income, which passes through on K-1 box 1. Gulfside's K-1 left it out and showed the distribution at book value.
   I entered the K-1 manually with box 1 $82,000 (Section 3 direct entry) and the distribution at FMV. Mark Tillman (Gulfside)
   agreed on 09/02/2026 and will amend the 1120-S after 10/15, so I attached **Form 8082** (inconsistent treatment) to explain the
   difference from the K-1 as issued.
2. **Stock basis (Form 7203).** Increases first (income incl. the gain + interest), then distributions at FMV ($40,000 cash + $32,000
   truck = $72,000), then nondeductible expenses and the charitable item: $95,000 -> **$101,750**. Basis was sufficient, so
   no distribution is taxable. Elena's basis in the truck is $32,000 (personal use - no deduction). Debt basis $0.
3. **2% shareholder health insurance.** W-2 box 14 shows $7,800 of premiums included in box 1 (not in boxes 3/5 - correct).
   Deducted on Schedule 1 line 17 (limited to her Bayline wages).
4. **QBI.** Boat repair is not an SSTB. QBI = $82,000 (the 1245 recapture is ordinary trade-or-business income, so it is QBI)
   less the health-insurance deduction $7,800 = $74,200. Taxable income before QBI is under $197,300, so the
   deduction is simply 20% = $14,840; the W-2 wages ($310,000) and UBIA ($180,000) from Statement A are recorded but not limiting.
5. **Grandmother's trust - final K-1.** Used the FINAL K-1 received 08/21/2026 (the June DRAFT with $410 interest is superseded).
   Interest $420, dividends $1,380 ($1,100 qualified).
   - **Suspended passive losses ($18,400).** The trust distributed the rental condo to Elena on 09/15/2025. Under IRC 469(j)(12)
     those losses are **not deductible** by anyone - they are added to the basis of the condo. Elena's basis = trust's adjusted basis
     $222,546 + $18,400 = **$240,946** (carryover basis; no 643(e)(3) election; holding period
     includes the trust's). The $305,000 FMV is irrelevant for basis. Recorded in PERM with the land/building split.
   - **Capital loss carryover $3,200 (box 11 code E).** Passes to the beneficiary in the year the trust terminates -> Schedule D line 14.
     Net capital loss is limited to $3,000; **$200 long-term carries to 2026**.
6. **Condo - no 2025 Schedule E.** Elena is painting it and will list it in March 2026 (HOA minimum lease 3 months - long-term rental).
   Not held out for rent in 2025, and the trust prepaid the 2025 HOA and taxes, so nothing to report. For 2026: continue the trust's
   27.5-year schedule on the carryover building basis ($174,546; IRC 168(i)(7)); treat the $14,431 basis increase as a new
   27.5-year asset placed in service in 2026 (*assumption - no direct guidance on depreciating a 469(j)(12) increase; flagged for signer*).
7. **Standard deduction.** Itemized (home mortgage $6,180 + property tax $3,920 + charity incl. K-1 box 12A $2,500 + $400) is less
   than the $15,750 standard deduction (even adding ~$1,500 of Florida sales tax), so the K-1 charitable contribution gives no benefit this year (it still reduces basis).
8. **Payments.** 4 x $3,200 estimates + $2,000 with extension + $11,400 withholding. No Form 2210 penalty: withholding + timely
   estimates ($24,200) exceed 100% of 2024 tax ($20,880; 2024 AGI under $150,000).
9. **Not NIIT / no Additional Medicare.** S corp income is nonpassive (she runs the business); MAGI < $200,000.

## Hand-verification
- AGI: wages 90,000 + interest 1,780 + dividends 2,020 + Sch E 82,000 - 3,000 capital loss - 7,800 health = $165,000.
- Taxable income $134,410: QD/CG worksheet (qualified dividends 1,620 at 15%) -> tax $24,960.

## Open items / client communication
- Gulfside to file amended 1120-S / amended K-1 (box 1 $82,000, 16D $72,000). When received, confirm
  it matches our return - no 1040-X needed. Calendar follow-up 11/15/2026.
- Told Elena the $18,400 suspended losses are not usable, but they increase her condo basis (lower gain / higher depreciation later).
- Ask for the 2026 lease and placed-in-service date for the condo next season.

## Hand-off to signer / routing
- [x] Return locked; Accountant's Copy saved as *reviewed*
- [x] Federal 1040 - e-file; extended due date 10/15/2026 (Form 4868 accepted 04/13/2026)
- [x] Form 8082 attached (e-file compatible); no state (FL); no FBAR
- [x] eSign 8879 - email elena@baylinemarine.example
- [x] Refund direct deposit ****0917
- Billing: $2,800 quote + 1.5 hrs (311(b) research, Form 8082, trust basis memo) - external reason (S corp preparer / trust), chargeable.
