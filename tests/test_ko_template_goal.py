from __future__ import annotations

import subprocess
import sys
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]


class KoreanTemplateGoalTests(unittest.TestCase):
    def test_ko_language_template_has_required_goal_files(self) -> None:
        template_root = REPO_ROOT / "template" / "epub_pipeline" / "Korean-to-Simplified-Chinese"
        required_files = [
            "AGENTS.md",
            "SKILL.md",
            "README.md",
            "MASTER_PROMPT.md",
            "TEMPLATE_VERSION.md",
            "retrospective_lessons.md",
            "package.json",
            "metadata/book.yaml",
            "metadata/korean_source_profile.md",
            "metadata/style_profile.md",
            "glossary/style_guide.md",
            "glossary/terms.csv",
            "qa/textual/korean_textual_notes.md",
            "qa/chapter_controls/_TEMPLATE.control.md",
            "references/korean_source_notes.md",
            "references/korean_title_strategy.md",
            "references/korean_to_chinese_literary_refinement.md",
            "references/quality_standard.md",
            "references/translation_research_universal.md",
            "reviews/scorecards/_TEMPLATE_random_spotcheck_score.md",
            "reviews/scorecards/_TEMPLATE_scorecard.md",
        ]
        required_files.extend(
            f"prompts/{number:02d}_{name}.md"
            for number, name in [
                (0, "orchestrator_zh_ko"),
                (1, "ingest_clean_zh_ko"),
                (2, "split_zh_ko"),
                (3, "global_translation_research_zh_ko"),
                (4, "book_specific_research_zh_ko"),
                (5, "pretranslation_trials_zh_ko"),
                (6, "glossary_style_zh_ko"),
                (7, "translate_chapters_zh_ko"),
                (8, "review_fidelity_zh_ko"),
                (9, "review_readability_imagery_zh_ko"),
                (10, "review_terminology_zh_ko"),
                (11, "chapter_quality_gate_zh_ko"),
                (12, "build_validate_zh_ko"),
                (13, "preproduction_stage1_spec_zh_ko"),
                (14, "preproduction_stage2_sample_zh_ko"),
                (15, "full_book_production_zh_ko"),
                (16, "independent_review_agents_zh_ko"),
                (17, "revision_routing_zh_ko"),
                (18, "final_output_zh_ko"),
                (19, "retrospective_template_update_zh_ko"),
            ]
        )

        missing = [path for path in required_files if not (template_root / path).exists()]

        self.assertEqual(missing, [])

    def test_create_book_project_dry_run_accepts_ko_template(self) -> None:
        result = subprocess.run(
            [
                sys.executable,
                str(REPO_ROOT / "books" / "scripts" / "create_book_project.py"),
                "sangnoksu_template_smoke_delete_me",
                "--source-target",
                "Korean-to-Simplified-Chinese",
                "--dry-run",
            ],
            cwd=REPO_ROOT,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertRegex(result.stdout, r"books/zh-Hans/\d+_sangnoksu_template_smoke_delete_me")

    def test_korean_source_notes_cover_hangul_hanja_and_colonial_period_risks(self) -> None:
        source_notes = (
            REPO_ROOT
            / "template"
            / "epub_pipeline"
            / "Korean-to-Simplified-Chinese"
            / "references"
            / "korean_source_notes.md"
        ).read_text(encoding="utf-8")

        for required_phrase in [
            "韩文/汉字混排",
            "日据时期",
            "不得把朝鲜语汉字词直接照搬为现代中文词",
            "Wikisource",
            "상록수",
        ]:
            self.assertIn(required_phrase, source_notes)


if __name__ == "__main__":
    unittest.main()
