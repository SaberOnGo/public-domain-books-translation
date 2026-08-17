from __future__ import annotations

import csv
import contextlib
import hashlib
import html
import importlib.util
import io
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
import zipfile
from unittest import mock
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]
SCRIPT = REPO / "template" / "epub_pipeline" / "common" / "scripts" / "translation_unit_pipeline.py"
RELEASE_SCRIPT = REPO / "template" / "epub_pipeline" / "common" / "scripts" / "create_release.py"
COMMON = REPO / "template" / "epub_pipeline" / "common"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


class TranslationUnitPipelineTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory(dir=REPO / "books")
        self.book = Path(self.temp.name)
        for relative in (
            "state/translation_contract.json",
            "glossary/proper_nouns.csv",
            "glossary/proper_noun_manual_candidates.csv",
            "glossary/proper_noun_candidates.csv",
            "glossary/proper_noun_occurrences.csv",
            "glossary/proper_noun_discovery_manifest.json",
            "glossary/proper_noun_manual_review.json",
        ):
            source = COMMON / relative
            target = self.book / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source, target)
        shutil.copytree(
            COMMON / "references" / "xliff-2.1-schemas",
            self.book / "references" / "xliff-2.1-schemas",
        )
        (self.book / "glossary" / "terms.csv").write_text("source_term,target_term,status\n", encoding="utf-8")
        (self.book / "chapters" / "src").mkdir(parents=True)
        (self.book / "chapters" / "src" / "001.md").write_text(
            "# 1\n\nNero used **power** in Rome. He governed for many years.\n",
            encoding="utf-8",
        )

    def tearDown(self) -> None:
        self.temp.cleanup()

    def run_cli(self, *args: str, ok: bool = True, env: dict[str, str] | None = None) -> subprocess.CompletedProcess[str]:
        result = subprocess.run(
            [sys.executable, str(SCRIPT), "--book-root", str(self.book), *args],
            text=True,
            encoding="utf-8",
            capture_output=True,
            check=False,
            env=env,
        )
        if ok and result.returncode:
            self.fail(f"command failed: {args}\nstdout={result.stdout}\nstderr={result.stderr}")
        if not ok and result.returncode == 0:
            self.fail(f"command unexpectedly passed: {args}\nstdout={result.stdout}")
        return result

    def configure_and_initialize(self) -> None:
        self.run_cli(
            "configure-contract",
            "--source-language", "en",
            "--target-language", "zh-Hans",
            "--edition-type", "bilingual_parallel",
        )
        self.run_cli("init-units")

    def finish_preproduction(self) -> None:
        self.configure_and_initialize()
        self.run_cli("discover-proper-nouns")
        candidate_path = self.book / "glossary" / "proper_noun_candidates.csv"
        with candidate_path.open("r", encoding="utf-8-sig", newline="") as handle:
            candidates = list(csv.DictReader(handle))
        expected = {row["source_form"] for row in candidates}
        self.assertTrue({"Nero", "Rome"}.issubset(expected))
        entity_for = {form: f"entity-{form.casefold()}" for form in expected}
        for row in candidates:
            row["decision"] = "registered"
            row["entity_id"] = entity_for[row["source_form"]]
        with candidate_path.open("w", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=candidates[0].keys())
            writer.writeheader()
            writer.writerows(candidates)

        register_path = self.book / "glossary" / "proper_nouns.csv"
        with (COMMON / "glossary" / "proper_nouns.csv").open("r", encoding="utf-8-sig", newline="") as handle:
            fields = list(csv.DictReader(handle).fieldnames or [])
        targets = {"Nero": "尼禄", "Rome": "罗马"}
        rows = []
        for form in sorted(expected):
            target = targets.get(form, f"译{form}")
            rows.append({
                "entity_id": entity_for[form],
                "source_name": form,
                "target_name": target,
                "category": "proper_noun",
                "display_policy": "3",
                "first_rendering": f"{target}（{form}）",
                "subsequent_rendering": target,
                "note_required": "false",
                "repeat_original_allowed_when": "",
                "notes": "test fixture",
                "source_aliases": "",
                "target_aliases": "",
                "scope": "whole_book",
                "status": "locked",
                "chinese_gloss": target,
                "display_strategy": "target_source_then_target",
                "first_occurrence_rule": "first_body_only",
                "same_name_disambiguation": "unique source form in fixture",
            })
        with register_path.open("w", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=fields)
            writer.writeheader()
            writer.writerows(rows)

        self.run_cli("build-proper-noun-ledger")
        contract = json.loads((self.book / "state" / "translation_contract.json").read_text(encoding="utf-8"))
        manifest_path = self.book / contract["canonical_units"]["manifest"]
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        source_files = sorted((self.book / "chapters" / "src").glob("*.md"))
        source_records = [
            {"path": path.relative_to(self.book).as_posix(), "sha256": sha256(path), "status": "SCANNED"}
            for path in source_files
        ]
        corpus_digest = hashlib.sha256(
            json.dumps(
                [{"path": row["path"], "sha256": row["sha256"]} for row in source_records],
                ensure_ascii=False,
                sort_keys=True,
                separators=(",", ":"),
            ).encode("utf-8")
        ).hexdigest()
        review = {
            "schema_version": "1.0",
            "status": "PASS",
            "reviewer": "independent-test-reviewer",
            "reviewed_at": "2026-08-16T00:00:00Z",
            "source_corpus_sha256": corpus_digest,
            "reviewed_files": [row["path"] for row in source_records],
            "candidate_table_sha256": sha256(candidate_path),
            "manual_candidates_sha256": sha256(self.book / "glossary" / "proper_noun_manual_candidates.csv"),
            "proper_nouns_sha256": sha256(register_path),
            "occurrence_ledger_sha256": sha256(self.book / "glossary" / "proper_noun_occurrences.csv"),
            "unresolved_candidates": 0,
            "unresolved_occurrences": 0,
            "review_summary": f"Reviewed all {manifest['unit_count']} source units and resolved all candidates.",
        }
        (self.book / "glossary" / "proper_noun_manual_review.json").write_text(
            json.dumps(review, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
        self.run_cli("lock-proper-noun-discovery")
        self.run_cli("lock-contract")
        self.run_cli("init-units")

    def units(self) -> list[dict]:
        contract = json.loads((self.book / "state" / "translation_contract.json").read_text(encoding="utf-8"))
        manifest = json.loads((self.book / contract["canonical_units"]["manifest"]).read_text(encoding="utf-8"))
        store = self.book / manifest["unit_store"]
        return [json.loads(line) for line in store.read_text(encoding="utf-8").splitlines() if line.strip()]

    def translate_all_with_patch(self, owner: str = "worker-1") -> None:
        updates = []
        for unit in self.units():
            if unit["unit_type"] == "heading":
                target = "第一章"
            else:
                target = "{{pn:entity-nero}}在{{pn:entity-rome}}运用**权力**。他治理了许多年。"
            updates.append({"unit_id": unit["unit_id"], "target_template": target, "target_state": "translated"})
        updates_path = self.book / "translation_units" / f"updates-{owner}.json"
        updates_path.parent.mkdir(parents=True, exist_ok=True)
        updates_path.write_text(json.dumps(updates, ensure_ascii=False), encoding="utf-8")
        patch_path = self.book / "translation_units" / f"patch-{owner}.json"
        self.run_cli(
            "create-chapter-patch", "--chapter", "001",
            "--updates", updates_path.relative_to(self.book).as_posix(),
            "--output", patch_path.relative_to(self.book).as_posix(),
            "--owner-run-id", owner,
        )
        self.run_cli("merge-chapter-patch", "--input", patch_path.relative_to(self.book).as_posix())

    def add_second_chapter(self) -> None:
        (self.book / "chapters" / "src" / "002.md").write_text(
            "# 2\n\nNero returned to Rome. He addressed the senate.\n",
            encoding="utf-8",
        )

    def create_patch_for_chapter(self, chapter: str, owner: str) -> str:
        updates = []
        for unit in self.units():
            if unit["chapter_id"] != chapter:
                continue
            template = (
                f"第{chapter}章"
                if unit["unit_type"] == "heading"
                else "{{pn:entity-nero}}回到{{pn:entity-rome}}并发表演说。"
            )
            updates.append({
                "unit_id": unit["unit_id"],
                "target_template": template,
                "target_state": "translated",
            })
        updates_path = self.book / "translation_units" / f"updates-{owner}.json"
        updates_path.parent.mkdir(parents=True, exist_ok=True)
        updates_path.write_text(json.dumps(updates, ensure_ascii=False), encoding="utf-8")
        patch_relative = f"translation_units/{owner}-patch.json"
        self.run_cli(
            "create-chapter-patch", "--chapter", chapter,
            "--updates", updates_path.relative_to(self.book).as_posix(),
            "--output", patch_relative,
            "--owner-run-id", owner,
        )
        return patch_relative

    def write_passing_chapter_audit(self, run_id: str) -> Path:
        run_root = self.book / "qa" / "translation_units" / "audit_runs" / run_id
        manifest = json.loads((run_root / "run_manifest.json").read_text(encoding="utf-8"))
        queue = {
            item["unit_id"]: item
            for item in (
                json.loads(line)
                for line in (run_root / "queue.jsonl").read_text(encoding="utf-8").splitlines()
                if line.strip()
            )
        }
        chapter = manifest["chapter_id"]
        chapter_units = [unit for unit in self.units() if unit["chapter_id"] == chapter]
        for unit in chapter_units:
            queue_item = queue[unit["unit_id"]]
            audit = {
                "status": "PASS",
                "unit_id": unit["unit_id"],
                "source_sha256": unit["source_sha256"],
                "target_sha256": unit["target_sha256"],
                "contract_sha256": unit["contract_sha256"],
                "proper_noun_revision": unit["proper_noun_revision"],
                "occurrence_ledger_revision": unit["occurrence_ledger_revision"],
                "terminology_revision": unit["terminology_revision"],
                "run_id": manifest["run_id"],
                "reviewer": manifest["reviewer"],
                "model": manifest["model"],
                "rubric_version": manifest["rubric_version"],
                "batch_id": queue_item["batch_id"],
                "attempt": 1,
                "input_tokens": 100,
                "output_tokens": 50,
                "checks": {
                    check: {"status": "PASS", "evidence": f"Reviewed {check} against source and target."}
                    for check in queue_item["required_checks"]
                },
                "findings": [],
                "review_summary": "Complete bidirectional semantic comparison passed.",
                "reviewed_at": "2026-08-16T00:00:00Z",
            }
            safe_id = hashlib.sha256(unit["unit_id"].encode("utf-8")).hexdigest()[:20]
            (run_root / "unit_audits" / f"{safe_id}.json").write_text(
                json.dumps(audit, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
            )
        chapter_review = {
            "status": "PASS",
            "scope": "FULL_CHAPTER",
            "issues_found": 0,
            "fixes_applied": 0,
            "unresolved_blocking_issues": 0,
            "chapter_digest": manifest["chapter_digest"],
            "reviewed_unit_ids": [unit["unit_id"] for unit in chapter_units],
            "run_id": manifest["run_id"],
            "reviewer": manifest["reviewer"],
            "model": manifest["model"],
            "rubric_version": manifest["rubric_version"],
            "findings": [],
            "reviewed_at": "2026-08-16T00:00:00Z",
            "review_summary": "Reviewed the complete chapter in canonical order with zero findings.",
        }
        (run_root / "chapter_reviews" / f"{chapter}.json").write_text(
            json.dumps(chapter_review, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
        return run_root

    def write_epub_fixture(
        self,
        kind: str,
        *,
        non_adjacent: bool = False,
        hidden_target: bool = False,
        hidden_ancestor: bool = False,
        extra_text: bool = False,
        bad_navigation: bool = False,
    ) -> Path:
        units = self.units()
        manifest = json.loads((self.book / "output" / "translation_unit_manifest.json").read_text(encoding="utf-8"))
        blocks = []
        for unit in units:
            source = html.escape(unit["source_text"].replace("**", "").replace("__", ""))
            target = html.escape(unit["target_text"].replace("**", "").replace("__", ""))
            attrs = (
                f'data-source-sha256="{unit["source_sha256"]}" '
                f'data-target-sha256="{unit["target_sha256"]}"'
            )
            if kind == "target_only":
                tag = "h1" if unit["unit_type"] == "heading" else "p"
                blocks.append(f'<{tag} data-unit-id="{unit["unit_id"]}" {attrs}>{target}</{tag}>')
            else:
                source_node = f'<p class="bitext-source">{source}</p>'
                target_node = f'<p class="bitext-target">{target}</p>'
                children = target_node + source_node if non_adjacent else source_node + target_node
                blocks.append(
                    f'<section class="bitext-unit" data-align-id="{unit["unit_id"]}" {attrs}>{children}</section>'
                )
        css = ".bitext-target { display: none; }" if hidden_target else ".bitext-target { display: block; }"
        if hidden_ancestor:
            css += "\n.chapter-content { visibility: hidden; }"
        rogue = "<p>Unregistered reader text.</p>" if extra_text else ""
        body_content = "".join(blocks) + rogue
        if hidden_ancestor:
            body_content = f'<main class="chapter-content">{body_content}</main>'
        xhtml = (
            '<?xml version="1.0" encoding="utf-8"?>'
            '<html xmlns="http://www.w3.org/1999/xhtml"><head><title>Fixture</title>'
            '<link rel="stylesheet" href="style.css"/></head><body>' + body_content + "</body></html>"
        )
        opf = (
            '<?xml version="1.0" encoding="utf-8"?>'
            '<package xmlns="http://www.idpf.org/2007/opf" version="3.0"><manifest>'
            '<item id="content" href="content.xhtml" media-type="application/xhtml+xml"/>'
            '<item id="nav" href="nav.xhtml" media-type="application/xhtml+xml" properties="nav"/>'
            '<item id="css" href="style.css" media-type="text/css"/>'
            '<item id="units" href="translation-unit-manifest.json" media-type="application/json"/>'
            '</manifest><spine><itemref idref="content"/></spine></package>'
        )
        nav_target = "missing.xhtml" if bad_navigation else "content.xhtml"
        nav = (
            '<?xml version="1.0" encoding="utf-8"?>'
            '<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops">'
            '<head><title>Contents</title></head><body><nav epub:type="toc"><ol>'
            f'<li><a href="{nav_target}">Fixture</a></li>'
            '</ol></nav></body></html>'
        )
        container = (
            '<?xml version="1.0" encoding="utf-8"?>'
            '<container xmlns="urn:oasis:names:tc:opendocument:xmlns:container" version="1.0">'
            '<rootfiles><rootfile full-path="EPUB/package.opf" media-type="application/oebps-package+xml"/>'
            '</rootfiles></container>'
        )
        output = self.book / "output"
        output.mkdir(parents=True, exist_ok=True)
        epub = output / ("book.epub" if kind == "target_only" else "book_bilingual_parallel.epub")
        with zipfile.ZipFile(epub, "w", compression=zipfile.ZIP_DEFLATED) as archive:
            archive.writestr("META-INF/container.xml", container)
            archive.writestr("EPUB/package.opf", opf)
            archive.writestr("EPUB/content.xhtml", xhtml)
            archive.writestr("EPUB/nav.xhtml", nav)
            archive.writestr("EPUB/style.css", css)
            archive.writestr("EPUB/translation-unit-manifest.json", json.dumps(manifest))
        state = {
            "edition_type": "bilingual_parallel",
            "output_editions": [
                {"edition_type": "target_only", "enabled": True, "artifact": "output/book.epub"},
                {"edition_type": "bilingual_parallel", "enabled": True, "artifact": "output/book_bilingual_parallel.epub"},
            ],
        }
        state_path = self.book / "state" / "pipeline_state.json"
        state_path.write_text(json.dumps(state), encoding="utf-8")
        return epub

    def test_default_policy_three_is_recorded_and_full_pipeline_materializes_identically(self) -> None:
        self.finish_preproduction()
        contract = json.loads((self.book / "state" / "translation_contract.json").read_text(encoding="utf-8"))
        self.assertEqual("3", contract["proper_nouns"]["policy_code"])
        self.assertEqual("default", contract["proper_nouns"]["selection_source"])
        self.translate_all_with_patch()
        self.run_cli("validate")
        self.run_cli("materialize")
        translated = (self.book / "chapters" / "translated" / "001.md").read_text(encoding="utf-8")
        final = (self.book / "chapters" / "final" / "001.md").read_text(encoding="utf-8")
        self.assertEqual(translated, final)
        self.assertIn("source-sha256:", final)
        self.assertIn("target-sha256:", final)
        (self.book / "chapters" / "translated" / "stale.md").write_text("stale", encoding="utf-8")
        (self.book / "chapters" / "final" / "stale.md").write_text("stale", encoding="utf-8")
        self.run_cli("materialize")
        self.assertFalse((self.book / "chapters" / "translated" / "stale.md").exists())
        self.assertFalse((self.book / "chapters" / "final" / "stale.md").exists())

    def test_contract_rejects_incomplete_translation_and_invalid_segment_bounds(self) -> None:
        self.run_cli(
            "configure-contract",
            "--source-language", "en",
            "--target-language", "zh-Hans",
            "--edition-type", "bilingual_parallel",
        )
        contract = json.loads((self.book / "state" / "translation_contract.json").read_text(encoding="utf-8"))
        contract["status"] = "LOCKED"
        contract["bilingual"]["complete_translation_required"] = False
        contract["bilingual"]["preferred_source_words_min"] = 160
        contract["bilingual"]["preferred_source_words_max"] = 60

        spec = importlib.util.spec_from_file_location("lifebook_translation_unit_pipeline_contract_test", SCRIPT)
        assert spec and spec.loader
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        issues = module.validate_contract(self.book, contract)

        self.assertIn("bilingual.complete_translation_required must be true", issues)
        self.assertIn("bilingual preferred source word bounds must be positive and max >= min", issues)

    def test_nonempty_initial_target_cannot_enter_canonical_projection(self) -> None:
        self.finish_preproduction()
        updates = []
        for unit in self.units():
            template = "第一章" if unit["unit_type"] == "heading" else "{{pn:entity-nero}}在{{pn:entity-rome}}治理。"
            updates.append({
                "unit_id": unit["unit_id"],
                "target_template": template,
                "target_state": "initial",
            })
        updates_path = self.book / "translation_units" / "updates-initial-state-worker.json"
        updates_path.write_text(json.dumps(updates, ensure_ascii=False), encoding="utf-8")
        result = self.run_cli(
            "create-chapter-patch", "--chapter", "001",
            "--updates", updates_path.relative_to(self.book).as_posix(),
            "--output", "translation_units/patch-initial-state-worker.json",
            "--owner-run-id", "initial-state-worker",
            ok=False,
        )
        output = result.stdout + result.stderr
        self.assertIn("requires non-empty target_template and eligible state", output)

    def test_persistent_ids_survive_insertion_before_existing_units(self) -> None:
        self.configure_and_initialize()
        before = {unit["source_text"]: unit["unit_id"] for unit in self.units()}
        chapter = self.book / "chapters" / "src" / "001.md"
        chapter.write_text("# 1\n\nA newly inserted paragraph.\n\nNero used **power** in Rome. He governed for many years.\n", encoding="utf-8")
        self.run_cli("init-units")
        after = {unit["source_text"]: unit["unit_id"] for unit in self.units()}
        for text, unit_id in before.items():
            self.assertEqual(unit_id, after[text])

    def test_stale_parallel_patch_is_rejected(self) -> None:
        self.finish_preproduction()
        unit = next(item for item in self.units() if item["unit_type"] != "heading")
        for owner in ("worker-a", "worker-b"):
            updates = self.book / "translation_units" / f"{owner}.json"
            updates.write_text(json.dumps([{
                "unit_id": unit["unit_id"],
                "target_template": f"{{{{pn:entity-nero}}}}在{{{{pn:entity-rome}}}}翻译自 {owner}。",
                "target_state": "translated",
            }], ensure_ascii=False), encoding="utf-8")
            self.run_cli(
                "create-chapter-patch", "--chapter", "001",
                "--updates", updates.relative_to(self.book).as_posix(),
                "--output", f"translation_units/{owner}-patch.json",
                "--owner-run-id", owner,
            )
        self.run_cli("merge-chapter-patch", "--input", "translation_units/worker-a-patch.json")
        failed = self.run_cli("merge-chapter-patch", "--input", "translation_units/worker-b-patch.json", ok=False)
        self.assertIn("PATCH_CONFLICT", failed.stderr + failed.stdout)

    def test_disjoint_chapter_patches_from_same_manifest_both_merge(self) -> None:
        self.add_second_chapter()
        self.finish_preproduction()
        first_patch = self.create_patch_for_chapter("001", "chapter-001-worker")
        second_patch = self.create_patch_for_chapter("002", "chapter-002-worker")

        self.run_cli("merge-chapter-patch", "--input", first_patch)
        self.run_cli("merge-chapter-patch", "--input", second_patch)

        translated = {unit["chapter_id"] for unit in self.units() if unit["target_text"].strip()}
        self.assertEqual({"001", "002"}, translated)

    def test_chapter_audit_survives_unrelated_merge_and_supports_distinct_reviewers(self) -> None:
        self.add_second_chapter()
        self.finish_preproduction()
        first_patch = self.create_patch_for_chapter("001", "translator-001")
        second_patch = self.create_patch_for_chapter("002", "translator-002")
        self.run_cli("merge-chapter-patch", "--input", first_patch)

        self.run_cli(
            "prepare-audit", "--chapter", "001", "--reviewer", "reviewer-001",
            "--model", "audit-model-a", "--run-id", "audit-001",
        )
        first_run = self.write_passing_chapter_audit("audit-001")
        self.run_cli("validate-audit", "--chapter", "001")
        self.assertTrue((first_run / "completion_manifest.json").is_file())

        self.run_cli("merge-chapter-patch", "--input", second_patch)
        self.run_cli("validate-audit", "--chapter", "001")

        self.run_cli(
            "prepare-audit", "--chapter", "002", "--reviewer", "reviewer-002",
            "--model", "audit-model-b", "--run-id", "audit-002",
        )
        self.write_passing_chapter_audit("audit-002")
        self.run_cli("validate-audit", "--chapter", "002")
        self.run_cli("validate", "--require-semantic-audit")

        completion = json.loads(
            (self.book / "qa" / "translation_units" / "audit_runs" / "book_completion_manifest.json").read_text(
                encoding="utf-8"
            )
        )
        self.assertEqual(["001", "002"], [item["chapter_id"] for item in completion["chapters"]])
        self.assertEqual({"reviewer-001", "reviewer-002"}, {item["reviewer"] for item in completion["chapters"]})

    def test_chapter_reviewer_cannot_be_its_translation_owner(self) -> None:
        self.finish_preproduction()
        patch = self.create_patch_for_chapter("001", "same-worker")
        self.run_cli("merge-chapter-patch", "--input", patch)

        failed = self.run_cli(
            "prepare-audit", "--chapter", "001", "--reviewer", "same-worker",
            "--model", "audit-model", "--run-id", "self-review", ok=False,
        )
        self.assertIn("AUDIT_INDEPENDENCE_VIOLATION", failed.stderr + failed.stdout)

    def test_chapter_audit_requires_translation_owner_evidence(self) -> None:
        self.finish_preproduction()
        self.translate_all_with_patch("traceable-worker")
        contract = json.loads((self.book / "state" / "translation_contract.json").read_text(encoding="utf-8"))
        manifest = json.loads((self.book / contract["canonical_units"]["manifest"]).read_text(encoding="utf-8"))
        store = self.book / manifest["unit_store"]
        units = [json.loads(line) for line in store.read_text(encoding="utf-8").splitlines() if line.strip()]
        units[0]["translator_run_id"] = ""
        store.write_text(
            "".join(json.dumps(unit, ensure_ascii=False, sort_keys=True) + "\n" for unit in units),
            encoding="utf-8",
        )

        failed = self.run_cli(
            "prepare-audit", "--chapter", "001", "--reviewer", "independent-reviewer",
            "--model", "audit-model", "--run-id", "missing-owner", ok=False,
        )
        self.assertIn("AUDIT_INDEPENDENCE_UNPROVABLE", failed.stderr + failed.stdout)

    def test_xliff_roundtrip_preserves_inline_and_rejects_source_tampering(self) -> None:
        self.finish_preproduction()
        self.translate_all_with_patch()
        self.run_cli("export-xliff")
        xliff = self.book / "translation_units" / "exchange.xlf"
        exported = xliff.read_text(encoding="utf-8")
        self.assertIn("<pc", exported)
        self.assertIn("<originalData>", exported)
        self.run_cli("import-xliff")
        tampered = exported.replace("power", "force", 1)
        xliff.write_text(tampered, encoding="utf-8")
        failed = self.run_cli("import-xliff", ok=False)
        self.assertIn("XLIFF_SOURCE_OR_INLINE_CHANGED", failed.stderr + failed.stdout)

    def test_relocking_terms_cannot_wash_old_target_revision(self) -> None:
        self.finish_preproduction()
        self.translate_all_with_patch()
        before = self.units()
        old_revision = before[0]["terminology_revision"]
        with (self.book / "glossary" / "terms.csv").open("a", encoding="utf-8") as handle:
            handle.write("empire,帝国,locked\n")
        self.run_cli("lock-contract")
        self.run_cli("refresh-derived")
        after = self.units()
        self.assertTrue(all(unit["target_state"] == "needs_retranslation" for unit in after))
        self.assertTrue(all(unit["terminology_revision"] == old_revision for unit in after))
        failed = self.run_cli("validate", ok=False)
        self.assertIn("STALE_TARGET_REVISION", failed.stderr + failed.stdout)

    def test_same_name_entities_require_locked_disambiguation(self) -> None:
        self.finish_preproduction()
        register = self.book / "glossary" / "proper_nouns.csv"
        with register.open("r", encoding="utf-8-sig", newline="") as handle:
            rows = list(csv.DictReader(handle))
            fields = list(rows[0].keys())
        nero = next(row for row in rows if row["source_name"] == "Nero")
        duplicate = dict(nero)
        duplicate["entity_id"] = "entity-nero-other"
        duplicate["same_name_disambiguation"] = ""
        rows.append(duplicate)
        with register.open("w", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=fields)
            writer.writeheader()
            writer.writerows(rows)
        failed = self.run_cli("lock-contract", ok=False)
        self.assertIn("ENTITY_DISAMBIGUATION_FAILED", failed.stderr + failed.stdout)

    def test_nested_proper_name_forms_use_longest_non_overlapping_spans(self) -> None:
        spec = importlib.util.spec_from_file_location("lifebook_translation_unit_pipeline_names_test", SCRIPT)
        self.assertIsNotNone(spec)
        self.assertIsNotNone(spec.loader)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        self.assertEqual(
            [(0, 13, "Julius Caesar"), (18, 24, "Caesar")],
            module.find_form_occurrences("Julius Caesar met Caesar", {"Julius Caesar", "Caesar"}),
        )

    def test_poisoned_sentence_level_unit_split_is_rejected(self) -> None:
        self.finish_preproduction()
        self.translate_all_with_patch()
        contract = json.loads((self.book / "state" / "translation_contract.json").read_text(encoding="utf-8"))
        manifest = json.loads((self.book / contract["canonical_units"]["manifest"]).read_text(encoding="utf-8"))
        store = self.book / manifest["unit_store"]
        units = self.units()
        poisoned = dict(next(unit for unit in units if unit["unit_type"] == "body"))
        poisoned["unit_id"] = "unit-poisoned-sentence-split"
        poisoned["global_order"] = len(units) + 1
        units.append(poisoned)
        store.write_text(
            "".join(json.dumps(unit, ensure_ascii=False, sort_keys=True) + "\n" for unit in units),
            encoding="utf-8",
        )
        failed = self.run_cli("validate", ok=False)
        self.assertIn("SENTENCE_OVERSEGMENTED", failed.stderr + failed.stdout)

    def test_empty_or_forged_name_discovery_cannot_be_locked(self) -> None:
        self.configure_and_initialize()
        forged = {
            "schema_version": "1.0",
            "status": "PASS",
            "reviewer": "forged-reviewer",
            "reviewed_at": "2026-08-16T00:00:00Z",
            "source_corpus_sha256": "0" * 64,
            "reviewed_files": [],
            "candidate_table_sha256": "0" * 64,
            "manual_candidates_sha256": "0" * 64,
            "proper_nouns_sha256": "0" * 64,
            "occurrence_ledger_sha256": "0" * 64,
            "unresolved_candidates": 0,
            "unresolved_occurrences": 0,
            "review_summary": "Forged empty review.",
        }
        review_path = self.book / "glossary" / "proper_noun_manual_review.json"
        review_path.write_text(json.dumps(forged, indent=2) + "\n", encoding="utf-8")
        failed = self.run_cli("lock-proper-noun-discovery", ok=False)
        self.assertIn("DISCOVERY_EVIDENCE_MISSING", failed.stderr + failed.stdout)

    def test_user_policy_four_and_non_latin_manual_candidates_are_preserved(self) -> None:
        chapter = self.book / "chapters" / "src" / "001.md"
        chapter.write_text("# 1\n\n清少纳言 wrote the passage.\n", encoding="utf-8")
        manual = self.book / "glossary" / "proper_noun_manual_candidates.csv"
        manual.write_text(
            "source_form,files,notes\n清少纳言,chapters/src/001.md,non-Latin manual discovery fixture\n",
            encoding="utf-8",
        )
        self.run_cli(
            "configure-contract",
            "--source-language", "ja", "--target-language", "zh-Hans",
            "--edition-type", "bilingual_parallel",
            "--proper-noun-policy", "4", "--decision-id", "user-policy-four",
        )
        self.run_cli("init-units")
        self.run_cli("discover-proper-nouns")
        contract = json.loads((self.book / "state" / "translation_contract.json").read_text(encoding="utf-8"))
        self.assertEqual("4", contract["proper_nouns"]["policy_code"])
        self.assertEqual("user", contract["proper_nouns"]["selection_source"])
        with (self.book / "glossary" / "proper_noun_candidates.csv").open("r", encoding="utf-8-sig") as handle:
            forms = {row["source_form"] for row in csv.DictReader(handle)}
        self.assertIn("清少纳言", forms)

    def test_translator_cannot_bypass_csv_with_direct_locked_name(self) -> None:
        self.finish_preproduction()
        updates = []
        for unit in self.units():
            template = "第一章" if unit["unit_type"] == "heading" else "尼禄在{{pn:entity-rome}}治理。"
            updates.append({"unit_id": unit["unit_id"], "target_template": template, "target_state": "translated"})
        updates_path = self.book / "translation_units" / "direct-name-updates.json"
        updates_path.parent.mkdir(parents=True, exist_ok=True)
        updates_path.write_text(json.dumps(updates, ensure_ascii=False), encoding="utf-8")
        self.run_cli(
            "create-chapter-patch", "--chapter", "001",
            "--updates", updates_path.relative_to(self.book).as_posix(),
            "--output", "translation_units/direct-name-patch.json",
            "--owner-run-id", "direct-name-worker",
        )
        failed = self.run_cli("merge-chapter-patch", "--input", "translation_units/direct-name-patch.json", ok=False)
        combined = failed.stderr + failed.stdout
        self.assertIn("ENTITY_OCCURRENCE_COVERAGE_FAILED", combined)

    def test_scalar_semantic_pass_cannot_satisfy_audit_gate(self) -> None:
        self.finish_preproduction()
        self.translate_all_with_patch()
        self.run_cli("prepare-audit", "--reviewer", "audit-reviewer", "--model", "audit-model", "--run-id", "poison-audit")
        run_root = self.book / "qa" / "translation_units" / "audit_runs" / "poison-audit"
        manifest = json.loads((run_root / "run_manifest.json").read_text(encoding="utf-8"))
        for unit in self.units():
            audit = {
                "status": "PASS",
                "unit_id": unit["unit_id"],
                "source_sha256": unit["source_sha256"],
                "target_sha256": unit["target_sha256"],
                "contract_sha256": unit["contract_sha256"],
                "proper_noun_revision": unit["proper_noun_revision"],
                "occurrence_ledger_revision": unit["occurrence_ledger_revision"],
                "terminology_revision": unit["terminology_revision"],
                "run_id": manifest["run_id"],
                "reviewer": manifest["reviewer"],
                "model": manifest["model"],
                "rubric_version": manifest["rubric_version"],
                "checks": {
                    "source_to_target_omission": "PASS",
                    "target_to_source_addition": "PASS",
                    "neighbor_boundary_contamination": "PASS",
                    "numbers_names_negation_notes": "PASS",
                },
                "findings": [],
                "review_summary": "Poisoned scalar PASS fixture.",
            }
            safe_id = hashlib.sha256(unit["unit_id"].encode("utf-8")).hexdigest()[:20]
            path = run_root / "unit_audits" / f"{safe_id}.json"
            path.write_text(json.dumps(audit, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        chapter_units = self.units()
        chapter_review = {
            "status": "PASS",
            "scope": "FULL_CHAPTER",
            "issues_found": 0,
            "fixes_applied": 0,
            "unresolved_blocking_issues": 0,
            "chapter_digest": manifest["chapter_digests"]["001"],
            "reviewed_unit_ids": [unit["unit_id"] for unit in chapter_units],
            "run_id": manifest["run_id"],
            "reviewer": manifest["reviewer"],
            "findings": [],
        }
        (run_root / "chapter_reviews" / "001.json").write_text(
            json.dumps(chapter_review, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
        failed = self.run_cli("validate-audit", ok=False)
        self.assertIn("SEMANTIC_OMISSION", failed.stderr + failed.stdout)
        self.assertIn("NEIGHBOR_CONTAMINATION", failed.stderr + failed.stdout)

    def test_structured_semantic_audit_is_sealed_and_tampering_is_rejected(self) -> None:
        self.finish_preproduction()
        self.translate_all_with_patch()
        self.run_cli(
            "prepare-audit", "--reviewer", "audit-reviewer", "--model", "audit-model",
            "--run-id", "valid-audit",
        )
        run_root = self.book / "qa" / "translation_units" / "audit_runs" / "valid-audit"
        manifest = json.loads((run_root / "run_manifest.json").read_text(encoding="utf-8"))
        queue = {
            item["unit_id"]: item
            for item in (
                json.loads(line)
                for line in (run_root / "queue.jsonl").read_text(encoding="utf-8").splitlines()
                if line.strip()
            )
        }
        audit_paths = []
        for unit in self.units():
            queue_item = queue[unit["unit_id"]]
            audit = {
                "status": "PASS",
                "unit_id": unit["unit_id"],
                "source_sha256": unit["source_sha256"],
                "target_sha256": unit["target_sha256"],
                "contract_sha256": unit["contract_sha256"],
                "proper_noun_revision": unit["proper_noun_revision"],
                "occurrence_ledger_revision": unit["occurrence_ledger_revision"],
                "terminology_revision": unit["terminology_revision"],
                "run_id": manifest["run_id"],
                "reviewer": manifest["reviewer"],
                "model": manifest["model"],
                "rubric_version": manifest["rubric_version"],
                "batch_id": queue_item["batch_id"],
                "attempt": 1,
                "input_tokens": 100,
                "output_tokens": 50,
                "checks": {
                    check: {"status": "PASS", "evidence": f"Reviewed {check} against source and target."}
                    for check in queue_item["required_checks"]
                },
                "findings": [],
                "review_summary": "Complete bidirectional semantic comparison passed.",
                "reviewed_at": "2026-08-16T00:00:00Z",
            }
            safe_id = hashlib.sha256(unit["unit_id"].encode("utf-8")).hexdigest()[:20]
            path = run_root / "unit_audits" / f"{safe_id}.json"
            path.write_text(json.dumps(audit, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            audit_paths.append(path)
        chapter_units = self.units()
        chapter_review = {
            "status": "PASS",
            "scope": "FULL_CHAPTER",
            "issues_found": 0,
            "fixes_applied": 0,
            "unresolved_blocking_issues": 0,
            "chapter_digest": manifest["chapter_digests"]["001"],
            "reviewed_unit_ids": [unit["unit_id"] for unit in chapter_units],
            "run_id": manifest["run_id"],
            "reviewer": manifest["reviewer"],
            "model": manifest["model"],
            "rubric_version": manifest["rubric_version"],
            "findings": [],
            "reviewed_at": "2026-08-16T00:00:00Z",
            "review_summary": "Reviewed the complete chapter in canonical order with zero findings.",
        }
        (run_root / "chapter_reviews" / "001.json").write_text(
            json.dumps(chapter_review, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
        self.run_cli("validate-audit", "--write-report")
        self.assertTrue((run_root / "completion_manifest.json").is_file())
        self.run_cli("validate", "--require-semantic-audit")

        poisoned = json.loads(audit_paths[0].read_text(encoding="utf-8"))
        poisoned["review_summary"] = "Modified after sealing."
        audit_paths[0].write_text(json.dumps(poisoned, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        failed = self.run_cli("validate-audit", ok=False)
        self.assertIn("sealed evidence is stale", failed.stderr + failed.stdout)

    def test_markdown_ast_preserves_protected_block_boundaries(self) -> None:
        chapter = self.book / "chapters" / "src" / "001.md"
        chapter.write_text(
            "---\ntitle: Fixture\n---\n\n"
            "# Heading\n\n"
            "A prose paragraph with **inline emphasis**.\n\n"
            "```python\nprint('first')\n\nprint('second')\n```\n\n"
            "| Name | Value |\n| --- | --- |\n| Nero | 1 |\n\n"
            "- first item\n  continuation\n- second item\n\n"
            "[^1]: A footnote line.\n    Continued footnote text.\n\n"
            "<div>\nHTML block\n</div>\n",
            encoding="utf-8",
        )
        self.configure_and_initialize()
        units = self.units()
        kinds = [unit["unit_type"] for unit in units]
        self.assertEqual(["heading", "body", "code", "table", "list", "note", "raw_html"], kinds)
        code = next(unit for unit in units if unit["unit_type"] == "code")
        self.assertIn("print('first')\n\nprint('second')", code["source_text"])
        self.assertFalse(any("title: Fixture" in unit["source_text"] for unit in units))

    def test_legacy_migration_is_read_only_and_blocks_rendered_name_drift(self) -> None:
        self.finish_preproduction()
        self.translate_all_with_patch()
        self.run_cli("materialize")
        contract = json.loads((self.book / "state" / "translation_contract.json").read_text(encoding="utf-8"))
        manifest_path = self.book / contract["canonical_units"]["manifest"]
        before = sha256(manifest_path)
        self.run_cli("migrate-legacy")
        report = json.loads((self.book / "output" / "legacy_migration_report.json").read_text(encoding="utf-8"))
        self.assertEqual("REVIEW_REQUIRED", report["status"])
        self.assertTrue(
            any(
                "CSV_ONLY_RENDER_REQUIRED" in issue or "ENTITY_OCCURRENCE_COVERAGE_FAILED" in issue
                for issue in report["issues"]
            ),
            report["issues"],
        )
        self.assertEqual(before, sha256(manifest_path))
        failed = self.run_cli("migrate-legacy", "--apply", "--owner-run-id", "legacy-worker", ok=False)
        self.assertIn("LEGACY_MIGRATION_BLOCKED", failed.stderr + failed.stdout)
        self.assertEqual(before, sha256(manifest_path))

    def test_rollback_restores_old_generation_as_new_auditable_generation(self) -> None:
        self.finish_preproduction()
        contract = json.loads((self.book / "state" / "translation_contract.json").read_text(encoding="utf-8"))
        manifest_path = self.book / contract["canonical_units"]["manifest"]
        untranslated_generation = json.loads(manifest_path.read_text(encoding="utf-8"))["generation_id"]
        self.translate_all_with_patch()
        translated_generation = json.loads(manifest_path.read_text(encoding="utf-8"))["generation_id"]
        self.assertNotEqual(untranslated_generation, translated_generation)
        self.run_cli(
            "rollback-generation", "--generation-id", untranslated_generation,
            "--reason", "poison-test-rollback",
        )
        restored_generation = json.loads(manifest_path.read_text(encoding="utf-8"))["generation_id"]
        self.assertNotIn(restored_generation, {untranslated_generation, translated_generation})
        self.assertTrue(all(not unit["target_text"] for unit in self.units()))

    def test_artifact_gate_rejects_non_adjacent_pairs_and_hidden_targets(self) -> None:
        self.finish_preproduction()
        self.translate_all_with_patch()
        self.run_cli("materialize")
        self.write_epub_fixture("target_only")
        self.write_epub_fixture("bilingual", non_adjacent=True)
        failed = self.run_cli("verify-artifacts", ok=False)
        self.assertIn("NON_ADJACENT_PAIR", failed.stderr + failed.stdout)
        self.write_epub_fixture("bilingual", hidden_target=True)
        failed = self.run_cli("verify-artifacts", ok=False)
        self.assertIn("TARGET_NOT_VISIBLE", failed.stderr + failed.stdout)
        self.write_epub_fixture("bilingual", hidden_ancestor=True)
        failed = self.run_cli("verify-artifacts", ok=False)
        self.assertIn("TARGET_NOT_VISIBLE", failed.stderr + failed.stdout)
        self.write_epub_fixture("bilingual", extra_text=True)
        failed = self.run_cli("verify-artifacts", ok=False)
        self.assertIn("UNREGISTERED_READER_TEXT", failed.stderr + failed.stdout)
        self.write_epub_fixture("bilingual", bad_navigation=True)
        failed = self.run_cli("verify-artifacts", ok=False)
        self.assertIn("NAVIGATION_INVALID", failed.stderr + failed.stdout)

    def test_release_reader_smoke_skips_with_disclosed_warning_when_unavailable(self) -> None:
        self.finish_preproduction()
        self.translate_all_with_patch()
        self.run_cli("materialize")
        self.write_epub_fixture("target_only")
        self.write_epub_fixture("bilingual")
        spec = importlib.util.spec_from_file_location("lifebook_translation_unit_pipeline_test", SCRIPT)
        self.assertIsNotNone(spec)
        self.assertIsNotNone(spec.loader)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        contract = json.loads((self.book / "state" / "translation_contract.json").read_text(encoding="utf-8"))
        with mock.patch.object(module, "detected_reader_apps", return_value=[]):
            issues, report = module.verify_artifacts(self.book, contract, "if_available")
        self.assertEqual([], issues)
        self.assertEqual("PASS", report["status"])
        self.assertEqual("SKIPPED_UNAVAILABLE", report["reader_validation_status"])
        self.assertTrue(any("REAL_READER_SKIPPED_UNAVAILABLE" in item for item in report["warnings"]))

    def test_available_reader_requires_hash_bound_viewports_navigation_and_screenshots(self) -> None:
        self.finish_preproduction()
        self.translate_all_with_patch()
        self.run_cli("materialize")
        target_epub = self.write_epub_fixture("target_only")
        bilingual_epub = self.write_epub_fixture("bilingual")
        spec = importlib.util.spec_from_file_location("lifebook_translation_unit_pipeline_reader_test", SCRIPT)
        self.assertIsNotNone(spec)
        self.assertIsNotNone(spec.loader)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        contract = json.loads((self.book / "state" / "translation_contract.json").read_text(encoding="utf-8"))
        manifest_path = self.book / contract["canonical_units"]["manifest"]
        screenshot_root = self.book / "qa" / "translation_units" / "reader_screenshots"
        screenshot_root.mkdir(parents=True, exist_ok=True)
        screenshots = []
        evidence_plan = [
            ("toc_jump", "phone"),
            ("chapter_start", "desktop"),
            ("ordinary_body", "phone"),
            ("bilingual_interleave", "desktop"),
        ]
        for index, (location, viewport) in enumerate(evidence_plan, start=1):
            screenshot = screenshot_root / f"{index:02d}-{location}-{viewport}.png"
            screenshot.write_bytes(b"\x89PNG\r\n\x1a\nreader-evidence-" + str(index).encode("ascii"))
            screenshots.append({
                "path": screenshot.relative_to(self.book).as_posix(),
                "sha256": sha256(screenshot),
                "location": location,
                "viewport": viewport,
            })
        reader_report = {
            "schema_version": "1.0",
            "status": "PASS",
            "canonical_manifest_sha256": sha256(manifest_path),
            "artifacts": [
                {"kind": "target_only", "epub_sha256": sha256(target_epub)},
                {"kind": "bilingual", "epub_sha256": sha256(bilingual_epub)},
            ],
            "viewports": [
                {"name": "phone", "status": "PASS"},
                {"name": "desktop", "status": "PASS"},
            ],
            "computed_style_checks": [{"selector": ".bitext-target", "status": "PASS"}],
            "navigation_checks": [{"location": "toc", "status": "PASS"}],
            "screenshots": screenshots,
            "validated_at": "2026-08-16T00:00:00Z",
            "validator": "reader-test-validator",
        }
        report_path = self.book / "qa" / "translation_units" / "reader_validation.json"
        report_path.write_text(json.dumps(reader_report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        with mock.patch.object(module, "detected_reader_apps", return_value=["Calibre ebook-viewer"]):
            issues, report = module.verify_artifacts(self.book, contract, "if_available")
        self.assertEqual([], issues)
        self.assertEqual("PASS", report["reader_validation_status"])

    def test_release_gate_rejects_epubcheck_report_bound_to_old_epub(self) -> None:
        output = self.book / "output"
        output.mkdir(parents=True, exist_ok=True)
        artifact = output / "book.epub"
        artifact.write_bytes(b"current-epub-bytes")
        (self.book / "state" / "pipeline_state.json").write_text(
            json.dumps({
                "output_editions": [
                    {"edition_type": "target_only", "enabled": True, "artifact": "output/book.epub"}
                ]
            }),
            encoding="utf-8",
        )
        (output / "epubcheck.json").write_text(
            json.dumps({
                "checker": {"nFatal": 0, "nError": 0, "nWarning": 0},
                "lifebook_evidence": {
                    "edition_type": "target_only",
                    "artifact_path": "output/book.epub",
                    "artifact_sha256": "0" * 64,
                },
            }),
            encoding="utf-8",
        )
        spec = importlib.util.spec_from_file_location("lifebook_create_release_test", RELEASE_SCRIPT)
        self.assertIsNotNone(spec)
        self.assertIsNotNone(spec.loader)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        records = module.expected_epubcheck_records(self.book)
        self.assertEqual(1, len(records))
        self.assertFalse(records[0]["hash_match"])
        summary = {
            "random_spotcheck_status": "PASS",
            "random_spotcheck_require_pass": True,
            "current_review_run_id": "current-run",
            "current_run_pass_rounds_required": 1,
            "current_run_pass_rounds_count": 1,
            "release_confidence": 0.95,
            "epubcheck_records": records,
            "translation_artifact_gate_status": "PASS",
            "translation_artifact_reader_policy": "if_available",
            "translation_artifact_reader_status": "SKIPPED_UNAVAILABLE",
            "translation_artifact_hash_match": True,
            "publication_lint_path": "output/publication_lint.json",
            "publication_lint_issue_count": 0,
            "translation_metrics_path": "output/release/translation_metrics.json",
            "translation_metrics_estimate_status": "PASS",
            "translation_metrics_actual_status": "PASS",
            "literary_style_review_path": "qa/literary_style/literary_style_review.md",
            "literary_style_status": "PASS",
            "literary_target_only_reading_score": 5,
            "literary_read_aloud_awkward_sentence_count": 0,
            "literary_unresolved_style_debt_count": 0,
            "literary_literal_explanatory_style_debt_count": 0,
            "literary_high_impact_sections_reviewed": True,
            "literary_author_preface_and_first_chapter_reviewed": True,
            "literary_source_fidelity_backcheck_after_polish": True,
        }
        output = io.StringIO()
        with contextlib.redirect_stdout(output), self.assertRaises(SystemExit):
            module.require_pass_gates(summary)
        self.assertIn("ARTIFACT_REPORT_HASH_MISMATCH", output.getvalue())

    def test_real_builders_and_epubcheck_validate_both_enabled_editions(self) -> None:
        self.finish_preproduction()
        self.translate_all_with_patch()
        self.run_cli("materialize")
        metadata = self.book / "metadata" / "book.yaml"
        metadata.parent.mkdir(parents=True, exist_ok=True)
        metadata.write_text(
            "title: Canonical Fixture\n"
            "author: Test Author\n"
            "language: zh-Hans\n"
            "identifier: urn:uuid:00000000-0000-4000-8000-000000000001\n"
            "publisher: LifeBook Test\n",
            encoding="utf-8",
        )
        state = {
            "source_language": "en",
            "target_language": "zh-Hans",
            "edition_type": "bilingual_parallel",
            "output_editions": [
                {"edition_type": "target_only", "enabled": True, "artifact": "output/book.epub"},
                {"edition_type": "bilingual_parallel", "enabled": True, "artifact": "output/book_bilingual_parallel.epub"},
            ],
            "bilingual_parallel": {
                "enabled": True,
                "alignment_map": "qa/bilingual_parallel/alignment_map.json",
            },
        }
        (self.book / "state" / "pipeline_state.json").write_text(json.dumps(state), encoding="utf-8")
        scripts = self.book / "scripts"
        scripts.mkdir(parents=True, exist_ok=True)
        for name in ("build_epub.js", "build_bilingual_epub.py", "run_epubcheck.js", "run_python.js"):
            shutil.copyfile(COMMON / "scripts" / name, scripts / name)

        commands = (
            ["node", str(scripts / "build_epub.js")],
            [sys.executable, str(scripts / "build_bilingual_epub.py")],
            ["node", str(scripts / "run_epubcheck.js"), "--all-enabled"],
        )
        for command in commands:
            result = subprocess.run(command, cwd=self.book, text=True, encoding="utf-8", capture_output=True, check=False)
            self.assertEqual(0, result.returncode, f"{command}\nstdout={result.stdout}\nstderr={result.stderr}")
        rerun = subprocess.run(commands[-1], cwd=self.book, text=True, encoding="utf-8", capture_output=True, check=False)
        self.assertEqual(0, rerun.returncode, f"EPUBCheck rerun failed\nstdout={rerun.stdout}\nstderr={rerun.stderr}")
        self.run_cli("verify-artifacts", "--write-report")
        for report_name, artifact_name in (
            ("epubcheck.json", "book.epub"),
            ("epubcheck_bilingual_parallel.json", "book_bilingual_parallel.epub"),
        ):
            report = json.loads((self.book / "output" / report_name).read_text(encoding="utf-8"))
            self.assertEqual(0, report["checker"]["nFatal"])
            self.assertEqual(0, report["checker"]["nError"])
            self.assertEqual(0, report["checker"]["nWarning"])
            self.assertEqual(sha256(self.book / "output" / artifact_name), report["lifebook_evidence"]["artifact_sha256"])


if __name__ == "__main__":
    unittest.main()
