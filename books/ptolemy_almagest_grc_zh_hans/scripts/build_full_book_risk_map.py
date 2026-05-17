from __future__ import annotations

import json
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
TOC = PROJECT_ROOT / "source" / "full_toc_draft.json"
OUT_JSON = PROJECT_ROOT / "qa" / "pretranslation" / "full_book_risk_map.json"
OUT_MD = PROJECT_ROOT / "qa" / "pretranslation" / "full_book_risk_map.md"


BOOK_MODULES: dict[int, str] = {
    1: "mathematical foundations, chord geometry, first tables",
    2: "spherical astronomy, latitude, rising times",
    3: "solar year and solar anomaly",
    4: "first lunar model and mean lunar motions",
    5: "lunar double anomaly, parallax, sizes/distances",
    6: "syzygies and eclipses",
    7: "fixed stars and northern star catalogue",
    8: "southern star catalogue, globe, star phenomena",
    9: "planetary order and Mercury model",
    10: "Venus and Mars models",
    11: "Jupiter and Saturn models, anomaly tables",
    12: "planetary stations and elongations",
    13: "planetary latitude models",
}


CONTROLS_BY_RISK: dict[str, list[str]] = {
    "FOUNDATION_GEOMETRY_HIGH": [
        "formal source split against Heiberg PDF and PAL Greek",
        "proof dependency map",
        "diagram/label audit when figures occur",
        "ancient/modern concept boundary note",
        "Chinese readability review for compressed geometrical prose",
    ],
    "TABLE_NUMERIC_HIGH": [
        "formal source split against Heiberg PDF and PAL Greek",
        "structured table extraction plan",
        "sexagesimal and unit-preserving numeric validation",
        "XHTML/EPUB responsive table strategy",
        "table facsimile or redraw asset inventory",
    ],
    "MODEL_NUMERIC_HIGH": [
        "formal source split against Heiberg PDF and PAL Greek",
        "astronomical model registry update",
        "parameter and sexagesimal numeric validation",
        "diagram/line-label audit for model geometry",
        "reference witness difference log for model interpretation only",
    ],
    "STAR_CATALOG_HIGH": [
        "formal source split against Heiberg PDF and PAL Greek",
        "star-name and constellation terminology registry",
        "coordinate/magnitude table validation",
        "catalogue table EPUB layout strategy",
        "ancient coordinate system boundary note",
    ],
}


def chapter_entries(data: dict[str, object]) -> list[dict[str, object]]:
    return [entry for entry in data["entries"] if entry.get("type") == "chapter"]  # type: ignore[index]


def build_rows(entries: list[dict[str, object]]) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for entry in entries:
        risk = str(entry["initial_risk"])
        rows.append(
            {
                "book": entry["book"],
                "book_number": entry["book_number"],
                "chapter": entry["chapter"],
                "anchor": entry["anchor"],
                "pal_title": entry["pal_title"],
                "risk": risk,
                "book_module": BOOK_MODULES.get(int(entry["book_number"]), "module classification pending"),
                "required_controls": CONTROLS_BY_RISK.get(
                    risk,
                    [
                        "formal source split against Heiberg PDF and PAL Greek",
                        "chapter-specific technical audit",
                    ],
                ),
                "translation_gate": "SOURCE_SPLIT_AND_TECHNICAL_QA_REQUIRED",
                "final_gate": "FORBIDDEN_UNTIL_CHAPTER_REVIEW_AND_FULL_BOOK_QA_PASS",
            }
        )
    return rows


