# EVG1016 Megan R. Doyle: 2025 preparation notes

## Result (federal, from tools/compute_return.py: final/return.json)
- Filing status: **Head of Household**
- AGI: **$118,662** = wages 88,600 + interest 62 + QDRO 401(k) distribution 30,000
- Deductions: standard deduction 23,625 (itemized only 16,394) + Schedule 1-A overtime 4,860 = 28,485
- Taxable income: **$90,177**. Tax 13,014, minus CTC 2,200 (Nora) and dependent care credit 1,040, gives **total tax $9,774**
- Withholding: 7,800 (W-2) + 6,000 (1099-R) = 13,800, so the **refund is $4,026** (direct deposit to LMCU ****3321)

## Key judgments
1. **Filing status: HOH, not Single.** Marital status is set on 12/31/2025. The divorce judgment was entered 02/10/2026 and the separation agreement is not a decree of separate maintenance, so Megan was **married** at year end and cannot file Single. She is treated as "considered unmarried" (IRC 7703(b), Pub 501) because:
   - she files separately (as the agreement art. 9.1 requires);
   - Brian moved out 03/01/2025, so he was not in the household for the last 6 months;
   - she paid $25,548 of the $30,330 cost of keeping up the home (84%, per her schedule; mortgage principal correctly excluded);
   - the home was the main home of Liam and Nora for all of 2025;
   - she can claim Nora. Releasing Liam via Form 8332 does not affect this.
   HOH is better than MFS. Tell the client "Single" is not available.
2. **Alimony of $13,500 is not income.** The agreement was executed 03/20/2025, after 2018, so under the TCJA it is neither taxable to her nor deductible by Brian. Child support of $8,100 is also not income. Neither is reported, although the organizer listed $13,500.
3. **QDRO distribution ($30,000, 1099-R code 1).** Megan received it as alternate payee spouse under a QDRO (plan administrator determined it qualified on 08/04/2025), so it is taxable to her (IRC 402(e)(1)(A)) on lines 5a/5b. It is **exempt from the 10% additional tax** under IRC 72(t)(2)(C). Because the payer used code 1, file **Form 5329 Part I, exception code 04**, for the full $30,000 so the additional tax is $0. Her friend's penalty concern does not apply. Withholding of $6,000 (20% mandatory) is claimed on line 25b.
4. **Dependents and CTC.** Nora is claimed as a dependent with a $2,200 CTC. Liam is released to Brian for 2025 by a Form 8332 signed 01/28/2026 (agreement art. 9.2, odd years), so he is not claimed on Megan's return. Brian attaches the 8332, not us.
5. **Form 2441: both children count.** As custodial parent, Megan treats Liam as a qualifying person even though he is released (IRC 21(e)(5)), and both children were under 13. Expenses were $5,200 paid to Kent Kids Club (EIN 00-4471208), under the $6,000 limit. The credit is 20% = $1,040. She qualifies as unmarried for 2441 under IRC 21(e)(4).
6. **Schedule 1-A qualified overtime: $4,860.** This is the W-2 box 14 FLSA premium portion only (employer letter: 162 hrs x $30). She is eligible as HOH (not MFS), and MAGI is under $150k, so there is no phase-down.
7. **Mortgage interest and real estate tax.** The 1098 is in both names. Per agreement art. 9.3 and her schedule, Megan paid interest of $6,750 and RE tax of $3,608 (Brian paid Jan-Feb). SALT is 6,036 (MI withholding 3,450 + 1,275, Grand Rapids withholding 1,311) + 3,608. Itemized totals 16,394, below the HOH standard deduction of 23,625, so we take the standard deduction. No Schedule A.
8. **Brian's W-2 (doc 13) is excluded.** It belongs to a former client with a separate preparer, and there is no joint return. Under the conflict check, do not use or retain it in her file beyond the receipt log, and do not share any of Megan's information with Brian.
9. **EIC not available** (AGI too high). Interest is $61.88, so no Schedule B is required (the engine shows it for reference only).

## State and local (estimates; prepare in state software)
- **MI-1040 (Michigan resident).** Michigan has no HOH status, so file as single/separate per MI instructions; Brian's name and SSN go on the return if Michigan requires it for married-separate. AGI is 118,662. There are no retirement subtractions: she was born in 1989, and the QDRO distribution is taxable to MI. Exemptions: 2 (Megan and Nora) x $5,800 = 11,600. Taxable income 107,062 x 4.25% = about $4,550. MI withholding is 3,450 + 1,275 = 4,725, so the refund is about **$175**. Homestead property tax credit is not available (total household resources exceed $69,700).
- **GR-1040R (Grand Rapids resident, 1.5%).** Wages 88,600 + interest 62. The 401(k) distribution is treated as taxable because 1099-R code 1 is a premature distribution, which Michigan city income tax instructions tax. **Reviewer to confirm**: if the QDRO payment is treated as an excludable pension, tax falls by about $450. Exemptions are 2 x $600. Taxable 117,462 x 1.5% = about $1,762. City withholding is 1,311, so about **$451 is due** (about $1 due if the 401(k) payment is excluded). Answer to Megan: yes, Grand Rapids requires its own return. Wyoming, MI has no city income tax, which only affects Brian.

## Open items / client communication
- Explain to the client that she files HOH (not Single), that the alimony is not taxable, and that there is no 10% penalty on the QDRO payout.
- Confirm Brian is current on child support. The 8332 release was conditional, but it has been signed and delivered.
- Advise on 2026 withholding and estimates: alimony is untaxed, but she will file Single or HOH in 2026 (divorce final). She claims Liam in even years.
- Due dates: 04/15/2026 (federal, MI) and 04/30/2026 (Grand Rapids). Documents were received 02/19/2026, and filing is assumed timely. Today is 10/12/2026, so confirm whether the returns were filed or extended. Federal and MI are refunds, so no late-payment penalty applies there, but the GR balance would carry interest and penalty if filed late.
