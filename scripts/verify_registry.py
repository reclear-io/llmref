#!/usr/bin/env python3
"""Validate llm-txts registry snapshots and catalog index."""
from __future__ import annotations

import hashlib
import json
import re
import sys
from datetime import datetime
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "registry"
INDEX_PATH = REGISTRY / "index.json"

TECH_ID_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
UUID_RE = re.compile(
    r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$",
    re.IGNORECASE,
)
FINGERPRINT_RE = re.compile(r"^[0-9a-f]{64}$", re.IGNORECASE)
LLMS_LINK_RE = re.compile(r"^\s*[-*]\s+\[[^\]]*\]\(([^)]+)\)", re.MULTILINE)
MARKDOWN_LINK_RE = re.compile(r"\[[^\]]*\]\(([^)]+)\)")

REQUIRED_META_FIELDS = {
    "project": str,
    "project_version": str,
    "snapshot_id": str,
    "snapshot_at": str,
    "source_last_seen_at": str,
    "content_fingerprint": str,
    "page_count": int,
    "source_root": str,
    "embedding_model": str,
    "chunking_profile": str,
    "generator_version": str,
}

ALLOWED_SNAPSHOT_FILES = {"llms.txt", "llms-full.txt", "meta.json"}
ALLOWED_REGISTRY_ROOT_FILES = {"index.json", ".gitkeep"}


def error(msg: str) -> None:
    print(f"ERROR: {msg}", file=sys.stderr)


def load_json(path: Path) -> dict:
    with path.open(encoding="utf-8") as f:
        return json.load(f)


def _parse_iso8601(value: str) -> datetime | None:
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None


def parse_iso8601(value: str, field: str, path: Path) -> datetime | None:
    parsed = _parse_iso8601(value)
    if parsed is None:
        error(f"{path}: {field} must be a valid ISO 8601 timestamp, got '{value}'")
    return parsed


def is_https_url(value: str) -> bool:
    parsed = urlparse(value)
    return parsed.scheme == "https" and bool(parsed.netloc)


def is_valid_url(value: str) -> bool:
    parsed = urlparse(value)
    return parsed.scheme in {"http", "https"} and bool(parsed.netloc)


