"""EVG1018 - Elena Vasquez (Single, Florida - Tampa). 100% owner of an S corp (boat repair, non-SSTB): the S corp
distributed a company truck and its accountant OMITTED the IRC 311(b) gain from the K-1 (property shown at book value);
2% shareholder health insurance; QBI with W-2 wage/UBIA data. Grandmother's trust terminated in 2025: final 1041 K-1
with in-kind distribution of a rental condo carrying suspended passive losses (IRC 469(j)(12) -> basis, not deduction)
and a long-term capital loss carryover."""
from common import ClientBuild, gotcha, fmt
from docs import statement, scanned_pages, write_text, write_xlsx
import forms as F
from tax2025 import Return1040, r

C = ClientBuild("EVG1018", "Vasquez", "Elena Vasquez")
ADDR = ("3907 W Bay Vista Ave", "Tampa, FL 33611")
T = {"name": "Elena M. Vasquez", "ssn": "XXX-XX-2741", "dob": "1983-08-27"}
REC = [T["name"], *ADDR, f"TIN: {T['ssn']}"]
SCORP = {"name": "Bayline Marine Services, Inc.", "addr1": "2210 Causeway Blvd", "addr2": "Tampa, FL 33619", "ein": "00-3318842"}
TRUST = "Rosa M. Delgado Trust u/a/d 05/14/2009"
CONDO = "1520 Gulf Blvd, Unit 12B (Gulf Palms Condominium), Clearwater, FL 33767"

# ------------------------------------------------------------------ key facts
BEG_STOCK_BASIS = 95000          # per 2024 Form 7203 (PERM)
K1_ORD_AS_ISSUED = 62000
TRUCK = {"desc": "2021 Ford F-250 XL (company truck) VIN 1FT7W2BT4MED04417", "cost": 45000, "accum_dep": 33000,
         "fmv": 32000, "date": "08/29/2025"}
TRUCK_NBV = TRUCK["cost"] - TRUCK["accum_dep"]
GAIN_311B = TRUCK["fmv"] - TRUCK_NBV
RECAPTURE_1245 = min(GAIN_311B, TRUCK["accum_dep"])          # all ordinary
K1_ORD = K1_ORD_AS_ISSUED + GAIN_311B
K1_INT = 1150
K1_CHAR = 2500
K1_NONDED = 1900
CASH_DIST = 40000
K1_W2_WAGES, K1_UBIA = 310000, 180000
HEALTH = 7800.00                  # 2% shareholder health premiums included in W-2 box 1
TR_INT, TR_DIV, TR_QDIV, TR_LTCL = 420.00, 1380.00, 1100.00, 3200
SUSP_PAL = 18400
DOD_FMV, DOD_LAND = 240000, 48000
DEP = [("2023 (placed in service 03/2023, 27.5-yr MM, 2.879%)", r((DOD_FMV - DOD_LAND) * .02879)),
       ("2024 (3.636%)", r((DOD_FMV - DOD_LAND) * .03636)),
       ("2025 through distribution 09/15/2025 (3.636% x 8.5/12)", r((DOD_FMV - DOD_LAND) * .03636 * 8.5 / 12))]
ACCUM_DEP = sum(x[1] for x in DEP)
TRUST_ADJ_BASIS = DOD_FMV - ACCUM_DEP
ELENA_CONDO_BASIS = TRUST_ADJ_BASIS + SUSP_PAL
BLDG_ADJ = DOD_FMV - DOD_LAND - ACCUM_DEP
INC_BLDG = r(SUSP_PAL * BLDG_ADJ / TRUST_ADJ_BASIS)
INC_LAND = SUSP_PAL - INC_BLDG

# ================================================================== PERM
C.write_profile(f"""
# EVG1018 - Vasquez, Elena  (PERM)

*Synthetic client - Project Evergreen training data.*

| Item | Detail |
|---|---|
| Client ID | EVG1018 |
| Taxpayer | Elena M. Vasquez, DOB 08/27/1983, SSN XXX-XX-2741 |
| Filing status | Single, no dependents |
| Address | {ADDR[0]}, {ADDR[1]} (Hillsborough County) - **Florida: no individual income tax** |
| Business | 100% shareholder, {SCORP['name']} (EIN {SCORP['ein']}), S corp since 2016, boat repair / marine mechanical (NAICS 811490 - not an SSTB). Officer W-2 + K-1 |
| S corp return | Prepared by **another firm**: Gulfside CPA Group, P.A. (contact: Mark Tillman, CPA, mtillman@gulfsidecpa.example, (813) 555-0167). We prepare the 1040 only |
| Trust | Beneficiary (1/1) of the {TRUST} - grandmother Rosa Delgado died 03/08/2023; trustee: uncle Hector Delgado. Trust terminated 2025 |
| Contact | Email elena@baylinemarine.example, cell (813) 555-0133; eSign OK |
| Engagement | Client since 2021. Quote $2,800 (1040 with S-corp K-1 basis tracking + trust K-1) |
| Payment info | Voided check on file (Suncoast Credit Union ****0917) |

## S-corp stock basis roll-forward (from our 2024 Form 7203)
| Year | Beginning | Income items | Distributions | Nonded./deductions | Ending |
|---|---|---|---|---|---|
| 2023 | 61,200 | 49,800 | (35,000) | (2,100) | 73,900 |
| 2024 | 73,900 | 58,300 | (35,000) | (2,200) | **95,000** |
No shareholder loans to the corporation (debt basis $0).
""")
F.prior_year_summary(C.perm_file("2024_Form_1040_Return_Summary.pdf", "Prior-year return summary"), "Elena Vasquez",
    "EVG1018", "Single", [
        ["1a", "W-2 wages - Bayline Marine Services, Inc. (incl. 2% shareholder health $7,500)", 88000],
        ["2b / 3b", "Interest / ordinary dividends", 1540],
        ["Sch E line 28", "Bayline Marine Services, Inc. - nonpassive ordinary income", 57200],
        ["Sch 1 line 17", "Self-employed health insurance (2% shareholder)", -7500],
        ["11", "AGI", 139240], ["12", "Standard deduction", 14600], ["13", "QBI deduction", 9940],
        ["15", "Taxable income", 114700], ["24", "Total tax", 20880], ["35a", "Refund", 520]],
    carryovers=[["Capital loss carryover", 0], ["S corp stock basis 12/31/2024 (Form 7203)", 95000]],
    notes="PY WP: 4 x $3,200 federal estimates for 2025 set up from 2024 liability. 2024 AGI < $150k -> 100% safe harbor.")
