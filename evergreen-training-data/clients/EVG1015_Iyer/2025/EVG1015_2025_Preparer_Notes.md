# EVG1015 - Iyer, Rajesh & Anita - 2025 Form 1040 - Preparer Notes

*Synthetic client - Project Evergreen. Return status: **signed off; extended return e-filed 09/22/2026 (accepted 09/23);
Form 3520 mailed 09/23/2026; FBAR filed 09/22/2026.***

## Return summary
| | |
|---|---|
| Filing status | Married filing jointly (both resident aliens - green card) |
| Wages | $340,000 |
| Interest | $8,527 (Chase $1,642, NRE $4,819, NRO $2,065) |
| AGI (line 11) | $348,527 |
| Deduction | Standard $31,500 |
| Taxable income | $317,027 |
| Tax (line 16) | $61,780 |
| Credits | CTC $2,200 (Vikram) + foreign tax credit $310 |
| Other taxes | Additional Medicare + NIIT $1,557 (NIIT $324) |
| Total tax | $60,827 |
| Withholding (incl. 8959 line 24) | $62,622 |
| **Refund** | **$1,795** |

## What I did and why (plain English)
1. **Residency.** Both have green cards (since 2022) -> US residents taxed on worldwide income. No treaty tie-breaker
   position (home, jobs, child all in the US).
2. **Indian interest - calendar year, not Indian FY.** Indian certificates run April-March. I took Jan-Mar 2025 from the
   FY 2024-25 certificates and Apr-Dec 2025 from the FY 2025-26 certificates (received 08/11/2026 - main reason for the
   extension). Calendar 2025: NRE INR 420,000; NRO INR 180,000; TDS INR 56,160. Converted at the
   IRS 2025 yearly average rate **87.147 INR/USD**: NRE $4,819, NRO $2,065.
3. **NRE interest is taxable in the US.** It is exempt in India (s.10(4)(ii)), but that has no effect on US tax. It was left off
   the 2024 (and earlier) self-prepared returns - flagged to signer below.
4. **Foreign tax credit (Form 1116, passive).** SBI withheld TDS at 31.2% because no Form 10F/TRC was given. Under the US-India
   treaty (Art. 11(2)) India may tax interest paid to a US resident at no more than 15%. Tax paid above the treaty rate is not a
   compulsory payment (Reg. 1.901-2(e)(5)) and is not creditable - it should be reclaimed from India. Creditable tax =
   15% x INR 180,000 = INR 27,000 = **$310**; excess INR 29,160 ($335)
   is a refund claim in India. *Translation note:* TDS was withheld quarterly; I used the yearly average rate as a reasonable
   approximation of the payment-date rates (difference is a few dollars). **Form 1116 is required** even though the credit
   is under $600: the de minimis election needs all foreign income to be reported on a qualified payee statement
   (1099/K-1), which Indian certificates are not. (The procedure's "$600 MFJ - skip the 1116" shortcut is imprecise; the
   law was followed.) Limitation $1,220 >> credit, so the full $310 is allowed.
5. **Gift from Anita's father (Form 3520 Part IV).** INR 1.3 crore wired 06/18/2025 - Chase credited **$150,812.53** (the
   actual USD received is the value). A gift is not income, but gifts over $100,000 from a nonresident alien individual must
   be reported on Form 3520 Part IV. Filed jointly (joint 1040 filers), due with the extended return 10/15/2026, **mailed
   separately to IRS Ogden** by certified mail on 09/23/2026 (it cannot be e-filed with the 1040). The money sits in a US
   account, so it is not a foreign account.
6. **FBAR.** Aggregate balances far exceed $10,000. Reported all **7** accounts - the 4 bank accounts from the 2024 FBAR plus the
   3 mutual fund folios (mutual fund accounts are "other financial accounts" - the 2024 FBAR missed them). Maximum values
   converted at the Treasury Reporting Rate for 12/31/2025, **assumed INR 89.87/USD** (verify against the published
   Treasury table; the FBAR rule is the 12/31 Treasury rate, not the IRS average). Aggregate max $202,648. All
   accounts are joint, so Rajesh filed one FBAR with Anita's Form 114a. Due 04/15 with automatic extension to 10/15/2026.
