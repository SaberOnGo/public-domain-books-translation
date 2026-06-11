#!/usr/bin/env python3
"""Estimate translation difficulty from book structure and source aggregates.

The evaluator is intentionally heuristic. It gives a fast, auditable starting
point before full translation starts, then writes publishable aggregate records
without source excerpts, prompts, private QA text, or local paths.
"""

from __future__ import annotations

import argparse
import json
import math
import re
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


DEFAULT_BOOK_ROOT = Path(__file__).resolve().parents[1]
TEXT_SUFFIXES = {".md", ".txt", ".html", ".xhtml", ".xml"}
TABLE_SUFFIXES = {".csv", ".tsv"}
FIGURE_SUFFIXES = {".svg", ".png", ".jpg", ".jpeg", ".webp"}
CODE_FENCE = re.compile(r"```[\s\S]*?```", re.MULTILINE)
DISPLAY_MATH = re.compile(r"\$\$[\s\S]*?\$\$|\\\[[\s\S]*?\\\]", re.MULTILINE)
INLINE_MATH = re.compile(r"(?<!\$)\$[^$\n]{1,160}\$(?!\$)|\\\([^)]{1,160}\\\)")
MARKDOWN_IMAGE = re.compile(r"!\[[^\]]*\]\([^)]+\)")
FOOTNOTE_DEF = re.compile(r"^\[\^[^\]]+\]:", re.MULTILINE)
HTML_NOTE = re.compile(r"<(?:aside|footnote|endnote)\b", re.IGNORECASE)
MARKDOWN_TABLE_ROW = re.compile(r"^\s*\|.+\|\s*$", re.MULTILINE)
LATIN_WORD = re.compile(r"\b[A-Za-z][A-Za-z'\-]*\b")
CJK_CHAR = re.compile(r"[\u3400-\u9fff]")
CAPITALIZED_PHRASE = re.compile(r"\b(?:[A-Z][a-z]+(?:\s+|$)){2,}")

BOOK_TYPE_KEYWORDS = {
    "history": {
        "history", "historical", "empire", "dynasty", "king", "queen", "republic", "senate",
        "war", "treaty", "chronology", "revolution", "archive", "state", "monarchy",
        "历史", "王朝", "帝国", "战争", "年代", "史料", "诸侯", "国君",
    },
    "philosophy": {
        "philosophy", "metaphysics", "ethics", "ontology", "epistemology", "causality",
        "dialectic", "logic", "concept", "argument", "theory", "plato", "aristotle",
        "哲学", "伦理", "本体", "认识论", "概念", "论证", "形而上",
    },
    "programming": {
        "programming", "software", "api", "function", "class", "method", "compiler",
        "runtime", "database", "javascript", "python", "c#", "java", "typescript",
        "编程", "代码", "函数", "接口", "数据库", "编译", "运行时",
    },
    "science": {
        "science", "astronomy", "physics", "chemistry", "biology", "medicine", "experiment",
        "equation", "proof", "theorem", "geometry", "optics", "mechanics",
        "科学", "天文", "物理", "化学", "医学", "几何", "公式", "证明",
    },
    "language_learning": {
        "grammar", "syntax", "vocabulary", "phonetics", "lesson", "exercise", "dialogue",
        "语言", "语法", "词汇", "发音", "练习", "课文",
    },
    "fiction": {
        "novel", "story", "chapter", "character", "dialogue", "narrator", "plot",
        "小说", "故事", "人物", "叙事", "情节", "对白",
    },
}

