# EVG1013 Nathan J. Brooks - 2025 Form 1040 preparation notes

Status: Single, no dependents, Illinois (Chicago) resident all year. Extension (Form 4868) filed 04/13/2026 with a $6,000 payment, so the extended due date is **10/15/2026**.

## Result (federal)
| Item | Amount |
|---|---:|
| Wages (W-2 box 1, Parallax) | 164,700 |
| Taxable interest (Wealthfront 1099-INT) | 1,284 |
| Capital gain/(loss) (NSO same-day sale, adjusted basis) | (25) |
| **AGI** | **165,959** |
| Standard deduction (single, OBBBA) | 15,750 |
| **Taxable income** | **150,209** |
| Regular tax | 28,897 |
| AMT (Form 6251, ISO spread) | 4,346 |
| **Total tax** | **33,243** |
| Withholding 27,600 + extension payment 6,000 | 33,600 |
| **Refund** | **357** |

## Treatment of each item
1. **W-2 Parallax.** Box 1 $164,700 already includes the $22,000 NSO spread (supplement). Box 12 D $12,000 (401(k)), W $4,300 (HSA payroll $3,300 + employer seed $1,000), V $22,000 (NSO), DD info only. Medicare wages $176,700 < $200,000, so no Additional Medicare Tax. SS wages equal the 2025 wage base ($176,100); single employer, so no excess-SS credit.
2. **NSO exercise and same-day sale (9/18/2025).** The 1099-B reports basis of only $4,000 (exercise price), which would tax the $22,000 again. Form 8949 Box A, adjusted basis $26,000 = $4,000 paid + $22,000 compensation on the W-2 (Treas. Reg. 1.6045-1(d)(6)(ii)(C); 1.83-4(b)), code B. Result: $24.95 short-term loss (the commissions). This answers the client's "taxed twice" question: he is not.
3. **ISO exercise and hold (Form 3921).** 4,000 shares, FMV $14.00 less $1.50 = $50,000 bargain element. No regular-tax income (IRC 421/422). AMT adjustment, Form 6251 line 2i = $50,000 (IRC 56(b)(3)). Result: AMT $4,346. AMT basis of the lot is $56,000 (regular basis $6,000); track for the disposition year. The full $4,346 relates to a deferral item, so it creates a **minimum tax credit carryforward of $4,346 to 2026 (Form 8801)**. Shares were held at 12/31/2025 (value $45,400 < AMT basis); a disqualifying disposition in 2025 did not occur, so no relief from AMT is available on the 2025 return. Prior-year WP noted the AMT warning.
4. **Loomwork AI founder stock / Section 83(b).** Grant (transfer) date 11/03/2025; an 83(b) election must be filed within 30 days of transfer, i.e. by **12/03/2025** (IRC 83(b)(2); Reg. 1.83-2(b)). Form 15620 was signed 12/08/2025 and the certified-mail postmark is **12/10/2025** - 7 days late. A late 83(b) election is invalid and the deadline cannot be extended (no 9100 relief; Reg. 1.83-2(b), 301.9100 does not apply to statutory deadlines). Therefore **$0 of the $8,000 is reported in 2025** (the shares are substantially nonvested, so there is no transfer for tax purposes until vesting). Instead, Brooks will recognize ordinary compensation income equal to the FMV of each tranche as it vests (first 25% on 11/03/2026, then monthly), which Loomwork should report on a W-2 (and withhold). Client advisory needed: the election being invalid is likely costly if Loomwork's value rises; consider with counsel whether the shares could be re-issued/modified (e.g., cancel and re-grant, or amend vesting) to allow a new timely election. Do not attach the Form 15620 to the return.
5. **HSA (Form 8889).** Self-only HDHP all year; 2025 limit $4,300; age 30 (no catch-up). Employer/cafeteria contributions (W-2 code W) = $4,300 = the limit. The $1,000 after-tax April contribution is an excess contribution. It and its $38 net income were withdrawn on 09/15/2026, before the extended due date (10/15/2026), so: no HSA deduction for the $1,000 (Form 8889 line 2 = $0, line 9 = $4,300, line 13 = $0), no 6% excise tax (no Form 5329 needed), and the $38 of earnings is taxable in **2026** (the year distributed; 2026 Form 1099-SA code 2). Form 5498-SA shows $5,300 total (consistent). Engine adjustment hsa = 0.
6. **Interest.** Wealthfront 1099-INT $1,284.37 (client estimate ~$1,300). Schedule B is not technically required under $1,500 but the engine prints it; harmless.
7. **Charity.** $250 cash to Chicago Public Library Foundation, written acknowledgment on file. Itemized ($8,150 state withholding + $250 = $8,400) is below the $15,750 standard deduction; no deduction. The OBBBA non-itemizer charitable deduction starts in 2026, not 2025.
8. **Estimated-tax penalty.** None: 2025 withholding $27,600 exceeds 100% of 2024 tax ($23,526; 2024 AGI under $150k), so the Form 2210 safe harbor is met.
9. **Digital assets:** answer No (organizer). **Foreign accounts:** No.

## Illinois (IL-1040) - resident
Base income = federal AGI $165,959 (no IL additions/subtractions identified; HSA treatment follows federal). Exemption $2,850 (2025; AGI under $250k). Net income $163,109 x 4.95% = **$8,074**. IL withholding (W-2 box 17) $8,150. **IL refund approx. $76.** IL extension is automatic to 10/15/2026; nothing was due at 4/15 as withholding exceeds tax. Illinois has no AMT. Chicago has no city income tax - no local return.

## Open items / advisory (for reviewer)
- Confirm with client that no other 83(b) copy was mailed earlier than 12/10/2025 (cap table shows company received copy 12/08/2025; that is also after 12/03/2025, so the conclusion is unchanged).
- Advise client in writing on the invalid 83(b) and future vesting income; Loomwork payroll should report vesting income.
- 2026 planning: Form 8801 credit $4,346 carryforward; AMT basis $56,000 in the ISO lot; HSA earnings $38 taxable in 2026; consider 2026 estimates/withholding for Loomwork vesting income.
- IL exemption amount ($2,850) taken from 2025 IL-1040 instructions as understood; verify in software.
