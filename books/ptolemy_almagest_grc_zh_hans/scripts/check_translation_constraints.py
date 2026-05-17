from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path


BOOK_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SCAN_DIRS = [
    BOOK_ROOT / "chapters" / "translated",
    BOOK_ROOT / "chapters" / "final",
    BOOK_ROOT / "frontmatter",
]


@dataclass(frozen=True)
class PatternRule:
    rule: str
    pattern: str
    message: str


FORBIDDEN_PATTERNS = [
    PatternRule("bare_eucl", r"Eucl\.", "正文不得裸写 Eucl. 缩写；改用“依据《几何原本》...〔n〕”。"),
    PatternRule("internal_sexagesimal", r"\b\d+;\d+,\d+\b", "读者版正文不得裸露内部六十进制校验记法，例如 37;4,55。"),
    PatternRule("false_part_minutes", r"\d+份\d+[′']", "非角度六十进制值不得写成 37份4′55″；使用 37p04′55″。"),
    PatternRule("hard_geometry_cut", r"将割", "古典作图语不得硬译为“将割”；改写为“交...于...”。"),
    PatternRule("hard_geometry_exceed", r"超过\s*`?ΔΖ`?", "古典作图语不得硬译为“超过 ΔΖ”；改写为“在 ΔΖ 的延长线上交于...”。"),
    PatternRule("overexplained_intersection", r"交出一点", "作图关系不应过度解释为“交出一点”；直接写“交...于...”。"),
    PatternRule("hard_half_arc_line", r"所对弧之半所对的直线", "几何读者版不得保留硬译句；使用“半弧对应的弦”。"),
]

TRIAL_BOOK_I10_REQUIRED_SNIPPETS = [
    "`37p04′55″`",
    "`1p02′50″`",
    "`0p31′25″`",
    "六十进制结构",
    "依据《几何原本》",
    "《几何原本》III.26、III.29：",
    "《几何原本》VI.33：",
    "以 `Δ` 为圆心、`ΔΕ` 为半径作圆，使它交 `ΑΔ` 于 `Η`，并在 `ΔΖ` 的延长线上交于 `Θ`",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Check reader-facing translation constraints.")
    parser.add_argument(
        "--scope",
        choices=["all", "trial-book-i10"],
        default="all",
        help="Use all for full-book gates; use trial-book-i10 for the Book I.10 sample.",
    )
    parser.add_argument("--write-report", action="store_true", help="Write qa/refinement/translation_constraints.json.")
    return parser.parse_args()


def rel(path: Path) -> str:
    return path.relative_to(BOOK_ROOT).as_posix()


def line_col(text: str, index: int) -> tuple[int, int]:
    line = text.count("\n", 0, index) + 1
    last_newline = text.rfind("\n", 0, index)
    col = index + 1 if last_newline == -1 else index - last_newline
    return line, col


def iter_files(scope: str) -> list[Path]:
    if scope == "trial-book-i10":
        return [BOOK_ROOT / "chapters" / "translated" / "010_book_i_10_chords.md"]
    files: list[Path] = []
    for root in DEFAULT_SCAN_DIRS:
        if not root.exists():
            continue
        files.extend(path for path in root.rglob("*") if path.suffix.lower() in {".md", ".xhtml"})
    return sorted(files)


def add_issue(issues: list[dict], file: Path, line: int, rule: str, message: str, sample: str) -> None:
    issues.append({
        "file": rel(file),
        "line": line,
        "rule": rule,
        "message": message,
        "sample": sample[:160],
    })


def check_forbidden(text: str, file: Path, issues: list[dict]) -> None:
    for rule in FORBIDDEN_PATTERNS:
        for match in re.finditer(rule.pattern, text):
            line, _ = line_col(text, match.start())
            add_issue(issues, file, line, rule.rule, rule.message, match.group(0).replace("\n", " "))

    for match in re.finditer(r"\d+\.\d+", text):
        line_start = text.rfind("\n", 0, match.start()) + 1
        line_end = text.find("\n", match.start())
        if line_end == -1:
            line_end = len(text)
        line_text = text[line_start:line_end]
        if "《几何原本》" in line_text or "Book I." in line_text or "Book " in line_text:
            continue
        line, _ = line_col(text, match.start())
        add_issue(
            issues,
            file,
            line,
            "decimalized_sexagesimal_risk",
            "读者版正文不得把原文六十进制值改成十进制小数；如确需现代换算，必须放入注释或校验记录。",
            match.group(0),
        )


def check_euclid_refs(text: str, file: Path, issues: list[dict]) -> None:
    refs = list(re.finditer(r"依据《几何原本》([^〔）]+)〔(\d+)〕", text))
    note_numbers = {
        int(match.group(1))
        for match in re.finditer(r"^(\d+)\.\s+《几何原本》", text, flags=re.MULTILINE)
    }

    for match in refs:
        number = int(match.group(2))
        if number not in note_numbers:
            line, _ = line_col(text, match.start())
            add_issue(
                issues,
                file,
                line,
                "euclid_ref_without_note",
                "正文《几何原本》依据必须有章末注释说明命题、定义或系的大意。",
                match.group(0),
            )

        ref = match.group(1).strip()
        if not re.search(r"(?:[IVXLCDM]+(?:\.\d+(?: 系)?| 定义 \d+)|[IVXLCDM]+\.\d+、[IVXLCDM]+\.\d+)", ref):
            line, _ = line_col(text, match.start())
            add_issue(
                issues,
                file,
                line,
                "euclid_ref_format",
                "《几何原本》依据格式必须可识别为卷号、命题号、定义或系。",
                ref,
            )

    for line_no, line in enumerate(text.splitlines(), 1):
        if "《几何原本》" not in line:
            continue
        if re.match(r"^\d+\.\s+《几何原本》", line):
            continue
        if "依据《几何原本》" in line:
            continue
        add_issue(
            issues,
            file,
            line_no,
            "bare_euclid_chinese_ref",
            "正文不得裸括《几何原本》编号；应写成“依据《几何原本》...〔n〕”。",
            line.strip(),
        )


def check_trial_book_i10_required(text: str, file: Path, issues: list[dict]) -> None:
    for snippet in TRIAL_BOOK_I10_REQUIRED_SNIPPETS:
        if snippet not in text:
            add_issue(
                issues,
                file,
                1,
                "missing_trial_book_i10_snippet",
                "Book I.10 试译必须保留已确认的读者版控制表达。",
                snippet,
            )


def write_report(report: dict) -> None:
    output = BOOK_ROOT / "qa" / "refinement" / "translation_constraints.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")


def main() -> None:
    args = parse_args()
    files = iter_files(args.scope)
    issues: list[dict] = []

    for file in files:
        if not file.exists():
            add_issue(issues, file, 1, "missing_file", "Expected translation file is missing.", str(file))
            continue
        text = file.read_text(encoding="utf-8")
        check_forbidden(text, file, issues)
        check_euclid_refs(text, file, issues)
        if args.scope == "trial-book-i10":
            check_trial_book_i10_required(text, file, issues)

    report = {
        "scope": args.scope,
        "files_checked": [rel(file) for file in files if file.exists()],
        "issue_count": len(issues),
        "issues": issues,
    }
    if args.write_report:
        write_report(report)

    if issues:
        print(json.dumps(report, ensure_ascii=False, indent=2), file=sys.stderr)
        raise SystemExit(1)

    print(f"translation constraint check passed: scope={args.scope}, files={len(report['files_checked'])}")


if __name__ == "__main__":
    main()
