"""
Project Evergreen - Tax Year 2025 federal computation engine.

Deterministic calculator used to generate the "answer key" returns for the
synthetic client data set. It is NOT a full tax engine: client build scripts
make the preparer judgement calls (e.g. passive-loss limits, basis fixes,
disallowed deductions) and hand the engine the correct inputs; the engine then
does the arithmetic consistently (brackets, tax table, cap-gain worksheet,
SE tax, NIIT, Additional Medicare, AMT, CTC/ACTC, EITC, education, 2441,
Schedule 1-A OBBBA deductions, standard vs itemized, QBI).

All 2025 figures reflect Rev. Proc. 2024-40 as modified by P.L. 119-21
(One Big Beautiful Bill Act, "OBBBA").
"""
from __future__ import annotations

import math
from collections import OrderedDict

# --------------------------------------------------------------------------
# 2025 constants
# --------------------------------------------------------------------------
STD_DED = {"S": 15750, "MFJ": 31500, "MFS": 15750, "HOH": 23625, "QSS": 31500}   # OBBBA
ADD_STD = {"S": 2000, "HOH": 2000, "MFJ": 1600, "MFS": 1600, "QSS": 1600}
DEP_STD_MIN, DEP_STD_EARNED_ADD = 1350, 450

BRACKETS = {
    "S":   [(11925, .10), (48475, .12), (103350, .22), (197300, .24), (250525, .32), (626350, .35), (math.inf, .37)],
    "MFJ": [(23850, .10), (96950, .12), (206700, .22), (394600, .24), (501050, .32), (751600, .35), (math.inf, .37)],
    "MFS": [(11925, .10), (48475, .12), (103350, .22), (197300, .24), (250525, .32), (375800, .35), (math.inf, .37)],
    "HOH": [(17000, .10), (64850, .12), (103350, .22), (197300, .24), (250500, .32), (626350, .35), (math.inf, .37)],
}
BRACKETS["QSS"] = BRACKETS["MFJ"]
LTCG_0 = {"S": 48350, "MFJ": 96700, "MFS": 48350, "HOH": 64750, "QSS": 96700}
LTCG_15 = {"S": 533400, "MFJ": 600050, "MFS": 300000, "HOH": 566700, "QSS": 600050}

SS_WAGE_BASE = 176100
ADDL_MED_THRESH = {"S": 200000, "HOH": 200000, "QSS": 200000, "MFJ": 250000, "MFS": 125000}
NIIT_THRESH = {"S": 200000, "HOH": 200000, "QSS": 250000, "MFJ": 250000, "MFS": 125000}

QBI_THRESH = {"S": 197300, "HOH": 197300, "QSS": 197300, "MFS": 197300, "MFJ": 394600}
QBI_RANGE = {"S": 50000, "HOH": 50000, "QSS": 50000, "MFS": 50000, "MFJ": 100000}  # 2025 (OBBBA widens from 2026)

SALT_CAP, SALT_CAP_MFS = 40000, 20000              # OBBBA 2025
SALT_PHASE_START, SALT_PHASE_START_MFS = 500000, 250000
SALT_FLOOR, SALT_FLOOR_MFS = 10000, 5000

AMT_EXEMPT = {"S": 88100, "HOH": 88100, "MFJ": 137000, "QSS": 137000, "MFS": 68500}
AMT_PHASEOUT = {"S": 626350, "HOH": 626350, "MFJ": 1252700, "QSS": 1252700, "MFS": 626350}
AMT_28_BREAK = {"S": 239100, "HOH": 239100, "MFJ": 239100, "QSS": 239100, "MFS": 119550}

CTC_PER_CHILD, ACTC_MAX, ODC = 2200, 1700, 500     # OBBBA 2025
CTC_PHASE = {"MFJ": 400000}                        # others 200,000

EITC = {  # kids: (phase-in rate, earned amt, max credit, phaseout rate, begin single, begin MFJ)
    0: (.0765, 8490, 649, .0765, 10620, 17730),
    1: (.34, 12730, 4328, .1598, 23350, 30470),
    2: (.40, 17880, 7152, .2106, 23350, 30470),
    3: (.45, 17880, 8046, .2106, 23350, 30470),
}
EITC_INVEST_LIMIT = 11950

SENIOR_DED, SENIOR_PHASE = 6000, {"MFJ": 150000}   # others 75,000
TIPS_MAX, OT_MAX, OT_MAX_MFJ = 25000, 12500, 25000
TIPS_OT_PHASE = {"MFJ": 300000}                    # others 150,000
CAR_INT_MAX, CAR_PHASE = 10000, {"MFJ": 200000}    # others 100,000

MED_FLOOR = .075
SE_FACTOR = .9235
MILEAGE_2025 = .70
KIDDIE_THRESH = 2700


def r(x: float) -> int:
    """IRS whole-dollar rounding (half up)."""
    return int(math.floor(x + 0.5)) if x >= 0 else -int(math.floor(-x + 0.5))


def _phase(status, table, default):
    return table.get(status, default)


# --------------------------------------------------------------------------
# Rate helpers
# --------------------------------------------------------------------------
def schedule_tax(ti: float, status: str) -> float:
    tax, lo = 0.0, 0.0
    for top, rate in BRACKETS[status]:
        if ti <= lo:
            break
        tax += (min(ti, top) - lo) * rate
        lo = top
    return tax


def marginal_integral(lo: float, hi: float, status: str, cap: float) -> float:
    """Tax on the slice [lo, hi] at ordinary marginal rates, each rate capped at `cap`."""
    tax, prev = 0.0, 0.0
    for top, rate in BRACKETS[status]:
        a, b = max(lo, prev), min(hi, top)
        if b > a:
            tax += (b - a) * min(rate, cap)
        prev = top
    return tax


def table_tax(ti: float, status: str) -> int:
    """2025 Tax Table (income under $100,000) or Tax Computation Worksheet."""
    if ti <= 0:
        return 0
    if ti >= 100000:
        return r(schedule_tax(ti, status))
    if ti < 5:
        return 0
    if ti < 15:
        mid = 10
    elif ti < 25:
        mid = 20
    elif ti < 3000:
        lo = 25 * math.floor(ti / 25)
        mid = lo + 12.5
    else:
        lo = 50 * math.floor(ti / 50)
        mid = lo + 25
    return r(schedule_tax(mid, status))


def tax_with_prefs(ti, status, qd=0, ncg=0, g28=0, u1250=0, ordinary_fn=None, amt=False):
    """Qualified Dividends & Capital Gain / Schedule D Tax Worksheet logic.
    ncg = net capital gain (min of Sch D 15 and 16, >=0); g28 = 28% rate gain; u1250 = unrecaptured 1250.
    Returns (tax, detail dict)."""
    ordinary_fn = ordinary_fn or table_tax
    ti = max(0, ti)
    pref_total = min(ti, max(0, qd) + max(0, ncg))
    r28 = min(max(0, g28), max(0, ncg))
    r25 = min(max(0, u1250), max(0, ncg) - r28)
    base = max(0, pref_total - r28 - r25)
    # if prefs exceed TI, the reduction comes out of the 25/28 buckets last
    ordinary = ti - pref_total
    if pref_total == 0:
        t = ordinary_fn(ti, status)
        return t, {"ordinary": ti, "pref": 0, "tax": t, "method": "table/schedule"}
    below = ordinary + r25 + r28
    t0 = LTCG_0[status]
    t15 = LTCG_15[status]
    p0 = max(0, min(base, t0 - ordinary - r25 - r28)) if below < t0 else 0
    p15 = max(0, min(base - p0, t15 - max(below, t0) if below < t15 else 0))
    p15 = max(0, min(base - p0, max(0, t15 - max(below + p0, t0))))
    p20 = base - p0 - p15
    t_ord = ordinary_fn(ordinary, status)
    t25 = marginal_integral(ordinary, ordinary + r25, status, .25) if r25 else 0
    t28 = marginal_integral(ordinary + r25, ordinary + r25 + r28, status, .28) if r28 else 0
    t = t_ord + t25 + t28 + p15 * .15 + p20 * .20
    regular = ordinary_fn(ti, status)
    total = r(min(t, regular))
    return total, {"ordinary_portion": ordinary, "qualified_div_and_ncg": pref_total, "at_0pct": p0,
                   "at_15pct": p15, "at_20pct": p20, "unrecaptured_1250": r25, "rate_28_gain": r28,
                   "tax_on_ordinary": t_ord, "tax": total, "regular_tax_on_all_TI": regular}


