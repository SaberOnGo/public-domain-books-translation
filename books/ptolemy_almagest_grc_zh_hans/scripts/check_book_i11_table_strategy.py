from __future__ import annotations

import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
PAL_XML = PROJECT_ROOT / "source" / "transcriptions" / "pal_heiberg" / "pal_heiberg_mathematike_syntaxis_1.xml"
STRATEGY = PROJECT_ROOT / "qa" / "technical" / "011_book_i_11_chord_table_strategy.md"
CONTACT_SHEET = PROJECT_ROOT / "qa" / "technical" / "page_screenshots" / "book_i11_chord_table_pages_028_035_contact_sheet.jpg"
TABLE_LOG = PROJECT_ROOT / "qa" / "technical" / "table_validation_log.md"
INVENTORY = PROJECT_ROOT / "qa" / "technical" / "diagram_table_inventory.md"
POLICY = PROJECT_ROOT / "qa" / "technical" / "chord_angle_calculation_policy.md"
STATE = PROJECT_ROOT / "state" / "pipeline_state.json"
OUT_JSON = PROJECT_ROOT / "qa" / "pretranslation" / "011_book_i_11_table_strategy_check.json"
OUT_MD = PROJECT_ROOT / "qa" / "pretranslation" / "011_book_i_11_table_strategy_check.md"


def rel(path: Path) -> str:
    return path.relative_to(PROJECT_ROOT).as_posix()


def pal_i11_chunk() -> str:
    raw = PAL_XML.read_text(encoding="utf-8")
    start = raw.find('<h3 id="I.11"')
    end = raw.find('<h3 id="I.12"', start)
    if start < 0 or end < 0 or end <= start:
        raise RuntimeError("Cannot locate PAL I.11/I.12 boundaries")
    return raw[start:end]


def contains_all(path: Path, required: list[str]) -> tuple[str, list[str]]:
    text = path.read_text(encoding="utf-8") if path.exists() else ""
    missing = [item for item in required if item not in text]
    return ("PASS" if path.exists() and not missing else "FAIL", missing)


def collect_checks() -> tuple[list[dict[str, object]], list[str]]:
    checks: list[dict[str, object]] = []
    failures: list[str] = []

    for path in [STRATEGY, CONTACT_SHEET, TABLE_LOG, INVENTORY, POLICY]:
        status = "PASS" if path.exists() else "FAIL"
        if status == "FAIL":
            failures.append(f"missing required file: {rel(path)}")
        checks.append({"id": "required_file", "path": rel(path), "status": status})

    strategy_status, strategy_missing = contains_all(
        STRATEGY,
        [
            "BOOK_I11_TABLE_STRATEGY_PASS__SOURCE_EXTRACTION_PENDING",
            "Heiberg PDF viewer pages `28`-`35`",
            "PAL XML",
            "英译本只能用于理解表头或疑难项的 reference witness",
            "source/tables/book_i_11_chord_table_raw.csv",
            "不得只给小数",
        ],
    )
    if strategy_status == "FAIL":
        failures.append(f"strategy file missing required wording: {strategy_missing}")
    checks.append({"id": "strategy_required_wording", "status": strategy_status, "missing": strategy_missing})

    table_log_status, table_log_missing = contains_all(
        TABLE_LOG,
        [
            "Book I.11",
            "STRATEGY_PASS_SOURCE_EXTRACTION_PENDING",
            "table must not be translated as prose",
        ],
    )
    if table_log_status == "FAIL":
        failures.append(f"table validation log missing required wording: {table_log_missing}")
    checks.append({"id": "table_validation_log_updated", "status": table_log_status, "missing": table_log_missing})

    inventory_status, inventory_missing = contains_all(
        INVENTORY,
        [
            "I.11-chord-table",
            "PDF viewer pages `28`-`35`",
            "structured_table_required",
            "STRATEGY_PASS_SOURCE_EXTRACTION_PENDING",
        ],
    )
    if inventory_status == "FAIL":
        failures.append(f"diagram/table inventory missing required wording: {inventory_missing}")
    checks.append({"id": "diagram_table_inventory_updated", "status": inventory_status, "missing": inventory_missing})

    policy_status, policy_missing = contains_all(
        POLICY,
        [
            "Book I.11 弦表专项规则",
            "0°30′",
            "chord = 120 * sin(arc / 2)",
            "结构化 XHTML 表格",
        ],
    )
    if policy_status == "FAIL":
        failures.append(f"chord policy missing required wording: {policy_missing}")
    checks.append({"id": "chord_policy_updated", "status": policy_status, "missing": policy_missing})

    chunk = pal_i11_chunk()
    reserve_markers = re.findall(r'data-reserve="\|([^|]+)\|"', chunk)
    page_markers = re.findall(r'class="pagina"\s+data-prae="/([^"]+)/"', chunk)
    pal_body_absent = "<table" not in chunk and "<u " not in chunk and len(reserve_markers) <= 2
    if not pal_body_absent:
        failures.append("PAL I.11 chunk appears to contain more than heading/page markers; strategy must be rechecked")
    checks.append(
        {
            "id": "pal_i11_table_body_absent",
            "status": "PASS" if pal_body_absent else "FAIL",
            "page_markers": page_markers,
            "reserve_marker_count": len(reserve_markers),
        }
    )

    state = json.loads(STATE.read_text(encoding="utf-8"))
    formal_allowed = state.get("formal_translation_allowed") is True
    if formal_allowed:
        failures.append("formal_translation_allowed is true; this strategy check expects pretranslation gating")
    checks.append({"id": "formal_translation_still_gated", "status": "PASS" if not formal_allowed else "FAIL"})

    return checks, failures


def write_reports(checks: list[dict[str, object]], failures: list[str], created: str) -> None:
    status = "PASS_BOOK_I11_TABLE_STRATEGY__SOURCE_EXTRACTION_PENDING" if not failures else "FAIL"
    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(
        json.dumps(
            {
                "status": status,
                "created_at_utc": created,
                "chapter": "Book I.11",
                "formal_translation_allowed": False,
                "checks": checks,
                "failures": failures,
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )

    lines = [
        "# Book I.11 弦表策略检查 / Chord Table Strategy Check",
        "",
        f"check_status: `{status}`",
        f"created_at_utc: `{created}`",
        "",
        "## 控制结论",
        "",
        "- 本检查只确认 Book I.11 弦表 source extraction 策略和门禁已建立。",
        "- 本检查不允许翻译 Book I.11，不允许写 `chapters/final/`，不允许生成正式 EPUB。",
        "",
        "## 检查项",
        "",
        "| id | status | detail |",
        "|---|---|---|",
    ]
    for check in checks:
        detail = check.get("path", check.get("missing", check.get("page_markers", "")))
        lines.append(f"| {check['id']} | {check['status']} | `{detail}` |")
    if failures:
        lines.extend(["", "## Failures", ""])
        lines.extend(f"- {failure}" for failure in failures)
    OUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    created = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    checks, failures = collect_checks()
    write_reports(checks, failures, created)
    print(f"wrote {OUT_JSON.relative_to(PROJECT_ROOT)}")
    print(f"wrote {OUT_MD.relative_to(PROJECT_ROOT)}")
    if failures:
        for failure in failures:
            print(f"FAIL: {failure}", file=sys.stderr)
        return 1
    print("Book I.11 table strategy check passed; source extraction remains pending")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
