from __future__ import annotations

import argparse
import csv
import difflib
import hashlib
import json
import os
import posixpath
import re
import shutil
import tempfile
import uuid
import zipfile
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable
from urllib.parse import unquote
from xml.etree import ElementTree as ET


DEFAULT_BOOK_ROOT = Path(__file__).resolve().parents[1]
CONTRACT_PATH = "state/translation_contract.json"
ALLOWED_PROPER_NOUN_MODES = {"all_chinese", "all_source", "hybrid"}
ALLOWED_STATES = {"initial", "translated", "reviewed", "final", "needs_rerender", "needs_retranslation"}
REQUIRED_NAME_COLUMNS = {
    "entity_id",
    "source_name",
    "target_name",
    "category",
    "display_policy",
    "first_rendering",
    "subsequent_rendering",
    "note_required",
    "repeat_original_allowed_when",
    "notes",
    "source_aliases",
    "target_aliases",
    "scope",
    "status",
    "chinese_gloss",
    "display_strategy",
    "first_occurrence_rule",
    "same_name_disambiguation",
}
REQUIRED_OCCURRENCE_COLUMNS = {
    "occurrence_id",
    "source_file",
    "unit_id",
    "start_offset",
    "end_offset",
    "source_form",
    "entity_id",
    "disambiguation_evidence",
    "is_body_occurrence",
    "counts_as_first_body_occurrence",
    "status",
}
XLIFF_NS = "urn:oasis:names:tc:xliff:document:2.0"
ET.register_namespace("", XLIFF_NS)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Manage LifeBook canonical source-target units and optional XLIFF 2.1 exchange."
    )
    parser.add_argument("--book-root", default=None)
    sub = parser.add_subparsers(dest="command", required=True)

    configure = sub.add_parser("configure-contract", help="Record preproduction choices without locking evidence.")
    configure.add_argument("--source-language", required=True)
    configure.add_argument("--target-language", required=True)
    configure.add_argument("--edition-type", choices=("target_only", "bilingual_parallel"), required=True)
    configure.add_argument("--proper-noun-mode", choices=sorted(ALLOWED_PROPER_NOUN_MODES), default=None)
    configure.add_argument("--proper-noun-policy", choices=("1", "2", "3", "4", "5"), default=None)
    configure.add_argument("--decision-id", default="")
    configure.add_argument("--alignment-granularity", choices=("short_paragraph",), default="short_paragraph")

    lock = sub.add_parser("lock-contract", help="Lock preproduction choices and verified register evidence.")
    lock.add_argument("--source-language", default=None)
    lock.add_argument("--target-language", default=None)
    lock.add_argument("--edition-type", choices=("target_only", "bilingual_parallel"), default=None)
    lock.add_argument("--proper-noun-mode", choices=sorted(ALLOWED_PROPER_NOUN_MODES), default=None)
    lock.add_argument("--proper-noun-policy", choices=("1", "2", "3", "4", "5"), default=None)
    lock.add_argument("--decision-id", default="")
    lock.add_argument("--alignment-granularity", choices=("short_paragraph",), default="short_paragraph")

    sub.add_parser("validate-contract", help="Validate the locked user contract and proper-noun decision set.")
    sub.add_parser("discover-proper-nouns", help="Refresh the whole-source proper-noun candidate decision table.")
    sub.add_parser("build-proper-noun-ledger", help="Build occurrence ledger for locked candidate entity decisions.")
    finish_names = sub.add_parser("lock-proper-noun-discovery", help="Lock discovery using an immutable manual-review record.")
    finish_names.add_argument("--review-record", default=None)

    init_units = sub.add_parser("init-units", help="Create or refresh canonical units from source natural paragraphs.")
    init_units.add_argument("--discard-existing-targets", action="store_true")

    refresh = sub.add_parser("refresh-derived", help="Refresh target hashes and invalidate stale review metadata.")
    refresh.add_argument("--promote-initial", action="store_true")
    sub.add_parser("render-proper-nouns", help="Render entity placeholders using only the locked CSV and occurrence ledger.")

    create_patch = sub.add_parser("create-chapter-patch", help="Create a worker-owned chapter patch against the immutable current manifest.")
    create_patch.add_argument("--chapter", required=True)
    create_patch.add_argument("--updates", required=True)
    create_patch.add_argument("--output", required=True)
    create_patch.add_argument("--owner-run-id", required=True)

    merge_patch = sub.add_parser("merge-chapter-patch", help="CAS-merge one chapter patch into a new canonical generation.")
    merge_patch.add_argument("--input", required=True)

    migration = sub.add_parser("migrate-legacy", help="Audit legacy translated/final projections and apply only an exact CSV-renderable migration.")
    migration.add_argument("--report", default="output/legacy_migration_report.json")
    migration.add_argument("--apply", action="store_true")
    migration.add_argument("--owner-run-id", default="")

    rollback = sub.add_parser("rollback-generation", help="Restore an immutable generation as a new auditable generation.")
    rollback.add_argument("--generation-id", required=True)
    rollback.add_argument("--reason", required=True)

    validate = sub.add_parser("validate", help="Validate contract, source coverage, units, names, and reviews.")
    validate.add_argument("--allow-incomplete", action="store_true")
    validate.add_argument("--require-semantic-audit", action="store_true")
    validate.add_argument("--write-report", action="store_true")

    sub.add_parser("materialize", help="Project canonical targets to translated/final and compatibility alignment map.")

    export = sub.add_parser("export-xliff", help="Export optional XLIFF 2.1 exchange file.")
    export.add_argument("--output", default=None)

    import_xliff = sub.add_parser("import-xliff", help="Safely import targets for known units from XLIFF 2.1.")
    import_xliff.add_argument("--input", default=None)

    prepare = sub.add_parser("prepare-audit", help="Prepare an immutable hash-bound semantic audit run.")
    prepare.add_argument("--chapter", default=None)
    prepare.add_argument("--reviewer", required=True)
    prepare.add_argument("--model", required=True)
    prepare.add_argument("--run-id", default=None)
    audit = sub.add_parser("validate-audit", help="Validate per-unit audits and full-chapter review records.")
    audit.add_argument("--chapter", default=None)
    audit.add_argument("--write-report", action="store_true")

    artifacts = sub.add_parser("verify-artifacts", help="Verify canonical target hashes and reader-visible EPUB units.")
    artifacts.add_argument("--write-report", action="store_true")
    reader_mode = artifacts.add_mutually_exclusive_group()
    reader_mode.add_argument("--require-reader", action="store_true")
    reader_mode.add_argument("--reader-if-available", action="store_true")
    return parser.parse_args()


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig").replace("\r\n", "\n").replace("\r", "\n")


def write_text(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f".{path.name}.{uuid.uuid4().hex}.tmp")
    temporary.write_text(value, encoding="utf-8")
    os.replace(temporary, path)


def read_json(path: Path) -> dict:
    value = json.loads(read_text(path))
    if not isinstance(value, dict):
        raise ValueError(f"JSON root must be an object: {path}")
    return value