7. **Form 8938.** MFJ living in the US: threshold $100,000 at year end / $150,000 at any time. Year-end value $194,843
   -> required. The FBAR does not satisfy 8938. Mutual funds count toward the threshold but are listed as excepted assets
   (3 Forms 8621).
8. **PFICs (Form 8621 x 3).** Indian mutual funds are foreign corporations with passive income -> PFICs. Growth option, no
   distributions, no redemptions in 2025 -> no excess distribution and no tax, but aggregate PFIC value $72,327
   exceeds the $50,000 MFJ exemption, so an annual Part I filing is required for each fund (section 1291 funds). When they
   redeem, gains are taxed under the excess-distribution regime (top rate + interest charge back to 2019-2022 when their
   holding periods as US persons began). **Recommend a planning call on the section 1296 mark-to-market election** (funds have
   a published daily NAV and are redeemable - treated as marketable) vs. an orderly exit; QEF is not practical (Indian AMCs do
   not issue PFIC Annual Information Statements).
9. **Parents are not dependents.** Organizer listed them and Rajesh asked about ITINs. A dependent must be a US citizen/national
   or a resident of the US, Canada or Mexico. They are Indian residents; I-94 shows 177 days in the US (04/05-09/28) with no
   2023/2024 presence -> substantial presence test not met -> nonresident aliens. No ODC, no ITIN applications.
10. **Additional Medicare / NIIT.** Neither W-2 alone passes $200,000 for full withholding; combined Medicare wages $387,000
    exceed the $250,000 MFJ threshold -> Form 8959 tax $1,233 less Cascadia's $122 withheld
    (line 25c). MAGI $348,527 > $250,000 -> NIIT 3.8% on all interest (foreign interest included) = $324.
    The FTC cannot offset NIIT.
11. **CTC.** Vikram (6) -> $2,200; AGI below $400,000, no phase-out. No child care expenses claimed.
12. **Washington.** No individual income tax; no capital gains excise (no sales). WA PFML / WA Cares in box 14 are not deductible.

## Open items / client communication
- **Prior years (signer decision - CONS project opened):** 2023-2024 returns omitted NRE interest (~$4,500/yr), over-claimed FTC,
  and omitted Forms 8938/8621; 2024 FBAR omitted MF folios. Options: amend 2022-2024 + late 8938/8621/FBAR with reasonable-cause
  statements, or Streamlined Domestic Offshore Procedures (5% miscellaneous offshore penalty). Engagement letter for the
  remediation to be sent separately; not included in this bill.
- Client to file an Indian ITR for FY 2025-26 claiming refund of excess TDS, and give SBI Form 10F + US Form 6166 (TRC) so
  2026 TDS is withheld at 15%. If India refunds the excess later, no US adjustment needed (it was never credited).
- PFIC MTM election discussion scheduled (must be made on a timely filed 2026 return if elected).

## Hand-off to signer / routing
- [x] Return locked; Accountant's copy saved as *reviewed*
- [x] Federal 1040 (with 1116, 8938, 8621 x 3) - e-file; due 10/15/2026 (extended) - accepted 09/23/2026
- [x] **Form 3520** - paper, mailed separately to IRS Ogden 09/23/2026, certified mail (tracking in WP); due 10/15/2026
- [x] **FinCEN 114 (FBAR)** - BSA E-Filing 09/22/2026 with Form 114a; due 10/15/2026 (automatic extension)
- [x] No state return (WA)
- [x] eSign 8879 - Rajesh by email
- Billing: international tier $3,400 (1040, 1116, 8938, 8621 x 3, 3520, FBAR). Prior-year remediation -> separate CONS
  project / MISC, time left in WIP.
