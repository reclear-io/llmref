#!/usr/bin/env python3
"""Validate fullcontext registry snapshots and catalog index."""
from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "registry"
INDEX_PATH = REGISTRY / "index.json"

TECH_ID_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
REQUIRED_META_FIELDS = {
    "project",
    "project_version",
    "source_root",
}
ALLOWED_SNAPSHOT_FILES = {"llms.txt", "llms-full.txt", "meta.json"}
ALLOWED_REGISTRY_ROOT_FILES = {"index.json", ".gitkeep"}


def error(msg: str) -> None:
    print(f"ERROR: {msg}", file=sys.stderr)


def warn(msg: str) -> None:
    print(f"WARN: {msg}")


def load_json(path: Path) -> dict:
    with path.open(encoding="utf-8") as f:
        return json.load(f)


def is_https_url(value: str) -> bool:
    parsed = urlparse(value)
    return parsed.scheme == "https" and bool(parsed.netloc)


def fingerprint_of(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def discover_snapshots() -> list[tuple[str, str, Path]]:
    snapshots: list[tuple[str, str, Path]] = []
    if not REGISTRY.exists():
        return snapshots

    for project_dir in sorted(REGISTRY.iterdir()):
        if not project_dir.is_dir():
            continue
        if project_dir.name in ALLOWED_REGISTRY_ROOT_FILES:
            continue

        tech_id = project_dir.name
        for version_dir in sorted(project_dir.iterdir()):
            if version_dir.is_dir():
                snapshots.append((tech_id, version_dir.name, version_dir))

    return snapshots


def validate_slug(tech_id: str) -> bool:
    ok = bool(TECH_ID_RE.fullmatch(tech_id))
    if not ok:
        error(f"invalid technology id '{tech_id}' (use lowercase letters, numbers, hyphens)")
    return ok


def validate_snapshot(tech_id: str, version: str, snapshot_dir: Path) -> bool:
    ok = True

    for entry in snapshot_dir.iterdir():
        if entry.is_file() and entry.name not in ALLOWED_SNAPSHOT_FILES:
            error(f"{snapshot_dir}: unexpected file '{entry.name}'")
            ok = False

    missing = [name for name in ALLOWED_SNAPSHOT_FILES if not (snapshot_dir / name).is_file()]
    if missing:
        error(f"{snapshot_dir}: missing required files: {', '.join(sorted(missing))}")
        return False

    llms_txt = (snapshot_dir / "llms.txt").read_text(encoding="utf-8")
    llms_full = (snapshot_dir / "llms-full.txt").read_text(encoding="utf-8")
    if not llms_txt.strip():
        error(f"{snapshot_dir}/llms.txt: must not be empty")
        ok = False
    if not llms_full.strip():
        error(f"{snapshot_dir}/llms-full.txt: must not be empty")
        ok = False

    try:
        meta = load_json(snapshot_dir / "meta.json")
    except json.JSONDecodeError as exc:
        error(f"{snapshot_dir}/meta.json: invalid JSON ({exc})")
        return False

    if not isinstance(meta, dict):
        error(f"{snapshot_dir}/meta.json: must be a JSON object")
        return False

    missing_fields = sorted(REQUIRED_META_FIELDS - set(meta))
    if missing_fields:
        error(f"{snapshot_dir}/meta.json: missing required fields: {', '.join(missing_fields)}")
        ok = False

    if meta.get("project") != tech_id:
        error(
            f"{snapshot_dir}/meta.json: project '{meta.get('project')}' "
            f"does not match directory '{tech_id}'"
        )
        ok = False

    if meta.get("project_version") != version:
        error(
            f"{snapshot_dir}/meta.json: project_version '{meta.get('project_version')}' "
            f"does not match directory '{version}'"
        )
        ok = False

    source_root = meta.get("source_root")
    if not isinstance(source_root, str) or not is_https_url(source_root):
        error(f"{snapshot_dir}/meta.json: source_root must be an https URL")
        ok = False

    fingerprint = meta.get("content_fingerprint")
    if isinstance(fingerprint, str) and fingerprint:
        expected = fingerprint_of(llms_full)
        if fingerprint != expected:
            warn(
                f"{snapshot_dir}/meta.json: content_fingerprint does not match llms-full.txt "
                "(maintainers may correct this on merge)"
            )

    return ok


def validate_index(snapshots: list[tuple[str, str, Path]]) -> bool:
    ok = True

    if not snapshots:
        if INDEX_PATH.exists():
            try:
                index = load_json(INDEX_PATH)
            except json.JSONDecodeError as exc:
                error(f"{INDEX_PATH}: invalid JSON ({exc})")
                return False
            if index.get("projects"):
                error(f"{INDEX_PATH}: lists projects but no snapshots exist under registry/")
                return False
        return True

    if not INDEX_PATH.is_file():
        error(f"{INDEX_PATH}: required when registry snapshots exist")
        return False

    try:
        index = load_json(INDEX_PATH)
    except json.JSONDecodeError as exc:
        error(f"{INDEX_PATH}: invalid JSON ({exc})")
        return False

    projects = index.get("projects")
    if not isinstance(projects, list):
        error(f"{INDEX_PATH}: projects must be an array")
        return False

    indexed: set[tuple[str, str]] = set()
    for project in projects:
        if not isinstance(project, dict):
            error(f"{INDEX_PATH}: each project entry must be an object")
            ok = False
            continue

        tech_id = project.get("id")
        versions = project.get("versions")
        if not isinstance(tech_id, str) or not isinstance(versions, list):
            error(f"{INDEX_PATH}: project entries require id and versions")
            ok = False
            continue

        for entry in versions:
            if not isinstance(entry, dict):
                error(f"{INDEX_PATH}: version entries must be objects")
                ok = False
                continue
            version = entry.get("version")
            if not isinstance(version, str):
                error(f"{INDEX_PATH}: version entries require version")
                ok = False
                continue
            indexed.add((tech_id, version))

    expected = {(tech_id, version) for tech_id, version, _ in snapshots}
    missing = sorted(expected - indexed)
    extra = sorted(indexed - expected)

    if missing:
        error(f"{INDEX_PATH}: missing entries for {missing}")
        ok = False
    if extra:
        error(f"{INDEX_PATH}: entries not present on disk {extra}")
        ok = False

    return ok


def main() -> int:
    ok = True
    snapshots = discover_snapshots()

    for tech_id, version, snapshot_dir in snapshots:
        ok = validate_slug(tech_id) and ok
        ok = validate_snapshot(tech_id, version, snapshot_dir) and ok

    ok = validate_index(snapshots) and ok

    if ok:
        print(f"Registry validation passed ({len(snapshots)} snapshot(s)).")
        return 0

    error("Registry validation failed.")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
