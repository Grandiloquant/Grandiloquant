"""Build the software-exception pack for every client that has a generator/swx/evgNNNN.py data module.
Runs after the client scripts (which rewrite the answer keys).  Usage: python3 build_swx.py [evg1007 ...]"""
import glob
import importlib
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "swx"))
from software_exceptions import build_pack, ROOT  # noqa: E402


class _Client:
    """Minimal stand-in for common.ClientBuild pointing at an existing client folder."""
    def __init__(self, cid, display):
        hits = glob.glob(os.path.join(ROOT, "clients", f"{cid}_*"))
        assert len(hits) == 1, (cid, hits)
        self.id, self.display, self.root = cid, display, hits[0]
        self.year = os.path.join(self.root, "2025")

    def year_file(self, name):
        return os.path.join(self.year, name)


def run(mods=None):
    mods = mods or sorted(os.path.basename(p)[:-3] for p in glob.glob(os.path.join(HERE, "swx", "evg*.py")))
    strict = bool(mods)
    for m in mods:
        try:
            mod = importlib.import_module(m)
            C = _Client(mod.CLIENT_ID, mod.DISPLAY)
            build_pack(C, mod.ITEMS, mod.TABS, getattr(mod, "PREPARER", "Preparer"),
                       getattr(mod, "REVIEWER", "Reviewer"), getattr(mod, "INTRO", ""))
            checks = getattr(mod, "CHECKS", {})
            if checks:  # recompute the filled workbook's formulas and compare with expected values
                from pycel import ExcelCompiler
                xl = ExcelCompiler(filename=C.year_file(f"{C.id}_2025_Software_Exception_Workbook.xlsx"))
                for ref, want in checks.items():
                    got = xl.evaluate(ref)
                    ok = (abs(float(got) - float(want)) <= 1) if isinstance(want, (int, float)) else (str(got) == str(want))
                    if not ok:
                        raise AssertionError(f"{mod.CLIENT_ID} workbook check {ref}: got {got!r}, expected {want!r}")
            print(f"swx {mod.CLIENT_ID}: {len(mod.ITEMS)} exceptions, {len(checks)} workbook checks OK")
        except Exception as e:  # one bad module must not block other clients' builds
            if strict:
                raise
            print(f"swx {m}: FAILED - {e!r}")


if __name__ == "__main__":
    run(sys.argv[1:])
