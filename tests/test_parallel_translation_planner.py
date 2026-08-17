from __future__ import annotations

import importlib.util
import json
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "template" / "epub_pipeline" / "common" / "scripts" / "plan_parallel_translation.py"


def load_planner():
    spec = importlib.util.spec_from_file_location("lifebook_parallel_translation_planner", SCRIPT)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def workload(total: int, chapters: int = 12) -> dict:
    each = total // chapters
    values = []
    assigned = 0
    for index in range(chapters):
        weighted = total - assigned if index == chapters - 1 else each
        assigned += weighted
        values.append({"chapter_id": f"{index + 1:03d}", "weighted_source_units": weighted})
    return {"weighted_source_units": total, "chapters": values}


def capabilities(provider_family: str, advertised: int = 32, **overrides) -> dict:
    now = datetime.now(timezone.utc)
    value = {
        "schema_version": "1.0",
        "supports_parallel_workers": True,
        "provider_family": provider_family,
        "advertised_max_spawned_workers": advertised,
        "user_max_spawned_workers": advertised,
        "rate_limit_max_spawned_workers": advertised,
        "budget_max_spawned_workers": advertised,
        "quality_max_spawned_workers": advertised,
        "user_allows_subagents": True,
        "worker_profile": "configured-worker",
        "verified_at": (now - timedelta(minutes=1)).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "valid_until": (now + timedelta(hours=1)).strftime("%Y-%m-%dT%H:%M:%SZ"),
    }
    value.update(overrides)
    return value


def passing_runtime() -> dict:
    return {
        "pilot_status": "passed",
        "structural_violations": 0,
        "name_policy_violations": 0,
        "first_pass_semantic_rate": 0.96,
        "rework_rate": 0.03,
        "patch_conflict_rate": 0.0,
    }