statement(C.perm_file("2024_Form_7203_Bayline_Marine.pdf", "Prior-year Form 7203"), "Form 7203 (2024) - S Corporation Shareholder Stock and Debt Basis - Bayline Marine Services, Inc.", [
    {"table": [["Line", "Description", "Amount"], ["1", "Stock basis at beginning of year", 73900], ["3a", "Ordinary business income", 57200],
               ["3b", "Interest income", 1100], ["4", "Total increases", 58300], ["6", "Distributions", 35000],
               ["8a", "Nondeductible expenses", 1400], ["8c/10", "Charitable contributions (box 12A)", 800],
               ["15", "Stock basis at end of year", 95000], ["Part II", "Debt basis", 0]], "left_align_cols": [0, 1]}])

# ================================================================== PBC
EE = {"name": T["name"], "addr1": ADDR[0], "addr2": ADDR[1], "ssn": T["ssn"]}
w2b = {"1": 90000.00, "2": 11400.00, "3": 82200.00, "4": 5096.40, "5": 82200.00, "6": 1191.90,
       "14": [("2% SH HLTH", HEALTH)], "control": "BMS-0001"}
F.organizer(C.pbc_file("01_2025_Organizer_completed.pdf", "Client organizer", "2026-03-02"), "Elena Vasquez", "EVG1018",
    general=[("Did your marital status change during 2025?", "No", ""),
             ("Did you receive any K-1s?", "Yes", "Bayline (from Mark) + Grandma's trust (final - Hector says in the summer)"),
             ("Did you receive property from a trust or estate?", "Yes", "Grandma's condo in Clearwater - deeded to me in Sept"),
             ("Did you buy or receive a vehicle?", "Yes", "Took the old company truck when Bayline bought a new one"),
             ("Do you own rental property?", "Not yet", "Will rent the condo starting 2026"),
             ("Did you make estimated tax payments?", "Yes", "4 x 3,200 (your vouchers)"),
             ("Did you receive, sell, exchange digital assets?", "No", "")],
    dependents=[],
    income_rows=[["Wages", SCORP["name"], 88000, "see W-2"],
                 ["S corp K-1", SCORP["name"], 57200, "Mark will send"],
                 ["Interest", "Suncoast Credit Union", 190, "210"],
                 ["Dividends", "Fidelity", 610, "see 1099"],
                 ["Trust K-1", TRUST, 740, "coming"]],
    deductions_rows=[["Estimated tax", "Federal", "4 x 3,200", "4 x 3,200"],
                     ["Health insurance", "paid by Bayline", 7500, "7,800"],
                     ["Charitable", "Tampa Bay Watch (through Bayline)", 800, "2,500"]],
    signature_date="02/27/2026")
F.w2(C.pbc_file("02_W-2_Bayline_Marine_Services.pdf", "Form W-2", "2026-03-02"), SCORP, EE, w2b)
F.f1099_int(C.pbc_file("03_1099-INT_Suncoast_CU.pdf", "Form 1099-INT", "2026-03-02"),
            ["Suncoast Credit Union", "6801 E Hillsborough Ave", "Tampa, FL 33610", "TIN: 00-0000613"], REC, {"1": 210.35},
            account="****0917")
F.f1099_div(C.pbc_file("04_1099-DIV_Fidelity.pdf", "Form 1099-DIV", "2026-03-02"),
            ["National Financial Services LLC (Fidelity)", "245 Summer St", "Boston, MA 02210", "TIN: 00-0000522"], REC,
            {"1a": 640.12, "1b": 520.40}, account="Z42-118830")
k1_boxes = [["1", "Ordinary business income (loss)", "", K1_ORD_AS_ISSUED], ["4", "Interest income", "", K1_INT],
            ["12", "Charitable contributions (cash, 60%)", "A", K1_CHAR], ["16", "Nondeductible expenses", "C", K1_NONDED],
            ["16", "Distributions", "D", CASH_DIST + TRUCK_NBV], ["17", "Section 199A information", "V", "STMT A"],
            ["17", "Gross receipts for section 448(c)", "AC", 2450000]]
F.k1_generic(C.pbc_file("05_K-1_1120-S_Bayline_Marine_Services.pdf", "Schedule K-1 (1120-S)", "2026-03-18", "Email from S-corp CPA"),
    "1120-S", SCORP["name"],
    [["A Corporation's EIN", SCORP["ein"]], ["B Name / address", f"{SCORP['name']}, {SCORP['addr1']}, {SCORP['addr2']}"],
     ["C IRS Center", "Ogden, UT (e-file)"], ["D Corporation's total shares", "1,000"]],
    [["E Shareholder's identifying number", T["ssn"]], ["F Shareholder", f"{T['name']}, {ADDR[0]}, {ADDR[1]}"]],
    [["G Current year allocation %", "100.000000%"], ["H Shares beginning / end", "1,000 / 1,000"],
     ["I Loans from shareholder beginning / end", "0 / 0"]],
    k1_boxes,
    supplemental=[
        {"heading": "Statement A - QBI Pass-through Entity Reporting (section 199A)",
         "table": [["Item", "Bayline Marine Services, Inc. (trade or business #1)"], ["Ordinary business income (QBI)", K1_ORD_AS_ISSUED],
                   ["W-2 wages", K1_W2_WAGES], ["UBIA of qualified property", K1_UBIA], ["SSTB?", "No"], ["Aggregated?", "No"]],
         "left_align_cols": [0]},
        {"heading": "Box 16D - Distributions detail",
         "table": [["Date", "Description", "Amount"], ["03/31/2025", "Cash", 10000], ["06/30/2025", "Cash", 10000],
                   ["09/30/2025", "Cash", 10000], ["12/19/2025", "Cash", 10000],
                   ["08/29/2025", f"Property - {TRUCK['desc']} (net book value)", TRUCK_NBV], ["", "Total box 16D", CASH_DIST + TRUCK_NBV]],
         "total_row": True},
        {"heading": "Shareholder basis",
         "para": "Shareholder is responsible for maintaining stock and debt basis (Form 7203). The corporation does not track shareholder basis."}],
    notes=["Prepared by Gulfside CPA Group, P.A. (synthetic)"])
