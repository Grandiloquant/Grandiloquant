"""EVG1011 Nguyen - software exceptions (CCH Axcess workbook tab 19 + log items; ProConnect equivalents).
Amounts tie to the EVG1011 answer key (1099-DA proceeds 370,811; staking 2,100.44 on Sch 1 line 8v; NFT 28% gain 8,976;
line 7 202,540)."""
from software_exceptions import exc

CLIENT_ID, DISPLAY = "EVG1011", "Thomas Nguyen"
PREPARER, REVIEWER = "P. Anand (staff)", "L. Chen (senior)"
INTRO = """
Thomas's return is a crypto-investor return in the first year brokers issue Form 1099-DA (gross proceeds only, no basis).
Neither package has a blockchain data feed: both calculate exactly what is imported. The three digital-asset items below
are all silent - no diagnostic fires when a 1099-DA and a full CoinLedger 8949 are both loaded, when a 1099-MISC staking
amount is also inside the CoinLedger income total, or when an NFT collectible comes in without a collectible code. The
fourth item (IP PIN) is an e-file reject the software cannot predict.
"""

ITEMS = [
    exc("EVG1011-SX1", "19", "Capital Loss", "Coinbase 1099-DA and the CoinLedger Form 8949 both loaded - proceeds counted twice",
        axcess_default="Autoflow/1099 import brings in the Coinbase 1099-DA as 7 sales with gross proceeds $370,811 and BLANK basis "
                       "(basis is not reported for 2025), and the CoinLedger 8949 import brings in the same Coinbase sales again with full "
                       "basis. Axcess treats the 1099-DA rows as $0-basis sales, so line 7 rises by ~$370,811. A blank basis on a "
                       "'basis not reported' row is a valid entry, so nothing is flagged. A generic CSV import also puts every row in "
                       "box C/F (no 1099) unless the box is mapped.",
        axcess_diagnostic="None - silent",
        manual_calc="Yes",
        axcess_fix="Gains and Losses > Capital Gains and Losses: delete the 1099-DA import; keep the CoinLedger FINAL (09/26/2026) detail only. "
                   "Map Coinbase rows to Form 8949 box H (ST) / box K (LT) - '1099-DA received, basis not reported'; MetaMask rows to box I / L "
                   "(no 1099-DA); Robinhood to A / D. Report Coinbase proceeds net of fees so they tie to the 1099-DA: CoinLedger $372,300 - "
                   "fees $1,489 = $370,811 (same gain - CoinLedger had the fees in basis). Reconciliation attached in the workpapers.",
        amount=370811,
        proconnect_default="Same - ProConnect computes Schedule D from whatever 8949 rows are entered or imported; a 1099-DA entered "
                           "manually or imported alongside the CoinLedger detail is a second set of sales with $0 basis.",
        proconnect_fix="Dispositions (Schedule D/4797/etc.): import or key the CoinLedger detail only, with the 8949 box set per row (H/K, I/L, "
                       "A/D). Alternative for many lots: enter summary totals by 8949 box and attach the CoinLedger detail as a PDF "
                       "(General > e-file PDF/Miscellaneous > Attach PDF, linked to Sch D/Form 8949 'Form 8949 Exception Reporting Statement') so Form 8453 is not "
                       "required - diagnostic ref 10322 clears once the PDF is attached.",
        proconnect_ref="Intuit help: 'Attaching a summary statement to Schedule D/Form 8949 in ProConnect Tax and resolving Diagnostic ref. 10322'",
        efile_impact="None if detail is entered; summary method requires the PDF attachment (or Form 8453)",
        affected_lines=["7", "Form 8949 boxes H/I/K/L", "Schedule D"],
        procedure_section="Schedule D - CoinLedger-provided Forms 8949 vs Consolidated 1099 / 1099-DA",
        notes="Self-transfers (Coinbase 'Send' 2.0 ETH 08/23 and 1.5 ETH 11/02 to his own MetaMask) are not dispositions; the 2.0 ETH "
              "swapped on Uniswap keeps its 04/22/2025 basis $3,574."),
    exc("EVG1011-SX2", "19", "Other", "Kraken 1099-MISC staking is already inside the CoinLedger income total",
        axcess_default="The Kraken 1099-MISC box 3 ($1,240.00) entered on the 1099-MISC worksheet flows to Schedule 1 'other income'; "
                       "the CoinLedger income report total ($2,100.44, which already includes the Kraken rewards) keyed as digital-asset "
                       "income adds it again -> $3,340.44. Axcess has no way to know one is a subset of the other.",
        axcess_diagnostic="None - silent",
        manual_calc="Yes",
        axcess_fix="Income > Other income: enter $2,100 once as digital assets received as ordinary income (Schedule 1 line 8v). Keep the "
                   "1099-MISC on file for matching but do not let it flow (or enter it as the 8v item and add only the $860.44 on-chain "
                   "balance). Not SE income (investor). Included in NII on Form 8960.",
        amount=2100,
        proconnect_default="Same - a 1099-MISC box 3 entry and a separate other-income entry both flow to Schedule 1.",
        proconnect_fix="Income > Other income: one Schedule 1 line 8v entry $2,100 (digital assets received as ordinary income); do not also "
                       "enter the Kraken 1099-MISC box 3 as other income (screen/field per current release - verify).",
        efile_impact="None",
        affected_lines=["8 (Schedule 1 line 8v)", "Form 8960"],
        procedure_section="Sch 1 line 8v - staking income",
        notes="Rev. Rul. 2023-14: staking rewards are income at FMV when the taxpayer gains dominion and control."),
    exc("EVG1011-SX3", "19", "Capital Loss", "NFT digital art imported without the collectible code - 28% gain taxed at 15%",
        axcess_default="The CoinLedger 8949 row for 'Chromatic Drift #214' imports as an ordinary long-term sale. Axcess applies 0/15/20% "
                       "rates to all long-term gain; it cannot tell an NFT that references a work of art is a collectible. Schedule D "
                       "line 18 (28% rate gain) stays $0.",
        axcess_diagnostic="None - silent",
        manual_calc="No",
        axcess_fix="Gains and Losses > Capital Gains and Losses, MetaMask NFT row (box L): adjustment code C (collectible) - gain $8,976 "
                   "flows to the 28% Rate Gain Worksheet / Schedule D line 18 (verify field name in current release).",
        amount=8976,
        proconnect_default="Same - collectible treatment requires the collectible indicator / code C on the disposition.",
        proconnect_fix="Dispositions: on the NFT row set the collectible indicator (28% rate gain) / 8949 code C; confirm Schedule D line 18 "
                       "= 8,976 (field per current release - verify).",
        efile_impact="None",
        affected_lines=["16", "Schedule D line 18"],
        procedure_section="Schedule D - adjustment codes (C collectibles, W wash sale)",
        notes="Notice 2023-27 look-through: an NFT whose associated right/asset is a work of art is a collectible. Also on this tab: the "
              "04/07 BTC loss ($14,866) stays allowed - section 1091 covers stock/securities, not digital assets, for 2025; the Robinhood "
              "TSLA code W ($3,960) is kept as the broker reported it."),
    exc("EVG1011-SX4", "2", "E-file Disqualifying", "Stale IP PIN from the January 2025 CP01A",
        axcess_default="Axcess transmits whatever 6-digit IP PIN is on the e-file input; it validates the format only. The CP01A in the "
                       "PBC was for the 2024 return - using it causes an IRS reject (IP PIN mismatch).",
        axcess_diagnostic="None - silent",
        manual_calc="No",
        axcess_fix="General > Electronic Filing: enter the 2026 IP PIN retrieved by the client from his IRS Online Account on 09/28/2026 "
                   "(taken by phone, not email). Prepare Form 8822 (paper) for the new address.",
        amount=None,
        proconnect_default="Same - the IP PIN field is not validated against IRS records before transmission.",
        proconnect_fix="General > Electronic Filing: Identity Protection PIN field = current 2026 IP PIN (screen/field per current release - verify).",
        efile_impact="Reject if stale PIN used; retransmit before 10/15/2026",
        affected_lines=[],
        procedure_section="E-File Rejects - IP PIN changes every year",
        notes="Nothing fires before transmission; the IRS rejects after transmission (IP PIN mismatch - IND-181/IND-183 family)."),
]

