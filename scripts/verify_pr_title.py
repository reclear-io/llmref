#!/usr/bin/env python3
"""Validate PR title format for registry snapshot pull requests."""
from __future__ import annotations

import re
import sys

# Add|Update [technology name] [version name] - [reason phrase]
TITLE_RE = re.compile(r"^(Add|Update) .+ .+ - .+$")


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: verify_pr_title.py <pr-title>", file=sys.stderr)
        return 2

    title = sys.argv[1].strip()
    if TITLE_RE.fullmatch(title):
        print(f"PR title OK: {title}")
        return 0

    print(
        "ERROR: PR title must match: Add|Update [technology name] [version name] - [reason phrase]",
        file=sys.stderr,
    )
    print(f"ERROR: got: {title}", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
