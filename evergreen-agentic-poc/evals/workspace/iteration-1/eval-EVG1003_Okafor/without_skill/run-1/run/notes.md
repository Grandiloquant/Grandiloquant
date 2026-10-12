# EVG1003 Daniel Okafor - 2025 Form 1040 preparation notes

Filing status: Single, no dependents. Nevada resident (Las Vegas, Clark County). Engine: `tools/compute_return.py`
(facts at `02_prepare/facts.json`, output at `final/`). Engine diagnostics: none.

## Result
| Item | Amount |
|---|---:|
| AGI (line 11) | 61,874 |
| Standard deduction | 15,750 |
| Schedule 1-A qualified tips deduction | 25,000 |
| QBI deduction | 3,175 |
| Taxable income (line 15) | 17,949 |
| Income tax (line 16) | 1,913 |
| SE tax 2,414 + Form 4137 tax 122 | 2,536 |
| Total tax (line 24) | 4,449 |
| Withholding 3,150 + 2025 estimates 1,000 | 4,150 |
| **Balance due (line 37)** | **299** |
| Form 2210 penalty | 0 (safe harbor met, see below) |

## Wages and tips
* W-2 Silver Sage Casino Resort: box 1 $44,400 (includes $24,600 tips reported to employer on Form 4070, box 7/box 14),
  box 2 $3,150, box 3 $19,800, box 5 $44,400. Box 4/6 agree to 6.2%/1.45%.
* **Unreported tips - Form 4137 on $1,600 actual, not the $2,900 box 8 allocated tips.** Client keeps a contemporaneous
  daily tip diary (sample January daily page + monthly totals, $24,600 reported + $1,600 unreported = $26,200; reported
  column ties exactly to W-2 box 7). Client confirmed (email 2/18/2026) the diary covers every shift. Allocated tips need
  not be reported when adequate records show actual tips (Treas. Reg. 31.6053-3; Form 4137 instructions; Pub. 531).
  Consistent with 2024 treatment. Line 1c $1,600; Form 4137 SS/Medicare $1,600 x 7.65% = $122.40. Statement explaining
  the allocated-tip difference to be attached.
* **Barback tip-outs (~$2,850) - no deduction.** Client reports tips to the employer after tip-out (diary and email), so
  amounts paid to barbacks were never included in his income; a further deduction would double count. Also an estimate
  ($15 x 190 shifts), not a record.

## Schedule 1-A - No tax on tips (OBBBA, IRC 224)
* Bartender is a listed tipped occupation; casino bar is not an SSTB; MAGI $61,874 is under the $150,000 phase-out.
* Qualified tips = W-2 box 7 $24,600 + Form 4137 $1,600 = $26,200 (cash tips voluntarily paid by customers), capped at
  $25,000. Uber rider tips ($2,860; rideshare driver is also a listed occupation) are not needed - cap already reached.
* Deduction $25,000 on line 13b (below AGI; does not reduce SE/FICA).

## Schedule C - Uber rideshare (NAICS 485310), cash method
| Item | Amount | Source / reason |
|---|---:|---|
| Gross receipts - 1099-K box 1a | 38,720 | Gross per PY method; one 1099-K only - doc 11 is an identical duplicate upload, dropped |
| Other income - 1099-NEC (incentives/referrals) | 1,150 | |
| Gross income | 39,870 | |
| Uber service, booking and airport/other fees | (11,140) | Uber tax summary; gross-up reconciles to deposits $28,730 |
| Car - standard mileage 15,145 mi x $0.70 | (10,601.50) | Uber online miles (app record, ties to log "uber app" column); std mileage elected in 2024 first year |
| Tolls | (340) | Tolls paid on trips (reimbursed by riders, included in gross); deductible in addition to standard rate |
| Phone $1,020 x 60% business | (612) | T-Mobile annual statement; 60% business per client, consistent with PY |
| Dash cam $149 x 63.8% business use | (95.01) | Vehicle business % = 15,145 / 23,750 total miles (odometer photos 48,210 -> 71,960) |
| **Net profit** | **17,081.49** | |

* **Commuting miles excluded (4,180).** Drive home <-> casino for the W-2 job is personal commuting (Rev. Rul. 99-7;
  Reg. 1.262-1(b)(5)); client confirmed in email he goes online from home, not from work. Total business miles on Form
  4562/Sch C Part IV = 15,145; commuting 0 claimed; other personal miles 8,605.
* Offline miles (home to first pickup before going online) are not in the Uber figure and no separate log exists, so
  none claimed (consistent with PY).
* Gas $3,900, GEICO insurance $2,280 (incl. TNC endorsement), maintenance $310: **not deductible separately** - covered by
  the standard mileage rate. No car loan (paid off 2024), so no Sch 1-A car-loan interest.
* Car washes / water & mints $380: car washes are covered by the standard mileage rate; rider amenities would be
  deductible supplies but the client gave one combined figure. **Not deducted - open item** (request split; max effect
  ~ $380 x ~30% marginal incl. SE).
* QBI = $17,081.49 - half SE tax $1,206.77 = $15,874.72; non-SSTB, below threshold; deduction 20% = $3,175.

## Self-employment tax
Net earnings $15,775 (92.35%); W-2 SS wages + SS tips + 4137 tips = $46,000 well under $176,100 base. SE tax $2,414;
half ($1,207) deducted on Sch 1 line 15.

## Payments and Form 2210
* W-2 withholding $3,150; 2025 estimates $500 (4/14/2025) + $500 (6/16/2025) per IRS online account = $1,000. The
  4/14/2025 $459 payment was the 2024 balance due, not a 2025 estimate. Client skipped Sept/Jan vouchers.
* No underpayment penalty: required annual payment = lesser of 90% of 2025 tax ($4,004) or 100% of 2024 tax ($3,159,
  AGI < $150k). Withholding treated as paid evenly ($787.50/qtr) plus estimates gives cumulative $1,287.50 / $2,575 /
  $3,362.50 / $4,150 vs required $789.75 / $1,579.50 / $2,369.25 / $3,159 - every installment met. Form 2210 not required.
* EIC: not eligible (AGI above the single no-child limit).

## State / local / other
* Nevada has no individual income tax; Las Vegas/Clark County have no local income tax - no state or local income tax
  return. Nevada Commerce Tax applies only above $4M Nevada gross revenue - not applicable.
* Compliance reminder (not a tax return): Nevada requires rideshare (TNC) drivers to hold a Nevada State Business
  License; confirm Danny's is current.
* 2026 estimates: 2026 safe harbor = 100% of 2025 tax $4,449. With similar withholding (~$3,150), recommend 1040-ES of
  about $325/quarter (4/15, 6/15, 9/15/2026, 1/15/2027); more if Uber income grows.

## Open items / assumptions
1. Split of the $380 car washes vs. water/mints for riders (excluded pending answer).
2. Confirm filing timing: today is 10/12/2026, past the 4/15/2026 due date. No Form 4868 is in the file. If an extension was
   filed, file by 10/15/2026; otherwise expect failure-to-file/pay penalties and interest on the $299 balance due.
3. Dash cam business share assumed equal to vehicle business-use %.
4. Phone 60% business use per client representation (as in 2024).