statement(C.pbc_file("06_Bayline_Fixed_Asset_Disposal_Report_2025.pdf", "S-corp depreciation report (excerpt)", "2026-03-18",
                     "Email from S-corp CPA", "sent with K-1"),
    "Bayline Marine Services, Inc. - 2025 Asset Disposal Report (tax) - excerpt", [
        {"table": [["Asset", "Placed in service", "Cost", "Accum. depreciation", "Net book value", "Disposal date", "Proceeds", "Method"],
                   [TRUCK["desc"], "02/12/2021", TRUCK["cost"], TRUCK["accum_dep"], TRUCK_NBV, TRUCK["date"], 0,
                    "Transferred to shareholder"]]},
        {"para": "Disposal coded 'transfer to shareholder - no sale'. No Form 4797 gain recorded."}], landscape_mode=True)
statement(C.pbc_file("07_Truck_Appraisal_Tampa_Bay_Ford.pdf", "Vehicle valuation letter", "2026-03-02"),
    "Tampa Bay Ford - Vehicle Appraisal", [
        {"para": [f"Date of appraisal: 08/26/2025. Vehicle: {TRUCK['desc']}, 61,420 miles, good condition.",
                  f"Retail value $34,500; trade-in value $29,800. Fair market value (private party) as of 08/26/2025: "
                  f"<b>${TRUCK['fmv']:,.0f}</b>.", "Requested by: Elena Vasquez / Bayline Marine Services, Inc."]}])
scanned_pages(C.pbc_file("08_Title_transfer_truck_photo.pdf", "Phone photo (image)", "2026-03-02"),
    [["FLORIDA CERTIFICATE OF TITLE - TRANSFER OF TITLE BY SELLER",
      "Vehicle: 2021 FORD F-250  VIN 1FT7W2BT4MED04417",
      "Seller: BAYLINE MARINE SERVICES INC",
      "Purchaser: ELENA M VASQUEZ",
      "Selling price: $0.00  (distribution to shareholder)",
      "Date of sale/transfer: 08/29/2025      Odometer: 61,488",
      "Signed: Elena M. Vasquez, President (for seller)",
      "        Elena M. Vasquez (purchaser)"]], handwritten=False, skew=1.8, seed=18)
write_text(C.pbc_file("09_Email_Elena_2026-03-20.txt", "Client correspondence", "2026-03-20", "Email"),
"""From: Elena Vasquez <elena@baylinemarine.example>
To: preparer@evergreentax.example
Date: Fri, 20 Mar 2026 07:48:31 -0400
Subject: Bayline K-1 + trust

Hi - Mark sent the Bayline K-1 (forwarded). Grandma's trust K-1 won't be ready until summer - Hector says the
trust accountant is finishing the final return. Please file an extension.

Also - the truck I took from Bayline. Mark said since it was "just a distribution at book value" there's no tax.
The dealer said it's worth about 32k. It's my personal truck now (Bayline bought a new one in July).

The condo in Clearwater is mine now (deeded in September). I'm painting it and it'll go on the market for rent in
March 2026. Hector said there were "suspended losses" I might be able to use?
Elena
""")
statement(C.pbc_file("10_Form_4868_Extension_Confirmation.pdf", "Extension confirmation", "2026-04-13", "Internal", "e-filed by firm"),
    "Form 4868 - Application for Automatic Extension - Acknowledgement", [
        {"table": [["Item", "Value"], ["Taxpayer", T["name"]], ["Submission ID", "00118826100410XXXXX"], ["Accepted", "04/13/2026"],
                   ["Estimated total tax liability", 26200], ["Total 2025 payments", 24200], ["Amount paid with extension", 2000],
                   ["Extended due date", "10/15/2026"]], "left_align_cols": [0, 1]}])
F.k1_generic(C.pbc_file("11_K-1_1041_Delgado_Trust_DRAFT_2026-06.pdf", "Schedule K-1 (1041) - DRAFT", "2026-06-10", "Email from trustee",
                        "marked draft"),
    "1041", TRUST + " - DRAFT (subject to change)",
    [["A Trust EIN", "00-7719034"], ["B Trust name", TRUST], ["C Fiduciary", "Hector Delgado, Trustee, 881 Bayshore Blvd, Tampa FL 33606"]],
    [["E Beneficiary identifying number", T["ssn"]], ["F Beneficiary", f"{T['name']}, {ADDR[0]}, {ADDR[1]}"]],
    [["G Beneficiary type", "Individual - domestic"]],
    [["1", "Interest income", "", 410.00], ["2a", "Ordinary dividends", "", 1380.00], ["2b", "Qualified dividends", "", 1100.00],
     ["11", "Final year deductions", "E", "TBD"]],
    final=True, notes=["DRAFT - do not file. Final K-1 to follow after trustee approval."])
