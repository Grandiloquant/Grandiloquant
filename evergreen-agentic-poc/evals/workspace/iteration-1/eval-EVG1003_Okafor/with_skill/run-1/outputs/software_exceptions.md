# EVG1003 - Okafor - Software exception log (CCH Axcess / ProConnect)

| ID | Workbook tab | Exception | Silent? | Amount | Axcess fix (input/override location) | ProConnect fix | E-file impact |
|---|---|---|---|---:|---|---|---|
| 1 | 2 Diagnostics Log (log-only) | W-2 box 8 allocated tips would flow to Form 4137 / line 1c instead of actual diary tips | Yes | 2,900 -> 1,600 | Enter W-2 box 8 as on the form for matching, then override Form 4137 unreported tips with the diary amount (Income > Wages/Form 4137 screen - verify field path in current release) | Form 4137 input: enter actual unreported tips; override allocated-tip flow (screen/field per current release - verify) | None; attach no statement required, keep diary in file |
| 2 | 2 Diagnostics Log (log-only) | Duplicate 1099-K (re-upload) scanned twice by AutoFlow | Yes | 38,720 | Delete second 1099-K input; keep one Sch C 1099-K entry | Delete duplicate 1099-K entry | None |
| 3 | 2 Diagnostics Log (log-only) | Vehicle: client's 19,325 "business" miles include 4,180 commuting; organizer lists gas/insurance/maintenance | Yes | 4,180 mi / 6,490 | Sch C vehicle screen: business 15,145, commuting 4,180, other 4,425; standard mileage method; do not key actual expenses (verify field path) | Auto/vehicle screen: same split; leave actual expense fields blank | None |
| 4 | 2 Diagnostics Log (log-only) | Schedule 1-A qualified tips need explicit inputs; Form 4137 tips and Sch C rider tips may not flow automatically; occupation code required | Possibly | 25,000 | Sch 1-A tips input: W-2 box 7 24,600 + 4137 1,600 + Sch C tips 2,860; occupation (bartender / rideshare); verify field path and whether box 7 flows | Sch 1-A / qualified tips screen (screen/field per current release - verify) | Deduction lost if not entered |
| 5 | 8 Form 2210 safe harbor | Software needs PY tax (3,159) and PY AGI; with the PY figures the 2210 test shows no penalty; without them it may compute a penalty on 90% of 2025 tax | Yes if PY tax missing | 0 | Enter 2024 tax 3,159 / AGI 39,978 on the 2210 input; confirm estimate dates 04/14 and 06/16/2025 (not the 459 PY balance) | Form 2210 screen: prior-year tax; estimate dates | None |

**1.** Most packages flow W-2 box 8 into Form 4137 automatically. Danny's daily tip diary (adequate records) shows 1,600 of
unreported cash tips, so the 4137 is based on 1,600; Form 4137 tax 122.40 instead of 221.85.
**2.** The client uploaded the same 1099-K twice (receipt log "client uploaded again"); identical issuer, amounts, not CORRECTED.
Loading both would add 38,720 of phantom income with no diagnostic.
**3.** The software accepts whatever miles are keyed; commuting is not deductible. Entering gas/insurance alongside the
standard rate would be wrong once standard mileage is chosen.
**4.** 2025 Schedule 1-A is new; confirm how the current release sources qualified tips (box 7 vs. a separate input) so
the 4137 and rideshare tips are not missed and the 25,000 cap applies once.
**5.** Only two estimates were paid; the 100%-of-PY safe harbor is met through withholding treated as paid evenly.
