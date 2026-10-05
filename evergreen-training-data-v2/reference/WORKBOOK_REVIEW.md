# Review of `CCH_Axcess_1040_Exception_Workbook_v2.xlsx`

I filled this workbook for 25 synthetic clients and checked every formula with a calculation engine (pycel). Several tabs
return wrong answers no matter what is typed in, because of formula-reference errors. The corrected copy
(`CCH_Axcess_1040_Exception_Workbook_v2_CORRECTED.xlsx`) fixes them, and its **Corrections Log** tab lists every changed
cell. All per-client workbooks in v2 are built from the corrected copy. The original is kept unchanged as
`..._ORIGINAL.xlsx`.

## Defects that change answers

| Tab | Problem | Effect | Fix |
|---|---|---|---|
| 5. Passive Activity (8582) | The formulas in E26-E28 read B23, B24, B26 and B27. Those cells sit inside merged label ranges (A:D), and the threshold and results live in column E. | The tab always shows the full **$25,000** special allowance, whatever the MAGI. | MAGI goes in **E23**. E26 `=MAX(0,E23-E24)`, E27 `=MIN(25000,ROUND(E26*0.5,0))`, E28 `=MAX(0,25000-E27)`. |
| 8. Est. Tax Penalty (2210) | Every formula reads B12-B19, which are inside merged A:D label ranges. | The required annual payment is always $0 and the tab always says **"YES - no penalty override needed"**. For example, EVG1007 owes a $779 penalty, which the original tab would wave through. | Inputs go in **E12** (CY tax), **E14** (PY AGI), **E15** (PY tax) and **E19** (payments), with the formulas rewired. Quarterly installments use E18. |
| 10. Capital Loss Carryover | The column-D formulas read B10-B12 and B14/B15, which are inside merged A:C ranges. | Every carryover is $0. If inputs could be entered, the $3,000 deduction would still never be subtracted. | Inputs go in **D10-D12**, and D13-D17 are rewired. |
| 7. Multi-State Allocation | The resident-credit limit is `MIN(tax paid, alloc % x total federal income)`. | It compares tax with **income** (state-source income), so the cap almost never binds. | New input column **G** (resident-state tax before credit). Limit `=MIN(E,G x D)`. |
| 12. S-Corp Dual Basis | `=MAX(0,E-(B+D))` nets a current-year **loss** against basis before testing distributions. | It overstates the taxable distribution when there is a loss. Distributions come before losses under Reg. 1.1367-1(f). | `=MAX(0,E-(B+MAX(0,D)))`. Losses then hit what is left of stock basis, followed by debt basis. |
| 21. Involuntary Conv. 1033 | The deadline is the event date + 2 x 365 days. | Too early. The statute runs to the end of the 2nd year (3rd for condemned business/investment real property, 4th for a disaster-area main home) **after the close of the first tax year in which gain is realized** (§1033(a)(2)(B)). | `=DATE(YEAR(B)+E,12,31)`. This assumes the gain is realized in the event year; override it if not. |
| 18. NUA & IRD | IRD rows reuse the NUA formula (Box 1 - Box 6). | `IRA value - estate tax` is not a §691(c) deduction. | The IRD deduction is (estate tax with IRD - estate tax without IRD) x the share of IRD received this year. Type the value into column E for IRD rows. |

## Wording and citation items
* **Tab 13:** cites §469(g). A trust's distribution of a passive activity falls under **§469(j)(12)**: suspended losses are added to basis and are not deductible. §469(g) covers fully taxable dispositions, where the losses *are* deductible. The title has been updated.
* **Tab 8:** the 110% prior-year test uses PY AGI > $150,000. For MFS the threshold is $75,000, so override E16 for MFS clients.
* **START HERE, "22 workflows":** the map lists 23 numbered tabs (2-24). Tab 2 is the log, so 22 calculation tabs is correct.

## Things the workbook can't do on its own (handled in each client's pack)
* It has no tab for the **SSTB flag**, **NIIT line 5c**, the **state-refund tax-benefit rule**, **PTE tax routing**,
  **IP PIN/e-file blockers**, or **forms the software doesn't support** (Form 3520, 8865, 1042-S on a 1040). These are logged on the Diagnostics Log
  (tab 2) as "log-only" items, and on the added **ProConnect Exceptions** tab.
