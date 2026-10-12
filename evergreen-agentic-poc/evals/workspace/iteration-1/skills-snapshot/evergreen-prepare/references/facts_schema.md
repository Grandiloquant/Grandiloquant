# facts.json - input schema for `tools/compute_return.py`

`facts.json` is what a preparer would key into Axcess. The engine does the arithmetic. **Every judgment is yours**: what goes
in, at what amount, on which line. Amounts are dollars (cents allowed; the engine rounds). Omit anything that doesn't apply.
The engine ignores unknown keys and lists them in `diagnostics.json`, so a typo silently drops data. Always read the
diagnostics.

Contents: 1 Identity · 2 Wages · 3 Interest/dividends · 4 Retirement & SS · 5 Capital gains · 6 Schedule 1 income ·
7 Adjustments & SE · 8 Deductions · 9 QBI · 10 Schedule 1-A · 11 Credits · 12 Other taxes · 13 Special computations ·
14 Payments · 15 Worked example

## 1. Identity and status
```json
"client_id": "EVG1xxx",
"status": "MFJ",                       // S | MFJ | MFS | HOH | QSS
"taxpayer": {"age65": false, "blind": false},
"spouse":   {"age65": true,  "blind": false},   // MFJ (or MFS when spouse has no income)
"dependents": [ {"name": "Child A", "ctc": true}, {"name": "Parent B", "odc": true} ],
"claimed_as_dependent": false, "earned_for_dep_std": 0     // dependent filers: earned income for the std-deduction limit
```
`ctc` = qualifying child under 17 at 12/31 with an SSN (the $2,200 credit). `odc` = any other dependent ($500). A child released
to the other parent via Form 8332 is NOT listed for CTC on the custodial parent's return. HOH/2441 eligibility is separate.

## 2. Wages (one entry per W-2 actually kept - drop duplicates)
```json
"w2": [ {"who": "T", "box1": 50000, "box2": 4000, "box3": 52000, "box4": 3224, "box5": 52000, "box6": 754, "box10": 0} ]
```
`who` T/S drives the excess-SS credit (two+ employers, same person) and Form 2441 earned income. Box 5/6 drive Form 8959.
Box 10 (dependent-care benefits) is excluded automatically up to $5,000 and reduces the 2441 credit base.
Other wage-type income: `"hh_wages_no_w2"`, `"unreported_tips"` (Form 4137 tips -> line 1c; also set
`"unreported_tips_medicare"` to the same amount and `"form4137_tax"` = 7.65% of it), `"other_earned"`.

## 3. Interest and dividends (Schedule B)
```json
"interest": [ {"payer": "Bank A", "amount": 1000},
              {"payer": "Accrued interest paid - XYZ bond", "amount": -150},
              {"payer": "Muni fund", "amount": 0, "tax_exempt": 2000} ],
"dividends": [ {"payer": "Schwab", "ordinary": 5000, "qualified": 4000, "capgain_dist": 500, "exempt_int_div": 0} ]
```
* `amount` is TAXABLE interest and may be negative for adjustments: accrued interest paid at purchase, amortizable bond
  premium (box 11), nominee interest. Market discount recognized on sale is a positive interest line.
* `ordinary` includes `qualified` (1099-DIV 1a / 1b). `capgain_dist` (box 2a) goes to Sch D line 13 automatically.
* Nondividend distributions (box 3) are NOT income: reduce basis, don't enter. 199A dividends (box 5): `qbi.reit`.
* Foreign accounts: `"foreign_accounts": true, "foreign_account_country": "Canada"`, `"foreign_trust": true` (Sch B Part III).

## 4. Retirement and Social Security
```json
"ira":     [ {"payer": "Brokerage IRA", "gross": 20000, "taxable": 20000} ],           // line 4a / 4b
"pension": [ {"payer": "Plan", "gross": 500000, "taxable": 80000} ],                // line 5a / 5b (NUA: taxable = cost basis)
"ssa":     [ {"who": "T", "net_benefits": 24000} ]                                   // SSA-1099 box 5 (after repayments)
```
Rollovers (code G, or indirect within 60 days): gross shows, taxable 0. QCDs: taxable reduced by the QCD (age 70 1/2+).
Roth conversions: taxable per Form 8606 pro-rata. Taxable Social Security is computed for you (tax-exempt interest counts);
override with `"ss_taxable_override"` only with a worksheet reason. 10% early-distribution tax: `"form5329_tax"`.

