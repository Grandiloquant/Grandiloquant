# EVG1022 - Gregory & Ellen Whitfield - 2025 Software Exceptions (CCH Axcess & Intuit ProConnect)

*Synthetic training data - Project Evergreen v2. Companion workbook: `EVG1022_2025_Software_Exception_Workbook.xlsx` (firm's corrected CCH Axcess Exception Workbook, filled in).*

A new client with a retiring mobile executive. Almost everything here is **silent** in both packages: the software calculates
exactly what the documents say, and the documents are incomplete or misleading - a W-2 that codes 100% of wages to Pennsylvania,
a 1099-B that cannot see a spouse's IRA purchase, a 1099-R whose box 6 is easy to skip, a consolidated 1099 whose accrued interest
lives only on a supplemental page, and a prior preparer's capital loss carryover with the wrong character. Neither CCH Axcess nor
ProConnect has a prior-year proforma for a new client, so every carryover is a manual entry. ProConnect's higher bundles
(Advanced/Elite) have the same form coverage - the tier changes return counts and users only.

| ID | Workbook tab | Exception | Axcess diagnostic? | Override amount | E-file impact |
|---|---|---|---|---:|---|
| EVG1022-SX1 | 23. Multi-State W-2 Days | Single PA-coded W-2 for a mobile executive - MA workday allocation | **silent** (no diagnostic) | 44,727 | None - PA and MA both e-filed |
| EVG1022-SX2 | 2. Diagnostics Log | NJ reciprocity and Illinois 30-day threshold - do NOT generate NJ/IL returns | **silent** (no diagnostic) | 0 | Avoids two unnecessary nonresident filings |
| EVG1022-SX3 | 7. Multi-State Allocation | PA resident credit (Schedule G-L) for MA tax - limited to PA tax on the MA income | **silent** (no diagnostic) | 1,373 | None |
| EVG1022-SX4 | 18. NUA & IRD Deduction | 401(k) lump sum with employer stock in kind - NUA (only cost basis taxable) | **silent** (no diagnostic) | 96,000 | None |
| EVG1022-SX5 | 17. Equity Comp & Wash Sales | Cross-account wash sale - spouse's IRA bought the same ETF (Rev. Rul. 2008-5) | **silent** (no diagnostic) | 18,000 | None (four transactions - no 8949 summary/PDF attachment needed) |
| EVG1022-SX6 | 14. Bond Interest & Premium | Bond premium (box 11/13) and accrued interest paid at purchase | **silent** (no diagnostic) | 3,768 | None |
| EVG1022-SX7 | 10. Capital Loss Carryover | New client - prior preparer's capital loss carryover had the wrong character | **silent** (no diagnostic) | 26,000 | None |
| EVG1022-SX8 | 8. Est. Tax Penalty (2210) | Form 2210 for a new client - prior-year tax not proforma'd | yes | 0 | None |
| EVG1022-SX9 | 2. Diagnostics Log | PA-40 classes differ from federal: box 16 compensation, no carryover, no wash-sale rule | **silent** (no diagnostic) | 47,000 | None |

## EVG1022-SX1 - Single PA-coded W-2 for a mobile executive - MA workday allocation

*Workbook tab:* 23. Multi-State W-2 Days  |  *Category:* State Allocation  |  *Manual calc:* Yes  |  *Amount:* $44,727  |  *Procedure doc:* SALT Implications - New State Filing Requirements

- **CCH Axcess by default:** The W-2 worksheet carries box 15/16 exactly as keyed: one PA row with $441,000 of state wages. Axcess has no work location data, so it produces only the PA resident return - no Massachusetts nonresident return and no MA-source wages.
- **Axcess diagnostic:** None - silent
- **Axcess fix:** Wages, Salaries, Tips (W-2) worksheet > state/local section: add a multi-state allocation row - MA wages $44,727 (410,000 x 18/165 workdays) - and activate the MA nonresident return (Form 1-NR/PY). Keep the PA row at box 16 ($441,000; PA taxes residents on all compensation). Verify field path in current release.
- **ProConnect by default:** Same - the W-2 screen's state section reflects only what is keyed; with one PA row only PA is generated.
- **ProConnect fix:** Wages, Salaries, Tips > W-2 > State and local information: add a second state line for MA with state wages $44,727 (state withholding 0) and generate the MA nonresident return (screen/field per current release - verify).
- **E-file impact:** None - PA and MA both e-filed
- **Return lines affected:** MA 1-NR/PY (MA-source wages), PA-40 Schedule G-L
- **Notes:** Workdays from the Outlook export: PA 112, NJ 22, MA 18, IL 13 = 165 (4 holidays + 4 PTO excluded). Massachusetts uses the working-day ratio for nonresident employees.

## EVG1022-SX2 - NJ reciprocity and Illinois 30-day threshold - do NOT generate NJ/IL returns

*Workbook tab:* 2. Diagnostics Log  |  *Category:* State Allocation  |  *Manual calc:* No  |  *Amount:* $0  |  *Procedure doc:* SALT Implications - New State Filing Requirements

- **CCH Axcess by default:** If the preparer allocates by days to every state on the log (adds NJ and IL W-2 state rows), Axcess generates an NJ-1040NR and an IL-1040 with Schedule NR and pushes resident credits to the PA return. Nothing in the software knows the PA-NJ reciprocal agreement or the Illinois 30-working-day nonresident employee threshold.
- **Axcess diagnostic:** None - silent
- **Axcess fix:** No NJ or IL state rows on the W-2 worksheet; leave the NJ/IL returns inactive. Document on the Diagnostics Log and tab 23 notes: NJ 22 days - reciprocity (PA only); IL 13 days <= 30 - not IL-source (assumption to verify; IL tax at stake about $1,599).
- **ProConnect by default:** Same - any state line keyed on the W-2 generates that state's nonresident return.
- **ProConnect fix:** Do not add NJ/IL lines on the W-2 screen; if a state was activated, delete it in the state return list (screen per current release - verify).
- **E-file impact:** Avoids two unnecessary nonresident filings
- **Return lines affected:** PA-40 Schedule G-L
- **Notes:** Workbook tab 23 note column records both rules.

## EVG1022-SX3 - PA resident credit (Schedule G-L) for MA tax - limited to PA tax on the MA income

*Workbook tab:* 7. Multi-State Allocation  |  *Category:* State Allocation  |  *Manual calc:* Yes  |  *Amount:* $1,373  |  *Procedure doc:* SALT Implications

- **CCH Axcess by default:** When the MA tax paid is keyed as the 'tax paid to other state' on the PA credit input without the MA income, or the credit is overridden to the MA tax, the full $2,191 is credited. PA limits the credit to the PA tax on the income taxed by MA.
- **Axcess diagnostic:** None - silent
- **Axcess fix:** PA return > Resident credit (Schedule G-L) input: income taxed by MA $44,727, MA tax $2,191; credit = MIN(2,191, 44,727 x 3.07% = 1,373) = $1,373 (override if the default differs). Tab 7 column G = PA tax before credit $17,821; column B = PA taxable income $580,485 so G x D = PA tax on the MA income. Verify field path in current release.
- **ProConnect by default:** Same - the PA credit for taxes paid to other states uses the income and tax entered for the other state.
- **ProConnect fix:** Pennsylvania return > Credits > Credit for taxes paid to other states (Schedule G-L): MA income 44,727, MA tax 2,191; confirm the computed credit is $1,373 (screen/field per current release - verify).
- **E-file impact:** None
- **Return lines affected:** PA-40 line 22, Schedule G-L
- **Notes:** Used the income MA actually taxed (box 1 based) rather than PA-measured wages incl. 401(k) deferrals - conservative.

## EVG1022-SX4 - 401(k) lump sum with employer stock in kind - NUA (only cost basis taxable)

*Workbook tab:* 18. NUA & IRD Deduction  |  *Category:* Other  |  *Manual calc:* Yes  |  *Amount:* $96,000  |  *Procedure doc:* Client IRAs / retirement distributions

- **CCH Axcess by default:** Axcess taxes the 1099-R box 2a amount keyed. If the stock distribution is keyed with box 2a = box 1 ($640,000) or 'taxable amount not determined', and box 6 is skipped, the whole $640,000 is taxed on line 5b. With box 2a $96,000 keyed correctly the federal result is right - the risk is purely input.
- **Axcess diagnostic:** None - silent
- **Axcess fix:** Income > Pensions, IRAs (1099-R) worksheet: distribution 1 - gross $640,000, taxable $96,000, box 6 NUA $544,000, code 2, total distribution; distribution 2 - gross $780,000, taxable $0, code G (rollover). Tab 18: Box 1 - Box 6 = $96,000. Set up the 8,000 KMDV shares in the client's basis records at $12.00/share. PA: mark the 1099-R as not PA-taxable (retirement distribution after retirement) on the PA 1099-R input - verify field path in current release.
- **ProConnect by default:** Same - ProConnect taxes the taxable amount keyed; box 6 must be entered for the NUA to be carried.
- **ProConnect fix:** Income > Pensions, Annuities (1099-R): enter both 1099-Rs - box 2a $96,000 and box 6 net unrealized appreciation $544,000 on the stock distribution, code 2; the code G rollover with taxable $0 (field labels per current release - verify). PA: exclude from PA income on the PA 1099-R/retirement income input.
- **E-file impact:** None
- **Return lines affected:** 5a, 5b, PA-40
- **Notes:** Code 2 (separation from service in/after the year he turned 55) - no 10% tax, no Form 5329. Taxing the full FMV would cost $199,260 of additional federal tax (answer key what-if).

## EVG1022-SX5 - Cross-account wash sale - spouse's IRA bought the same ETF (Rev. Rul. 2008-5)

*Workbook tab:* 17. Equity Comp & Wash Sales  |  *Category:* Capital Loss  |  *Manual calc:* Yes  |  *Amount:* $18,000  |  *Procedure doc:* Schedule D - adjustment code W

- **CCH Axcess by default:** Schwab's 1099-B for Gregory's account shows the IVV sale with box 1g blank (the repurchase was in Ellen's IRA - a different owner and account). Autoflow/keying the 1099-B as reported deducts the $18,000 loss.
- **Axcess diagnostic:** None - silent
- **Axcess fix:** Gains and Losses > Capital Gains and Losses (Form 8949) - IVV line: adjustment code W, adjustment amount +$18,000 (loss disallowed). Do NOT increase any basis (IRA purchase - the loss is permanently lost).
- **ProConnect by default:** Same - the disposition is imported/keyed as reported; nothing cross-matches other accounts or a spouse's IRA.
- **ProConnect fix:** Dispositions (Schedule D/4797) > the IVV transaction: adjustment code W, adjustment +18,000 (field labels per current release - verify). No basis entry elsewhere.
- **E-file impact:** None (four transactions - no 8949 summary/PDF attachment needed)
- **Return lines affected:** 7, Form 8949 box A
- **Notes:** Evidence: Ellen's 02/24 email + Schwab IRA ****8831 Q4 statement (buy 420 sh IVV 11/20/2025).

## EVG1022-SX6 - Bond premium (box 11/13) and accrued interest paid at purchase

*Workbook tab:* 14. Bond Interest & Premium  |  *Category:* Other  |  *Manual calc:* Yes  |  *Amount:* $3,768  |  *Procedure doc:* Schedule B - accrued interest; Scan - consolidated 1099

- **CCH Axcess by default:** Scan/autoflow of the composite 1099 picks up box 1 ($12,640.55) and box 8 ($7,500). The accrued interest paid ($2,981.94) appears only on Schwab's supplemental page and the trade confirm - no 1099 box - so it is never reversed. If box 11/13 are not captured in their fields, no ABP adjustment is made and line 2a stays at $7,500.
- **Axcess diagnostic:** None - silent
- **Axcess fix:** Interest Income (1099-INT) worksheet: box 11 bond premium $786.12 and box 13 $1,104.30 in their fields (ABP adjustment line on Schedule B; line 2a $6,396); add a separate line 'Accrued interest' -$2,981.94. Line 2b $9,085.
- **ProConnect by default:** Same - the accrued interest is not on a 1099 box; box 11/13 must be keyed to be netted.
- **ProConnect fix:** Income > Interest Income (1099-INT): enter box 11 and box 13 premium amounts in their fields and the accrued interest as an adjustment line/'Accrued interest' (screen/field per current release - verify).
- **E-file impact:** None
- **Return lines affected:** 2a, 2b
- **Notes:** Override amount = 786.12 + 2,981.94 reduction of taxable interest.

## EVG1022-SX7 - New client - prior preparer's capital loss carryover had the wrong character

*Workbook tab:* 10. Capital Loss Carryover  |  *Category:* Capital Loss  |  *Manual calc:* Yes  |  *Amount:* $26,000  |  *Procedure doc:* General Return Prep Notes

- **CCH Axcess by default:** No proforma for a new client. Keying the prior preparer's worksheet ($38,000 long-term) is accepted without question; Axcess then nets the $5,000 short-term gain as ordinary income.
- **Axcess diagnostic:** None - silent
- **Axcess fix:** Gains and Losses > Capital Loss Carryovers: short-term $26,000, long-term $12,000 (recomputed from the 2024 Schedule D: ST (29,000), LT (12,000), $3,000 allowed absorbs ST first). Tax $1,000 lower than the all-LT version.
- **ProConnect by default:** Same - carryovers for a new client are manual entries; ProConnect uses whatever character is keyed.
- **ProConnect fix:** Schedule D input > Capital loss carryover: short-term 26,000, long-term 12,000 (screen/field per current release - verify).
- **E-file impact:** None
- **Return lines affected:** 7, 16, Schedule D lines 6/14
- **Notes:** Workbook tab 10 (corrected formulas): D16 26,000 / D17 12,000.

## EVG1022-SX8 - Form 2210 for a new client - prior-year tax not proforma'd

*Workbook tab:* 8. Est. Tax Penalty (2210)  |  *Category:* Est. Tax Penalty  |  *Manual calc:* Yes  |  *Amount:* $0  |  *Procedure doc:* Workpapers / Responding to Review Points

- **CCH Axcess by default:** Axcess computes Form 2210 from the prior-year tax and AGI it has. For a new client those fields are blank unless keyed, so the 110%-of-prior-year safe harbor is not available to the calculation; front-loaded withholding is treated as paid evenly by default.
- **Axcess diagnostic:** Penalty/2210 informational message may appear for missing prior-year data - verify; otherwise silent
- **Axcess fix:** General > Payments > Penalties and Interest (Form 2210): 2024 tax $164,982, 2024 AGI $669,300; estimates by date (4 x $8,000 timely). Required annual payment = lesser of 90% of 2025 tax $126,067 or 110% of 2024 tax $181,480 -> $126,067; paid $137,769 (each quarter covered) -> no penalty, no override.
- **ProConnect by default:** Same - prior-year tax/AGI for Form 2210 must be entered for a new client.
- **ProConnect fix:** Payments, Penalties & Extensions > Underpayment penalty (2210): enter prior-year tax and AGI; estimates with dates (screen/field per current release - verify).
- **E-file impact:** None
- **Return lines affected:** 38

## EVG1022-SX9 - PA-40 classes differ from federal: box 16 compensation, no carryover, no wash-sale rule

*Workbook tab:* 2. Diagnostics Log  |  *Category:* State Allocation  |  *Manual calc:* Yes  |  *Amount:* $47,000  |  *Procedure doc:* SALT Implications

- **CCH Axcess by default:** The PA return starts from federal data. Unless PA adjustments are made: compensation may be pulled from federal box 1 instead of box 16 (PA taxes 401(k)/403(b) deferrals); the federal capital loss carryover and the code W disallowance can flow into PA net gains; the $96,000 taxable 1099-R can be treated as PA income.
- **Axcess diagnostic:** None - silent
- **Axcess fix:** PA return inputs: compensation = W-2 box 16 ($506,000); PA net gains = 2025 sales only $47,000 (no PA carryover; IVV loss allowed - PA has no wash-sale provision, verify); 1099-R marked non-PA-taxable (retirement). PA taxable income $580,485, tax $17,821. Verify field paths in current release.
- **ProConnect by default:** Same risk - PA adjustments to federal amounts are separate state inputs.
- **ProConnect fix:** Pennsylvania return > income class adjustments: PA compensation from box 16; PA gains adjustment to remove the carryover and the code W adjustment; 1099-R PA exclusion (screen/field per current release - verify).
- **E-file impact:** None
- **Return lines affected:** PA-40 lines 1a, 5
- **Notes:** PA wash-sale treatment is an assumption flagged for the signer (PA tax effect $553).