def fingerprint_of(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def discover_snapshots() -> tuple[list[tuple[str, str, Path]], bool]:
    snapshots: list[tuple[str, str, Path]] = []
    ok = True

    if not REGISTRY.exists():
        return snapshots, ok

    for entry in sorted(REGISTRY.iterdir()):
        if entry.is_file():
            if entry.name not in ALLOWED_REGISTRY_ROOT_FILES:
                error(f"{REGISTRY}: unexpected file '{entry.name}'")
                ok = False
            continue

        if not entry.is_dir():
            continue

        if entry.name in ALLOWED_REGISTRY_ROOT_FILES:
            continue

        tech_id = entry.name
        project_ok, project_snapshots = _discover_project_snapshots(tech_id, entry)
        ok = project_ok and ok
        snapshots.extend(project_snapshots)

    return snapshots, ok


def _discover_project_snapshots(tech_id: str, project_dir: Path) -> tuple[bool, list[tuple[str, str, Path]]]:
    snapshots: list[tuple[str, str, Path]] = []
    ok = True
    found_version = False

    for entry in sorted(project_dir.iterdir()):
        if entry.is_dir():
            found_version = True
            snapshots.append((tech_id, entry.name, entry))
            continue

        error(f"{project_dir}: unexpected file '{entry.name}' (only version directories allowed)")
        ok = False

    if not found_version:
        error(f"{project_dir}: project has no version directories")
        ok = False

    return ok, snapshots


def validate_slug(tech_id: str) -> bool:
    ok = bool(TECH_ID_RE.fullmatch(tech_id))
    if not ok:
        error(f"invalid technology id '{tech_id}' (use lowercase letters, numbers, hyphens)")
    return ok


def validate_llms_txt(path: Path, llms_txt: str, source_root: str) -> bool:
    ok = True

    links = MARKDOWN_LINK_RE.findall(llms_txt)
    if not links:
        error(f"{path}/llms.txt: must contain at least one markdown link")
        ok = False

    for link in links:
        if not is_valid_url(link):
            error(f"{path}/llms.txt: invalid link URL '{link}'")
            ok = False

    if source_root and not llms_txt.strip():
        error(f"{path}/llms.txt: must not be empty")
        ok = False

    return ok


def validate_meta(meta: dict, tech_id: str, version: str, snapshot_dir: Path, llms_full: str, llms_txt: str) -> bool:
    ok = True
    meta_path = snapshot_dir / "meta.json"

    for field, expected_type in REQUIRED_META_FIELDS.items():
        if field not in meta:
            error(f"{meta_path}: missing required field '{field}'")
            ok = False
            continue
        if not isinstance(meta[field], expected_type):
            error(f"{meta_path}: field '{field}' must be {expected_type.__name__}")
            ok = False
        elif expected_type is str and not meta[field].strip():
            error(f"{meta_path}: field '{field}' must not be empty")
            ok = False

    if meta.get("project") != tech_id:
        error(f"{meta_path}: project '{meta.get('project')}' does not match directory '{tech_id}'")
        ok = False

    if meta.get("project_version") != version:
        error(
            f"{meta_path}: project_version '{meta.get('project_version')}' "
            f"does not match directory '{version}'"
        )
        ok = False

    source_root = meta.get("source_root", "")
    if not isinstance(source_root, str) or not is_https_url(source_root):
        error(f"{meta_path}: source_root must be an https URL")
        ok = False

    snapshot_id = meta.get("snapshot_id", "")
    if isinstance(snapshot_id, str) and not UUID_RE.fullmatch(snapshot_id):
        error(f"{meta_path}: snapshot_id must be a UUID")
        ok = False

    for ts_field in ("snapshot_at", "source_last_seen_at"):
        value = meta.get(ts_field)
        if isinstance(value, str) and parse_iso8601(value, ts_field, meta_path) is None:
            ok = False

    fingerprint = meta.get("content_fingerprint", "")
    if not isinstance(fingerprint, str) or not FINGERPRINT_RE.fullmatch(fingerprint):
        error(f"{meta_path}: content_fingerprint must be a 64-character hex SHA-256 digest")
        ok = False
    else:
        expected = fingerprint_of(llms_full)
        if fingerprint.lower() != expected:
            error(
                f"{meta_path}: content_fingerprint does not match sha256(llms-full.txt); "
                f"expected {expected}"
            )
            ok = False

    linked_pages = len(LLMS_LINK_RE.findall(llms_txt))
    page_count = meta.get("page_count")
    expected_page_count = linked_pages if linked_pages > 0 else 1
    if isinstance(page_count, int):
        if page_count < 1:
            error(f"{meta_path}: page_count must be at least 1")
            ok = False
        elif page_count != expected_page_count:
            error(
                f"{meta_path}: page_count {page_count} does not match llms.txt link count "
                f"{expected_page_count}"
            )
            ok = False

    ok = validate_llms_txt(snapshot_dir, llms_txt, source_root) and ok
    return ok


def validate_snapshot(tech_id: str, version: str, snapshot_dir: Path) -> tuple[bool, dict | None]:
    ok = True

    for entry in snapshot_dir.iterdir():
        if entry.name not in ALLOWED_SNAPSHOT_FILES:
            error(f"{snapshot_dir}: unexpected {'directory' if entry.is_dir() else 'file'} '{entry.name}'")
            ok = False

    missing = [name for name in ALLOWED_SNAPSHOT_FILES if not (snapshot_dir / name).is_file()]
    if missing:
        error(f"{snapshot_dir}: missing required files: {', '.join(sorted(missing))}")
        return False, None

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
        return False, None

    if not isinstance(meta, dict):
        error(f"{snapshot_dir}/meta.json: must be a JSON object")
        return False, None

    ok = validate_meta(meta, tech_id, version, snapshot_dir, llms_full, llms_txt) and ok
    return ok, meta


def find_index_entry(index: dict, tech_id: str, version: str) -> dict | None:
    for project in index.get("projects", []):
        if project.get("id") == tech_id:
            for entry in project.get("versions", []):
                if entry.get("version") == version:
                    return entry
    return None


def validate_index(snapshots: list[tuple[str, str, Path]], metas: dict[tuple[str, str], dict]) -> bool:
    ok = True

    if not snapshots:
        if INDEX_PATH.exists():
            try:
                index = load_json(INDEX_PATH)
            except json.JSONDecodeError as exc:
                error(f"{INDEX_PATH}: invalid JSON ({exc})")
                return False
            if not isinstance(index, dict):
                error(f"{INDEX_PATH}: must be a JSON object")
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

    if not isinstance(index, dict):
        error(f"{INDEX_PATH}: must be a JSON object")
        return False

    generated_at = index.get("generated_at")
    if not isinstance(generated_at, str) or parse_iso8601(generated_at, "generated_at", INDEX_PATH) is None:
        error(f"{INDEX_PATH}: generated_at must be a valid ISO 8601 timestamp")
        ok = False

    projects = index.get("projects")
    if not isinstance(projects, list):
        error(f"{INDEX_PATH}: projects must be an array")
        return False

    indexed: set[tuple[str, str]] = set()
    seen_project_ids: set[str] = set()

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

        if tech_id in seen_project_ids:
            error(f"{INDEX_PATH}: duplicate project id '{tech_id}'")
            ok = False
        seen_project_ids.add(tech_id)

        if not validate_slug(tech_id):
            ok = False

        if not versions:
            error(f"{INDEX_PATH}: project '{tech_id}' must include at least one version")
            ok = False

        for entry in versions:
            if not isinstance(entry, dict):
                error(f"{INDEX_PATH}: version entries must be objects")
                ok = False
                continue

            version = entry.get("version")
            if not isinstance(version, str) or not version.strip():
                error(f"{INDEX_PATH}: version entries require a non-empty version string")
                ok = False
                continue

            key = (tech_id, version)
            if key in indexed:
                error(f"{INDEX_PATH}: duplicate entry for {tech_id}/{version}")
                ok = False
                continue
            indexed.add(key)

            meta = metas.get(key)
            if meta is None:
                continue

            for field in ("source_root", "content_fingerprint"):
                index_value = entry.get(field)
                meta_value = meta.get(field)
                if field == "content_fingerprint" and isinstance(index_value, str) and isinstance(meta_value, str):
                    if index_value.lower() != meta_value.lower():
                        error(f"{INDEX_PATH}: {tech_id}/{version} {field} does not match meta.json")
                        ok = False
                elif index_value != meta_value:
                    error(f"{INDEX_PATH}: {tech_id}/{version} {field} does not match meta.json")
                    ok = False

            index_snapshot_at = entry.get("snapshot_at")
            meta_snapshot_at = meta.get("snapshot_at")
            if not isinstance(index_snapshot_at, str):
                error(f"{INDEX_PATH}: {tech_id}/{version} snapshot_at is required")
                ok = False
            elif index_snapshot_at != meta_snapshot_at:
                error(
                    f"{INDEX_PATH}: {tech_id}/{version} snapshot_at must match meta.json exactly"
                )
                ok = False

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


def validate_snapshot_ids(metas: dict[tuple[str, str], dict]) -> bool:
    ok = True
    seen_ids: dict[str, tuple[str, str]] = {}

    for (tech_id, version), meta in metas.items():
        snapshot_id = meta.get("snapshot_id")
        if not isinstance(snapshot_id, str):
            continue
        if snapshot_id in seen_ids:
            prior = seen_ids[snapshot_id]
            error(
                f"duplicate snapshot_id '{snapshot_id}' for {tech_id}/{version} "
                f"and {prior[0]}/{prior[1]}"
            )
            ok = False
            continue
        seen_ids[snapshot_id] = (tech_id, version)

    return ok


def main() -> int:
    ok = True
    snapshots, layout_ok = discover_snapshots()
    ok = layout_ok and ok
    metas: dict[tuple[str, str], dict] = {}

    for tech_id, version, snapshot_dir in snapshots:
        ok = validate_slug(tech_id) and ok
        snapshot_ok, meta = validate_snapshot(tech_id, version, snapshot_dir)
        ok = snapshot_ok and ok
        if meta is not None:
            metas[(tech_id, version)] = meta

    ok = validate_snapshot_ids(metas) and ok
    ok = validate_index(snapshots, metas) and ok

    if ok:
        print(f"Registry validation passed ({len(snapshots)} snapshot(s)).")
        return 0

    error("Registry validation failed.")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