def write_json(path: Path, value: object) -> None:
    write_text(path, json.dumps(value, ensure_ascii=False, indent=2) + "\n")


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha256_text(value: str) -> str:
    return sha256_bytes(value.encode("utf-8"))


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def canonical_json_digest(value: object) -> str:
    return sha256_text(json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")))


def resolve_inside(book_root: Path, relative: str) -> Path:
    root = book_root.resolve()
    path = (root / relative).resolve()
    if path != root and root not in path.parents:
        raise ValueError(f"Configured path escapes book root: {relative}")
    return path


def contract_digest(contract: dict) -> str:
    copy = json.loads(json.dumps(contract))
    copy["contract_sha256"] = ""
    copy["locked_at"] = ""
    return canonical_json_digest(copy)


def load_contract(book_root: Path) -> tuple[Path, dict]:
    path = book_root / CONTRACT_PATH
    if not path.is_file():
        raise ValueError(f"Missing translation contract: {CONTRACT_PATH}")
    return path, read_json(path)


def contract_path(contract: dict, section: str, key: str) -> str:
    value = contract.get(section)
    if not isinstance(value, dict) or not str(value.get(key) or "").strip():
        raise ValueError(f"translation contract lacks {section}.{key}")
    return str(value[key])


def parse_aliases(value: str) -> list[str]:
    return [item.strip() for item in re.split(r"[;|]", value or "") if item.strip()]


def find_form_occurrences(text: str, forms: Iterable[str]) -> list[tuple[int, int, str]]:
    """Return deterministic longest-first, non-overlapping registered-name spans."""
    candidates: list[tuple[int, int, str]] = []
    for form in sorted({item for item in forms if item}, key=lambda item: (-len(item), item.casefold())):
        candidates.extend((match.start(), match.end(), form) for match in re.finditer(re.escape(form), text))
    selected: list[tuple[int, int, str]] = []
    cursor = 0
    for start, end, form in sorted(candidates, key=lambda item: (item[0], -(item[1] - item[0]), item[2].casefold())):
        if start < cursor:
            continue
        selected.append((start, end, form))
        cursor = end
    return selected


def load_name_rows(book_root: Path, contract: dict) -> tuple[Path, list[dict[str, str]], set[str]]:
    path = resolve_inside(book_root, contract_path(contract, "proper_nouns", "register"))
    if not path.is_file():
        raise ValueError(f"Missing proper-noun register: {path.relative_to(book_root).as_posix()}")
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        columns = set(reader.fieldnames or [])
        rows = [{key: (value or "").strip() for key, value in row.items()} for row in reader if any(row.values())]
    return path, rows, columns


def load_candidate_rows(book_root: Path, contract: dict) -> tuple[Path, list[dict[str, str]]]:
    path = resolve_inside(book_root, contract_path(contract, "proper_nouns", "candidate_decisions"))
    if not path.is_file():
        raise ValueError(f"Missing proper-noun candidate decisions: {path.relative_to(book_root).as_posix()}")
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return path, [dict(row) for row in csv.DictReader(handle) if any(row.values())]


def load_manual_candidate_rows(book_root: Path, contract: dict) -> tuple[Path, list[dict[str, str]]]:
    path = resolve_inside(book_root, contract_path(contract, "proper_nouns", "manual_candidates"))
    if not path.is_file():
        raise ValueError(f"Missing manual proper-noun candidates: {path.relative_to(book_root).as_posix()}")
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        expected = {"source_form", "files", "notes"}
        if not expected.issubset(set(reader.fieldnames or [])):
            raise ValueError("proper_noun_manual_candidates.csv requires source_form,files,notes")
        return path, [{key: (value or "").strip() for key, value in row.items()} for row in reader if any(row.values())]


def load_occurrence_rows(book_root: Path, contract: dict) -> tuple[Path, list[dict[str, str]], set[str]]:
    path = resolve_inside(book_root, contract_path(contract, "proper_nouns", "occurrence_ledger"))
    if not path.is_file():
        raise ValueError(f"Missing proper-noun occurrence ledger: {path.relative_to(book_root).as_posix()}")
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        columns = set(reader.fieldnames or [])
        rows = [{key: (value or "").strip() for key, value in row.items()} for row in reader if any(row.values())]
    return path, rows, columns


def source_file_records(book_root: Path, contract: dict) -> list[dict[str, str]]:
    return [
        {"path": path.relative_to(book_root).as_posix(), "sha256": sha256_file(path), "status": "SCANNED"}
        for path in source_files(book_root, contract)
    ]


def corpus_digest(records: list[dict[str, str]]) -> str:
    return canonical_json_digest([{"path": row["path"], "sha256": row["sha256"]} for row in records])


def validate_discovery_manifest(book_root: Path, contract: dict) -> list[str]:
    issues: list[str] = []
    proper = contract.get("proper_nouns") if isinstance(contract.get("proper_nouns"), dict) else {}
    try:
        path = resolve_inside(book_root, contract_path(contract, "proper_nouns", "discovery_manifest"))
        manifest = read_json(path)
        candidate_path, candidates = load_candidate_rows(book_root, contract)
        manual_candidate_path, manual_candidates = load_manual_candidate_rows(book_root, contract)
        register_path, names, _columns = load_name_rows(book_root, contract)
        occurrence_path, occurrences, occurrence_columns = load_occurrence_rows(book_root, contract)
    except (OSError, ValueError, csv.Error, json.JSONDecodeError) as exc:
        return [str(exc)]
    missing_occurrence_columns = sorted(REQUIRED_OCCURRENCE_COLUMNS - occurrence_columns)
    if missing_occurrence_columns:
        issues.append("proper_noun_occurrences.csv missing columns: " + ", ".join(missing_occurrence_columns))
    records = source_file_records(book_root, contract)
    if not records:
        issues.append("DISCOVERY_EVIDENCE_MISSING: source corpus is empty")
    if manifest.get("status") != "LOCKED":
        issues.append("DISCOVERY_EVIDENCE_MISSING: discovery manifest status must be LOCKED")
    if not str(manifest.get("discovery_engine") or "").strip() or not str(manifest.get("discovery_engine_version") or "").strip():
        issues.append("DISCOVERY_EVIDENCE_MISSING: discovery engine and version are required")
    plugins = manifest.get("language_plugins")
    if not isinstance(plugins, list) or not plugins:
        issues.append("DISCOVERY_EVIDENCE_MISSING: at least one language plugin is required")
    if manifest.get("source_files") != records or manifest.get("source_corpus_sha256") != corpus_digest(records):
        issues.append("DISCOVERY_EVIDENCE_STALE: discovery manifest does not bind the current complete source corpus")
    if manifest.get("candidate_count") != len(candidates):
        issues.append("DISCOVERY_EVIDENCE_STALE: candidate count mismatch")
    if manifest.get("manual_candidate_count") != len(manual_candidates):
        issues.append("DISCOVERY_EVIDENCE_STALE: manual candidate count mismatch")
    decided = sum(str(row.get("decision") or "").strip() in {"registered", "not_proper_noun"} for row in candidates)
    unresolved = len(candidates) - decided
    if manifest.get("decided_candidate_count") != decided or manifest.get("unresolved_candidate_count") != unresolved or unresolved:
        issues.append("DISCOVERY_UNRESOLVED: every discovered candidate requires a decision")
    if not candidates and not str(manifest.get("no_candidate_reason") or "").strip():
        issues.append("DISCOVERY_EVIDENCE_MISSING: zero candidates requires a documented no_candidate_reason")
    if manifest.get("manual_review_complete") is not True:
        issues.append("DISCOVERY_EVIDENCE_MISSING: full-source manual review must be recorded")
    if manifest.get("occurrence_count") != len(occurrences):
        issues.append("DISCOVERY_EVIDENCE_STALE: occurrence count mismatch")
    unresolved_occurrences = sum(row.get("status") != "locked" or not row.get("entity_id") for row in occurrences)
    if manifest.get("unresolved_occurrence_count") != unresolved_occurrences or unresolved_occurrences:
        issues.append("ENTITY_DISAMBIGUATION_FAILED: every occurrence must be locked to an entity")
    for key, expected in (
        ("candidate_decisions_sha256", sha256_file(candidate_path)),
        ("manual_candidates_sha256", sha256_file(manual_candidate_path)),
        ("proper_nouns_sha256", sha256_file(register_path)),
        ("occurrence_ledger_sha256", sha256_file(occurrence_path)),
    ):
        if manifest.get(key) != expected:
            issues.append(f"DISCOVERY_EVIDENCE_STALE: {key} mismatch")
    try:
        review_path = resolve_inside(book_root, contract_path(contract, "proper_nouns", "manual_review_record"))
        if not review_path.is_file() or manifest.get("manual_review_record_sha256") != sha256_file(review_path):
            issues.append("DISCOVERY_EVIDENCE_STALE: manual review record hash mismatch")
    except ValueError as exc:
        issues.append(str(exc))
    if proper.get("discovery_manifest_sha256") and proper.get("discovery_manifest_sha256") != sha256_file(path):
        issues.append("DISCOVERY_EVIDENCE_STALE: locked discovery manifest hash mismatch")
    return issues


def validate_name_register(book_root: Path, contract: dict) -> list[str]:
    issues: list[str] = []
    try:
        _path, rows, columns = load_name_rows(book_root, contract)
    except (OSError, ValueError, csv.Error) as exc:
        return [str(exc)]
    missing = sorted(REQUIRED_NAME_COLUMNS - columns)
    if missing:
        issues.append(f"proper_nouns.csv missing columns: {', '.join(missing)}")
        return issues
    mode = str((contract.get("proper_nouns") or {}).get("mode") or "")
    seen_entities: set[str] = set()
    for index, row in enumerate(rows, start=2):
        entity_id = row["entity_id"]
        source = row["source_name"]
        target = row["target_name"] or row["chinese_gloss"]
        if not entity_id:
            issues.append(f"proper_nouns.csv:{index}: entity_id is required")
        elif entity_id in seen_entities:
            issues.append(f"proper_nouns.csv:{index}: duplicate entity_id {entity_id!r}")
        seen_entities.add(entity_id)
        if not source:
            issues.append(f"proper_nouns.csv:{index}: source_name is required")
            continue
        if row["status"] != "locked":
            issues.append(f"proper_nouns.csv:{index}: status must be locked for {source!r}")
        policy = row["display_policy"]
        if policy not in {"1", "2", "3", "4", "5"}:
            issues.append(f"proper_nouns.csv:{index}: display_policy must be 1..5 for {source!r}")
        if not row["display_strategy"]:
            issues.append(f"proper_nouns.csv:{index}: display_strategy is required for {source!r}")
        if not row["first_occurrence_rule"]:
            issues.append(f"proper_nouns.csv:{index}: first_occurrence_rule is required for {source!r}")
        if not row["same_name_disambiguation"]:
            issues.append(f"proper_nouns.csv:{index}: same_name_disambiguation is required for {source!r}")
        if mode == "all_chinese":
            if not target:
                issues.append(f"proper_nouns.csv:{index}: all_chinese requires a Chinese form for {source!r}")
            if target and (target not in row["first_rendering"] or target not in row["subsequent_rendering"]):
                issues.append(f"proper_nouns.csv:{index}: all_chinese renderings must use the Chinese form for {source!r}")
        elif mode == "all_source":
            if source not in row["first_rendering"] or source not in row["subsequent_rendering"]:
                issues.append(f"proper_nouns.csv:{index}: all_source renderings must retain {source!r}")
        elif mode == "hybrid":
            if row["display_strategy"] not in {
                "established_chinese_only",
                "source_only",
                "target_source_then_target",
                "target_source_then_source",
                "target_source_note_then_target",
                "source_first_chinese_gloss_then_source",
            }:
                issues.append(
                    f"proper_nouns.csv:{index}: unsupported hybrid display_strategy for {source!r}"
                )
        strategy_by_policy = {
            "1": {"established_chinese_only"},
            "2": {"source_only"},
            "3": {"target_source_then_target"},
            "4": {"target_source_then_source", "source_first_chinese_gloss_then_source"},
            "5": {"target_source_note_then_target"},
        }
        if policy in strategy_by_policy and row["display_strategy"] not in strategy_by_policy[policy]:
            issues.append(f"proper_nouns.csv:{index}: display_policy and display_strategy disagree for {source!r}")
        if policy == "1":
            if not target or row["first_rendering"] != target or row["subsequent_rendering"] != target:
                issues.append(f"proper_nouns.csv:{index}: policy 1 must render only the target form for {source!r}")
        elif policy == "2":
            if row["first_rendering"] != source or row["subsequent_rendering"] != source:
                issues.append(f"proper_nouns.csv:{index}: policy 2 must render only the source form for {source!r}")
        elif policy in {"3", "4", "5"}:
            gloss = row["chinese_gloss"] or target
            if not gloss or source not in row["first_rendering"] or gloss not in row["first_rendering"]:
                issues.append(f"proper_nouns.csv:{index}: policy {policy} first_rendering needs source and Chinese form for {source!r}")
            expected_subsequent = source if policy == "4" else target
            if row["subsequent_rendering"] != expected_subsequent:
                issues.append(f"proper_nouns.csv:{index}: policy {policy} subsequent_rendering is inconsistent for {source!r}")
            if policy == "5" and row["note_required"].casefold() != "true":
                issues.append(f"proper_nouns.csv:{index}: policy 5 requires note_required=true for {source!r}")
    by_source: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        by_source[row["source_name"].casefold()].append(row)
    for source_key, same_name_rows in by_source.items():
        if len(same_name_rows) < 2:
            continue
        scopes = {row.get("scope", "") for row in same_name_rows}
        if "" in scopes or len(scopes) != len(same_name_rows):
            issues.append(f"ENTITY_DISAMBIGUATION_FAILED: same-name entities {source_key!r} require distinct non-empty scopes")
        for row in same_name_rows:
            evidence = row.get("same_name_disambiguation", "").strip().casefold()
            if evidence in {"", "n/a", "na", "none", "不适用"}:
                issues.append(f"ENTITY_DISAMBIGUATION_FAILED: {row.get('entity_id')!r} requires executable disambiguation evidence")
    try:
        _candidate_path, candidates = load_candidate_rows(book_root, contract)
    except (OSError, ValueError, csv.Error) as exc:
        issues.append(str(exc))
        return issues
    registered_entities = set()
    registered_forms = set()
    for row in rows:
        registered_entities.add(row["entity_id"])
        registered_forms.add(row["source_name"].casefold())
        registered_forms.update(item.casefold() for item in parse_aliases(row["source_aliases"]))
    for index, row in enumerate(candidates, start=2):
        decision = str(row.get("decision") or "").strip()
        form = str(row.get("source_form") or "").strip()
        if decision not in {"registered", "not_proper_noun"}:
            issues.append(f"proper_noun_candidates.csv:{index}: unresolved decision for {form!r}")
        if decision == "registered":
            entity = str(row.get("entity_id") or "").strip()
            if entity not in registered_entities:
                issues.append(f"proper_noun_candidates.csv:{index}: registered candidate {form!r} is absent from proper_nouns.csv")
    try:
        _occurrence_path, occurrences, occurrence_columns = load_occurrence_rows(book_root, contract)
        missing_occurrence_columns = sorted(REQUIRED_OCCURRENCE_COLUMNS - occurrence_columns)
        if missing_occurrence_columns:
            issues.append("proper_noun_occurrences.csv missing columns: " + ", ".join(missing_occurrence_columns))
        seen_occurrences: set[str] = set()
        for index, row in enumerate(occurrences, start=2):
            occurrence_id = row.get("occurrence_id", "")
            if not occurrence_id or occurrence_id in seen_occurrences:
                issues.append(f"proper_noun_occurrences.csv:{index}: occurrence_id must be unique")
            seen_occurrences.add(occurrence_id)
            if row.get("entity_id") not in registered_entities:
                issues.append(f"proper_noun_occurrences.csv:{index}: unknown entity_id {row.get('entity_id')!r}")
            if row.get("status") != "locked" or not row.get("disambiguation_evidence"):
                issues.append(f"proper_noun_occurrences.csv:{index}: occurrence must be locked with disambiguation evidence")
        _manifest_path, store_path = unit_paths(book_root, contract)
        if store_path.is_file():
            units_by_id = {str(unit.get("unit_id")): unit for unit in read_units(store_path)}
            expected_occurrences: set[tuple[str, int, int, str]] = set()
            forms: set[str] = set()
            for row in rows:
                forms.update(item for item in [row.get("source_name", ""), *parse_aliases(row.get("source_aliases", ""))] if item)
            for unit_id, unit in units_by_id.items():
                source_text = str(unit.get("source_text") or "")
                for start, end, form in find_form_occurrences(source_text, forms):
                    expected_occurrences.add((unit_id, start, end, form))
            actual_occurrences: set[tuple[str, int, int, str]] = set()
            first_counts: dict[str, int] = defaultdict(int)
            entity_forms = {
                row["entity_id"]: {item for item in [row.get("source_name", ""), *parse_aliases(row.get("source_aliases", ""))] if item}
                for row in rows
            }
            for index, row in enumerate(occurrences, start=2):
                try:
                    start, end = int(row["start_offset"]), int(row["end_offset"])
                except (KeyError, ValueError):
                    issues.append(f"proper_noun_occurrences.csv:{index}: offsets must be integers")
                    continue
                unit = units_by_id.get(row.get("unit_id", ""))
                if not unit or str(unit.get("source_file")) != row.get("source_file"):
                    issues.append(f"proper_noun_occurrences.csv:{index}: unit/source_file does not exist")
                    continue
                source_text = str(unit.get("source_text") or "")
                if start < 0 or end > len(source_text) or source_text[start:end] != row.get("source_form"):
                    issues.append(f"proper_noun_occurrences.csv:{index}: source span does not match canonical source")
                if row.get("source_form") not in entity_forms.get(row.get("entity_id", ""), set()):
                    issues.append(f"proper_noun_occurrences.csv:{index}: source form is not registered for entity")
                actual_occurrences.add((row.get("unit_id", ""), start, end, row.get("source_form", "")))
                if row.get("counts_as_first_body_occurrence") == "true":
                    first_counts[row.get("entity_id", "")] += 1
                    if row.get("is_body_occurrence") != "true":
                        issues.append(f"proper_noun_occurrences.csv:{index}: heading/navigation cannot count as first body occurrence")
            if actual_occurrences != expected_occurrences:
                issues.append("ENTITY_DISAMBIGUATION_FAILED: occurrence ledger does not cover the exact registered source-form occurrences")
            for entity_id, count in first_counts.items():
                if count != 1:
                    issues.append(f"ENTITY_DISAMBIGUATION_FAILED: entity {entity_id!r} has {count} first-body occurrences")
    except (OSError, ValueError, csv.Error) as exc:
        issues.append(str(exc))
    return issues


def validate_contract(book_root: Path, contract: dict) -> list[str]:
    issues: list[str] = []
    if contract.get("schema_version") != "2.0":
        issues.append("translation contract schema_version must be 2.0")
    if contract.get("status") != "LOCKED":
        issues.append("translation contract status must be LOCKED")
    if not str(contract.get("source_language") or "").strip() or not str(contract.get("target_language") or "").strip():
        issues.append("source_language and target_language are required")
    if contract.get("edition_type") not in {"target_only", "bilingual_parallel"}:
        issues.append("edition_type must be target_only or bilingual_parallel")
    bilingual = contract.get("bilingual") if isinstance(contract.get("bilingual"), dict) else {}
    expected = {
        "alignment_granularity": "short_paragraph",
        "order": "source_then_target",
        "source_natural_paragraph_boundary": "non_crossable",
        "sentence_by_sentence_display": "forbidden",
        "page_grouped_languages": "forbidden",
    }
    for key, value in expected.items():
        if bilingual.get(key) != value:
            issues.append(f"bilingual.{key} must be {value!r}")
    if bilingual.get("complete_translation_required") is not True:
        issues.append("bilingual.complete_translation_required must be true")
    minimum = bilingual.get("preferred_source_words_min")
    maximum = bilingual.get("preferred_source_words_max")
    if not isinstance(minimum, int) or not isinstance(maximum, int) or minimum <= 0 or maximum < minimum:
        issues.append("bilingual preferred source word bounds must be positive and max >= min")
    if bilingual.get("segmentation_engine") != "markdown_ast" or not str(bilingual.get("segmentation_engine_version") or "").strip():
        issues.append("bilingual segmentation engine must be versioned markdown_ast")
    proper = contract.get("proper_nouns") if isinstance(contract.get("proper_nouns"), dict) else {}
    if proper.get("mode") not in ALLOWED_PROPER_NOUN_MODES:
        issues.append("proper_nouns.mode must be selected or resolved to the approved default")
    if proper.get("selection_source") not in {"user", "default"}:
        issues.append("proper_nouns.selection_source must be user or default")
    if proper.get("selection_source") == "default" and (proper.get("policy_code") != "3" or proper.get("mode") != "hybrid"):
        issues.append("default proper-noun selection must resolve to policy 3 / hybrid")
    if proper.get("policy_code") not in {"1", "2", "3", "4", "5"}:
        issues.append("proper_nouns.policy_code must be 1..5")
    if proper.get("selection_source") == "user" and not str(proper.get("decision_id") or "").strip():
        issues.append("user-selected proper-noun mode requires decision_id")
    if not str(proper.get("policy_version") or "").strip() or not str(proper.get("selected_at") or "").strip():
        issues.append("proper-noun selection policy_version and selected_at are required")
    if proper.get("discovery_status") != "LOCKED":
        issues.append("proper_nouns.discovery_status must be LOCKED")
    for section, key, hash_key in (
        ("proper_nouns", "register", "register_sha256"),
        ("proper_nouns", "manual_candidates", "manual_candidates_sha256"),
        ("proper_nouns", "candidate_decisions", "candidate_decisions_sha256"),
        ("proper_nouns", "occurrence_ledger", "occurrence_ledger_sha256"),
        ("proper_nouns", "discovery_manifest", "discovery_manifest_sha256"),
        ("terminology", "register", "register_sha256"),
    ):
        try:
            path = resolve_inside(book_root, contract_path(contract, section, key))
        except ValueError as exc:
            issues.append(str(exc))
            continue
        expected_hash = str((contract.get(section) or {}).get(hash_key) or "")
        if not path.is_file():
            issues.append(f"missing locked input: {path.relative_to(book_root).as_posix()}")
        elif expected_hash != sha256_file(path):
            issues.append(f"locked hash mismatch; relock contract: {path.relative_to(book_root).as_posix()}")
    if contract.get("contract_sha256") != contract_digest(contract):
        issues.append("translation contract hash is stale; relock contract")
    issues.extend(validate_name_register(book_root, contract))
    issues.extend(validate_discovery_manifest(book_root, contract))
    xliff = contract.get("xliff") if isinstance(contract.get("xliff"), dict) else {}
    try:
        schema_path = resolve_inside(book_root, str(xliff.get("core_schema") or ""))
        if xliff.get("schema_validation_required") is not True:
            issues.append("xliff.schema_validation_required must be true")
        elif not schema_path.is_file() or sha256_file(schema_path) != xliff.get("core_schema_sha256"):
            issues.append("official XLIFF schema is missing or stale")
    except ValueError as exc:
        issues.append(str(exc))
    return issues


def configure_contract(book_root: Path, args: argparse.Namespace) -> None:
    path, contract = load_contract(book_root)
    contract["source_language"] = args.source_language
    contract["target_language"] = args.target_language
    contract["edition_type"] = args.edition_type
    contract["bilingual"]["alignment_granularity"] = args.alignment_granularity
    contract["bilingual"]["segmentation_engine_version"] = "lifebook-markdown-ast-v1"
    proper = contract["proper_nouns"]
    selected_policy = args.proper_noun_policy or ({"all_chinese": "1", "all_source": "2", "hybrid": "3"}.get(args.proper_noun_mode or ""))
    if selected_policy:
        proper["mode"] = {"1": "all_chinese", "2": "all_source"}.get(selected_policy, "hybrid")
        proper["selection_source"] = "user"
        proper["selection_reason"] = "explicit_user_choice"
        proper["decision_id"] = args.decision_id or f"user-{uuid.uuid4()}"
        proper["policy_code"] = selected_policy
    else:
        proper["mode"] = "hybrid"
        proper["policy_code"] = "3"
        proper["selection_source"] = "default"
        proper["selection_reason"] = "user_did_not_specify"
        proper["decision_id"] = ""
    proper["selected_at"] = utc_now()
    proper["discovery_status"] = "INCOMPLETE"
    contract["status"] = "PREPRODUCTION_REQUIRED"
    contract["locked_at"] = ""
    contract["contract_sha256"] = ""
    write_json(path, contract)
    print(f"translation contract configured: proper_nouns={proper['mode']} source={proper['selection_source']}")


def lock_contract(book_root: Path, args: argparse.Namespace) -> None:
    path, contract = load_contract(book_root)
    contract["source_language"] = args.source_language or contract.get("source_language")
    contract["target_language"] = args.target_language or contract.get("target_language")
    contract["edition_type"] = args.edition_type or contract.get("edition_type")
    contract["bilingual"]["alignment_granularity"] = args.alignment_granularity
    contract["bilingual"]["segmentation_engine_version"] = "lifebook-markdown-ast-v1"
    proper = contract["proper_nouns"]
    selected_policy = args.proper_noun_policy or ({"all_chinese": "1", "all_source": "2", "hybrid": "3"}.get(args.proper_noun_mode or ""))
    if selected_policy:
        proper["mode"] = {"1": "all_chinese", "2": "all_source"}.get(selected_policy, "hybrid")
        proper["selection_source"] = "user"
        proper["selection_reason"] = "explicit_user_choice"
        proper["decision_id"] = args.decision_id or f"user-{uuid.uuid4()}"
        proper["policy_code"] = selected_policy
        proper["selected_at"] = utc_now()
    elif proper.get("selection_source") not in {"user", "default"}:
        proper.update({
            "mode": "hybrid",
            "policy_code": "3",
            "selection_source": "default",
            "selection_reason": "user_did_not_specify",
            "decision_id": "",
            "selected_at": utc_now(),
        })
    contract["proper_nouns"]["discovery_status"] = "LOCKED"
    for section, key, hash_key in (
        ("proper_nouns", "register", "register_sha256"),
        ("proper_nouns", "manual_candidates", "manual_candidates_sha256"),
        ("proper_nouns", "candidate_decisions", "candidate_decisions_sha256"),
        ("proper_nouns", "occurrence_ledger", "occurrence_ledger_sha256"),
        ("proper_nouns", "discovery_manifest", "discovery_manifest_sha256"),
        ("terminology", "register", "register_sha256"),
    ):
        input_path = resolve_inside(book_root, contract_path(contract, section, key))
        if not input_path.is_file():
            raise SystemExit(f"Cannot lock missing input: {input_path.relative_to(book_root).as_posix()}")
        contract[section][hash_key] = sha256_file(input_path)
    contract["status"] = "LOCKED"
    contract["locked_at"] = utc_now()
    contract["contract_sha256"] = contract_digest(contract)
    issues = validate_contract(book_root, contract)
    if issues:
        raise SystemExit("Contract lock rejected:\n- " + "\n- ".join(issues))
    write_json(path, contract)
    print(f"translation contract locked: {contract['contract_sha256']}")


NAME_PATTERN = re.compile(
    r"(?<![A-Za-zÀ-ÖØ-öø-ÿ])"
    r"(?:[A-ZÀ-ÖØ-ÞÆŒ][A-Za-zÀ-ÖØ-öø-ÿÆŒæœ'’-]+)"
    r"(?:\s+(?:(?:of|the|de|del|da|di|van|von|la|le)\s+)?[A-ZÀ-ÖØ-ÞÆŒ][A-Za-zÀ-ÖØ-öø-ÿÆŒæœ'’-]+){0,4}"
)
NAME_STOPWORDS = {
    "A", "An", "And", "As", "At", "But", "By", "Chapter", "For", "From", "He", "Her", "His", "I",
    "If", "In", "It", "Its", "No", "Not", "Of", "On", "Or", "Our", "She", "Since", "That", "The",
    "Their", "There", "These", "They", "This", "Those", "To", "Under", "We", "When", "Where", "Which",
    "While", "Who", "With", "Yet",
}


def source_files(book_root: Path, contract: dict) -> list[Path]:
    root = resolve_inside(book_root, contract_path(contract, "canonical_units", "source_root"))
    return sorted(path for path in root.glob("*.md") if path.is_file())


def discover_proper_nouns(book_root: Path, contract: dict) -> None:
    path, old_rows = load_candidate_rows(book_root, contract)
    manual_path, manual_rows = load_manual_candidate_rows(book_root, contract)
    old = {str(row.get("source_form") or "").strip(): row for row in old_rows}
    hits: dict[str, list[str]] = defaultdict(list)
    for file in source_files(book_root, contract):
        relative = file.relative_to(book_root).as_posix()
        for match in NAME_PATTERN.finditer(read_text(file)):
            value = re.sub(r"\s+", " ", match.group(0)).strip(" .,:;!?()[]{}\"“”")
            if value and value not in NAME_STOPWORDS:
                hits[value].append(relative)
    source_texts = {
        file.relative_to(book_root).as_posix(): read_text(file)
        for file in source_files(book_root, contract)
    }
    for row in manual_rows:
        form = str(row.get("source_form") or "").strip()
        if not form:
            continue
        declared_files = parse_aliases(str(row.get("files") or ""))
        matching_files = [name for name, text in source_texts.items() if form in text]
        if declared_files:
            unknown = sorted(set(declared_files) - set(source_texts))
            missing_form = sorted(name for name in declared_files if name in source_texts and form not in source_texts[name])
            if unknown or missing_form:
                raise SystemExit(
                    f"manual proper-noun candidate {form!r} has invalid file evidence: unknown={unknown} missing_form={missing_form}"
                )
            matching_files = declared_files
        if not matching_files:
            raise SystemExit(f"manual proper-noun candidate {form!r} does not occur in the source corpus")
        hits[form].extend(matching_files)
    rows: list[dict[str, str]] = []
    for form in sorted(hits, key=str.casefold):
        files = sorted(set(hits[form]))
        prior = old.get(form, {})
        rows.append({
            "source_form": form,
            "count": str(len(hits[form])),
            "files": ";".join(files),
            "decision": str(prior.get("decision") or ""),
            "entity_id": str(prior.get("entity_id") or ""),
            "notes": str(prior.get("notes") or ""),
        })
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["source_form", "count", "files", "decision", "entity_id", "notes"])
        writer.writeheader()
        writer.writerows(rows)
    records = source_file_records(book_root, contract)
    manifest_path = resolve_inside(book_root, contract_path(contract, "proper_nouns", "discovery_manifest"))
    manifest = {
        "schema_version": "1.0",
        "status": "DISCOVERED_NEEDS_DECISIONS",
        "discovery_engine": "lifebook-proper-noun-discovery",
        "discovery_engine_version": "2.0",
        "language_plugins": [
            f"{contract.get('source_language') or 'und'}:latin-titlecase-v1",
            f"{contract.get('source_language') or 'und'}:manual-candidate-supplement-v1",
            "manual-full-source-review-v1",
        ],
        "source_files": records,
        "source_corpus_sha256": corpus_digest(records),
        "candidate_count": len(rows),
        "manual_candidate_count": len(manual_rows),
        "manual_candidates_sha256": sha256_file(manual_path),
        "manual_review_complete": False,
        "no_candidate_reason": "",
        "decided_candidate_count": sum(row["decision"] in {"registered", "not_proper_noun"} for row in rows),
        "unresolved_candidate_count": sum(row["decision"] not in {"registered", "not_proper_noun"} for row in rows),
        "occurrence_count": 0,
        "unresolved_occurrence_count": 0,
        "candidate_decisions_sha256": sha256_file(path),
        "proper_nouns_sha256": "",
        "occurrence_ledger_sha256": "",
        "manual_review_record_sha256": "",
        "locked_at": "",
    }
    write_json(manifest_path, manifest)
    print(f"proper-noun candidates refreshed: {len(rows)} -> {path.relative_to(book_root).as_posix()}")


