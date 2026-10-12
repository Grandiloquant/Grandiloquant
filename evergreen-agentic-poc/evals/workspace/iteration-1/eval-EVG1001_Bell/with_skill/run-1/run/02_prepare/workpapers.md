# EVG1001 - Bell - 2025 Workpapers (off-system computations)

## WP-1 Wages (Form 1040 line 1a)
| W-2 | Box 1 | Box 2 | Source |
|---|---:|---:|---|
| Lone Star Distribution (Marcus) | 58,477.50 | 3,960.00 | PBC/02 |
| Brightsmile Dental (Tanya) | 47,000.00 | 2,810.00 | PBC/03 |
| Brightsmile photo copy | excluded - DUP | excluded | PBC/04 (identical control BSD-22-014, all boxes) |
| **Total** | **105,477.50** | **6,770.00** | |
Tie-out Marcus: box 3/5 61,850.00 - code D 401(k) 3,372.50 = 58,477.50 box 1 (SEC125 3,600 incl. HSA already outside box 3/5). Excess SS: n/a (one employer each).
Additional Medicare: n/a (Medicare wages < 250k).

## WP-2 Interest (line 2b)
Chase 38.42 (PBC/05) + Ally 1,246.19 (PBC/13) = 1,284.61. Under $1,500 - Schedule B not strictly required (engine prints it; harmless).

## WP-3 Schedule 1-A overtime (Part III)
Marcus: hourly non-exempt (PERM/Client_Profile.md) -> FLSA overtime. W-2 box 14 "OVERTIME 9,450.00" (PBC/02) is not labelled as
premium-only. Per 2025 reference/IRS transition guidance, where the amount reported is total overtime paid at 1.5x, the
qualified premium = total / 3 = 9,450.00 / 3 = **3,150.00**. Cap 25,000 MFJ; MAGI 106,763 < 300,000 phase-out - no reduction.
MFJ required - met. Open item: confirm with employer; if 9,450 is already the premium, deduction rises to 9,450 (tax ~-760 at 12%).

## WP-4 Schedule 1-A qualified passenger vehicle loan interest (Part IV)
| Test | F-150 (PBC/08) | CR-V (PBC/09) |
|---|---|---|
| New (original use) | Yes - 2025 model, NEW | No - 2022, pre-owned |
| Loan originated after 12/31/2024 | 03/08/2025 | 06/14/2024 - fails |
| Secured by vehicle | First lien | n/a |
| Final assembly in US | Dearborn, MI (Monroney) | n/a |
| VIN | 1FTFW1E58SFA10393 | n/a |
| 2025 interest | **2,452.18** | 1,104.77 - not deductible |
Cap 10,000; phase-out starts MAGI 200,000 MFJ - none. Personal use assumed (organizer "new truck"; no business activity on return).

## WP-5 Form 2441 dependent care
| Provider / child | Amount | Qualified? |
|---|---:|---|
| Kids Kampus after-school (EIN 00-6618204) - Maya | 4,200.00 | Yes |
| Camp Cedar Ridge (EIN 00-5512093) day camp - Jaylen | 1,300.00 | Yes (day camp) |
| Camp Cedar Ridge day camp - Maya | 1,300.00 | Yes |
| Camp Cedar Ridge Adventure Week overnight - Jaylen | 1,400.00 | **No** - overnight camp (Reg. 1.21-1(d)(9); Pub 503) |
| Sum of statement lines | 8,200.00 | (statement prints "Total 5,400" - arithmetic/PY figure error) |
| Qualified expenses | **6,800.00** | |
Qualifying persons with expenses: Jaylen (10), Maya (6) -> $6,000 limit. Employer benefits (Tanya W-2 box 10) 5,000 - fully
excluded (<= 5,000, <= expenses, <= lower earned income 47,000). Credit base = min(6,800 - 5,000, 6,000 - 5,000) = 1,000 x 20%
(AGI > 43,000) = **200**. Tanya's "9,600 paid" (1,400 more than the statements) is unsupported but would not change the credit.

## WP-6 HSA (Form 8889)
Family HDHP (PY WP). Contributions: W-2 code W 3,000.00 (employer + pre-tax payroll; ties to 5498-SA box 2 3,000.00).
Limit 8,550 family (both under 55) - no excess; no additional deduction (line 13 = 0). Distribution 1099-SA 1,150.00 code 1 -
assumed qualified medical expenses -> taxable 0, no 20% additional tax. (Engine has no 8889 input; nothing flows to 1040.)

## WP-7 Dependents / CTC
Jaylen (10), Maya (6), Noah (born 12/18/2025 - counts as lived with parents all year; SSN issued before return due date):
3 x 2,200 = 6,600. MAGI 106,763 < 400,000. Fully absorbed as nonrefundable (tax before credits 7,884).

## WP-8 Deduction choice
Standard 31,500 MFJ. No itemizable items (no mortgage, TX - no income tax; sales tax would be well under 31,500). Standard used.

## WP-9 Prior-year comparison
| Item | 2024 | 2025 | Why |
|---|---:|---:|---|
| Wages | 101,240 | 105,478 | raises/overtime |
| Interest | 1,011 | 1,285 | higher Ally HYSA rate/balance |
| AGI | 102,251 | 106,763 | |
| Std deduction | 29,200 | 31,500 | OBBBA |
| Sch 1-A | - | 5,602 | new OBBBA deductions |
| Taxable income | 73,051 | 69,661 | |
| CTC | 4,000 | 6,600 | newborn + $2,200/child |
| 2441 credit | 200 | 200 | same FSA pattern |
| Refund | 3,902 | 5,686 | above items |

## WP-10 Payments / Form 2210
Withholding 6,770.00 (3,960.00 + 2,810.00). No estimates. Refund - no 2210.
