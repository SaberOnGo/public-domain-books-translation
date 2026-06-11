#!/usr/bin/env python3
"""Create and validate publishable translation effort metrics.

The metrics live in output/release/ for public projects so future agents and
users can compare estimates with actual translation outcomes without reading
private working files, prompts, source text, or QA logs.
"""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


DEFAULT_BOOK_ROOT = Path(__file__).resolve().parents[1]
METRICS_JSON = "translation_metrics.json"
METRICS_MD = "translation_metrics.md"
PROVIDER_TEMPLATES = [
    {
        "provider": "deepseek",
        "model_name": "",
        "model_tier": "medium",
        "recommended_for": "draft translation and low-cost broad coverage",
        "estimated_input_tokens": 0,
        "estimated_output_tokens": 0,
        "cost_control_notes": [],
        "quality_risk_notes": [],
    },
    {
        "provider": "gpt",
        "model_name": "",
        "model_tier": "high",
        "recommended_for": "final-quality translation, chapter control, and difficult passages",
        "estimated_input_tokens": 0,
        "estimated_output_tokens": 0,
        "cost_control_notes": [],
        "quality_risk_notes": [],
    },
    {
        "provider": "claude",
        "model_name": "",
        "model_tier": "high",
        "recommended_for": "long-context review, style consistency, and comparative QA",
        "estimated_input_tokens": 0,
        "estimated_output_tokens": 0,
        "cost_control_notes": [],
        "quality_risk_notes": [],
    },
]
DIFFICULTY_COMPONENTS = {
    "source_language_complexity": 0,
    "domain_knowledge_load": 0,
    "terminology_density": 0,
    "argument_or_plot_complexity": 0,
    "historical_context_load": 0,
    "philosophical_or_theoretical_density": 0,
    "technical_code_or_formula_load": 0,
    "tables_figures_formula_load": 0,
    "target_style_difficulty": 0,
    "annotation_and_cross_reference_load": 0,
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Create or validate translation metrics for a book project.")
    parser.add_argument("--book-root", default=None, help="Book project root. Defaults to the parent of scripts/.")
    parser.add_argument("--release-dir", default="output/release", help="Metrics directory relative to the book root.")
    parser.add_argument(
        "--init",
        action="store_true",
        help="Create translation_metrics.json and translation_metrics.md when missing.",
    )
    parser.add_argument(
        "--validate",
        action="store_true",
        help="Validate existing metrics. This is the default when --init is not provided.",
    )
    parser.add_argument(
        "--require-actual-pass",
        action="store_true",
        help="Require completed post-translation actual metrics. Use before PASS release.",
    )
    parser.add_argument("--write-report", action="store_true", help="Write output/translation_metrics_check.json.")
    return parser.parse_args()


def now_utc() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def resolve_book_root(value: str | None) -> Path:
    return (Path(value) if value else DEFAULT_BOOK_ROOT).resolve()


def rel(book_root: Path, path: Path) -> str:
    try:
        return path.resolve().relative_to(book_root.resolve()).as_posix()
    except ValueError:
        return str(path)


def read_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")


def read_yaml_scalar(path: Path, key: str) -> str:
    if not path.exists():
        return ""
    prefix = f"{key}:"
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        if line.strip().startswith(prefix):
            return line.split(":", 1)[1].strip().strip("\"'")
    return ""


def default_metrics(book_root: Path) -> dict[str, Any]:
    metadata = book_root / "metadata" / "book.yaml"
    state = read_json(book_root / "state" / "pipeline_state.json")
    return {
        "schema_version": "1.0.0",
        "metrics_status": "DRAFT",
        "created_at": now_utc(),
        "updated_at": now_utc(),
        "privacy_contract": {
            "contains_source_text": False,
            "contains_prompt_text": False,
            "contains_local_absolute_paths": False,
            "publishable_to_github": state.get("publication_mode") != "private_use",
        },
        "book": {
            "title": read_yaml_scalar(metadata, "title"),
            "original_title": read_yaml_scalar(metadata, "original_title"),
            "author": read_yaml_scalar(metadata, "author"),
            "source_target": state.get("template_root", ""),
            "publication_mode": state.get("publication_mode", "public_domain"),
            "profile": state.get("profile", ""),
        },
        "pretranslation_estimate": {
            "status": "DRAFT",
            "created_at": "",
            "book_complexity_profile": {
                "primary_book_type": "",
                "secondary_book_types": [],
                "domains": [],
                "source_unit": "characters_or_words",
                "source_unit_count": 0,
                "chapter_count": 0,
                "estimated_target_unit_count": 0,
                "figures_count": 0,
                "tables_count": 0,
                "formula_or_code_block_count": 0,
                "notes_or_annotations_count": 0,
                "named_entity_density": "",
                "requires_external_research": False,
                "requires_table_or_figure_reconstruction": False,
                "requires_formula_or_code_validation": False,
                "requires_historical_or_philosophical_context": False,
                "special_risk_notes": [],
            },
            "difficulty_level": "",
            "difficulty_score_1_to_5": 0,
            "difficulty_components_1_to_5": DIFFICULTY_COMPONENTS,
            "difficulty_factors": [],
            "difficulty_rationale": "",
            "estimated_calendar_days": {"min": 0, "max": 0},
            "estimated_active_hours": {"min": 0, "max": 0},
            "estimated_review_rounds": 0,
            "historical_reference": {
                "matched_count": 0,
                "candidate_count": 0,
                "similar_books": [],
                "estimated_from_history": {
                    "active_hours_per_10k_source_units": 0,
                    "input_tokens_per_source_unit": 0,
                    "output_tokens_per_source_unit": 0,
                },
                "history_usage_note": "",
            },
            "model_recommendations": PROVIDER_TEMPLATES,
            "cost_quality_strategy": [],
        },
        "post_translation_actual": {
            "status": "DRAFT",
            "started_at": "",
            "finished_at": "",
            "actual_calendar_days": 0,
            "actual_active_hours": 0,
            "actual_review_rounds": 0,
            "actual_difficulty_level": "",
            "actual_difficulty_score_1_to_5": 0,
            "models_used": [],
            "total_input_tokens": 0,
            "total_output_tokens": 0,
            "quality_scores": {
                "random_spotcheck_average": 0,
                "random_spotcheck_lowest": 0,
                "release_confidence": 0,
            },
            "variance_against_estimate": "",
            "lessons_for_future_estimates": [],
        },
    }


def is_positive_number(value: Any) -> bool:
    return isinstance(value, (int, float)) and value > 0


def nonempty(value: Any) -> bool:
    if isinstance(value, str):
        return bool(value.strip())
    if isinstance(value, list):
        return bool(value)
    return value is not None


def validate_estimate(data: dict[str, Any], issues: list[str]) -> None:
    estimate = data.get("pretranslation_estimate", {})
    if not isinstance(estimate, dict):
        issues.append("pretranslation_estimate must be an object")
        return
    if estimate.get("status") != "PASS":
        issues.append("pretranslation_estimate.status must be PASS")
    profile = estimate.get("book_complexity_profile", {})
    if not isinstance(profile, dict):
        issues.append("pretranslation_estimate.book_complexity_profile must be an object")
        profile = {}
    for field in ["primary_book_type", "source_unit", "named_entity_density"]:
        if not nonempty(profile.get(field)):
            issues.append(f"book_complexity_profile.{field} is required")
    for field in [
        "source_unit_count",
        "chapter_count",
        "estimated_target_unit_count",
        "figures_count",
        "tables_count",
        "formula_or_code_block_count",
        "notes_or_annotations_count",
    ]:
        value = profile.get(field)
        if not isinstance(value, (int, float)) or value < 0:
            issues.append(f"book_complexity_profile.{field} must be a non-negative number")
    if not is_positive_number(profile.get("source_unit_count")):
        issues.append("book_complexity_profile.source_unit_count must be positive")
    if not is_positive_number(profile.get("chapter_count")):
        issues.append("book_complexity_profile.chapter_count must be positive")
    for field in ["secondary_book_types", "domains", "special_risk_notes"]:
        if not isinstance(profile.get(field), list):
            issues.append(f"book_complexity_profile.{field} must be a list")
    for field in ["created_at", "difficulty_level", "difficulty_rationale"]:
        if not nonempty(estimate.get(field)):
            issues.append(f"pretranslation_estimate.{field} is required")
    for field in ["difficulty_score_1_to_5", "estimated_review_rounds"]:
        if not is_positive_number(estimate.get(field)):
            issues.append(f"pretranslation_estimate.{field} must be a positive number")
    components = estimate.get("difficulty_components_1_to_5", {})
    if not isinstance(components, dict):
        issues.append("pretranslation_estimate.difficulty_components_1_to_5 must be an object")
    else:
        for field in DIFFICULTY_COMPONENTS:
            value = components.get(field)
            if not isinstance(value, (int, float)) or value < 1 or value > 5:
                issues.append(f"difficulty_components_1_to_5.{field} must be between 1 and 5")
    for range_field in ["estimated_calendar_days", "estimated_active_hours"]:
        value = estimate.get(range_field, {})
        if not isinstance(value, dict) or not is_positive_number(value.get("min")) or not is_positive_number(value.get("max")):
            issues.append(f"pretranslation_estimate.{range_field}.min/max must be positive numbers")
        elif float(value["min"]) > float(value["max"]):
            issues.append(f"pretranslation_estimate.{range_field}.min must be <= max")
    recommendations = estimate.get("model_recommendations", [])
    history = estimate.get("historical_reference", {})
    if not isinstance(history, dict):
        issues.append("pretranslation_estimate.historical_reference must be an object")
    else:
        if "matched_count" not in history:
            issues.append("historical_reference.matched_count is required")
        if not isinstance(history.get("similar_books", []), list):
            issues.append("historical_reference.similar_books must be a list")
        historical_estimate = history.get("estimated_from_history", {})
        if not isinstance(historical_estimate, dict):
            issues.append("historical_reference.estimated_from_history must be an object")
    if not isinstance(recommendations, list) or not recommendations:
        issues.append("pretranslation_estimate.model_recommendations must include provider options")
    else:
        providers = {str(item.get("provider", "")).lower() for item in recommendations if isinstance(item, dict)}
        for provider in ["deepseek", "gpt", "claude"]:
            if provider not in providers:
                issues.append(f"pretranslation_estimate.model_recommendations missing provider: {provider}")
        for index, item in enumerate(recommendations):
            if not isinstance(item, dict):
                issues.append(f"model_recommendations[{index}] must be an object")
                continue
            for field in ["provider", "model_tier", "recommended_for"]:
                if not nonempty(item.get(field)):
                    issues.append(f"model_recommendations[{index}].{field} is required")
            if str(item.get("model_tier", "")).lower() not in {"low", "medium", "high", "very_high"}:
                issues.append(f"model_recommendations[{index}].model_tier must be low, medium, high, or very_high")
            if not is_positive_number(item.get("estimated_input_tokens")):
                issues.append(f"model_recommendations[{index}].estimated_input_tokens must be positive")
            if not is_positive_number(item.get("estimated_output_tokens")):
                issues.append(f"model_recommendations[{index}].estimated_output_tokens must be positive")


def validate_actual(data: dict[str, Any], issues: list[str]) -> None:
    actual = data.get("post_translation_actual", {})
    if not isinstance(actual, dict):
        issues.append("post_translation_actual must be an object")
        return
    if actual.get("status") != "PASS":
        issues.append("post_translation_actual.status must be PASS")
    for field in ["started_at", "finished_at", "actual_difficulty_level", "variance_against_estimate"]:
        if not nonempty(actual.get(field)):
            issues.append(f"post_translation_actual.{field} is required")
    for field in [
        "actual_calendar_days",
        "actual_active_hours",
        "actual_review_rounds",
        "actual_difficulty_score_1_to_5",
        "total_input_tokens",
        "total_output_tokens",
    ]:
        if not is_positive_number(actual.get(field)):
            issues.append(f"post_translation_actual.{field} must be a positive number")
    models_used = actual.get("models_used", [])
    if not isinstance(models_used, list) or not models_used:
        issues.append("post_translation_actual.models_used must include at least one model")
    else:
        for index, item in enumerate(models_used):
            if not isinstance(item, dict):
                issues.append(f"models_used[{index}] must be an object")
                continue
            for field in ["provider", "model_name", "model_tier", "role"]:
                if not nonempty(item.get(field)):
                    issues.append(f"models_used[{index}].{field} is required")
            for field in ["input_tokens", "output_tokens"]:
                if not is_positive_number(item.get(field)):
                    issues.append(f"models_used[{index}].{field} must be positive")
    if not nonempty(actual.get("lessons_for_future_estimates")):
        issues.append("post_translation_actual.lessons_for_future_estimates is required")


def validate_privacy(data: dict[str, Any], issues: list[str]) -> None:
    contract = data.get("privacy_contract", {})
    if not isinstance(contract, dict):
        issues.append("privacy_contract must be an object")
        return
    for field in ["contains_source_text", "contains_prompt_text", "contains_local_absolute_paths"]:
        if contract.get(field) is not False:
            issues.append(f"privacy_contract.{field} must be false")


def validate_metrics(data: dict[str, Any], require_actual_pass: bool) -> list[str]:
    issues: list[str] = []
    if data.get("schema_version") != "1.0.0":
        issues.append("schema_version must be 1.0.0")
    validate_privacy(data, issues)
    validate_estimate(data, issues)
    if require_actual_pass:
        validate_actual(data, issues)
    return issues


def render_markdown(data: dict[str, Any]) -> str:
    book = data.get("book", {})
    estimate = data.get("pretranslation_estimate", {})
    actual = data.get("post_translation_actual", {})
    recommendations = estimate.get("model_recommendations", []) if isinstance(estimate, dict) else []
    models = actual.get("models_used", []) if isinstance(actual, dict) else []
    rec_lines = [
        f"- {item.get('provider', '')}: {item.get('model_name') or 'model name TBD'} "
        f"({item.get('model_tier', '')}) - {item.get('recommended_for', '')}"
        for item in recommendations
        if isinstance(item, dict)
    ]
    model_lines = [
        f"- {item.get('provider', '')}: {item.get('model_name', '')} "
        f"({item.get('model_tier', '')}), role={item.get('role', '')}, "
        f"input_tokens={item.get('input_tokens', 0)}, output_tokens={item.get('output_tokens', 0)}"
        for item in models
        if isinstance(item, dict)
    ] or ["- Not recorded yet."]
    lesson_lines = [f"- {item}" for item in actual.get("lessons_for_future_estimates", [])] or ["- Not recorded yet."]
    return "\n".join(
        [
            "# Translation Effort Metrics / 翻译任务预估与实际统计",
            "",
            "This publishable record helps future users and agents estimate translation time, difficulty, token use, and model tier choices for similar books.",
            "",
            "本文件用于公开记录翻译前预估与翻译后实际统计，方便后续用户和 AI 参考类似书籍的时间、难度、token 消耗和模型等级选择。",
            "",
            "## Book / 书籍",
            "",
            f"- title: {book.get('title', '')}",
            f"- original_title: {book.get('original_title', '')}",
            f"- author: {book.get('author', '')}",
            f"- source_target: {book.get('source_target', '')}",
            f"- publication_mode: {book.get('publication_mode', '')}",
            "",
            "## Pre-Translation Estimate / 翻译前预估",
            "",
            f"- status: {estimate.get('status', '')}",
            f"- primary_book_type: {estimate.get('book_complexity_profile', {}).get('primary_book_type', '')}",
            f"- domains: {', '.join(estimate.get('book_complexity_profile', {}).get('domains', []))}",
            f"- source_unit_count: {estimate.get('book_complexity_profile', {}).get('source_unit_count', 0)} {estimate.get('book_complexity_profile', {}).get('source_unit', '')}",
            f"- chapter_count: {estimate.get('book_complexity_profile', {}).get('chapter_count', 0)}",
            f"- figures_count: {estimate.get('book_complexity_profile', {}).get('figures_count', 0)}",
            f"- tables_count: {estimate.get('book_complexity_profile', {}).get('tables_count', 0)}",
            f"- formula_or_code_block_count: {estimate.get('book_complexity_profile', {}).get('formula_or_code_block_count', 0)}",
            f"- notes_or_annotations_count: {estimate.get('book_complexity_profile', {}).get('notes_or_annotations_count', 0)}",
            f"- difficulty: {estimate.get('difficulty_level', '')} ({estimate.get('difficulty_score_1_to_5', 0)}/5)",
            f"- difficulty_rationale: {estimate.get('difficulty_rationale', '')}",
            f"- estimated_calendar_days: {estimate.get('estimated_calendar_days', {}).get('min', 0)}-{estimate.get('estimated_calendar_days', {}).get('max', 0)}",
            f"- estimated_active_hours: {estimate.get('estimated_active_hours', {}).get('min', 0)}-{estimate.get('estimated_active_hours', {}).get('max', 0)}",
            f"- estimated_review_rounds: {estimate.get('estimated_review_rounds', 0)}",
            f"- historical_reference_matched_count: {estimate.get('historical_reference', {}).get('matched_count', 0)}",
            f"- historical_active_hours_per_10k_source_units: {estimate.get('historical_reference', {}).get('estimated_from_history', {}).get('active_hours_per_10k_source_units', 0)}",
            "",
            "### Model Options / 模型选择",
            "",
            *rec_lines,
            "",
            "## Post-Translation Actuals / 翻译后实际统计",
            "",
            f"- status: {actual.get('status', '')}",
            f"- started_at: {actual.get('started_at', '')}",
            f"- finished_at: {actual.get('finished_at', '')}",
            f"- actual_calendar_days: {actual.get('actual_calendar_days', 0)}",
            f"- actual_active_hours: {actual.get('actual_active_hours', 0)}",
            f"- actual_review_rounds: {actual.get('actual_review_rounds', 0)}",
            f"- actual_difficulty: {actual.get('actual_difficulty_level', '')} ({actual.get('actual_difficulty_score_1_to_5', 0)}/5)",
            f"- total_input_tokens: {actual.get('total_input_tokens', 0)}",
            f"- total_output_tokens: {actual.get('total_output_tokens', 0)}",
            f"- variance_against_estimate: {actual.get('variance_against_estimate', '')}",
            "",
            "### Models Used / 实际模型使用",
            "",
            *model_lines,
            "",
            "### Lessons / 后续预估经验",
            "",
            *lesson_lines,
            "",
            "## Privacy / 隐私与发布边界",
            "",
            "- This file must not contain source text, prompt text, private QA logs, or local absolute paths.",
            "- 本文件不得包含原文、prompt、私人 QA 日志或本机绝对路径。",
            "",
        ]
    )


def write_report(book_root: Path, issues: list[str], json_path: Path, md_path: Path) -> None:
    report = {
        "status": "FAIL" if issues else "PASS",
        "issue_count": len(issues),
        "issues": issues,
        "metrics_json": rel(book_root, json_path),
        "metrics_markdown": rel(book_root, md_path),
    }
    write_json(book_root / "output" / "translation_metrics_check.json", report)


def main() -> int:
    args = parse_args()
    book_root = resolve_book_root(args.book_root)
    release_dir = (book_root / args.release_dir).resolve()
    json_path = release_dir / METRICS_JSON
    md_path = release_dir / METRICS_MD

    if args.init:
        if json_path.exists():
            data = read_json(json_path)
            data["updated_at"] = now_utc()
        else:
            data = default_metrics(book_root)
        write_json(json_path, data)
        md_path.write_text(render_markdown(data), encoding="utf-8", newline="\n")
        if args.write_report:
            write_report(book_root, [], json_path, md_path)
        print(f"initialized {rel(book_root, json_path)}")
        print(f"initialized {rel(book_root, md_path)}")
        if not args.validate and not args.require_actual_pass:
            return 0

    if not json_path.exists():
        issues = [f"missing {rel(book_root, json_path)}; run metrics:init first"]
        if args.write_report:
            write_report(book_root, issues, json_path, md_path)
        print("translation metrics FAIL")
        for issue in issues:
            print(f"- {issue}")
        return 1

    data = read_json(json_path)
    md_path.write_text(render_markdown(data), encoding="utf-8", newline="\n")
    issues = validate_metrics(data, args.require_actual_pass)
    if not md_path.exists():
        issues.append(f"missing {rel(book_root, md_path)}")
    if args.write_report:
        write_report(book_root, issues, json_path, md_path)
    if issues:
        print("translation metrics FAIL")
        for issue in issues:
            print(f"- {issue}")
        return 1
    print("translation metrics PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
