#!/usr/bin/env python3
"""Reject captures attached to another project's documentation identity."""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
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
    versions = [v for v in versions if not v.get("canonical_target")]
    if len({source_scope(v["source_root"], v["version"]) for v in versions}) <= 1:
        return versions
    if any(all(contains(root, v) for v in versions) for root in versions):
        return versions
    raise ValueError("Conflicting source identities require explicit maintainer review; capture dates do not establish ownership")


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
    if previous and all(v.get("canonical_target") for v in previous):
        return errors + [f"{project}: compatibility namespace requires a qualified canonical project ID"]
    try:
        allowed = canonical_versions(previous) if previous and not approved_move else [new_captures[0]]
        for capture in new_captures:
            if not any(contains(old, capture) for old in allowed) and not (previous and approved_move):
                errors.append(f"{project}@{capture['version']}: documentation belongs to a different source; use a distinct project ID or obtain reviewed source-move approval")
    except (KeyError, TypeError, ValueError) as exc:
        errors.append(f"{project}: cannot establish a canonical source: {exc}")
    return errors


def git(*args: str) -> str:
    return subprocess.check_output(["git", *args], text=True)



def alias_catalog_errors(catalog: dict) -> list[str]:
    errors = []
    try:
        records = {(p["id"], v["version"]): v for p in catalog["projects"] for v in p["versions"]}
        for project in catalog["projects"]:
            versions = project["versions"]
            aliases = [v for v in versions if v.get("canonical_target") is not None]
            if not aliases:
                if any(v.get("legacy_default") for v in versions):
                    errors.append(f"{project['id']}: legacy default requires a canonical target")
                continue
            if len(aliases) != len(versions):
                errors.append(f"{project['id']}: compatibility namespaces cannot contain new captures")
            if sum(v.get("legacy_default") is True for v in aliases) != 1:
                errors.append(f"{project['id']}: exactly one frozen legacy default is required")
            for alias in aliases:
                target = alias["canonical_target"]
                if "legacy_default" in alias and not isinstance(alias["legacy_default"], bool):
                    errors.append(f"{project['id']}: legacy_default must be boolean")
                if not isinstance(target, dict) or set(target) != {"project", "version"}:
                    errors.append(f"{project['id']}: invalid canonical target")
                    continue
                if not all(isinstance(x, str) and x for x in target.values()):
                    errors.append(f"{project['id']}: invalid canonical target")
                    continue
                if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", target["project"]) or target["version"] in {".", ".."} or not re.fullmatch(r"[A-Za-z0-9._+-]+", target["version"]):
                    errors.append(f"{project['id']}: unsafe canonical target")
                    continue
                if target["project"] == project["id"]:
                    errors.append(f"{project['id']}: canonical target must be a distinct project")
                fingerprint = alias.get("content_fingerprint")
                if not isinstance(fingerprint, str) or not re.fullmatch(r"[0-9a-f]{64}", fingerprint):
                    errors.append(f"{project['id']}: a retained SHA-256 fingerprint is required")
                if not isinstance(alias.get("source_root"), str) or not alias["source_root"]:
                    errors.append(f"{project['id']}: a retained source URL is required")
                leaf = records.get((target["project"], target["version"]))
                if leaf is None or leaf.get("canonical_target"):
                    errors.append(f"{project['id']}: target must exist as a leaf; chains and cycles are forbidden")
                elif any(alias.get(k) != leaf.get(k) for k in ("source_root", "content_fingerprint")):
                    errors.append(f"{project['id']}: target must preserve the exact source and original fingerprint")
    except (KeyError, TypeError, ValueError) as exc:
        errors.append("Invalid compatibility alias catalog: " + str(exc))
    return errors


def alias_transition_errors(previous: dict, proposed: dict, *, approved: bool = False) -> list[str]:
    if approved:
        return []
    prior = {(p["id"], v["version"]): v for p in previous["projects"] for v in p["versions"]}
    errors = []
    for project in proposed["projects"]:
        for version in project["versions"]:
            old = prior.get((project["id"], version["version"]), {})
            if old.get("canonical_target") != version.get("canonical_target") or bool(old.get("legacy_default")) != bool(version.get("legacy_default")):
                errors.append(f"{project['id']}@{version['version']}: canonical alias/default changes require explicit source-move review")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base", required=True, help="Exact PR base commit SHA")
    parser.add_argument("--approved-source-move", action="store_true")
    args = parser.parse_args()
    base = git("rev-parse", "--verify", args.base + "^{commit}").strip()
    catalog = json.loads(git("show", base + ":registry/index.json"))
    projects = {p["id"]: p["versions"] for p in catalog["projects"]}
    proposed_catalog = json.loads(Path("registry/index.json").read_text())
    alias_errors = alias_catalog_errors(proposed_catalog) + alias_transition_errors(catalog, proposed_catalog, approved=args.approved_source_move)
    paths = git("diff", "--name-only", "--diff-filter=AM", base, "HEAD", "--", "registry/").splitlines()
    changed: dict[str, list[dict]] = {}
    for name in paths:
        parts = Path(name).parts
        if len(parts) != 4 or parts[-1] != "meta.json":
            continue
        meta = json.loads(Path(name).read_text())
        changed.setdefault(parts[1], []).append({**meta, "version": parts[2]})
    errors = alias_errors + [e for project, captures in changed.items() for e in check_project(project, projects.get(project, []), captures, approved_move=args.approved_source_move)]
    for error in errors:
        print("ERROR: " + error, file=sys.stderr)
    print(f"Checked source identity for {len(changed)} changed projects; {len(errors)} errors")
    return bool(errors)


if __name__ == "__main__":
    sys.exit(main())