F.k1_generic(C.pbc_file("12_K-1_1041_Delgado_Trust_FINAL.pdf", "Schedule K-1 (1041) - final", "2026-08-21", "Email from trustee"),
    "1041", TRUST,
    [["A Trust EIN", "00-7719034"], ["B Trust name", TRUST], ["C Fiduciary", "Hector Delgado, Trustee, 881 Bayshore Blvd, Tampa FL 33606"],
     ["D Check if Form 1041-T was filed", "No"]],
    [["E Beneficiary identifying number", T["ssn"]], ["F Beneficiary", f"{T['name']}, {ADDR[0]}, {ADDR[1]}"]],
    [["G Beneficiary type", "Individual - domestic (sole remainder beneficiary, 100%)"]],
    [["1", "Interest income", "", TR_INT], ["2a", "Ordinary dividends", "", TR_DIV], ["2b", "Qualified dividends", "", TR_QDIV],
     ["11", "Final year deductions - long-term capital loss carryover", "E", TR_LTCL], ["14", "Other information", "", "See statements"]],
    final=True,
    supplemental=[
        {"heading": "Statement - Distribution of property in kind (final distribution 09/15/2025)",
         "table": [["Item", "Amount"], ["Property", CONDO], ["Trust's basis: date-of-death FMV 03/08/2023 (IRC 1014)", DOD_FMV],
                   ["  of which land", DOD_LAND], ["Accumulated depreciation claimed by trust 2023-2025", ACCUM_DEP],
                   ["Trust's adjusted basis immediately before distribution", TRUST_ADJ_BASIS],
                   ["FMV at distribution (broker opinion)", 305000], ["IRC 643(e)(3) election to recognize gain", "Not made"]],
         "left_align_cols": [0]},
        {"heading": "Statement - Passive activity (rental condominium)",
         "para": [f"The trust's rental activity (the Clearwater condominium) had suspended passive activity losses of "
                  f"<b>${SUSP_PAL:,}</b> at the date of distribution (2023 $6,900; 2024 $7,300; 2025 $4,200). "
                  "These losses are not reported in any box of this Schedule K-1. See IRC section 469(j)(12).",
                  "Tenant lease ended 06/30/2025; the unit remained held out for rent by the trustee until the distribution."]},
        {"heading": "Statement - Depreciation schedule (trust)",
         "table": [["Year", "Depreciation"]] + [[a, b] for a, b in DEP] + [["Total", ACCUM_DEP]], "total_row": True}],
    notes=["Final return of the trust. Prepared by Seaside Fiduciary Tax Services (synthetic)."])
scanned_pages(C.pbc_file("13_Trustees_Deed_Clearwater_Condo.pdf", "Legal document (scan)", "2026-08-21", "Email from trustee"),
    [["TRUSTEE'S DEED", "Prepared by: Harbor Title & Trust Law, P.A., Clearwater FL",
      "THIS TRUSTEE'S DEED made 09/15/2025 by HECTOR DELGADO, as Trustee of the",
      "ROSA M. DELGADO TRUST u/a/d 05/14/2009 (Grantor) to ELENA M. VASQUEZ,",
      "a single woman, 3907 W Bay Vista Ave, Tampa FL 33611 (Grantee).",
      "Grantor, in distribution of the trust estate and for no consideration,",
      "conveys: Unit 12B, GULF PALMS CONDOMINIUM, per Declaration OR Book 4410",
      "Page 1180, Public Records of Pinellas County, Florida.",
      "Documentary stamp tax: $0.70 (minimum - no consideration)",
      "Signed, sealed and delivered in presence of two witnesses.",
      "Recorded 09/19/2025  Pinellas County Clerk  Instr # 2025-0918XXXX"]], handwritten=False, seed=19, skew=-0.9)
statement(C.pbc_file("14_Gulf_Palms_HOA_Welcome_Letter.pdf", "Correspondence (HOA)", "2026-08-21", "Email from client"),
    "Gulf Palms Condominium Association - Welcome New Owner", [
        {"para": ["Welcome, Elena! Our records show Unit 12B transferred to you on 09/15/2025. Monthly assessments of $610 are "
                  "due on the 1st. The trust prepaid assessments through 12/31/2025.",
                  "Rental policy: minimum lease term 3 months; registration of tenants required."]}])
write_text(C.pbc_file("15_Email_thread_Gulfside_CPA_2026-08-27_to_09-02.txt", "Correspondence with S-corp CPA", "2026-09-02", "Email",
                      "cc client"),
f"""From: preparer@evergreentax.example
To: Mark Tillman <mtillman@gulfsidecpa.example>
Cc: Elena Vasquez
Date: Thu, 27 Aug 2026 10:22:05 -0400
Subject: Bayline Marine Services 2025 K-1 - property distribution (IRC 311(b))

Mark - the 2025 K-1 reports the F-250 distribution at net book value (${TRUCK_NBV:,}) in box 16D and the disposal
report shows no gain. Under IRC 311(b) the corporation recognizes gain as if it sold the truck at FMV. Using the
dealer appraisal (${TRUCK['fmv']:,}) the gain is ${GAIN_311B:,}, all section 1245 recapture (accumulated depreciation
${TRUCK['accum_dep']:,}), which should be ordinary income in box 1 (Form 4797 Part III on the 1120-S), and the box 16D
property distribution should be ${TRUCK['fmv']:,}. Can you amend the 1120-S and issue an amended K-1?

-----
From: Mark Tillman
Date: Wed, 2 Sep 2026 16:40:12 -0400
Subject: RE: Bayline Marine Services 2025 K-1 - property distribution

Agreed - we missed that when we coded the disposal. We will file an amended 1120-S (box 1 becomes ${K1_ORD:,},
16D ${CASH_DIST + TRUCK['fmv']:,}) but we can't get to it until after 10/15. Go ahead and file Elena's return
consistent with the corrected numbers.
Mark
""")

