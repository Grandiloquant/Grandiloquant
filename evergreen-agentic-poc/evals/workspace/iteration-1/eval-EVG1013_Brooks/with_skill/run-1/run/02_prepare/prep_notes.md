# EVG1013 - Nathan J. Brooks - 2025 Form 1040 - Preparer Notes

## Return summary
| | Federal | IL-1040 |
|---|---:|---:|
| Filing status | Single | Resident |
| AGI / IL base income | 165,959 | 165,959 |
| Deduction / exemption | Standard 15,750 | 2,850 |
| Taxable income / net income | 150,209 | 163,109 |
| Regular tax | 28,897 | |
| AMT (Form 6251) | 4,346 | |
| Total tax | 33,243 | 8,074 |
| Payments | 33,600 (W/H 27,600 + extension 6,000) | 8,150 W/H |
| **Refund** | **357** | **76** |
Engine diagnostics: none. Chicago: no city tax.

## What I did and why
1. **Filing status.** Single, no dependents, no marital change (organizer Q1; PERM). Age 30.
2. **Wages.** One W-2 (Parallax) box 1 $164,700 incl. code V $22,000 NSO income. Medicare wages $176,700 < $200,000 -> no
   Additional Medicare. SS at the $176,100 wage base (one employer -> no excess SS).
3. **NSO sale (WP-1).** 1099-B basis $4,000 is the strike only. Basis corrected to $26,000 (strike + $22,000 W-2 code V
   income; Reg. 1.6045-1(d)(6)); 8949 box A code B -> ST loss $(24.95). This answers the client's double-tax question.
4. **ISO exercise (WP-2).** Form 3921: 4,000 sh at $1.50, FMV $14.00 (409A) -> $50,000 AMT adjustment (IRC 56(b)(3)), no
   regular-tax income; shares held at year-end so no disqualifying disposition. AMT $4,346. AMT basis $56,000 vs regular
   $6,000. Entire AMT is deferral-type -> MTC carryforward $4,346 (WP-3).
5. **Loomwork founder shares / 83(b) (WP-5).** Grant 11/03/2025; election due 12/03/2025 (IRC 83(b)(2), Reg. 1.83-2(b));
   Form 15620 signed 12/08 and postmarked 12/10/2025 -> untimely, so the election is invalid. Shares are unvested at
   12/31/2025 -> **no 2025 income**; the client's "$8,000" is not reported. Income will arise at each vesting date
   (FMV at vesting) beginning 11/03/2026. Flagged for signer and client advice.
6. **Interest.** Wealthfront 1099-INT $1,284.37 (Sch B optional at this level; engine shows it).
7. **HSA (WP-4).** Self-only limit $4,300 fully used by payroll + employer (W-2 code W). The $1,000 April after-tax deposit
   was excess and was returned with $38 NIA on 09/15/2026, before the 10/15/2026 extended due date -> no 6% excise (no
   Form 5329), no deduction (Form 8889 line 2 = 0), $38 taxable in 2026. Form 8889 filed (line 9 = 4,300).
8. **Deductions (WP-6).** Itemized would be $8,400 (IL W/H 8,150 + CPL Foundation $250) vs standard $15,750 -> standard.
   The $250 gift gives no 2025 benefit (non-itemizer charitable deduction starts 2026).
9. **Payments (WP-7).** W/H $27,600 (W-2 box 2); extension payment $6,000 (Form 4868 04/13/2026 per receipt log) on
   Sch 3 line 10. No estimates. Form 2210: withholding exceeds 100% of 2024 tax ($23,526) -> no penalty.
10. **Illinois (WP-8).** AGI with no modifications; exemption $2,850; tax $8,074; W/H $8,150; refund $76.
11. **PY comparison (WP-9).** Tax up $9,717: wages +$24,820 (incl. NSO) and AMT $4,346.

## Items excluded or treated differently from the documents
* 1099-B basis $4,000 -> $26,000 (code B).
* Form 15620 line 12 "$8,000 includible" -> $0 (late election).
* 5498-SA box 2 $5,300 -> not entered as contributions; only W-2 code W $4,300 as employer contributions; excess $1,000 removed.
* E*TRADE supplement, organizer, cap table, PY summary - informational only.
* Organizer interest "~1,300" -> 1,284.37 per 1099-INT.

## Assumptions and open items
* $6,000 extension payment taken from the receipt log; EFTPS/Direct Pay confirmation requested (non-blocking; tie to IRS
  account transcript before e-file if possible).
* Assumed no earlier mailing of the 83(b) exists (the only evidence shows 12/10/2025 postmark).
* Assumed no other HSA/HDHP changes and no other accounts (organizer; PERM).

## Carryforwards to 2026
* Minimum tax credit (Form 8801): **$4,346**.
* ISO lot 4,000 PLXR, acquired 02/14/2025: regular basis $6,000; AMT basis $56,000 (Form 6251 line 2k adjustment on sale).
* Capital loss carryover: none (2025 net loss $25 fully used against ordinary income).
* HSA: $38 NIA reportable in 2026 (Sch 1 other income) from the 2026 1099-SA code 2.
* Loomwork RSA: 20,000 shares vesting from 11/03/2026 - compensation at vesting FMV (no valid 83(b)); $0 basis.

## Filing notes for the signer
* Returns: Federal 1040 (Single) + Sch D/8949, Form 6251, Schedule 2, Schedule 3, Form 8889; IL-1040. E-file both.
  Extended due date **10/15/2026** - three days away; file now.
* Refunds: federal $357, IL $76 - direct deposit to Chase ****7730 (voided check on file).
* Client advice: (a) late 83(b) - explain consequences and recommend he talk to Loomwork counsel promptly (e.g. whether the
  company can restructure the grant so a new, timely election can be made); (b) ISO shares - qualifying holding period met
  after 02/14/2026; a 2026 sale lets him use the $4,346 MTC and the AMT basis; a disqualifying disposition would be possible
  but now unnecessary; (c) 2026 withholding/estimates - safe harbor 110% of 2025 tax = $36,567; vesting Loomwork income and any
  PLXR sales should be planned; (d) HSA - keep total payroll+employer+personal at or below the 2026 self-only limit.
