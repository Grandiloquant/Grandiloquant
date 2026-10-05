# EVG1017 - Frank & Diane Russo - 2025 Software Exceptions (CCH Axcess & Intuit ProConnect)

*Synthetic training data - Project Evergreen v2. Companion workbook: `EVG1017_2025_Software_Exception_Workbook.xlsx` (firm's corrected CCH Axcess Exception Workbook, filled in).*

A large brokerage-plus-K-1 return where the software's imports are complete-looking but wrong in quiet ways: two
consolidated 1099s for the same account, a broker statement whose accrued-interest and WHFIT sections sit outside the
form totals, a noncovered lot with no basis, and a partnership distribution that exceeds basis only once the 752(b)
deemed distribution is counted. All seven items are silent. Workbook tabs 3/11 (Ridgeview basis and 752(b)),
5 (passive and PTP baskets), 7 (PA credit) and 14 (bond interest) carry the supporting numbers.

| ID | Workbook tab | Exception | Axcess diagnostic? | Override amount | E-file impact |
|---|---|---|---|---:|---|
| EVG1017-SX1 | 2. Diagnostics Log | Original AND corrected Morgan Stanley consolidated 1099 both imported | **silent** (no diagnostic) | 78,400 | None |
| EVG1017-SX2 | 14. Bond Interest & Premium | Accrued interest paid at purchase and accrued market discount - not netted by the broker | **silent** (no diagnostic) | -1,550 | None |
| EVG1017-SX3 | 2. Diagnostics Log | Noncovered Abbott lot imports with $0 basis; WHFIT section outside the 1099 totals | **silent** (no diagnostic) | 14,850 | None |
| EVG1017-SX4 | 3. K-1 Basis Limitation | Ridgeview distribution exceeds outside basis once the 752(b) deemed distribution is counted | **silent** (no diagnostic) | 9,500 | None |
| EVG1017-SX5 | 5. Passive Activity (8582) | Passive baskets - Oak Brook LP loss + omitted PY carryover vs PTP isolation | **silent** (no diagnostic) | 41,700 | None |
| EVG1017-SX6 | 7. Multi-State Allocation | PA-source K-1 income - PA-40 NR and IL Schedule CR not generated from the K-1 matrix | **silent** (no diagnostic) | 1,173 | PA-40 NR e-filed with the IL-1040 |
| EVG1017-SX7 | 2. Diagnostics Log | IL subtraction for US Treasury interest must be net of accrued interest paid; muni add-back | **silent** (no diagnostic) | 9,290 | None |

## EVG1017-SX1 - Original AND corrected Morgan Stanley consolidated 1099 both imported

*Workbook tab:* 2. Diagnostics Log  |  *Category:* Other  |  *Manual calc:* No  |  *Amount:* $78,400  |  *Procedure doc:* Scan - consolidated 1099 (corrected statements)

- **CCH Axcess by default:** Autoflow treated the 02/13 original and the 03/12 CORRECTED consolidated 1099s as two payer documents: dividends ~$158k, interest and sales doubled. The original also had box 3 nondividend $900 (vs $2,150), box 5 $8,400 (vs $9,200) and no box 1f market discount.
- **Axcess diagnostic:** None - silent
- **Axcess fix:** Delete the original statement's import (bookmark 'superseded'); keep only the CORRECTED 03/12/2026 statement: box 1a $78,400 (+ WHFIT $1,380 = Sch B $79,780), box 3 return of capital $2,150 (reduces VGSLX basis - not income), box 5 $9,200, box 1f $1,624.
- **ProConnect by default:** Same - an imported/entered second consolidated 1099 is additive; ProConnect does not know one supersedes the other.
- **ProConnect fix:** Delete the original 1099 entries; import/key the corrected statement only (screen per current release - verify).
- **E-file impact:** None
- **Return lines affected:** 2b, 3a, 3b, 7, 13a

## EVG1017-SX2 - Accrued interest paid at purchase and accrued market discount - not netted by the broker

*Workbook tab:* 14. Bond Interest & Premium  |  *Category:* Other  |  *Manual calc:* Yes  |  *Amount:* $-1,550  |  *Procedure doc:* Schedule B - accrued interest / state exemption

- **CCH Axcess by default:** The 1099-INT import reports box 1 $14,250 + box 3 $9,600 gross. The $1,240 (Apple bond) and $310 (Treasury note) of accrued interest Frank PAID sellers is only on the supplemental page, and the Ford bond's accrued market discount (1099-B box 1f, $1,624) stays inside the capital gain unless code D is entered.
- **Axcess diagnostic:** None - silent
- **Axcess fix:** Income > Interest Income: add negative lines 'Accrued interest' -1,240 (corporate) and -310 (US obligation, so the IL subtraction is also reduced); add $1,624 market discount as interest. Gains and Losses: Ford row box D, code D, adjustment -1,624. Schedule B line 2b = $26,184.
- **ProConnect by default:** Same - accrued interest paid and market discount must be entered as separate adjustments.
- **ProConnect fix:** Interest income input: 'Accrued interest paid' / negative adjustment lines (-1,240 and -310, the latter flagged as US obligation interest); Dispositions: Ford sale code D -1,624 with the $1,624 reported as interest (screen/field per current release - verify).
- **E-file impact:** None
- **Return lines affected:** 2b, Schedule B, Form 8949 box D, IL Schedule M

## EVG1017-SX3 - Noncovered Abbott lot imports with $0 basis; WHFIT section outside the 1099 totals

*Workbook tab:* 2. Diagnostics Log  |  *Category:* Capital Loss  |  *Manual calc:* Yes  |  *Amount:* $14,850  |  *Procedure doc:* Schedule D - missing cost basis

- **CCH Axcess by default:** (1) The ABT sale (box E, noncovered) imports with blank basis -> $36,900 gain. (2) The Invesco UIT (WHFIT) dividends $1,380 and pro-rata sales are reported in a separate statement section that is not in the 1099-DIV/B summary the import reads, so they are omitted. Neither is flagged.
- **Axcess diagnostic:** None - silent
- **Axcess fix:** Gains and Losses: ABT row basis $14,850 (2009 Schwab confirm) -> gain $22,050. Add WHFIT: dividends $1,380 ($1,210 qualified) on Schedule B; pro-rata sales on 8949 box E proceeds $4,820 / basis $4,310 (+$510); trust expenses $95 not deductible.
- **ProConnect by default:** Same - noncovered basis must be keyed; WHFIT items are not part of a 1099 import.
- **ProConnect fix:** Dispositions: enter ABT cost basis 14,850; add WHFIT dividends and pro-rata sale lines manually (screen per current release - verify).
- **E-file impact:** None
- **Return lines affected:** 3a, 3b, 7

## EVG1017-SX4 - Ridgeview distribution exceeds outside basis once the 752(b) deemed distribution is counted

*Workbook tab:* 3. K-1 Basis Limitation  |  *Category:* Basis/At-Risk/Passive  |  *Manual calc:* Yes  |  *Amount:* $9,500  |  *Procedure doc:* Schedules K-1

- **CCH Axcess by default:** Without the Section 6 basis limitation applied (beginning basis blank), Axcess treats the $80,000 box 19 distribution as tax-free. Even with basis entered, the $4,000 decrease in his share of liabilities (K-1 item K: 18,000 -> 14,000) is not a box 19 amount, so it is not counted as a distribution.
- **Axcess diagnostic:** None - silent
- **Axcess fix:** Income/Deductions > Partnership Passthrough > Section 6 (Basis Limitation): beginning basis $15,500 (tax capital -2,500 + liabilities 18,000); income +$59,000; distributions $80,000 cash + $4,000 752(b) deemed = $84,000 -> excess $9,500 IRC 731(a) LTCG on Form 8949 box F (held since 2017; footnote: no 751 property). Ending basis $0.
- **ProConnect by default:** Same - ProConnect does not compute partner outside basis from the K-1; a liability-share decrease must be entered as a deemed distribution.
- **ProConnect fix:** Partnership K-1 > basis worksheet / Dispositions: enter the $9,500 excess distribution as a long-term capital gain (8949 box F) and document basis (screen/field per current release - verify).
- **E-file impact:** None
- **Return lines affected:** 7, Form 8949 box F
- **Notes:** Supporting rows on tab 3 (basis) and tab 11 (752(b) liability shift).

## EVG1017-SX5 - Passive baskets - Oak Brook LP loss + omitted PY carryover vs PTP isolation

*Workbook tab:* 5. Passive Activity (8582)  |  *Category:* Basis/At-Risk/Passive  |  *Manual calc:* Yes  |  *Amount:* $41,700  |  *Procedure doc:* Schedules K-1

- **CCH Axcess by default:** (1) The organizer's PY column left the Oak Brook suspended loss ($7,300) blank, so Form 8582 shows no prior-year unallowed loss. (2) Unless the Permian K-1 is flagged as a PTP, its ($2,340) loss nets against Ridgeview's passive income and enters QBI.
- **Axcess diagnostic:** None - silent
- **Axcess fix:** Partnership Passthrough: Oak Brook prior-year unallowed loss $7,300 (from PY 8582 / PERM); Permian: check 'Publicly traded partnership' so 469(k) isolates it (PY suspended $1,150). Result: Oak Brook $9,600 + $7,300 allowed against Ridgeview $58,600 -> Schedule E $41,700; PTP $3,490 suspended (excluded from QBI). LP -> no $25k allowance.
- **ProConnect by default:** Same - prior-year unallowed losses and the PTP indicator are inputs.
- **ProConnect fix:** Partnership K-1 > Passive Losses tab: prior-year unallowed Regular (and AMT) = 7,300 for Oak Brook; Permian: PTP = Yes with PY unallowed 1,150. Form 8582 can be forced (1=when applicable, 2=force) if needed. *(ref: Intuit help: 'How to generate Form 8582 ... ProConnect Tax' (prior years' unallowed losses))*
- **E-file impact:** None
- **Return lines affected:** 8 (Schedule 1 line 5), Schedule E line 41, Form 8582, 13a

## EVG1017-SX6 - PA-source K-1 income - PA-40 NR and IL Schedule CR not generated from the K-1 matrix

*Workbook tab:* 7. Multi-State Allocation  |  *Category:* State Allocation  |  *Manual calc:* Yes  |  *Amount:* $1,173  |  *Procedure doc:* SALT Implications - New State Filing Requirements

- **CCH Axcess by default:** The Ridgeview state matrix ($38,200 PA) is a K-1 footnote; unless the PA amount is entered as PA-source and a PA nonresident return is added, no PA-40 NR is produced and IL Schedule CR has no tax paid to another state to credit.
- **Axcess diagnostic:** None - silent
- **Axcess fix:** Partnership Passthrough > state allocation: PA $38,200 (IL $19,000; WI $1,400 under WI's $2,000 threshold). Add PA-40 NR: tax $1,173 = NRK-1 withholding $1,173. IL Schedule CR: lesser of PA tax $1,173 or IL tax on PA income (16,864 x 38,200/346,385 = $1,860) -> $1,173. 731 gain treated as non-PA-source (assumption, flagged for signer).
- **ProConnect by default:** Same - nonresident state returns and the resident credit depend on state-source amounts entered per K-1.
- **ProConnect fix:** Partnership K-1 > State: PA-source 38,200; activate PA nonresident return; IL credit for tax paid to PA = 1,173 (screen/field per current release - verify).
- **E-file impact:** PA-40 NR e-filed with the IL-1040
- **Return lines affected:** IL-1040 Schedule CR, PA-40 NR

## EVG1017-SX7 - IL subtraction for US Treasury interest must be net of accrued interest paid; muni add-back

*Workbook tab:* 2. Diagnostics Log  |  *Category:* State Allocation  |  *Manual calc:* Yes  |  *Amount:* $9,290  |  *Procedure doc:* SALT Implications

- **CCH Axcess by default:** The IL subtraction for US obligation interest pulls 1099-INT box 3 ($9,600) in full; the $310 accrued interest paid on the Treasury note, entered as a separate negative line, is not tied to it unless flagged as US obligation interest. Out-of-state muni interest $4,800 must be identified as non-IL to be added back.
- **Axcess diagnostic:** None - silent
- **Axcess fix:** Illinois > Schedule M: US obligation subtraction $9,290 (9,600 - 310); tax-exempt interest add-back $4,800 (NY/CA/TX issuers). IL base income $346,385.
- **ProConnect by default:** Same - the state US-obligation subtraction follows the amounts flagged as US obligation interest.
- **ProConnect fix:** Illinois return > subtractions: US obligation interest 9,290; additions: out-of-state tax-exempt interest 4,800 (screen/field per current release - verify).
- **E-file impact:** None
- **Return lines affected:** IL-1040 lines 2/5, IL Schedule M

