#!/usr/bin/env python3
"""Create evals/workspace/iteration-N/eval-<id>/<config>/run-1/{run/input, outputs/} for a list of clients.
    python3 evals/setup_iteration.py <N> <config,config> <CID> [<CID> ...]"""
import glob, json, os, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.abspath(os.path.join(HERE, "..", "..", "evergreen-training-data-v2"))
n, configs, cids = sys.argv[1], sys.argv[2].split(","), sys.argv[3:]
for cid in cids:
    folder = os.path.basename(glob.glob(os.path.join(DATA, "clients", f"{cid}_*"))[0])
    ev = os.path.join(HERE, "workspace", f"iteration-{n}", f"eval-{folder}")
    os.makedirs(ev, exist_ok=True)
    json.dump({"eval_id": cid, "eval_name": folder, "prompt": f"Take client {cid} from intake to a filing-ready 2025 return.",
               "answer_key": glob.glob(os.path.join(DATA, "clients", folder, "2025", "*_Answer_Key.json"))[0],
               "assertions": []}, open(os.path.join(ev, "eval_metadata.json"), "w"), indent=2)
    for c in configs:
        run = os.path.join(ev, c, "run-1")
        os.makedirs(os.path.join(run, "outputs"), exist_ok=True)
        subprocess.run([sys.executable, os.path.join(HERE, "make_run.py"), DATA, cid, os.path.join(run, "run")], check=True)
