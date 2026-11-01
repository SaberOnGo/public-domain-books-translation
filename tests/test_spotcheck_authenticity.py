import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
SCRIPTS = REPO / "template/epub_pipeline/common/scripts"


def load(name):
    spec = importlib.util.spec_from_file_location(name, SCRIPTS / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


validator = load("validate_random_spotcheck")
release = load("create_release")

UNITS = [f"chapters/final/001.md::paragraph::{i:04d}" for i in range(12)]


def review(rows):
    lines = ["| sample | score | reason |", "| --- | --- | --- |"]
    lines += [f"| `{unit}` | {score} | {reason} |" for unit, score, reason in rows]
    return "\n".join(lines) + "\n"


class SpotcheckAuthenticityTests(unittest.TestCase):
    def rows(self, text):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "agent_a_review.md"
            path.write_text(text, encoding="utf-8")
            return validator.scored_review_rows(path, set(UNITS))

    def test_identical_rows_are_rejected(self):
        rows = self.rows(review([(unit, "94", "内容完整、人物语气和语义映射清晰。") for unit in UNITS]))
        errors = validator.review_authenticity_errors({"agent_a": rows}, {"agent_a": "agent_a_review.md"})
        self.assertTrue(any("TEMPLATED_REVIEW" in error for error in errors))

    def test_duplicated_agents_are_rejected(self):
        rows = self.rows(review([(unit, str(80 + i), f"第{i}句：引文“例句{i}”略硬，已核原文。") for i, unit in enumerate(UNITS)]))
        errors = validator.review_authenticity_errors({"agent_a": rows, "agent_b": list(rows)},
                                                      {"agent_a": "a.md", "agent_b": "b.md"})
        self.assertTrue(any("DUPLICATED_REVIEW" in error for error in errors))

    def test_per_sample_judgements_pass(self):
        rows = self.rows(review([(unit, str(85 + i % 5), f"第{i}句：引文“例句{i}”忠实，节奏自然。") for i, unit in enumerate(UNITS)]))
        self.assertEqual([], validator.review_authenticity_errors({"agent_a": rows}, {"agent_a": "a.md"}))


class ReleaseDirectoryTests(unittest.TestCase):
    def test_unregistered_epub_is_detected(self):
        with tempfile.TemporaryDirectory() as tmp:
            release_dir = Path(tmp)
            (release_dir / "书_v0.0.1.epub").write_bytes(b"x")
            (release_dir / "third party.epub").write_bytes(b"x")
            (release_dir / "release_index.md").write_text(
                "| version | status | epub |\n| --- | --- | --- |\n| v0.0.1 | PASS | `书_v0.0.1.epub` |\n", encoding="utf-8")
            registered = release.registered_release_epubs(release_dir, {})
        self.assertIn("书_v0.0.1.epub", registered)
        self.assertNotIn("third party.epub", registered)


if __name__ == "__main__":
    unittest.main()
