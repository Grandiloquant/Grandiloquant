# Tax Year 2025 quick reference (federal + the states the firm files most)

Law: Rev. Proc. 2024-40 as amended by P.L. 119-21 (the One Big Beautiful Bill Act, "OBBBA"). The calculation engine
(`tools/compute_return.py`) already contains the brackets, tax table, capital-gain worksheet, standard deduction, SE tax,
Additional Medicare, NIIT, AMT exemptions, CTC/ACTC/ODC, EITC, education credits, Form 2441, Schedule 1-A, SALT phase-down and
QBI thresholds. This sheet is for the **judgment calls** the engine can't make.

## Federal figures
| Item | 2025 |
|---|---|
| Standard deduction | S/MFS $15,750; MFJ/QSS $31,500; HOH $23,625; +$2,000 (S/HOH) or +$1,600 (married) per 65+/blind box. Dependent: greater of $1,350 or earned income + $450 (capped at regular amount) |
| Senior deduction (new, Sch 1-A) | $6,000 per person who is 65 by 12/31/2025 (born before 1/2/1961); reduced 6% of MAGI over $75k ($150k MFJ), per person; MFS not allowed; SSN required |
| No tax on tips (Sch 1-A) | Qualified tips in a listed occupation (bartenders, servers, rideshare drivers, etc.), up to $25,000; phase-out $100 per $1,000 MAGI over $150k ($300k MFJ); married must file jointly; SE tips limited to the business's net income |
| No tax on overtime (Sch 1-A) | Only the FLSA **premium** (the "half" in time-and-a-half) - if a W-2 shows total OT paid at 1.5x, premium = total / 3; cap $12,500 ($25,000 MFJ); same phase-out; married must file jointly. If the employer reports the premium itself, use it as is |
| Car-loan interest (Sch 1-A) | New personal-use vehicle, final assembly in the US, loan originated after 12/31/2024, secured by the vehicle; up to $10,000; VIN required; phase-out $200 per $1,000 over $100k ($200k MFJ). Used cars and pre-2025 loans don't qualify |
| SALT cap | $40,000 ($20,000 MFS), minus 30% of MAGI over $500,000 ($250k MFS), floor $10,000. Pass-through entity (PTE) tax paid by an entity is deducted at the entity, not on Sch A |
| CTC / ACTC / ODC | $2,200 per child under 17 with SSN / refundable up to $1,700 / $500 other dependents; phase-out $50 per $1,000 over $200k ($400k MFJ). A child born during the year counts as living with you all year |
| Qualifying relative gross-income test | $5,200 (nontaxable Social Security doesn't count) |
| Kiddie tax | Unearned income > $2,700 -> Form 8615 at the parent's rate. Form 8814 (parents report) only if the child's income is solely interest/dividends/cap-gain distributions and < $13,500. Child must file if unearned income > $1,350 |
| Dependent care | Credit 20-35% of up to $3,000/$6,000 **minus** excluded employer benefits (W-2 box 10, excludable up to $5,000). Overnight camp isn't a qualified expense |
| Education | AOTC 100% of first $2,000 + 25% of next $2,000, 40% refundable, 4 years; LLC 20% of $10,000; both phase out $80-90k / $160-180k MFJ; reduce expenses by tax-free scholarships |
| QBI | Threshold $197,300 / $394,600 MFJ; phase-in $50k / $100k; SSTB fully out above the range; limit 20% x (taxable income - net capital gain) |
| Gambling | 2025 losses deductible up to 100% of winnings, itemized only. (The OBBBA 90% limit starts in **2026**) |
| Charitable | Itemizers only in 2025 (the non-itemizer deduction and 0.5% floor start **2026**). Used clothing = FMV (thrift value), never more than cost. Gifts to individuals (GoFundMe) aren't deductible. DAF gifts count when made |
| Personal casualty | Only federally declared disasters in 2025 (state-declared starts 2026) |
| Mortgage interest | Acquisition debt limit $750,000; $1,000,000 for debt incurred before 12/16/2017 (grandfathered). Pro-rate by average balance |
| Retirement | IRA $7,000 (+$1,000 at 50+); 401(k) $23,500; SEP 25% of comp (20% of net SE earnings after 1/2 SE tax for the self-employed), max $70,000; QCD age 70 1/2, limit $108,000; RMD age 73 |
| HSA | $4,300 self / $8,550 family (+$1,000 at 55+); W-2 code W already includes pre-tax payroll deferrals. Excess removed (with earnings) by the extended due date avoids the 6% excise |
| SE tax | 15.3% on 92.35% of net SE earnings; SS portion only up to $176,100 minus W-2 SS wages **and** SS tips (box 7) and Form 4137 tips (Sch SE lines 8a-8b) |
| Tips deduction mechanics | Qualified tips = W-2 box 7 SS tips + Form 4137 unreported tips + self-employed tips (e.g. rideshare rider tips); SE tips limited to that business's net income; then the $25,000 cap |
| NIIT detail | NII = interest + dividends + net gains + passive income - properly allocable deductions (investment interest; state/local income tax allocable to NII on Form 8960 line 9b = deductible income-tax portion of Sch A SALT x NII/AGI-type ratio; advisory fees not deductible 2018-2025). Active S-corp/partnership gains: 8960 line 5c |
| AMT credit | AMT from deferral items (ISO spread) creates a Form 8801 minimum tax credit carryforward; track AMT basis of ISO shares |
| Timely mailing | A paper election/return is timely if postmarked by the deadline (IRC 7502). 83(b): within 30 days of transfer - no extensions |
| HSA excess | Excess + earnings withdrawn by the extended due date: no 6% excise, no deduction for the excess, earnings taxable in the year withdrawn. Form 8889 still filed |
| Vacation home (280A) | Firm default = IRS method (rental days / total days used) for all expenses; mention Bolton (interest & taxes by rental days / 365) as an alternative when it helps. Costs before the property was first rented aren't rental expenses. Converted personal home: depreciable basis = lower of FMV or adjusted basis at conversion. Expenses solely for guests (supplies, cleaning fees) are 100% rental |
| Mileage | 70 cents/mile (business). Commuting is never deductible. Standard mileage covers ALL vehicle operating costs (gas, insurance, repairs, car washes, depreciation) - only parking, tolls and business % of auto-loan interest (self-employed) are added. Equipment used in the car for all driving (dash cam) follows the vehicle's business-use % |
| De minimis safe harbor | $2,500 per item/invoice (election statement); improvements (new roof) must be capitalized |
| Depreciation | 100% bonus for property acquired after 01/19/2025; residential rental 27.5-yr, nonresidential (incl. transient-use units) 39-yr, mid-month |
| 1099-K | Reporting threshold back to $20,000 and 200 transactions; personal items sold at a loss: report proceeds on Sch 1 line 8z and offset on 24z |
| 1099-DA | 2025 forms report gross proceeds only (no basis). Use Form 8949 digital-asset boxes G/H/I (short) and J/K/L (long). Wash sales don't apply to crypto in 2025 |
| Clean energy | 25D (30%) and 25C only for expenditures through 12/31/2025; clean vehicle credit ended for vehicles acquired after 09/30/2025 |
| Estimated tax safe harbor | Lesser of 90% of current-year tax or 100% of prior-year tax (110% if prior-year AGI > $150k, $75k MFS). Withholding is treated as paid evenly |
| Foreign | FBAR if foreign accounts total > $10,000 at any time (signature authority counts). Form 8938 (living in US): > $50k year-end/$75k any time (single), $100k/$150k (MFJ). Form 3520 for gifts from foreign individuals > $100,000 or any foreign-trust distribution. FTC de minimis ($300/$600 MFJ) only if ALL foreign income is qualified passive income on a payee statement (1099/K-1) - foreign pensions and foreign bank interest don't qualify -> Form 1116. Creditable foreign tax is limited to the treaty rate. FX: IRS yearly average 2025 CAD 1.398, INR 87.147 |
| Passive | $25,000 rental allowance (active participation) phases out between $100k and $150k MAGI; limited partners don't get it. Short-term rentals (average stay 7 days or less) aren't "rental activities" - test material participation |
| PTC | Enhanced subsidies still apply for 2025; at or above 400% FPL there is no repayment cap |

## Filing status reminders
* Schedule 1-A tips/overtime/senior deductions require a joint return if *married*; a separated parent who qualifies as
  "considered unmarried" for HOH is treated as not married (IRC 7703(b)) and can claim them.
* Married at 12/31 = married for the whole year (MFJ or MFS). Divorced by 12/31 = unmarried. Separated is still married,
  BUT a separated parent can file HOH if "considered unmarried" (spouse out of the home the last 6 months, taxpayer paid
  more than half the cost of the home, child lived there more than half the year).
* Spouse died during 2025: the survivor files **MFJ** for 2025. Qualifying surviving spouse applies only to the two
  following years, and only with a dependent child.
* Single + qualifying person -> check HOH.

## State quick facts (summary-level state returns)
| State | 2025 rule of thumb |
|---|---|
| IL | 4.95% flat on federal AGI +/- modifications (US Treasury interest, retirement income and Social Security subtracted); exemption $2,850 each (none if AGI > $250k single / $500k MFJ); IL EIC 20% of federal; property-tax credit 5% (AGI limits). Nonresident employees working 30 or fewer days in IL aren't taxed on that compensation (verify) |
| MI | 4.25%; exemption $5,800 per person/dependent claimed on the federal return. Cities: Detroit 2.4% resident / 1.2% nonresident ($600 exemption); Grand Rapids 1.5% / 0.75% ($600 exemption). No Michigan tips/overtime subtraction is in this reference for 2025 - don't apply one; flag it |
| PA | 3.07% flat on PA income classes (compensation, interest, dividends, net gains, rents...). No standard deduction; losses don't cross classes; retirement distributions after retirement aren't taxable; credit for tax paid to other states on the same income. PA-NJ reciprocity on wages |
| NC | 4.25%; NC standard deduction $12,750 S / $25,500 MFJ / $19,125 HOH; Social Security subtracted; Bailey-settlement government pensions (5+ years vested by 08/12/1989) exempt; NC adds back 85% of federal bonus depreciation and deducts it 20%/yr over 5 years |
| MA | 5% (4% surtax above ~$1.08M); nonresidents taxed on MA-source income (wages by MA workdays); exemptions prorated |
| TX, FL, NV, TN, WA, SD, WY, AK, NH | No wage income tax (WA has a 7% capital-gains excise above its standard deduction - check large LTCG) |
