from __future__ import annotations

import subprocess
import sys
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]


class LiteraryChineseTemplateGoalTests(unittest.TestCase):
    def test_lzh_language_template_has_required_goal_files(self) -> None:
        template_root = REPO_ROOT / "template" / "epub_pipeline" / "Literary-Chinese-to-Simplified-Chinese"
        required_files = [
            "AGENTS.md",
            "SKILL.md",
            "README.md",
            "MASTER_PROMPT.md",
            "TEMPLATE_VERSION.md",
            "package.json",
            "metadata/book.yaml",
            "metadata/classical_chinese_source_profile.md",
            "metadata/source_witness_manifest.md",
            "metadata/style_profile.md",
            "glossary/style_guide.md",
            "glossary/terms.csv",
            "qa/textual/classical_chinese_textual_notes.md",
            "qa/chapter_controls/_TEMPLATE.control.md",
            "references/classical_chinese_parallel_text_policy.md",
            "references/classical_chinese_annotation_policy.md",
            "references/classical_chinese_source_notes.md",
            "references/classical_chinese_textual_criticism_policy.md",
            "references/classical_chinese_title_strategy.md",
            "references/classical_chinese_to_modern_chinese_literary_refinement.md",
            "references/quality_standard.md",
            "references/translation_research_universal.md",
            "reviews/scorecards/_TEMPLATE_random_spotcheck_score.md",
            "reviews/scorecards/_TEMPLATE_scorecard.md",
        ]
        required_files.extend(f"prompts/{number:02d}_{name}.md" for number, name in [
            (0, "orchestrator_zh_lzh"),
            (1, "ingest_clean_zh_lzh"),
            (2, "split_zh_lzh"),
            (3, "global_translation_research_zh_lzh"),
            (4, "book_specific_research_zh_lzh"),
            (5, "pretranslation_trials_zh_lzh"),
            (6, "glossary_style_zh_lzh"),
            (7, "translate_chapters_zh_lzh"),
            (8, "review_fidelity_zh_lzh"),
            (9, "review_readability_imagery_zh_lzh"),
            (10, "review_terminology_zh_lzh"),
            (11, "chapter_quality_gate_zh_lzh"),
            (12, "build_validate_zh_lzh"),
            (13, "preproduction_stage1_spec_zh_lzh"),
            (14, "preproduction_stage2_sample_zh_lzh"),
            (15, "full_book_production_zh_lzh"),
            (16, "independent_review_agents_zh_lzh"),
            (17, "revision_routing_zh_lzh"),
            (18, "final_output_zh_lzh"),
            (19, "retrospective_template_update_zh_lzh"),
        ])

        missing = [path for path in required_files if not (template_root / path).exists()]

        self.assertEqual(missing, [])

    def test_classical_history_profile_has_required_goal_files(self) -> None:
        profile_root = REPO_ROOT / "template" / "epub_pipeline" / "profiles" / "classical-history-zh-Hans"
        required_files = [
            "AGENTS.md",
            "SKILL.md",
            "README.md",
            "MASTER_PROMPT.md",
            "TEMPLATE_VERSION.md",
            "metadata/historical_context.md",
            "glossary/historical_terms.csv",
            "glossary/people_places.csv",
            "qa/historical/_TEMPLATE.chapter_historical_audit.md",
            "qa/historical/event_timeline.md",
            "qa/historical/state_relations_matrix.csv",
            "references/chronology_and_state_relations_policy.md",
            "references/classical_history_annotation_policy.md",
            "references/historical_publication_control.md",
            "references/named_entity_policy.md",
            "prompts/00_profile_integration_zh_Hans.md",
            "prompts/04a_historical_context_zh_Hans.md",
            "prompts/06a_named_entity_lock_zh_Hans.md",
            "prompts/08b_chapter_historical_audit_zh_Hans.md",
            "prompts/16b_history_random_spotcheck_zh_Hans.md",
            "reviews/scorecards/_TEMPLATE_history_scorecard.md",
        ]

        missing = [path for path in required_files if not (profile_root / path).exists()]

        self.assertEqual(missing, [])

    def test_create_book_project_dry_run_accepts_lzh_with_classical_history_profile(self) -> None:
        result = subprocess.run(
            [
                sys.executable,
                str(REPO_ROOT / "books" / "scripts" / "create_book_project.py"),
                "zhanguoce_template_smoke_delete_me",
                "--source-target",
                "Literary-Chinese-to-Simplified-Chinese",
                "--profile",
                "classical-history-zh-Hans",
                "--dry-run",
            ],
            cwd=REPO_ROOT,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertRegex(result.stdout, r"books/zh-Hans/\d+_zhanguoce_template_smoke_delete_me")

    def test_lzh_source_notes_require_multi_witness_selection(self) -> None:
        source_notes = (
            REPO_ROOT
            / "template"
            / "epub_pipeline"
            / "Literary-Chinese-to-Simplified-Chinese"
            / "references"
            / "classical_chinese_source_notes.md"
        ).read_text(encoding="utf-8")

        for required_phrase in [
            "多见证底本选择门禁",
            "不得把单一影印本、OCR、网页转写或协作标点直接升格为正式主底本",
            "为什么用这个 PDF/扫描，是否有更好的文本",
            "source_selection_report",
        ]:
            self.assertIn(required_phrase, source_notes)

    def test_common_epub_builder_preserves_lzh_parallel_html(self) -> None:
        build_script = (
            REPO_ROOT
            / "template"
            / "epub_pipeline"
            / "common"
            / "scripts"
            / "build_epub.js"
        ).read_text(encoding="utf-8")

        self.assertIn("function isRawHtmlLine", build_script)
        self.assertIn("parallel-passage", build_script)
        self.assertIn("source-text", build_script)
        self.assertIn("modern-text", build_script)

        parallel_policy = (
            REPO_ROOT
            / "template"
            / "epub_pipeline"
            / "Literary-Chinese-to-Simplified-Chinese"
            / "references"
            / "classical_chinese_parallel_text_policy.md"
        ).read_text(encoding="utf-8")
        self.assertIn("不得把它们转义成", parallel_policy)
        self.assertIn("xmlns:epub", parallel_policy)


if __name__ == "__main__":
    unittest.main()
