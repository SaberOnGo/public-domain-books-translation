"""Content-level alignment check for bilingual parallel EPUBs.

check_bilingual_parallel.py proves structure: IDs, hashes, order, language tags. It cannot see that a
target block translates its neighbour, which is how a whole run of pairs drifts by one unit while every
count still matches. This script reads the finished bilingual EPUB and compares each source block with
its own target block and with the neighbouring target blocks, using anchors that survive translation:
numbers, note markers, and words left in the source script (names, Latin terms, original lines).

- error   misaligned_run: two or more consecutive anchored pairs match a neighbour better than their own block.
- warning length_ratio_high / length_ratio_low: target much longer or shorter than the book's norm
          (possible addition, omission, or text moved across a pair boundary).

本脚本按“锚点”（数字、注号、未译出的原文词）检查双语对照版的每一对原文/译文块是否真的对应，
找出整段错开一格的对齐漂移，并按长度比标出可能的增写或漏译。
"""
from __future__ import annotations

import argparse
import json
import math
import posixpath
import re
import sys
import zipfile
from dataclasses import dataclass
from html.parser import HTMLParser
from pathlib import Path
from xml.etree import ElementTree as ET


DEFAULT_BOOK_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_REPORT = "output/bilingual_alignment_check.json"
CJK_RE = re.compile(r"[぀-ヿ㐀-䶿一-鿿豈-﫿]")
CJK_RUN_RE = re.compile(r"[぀-ヿ㐀-䶿一-鿿豈-﫿]{2,}")
LATIN_WORD_RE = re.compile(r"[A-Za-zÀ-ÖØ-öø-ÿĀ-ž][A-Za-zÀ-ÖØ-öø-ÿĀ-ž'’-]{2,}")
DIGITS_RE = re.compile(r"\d+")
NOTE_RE = re.compile(r"\[(\d{1,4})\]")
FULLWIDTH_DIGITS = str.maketrans("０１２３４５６７８９", "0123456789")
SHIFT_MARGIN = 0.34
OWN_SCORE_CEILING = 0.6
MIN_RUN = 2
MAX_GAP = 2
MAX_REPORTED = 40


@dataclass
class Pair:
    index: int
    document: str
    unit_id: str
    source: str
    target: str


