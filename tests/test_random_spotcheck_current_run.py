from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = REPO_ROOT / "template" / "epub_pipeline" / "common" / "scripts" / "validate_random_spotcheck.py"


def write_pass_round(book_root: Path, round_number: int, *, run_id: str | None, generated_at: datetime | None) -> None:
    round_id = f"round_{round_number:03d}"
    round_dir = book_root / "reviews" / "random_spotcheck" / round_id
    for subdir in ["samples/agent_a", "samples/agent_b", "reviews", "fixes", "verification"]:
        (round_dir / subdir).mkdir(parents=True, exist_ok=True)

    manifest = {
        "schema_version": "2.0",
        "round_id": round_id,
        "seed": f"seed-{round_number}",
        "book_root": ".",
        "source_dir": "chapters/final",
        "output_dir": "reviews/random_spotcheck",
        "profile": "standard",
        "agents": 2,
        "target_confidence": 0.80,
        "defect_rate": 0.10,
        "release_confidence": 1.0,
        "strata": {
            "paragraph": {
                "candidate_count": 2,
                "sample_count": 2,
                "full_scan": True,
                "estimated_confidence_after_planned_rounds": 1.0,
            },
            "table": {"candidate_count": 0, "sample_count": 0, "full_scan": False},
            "figure": {"candidate_count": 0, "sample_count": 0, "full_scan": False},
            "formula": {"candidate_count": 0, "sample_count": 0, "full_scan": False},
            "caption_note": {"candidate_count": 0, "sample_count": 0, "full_scan": False},
        },
        "sample_sets": {
            "agent_a": {"paragraph": [{"id": "chapter::paragraph::0001"}]},
            "agent_b": {"paragraph": [{"id": "chapter::paragraph::0002"}]},
        },
    }
    if run_id is not None:
        manifest["review_run_id"] = run_id
    if generated_at is not None:
        manifest["generated_at"] = generated_at.strftime("%Y-%m-%dT%H:%M:%SZ")

    (round_dir / "random_sample_manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    for agent in ["agent_a", "agent_b"]:
        (round_dir / "samples" / agent / "all_samples.md").write_text("# samples\n", encoding="utf-8")
        (round_dir / "reviews" / f"{agent}_review.md").write_text(
            "\n".join(
                [
                    f"# {agent}",
                    'status: "PASS"',
                    "average_score: 90",
                    "lowest_score: 88",
                    "blocking_issue_count: 0",
                    "",
                ]
            ),
            encoding="utf-8",
        )
    (round_dir / "fixes" / "fix_log.md").write_text('status: "PASS"\n', encoding="utf-8")
    (round_dir / "verification" / "closure_check.md").write_text(
        'status: "PASS"\nopen_p0_p1_p2_count: 0\n',
        encoding="utf-8",
    )


class RandomSpotcheckCurrentRunTests(unittest.TestCase):
    def run_validator(self, book_root: Path, min_rounds: int | None = None) -> subprocess.CompletedProcess[str]:
        command = [
            sys.executable,
            str(VALIDATOR),
            "--book-root",
            str(book_root),
            "--require-pass",
        ]
        if min_rounds is not None:
            command.extend(["--min-current-run-pass-rounds", str(min_rounds)])
        return subprocess.run(
            command,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

    def test_rejects_three_legacy_pass_rounds_without_current_run_marker(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            book_root = Path(tmp)
            for round_number in [1, 2, 3]:
                write_pass_round(book_root, round_number, run_id=None, generated_at=None)

            result = self.run_validator(book_root, 3)

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("current-run PASS rounds", result.stdout + result.stderr)

    def test_default_accepts_two_new_consecutive_pass_rounds_from_same_current_run(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            book_root = Path(tmp)
            started = datetime.now(timezone.utc) - timedelta(minutes=5)
            for offset, round_number in enumerate([1, 2]):
                write_pass_round(
                    book_root,
                    round_number,
                    run_id="run-current",
                    generated_at=started + timedelta(minutes=offset),
                )

            result = self.run_validator(book_root)

            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            report = json.loads(
                (
                    book_root
                    / "reviews"
                    / "random_spotcheck"
                    / "round_002"
                    / "validation_report.json"
                ).read_text(encoding="utf-8")
            )
            self.assertEqual(report["current_run_pass_rounds_required"], 2)
            self.assertEqual(report["current_run_pass_rounds_count"], 2)
            self.assertEqual(report["current_review_run_id"], "run-current")

    def test_user_override_accepts_three_new_consecutive_pass_rounds_from_same_current_run(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            book_root = Path(tmp)
            started = datetime.now(timezone.utc) - timedelta(minutes=5)
            for offset, round_number in enumerate([1, 2, 3]):
                write_pass_round(
                    book_root,
                    round_number,
                    run_id="run-current",
                    generated_at=started + timedelta(minutes=offset),
                )

            result = self.run_validator(book_root, 3)

            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            report = json.loads(
                (
                    book_root
                    / "reviews"
                    / "random_spotcheck"
                    / "round_003"
                    / "validation_report.json"
                ).read_text(encoding="utf-8")
            )
            self.assertEqual(report["current_run_pass_rounds_required"], 3)
            self.assertEqual(report["current_run_pass_rounds_count"], 3)
            self.assertEqual(report["current_review_run_id"], "run-current")

    def test_user_override_accepts_one_current_run_pass_round(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            book_root = Path(tmp)
            write_pass_round(
                book_root,
                1,
                run_id="run-current",
                generated_at=datetime.now(timezone.utc),
            )

            result = self.run_validator(book_root, 1)

            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            report = json.loads(
                (
                    book_root
                    / "reviews"
                    / "random_spotcheck"
                    / "round_001"
                    / "validation_report.json"
                ).read_text(encoding="utf-8")
            )
            self.assertEqual(report["current_run_pass_rounds_required"], 1)
            self.assertEqual(report["current_run_pass_rounds_count"], 1)


if __name__ == "__main__":
    unittest.main()
