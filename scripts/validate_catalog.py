#!/usr/bin/env python3
"""Validate the case catalog without extracting untrusted archives to disk."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import zipfile
from pathlib import Path, PurePosixPath
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
CATALOG_PATH = ROOT / "catalog.json"
REQUIRED_PROVENANCE_FIELDS = {
    "origin",
    "captured_at",
    "license",
    "consent",
    "privacy_review",
    "sanitization_review",
    "publication_status",
    "article_urls",
}
REVIEW_STATES = {"approved", "pending", "rejected"}
PUBLICATION_STATES = {"approved", "pending", "rejected", "legacy-published"}
CONTENT_FORMATS = {"perfetto-protobuf", "legacy-systrace-html", "art-method-trace"}
PACKAGING = {"raw", "zip"}
MAX_ARCHIVE_UNCOMPRESSED_BYTES = 1_000_000_000
MAX_COMPRESSION_RATIO = 200
MAX_ARCHIVE_MEMBERS = 10_000


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def validate_provenance(item: dict[str, Any], label: str) -> list[str]:
    errors: list[str] = []
    missing = REQUIRED_PROVENANCE_FIELDS - set(item)
    if missing:
        errors.append(f"{label}: missing provenance fields: {sorted(missing)}")
        return errors
    if not isinstance(item["origin"], str) or not item["origin"].strip():
        errors.append(f"{label}: origin must be non-empty")
    if item["captured_at"] is not None and not isinstance(item["captured_at"], str):
        errors.append(f"{label}: captured_at must be a string or null")
    if item["license"] is not None and not isinstance(item["license"], str):
        errors.append(f"{label}: license must be a string or null")
    if item["consent"] is not None and not isinstance(item["consent"], str):
        errors.append(f"{label}: consent must be a string or null")
    if item["privacy_review"] not in REVIEW_STATES:
        errors.append(f"{label}: invalid privacy_review")
    if item["sanitization_review"] not in REVIEW_STATES:
        errors.append(f"{label}: invalid sanitization_review")
    if item["publication_status"] not in PUBLICATION_STATES:
        errors.append(f"{label}: invalid publication_status")
    if not isinstance(item["article_urls"], list) or any(
        not isinstance(url, str) or not url.startswith("https://") for url in item["article_urls"]
    ):
        errors.append(f"{label}: article_urls must contain HTTPS URLs only")
    return errors


def validate_zip(path: Path, artifact: dict[str, Any], label: str) -> list[str]:
    errors: list[str] = []
    archive = artifact.get("archive")
    if not isinstance(archive, dict):
        return [f"{label}: zip artifact requires archive metadata"]
    try:
        with zipfile.ZipFile(path) as zipped:
            members = zipped.infolist()
            total_uncompressed = 0
            total_compressed = 0
            for member in members:
                member_path = PurePosixPath(member.filename.replace("\\", "/"))
                first_part = member_path.parts[0] if member_path.parts else ""
                drive_qualified = re.fullmatch(r"[A-Za-z]:", first_part) is not None
                if member_path.is_absolute() or drive_qualified or ".." in member_path.parts:
                    errors.append(f"{label}: unsafe archive member path: {member.filename}")
                if member.flag_bits & 0x1:
                    errors.append(
                        f"{label}: encrypted archive member is not allowed: {member.filename}"
                    )
                total_uncompressed += member.file_size
                total_compressed += member.compress_size

            if len(members) > MAX_ARCHIVE_MEMBERS:
                errors.append(f"{label}: archive exceeds safe member-count limit")
            if total_uncompressed > MAX_ARCHIVE_UNCOMPRESSED_BYTES:
                errors.append(f"{label}: archive exceeds safe uncompressed-size limit")
            if total_compressed and total_uncompressed / total_compressed > MAX_COMPRESSION_RATIO:
                errors.append(f"{label}: archive compression ratio exceeds safe limit")
            if archive.get("member_count") != len(members):
                errors.append(f"{label}: archive member_count mismatch")
            if archive.get("uncompressed_size_bytes") != total_uncompressed:
                errors.append(f"{label}: archive uncompressed_size_bytes mismatch")
            if archive.get("compressed_size_bytes") != path.stat().st_size:
                errors.append(f"{label}: archive compressed_size_bytes mismatch")

            corrupt_member = None if errors else zipped.testzip()
    except zipfile.BadZipFile as exc:
        return [f"{label}: invalid zip: {exc}"]
    except RuntimeError as exc:
        return [f"{label}: unreadable zip: {exc}"]

    if corrupt_member is not None:
        errors.append(f"{label}: CRC check failed for archive member: {corrupt_member}")
    return errors


def discover_artifacts() -> set[str]:
    result: set[str] = set()
    for directory in ROOT.iterdir():
        if not directory.is_dir() or not directory.name.startswith("Android_"):
            continue
        for path in directory.rglob("*"):
            if path.is_file() and path.name != ".DS_Store":
                result.add(path.relative_to(ROOT).as_posix())
    return result


def validate_catalog(check_hashes: bool = True) -> list[str]:
    errors: list[str] = []
    try:
        catalog = json.loads(CATALOG_PATH.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return [f"catalog.json: {exc}"]
    if catalog.get("schema_version") != 1:
        errors.append("catalog.json: schema_version must be 1")
    inventory = catalog.get("inventory")
    if not isinstance(inventory, dict):
        errors.append("catalog.json: inventory must be an object")
    cases = catalog.get("cases")
    if not isinstance(cases, list):
        return errors + ["catalog.json: cases must be a list"]

    case_ids: set[str] = set()
    catalog_paths: set[str] = set()
    for case_index, case in enumerate(cases):
        label = f"cases[{case_index}]"
        if not isinstance(case, dict):
            errors.append(f"{label}: must be an object")
            continue
        case_id = case.get("id")
        if not isinstance(case_id, str) or not case_id:
            errors.append(f"{label}: id is required")
        elif case_id in case_ids:
            errors.append(f"{label}: duplicate id {case_id}")
        else:
            case_ids.add(case_id)
        for field in ("title", "description", "scene"):
            if not isinstance(case.get(field), str) or not case[field].strip():
                errors.append(f"{label}: {field} is required")
        errors.extend(validate_provenance(case, label))
        artifacts = case.get("artifacts")
        if not isinstance(artifacts, list) or not artifacts:
            errors.append(f"{label}: artifacts must be a non-empty list")
            continue

        for artifact_index, artifact in enumerate(artifacts):
            artifact_label = f"{label}.artifacts[{artifact_index}]"
            if not isinstance(artifact, dict):
                errors.append(f"{artifact_label}: must be an object")
                continue
            errors.extend(validate_provenance(artifact, artifact_label))
            raw_path = artifact.get("path")
            if not isinstance(raw_path, str):
                errors.append(f"{artifact_label}: path is required")
                continue
            relative = PurePosixPath(raw_path)
            if relative.is_absolute() or ".." in relative.parts:
                errors.append(f"{artifact_label}: unsafe relative path")
                continue
            if raw_path in catalog_paths:
                errors.append(f"{artifact_label}: duplicate artifact path")
            catalog_paths.add(raw_path)
            path = ROOT / Path(*relative.parts)
            if not path.is_file():
                errors.append(f"{artifact_label}: file does not exist: {raw_path}")
                continue
            if artifact.get("content_format") not in CONTENT_FORMATS:
                errors.append(f"{artifact_label}: invalid content_format")
            packaging = artifact.get("packaging")
            if packaging not in PACKAGING:
                errors.append(f"{artifact_label}: invalid packaging")
            if artifact.get("size_bytes") != path.stat().st_size:
                errors.append(f"{artifact_label}: size_bytes mismatch")
            digest = artifact.get("sha256")
            if not isinstance(digest, str) or len(digest) != 64:
                errors.append(f"{artifact_label}: sha256 must be a 64-character digest")
            elif check_hashes and sha256(path) != digest:
                errors.append(f"{artifact_label}: sha256 mismatch")
            if packaging == "zip":
                errors.extend(validate_zip(path, artifact, artifact_label))
            elif "archive" in artifact:
                errors.append(f"{artifact_label}: raw artifact must not declare archive metadata")

    discovered = discover_artifacts()
    if catalog_paths != discovered:
        for path in sorted(discovered - catalog_paths):
            errors.append(f"uncataloged artifact: {path}")
        for path in sorted(catalog_paths - discovered):
            errors.append(f"catalog path is outside the artifact inventory: {path}")
    if isinstance(inventory, dict):
        if inventory.get("case_count") != len(cases):
            errors.append("catalog.json: inventory case_count mismatch")
        if inventory.get("artifact_count") != len(catalog_paths):
            errors.append("catalog.json: inventory artifact_count mismatch")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--skip-hashes", action="store_true", help="skip SHA-256 calculation")
    args = parser.parse_args()
    errors = validate_catalog(check_hashes=not args.skip_hashes)
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    catalog = json.loads(CATALOG_PATH.read_text(encoding="utf-8"))
    case_count = len(catalog["cases"])
    artifact_count = sum(len(case["artifacts"]) for case in catalog["cases"])
    print(f"OK: {case_count} cases and {artifact_count} artifacts validated")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
