# EVG1018 - Elena Vasquez - 2025 Software Exceptions (CCH Axcess & Intuit ProConnect)

*Synthetic training data - Project Evergreen v2. Companion workbook: `EVG1018_2025_Software_Exception_Workbook.xlsx` (firm's corrected CCH Axcess Exception Workbook, filled in).*

Two K-1s that are each wrong or incomplete as issued. Bayline's 1120-S omitted the IRC 311(b) gain on the truck it
distributed, so the K-1 must be entered differently from the form (with Form 8082) - and everything downstream (basis,
QBI) then has to be overridden consistently. The grandmother's trust's FINAL K-1 reports suspended passive losses in a
footnote that neither package can deduct and neither package tracks as a basis increase. All five items are silent.

| ID | Workbook tab | Exception | Axcess diagnostic? | Override amount | E-file impact |
|---|---|---|---|---:|---|
| EVG1018-SX1 | 2. Diagnostics Log | S corp K-1 omits the IRC 311(b) gain on the distributed truck - report inconsistently with Form 8082 | **silent** (no diagnostic) | 20,000 | Form 8082 attached (e-file compatible) |
| EVG1018-SX2 | 12. S-Corp Dual Basis | Form 7203 ordering with a property distribution - gain first, distribution at FMV | **silent** (no diagnostic) | 72,000 | None (Form 7203 attached) |
| EVG1018-SX3 | 2. Diagnostics Log | QBI from K-1 Statement A omits the 1245 recapture; reduce for 2% shareholder health insurance | **silent** (no diagnostic) | 14,840 | None |
| EVG1018-SX4 | 13. Trust Termination PAL | Trust's final K-1: $18,400 suspended passive losses are a basis step-up, not a deduction | **silent** (no diagnostic) | 18,400 | None |
| EVG1018-SX5 | 2. Diagnostics Log | 2% shareholder health insurance in W-2 box 14 - deduction needs its own input | **silent** (no diagnostic) | 7,800 | None |

## EVG1018-SX1 - S corp K-1 omits the IRC 311(b) gain on the distributed truck - report inconsistently with Form 8082

*Workbook tab:* 2. Diagnostics Log  |  *Category:* Other  |  *Manual calc:* Yes  |  *Amount:* $20,000  |  *Procedure doc:* Schedules K-1

- **CCH Axcess by default:** Entering the K-1 as issued (box 1 $62,000; box 16D property distribution at book value $12,000) gives no gain. Axcess has no way to know the corporation distributed appreciated property.
- **Axcess diagnostic:** None - silent
- **Axcess fix:** Income/Deductions > S Corporation Passthrough: box 1 ordinary income $82,000 (62,000 + 1245 recapture 20,000 = FMV 32,000 - adjusted basis 12,000; accumulated depreciation 33,000 > gain); property distribution at FMV $32,000 (16D total $72,000). Prepare Form 8082 (inconsistent treatment) identifying box 1 and 16D; e-file compatible. Gulfside agreed 09/02/2026 to amend the 1120-S (follow-up 11/15/2026).
- **ProConnect by default:** Same - ProConnect uses the K-1 amounts entered; Form 8082 must be added for the inconsistent position.
- **ProConnect fix:** S Corp Info (1120S K-1): ordinary income 82,000; distributions 72,000 (property at FMV); add Form 8082 (screen per current release - verify).
- **E-file impact:** Form 8082 attached (e-file compatible)
- **Return lines affected:** 8 (Schedule 1 line 5), Schedule E Part II, Form 8082
- **Notes:** IRC 311(b) / 1371(a): the corporation is treated as selling the property at FMV; Elena's basis in the truck = $32,000 (301(d)).

## EVG1018-SX2 - Form 7203 ordering with a property distribution - gain first, distribution at FMV

*Workbook tab:* 12. S-Corp Dual Basis  |  *Category:* Basis/At-Risk/Passive  |  *Manual calc:* Yes  |  *Amount:* $72,000  |  *Procedure doc:* Schedules K-1 - S corp basis

- **CCH Axcess by default:** With the K-1 as issued the basis worksheet reduces stock basis by the book value ($12,000) and never adds the 311(b) gain; if only the distribution is corrected to FMV without the gain, a phantom excess-distribution capital gain can appear. Both are silent results of the inputs.
- **Axcess diagnostic:** None - silent
- **Axcess fix:** S Corporation Passthrough > Basis Limitation section: beginning stock basis $95,000 (debt basis $0); increases $83,150 (box 1 82,000 incl. gain + interest 1,150) -> $178,150; distributions at FMV $72,000 (cash 40,000 + truck 32,000) -> no excess; then nondeductible expenses and charitable item -> ending $101,750. Form 7203 attached.
- **ProConnect by default:** Form 7203 is produced because there is a distribution; ProConnect requires 'Stock basis at beginning of year' (diagnostic ref 56844 if missing).
- **ProConnect fix:** S Corp Info (1120S K-1) > Shareholder's Basis (7203): stock basis at beginning of year 95,000; distributions 72,000 (at FMV); confirm no gain and ending basis 101,750. *(ref: Intuit help: 'How to complete Form 7203 and resolve diagnostic 56844 in ProConnect Tax')*
- **E-file impact:** None (Form 7203 attached)
- **Return lines affected:** Form 7203, Schedule D (none)

## EVG1018-SX3 - QBI from K-1 Statement A omits the 1245 recapture; reduce for 2% shareholder health insurance

*Workbook tab:* 2. Diagnostics Log  |  *Category:* Other  |  *Manual calc:* Yes  |  *Amount:* $14,840  |  *Procedure doc:* QBI (QOFs, QROFs)

- **CCH Axcess by default:** Section 199A amounts come from the K-1 Statement A input (QBI $62,000), which does not change when box 1 is overridden to $82,000. The QBI reduction for the Schedule 1 line 17 deduction attributable to the S corp must also be reflected (verify whether the current release applies it automatically).
- **Axcess diagnostic:** None - silent
- **Axcess fix:** S Corporation Passthrough > Section 199A: QBI $82,000 (1245 recapture is ordinary trade-or-business income) less 2% shareholder health deduction $7,800 = $74,200; W-2 wages $310,000 / UBIA $180,000 (not limiting - TI before QBI $149,250 < $197,300). Deduction 20% = $14,840.
- **ProConnect by default:** Same - QBI comes from the 199A fields entered from Statement A.
- **ProConnect fix:** S Corp Info (1120S K-1) > Qualified Business Income (199A): QBI 82,000; confirm the SE health insurance adjustment reduces QBI to 74,200 (field per current release - verify).
- **E-file impact:** None
- **Return lines affected:** 13a, Form 8995

## EVG1018-SX4 - Trust's final K-1: $18,400 suspended passive losses are a basis step-up, not a deduction

*Workbook tab:* 13. Trust Termination PAL  |  *Category:* Basis/At-Risk/Passive  |  *Manual calc:* Yes  |  *Amount:* $18,400  |  *Procedure doc:* Schedules K-1 - trust final K-1

- **CCH Axcess by default:** If the footnote's suspended PAL ($18,400) is keyed as a final-year deduction or a Schedule E loss on the K-1 (1041) input, Axcess deducts it. Axcess has no field that adds it to the basis of the distributed condo - that basis lives outside the return until the property is placed in service.
- **Axcess diagnostic:** None - silent
- **Axcess fix:** K-1 (Form 1041) input: enter only interest $420, dividends $1,380 ($1,100 qualified) and box 11 code E LT capital loss carryover $3,200 (Schedule D line 14; $200 carries to 2026). No PAL deduction (IRC 469(j)(12)). Record condo basis $222,546 + $18,400 = $240,946 in PERM; 2026 Rental input: continue trust's 27.5-yr schedule on carryover building basis $174,546 and add the $14,431 increase as a new asset (assumption flagged).
- **ProConnect by default:** Same - suspended losses from a trust footnote are not deductible and must not be entered as a K-1 loss.
- **ProConnect fix:** Trust K-1 (1041) input: no passive loss entry; Schedule D capital loss carryover 3,200 via the K-1 final-year field; basis memo for the 2026 rental asset entries (screen/field per current release - verify).
- **E-file impact:** None
- **Return lines affected:** Schedule E (no loss), Schedule D line 14, PERM basis record
- **Notes:** Use only the FINAL K-1 (08/21/2026); the June DRAFT ($410 interest) is superseded.

## EVG1018-SX5 - 2% shareholder health insurance in W-2 box 14 - deduction needs its own input

*Workbook tab:* 2. Diagnostics Log  |  *Category:* Other  |  *Manual calc:* No  |  *Amount:* $7,800  |  *Procedure doc:* Schedules K-1 - 2% shareholder fringe benefits

- **CCH Axcess by default:** W-2 box 14 text ('2% SH HLTH 7,800') is informational; nothing flows to Schedule 1 line 17 from it. Without the separate self-employed health insurance entry linked to the S corp, the premiums stay taxed as wages.
- **Axcess diagnostic:** None - silent
- **Axcess fix:** Adjustments > Self-Employed Health Insurance: $7,800, linked to Bayline (more-than-2% shareholder; premiums in box 1, not boxes 3/5 - confirmed). Limited to Bayline wages $90,000 (verify field path in current release).
- **ProConnect by default:** Same - box 14 amounts do not create the deduction by themselves.
- **ProConnect fix:** Adjustments to Income > Self-employed health insurance: 7,800, linked to the S corporation (field per current release - verify).
- **E-file impact:** None
- **Return lines affected:** 10 (Schedule 1 line 17)
- **Notes:** Notice 2008-1.