# ================================================================== RETURN
stock = [["Form 7203 - Bayline Marine Services, Inc. (EIN 00-3318842) - Part I Stock basis", "Amount"],
         ["1 Stock basis at beginning of year (2024 Form 7203)", BEG_STOCK_BASIS],
         ["3a Ordinary business income - K-1 box 1 as issued", K1_ORD_AS_ISSUED],
         ["3a Ordinary business income - IRC 311(b) gain on truck omitted from K-1 (Form 8082)", GAIN_311B],
         ["3b Interest income (box 4)", K1_INT],
         ["4 Total increases", K1_ORD + K1_INT],
         ["5 Stock basis before distributions", BEG_STOCK_BASIS + K1_ORD + K1_INT],
         [f"6 Distributions: cash {CASH_DIST:,} + truck at FMV {TRUCK['fmv']:,} (IRC 301(b)) - not NBV {TRUCK_NBV:,}", CASH_DIST + TRUCK["fmv"]],
         ["7 Stock basis after distributions (no excess -> no capital gain)", BEG_STOCK_BASIS + K1_ORD + K1_INT - CASH_DIST - TRUCK["fmv"]],
         ["8a Nondeductible expenses (box 16C)", K1_NONDED],
         ["10 Stock basis before losses and deductions", BEG_STOCK_BASIS + K1_ORD + K1_INT - CASH_DIST - TRUCK["fmv"] - K1_NONDED],
         ["Part III - charitable contributions (box 12A) - allowed (basis sufficient)", K1_CHAR],
         ["15 Stock basis at end of year", BEG_STOCK_BASIS + K1_ORD + K1_INT - CASH_DIST - TRUCK["fmv"] - K1_NONDED - K1_CHAR],
         ["Part II Debt basis", 0]]
END_BASIS = stock[-2][1]
f8082 = [["Form 8082 - Notice of Inconsistent Treatment (S corporation)", "As shown on K-1", "Reported on return", "Difference"],
         ["Box 1 ordinary business income", K1_ORD_AS_ISSUED, K1_ORD, GAIN_311B],
         ["Box 16D distributions (property at FMV)", CASH_DIST + TRUCK_NBV, CASH_DIST + TRUCK["fmv"], TRUCK["fmv"] - TRUCK_NBV],
         ["Explanation: S corp distributed a truck (FMV $32,000, adjusted basis $12,000, accumulated depreciation $33,000) to its "
          "100% shareholder on 08/29/2025. IRC 311(b)/1371(a) require the corporation to recognize $20,000 gain, all ordinary under "
          "IRC 1245. K-1 omitted the gain and reported the distribution at book value. Corporation's preparer has agreed to amend (email 09/02/2026).", "", "", ""]]
sch_e2 = [["Schedule E Part II", "Passive/nonpassive", "Nonpassive income (line 28k)"],
          [f"{SCORP['name']} (S corp, EIN {SCORP['ein']}) - material participation, basis sufficient, at-risk not applicable", "Nonpassive", K1_ORD]]
trust_ws = [["Trust termination worksheet - " + TRUST + " (final K-1)", "Amount"],
            ["Trust's adjusted basis in condo immediately before distribution (DOD FMV 240,000 - depreciation " + f"{ACCUM_DEP:,})", TRUST_ADJ_BASIS],
            ["+ Suspended passive losses allocable to the condo - IRC 469(j)(12) (NOT deductible by beneficiary or trust)", SUSP_PAL],
            ["= Elena's basis in condo (carryover basis, IRC 643(e); holding period tacks)", ELENA_CONDO_BASIS],
            [f"  Land: {DOD_LAND:,} + {INC_LAND:,} of the 469(j)(12) increase (pro rata to adjusted basis)", DOD_LAND + INC_LAND],
            [f"  Building: carryover {BLDG_ADJ:,} (continue trust's 27.5-yr recovery) + {INC_BLDG:,} increase (new 27.5-yr asset when placed in service 2026)", BLDG_ADJ + INC_BLDG],
            ["2025 Schedule E for condo", "None - not held out for rent until 2026"],
            ["Box 11 code E - long-term capital loss carryover (Schedule D line 14, 2025 = year of termination)", TR_LTCL]]

facts = {
    "status": "S",
    "taxpayer": {"age65": False},
    "w2": [{"who": "T", "box1": w2b["1"], "box2": w2b["2"], "box3": w2b["3"], "box4": w2b["4"], "box5": w2b["5"], "box6": w2b["6"]}],
    "interest": [{"payer": f"{SCORP['name']} (K-1 box 4)", "amount": K1_INT},
                 {"payer": f"{TRUST} (K-1 box 1)", "amount": TR_INT},
                 {"payer": "Suncoast Credit Union", "amount": 210.35}],
    "dividends": [{"payer": f"{TRUST} (K-1 box 2a)", "ordinary": TR_DIV, "qualified": TR_QDIV},
                  {"payer": "National Financial Services (Fidelity)", "ordinary": 640.12, "qualified": 520.40}],
    "cap_loss_co": {"st": 0, "lt": TR_LTCL},
    "sch1": {"sch_e": K1_ORD},
    "adjustments": {"se_health": HEALTH},
    "qbi": {"businesses": [{"name": "Bayline Marine Services, Inc.", "qbi": K1_ORD - HEALTH, "w2_wages": K1_W2_WAGES, "ubia": K1_UBIA}]},
    "itemized": {"real_estate_tax": 3920, "mortgage_interest_1098": 6180, "charity_cash": K1_CHAR + 400, "state_income_tax": 0},
    "estimated_payments": 4 * 3200,
    "extension_payment": 2000,
}
R = Return1040(facts).compute()
v = R.values
ITEMIZED_CHECK = v["itemized_total_computed"]
R.forms.pop("Schedule A", None)          # standard deduction used - comparison shown as an attachment instead
R.forms["Schedule D"] = [(ln, "Long-term capital loss carryover - final Schedule K-1 (Form 1041) box 11 code E (trust terminated 2025)"
                          if ln == "14" else d, a) for ln, d, a in R.forms["Schedule D"]]
cl = v.get("capital_loss_carryover_2026", {})
qbi_rows = [["Form 8995 support", "Amount"], ["K-1 box 1 as issued (Statement A QBI)", K1_ORD_AS_ISSUED],
            ["+ IRC 311(b) gain - IRC 1245 ordinary recapture (trade or business income, is QBI)", GAIN_311B],
            ["- 2% shareholder health insurance deduction attributable to the business (Reg. 1.199A-3(b)(1)(vi))", -HEALTH],
            ["= QBI", K1_ORD - HEALTH], ["W-2 wages / UBIA (not limiting - taxable income below $197,300 threshold)", f"{K1_W2_WAGES:,} / {K1_UBIA:,}"]]
