# EVG1022 - Software exception log (CCH Axcess / ProConnect)

| ID | Workbook tab | Exception | Silent? | Amount | Axcess fix (input/override location) | ProConnect fix | E-file impact |
|---|---|---|---|---:|---|---|---|
| 1 | 17 Equity comp basis & cross-account wash sales | IVV loss disallowed by spouse's IRA purchase - Schwab 1099-B shows no W | Yes - silent | 18,000 | Income > Dispositions (8949) - IVV line: adjustment code W, amount 18,000 (verify field path in current release) | Schedule D/4797 screen - adjustment code W / amount (screen/field per current release - verify) | None; 8949 box A detail line |
| 2 | 10 Capital loss carryover (new clients) | Prior preparer's carryover all LT; correct ST 26,000 / LT 12,000 | Yes - silent | 38,000 | Income > Carryovers - ST and LT capital loss carryover fields (verify) | Carryover screen - ST/LT fields (verify) | None |
| 3 | 14 Bond accrued interest & premium | Accrued interest paid (supplemental page, not on 1099) and box 11/13 premium need netting | Partly - accrued interest silent | 2,981.94 / 786.12 / 1,104.30 | Interest input: "Accrued interest" and "ABP adjustment" subtraction lines on Schedule B; tax-exempt amount net of box 13 (verify) | 1099-INT screen adjustment fields (verify) | None |
| 4 | 18 NUA & IRD | 1099-R box 6 NUA 544,000; taxable 96,000; code 2 | No (flows from 1099-R if box 6 keyed) | 544,000 | 1099-R input: box 2a 96,000, box 6 544,000, code 2; mark total distribution (verify) | 1099-R screen (verify) | None |
| 5 | 23 Multi-state W-2 workdays | W-2 box 16 100% PA; 18 MA workdays | Yes - silent | 48,109 MA wages | State > W-2 state allocation: add MA line, wages 48,109.09, withholding 0; or MA nonresident allocation worksheet by days 18/165 (verify) | State W-2 allocation (verify) | MA 1-NR/PY e-file |
| 6 | 7 Multi-state allocation & resident credit | PA Schedule G-L credit for MA tax | Partly | 1,476.95 | PA > Credit for taxes paid to other states (verify) | PA credit screen (verify) | None |
| 7 | 8 Form 2210 safe harbor | ES payment dates (Q4 paid 01/15/2026) must be keyed | No | 32,000 | Payments > Federal estimates with actual dates (verify) | Estimates screen (verify) | None - no penalty |
| 8 | Log-only (tab 2) | NIIT line 9b state tax allocation - software default is 0 | Yes - silent | 592.48 | Form 8960 line 9b override (verify) | 8960 screen (verify) | None |
| 9 | Log-only (tab 2) | PA differences: PA Turnpike exempt; no wash sale disallowance/carryover for PA; 401(k) excluded; no PA premium amortization | Yes - silent | see state WP | PA modifications/override fields (verify) | PA screens (verify) | None |
| 10 | Log-only (tab 2) | Local EIT final return (Keystone Collections) - prepared outside the 1040 package; PSD code question | n/a | 5,060 | Prepare outside / local module if licensed (verify) | n/a | Separate filing |

1. **Wash sale (silent).** Software imports the Schwab 1099-B and allows the $18,000 loss; it cannot see Ellen's IRA purchase. Rev. Rul. 2008-5 disallows permanently.
2. **Carryover (silent).** A new-client proforma will take the $38,000 LT from the prior preparer; correct character per the Capital Loss Carryover Worksheet is ST 26,000 / LT 12,000.
3. **Bond.** Box 1 imports gross 12,640.55; the accrued interest is only on the supplemental page and won't flow. Box 11 imports but confirm an ABP subtraction is generated.
4. **NUA.** Flows correctly if box 6 and code 2 are keyed; note for PA exclusion.
5. **MA workdays (silent).** Without a manual allocation the software produces no MA income because box 15/16 list only PA.
8. **NIIT 9b.** Default 0 - minor ($22 tax).
