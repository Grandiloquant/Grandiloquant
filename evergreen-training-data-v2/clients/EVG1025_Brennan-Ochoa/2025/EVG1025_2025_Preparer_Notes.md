# EVG1025 - Brennan-Ochoa, Victor & Lena - 2025 Form 1040 - Preparer Notes

*Synthetic client - Project Evergreen (new client 2025). Return status: **signed off; extended return PAPER filed 09/24/2026
(certified mail); FBAR e-filed 09/22/2026.***

## Return summary
| | |
|---|---|
| Filing status | Married filing jointly |
| Wages | $180,000 (Victor) |
| Interest / dividends | $1,850 / $12,000 (1042-S dividends; qualified $12,000) |
| Capital gains (line 7) | $415,000 = boot $300,000 + constructive sale $150,000 + liquidation loss ($35,000) |
| AGI (line 11) | $608,850 (GILTI not included - section 962 election) |
| Deduction | Standard $31,500 (itemized only $25,613 after the SALT cap phase-down to $10,000) |
| Taxable income | $577,350 |
| Tax (line 16) | $89,241 = regular tax $86,955 + section 962 tax $2,286 |
| NIIT | $13,636 |
| Total tax | $102,877 |
| Payments | W-2 $32,000 + 1042-S $3,600 + estimates $40,000 + extension $25,000 = $100,600 |
| **Balance due** | **$2,277** (paid by IRS Direct Pay 09/24/2026; IRS will bill interest from 04/15/2026) |

## What I did and why (plain English)
1. **Ochoa Engineering Ltd. - GILTI and the section 962 election.** Victor owns 100% of an Irish company -> CFC. Its tested income is
   $400,000 after 12.5% Irish tax ($57,143); no QBAI, no subpart F (services performed in Ireland), and 12.5% is
   below the 18.9% high-tax threshold -> GILTI inclusion $400,000. Without an election, an individual is taxed on GILTI at ordinary
   rates with no section 250 deduction and no foreign tax credit for the company's Irish tax. Under the **section 962 election** (made
   every year since 2022) Victor is taxed as if a corporation: (400,000 + 57,143 section 78 gross-up) less the 50% section 250
   deduction = $228,572 x 21% = $48,000, less the 80% deemed-paid credit $45,714 = **$2,286**.
   The tax goes on **line 16** with an attached statement (election statement, pro-forma 1120 / 1118 computations, Forms 8992 and
   8993); the inclusion itself is not added to AGI. *Presentation is stated as an assumption to verify against the current Form 1040
   line 16 instructions.* Election saves $125,391 of 2025 federal income tax (without it, tax on line 16 would be
   $214,632). Trade-off: when the company eventually distributes this PTEP, the distribution is taxable to the extent it exceeds
   the 962 tax paid (IRC 962(d)) - as a qualified dividend if Ireland treaty requirements are met. Kinsale & Murphy's package (received
   06/24/2026 - main reason for the extension) was re-performed, not just copied.
2. **Form 5471 / 8938 / FBAR.** Form 5471 Categories 4 and 5, Forms 8992 and 8993 attached. No Form 926 (no transfers to the CFC in
   2025). Form 8938 required (CFC stock is a specified foreign financial asset - listed as excepted, reported on 5471). The company's
   AIB account: Victor owns more than 50% of the account owner (financial interest) and is a signer -> **FBAR required** and
   Schedule B line 7a **Yes / Ireland**. The prior preparer answered "No" and filed no FBARs for 2022-2024 - flagged to signer
   (delinquent FBAR submission procedures; separate engagement).
3. **Lena - merger boot (IRC 356).** 1,800 GCDL shares (basis $200,000, 2012) were exchanged in an A reorganization for 10,000 Meridian
   shares (FMV $900,000) plus $300,000 cash. Realized gain $1,000,000; recognized = lesser of the boot or the
   realized gain = **$300,000**. Under Clark the boot is tested as a hypothetical redemption of Meridian stock: Lena's
   interest in Meridian is tiny and the hypothetical redemption is a meaningful reduction -> capital gain, not a dividend. Long-term
   (GCDL held since 2012). The exchange agent's 1099-B shows proceeds $300,000 and no basis: reported on 8949 box E with basis $0
   and a statement (not $1.2M proceeds, and not $300,000 less $200,000). Meridian basis = 200,000 - 300,000 + 300,000 = **$200,000
   ($20/share)**, holding period tacks.
4. **VBO Holdings liquidation (IRC 331).** 1099-DIV box 9 shows an $85,000 cash liquidating distribution - not a dividend. Exchange
   treatment against Victor's $120,000 basis -> **($35,000)** long-term capital loss (8949 box F).
5. **Constructive sale (IRC 1259).** On 12/10/2025 Lena sold short 2,000 Meridian shares at $95 while holding 10,000 long shares -
   "short against the box". That is a constructive sale of 2,000 long shares on 12/10/2025. The exception for a short closed within
   30 days after year end does not apply (closed 03/15/2026). Gain 2,000 x ($95 - $20) = **$150,000** long-term in 2025 - no
   1099-B exists for 2025. Those 2,000 shares now have a $95 basis and a new holding period; when the 2026 1099-B reports the
   March close with unknown basis, report basis $190,000 so the gain isn't taxed twice (2026 diary note).
6. **Form 1042-S.** Atlas Clearing still had Lena's 2017 W-8BEN (Madrid) and withheld 30% on $12,000 of dividends. She is a
   U.S. citizen: the dividends are taxable normally (qualified - domestic stock held since 2019) and the $3,600 is credited
   as withholding on line 25c. Per Intuit, a Form 1040 claiming 1042-S withholding cannot be e-filed in ProConnect; firm policy is the
   same in Axcess -> **paper return** with a copy of the 1042-S attached. Lena gave Atlas a W-9 on 03/18/2026.
7. **NIIT.** NII = interest + dividends + net gains = $428,850; MAGI over $250,000 = $358,850 is smaller ->
   NIIT **$13,636**. The 962 inclusion is not NII. No Additional Medicare tax (Medicare wages $196,000 < $250,000 MFJ).
8. **Deduction.** MAGI over $500,000 phases the SALT cap down to the $10,000 floor; itemized would be $25,613
   -> standard deduction $31,500.
9. **Payments / penalties.** 2024 tax $24,072 (AGI > $150,000 -> 110% = $26,479); withholding alone ($35,600) exceeds it ->
   no Form 2210 penalty. Extension payment + estimates covered > 90% of the tax by 04/15/2026, so no late-payment penalty for the
   extension period; IRS will bill interest on the $2,277 balance.

## Open items / client communication
- FBAR 2022-2024 and Schedule B 7a for those years: delinquent FBAR submission procedures - engagement letter to be sent (CONS).
- 2026: Meridian 2,000-share basis $95 (code B adjustment on the 2026 1099-B); 8,000 remaining shares $20 basis.
- 2026 GILTI: section 250 deduction for GILTI changes to 40% (OBBBA) and the deemed-paid credit to 90% - re-run the 962 comparison.

## Hand-off to signer / routing
- [x] Return locked; Accountant's copy saved as *reviewed*
- [x] Federal 1040 - **PAPER** (1042-S withholding); government copy + 1042-S copy + statements; certified mail 09/24/2026 (tracking in WP)
- [x] **FinCEN 114** - BSA E-Filing 09/22/2026 (Victor; financial interest + signature authority)
- [x] No state (TX)
- [x] Signature: wet-signed jurat (paper return) - both spouses
- Billing: international tier $5,800 (+ $600 constructive-sale / reorg research). Prior-year FBAR remediation -> separate CONS project.
