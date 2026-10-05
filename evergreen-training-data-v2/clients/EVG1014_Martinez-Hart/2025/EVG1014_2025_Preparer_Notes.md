# EVG1014 - Martinez, Sofia & Hart, Liam - 2025 Form 1040 - Preparer Notes

*Synthetic client - Project Evergreen. Return status: **signed off; e-filed 04/08/2026 (rejected IND-031-04), corrected and
retransmitted 04/09/2026, accepted 04/10/2026.***

## Return summary
| | |
|---|---|
| Filing status | Married filing jointly (primary: Sofia E. Martinez) |
| AGI (line 11) | $115,144 |
| Deduction | Standard $31,500; QBI $4,267 |
| Taxable income | $79,377 |
| Income tax / SE tax | $9,048 / $3,244 |
| Total tax | $12,292 |
| Withholding (W-2 + 1099-G) | $9,446 |
| **Balance due** | **$2,846** (paid by direct debit 04/15/2026; no 2210 penalty) |
| Michigan | tax $4,401, withheld $4,032, balance due $369 |

## What I did and why (plain English)
1. **Filing status.** They married 12/20/2025. You are married for the whole year if married on 12/31, so Single is not
   an option (answering the co-worker's advice in Liam's email). Per the Projections procedure I ran both MFJ and MFS:
   MFJ total tax $12,292 vs MFS $4,137 (Sofia) + $10,859 (Liam) = $14,996 ->
   **MFJ saves $2,704**, mainly because Liam's income in the MFS 22% bracket drops to 12% on a joint return.
   Michigan is a flat 4.25% with the same exemptions either way, so no state difference. Clients chose MFJ.
2. **Names / e-file.** The organizer and Liam's email said "Sofia Hart", and the first transmission used Hart. It was
   rejected on 04/08 with **IND-031-04** (primary name control does not match SSA). Sofia confirmed she has not filed an
   SS-5, so the return must use **Sofia E. Martinez / name control MART**. Per the E-File Rejects procedure: reject reason
   documented, corrected version saved (v2), retransmitted 04/09, monitored - accepted 04/10. Told Sofia to file Form SS-5
   with SSA (and update her Stripe/1099 W-9s) before switching to Hart on the 2026 return.
3. **Schedule C - gross receipts.** Information returns total $18,000 + $9,500 + $12,400 = $39,900, but the Stripe balance
   history shows the Arbor Brewing invoices ($9,500) were paid by card through Stripe, so the same money is on both the
   Arbor 1099-NEC and the Stripe 1099-K. Unique receipts: Kerrytown $18,000 + Stripe $12,400 + a Venmo
   logo job $350 with no form (still income) = **$30,750**. Reconciliation (client spreadsheet vs 1099s vs
   Stripe CSV) is in WP 9-10. If the IRS AUR matches the 1099-NEC and 1099-K separately we have the support.
4. **Schedule C - expenses.** From her workbook: Stripe fees $363 (from the CSV, not her estimate), software,
   fonts, website, cards, phone at 50%, meals at 50%. Laptop ($1,899) and tablet ($379) are each under $2,500 -> expensed
   under the **de minimis safe harbor election** (statement attached to the return). Removed personal items: Spotify ($99)
   and **their own wedding invitations** ($640). Top-of-form boxes: **line H checked (started 04/2025)**; line I "No"
   (she paid no contractors). Net profit $22,956.
5. **Home office.** Second bedroom, 150 of 900 sq ft (16.67%), used regularly and exclusively for design since April.
   Form 8829 with only April-December rent, DTE, internet and renters insurance ($19,233) -> **$3,206**.
   Simplified method would be only $563 ($5 x average monthly 112.5 sq ft for a 9-month year), so 8829 used.
   They rent - no depreciation/recapture issue.
6. **SE tax and QBI.** SE tax $3,244 (half = $1,622 on Sch 1 line 15). QBI = net profit less
   half SE tax = $21,334 -> 20% deduction $4,267 (well below the $394,600 threshold). No SE health insurance
   (Sofia was on her father's plan and paid no premiums).
7. **Unemployment.** 1099-G $5,460 (Jan-Mar) on Schedule 1 line 7; $546 federal withholding on line 25b; $232 MI withholding.
   Taxable for Michigan too.
8. **Estimated tax penalty (Form 2210).** No estimates were made and the balance due exceeds $1,000. 90% of 2025 tax is
   $11,063, more than withholding $9,446. But the prior-year safe harbor for a couple filing jointly in 2025
   who filed separately in 2024 uses the **sum of both 2024 taxes**: Liam $5,963 + Sofia $2,947
   = $8,910 (combined 2024 AGI under $150,000, so 100%). Withholding exceeds that -> **no penalty**.
9. **Michigan.** MI-1040 joint: federal AGI $115,144 less 2 x $5,800 exemptions = $103,544 x 4.25% = $4,401;
   withholding $4,032; due $369 (under $500 - no MI estimate penalty). Ann Arbor has no city income tax, so
   no local return (checked per Local Filing Requirements).

## Open items / client communication
- Closed: name issue (04/09 email). Sofia to file SS-5; update PERM once SSA confirms.
- 2026 planning email sent 04/10: quarterly estimates for Sofia's business (suggested $1,300/quarter federal, $350 MI) or
  increase Liam's W-4 using the MFJ checkbox; keep a mileage log if she starts client visits; consider a Solo 401(k)/SEP.

## Hand-off to signer / routing
- [x] Return locked; Accountant's copy saved as *reviewed* (v2 after reject)
- [x] Federal 1040 - e-file; due 04/15/2026 - accepted 04/10/2026
- [x] MI-1040 - e-file; due 04/15/2026 - accepted
- [x] No FBAR; no local return (Ann Arbor)
- [x] eSign 8879 + MI-8453 - both spouses signed; contact Liam by email
- [x] Balance due: direct debit 04/15/2026 from UMCU ****5580
- Billing: joint + first-year Sch C $1,650 + home office 0.5 hr + MFJ/MFS simulation 0.5 hr. The e-file reject rework
  (0.3 hr) is an **external** reason (client-provided name) - chargeable per Updating Returns procedure; signer elected to W/O as goodwill.
