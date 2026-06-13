from __future__ import annotations

import subprocess
import sys
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]


class ItalianTemplateGoalTests(unittest.TestCase):
    def test_it_language_template_has_required_goal_files(self) -> None:
        template_root = REPO_ROOT / "template" / "epub_pipeline" / "Italian-to-Simplified-Chinese"
        required_files = [
            "AGENTS.md",
            "SKILL.md",
            "README.md",
            "MASTER_PROMPT.md",
            "TEMPLATE_VERSION.md",
            "retrospective_lessons.md",
            "package.json",
            "metadata/book.yaml",
            "metadata/italian_source_profile.md",
            "metadata/style_profile.md",
            "glossary/style_guide.md",
            "glossary/terms.csv",
            "qa/chapter_controls/_TEMPLATE.control.md",
            "references/italian_source_notes.md",
            "references/italian_title_strategy.md",
            "references/italian_to_chinese_literary_refinement.md",
            "references/quality_standard.md",
            "references/translation_research_universal.md",
            "reviews/scorecards/_TEMPLATE_random_spotcheck_score.md",
            "reviews/scorecards/_TEMPLATE_scorecard.md",
        ]
        required_files.extend(
            f"prompts/{number:02d}_{name}.md"
            for number, name in [
                (0, "orchestrator_zh_it"),
                (1, "ingest_clean_zh_it"),
                (2, "split_zh_it"),
                (3, "global_translation_research_zh_it"),
                (4, "book_specific_research_zh_it"),
                (5, "pretranslation_trials_zh_it"),
                (6, "glossary_style_zh_it"),
                (7, "translate_chapters_zh_it"),
                (8, "review_fidelity_zh_it"),
                (9, "review_readability_imagery_zh_it"),
                (10, "review_terminology_zh_it"),
                (11, "chapter_quality_gate_zh_it"),
                (12, "build_validate_zh_it"),
                (13, "preproduction_stage1_spec_zh_it"),
                (14, "preproduction_stage2_sample_zh_it"),
                (15, "full_book_production_zh_it"),
                (16, "independent_review_agents_zh_it"),
                (17, "revision_routing_zh_it"),
                (18, "final_output_zh_it"),
                (19, "retrospective_template_update_zh_it"),
            ]
        )

        missing = [path for path in required_files if not (template_root / path).exists()]

        self.assertEqual(missing, [])

    def test_create_book_project_dry_run_accepts_it_template(self) -> None:
        result = subprocess.run(
            [
                sys.executable,
                str(REPO_ROOT / "books" / "scripts" / "create_book_project.py"),
                "le_tigri_di_mompracem_template_smoke_delete_me",
                "--source-target",
                "Italian-to-Simplified-Chinese",
                "--dry-run",
            ],
            cwd=REPO_ROOT,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertRegex(result.stdout, r"books/zh-Hans/\d+_le_tigri_di_mompracem_template_smoke_delete_me")

    def test_italian_source_notes_cover_adventure_and_source_risks(self) -> None:
        source_notes = (
            REPO_ROOT
            / "template"
            / "epub_pipeline"
            / "Italian-to-Simplified-Chinese"
            / "references"
            / "italian_source_notes.md"
        ).read_text(encoding="utf-8")

        for required_phrase in [
            "意大利语",
            "Salgari",
            "Sandokan",
            "殖民时代",
            "不得使用现代中文译本",
            "Wikisource",
        ]:
            self.assertIn(required_phrase, source_notes)


if __name__ == "__main__":
    unittest.main()
