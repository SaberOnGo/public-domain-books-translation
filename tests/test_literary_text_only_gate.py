"""Translation release gates require text quality, without an audio test."""
import contextlib
import importlib.util
import io
from pathlib import Path
import tempfile
import unittest

SCRIPTS = Path(__file__).resolve().parents[1] / 'template/epub_pipeline/common/scripts'


def load(name):
    spec = importlib.util.spec_from_file_location(name, SCRIPTS / (name + '.py'))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class LiteraryTextOnlyGateTests(unittest.TestCase):
    def test_complete_text_review_needs_no_audio_fields(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            review = root / 'review.md'
            review.write_text('status: PASS\ntarget_only_reading_score: 5\n'
                'unresolved_style_debt_count: 0\nliteral_explanatory_style_debt_count: 0\n'
                'high_impact_sections_reviewed: true\nauthor_preface_and_first_chapter_reviewed: true\n'
                'source_fidelity_backcheck_after_polish: true\n', encoding='utf-8')
            self.assertEqual(load('check_literary_style_gate').validate_review(root, review), [])
            review.write_text(review.read_text().replace('unresolved_style_debt_count: 0',
                'unresolved_style_debt_count: 1'), encoding='utf-8')
            rules = {i['rule'] for i in load('check_literary_style_gate').validate_review(root, review)}
            self.assertIn('literary_unresolved_style_debt', rules)

    def test_release_keeps_text_and_artifact_gates_without_audio(self):
        summary = dict(random_spotcheck_status='PASS', random_spotcheck_require_pass=True,
            current_review_run_id='fixture', current_run_pass_rounds_required=2,
            current_run_pass_rounds_count=2, release_confidence=0.95,
            epubcheck_records=[dict(edition_type='target_only',report_path='fixture.json',hash_match=True,
                identity_match=True,fatal=0,error=0,warning=0)],
            translation_artifact_gate_status='PASS', translation_artifact_reader_policy='if_available',
            translation_artifact_reader_status='PASS', translation_artifact_hash_match=True,
            publication_lint_path='fixture.json',publication_lint_issue_count=0,
            translation_metrics_path='fixture.json',translation_metrics_estimate_status='PASS',
            translation_metrics_actual_status='PASS',literary_style_review_path='review.md',
            literary_style_status='PASS',literary_target_only_reading_score=5,
            literary_unresolved_style_debt_count=0,literary_literal_explanatory_style_debt_count=0,
            literary_high_impact_sections_reviewed=True,literary_author_preface_and_first_chapter_reviewed=True,
            literary_source_fidelity_backcheck_after_polish=True)
        module = load('create_release')
        module.require_pass_gates(summary)
        summary['literary_source_fidelity_backcheck_after_polish'] = False
        output = io.StringIO()
        with contextlib.redirect_stdout(output), self.assertRaises(SystemExit):
            module.require_pass_gates(summary)
        self.assertIn('source fidelity', output.getvalue())


if __name__ == '__main__':
    unittest.main()
