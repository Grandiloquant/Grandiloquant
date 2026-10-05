# EVG1008 - Kevin & Samantha O'Brien - 2025 Software Exceptions (CCH Axcess & Intuit ProConnect)

*Synthetic training data - Project Evergreen v2. Companion workbook: `EVG1008_2025_Software_Exception_Workbook.xlsx` (firm's corrected CCH Axcess Exception Workbook, filled in).*

Two rentals: a long-term duplex (passive, fully suspended) and a cabin that became a sec. 280A residence because of 21 personal
days. Tab 5 documents the $25,000 allowance phase-out and the suspended loss; tab 16 the cabin's IRS-method allocation. The
silent items are the duplex 1098 (rental address) AutoFlowing to Schedule A, the roof coded as a repair in the client's ledger,
the day counts the vacation-home calculation depends on, and PA compensation/rents that do not follow the federal numbers.

| ID | Workbook tab | Exception | Axcess diagnostic? | Override amount | E-file impact |
|---|---|---|---|---:|---|
| EVG1008-SX1 | 2. Diagnostics Log | Duplex Form 1098 (box 8 = rental address) AutoFlowed to Schedule A; escrow summary imported as a second 1098 | **silent** (no diagnostic) | 9,860 | None |
| EVG1008-SX2 | 2. Diagnostics Log | Roof coded 'Repairs' in the client ledger; water heater de minimis; window repair | **silent** (no diagnostic) | 276 | De minimis election statement attached |
| EVG1008-SX3 | 5. Passive Activity (8582) | Form 8582: PY unallowed loss $6,200 not on the organizer; $25,000 allowance fully phased out | **silent** (no diagnostic) | 9,407 | None |
| EVG1008-SX4 | 16. Vacation Home Allocation | Cabin - sec. 280A residence: personal days must include the brother's free stay | **silent** (no diagnostic) | 0 | None |
| EVG1008-SX5 | 2. Diagnostics Log | PA-40: compensation from W-2 box 16 (401k/403b taxable) and rents loss stays in its class | **silent** (no diagnostic) | 189,300 | PA-40 e-filed with the federal return |

## EVG1008-SX1 - Duplex Form 1098 (box 8 = rental address) AutoFlowed to Schedule A; escrow summary imported as a second 1098

*Workbook tab:* 2. Diagnostics Log  |  *Category:* Other  |  *Manual calc:* No  |  *Amount:* $9,860  |  *Procedure doc:* Schedule E - Rental Properties (Form 1098 treated as personal)

- **CCH Axcess by default:** AutoFlow treats every Form 1098 as home mortgage interest: the duplex 1098 ($9,860 interest; $5,420 escrowed taxes) went to Schedule A, flipping the return to itemized ($41,825) and overstating the duplex result. The lender's escrow year-end summary was imported as another 1098 (duplicate).
- **Axcess diagnostic:** None - silent
- **Axcess fix:** Delete the Schedule A 1098 entries for the duplex and the escrow-summary record. Rental (Schedule E) Property A: mortgage interest $9,860 (line 12), taxes $5,420 (line 16). Itemized $26,545 < standard $31,500 -> standard.
- **ProConnect by default:** If the 1098 is entered on the itemized-deduction mortgage screen it is deducted on Schedule A; ProConnect does not read box 8.
- **ProConnect fix:** Enter the interest and taxes on the Rental & Royalty Income (Schedule E) screen for the duplex, not on the Schedule A mortgage interest screen (screen names per current release - verify). *(ref: Screen names per current release - verify)*
- **E-file impact:** None
- **Return lines affected:** 12e, Sch E 12, Sch E 16
- **Notes:** Box 7 'No' (not the borrower's residence) and box 8 address are the tells.

## EVG1008-SX2 - Roof coded 'Repairs' in the client ledger; water heater de minimis; window repair

*Workbook tab:* 2. Diagnostics Log  |  *Category:* Depreciation  |  *Manual calc:* No  |  *Amount:* $276  |  *Procedure doc:* Schedule E - capitalization of repairs vs improvements; de minimis election

- **CCH Axcess by default:** Rental expenses are keyed from the client's ledger by category, so the $14,000 full roof replacement lands on Schedule E line 14 as a repair. Axcess cannot distinguish a restoration of a building system from a repair, and applies the de minimis safe harbor only if the election is made.
- **Axcess diagnostic:** None - silent
- **Axcess fix:** Depreciation (Form 4562) for Property A: add 'Roof replacement' 06/2025, $14,000, residential rental 27.5-yr SL mid-month -> $276. Remove it from repairs. Water heater $1,900 on line 19 with the Reg. 1.263(a)-1(f) election statement (General > Elections / statement - verify); window $450 stays a repair. Small-taxpayer safe harbor not available (> 2% of $265,000 UBB).
- **ProConnect by default:** Same - expenses entered as repairs are deducted; capitalization is a preparer determination.
- **ProConnect fix:** Add the roof as a residential rental asset on the property's depreciation screen (27.5-yr, 06/2025); generate the de minimis election statement (screen/field per current release - verify). *(ref: Screen/field per current release - verify)*
- **E-file impact:** De minimis election statement attached
- **Return lines affected:** Sch E 14, Sch E 18, Form 4562
- **Notes:** Loss is suspended either way, but the basis and the suspended-loss carryforward would be wrong.

## EVG1008-SX3 - Form 8582: PY unallowed loss $6,200 not on the organizer; $25,000 allowance fully phased out

*Workbook tab:* 5. Passive Activity (8582)  |  *Category:* Basis/At-Risk/Passive  |  *Manual calc:* Yes  |  *Amount:* $9,407  |  *Procedure doc:* General Return Prep Notes - blank organizer line with PY amount (suspended passive loss)

- **CCH Axcess by default:** Axcess releases or suspends only the prior-year unallowed loss present on the activity's carryover input. The organizer was silent; if the 2024 carryover is not on the duplex activity (e.g., the property is re-keyed as a new activity from the scanned ledger) the $6,200 is silently lost.
- **Axcess diagnostic:** None - silent
- **Axcess fix:** Rental (Schedule E) Property A > passive carryover input: prior-year unallowed loss (regular) $6,200 per the 2024 Form 8582 / PERM (verify AMT carryover - same amount, no AMT preferences). MAGI $171,682 > $150,000 -> special allowance $0; 2025 loss ($3,207) also suspended -> $9,407 to 2026.
- **ProConnect by default:** Same - ProConnect uses the prior-year unallowed losses entered on the rental's Passive Losses tab.
- **ProConnect fix:** Rental & Royalty Income > Passive Losses tab: prior-year unallowed losses - Regular $6,200 and AMT $6,200 (enter both). Form 8582 generates automatically (or force: 1 = when applicable, 2 = force). *(ref: Intuit help: 'How to generate Form 8582 in ProConnect Tax'; community thread on prior years' unallowed losses)*
- **E-file impact:** None
- **Return lines affected:** Form 8582, Sch E 22
- **Notes:** The 9,407 carryforward is not listed in the answer key's carryforwards_to_2026 block (only in the gotchas/notes).

## EVG1008-SX4 - Cabin - sec. 280A residence: personal days must include the brother's free stay

*Workbook tab:* 16. Vacation Home Allocation  |  *Category:* Basis/At-Risk/Passive  |  *Manual calc:* Yes  |  *Amount:* $0  |  *Procedure doc:* Schedule E - personal use days (sec. 280A)

- **CCH Axcess by default:** Axcess's vacation-home limitation uses the personal-use and rental days entered. The draft keyed 18 personal days (family only) - under 18 days the cabin is still a residence (18 > 14), but the allocation % and the carryovers change; the first draft went further and keyed the cabin as a regular rental with a ~$7,000 loss. The software cannot know Pat's free nights are personal use or that the deck weekend was repair work.
- **Axcess diagnostic:** None - silent
- **Axcess fix:** Rental (Schedule E) Property B: type 1 (single family / vacation), fair rental days 62, personal use days 21 (18 family + 3 brother; 10/11-10/12 repair weekend excluded). IRS method 62/83 = 74.70%; rental income limit applies (Pub. 527 Worksheet 5-1): interest $6,200 + taxes $2,480 + direct $2,430 -> operating $3,770 of $4,030 -> depreciation $0 of $4,244. Net $0; carry forward operating $260 + depreciation $4,244. Personal share of interest $2,100 / taxes $840 to the Schedule A worksheet.
- **ProConnect by default:** Same - the vacation home limitation is computed from the days entered on the rental screen.
- **ProConnect fix:** Rental & Royalty Income: days rented at fair rental 62; personal use days 21; vacation home limitation applies (IRS method). Check the carryover of operating expenses and depreciation (screen/field per current release - verify). *(ref: Screen/field per current release - verify)*
- **E-file impact:** None
- **Return lines affected:** Sch E line 2, Sch E 21, Form 4562
- **Notes:** Bolton method (interest/taxes x 62/365) would free more operating expense; IRS method used per firm procedure - no 2025 tax difference (standard deduction). Not a passive activity (sec. 469(j)(10)) - no 8582 for the cabin.

## EVG1008-SX5 - PA-40: compensation from W-2 box 16 (401k/403b taxable) and rents loss stays in its class

*Workbook tab:* 2. Diagnostics Log  |  *Category:* State Allocation  |  *Manual calc:* No  |  *Amount:* $189,300  |  *Procedure doc:* SALT Implications - Pennsylvania

- **CCH Axcess by default:** The draft PA return used federal W-2 box 1 as PA compensation and netted the rents-class loss against wages. PA compensation must come from box 16 (elective deferrals are PA-taxable); if box 16 is blank or copied from box 1 on the W-2 input, the PA return understates compensation with no diagnostic.
- **Axcess diagnostic:** None - silent
- **Axcess fix:** W-2 inputs: PA state wages (box 16) $189,300 combined. PA rents class: duplex ($3,207) + cabin (PA - no sec. 280A limit assumed) = loss ($7,711) - not netted against compensation (PA Schedule E / class-netting input - verify). PA taxable income $189,682 x 3.07% = $5,823; withheld $5,812 -> due $11.
- **ProConnect by default:** Same - PA compensation follows the state wages entered on the W-2 screen.
- **ProConnect fix:** W-2 screen: PA state wages = box 16; PA return rents class shows the loss with no offset (screen/field per current release - verify). *(ref: Screen/field per current release - verify)*
- **E-file impact:** PA-40 e-filed with the federal return
- **Return lines affected:** PA-40 line 1a, PA-40 line 6
- **Notes:** Local Manheim Twp EIT final return filed separately with LCTCB (not in either package's 1040 workflow).