def build_proper_noun_ledger(book_root: Path, contract: dict) -> None:
    _register_path, names, columns = load_name_rows(book_root, contract)
    missing = REQUIRED_NAME_COLUMNS - columns
    if missing:
        raise SystemExit("proper_nouns.csv missing columns: " + ", ".join(sorted(missing)))
    _manifest_path, store_path = unit_paths(book_root, contract)
    if not store_path.is_file():
        raise SystemExit("Initialize source units before building the proper-noun occurrence ledger.")
    units = read_units(store_path)
    form_entities: dict[str, list[str]] = defaultdict(list)
    for row in names:
        if row.get("status") != "locked" or not row.get("entity_id"):
            continue
        for form in [row.get("source_name", ""), *parse_aliases(row.get("source_aliases", ""))]:
            if form:
                form_entities[form].append(row["entity_id"])
    ledger_path = resolve_inside(book_root, contract_path(contract, "proper_nouns", "occurrence_ledger"))
    existing_by_key: dict[tuple[str, int, int, str], dict[str, str]] = {}
    if ledger_path.is_file():
        _path, existing, _columns = load_occurrence_rows(book_root, contract)
        for row in existing:
            try:
                key = (row["unit_id"], int(row["start_offset"]), int(row["end_offset"]), row["source_form"])
            except (KeyError, ValueError):
                continue
            existing_by_key[key] = row
    rows: list[dict[str, str]] = []
    first_seen_entities: set[str] = set()
    for unit in units:
        source = str(unit.get("source_text") or "")
        for start, end, form in find_form_occurrences(source, form_entities):
            entity_ids = form_entities[form]
            key = (str(unit["unit_id"]), start, end, form)
            previous = existing_by_key.get(key, {})
            entity_id = previous.get("entity_id", "")
            if len(entity_ids) == 1:
                entity_id = entity_ids[0]
            elif entity_id not in entity_ids:
                entity_id = ""
            kind = str(unit.get("unit_type") or "body")
            body = kind not in {"heading", "navigation", "subtitle"}
            counts_first = bool(body and entity_id and entity_id not in first_seen_entities)
            if counts_first:
                first_seen_entities.add(entity_id)
            rows.append({
                "occurrence_id": previous.get("occurrence_id") or f"occ-{uuid.uuid4()}",
                "source_file": str(unit["source_file"]),
                "unit_id": str(unit["unit_id"]),
                "start_offset": str(start),
                "end_offset": str(end),
                "source_form": form,
                "entity_id": entity_id,
                "disambiguation_evidence": previous.get("disambiguation_evidence") or ("unique_locked_source_form" if entity_id and len(entity_ids) == 1 else ""),
                "is_body_occurrence": "true" if body else "false",
                "counts_as_first_body_occurrence": "true" if counts_first else "false",
                "status": "locked" if entity_id and (previous.get("disambiguation_evidence") or len(entity_ids) == 1) else "unresolved",
            })
    ledger_path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile("w", encoding="utf-8", newline="", delete=False, dir=ledger_path.parent, prefix=f".{ledger_path.name}.", suffix=".tmp") as handle:
        writer = csv.DictWriter(handle, fieldnames=sorted(REQUIRED_OCCURRENCE_COLUMNS, key=lambda key: [
            "occurrence_id", "source_file", "unit_id", "start_offset", "end_offset", "source_form", "entity_id",
            "disambiguation_evidence", "is_body_occurrence", "counts_as_first_body_occurrence", "status"
        ].index(key)))
        writer.writeheader()
        writer.writerows(rows)
        temporary = Path(handle.name)
    os.replace(temporary, ledger_path)
    print(f"proper-noun occurrence ledger refreshed: occurrences={len(rows)}")


def lock_proper_noun_discovery(book_root: Path, contract: dict, review_arg: str | None) -> None:
    proper = contract.get("proper_nouns") or {}
    review_path = resolve_inside(book_root, review_arg or contract_path(contract, "proper_nouns", "manual_review_record"))
    review = read_json(review_path)
    records = source_file_records(book_root, contract)
    candidate_path, candidates = load_candidate_rows(book_root, contract)
    manual_candidate_path, manual_candidates = load_manual_candidate_rows(book_root, contract)
    register_path, _names, _columns = load_name_rows(book_root, contract)
    occurrence_path, occurrences, _occurrence_columns = load_occurrence_rows(book_root, contract)
    unresolved_candidates = sum(str(row.get("decision") or "").strip() not in {"registered", "not_proper_noun"} for row in candidates)
    unresolved_occurrences = sum(row.get("status") != "locked" or not row.get("entity_id") for row in occurrences)
    expected_files = [row["path"] for row in records]
    checks = {
        "status": review.get("status") == "PASS",
        "reviewer": bool(str(review.get("reviewer") or "").strip()),
        "reviewed_at": bool(str(review.get("reviewed_at") or "").strip()),
        "source_corpus_sha256": review.get("source_corpus_sha256") == corpus_digest(records),
        "reviewed_files": review.get("reviewed_files") == expected_files,
        "candidate_table_sha256": review.get("candidate_table_sha256") == sha256_file(candidate_path),
        "manual_candidates_sha256": review.get("manual_candidates_sha256") == sha256_file(manual_candidate_path),
        "proper_nouns_sha256": review.get("proper_nouns_sha256") == sha256_file(register_path),
        "occurrence_ledger_sha256": review.get("occurrence_ledger_sha256") == sha256_file(occurrence_path),
        "unresolved_candidates": unresolved_candidates == 0 and review.get("unresolved_candidates") == 0,
        "unresolved_occurrences": unresolved_occurrences == 0 and review.get("unresolved_occurrences") == 0,
        "review_summary": bool(str(review.get("review_summary") or "").strip()),
    }
    failed = [key for key, passed in checks.items() if not passed]
    if failed:
        raise SystemExit("DISCOVERY_EVIDENCE_MISSING: manual review record failed: " + ", ".join(failed))
    manifest_path = resolve_inside(book_root, contract_path(contract, "proper_nouns", "discovery_manifest"))
    prior = read_json(manifest_path)
    manifest = {
        **prior,
        "status": "LOCKED",
        "source_files": records,
        "source_corpus_sha256": corpus_digest(records),
        "candidate_count": len(candidates),
        "manual_candidate_count": len(manual_candidates),
        "manual_candidates_sha256": sha256_file(manual_candidate_path),
        "manual_review_complete": True,
        "decided_candidate_count": len(candidates),
        "unresolved_candidate_count": 0,
        "occurrence_count": len(occurrences),
        "unresolved_occurrence_count": 0,
        "candidate_decisions_sha256": sha256_file(candidate_path),
        "proper_nouns_sha256": sha256_file(register_path),
        "occurrence_ledger_sha256": sha256_file(occurrence_path),
        "manual_review_record_sha256": sha256_file(review_path),
        "locked_at": utc_now(),
    }
    write_json(manifest_path, manifest)
    print(f"proper-noun discovery LOCKED: {sha256_file(manifest_path)}")


ID_COMMENT = re.compile(r"<!--\s*(?:id|paragraph-id|para-id)\s*:\s*([A-Za-z0-9_.:-]+)\s*-->\s*")
FENCE_START = re.compile(r"^\s{0,3}(`{3,}|~{3,})")
LIST_START = re.compile(r"^\s{0,3}(?:[-+*]\s+|\d+[.)]\s+)")
FOOTNOTE_START = re.compile(r"^\s{0,3}\[\^[^\]]+\]:")
HTML_BLOCK_START = re.compile(r"^\s{0,3}<(address|article|aside|blockquote|details|dialog|div|dl|fieldset|figure|footer|form|h[1-6]|header|hr|main|nav|ol|p|pre|section|table|ul)(?:\s|>|/)", re.I)
TABLE_DELIMITER = re.compile(r"^\s*\|?\s*:?-{3,}:?\s*(?:\|\s*:?-{3,}:?\s*)+\|?\s*$")


def markdown_ast_blocks(path: Path) -> list[dict[str, str]]:
    """Parse the block structure needed by the translation store without flattening protected Markdown blocks."""
    lines = read_text(path).split("\n")
    nodes: list[dict[str, str]] = []
    pending_id = ""
    index = 0

    def emit(kind: str, captured: list[str]) -> None:
        nonlocal pending_id
        raw = "\n".join(captured).strip("\n")
        if not raw.strip():
            return
        explicit_match = ID_COMMENT.fullmatch(raw.strip())
        if explicit_match:
            pending_id = raw.strip()
            return
        if pending_id:
            raw = f"{pending_id}\n{raw}"
            pending_id = ""
        nodes.append({"kind": kind, "raw": raw})

    while index < len(lines):
        line = lines[index]
        if not line.strip():
            index += 1
            continue
        if index == 0 and line.strip() == "---":
            end = index + 1
            while end < len(lines) and lines[end].strip() != "---":
                end += 1
            if end < len(lines):
                emit("frontmatter", lines[index:end + 1])
                index = end + 1
                continue
        fence = FENCE_START.match(line)
        if fence:
            marker = fence.group(1)
            captured = [line]
            index += 1
            closing = re.compile(rf"^\s{{0,3}}{re.escape(marker[0])}{{{len(marker)},}}\s*$")
            while index < len(lines):
                captured.append(lines[index])
                current = lines[index]
                index += 1
                if closing.match(current):
                    break
            emit("code", captured)
            continue
        if re.match(r"^\s{0,3}#{1,6}(?:\s+|$)", line):
            emit("heading", [line])
            index += 1
            continue
        if re.match(r"^\s{0,3}(?:-{3,}|\*{3,}|_{3,})\s*$", line):
            emit("thematic_break", [line])
            index += 1
            continue
        if index + 1 < len(lines) and line.strip() and re.match(r"^\s{0,3}(?:=+|-+)\s*$", lines[index + 1]):
            emit("heading", [line, lines[index + 1]])
            index += 2
            continue
        if index + 1 < len(lines) and "|" in line and TABLE_DELIMITER.match(lines[index + 1]):
            captured = [line, lines[index + 1]]
            index += 2
            while index < len(lines) and lines[index].strip() and "|" in lines[index]:
                captured.append(lines[index])
                index += 1
            emit("table", captured)
            continue
        html = HTML_BLOCK_START.match(line)
        if html:
            tag = html.group(1).lower()
            captured = [line]
            index += 1
            closing = re.compile(rf"</{re.escape(tag)}\s*>", re.I)
            while index < len(lines) and not closing.search("\n".join(captured)):
                if not lines[index].strip():
                    break
                captured.append(lines[index])
                index += 1
            emit("raw_html", captured)
            continue
        if line.lstrip().startswith("<!--"):
            captured = [line]
            index += 1
            while index < len(lines) and "-->" not in "\n".join(captured):
                captured.append(lines[index])
                index += 1
            emit("raw_html", captured)
            continue
        if line.lstrip().startswith(">"):
            captured = [line]
            index += 1
            while index < len(lines) and (lines[index].lstrip().startswith(">") or (not lines[index].strip() and index + 1 < len(lines) and lines[index + 1].lstrip().startswith(">"))):
                captured.append(lines[index])
                index += 1
            emit("quote", captured)
            continue
        if FOOTNOTE_START.match(line):
            captured = [line]
            index += 1
            while index < len(lines) and (lines[index].startswith(("    ", "\t")) or not lines[index].strip()):
                if not lines[index].strip() and (index + 1 >= len(lines) or not lines[index + 1].startswith(("    ", "\t"))):
                    break
                captured.append(lines[index])
                index += 1
            emit("note", captured)
            continue
        if LIST_START.match(line):
            captured = [line]
            index += 1
            while index < len(lines):
                current = lines[index]
                if not current.strip():
                    if index + 1 < len(lines) and (LIST_START.match(lines[index + 1]) or lines[index + 1].startswith(("  ", "\t"))):
                        captured.append(current)
                        index += 1
                        continue
                    break
                if LIST_START.match(current) or current.startswith(("  ", "\t")):
                    captured.append(current)
                    index += 1
                    continue
                break
            emit("list", captured)
            continue
        captured = [line]
        index += 1
        while index < len(lines) and lines[index].strip():
            candidate = lines[index]
            if (
                FENCE_START.match(candidate)
                or re.match(r"^\s{0,3}#{1,6}(?:\s+|$)", candidate)
                or LIST_START.match(candidate)
                or FOOTNOTE_START.match(candidate)
                or candidate.lstrip().startswith(">")
                or HTML_BLOCK_START.match(candidate)
            ):
                break
            captured.append(candidate)
            index += 1
        emit("body", captured)
    if pending_id:
        nodes.append({"kind": "raw_html", "raw": pending_id})
    return nodes


def strip_explicit_id(block: str) -> tuple[str, str]:
    found = ID_COMMENT.search(block)
    explicit = found.group(1) if found else ""
    return explicit, ID_COMMENT.sub("", block).strip()


def unit_type(block: str) -> tuple[str, int]:
    heading = re.match(r"^(#{1,6})\s+", block)
    if heading:
        return "heading", len(heading.group(1))
    if re.match(r"^\[\^?\d+[A-Za-z]?\]:|^\(?(?:note|注)\s*\d+", block, re.IGNORECASE):
        return "note", 0
    if block.lstrip().startswith(">") or block.lstrip().startswith("<blockquote"):
        return "quote", 0
    if re.match(r"^(?:[-*+]\s+|\d+\.\s+)", block):
        return "list", 0
    if FENCE_START.match(block):
        return "code", 0
    if TABLE_DELIMITER.search(block):
        return "table", 0
    if HTML_BLOCK_START.match(block):
        return "raw_html", 0
    return "body", 0


def visible_source(block: str, kind: str) -> str:
    if kind == "heading":
        if re.match(r"^#{1,6}\s+", block):
            return re.sub(r"^#{1,6}\s+", "", block).strip()
        return block.split("\n", 1)[0].strip()
    return block.strip()


def split_sentences(text: str, language: str) -> list[str]:
    normalized = re.sub(r"\s+", " ", text).strip()
    if not normalized:
        return []
    if language.lower().startswith(("zh", "ja")):
        parts = re.split(r"(?<=[。！？])\s*", normalized)
    else:
        parts = re.split(r"(?<=[.!?])\s+(?=[\"'“‘(\[]?[A-ZÀ-ÖØ-Þ])", normalized)
    return [part.strip() for part in parts if part.strip()]


def source_word_count(text: str, language: str) -> int:
    if language.lower().startswith(("zh", "ja")):
        return len(re.sub(r"\s+", "", text))
    return len(re.findall(r"\b[\wÀ-ÖØ-öø-ÿ'’.-]+\b", text, re.UNICODE))


def group_sentences(sentences: list[str], language: str, preferred_min: int, preferred_max: int) -> list[list[str]]:
    if not sentences:
        return []
    groups: list[list[str]] = []
    current: list[str] = []
    current_count = 0
    for sentence in sentences:
        count = source_word_count(sentence, language)
        if current and current_count >= preferred_min and current_count + count > preferred_max:
            groups.append(current)
            current = []
            current_count = 0
        current.append(sentence)
        current_count += count
    if current:
        if groups and current_count < preferred_min:
            groups[-1].extend(current)
        else:
            groups.append(current)
    return groups


def apply_persistent_unit_ids(units: list[dict], existing_units: list[dict]) -> None:
    old_grouped: dict[str, list[dict]] = defaultdict(list)
    new_grouped: dict[str, list[dict]] = defaultdict(list)
    for unit in existing_units:
        old_grouped[str(unit.get("source_file") or "")].append(unit)
    for unit in units:
        new_grouped[str(unit.get("source_file") or "")].append(unit)
    for source_file, new_rows in new_grouped.items():
        old_rows = old_grouped.get(source_file, [])
        old_fingerprints = [(row.get("unit_type"), row.get("source_sha256"), row.get("source_text")) for row in old_rows]
        new_fingerprints = [(row.get("unit_type"), row.get("source_sha256"), row.get("source_text")) for row in new_rows]
        matcher = difflib.SequenceMatcher(a=old_fingerprints, b=new_fingerprints, autojunk=False)
        for block in matcher.get_matching_blocks():
            for offset in range(block.size):
                old = old_rows[block.a + offset]
                new = new_rows[block.b + offset]
                new["unit_id"] = old["unit_id"]
                new["source_parent_id"] = old["source_parent_id"]
                for sentence_index, sentence in enumerate(new["source_sentences"], start=1):
                    sentence["sentence_id"] = f"{new['unit_id']}::s{sentence_index:02d}"


def build_expected_units(book_root: Path, contract: dict, existing_units: list[dict] | None = None) -> list[dict]:
    bilingual = contract.get("bilingual") or {}
    preferred_min = int(bilingual.get("preferred_source_words_min") or 60)
    preferred_max = int(bilingual.get("preferred_source_words_max") or 160)
    language = str(contract.get("source_language") or "")
    units: list[dict] = []
    order = 0
    for file in source_files(book_root, contract):
        source_file = file.relative_to(book_root).as_posix()
        chapter_id = file.stem
        parent_index = 0
        for ast_node in markdown_ast_blocks(file):
            raw_block = ast_node["raw"]
            explicit, block = strip_explicit_id(raw_block)
            ast_kind = ast_node["kind"]
            if not block or ast_kind in {"frontmatter", "thematic_break"}:
                continue
            parent_index += 1
            fallback_kind, heading_level = unit_type(block)
            kind = ast_kind if ast_kind != "body" else fallback_kind
            text = visible_source(block, kind)
            parent_id = explicit or f"parent-{uuid.uuid4()}"
            if kind in {"heading", "note", "quote", "list", "code", "table", "raw_html"}:
                groups = [[text]]
            else:
                groups = group_sentences(split_sentences(text, language), language, preferred_min, preferred_max) or [[text]]
            for sub_index, sentences in enumerate(groups, start=1):
                source_text = " ".join(sentences).strip()
                unit_id = f"unit-{uuid.uuid4()}"
                order += 1
                sentence_records = []
                for sentence_index, sentence in enumerate(sentences, start=1):
                    sentence_records.append({
                        "sentence_id": f"{unit_id}::s{sentence_index:02d}",
                        "text": sentence,
                        "sha256": sha256_text(sentence),
                    })
                units.append({
                    "schema_version": "2.0",
                    "unit_id": unit_id,
                    "chapter_id": chapter_id,
                    "source_file": source_file,
                    "source_parent_id": parent_id,
                    "source_parent_index": parent_index,
                    "source_parent_locator": f"{source_file}::natural-block:{parent_index}",
                    "source_unit_index": sub_index,
                    "global_order": order,
                    "unit_type": kind,
                    "source_ast_kind": ast_kind,
                    "markdown_heading_level": heading_level,
                    "split_reason": "source_natural_paragraph" if len(groups) == 1 else "complete_sentence_group_length",
                    "source_text": source_text,
                    "source_sha256": sha256_text(source_text),
                    "source_sentences": sentence_records,
                    "target_text": "",
                    "target_sha256": "",
                    "target_template": "",
                    "target_template_sha256": "",
                    "target_state": "initial",
                    "translator_run_id": "",
                    "contract_sha256": "",
                    "proper_noun_revision": "",
                    "occurrence_ledger_revision": "",
                    "terminology_revision": "",
                })
    if existing_units:
        apply_persistent_unit_ids(units, existing_units)
    return units


def unit_paths(book_root: Path, contract: dict) -> tuple[Path, Path]:
    manifest_path = resolve_inside(book_root, contract_path(contract, "canonical_units", "manifest"))
    if manifest_path.is_file():
        manifest = read_json(manifest_path)
        stored = str(manifest.get("unit_store") or "")
        if stored:
            return manifest_path, resolve_inside(book_root, stored)
    return manifest_path, resolve_inside(book_root, contract_path(contract, "canonical_units", "store"))


def read_units(path: Path) -> list[dict]:
    units: list[dict] = []
    for line_number, line in enumerate(read_text(path).split("\n"), start=1):
        if not line.strip():
            continue
        value = json.loads(line)
        if not isinstance(value, dict):
            raise ValueError(f"{path}:{line_number}: unit must be an object")
        units.append(value)
    return units


def write_units(path: Path, units: list[dict]) -> None:
    write_text(path, "".join(json.dumps(unit, ensure_ascii=False, sort_keys=True) + "\n" for unit in units))


def source_hash_manifest(book_root: Path, contract: dict) -> dict[str, str]:
    return {path.relative_to(book_root).as_posix(): sha256_file(path) for path in source_files(book_root, contract)}


