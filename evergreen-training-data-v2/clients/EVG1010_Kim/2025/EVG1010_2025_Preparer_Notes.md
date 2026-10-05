# EVG1010 - Kim, Daniel & Grace - 2025 Form 1040 - Preparer Notes

*Synthetic client - Project Evergreen. Return status: **signed off, e-filed 04/13/2026, accepted.***

## Return summary
| | |
|---|---|
| Filing status | Married filing jointly |
| AGI (line 11) | $448,778 |
| Deduction | Itemized $46,459 (standard would be $31,500) |
| Taxable income (line 15) | $402,319 - **exported to EVG1021 (Ethan) Form 8615 line 6** |
| Tax (line 16) | $80,885 (includes Form 8814 tax on Chloe's interest $55) |
| Child tax credit | $1,950 (2 x $2,200 less phase-out $2,450) |
| Other taxes (line 23) | $6,965 = Schedule H $4,326 + Form 8959 $1,920 + NIIT $719 |
| Total tax (line 24) | $85,900 |
| Payments | W-2 withholding $86,280 + Additional Medicare withheld $1,200 |
| **Refund** | **$1,580** |

## What I did and why (plain English)
1. **Wages.** Daniel $309,850 (includes RSU vest income $86,400 shown in box 14) and Grace $120,000. Box 12 C (group-term
   life over $50k) is already in box 1; D and DD need no entry. WA PFML in box 14 is informational (see #8).
2. **RSU stock sales (Form 8949).** Summit Shareworks reported 6 sales with **$0 basis** and "basis not reported to IRS". The supplemental
   statement gives the FMV at release, which was already taxed as wages. I reported each sale in box B (short-term: the four sell-to-cover
   sales and the 12/05 sale) or box E (long-term: 150 shares from the 03/15/2023 release), entered the 1099-B basis $0, code **B**, and a
   negative column (g) adjustment equal to the FMV basis. Net result: ST $788, LT $8,670 instead of
   $69,338 of phantom gain. Joint Rainier account: interest $1,452, dividends $6,811 (qualified $5,904),
   capital gain distributions $1,207 (Sch D line 13). Schedule D line 16 $10,665.
3. **Nanny = household employee (Schedule H).** The organizer said "no household employees" and the clients sent Maria a 1099-NEC,
   but the facts (their home, their schedule and duties, their car, weekly pay, no other clients) make her a common-law employee.
   Nannies are the classic household employee (Pub. 926). 2025 cash wages $28,000 >= $2,800, so:
   - Social security 12.4% + Medicare 2.9% on $28,000 = $4,284. The Kims did not withhold Maria's share, and chose to pay it
     rather than recover it from her; the $2,142 employee share they pay is extra **wages for income tax only** (W-2 box 1
     $30,142.00; boxes 3/5 stay $28,000).
   - FUTA: wages of $1,000+ in a quarter -> 0.6% x $7,000 = $42. The 0.6% net rate assumes full state credit, which
     requires the WA ESD contributions to be paid by 04/15/2026 - Grace paid them 04/06/2026 (Schedule H line 14 "Yes").
   - Schedule H total $4,326 -> Schedule 2 line 9. Paid with the return (no penalty - see #9).
   - Admin items done outside the 1040: EIN obtained 03/03/2026; W-2/W-3 filed 03/10/2026 (after the 02/02/2026 due date - possible
     late-filing penalty; we will request first-time/reasonable-cause relief if a notice arrives); corrected $0 1099-NEC filed; WA ESD
     registration 03/12/2026. WA L&I and WA PFML/WA Cares obligations for household employers referred to a payroll provider (not a 1040 item).
   - **2024:** Maria was paid $6,240 in Sept-Dec 2024, over the 2024 $2,700 threshold - a 2024 Schedule H (1040-X) is needed.
     Opened as a separate MISC project (in WIP, billed separately).
4. **Form 2441.** Chloe (12) is the only qualifying person - Ethan is 16. Grace's $5,000 dependent-care FSA (W-2 box 10) is excluded;
   with one qualifying person the credit base is $3,000 less the $5,000 exclusion = **$0 credit**. Form 2441 is still filed (provider:
   Maria Lopez, SSN on file) to support the exclusion - taxable benefits $0.
5. **Kids' investment income (Kid Taxes procedure).**
   - **Ethan (16):** UTMA interest $900 + dividends $2,400 (qualified $1,900) + a $3,100 long-term gain from selling part of his index fund,
     plus a $3,200 summer W-2. Grace asked for Form 8814 again, but 8814 only works when the child's income is only interest and dividends -
     the fund **sale** (and the wages) disqualify him. Unearned income $6,400 > $2,700 -> kiddie tax on **his own return with Form 8615**.
     Per procedure, discussed with Grace (02/20) and opened a separate client ID **EVG1021** with its own 1040 project code. His return was
     finished after this one because Form 8615 needs our taxable income ($402,319), tax, qualified dividends $5,904 and net
     capital gain $9,877.
   - **Chloe (12):** only $1,900 of credit-union interest. She must file (unearned > $1,350) unless we elect Form 8814. Election made:
     nothing added to our income (under $2,700); tax = 10% x ($1,900 - $1,350) = **$55** on line 16. Trade-off explained
     to Grace: the tax is the same $55 either way; 8814 saves a return and a fee. (If the parents' AGI mattered for any credit or
     deduction, including the child's income could hurt - not the case here since $0 is included.)
6. **WA529 1099-Q ($10,000).** Paid directly to Lakeside Hills Academy for grade-7 tuition. K-12 tuition up to $10,000 per beneficiary
   per year is a qualified expense in 2025 -> not taxable; nothing reported.
7. **CTC, Additional Medicare, NIIT.** Two children under 17 -> $4,400 before phase-out; MAGI $448,778 exceeds $400,000 by
   $48,778 -> reduction $2,450 -> CTC $1,950 (nonrefundable, fully used). Form 8959: Medicare wages
   $463,350 - $250,000 x 0.9% = $1,920; Northshore withheld $1,200 (0.9% over $200,000
   of Daniel's wages), claimed on line 25c. NIIT: NII $18,928 (interest, dividends, CG distributions, net RSU gains)
   x 3.8% = $719 (MAGI is far over $250,000, so the full NII is taxed).
8. **Itemized deductions.** WA has no income tax, so I elected **general sales tax** ($3,912 per the IRS calculator - Axcess blended-rate
   option). Even if the WA PFML employee premiums are treated as state income taxes (Rev. Rul. 2025-4), that option is only
   $2,011. SALT $18,148 (well under the $40,000 cap; MAGI < $500,000). Mortgage interest $24,311
   (post-2017 loan, balance $648k < $750k - no limitation), charity $4,000. Total $46,459 vs $31,500 standard -> itemize.
9. **Estimated tax penalty.** None. 2025 withholding $87,480 exceeds 110% of 2024 total tax (110% x $72,797 = $80,077), and
   Schedule H taxes are included in the 2210 computation and covered by that safe harbor.
10. **Washington.** No income tax return. WA capital gains excise applies only to long-term gains above the WA standard deduction
    (~$278,000 for 2025) - LT gains here are ~$9,877; not required.

## Open items / client communication
- None for the 2025 return. MISC project: 2024 amended return with Schedule H (Maria's 2024 wages) - in WIP.
- Advised clients: for 2026 either withhold Maria's income tax / FICA through a household payroll service or increase W-4 withholding
  to cover Schedule H; give Maria a 2026 W-4; calendar the 01/31 W-2 deadline.
- Next year Ethan will be 17: no CTC for him (ODC $500 instead), and kiddie tax still applies.

## Hand-off to signer / routing
- [x] Return locked; Accountant's copy saved as *reviewed*
- [x] Federal 1040 incl. Schedule H - e-file; no state return; no FBAR
- [x] Due date 04/15/2026 - filed 04/13/2026 (no extension)
- [x] Related filings routed: EVG1021 Ethan 1040 (e-filed 04/14/2026); W-2/W-3 (SSA, filed 03/10/2026); corrected 1099-NEC
- [x] eSign (Form 8879) - Grace preferred contact via email; refund by direct deposit (voided check on file)
- Billing: tier $2,400 + household-employer setup (EIN, W-2/W-3, corrected 1099, ESD guidance) 3.0 hrs billed on EVG1010-MISC-2025 (client
  chargeable - external reason: client-provided treatment was wrong). Ethan's return billed on its own project code. Nothing to W/O.
