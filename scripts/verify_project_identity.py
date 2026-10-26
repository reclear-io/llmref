#!/usr/bin/env python3
"""Reject captures attached to another project's documentation identity."""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from urllib.parse import urlparse


def source_scope(url: str, version: str) -> tuple[str, str]:
    parsed = urlparse(url)
    if parsed.scheme not in {"http", "https"} or not parsed.hostname or parsed.username or parsed.password:
        raise ValueError("Invalid documentation source URL")
    path = parsed.path.rstrip("/")
    if path.lower().endswith("/llms.txt"):
        path = path.rsplit("/", 1)[0]
    parts = path.split("/")
    protected = 2 if (
        parsed.hostname in {"github.com", "rubydoc.info", "www.rubydoc.info"}
        or (len(parts) > 1 and parts[1] in {"gems", "packages", "projects"})
    ) else 1
    for i, part in enumerate(parts):
        if i > protected and (part in {version, "v" + version} or re.fullmatch(r"v\d+(?:\.\d+)*", part)):
            parts[i] = "{version}"
    return parsed.netloc.lower(), "/".join(parts)


def contains(old: dict, new: dict) -> bool:
    old_host, old_path = source_scope(old["source_root"], old["version"])
    host, path = source_scope(new["source_root"], new["version"])
    return host == old_host and (path == old_path or path.startswith(old_path.rstrip("/") + "/"))


def canonical_versions(versions: list[dict]) -> list[dict]:
    if len({source_scope(v["source_root"], v["version"]) for v in versions}) <= 1:
        return versions
    # Preserve legacy routes, but an older collision cannot authorize a refresh.
    dated = [(datetime.fromisoformat(v["snapshot_at"].replace("Z", "+00:00")), v) for v in versions]
    latest = max(date for date, _ in dated)
    current = [v for date, v in dated if date == latest]
    if len({source_scope(v["source_root"], v["version"]) for v in current}) != 1:
        raise ValueError("Conflicting source identities have the same observation date")
    return [v for v in versions if contains(current[0], v)]


def check_project(project: str, previous: list[dict], proposed: list[dict], *, approved_move: bool = False) -> list[str]:
    errors = []
    prior_by_version = {v["version"]: v for v in previous}
    new_captures = []
    for capture in proposed:
        prior = prior_by_version.get(capture["version"])
        # A license/storage metadata repair can retain an old explicit route.
        if prior and all(prior.get(k) == capture.get(k) for k in ("source_root", "content_fingerprint", "snapshot_at")):
            continue
        if urlparse(capture["source_root"]).scheme != "https":
            errors.append(f"{project}@{capture['version']}: new captures require HTTPS")
        new_captures.append(capture)
    if not new_captures:
        return errors
    try:
        allowed = canonical_versions(previous) if previous else [new_captures[0]]
        for capture in new_captures:
            if not any(contains(old, capture) for old in allowed) and not (previous and approved_move):
                errors.append(f"{project}@{capture['version']}: documentation belongs to a different source; use a distinct project ID or obtain reviewed source-move approval")
    except (KeyError, TypeError, ValueError) as exc:
        errors.append(f"{project}: cannot establish a canonical source: {exc}")
    return errors


def git(*args: str) -> str:
    return subprocess.check_output(["git", *args], text=True)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base", required=True, help="Exact PR base commit SHA")
    parser.add_argument("--approved-source-move", action="store_true")
    args = parser.parse_args()
    base = git("rev-parse", "--verify", args.base + "^{commit}").strip()
    catalog = json.loads(git("show", base + ":registry/index.json"))
    projects = {p["id"]: p["versions"] for p in catalog["projects"]}
    paths = git("diff", "--name-only", "--diff-filter=AM", base, "HEAD", "--", "registry/").splitlines()
    changed: dict[str, list[dict]] = {}
    for name in paths:
        parts = Path(name).parts
        if len(parts) != 4 or parts[-1] != "meta.json":
            continue
        meta = json.loads(Path(name).read_text())
        changed.setdefault(parts[1], []).append({**meta, "version": parts[2]})
    errors = [e for project, captures in changed.items() for e in check_project(project, projects.get(project, []), captures, approved_move=args.approved_source_move)]
    for error in errors:
        print("ERROR: " + error, file=sys.stderr)
    print(f"Checked source identity for {len(changed)} changed projects; {len(errors)} errors")
    return bool(errors)


if __name__ == "__main__":
    sys.exit(main())
