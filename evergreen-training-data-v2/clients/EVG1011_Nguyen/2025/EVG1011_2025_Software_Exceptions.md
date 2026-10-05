# EVG1011 - Thomas Nguyen - 2025 Software Exceptions (CCH Axcess & Intuit ProConnect)

*Synthetic training data - Project Evergreen v2. Companion workbook: `EVG1011_2025_Software_Exception_Workbook.xlsx` (firm's corrected CCH Axcess Exception Workbook, filled in).*

Thomas's return is a crypto-investor return in the first year brokers issue Form 1099-DA (gross proceeds only, no basis).
Neither package has a blockchain data feed: both calculate exactly what is imported. The three digital-asset items below
are all silent - no diagnostic fires when a 1099-DA and a full CoinLedger 8949 are both loaded, when a 1099-MISC staking
amount is also inside the CoinLedger income total, or when an NFT collectible comes in without a collectible code. The
fourth item (IP PIN) is an e-file reject the software cannot predict.

| ID | Workbook tab | Exception | Axcess diagnostic? | Override amount | E-file impact |
|---|---|---|---|---:|---|
| EVG1011-SX1 | 19. Crypto Income & Basis | Coinbase 1099-DA and the CoinLedger Form 8949 both loaded - proceeds counted twice | **silent** (no diagnostic) | 370,811 | None if detail is entered; summary method requires the PDF attachment (or Form 8453) |
| EVG1011-SX2 | 19. Crypto Income & Basis | Kraken 1099-MISC staking is already inside the CoinLedger income total | **silent** (no diagnostic) | 2,100 | None |
| EVG1011-SX3 | 19. Crypto Income & Basis | NFT digital art imported without the collectible code - 28% gain taxed at 15% | **silent** (no diagnostic) | 8,976 | None |
| EVG1011-SX4 | 2. Diagnostics Log | Stale IP PIN from the January 2025 CP01A | **silent** (no diagnostic) |  | Reject if stale PIN used; retransmit before 10/15/2026 |

## EVG1011-SX1 - Coinbase 1099-DA and the CoinLedger Form 8949 both loaded - proceeds counted twice

*Workbook tab:* 19. Crypto Income & Basis  |  *Category:* Capital Loss  |  *Manual calc:* Yes  |  *Amount:* $370,811  |  *Procedure doc:* Schedule D - CoinLedger-provided Forms 8949 vs Consolidated 1099 / 1099-DA

- **CCH Axcess by default:** Autoflow/1099 import brings in the Coinbase 1099-DA as 7 sales with gross proceeds $370,811 and BLANK basis (basis is not reported for 2025), and the CoinLedger 8949 import brings in the same Coinbase sales again with full basis. Axcess treats the 1099-DA rows as $0-basis sales, so line 7 rises by ~$370,811. A blank basis on a 'basis not reported' row is a valid entry, so nothing is flagged. A generic CSV import also puts every row in box C/F (no 1099) unless the box is mapped.
- **Axcess diagnostic:** None - silent
- **Axcess fix:** Gains and Losses > Capital Gains and Losses: delete the 1099-DA import; keep the CoinLedger FINAL (09/26/2026) detail only. Map Coinbase rows to Form 8949 box H (ST) / box K (LT) - '1099-DA received, basis not reported'; MetaMask rows to box I / L (no 1099-DA); Robinhood to A / D. Report Coinbase proceeds net of fees so they tie to the 1099-DA: CoinLedger $372,300 - fees $1,489 = $370,811 (same gain - CoinLedger had the fees in basis). Reconciliation attached in the workpapers.
- **ProConnect by default:** Same - ProConnect computes Schedule D from whatever 8949 rows are entered or imported; a 1099-DA entered manually or imported alongside the CoinLedger detail is a second set of sales with $0 basis.
- **ProConnect fix:** Dispositions (Schedule D/4797/etc.): import or key the CoinLedger detail only, with the 8949 box set per row (H/K, I/L, A/D). Alternative for many lots: enter summary totals by 8949 box and attach the CoinLedger detail as a PDF (General > e-file PDF/Miscellaneous > Attach PDF, linked to Sch D/Form 8949 'Form 8949 Exception Reporting Statement') so Form 8453 is not required - diagnostic ref 10322 clears once the PDF is attached. *(ref: Intuit help: 'Attaching a summary statement to Schedule D/Form 8949 in ProConnect Tax and resolving Diagnostic ref. 10322')*
- **E-file impact:** None if detail is entered; summary method requires the PDF attachment (or Form 8453)
- **Return lines affected:** 7, Form 8949 boxes H/I/K/L, Schedule D
- **Notes:** Self-transfers (Coinbase 'Send' 2.0 ETH 08/23 and 1.5 ETH 11/02 to his own MetaMask) are not dispositions; the 2.0 ETH swapped on Uniswap keeps its 04/22/2025 basis $3,574.

## EVG1011-SX2 - Kraken 1099-MISC staking is already inside the CoinLedger income total

*Workbook tab:* 19. Crypto Income & Basis  |  *Category:* Other  |  *Manual calc:* Yes  |  *Amount:* $2,100  |  *Procedure doc:* Sch 1 line 8v - staking income

- **CCH Axcess by default:** The Kraken 1099-MISC box 3 ($1,240.00) entered on the 1099-MISC worksheet flows to Schedule 1 'other income'; the CoinLedger income report total ($2,100.44, which already includes the Kraken rewards) keyed as digital-asset income adds it again -> $3,340.44. Axcess has no way to know one is a subset of the other.
- **Axcess diagnostic:** None - silent
- **Axcess fix:** Income > Other income: enter $2,100 once as digital assets received as ordinary income (Schedule 1 line 8v). Keep the 1099-MISC on file for matching but do not let it flow (or enter it as the 8v item and add only the $860.44 on-chain balance). Not SE income (investor). Included in NII on Form 8960.
- **ProConnect by default:** Same - a 1099-MISC box 3 entry and a separate other-income entry both flow to Schedule 1.
- **ProConnect fix:** Income > Other income: one Schedule 1 line 8v entry $2,100 (digital assets received as ordinary income); do not also enter the Kraken 1099-MISC box 3 as other income (screen/field per current release - verify).
- **E-file impact:** None
- **Return lines affected:** 8 (Schedule 1 line 8v), Form 8960
- **Notes:** Rev. Rul. 2023-14: staking rewards are income at FMV when the taxpayer gains dominion and control.

## EVG1011-SX3 - NFT digital art imported without the collectible code - 28% gain taxed at 15%

*Workbook tab:* 19. Crypto Income & Basis  |  *Category:* Capital Loss  |  *Manual calc:* No  |  *Amount:* $8,976  |  *Procedure doc:* Schedule D - adjustment codes (C collectibles, W wash sale)

- **CCH Axcess by default:** The CoinLedger 8949 row for 'Chromatic Drift #214' imports as an ordinary long-term sale. Axcess applies 0/15/20% rates to all long-term gain; it cannot tell an NFT that references a work of art is a collectible. Schedule D line 18 (28% rate gain) stays $0.
- **Axcess diagnostic:** None - silent
- **Axcess fix:** Gains and Losses > Capital Gains and Losses, MetaMask NFT row (box L): adjustment code C (collectible) - gain $8,976 flows to the 28% Rate Gain Worksheet / Schedule D line 18 (verify field name in current release).
- **ProConnect by default:** Same - collectible treatment requires the collectible indicator / code C on the disposition.
- **ProConnect fix:** Dispositions: on the NFT row set the collectible indicator (28% rate gain) / 8949 code C; confirm Schedule D line 18 = 8,976 (field per current release - verify).
- **E-file impact:** None
- **Return lines affected:** 16, Schedule D line 18
- **Notes:** Notice 2023-27 look-through: an NFT whose associated right/asset is a work of art is a collectible. Also on this tab: the 04/07 BTC loss ($14,866) stays allowed - section 1091 covers stock/securities, not digital assets, for 2025; the Robinhood TSLA code W ($3,960) is kept as the broker reported it.

## EVG1011-SX4 - Stale IP PIN from the January 2025 CP01A

*Workbook tab:* 2. Diagnostics Log  |  *Category:* E-file Disqualifying  |  *Manual calc:* No  |  *Amount:* -  |  *Procedure doc:* E-File Rejects - IP PIN changes every year

- **CCH Axcess by default:** Axcess transmits whatever 6-digit IP PIN is on the e-file input; it validates the format only. The CP01A in the PBC was for the 2024 return - using it causes an IRS reject (IP PIN mismatch).
- **Axcess diagnostic:** None - silent
- **Axcess fix:** General > Electronic Filing: enter the 2026 IP PIN retrieved by the client from his IRS Online Account on 09/28/2026 (taken by phone, not email). Prepare Form 8822 (paper) for the new address.
- **ProConnect by default:** Same - the IP PIN field is not validated against IRS records before transmission.
- **ProConnect fix:** General > Electronic Filing: Identity Protection PIN field = current 2026 IP PIN (screen/field per current release - verify).
- **E-file impact:** Reject if stale PIN used; retransmit before 10/15/2026
- **Notes:** Nothing fires before transmission; the IRS rejects after transmission (IP PIN mismatch - IND-181/IND-183 family).