def write_unit_manifest(book_root: Path, contract: dict, units: list[dict], store_path: Path | None = None) -> dict:
    manifest_path, current_store = unit_paths(book_root, contract)
    store_path = store_path or current_store
    targets = [
        {
            "unit_id": unit["unit_id"],
            "source_sha256": unit.get("source_sha256", ""),
            "target_sha256": unit.get("target_sha256", ""),
            "global_order": unit.get("global_order"),
            "unit_type": unit.get("unit_type"),
        }
        for unit in units
    ]
    manifest = {
        "schema_version": "1.0",
        "generated_at": utc_now(),
        "contract_sha256": contract.get("contract_sha256", ""),
        "proper_noun_revision": (contract.get("proper_nouns") or {}).get("register_sha256", ""),
        "occurrence_ledger_revision": (contract.get("proper_nouns") or {}).get("occurrence_ledger_sha256", ""),
        "terminology_revision": (contract.get("terminology") or {}).get("register_sha256", ""),
        "source_file_sha256": source_hash_manifest(book_root, contract),
        "unit_store": store_path.relative_to(book_root).as_posix(),
        "unit_store_sha256": sha256_file(store_path),
        "unit_count": len(units),
        "target_unit_manifest_sha256": canonical_json_digest(targets),
        "target_units": targets,
    }
    write_json(manifest_path, manifest)
    output_manifest = book_root / "output" / "translation_unit_manifest.json"
    write_json(output_manifest, manifest)
    return manifest


def commit_generation(book_root: Path, contract: dict, units: list[dict], reason: str) -> dict:
    generation_root = resolve_inside(book_root, contract_path(contract, "canonical_units", "generation_root"))
    generation_id = f"{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}-{uuid.uuid4().hex[:12]}"
    store_path = generation_root / generation_id / "units.jsonl"
    write_units(store_path, units)
    manifest = write_unit_manifest(book_root, contract, units, store_path)
    manifest["generation_id"] = generation_id
    manifest["generation_reason"] = reason
    manifest["manifest_sha256"] = canonical_json_digest({key: value for key, value in manifest.items() if key != "manifest_sha256"})
    manifest_path = resolve_inside(book_root, contract_path(contract, "canonical_units", "manifest"))
    write_json(manifest_path, manifest)
    write_json(book_root / "output" / "translation_unit_manifest.json", manifest)
    return manifest


def init_units(book_root: Path, contract: dict, discard: bool) -> None:
    if not str(contract.get("source_language") or "").strip():
        raise SystemExit("Configure source_language before initializing source units.")
    manifest_path, store_path = unit_paths(book_root, contract)
    old_units: list[dict] = []
    if store_path.is_file() and not discard:
        old_units = read_units(store_path)
    units = build_expected_units(book_root, contract, old_units)
    old_by_id = {str(unit.get("unit_id") or ""): unit for unit in old_units}
    preserved = 0
    for unit in units:
        old = old_by_id.get(str(unit["unit_id"]))
        if old and old.get("source_text") == unit["source_text"] and old.get("target_text"):
            unit["target_text"] = old["target_text"]
            unit["target_sha256"] = sha256_text(str(old["target_text"]))
            unit["target_template"] = old.get("target_template", old["target_text"])
            unit["target_template_sha256"] = sha256_text(str(unit["target_template"]))
            unit["target_state"] = old.get("target_state") if old.get("target_state") in ALLOWED_STATES else "translated"
            unit["translator_run_id"] = old.get("translator_run_id", "")
            unit["contract_sha256"] = old.get("contract_sha256", "")
            unit["proper_noun_revision"] = old.get("proper_noun_revision", "")
            unit["occurrence_ledger_revision"] = old.get("occurrence_ledger_revision", "")
            unit["terminology_revision"] = old.get("terminology_revision", "")
            current = (
                contract.get("contract_sha256", ""),
                (contract.get("proper_nouns") or {}).get("register_sha256", ""),
                (contract.get("proper_nouns") or {}).get("occurrence_ledger_sha256", ""),
                (contract.get("terminology") or {}).get("register_sha256", ""),
            )
            prior = (
                unit["contract_sha256"], unit["proper_noun_revision"],
                unit["occurrence_ledger_revision"], unit["terminology_revision"],
            )
            if all(current) and prior != current:
                unit["stale_from_state"] = unit["target_state"]
                if prior[3] == current[3] and "{{pn:" in str(unit.get("target_template") or ""):
                    unit["target_state"] = "needs_rerender"
                else:
                    unit["target_state"] = "needs_retranslation"
            preserved += 1
        elif contract.get("status") == "LOCKED":
            unit["contract_sha256"] = contract.get("contract_sha256", "")
            unit["proper_noun_revision"] = (contract.get("proper_nouns") or {}).get("register_sha256", "")
            unit["occurrence_ledger_revision"] = (contract.get("proper_nouns") or {}).get("occurrence_ledger_sha256", "")
            unit["terminology_revision"] = (contract.get("terminology") or {}).get("register_sha256", "")
    manifest = commit_generation(book_root, contract, units, "init_units")
    print(f"canonical units initialized: units={len(units)} preserved_targets={preserved} manifest={manifest_path.relative_to(book_root)}")


def refresh_derived(book_root: Path, contract: dict, promote_initial: bool) -> None:
    _manifest_path, store_path = unit_paths(book_root, contract)
    units = read_units(store_path)
    for unit in units:
        target = str(unit.get("target_text") or "")
        unit["target_sha256"] = sha256_text(target) if target else ""
        template = str(unit.get("target_template") or "")
        unit["target_template_sha256"] = sha256_text(template) if template else ""
        if target and promote_initial and unit.get("target_state") == "initial":
            unit["target_state"] = "translated"
        current = (
            contract.get("contract_sha256", ""),
            (contract.get("proper_nouns") or {}).get("register_sha256", ""),
            (contract.get("proper_nouns") or {}).get("occurrence_ledger_sha256", ""),
            (contract.get("terminology") or {}).get("register_sha256", ""),
        )
        prior = (
            unit.get("contract_sha256", ""), unit.get("proper_noun_revision", ""),
            unit.get("occurrence_ledger_revision", ""), unit.get("terminology_revision", ""),
        )
        if target and prior != current:
            unit["stale_from_state"] = unit.get("target_state", "translated")
            if prior[3] == current[3] and "{{pn:" in template:
                unit["target_state"] = "needs_rerender"
            else:
                unit["target_state"] = "needs_retranslation"
    commit_generation(book_root, contract, units, "refresh_derived")
    print(f"refreshed derived hashes for {len(units)} units")


def name_forms(row: dict[str, str]) -> tuple[list[str], list[str]]:
    source = [row["source_name"], *parse_aliases(row["source_aliases"])]
    target = [row["target_name"], row["chinese_gloss"], *parse_aliases(row["target_aliases"])]
    return ([item for item in source if item], list(dict.fromkeys(item for item in target if item)))


ENTITY_TOKEN_RE = re.compile(r"\{\{pn:([A-Za-z0-9_.:-]+)\}\}")


def render_target_templates(book_root: Path, contract: dict, units: list[dict]) -> tuple[dict[str, str], list[str]]:
    issues: list[str] = []
    _name_path, names, _columns = load_name_rows(book_root, contract)
    _occurrence_path, occurrences, _occurrence_columns = load_occurrence_rows(book_root, contract)
    by_entity = {row["entity_id"]: row for row in names}
    occurrence_by_unit: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in occurrences:
        occurrence_by_unit[row["unit_id"]].append(row)
    for rows in occurrence_by_unit.values():
        rows.sort(key=lambda row: (int(row["start_offset"]), int(row["end_offset"])))
    locked_literals: set[str] = set()
    for row in names:
        source_forms, target_forms = name_forms(row)
        locked_literals.update(source_forms)
        locked_literals.update(target_forms)
        locked_literals.update(item for item in (row.get("first_rendering", ""), row.get("subsequent_rendering", "")) if item)
    rendered: dict[str, str] = {}
    for unit in units:
        unit_id = str(unit["unit_id"])
        template = str(unit.get("target_template") or "")
        if not template and not unit.get("target_text") and unit.get("target_state") == "initial":
            rendered[unit_id] = ""
            continue
        if not template and unit.get("target_text"):
            issues.append(f"CSV_ONLY_RENDER_REQUIRED: {unit_id} has target_text without target_template")
            continue
        markers = ENTITY_TOKEN_RE.findall(template)
        expected_occurrences = occurrence_by_unit.get(unit_id, [])
        expected_entities = [row["entity_id"] for row in expected_occurrences]
        if sorted(markers) != sorted(expected_entities):
            issues.append(f"ENTITY_OCCURRENCE_COVERAGE_FAILED: {unit_id} target markers do not match the locked occurrence ledger")
            continue
        without_markers = ENTITY_TOKEN_RE.sub("", template)
        for literal in sorted(locked_literals, key=len, reverse=True):
            if literal and literal in without_markers:
                issues.append(f"CSV_ONLY_RENDER_REQUIRED: {unit_id} contains direct locked name form {literal!r}")
                break
        render_queue: dict[str, list[str]] = defaultdict(list)
        for occurrence in expected_occurrences:
            entity = by_entity.get(occurrence["entity_id"])
            if entity is None:
                issues.append(f"ENTITY_DISAMBIGUATION_FAILED: {unit_id} references unknown entity {occurrence['entity_id']!r}")
                continue
            use_first = occurrence.get("counts_as_first_body_occurrence") == "true"
            value = entity.get("first_rendering") if use_first else entity.get("subsequent_rendering")
            if not value:
                issues.append(f"CSV_ONLY_RENDER_REQUIRED: missing locked rendering for {entity['entity_id']!r}")
                continue
            render_queue[entity["entity_id"]].append(str(value))

        def replace(match: re.Match[str]) -> str:
            entity_id = match.group(1)
            if entity_id not in by_entity or not render_queue[entity_id]:
                issues.append(f"CSV_ONLY_RENDER_REQUIRED: invalid or excess entity marker {entity_id!r} in {unit_id}")
                return match.group(0)
            return render_queue[entity_id].pop(0)

        rendered[unit_id] = ENTITY_TOKEN_RE.sub(replace, template)
    return rendered, issues


def apply_target_rendering(book_root: Path, contract: dict, units: list[dict], allow_retranslation: bool = False) -> None:
    rendered, issues = render_target_templates(book_root, contract, units)
    if issues:
        raise ValueError("\n".join(issues))
    for unit in units:
        unit_id = str(unit["unit_id"])
        if unit.get("target_state") == "needs_retranslation" and not allow_retranslation:
            raise ValueError(f"{unit_id}: needs retranslation; CSV rendering alone cannot repair it")
        template = str(unit.get("target_template") or "")
        unit["target_template_sha256"] = sha256_text(template) if template else ""
        target = rendered.get(unit_id, "")
        unit["target_text"] = target
        unit["target_sha256"] = sha256_text(target) if target else ""
        if unit.get("target_state") == "needs_rerender":
            unit["target_state"] = unit.pop("stale_from_state", "translated")
        if target:
            unit["contract_sha256"] = contract.get("contract_sha256", "")
            unit["proper_noun_revision"] = (contract.get("proper_nouns") or {}).get("register_sha256", "")
            unit["occurrence_ledger_revision"] = (contract.get("proper_nouns") or {}).get("occurrence_ledger_sha256", "")


def render_proper_nouns(book_root: Path, contract: dict) -> None:
    issues = validate_contract(book_root, contract)
    if issues:
        raise SystemExit("Cannot render names:\n- " + "\n- ".join(issues))
    _manifest_path, store_path = unit_paths(book_root, contract)
    units = read_units(store_path)
    apply_target_rendering(book_root, contract, units)
    commit_generation(book_root, contract, units, "render_proper_nouns")
    print(f"proper-noun entity rendering complete: units={len(units)}")


def validate_name_rendering(units: list[dict], rows: list[dict[str, str]], mode: str) -> list[str]:
    issues: list[str] = []
    complete_text = "\n".join(str(unit.get("target_text") or "") for unit in units)
    for row in rows:
        source_forms, target_forms = name_forms(row)
        for source in source_forms:
            nested_patterns = [f"{source}（{source}（"] + [f"{target}（{source}（" for target in target_forms]
            if any(pattern in complete_text for pattern in nested_patterns):
                issues.append(f"nested proper-name rendering detected for {row['source_name']!r}")
        if mode == "all_chinese":
            allowed = str(row.get("repeat_original_allowed_when") or "").strip()
            if not allowed:
                for source in source_forms:
                    if source and source in complete_text:
                        issues.append(f"all_chinese forbids source form in body: {source!r}")
        elif mode == "all_source":
            for target in target_forms:
                if target and target in complete_text:
                    issues.append(f"all_source forbids translated proper-name form in body: {target!r}")
        elif mode == "hybrid":
            strategy = row.get("display_strategy")
            if strategy == "established_chinese_only":
                for source in source_forms:
                    if source and source in complete_text and not row.get("repeat_original_allowed_when"):
                        issues.append(f"established_chinese_only forbids source form in body: {source!r}")
            elif strategy == "target_source_then_target":
                first_rendering = row.get("first_rendering") or ""
                occurrences = [(index, str(unit.get("target_text") or "")) for index, unit in enumerate(units) if any(form in str(unit.get("target_text") or "") for form in source_forms + target_forms)]
                if occurrences:
                    if first_rendering not in occurrences[0][1]:
                        issues.append(f"policy 3 first occurrence does not use locked first_rendering for {row['source_name']!r}")
                    for _index, text in occurrences[1:]:
                        if first_rendering and first_rendering in text:
                            issues.append(f"policy 3 first_rendering repeats after first occurrence for {row['source_name']!r}")
                            break
            elif strategy == "source_first_chinese_gloss_then_source":
                occurrences = [(index, str(unit.get("target_text") or "")) for index, unit in enumerate(units) if row["source_name"] in str(unit.get("target_text") or "")]
                if occurrences:
                    first_rendering = row.get("first_rendering") or ""
                    if first_rendering not in occurrences[0][1]:
                        issues.append(f"first source-first occurrence does not use locked first_rendering for {row['source_name']!r}")
                    for _index, text in occurrences[1:]:
                        if first_rendering and first_rendering in text:
                            issues.append(f"source-first first_rendering repeats after first occurrence for {row['source_name']!r}")
                            break
    return issues


def validate_units(book_root: Path, contract: dict, allow_incomplete: bool, require_semantic: bool) -> tuple[list[str], dict]:
    issues = validate_contract(book_root, contract)
    manifest_path, store_path = unit_paths(book_root, contract)
    if not store_path.is_file():
        issues.append(f"missing canonical unit store: {store_path.relative_to(book_root).as_posix()}")
        return issues, {"unit_count": 0}
    try:
        units = read_units(store_path)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        issues.append(str(exc))
        return issues, {"unit_count": 0}
    expected = build_expected_units(book_root, contract, units)
    if len(units) != len(expected):
        issues.append(f"source coverage mismatch: canonical={len(units)} expected={len(expected)}")
        if len(units) > len(expected):
            issues.append("SENTENCE_OVERSEGMENTED: canonical store has more visible units than the locked natural-paragraph segmentation")
    ids = [str(unit.get("unit_id") or "") for unit in units]
    if len(ids) != len(set(ids)):
        issues.append("canonical unit IDs must be unique")
    rendered_targets, render_issues = render_target_templates(book_root, contract, units)
    issues.extend(render_issues)
    for index, (unit, wanted) in enumerate(zip(units, expected), start=1):
        for key in (
            "unit_id", "source_file", "source_parent_id", "source_text", "source_sha256",
            "global_order", "unit_type", "source_ast_kind", "source_sentences",
        ):
            if unit.get(key) != wanted.get(key):
                issues.append(f"unit[{index}] {key} differs from frozen source segmentation")
        target = str(unit.get("target_text") or "")
        if not allow_incomplete and not target.strip():
            issues.append(f"{unit.get('unit_id')}: target_text is empty")
        expected_target_hash = sha256_text(target) if target else ""
        if unit.get("target_sha256") != expected_target_hash:
            issues.append(f"{unit.get('unit_id')}: target_sha256 is stale")
        template = str(unit.get("target_template") or "")
        expected_template_hash = sha256_text(template) if template else ""
        if unit.get("target_template_sha256") != expected_template_hash:
            issues.append(f"{unit.get('unit_id')}: target_template_sha256 is stale")
        if str(unit.get("target_text") or "") != rendered_targets.get(str(unit.get("unit_id")), ""):
            issues.append(f"{unit.get('unit_id')}: target_text is not the CSV-only rendering of target_template")
        if unit.get("target_state") not in ALLOWED_STATES:
            issues.append(f"{unit.get('unit_id')}: unsupported target_state")
        if not allow_incomplete and target and unit.get("target_state") in {"initial", "needs_rerender", "needs_retranslation"}:
            issues.append(f"{unit.get('unit_id')}: target state is not eligible for projection: {unit.get('target_state')}")
        if unit.get("contract_sha256") != contract.get("contract_sha256"):
            issues.append(f"STALE_TARGET_REVISION: {unit.get('unit_id')} contract revision is stale")
        if unit.get("proper_noun_revision") != (contract.get("proper_nouns") or {}).get("register_sha256"):
            issues.append(f"STALE_TARGET_REVISION: {unit.get('unit_id')} proper-noun revision is stale")
        if unit.get("occurrence_ledger_revision") != (contract.get("proper_nouns") or {}).get("occurrence_ledger_sha256"):
            issues.append(f"STALE_TARGET_REVISION: {unit.get('unit_id')} occurrence-ledger revision is stale")
        if unit.get("terminology_revision") != (contract.get("terminology") or {}).get("register_sha256"):
            issues.append(f"STALE_TARGET_REVISION: {unit.get('unit_id')} terminology revision is stale")
    if manifest_path.is_file():
        manifest = read_json(manifest_path)
        if manifest.get("unit_store_sha256") != sha256_file(store_path):
            issues.append("translation unit manifest is stale")
    else:
        issues.append(f"missing canonical unit manifest: {manifest_path.relative_to(book_root).as_posix()}")
    try:
        _name_path, name_rows, _columns = load_name_rows(book_root, contract)
        issues.extend(validate_name_rendering(units, name_rows, str((contract.get("proper_nouns") or {}).get("mode") or "")))
    except (OSError, ValueError, csv.Error) as exc:
        issues.append(str(exc))
    semantic_status = "NOT_REQUESTED"
    if require_semantic:
        audit_issues, _audit_report = validate_audits(book_root, contract, units, require_seal=True)
        issues.extend(audit_issues)
        semantic_status = "PASS" if not audit_issues else "FAIL"
    report = {
        "structural_status": "PASS" if not issues else "FAIL",
        "semantic_audit_status": semantic_status,
        "unit_count": len(units),
        "expected_source_unit_count": len(expected),
        "complete_target_count": sum(bool(str(unit.get("target_text") or "").strip()) for unit in units),
        "issues": issues,
    }
    return issues, report


def safe_marker_id(unit_id: str) -> str:
    return sha256_text(unit_id)[:20]


def current_manifest_digest(book_root: Path, contract: dict) -> str:
    manifest_path = resolve_inside(book_root, contract_path(contract, "canonical_units", "manifest"))
    if not manifest_path.is_file():
        raise ValueError("Canonical manifest does not exist.")
    return sha256_file(manifest_path)


def read_update_rows(path: Path) -> list[dict]:
    text = read_text(path).strip()
    if not text:
        return []
    if text.startswith("["):
        value = json.loads(text)
        if not isinstance(value, list) or not all(isinstance(item, dict) for item in value):
            raise ValueError("Chapter update input must be a JSON array of objects or JSONL objects.")
        return value
    rows = [json.loads(line) for line in text.split("\n") if line.strip()]
    if not all(isinstance(item, dict) for item in rows):
        raise ValueError("Chapter update JSONL rows must be objects.")
    return rows


