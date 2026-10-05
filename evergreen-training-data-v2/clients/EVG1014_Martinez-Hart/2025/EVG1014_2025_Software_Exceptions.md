# EVG1014 - Sofia Martinez & Liam Hart - 2025 Software Exceptions (CCH Axcess & Intuit ProConnect)

*Synthetic training data - Project Evergreen v2. Companion workbook: `EVG1014_2025_Software_Exception_Workbook.xlsx` (firm's corrected CCH Axcess Exception Workbook, filled in).*

Newlyweds, a first-year Schedule C, and a first joint return. Two software defaults bit this return: the prior-year
tax that proformas into Form 2210 came only from Liam's 2024 return in our system (Sofia was a TurboTax filer), and the
name control is built from whatever last name is typed in - the software has no SSA lookup, so the mismatch surfaced only as
an IRS reject. The 1099-K/1099-NEC overlap and part-year home office are silent input traps.

| ID | Workbook tab | Exception | Axcess diagnostic? | Override amount | E-file impact |
|---|---|---|---|---:|---|
| EVG1014-SX1 | 8. Est. Tax Penalty (2210) | Form 2210 - joint 2025 return after two separate 2024 returns; PY tax rolled from one spouse | **silent** (no diagnostic) | 0 | None |
| EVG1014-SX2 | 2. Diagnostics Log | Primary name 'Sofia Hart' - name control does not match SSA (IND-031-04) | **silent** (no diagnostic) |  | IRS reject IND-031-04 on 04/08/2026; accepted after correction 04/10/2026 |
| EVG1014-SX3 | 2. Diagnostics Log | Stripe 1099-K includes the Arbor Brewing payments already on a 1099-NEC | **silent** (no diagnostic) | 30,750 | None |
| EVG1014-SX4 | 2. Diagnostics Log | Form 8829 for a part-year office in a rented apartment | **silent** (no diagnostic) | 3,206 | None |

## EVG1014-SX1 - Form 2210 - joint 2025 return after two separate 2024 returns; PY tax rolled from one spouse

*Workbook tab:* 8. Est. Tax Penalty (2210)  |  *Category:* Est. Tax Penalty  |  *Manual calc:* Yes  |  *Amount:* $0  |  *Procedure doc:* Workpapers / Responding to Review Points

- **CCH Axcess by default:** Proforma brings in Liam's 2024 tax ($5,963) only - Sofia's 2024 return was self-prepared. With the 2210 input left on the current-year test, Axcess computes a penalty: 90% of 2025 tax $11,063 > withholding $9,446 and no estimates.
- **Axcess diagnostic:** None - silent
- **Axcess fix:** Penalties and Interest / Form 2210 input: prior-year tax = $8,910 (Liam $5,963 + Sofia $2,947 - the sum of both separate 2024 taxes when filing jointly for 2025); prior-year AGI $105,285 (< $150,000 -> 100%). Required annual payment $8,910 < withholding $9,446 -> penalty $0. Support: Sofia's 2024 TurboTax summary (PBC #12).
- **ProConnect by default:** Same - prior-year tax for the 2210 safe harbor comes from the data entered/rolled; ProConnect cannot know a spouse filed elsewhere.
- **ProConnect fix:** Payments, Penalties & Extensions > 2210: 2024 tax = 8,910 (combined), 2024 AGI = 105,285 (screen per current release - verify).
- **E-file impact:** None
- **Return lines affected:** 38
- **Notes:** Form 2210 instructions: if you file jointly for 2025 but separately for 2024, use the sum of the two 2024 taxes.

## EVG1014-SX2 - Primary name 'Sofia Hart' - name control does not match SSA (IND-031-04)

*Workbook tab:* 2. Diagnostics Log  |  *Category:* E-file Disqualifying  |  *Manual calc:* No  |  *Amount:* -  |  *Procedure doc:* E-File Rejects

- **CCH Axcess by default:** Axcess builds the primary name control from the last name keyed on the client/taxpayer input. 'Hart' (from the organizer) passes every internal check; the mismatch with SSA ('Martinez') is only found by the IRS.
- **Axcess diagnostic:** None - silent
- **Axcess fix:** General > Taxpayer information: last name 'Martinez' (Sofia E. Martinez) - name control MART - until she files Form SS-5. Save corrected version (v2), retransmit, monitor to acceptance (accepted 04/10/2026).
- **ProConnect by default:** Same - name control is derived from the name entered; no SSA validation before transmission.
- **ProConnect fix:** General > Taxpayer/Spouse information: taxpayer last name = Martinez; retransmit (name control override field, if used, per current release - verify).
- **E-file impact:** IRS reject IND-031-04 on 04/08/2026; accepted after correction 04/10/2026
- **Return lines affected:** Page 1 name
- **Notes:** Add to the newlywed filing-status checklist: compare organizer name to SS card / 1099 names.

## EVG1014-SX3 - Stripe 1099-K includes the Arbor Brewing payments already on a 1099-NEC

*Workbook tab:* 2. Diagnostics Log  |  *Category:* Other  |  *Manual calc:* Yes  |  *Amount:* $30,750  |  *Procedure doc:* Schedule C

- **CCH Axcess by default:** Each 1099-NEC and 1099-K entered on the Schedule C information-return inputs flows to gross receipts: $18,000 + $9,500 + $12,400 = $39,900. Axcess cannot see that $9,500 of the Stripe card volume is the same money as the Arbor Brewing 1099-NEC, and the $350 Venmo job (no form) is missing.
- **Axcess diagnostic:** None - silent
- **Axcess fix:** Business Income (Schedule C) > Gross receipts: $30,750 = Kerrytown $18,000 + Stripe $12,400 + Venmo $350 (Arbor's $9,500 counted once, inside Stripe). Keep the CSV-to-1099 reconciliation in WP 10 for any AUR notice. Stripe fees $363 from the CSV.
- **ProConnect by default:** Same - 1099-NEC and 1099-K amounts linked to Schedule C both flow to gross receipts.
- **ProConnect fix:** Business Income (Sch C) > Income: enter unique receipts $30,750 (do not link both the Arbor 1099-NEC and the full 1099-K); keep the reconciliation (screen/field per current release - verify).
- **E-file impact:** None
- **Return lines affected:** 8 (Schedule 1 line 3), Schedule C line 1, Schedule SE, 13a

## EVG1014-SX4 - Form 8829 for a part-year office in a rented apartment

*Workbook tab:* 2. Diagnostics Log  |  *Category:* Other  |  *Manual calc:* Yes  |  *Amount:* $3,206  |  *Procedure doc:* Schedule C

- **CCH Axcess by default:** Form 8829 applies the business-use % (150/900 = 16.67%) to whatever expense totals are entered. Keying the full-year rent and utilities from the lease/bills deducts January-March, before the business started; the simplified method, if chosen, needs the average monthly square footage for a 9-month year.
- **Axcess diagnostic:** None - silent
- **Axcess fix:** Business Income > Business Use of Home (8829): enter April-December rent, DTE, internet and renters insurance only ($19,233) -> $3,206. Simplified comparison $563 ($5 x average 112.5 sq ft) kept on the WP. No depreciation (rented).
- **ProConnect by default:** Same - the home-office percentage is applied to the expense amounts entered; part-year proration is manual.
- **ProConnect fix:** Business Income > Business Use of Home (8829): enter only April-December expenses (screen/field per current release - verify).
- **E-file impact:** None
- **Return lines affected:** Schedule C line 30, Form 8829

