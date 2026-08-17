from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = REPO_ROOT / "template" / "epub_pipeline" / "common" / "scripts" / "evaluate_translation_difficulty.py"
METRICS_SCRIPT_PATH = REPO_ROOT / "template" / "epub_pipeline" / "common" / "scripts" / "update_translation_metrics.py"
RELEASE_SCRIPT_PATH = REPO_ROOT / "template" / "epub_pipeline" / "common" / "scripts" / "create_release.py"


class TranslationDifficultyEvaluatorTests(unittest.TestCase):
    def make_complex_book(self, root: Path) -> Path:
        book_root = root / "books" / "zh-Hans" / "1_test_book"
        (book_root / "metadata").mkdir(parents=True)
        (book_root / "state").mkdir(parents=True)
        (book_root / "chapters" / "source").mkdir(parents=True)
        (book_root / "source" / "tables").mkdir(parents=True)
        (book_root / "assets" / "figures").mkdir(parents=True)
        (book_root / "metadata" / "book.yaml").write_text(
            "\n".join(
                [
                    'title: "历史与思想测试书"',
                    'original_title: "A Test Book of History and Ideas"',
                    'author: "Test Author"',
                ]
            )
            + "\n",
            encoding="utf-8",
        )
        (book_root / "state" / "pipeline_state.json").write_text(
            json.dumps(
                {
                    "template_root": "template/epub_pipeline/English-to-Simplified-Chinese",
                    "publication_mode": "public_domain",
                    "profile": "classical-history-zh-Hans",
                },
                ensure_ascii=False,
                indent=2,
            )
            + "\n",
            encoding="utf-8",
        )
        chapter = "\n".join(
            [
                "# Chapter 1",
                "",
                "The empire, dynasty, senate, king, treaty, chronology, and revolution shaped the archive.",
                "Plato and Aristotle debated metaphysics, ethics, causality, ontology, and epistemology.",
                "Napoleon Bonaparte, Roman Republic, Ming Dynasty, Athens, and Alexander appear repeatedly.",
                "",
                "![battle map](../../assets/figures/map.svg)",
                "",
                "| Year | Event |",
                "| --- | --- |",
                "| 1804 | Constitutional reform |",
                "",
                "$$E = mc^2$$",
                "",
                "```python",
                "def example():",
                "    return {'api': 'version-specific'}",
                "```",
                "",
                "A dense note follows.[^1]",
                "",
                "[^1]: This note explains a disputed historical interpretation and source witness.",
            ]
        )
        (book_root / "chapters" / "source" / "001.md").write_text(chapter, encoding="utf-8")
        (book_root / "source" / "tables" / "events.csv").write_text("year,event\n1804,reform\n", encoding="utf-8")
        (book_root / "assets" / "figures" / "map.svg").write_text("<svg></svg>\n", encoding="utf-8")
        return book_root

    def test_evaluator_scores_multidimensional_complexity_and_writes_metrics(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            book_root = self.make_complex_book(Path(tmp))

            result = subprocess.run(
                [sys.executable, str(SCRIPT_PATH), "--book-root", str(book_root), "--write-metrics"],
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )

            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            assessment = json.loads((book_root / "output" / "release" / "translation_difficulty_assessment.json").read_text(encoding="utf-8"))
            self.assertEqual(assessment["assessment_status"], "PASS")
            self.assertIn("history", assessment["book_complexity_profile"]["detected_book_types"])
            self.assertIn("philosophy", assessment["book_complexity_profile"]["detected_book_types"])
            self.assertGreaterEqual(assessment["book_complexity_profile"]["figures_count"], 1)
            self.assertGreaterEqual(assessment["book_complexity_profile"]["tables_count"], 2)
            self.assertGreaterEqual(assessment["book_complexity_profile"]["formula_or_code_block_count"], 2)
            self.assertGreaterEqual(assessment["difficulty_components_1_to_5"]["historical_context_load"], 3)
            self.assertGreaterEqual(assessment["difficulty_components_1_to_5"]["philosophical_or_theoretical_density"], 3)
            self.assertGreaterEqual(assessment["overall_difficulty_score_1_to_5"], 3)
            parallel = assessment["parallelization_profile"]
            self.assertGreater(parallel["weighted_source_unit_estimate"], 0)
            self.assertEqual(assessment["book_complexity_profile"]["chapter_count"], parallel["chapter_count"])
            self.assertEqual("npm run translation:orchestration:plan", parallel["next_command"])
            self.assertIn("not_page_count", parallel["planning_basis"])
            providers = {item["provider"] for item in assessment["model_recommendations"]}
            self.assertEqual({"deepseek", "gpt", "claude"}, providers)
            assessment_md = (book_root / "output" / "release" / "translation_difficulty_assessment.md").read_text(encoding="utf-8")
            self.assertIn("# 翻译难度评估", assessment_md)
            self.assertIn("## 模型建议", assessment_md)
            self.assertNotIn("# Translation Difficulty Assessment", assessment_md)

            metrics = json.loads((book_root / "output" / "release" / "translation_metrics.json").read_text(encoding="utf-8"))
            estimate = metrics["pretranslation_estimate"]
            self.assertEqual(estimate["status"], "PASS")
            self.assertEqual(estimate["book_complexity_profile"]["primary_book_type"], assessment["book_complexity_profile"]["primary_book_type"])
            self.assertEqual(estimate["difficulty_score_1_to_5"], assessment["overall_difficulty_score_1_to_5"])

    def test_evaluator_uses_publishable_historical_metrics_for_similar_books(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            book_root = self.make_complex_book(root)
            previous_root = root / "books" / "zh-Hans" / "2_previous_history"
            release = previous_root / "output" / "release"
            release.mkdir(parents=True)
            (release / "translation_metrics.json").write_text(
                json.dumps(
                    {
                        "schema_version": "1.0.0",
                        "privacy_contract": {
                            "contains_source_text": False,
                            "contains_prompt_text": False,
                            "contains_local_absolute_paths": False,
                            "publishable_to_github": True,
                        },
                        "book": {"title": "Previous History", "publication_mode": "public_domain"},
                        "pretranslation_estimate": {
                            "status": "PASS",
                            "book_complexity_profile": {
                                "primary_book_type": "history",
                                "domains": ["history", "philosophy"],
                                "source_unit_count": 10000,
                            },
                            "difficulty_score_1_to_5": 4,
                            "difficulty_level": "high",
                        },
                        "post_translation_actual": {
                            "status": "PASS",
                            "actual_active_hours": 28,
                            "actual_calendar_days": 7,
                            "actual_review_rounds": 4,
                            "actual_difficulty_score_1_to_5": 4,
                            "actual_difficulty_level": "high",
                            "total_input_tokens": 52000,
                            "total_output_tokens": 31000,
                            "models_used": [
                                {
                                    "provider": "gpt",
                                    "model_name": "example-high-tier",
                                    "model_tier": "high",
                                    "role": "final QA",
                                }
                            ],
                            "lessons_for_future_estimates": [
                                "Historical names and philosophical terms increased review time.",
                            ],
                        },
                    },
                    ensure_ascii=False,
                    indent=2,
                )
                + "\n",
                encoding="utf-8",
            )

            result = subprocess.run(
                [sys.executable, str(SCRIPT_PATH), "--book-root", str(book_root), "--write-metrics"],
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )

            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            assessment = json.loads((book_root / "output" / "release" / "translation_difficulty_assessment.json").read_text(encoding="utf-8"))
            history = assessment["historical_reference"]
            self.assertEqual(history["matched_count"], 1)
            self.assertEqual(history["similar_books"][0]["book_title"], "Previous History")
            self.assertEqual(history["similar_books"][0]["actual_active_hours"], 28)
            self.assertGreater(history["estimated_from_history"]["active_hours_per_10k_source_units"], 0)

            metrics = json.loads((book_root / "output" / "release" / "translation_metrics.json").read_text(encoding="utf-8"))
            self.assertEqual(metrics["pretranslation_estimate"]["historical_reference"]["matched_count"], 1)

    def test_metrics_validator_accepts_estimate_plus_post_translation_actuals(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            book_root = self.make_complex_book(Path(tmp))
            subprocess.run(
                [sys.executable, str(SCRIPT_PATH), "--book-root", str(book_root), "--write-metrics"],
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=True,
            )
            metrics_path = book_root / "output" / "release" / "translation_metrics.json"
            metrics = json.loads(metrics_path.read_text(encoding="utf-8"))
            metrics["post_translation_actual"] = {
                "status": "PASS",
                "started_at": "2026-06-01T00:00:00Z",
                "finished_at": "2026-06-03T00:00:00Z",
                "actual_calendar_days": 2,
                "actual_active_hours": 12,
                "actual_review_rounds": 3,
                "actual_difficulty_level": "high",
                "actual_difficulty_score_1_to_5": 4,
                "models_used": [
                    {
                        "provider": "gpt",
                        "model_name": "example-high-tier",
                        "model_tier": "high",
                        "role": "final translation and QA",
                        "input_tokens": 12000,
                        "output_tokens": 8000,
                    }
                ],
                "total_input_tokens": 12000,
                "total_output_tokens": 8000,
                "quality_scores": {
                    "random_spotcheck_average": 94,
                    "random_spotcheck_lowest": 90,
                    "release_confidence": 0.9,
                },
                "variance_against_estimate": "Actual effort stayed inside the estimated range.",
                "lessons_for_future_estimates": [
                    "Historical and philosophical density increased review time more than raw length.",
                ],
            }
            metrics_path.write_text(json.dumps(metrics, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

            result = subprocess.run(
                [
                    sys.executable,
                    str(METRICS_SCRIPT_PATH),
                    "--book-root",
                    str(book_root),
                    "--validate",
                    "--require-actual-pass",
                    "--write-report",
                ],
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )

            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            metrics_md = (book_root / "output" / "release" / "translation_metrics.md").read_text(encoding="utf-8")
            self.assertIn("# 翻译任务预估与实际统计", metrics_md)
            self.assertIn("## 翻译后实际统计", metrics_md)
            report = json.loads((book_root / "output" / "translation_metrics_check.json").read_text(encoding="utf-8"))
            self.assertEqual(report["status"], "PASS")

    def test_pass_release_rejects_missing_translation_metrics(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            book_root = self.make_complex_book(Path(tmp))
            (book_root / "output").mkdir(parents=True, exist_ok=True)
            (book_root / "output" / "book.epub").write_bytes(b"fake epub")
            (book_root / "output" / "epubcheck.json").write_text(
                json.dumps({"checker": {"nFatal": 0, "nError": 0, "nWarning": 0}}, ensure_ascii=False),
                encoding="utf-8",
            )
            (book_root / "output" / "publication_lint.json").write_text(
                json.dumps({"issues": []}, ensure_ascii=False),
                encoding="utf-8",
            )
            round_root = book_root / "reviews" / "random_spotcheck" / "round_001"
            round_root.mkdir(parents=True)
            (round_root / "validation_report.json").write_text(
                json.dumps(
                    {
                        "status": "PASS",
                        "require_pass": True,
                        "current_review_run_id": "run-test",
                        "current_run_pass_rounds_required": 1,
                        "current_run_pass_rounds_count": 1,
                        "release_confidence": 0.9,
                    },
                    ensure_ascii=False,
                    indent=2,
                ),
                encoding="utf-8",
            )

            result = subprocess.run(
                [
                    sys.executable,
                    str(RELEASE_SCRIPT_PATH),
                    "--book-root",
                    str(book_root),
                    "--status",
                    "PASS",
                    "--require-pass",
                ],
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("translation metrics", result.stdout)


if __name__ == "__main__":
    unittest.main()
