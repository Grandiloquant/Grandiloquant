# EVG1020 - Ashley Turner - 2025 Software Exceptions (CCH Axcess & Intuit ProConnect)

*Synthetic training data - Project Evergreen v2. Companion workbook: `EVG1020_2025_Software_Exception_Workbook.xlsx` (firm's corrected CCH Axcess Exception Workbook, filled in).*

A first-year short-term rental. The software's Schedule E defaults all assume a long-term residential rental: passive
with a $25,000 active-participation allowance, 27.5-year building, not a QBI trade or business. For an Airbnb with a
3.1-night average stay that she materially participates in, every one of those defaults is wrong - and because her MAGI
is under $100,000, the passive default even produced the right 2025 dollars for the wrong reason, which is exactly why it is
silent. The NC nonresident return for the casino jackpot is not created by the W-2G alone.

| ID | Workbook tab | Exception | Axcess diagnostic? | Override amount | E-file impact |
|---|---|---|---|---:|---|
| EVG1020-SX1 | 5. Passive Activity (8582) | Short-term rental treated as a passive rental with the $25,000 allowance | **silent** (no diagnostic) | -15,147 | None |
| EVG1020-SX2 | 16. Vacation Home Allocation | Personal-use days - 280A(e) allocation of shared expenses (not the vacation-home limit) | **silent** (no diagnostic) | 54,616 | None |
| EVG1020-SX3 | 2. Diagnostics Log | STR building life (39-yr, transient use) and 100% bonus on furniture acquired after 01/19/2025 | **silent** (no diagnostic) | 6,005 | None |
| EVG1020-SX4 | 7. Multi-State Allocation | NC casino W-2G - NC nonresident D-400 / Schedule PN not created automatically | **silent** (no diagnostic) | 437 | NC D-400 nonresident e-filed |
| EVG1020-SX5 | 2. Diagnostics Log | Rental not flagged as a QBI trade or business - $15,147 QBI loss carryforward dropped | **silent** (no diagnostic) | -15,147 | None |

## EVG1020-SX1 - Short-term rental treated as a passive rental with the $25,000 allowance

*Workbook tab:* 5. Passive Activity (8582)  |  *Category:* Basis/At-Risk/Passive  |  *Manual calc:* Yes  |  *Amount:* $-15,147  |  *Procedure doc:* Rental Properties

- **CCH Axcess by default:** A Schedule E rental defaults to rental real estate, passive, active participation. Form 8582 then allows the ($15,147) loss under the $25,000 special allowance (MAGI $89,104 < $100,000) - right number, wrong reason. In any year MAGI exceeds $150,000 (or for an LP-style owner) the same default would suspend the loss.
- **Axcess diagnostic:** None - silent
- **Axcess fix:** Rental and Royalty Income (Schedule E): property type 3 (short-term rental); activity is NOT a rental activity for 469 (average stay 192/62 = 3.10 nights <= 7 - Reg. 1.469-1T(e)(3)(ii)(A)); material participation = Yes (test 3: 180 hours, more than the cleaner's ~95). Nonpassive -> no Form 8582; loss offsets wages. No substantial services -> stays on Schedule E, no SE tax (verify field names in current release).
- **ProConnect by default:** Same - a rental defaults to passive with the special allowance unless the activity is marked nonpassive / material participation.
- **ProConnect fix:** Rental & Royalty Income (Sch E): property type 'Short-term rental'; check 'Materially participated' / not a passive activity; Form 8582 not generated (screen/field per current release - verify).
- **E-file impact:** None
- **Return lines affected:** 8 (Schedule 1 line 5), Schedule E line 26
- **Notes:** Audit-exposed position: contemporaneous dated hours log advised for 2026; the average-stay test is annual.

## EVG1020-SX2 - Personal-use days - 280A(e) allocation of shared expenses (not the vacation-home limit)

*Workbook tab:* 16. Vacation Home Allocation  |  *Category:* Other  |  *Manual calc:* No  |  *Amount:* $54,616  |  *Procedure doc:* Rental Properties

- **CCH Axcess by default:** With personal-use days left at 0, Axcess deducts 100% of shared expenses. Entering the girls' trip (6 days) makes the software allocate by rental/total days used; personal use is under the greater of 14 days or 10% of rental days, so the 280A(c)(5) income limit does not apply.
- **Axcess diagnostic:** None - silent
- **Axcess fix:** Rental input: days rented at fair rental 192; personal-use days 6 (10/12-10/18; the two August repair days are not personal days). Shared expenses $56,323 (incl. depreciation) x 192/198 = 96.97% -> $54,616. Guest-only costs 100% rental. Personal share of property tax ($66) to Schedule A; personal mortgage interest ($429) nondeductible.
- **ProConnect by default:** Same - expenses are prorated only when personal-use days are entered.
- **ProConnect fix:** Rental & Royalty Income: 'Days rented at fair rental value' 192, 'Personal use days' 6; vacation-home limitation not applicable (screen/field per current release - verify).
- **E-file impact:** None
- **Return lines affected:** Schedule E expenses, Schedule A line 5b

## EVG1020-SX3 - STR building life (39-yr, transient use) and 100% bonus on furniture acquired after 01/19/2025

*Workbook tab:* 2. Diagnostics Log  |  *Category:* Depreciation  |  *Manual calc:* Yes  |  *Amount:* $6,005  |  *Procedure doc:* Rental Properties

- **CCH Axcess by default:** A building on a residential rental defaults to 27.5-year residential rental property. Furniture added as 5-year property gets the bonus rate tied to the acquisition date entered - if the acquisition date is blank or before 01/20/2025 the 40% phase-down rate applies instead of 100%. Client spreadsheet expensed closing costs and furniture.
- **Axcess diagnostic:** None - silent
- **Axcess fix:** Depreciation (4562) for the rental: building $330,148 (basis $388,410 incl. $3,410 closing costs; land $58,262 by assessor ratio) = 39-year nonresidential SL MM, PIS 04/2025 -> $6,005 (a unit used predominantly by transients is not a 'dwelling unit' - 168(e)(2)(A); 27.5-yr is the aggressive alternative, signer agreed 39). Furniture $24,600 5-yr, acquisition dates 03/22-03/30/2025 -> 100% special allowance. Loan costs $4,510 amortized 360 months ($113 for 9).
- **ProConnect by default:** Same - asset method/life follow the asset category chosen; bonus % follows the acquisition date entered.
- **ProConnect fix:** Rental > Depreciation: building as nonresidential real property (39-yr, MM); furniture 5-yr with acquisition date after 01/19/2025 so 100% special allowance applies (screen/field per current release - verify).
- **E-file impact:** None
- **Return lines affected:** Schedule E line 18, Form 4562

## EVG1020-SX4 - NC casino W-2G - NC nonresident D-400 / Schedule PN not created automatically

*Workbook tab:* 7. Multi-State Allocation  |  *Category:* State Allocation  |  *Manual calc:* No  |  *Amount:* $437  |  *Procedure doc:* SALT Implications - New State Filing Requirements

- **CCH Axcess by default:** The W-2G's state boxes (NC, $510 withheld) do not by themselves create a nonresident NC return for a Tennessee resident; the NC withholding can be lost or (wrongly) claimed nowhere.
- **Axcess diagnostic:** None - silent
- **Axcess fix:** Add North Carolina nonresident (D-400 with Schedule PN): NC-source income = gambling winnings $12,000 of federal AGI $89,104 = 13.47%; NC standard $12,750 (no NC gambling-loss deduction) -> NC TI $76,354 x 13.47% = $10,285 x 4.25% = $437; withholding $510 -> refund $73. No resident credit (TN has no income tax).
- **ProConnect by default:** Same - the nonresident state return must be activated and the W-2G sourced to NC.
- **ProConnect fix:** State > North Carolina (nonresident): source the W-2G winnings to NC and enter NC withholding 510 (screen/field per current release - verify).
- **E-file impact:** NC D-400 nonresident e-filed
- **Return lines affected:** NC D-400 / Schedule PN

## EVG1020-SX5 - Rental not flagged as a QBI trade or business - $15,147 QBI loss carryforward dropped

*Workbook tab:* 2. Diagnostics Log  |  *Category:* Other  |  *Manual calc:* No  |  *Amount:* $-15,147  |  *Procedure doc:* QBI (QOFs, QROFs)

- **CCH Axcess by default:** Rental activities default to 'not a section 199A trade or business'. With a net loss there is no 2025 deduction either way, so nothing looks wrong - but the $15,147 qualified business loss is not carried to 2026 and 2026 QBI is overstated.
- **Axcess diagnostic:** None - silent
- **Axcess fix:** Rental input > Section 199A: mark the STR as a qualified trade or business (self-managed, regular and continuous); Form 8995 shows QBI (15,147) -> deduction $0, QBI loss carryforward $15,147 to 2026 (PERM / carryforward report).
- **ProConnect by default:** Same - the rental must be designated as a QBI trade or business for the loss to carry forward.
- **ProConnect fix:** Rental & Royalty Income > Qualified Business Income (199A): 'Trade or business' = Yes (field per current release - verify).
- **E-file impact:** None
- **Return lines affected:** 13a, Form 8995, 2026 carryforward

