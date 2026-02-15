#!/usr/bin/env python3
"""Build OneLive standalone executable via PyInstaller."""

from __future__ import annotations

import argparse
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
DIST_DIR = ROOT / "dist"
BUILD_DIR = ROOT / "build"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build onelive executable")
    parser.add_argument("--clean", action="store_true", help="Delete build/dist directories first")
    parser.add_argument("--name", default="onelive", help="Executable name")
    return parser.parse_args()


def remove_path(path: pathlib.Path) -> None:
    if path.exists():
        for child in sorted(path.rglob("*"), reverse=True):
            if child.is_file() or child.is_symlink():
                child.unlink()
            else:
                child.rmdir()
        path.rmdir()


def main() -> int:
    args = parse_args()

    if args.clean:
        remove_path(BUILD_DIR)
        remove_path(DIST_DIR)

    cmd = [
        sys.executable,
        "-m",
        "PyInstaller",
        "--onefile",
        "--name",
        args.name,
        "onelive.py",
    ]
    cmd.append("--console")

    print("[build] Running:", " ".join(cmd))
    result = subprocess.run(cmd, cwd=ROOT, check=False)
    if result.returncode:
        print(f"[build] Failed with exit code {result.returncode}")
        return result.returncode

    binary = DIST_DIR / (f"{args.name}.exe" if sys.platform.startswith("win") else args.name)
    if binary.exists():
        print(f"[build] Success: {binary}")
    else:
        print("[build] PyInstaller finished, but executable was not found in dist/")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