class PairCollector(HTMLParser):
    """Collect (source text, target text) for every section.bitext-unit in document order."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.depth = 0
        self.unit_depth: int | None = None
        self.side: str | None = None
        self.side_depth: int | None = None
        self.unit_id = ""
        self.buffers = {"source": [], "target": []}
        self.pairs: list[tuple[str, str, str]] = []

    def handle_starttag(self, tag: str, attrs: list) -> None:
        self.depth += 1
        values = dict(attrs)
        classes = (values.get("class") or "").split()
        if tag == "br" and self.side:
            self.buffers[self.side].append(" ")
        if "bitext-unit" in classes and self.unit_depth is None:
            self.unit_depth = self.depth
            self.unit_id = values.get("data-align-id") or values.get("data-unit-id") or ""
            self.buffers = {"source": [], "target": []}
        elif self.unit_depth is not None and self.side is None:
            if "bitext-source" in classes:
                self.side, self.side_depth = "source", self.depth
            elif "bitext-target" in classes:
                self.side, self.side_depth = "target", self.depth
        if tag in {"br", "img", "meta", "link", "hr"}:
            self.depth -= 1

    def handle_startendtag(self, tag: str, attrs: list) -> None:
        if tag == "br" and self.side:
            self.buffers[self.side].append(" ")

    def handle_endtag(self, tag: str) -> None:
        if self.side is not None and self.depth == self.side_depth:
            self.side, self.side_depth = None, None
        if self.unit_depth is not None and self.depth == self.unit_depth:
            source = " ".join("".join(self.buffers["source"]).split())
            target = " ".join("".join(self.buffers["target"]).split())
            self.pairs.append((self.unit_id, source, target))
            self.unit_depth = None
        self.depth -= 1

    def handle_data(self, data: str) -> None:
        if self.side:
            self.buffers[self.side].append(data)


def local(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


def read_pairs(path: Path) -> list[Pair]:
    pairs: list[Pair] = []
    with zipfile.ZipFile(path) as archive:
        container = ET.fromstring(archive.read("META-INF/container.xml"))
        opf_path = next(el.attrib["full-path"] for el in container.iter() if local(el.tag) == "rootfile")
        base = posixpath.dirname(opf_path)
        opf = ET.fromstring(archive.read(opf_path))
        manifest = {el.attrib.get("id"): el.attrib for el in opf.iter() if local(el.tag) == "item"}
        for el in opf.iter():
            if local(el.tag) != "itemref":
                continue
            item = manifest.get(el.attrib.get("idref"))
            if not item or "html" not in item.get("media-type", ""):
                continue
            href = posixpath.normpath(posixpath.join(base, item.get("href", "")))
            try:
                raw = archive.read(href).decode("utf-8", "replace")
            except KeyError:
                continue
            if "bitext-unit" not in raw:
                continue
            collector = PairCollector()
            collector.feed(raw)
            for unit_id, source, target in collector.pairs:
                pairs.append(Pair(len(pairs), href, unit_id, source, target))
    return pairs


def script_of(text: str) -> str:
    cjk = len(CJK_RE.findall(text))
    latin = len(LATIN_WORD_RE.findall(text))
    return "cjk" if cjk >= latin else "latin"


def measure(text: str, script: str) -> int:
    return len(CJK_RE.findall(text)) if script == "cjk" else len(LATIN_WORD_RE.findall(text))


def digit_set(text: str) -> set[str]:
    text = NOTE_RE.sub(" ", text.translate(FULLWIDTH_DIGITS))
    return {match.lstrip("0") or "0" for match in DIGITS_RE.findall(text)}


def foreign_tokens(target: str, source_script: str) -> set[str]:
    """Tokens written in the source script inside the target block (names, terms, original lines)."""
    if source_script == "latin":
        return {word.lower() for word in LATIN_WORD_RE.findall(target)}
    return set(CJK_RUN_RE.findall(target))


def source_index(source: str, source_script: str) -> set[str] | str:
    return {word.lower() for word in LATIN_WORD_RE.findall(source)} if source_script == "latin" else source


LENGTH_TOLERANCE = 0.7  # log-ratio scale of the length-fit score
STRONG_MISFIT = 0.2
EXTREME_MISFIT = 0.06
# Labelled translator supplements are target-only by design; they must not count as misalignment.
TRANSLATOR_NOTE_RE = re.compile(r"(?:译制补注|译者补注|译注|译者注|Translator['’]s note|Translator note)\s*[:：].*$", re.IGNORECASE | re.DOTALL)


def length_fit(src_len: int, tgt_len: int, median_ratio: float) -> float:
    """1.0 when the target length is what the book's median ratio predicts, falling towards 0 as it diverges."""
    smoothing = max(median_ratio * 2.0, 2.0)
    expected = median_ratio * src_len + smoothing
    return math.exp(-abs(math.log((tgt_len + smoothing) / expected)) / LENGTH_TOLERANCE)


def similarity(src: dict, tgt: dict, source_script: str, median_ratio: float | None = None) -> float | None:
    parts: list[float] = []
    fit = None
    if median_ratio is not None:
        fit = length_fit(src["length"], tgt["length"], median_ratio)
        parts.append(fit)
    tokens = tgt["foreign"]
    if tokens:
        index = src["index"]
        found = sum(1 for token in tokens if (token in index))
        parts.append(found / len(tokens))
    digits = src["digits"] | tgt["digits"]
    if digits:
        parts.append(len(src["digits"] & tgt["digits"]) / len(digits))
    notes = src["notes"] | tgt["notes"]
    if notes:
        parts.append(len(src["notes"] & tgt["notes"]) / len(notes))
    if not parts:
        return None
    score = sum(parts) / len(parts)
    # Shared names or a quoted original line cannot rescue a pair whose lengths are wildly incompatible.
    return min(score, 0.3) if fit is not None and fit < 0.1 else score


