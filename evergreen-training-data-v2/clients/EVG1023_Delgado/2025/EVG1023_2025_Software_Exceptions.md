# EVG1023 - Raymond & Carla Delgado - 2025 Software Exceptions (CCH Axcess & Intuit ProConnect)

*Synthetic training data - Project Evergreen v2. Companion workbook: `EVG1023_2025_Software_Exception_Workbook.xlsx` (firm's corrected CCH Axcess Exception Workbook, filled in).*

Three partnerships, a rental fire and a foreign partnership - and a new client, so neither package has a proforma of basis,
at-risk or passive carryovers. Every limitation here is input-driven: CCH Axcess and ProConnect apply basis, at-risk and passive
rules only to the extent the preparer supplies beginning basis, the at-risk character of each liability, and prior-year unallowed
losses (separately for regular tax and AMT). Two items have no input at all - the IRC 704(c)(1)(B) gain hidden in a K-1 footnote and
the IRC 1033 replacement deadline - and must be calculated off-system (workbook tabs 11 and 21). Form 8865 cannot be produced in
ProConnect at any subscription tier (Advanced/Elite bundles change return counts and users, not form coverage).

| ID | Workbook tab | Exception | Axcess diagnostic? | Override amount | E-file impact |
|---|---|---|---|---:|---|
| EVG1023-SX1 | 3. K-1 Basis Limitation | Catawba River Outfitters - loss exceeds outside basis (guaranteed payments don't add basis) | **silent** (no diagnostic) | 30,000 | None |
| EVG1023-SX2 | 4. At-Risk (Form 6198) | At-risk: nonrecourse seller financing on equipment is not qualified nonrecourse financing | **silent** (no diagnostic) | -2,000 | None (Form 6198 attached) |
| EVG1023-SX3 | 9. AMT Adjustments (6251) | K-1 box 17A +$6,000 on a loss that is limited by basis/at-risk - Form 6251 line 2n = 0 | **silent** (no diagnostic) | 0 | None |
| EVG1023-SX4 | 11. Hot Assets & Mixing Bowl | IRC 704(c)(1)(B) mixing-bowl gain disclosed only in a K-1 footnote | **silent** (no diagnostic) | 250,000 | Explanation statement attached (PDF) |
| EVG1023-SX5 | 11. Hot Assets & Mixing Bowl | IRC 752(b) deemed distribution - liability share 180,000 -> 95,000 | **silent** (no diagnostic) | -85,000 | None |
| EVG1023-SX6 | 5. Passive Activity (8582) | New client - Form 8582 prior-year unallowed losses (Regular vs AMT); LP gets no $25,000 | **silent** (no diagnostic) | 51,253 | None |
| EVG1023-SX7 | 6. Depreciation Overrides | NC decouples from bonus depreciation - 85% addback on Carla's $28,000 | **silent** (no diagnostic) | 23,800 | None |
| EVG1023-SX8 | 21. Involuntary Conv. 1033 | Rental duplex destroyed by fire - IRC 1033 election and replacement deadline | **silent** (no diagnostic) | 179,758 | Election statement attached (PDF) |
| EVG1023-SX9 | ProConnect-only | Form 8865 (Baja Coastal - Categories 3 and 4) is not available in ProConnect | **silent** (no diagnostic) | 0 | ProConnect: paper filing required (firm decision); Axcess: e-file |
| EVG1023-SX10 | 2. Diagnostics Log | Form 8938 - foreign partnership interest reported on Form 8865 still counts (excepted asset) | **silent** (no diagnostic) | 180,000 | None (Axcess); paper with the return if prepared in ProConnect |

## EVG1023-SX1 - Catawba River Outfitters - loss exceeds outside basis (guaranteed payments don't add basis)

*Workbook tab:* 3. K-1 Basis Limitation  |  *Category:* Basis/At-Risk/Passive  |  *Manual calc:* Yes  |  *Amount:* $30,000  |  *Procedure doc:* Schedules K-1 - partnership distributions/losses in excess of basis (Section 6 - apply the limitation)

- **CCH Axcess by default:** Without Section 6 (Basis Limitation) inputs, Axcess allows the full ($52,000) K-1 loss. If the preparer keys basis but adds the $95,000 guaranteed payment as an 'other increase', basis looks sufficient and the full loss is still allowed.
- **Axcess diagnostic:** None - silent
- **Axcess fix:** Income/Deductions > Partnership Passthrough > Catawba > Section 6 Basis Limitation: check 'apply the limitation'; beginning basis $30,000 (capital 2,000 + nonrecourse share 28,000); no increase for guaranteed payments. Allowed by basis $30,000; $22,000 suspended (704(d) carryover). Verify field path in current release.
- **ProConnect by default:** Same - ProConnect applies the partner basis limitation only when basis information is entered on the K-1 screen's basis worksheet.
- **ProConnect fix:** Partnership Information > Schedule K-1 (1065) > Basis Limitations / Partner's basis worksheet: beginning basis 30,000; enforce limitation (screen/field per current release - verify). Suspended 22,000 carries in the 704(d) carryover field.
- **E-file impact:** None
- **Return lines affected:** 8 (Sch E line 28), Sch E Part II
- **Notes:** Tab 3 also documents Lakewood: 296,000 + 250,000 (704(c)) - 85,000 (752(b)) = 461,000 before the 14,000 loss.

## EVG1023-SX2 - At-risk: nonrecourse seller financing on equipment is not qualified nonrecourse financing

*Workbook tab:* 4. At-Risk (Form 6198)  |  *Category:* Basis/At-Risk/Passive  |  *Manual calc:* Yes  |  *Amount:* $-2,000  |  *Procedure doc:* Schedules K-1

- **CCH Axcess by default:** Unless 'subject to at-risk limitation' is checked and the liability character is entered, Axcess treats the $30,000 that cleared basis as fully allowed. K-1 item K reports the $28,000 as 'nonrecourse' - Axcess cannot know it is equipment seller financing rather than qualified (real property) nonrecourse financing.
- **Axcess diagnostic:** None - silent
- **Axcess fix:** Partnership Passthrough > Catawba > Section 6 / At-Risk: check 'subject this entity to the at-risk limitation'; amount at risk $2,000 (basis 30,000 less nonrecourse non-QNF 28,000). Form 6198 allows $2,000; $28,000 suspended (Form 6198 carryover). Verify field path in current release.
- **ProConnect by default:** Same - Form 6198 is produced only when the at-risk box and at-risk amounts are entered.
- **ProConnect fix:** Schedule K-1 (1065) > At-Risk (6198) section: some investment is not at risk = Yes; amount at risk 2,000 (screen/field per current release - verify).
- **E-file impact:** None (Form 6198 attached)
- **Return lines affected:** 8, Form 6198, 13a
- **Notes:** IRC 465(b)(6) QNF is limited to the activity of holding real property; this is equipment. Tax effect of skipping tabs 3-4: $11,804.

## EVG1023-SX3 - K-1 box 17A +$6,000 on a loss that is limited by basis/at-risk - Form 6251 line 2n = 0

*Workbook tab:* 9. AMT Adjustments (6251)  |  *Category:* AMT  |  *Manual calc:* Yes  |  *Amount:* $0  |  *Procedure doc:* Schedules K-1

- **CCH Axcess by default:** Axcess carries the K-1 box 17A post-1986 depreciation adjustment to Form 6251 line 2l (+6,000) even though only $2,000 of the regular loss is allowed - unless the AMT basis/at-risk amounts are entered so the AMT allowed loss is recomputed.
- **Axcess diagnostic:** None - silent
- **Axcess fix:** AMT input for the Catawba K-1: AMT basis 30,000 and AMT at-risk 2,000 (AMT columns of the basis/at-risk worksheet); if the line still shows +6,000, use the 'Loss limits (Force)' line 2n override so the net AMT adjustment is $0 (regular allowed 2,000 = AMT allowed 2,000). Lakewood's +1,200 also nets to $0 (loss suspended). Verify field names.
- **ProConnect by default:** Same risk - AMT K-1 items flow to 6251 unless AMT limitation amounts are entered.
- **ProConnect fix:** Schedule K-1 (1065) > AMT / Basis and at-risk AMT amounts: enter AMT basis and AMT at-risk; confirm Form 6251 shows no net adjustment (screen/field per current release - verify).
- **E-file impact:** None
- **Return lines affected:** Form 6251 lines 2l/2n
- **Notes:** No AMT in 2025 either way, but the AMT suspended amounts carried forward depend on it.

## EVG1023-SX4 - IRC 704(c)(1)(B) mixing-bowl gain disclosed only in a K-1 footnote

*Workbook tab:* 11. Hot Assets & Mixing Bowl  |  *Category:* Basis/At-Risk/Passive  |  *Manual calc:* Yes  |  *Amount:* $250,000  |  *Procedure doc:* Schedules K-1 - hot assets / disproportionate distributions (mixing bowl)

- **CCH Axcess by default:** Axcess reads the K-1 boxes: box 9a = 0, box 2 (14,000). The $250,000 precontribution gain in footnote 3 is not in any box, so nothing is reported and outside basis is understated.
- **Axcess diagnostic:** None - silent
- **Axcess fix:** Partnership Passthrough > Lakewood: add $250,000 net long-term capital gain (K-1 Section 3 direct entry / box 9a override) with a statement explaining IRC 704(c)(1)(B); Section 6 Basis: other increase +250,000. Gain is NII and portfolio (not passive) income. Verify field path in current release.
- **ProConnect by default:** Same - ProConnect imports/keys K-1 boxes; a footnote amount must be entered manually.
- **ProConnect fix:** Schedule K-1 (1065) > Lakewood > Net long-term capital gain: 250,000 (adjusted from K-1 with explanation statement); basis worksheet other increase 250,000; ensure the gain is not treated as passive income (screen/field per current release - verify).
- **E-file impact:** Explanation statement attached (PDF)
- **Return lines affected:** 7, Sch D line 12, Form 8960
- **Notes:** Contributed 03/22/2021 (FMV 400,000, basis 150,000); distributed to another partner 08/14/2025 (< 7 years). Tax effect $44,094.

## EVG1023-SX5 - IRC 752(b) deemed distribution - liability share 180,000 -> 95,000

*Workbook tab:* 11. Hot Assets & Mixing Bowl  |  *Category:* Basis/At-Risk/Passive  |  *Manual calc:* Yes  |  *Amount:* $-85,000  |  *Procedure doc:* Schedules K-1

- **CCH Axcess by default:** If only the K-1 boxes are keyed, Axcess's basis worksheet does not reflect the $85,000 decrease in the partner's share of liabilities (item K) - basis is overstated going forward (no gain this year because basis is sufficient).
- **Axcess diagnostic:** None - silent
- **Axcess fix:** Section 6 Basis: beginning share of liabilities 180,000, ending 95,000 (or 'other decrease' 85,000 as a deemed cash distribution). Basis before loss 461,000; ending 447,000. No IRC 731 gain.
- **ProConnect by default:** Same - liability changes must be entered on the basis worksheet.
- **ProConnect fix:** Schedule K-1 (1065) > Partner's basis worksheet: beginning/ending liabilities (screen/field per current release - verify).
- **E-file impact:** None
- **Return lines affected:** K-1 basis worksheet

## EVG1023-SX6 - New client - Form 8582 prior-year unallowed losses (Regular vs AMT); LP gets no $25,000

*Workbook tab:* 5. Passive Activity (8582)  |  *Category:* Basis/At-Risk/Passive  |  *Manual calc:* Yes  |  *Amount:* $51,253  |  *Procedure doc:* Schedules K-1 / Schedule E

- **CCH Axcess by default:** No proforma: Axcess shows no prior-year unallowed loss for Lakewood unless keyed, and a single amount keyed only in the regular column leaves the AMT carryover blank (or equal to regular). The duplex is flagged active participation, but MAGI > $150,000 removes the allowance; if 'disposed of activity' is checked for the fire, Axcess releases the duplex loss although the IRC 1033 deferral means no fully taxable disposition.
- **Axcess diagnostic:** None - silent
- **Axcess fix:** Partnership Passthrough > Lakewood > Passive Activity carryovers: prior-year unallowed ordinary loss Regular 31,000, AMT 27,500; limited partner. Duplex rental: active participation, do NOT check disposed. Result: all passive losses suspended - Regular 51,253 / AMT 46,553 carried to 2026.
- **ProConnect by default:** ProConnect also has no prior-year data for a new client; prior-year unallowed losses must be entered per activity, with regular and AMT (operating) amounts entered separately; Form 8582 can be forced (1 = when applicable, 2 = force).
- **ProConnect fix:** Partnership K-1 (and Rental) > Passive Losses tab / prior years' unallowed losses: Regular 31,000 and AMT 27,500 for Lakewood; no disposition for the duplex; Form 8582 'when applicable'. *(ref: Intuit help: 'How to generate Form 8582 ... in ProConnect Tax'; Intuit Accountants Community thread on prior years' unallowed losses)*
- **E-file impact:** None
- **Return lines affected:** 8, Form 8582
- **Notes:** Tab 5 MAGI 423,527 -> special allowance $0 (corrected formulas).

## EVG1023-SX7 - NC decouples from bonus depreciation - 85% addback on Carla's $28,000

*Workbook tab:* 6. Depreciation Overrides  |  *Category:* Depreciation  |  *Manual calc:* Yes  |  *Amount:* $23,800  |  *Procedure doc:* SALT Implications

- **CCH Axcess by default:** Carla's bookkeeper's asset list is keyed on the Sch C as a summary depreciation figure (not in the Depreciation module), so no NC asset-level difference is computed and the D-400 shows no bonus addback.
- **Axcess diagnostic:** None - silent
- **Axcess fix:** Enter the three assets in the Depreciation module with NC treatment, or key the NC addition directly: NC > Additions > Bonus depreciation $23,800 (85% of 28,000); set up the 20% ($4,760) deduction for 2026-2030. Verify field path in current release; verify NC conformity for OBBBA 100% bonus.
- **ProConnect by default:** Same - the NC addback is computed only from asset entries with state depreciation; summary entries need a manual NC adjustment.
- **ProConnect fix:** Depreciation (4562) asset entries with state (NC) bonus treatment, or North Carolina > Additions > bonus depreciation 23,800 (screen/field per current release - verify).
- **E-file impact:** None
- **Return lines affected:** NC D-400 Schedule S, Form 4562
- **Notes:** Federal: 100% bonus (assets acquired 03-06/2025, after 01/19/2025) - bookkeeper's 40% replaced.

## EVG1023-SX8 - Rental duplex destroyed by fire - IRC 1033 election and replacement deadline

*Workbook tab:* 21. Involuntary Conv. 1033  |  *Category:* Other  |  *Manual calc:* Yes  |  *Amount:* $179,758  |  *Procedure doc:* Rare events / Tax Research

- **CCH Axcess by default:** Entering the casualty on Form 4684 Section B with proceeds $410,000 and basis $230,242 recognizes the $179,758 gain (Form 4797) unless the postponement election is made. Axcess keeps no multi-year ledger of the replacement deadline. The firm workbook's ORIGINAL formula (event date + 2 x 365) would show 01/24/2027 - wrong.
- **Axcess diagnostic:** None - silent
- **Axcess fix:** Gains and Losses > Casualties and Thefts (Form 4684 Section B): enter the conversion; election to postpone gain under IRC 1033 / gain postponed 179,758; attach election statement (property, date, proceeds, basis, intent to replace, deadline 12/31/2027). Tab 21 (corrected formula) tracks the deadline and replacement cost. Verify field path in current release.
- **ProConnect by default:** Same - the postponement must be elected on the casualty/disposition input; no deadline tracking.
- **ProConnect fix:** Dispositions > Casualties and Thefts (4684): business property, election to postpone gain (1033), amount postponed 179,758; attach the 1033 statement (screen/field per current release - verify).
- **E-file impact:** Election statement attached (PDF)
- **Return lines affected:** Form 4684, Form 4797, 7
- **Notes:** Replacement period = 2 years after the close of the first tax year in which any part of the gain is realized (2025) -> 12/31/2027; 3 years applies only to condemned real property.

## EVG1023-SX9 - Form 8865 (Baja Coastal - Categories 3 and 4) is not available in ProConnect

*Workbook tab:* ProConnect-only  |  *Category:* E-file Disqualifying  |  *Manual calc:* No  |  *Amount:* $0  |  *Procedure doc:* E-Filing / Paper Filing Returns; Foreign Transactions

- **CCH Axcess by default:** Form 8865 prepared in the Axcess 1040 foreign forms (verify availability in the firm's current release and license) and e-filed with the return.
- **Axcess diagnostic:** None - silent
- **Axcess fix:** n/a (firm e-filed from Axcess with Form 8865 Schedules O and P included).
- **ProConnect by default:** Form 8865 is not available in ProConnect Tax (or Lacerte). The software cannot generate it or include it in the 1040 e-file.
- **ProConnect fix:** Prepare Form 8865 outside ProConnect (IRS fillable PDF or software that supports it). Firm policy: when the 1040 is prepared in ProConnect, paper-file the complete return with Form 8865 attached (an e-filed return cannot carry the form). Report the Baja loss on Sch E/8582 as a passive partnership activity and list the interest on Form 8938 Part IV as reported on Form 8865. *(ref: Intuit Accountants Community / product discussions: Form 8865 is not available in Lacerte or ProConnect Tax)*
- **E-file impact:** ProConnect: paper filing required (firm decision); Axcess: e-file
- **Return lines affected:** Form 8865, Form 8938
- **Notes:** Penalty for failure to file Form 8865: $10,000 per form.

## EVG1023-SX10 - Form 8938 - foreign partnership interest reported on Form 8865 still counts (excepted asset)

*Workbook tab:* 2. Diagnostics Log  |  *Category:* Other  |  *Manual calc:* No  |  *Amount:* $180,000  |  *Procedure doc:* Foreign Transactions - FinCEN114/FBAR

- **CCH Axcess by default:** Nothing triggers Form 8938 from a Form 8865 entry; if 8938 is not opened, it is not produced. If it is opened, the preparer must list the 8865 interest as an excepted asset in Part IV rather than in Part VI.
- **Axcess diagnostic:** None - silent
- **Axcess fix:** Foreign > Form 8938: MFJ living in the US; Part IV - number of Forms 8865 = 1 (asset counted toward the threshold: max value $180,000, year-end $174,000 -> filing required). No FBAR. Verify field path in current release.
- **ProConnect by default:** ProConnect supports Form 8938 entry, but with no 8865 in the file nothing prompts it.
- **ProConnect fix:** Foreign Reporting > Form 8938: enter the excepted-asset information (screen/field per current release - verify).
- **E-file impact:** None (Axcess); paper with the return if prepared in ProConnect
- **Return lines affected:** Form 8938, Schedule B Part III

