# EVG1022 - Whitfield, Gregory & Ellen - 2025 Form 1040 - Preparer Notes

*Synthetic client - Project Evergreen. NEW CLIENT. Return status: **signed off; federal, PA-40 and MA 1-NR/PY e-filed 09/17/2026 (extended), accepted.***

## Return summary
| | |
|---|---|
| Filing status | Married filing jointly (Gregory 58, Ellen 56) |
| Wages (line 1a) | $472,000 |
| Taxable / tax-exempt interest | $9,085 / $6,396 |
| Ordinary / qualified dividends | $18,400 / $15,900 |
| Pensions (5a / 5b) | $1,420,000 / $96,000 (NUA cost basis only) |
| Capital gain (line 7) | $27,000 (net ST ($21,000); net LT $48,000) |
| AGI | $622,485 |
| Itemized deductions | $36,240 (SALT limited to $10,000) |
| Taxable income | $586,245 |
| Tax (QD & CG worksheet) | $135,700 |
| Additional Medicare / NIIT | $2,304 / $2,070 |
| Total tax | $140,074 |
| Payments (withholding $105,769 + estimates $32,000 + extension $3,000) | $140,769 |
| **Federal refund** | **$695** |
| PA-40 | tax $17,821 - MA credit $1,373 = $16,448; **refund $86** |
| MA 1-NR/PY | tax $2,191; **refund $109** |

## What I did and why (plain English)
1. **Where Gregory worked (multi-state W-2).** Keystone coded all of Gregory's wages to PA (box 15/16). His Outlook export (uploaded twice -
   item 04b marked DUP) shows 165 workdays from 01/02 to his last day 08/29 after removing 4 company holidays and 4 PTO days:
   PA 112, NJ 22, MA 18, IL 13. (His own guess of "about 20 MA / 15 IL" was close but not usable.)
   - **New Jersey** - PA and NJ have a reciprocal agreement for employee compensation: a PA resident's NJ-earned wages are taxed only by PA.
     No NJ-1040NR; nothing to credit.
   - **Illinois** - Illinois does not tax a nonresident employee's compensation when he is present in IL performing services for 30 or
     fewer working days in the year (rule effective 2020). 13 days -> no IL return. *Assumption to verify:* no exception applies to
     Gregory's role; if IL-source, IL tax would be about $1,599.
   - **Massachusetts** - no day threshold for nonresident employees. MA-source wages = box 1 $410,000 x 18/165 =
     **$44,727** (workday method; box 14 severance/PTO payout is in box 1 and allocated with the rest - it relates to 2025 service).