def analyse(pairs: list[Pair]) -> dict:
    sample_source = " ".join(pair.source for pair in pairs[:400])
    sample_target = " ".join(pair.target for pair in pairs[:400])
    source_script, target_script = script_of(sample_source), script_of(sample_target)
    feats_src = [{
        "index": source_index(pair.source, source_script),
        "digits": digit_set(pair.source),
        "notes": set(NOTE_RE.findall(pair.source)),
        "length": measure(pair.source, source_script),
    } for pair in pairs]
    feats_tgt = [{
        "foreign": foreign_tokens(pair.target, source_script) if source_script != target_script else set(),
        "digits": digit_set(pair.target),
        "notes": set(NOTE_RE.findall(pair.target)),
        "length": measure(TRANSLATOR_NOTE_RE.sub("", pair.target), target_script),
    } for pair in pairs]

    ratios: list[tuple[int, float]] = []
    for pair, src, tgt in zip(pairs, feats_src, feats_tgt):
        enough = src["length"] >= (12 if source_script == "latin" else 20)
        if enough and tgt["length"]:
            ratios.append((pair.index, tgt["length"] / src["length"]))
    logs = sorted(math.log(value) for _, value in ratios)
    median = logs[len(logs) // 2] if logs else 0.0
    median_ratio = math.exp(median) if logs else None

    shifted: list[tuple[int, int, float, float]] = []  # (index, offset, own, neighbour)
    for i in range(len(pairs)):
        own = similarity(feats_src[i], feats_tgt[i], source_script, median_ratio)
        if own is None or own >= OWN_SCORE_CEILING:
            continue
        best_offset, best = 0, own
        for offset in (-1, 1):
            j = i + offset
            if 0 <= j < len(pairs) and pairs[j].document == pairs[i].document:
                score = similarity(feats_src[i], feats_tgt[j], source_script, median_ratio)
                if score is not None and score > best:
                    best_offset, best = offset, score
        if best_offset and best >= own + SHIFT_MARGIN:
            shifted.append((i, best_offset, own, best))

    runs: list[list[tuple[int, int, float, float]]] = []
    for item in shifted:
        if runs and item[1] == runs[-1][-1][1] and item[0] - runs[-1][-1][0] <= MAX_GAP + 1:
            runs[-1].append(item)
        else:
            runs.append([item])
    # A real drift shows at least one pair that is badly wrong on its own, not just slightly worse.
    misaligned = [run for run in runs if len(run) >= MIN_RUN and min(own for _, _, own, _ in run) <= STRONG_MISFIT]

    # A heading or short line paired with a whole paragraph (or the reverse) is wrong even without a neighbour match.
    extreme: list[int] = []
    untranslated: list[int] = []
    long_source = 25 if source_script == "latin" else 40
    long_target = 25 if target_script == "latin" else 40
    if median_ratio is not None:
        for i, (src, tgt) in enumerate(zip(feats_src, feats_tgt)):
            # A target block written only in the source script (kept verse, a constructed language,
            # an untranslated quotation) is a translation decision to review, not a pairing error.
            if source_script != target_script and tgt["length"] < 2 and src["length"] >= 5:
                untranslated.append(i)
                continue
            if src["length"] < long_source and tgt["length"] < long_target:
                continue
            if length_fit(src["length"], tgt["length"], median_ratio) < EXTREME_MISFIT:
                extreme.append(i)
    high, low = [], []
    for index, value in ratios:
        deviation = math.log(value) - median
        if deviation > math.log(2.0):
            high.append((deviation, index, value))
        elif deviation < math.log(0.45):
            low.append((deviation, index, value))
    high.sort(reverse=True)
    low.sort()

    def show(index: int) -> dict:
        pair = pairs[index]
        return {"document": pair.document, "unit_id": pair.unit_id,
                "source": pair.source[:160], "target": pair.target[:120]}

    issues = []
    for run in misaligned[:MAX_REPORTED]:
        first, last = run[0][0], run[-1][0]
        issues.append({
            "rule": "misaligned_run",
            "severity": "error",
            "message_zh": "连续多对原文/译文块与相邻块更吻合，疑似整体错开一格",
            "message_en": "consecutive pairs match a neighbouring block better than their own; the run looks shifted",
            "offset": run[0][1],
            "pairs_in_run": len(run),
            "first": show(first),
            "last": show(last),
            "evidence": [{"index": i, "own_score": round(own, 2), "neighbour_score": round(best, 2)} for i, _, own, best in run[:6]],
        })
    for index in extreme[:MAX_REPORTED]:
        issues.append({"rule": "extreme_length_mismatch", "severity": "error",
                       "message_zh": "原文块与译文块长度极不相称（如小标题配整段译文），对照关系错误",
                       "message_en": "source and target block lengths are incompatible (e.g. a heading paired with a paragraph)",
                       "source_length": feats_src[index]["length"], "target_length": feats_tgt[index]["length"], **show(index)})
    for index in untranslated[:MAX_REPORTED]:
        issues.append({"rule": "untranslated_block", "severity": "warning",
                       "message_zh": "译文块里没有目标语文字（保留原文的诗句、构造语言或引文）；确认是有意保留",
                       "message_en": "target block has no target-language text (kept verse, constructed language or quotation); confirm it is intentional",
                       **show(index)})
    for deviation, index, value in high[:MAX_REPORTED]:
        issues.append({"rule": "length_ratio_high", "severity": "warning",
                       "message_zh": "译文远长于全书常态，可能有增写或吸收了邻段内容",
                       "message_en": "target much longer than the book's norm: possible addition or absorbed neighbour text",
                       "ratio": round(value, 2), "book_median": round(math.exp(median), 2), **show(index)})
    for deviation, index, value in low[:MAX_REPORTED]:
        issues.append({"rule": "length_ratio_low", "severity": "warning",
                       "message_zh": "译文远短于全书常态，可能有漏译或内容被挪到邻段",
                       "message_en": "target much shorter than the book's norm: possible omission or text moved to a neighbour",
                       "ratio": round(value, 2), "book_median": round(math.exp(median), 2), **show(index)})
    return {
        "pair_count": len(pairs),
        "source_script": source_script,
        "target_script": target_script,
        "anchored_pairs": sum(1 for i in range(len(pairs)) if similarity(feats_src[i], feats_tgt[i], source_script) is not None),
        "median_length_ratio": round(median_ratio, 3) if median_ratio else None,
        "misaligned_runs": len(misaligned),
        "misaligned_pairs": sum(len(run) for run in misaligned),
        "extreme_length_mismatches": len(extreme),
        "untranslated_blocks": len(untranslated),
        "length_ratio_high": len(high),
        "length_ratio_low": len(low),
        "status": "FAIL" if (misaligned or extreme) else "PASS",
        "issues": issues,
    }


def read_json(path: Path) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8-sig"))
    except (OSError, json.JSONDecodeError):
        return {}


def bilingual_artifact(book_root: Path) -> Path | None:
    state = read_json(book_root / "state" / "pipeline_state.json")
    enabled = state.get("edition_type") == "bilingual_parallel"
    artifact = "output/book_bilingual_parallel.epub"
    for item in state.get("output_editions") or []:
        if isinstance(item, dict) and item.get("edition_type") == "bilingual_parallel":
            enabled = enabled or item.get("enabled") is True
            artifact = str(item.get("artifact") or artifact)
    return (book_root / artifact) if enabled else None


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Check that each bilingual source block is paired with its own translation.")
    parser.add_argument("--book-root", default=None, help="Book project root (defaults to the parent of scripts/).")
    parser.add_argument("--epub", action="append", default=[], help="Bilingual EPUB to check; repeatable.")
    parser.add_argument("--write-report", action="store_true", help=f"Write {DEFAULT_REPORT} under the book root.")
    parser.add_argument("--report", default=None, help="Explicit report path.")
    parser.add_argument("--warn-only", action="store_true", help="Exit 0 even when misaligned runs are found.")
    return parser.parse_args()


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    args = parse_args()
    book_root = Path(args.book_root).resolve() if args.book_root else DEFAULT_BOOK_ROOT
    targets = [Path(value).resolve() for value in args.epub]
    if not targets:
        artifact = bilingual_artifact(book_root)
        if artifact is None:
            print("bilingual alignment check skipped: bilingual edition disabled")
            return 0
        if not artifact.is_file():
            print(f"ERROR: bilingual EPUB not found: {artifact}")
            return 1
        targets = [artifact]
    results = []
    for path in targets:
        result = analyse(read_pairs(path))
        try:
            result["epub"] = path.relative_to(book_root if not args.epub else Path.cwd().resolve()).as_posix()
        except ValueError:
            result["epub"] = path.name
        results.append(result)
        print(f"{result['status']} pairs={result['pair_count']} anchored={result['anchored_pairs']} "
              f"misaligned_runs={result['misaligned_runs']} misaligned_pairs={result['misaligned_pairs']} "
              f"extreme={result['extreme_length_mismatches']} "
              f"ratio_high={result['length_ratio_high']} ratio_low={result['length_ratio_low']} {path.name}")
    report_path = Path(args.report).resolve() if args.report else (book_root / DEFAULT_REPORT if args.write_report else None)
    if report_path is not None:
        report_path.parent.mkdir(parents=True, exist_ok=True)
        status = "FAIL" if any(item["status"] == "FAIL" for item in results) else "PASS"
        report_path.write_text(json.dumps({"schema_version": "1.0", "status": status, "results": results},
                                          ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    failed = any(item["status"] == "FAIL" for item in results)
    return 0 if (args.warn_only or not failed) else 1


if __name__ == "__main__":
    raise SystemExit(main())
