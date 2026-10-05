# EVG1012 - Walter & June Hoffman - 2025 Software Exceptions (CCH Axcess & Intuit ProConnect)

*Synthetic training data - Project Evergreen v2. Companion workbook: `EVG1012_2025_Software_Exception_Workbook.xlsx` (firm's corrected CCH Axcess Exception Workbook, filled in).*

A retiree return where the software's carry-forward data is necessary but not sufficient. The installment note proformas
from 2024, but Axcess cannot know what was actually received in 2025, so a blank organizer line silently produces no
gain and no interest. The NC Bailey exclusion depends on a fact (June's 1989 vesting) that is nowhere on the 1099-R.
The Form 2210 item documents why no penalty override is needed and flags the 2026 voucher amount.

| ID | Workbook tab | Exception | Axcess diagnostic? | Override amount | E-file impact |
|---|---|---|---|---:|---|
| EVG1012-SX1 | 2. Diagnostics Log | Installment sale year 2 - proforma'd Form 6252 computes $0 when 2025 payments are blank | **silent** (no diagnostic) | 16,904 | None |
| EVG1012-SX2 | 2. Diagnostics Log | Seller-financed mortgage interest - buyer's name, SSN and address must print first on Schedule B | **silent** (no diagnostic) | 17,983 | None ($50 penalty for omitting the buyer SSN) |
| EVG1012-SX3 | 2. Diagnostics Log | NC Bailey settlement - June's TSERS pension taxed by default | **silent** (no diagnostic) | 30,788 | NC D-400 e-filed |
| EVG1012-SX4 | 8. Est. Tax Penalty (2210) | Form 2210 - 110% prior-year safe harbor missed, 90% current-year test met; 2026 vouchers | **silent** (no diagnostic) | 0 | None |

## EVG1012-SX1 - Installment sale year 2 - proforma'd Form 6252 computes $0 when 2025 payments are blank

*Workbook tab:* 2. Diagnostics Log  |  *Category:* Other  |  *Manual calc:* Yes  |  *Amount:* $16,904  |  *Procedure doc:* Return - General Return Prep Notes (blank organizer line is not zero) / Installment Sales

- **CCH Axcess by default:** The 2024 Form 6252 rolls forward with the contract price, gross profit % (73.0952%) and note balance, but the current-year 'payments received' fields are blank because the organizer line was blank. Axcess computes $0 installment gain and the note interest never reaches Schedule B. If the attorney's amortization schedule is keyed instead of actual receipts, it picks up 12 payments (the December check was received 01/06/2026).
- **Axcess diagnostic:** None - silent
- **Axcess fix:** Gains and Losses > Installment Sales (Form 6252), Caldwell land note: 2025 principal received $23,126 (11 payments, amortization-schedule split - interest first). Gain = 23,126 x 73.0952% = $16,904 LT (Schedule D line 11). No 1250/1245 recapture (unimproved land). Payment 12 (received 01/06/2026) goes to 2026.
- **ProConnect by default:** Same - the installment sale carries forward from the prior year, but the current-year payment must be entered; blank = no gain.
- **ProConnect fix:** Dispositions > Installment Sale (6252): enter 2025 payments received (principal) $23,126; confirm gross profit % 73.0952% carried from 2024 and line 26 gain $16,904 (field names per current release - verify).
- **E-file impact:** None
- **Return lines affected:** 7, Form 6252 line 21/26, Schedule D line 11
- **Notes:** Cash-basis: payments count when received. PERM note balance 12/31/2025 $312,874.

## EVG1012-SX2 - Seller-financed mortgage interest - buyer's name, SSN and address must print first on Schedule B

*Workbook tab:* 2. Diagnostics Log  |  *Category:* Other  |  *Manual calc:* Yes  |  *Amount:* $17,983  |  *Procedure doc:* Schedule B

- **CCH Axcess by default:** Note interest keyed as an ordinary interest payer (or lumped with the bank CD) prints as a plain Schedule B line; the seller-financed disclosure (buyer name/SSN/address, listed first) is only produced when the interest is flagged as seller-financed mortgage interest. Nothing prompts for it.
- **Axcess diagnostic:** None - silent
- **Axcess fix:** Income > Interest Income: payer 'Aaron M. & Beth L. Caldwell', mark as seller-financed mortgage (buyer used property as a personal residence), enter buyer SSN XXX-XX-6641 and address; amount $17,983 = amortization-schedule interest on 11 payments $17,908 + $75 late charge (verify field path in current release).
- **ProConnect by default:** Same - the seller-financed indicator and buyer information must be entered on the interest input.
- **ProConnect fix:** Income > Interest Income (1099-INT, 1099-OID): enter the Caldwell note as a separate payer with the 'seller-financed mortgage' option and the buyer's SSN/address (screen/field per current release - verify).
- **E-file impact:** None ($50 penalty for omitting the buyer SSN)
- **Return lines affected:** 2b, Schedule B line 1

## EVG1012-SX3 - NC Bailey settlement - June's TSERS pension taxed by default

*Workbook tab:* 2. Diagnostics Log  |  *Category:* State Allocation  |  *Manual calc:* No  |  *Amount:* $30,788  |  *Procedure doc:* SALT Implications

- **CCH Axcess by default:** The NC return taxes every 1099-R that is taxable federally unless the distribution is identified as a Bailey-qualifying government retirement benefit. The 1099-R itself carries no Bailey indicator, and Walter's private pension and IRA must stay taxable - so the result depends entirely on a per-1099-R state input.
- **Axcess diagnostic:** None - silent
- **Axcess fix:** North Carolina > Retirement/Schedule S deductions: mark June's TSERS 1099-R as Bailey-exempt (5+ years creditable service as of 08/12/1989 - PERM). Schedule S: SS $49,317 + Bailey $30,788. Leave Walter's pension and IRA taxable. NC taxable income $51,829; tax $2,203 (verify field path in current release).
- **ProConnect by default:** Same - the Bailey deduction is driven by a state-specific input per 1099-R.
- **ProConnect fix:** North Carolina return > retirement benefits (Bailey) input for June's TSERS 1099-R = $30,788 (screen/field per current release - verify).
- **E-file impact:** NC D-400 e-filed
- **Return lines affected:** NC D-400 Schedule S

## EVG1012-SX4 - Form 2210 - 110% prior-year safe harbor missed, 90% current-year test met; 2026 vouchers

*Workbook tab:* 8. Est. Tax Penalty (2210)  |  *Category:* Est. Tax Penalty  |  *Manual calc:* Yes  |  *Amount:* $0  |  *Procedure doc:* Workpapers / Estimated tax

- **CCH Axcess by default:** Axcess correctly computes the lesser of 90% of 2025 tax and 110% of 2024 tax (2024 AGI $171,273) - no penalty. The trap is a manual one: forcing a penalty because the 110% test failed, or (for 2026) hand-setting vouchers at 4 x $1,500 using the 100% rule. 2025 AGI is $157,434 (> $150,000), so the 2026 prior-year safe harbor is 110% of $12,817 = $14,099; withholding at the 2025 level + 4 x $1,500 = $12,780 falls short of it by $1,319.
- **Axcess diagnostic:** None - silent
- **Axcess fix:** Penalties and Interest: no override, no waiver - regular method; required annual payment $11,535 (90% of 2025 tax) is met every quarter. Estimates input for 2026: let the 110% method compute vouchers (or document a 90%-of-2026 projection if the clients prefer $1,500/quarter).
- **ProConnect by default:** Same calculation - ProConnect uses the lesser of the 90% / 110% tests from the prior-year data entered.
- **ProConnect fix:** Payments, Penalties & Extensions: confirm 2024 tax $20,486 and AGI $171,273 are entered; no penalty override. 2026 estimate vouchers: 110% method (screen per current release - verify).
- **E-file impact:** None
- **Return lines affected:** 38, 2026 Form 1040-ES
- **Notes:** Caught in v2 review: the draft open item applied the 100% rule (2025 AGI $157,434 > $150,000). Preparer Notes now recommend 4 x $1,830 federal estimates for 2026.

