# EVG1013 - Brooks - 2025 Software Exception Log (CCH Axcess / ProConnect)

| ID | Workbook tab | Exception | Silent? | Amount | Axcess fix (input/override location) | ProConnect fix | E-file impact |
|---|---|---|---|---:|---|---|---|
| SE-1 | 17 Equity comp basis & cross-account wash sales | NSO same-day sale: 1099-B basis = strike only; $22,000 W-2 code V income not in basis | Yes - silent | 22,000 basis adj (gain 21,975.05 -> loss 24.95) | Income/Deductions > Dispositions (Sch D/4797): enter 1099-B as reported, Form 8949 adjustment code B, adjustment -22,000 (or corrected basis 26,000 with code B) - verify field path in current release | Schedule D/4797 > Dispositions: adjustment code B, amount -22,000 - screen/field per current release - verify | None (box A with adjustment; 8949 detail e-filed) |
| SE-2 | 17 Equity comp basis (ISO) / 9 AMT | Form 3921 ISO exercise-and-hold is not on any 1099/W-2; nothing imports, so no AMT unless the 3921 is keyed | Yes - silent | 50,000 AMT adj; AMT 4,346 | Income/Deductions > Form 3921 (ISO) input, or AMT adjustment for ISOs on Form 6251 line 2i - verify field path in current release | Form 3921 / AMT ISO adjustment input - screen/field per current release - verify | None |
| SE-3 | 2 Diagnostics Log (log-only) | Track dual basis of ISO lot (regular 6,000 / AMT 56,000) and MTC carryforward 4,346 to 2026 Form 8801 | Yes - silent | 4,346 | Confirm the proforma carries the MTC carryforward and AMT basis to 2026 (asset/AMT basis memo field) - verify | Same - verify carryforward screen | None |
| SE-4 | 2 Diagnostics Log (log-only) | HSA excess contribution withdrawn by the extended due date: if 5498-SA box 2 ($5,300) is keyed as contributions, software computes a $1,000 excess and a 6% Form 5329 excise ($60) | Partly - Form 5329 generates without a warning | 1,000 excess / 60 excise avoided | Health Care > HSA (8889): enter employer contributions 4,300 (from W-2 code W); participant contributions 0 (excess withdrawn before due date - Form 8889 instr. line 2); do not key 5498-SA box 2 total - verify field path | HSA screen: same inputs - screen/field per current release - verify | None |
| SE-5 | 2 Diagnostics Log (log-only) | Untimely 83(b) (Form 15620 line 12 $8,000): no form/import, but do NOT key the $8,000 as wages/other income | Yes - silent (keying error risk) | 8,000 excluded | No entry. Memo in workpapers | No entry | None |

**SE-1.** Both packages import the E*TRADE 1099-B with $4,000 basis and compute a $21,975 short-term gain. The $22,000 bargain
element is already in W-2 box 1 (code V), so as imported the income is taxed twice. Corrected basis $26,000 (Reg. 1.6045-1(d)(6));
reported on 8949 box A with code B. Net loss $(24.95).

**SE-2.** ISO exercises produce no W-2/1099 income, so the software computes no AMT preference unless the Form 3921 is
entered. 4,000 x ($14.00 - $1.50) = $50,000 -> Form 6251 line 2i -> AMT $4,346.

**SE-3.** The AMT basis and the minimum tax credit live outside the 2025 forms. If they are not carried forward, the client
over-pays AMT-basis gain (regular vs AMT gain on sale) and loses the $4,346 credit in 2026+.

**SE-4.** Default HSA input from the 5498-SA overstates contributions. Per the Form 8889 instructions, contributions withdrawn
as an excess by the due date (incl. extensions) are excluded from line 2; the $38 earnings are 2026 income.

**SE-5.** The client's Form 15620 shows $8,000 "includible in income". The election was postmarked 12/10/2025, after the
12/03/2025 deadline, so it is void; nothing is reported in 2025.
