# EVG1011 - Nguyen, Thomas - 2025 Form 1040 - Preparer Notes

*Synthetic client - Project Evergreen. Return status: **signed off 09/28/2026; transmitted 09/29/2026 (acknowledgment pending).***

## Return summary
| | |
|---|---|
| Filing status | Single |
| Wages / interest / staking | $21,400 / $1,850 / $2,100 (Sch 1 line 8v) |
| Capital gains (line 7) | $202,540 = ST $30,066 + LT $172,474 (incl. 28% collectible NFT gain $8,976) |
| AGI (line 11) | $227,890 |
| Standard deduction | $15,750 |
| Taxable income | $212,140 |
| Tax (line 16) | $30,142 |
| Excess APTC repayment (Sch 2 line 2) | $3,528 |
| NIIT (Sch 2 line 12) | $1,060 |
| Total tax (line 24) | $34,730 |
| Payments | withholding $2,568 + estimates $22,000 + extension $12,000 |
| **Refund** | **$1,838** |

## What I did and why (plain English)
1. **Investor, not trader.** Thomas made ~12 disposals across the year and held most positions for months or years; no business
   activity -> investor. Everything goes on Form 8949 / Schedule D; no Schedule C, no 475(f) mark-to-market. His CoinLedger subscription
   and hardware wallet are investment expenses (miscellaneous itemized deductions) - not deductible.
2. **Which crypto source to use.** The Coinbase 1099-DA reports gross proceeds only (no basis in 2025). The final CoinLedger report
   covers Coinbase, Kraken and his MetaMask wallet with full basis. I used **only the CoinLedger detail** and did not load the 1099-DA
   (loading both would count $370,811 of Coinbase proceeds twice, the second time with $0 basis). Reconciliation: CoinLedger's
   Coinbase proceeds $372,300 are before sale fees and it puts the $1,489 of fees in cost basis; the 1099-DA
   reports proceeds net of fees. Same gain either way; I reported the 1099-DA proceeds figures so the IRS match ties.
   - Coinbase sales -> 8949 **box H** (short-term) / **box K** (long-term): "reported on Form 1099-DA, basis not reported".
   - MetaMask disposals (Uniswap swap, NFT sale) -> **box I / box L**: no 1099-DA.
   - Robinhood stock sales -> box A / box D (covered, basis reported).
3. **Self-transfers.** Coinbase shows "Send" 2.0 ETH (08/23) and 1.5 ETH (11/02) to 0x7c3a...91be - that is his own MetaMask wallet
   (per his note and the CoinLedger wallet list). Not sales. The 2.0 ETH swapped for USDC on 08/24 keeps its 04/22/2025 Coinbase
   basis ($3,574).
4. **BTC loss and "wash sale".** He sold 0.5 BTC at a $14,866 loss on 04/07 and rebought 0.5 BTC on 04/18. The wash-sale rule
   (sec. 1091) covers stock and securities; crypto is property, not a security, for 2025 -> **loss allowed**. His Robinhood TSLA sale on
   03/10 IS a wash sale (replacement bought 03/24): Robinhood disallowed $3,960 (box 1g) and added it to the replacement shares'
   basis - reported with code W as the broker did.
5. **NFT = collectible.** The NFT is digital art; under Notice 2023-27's look-through approach an NFT whose associated asset is a
   work of art is a collectible. Held > 1 year -> 28%-rate gain $8,976 (8949 code C, Schedule D line 18).
6. **Staking.** Kraken 1099-MISC box 3 $1,240.00 is part of CoinLedger's income report ($1,240.00 Kraken + $860.44 on-chain =
   $2,100). Reported once on Schedule 1 line 8v at FMV when received (Rev. Rul. 2023-14). Not self-employment income.
7. **NIIT.** Net investment income $206,490 (interest, staking, net gains) but MAGI exceeds $200,000 by only $27,890
   -> 3.8% x $27,890 = $1,060.
8. **Premium tax credit (Form 8962).** Marketplace plan Apr-Dec with APTC $3,528 based on the $36,000 income he projected
   when he quit. Actual household income $227,890 = 1,513% of the 2024 FPL ($15,060). 2025 still has the enhanced PTC
   (no 400% cliff), but at 8.5% his monthly contribution ($1,614) exceeds the benchmark plan ($441) -> PTC $0 each month.
   Above 400% FPL there is no repayment cap -> repay all $3,528 (Schedule 2 line 2).
9. **IP PIN.** He is in the IP PIN program. The CP01A he scanned is dated 01/06/2025 - that PIN was for the 2024 return. The 2026 letter
   was mailed to his old address. He retrieved the current PIN from his IRS Online Account on 09/28 (phone, not email). Entered on the
   e-file screen. Using the stale PIN would reject the return. Form 8822 prepared for his new address.
10. **Estimated tax / extension.** Estimates $22,000 (4 x $5,500, timely) + extension payment $12,000 (04/14/2026). Form 2210:
    2024 AGI $104,955 (< $150,000) -> safe harbor is 100% of 2024 tax $14,212; timely withholding + estimates exceed $3,553 per quarter
    -> no penalty. Refund results; no late-payment penalty or interest since the full tax was paid by 04/15/2026.
11. **Tennessee.** No individual income tax (Hall tax on interest/dividends repealed from 2021) - no state return.

## Open items / client communication
- Acknowledgment for the 09/29/2026 transmission pending - monitor; if rejected, follow E-File Rejects procedure (document reason,
  save updated return, retransmit before 10/15/2026).
- Form 8822 mailed with his signature. Remind him: new IP PIN each January (Online Account).
- 2026: brokers start reporting crypto cost basis on 1099-DA for covered assets - keep CoinLedger connected to all wallets.

## Hand-off to signer / routing
- [x] Return locked; Accountant's copy saved as *reviewed*
- [x] Federal 1040 - e-file with current IP PIN; no state; no FBAR (no foreign accounts - Kraken/Coinbase are US entities)
- [x] Extended due date 10/15/2026 populated
- [x] eSign (Form 8879) - client prefers text/email; 24-hour ELF hold observed before transmission
- [x] Form 8822 (paper) - special processing instruction for Admin
- Billing: crypto tier $1,600 + 4.0 hrs reconciliation (1099-DA / CoinLedger / Robinhood) = $2,340; **15% expedite fee** (final
  CoinLedger report received 09/26/2026, within 15 days of 10/15) = $351; total $2,691. Time spent
  chasing the missing MetaMask import is client-chargeable (external reason).