def summarize_by_book(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    grouped: dict[int, list[dict[str, object]]] = defaultdict(list)
    for row in rows:
        grouped[int(row["book_number"])].append(row)

    summaries: list[dict[str, object]] = []
    for book_number in sorted(grouped):
        book_rows = grouped[book_number]
        risk_counts = Counter(str(row["risk"]) for row in book_rows)
        summaries.append(
            {
                "book": book_rows[0]["book"],
                "book_number": book_number,
                "module": BOOK_MODULES.get(book_number, "module classification pending"),
                "chapter_count": len(book_rows),
                "risk_counts": dict(sorted(risk_counts.items())),
                "next_pre_research_action": next_action_for_book(book_number),
            }
        )
    return summaries


def next_action_for_book(book_number: int) -> str:
    if book_number == 1:
        return "finish Book I formal source split readiness, especially I.11 table strategy"
    if book_number == 2:
        return "build spherical-astronomy diagram/table inventory and PDF boundary sampling"
    if book_number in {3, 4, 5, 6}:
        return "prepare solar/lunar model registry, numeric controls, and table routes"
    if book_number in {7, 8}:
        return "prepare star-catalogue table, star-name, coordinate, and magnitude controls"
    return "prepare planetary model registry, diagram inventory, and numeric/table controls"


def write_markdown(
    rows: list[dict[str, object]],
    book_summaries: list[dict[str, object]],
    risk_counts: Counter[str],
    created: str,
) -> None:
    lines = [
        "# 《Almagest》全书风险图 / Full-Book Risk Map",
        "",
        "risk_map_status: `DRAFT_FROM_PAL_TOC__PRE_RESEARCH_GATE_ONLY`",
        f"created_at_utc: `{created}`",
        "",
        "## 控制说明",
        "",
        "- 本文件由 `source/full_toc_draft.json` 生成，只用于全书预研究和章节 QA 路由。",
        "- 本文件不替代 Heiberg PDF 页图核验，也不替代正式 `chapters/src/*.md`。",
        "- PAL 古希腊转写是 source split 的辅助转写；英译本只能作 reference witness。",
        "- 任一章节进入翻译前，仍必须完成 formal source split、章节控制和对应技术审计。",
        "- 当前不得写 `chapters/final/`，不得生成正式 `output/book.epub`。",
        "",
        "## 风险统计",
        "",
        f"- total_chapters: `{len(rows)}`",
    ]
    for risk, count in sorted(risk_counts.items()):
        lines.append(f"- {risk}: `{count}`")

    lines.extend(
        [
            "",
            "## 逐卷模块与下一步",
            "",
            "| book | chapters | module | risk counts | next pre-research action |",
            "|---|---:|---|---|---|",
        ]
    )
    for item in book_summaries:
        risk_text = "<br/>".join(f"{key}: {value}" for key, value in item["risk_counts"].items())  # type: ignore[union-attr]
        lines.append(
            "| {book} | {chapter_count} | {module} | {risk_text} | {next_action} |".format(
                book=item["book"],
                chapter_count=item["chapter_count"],
                module=item["module"],
                risk_text=risk_text,
                next_action=item["next_pre_research_action"],
            )
        )

    lines.extend(
        [
            "",
            "## 章节 QA 路由",
            "",
            "| anchor | risk | required controls | translation gate |",
            "|---|---|---|---|",
        ]
    )
    for row in rows:
        controls = "<br/>".join(str(control) for control in row["required_controls"])
        lines.append(
            "| {anchor} | {risk} | {controls} | {gate} |".format(
                anchor=row["anchor"],
                risk=row["risk"],
                controls=controls,
                gate=row["translation_gate"],
            )
        )

    lines.extend(
        [
            "",
            "## 下一步",
            "",
            "1. 继续推进 Book I formal source split readiness，优先关闭 I.1-I.9 和 I.11 的阻断项。",
            "2. 为 Book II 建立 PDF 页图抽样和球面天文学图表清单。",
            "3. 为 Book III-VI 建立太阳/月球/食相关模型、表格和数值控制模板。",
            "4. 为 Book VII-VIII 建立星表、星名、坐标和星等控制模板。",
            "5. 为 Book IX-XIII 建立行星模型、几何图、参数和表格控制模板。",
        ]
    )
    OUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    data = json.loads(TOC.read_text(encoding="utf-8"))
    entries = chapter_entries(data)
    rows = build_rows(entries)
    risk_counts = Counter(str(row["risk"]) for row in rows)
    book_summaries = summarize_by_book(rows)
    created = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(
        json.dumps(
            {
                "risk_map_status": "DRAFT_FROM_PAL_TOC__PRE_RESEARCH_GATE_ONLY",
                "created_at_utc": created,
                "source": "source/full_toc_draft.json",
                "source_authority": {
                    "heiberg_pdf": "primary facsimile authority for formal split",
                    "pal_greek_xml": "auxiliary Ancient Greek transcription",
                    "english_translations": "reference witness only",
                },
                "chapter_count": len(rows),
                "risk_counts": dict(sorted(risk_counts.items())),
                "book_summaries": book_summaries,
                "rows": rows,
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    write_markdown(rows, book_summaries, risk_counts, created)
    print(f"wrote {OUT_JSON.relative_to(PROJECT_ROOT)}")
    print(f"wrote {OUT_MD.relative_to(PROJECT_ROOT)}")
    print(f"chapters={len(rows)} risks={dict(sorted(risk_counts.items()))}")


if __name__ == "__main__":
    main()
