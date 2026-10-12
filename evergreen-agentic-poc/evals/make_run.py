#!/usr/bin/env python3
"""Create a sandboxed run folder for one test client - INPUTS ONLY (no answer key, notes, review points, deliverables).

    python3 evals/make_run.py <dataset_root> <client_id> <run_dir>

Copies <dataset_root>/clients/<ID>_*/PERM/ and .../2025/PBC/ (+ the neutral PBC receipt log) into <run_dir>/input/.
"""
import glob
import os
import shutil
import sys


def main(dataset_root, cid, run_dir):
    hits = glob.glob(os.path.join(dataset_root, "clients", f"{cid}_*"))
    if len(hits) != 1:
        sys.exit(f"client {cid} not found under {dataset_root}/clients")
    src = hits[0]
    dst = os.path.join(run_dir, "input")
    if os.path.exists(dst):
        shutil.rmtree(dst)
    shutil.copytree(os.path.join(src, "PERM"), os.path.join(dst, "PERM"))
    shutil.copytree(os.path.join(src, "2025", "PBC"), os.path.join(dst, "PBC"))
    for log in glob.glob(os.path.join(src, "2025", "*_PBC_Receipt_Log.md")):
        shutil.copy(log, os.path.join(dst, os.path.basename(log)))
    leaked = [f for f in glob.glob(os.path.join(dst, "**", "*"), recursive=True)
              if any(k in os.path.basename(f) for k in ("Answer_Key", "Preparer_Notes", "Review_Points", "Software_Exception"))]
    assert not leaked, f"answer material leaked into run input: {leaked}"
    n = sum(len(fs) for _, _, fs in os.walk(dst))
    print(f"{cid}: {n} input files -> {dst}")


if __name__ == "__main__":
    if len(sys.argv) != 4:
        sys.exit(__doc__)
    main(*sys.argv[1:])