## 5. Capital gains (Form 8949 / Schedule D)
```json
"trades": [ {"id": "1", "desc": "100 sh XYZ", "acq": "03/01/2019", "sold": "06/02/2025", "proceeds": 12000, "basis": 7000,
             "adj": 0, "code": "", "box": "D", "collectible": false} ],
"k1_st": 0, "k1_lt": 0,              // Sch D lines 5 / 12 (K-1 capital gains)
"other_st": 0, "other_lt": 0,        // Form 6252 installment gain, Form 4797 net 1231 gain, etc. (line 4 / 11)
"cap_loss_co": {"st": 0, "lt": 0},   // carryover INTO 2025, as positive numbers, by character
"unrecaptured_1250": 0, "g28_other": 0
```
* Gain = proceeds - basis + `adj`. Column (g) sign: a disallowed wash-sale loss is a POSITIVE adj (code W); market discount moved
  to interest is a NEGATIVE adj (code D); basis corrections (RSU/NSO) go in `basis` with code B; home-sale exclusion is a
  negative adj with code H. Collectibles: `"collectible": true` (28% rate).
* Boxes: A/B/C short-term (basis reported / not reported / no 1099-B); D/E/F long-term; G/H/I and J/K/L the 2025
  digital-asset boxes (1099-DA basis reported / not reported / no 1099-DA).
* Gains that aren't trades (excess S-corp/partnership distributions, 704(c)(1)(B), constructive sales, worthless stock) are
  entered as a trade line on box C/F with a clear desc.

## 6. Schedule 1 income
```json
"sch1": {"taxable_refunds": 0, "alimony": 0, "sch_c": 60000, "f4797": 0, "sch_e": 20000, "farm": 0, "unemployment": 4000,
         "other": [ ["8b", "Gambling winnings (W-2G)", 5000], ["8v", "Digital assets received as ordinary income", 1000],
                    ["8z", "Form 1099-K personal items sold at a loss", 3000] ]}
```
`sch_c` = sum of Schedule C net profit (after your book-to-tax adjustments and home office). `sch_e` = net Schedule E total
(rentals after passive/280A limits + K-1 income/loss actually allowed + guaranteed payments). `f4797` includes section
1244 ordinary loss (negative).

## 7. Adjustments and self-employment tax
```json
"se": [ {"who": "T", "net_profit": 60000, "w2_ss_wages": 0} ],     // Sch C net + K-1 box 14A; one entry per person
"adjustments": {"educator": 300, "hsa": 0, "sep": 10000, "se_health": 0, "early_wd_penalty": 0, "alimony_paid": 0,
                "ira_ded": 0, "student_loan": 1500,
                "other": [ ["24z", "Form 1099-K personal items (offset)", 3000] ]},
"se_earned_T": 0, "se_earned_S": 0       // SE earned income for Form 2441 earned-income test
```
Half of SE tax is computed for you. Student-loan interest phase-out is applied for you (enter interest paid, max $2,500).

## 8. Deductions
```json
"itemized": {"medical": 0, "state_income_tax": 14000, "use_sales_tax": false, "real_estate_tax": 9000, "personal_property_tax": 0,
             "other_taxes": 0, "mortgage_interest_1098": 15000, "mortgage_interest_no_1098": 0, "points": 0,
             "investment_interest": 2000, "charity_cash": 5000, "charity_noncash": 0, "charity_carryover": 0,
             "casualty": 0, "other_itemized": 0, "other_itemized_desc": ""},
"force_itemize": false, "salt_magi_addback": 0
```
Supply `itemized` whenever there's anything to compare. The engine takes the larger of itemized and standard (unless
`force_itemize`), applies the 7.5% medical floor and the SALT cap/phase-down. Enter the **allowable** mortgage interest
(after any $750k/$1M limitation and after removing the home-office share) and allowable investment interest (Form 4952).
`state_income_tax` = state/local income tax actually PAID in 2025 (withholding + estimates paid in 2025 + prior-year balance
paid in 2025). `use_sales_tax: true` if general sales tax is larger. Gambling losses (up to winnings), 691(c) IRD deduction ->
`other_itemized`.