def create_chapter_patch(book_root: Path, contract: dict, args: argparse.Namespace) -> None:
    issues = validate_contract(book_root, contract)
    if issues:
        raise SystemExit("Cannot create chapter patch:\n- " + "\n- ".join(issues))
    _manifest_path, store_path = unit_paths(book_root, contract)
    units = read_units(store_path)
    chapter_units = {str(unit["unit_id"]): unit for unit in units if str(unit.get("chapter_id")) == args.chapter}
    if not chapter_units:
        raise SystemExit(f"Unknown or empty chapter: {args.chapter}")
    updates_path = resolve_inside(book_root, args.updates)
    updates = read_update_rows(updates_path)
    seen: set[str] = set()
    normalized: list[dict] = []
    for row in updates:
        unit_id = str(row.get("unit_id") or "")
        if unit_id not in chapter_units or unit_id in seen:
            raise SystemExit(f"Chapter patch contains unknown or duplicate unit: {unit_id}")
        seen.add(unit_id)
        target_template = str(row.get("target_template") or "")
        state = str(row.get("target_state") or "translated")
        if not target_template.strip() or state not in {"translated", "reviewed", "final"}:
            raise SystemExit(f"Chapter patch requires non-empty target_template and eligible state: {unit_id}")
        normalized.append({
            "unit_id": unit_id,
            "old_target_sha256": str(chapter_units[unit_id].get("target_sha256") or ""),
            "old_target_template_sha256": str(chapter_units[unit_id].get("target_template_sha256") or ""),
            "new_target_template": target_template,
            "new_target_template_sha256": sha256_text(target_template),
            "new_target_state": state,
        })
    output = resolve_inside(book_root, args.output)
    patch = {
        "schema_version": "1.0",
        "created_at": utc_now(),
        "base_manifest_sha256": current_manifest_digest(book_root, contract),
        "base_chapter_digest": chapter_digest(list(chapter_units.values())),
        "contract_sha256": contract.get("contract_sha256"),
        "chapter_id": args.chapter,
        "owner_run_id": args.owner_run_id,
        "updates": normalized,
    }
    write_json(output, patch)
    print(f"chapter patch created: chapter={args.chapter} updates={len(normalized)}")