# --------------------------------------------------------------------------
# Component calculators (usable standalone by client scripts)
# --------------------------------------------------------------------------
def se_tax(net_profit: float, w2_ss_wages: float = 0.0, church=False):
    """Schedule SE (one person). Returns dict."""
    base = net_profit * SE_FACTOR if net_profit > 0 else 0
    if base < 400:
        return {"net_earnings": 0, "ss_part": 0, "medicare_part": 0, "se_tax": 0, "half": 0}
    ss_room = max(0, SS_WAGE_BASE - w2_ss_wages)
    ss = min(base, ss_room) * .124
    med = base * .029
    tot = r(ss + med)
    return {"net_earnings": r(base), "ss_part": r(ss), "medicare_part": r(med), "se_tax": tot,
            "half": r(tot / 2)}


def taxable_ss(benefits: float, other_income: float, tax_exempt_int: float, adjustments_ex_sl: float, status: str,
               lived_with_spouse_mfs=False):
    """Social Security Benefits Worksheet (Form 1040 instructions)."""
    if benefits <= 0:
        return 0
    l2 = benefits * .5
    l3 = other_income + tax_exempt_int  # income lines 1z,2b,3b,4b,5b,7,8
    l5 = l2 + l3 - adjustments_ex_sl
    if status == "MFS" and lived_with_spouse_mfs:
        return r(min(l5 * .85, benefits * .85)) if l5 > 0 else 0
    base1 = 32000 if status == "MFJ" else 25000
    base2 = 12000 if status == "MFJ" else 9000
    if l5 <= base1:
        return 0
    l9 = l5 - base1
    l11 = max(0, l9 - base2)
    l12 = min(l9, base2)
    l13 = l12 / 2
    l14 = min(l2, l13)
    l15 = l11 * .85
    l16 = l14 + l15
    return r(min(l16, benefits * .85))


def eitc(kids: int, earned: float, agi: float, status: str, invest_income: float = 0):
    kids = min(kids, 3)
    if invest_income > EITC_INVEST_LIMIT or status == "MFS" and False:
        return 0
    rin, e_amt, mx, rout, b_s, b_j = EITC[kids]
    begin = b_j if status == "MFJ" else b_s

    def cr(x):
        if x <= 0:
            return 0
        mid = 50 * math.floor(x / 50) + 25 if x >= 1 else 0.5
        c = min(rin * mid, mx)
        c -= max(0, mid - begin) * rout
        return max(0, r(c))
    c1 = cr(earned)
    if agi >= begin and agi != earned:
        c1 = min(c1, cr(agi))
    return c1


def dependent_care_credit(expenses: float, n_qual: int, agi: float, earned_t: float, earned_s: float | None,
                          employer_benefits: float = 0, status="S"):
    """Form 2441 (2025 rules). Returns dict incl. taxable benefits (line 26) and credit before tax limit."""
    excl_limit = 2500 if status == "MFS" else 5000
    min_earned = earned_t if earned_s is None else min(earned_t, earned_s)
    exclusion = min(employer_benefits, excl_limit, expenses, min_earned)
    taxable_benefits = max(0, employer_benefits - exclusion)
    cap = 3000 if n_qual == 1 else 6000 if n_qual >= 2 else 0
    # Part III: credit base = smaller of (expenses not reimbursed by excluded benefits) and (cap - exclusion),
    # further limited by earned income (Part I lines 4-5)
    allowed = max(0, min(expenses - exclusion, cap - exclusion, min_earned - exclusion)) if cap - exclusion > 0 else 0
    pct = .35
    if agi > 15000:
        steps = math.ceil((agi - 15000) / 2000)
        pct = max(.20, .35 - .01 * steps)
    return {"employer_benefits": employer_benefits, "exclusion": r(exclusion), "taxable_benefits": r(taxable_benefits),
            "qualified_expenses_allowed": r(allowed), "pct": pct, "credit": r(allowed * pct)}


def education_credits(students, magi, status):
    """students: list of dicts {name, type:'AOTC'|'LLC', qualified_expenses}. Returns dict."""
    lo, hi = (160000, 180000) if status == "MFJ" else (80000, 90000)
    if status == "MFS":
        return {"aotc_total": 0, "refundable": 0, "nonrefundable_aotc": 0, "llc": 0, "phase_fraction": 0}
    frac = 1 if magi <= lo else 0 if magi >= hi else (hi - magi) / (hi - lo)
    aotc = 0
    llc_exp = 0
    detail = []
    for s in students:
        if s["type"] == "AOTC":
            q = min(s["qualified_expenses"], 4000)
            a = min(q, 2000) + max(0, q - 2000) * .25
            aotc += a
            detail.append((s["name"], "AOTC", s["qualified_expenses"], a))
        else:
            llc_exp += s["qualified_expenses"]
            detail.append((s["name"], "LLC", s["qualified_expenses"], None))
    aotc_allowed = r(aotc * frac) if frac < 1 else r(aotc)
    if frac < 1:
        aotc_allowed = r(aotc * round(frac, 3))
    refundable = r(aotc_allowed * .40)
    llc = r(min(llc_exp, 10000) * .20 * (round(frac, 3) if frac < 1 else 1))
    return {"aotc_tentative": r(aotc), "phase_fraction": round(frac, 3), "aotc_total": aotc_allowed,
            "refundable": refundable, "nonrefundable_aotc": aotc_allowed - refundable, "llc": llc, "detail": detail}


def macrs_residential(cost_basis: float, month_placed: int, year_index: int) -> int:
    """27.5-year SL mid-month. year_index 1 = placed-in-service year."""
    annual = cost_basis / 27.5
    if year_index == 1:
        return r(annual * (12 - month_placed + 0.5) / 12)
    return r(annual)


MACRS_HY = {5: [.20, .32, .192, .1152, .1152, .0576], 7: [.1429, .2449, .1749, .1249, .0893, .0892, .0893, .0446]}