C.write_return(R, [
    ("Taxpayer", "Elena M. Vasquez (XXX-XX-2741), DOB 08/27/1983"),
    ("Address", ", ".join(ADDR)),
    ("Filing status", "Single"),
    ("Digital assets question", "No"),
    ("Forms included", "1040, Schedules 1, B, D, E, Form 7203, Form 8082, Form 8995; statements"),
    ("State", "None - Florida has no individual income tax"),
    ("Extension", "Form 4868 accepted 04/13/2026 ($2,000 paid); return e-filed 09/15/2026"),
    ("Filing method", "E-file (Form 8879 signed 09/14/2026); refund direct deposit Suncoast CU ****0917"),
], attachments=[("Form 7203 - S corporation shareholder stock and debt basis", stock),
                ("Form 8082 - inconsistent treatment", f8082), ("Schedule E Part II", sch_e2),
                ("Form 8995 - QBI support", qbi_rows),
                ("Standard vs itemized", [["Comparison", "Amount"], ["Standard deduction (single)", v["standard_deduction_available"]],
                                          ["Itemized: mortgage 6,180 + real estate tax 3,920 + charity 2,900 (incl. K-1 box 12A)", ITEMIZED_CHECK],
                                          ["Even adding FL general sales tax (~1,500 table amount), itemized < standard", ""]]), ("Trust termination - basis of distributed condo", trust_ws)])

gotchas = [
    gotcha("EVG1018-G1", "Schedules K-1 - S corp IRC 311(b) property distribution", "S corp omitted the 311(b) gain on the truck",
           f"Enter the K-1 as issued: box 1 {fmt(K1_ORD_AS_ISSUED)}, property distribution at book value {fmt(TRUCK_NBV)} -> no gain.",
           f"Distribution of appreciated property = deemed sale at FMV at the corporate level (IRC 311(b), 1371(a)). Gain "
           f"{fmt(GAIN_311B)} (FMV {fmt(TRUCK['fmv'])} - adjusted basis {fmt(TRUCK_NBV)}) is all IRC 1245 recapture (accumulated depreciation "
           f"{fmt(TRUCK['accum_dep'])}) -> ordinary, flows through box 1. Manually add to the K-1 ordinary income: {fmt(K1_ORD)}.",
           f"Income understated {fmt(GAIN_311B)} (~{fmt(r(GAIN_311B * .24))} tax before QBI)", ["Sch E line 28", "Sch 1 line 5", "11"], "hard"),
    gotcha("EVG1018-G2", "Schedules K-1 - basis limitation (Section 5 line 16 other increases)", "Basis ordering with a property distribution",
           "Reduce basis by the book value (or reduce by FMV without first adding the gain) -> wrong ending basis, or a phantom "
           "excess-distribution capital gain.",
           f"Form 7203: increase stock basis by the gain first, then reduce by distributions at FMV ({fmt(CASH_DIST + TRUCK['fmv'])}); "
           f"basis before distributions {fmt(BEG_STOCK_BASIS + K1_ORD + K1_INT)} is sufficient -> no capital gain; ending basis "
           f"{fmt(END_BASIS)}. Elena's basis in the truck = FMV {fmt(TRUCK['fmv'])} (IRC 301(d)).", "Form 7203; Sch D (none)", ["7203"], "medium"),
    gotcha("EVG1018-G3", "Schedules K-1 - S corp accountant fails to reflect 311(b); Review - tax research",
           "Reporting inconsistently with the K-1 requires Form 8082",
           "Silently report different numbers from the K-1 (IRS matching / IRC 6037(c) consistency) or wait for an amended K-1 "
           "past the extended due date.",
           "Attach Form 8082 (inconsistent treatment) identifying box 1 and box 16D differences; notify the S corp's CPA to amend "
           "the 1120-S (agreed 09/02/2026). Keep the email in the WP.", "Filing compliance", ["8082"], "medium"),
    gotcha("EVG1018-G4", "QBI - ensure QBI, UBIA and W-2 wages properly reported", "QBI includes the 1245 recapture; reduced by SE health",
           "Use K-1 Statement A QBI of $62,000 (omits gain), or exclude the gain as 'not QBI', or ignore the health-insurance reduction.",
           f"IRC 1245 recapture is ordinary trade-or-business income -> QBI. QBI = {fmt(K1_ORD)} - {fmt(r(HEALTH))} 2% shareholder "
           f"health deduction = {fmt(K1_ORD - r(HEALTH))}; taxable income below $197,300 -> 20% = {fmt(v['13a'])}; W-2 wages/UBIA "
           "not limiting.", "Line 13a", ["13a"], "medium"),
    gotcha("EVG1018-G5", "Schedules K-1 (S corp) / W-2 box 14", "2% shareholder health insurance",
           "Treat the $7,800 in box 1 as ordinary wages with no deduction (or deduct it on Schedule A medical).",
           "Premiums paid by the S corp for a >2% shareholder are included in W-2 box 1 (not boxes 3/5) and deductible on Sch 1 "
           "line 17 (Notice 2008-1), limited to the S corp wages.", "Sch 1 line 17", ["10"], "easy"),
    gotcha("EVG1018-G6", "Schedules K-1 - trust termination suspended passive losses", "Trust's $18,400 suspended PAL on the distributed condo",
           f"Deduct the {fmt(SUSP_PAL)} suspended loss on Schedule E (Hector: 'you might be able to use them').",
           f"IRC 469(j)(12): on distribution of the passive activity the losses are never deductible; they increase the basis of the "
           f"distributed property. Condo basis {fmt(TRUST_ADJ_BASIS)} + {fmt(SUSP_PAL)} = {fmt(ELENA_CONDO_BASIS)} (carryover basis under "
           "IRC 643(e), no 643(e)(3) election). Record in PERM for 2026 depreciation.", "Sch E (no loss); basis memo", ["Sch E"], "hard"),
    gotcha("EVG1018-G7", "Schedules K-1 (1041) - final year items", "Trust's long-term capital loss carryover passes to beneficiary",
           "Ignore box 11 code E (not on 1099s) or treat it as a current-year K-1 loss.",
           f"Final K-1 box 11 code E {fmt(TR_LTCL)} -> Schedule D line 14 in the beneficiary's year the trust terminates (Reg. 1.642(h)-1). "
           f"Net capital loss limited to $3,000; {fmt(cl.get('total', 0))} carries to 2026.", "Line 7 / Sch D", ["7"], "medium"),
    gotcha("EVG1018-G8", "Scan - duplicate documents (draft vs final K-1)", "Draft trust K-1 in the PBC",
           "Load both the June DRAFT and August FINAL trust K-1s (double interest/dividends), or use the draft's $410 interest.",
           "Use only the FINAL K-1 (interest $420). Bookmark the draft as superseded.", "Lines 2b/3b", ["2b", "3b"], "easy"),
    gotcha("EVG1018-G9", "Schedule E / Rental Properties", "No 2025 Schedule E for the inherited-then-distributed condo",
           "Start depreciation in 2025 on stepped-up or FMV basis ($305,000), or claim the trust's 2025 depreciation again.",
           f"Not held out for rent in 2025 (painting; listed March 2026) -> no 2025 Sch E. 2026: continue trust's 27.5-yr schedule on "
           f"carryover building basis {fmt(BLDG_ADJ)} (IRC 168(i)(7)); the {fmt(INC_BLDG)} basis increase is treated as a new 27.5-yr asset "
           "(assumption). Holding period tacks.", "PERM basis record", [], "medium"),
]
C.write_answer_key(R, {"residence": "FL (no state income tax)", "complexity": "S-corp owner with 311(b) fix + final trust K-1"}, gotchas,
                   filings=[{"form": "Form 4868", "filed": "2026-04-13", "payment": 2000},
                            {"form": "Form 1040 (with Forms 7203, 8082, 8995)", "method": "e-file", "due": "2026-10-15", "filed": "2026-09-15"}],
                   extra={"s_corp_basis": {"beginning": BEG_STOCK_BASIS, "ordinary_income_corrected": K1_ORD, "gain_311b": GAIN_311B,
                                           "distributions_fmv": CASH_DIST + TRUCK["fmv"], "ending": END_BASIS},
                          "condo_basis_from_trust": {"trust_adjusted_basis": TRUST_ADJ_BASIS, "suspended_pal_added": SUSP_PAL,
                                                     "elena_basis": ELENA_CONDO_BASIS, "land": DOD_LAND + INC_LAND,
                                                     "building": BLDG_ADJ + INC_BLDG},
                          "truck_basis_to_shareholder": TRUCK["fmv"]})

