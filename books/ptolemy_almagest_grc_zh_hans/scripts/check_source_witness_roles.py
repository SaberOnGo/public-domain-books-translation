from __future__ import annotations

import json
import re
import sys
from pathlib import Path


BOOK_ROOT = Path(__file__).resolve().parents[1]

REQUIRED_FILES = [
    "metadata/source_witness_manifest.md",
    "metadata/reference_witness_policy.md",
    "source/triangulated_source_control.md",
    "source/README.md",
    "metadata/book_specific_translation_research.md",
]

REQUIRED_SNIPPETS = {
    "metadata/source_witness_manifest.md": [
        "Heiberg PDF 扫描",
        "PAL Heiberg 古希腊文转写",
        "reference witness only",
        "不得作为中文转译底稿",
        "不得单独修正古希腊文底稿",
    ],
    "metadata/reference_witness_policy.md": [
        "Heiberg PDF 扫描",
        "PAL Heiberg 古希腊文转写 XML",
        "英译本",
        "reference witness only",
        "不能作为 OCR/转写校正的最终依据",
    ],
    "source/triangulated_source_control.md": [
        "PDF 扫描 + PAL 古希腊转写共同构成本书的古希腊证据链",
        "英译本不属于古希腊底稿链",
        "英译本不得作为 OCR/转写修正 authority",
    ],
    "source/README.md": [
        "Heiberg PDF 扫描",
        "PAL Heiberg 古希腊文转写",
        "英译本：只作 reference witness",
        "不作中文转译来源",
    ],
    "metadata/book_specific_translation_research.md": [
        "来源角色分工",
        "Heiberg PDF 扫描是主底本影像",
        "PAL Heiberg 古希腊文转写 XML 是辅助古希腊文转写",
        "英译本只作 reference witness",
    ],
}

FORBIDDEN_PATTERNS = [
    (
        re.compile(r"英译本.{0,20}(?:底本|底稿|source text|OCR authority|转写修正 authority)"),
        "英译本不得表述为底本、底稿、source text 或 OCR/转写修正 authority。",
    ),
    (
        re.compile(r"English translation.{0,40}(?:base text|source text|OCR authority)", re.IGNORECASE),
        "English translation must not be described as base/source text or OCR authority.",
    ),
]


def rel(path: Path) -> str:
    return path.relative_to(BOOK_ROOT).as_posix()


def add_issue(issues: list[dict], file: str, rule: str, message: str, sample: str = "") -> None:
    issues.append({
        "file": file,
        "rule": rule,
        "message": message,
        "sample": sample[:180],
    })


def check_markdown_roles(issues: list[dict]) -> None:
    for file in REQUIRED_FILES:
        path = BOOK_ROOT / file
        if not path.exists():
            add_issue(issues, file, "missing_file", "source role control file is missing")
            continue
        text = path.read_text(encoding="utf-8")
        for snippet in REQUIRED_SNIPPETS.get(file, []):
            if snippet not in text:
                add_issue(issues, file, "missing_required_source_role_snippet", f"missing required source-role statement: {snippet}")
        for pattern, message in FORBIDDEN_PATTERNS:
            for match in pattern.finditer(text):
                sample = match.group(0)
                if any(negation in sample for negation in ["不得", "不能", "不是", "不属于", "不作"]):
                    continue
                if "must not" in sample.lower() or "not " in sample.lower():
                    continue
                add_issue(issues, file, "forbidden_reference_translation_role", message, sample)


def check_source_manifest_json(issues: list[dict]) -> None:
    path = BOOK_ROOT / "source" / "source_manifest.json"
    if not path.exists():
        add_issue(issues, rel(path), "missing_file", "source_manifest.json is missing")
        return
    data = json.loads(path.read_text(encoding="utf-8"))
    hierarchy = data.get("source_role_hierarchy")
    if not isinstance(hierarchy, dict):
        add_issue(issues, rel(path), "missing_source_role_hierarchy", "source_manifest.json must record source_role_hierarchy")
        return
    for key in ["primary_facsimile", "auxiliary_greek_transcription", "reference_translation"]:
        if key not in hierarchy:
            add_issue(issues, rel(path), "missing_source_role_hierarchy_key", f"missing key: {key}")
    ref = str(hierarchy.get("reference_translation", ""))
    if "not a pivot source" not in ref or "not OCR/transcription authority" not in ref:
        add_issue(
            issues,
            rel(path),
            "weak_reference_translation_boundary",
            "reference_translation role must explicitly say it is not pivot and not OCR/transcription authority",
            ref,
        )


def main() -> None:
    issues: list[dict] = []
    check_markdown_roles(issues)
    check_source_manifest_json(issues)
    report = {
        "check": "source_witness_roles",
        "issue_count": len(issues),
        "issues": issues,
    }
    output = BOOK_ROOT / "qa" / "refinement" / "source_witness_roles.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8", newline="\n")

    if issues:
        print(json.dumps(report, ensure_ascii=False, indent=2), file=sys.stderr)
        raise SystemExit(1)

    print("source witness role check passed")


if __name__ == "__main__":
    main()
