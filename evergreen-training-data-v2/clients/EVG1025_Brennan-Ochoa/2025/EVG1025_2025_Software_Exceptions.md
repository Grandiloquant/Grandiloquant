# EVG1025 - Victor & Lena Brennan-Ochoa - 2025 Software Exceptions (CCH Axcess & Intuit ProConnect)

*Synthetic training data - Project Evergreen v2. Companion workbook: `EVG1025_2025_Software_Exception_Workbook.xlsx` (firm's corrected CCH Axcess Exception Workbook, filled in).*

Three shareholder-level stock events that no broker statement computes correctly (merger boot, a corporate liquidation reported
only on a 1099-DIV, and a constructive sale with no 1099-B), a CFC whose GILTI is taxed under a section 962 election that both
packages handle only through an outside computation, and a Form 1042-S that forces a paper return. The ProConnect tier does not
matter here - the Advanced/Elite bundles have the same form coverage as the other tiers; they only change return counts and users.

| ID | Workbook tab | Exception | Axcess diagnostic? | Override amount | E-file impact |
|---|---|---|---|---:|---|
| EVG1025-SX1 | 24. Rare-Event Log | Section 962 election - GILTI tax computed outside the 1040 engine, $2,286 on line 16 | **silent** (no diagnostic) | 2,286 | Return is paper filed anyway (see SX6); statement and pro-forma forms attached to the paper return |
| EVG1025-SX2 | 24. Rare-Event Log | Form 5471 (Cat 4/5), Form 8992 / 8993 and pro-forma Form 1118 - specialist workpaper, not the 1040 engine | yes | 400,000 | Attached to the paper return |
| EVG1025-SX3 | 22. Reorg, Liquidation, 1244 | Merger cash boot - exchange agent 1099-B: $300,000 proceeds, no basis, no acquisition date | yes | 300,000 | None (return paper filed for SX6) |
| EVG1025-SX4 | 22. Reorg, Liquidation, 1244 | VBO Holdings liquidation - 1099-DIV box 9 creates no Form 8949 line | **silent** (no diagnostic) | -35,000 | None |
| EVG1025-SX5 | 22. Reorg, Liquidation, 1244 | Constructive sale (IRC 1259) - short against the box with no 2025 1099-B | **silent** (no diagnostic) | 150,000 | None |
| EVG1025-SX6 | ProConnect-only | Form 1042-S withholding on a U.S. citizen's 1040 - paper filing required | **silent** (no diagnostic) | 3,600 | Paper filing required (ProConnect); firm policy paper in Axcess as well |
| EVG1025-SX7 | 2. Diagnostics Log | FBAR / Schedule B line 7a - CFC's Irish bank account (financial interest + signature authority) | **silent** (no diagnostic) | EUR 310,000 max | None (FBAR filed separately) |

## EVG1025-SX1 - Section 962 election - GILTI tax computed outside the 1040 engine, $2,286 on line 16

*Workbook tab:* 24. Rare-Event Log  |  *Category:* Other  |  *Manual calc:* Yes  |  *Amount:* $2,286  |  *Procedure doc:* Foreign Corps

- **CCH Axcess by default:** If the Form 8992 GILTI inclusion ($400,000) is entered as income, Axcess taxes it at individual ordinary rates with no section 250 deduction and no deemed-paid credit - about $125,391 more income tax. The 1040 engine does not compute the corporate-rate 962 tax or the IRC 960(d) credit.
- **Axcess diagnostic:** None - silent
- **Axcess fix:** International specialist workpaper (workbook tab 24): (400,000 + 57,143 gross-up) - 50% IRC 250 = 228,571.50 x 21% = 48,000 - 80% deemed-paid credit 45,714 = 2,286. Do not carry the 951A inclusion to Schedule 1 (not in AGI under the election - presentation assumption to verify). Enter 2,286 as additional tax included on Form 1040 line 16 with the 962 election statement and pro-forma 1120/1118 attached (Taxes > other tax / line 16 adjustment - verify field path in current release); document the override amount.
- **ProConnect by default:** ProConnect does not compute the section 962 tax; Form 1118 is not available.
- **ProConnect fix:** Practitioner workaround (verify): prepare the pro-forma 1120/1118/8992/8993 outside the software and enter the computed 962 tax on screen 45.3 (Other Taxes) through the 'Section 962 tax' adjustment. Community guidance describes it as a NEGATIVE adjustment where the inclusion has been entered as income, so that net tax equals the 962 computation. For this return the inclusion is not entered as income; confirm the sign convention so line 16 = regular tax 86,955 + 2,286 = 89,241 and attach the statement as a PDF. *(ref: Intuit Accountants Community thread on section 962 election / Form 8992 (practitioner workaround - verify))*
- **E-file impact:** Return is paper filed anyway (see SX6); statement and pro-forma forms attached to the paper return
- **Return lines affected:** 16, Line 16 statement, Form 8992, Form 8993
- **Notes:** Override amount documented per Intuit 'Using overrides and adjustments in ProConnect Tax'. Future PTEP distributions taxable under IRC 962(d) to the extent they exceed 962 tax paid.

## EVG1025-SX2 - Form 5471 (Cat 4/5), Form 8992 / 8993 and pro-forma Form 1118 - specialist workpaper, not the 1040 engine

*Workbook tab:* 24. Rare-Event Log  |  *Category:* Other  |  *Manual calc:* Yes  |  *Amount:* $400,000  |  *Procedure doc:* Foreign Corps

- **CCH Axcess by default:** The 1040 module prepares the information returns only from what is keyed into the 5471/8992/8993 inputs; the GILTI high-tax test, tested income, QBAI and the 962 deemed-paid credit (Form 1118 is a corporate form) are not computed from the Irish accountants' package.
- **Axcess diagnostic:** Completeness diagnostics only for keyed 5471/8992 inputs (gist - verify); the GILTI/962 amounts themselves are not tested
- **Axcess fix:** Key Form 5471 Categories 4 and 5 (Schedules C, E, F, H, I-1, J, P, Q, R, M) and Form 8992 Schedule A from the re-performed Kinsale & Murphy package (tested income 400,000; QBAI 0; tested foreign income taxes 57,143). Form 8993 and the pro-forma 1118 are part of the 962 statement (tab 24, row 2). No Form 926 (no 2025 transfers).
- **ProConnect by default:** Form 1118 is not available in ProConnect; practitioners prepare pro-forma 1120/1118/8992/8993 for the 962 election.
- **ProConnect fix:** Prepare the 962 pro-forma set outside ProConnect; whether ProConnect's Form 5471 output is adequate for Categories 4/5 is not relied on - verify in the current release or prepare 5471 in the firm's international software and attach to the paper return. *(ref: Intuit Accountants Community thread on section 962 election / Form 8992)*
- **E-file impact:** Attached to the paper return
- **Return lines affected:** Form 5471, Form 8992, Form 8993, Form 8938 Part IV
- **Notes:** Form 8938 also filed: CFC stock is a specified foreign financial asset, excepted because reported on Form 5471.

## EVG1025-SX3 - Merger cash boot - exchange agent 1099-B: $300,000 proceeds, no basis, no acquisition date

*Workbook tab:* 22. Reorg, Liquidation, 1244  |  *Category:* Capital Loss  |  *Manual calc:* Yes  |  *Amount:* $300,000  |  *Procedure doc:* Schedule D

- **CCH Axcess by default:** Axcess imports the 1099-B with blank basis and blank date acquired. Missing basis is treated as zero, so the gain is $300,000 - numerically right only by coincidence - but with no acquisition date the term is not established and the IRC 356 support is missing. The common manual 'fix' (basis 200,000 -> gain 100,000) is wrong.
- **Axcess diagnostic:** Possibly an informational missing-basis / date-acquired message (gist - verify); the $300,000 gain itself calculates without any IRC 356 check
- **Axcess fix:** Workbook tab 22 (Reorg Boot row): realized 1,000,000; recognized = lesser of boot or realized = 300,000; Clark -> capital. Capital Gains worksheet: date acquired 03/15/2012, basis 0 entered explicitly, long-term, box E, statement attached. Record Meridian basis 200,000 ($20/share) in the client's basis schedule.
- **ProConnect by default:** Same - blank basis treated as zero; term needs the acquisition date.
- **ProConnect fix:** Dispositions: enter the transaction with date acquired 03/15/2012, cost 0, long-term, box E, and attach the IRC 356 statement (screen/field per current release - verify).
- **E-file impact:** None (return paper filed for SX6)
- **Return lines affected:** 7, Form 8949 box E

## EVG1025-SX4 - VBO Holdings liquidation - 1099-DIV box 9 creates no Form 8949 line

*Workbook tab:* 22. Reorg, Liquidation, 1244  |  *Category:* Capital Loss  |  *Manual calc:* Yes  |  *Amount:* $-35,000  |  *Procedure doc:* Schedule D

- **CCH Axcess by default:** Box 9 (cash liquidation distributions) is informational on the dividend input - Axcess cannot know Victor's stock basis, so no gain/loss is computed. If keyed as box 1a it becomes an $85,000 dividend. Either way the $35,000 IRC 331 loss is missing.
- **Axcess diagnostic:** None - silent
- **Axcess fix:** Workbook tab 22 (Liquidation row). Capital Gains worksheet: VBO Holdings, Inc., acquired 05/09/2016, sold 11/14/2025, proceeds 85,000, cost 120,000 -> (35,000) LT, box F.
- **ProConnect by default:** Same - the 1099-DIV box 9 entry does not create a disposition.
- **ProConnect fix:** Dispositions: add the liquidation as a sale (proceeds 85,000, cost 120,000, LT, box F) (screen/field per current release - verify).
- **E-file impact:** None
- **Return lines affected:** 7, Form 8949 box F

## EVG1025-SX5 - Constructive sale (IRC 1259) - short against the box with no 2025 1099-B

*Workbook tab:* 22. Reorg, Liquidation, 1244  |  *Category:* Capital Loss  |  *Manual calc:* Yes  |  *Amount:* $150,000  |  *Procedure doc:* Schedule D

- **CCH Axcess by default:** Nothing is reported for 2025: the short sale is reported on a 1099-B only in 2026 when closed. Axcess has no information that a constructive sale occurred - $150,000 of 2025 gain is omitted. In 2026 the 1099-B will show unknown basis and the same gain would be taxed again.
- **Axcess diagnostic:** None - silent
- **Axcess fix:** Workbook tab 22 (Constructive Sale row). Capital Gains worksheet: Meridian 2,000 sh, acquired 03/15/2012 (tacked), transaction date overridden to the constructive-sale date 12/10/2025, proceeds 190,000, cost 40,000 -> 150,000 LT, box F. 2026 proforma note: basis of the 2,000 shares 190,000 (code B adjustment).
- **ProConnect by default:** Same - no 2025 document; nothing reported unless entered manually.
- **ProConnect fix:** Dispositions: enter the deemed sale (date sold 12/10/2025, proceeds 190,000, cost 40,000, LT, box F) with an explanatory statement; carry the $95/share basis to 2026 (screen/field per current release - verify).
- **E-file impact:** None
- **Return lines affected:** 7, Form 8949 box F

## EVG1025-SX6 - Form 1042-S withholding on a U.S. citizen's 1040 - paper filing required

*Workbook tab:* ProConnect-only  |  *Category:* E-file Disqualifying  |  *Manual calc:* No  |  *Amount:* $3,600  |  *Procedure doc:* Paper Filing Returns

- **CCH Axcess by default:** Axcess: verify MeF support for claiming Form 1042-S withholding on a Form 1040; firm policy is paper filing with the 1042-S copy attached. The dividends must be keyed as ordinary/qualified dividends (no 1099-DIV was issued).
- **Axcess diagnostic:** None - silent
- **Axcess fix:** Dividends input: Atlas Clearing 12,000 ordinary / 12,000 qualified; withholding input: 3,600 federal tax withheld from Form 1042-S -> line 25c (verify field path in current release). Mark the return for paper filing; attach the 1042-S.
- **ProConnect by default:** Form 1042-S is not supported in the e-file of Form 1040 (only 1040-NR supports 1042-S) - per Intuit, returns claiming 1042-S withholding must be paper filed.
- **ProConnect fix:** Enter the 1042-S dividends and withholding, suppress e-file and paper file the 1040 with a copy of the 1042-S attached. Client to give the broker a Form W-9. *(ref: Intuit help: e-file diagnostic Ref 47040/47039/47310 for Form 1042-S)*
- **E-file impact:** Paper filing required (ProConnect); firm policy paper in Axcess as well
- **Return lines affected:** 3a, 3b, 25c

## EVG1025-SX7 - FBAR / Schedule B line 7a - CFC's Irish bank account (financial interest + signature authority)

*Workbook tab:* 2. Diagnostics Log  |  *Category:* Other  |  *Manual calc:* No  |  *Amount:* EUR 310,000 max  |  *Procedure doc:* FinCEN114/FBAR

- **CCH Axcess by default:** Schedule B Part III and the FBAR are driven by the foreign-account questions and FBAR inputs; with no 1099 for the account the software has nothing to trigger them. The proforma (prior preparer) answer 'No' carries forward.
- **Axcess diagnostic:** None - silent
- **Axcess fix:** General > foreign accounts question: Yes; country Ireland. FBAR (FinCEN 114) filed separately through BSA E-Filing - AIB ****4471, max EUR 310,000, owner Ochoa Engineering Ltd. (Victor > 50% owner and signatory).
- **ProConnect by default:** Same - question-driven; ProConnect does not file the FBAR.
- **ProConnect fix:** Schedule B foreign account question = Yes / Ireland; FBAR filed through BSA E-Filing outside the return (screen/field per current release - verify).
- **E-file impact:** None (FBAR filed separately)
- **Return lines affected:** Sch B line 7a/7b, FinCEN 114
- **Notes:** Prior-year (2022-2024) FBARs not filed by the prior preparer - delinquent FBAR procedures (separate engagement).