C.write_receipt_log("EVG1018-1040-2025", "R. Patel (staff)", "M. Osei (senior)", "S. Kennedy, CPA", "2026-03-02",
                    extension="E-filed 04/13/2026, accepted; $2,000 paid")
tax_std_check = v["standard_deduction_available"]
C.write_notes(f"""
# EVG1018 - Vasquez, Elena - 2025 Form 1040 - Preparer Notes

*Synthetic client - Project Evergreen. Return status: **signed off; e-filed 09/15/2026 (extended), accepted.***

## Return summary
| | |
|---|---|
| Filing status | Single |
| Wages (Bayline W-2) | {fmt(v['1a'])} |
| S corp K-1 ordinary income (as corrected) | {fmt(K1_ORD)} (K-1 {fmt(K1_ORD_AS_ISSUED)} + 311(b) gain {fmt(GAIN_311B)}) |
| Capital loss (trust carryover, limited) | {fmt(v['7'])} |
| AGI (line 11) | {fmt(v['11'])} |
| Standard deduction | {fmt(v['12e'])} |
| QBI deduction | {fmt(v['13a'])} |
| Taxable income | {fmt(v['15'])} |
| Total tax | {fmt(v['24'])} |
| Payments (withholding {fmt(v['25d'])} + estimates {fmt(v['26'])} + extension $2,000) | {fmt(v['33'])} |
| **{'Refund' if v['refund'] else 'Balance due'}** | **{fmt(v['refund'] or v['balance_due'])}** |

## What I did and why (plain English)
1. **The truck (IRC 311(b)).** Bayline gave Elena its 2021 F-250 on 08/29/2025. When an S corp distributes property that is worth
   more than its tax basis, the *corporation* is treated as if it sold it at fair market value. FMV $32,000 (dealer appraisal) -
   adjusted basis $12,000 = **$20,000 gain**. Because the truck had $33,000 of depreciation, the whole gain is IRC 1245 recapture ->
   ordinary income, which passes through on K-1 box 1. Gulfside's K-1 left it out and showed the distribution at book value.
   I entered the K-1 manually with box 1 {fmt(K1_ORD)} (Section 3 direct entry) and the distribution at FMV. Mark Tillman (Gulfside)
   agreed on 09/02/2026 and will amend the 1120-S after 10/15, so I attached **Form 8082** (inconsistent treatment) to explain the
   difference from the K-1 as issued.
2. **Stock basis (Form 7203).** Increases first (income incl. the gain + interest), then distributions at FMV ($40,000 cash + $32,000
   truck = $72,000), then nondeductible expenses and the charitable item: $95,000 -> **{fmt(END_BASIS)}**. Basis was sufficient, so
   no distribution is taxable. Elena's basis in the truck is $32,000 (personal use - no deduction). Debt basis $0.
3. **2% shareholder health insurance.** W-2 box 14 shows $7,800 of premiums included in box 1 (not in boxes 3/5 - correct).
   Deducted on Schedule 1 line 17 (limited to her Bayline wages).
4. **QBI.** Boat repair is not an SSTB. QBI = {fmt(K1_ORD)} (the 1245 recapture is ordinary trade-or-business income, so it is QBI)
   less the health-insurance deduction {fmt(r(HEALTH))} = {fmt(K1_ORD - r(HEALTH))}. Taxable income before QBI is under $197,300, so the
   deduction is simply 20% = {fmt(v['13a'])}; the W-2 wages ($310,000) and UBIA ($180,000) from Statement A are recorded but not limiting.
5. **Grandmother's trust - final K-1.** Used the FINAL K-1 received 08/21/2026 (the June DRAFT with $410 interest is superseded).
   Interest $420, dividends $1,380 ($1,100 qualified).
   - **Suspended passive losses ($18,400).** The trust distributed the rental condo to Elena on 09/15/2025. Under IRC 469(j)(12)
     those losses are **not deductible** by anyone - they are added to the basis of the condo. Elena's basis = trust's adjusted basis
     {fmt(TRUST_ADJ_BASIS)} + {fmt(SUSP_PAL)} = **{fmt(ELENA_CONDO_BASIS)}** (carryover basis; no 643(e)(3) election; holding period
     includes the trust's). The $305,000 FMV is irrelevant for basis. Recorded in PERM with the land/building split.
   - **Capital loss carryover $3,200 (box 11 code E).** Passes to the beneficiary in the year the trust terminates -> Schedule D line 14.
     Net capital loss is limited to $3,000; **{fmt(cl.get('total', 0))} long-term carries to 2026**.
6. **Condo - no 2025 Schedule E.** Elena is painting it and will list it in March 2026 (HOA minimum lease 3 months - long-term rental).
   Not held out for rent in 2025, and the trust prepaid the 2025 HOA and taxes, so nothing to report. For 2026: continue the trust's
   27.5-year schedule on the carryover building basis ({fmt(BLDG_ADJ)}; IRC 168(i)(7)); treat the {fmt(INC_BLDG)} basis increase as a new
   27.5-year asset placed in service in 2026 (*assumption - no direct guidance on depreciating a 469(j)(12) increase; flagged for signer*).
7. **Standard deduction.** Itemized (home mortgage $6,180 + property tax $3,920 + charity incl. K-1 box 12A $2,500 + $400) is less
   than the $15,750 standard deduction (even adding ~$1,500 of Florida sales tax), so the K-1 charitable contribution gives no benefit this year (it still reduces basis).
8. **Payments.** 4 x $3,200 estimates + $2,000 with extension + $11,400 withholding. No Form 2210 penalty: withholding + timely
   estimates ($24,200) exceed 100% of 2024 tax ($20,880; 2024 AGI under $150,000).
9. **Not NIIT / no Additional Medicare.** S corp income is nonpassive (she runs the business); MAGI < $200,000.

## Hand-verification
- AGI: wages 90,000 + interest {v['2b']:,} + dividends {v['3b']:,} + Sch E {K1_ORD:,} - 3,000 capital loss - 7,800 health = {fmt(v['11'])}.
- Taxable income {fmt(v['15'])}: QD/CG worksheet (qualified dividends {v['3a']:,} at 15%) -> tax {fmt(v['16'])}.

## Open items / client communication
- Gulfside to file amended 1120-S / amended K-1 (box 1 {fmt(K1_ORD)}, 16D {fmt(CASH_DIST + TRUCK['fmv'])}). When received, confirm
  it matches our return - no 1040-X needed. Calendar follow-up 11/15/2026.
- Told Elena the $18,400 suspended losses are not usable, but they increase her condo basis (lower gain / higher depreciation later).
- Ask for the 2026 lease and placed-in-service date for the condo next season.

## Hand-off to signer / routing
- [x] Return locked; Accountant's Copy saved as *reviewed*
- [x] Federal 1040 - e-file; extended due date 10/15/2026 (Form 4868 accepted 04/13/2026)
- [x] Form 8082 attached (e-file compatible); no state (FL); no FBAR
- [x] eSign 8879 - email elena@baylinemarine.example
- [x] Refund direct deposit ****0917
- Billing: $2,800 quote + 1.5 hrs (311(b) research, Form 8082, trust basis memo) - external reason (S corp preparer / trust), chargeable.
""")
C.write_review_points(f"""
# Review Points - EVG1018 - 2025 - Form 1040

*Reviewer: M. Osei (blue). Preparer responses in red. Synthetic.*

1. **Sch E Part II / K-1 Bayline** - Draft entered box 1 {fmt(K1_ORD_AS_ISSUED)} and the truck at NBV $12,000. The disposal report shows a
   truck with $33,000 of depreciation distributed to the shareholder with no gain. IRC 311(b) - the S corp recognizes gain at FMV.
   - Get support for FMV (dealer appraisal in PBC: $32,000). Gain $20,000, all 1245 -> box 1.
   - Contact Gulfside (draft email to me first) re amending.
   - *Preparer: Email sent 08/27 after your OK; Mark agreed 09/02. Box 1 now {fmt(K1_ORD)}; Form 8082 attached.*
2. **Form 7203** - Draft reduced basis by $12,000 for the truck. Distribution is FMV; gain increases basis before distributions.
   - *Preparer: Corrected; ending basis {fmt(END_BASIS)}; no excess distribution.*
3. **Form 8995** - QBI must include the $20,000 recapture and be reduced by the 2% shareholder health deduction.
   - *Preparer: QBI {fmt(K1_ORD - r(HEALTH))}; deduction {fmt(v['13a'])}.*
4. **Trust K-1** - Draft used the June DRAFT K-1. Replace with FINAL (08/21).
   - *Preparer: Done; draft bookmarked "superseded - do not use".*
5. **Trust K-1 statement** - Draft entered the $18,400 suspended losses as a Schedule E loss. Not allowed - IRC 469(j)(12). Add to condo basis in PERM.
   - *Preparer: Removed. Basis memo in PERM: {fmt(ELENA_CONDO_BASIS)}.*
6. **Schedule D** - Box 11 code E LT capital loss carryover $3,200 missing.
   - *Preparer: Added to Sch D line 14; $200 carryforward to 2026.*
7. FYI - Sch 1 line 17 health insurance for 2% shareholders: confirm the premiums are in box 1 and not in boxes 3/5 (they are).
""")
print("EVG1018 done", R.summary()["11"], R.summary()["15"], R.summary()["24"], v["refund"], v["balance_due"])