class ParallelTranslationPlannerTests(unittest.TestCase):
    def test_template_wires_command_and_safe_capability_defaults(self) -> None:
        package = json.loads((ROOT / "template" / "epub_pipeline" / "common" / "package.json").read_text(encoding="utf-8"))
        command = package["scripts"]["translation:orchestration:plan"]
        defaults = json.loads(
            (ROOT / "template" / "epub_pipeline" / "common" / "state" / "orchestration_capabilities.json").read_text(
                encoding="utf-8"
            )
        )
        self.assertIn("plan_parallel_translation.py --write-plan", command)
        self.assertFalse(defaults["supports_parallel_workers"])
        self.assertFalse(defaults["user_allows_subagents"])
        self.assertEqual("unknown", defaults["provider_family"])

    def test_authoritative_chapter_gates_do_not_globally_serialize_independent_owners(self) -> None:
        files = [
            ROOT / "template" / "epub_pipeline" / "common" / "references" / "quality_gate_framework.md",
            ROOT / "template" / "epub_pipeline" / "common" / "PIPELINE_SPEC.md",
            ROOT / "template" / "epub_pipeline" / "common" / "automation_contract.md",
            ROOT / "template" / "epub_pipeline" / "common" / "README.md",
            ROOT / "template" / "epub_pipeline" / "common" / "prompts" / "08a_chapter_post_translation_control.md",
        ]
        for path in files:
            text = path.read_text(encoding="utf-8")
            self.assertIn("other independently owned chapters", text, path)
            self.assertIn("其他独立 owner 的章节", text, path)

    def test_unknown_or_missing_capability_is_conservative(self) -> None:
        planner = load_planner()
        plan = planner.derive_worker_plan(workload(900_000), {})
        self.assertEqual(0, plan["spawned_worker_count"])
        self.assertEqual("capability_unknown", plan["decision_code"])

    def test_unverified_expired_or_malformed_capability_cannot_spawn(self) -> None:
        planner = load_planner()
        missing_verification = capabilities("gpt")
        missing_verification.pop("verified_at")
        expired = capabilities(
            "gpt",
            verified_at="2020-01-01T00:00:00Z",
            valid_until="2020-01-01T01:00:00Z",
        )
        malformed_cap = capabilities("gpt", advertised_max_spawned_workers=True)

        missing_plan = planner.derive_worker_plan(workload(900_000), missing_verification, passing_runtime())
        expired_plan = planner.derive_worker_plan(workload(900_000), expired, passing_runtime())
        malformed_plan = planner.derive_worker_plan(workload(900_000), malformed_cap, passing_runtime())

        self.assertEqual((0, "capability_unverified"), (missing_plan["spawned_worker_count"], missing_plan["decision_code"]))
        self.assertEqual((0, "capability_stale"), (expired_plan["spawned_worker_count"], expired_plan["decision_code"]))
        self.assertEqual((0, "capability_invalid"), (malformed_plan["spawned_worker_count"], malformed_plan["decision_code"]))

    def test_gpt_spawned_worker_cap_is_four_with_independent_auditor(self) -> None:
        planner = load_planner()
        plan = planner.derive_worker_plan(
            workload(900_000),
            capabilities("gpt"),
            passing_runtime(),
        )
        self.assertEqual(4, plan["spawned_worker_count"])
        self.assertEqual(3, plan["role_counts"]["translation_producers"])
        self.assertEqual(1, plan["role_counts"]["audit_consumers"])
        self.assertEqual("coordinator", plan["merge_authority"])
        self.assertFalse(plan["coordinator_counts_toward_spawned_cap"])

    def test_non_gpt_cap_never_exceeds_eight(self) -> None:
        planner = load_planner()
        plan = planner.derive_worker_plan(
            workload(2_000_000, chapters=24),
            capabilities("non_gpt", advertised=64),
            passing_runtime(),
        )
        self.assertEqual(8, plan["spawned_worker_count"])
        self.assertEqual(6, plan["role_counts"]["translation_producers"])
        self.assertEqual(2, plan["role_counts"]["audit_consumers"])

    def test_user_and_operational_caps_are_minimum_and_user_prohibition_wins(self) -> None:
        planner = load_planner()
        limited = planner.derive_worker_plan(
            workload(900_000),
            capabilities("gpt", user_max_spawned_workers=3, budget_max_spawned_workers=2),
            passing_runtime(),
        )
        prohibited = planner.derive_worker_plan(
            workload(900_000),
            capabilities("gpt", user_allows_subagents=False),
        )
        self.assertEqual(2, limited["spawned_worker_count"])
        self.assertEqual(0, prohibited["spawned_worker_count"])
        self.assertEqual("parallel_workers_disabled", prohibited["decision_code"])

    def test_small_book_stays_single_coordinator(self) -> None:
        planner = load_planner()
        plan = planner.derive_worker_plan(workload(30_000, chapters=4), capabilities("gpt"))
        self.assertEqual(0, plan["spawned_worker_count"])
        self.assertEqual("workload_below_parallel_threshold", plan["decision_code"])

    def test_pending_pilot_starts_at_two_and_bad_quality_downscales(self) -> None:
        planner = load_planner()
        pending = planner.derive_worker_plan(workload(900_000), capabilities("non_gpt"))
        failed = planner.derive_worker_plan(
            workload(900_000),
            capabilities("non_gpt"),
            {
                "pilot_status": "failed",
                "structural_violations": 1,
                "name_policy_violations": 1,
                "first_pass_semantic_rate": 0.70,
                "rework_rate": 0.30,
                "patch_conflict_rate": 0.20,
            },
        )
        self.assertEqual(2, pending["spawned_worker_count"])
        self.assertEqual(1, failed["spawned_worker_count"])
        self.assertIn("quality_downscale", failed["decision_code"])

    def test_claimed_pass_without_complete_pilot_metrics_cannot_scale_up(self) -> None:
        planner = load_planner()
        plan = planner.derive_worker_plan(
            workload(2_000_000, chapters=24),
            capabilities("non_gpt", advertised=64),
            {"pilot_status": "passed", "first_pass_semantic_rate": 0.96},
        )
        self.assertEqual(2, plan["spawned_worker_count"])
        self.assertEqual("pilot_evidence_incomplete", plan["decision_code"])

    def test_out_of_range_pilot_metrics_are_poisoned_evidence(self) -> None:
        planner = load_planner()
        poisoned = passing_runtime()
        poisoned["first_pass_semantic_rate"] = 1.5
        plan = planner.derive_worker_plan(
            workload(2_000_000, chapters=24),
            capabilities("non_gpt", advertised=64),
            poisoned,
        )
        self.assertEqual(1, plan["spawned_worker_count"])
        self.assertEqual("quality_downscale_invalid_pilot_evidence", plan["decision_code"])

    def test_rate_limit_wins_over_claimed_pass_with_incomplete_evidence(self) -> None:
        planner = load_planner()
        plan = planner.derive_worker_plan(
            workload(2_000_000, chapters=24),
            capabilities("non_gpt", advertised=64),
            {"pilot_status": "passed", "rate_limited": True},
        )
        self.assertEqual(1, plan["spawned_worker_count"])
        self.assertEqual("quality_downscale_rate_limited", plan["decision_code"])

    def test_known_blocking_violation_downscales_even_when_other_metrics_are_missing(self) -> None:
        planner = load_planner()
        plan = planner.derive_worker_plan(
            workload(2_000_000, chapters=24),
            capabilities("non_gpt", advertised=64),
            {"pilot_status": "passed", "structural_violations": 1},
        )
        self.assertEqual(1, plan["spawned_worker_count"])
        self.assertEqual("quality_downscale", plan["decision_code"])

    def test_chapter_bundles_are_complete_contiguous_and_have_single_owners(self) -> None:
        planner = load_planner()
        source = workload(900_000, chapters=13)
        plan = planner.derive_worker_plan(
            source,
            capabilities("gpt"),
            passing_runtime(),
        )
        bundles = plan["translation_bundles"]
        flattened = [chapter for bundle in bundles for chapter in bundle["chapter_ids"]]
        expected = [item["chapter_id"] for item in source["chapters"]]
        self.assertEqual(expected, flattened)
        self.assertEqual(len(expected), len(set(flattened)))
        positions = {chapter: index for index, chapter in enumerate(expected)}
        for bundle in bundles:
            indexes = [positions[chapter] for chapter in bundle["chapter_ids"]]
            self.assertEqual(list(range(min(indexes), max(indexes) + 1)), indexes)
        producer_ids = {bundle["owner_run_id"] for bundle in bundles}
        auditor_ids = set(plan["audit_consumer_ids"])
        self.assertTrue(producer_ids.isdisjoint(auditor_ids))


if __name__ == "__main__":
    unittest.main()
