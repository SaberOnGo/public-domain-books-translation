import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE_URL = "https://www.gutenberg.org/ebooks/19141.txt.utf-8"
SOURCE_PAGE_URL = "https://www.gutenberg.org/ebooks/19141"
START_MARKER = "*** START OF THE PROJECT GUTENBERG EBOOK EDISON'S CONQUEST OF MARS ***"
END_MARKER = "*** END OF THE PROJECT GUTENBERG EBOOK EDISON'S CONQUEST OF MARS ***"


def slugify(title: str) -> str:
    text = title.lower()
    text = re.sub(r"[^a-z0-9]+", "_", text)
    return text.strip("_") or "section"


def normalize_text(text: str) -> str:
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = text.replace("\ufeff", "")
    text = re.sub(r"[ \t]+\n", "\n", text)
    return text


def strip_gutenberg_boilerplate(raw: str) -> str:
    raw = normalize_text(raw)
    if START_MARKER in raw:
        raw = raw.split(START_MARKER, 1)[1]
    if END_MARKER in raw:
        raw = raw.split(END_MARKER, 1)[0]
    return raw.strip() + "\n"


def split_sections(clean: str) -> list[tuple[str, str]]:
    lines = clean.splitlines()
    starts: list[tuple[int, str]] = [(0, "Front Matter")]
    heading_re = re.compile(r"^Chapter ([IVXLCDM]+)\.$")
    for idx, line in enumerate(lines):
        stripped = line.strip()
        if line == stripped and heading_re.match(stripped):
            starts.append((idx, stripped))

    sections: list[tuple[str, str]] = []
    for pos, (start, title) in enumerate(starts):
        end = starts[pos + 1][0] if pos + 1 < len(starts) else len(lines)
        body = "\n".join(lines[start:end]).strip() + "\n"
        sections.append((title, body))
    return sections


def write_markdown_sections(sections: list[tuple[str, str]]) -> None:
    out_dir = ROOT / "chapters" / "src"
    out_dir.mkdir(parents=True, exist_ok=True)
    for old in out_dir.glob("*.md"):
        old.unlink()

    toc = []
    for index, (title, body) in enumerate(sections, start=1):
        filename = f"{index:03d}_{slugify(title)}.md"
        path = out_dir / filename
        path.write_text(f"# {title}\n\n{body}", encoding="utf-8")
        toc.append({"index": index, "title": title, "filename": filename})

    (ROOT / "source" / "toc.json").write_text(
        json.dumps(toc, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def update_state(section_count: int) -> None:
    state_path = ROOT / "state" / "pipeline_state.json"
    state = json.loads(state_path.read_text(encoding="utf-8"))
    state.update(
        {
            "template_root": "template/epub_pipeline/en-zh-Hans",
            "project_root": "books/zh-Hans/3_pg19141_edisons_conquest_of_mars",
            "source_url": SOURCE_URL,
            "status": "SOURCE_SPLIT",
            "chapters_total": section_count,
            "chapters_translated": 0,
            "chapters_reviewed": 0,
            "current_step": "source_ingested_cleaned_split",
            "last_error": "",
        }
    )
    state["quality_gate"]["rights_check"] = "metadata/rights_checklist.md"
    state_path.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")


def main() -> None:
    source_dir = ROOT / "source"
    raw_path = source_dir / "source_text_raw.txt"
    clean_path = source_dir / "source_text.txt"
    raw = raw_path.read_text(encoding="utf-8")
    clean = strip_gutenberg_boilerplate(raw)
    clean_path.write_text(clean, encoding="utf-8")

    sections = split_sections(clean)
    manifest = {
        "source_url": SOURCE_URL,
        "source_page_url": SOURCE_PAGE_URL,
        "duplicate_reference_url": "https://www.gutenberg.org/ebooks/21670",
        "retrieved_at_utc": datetime.now(timezone.utc).isoformat(),
        "raw_sha256": hashlib.sha256(raw.encode("utf-8")).hexdigest(),
        "clean_sha256": hashlib.sha256(clean.encode("utf-8")).hexdigest(),
        "raw_bytes": len(raw.encode("utf-8")),
        "clean_bytes": len(clean.encode("utf-8")),
        "section_count": len(sections),
    }
    (source_dir / "source_manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    write_markdown_sections(sections)
    update_state(len(sections))
    print(f"split_sections={len(sections)}")


if __name__ == "__main__":
    main()
