# EVG1022 Whitfield - 2025 Form 1040 preparation notes

MFJ, PA residents (West Chester, West Goshen Twp). Neither spouse was 65 or older, and they have no dependents. The return is on extension (4868 accepted 04/15/2026), so the extended due date is **10/15/2026**.

## Result (engine: final/return.json)
| Item | Amount |
|---|---:|
| AGI | 622,485 |
| Itemized deductions | 36,240 |
| Taxable income | 586,245 |
| Income tax (line 16) | 135,700 |
| Additional Medicare tax 2,304 + NIIT 2,070 | 4,374 |
| Total tax (line 24) | 140,074 |
| Payments: W-2 withholding 103,600 + Add'l Medicare withheld 2,169 + ES 32,000 + 4868 3,000 | 140,769 |
| **Refund** | **695** |
| AMT (6251 test) | 0 |
| Form 2210 penalty | none (see below) |

## Income treatment
- **Wages:** Gregory (Keystone) box 1 is 410,000, which includes the 38,500 severance/PTO payout. Ellen (BVSD) box 1 is 62,000. Total 472,000. Box 5 is consistent: Gregory's 441,000 less the 31,000 401(k) deferral equals box 1.
- **Interest:** Schwab 2207 box 1 is 12,640.55. From it I subtracted the **accrued interest paid** on the Pfizer bond purchased 03/12/2025 (2,981.94, per the trade confirmation; this answers Ellen's question). It is a reduction of interest, not an itemized deduction. I also subtracted the **box 11 bond premium amortization** (786.12). Adding BFCU interest of 212.40 gives 9,084.89 taxable.
- **Tax-exempt interest:** PA Turnpike interest is 7,500 less box 13 premium of 1,104.30, so 6,395.70 goes on line 2a.
- **Dividends:** ordinary 18,400 and qualified 15,900 (Schwab 2207 + 4410).
- **401(k) lump sum (NUA):** this is a total distribution after separation at age 58 (code 2, so no 10% tax).
  - KMDV shares in kind: gross 640,000. Only the plan cost basis of 96,000 is taxable (line 5b).
  - The **NUA of 544,000 is deferred** until the shares are sold (IRC 402(e)(4)). It will be LTCG at sale.
  - The Schwab "cost basis" must stay at 96,000 ($12/sh). Gregory's note of 640k is wrong. Post-distribution appreciation is short-term or long-term depending on how long he holds after 09/10/2025.
  - The rollover of 780,000 (code G) is shown in gross and is nontaxable.
  - Form 4972 is not available (born after 1936).
- **Capital gains:**
  - Long-term: PG +35,200 and VTI +24,800.
  - Short-term: LLY +5,000.
  - **IVV loss of 18,000 is disallowed as a wash sale (code W).** Ellen bought 420 sh IVV in her traditional IRA on 11/20/2025, 10 days after Gregory sold 400 sh IVV at a loss on 11/10/2025. A related purchase by a spouse/IRA triggers sec. 1091 (Rev. Rul. 2008-5). The disallowed loss is **not** added to IRA basis and is permanently lost. Schwab did not flag it because it tracks wash sales within one account only.
- **Capital loss carryover corrected:**
  - The prior preparer's worksheet carried the full 38,000 as long-term. That is wrong: the 2024 Schedule D had ST (29,000) and LT (12,000), and the 3,000 allowed in 2024 absorbs ST loss first.
  - The correct carryover is **ST 26,000 / LT 12,000** (same 38,000 total).
  - Net result: ST (21,000), LT +48,000, net 27,000 long-term (preferential rates). The prior worksheet would have left 5,000 taxed as ordinary ST gain.
  - 2025 uses up the carryover entirely, so nothing carries to 2026.

## Deductions
- **SALT paid in 2025 totals 30,424.20:**
  - PA withholding 15,534.20
  - local EIT withheld 5,060
  - PA 2024 balance of 410 paid 4/2025
  - real estate taxes 9,830
- **SALT is limited to 10,000.** The OBBBA cap of 40,000 is reduced by 30% of MAGI over 500,000, which takes it below the floor, so the 10,000 floor applies. PA UC withholding is not deductible. The PA/MA extension payments were made in 2026, so they are deductible in 2026.
- **Mortgage interest:** 11,240 (1098; principal of about 318k is under 750k).
- **Charity:** 15,000 cash, written acknowledgments on file, within the 60% limit.
- **Itemized total:** 36,240, which is more than the 31,500 standard deduction.

## Other taxes and payments
- **Form 8959:** Medicare wages 506,000, tax 2,304. Keystone withheld 2,169 of additional Medicare tax, which is credited on line 25c.
- **Form 8960:** NII 54,484.89 (interest, dividends, net gain). The 401(k) distribution is excluded. NIIT 2,070.
- **Excess SS:** none (each spouse had a single employer).
- **Estimated payments:** 4 x 8,000. The 01/15/2026 payment counts for 2025 (handwritten note and organizer).
- **Form 2210:** the required annual payment is the lesser of 90% of 2025 tax (126,067) or 110% of 2024 tax (181,480). Withholding of 105,769 is treated as paid evenly through the year. Adding the ES payments covers each quarterly installment of 31,517, so **there is no penalty**.

## State / local
**Work-day allocation (Outlook export, 04).** I used the original upload. 04b is a duplicate without the notes sheet, and the day data is identical.
- 165 workdays
- PA 112
- NJ 22
- MA 18
- IL 13
- Gregory estimated "20 MA / 15 IL". The counted figures are used.

**PA-40 (resident).** Keystone coded 100% of wages to PA. Estimated PA tax is about 15,500, against withholding 15,534 plus REV-276 1,000, giving a small refund. The figures below are estimates and the PA return needs to be finalized.
- PA compensation is box 16 (441,000 + 65,000). PA taxes 401(k) and 403(b) deferrals.
- Interest is taxable except the PA Turnpike interest, which is exempt.
- Dividends are taxable.
- Net gains are 47,000 or 65,000. **Review:** whether PA follows the IRA wash sale.
- The 401(k) distribution is treated as **not PA-taxable** because it was made on retirement from an eligible plan (open item: confirm that Gregory met the plan's retirement criteria).
- PA has no capital loss carryover, so the federal carryover does not apply.
- Schedule G-L credit for MA and IL tax, limited to PA tax at 3.07% on the same income.

**MA Form 1-NR/PY (nonresident).**
- MA-source wages = 410,000 x 18/165 = 44,727 (above the 8,000 filing threshold). Estimated MA tax is about 2,200, against the M-4868 payment of 2,300.
- Severance/PTO is allocated by the same ratio (review). The 401(k) distribution is not MA-source (4 USC 114).
- First MA filing. No 2024 MA travel per client.

**IL-1040 + Schedule NR (nonresident).**
- IL-source wages = 410,000 x 13/165 = 32,303. Estimated tax is 4.95% of that, about 1,599.
- No exemption, because AGI is above 500k.
- **No IL extension payment was made**, so expect late-payment interest/penalty from 04/15/2026.

**NJ: no return.** The PA-NJ Reciprocal Personal Income Tax Agreement makes the compensation of PA residents earned in NJ exempt from NJ tax. NJ-165 should have been filed with the employer, which is now moot.

**Local EIT final return** (Keystone Collections Group, Chester County TCD), for both spouses.
- The W-2s show "W CHESTER BORO EIT" for both spouses, but the residence is in **West Goshen Twp**. The PSD code mismatch is an open item: confirm the resident PSD code and rate, and that the withholding was remitted to the correct jurisdiction.
- Claim the local credit for MA/IL tax in excess of the PA credit. That gives a small local refund (about 770).

## Open items / assumptions
1. Gregory met the 401(k) plan's retirement criteria (PA exclusion).
2. PA treatment of the IVV loss disallowed under federal sec. 1091 via the spouse's IRA purchase.
3. MA sourcing of the 38,500 severance/PTO payout.
4. Local PSD code (West Goshen Twp vs West Chester Boro) and local extension acceptance.
5. Advise the client that the KMDV basis is 96,000. On a future sale, the first 544,000 of gain is LTCG regardless of holding period, and NUA is not NII-exempt.
6. Ellen's IRA: the Form 5498 is informational. No 2025 IRA reporting is needed beyond the wash-sale effect.