SOURCE_LANGUAGE_BASE = {
    "lzh": 5,
    "grc": 5,
    "la": 5,
    "ar": 4,
    "de": 4,
    "ja": 4,
    "ko": 4,
    "fr": 3,
    "it": 3,
    "es": 3,
    "en": 2,
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Evaluate book translation difficulty before full translation.")
    parser.add_argument("--book-root", default=None, help="Book project root. Defaults to the parent of scripts/.")
    parser.add_argument(
        "--source-dir",
        action="append",
        default=[],
        help="Additional source directory relative to the book root. Can be repeated.",
    )
    parser.add_argument("--write-metrics", action="store_true", help="Update output/release/translation_metrics.json.")
    parser.add_argument("--release-dir", default="output/release", help="Output directory relative to the book root.")
    parser.add_argument(
        "--history-root",
        default=None,
        help="Directory that contains public book projects to scan for output/release/translation_metrics.json.",
    )
    return parser.parse_args()


def now_utc() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def resolve_book_root(value: str | None) -> Path:
    return (Path(value) if value else DEFAULT_BOOK_ROOT).resolve()


def read_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def find_books_root(book_root: Path) -> Path:
    current = book_root.resolve()
    for parent in [current, *current.parents]:
        if parent.name == "books":
            return parent
    return book_root.resolve().parents[1]


def write_json(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")


def read_yaml_scalar(path: Path, key: str) -> str:
    if not path.exists():
        return ""
    prefix = f"{key}:"
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        stripped = line.strip()
        if stripped.startswith(prefix):
            return stripped.split(":", 1)[1].strip().strip("\"'")
    return ""


def iter_text_files(book_root: Path, extra_source_dirs: list[str]) -> list[Path]:
    candidates = [
        "source",
        "chapters/source",
        "chapters/raw",
        "chapters/clean",
        "chapters/cleaned",
        "chapters/translated",
        "chapters/final",
        *extra_source_dirs,
    ]
    files: list[Path] = []
    seen: set[Path] = set()
    for candidate in candidates:
        root = (book_root / candidate).resolve()
        if not root.exists():
            continue
        for path in root.rglob("*"):
            if path.is_file() and path.suffix.lower() in TEXT_SUFFIXES and path.resolve() not in seen:
                seen.add(path.resolve())
                files.append(path)
    return sorted(files)


def read_text_files(files: list[Path]) -> str:
    chunks: list[str] = []
    for path in files:
        chunks.append(path.read_text(encoding="utf-8", errors="replace"))
    return "\n".join(chunks)


def count_markdown_tables(text: str) -> int:
    lines = text.splitlines()
    count = 0
    in_table = False
    for line in lines:
        is_row = bool(MARKDOWN_TABLE_ROW.match(line))
        if is_row and not in_table:
            count += 1
            in_table = True
        elif not is_row:
            in_table = False
    return count


def count_files(root: Path, suffixes: set[str]) -> int:
    if not root.exists():
        return 0
    return sum(1 for path in root.rglob("*") if path.is_file() and path.suffix.lower() in suffixes)


def count_chapters(files: list[Path]) -> int:
    chapter_like = [path for path in files if path.parent.name in {"source", "raw", "clean", "cleaned", "translated", "final"}]
    return max(1, len(chapter_like) or len(files))


def unit_counts(text: str) -> tuple[str, int, int, int]:
    cjk_count = len(CJK_CHAR.findall(text))
    word_count = len(LATIN_WORD.findall(text))
    char_count = len(re.sub(r"\s+", "", text))
    if cjk_count > word_count:
        return "characters", cjk_count, word_count, char_count
    return "words", word_count, word_count, char_count


def keyword_counts(text: str) -> Counter[str]:
    lower = text.lower()
    counts: Counter[str] = Counter()
    for book_type, keywords in BOOK_TYPE_KEYWORDS.items():
        for keyword in keywords:
            if re.search(r"[\u3400-\u9fff]", keyword):
                counts[book_type] += lower.count(keyword.lower())
            else:
                counts[book_type] += len(re.findall(rf"\b{re.escape(keyword)}\b", lower))
    return counts


def source_language_score(state: dict[str, Any]) -> int:
    template_root = str(state.get("template_root", ""))
    direction = template_root.rsplit("/", 1)[-1]
    source = direction.split("-", 1)[0] if "-" in direction else direction
    return SOURCE_LANGUAGE_BASE.get(source, 3)


def clamp_score(value: float) -> int:
    return max(1, min(5, int(math.ceil(value))))


def density_score(count: int, unit_count: int, thresholds: tuple[float, float, float, float]) -> int:
    if unit_count <= 0:
        return 1
    per_10k = count / max(unit_count, 1) * 10000
    if per_10k >= thresholds[3]:
        return 5
    if per_10k >= thresholds[2]:
        return 4
    if per_10k >= thresholds[1]:
        return 3
    if per_10k >= thresholds[0]:
        return 2
    return 1


def named_entity_density(text: str, unit_count: int) -> tuple[str, int]:
    latin_entities = len(CAPITALIZED_PHRASE.findall(text))
    cjk_markers = sum(text.count(token) for token in ["王", "帝", "国", "城", "州", "侯", "氏", "公", "君"])
    total = latin_entities + cjk_markers
    score = density_score(total, unit_count, (4, 10, 18, 30))
    label = ["low", "low", "medium", "high", "very_high"][score - 1]
    return label, total


def model_tier(overall: int, role: str) -> str:
    if overall >= 5:
        return "very_high" if role != "draft" else "high"
    if overall >= 4:
        return "high" if role != "draft" else "medium"
    if overall >= 3:
        return "medium" if role == "draft" else "high"
    return "medium"


def estimate_token_budget(unit_count: int, overall: int, multiplier: float) -> int:
    return int(max(1000, round(unit_count * multiplier * (1 + overall * 0.22), -2)))


def classify_difficulty(score: int) -> str:
    return {
        1: "low",
        2: "medium_low",
        3: "medium",
        4: "high",
        5: "very_high",
    }[score]


def safe_number(value: Any) -> float:
    return float(value) if isinstance(value, (int, float)) else 0.0


def iter_historical_metric_files(book_root: Path, history_root: Path) -> list[Path]:
    files: list[Path] = []
    current_metrics = (book_root / "output" / "release" / "translation_metrics.json").resolve()
    private_root = history_root / "private"
    for path in history_root.rglob("output/release/translation_metrics.json"):
        resolved = path.resolve()
        if resolved == current_metrics:
            continue
        try:
            resolved.relative_to(private_root.resolve())
            continue
        except ValueError:
            pass
        files.append(path)
    return sorted(files)


def historical_similarity(profile: dict[str, Any], metrics: dict[str, Any]) -> float:
    estimate = metrics.get("pretranslation_estimate", {})
    previous_profile = estimate.get("book_complexity_profile", {}) if isinstance(estimate, dict) else {}
    score = 0.0
    if previous_profile.get("primary_book_type") == profile.get("primary_book_type"):
        score += 0.45
    current_domains = set(profile.get("domains", []))
    previous_domains = set(previous_profile.get("domains", []))
    if current_domains or previous_domains:
        score += 0.35 * (len(current_domains & previous_domains) / max(len(current_domains | previous_domains), 1))
    previous_units = safe_number(previous_profile.get("source_unit_count"))
    current_units = safe_number(profile.get("source_unit_count"))
    if previous_units > 0 and current_units > 0:
        score += 0.20 * (min(previous_units, current_units) / max(previous_units, current_units))
    return round(score, 4)


def build_historical_reference(book_root: Path, profile: dict[str, Any], history_root: Path) -> dict[str, Any]:
    candidates: list[dict[str, Any]] = []
    for path in iter_historical_metric_files(book_root, history_root):
        try:
            metrics = read_json(path)
        except (OSError, json.JSONDecodeError):
            continue
        contract = metrics.get("privacy_contract", {})
        if not isinstance(contract, dict) or contract.get("publishable_to_github") is not True:
            continue
        if contract.get("contains_source_text") is not False or contract.get("contains_prompt_text") is not False:
            continue
        estimate = metrics.get("pretranslation_estimate", {})
        actual = metrics.get("post_translation_actual", {})
        if not isinstance(estimate, dict) or not isinstance(actual, dict):
            continue
        if estimate.get("status") != "PASS" or actual.get("status") != "PASS":
            continue
        similarity = historical_similarity(profile, metrics)
        if similarity <= 0:
            continue
        previous_profile = estimate.get("book_complexity_profile", {})
        candidates.append(
            {
                "book_title": metrics.get("book", {}).get("title", ""),
                "similarity": similarity,
                "primary_book_type": previous_profile.get("primary_book_type", ""),
                "domains": previous_profile.get("domains", []),
                "source_unit_count": previous_profile.get("source_unit_count", 0),
                "difficulty_level": actual.get("actual_difficulty_level") or estimate.get("difficulty_level", ""),
                "difficulty_score_1_to_5": actual.get("actual_difficulty_score_1_to_5") or estimate.get("difficulty_score_1_to_5", 0),
                "actual_active_hours": actual.get("actual_active_hours", 0),
                "actual_calendar_days": actual.get("actual_calendar_days", 0),
                "actual_review_rounds": actual.get("actual_review_rounds", 0),
                "total_input_tokens": actual.get("total_input_tokens", 0),
                "total_output_tokens": actual.get("total_output_tokens", 0),
                "model_tiers_used": sorted(
                    {
                        str(item.get("model_tier", ""))
                        for item in actual.get("models_used", [])
                        if isinstance(item, dict) and item.get("model_tier")
                    }
                ),
                "lessons": actual.get("lessons_for_future_estimates", []),
            }
        )
    candidates.sort(key=lambda item: item["similarity"], reverse=True)
    selected = candidates[:5]
    total_units = sum(safe_number(item.get("source_unit_count")) for item in selected)
    total_hours = sum(safe_number(item.get("actual_active_hours")) for item in selected)
    total_input = sum(safe_number(item.get("total_input_tokens")) for item in selected)
    total_output = sum(safe_number(item.get("total_output_tokens")) for item in selected)
    if selected and total_units > 0:
        active_hours_per_10k = round(total_hours / total_units * 10000, 2)
        input_tokens_per_source_unit = round(total_input / total_units, 2)
        output_tokens_per_source_unit = round(total_output / total_units, 2)
    else:
        active_hours_per_10k = 0
        input_tokens_per_source_unit = 0
        output_tokens_per_source_unit = 0
    return {
        "history_root": history_root.as_posix(),
        "matched_count": len(selected),
        "candidate_count": len(candidates),
        "similar_books": selected,
        "estimated_from_history": {
            "active_hours_per_10k_source_units": active_hours_per_10k,
            "input_tokens_per_source_unit": input_tokens_per_source_unit,
            "output_tokens_per_source_unit": output_tokens_per_source_unit,
        },
        "history_usage_note": (
            "Uses only publishable output/release/translation_metrics.json files with PASS estimates and PASS actuals. "
            "Private-use projects and metrics containing source text or prompt text are ignored."
        ),
    }


def build_assessment(book_root: Path, extra_source_dirs: list[str], history_root: Path | None = None) -> dict[str, Any]:
    metadata_path = book_root / "metadata" / "book.yaml"
    state = read_json(book_root / "state" / "pipeline_state.json")
    files = iter_text_files(book_root, extra_source_dirs)
    text = read_text_files(files)
    source_unit, source_unit_count, word_count, char_count = unit_counts(text)
    chapter_count = count_chapters(files)
    figures_count = len(MARKDOWN_IMAGE.findall(text)) + count_files(book_root / "assets" / "figures", FIGURE_SUFFIXES)
    tables_count = count_markdown_tables(text) + count_files(book_root / "source" / "tables", TABLE_SUFFIXES)
    formula_or_code_count = len(CODE_FENCE.findall(text)) + len(DISPLAY_MATH.findall(text)) + len(INLINE_MATH.findall(text))
    notes_count = len(FOOTNOTE_DEF.findall(text)) + len(HTML_NOTE.findall(text)) + text.count("[^")
    keywords = keyword_counts(text + "\n" + " ".join(str(state.get(key, "")) for key in ["template_root", "profile"]))
    detected = [book_type for book_type, count in keywords.most_common() if count > 0]
    if not detected:
        detected = ["general_nonfiction" if tables_count or formula_or_code_count else "fiction_or_general_prose"]
    primary = detected[0]
    entity_label, entity_count = named_entity_density(text, source_unit_count)

    components = {
        "source_language_complexity": source_language_score(state),
        "domain_knowledge_load": clamp_score(1 + max(keywords.values() or [0]) / 6 + len(detected) / 4),
        "terminology_density": max(
            density_score(entity_count, source_unit_count, (4, 10, 18, 30)),
            4 if "programming" in detected or "science" in detected else 1,
        ),
        "argument_or_plot_complexity": 4 if "philosophy" in detected else (3 if "history" in detected or "fiction" in detected else 2),
        "historical_context_load": 4 if "history" in detected else (3 if "philosophy" in detected else 1),
        "philosophical_or_theoretical_density": 4 if "philosophy" in detected else (3 if "science" in detected else 1),
        "technical_code_or_formula_load": density_score(formula_or_code_count, source_unit_count, (1, 3, 8, 15)),
        "tables_figures_formula_load": density_score(figures_count + tables_count + formula_or_code_count, source_unit_count, (2, 5, 12, 25)),
        "target_style_difficulty": 4 if primary in {"philosophy", "history", "science"} else 3,
        "annotation_and_cross_reference_load": density_score(notes_count, source_unit_count, (2, 5, 12, 25)),
    }
    weighted = (
        components["source_language_complexity"] * 1.1
        + components["domain_knowledge_load"] * 1.1
        + components["terminology_density"] * 1.0
        + components["argument_or_plot_complexity"] * 1.0
        + components["historical_context_load"] * 0.9
        + components["philosophical_or_theoretical_density"] * 0.9
        + components["technical_code_or_formula_load"] * 0.9
        + components["tables_figures_formula_load"] * 0.8
        + components["target_style_difficulty"] * 0.9
        + components["annotation_and_cross_reference_load"] * 0.7
    ) / 9.3
    length_bump = 0.45 if source_unit_count >= 150000 else 0.25 if source_unit_count >= 80000 else 0.1 if source_unit_count >= 40000 else 0
    overall = clamp_score(weighted + length_bump)
    active_min = max(2, math.ceil(source_unit_count / 3000 * (0.75 + overall * 0.25) + figures_count * 0.25 + tables_count * 0.3 + formula_or_code_count * 0.4))
    active_max = max(active_min + 1, math.ceil(active_min * (1.35 + overall * 0.08)))
    calendar_min = max(1, math.ceil(active_min / 5))
    calendar_max = max(calendar_min + 1, math.ceil(active_max / 3))
    review_rounds = max(2, overall + (1 if figures_count + tables_count + formula_or_code_count > 10 else 0))
    recommendations = [
        {
            "provider": "deepseek",
            "model_name": "",
            "model_tier": model_tier(overall, "draft"),
            "recommended_for": "low-cost first-pass translation, terminology expansion, and broad chapter drafts",
            "estimated_input_tokens": estimate_token_budget(source_unit_count, overall, 1.4),
            "estimated_output_tokens": estimate_token_budget(source_unit_count, overall, 1.1),
            "cost_control_notes": [
                "Use for broad drafting when the difficulty components are not dominated by philosophy, formulas, or dense historical context.",
                "Escalate sampled hard passages to a higher-tier reviewer before finalizing.",
            ],
            "quality_risk_notes": [
                "Watch for term drift, over-literal prose, and missed context in high-density historical or philosophical passages.",
            ],
        },
        {
            "provider": "gpt",
            "model_name": "",
            "model_tier": model_tier(overall, "final"),
            "recommended_for": "final-quality translation, difficult passages, polysemy checks, and release-facing QA",
            "estimated_input_tokens": estimate_token_budget(source_unit_count, overall, 1.7),
            "estimated_output_tokens": estimate_token_budget(source_unit_count, overall, 1.2),
            "cost_control_notes": [
                "Reserve higher-tier GPT use for dense chapters, final polish, terminology-sensitive passages, and failed review families.",
                "Use medium tier only when trial translation and random samples prove stable quality.",
            ],
            "quality_risk_notes": [
                "For history, philosophy, programming, and science books, require source-supported review rather than fluency-only scoring.",
            ],
        },
        {
            "provider": "claude",
            "model_name": "",
            "model_tier": model_tier(overall, "review"),
            "recommended_for": "long-context consistency review, style comparison, and independent QA",
            "estimated_input_tokens": estimate_token_budget(source_unit_count, overall, 1.5),
            "estimated_output_tokens": estimate_token_budget(source_unit_count, overall, 0.45),
            "cost_control_notes": [
                "Use as an independent reviewer on representative samples or high-risk chapters rather than duplicating the full draft path.",
            ],
            "quality_risk_notes": [
                "Require explicit issue rows and source references; do not accept general praise as a quality gate.",
            ],
        },
    ]
    rationale_parts = [
        f"Primary detected type is {primary}; secondary types: {', '.join(detected[1:]) or 'none'}.",
        f"Source size is {source_unit_count} {source_unit}; chapter_count={chapter_count}.",
        f"Detected figures={figures_count}, tables={tables_count}, formula_or_code_blocks={formula_or_code_count}, notes={notes_count}.",
        f"Named-entity density is {entity_label}.",
    ]
    profile = {
        "primary_book_type": primary,
        "secondary_book_types": detected[1:],
        "detected_book_types": detected,
        "domains": detected,
        "source_unit": source_unit,
        "source_unit_count": source_unit_count,
        "word_count": word_count,
        "character_count": char_count,
        "chapter_count": chapter_count,
        "estimated_target_unit_count": int(source_unit_count * 1.15),
        "figures_count": figures_count,
        "tables_count": tables_count,
        "formula_or_code_block_count": formula_or_code_count,
        "notes_or_annotations_count": notes_count,
        "named_entity_density": entity_label,
        "named_entity_estimate_count": entity_count,
        "requires_external_research": primary in {"history", "philosophy", "science", "programming"},
        "requires_table_or_figure_reconstruction": figures_count + tables_count > 0,
        "requires_formula_or_code_validation": formula_or_code_count > 0 or primary in {"programming", "science"},
        "requires_historical_or_philosophical_context": "history" in detected or "philosophy" in detected,
        "special_risk_notes": rationale_parts,
    }
    history = build_historical_reference(book_root, profile, history_root or find_books_root(book_root))
    return {
        "schema_version": "1.0.0",
        "assessment_status": "PASS",
        "created_at": now_utc(),
        "privacy_contract": {
            "contains_source_text": False,
            "contains_prompt_text": False,
            "contains_local_absolute_paths": False,
            "publishable_to_github": state.get("publication_mode") != "private_use",
        },
        "book": {
            "title": read_yaml_scalar(metadata_path, "title"),
            "original_title": read_yaml_scalar(metadata_path, "original_title"),
            "author": read_yaml_scalar(metadata_path, "author"),
            "source_target": state.get("template_root", ""),
            "publication_mode": state.get("publication_mode", "public_domain"),
            "profile": state.get("profile", ""),
        },
        "book_complexity_profile": profile,
        "difficulty_components_1_to_5": components,
        "overall_difficulty_level": classify_difficulty(overall),
        "overall_difficulty_score_1_to_5": overall,
        "difficulty_rationale": " ".join(rationale_parts),
        "estimated_calendar_days": {"min": calendar_min, "max": calendar_max},
        "estimated_active_hours": {"min": active_min, "max": active_max},
        "estimated_review_rounds": review_rounds,
        "historical_reference": history,
        "model_recommendations": recommendations,
        "cost_quality_strategy": [
            "Use lower-cost models for broad drafting only after sample quality is acceptable.",
            "Escalate high-risk chapters and recurring defect families to high or very_high tier models.",
            "Spend reviewer tokens on source-supported checks, terminology consistency, and structural assets before broad rereads.",
        ],
    }


def render_assessment_md(data: dict[str, Any]) -> str:
    profile = data["book_complexity_profile"]
    components = data["difficulty_components_1_to_5"]
    recs = data["model_recommendations"]
    history = data.get("historical_reference", {})
    similar_books = history.get("similar_books", []) if isinstance(history, dict) else []
    history_lines = [
        f"- {item.get('book_title', '')}: similarity={item.get('similarity', 0)}, "
        f"actual_active_hours={item.get('actual_active_hours', 0)}, "
        f"tokens={(item.get('total_input_tokens') or 0) + (item.get('total_output_tokens') or 0)}, "
        f"tiers={', '.join(item.get('model_tiers_used', [])) or 'not recorded'}"
        for item in similar_books
        if isinstance(item, dict)
    ] or ["- No publishable similar-book metrics found yet."]
    return "\n".join(
        [
            "# Translation Difficulty Assessment / 翻译难度评估",
            "",
            "This is a pre-translation aggregate estimate. It contains no source excerpts or prompt text.",
            "",
            "这是翻译前的聚合预估记录，不包含原文摘录或 prompt 文本。",
            "",
            "## Overall / 总体判断",
            "",
            f"- difficulty: {data['overall_difficulty_level']} ({data['overall_difficulty_score_1_to_5']}/5)",
            f"- rationale: {data['difficulty_rationale']}",
            f"- estimated_calendar_days: {data['estimated_calendar_days']['min']}-{data['estimated_calendar_days']['max']}",
            f"- estimated_active_hours: {data['estimated_active_hours']['min']}-{data['estimated_active_hours']['max']}",
            f"- estimated_review_rounds: {data['estimated_review_rounds']}",
            "",
            "## Complexity Profile / 复杂度画像",
            "",
            f"- primary_book_type: {profile['primary_book_type']}",
            f"- detected_book_types: {', '.join(profile['detected_book_types'])}",
            f"- source_unit_count: {profile['source_unit_count']} {profile['source_unit']}",
            f"- chapter_count: {profile['chapter_count']}",
            f"- figures_count: {profile['figures_count']}",
            f"- tables_count: {profile['tables_count']}",
            f"- formula_or_code_block_count: {profile['formula_or_code_block_count']}",
            f"- notes_or_annotations_count: {profile['notes_or_annotations_count']}",
            f"- named_entity_density: {profile['named_entity_density']}",
            "",
            "## Component Scores / 分项评分",
            "",
            *[f"- {key}: {value}/5" for key, value in components.items()],
            "",
            "## Historical Reference / 历史统计参考",
            "",
            f"- matched_count: {history.get('matched_count', 0) if isinstance(history, dict) else 0}",
            f"- active_hours_per_10k_source_units: {history.get('estimated_from_history', {}).get('active_hours_per_10k_source_units', 0) if isinstance(history, dict) else 0}",
            f"- input_tokens_per_source_unit: {history.get('estimated_from_history', {}).get('input_tokens_per_source_unit', 0) if isinstance(history, dict) else 0}",
            f"- output_tokens_per_source_unit: {history.get('estimated_from_history', {}).get('output_tokens_per_source_unit', 0) if isinstance(history, dict) else 0}",
            "",
            *history_lines,
            "",
            "## Model Recommendations / 模型建议",
            "",
            *[
                f"- {item['provider']}: tier={item['model_tier']}; use={item['recommended_for']}; "
                f"estimated_input_tokens={item['estimated_input_tokens']}; estimated_output_tokens={item['estimated_output_tokens']}"
                for item in recs
            ],
            "",
        ]
    )


def merge_metrics(book_root: Path, assessment: dict[str, Any], release_dir: Path) -> None:
    metrics_path = release_dir / "translation_metrics.json"
    if metrics_path.exists():
        metrics = read_json(metrics_path)
    else:
        metrics = {
            "schema_version": "1.0.0",
            "metrics_status": "DRAFT",
            "created_at": now_utc(),
            "privacy_contract": assessment["privacy_contract"],
            "book": assessment["book"],
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
    metrics["updated_at"] = now_utc()
    metrics["privacy_contract"] = assessment["privacy_contract"]
    metrics["book"] = assessment["book"]
    metrics["pretranslation_estimate"] = {
        "status": "PASS",
        "created_at": assessment["created_at"],
        "book_complexity_profile": {
            key: assessment["book_complexity_profile"][key]
            for key in [
                "primary_book_type",
                "secondary_book_types",
                "domains",
                "source_unit",
                "source_unit_count",
                "chapter_count",
                "estimated_target_unit_count",
                "figures_count",
                "tables_count",
                "formula_or_code_block_count",
                "notes_or_annotations_count",
                "named_entity_density",
                "requires_external_research",
                "requires_table_or_figure_reconstruction",
                "requires_formula_or_code_validation",
                "requires_historical_or_philosophical_context",
                "special_risk_notes",
            ]
        },
        "difficulty_level": assessment["overall_difficulty_level"],
        "difficulty_score_1_to_5": assessment["overall_difficulty_score_1_to_5"],
        "difficulty_components_1_to_5": assessment["difficulty_components_1_to_5"],
        "difficulty_factors": assessment["book_complexity_profile"]["special_risk_notes"],
        "difficulty_rationale": assessment["difficulty_rationale"],
        "estimated_calendar_days": assessment["estimated_calendar_days"],
        "estimated_active_hours": assessment["estimated_active_hours"],
        "estimated_review_rounds": assessment["estimated_review_rounds"],
        "historical_reference": assessment["historical_reference"],
        "model_recommendations": assessment["model_recommendations"],
        "cost_quality_strategy": assessment["cost_quality_strategy"],
    }
    write_json(metrics_path, metrics)


def main() -> int:
    args = parse_args()
    book_root = resolve_book_root(args.book_root)
    history_root = Path(args.history_root).resolve() if args.history_root else None
    release_dir = (book_root / args.release_dir).resolve()
    release_dir.mkdir(parents=True, exist_ok=True)
    assessment = build_assessment(book_root, args.source_dir, history_root)
    assessment_json = release_dir / "translation_difficulty_assessment.json"
    assessment_md = release_dir / "translation_difficulty_assessment.md"
    write_json(assessment_json, assessment)
    assessment_md.write_text(render_assessment_md(assessment), encoding="utf-8", newline="\n")
    if args.write_metrics:
        merge_metrics(book_root, assessment, release_dir)
    print(f"translation difficulty: {assessment['overall_difficulty_level']} ({assessment['overall_difficulty_score_1_to_5']}/5)")
    print(f"wrote {assessment_json.relative_to(book_root).as_posix()}")
    print(f"wrote {assessment_md.relative_to(book_root).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