TABS = {
    "19": [
        {"A": "Kraken (exchange)", "B": "Stake", "C": 1, "D": 1240.00, "F": "Ordinary (Sch 1 line 8v)",
         "G": "1099-MISC box 3 total - one line for all 2025 reward events at FMV when credited. SUBSET of the CoinLedger income "
              "report - do not add again."},
        {"A": "MetaMask - on-chain ETH staking", "B": "Stake", "C": 1, "D": 860.44, "F": "Ordinary (Sch 1 line 8v)",
         "G": "CoinLedger income report; no information return. Kraken 1,240.00 + on-chain 860.44 = 2,100.44 -> line 8v $2,100."},
        {"A": "MetaMask - Uniswap swap 2.0 ETH -> 8,900 USDC (08/24/2025)", "B": "Disposal", "C": 2, "D": 4443.00,
         "F": "Capital - ST (8949 box I)",
         "G": "Basis 3,574 = Coinbase lot acquired 04/22/2025 (Send 08/23 to own wallet is not a sale). Gain 5,312."},
        {"A": "MetaMask - NFT 'Chromatic Drift #214' (sold 11/12/2025 for 3.9 ETH)", "B": "Disposal", "C": 1, "D": 11969.00,
         "F": "Capital - LT collectible 28% (8949 box L, code C)", "G": "Basis 2,992 (acq 02/05/2023). Gain 8,976 -> Sch D line 18."},
        {"A": "Coinbase - 0.5 BTC sold 04/07/2025", "B": "Disposal", "C": 0.5, "D": 76692.00, "F": "Capital - ST (8949 box H)",
         "G": "Basis 53,212 -> loss (14,866) ALLOWED: no wash-sale rule for digital assets in 2025 (repurchased 0.5 BTC 04/18)."},
        {"A": "Coinbase - all 2025 sales per 1099-DA (7 rows)", "B": "Disposal (summary)", "C": 1, "D": 370811.00,
         "F": "Capital - 8949 boxes H/K",
         "G": "1099-DA gross proceeds net of fees. Reported ONCE from CoinLedger detail (CoinLedger 372,300 - fees 1,489). Do NOT "
              "import the 1099-DA separately (would add ~370,811 of $0-basis gain)."},
    ],
}

CHECKS = {
    "'19. Crypto Income & Basis'!E13": 1240,
    "'19. Crypto Income & Basis'!E14": 860.44,
    "'19. Crypto Income & Basis'!E15": 8886,
    "'19. Crypto Income & Basis'!E16": 11969,
    "'19. Crypto Income & Basis'!E17": 38346,
    "'19. Crypto Income & Basis'!E18": 370811,
}
