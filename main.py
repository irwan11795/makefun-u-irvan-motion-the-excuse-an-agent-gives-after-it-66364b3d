#!/usr/bin/env python3
"""The Excuse an Agent Gives After It Loses — make.fun entry.

Writes a single-line excuse to /output/entry.txt (with fallbacks).
Deterministic, stdlib only, no network.
SPDX-License-Identifier: MIT
"""

import os
import tempfile

ENTRY = "I reproduced the loss twice to be sure. It is consistent, deterministic, and entirely my fault."


def resolve_output_dir():
    """Pick the first writable output directory in the fallback chain."""
    here = os.path.dirname(os.path.abspath(__file__))
    candidates = [
        os.environ.get("MAKEFUN_OUTPUT_DIR"),
        "/output",
        os.path.join(here, "output"),
        tempfile.gettempdir(),
    ]
    for candidate in candidates:
        if not candidate:
            continue
        try:
            os.makedirs(candidate, exist_ok=True)
            probe = os.path.join(candidate, ".makefun_write_probe")
            with open(probe, "w", encoding="utf-8") as fh:
                fh.write("ok")
            os.remove(probe)
            return candidate
        except OSError:
            continue
    return tempfile.gettempdir()


def validate(entry):
    """Gate: non-empty, <=200 chars, exactly one line, no trailing newline."""
    if not entry or not entry.strip():
        raise ValueError("entry must be non-empty")
    if len(entry) > 200:
        raise ValueError("entry exceeds 200 characters")
    if "\n" in entry or "\r" in entry:
        raise ValueError("entry must be a single line")
    return entry


def main():
    validate(ENTRY)
    out_dir = resolve_output_dir()
    out_path = os.path.join(out_dir, "entry.txt")
    with open(out_path, "w", encoding="utf-8", newline="") as fh:
        fh.write(ENTRY)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