2. **MA Form 1-NR/PY.** Joint nonresident return. Nonresident deduction & exemption ratio = MA-source income / income from all sources
   ($44,727 / $628,881 = 0.0711). The denominator is approximated from the federal return (wages, interest incl. the
   PA Turnpike bond - MA taxes other states' munis -, dividends, capital gain, taxable 401(k) amount); it only drives the prorated
   exemption ($8,800 x ratio = $626) and the Social Security/Medicare deduction (2 x $2,000 x ratio = $284 -
   *assumption: prorated for nonresidents*). Tax 5% x $43,817 = **$2,191**; no 4% surtax (far below the ~$1.08M threshold).
   No MA withholding; the $2,300 M-4868 payment covers it. No M-2210 penalty assumed - no MA tax in 2024 (New England territory started
   01/2025) - *verify the exception*.
3. **PA-40 and the credit for MA tax.** PA compensation is W-2 box 16 (**includes** the $31,000 401(k) and Ellen's $3,000 403(b) deferrals):
   $506,000. Interest $9,085 (PA Turnpike bond is a PA obligation - exempt; *assumption: PA interest = federal net of the
   ABP and accrued-interest reversals*), dividends $18,400, net gains $47,000 (2025 sales only - PA has no capital loss
   carryover - and the IVV loss is allowed because PA has no wash-sale rule; *verify*; effect $553 of PA tax). The 401(k)
   distribution after retirement is not PA income. PA tax 3.07% x $580,485 = $17,821. Schedule G-L credit = lesser of MA tax
   $2,191 or PA tax on the income MA taxed ($44,727 x 3.07% = $1,373) -> **$1,373**. I used the MA-taxed
   wages (box 1 based, without the 401(k) deferral portion that MA did not tax) - conservative.
4. **401(k) lump sum - NUA.** Gregory separated from service 08/29/2025 at 58 and Fidelity distributed the **entire** balance in one tax year
   (lump-sum distribution): 8,000 KMDV shares in kind (FMV $640,000) and a direct rollover of $780,000 to a Fidelity IRA.
   Only the plan's cost basis of the stock, **$96,000**, is taxable now (1099-R box 2a; line 5b). The NUA of $544,000 is not taxed
   until the shares are sold and will be long-term capital gain whenever sold. Rollover: line 5a only, marked "Rollover". Code 2 = the
   age-55 separation exception - no 10% tax, no Form 5329. No withholding (stock-only distribution). Taxing the full FMV would have
   overstated tax by $199,260.
5. **Wash sale across accounts.** Gregory sold 400 IVV at an $18,000 loss on 11/10 (his account). Ellen's email and IRA statement show her IRA
   bought 420 IVV on 11/20 - within 30 days. A purchase by a spouse or in an IRA counts (Pub. 550; Rev. Rul. 2008-5). Schwab's 1099-B
   can't see it (different owner/account). Form 8949 code W, +$18,000: the loss is **permanently** disallowed - the IRA gets no basis step-up.
6. **Bonds (Schedule B).** Pfizer 4.75% 2033 bought 03/12 at 104.25 with $2,981.94 of accrued interest paid to the seller (trade confirm +
   Schwab supplemental page). Schwab reports the full coupons in box 1 and the premium amortization in box 11. Schedule B: gross box 1, then
   "ABP Adjustment" (-786.12) and "Accrued interest" (-2,981.94) lines -> taxable interest $9,085. PA Turnpike muni:
   box 8 $7,500 less box 13 premium $1,104.30 = $6,396 on line 2a (premium on a tax-exempt bond is not deductible; it just
   reduces the exempt interest and basis). Ellen asked if the accrued interest is "deductible" - it's a reduction of interest income, done.
7. **Capital loss carryover (new client).** The prior preparer's worksheet carried the whole $38,000 as long-term. Their own 2024 Schedule D
   shows ST (29,000) and LT (12,000); the $3,000 allowed loss uses short-term first -> correct carryover **ST $26,000 / LT
   $12,000**. 2025: ST gains $5,000 - 26,000 = ($21,000); LT 60,000 - 12,000 = $48,000; net $27,000 - all
   taxed at 15%. With the wrong character the $5,000 ST gain would be taxed at 35% -> **$1,000** more tax. Nothing carries to 2026.
8. **Itemized / SALT.** PA withholding + local EIT + 2024 PA balance paid = $21,004, real estate tax $9,830.
   MAGI $622,485 is over $500,000 -> SALT cap = $40,000 - 30% of the excess = below the floor -> **$10,000**. Mortgage $11,240 +
   charity $15,000 -> itemized $36,240 > standard $31,500. AMT checked - none (tentative minimum tax below regular tax).
9. **Additional Medicare / NIIT.** Medicare wages $506,000 - $250,000 = $256,000 x 0.9% = $2,304; Keystone withheld
   0.9% over $200,000 ($2,169 - Form 8959 line 24, included on line 25c). NII = interest + dividends + net capital gain = $54,485 (the 401(k)
   distribution and muni interest are excluded) -> NIIT $2,070.
10. **Estimated tax penalty.** None - 4 x $8,000 timely estimates plus withholding (treated as paid evenly) meet 25% of the required annual
    payment each quarter (90% of 2025 tax $126,067 is less than 110% of 2024 tax $181,480). Workbook tab 8.

## Open items / client communication
- **KMDV shares (NUA):** basis is $12.00/share ($96,000) - Schwab shows $80.00 in its unrealized gain report. Gregory's handwritten note asked
  about this. Do NOT let a future 1099-B basis of $640,000 through. When sold: NUA portion LTCG regardless of holding period. Recommended
  he talk to us before selling (and before any PA-basis question arises).
- Ellen's IRA and Gregory's taxable account: told them to avoid buying the same fund in either account within 30 days of a loss sale.
- 2026: Gregory no longer has wages - 2026 estimates (federal/PA) sent; no MA/IL filings expected.

## Hand-off to signer / routing
- [x] Return locked; Accountant's Copy saved as *reviewed*
- [x] Federal 1040 (extended) - e-file; due 10/15/2026
- [x] PA-40 (extended) - e-file; due 10/15/2026
- [x] MA Form 1-NR/PY (extended) - e-file; due 10/15/2026
- [x] No NJ or IL returns (reciprocity / 30-day rule - documented on workbook tab 23)
- [x] No FBAR / no foreign items
- [x] eSign (8879, PA-8879, M-8453); call with Gregory held 09/14/2026
- Billing: quote $4,800 + MA $450 + 1.5 hrs re-creating the capital loss carryover from the prior preparer's return (new-client setup).
  Calendar export received 03/09 - no expedite fee.