# --------------------------------------------------------------------------
# The return
# --------------------------------------------------------------------------
class Return1040:
    """Collects forms/lines. Call .compute() after inputs are set."""

    def __init__(self, f: dict):
        self.f = f
        self.status = f["status"]
        self.forms: "OrderedDict[str, list]" = OrderedDict()
        self.values: dict = {}
        self.notes: list = []

    # ---- output helpers
    def line(self, form, ln, desc, amt, key=None):
        self.forms.setdefault(form, []).append((ln, desc, amt))
        if key:
            self.values[key] = amt
        return amt

    def g(self, k, d=0):
        return self.f.get(k, d)

    # ---- main
    def compute(self):
        f, st = self.f, self.status
        mfj = st == "MFJ"
        w2 = f.get("w2", [])

        # ================= INCOME =====================================
        wages = sum(x.get("box1", 0) for x in w2)
        dc = f.get("dependent_care")
        dc_res = None
        earned_t = sum(x.get("box1", 0) for x in w2 if x.get("who", "T") == "T") + f.get("se_earned_T", 0)
        earned_s = sum(x.get("box1", 0) for x in w2 if x.get("who") == "S") + f.get("se_earned_S", 0) if mfj else None
        if dc:
            earned_t += dc.get("extra_earned_T", 0)
            if mfj:
                earned_s += dc.get("extra_earned_S", 0)
        dcb = sum(x.get("box10", 0) for x in w2)
        l1a = self.line("Form 1040", "1a", "Total amount from Form(s) W-2, box 1", r(wages), "1a")
        l1b = self.line("Form 1040", "1b", "Household employee wages not reported on Form(s) W-2", r(f.get("hh_wages_no_w2", 0)))
        l1c = self.line("Form 1040", "1c", "Tip income not reported on line 1a (Form 4137)", r(f.get("unreported_tips", 0)), "1c")
        l1e = 0
        self._dc_pending = (dc, dcb, earned_t, earned_s)
        # taxable dependent care benefits need AGI only for credit %, exclusion is independent of AGI
        if dcb:
            tmp = dependent_care_credit(dc["expenses"] if dc else 0, dc["n_qual"] if dc else 0, 0, earned_t,
                                        earned_s, dcb, st)
            l1e = tmp["taxable_benefits"]
        l1e = self.line("Form 1040", "1e", "Taxable dependent care benefits (Form 2441, line 26)", l1e)
        l1h = self.line("Form 1040", "1h", "Other earned income", r(f.get("other_earned", 0)))
        l1z = self.line("Form 1040", "1z", "Add lines 1a through 1h", l1a + l1b + l1c + l1e + l1h, "1z")

        # Schedule B
        ints = f.get("interest", [])
        divs = f.get("dividends", [])
        taxable_int = r(sum(x.get("amount", 0) for x in ints))
        exempt_int = r(sum(x.get("tax_exempt", 0) for x in ints) + sum(x.get("exempt_int_div", 0) for x in divs))
        ord_div = r(sum(x.get("ordinary", 0) for x in divs))
        qual_div = r(sum(x.get("qualified", 0) for x in divs))
        if ints or divs:
            for i, x in enumerate(ints):
                self.line("Schedule B", f"1.{i+1}", x["payer"], r(x.get("amount", 0)))
            self.line("Schedule B", "2", "Total interest", taxable_int)
            self.line("Schedule B", "4", "Taxable interest (to Form 1040, line 2b)", taxable_int)
            for i, x in enumerate(divs):
                self.line("Schedule B", f"5.{i+1}", x["payer"], r(x.get("ordinary", 0)))
            self.line("Schedule B", "6", "Ordinary dividends (to Form 1040, line 3b)", ord_div)
            fa = f.get("foreign_accounts", False)
            self.line("Schedule B", "7a", "Foreign financial account at any time in 2025? / FBAR required?",
                      "Yes / Yes" if fa else "No")
            if fa:
                self.line("Schedule B", "7b", "Country", f.get("foreign_account_country", ""))
            self.line("Schedule B", "8", "Grantor of / transferor to a foreign trust?", "Yes" if f.get("foreign_trust") else "No")
        self.line("Form 1040", "2a", "Tax-exempt interest", exempt_int, "2a")
        l2b = self.line("Form 1040", "2b", "Taxable interest", taxable_int, "2b")
        l3a = self.line("Form 1040", "3a", "Qualified dividends", qual_div, "3a")
        l3b = self.line("Form 1040", "3b", "Ordinary dividends", ord_div, "3b")

        iras = f.get("ira", [])
        pens = f.get("pension", [])
        l4a = self.line("Form 1040", "4a", "IRA distributions", r(sum(x["gross"] for x in iras)), "4a")
        l4b = self.line("Form 1040", "4b", "IRA distributions - taxable amount", r(sum(x["taxable"] for x in iras)), "4b")
        l5a = self.line("Form 1040", "5a", "Pensions and annuities", r(sum(x["gross"] for x in pens)), "5a")
        l5b = self.line("Form 1040", "5b", "Pensions and annuities - taxable amount", r(sum(x["taxable"] for x in pens)), "5b")

        # Capital gains (Schedule D)
        l7 = self._schedule_d()

        # Schedule 1 part I
        s1 = f.get("sch1", {})
        s1_items = [
            ("1", "Taxable refunds, credits, or offsets of state and local income taxes", "taxable_refunds"),
            ("2a", "Alimony received (pre-2019 instrument)", "alimony"),
            ("3", "Business income or (loss) - Schedule C", "sch_c"),
            ("4", "Other gains or (losses) - Form 4797", "f4797"),
            ("5", "Rental real estate, royalties, partnerships, S corps, trusts - Schedule E", "sch_e"),
            ("6", "Farm income or (loss)", "farm"),
            ("7", "Unemployment compensation", "unemployment"),
        ]
        tot1 = 0
        for ln, d, k in s1_items:
            v = r(s1.get(k, 0))
            if v:
                self.line("Schedule 1", ln, d, v)
            tot1 += v
        self.values["sch1_business"] = r(s1.get("sch_c", 0))
        self.values["sch1_sch_e"] = r(s1.get("sch_e", 0))
        other = s1.get("other", [])  # list of (line, desc, amt)
        tot_other = 0
        for ln, d, v in other:
            self.line("Schedule 1", ln, d, r(v))
            tot_other += r(v)
        if other:
            self.line("Schedule 1", "9", "Total other income", tot_other)
        s1_10 = tot1 + tot_other
        if s1_10 or other or any(s1.get(k) for _, _, k in s1_items):
            self.line("Schedule 1", "10", "Additional income (to Form 1040, line 8)", s1_10)
        l8 = self.line("Form 1040", "8", "Additional income from Schedule 1, line 10", s1_10, "8")

        # Social security
        ssa = f.get("ssa", [])
        ss_ben = r(sum(x["net_benefits"] for x in ssa))
        adj = f.get("adjustments", {})
        # adjustments (other than student loan interest) needed for SS worksheet
        se_list = f.get("se", [])  # [{who, net_profit, w2_ss_wages}]
        se_results = []
        for s in se_list:
            res = se_tax(s["net_profit"], s.get("w2_ss_wages", 0))
            res["who"] = s.get("who", "T")
            se_results.append(res)
        half_se = sum(x["half"] for x in se_results)
        adj_items = [
            ("11", "Educator expenses", "educator"),
            ("13", "Health savings account deduction (Form 8889)", "hsa"),
            ("15", "Deductible part of self-employment tax (Schedule SE)", "__halfse"),
            ("16", "Self-employed SEP, SIMPLE, and qualified plans", "sep"),
            ("17", "Self-employed health insurance deduction", "se_health"),
            ("18", "Penalty on early withdrawal of savings", "early_wd_penalty"),
            ("19a", "Alimony paid (pre-2019 instrument)", "alimony_paid"),
            ("20", "IRA deduction", "ira_ded"),
            ("21", "Student loan interest deduction", "student_loan"),
        ]
        adj_vals = {}
        for ln, d, k in adj_items:
            v = half_se if k == "__halfse" else r(adj.get(k, 0))
            adj_vals[k] = v
        adj_other = adj.get("other", [])  # (line, desc, amt)
        # student loan interest phase-out needs MAGI; compute preliminary
        total_income_ex_ss = l1z + l2b + l3b + l4b + l5b + l7 + l8
        adj_ex_sl = sum(v for k, v in adj_vals.items() if k != "student_loan") + sum(r(a[2]) for a in adj_other)
        l6a = self.line("Form 1040", "6a", "Social security benefits", ss_ben, "6a")
        l6b = taxable_ss(ss_ben, total_income_ex_ss, exempt_int, adj_ex_sl, st) if ss_ben else 0
        if f.get("ss_taxable_override") is not None:
            l6b = f["ss_taxable_override"]
        l6b = self.line("Form 1040", "6b", "Social security benefits - taxable amount", l6b, "6b")
        l7 = self.line("Form 1040", "7", "Capital gain or (loss) (Schedule D)", l7, "7")
        l9 = self.line("Form 1040", "9", "Total income", total_income_ex_ss + l6b, "9")

        # student loan interest phase-out (2025: 85k-100k single, 170k-200k MFJ)
        if adj.get("student_loan"):
            magi = l9 - adj_ex_sl
            lo, width = (170000, 30000) if mfj else (85000, 15000)
            sl = min(2500, adj["student_loan"])
            if magi > lo:
                sl = sl - sl * min(1, (magi - lo) / width)
            adj_vals["student_loan"] = r(sl)
        tot_adj = 0
        for ln, d, k in adj_items:
            v = adj_vals[k]
            if v:
                self.line("Schedule 1", ln, d, v)
            tot_adj += v
        for ln, d, v in adj_other:
            self.line("Schedule 1", ln, d, r(v))
            tot_adj += r(v)
        if tot_adj:
            self.line("Schedule 1", "26", "Total adjustments to income (to Form 1040, line 10)", tot_adj)
        l10 = self.line("Form 1040", "10", "Adjustments to income from Schedule 1, line 26", tot_adj, "10")
        agi = self.line("Form 1040", "11", "Adjusted gross income", l9 - l10, "11")
        self.agi = agi

        # ================= DEDUCTIONS =================================
        std = self._standard_deduction()
        itemized = self._schedule_a(agi) if f.get("itemized") else None
        force = f.get("force_itemize", False)
        if itemized is not None and (itemized > std or force):
            ded = itemized
            self.values["deduction_type"] = "Itemized (Schedule A)"
        else:
            ded = std
            self.values["deduction_type"] = "Standard"
            if itemized is not None:
                self.notes.append(f"Itemized deductions ${itemized:,} < standard deduction ${std:,}; standard deduction used.")
                # Schedule A is not filed - keep it only as a labelled comparison workpaper
                self.forms["Itemized vs. standard comparison (Schedule A not filed)"] = self.forms.pop("Schedule A")
        self.values["standard_deduction_available"] = std
        self.values["itemized_total_computed"] = itemized
        l12 = self.line("Form 1040", "12e", f"Standard deduction or itemized deductions ({self.values['deduction_type']})", ded, "12e")

        # QBI
        # Schedule 1-A (computed first: QBI's taxable-income limit is figured after these deductions)
        s1a = self._schedule_1a(agi)
        ti_before_qbi = max(0, agi - ded - s1a)
        qbi = self._qbi(ti_before_qbi)
        l13a = self.line("Form 1040", "13a", "Qualified business income deduction (Form 8995/8995-A)", qbi, "13a")
        l13b = self.line("Form 1040", "13b", "Additional deductions from Schedule 1-A, line 38", s1a, "13b")
        l14 = self.line("Form 1040", "14", "Add lines 12e, 13a, and 13b", l12 + l13a + l13b)
        ti = self.line("Form 1040", "15", "Taxable income", max(0, agi - l14), "15")
        self.ti = ti

        # ================= TAX =======================================
        if f.get("kiddie_8615"):
            tax, det = self._form_8615(ti)
        else:
            tax, det = self._regular_tax(ti)
        self.tax_detail = det
        extra_16 = r(f.get("form_8814_tax", 0))
        label = " (incl. Form 8814 child tax)" if extra_16 else ""
        for desc, amt in f.get("line16_other", []):   # e.g. section 962 election tax, Form 4970 - per attached statement
            extra_16 += r(amt)
            self.line("Line 16 statement", desc, desc, r(amt))
            label += f" (incl. {desc})"
        if extra_16:
            self.line("Line 16 statement", "regular", "Regular tax on taxable income (tax table / worksheets)", tax)
        l16 = self.line("Form 1040", "16", "Tax" + label, tax + extra_16, "16")

        # Schedule 2 Part I
        amt = self._amt(ti, ded, tax) if f.get("amt") else 0
        aptc = r(f.get("excess_aptc", 0))
        s2_3 = amt + aptc
        if amt:
            self.line("Schedule 2", "1", "Alternative minimum tax (Form 6251)", amt)
        if aptc:
            self.line("Schedule 2", "2", "Excess advance premium tax credit repayment (Form 8962)", aptc)
        if s2_3:
            self.line("Schedule 2", "3", "Total Part I (to Form 1040, line 17)", s2_3)
        l17 = self.line("Form 1040", "17", "Amount from Schedule 2, line 3", s2_3, "17")
        l18 = self.line("Form 1040", "18", "Add lines 16 and 17", l16 + l17, "18")

        # nonrefundable credits (Schedule 3 Part I) - computed before CTC per 8812 ordering
        s3 = self._schedule3_nonref(agi, l18)
        # CTC / ODC
        ctc_nonref, actc = self._ctc(agi, l18 - s3["before_ctc"], l1z)
        l19 = self.line("Form 1040", "19", "Child tax credit / credit for other dependents (Schedule 8812)", ctc_nonref, "19")
        # remaining nonref credits after CTC (energy credits etc. limited)
        s3_8 = self._finish_schedule3_nonref(s3, l18 - ctc_nonref)
        l20 = self.line("Form 1040", "20", "Amount from Schedule 3, line 8", s3_8, "20")
        l21 = self.line("Form 1040", "21", "Add lines 19 and 20", l19 + l20)
        l22 = self.line("Form 1040", "22", "Subtract line 21 from line 18", max(0, l18 - l21), "22")

        # Schedule 2 Part II other taxes
        l23 = self._schedule2_other(agi, se_results, w2)
        l23 = self.line("Form 1040", "23", "Other taxes, including self-employment tax, from Schedule 2, line 21", l23, "23")
        l24 = self.line("Form 1040", "24", "Total tax", l22 + l23, "24")

        # ================= PAYMENTS ==================================
        wh_w2 = r(sum(x.get("box2", 0) for x in w2))
        wh_1099 = r(f.get("withholding_1099", 0))
        wh_other = r(self.values.get("addl_medicare_withheld", 0)) + r(f.get("withholding_other", 0))
        self.line("Form 1040", "25a", "Federal income tax withheld - Form(s) W-2", wh_w2, "25a")
        self.line("Form 1040", "25b", "Federal income tax withheld - Form(s) 1099", wh_1099, "25b")
        self.line("Form 1040", "25c", "Federal income tax withheld - other forms (incl. Form 8959 line 24)", wh_other, "25c")
        l25d = self.line("Form 1040", "25d", "Total withholding", wh_w2 + wh_1099 + wh_other, "25d")
        est = r(f.get("estimated_payments", 0))
        l26 = self.line("Form 1040", "26", "2025 estimated tax payments and amount applied from 2024 return", est, "26")
        eic = self._eic(agi, l1z) if f.get("eic_eligible") else 0
        l27 = self.line("Form 1040", "27a", "Earned income credit (EIC)", eic, "27a")
        l28 = self.line("Form 1040", "28", "Additional child tax credit (Schedule 8812)", actc, "28")
        l29 = self.line("Form 1040", "29", "American opportunity credit - refundable (Form 8863, line 8)",
                        self.values.get("aotc_refundable", 0), "29")
        s3_15 = self._schedule3_ref(w2)
        l31 = self.line("Form 1040", "31", "Amount from Schedule 3, line 15", s3_15, "31")
        l32 = self.line("Form 1040", "32", "Total other payments and refundable credits", l27 + l28 + l29 + l31, "32")
        l33 = self.line("Form 1040", "33", "Total payments", l25d + l26 + l32, "33")
        over = l33 - l24
        apply_next = 0
        if over > 0:
            self.line("Form 1040", "34", "Amount overpaid", over, "34")
            apply_next = min(over, r(f.get("apply_to_2026", 0)))
            self.line("Form 1040", "35a", "Refund", over - apply_next, "35a")
            if apply_next:
                self.line("Form 1040", "36", "Amount applied to 2026 estimated tax", apply_next, "36")
            self.line("Form 1040", "37", "Amount you owe", 0, "37")
        else:
            self.line("Form 1040", "34", "Amount overpaid", 0, "34")
            self.line("Form 1040", "35a", "Refund", 0, "35a")
            self.line("Form 1040", "37", "Amount you owe", -over, "37")
        pen = r(f.get("es_penalty", 0))
        self.line("Form 1040", "38", "Estimated tax penalty (Form 2210)", pen, "38")
        self.values["refund"] = max(0, over - apply_next)
        self.values["balance_due"] = max(0, -over) + pen
        self._reorder_1040()
        return self

    # ---------------------------------------------------------------
    def _reorder_1040(self):
        order = ["1a", "1b", "1c", "1e", "1h", "1z", "2a", "2b", "3a", "3b", "4a", "4b", "5a", "5b", "6a", "6b", "7",
                 "8", "9", "10", "11", "12e", "13a", "13b", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23",
                 "24", "25a", "25b", "25c", "25d", "26", "27a", "28", "29", "31", "32", "33", "34", "35a", "36", "37", "38"]
        lines = self.forms["Form 1040"]
        lines.sort(key=lambda x: order.index(x[0]) if x[0] in order else 999)

    def _standard_deduction(self):
        f, st = self.f, self.status
        if f.get("mfs_spouse_itemizes"):
            return 0
        base = STD_DED[st]
        if f.get("claimed_as_dependent"):
            base = min(base, max(DEP_STD_MIN, f.get("earned_for_dep_std", 0) + DEP_STD_EARNED_ADD))
        n = 0
        t = f.get("taxpayer", {})
        s = f.get("spouse", {})
        n += int(bool(t.get("age65"))) + int(bool(t.get("blind")))
        if st in ("MFJ",) or (st == "MFS" and f.get("mfs_spouse_no_income")):
            n += int(bool(s.get("age65"))) + int(bool(s.get("blind")))
        amt = base + n * ADD_STD[st]
        self.values["std_ded_additional_boxes"] = n
        return amt

    # ---------------------------------------------------------------
    def _schedule_d(self):
        f, st = self.f, self.status
        trades = f.get("trades", [])  # 8949 rows
        kst, klt = f.get("k1_st", 0), f.get("k1_lt", 0)
        cgd = sum(x.get("capgain_dist", 0) for x in f.get("dividends", []))
        other_st, other_lt = f.get("other_st", 0), f.get("other_lt", 0)  # 6252/4797 etc.
        co = f.get("cap_loss_co", {"st": 0, "lt": 0})
        if not (trades or kst or klt or cgd or other_st or other_lt or co["st"] or co["lt"]):
            self.values["sch_d"] = None
            return 0
        boxes = OrderedDict()
        for t in trades:
            b = t["box"]
            g = t["proceeds"] - t["basis"] + t.get("adj", 0)
            e = boxes.setdefault(b, [0, 0, 0, 0])
            e[0] += t["proceeds"]; e[1] += t["basis"]; e[2] += t.get("adj", 0); e[3] += g
            self.line(f"Form 8949 (Box {b})", t.get("id", ""), f"{t['desc']} | acq {t.get('acq','VARIOUS')} | sold {t.get('sold','VARIOUS')}"
                      f" | proceeds {r(t['proceeds']):,} | basis {r(t['basis']):,} | code {t.get('code','')} adj {r(t.get('adj',0)):,}",
                      r(g))
        stb = [b for b in boxes if b in "ABCGHI"]
        ltb = [b for b in boxes if b in "DEFJKL"]
        for b in stb:
            p, c, a, g = boxes[b]
            self.line("Schedule D", f"ST box {b}", f"Short-term from Form 8949 box {b} (proceeds {r(p):,}; cost {r(c):,}; adj {r(a):,})", r(g))
        if other_st:
            self.line("Schedule D", "4", "Short-term gain from Forms 6252, 4684, 6781, 8824", r(other_st))
        if kst:
            self.line("Schedule D", "5", "Net short-term gain/(loss) from Schedules K-1", r(kst))
        if co["st"]:
            self.line("Schedule D", "6", "Short-term capital loss carryover from 2024", -r(co["st"]))
        net_st = r(sum(boxes[b][3] for b in stb) + other_st + kst - co["st"])
        self.line("Schedule D", "7", "Net short-term capital gain or (loss)", net_st)
        for b in ltb:
            p, c, a, g = boxes[b]
            self.line("Schedule D", f"LT box {b}", f"Long-term from Form 8949 box {b} (proceeds {r(p):,}; cost {r(c):,}; adj {r(a):,})", r(g))
        if other_lt:
            self.line("Schedule D", "11", "Gain from Form 4797 Part I; long-term gain from Forms 2439, 6252, 4684, 6781, 8824", r(other_lt))
        if klt:
            self.line("Schedule D", "12", "Net long-term gain/(loss) from Schedules K-1", r(klt))
        if cgd:
            self.line("Schedule D", "13", "Capital gain distributions", r(cgd))
        if co["lt"]:
            self.line("Schedule D", "14", "Long-term capital loss carryover from 2024", -r(co["lt"]))
        net_lt = r(sum(boxes[b][3] for b in ltb) + other_lt + klt + cgd - co["lt"])
        self.line("Schedule D", "15", "Net long-term capital gain or (loss)", net_lt)
        l16 = net_st + net_lt
        self.line("Schedule D", "16", "Combine lines 7 and 15", l16)
        g28 = r(sum(t["proceeds"] - t["basis"] + t.get("adj", 0) for t in trades if t.get("collectible")) + f.get("g28_other", 0))
        u1250 = r(f.get("unrecaptured_1250", 0))
        if g28:
            self.line("Schedule D", "18", "28% rate gain", g28)
        if u1250:
            self.line("Schedule D", "19", "Unrecaptured section 1250 gain", u1250)
        limit = 1500 if st == "MFS" else 3000
        if l16 < 0:
            allowed = -min(-l16, limit)
            self.line("Schedule D", "21", "Allowable capital loss", allowed)
            carry = -l16 - (-allowed)
            # carryover character (simplified capital loss carryover worksheet)
            st_co = max(0, -net_st)
            st_used = min(st_co, -allowed)
            st_left = st_co - st_used
            lt_co = max(0, -net_lt)
            lt_left = max(0, lt_co - max(0, -allowed - st_used) - max(0, net_st))
            if net_lt > 0:
                st_left = max(0, -(net_st + net_lt) - (-allowed)) if net_st < 0 else 0
            if net_st > 0:
                lt_left = max(0, -(net_st + net_lt) - (-allowed))
            self.values["capital_loss_carryover_2026"] = {"st": r(st_left), "lt": r(lt_left), "total": r(carry)}
            ncg = 0
            result = allowed
        else:
            ncg = max(0, min(net_lt, l16))
            result = l16
        self.values["sch_d"] = {"net_st": net_st, "net_lt": net_lt, "line16": l16, "ncg": ncg, "g28": g28,
                                "u1250": u1250}
        return result

    # ---------------------------------------------------------------
    def _regular_tax(self, ti):
        sd = self.values.get("sch_d") or {}
        qd = self.values.get("3a", 0)
        ncg = sd.get("ncg", 0) if sd else 0
        # QD reduced by amounts elected as investment income (4952 line 4g) - rarely used
        qd -= self.f.get("qd_elected_4952", 0)
        return tax_with_prefs(ti, self.status, qd, ncg, sd.get("g28", 0) if sd else 0,
                              sd.get("u1250", 0) if sd else 0)

    def _form_8615(self, ti):
        """Kiddie tax. f['kiddie_8615'] = {parent_ti, parent_status, parent_qd, parent_ncg, child_net_unearned,
        child_qd_share, child_ncg_share, other_children_nui} ."""
        k = self.f["kiddie_8615"]
        nui = r(k["net_unearned"])  # line 5 (already = unearned - 2,700, limited to TI)
        nui = min(nui, ti)
        pst = k["parent_status"]
        # parent tax with and without child's NUI
        tot_nui = nui + k.get("other_children_nui", 0)
        p_ti = k["parent_ti"]
        pq, pn = k.get("parent_qd", 0), k.get("parent_ncg", 0)
        cq, cn = k.get("child_qd_nui_share", 0), k.get("child_ncg_nui_share", 0)
        t_with, _ = tax_with_prefs(p_ti + tot_nui, pst, pq + cq, pn + cn)
        t_without, _ = tax_with_prefs(p_ti, pst, pq, pn)
        tentative = t_with - t_without
        child_share = r(tentative * (nui / tot_nui)) if tot_nui else 0
        # child's own tax on TI minus NUI
        c_q_rem = max(0, self.values.get("3a", 0) - cq)
        sd = self.values.get("sch_d") or {}
        c_n_rem = max(0, (sd.get("ncg", 0) if sd else 0) - cn)
        t_child_rest, _ = tax_with_prefs(ti - nui, self.status, c_q_rem, c_n_rem)
        l15 = child_share + t_child_rest
        t_child_all, _ = self._plain_child_tax(ti)
        total = max(l15, t_child_all)
        det = {"line5_net_unearned_income": nui, "parent_tax_with_nui": t_with, "parent_tax_without": t_without,
               "line13_tentative_tax_on_nui": tentative, "child_share": child_share,
               "tax_on_child_TI_less_NUI": t_child_rest, "line15": l15, "tax_as_if_no_8615": t_child_all,
               "line18_tax": total}
        for kk, vv in det.items():
            self.line("Form 8615", kk, kk.replace("_", " "), vv)
        return total, det

    def _plain_child_tax(self, ti):
        sd = self.values.get("sch_d") or {}
        return tax_with_prefs(ti, self.status, self.values.get("3a", 0), sd.get("ncg", 0) if sd else 0)

    # ---------------------------------------------------------------
    def _schedule_a(self, agi):
        a = self.f["itemized"]
        st = self.status
        med = a.get("medical", 0)
        floor = r(agi * MED_FLOOR)
        med_ded = max(0, r(med) - floor)
        self.line("Schedule A", "1", "Medical and dental expenses", r(med))
        self.line("Schedule A", "3", "7.5% of AGI", floor)
        self.line("Schedule A", "4", "Deductible medical", med_ded)
        inc_or_sales = r(a.get("state_income_tax", 0))
        label = "State and local income taxes" if not a.get("use_sales_tax") else "General sales taxes"
        self.line("Schedule A", "5a", label, inc_or_sales)
        re_tax = r(a.get("real_estate_tax", 0))
        pp_tax = r(a.get("personal_property_tax", 0))
        self.line("Schedule A", "5b", "State and local real estate taxes", re_tax)
        self.line("Schedule A", "5c", "State and local personal property taxes", pp_tax)
        tot_salt = inc_or_sales + re_tax + pp_tax
        self.line("Schedule A", "5d", "Add lines 5a through 5c", tot_salt)
        cap, start, floor_c = (SALT_CAP_MFS, SALT_PHASE_START_MFS, SALT_FLOOR_MFS) if st == "MFS" else (SALT_CAP, SALT_PHASE_START, SALT_FLOOR)
        magi = agi + self.f.get("salt_magi_addback", 0)
        if magi > start:
            cap = max(floor_c, cap - r(.30 * (magi - start)))
        self.values["salt_cap_applied"] = cap
        salt = min(tot_salt, cap)
        self.line("Schedule A", "5e", f"Smaller of line 5d or SALT limit (${cap:,} after MAGI phase-down)", salt)
        other_tax = r(a.get("other_taxes", 0))
        if other_tax:
            self.line("Schedule A", "6", "Other taxes", other_tax)
        l7 = self.line("Schedule A", "7", "Total taxes", salt + other_tax)
        mi = r(a.get("mortgage_interest_1098", 0))
        mi_no = r(a.get("mortgage_interest_no_1098", 0))
        pts = r(a.get("points", 0))
        self.line("Schedule A", "8a", "Home mortgage interest and points reported on Form 1098", mi)
        if mi_no:
            self.line("Schedule A", "8b", "Home mortgage interest not reported on Form 1098", mi_no)
        if pts:
            self.line("Schedule A", "8c", "Points not reported on Form 1098", pts)
        l8e = mi + mi_no + pts
        self.line("Schedule A", "8e", "Add lines 8a through 8c", l8e)
        inv = r(a.get("investment_interest", 0))
        if inv:
            self.line("Schedule A", "9", "Investment interest (Form 4952)", inv)
        l10 = self.line("Schedule A", "10", "Total interest", l8e + inv)
        cash = r(a.get("charity_cash", 0))
        nonc = r(a.get("charity_noncash", 0))
        co = r(a.get("charity_carryover", 0))
        self.line("Schedule A", "11", "Gifts by cash or check", cash)
        self.line("Schedule A", "12", "Other than by cash or check", nonc)
        if co:
            self.line("Schedule A", "13", "Carryover from prior year", co)
        l14 = self.line("Schedule A", "14", "Total gifts to charity", cash + nonc + co)
        cas = r(a.get("casualty", 0))
        if cas:
            self.line("Schedule A", "15", "Casualty and theft loss(es) from federally declared disasters (Form 4684)", cas)
        oth = r(a.get("other_itemized", 0))
        if oth:
            self.line("Schedule A", "16", a.get("other_itemized_desc", "Other itemized deductions"), oth)
        total = med_ded + l7 + l10 + l14 + cas + oth
        self.line("Schedule A", "17", "Total itemized deductions", total)
        return total

    # ---------------------------------------------------------------
    def _qbi(self, ti_before):
        q = self.f.get("qbi")
        if not q:
            return 0
        st = self.status
        sd = self.values.get("sch_d") or {}
        ncg_plus_qd = (sd.get("ncg", 0) if sd else 0) + self.values.get("3a", 0)
        thresh, rng = QBI_THRESH[st], QBI_RANGE[st]
        comps = []
        total_comp = 0
        for b in q.get("businesses", []):
            qbi = b["qbi"]
            w2w, ubia = b.get("w2_wages", 0), b.get("ubia", 0)
            if ti_before <= thresh:
                comp = .20 * qbi
                how = "below threshold: 20% x QBI"
            else:
                frac_over = min(1, (ti_before - thresh) / rng)
                if b.get("sstb"):
                    app = 1 - frac_over
                    qbi, w2w, ubia = qbi * app, w2w * app, ubia * app
                tentative = .20 * qbi
                wage_lim = max(.5 * w2w, .25 * w2w + .025 * ubia)
                if frac_over >= 1:
                    comp = min(tentative, wage_lim)
                else:
                    if tentative > wage_lim:
                        comp = tentative - (tentative - wage_lim) * frac_over
                    else:
                        comp = tentative
                how = f"above threshold ({'SSTB ' if b.get('sstb') else ''}phase {frac_over:.4f})"
            comp = max(0, comp) if qbi >= 0 else .20 * qbi
            comps.append((b["name"], r(b["qbi"]), r(comp), how))
            total_comp += comp
        co = q.get("loss_carryforward", 0)
        if co:
            total_comp += .20 * (-abs(co))
        reit_ptp = q.get("reit", 0) + q.get("ptp", 0)
        reit_comp = .20 * max(0, reit_ptp)
        base = max(0, total_comp) + reit_comp
        limit = .20 * max(0, ti_before - ncg_plus_qd)
        ded = r(min(base, limit))
        form = "Form 8995" if ti_before <= thresh else "Form 8995-A"
        for n, qb, c, how in comps:
            self.line(form, n, f"QBI {qb:,}; component ({how})", c)
        if reit_ptp:
            self.line(form, "REIT/PTP", f"Qualified REIT dividends {r(q.get('reit',0)):,} + PTP income {r(q.get('ptp',0)):,} x 20%", r(reit_comp))
        self.line(form, "limit", f"20% x (taxable income before QBI {r(ti_before):,} - net capital gain & qualified dividends {r(ncg_plus_qd):,})", r(limit))
        self.line(form, "deduction", "Qualified business income deduction", ded)
        return ded

    # ---------------------------------------------------------------
    def _schedule_1a(self, agi):
        s = self.f.get("sch1a")
        st = self.status
        if not s:
            return 0
        magi = agi + s.get("magi_addback", 0)
        form = "Schedule 1-A"
        self.line(form, "Part I", "Modified AGI", r(magi))
        total = 0
        married_sep = st == "MFS"
        # tips
        if s.get("tips"):
            t = min(s["tips"], TIPS_MAX)
            thr = TIPS_OT_PHASE.get(st, 150000)
            red = 100 * math.ceil(max(0, magi - thr) / 1000) if magi > thr else 0
            tips = 0 if married_sep else max(0, t - red)
            self.line(form, "Part II", f"Qualified tips deduction (qualified tips {r(s['tips']):,}, occupation: {s.get('tip_occupation','')})", tips)
            total += tips
        if s.get("overtime"):
            mx = OT_MAX_MFJ if st == "MFJ" else OT_MAX
            t = min(s["overtime"], mx)
            thr = TIPS_OT_PHASE.get(st, 150000)
            red = 100 * math.ceil(max(0, magi - thr) / 1000) if magi > thr else 0
            ot = 0 if married_sep else max(0, t - red)
            self.line(form, "Part III", f"Qualified overtime compensation deduction (FLSA premium portion {r(s['overtime']):,})", ot)
            total += ot
        if s.get("car_interest"):
            t = min(s["car_interest"], CAR_INT_MAX)
            thr = CAR_PHASE.get(st, 100000)
            red = 200 * math.ceil(max(0, magi - thr) / 1000) if magi > thr else 0
            ci = max(0, t - red)
            self.line(form, "Part IV", f"Qualified passenger vehicle loan interest (VIN {s.get('vin','')})", ci)
            total += ci
        if s.get("seniors"):
            n = s["seniors"]
            thr = SENIOR_PHASE.get(st, 75000)
            red = .06 * max(0, magi - thr)
            per = max(0, SENIOR_DED - red)
            sd = 0 if married_sep else r(per * n)
            self.line(form, "Part V", f"Enhanced deduction for seniors ({n} x max(0, 6,000 - 6% x excess MAGI {r(max(0, magi-thr)):,}))", sd)
            total += sd
        self.line(form, "38", "Total additional deductions (to Form 1040, line 13b)", r(total))
        return r(total)

    # ---------------------------------------------------------------
    def _amt(self, ti, ded, regular_tax):
        f, st = self.f, self.status
        a = f["amt"]
        amti = ti
        lines = [("1", "Taxable income (Form 1040 line 15)", ti)]
        if self.values["deduction_type"] == "Standard":
            amti += ded
            lines.append(("2a", "Standard deduction add-back", ded))
        else:
            salt = self.forms_value("Schedule A", "7")
            amti += salt
            lines.append(("2a", "Taxes from Schedule A line 7", salt))
        for k, d in [("iso", "2i Incentive stock options (exercise spread)"), ("pab", "2g Private activity bond interest"),
                     ("other", "Other adjustments")]:
            if a.get(k):
                amti += a[k]
                lines.append((d.split()[0], d, a[k]))
        amti = r(amti)
        lines.append(("4", "Alternative minimum taxable income", amti))
        ex = AMT_EXEMPT[st] - .25 * max(0, amti - AMT_PHASEOUT[st])
        ex = max(0, r(ex))
        lines.append(("5", "Exemption", ex))
        base = max(0, amti - ex)
        lines.append(("6", "AMTI less exemption", base))
        sd = self.values.get("sch_d") or {}
        qd = self.values.get("3a", 0)
        ncg = (sd.get("ncg", 0) if sd else 0) + a.get("amt_ncg_adj", 0)
        brk = AMT_28_BREAK[st]

        def amt_ord(x, _st):
            return .26 * min(x, brk) + .28 * max(0, x - brk)
        if qd + ncg > 0:
            # Part III - AMT with preferential rates, ordinary portion at 26/28
            pref = min(base, qd + ncg)
            ordinary = base - pref
            t0, t15 = LTCG_0[st], LTCG_15[st]
            below = ordinary
            p0 = max(0, min(pref, t0 - below))
            p15 = max(0, min(pref - p0, t15 - max(below + p0, t0)))
            p20 = pref - p0 - p15
            tmt = amt_ord(ordinary, st) + .15 * p15 + .20 * p20
            tmt = min(tmt, amt_ord(base, st))
        else:
            tmt = amt_ord(base, st)
        tmt = r(tmt)
        lines.append(("7-9", "Tentative minimum tax", tmt))
        ftc = self.values.get("ftc", 0)
        reg = regular_tax - ftc
        lines.append(("10", "Regular tax (Form 1040 line 16 less Sch 3 line 1 FTC)", reg))
        amt = max(0, tmt - reg)
        lines.append(("11", "Alternative minimum tax", amt))
        for ln, d, v in lines:
            self.line("Form 6251", ln, d, r(v) if isinstance(v, (int, float)) else v)
        self.values["amt_tmt"] = tmt
        return amt

    def forms_value(self, form, ln):
        for l, d, v in self.forms.get(form, []):
            if l == ln:
                return v
        return 0

    # ---------------------------------------------------------------
    def _schedule3_nonref(self, agi, l18):
        f = self.f
        res = {"ftc": 0, "care": 0, "edu": 0, "saver": 0, "clean": 0, "home_imp": 0, "other": 0}
        ftc = f.get("ftc")
        if ftc:
            if ftc.get("method") == "direct":
                res["ftc"] = r(ftc["taxes"])
            else:
                # Form 1116 simplified limitation: FTC <= US tax x (foreign source TI / worldwide TI)
                limit = self.values["16"] * min(1, ftc["foreign_source_ti"] / max(1, self.ti))
                res["ftc"] = r(min(ftc["taxes"], limit))
                self.line("Form 1116", "summary", f"Category: {ftc.get('category','passive')}; foreign taxes {r(ftc['taxes']):,}; "
                          f"foreign-source TI {r(ftc['foreign_source_ti']):,}; limitation {r(limit):,}", res["ftc"])
                if ftc["taxes"] > limit:
                    self.values["ftc_carryforward"] = r(ftc["taxes"] - limit)
            self.values["ftc"] = res["ftc"]
        dc = f.get("dependent_care")
        if dc:
            w2 = f.get("w2", [])
            dcb = sum(x.get("box10", 0) for x in w2)
            _, _, et, es = self._dc_pending
            d = dependent_care_credit(dc["expenses"], dc["n_qual"], agi, et, es, dcb, self.status)
            res["care"] = d["credit"]
            self.values["form2441"] = d
            for k, v in d.items():
                self.line("Form 2441", k, k.replace("_", " "), v)
        edu = f.get("education")
        if edu:
            e = education_credits(edu, agi, self.status)
            self.values["aotc_refundable"] = e["refundable"]
            res["edu"] = e["nonrefundable_aotc"] + e["llc"]
            for d in e["detail"]:
                self.line("Form 8863", d[0], f"{d[1]} qualified expenses {r(d[2]):,}", r(d[3]) if d[3] is not None else "")
            self.line("Form 8863", "phase", "MAGI phase-out fraction applied", e["phase_fraction"])
            self.line("Form 8863", "8", "Refundable American opportunity credit", e["refundable"])
            self.line("Form 8863", "19", "Nonrefundable education credits", res["edu"])
        res["clean"] = r(f.get("res_clean_energy", 0))
        res["home_imp"] = r(f.get("energy_home_improvement", 0))
        res["other"] = r(f.get("other_nonref_credits", 0))
        res["before_ctc"] = res["ftc"] + res["care"] + res["edu"]  # ordering per 8812 Credit Limit Worksheet A
        self._s3 = res
        return res

    def _finish_schedule3_nonref(self, res, remaining):
        # credits limited to remaining tax in order
        order = [("1", "Foreign tax credit", "ftc"), ("2", "Credit for child and dependent care expenses (Form 2441)", "care"),
                 ("3", "Education credits (Form 8863, line 19)", "edu"),
                 ("5a", "Residential clean energy credit (Form 5695)", "clean"),
                 ("5b", "Energy efficient home improvement credit (Form 5695)", "home_imp"),
                 ("6z", "Other nonrefundable credits", "other")]
        left = remaining
        tot = 0
        for ln, d, k in order:
            v = res.get(k, 0)
            if not v:
                continue
            used = min(v, max(0, left))
            if used < v and k == "clean":
                self.values["res_clean_energy_carryforward"] = v - used
            if used < v and k not in ("clean",):
                self.values[f"{k}_unused"] = v - used
            self.line("Schedule 3", ln, d + (f" (limited from {v:,})" if used < v else ""), used)
            left -= used
            tot += used
        if tot:
            self.line("Schedule 3", "8", "Total nonrefundable credits (to Form 1040, line 20)", tot)
        return tot

    # ---------------------------------------------------------------
    def _ctc(self, agi, tax_avail, earned_1z):
        f, st = self.f, self.status
        deps = f.get("dependents", [])
        n_ctc = sum(1 for d in deps if d.get("ctc"))
        n_odc = sum(1 for d in deps if d.get("odc"))
        if not (n_ctc or n_odc):
            return 0, 0
        tent = n_ctc * CTC_PER_CHILD + n_odc * ODC
        thr = CTC_PHASE.get(st, 200000)
        magi = agi + f.get("ctc_magi_addback", 0)
        red = 50 * math.ceil(max(0, magi - thr) / 1000) if magi > thr else 0
        after = max(0, tent - red)
        nonref = min(after, max(0, tax_avail))
        # ACTC
        actc = 0
        if n_ctc and after > nonref:
            # ODC is nonrefundable only; refundable portion limited to CTC not used
            ctc_after = max(0, min(after, n_ctc * CTC_PER_CHILD) - nonref) if nonref < after else 0
            remaining = min(after - nonref, ctc_after) if ctc_after else after - nonref
            cap = ACTC_MAX * n_ctc
            earned = f.get("earned_income_8812", earned_1z + f.get("se_net_for_8812", 0))
            e15 = max(0, earned - 2500) * .15
            actc = r(min(remaining, cap, e15))
        form = "Schedule 8812"
        self.line(form, "4", "Number of qualifying children under 17 with SSN", n_ctc)
        self.line(form, "6", "Number of other dependents", n_odc)
        self.line(form, "8", "Tentative credit", tent)
        self.line(form, "10-11", f"Phase-out reduction (MAGI {r(magi):,} vs {thr:,})", red)
        self.line(form, "12", "Credit after phase-out", after)
        self.line(form, "14", "Nonrefundable CTC/ODC (to Form 1040 line 19)", nonref)
        self.line(form, "27", "Additional child tax credit (to Form 1040 line 28)", actc)
        return nonref, actc

    # ---------------------------------------------------------------
    def _schedule2_other(self, agi, se_results, w2):
        f, st = self.f, self.status
        tot = 0
        se_total = sum(x["se_tax"] for x in se_results)
        for x in se_results:
            self.line("Schedule SE", x["who"], f"Net earnings {x['net_earnings']:,}; SS {x['ss_part']:,}; Medicare {x['medicare_part']:,}; half deductible {x['half']:,}", x["se_tax"])
        if se_total:
            self.line("Schedule 2", "4", "Self-employment tax (Schedule SE)", se_total)
        tot += se_total
        t4137 = r(f.get("form4137_tax", 0))
        if t4137:
            self.line("Schedule 2", "5", "Social security and Medicare tax on unreported tip income (Form 4137)", t4137)
            tot += t4137
        t5329 = r(f.get("form5329_tax", 0))
        if t5329:
            self.line("Schedule 2", "8", "Additional tax on IRAs or other tax-favored accounts (Form 5329)", t5329)
            tot += t5329
        hh = r(f.get("schedule_h_tax", 0))
        if hh:
            self.line("Schedule 2", "9", "Household employment taxes (Schedule H)", hh)
            tot += hh
        # Form 8959
        med_w = sum(x.get("box5", 0) for x in w2) + f.get("unreported_tips_medicare", 0)
        se_med = sum(x["net_earnings"] for x in se_results)
        thr = ADDL_MED_THRESH[st]
        part1 = max(0, med_w - thr) * .009
        part2 = max(0, se_med - max(0, thr - med_w)) * .009
        amt8959 = r(part1 + part2)
        med_withheld = sum(x.get("box6", 0) for x in w2)
        reg_med = sum(x.get("box5", 0) for x in w2) * .0145
        addl_wh = r(max(0, med_withheld - reg_med))
        self.values["addl_medicare_withheld"] = addl_wh if amt8959 or addl_wh else 0
        if amt8959:
            self.line("Form 8959", "7/13", f"Additional Medicare Tax (Medicare wages {r(med_w):,}; SE {r(se_med):,}; threshold {thr:,})", amt8959)
            self.line("Form 8959", "24", "Additional Medicare Tax withheld by employer(s)", addl_wh)
            self.line("Schedule 2", "11", "Additional Medicare Tax (Form 8959)", amt8959)
            tot += amt8959
        # NIIT
        nii = f.get("niit")
        if nii:
            magi = agi + nii.get("magi_addback", 0)
            thr = NIIT_THRESH[st]
            base = min(max(0, nii["nii"]), max(0, magi - thr))
            niit = r(base * .038)
            self.line("Form 8960", "8", "Net investment income before deductions" if False else "Total investment income", r(nii.get("gross", nii["nii"])))
            if nii.get("deductions"):
                self.line("Form 8960", "11", "Properly allocable deductions (incl. investment interest)", r(nii["deductions"]))
            self.line("Form 8960", "12", "Net investment income", r(nii["nii"]))
            self.line("Form 8960", "13-16", f"MAGI {r(magi):,} over threshold {thr:,}", r(max(0, magi - thr)))
            self.line("Form 8960", "17", "Net investment income tax", niit)
            if niit:
                self.line("Schedule 2", "12", "Net investment income tax (Form 8960)", niit)
            tot += niit
            self.values["niit"] = niit
        unc = r(f.get("uncollected_fica_w2", 0))
        if unc:
            self.line("Schedule 2", "13", "Uncollected social security and Medicare tax on wages (W-2 box 12)", unc)
            tot += unc
        for ln, d, v in f.get("sch2_other", []):
            self.line("Schedule 2", ln, d, r(v))
            tot += r(v)
        if tot:
            self.line("Schedule 2", "21", "Total other taxes (to Form 1040, line 23)", tot)
        return tot

    # ---------------------------------------------------------------
    def _schedule3_ref(self, w2):
        f = self.f
        tot = 0
        ptc = r(f.get("net_ptc", 0))
        if ptc:
            self.line("Schedule 3", "9", "Net premium tax credit (Form 8962)", ptc); tot += ptc
        ext = r(f.get("extension_payment", 0))
        if ext:
            self.line("Schedule 3", "10", "Amount paid with request for extension to file (Form 4868)", ext); tot += ext
        # excess social security - per person with 2+ employers
        excess = 0
        for who in ("T", "S"):
            ws = [x for x in w2 if x.get("who", "T") == who]
            if len(ws) > 1:
                ss = sum(x.get("box4", 0) for x in ws)
                mx = SS_WAGE_BASE * .062
                if ss > mx:
                    excess += ss - mx
        excess = r(excess)
        if excess:
            self.line("Schedule 3", "11", "Excess social security and tier 1 RRTA tax withheld", excess); tot += excess
        self.values["excess_ss"] = excess
        for ln, d, v in f.get("sch3_ref_other", []):
            self.line("Schedule 3", ln, d, r(v)); tot += r(v)
        if tot:
            self.line("Schedule 3", "15", "Total other payments and refundable credits (to Form 1040, line 31)", tot)
        return tot

    # ---------------------------------------------------------------
    def _eic(self, agi, l1z):
        f = self.f
        kids = f.get("eic_kids", 0)
        earned = f.get("eic_earned", l1z)
        inv = f.get("eic_invest_income", 0)
        c = eitc(kids, earned, agi, self.status, inv)
        self.line("EIC Worksheet", "kids", "Qualifying children", kids)
        self.line("EIC Worksheet", "earned", "Earned income", r(earned))
        self.line("EIC Worksheet", "agi", "AGI", agi)
        self.line("EIC Worksheet", "credit", "Earned income credit (EIC Table)", c)
        return c

    # ---------------------------------------------------------------
    def summary(self):
        v = self.values
        keys = ["1z", "2a", "2b", "3a", "3b", "4b", "5b", "6b", "7", "8", "9", "10", "11", "12e", "13a", "13b", "15", "16",
                "17", "19", "20", "22", "23", "24", "25d", "26", "27a", "28", "29", "31", "33", "34", "35a", "37"]
        return OrderedDict((k, v.get(k, 0)) for k in keys)