def acquire_merge_lock(book_root: Path, contract: dict) -> tuple[int, Path]:
    patch_root = resolve_inside(book_root, contract_path(contract, "canonical_units", "patch_root"))
    patch_root.mkdir(parents=True, exist_ok=True)
    lock_path = patch_root / ".merge.lock"
    try:
        descriptor = os.open(lock_path, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
    except FileExistsError as exc:
        raise ValueError(f"PATCH_CONFLICT: merge lock already exists: {lock_path.relative_to(book_root).as_posix()}") from exc
    os.write(descriptor, f"pid={os.getpid()} created_at={utc_now()}\n".encode("utf-8"))
    return descriptor, lock_path


def merge_chapter_patch(book_root: Path, contract: dict, input_arg: str) -> None:
    descriptor, lock_path = acquire_merge_lock(book_root, contract)
    try:
        patch_path = resolve_inside(book_root, input_arg)
        patch = read_json(patch_path)
        if patch.get("schema_version") != "1.0" or not str(patch.get("owner_run_id") or "").strip():
            raise ValueError("PATCH_CONFLICT: invalid patch schema or missing owner_run_id")
        if not str(patch.get("base_manifest_sha256") or "").strip():
            raise ValueError("PATCH_CONFLICT: patch lacks base manifest traceability")
        if patch.get("contract_sha256") != contract.get("contract_sha256"):
            raise ValueError("PATCH_CONFLICT: patch contract is stale")
        _manifest_path, store_path = unit_paths(book_root, contract)
        units = read_units(store_path)
        by_id = {str(unit["unit_id"]): unit for unit in units}
        chapter = str(patch.get("chapter_id") or "")
        current_chapter_units = [unit for unit in units if str(unit.get("chapter_id")) == chapter]
        if not current_chapter_units or patch.get("base_chapter_digest") != chapter_digest(current_chapter_units):
            raise ValueError("PATCH_CONFLICT: patch chapter base is stale")
        seen: set[str] = set()
        updates = patch.get("updates")
        if not isinstance(updates, list):
            raise ValueError("PATCH_CONFLICT: updates must be a list")
        for update in updates:
            if not isinstance(update, dict):
                raise ValueError("PATCH_CONFLICT: update must be an object")
            unit_id = str(update.get("unit_id") or "")
            unit = by_id.get(unit_id)
            if not unit or str(unit.get("chapter_id")) != chapter or unit_id in seen:
                raise ValueError(f"PATCH_CONFLICT: unknown, foreign, or duplicate unit {unit_id}")
            seen.add(unit_id)
            if str(unit.get("target_sha256") or "") != str(update.get("old_target_sha256") or ""):
                raise ValueError(f"PATCH_CONFLICT: target changed since patch base for {unit_id}")
            if str(unit.get("target_template_sha256") or "") != str(update.get("old_target_template_sha256") or ""):
                raise ValueError(f"PATCH_CONFLICT: target template changed since patch base for {unit_id}")
            target_template = str(update.get("new_target_template") or "")
            state = str(update.get("new_target_state") or "")
            if not target_template.strip() or sha256_text(target_template) != update.get("new_target_template_sha256") or state not in {"translated", "reviewed", "final"}:
                raise ValueError(f"PATCH_CONFLICT: invalid target template payload for {unit_id}")
            unit["target_template"] = target_template
            unit["target_template_sha256"] = sha256_text(target_template)
            unit["target_state"] = state
            unit["translator_run_id"] = str(patch.get("owner_run_id") or "")
            unit["contract_sha256"] = contract.get("contract_sha256", "")
            unit["proper_noun_revision"] = (contract.get("proper_nouns") or {}).get("register_sha256", "")
            unit["occurrence_ledger_revision"] = (contract.get("proper_nouns") or {}).get("occurrence_ledger_sha256", "")
            unit["terminology_revision"] = (contract.get("terminology") or {}).get("register_sha256", "")
        apply_target_rendering(book_root, contract, units, allow_retranslation=True)
        commit_generation(book_root, contract, units, f"merge_patch:{chapter}:{patch.get('owner_run_id')}")
        print(f"chapter patch merged: chapter={chapter} updates={len(updates)}")
    finally:
        os.close(descriptor)
        lock_path.unlink(missing_ok=True)


def projection_target_blocks(path: Path) -> list[str]:
    values: list[str] = []
    for node in markdown_ast_blocks(path):
        if node["kind"] in {"frontmatter", "thematic_break"}:
            continue
        raw = re.sub(r"<!--\s*lifebook-unit:[^>]+-->\s*", "", node["raw"]).strip()
        if not raw:
            continue
        kind, _level = unit_type(raw)
        values.append(visible_source(raw, kind))
    return values


def migrate_legacy(book_root: Path, contract: dict, report_arg: str, apply: bool, owner_run_id: str) -> None:
    contract_issues = validate_contract(book_root, contract)
    if contract_issues:
        raise ValueError("Legacy migration requires a locked valid contract: " + "; ".join(contract_issues[:10]))
    _manifest_path, store_path = unit_paths(book_root, contract)
    units = read_units(store_path)
    grouped = group_units_by_chapter(units)
    translated_root = resolve_inside(book_root, contract_path(contract, "canonical_units", "translated_projection"))
    final_root = resolve_inside(book_root, contract_path(contract, "canonical_units", "final_projection"))
    proposed = [dict(unit) for unit in units]
    proposed_by_id = {str(unit["unit_id"]): unit for unit in proposed}
    chapters: list[dict] = []
    issues: list[str] = []
    for chapter_id, chapter_units in grouped.items():
        source_name = Path(str(chapter_units[0]["source_file"])).name
        translated_path = translated_root / source_name
        final_path = final_root / source_name
        chapter_record = {
            "chapter_id": chapter_id,
            "source_unit_count": len(chapter_units),
            "translated_path": translated_path.relative_to(book_root).as_posix(),
            "final_path": final_path.relative_to(book_root).as_posix(),
            "translated_sha256": sha256_file(translated_path) if translated_path.is_file() else "",
            "final_sha256": sha256_file(final_path) if final_path.is_file() else "",
            "status": "READY",
            "issues": [],
        }
        if not translated_path.is_file() or not final_path.is_file():
            chapter_record["issues"].append("missing translated or final legacy projection")
        elif read_text(translated_path) != read_text(final_path):
            chapter_record["issues"].append("translated and final legacy projections differ")
        else:
            targets = projection_target_blocks(final_path)
            chapter_record["legacy_target_block_count"] = len(targets)
            if len(targets) != len(chapter_units):
                chapter_record["issues"].append(
                    f"legacy target block count {len(targets)} differs from canonical source unit count {len(chapter_units)}"
                )
            else:
                for unit, target_template in zip(chapter_units, targets):
                    candidate = proposed_by_id[str(unit["unit_id"])]
                    candidate["target_template"] = target_template
                    candidate["target_template_sha256"] = sha256_text(target_template)
                    candidate["target_state"] = "translated"
                    candidate["contract_sha256"] = contract.get("contract_sha256", "")
                    candidate["proper_noun_revision"] = (contract.get("proper_nouns") or {}).get("register_sha256", "")
                    candidate["occurrence_ledger_revision"] = (contract.get("proper_nouns") or {}).get("occurrence_ledger_sha256", "")
                    candidate["terminology_revision"] = (contract.get("terminology") or {}).get("register_sha256", "")
        if chapter_record["issues"]:
            chapter_record["status"] = "REVIEW_REQUIRED"
            issues.extend(f"{chapter_id}: {item}" for item in chapter_record["issues"])
        chapters.append(chapter_record)
    if not issues:
        _rendered, render_issues = render_target_templates(book_root, contract, proposed)
        issues.extend(render_issues)
    status = "READY" if not issues else "REVIEW_REQUIRED"
    report = {
        "schema_version": "1.0",
        "status": status,
        "mode": "APPLIED" if apply and status == "READY" else "READ_ONLY_AUDIT",
        "canonical_store_sha256_before": sha256_file(store_path),
        "contract_sha256": contract.get("contract_sha256"),
        "chapters": chapters,
        "issues": issues,
        "note": "No canonical data is changed unless --apply is explicit and every chapter has exact block coverage, identical translated/final projections, and CSV-only entity rendering.",
    }
    report_path = resolve_inside(book_root, report_arg)
    write_json(report_path, report)
    if not apply:
        print(f"legacy migration audit {status}: {report_path.relative_to(book_root).as_posix()}")
        return
    if status != "READY":
        raise ValueError("LEGACY_MIGRATION_BLOCKED: " + "; ".join(issues[:20]))
    if not owner_run_id.strip():
        raise ValueError("LEGACY_MIGRATION_BLOCKED: --owner-run-id is required with --apply")
    for unit in proposed:
        if str(unit.get("target_text") or unit.get("target_template") or "").strip():
            unit["translator_run_id"] = owner_run_id
    apply_target_rendering(book_root, contract, proposed, allow_retranslation=True)
    commit_generation(book_root, contract, proposed, f"legacy_migration:{owner_run_id}")
    report["mode"] = "APPLIED"
    report["applied_at"] = utc_now()
    write_json(report_path, report)
    print(f"legacy migration applied: units={len(proposed)} owner={owner_run_id}")


def rollback_generation(book_root: Path, contract: dict, generation_id: str, reason: str) -> None:
    if not re.fullmatch(r"[A-Za-z0-9_.:-]+", generation_id):
        raise ValueError("Invalid generation ID.")
    generation_root = resolve_inside(book_root, contract_path(contract, "canonical_units", "generation_root"))
    source_store = generation_root / generation_id / "units.jsonl"
    if not source_store.is_file():
        raise ValueError(f"Unknown immutable generation: {generation_id}")
    units = read_units(source_store)
    expected = build_expected_units(book_root, contract, units)
    source_identity = [(item["unit_id"], item["source_sha256"]) for item in units]
    expected_identity = [(item["unit_id"], item["source_sha256"]) for item in expected]
    if source_identity != expected_identity:
        raise ValueError("ROLLBACK_BLOCKED: generation source coverage differs from the current source corpus")
    current_revisions = (
        contract.get("contract_sha256", ""),
        (contract.get("proper_nouns") or {}).get("register_sha256", ""),
        (contract.get("proper_nouns") or {}).get("occurrence_ledger_sha256", ""),
        (contract.get("terminology") or {}).get("register_sha256", ""),
    )
    for unit in units:
        prior_revisions = (
            unit.get("contract_sha256", ""), unit.get("proper_noun_revision", ""),
            unit.get("occurrence_ledger_revision", ""), unit.get("terminology_revision", ""),
        )
        if unit.get("target_text") and prior_revisions != current_revisions:
            unit["stale_from_state"] = unit.get("target_state", "translated")
            unit["target_state"] = (
                "needs_rerender"
                if prior_revisions[0] == current_revisions[0]
                and prior_revisions[3] == current_revisions[3]
                and "{{pn:" in str(unit.get("target_template") or "")
                else "needs_retranslation"
            )
    manifest = commit_generation(book_root, contract, units, f"rollback:{generation_id}:{reason.strip()}")
    print(f"rollback restored as new generation: source={generation_id} current={manifest['generation_id']}")


def materialize(book_root: Path, contract: dict) -> None:
    issues, _report = validate_units(book_root, contract, allow_incomplete=False, require_semantic=False)
    if issues:
        raise SystemExit("Cannot materialize invalid units:\n- " + "\n- ".join(issues[:50]))
    _manifest_path, store_path = unit_paths(book_root, contract)
    units = read_units(store_path)
    grouped: dict[str, list[dict]] = defaultdict(list)
    for unit in units:
        grouped[str(unit["source_file"])].append(unit)
    translated_root = resolve_inside(book_root, contract_path(contract, "canonical_units", "translated_projection"))
    final_root = resolve_inside(book_root, contract_path(contract, "canonical_units", "final_projection"))
    expected_files: set[str] = set()
    rendered_files: dict[str, str] = {}
    for source_file, chapter_units in grouped.items():
        name = Path(source_file).name
        expected_files.add(name)
        blocks = []
        for unit in chapter_units:
            target = str(unit["target_text"]).strip()
            marker = (
                f"<!-- lifebook-unit:{unit['unit_id']} source-sha256:{unit['source_sha256']} "
                f"target-sha256:{unit['target_sha256']} -->"
            )
            if unit.get("unit_type") == "heading":
                level = max(1, min(6, int(unit.get("markdown_heading_level") or 1)))
                rendered = f"{'#' * level} {target}"
            else:
                rendered = target
            blocks.append(f"{marker}\n{rendered}")
        content = "\n\n".join(blocks).rstrip() + "\n"
        rendered_files[name] = content
    staged_roots: list[tuple[Path, Path]] = []
    backups: dict[Path, Path] = {}
    for root in (translated_root, final_root):
        root.parent.mkdir(parents=True, exist_ok=True)
        if root.exists() and not root.is_dir():
            raise SystemExit(f"Projection path is not a directory: {root.relative_to(book_root).as_posix()}")
        staged = Path(tempfile.mkdtemp(prefix=f".{root.name}.staged-", dir=root.parent))
        for name, content in rendered_files.items():
            write_text(staged / name, content)
        if {path.name for path in staged.glob("*.md") if path.is_file()} != expected_files:
            raise SystemExit(f"Projection staging coverage failed: {root.relative_to(book_root).as_posix()}")
        staged_roots.append((root, staged))
    replaced: list[Path] = []
    try:
        for root, staged in staged_roots:
            backup = root.with_name(f".{root.name}.backup-{uuid.uuid4().hex}")
            if root.exists():
                os.replace(root, backup)
                backups[root] = backup
            os.replace(staged, root)
            replaced.append(root)
    except OSError:
        for root in reversed(replaced):
            if root.exists():
                shutil.rmtree(root)
            backup = backups.get(root)
            if backup and backup.exists():
                os.replace(backup, root)
        for root, _staged in staged_roots:
            backup = backups.get(root)
            if root not in replaced and backup and backup.exists() and not root.exists():
                os.replace(backup, root)
        raise
    finally:
        for _root, staged in staged_roots:
            if staged.exists():
                shutil.rmtree(staged)
    projection_error = ""
    for root in (translated_root, final_root):
        if {path.name for path in root.glob("*.md") if path.is_file()} != expected_files:
            projection_error = f"Projection output coverage failed: {root.relative_to(book_root).as_posix()}"
            break
    if not projection_error:
        for name, content in rendered_files.items():
            translated = read_text(translated_root / name)
            final = read_text(final_root / name)
            if translated != content or final != content or translated != final:
                projection_error = f"Projection write verification failed: {name}"
                break
    if projection_error:
        for root in reversed(replaced):
            if root.exists():
                shutil.rmtree(root)
            backup = backups.get(root)
            if backup and backup.exists():
                os.replace(backup, root)
        raise SystemExit(projection_error)
    for backup in backups.values():
        if backup.exists():
            shutil.rmtree(backup)
    alignment_path = resolve_inside(book_root, contract_path(contract, "canonical_units", "alignment_projection"))
    alignment_units = []
    for unit in units:
        alignment_units.append({
            "id": unit["unit_id"],
            "chapter": unit["source_file"].replace("chapters/src/", "chapters/final/"),
            "source_file": unit["source_file"],
            "target_file": unit["source_file"].replace("chapters/src/", "chapters/final/"),
            "unit_type": unit.get("unit_type") or "body",
            "markdown_heading_level": int(unit.get("markdown_heading_level") or 0),
            "source_parent_id": unit["source_parent_id"],
            "source_text": unit["source_text"],
            "target_text": unit["target_text"],
            "source_sha256": unit["source_sha256"],
            "target_sha256": unit["target_sha256"],
        })
    manifest = write_unit_manifest(book_root, contract, units)
    alignment = {
        "schema_version": "canonical-units-1.0",
        "generated_at": utc_now(),
        "canonical_unit_store": store_path.relative_to(book_root).as_posix(),
        "canonical_unit_store_sha256": sha256_file(store_path),
        "contract_sha256": contract.get("contract_sha256"),
        "target_unit_manifest_sha256": manifest["target_unit_manifest_sha256"],
        "alignment_units": alignment_units,
        "metrics": {"alignment_units": len(alignment_units), "unmatched_source_notes": 0, "unmatched_target_notes": 0},
    }
    write_json(alignment_path, alignment)
    print(f"materialized {len(grouped)} chapters and {len(alignment_units)} source-target alignment units")


INLINE_TOKEN_RE = re.compile(
    r"(\[[^\]\n]+\]\([^\)\n]+\)|\*\*[^*\n]+\*\*|__[^_\n]+__|(?<!\*)\*[^*\n]+\*(?!\*)|"
    r"(?<!_)_[^_\n]+_(?!_)|`[^`\n]+`|\[\^[^\]\n]+\]|</?[^>\n]+>|\{[A-Za-z0-9_.:-]+\})"
)


def add_original_data(original_data: ET.Element, value: str, counter: list[int]) -> str:
    counter[0] += 1
    data_id = f"d{counter[0]}"
    node = ET.SubElement(original_data, f"{{{XLIFF_NS}}}data", {"id": data_id})
    node.text = value
    return data_id


def append_text(node: ET.Element, value: str) -> None:
    if not len(node):
        node.text = (node.text or "") + value
    else:
        node[-1].tail = (node[-1].tail or "") + value


def write_xliff_inline(node: ET.Element, original_data: ET.Element, value: str, counter: list[int]) -> None:
    cursor = 0
    for match in INLINE_TOKEN_RE.finditer(value):
        append_text(node, value[cursor:match.start()])
        token = match.group(0)
        inline_id = counter[0] + 1
        pair: tuple[str, str, str] | None = None
        if token.startswith("[") and "](" in token:
            split = token.index("](")
            pair = ("[", token[1:split], token[split:])
        elif token.startswith("**") and token.endswith("**"):
            pair = ("**", token[2:-2], "**")
        elif token.startswith("__") and token.endswith("__"):
            pair = ("__", token[2:-2], "__")
        elif token.startswith("*") and token.endswith("*"):
            pair = ("*", token[1:-1], "*")
        elif token.startswith("_") and token.endswith("_"):
            pair = ("_", token[1:-1], "_")
        if pair:
            start, inner, end = pair
            pc = ET.SubElement(node, f"{{{XLIFF_NS}}}pc", {
                "id": f"pc{inline_id}",
                "dataRefStart": add_original_data(original_data, start, counter),
                "dataRefEnd": add_original_data(original_data, end, counter),
            })
            pc.text = inner
        else:
            ET.SubElement(node, f"{{{XLIFF_NS}}}ph", {
                "id": f"ph{inline_id}",
                "dataRef": add_original_data(original_data, token, counter),
                "canDelete": "no",
            })
        cursor = match.end()
    append_text(node, value[cursor:])


def read_xliff_inline(node: ET.Element | None, data: dict[str, str]) -> str:
    if node is None:
        return ""
    parts = [node.text or ""]
    for child in list(node):
        local = child.tag.rsplit("}", 1)[-1]
        if local == "ph":
            parts.append(data.get(str(child.get("dataRef") or ""), ""))
        elif local == "pc":
            parts.append(data.get(str(child.get("dataRefStart") or ""), ""))
            parts.append(read_xliff_inline(child, data))
            parts.append(data.get(str(child.get("dataRefEnd") or ""), ""))
        else:
            raise ValueError(f"Unsupported XLIFF inline element: {local}")
        parts.append(child.tail or "")
    return "".join(parts)


def validate_xliff_schema(book_root: Path, contract: dict, document_path: Path) -> dict:
    xliff_config = contract.get("xliff") if isinstance(contract.get("xliff"), dict) else {}
    if xliff_config.get("schema_validation_required") is not True:
        raise ValueError("XLIFF schema_validation_required must remain true for import/export.")
    schema_path = resolve_inside(book_root, str(xliff_config.get("core_schema") or ""))
    expected_schema_hash = str(xliff_config.get("core_schema_sha256") or "")
    if not schema_path.is_file() or sha256_file(schema_path) != expected_schema_hash:
        raise ValueError("Official XLIFF core schema is missing or its pinned SHA-256 differs.")
    try:
        from lxml import etree  # type: ignore[import-not-found]
    except ImportError as exc:
        raise ValueError("XLIFF import/export requires Python lxml for official XSD validation.") from exc
    try:
        schema = etree.XMLSchema(etree.parse(str(schema_path)))
        document = etree.parse(str(document_path))
        schema.assertValid(document)
    except (etree.XMLSchemaParseError, etree.XMLSyntaxError, etree.DocumentInvalid) as exc:
        raise ValueError(f"XLIFF_SCHEMA_INVALID: {exc}") from exc
    report = {
        "status": "PASS",
        "schema_version": "OASIS-XLIFF-2.1-core-XSD",
        "schema_path": schema_path.relative_to(book_root).as_posix(),
        "schema_sha256": sha256_file(schema_path),
        "document_path": document_path.relative_to(book_root).as_posix(),
        "document_sha256": sha256_file(document_path),
        "validated_at": utc_now(),
    }
    write_json(book_root / "output" / "xliff_schema_validation.json", report)
    return report


def export_xliff(book_root: Path, contract: dict, output_arg: str | None) -> None:
    _manifest_path, store_path = unit_paths(book_root, contract)
    units = read_units(store_path)
    output = resolve_inside(book_root, output_arg or contract_path(contract, "xliff", "exchange_path"))
    root = ET.Element(f"{{{XLIFF_NS}}}xliff", {
        "version": "2.1",
        "srcLang": str(contract["source_language"]),
        "trgLang": str(contract["target_language"]),
    })
    grouped: dict[str, list[dict]] = defaultdict(list)
    for unit in units:
        grouped[str(unit["source_file"])].append(unit)
    for file_index, (source_file, file_units) in enumerate(grouped.items(), start=1):
        file_node = ET.SubElement(root, f"{{{XLIFF_NS}}}file", {"id": f"f{file_index:04d}", "original": source_file})
        for unit in file_units:
            unit_node = ET.SubElement(file_node, f"{{{XLIFF_NS}}}unit", {
                "id": str(unit["unit_id"]),
                "type": f"lifebook:{str(unit.get('unit_type') or 'body')}",
            })
            notes = ET.SubElement(unit_node, f"{{{XLIFF_NS}}}notes")
            for category, value in (
                ("source-sha256", unit["source_sha256"]),
                ("source-parent-id", unit["source_parent_id"]),
                ("contract-sha256", unit["contract_sha256"]),
                ("proper-noun-revision", unit["proper_noun_revision"]),
                ("terminology-revision", unit["terminology_revision"]),
                ("lifebook-target-state", unit.get("target_state") or "initial"),
            ):
                note = ET.SubElement(notes, f"{{{XLIFF_NS}}}note", {"category": category})
                note.text = str(value)
            original_data = ET.SubElement(unit_node, f"{{{XLIFF_NS}}}originalData")
            inline_counter = [0]
            target_state = str(unit.get("target_state") or "initial")
            segment_state = target_state if target_state in {"initial", "translated", "reviewed", "final"} else "initial"
            segment = ET.SubElement(unit_node, f"{{{XLIFF_NS}}}segment", {"id": "s1", "state": segment_state})
            source = ET.SubElement(segment, f"{{{XLIFF_NS}}}source")
            write_xliff_inline(source, original_data, str(unit["source_text"]), inline_counter)
            target = ET.SubElement(segment, f"{{{XLIFF_NS}}}target")
            write_xliff_inline(target, original_data, str(unit.get("target_template") or ""), inline_counter)
            if len(original_data) == 0:
                unit_node.remove(original_data)
    ET.indent(root, space="  ")
    output.parent.mkdir(parents=True, exist_ok=True)
    ET.ElementTree(root).write(output, encoding="utf-8", xml_declaration=True)
    validate_xliff_schema(book_root, contract, output)
    print(f"XLIFF 2.1 exported: {output.relative_to(book_root).as_posix()} units={len(units)}")


def import_xliff(book_root: Path, contract: dict, input_arg: str | None) -> None:
    input_path = resolve_inside(book_root, input_arg or contract_path(contract, "xliff", "exchange_path"))
    try:
        validate_xliff_schema(book_root, contract, input_path)
    except ValueError as exc:
        raise SystemExit(str(exc)) from exc
    tree = ET.parse(input_path)
    root = tree.getroot()
    if root.tag != f"{{{XLIFF_NS}}}xliff" or root.get("version") != "2.1":
        raise SystemExit("Input must be an XLIFF 2.1 document using the core 2.0 namespace.")
    if root.get("srcLang") != contract.get("source_language") or root.get("trgLang") != contract.get("target_language"):
        raise SystemExit("XLIFF source/target languages do not match the locked contract.")
    _manifest_path, store_path = unit_paths(book_root, contract)
    units = read_units(store_path)
    by_id = {str(unit["unit_id"]): unit for unit in units}
    imported_ids: list[str] = []
    for unit_node in root.findall(f".//{{{XLIFF_NS}}}unit"):
        unit_id = str(unit_node.get("id") or "")
        if unit_id not in by_id:
            raise SystemExit(f"XLIFF contains unknown unit ID: {unit_id}")
        segment = unit_node.find(f"{{{XLIFF_NS}}}segment")
        if segment is None:
            raise SystemExit(f"XLIFF unit lacks segment: {unit_id}")
        source = segment.find(f"{{{XLIFF_NS}}}source")
        target = segment.find(f"{{{XLIFF_NS}}}target")
        original_data = unit_node.find(f"{{{XLIFF_NS}}}originalData")
        data = {
            str(item.get("id") or ""): "".join(item.itertext())
            for item in ([] if original_data is None else original_data.findall(f"{{{XLIFF_NS}}}data"))
        }
        source_text = read_xliff_inline(source, data)
        if source_text != by_id[unit_id]["source_text"] or sha256_text(source_text) != by_id[unit_id]["source_sha256"]:
            raise SystemExit(f"XLIFF_SOURCE_OR_INLINE_CHANGED: XLIFF attempted to change locked source text: {unit_id}")
        notes = {
            str(note.get("category") or ""): "".join(note.itertext())
            for note in unit_node.findall(f"{{{XLIFF_NS}}}notes/{{{XLIFF_NS}}}note")
        }
        state = str(segment.get("state") or "initial")
        if state == "initial" and notes.get("lifebook-target-state") in {"needs_rerender", "needs_retranslation"}:
            state = notes["lifebook-target-state"]
        if state not in ALLOWED_STATES:
            raise SystemExit(f"Unsupported XLIFF state {state!r}: {unit_id}")
        target_template = read_xliff_inline(target, data)
        by_id[unit_id]["target_template"] = target_template
        by_id[unit_id]["target_template_sha256"] = sha256_text(target_template) if target_template else ""
        by_id[unit_id]["target_state"] = state
        by_id[unit_id]["translator_run_id"] = "xliff-import"
        by_id[unit_id]["contract_sha256"] = contract.get("contract_sha256", "")
        by_id[unit_id]["proper_noun_revision"] = (contract.get("proper_nouns") or {}).get("register_sha256", "")
        by_id[unit_id]["occurrence_ledger_revision"] = (contract.get("proper_nouns") or {}).get("occurrence_ledger_sha256", "")
        by_id[unit_id]["terminology_revision"] = (contract.get("terminology") or {}).get("register_sha256", "")
        imported_ids.append(unit_id)
    if imported_ids != [str(unit["unit_id"]) for unit in units]:
        raise SystemExit("XLIFF unit set/order differs from the canonical store; import refused.")
    apply_target_rendering(book_root, contract, units, allow_retranslation=True)
    commit_generation(book_root, contract, units, "xliff_import")
    print(f"XLIFF targets imported safely: units={len(units)}")


def chapter_digest(chapter_units: list[dict]) -> str:
    return canonical_json_digest([
        {
            "unit_id": unit["unit_id"],
            "source_sha256": unit["source_sha256"],
            "target_sha256": unit["target_sha256"],
            "translator_run_id": unit.get("translator_run_id", ""),
            "contract_sha256": unit["contract_sha256"],
            "proper_noun_revision": unit["proper_noun_revision"],
            "occurrence_ledger_revision": unit.get("occurrence_ledger_revision", ""),
            "terminology_revision": unit["terminology_revision"],
        }
        for unit in chapter_units
    ])


def group_units_by_chapter(units: list[dict]) -> dict[str, list[dict]]:
    grouped: dict[str, list[dict]] = defaultdict(list)
    for unit in units:
        grouped[str(unit["chapter_id"])].append(unit)
    return grouped


def resolve_audit_chapter(units: list[dict], requested_chapter: str | None) -> str:
    chapters = list(group_units_by_chapter(units))
    if requested_chapter:
        if requested_chapter not in chapters:
            raise ValueError(f"Unknown semantic audit chapter: {requested_chapter}")
        return requested_chapter
    if len(chapters) != 1:
        raise ValueError("Semantic audit chapter is required when the canonical store contains multiple chapters.")
    return chapters[0]


def audit_pointer_path(run_root: Path) -> Path:
    return run_root / "current_by_chapter.json"


def read_audit_pointers(run_root: Path) -> dict:
    path = audit_pointer_path(run_root)
    if not path.is_file():
        return {"schema_version": "1.0", "chapters": {}}
    value = read_json(path)
    if value.get("schema_version") != "1.0" or not isinstance(value.get("chapters"), dict):
        raise ValueError("Semantic audit chapter pointer file is invalid.")
    return value


def current_audit_run(book_root: Path, contract: dict, chapter: str | None = None) -> tuple[Path, dict]:
    _manifest_path, store_path = unit_paths(book_root, contract)
    units = read_units(store_path)
    chapter = resolve_audit_chapter(units, chapter)
    run_root = resolve_inside(book_root, contract_path(contract, "semantic_audit", "immutable_run_root"))
    pointers = read_audit_pointers(run_root)
    pointer = pointers["chapters"].get(chapter)
    if not isinstance(pointer, dict):
        raise ValueError(f"Current semantic audit pointer is missing for chapter {chapter}.")
    run_id = str(pointer.get("run_id") or "")
    if not run_id or not re.fullmatch(r"[A-Za-z0-9_.:-]+", run_id):
        raise ValueError(f"Current semantic audit pointer has invalid run_id for chapter {chapter}.")
    run_path = run_root / run_id
    manifest_path = run_path / "run_manifest.json"
    manifest = read_json(manifest_path)
    if pointer.get("run_manifest_sha256") != sha256_file(manifest_path):
        raise ValueError(f"Current semantic audit pointer has a stale run_manifest_sha256 for chapter {chapter}.")
    if manifest.get("chapter_id") != chapter:
        raise ValueError(f"Current semantic audit pointer targets the wrong chapter: {chapter}.")
    return run_path, manifest


def prepare_audit(
    book_root: Path,
    contract: dict,
    reviewer: str,
    model: str,
    requested_run_id: str | None,
    requested_chapter: str | None = None,
) -> None:
    manifest_path, store_path = unit_paths(book_root, contract)
    units = read_units(store_path)
    chapter = resolve_audit_chapter(units, requested_chapter)
    chapter_units = [unit for unit in units if str(unit.get("chapter_id")) == chapter]
    if any(not str(unit.get("target_text") or "").strip() for unit in chapter_units):
        raise ValueError(f"Semantic audit chapter has incomplete targets: {chapter}")
    if any(not str(unit.get("translator_run_id") or "").strip() for unit in chapter_units):
        raise ValueError(f"AUDIT_INDEPENDENCE_UNPROVABLE: chapter {chapter} lacks translation owner evidence.")
    translator_run_ids = sorted({
        str(unit.get("translator_run_id") or "").strip()
        for unit in chapter_units
        if str(unit.get("translator_run_id") or "").strip()
    })
    if reviewer in translator_run_ids:
        raise ValueError(
            f"AUDIT_INDEPENDENCE_VIOLATION: reviewer {reviewer!r} translated chapter {chapter}."
        )
    run_root = resolve_inside(book_root, contract_path(contract, "semantic_audit", "immutable_run_root"))
    run_id = requested_run_id or f"audit-{chapter}-{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}-{uuid.uuid4().hex[:8]}"
    if not re.fullmatch(r"[A-Za-z0-9_.:-]+", run_id):
        raise ValueError("Audit run_id contains unsupported characters.")
    run_path = run_root / run_id
    if run_path.exists():
        raise ValueError(f"Immutable audit run already exists: {run_id}")
    queue_path = run_path / "queue.jsonl"
    audit_root = run_path / "unit_audits"
    chapter_root = run_path / "chapter_reviews"
    batch_root = run_path / "batches"
    audit_root.mkdir(parents=True, exist_ok=False)
    chapter_root.mkdir(parents=True, exist_ok=False)
    batch_root.mkdir(parents=True, exist_ok=False)
    audit_config = contract.get("semantic_audit") if isinstance(contract.get("semantic_audit"), dict) else {}
    batch_max_units = int(audit_config.get("batch_max_units") or 0)
    max_attempts = int(audit_config.get("max_attempts_per_unit") or 0)
    token_budget = int(audit_config.get("token_budget_per_unit") or 0)
    if batch_max_units < 1 or max_attempts < 1 or token_budget < 256:
        raise ValueError("semantic audit batching, max attempts, and token budget must be positive")
    queue: list[dict] = []
    for index, unit in enumerate(chapter_units):
        batch_id = f"batch-{index // batch_max_units + 1:04d}"
        audit_path = audit_root / f"{safe_marker_id(str(unit['unit_id']))}.json"
        previous = chapter_units[index - 1] if index else None
        following = chapter_units[index + 1] if index + 1 < len(chapter_units) else None
        queue.append({
            "unit_id": unit["unit_id"],
            "chapter_id": chapter,
            "audit_path": audit_path.relative_to(book_root).as_posix(),
            "batch_id": batch_id,
            "max_attempts": max_attempts,
            "token_budget": token_budget,
            "source_text": unit["source_text"],
            "target_text": unit["target_text"],
            "previous_source_context": previous["source_text"] if previous else "",
            "next_source_context": following["source_text"] if following else "",
            "source_sha256": unit["source_sha256"],
            "target_sha256": unit["target_sha256"],
            "translator_run_id": unit.get("translator_run_id", ""),
            "contract_sha256": contract.get("contract_sha256"),
            "proper_noun_revision": unit["proper_noun_revision"],
            "occurrence_ledger_revision": unit.get("occurrence_ledger_revision", ""),
            "terminology_revision": unit["terminology_revision"],
            "required_checks": [
                "source_to_target_omission",
                "target_to_source_addition",
                "neighbor_boundary_contamination",
                "numbers_names_negation_notes",
            ],
        })
    write_text(queue_path, "".join(json.dumps(item, ensure_ascii=False, sort_keys=True) + "\n" for item in queue))
    batch_manifests: dict[str, dict] = {}
    for batch_id in sorted({str(item["batch_id"]) for item in queue}):
        batch_items = [item for item in queue if item["batch_id"] == batch_id]
        batch_path = batch_root / f"{batch_id}.json"
        write_json(batch_path, {
            "schema_version": "1.0",
            "run_id": run_id,
            "chapter_id": chapter,
            "batch_id": batch_id,
            "reviewer": reviewer,
            "model": model,
            "unit_ids": [item["unit_id"] for item in batch_items],
            "queue_item_sha256": canonical_json_digest(batch_items),
            "max_attempts_per_unit": max_attempts,
            "token_budget_per_unit": token_budget,
        })
        batch_manifests[batch_id] = {
            "path": batch_path.relative_to(book_root).as_posix(),
            "sha256": sha256_file(batch_path),
            "unit_count": len(batch_items),
        }
    digest = chapter_digest(chapter_units)
    run_manifest = {
        "schema_version": "2.0",
        "run_id": run_id,
        "chapter_id": chapter,
        "created_at": utc_now(),
        "reviewer": reviewer,
        "model": model,
        "translator_run_ids": translator_run_ids,
        "rubric_version": str(audit_config.get("rubric_version") or ""),
        "contract_sha256": contract.get("contract_sha256"),
        "canonical_manifest_sha256": sha256_file(manifest_path),
        "unit_store_sha256": sha256_file(store_path),
        "chapter_digest": digest,
        "chapter_digests": {chapter: digest},
        "queue_sha256": sha256_file(queue_path),
        "unit_count": len(chapter_units),
        "batch_count": len({item["batch_id"] for item in queue}),
        "batch_max_units": batch_max_units,
        "max_attempts_per_unit": max_attempts,
        "token_budget_per_unit": token_budget,
        "retry_requires_failure_evidence": audit_config.get("retry_requires_failure_evidence") is True,
        "batch_manifests": batch_manifests,
    }
    if not run_manifest["rubric_version"]:
        raise ValueError("semantic_audit.rubric_version must be configured before preparing audits")
    run_manifest_path = run_path / "run_manifest.json"
    write_json(run_manifest_path, run_manifest)
    pointers = read_audit_pointers(run_root)
    pointers["chapters"][chapter] = {
        "run_id": run_id,
        "run_manifest_sha256": sha256_file(run_manifest_path),
    }
    write_json(audit_pointer_path(run_root), pointers)
    print(f"semantic audit run prepared: chapter={chapter} run={run_id} units={len(queue)}")


def semantic_audit_evidence_files(run_path: Path) -> list[Path]:
    files = [run_path / "run_manifest.json", run_path / "queue.jsonl"]
    for directory in (run_path / "batches", run_path / "unit_audits", run_path / "chapter_reviews"):
        if directory.is_dir():
            files.extend(sorted(path for path in directory.glob("*.json") if path.is_file()))
    return files


def seal_audit_run(book_root: Path, contract: dict, chapter: str | None = None) -> None:
    run_path, run_manifest = current_audit_run(book_root, contract, chapter)
    chapter = str(run_manifest.get("chapter_id") or "")
    completion_path = run_path / "completion_manifest.json"
    if completion_path.exists():
        raise ValueError("Semantic audit run is already sealed; create a new run instead of overwriting evidence.")
    evidence = {
        path.relative_to(run_path).as_posix(): sha256_file(path)
        for path in semantic_audit_evidence_files(run_path)
    }
    completion = {
        "schema_version": "1.0",
        "status": "SEALED",
        "run_id": run_manifest.get("run_id"),
        "chapter_id": chapter,
        "chapter_digest": run_manifest.get("chapter_digest"),
        "sealed_at": utc_now(),
        "contract_sha256": contract.get("contract_sha256"),
        "canonical_manifest_sha256": run_manifest.get("canonical_manifest_sha256"),
        "evidence_sha256": evidence,
    }
    write_json(completion_path, completion)
    run_root = resolve_inside(book_root, contract_path(contract, "semantic_audit", "immutable_run_root"))
    pointers = read_audit_pointers(run_root)
    pointers["chapters"][chapter] = {
        "run_id": run_manifest.get("run_id"),
        "run_manifest_sha256": sha256_file(run_path / "run_manifest.json"),
        "completion_manifest_sha256": sha256_file(completion_path),
    }
    write_json(audit_pointer_path(run_root), pointers)


def validate_chapter_audit(
    book_root: Path,
    contract: dict,
    units: list[dict],
    chapter: str,
    require_seal: bool = True,
) -> tuple[list[str], dict]:
    chapter_units = [unit for unit in units if str(unit.get("chapter_id")) == chapter]
    issues: list[str] = []
    try:
        run_path, run_manifest = current_audit_run(book_root, contract, chapter)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        return [str(exc)], {"status": "FAIL", "issues": [str(exc)]}
    queue_path = run_path / "queue.jsonl"
    try:
        queue = read_units(queue_path)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        queue = []
        issues.append(f"invalid semantic audit queue: {exc}")
    queue_by_id = {str(item.get("unit_id") or ""): item for item in queue}
    if len(queue_by_id) != len(queue) or [str(item.get("unit_id") or "") for item in queue] != [str(unit["unit_id"]) for unit in chapter_units]:
        issues.append(f"semantic audit queue unit coverage/order differs from canonical chapter {chapter}")
    if not queue_path.is_file() or run_manifest.get("queue_sha256") != sha256_file(queue_path):
        issues.append("stale semantic audit run: queue_sha256 mismatch")
    for key, expected in (
        ("contract_sha256", contract.get("contract_sha256")),
        ("chapter_id", chapter),
        ("chapter_digest", chapter_digest(chapter_units)),
        ("unit_count", len(chapter_units)),
    ):
        if run_manifest.get(key) != expected:
            issues.append(f"stale semantic audit run: {key} mismatch")
    translator_run_ids = sorted({
        str(unit.get("translator_run_id") or "").strip()
        for unit in chapter_units
        if str(unit.get("translator_run_id") or "").strip()
    })
    if any(not str(unit.get("translator_run_id") or "").strip() for unit in chapter_units):
        issues.append(f"AUDIT_INDEPENDENCE_UNPROVABLE: chapter {chapter} lacks translation owner evidence")
    if run_manifest.get("translator_run_ids") != translator_run_ids:
        issues.append("stale semantic audit run: translator_run_ids mismatch")
    if str(run_manifest.get("reviewer") or "") in translator_run_ids:
        issues.append(f"AUDIT_INDEPENDENCE_VIOLATION: reviewer translated chapter {chapter}")
    if not all(str(run_manifest.get(key) or "").strip() for key in ("run_id", "reviewer", "model", "rubric_version")):
        issues.append("semantic audit run lacks reviewer/model/rubric identity")
    audit_config = contract.get("semantic_audit") if isinstance(contract.get("semantic_audit"), dict) else {}
    for key, expected in (
        ("batch_max_units", int(audit_config.get("batch_max_units") or 0)),
        ("max_attempts_per_unit", int(audit_config.get("max_attempts_per_unit") or 0)),
        ("token_budget_per_unit", int(audit_config.get("token_budget_per_unit") or 0)),
        ("retry_requires_failure_evidence", audit_config.get("retry_requires_failure_evidence") is True),
    ):
        if run_manifest.get(key) != expected:
            issues.append(f"semantic audit run policy mismatch: {key}")
    if run_manifest.get("batch_count") != len({str(item.get("batch_id") or "") for item in queue}):
        issues.append("semantic audit run batch_count differs from queue")
    required_checks = [
        "source_to_target_omission",
        "target_to_source_addition",
        "neighbor_boundary_contamination",
        "numbers_names_negation_notes",
    ]
    for item in queue:
        if (
            item.get("max_attempts") != run_manifest.get("max_attempts_per_unit")
            or item.get("token_budget") != run_manifest.get("token_budget_per_unit")
            or item.get("required_checks") != required_checks
        ):
            issues.append(f"semantic audit queue policy differs for unit {item.get('unit_id')}")
    expected_batches: dict[str, list[dict]] = defaultdict(list)
    for item in queue:
        expected_batches[str(item.get("batch_id") or "")].append(item)
    recorded_batches = run_manifest.get("batch_manifests") if isinstance(run_manifest.get("batch_manifests"), dict) else {}
    if set(recorded_batches) != set(expected_batches):
        issues.append("semantic audit batch manifest coverage differs from queue")
    batch_root = run_path / "batches"
    actual_batch_names = {path.stem for path in batch_root.glob("*.json") if path.is_file()} if batch_root.is_dir() else set()
    if actual_batch_names != set(expected_batches):
        issues.append("semantic audit batch files differ from queue")
    for batch_id, batch_items in expected_batches.items():
        batch_path = batch_root / f"{batch_id}.json"
        record = recorded_batches.get(batch_id) if isinstance(recorded_batches.get(batch_id), dict) else {}
        if not batch_path.is_file():
            continue
        try:
            batch = read_json(batch_path)
        except (OSError, ValueError, json.JSONDecodeError) as exc:
            issues.append(f"invalid semantic audit batch {batch_id}: {exc}")
            continue
        expected_path = batch_path.relative_to(book_root).as_posix()
        expected_ids = [item.get("unit_id") for item in batch_items]
        if record.get("path") != expected_path or record.get("sha256") != sha256_file(batch_path) or record.get("unit_count") != len(batch_items):
            issues.append(f"semantic audit batch manifest is stale: {batch_id}")
        if (
            batch.get("run_id") != run_manifest.get("run_id")
            or batch.get("batch_id") != batch_id
            or batch.get("unit_ids") != expected_ids
            or batch.get("queue_item_sha256") != canonical_json_digest(batch_items)
            or batch.get("max_attempts_per_unit") != run_manifest.get("max_attempts_per_unit")
            or batch.get("token_budget_per_unit") != run_manifest.get("token_budget_per_unit")
        ):
            issues.append(f"semantic audit batch content differs from queue: {batch_id}")
    audit_root = run_path / "unit_audits"
    expected_audit_names = {f"{safe_marker_id(str(unit['unit_id']))}.json" for unit in chapter_units}
    actual_audit_names = {path.name for path in audit_root.glob("*.json") if path.is_file()} if audit_root.is_dir() else set()
    if actual_audit_names != expected_audit_names:
        issues.append("semantic unit audit file set differs from canonical unit coverage")
    passed_ids: list[str] = []
    for unit in chapter_units:
        path = audit_root / f"{safe_marker_id(str(unit['unit_id']))}.json"
        if not path.is_file():
            issues.append(f"missing semantic unit audit: {path.relative_to(book_root).as_posix()}")
            continue
        try:
            audit = read_json(path)
        except (OSError, ValueError, json.JSONDecodeError) as exc:
            issues.append(str(exc))
            continue
        queue_item = queue_by_id.get(str(unit["unit_id"]), {})
        for key, expected in (
            ("unit_id", unit["unit_id"]),
            ("source_sha256", unit["source_sha256"]),
            ("target_sha256", unit["target_sha256"]),
            ("contract_sha256", contract.get("contract_sha256")),
            ("proper_noun_revision", unit["proper_noun_revision"]),
            ("occurrence_ledger_revision", unit.get("occurrence_ledger_revision", "")),
            ("terminology_revision", unit["terminology_revision"]),
            ("run_id", run_manifest.get("run_id")),
            ("reviewer", run_manifest.get("reviewer")),
            ("model", run_manifest.get("model")),
            ("rubric_version", run_manifest.get("rubric_version")),
            ("batch_id", queue_item.get("batch_id")),
        ):
            if audit.get(key) != expected:
                issues.append(f"stale semantic audit {path.name}: {key} mismatch")
        if audit.get("status") != "PASS":
            issues.append(f"semantic audit is not PASS: {path.name}")
        checks = audit.get("checks") if isinstance(audit.get("checks"), dict) else {}
        check_codes = {
            "source_to_target_omission": "SEMANTIC_OMISSION",
            "target_to_source_addition": "SEMANTIC_ADDITION",
            "neighbor_boundary_contamination": "NEIGHBOR_CONTAMINATION",
            "numbers_names_negation_notes": "SEMANTIC_CRITICAL_DETAIL",
        }
        for check, error_code in check_codes.items():
            result = checks.get(check) if isinstance(checks.get(check), dict) else {}
            if result.get("status") != "PASS" or not str(result.get("evidence") or "").strip():
                issues.append(f"{error_code}: semantic audit lacks structured PASS evidence for {check}: {path.name}")
        findings = audit.get("findings")
        if not isinstance(findings, list) or findings:
            issues.append(f"semantic PASS requires an explicit empty findings list: {path.name}")
        if not str(audit.get("review_summary") or "").strip():
            issues.append(f"semantic audit lacks evidence summary: {path.name}")
        if not str(audit.get("reviewed_at") or "").strip():
            issues.append(f"semantic audit lacks reviewed_at traceability: {path.name}")
        attempt = audit.get("attempt")
        max_attempts = int(queue_item.get("max_attempts") or 0)
        token_budget = int(queue_item.get("token_budget") or 0)
        if not isinstance(attempt, int) or attempt < 1 or attempt > max_attempts:
            issues.append(f"semantic audit attempt is outside retry policy: {path.name}")
        for token_field in ("input_tokens", "output_tokens"):
            token_count = audit.get(token_field)
            if not isinstance(token_count, int) or token_count < 0 or token_count > token_budget:
                issues.append(f"semantic audit {token_field} exceeds or lacks token budget evidence: {path.name}")
        if isinstance(attempt, int) and attempt > 1 and run_manifest.get("retry_requires_failure_evidence") is True:
            prior_attempts = audit.get("prior_attempts")
            if (
                not isinstance(prior_attempts, list)
                or len(prior_attempts) != attempt - 1
                or any(
                    not isinstance(item, dict)
                    or item.get("status") != "FAIL"
                    or not str(item.get("failure_evidence") or "").strip()
                    for item in prior_attempts
                )
            ):
                issues.append(f"semantic audit retry lacks prior failure evidence: {path.name}")
        if not any(issue.endswith(path.name) or path.name in issue for issue in issues):
            passed_ids.append(str(unit["unit_id"]))
    chapter_root = run_path / "chapter_reviews"
    grouped = {chapter: chapter_units}
    expected_chapter_names = {f"{chapter}.json" for chapter in grouped}
    actual_chapter_names = {path.name for path in chapter_root.glob("*.json") if path.is_file()} if chapter_root.is_dir() else set()
    if actual_chapter_names != expected_chapter_names:
        issues.append("full-chapter review file set differs from canonical chapter coverage")
    for chapter, chapter_units in grouped.items():
        path = chapter_root / f"{chapter}.json"
        if not path.is_file():
            issues.append(f"missing full-chapter review: {path.relative_to(book_root).as_posix()}")
            continue
        review = read_json(path)
        expected_ids = [str(unit["unit_id"]) for unit in chapter_units]
        if review.get("status") != "PASS" or review.get("scope") != "FULL_CHAPTER":
            issues.append(f"full-chapter review is not a FULL_CHAPTER PASS: {path.name}")
        if review.get("issues_found") != 0 or review.get("fixes_applied") != 0 or review.get("unresolved_blocking_issues") != 0:
            issues.append(f"full-chapter PASS must be a fresh zero-issue round: {path.name}")
        if review.get("chapter_digest") != chapter_digest(chapter_units):
            issues.append(f"full-chapter review is stale: {path.name}")
        if review.get("reviewed_unit_ids") != expected_ids:
            issues.append(f"full-chapter review lacks exact unit coverage/order: {path.name}")
        if (
            review.get("run_id") != run_manifest.get("run_id")
            or review.get("reviewer") != run_manifest.get("reviewer")
            or review.get("model") != run_manifest.get("model")
            or review.get("rubric_version") != run_manifest.get("rubric_version")
        ):
            issues.append(f"full-chapter review identity differs from immutable run: {path.name}")
        if not isinstance(review.get("findings"), list) or review.get("findings"):
            issues.append(f"full-chapter PASS requires an explicit empty findings list: {path.name}")
        if not str(review.get("reviewed_at") or "").strip() or not str(review.get("review_summary") or "").strip():
            issues.append(f"full-chapter review lacks timestamp or evidence summary: {path.name}")
    completion_path = run_path / "completion_manifest.json"
    if require_seal:
        if not completion_path.is_file():
            issues.append("semantic audit run is not sealed")
        else:
            try:
                completion = read_json(completion_path)
                pointers = read_audit_pointers(run_path.parent)
                pointer = pointers["chapters"].get(chapter, {})
                expected_evidence = completion.get("evidence_sha256") if isinstance(completion.get("evidence_sha256"), dict) else {}
                actual_evidence = {
                    path.relative_to(run_path).as_posix(): sha256_file(path)
                    for path in semantic_audit_evidence_files(run_path)
                }
                if (
                    completion.get("status") != "SEALED"
                    or completion.get("run_id") != run_manifest.get("run_id")
                    or completion.get("contract_sha256") != contract.get("contract_sha256")
                    or completion.get("canonical_manifest_sha256") != run_manifest.get("canonical_manifest_sha256")
                    or expected_evidence != actual_evidence
                    or pointer.get("completion_manifest_sha256") != sha256_file(completion_path)
                ):
                    issues.append("semantic audit sealed evidence is stale or has been modified")
            except (OSError, ValueError, json.JSONDecodeError) as exc:
                issues.append(f"invalid semantic audit completion manifest: {exc}")
    report = {
        "status": "PASS" if not issues else "FAIL",
        "unit_count": len(chapter_units),
        "unit_audit_pass_count": len(passed_ids),
        "chapter_count": 1,
        "chapter_id": chapter,
        "run_id": run_manifest.get("run_id"),
        "canonical_manifest_sha256": run_manifest.get("canonical_manifest_sha256"),
        "issues": issues,
        "note": "PASS here validates hash-bound audit evidence and coverage; it does not replace the substantive reviewer judgment recorded in those audits.",
    }
    return issues, report


def validate_audits(
    book_root: Path,
    contract: dict,
    units: list[dict] | None = None,
    require_seal: bool = True,
    chapter: str | None = None,
) -> tuple[list[str], dict]:
    if units is None:
        _manifest_path, store_path = unit_paths(book_root, contract)
        units = read_units(store_path)
    grouped = group_units_by_chapter(units)
    chapters = [resolve_audit_chapter(units, chapter)] if chapter else sorted(grouped)
    issues: list[str] = []
    chapter_reports: list[dict] = []
    for chapter_id in chapters:
        chapter_issues, chapter_report = validate_chapter_audit(
            book_root,
            contract,
            units,
            chapter_id,
            require_seal=require_seal,
        )
        issues.extend(chapter_issues)
        chapter_reports.append(chapter_report)

    completion_path = resolve_inside(
        book_root,
        contract_path(contract, "semantic_audit", "immutable_run_root"),
    ) / "book_completion_manifest.json"
    if chapter is None and require_seal and not issues:
        manifest_path, store_path = unit_paths(book_root, contract)
        completion_chapters: list[dict] = []
        for report in chapter_reports:
            chapter_id = str(report["chapter_id"])
            run_path, run_manifest = current_audit_run(book_root, contract, chapter_id)
            chapter_completion = read_json(run_path / "completion_manifest.json")
            completion_chapters.append({
                "chapter_id": chapter_id,
                "chapter_digest": run_manifest.get("chapter_digest"),
                "run_id": run_manifest.get("run_id"),
                "reviewer": run_manifest.get("reviewer"),
                "model": run_manifest.get("model"),
                "run_manifest_sha256": sha256_file(run_path / "run_manifest.json"),
                "completion_manifest_sha256": sha256_file(run_path / "completion_manifest.json"),
                "sealed_at": chapter_completion.get("sealed_at"),
            })
        write_json(completion_path, {
            "schema_version": "1.0",
            "status": "PASS",
            "contract_sha256": contract.get("contract_sha256"),
            "canonical_manifest_sha256": sha256_file(manifest_path),
            "unit_store_sha256": sha256_file(store_path),
            "chapter_count": len(completion_chapters),
            "chapters": completion_chapters,
        })

    report = {
        "status": "PASS" if not issues else "FAIL",
        "unit_count": sum(int(item.get("unit_count") or 0) for item in chapter_reports),
        "unit_audit_pass_count": sum(int(item.get("unit_audit_pass_count") or 0) for item in chapter_reports),
        "chapter_count": len(chapter_reports),
        "chapter_reports": chapter_reports,
        "book_completion_manifest": completion_path.relative_to(book_root).as_posix() if completion_path.is_file() and not issues else "",
        "issues": issues,
        "note": "PASS validates current chapter-scoped immutable evidence; substantive translation quality remains the reviewers' recorded judgment.",
    }
    return issues, report


MARKER_RE = re.compile(r"<!--\s*lifebook-unit:([^\s]+)\s+target-sha256:([0-9a-f]{64})\s*-->")


def artifact_manifest(archive: zipfile.ZipFile) -> dict:
    names = [name for name in archive.namelist() if name.endswith("translation-unit-manifest.json")]
    if len(names) != 1:
        raise ValueError(f"EPUB must contain exactly one translation-unit-manifest.json; found {len(names)}")
    value = json.loads(archive.read(names[0]).decode("utf-8-sig"))
    if not isinstance(value, dict):
        raise ValueError("EPUB translation unit manifest must be an object")
    return value


def local_name(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


def epub_spine_documents(archive: zipfile.ZipFile) -> list[str]:
    container = ET.fromstring(archive.read("META-INF/container.xml"))
    rootfile = next((node for node in container.iter() if local_name(node.tag) == "rootfile"), None)
    if rootfile is None or not rootfile.get("full-path"):
        raise ValueError("EPUB container lacks package rootfile")
    opf_name = str(rootfile.get("full-path"))
    opf = ET.fromstring(archive.read(opf_name))
    href_by_id = {
        str(node.get("id")): str(node.get("href"))
        for node in opf.iter()
        if local_name(node.tag) == "item" and node.get("id") and node.get("href")
    }
    base = str(Path(opf_name).parent).replace("\\", "/")
    names: list[str] = []
    for node in opf.iter():
        if local_name(node.tag) != "itemref":
            continue
        href = href_by_id.get(str(node.get("idref") or ""))
        if href:
            names.append(f"{base}/{href}" if base not in {"", "."} else href)
    return names


def validate_epub_navigation(archive: zipfile.ZipFile, content_documents: set[str]) -> list[str]:
    issues: list[str] = []
    container = ET.fromstring(archive.read("META-INF/container.xml"))
    rootfile = next((node for node in container.iter() if local_name(node.tag) == "rootfile"), None)
    if rootfile is None or not rootfile.get("full-path"):
        return ["NAVIGATION_INVALID: EPUB container lacks package rootfile"]
    opf_name = str(rootfile.get("full-path"))
    opf = ET.fromstring(archive.read(opf_name))
    nav_items = [
        node for node in opf.iter()
        if local_name(node.tag) == "item" and "nav" in str(node.get("properties") or "").split()
    ]
    if len(nav_items) != 1 or not nav_items[0].get("href"):
        return [f"NAVIGATION_INVALID: EPUB must declare exactly one nav item; found {len(nav_items)}"]
    opf_base = posixpath.dirname(opf_name)
    nav_name = posixpath.normpath(posixpath.join(opf_base, str(nav_items[0].get("href"))))
    if nav_name not in archive.namelist():
        return [f"NAVIGATION_INVALID: nav document is missing: {nav_name}"]
    nav_root = ET.fromstring(archive.read(nav_name))
    toc = next(
        (
            node for node in nav_root.iter()
            if local_name(node.tag) == "nav"
            and (
                node.get("{http://www.idpf.org/2007/ops}type") == "toc"
                or "toc" in str(node.get("role") or "").casefold()
            )
        ),
        None,
    )
    if toc is None:
        return ["NAVIGATION_INVALID: nav document lacks a table of contents"]
    nav_base = posixpath.dirname(nav_name)
    linked_documents: set[str] = set()
    links = [node for node in toc.iter() if local_name(node.tag) == "a" and node.get("href")]
    if not links:
        issues.append("NAVIGATION_INVALID: table of contents has no links")
    for link in links:
        href = unquote(str(link.get("href") or ""))
        if re.match(r"^[A-Za-z][A-Za-z0-9+.-]*:", href):
            continue
        path_part, _separator, fragment = href.partition("#")
        target_name = posixpath.normpath(posixpath.join(nav_base, path_part or posixpath.basename(nav_name)))
        if target_name not in archive.namelist():
            issues.append(f"NAVIGATION_INVALID: TOC target is missing: {href}")
            continue
        linked_documents.add(target_name)
        if fragment:
            target_root = ET.fromstring(archive.read(target_name))
            if not any(node.get("id") == fragment for node in target_root.iter()):
                issues.append(f"NAVIGATION_INVALID: TOC fragment is missing: {href}")
    uncovered = sorted(content_documents - linked_documents)
    if uncovered:
        issues.append("NAVIGATION_INVALID: reader-content spine documents lack TOC coverage: " + ", ".join(uncovered[:10]))
    return issues


def node_text(node: ET.Element | None) -> str:
    return "" if node is None else " ".join("".join(node.itertext()).split())


HIDDEN_CSS_DECLARATION_RE = re.compile(
    r"(?:display\s*:\s*none|visibility\s*:\s*(?:hidden|collapse)|opacity\s*:\s*0(?:\D|$)|"
    r"font-size\s*:\s*0(?:\D|$)|color\s*:\s*transparent|clip-path\s*:|clip\s*:\s*rect\s*\(\s*0)",
    re.I | re.S,
)


def bilingual_target_selector_tokens(archive: zipfile.ZipFile) -> set[str]:
    tokens = {"html", "body", ".bitext-unit", ".bitext-target"}
    for name in epub_spine_documents(archive):
        if name not in archive.namelist():
            continue
        root = ET.fromstring(archive.read(name))
        parent_map = {child: parent for parent in root.iter() for child in parent}
        targets = [
            node for node in root.iter()
            if "bitext-target" in str(node.get("class") or "").split()
        ]
        for target in targets:
            current: ET.Element | None = target
            while current is not None:
                tokens.add(local_name(current.tag).casefold())
                tokens.update(f".{value}" for value in str(current.get("class") or "").split() if value)
                if current.get("id"):
                    tokens.add(f"#{current.get('id')}")
                current = parent_map.get(current)
    return tokens


def css_hidden_bilingual_selectors(css: str, content_tokens: set[str]) -> list[str]:
    hidden: list[str] = []
    for match in re.finditer(r"([^{}]+)\{([^{}]*)\}", css, re.S):
        selector_group, declarations = match.group(1), match.group(2)
        if not HIDDEN_CSS_DECLARATION_RE.search(declarations):
            continue
        for raw_selector in selector_group.split(","):
            selector = raw_selector.strip()
            if not selector or selector.startswith("@"):
                continue
            classes = {f".{item}" for item in re.findall(r"\.([A-Za-z_][\w-]*)", selector)}
            ids = {f"#{item}" for item in re.findall(r"#([A-Za-z_][\w-]*)", selector)}
            if not classes.issubset(content_tokens) or not ids.issubset(content_tokens):
                continue
            selector_tags = {
                item.casefold() for item in re.findall(r"(?:^|[\s>+~])([A-Za-z][\w-]*)", selector)
                if item.casefold() not in {"not", "is", "where"}
            }
            if selector.strip() == "*" or (
                (classes or ids or selector_tags)
                and (not selector_tags or bool(selector_tags & content_tokens))
            ):
                hidden.append(selector)
    return hidden


def extract_epub_units(archive: zipfile.ZipFile, kind: str) -> tuple[list[dict], list[str]]:
    records: list[dict] = []
    issues: list[str] = []
    seen: set[str] = set()
    block_tags = {"p", "h1", "h2", "h3", "h4", "h5", "h6", "blockquote", "li", "table", "figure", "aside", "section", "div"}
    attribute = "data-unit-id" if kind == "target_only" else "data-align-id"
    for name in epub_spine_documents(archive):
        if name not in archive.namelist():
            issues.append(f"spine document is missing: {name}")
            continue
        root = ET.fromstring(archive.read(name))
        body = next((node for node in root.iter() if local_name(node.tag) == "body"), None)
        if body is None:
            issues.append(f"spine document lacks body: {name}")
            continue
        unit_nodes = [node for node in body.iter() if node.get(attribute)]
        if not unit_nodes:
            continue
        parent_map = {child: parent for parent in body.iter() for child in parent}
        for node in body.iter():
            if local_name(node.tag) not in block_tags or not node_text(node):
                continue
            if node.get("data-lifebook-editorial"):
                continue
            current: ET.Element | None = node
            inside_unit = False
            while current is not None:
                if current.get(attribute):
                    inside_unit = True
                    break
                current = parent_map.get(current)
            has_unit_descendant = any(desc.get(attribute) for desc in node.iter() if desc is not node)
            if not inside_unit and not has_unit_descendant:
                issues.append(f"UNREGISTERED_READER_TEXT: {name}:{local_name(node.tag)}:{node_text(node)[:80]}")
        for node in unit_nodes:
            unit_id = str(node.get(attribute) or "")
            if unit_id in seen:
                issues.append(f"duplicate reader unit ID: {unit_id}")
            seen.add(unit_id)
            record = {
                "unit_id": unit_id,
                "source_sha256": str(node.get("data-source-sha256") or ""),
                "target_sha256": str(node.get("data-target-sha256") or ""),
                "document": name,
            }
            if kind == "bilingual":
                children = [child for child in list(node) if isinstance(child.tag, str)]
                source_nodes = [child for child in children if "bitext-source" in child.get("class", "").split()]
                target_nodes = [child for child in children if "bitext-target" in child.get("class", "").split()]
                if len(source_nodes) != 1 or len(target_nodes) != 1 or children.index(source_nodes[0]) + 1 != children.index(target_nodes[0]):
                    issues.append(f"NON_ADJACENT_PAIR: {unit_id}")
                    source_node = source_nodes[0] if source_nodes else None
                    target_node = target_nodes[0] if target_nodes else None
                else:
                    source_node, target_node = source_nodes[0], target_nodes[0]
                record["source_text"] = node_text(source_node)
                record["target_text"] = node_text(target_node)
            else:
                record["target_text"] = node_text(node)
            records.append(record)
    return records, issues


def plain_markdown_text(value: str) -> str:
    value = re.sub(r"<!--.*?-->", "", value, flags=re.DOTALL)
    value = re.sub(r"<[^>]+>", " ", value)
    value = re.sub(r"^#{1,6}\s+", "", value)
    value = re.sub(r"[`*_]", "", value)
    return " ".join(value.split())


def detected_reader_apps() -> list[str]:
    found: set[str] = set()
    command_names = ("ebook-viewer", "thorium", "foliate", "fbreader")
    for command in command_names:
        if shutil.which(command):
            found.add(command)
    environment_candidates = (
        ("ProgramFiles", "Calibre2", "ebook-viewer.exe", "Calibre ebook-viewer"),
        ("ProgramFiles(x86)", "Calibre2", "ebook-viewer.exe", "Calibre ebook-viewer"),
        ("LOCALAPPDATA", "Programs", "Thorium", "Thorium.exe", "Thorium Reader"),
    )
    for env_name, *parts in environment_candidates:
        root = os.environ.get(env_name)
        if not root:
            continue
        label = parts[-1]
        if Path(root, *parts[:-1]).is_file():
            found.add(label)
    return sorted(found)


def verify_artifacts(book_root: Path, contract: dict, reader_mode: str = "none") -> tuple[list[str], dict]:
    issues: list[str] = []
    warnings: list[str] = []
    manifest_path, store_path = unit_paths(book_root, contract)
    units = read_units(store_path)
    expected = [
        {
            "unit_id": str(unit["unit_id"]),
            "source_sha256": str(unit["source_sha256"]),
            "target_sha256": str(unit["target_sha256"]),
            "source_text": plain_markdown_text(str(unit.get("source_text") or "")),
            "target_text": plain_markdown_text(str(unit.get("target_text") or "")),
        }
        for unit in units
    ]
    expected_ids = [row["unit_id"] for row in expected]
    expected_manifest = read_json(book_root / "output" / "translation_unit_manifest.json")
    if expected_manifest.get("unit_store_sha256") != sha256_file(store_path):
        issues.append("output translation-unit manifest is stale")
    state_path = book_root / "state" / "pipeline_state.json"
    state = read_json(state_path) if state_path.is_file() else {}
    target_epub = resolve_inside(book_root, str(next(
        (
            item.get("artifact") for item in state.get("output_editions", [])
            if item.get("edition_type") == "target_only" and item.get("enabled")
        ),
        "output/book.epub",
    )))
    bilingual_epub = resolve_inside(book_root, str(next(
        (
            item.get("artifact") for item in state.get("output_editions", [])
            if item.get("edition_type") == "bilingual_parallel" and item.get("enabled")
        ),
        "output/book_bilingual_parallel.epub",
    )))
    artifact_info = []
    artifact_records: dict[str, list[dict]] = {}
    artifact_hashes: dict[str, str] = {}
    for kind, path in (("target_only", target_epub), ("bilingual", bilingual_epub)):
        if kind == "bilingual" and contract.get("edition_type") != "bilingual_parallel":
            continue
        if not path.is_file():
            issues.append(f"missing {kind} EPUB: {path.relative_to(book_root).as_posix()}")
            continue
        try:
            with zipfile.ZipFile(path) as archive:
                manifest = artifact_manifest(archive)
                if manifest.get("target_unit_manifest_sha256") != expected_manifest.get("target_unit_manifest_sha256"):
                    issues.append(f"{kind} EPUB target unit manifest differs from canonical units")
                records, record_issues = extract_epub_units(archive, kind)
                issues.extend(f"{kind}: {issue}" for issue in record_issues)
                issues.extend(f"{kind}: {issue}" for issue in validate_epub_navigation(
                    archive,
                    {str(record.get("document") or "") for record in records if record.get("document")},
                ))
                artifact_records[kind] = records
                artifact_hashes[kind] = sha256_file(path)
                if kind == "bilingual":
                    css = "\n".join(archive.read(name).decode("utf-8", errors="replace") for name in archive.namelist() if name.lower().endswith(".css"))
                    hidden_selectors = css_hidden_bilingual_selectors(css, bilingual_target_selector_tokens(archive))
                    if hidden_selectors:
                        issues.append(
                            "TARGET_NOT_VISIBLE: bilingual EPUB CSS can hide reader content via "
                            + ", ".join(hidden_selectors[:5])
                        )
                artifact_info.append({
                    "kind": kind,
                    "path": path.relative_to(book_root).as_posix(),
                    "epub_sha256": sha256_file(path),
                    "unit_count": len(records),
                })
        except (OSError, zipfile.BadZipFile, ValueError, json.JSONDecodeError) as exc:
            issues.append(f"invalid {kind} EPUB: {exc}")
    for kind, actual in artifact_records.items():
        if kind == "bilingual" and contract.get("edition_type") != "bilingual_parallel":
            continue
        actual_ids = [row["unit_id"] for row in actual]
        if actual_ids != expected_ids:
            issues.append(f"{kind} EPUB unit ID coverage/order differs from canonical units")
            continue
        for actual_row, wanted in zip(actual, expected):
            unit_id = wanted["unit_id"]
            for key in ("source_sha256", "target_sha256", "target_text"):
                if actual_row.get(key) != wanted.get(key):
                    issues.append(f"{kind} EPUB {key} differs for {unit_id}")
            if kind == "bilingual" and actual_row.get("source_text") != wanted.get("source_text"):
                issues.append(f"bilingual EPUB source reader text differs for {unit_id}")
                if len(issues) >= 100:
                    break
    if "target_only" in artifact_records and "bilingual" in artifact_records:
        target_projection = [(row["unit_id"], row.get("target_sha256"), row.get("target_text")) for row in artifact_records["target_only"]]
        bilingual_projection = [(row["unit_id"], row.get("target_sha256"), row.get("target_text")) for row in artifact_records["bilingual"]]
        if target_projection != bilingual_projection:
            issues.append("target-only and bilingual EPUB reader-visible target units differ")

    artifact_config = contract.get("artifact_validation") if isinstance(contract.get("artifact_validation"), dict) else {}
    reader_report_path = resolve_inside(book_root, str(artifact_config.get("reader_validation_report") or "qa/translation_units/reader_validation.json"))
    available_readers = detected_reader_apps() if reader_mode in {"required", "if_available"} else []
    reader_status = "NOT_REQUESTED"
    reader_issue_start = len(issues)
    try:
        if reader_mode == "none":
            raise FileNotFoundError("reader smoke test is release-candidate-only")
        if reader_mode == "if_available" and not available_readers:
            reader_status = "SKIPPED_UNAVAILABLE"
            warnings.append(
                "REAL_READER_SKIPPED_UNAVAILABLE: no supported local EPUB reader was detected; disclose this release boundary to the user"
            )
            raise FileNotFoundError("no supported reader is available")
        reader = read_json(reader_report_path)
        if reader.get("status") != "PASS" or not str(reader.get("validator") or "").strip() or not str(reader.get("validated_at") or "").strip():
            issues.append("reader validation report is not a traceable PASS")
        if reader.get("canonical_manifest_sha256") != sha256_file(manifest_path):
            issues.append("ARTIFACT_REPORT_HASH_MISMATCH: reader report canonical manifest is stale")
        reader_artifacts = {
            str(item.get("kind")): str(item.get("epub_sha256"))
            for item in reader.get("artifacts", []) if isinstance(item, dict)
        }
        if reader_artifacts != artifact_hashes:
            issues.append("ARTIFACT_REPORT_HASH_MISMATCH: reader report EPUB hashes differ")
        required_viewports = set(artifact_config.get("required_viewports") or [])
        passed_viewports = {
            str(item.get("name")) for item in reader.get("viewports", [])
            if isinstance(item, dict) and item.get("status") == "PASS"
        }
        if not required_viewports.issubset(passed_viewports):
            issues.append("reader report lacks required passing viewports")
        if not reader.get("computed_style_checks") or any(item.get("status") != "PASS" for item in reader.get("computed_style_checks", []) if isinstance(item, dict)):
            issues.append("TARGET_NOT_VISIBLE: computed-style evidence is missing or failed")
        if not reader.get("navigation_checks") or any(item.get("status") != "PASS" for item in reader.get("navigation_checks", []) if isinstance(item, dict)):
            issues.append("reader navigation evidence is missing or failed")
        screenshots = reader.get("screenshots") if isinstance(reader.get("screenshots"), list) else []
        valid_screenshot_viewports: set[str] = set()
        valid_screenshot_locations: set[str] = set()
        for shot in screenshots:
            if not isinstance(shot, dict):
                continue
            path_value = str(shot.get("path") or "")
            screenshot = resolve_inside(book_root, path_value) if path_value else None
            if screenshot is None or not screenshot.is_file() or shot.get("sha256") != sha256_file(screenshot):
                issues.append("reader screenshot evidence is missing or stale")
            else:
                valid_screenshot_viewports.add(str(shot.get("viewport") or ""))
                valid_screenshot_locations.add(str(shot.get("location") or ""))
        if not required_viewports.issubset(valid_screenshot_viewports):
            issues.append("reader screenshots do not cover all required viewports")
        required_locations = set(artifact_config.get("required_reader_locations") or [])
        if not required_locations.issubset(valid_screenshot_locations):
            issues.append("reader screenshots do not cover all required representative locations")
        if len(issues) == reader_issue_start:
            reader_status = "PASS"
    except FileNotFoundError as exc:
        if reader_mode == "required" or (reader_mode == "if_available" and available_readers):
            issues.append(f"reader validation evidence invalid: {exc}")
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        issues.append(f"reader validation evidence invalid: {exc}")

    report = {
        "status": "PASS" if not issues else "FAIL",
        "canonical_manifest_sha256": sha256_file(manifest_path),
        "artifacts": artifact_info,
        "reader_policy": reader_mode,
        "reader_validation_status": reader_status,
        "detected_readers": available_readers,
        "warnings": warnings,
        "issues": issues,
    }
    return issues, report


def main() -> None:
    args = parse_args()
    book_root = (Path(args.book_root) if args.book_root else DEFAULT_BOOK_ROOT).resolve()
    try:
        _contract_file, contract = load_contract(book_root)
        if args.command == "configure-contract":
            configure_contract(book_root, args)
            return
        if args.command == "lock-contract":
            lock_contract(book_root, args)
            return
        if args.command == "discover-proper-nouns":
            discover_proper_nouns(book_root, contract)
            return
        if args.command == "build-proper-noun-ledger":
            build_proper_noun_ledger(book_root, contract)
            return
        if args.command == "lock-proper-noun-discovery":
            lock_proper_noun_discovery(book_root, contract, args.review_record)
            return
        if args.command == "validate-contract":
            issues = validate_contract(book_root, contract)
            if issues:
                raise SystemExit("translation contract FAIL:\n- " + "\n- ".join(issues))
            print("translation contract PASS")
            return
        if args.command == "init-units":
            init_units(book_root, contract, args.discard_existing_targets)
            return
        if args.command == "refresh-derived":
            refresh_derived(book_root, contract, args.promote_initial)
            return
        if args.command == "render-proper-nouns":
            render_proper_nouns(book_root, contract)
            return
        if args.command == "create-chapter-patch":
            create_chapter_patch(book_root, contract, args)
            return
        if args.command == "merge-chapter-patch":
            merge_chapter_patch(book_root, contract, args.input)
            return
        if args.command == "migrate-legacy":
            migrate_legacy(book_root, contract, args.report, args.apply, args.owner_run_id)
            return
        if args.command == "rollback-generation":
            rollback_generation(book_root, contract, args.generation_id, args.reason)
            return
        if args.command == "validate":
            issues, report = validate_units(book_root, contract, args.allow_incomplete, args.require_semantic_audit)
            if args.write_report:
                write_json(book_root / "output" / "translation_unit_check.json", report)
            if issues:
                raise SystemExit("translation unit gate FAIL:\n- " + "\n- ".join(issues[:100]))
            print(f"translation unit structural PASS; semantic={report['semantic_audit_status']} units={report['unit_count']}")
            return
        if args.command == "materialize":
            materialize(book_root, contract)
            return
        if args.command == "export-xliff":
            export_xliff(book_root, contract, args.output)
            return
        if args.command == "import-xliff":
            import_xliff(book_root, contract, args.input)
            return
        if args.command == "prepare-audit":
            prepare_audit(book_root, contract, args.reviewer, args.model, args.run_id, args.chapter)
            return
        if args.command == "validate-audit":
            _manifest_path, store_path = unit_paths(book_root, contract)
            chapter = resolve_audit_chapter(read_units(store_path), args.chapter)
            run_path, _run_manifest = current_audit_run(book_root, contract, chapter)
            completion_path = run_path / "completion_manifest.json"
            issues, report = validate_audits(
                book_root,
                contract,
                require_seal=completion_path.is_file(),
                chapter=chapter,
            )
            if not issues and not completion_path.is_file():
                seal_audit_run(book_root, contract, chapter)
                issues, report = validate_audits(book_root, contract, require_seal=True, chapter=chapter)
            if not issues:
                validate_audits(book_root, contract, require_seal=True)
            if args.write_report:
                write_json(book_root / "output" / "translation_unit_semantic_audit_check.json", report)
            if issues:
                raise SystemExit("semantic audit evidence gate FAIL:\n- " + "\n- ".join(issues[:100]))
            print(f"semantic audit evidence PASS: units={report['unit_count']} chapters={report['chapter_count']}")
            return
        if args.command == "verify-artifacts":
            reader_policy = "required" if args.require_reader else ("if_available" if args.reader_if_available else "none")
            issues, report = verify_artifacts(book_root, contract, reader_policy)
            if args.write_report:
                write_json(book_root / "output" / "translation_unit_artifact_check.json", report)
            if issues:
                raise SystemExit("translation unit artifact gate FAIL:\n- " + "\n- ".join(issues[:100]))
            print("translation unit artifact PASS")
            return
    except (OSError, ValueError, json.JSONDecodeError, csv.Error, ET.ParseError) as exc:
        raise SystemExit(str(exc)) from exc


if __name__ == "__main__":
    main()