## 9. QBI
```json
"qbi": {"businesses": [ {"name": "Sch C - Lawn", "qbi": 50000, "w2_wages": 0, "ubia": 0, "sstb": false} ],
        "loss_carryforward": 0, "reit": 0, "ptp": 0}
```
`qbi` = net business income REDUCED by deductible half SE tax, SE health and retirement contributions attributable to it.
`reit` = 1099-DIV box 5; `ptp` = PTP qualified income. Above the threshold, `w2_wages`/`ubia`/`sstb` matter.

## 10. Schedule 1-A (OBBBA)
```json
"sch1a": {"tips": 4000, "tip_occupation": "Bartender", "overtime": 2000, "car_interest": 1500, "vin": "1FA...", "seniors": 1}
```
`overtime` = qualified PREMIUM only. `seniors` = number of people 65+ at 12/31/2025 (1 or 2). Omit for MFS.

## 11. Credits
```json
"dependent_care": {"expenses": 6000, "n_qual": 2},           // qualified expenses paid (before FSA), # qualifying persons
"education": [ {"name": "Student", "type": "AOTC", "qualified_expenses": 4000} ],   // after tax-free scholarships
"eic_eligible": true, "eic_kids": 1, "eic_invest_income": 0,
"ftc": {"method": "direct", "taxes": 250},                                         // de minimis election
"ftc": {"method": "1116", "taxes": 2000, "foreign_source_ti": 10000, "category": "general"},
"res_clean_energy": 0, "energy_home_improvement": 0, "other_nonref_credits": 0,
"ctc_magi_addback": 0, "earned_income_8812": null
```
CTC/ODC come from `dependents`. Credit ordering and the tax-liability limit are applied for you.

## 12. Other taxes (Schedule 2) and AMT
```json
"amt": {"iso": 25000, "pab": 0, "other": 0},       // ANY non-empty dict runs Form 6251; use {"check": true} to just test
"niit": {"nii": 98000, "gross": 100000, "deductions": 2000},   // you compute NII (Form 8960 lines 1-11)
"form5329_tax": 0, "schedule_h_tax": 0, "excess_aptc": 0, "uncollected_fica_w2": 0,
"sch2_other": [ ["17z", "Description", 0] ]
```
Additional Medicare Tax (Form 8959) is computed from W-2 box 5/6 and SE earnings automatically.

## 13. Special computations
```json
"kiddie_8615": {"net_unearned": 2000, "parent_status": "MFJ", "parent_ti": 250000, "parent_qd": 0, "parent_ncg": 0,
                "child_qd_nui_share": 0, "child_ncg_nui_share": 0, "other_children_nui": 0},
"form_8814_tax": 0,                                          // parent's return: child's interest under Form 8814
"line16_other": [ ["Section 962 election tax (statement)", 1000] ]
```

## 14. Payments
```json
"withholding_1099": 0, "withholding_other": 0,      // 1099-R/1099-G/W-2G/1042-S withholding (other = 1042-S, etc.)
"estimated_payments": 8000,                         // 2025 estimates actually paid + 2024 overpayment applied
"extension_payment": 2000, "apply_to_2026": 0, "es_penalty": 0,
"net_ptc": 0, "sch3_ref_other": []
```
Excess Social Security (two+ employers) is computed from the W-2s automatically.

## 15. Worked example (MFJ, two W-2s, newborn, overtime premium)
```json
{"client_id": "EXAMPLE", "status": "MFJ", "taxpayer": {"age65": false}, "spouse": {"age65": false},
 "dependents": [{"name": "Kid 1", "ctc": true}, {"name": "Kid 2", "ctc": true}, {"name": "Newborn", "ctc": true}],
 "w2": [{"who": "T", "box1": 50000, "box2": 4000, "box4": 3224, "box5": 52000, "box6": 754},
        {"who": "S", "box1": 40000, "box2": 2500, "box4": 2480, "box5": 40000, "box6": 580, "box10": 5000}],
 "interest": [{"payer": "Bank A", "amount": 1000}, {"payer": "Bank B", "amount": 40}],
 "dependent_care": {"expenses": 6000, "n_qual": 2},
 "sch1a": {"overtime": 2000, "car_interest": 1500, "vin": "1FA6P8XXXXXXXXXXX"}}
```
