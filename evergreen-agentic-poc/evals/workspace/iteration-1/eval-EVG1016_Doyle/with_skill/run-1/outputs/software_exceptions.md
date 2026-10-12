# EVG1016 - Doyle - Software exception log (CCH Axcess / ProConnect)

| ID | Workbook tab | Exception | Silent? | Amount | Axcess fix (input/override location) | ProConnect fix | E-file impact |
|---|---|---|---|---|---|---|---|
| 1 | 2 Diagnostics Log (log-only) | 1099-R code 1 QDRO distribution - 10% additional tax would calculate unless the 72(t) exception is entered | Yes - silent (code 1 produces Form 5329 tax by default) | $30,000 exception / $3,000 tax avoided | Retirement > 1099-R: early-distribution exception code 04 (QDRO) for $30,000 (verify field path in current release) | 1099-R screen, early-distribution exception field - screen/field per current release - verify | None once entered |
| 2 | 2 Diagnostics Log (log-only) | Filing status rolls forward from 2024 as MFJ with spouse data | Partly - diagnostic only if spouse data incomplete | n/a | General > Basic Data: change status to HOH, remove spouse income, enter Brian as spouse name/SSN for HOH-married-living-apart line; check "lived apart last 6 months" (verify field path) | Screen/field per current release - verify | HOH requires qualifying person entry |
| 3 | 2 Diagnostics Log (log-only) | Liam: dependent rolls forward with CTC; must be marked released to noncustodial parent (8332) but kept for HOH/2441 | Yes - silent; CTC would calculate for both children | $2,200 CTC | Dependents: Liam - code as "custodial parent releasing claim (8332)" / not claimed for CTC; keep as 2441 qualifying person (verify field path) | Screen/field per current release - verify | Duplicate-claim reject risk if left as dependent (Brian claims) |
| 4 | 2 Diagnostics Log (log-only) | Organizer alimony $13,500 may flow to Schedule 1 line 2a via organizer import | Yes - silent | $13,500 | Do not enter alimony received (post-2018 instrument); clear any organizer-imported amount | Screen/field per current release - verify | None |
| 5 | 2 Diagnostics Log (log-only) | W-2 box 14 "QUAL OT PREM" needs to be mapped to the Sch 1-A qualified overtime input (box 14 text is not recognized automatically) | Yes - silent | $4,860 | W-2 box 14 entry with the qualified-overtime code, or Sch 1-A overtime input (verify field path in current release) | Screen/field per current release - verify | None |
| 6 | 2 Diagnostics Log (log-only) | Joint 1098 - only Megan-paid share is hers (moot: standard deduction) | Yes | 6,750 / 3,608 | Enter Megan's share for comparison only | Same | None |
| 7 | 2 Diagnostics Log (log-only) | Brian's W-2 copy uploaded by client - must not be entered | Yes | $73,850 | Do not enter; keep in file as not-this-client | Same | None |
| 8 | 7 Multi-state allocation | MI overtime subtraction and GR treatment of the QDRO distribution need manual review in state/city modules | Yes | 4,860 / 30,000 | MI Schedule 1 subtraction; GR income schedule (verify field path) | Screen/field per current release - verify | None |

1. **QDRO 10% exception.** Code 1 tells the software "early, no known exception", so it computes 10% ($3,000) on Form 5329/Sch 2
unless the exception is entered. The plan is a qualified plan and the payee is an alternate payee spouse under a QDRO
(PBC/07), so 72(t)(2)(C) applies; enter exception 04 for the full $30,000.
2. **Filing status.** Rolled-forward MFJ is wrong; married at year end but considered unmarried (WP-1) -> HOH.
3. **Liam.** If he stays a full dependent, the software gives a $2,200 CTC Megan released to Brian. He must remain on the return
only as HOH qualifying person / 2441 qualifying person.
4. **Alimony.** Organizer lists $13,500 as alimony income; under a 2025 agreement it's excluded.
5. **Overtime.** Software keys on box 12/14 codes; free-text box 14 labels may not flow to Schedule 1-A.
6-8. As described in the table.
