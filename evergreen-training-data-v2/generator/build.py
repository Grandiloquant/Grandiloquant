"""Build the full Project Evergreen synthetic data set: python3 build.py [client_module ...]"""
import importlib
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "clients"))


def main(argv):
    mods = argv or sorted(f[:-3] for f in os.listdir(os.path.join(HERE, "clients")) if f.startswith("c") and f.endswith(".py"))
    for m in mods:
        importlib.import_module(m)
    import build_swx
    build_swx.run()
    import summarize  # noqa: F401  (rebuilds index files)


if __name__ == "__main__":
    main(sys.argv[1:])
