"""Translationese profile for Chinese target text, per chapter.

Counts the surface signals that independent reviews found over-represented in AI Chinese translations
(semicolons, explanatory colons, dashes, third-person and possessive pronouns, the article calque 一个,
hedges such as 某种, stock AI phrasing, Latin-script parentheticals) and the sentence-length distribution.
Rates are per 10,000 CJK characters. A chapter whose rate exceeds the threshold, or whose sentence
length sits outside the band, is listed for review: the reviewer must quote the sentences and rewrite
the ones that really are translationese. This is a signal for review, not a pass/fail verdict on prose,
so the script exits 0 unless --fail-on-flag is given.

中文译文的翻译腔剖面：按章统计分号、解释性冒号、破折号、代词、物主代词、“一个”、某种、AI 套语、
正文外文括注和句长分布（每万汉字）。超出阈值的章节进入复核清单，复核时必须引用具体句子并重写确属
翻译腔的句子。它是复核信号，不是对文笔的放行结论。
"""
from __future__ import annotations

import argparse
import json
import re
import statistics
import sys
from pathlib import Path

DEFAULT_BOOK_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_REPORT = "output/translationese_profile.json"
CJK = re.compile(r"[一-鿿]")

# Thresholds per 10k CJK characters. Native modern Chinese narrative prose stays well below these;
# they sit around 2.5x the rates measured on a native Chinese novel used as the project baseline.
THRESHOLDS = {
    "semicolon": 40.0,
    "explanatory_colon": 25.0,
    "dash": 20.0,
    "pronoun_3p": 300.0,
    "possessive_pronoun": 60.0,
    "yige": 30.0,
    "mouzhong": 3.0,
    "ai_cliche": 10.0,
    "latin_parenthetical": 3.0,
}
SENTENCE_MEAN_BAND = (16.0, 42.0)
LONG_SENTENCE_SHARE_MAX = 15.0  # percent of sentences over 60 CJK characters

PATTERNS = {
    "semicolon": re.compile(r"；"),
    # Speaker labels ("沃尔特：") and colons that introduce quoted speech are ordinary Chinese; the
    # explanatory "X：Y" colon inside narration is the one to watch.
    "explanatory_colon": re.compile(r"(?<![说道问答喊叫写])：(?!\s*[“「『])"),
    "dash": re.compile(r"——"),
    "pronoun_3p": re.compile(r"[他她它](?:们)?"),
    "possessive_pronoun": re.compile(r"[他她它我你](?:们)?的"),
    "yige": re.compile(r"一个"),
    "mouzhong": re.compile(r"某种"),
    "ai_cliche": re.compile(r"一丝|不禁|不由得|缓缓|微微|淡淡|仿佛|宛如|难以言喻|无法言说|涌上心头|心头一"),
    "latin_parenthetical": re.compile(r"[（(][A-Za-zÀ-ÿĀ-ž][^）)]{0,60}[）)]"),
}
SPEAKER_LABEL = re.compile(r"^[一-鿿·]{1,8}：", re.MULTILINE)


def clean_markdown(text: str) -> str:
    text = re.sub(r"<!--.*?-->", "", text, flags=re.DOTALL)
    text = re.sub(r"^#{1,6}\s.*$", "", text, flags=re.MULTILINE)
    text = re.sub(r"<[^>]+>", "", text)
    return SPEAKER_LABEL.sub("", text)


def profile_text(text: str) -> dict:
    n = len(CJK.findall(text)) or 1
    rates = {key: round(len(rx.findall(text)) * 10000 / n, 1) for key, rx in PATTERNS.items()}
    sentences = [s for s in re.split(r"[。！？!?]+", text) if len(CJK.findall(s)) >= 2]
    lengths = [len(CJK.findall(s)) for s in sentences]
    mean = round(statistics.mean(lengths), 1) if lengths else 0.0
    long_share = round(100 * sum(1 for x in lengths if x > 60) / len(lengths), 1) if lengths else 0.0
    flags = [f"{key}={value} (> {THRESHOLDS[key]})" for key, value in rates.items() if value > THRESHOLDS[key]]
    if lengths and not SENTENCE_MEAN_BAND[0] <= mean <= SENTENCE_MEAN_BAND[1]:
        flags.append(f"sentence_mean={mean} (outside {SENTENCE_MEAN_BAND[0]}-{SENTENCE_MEAN_BAND[1]})")
    if long_share > LONG_SENTENCE_SHARE_MAX:
        flags.append(f"long_sentence_share={long_share}% (> {LONG_SENTENCE_SHARE_MAX}%)")
    return {"cjk_chars": n, "rates_per_10k": rates, "sentence_mean": mean, "long_sentence_share_pct": long_share, "flags": flags}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Per-chapter translationese profile for Chinese target text.")
    parser.add_argument("--book-root", default=None, help="Book project root (defaults to the parent of scripts/).")
    parser.add_argument("--source-dir", default="chapters/final", help="Chapter directory relative to the book root.")
    parser.add_argument("--min-chars", type=int, default=1500, help="Skip chapters shorter than this many CJK characters.")
    parser.add_argument("--write-report", action="store_true", help=f"Write {DEFAULT_REPORT}.")
    parser.add_argument("--fail-on-flag", action="store_true", help="Exit 1 when any chapter is flagged.")
    return parser.parse_args()


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    args = parse_args()
    root = Path(args.book_root).resolve() if args.book_root else DEFAULT_BOOK_ROOT
    chapters = sorted((root / args.source_dir).glob("*.md"))
    if not chapters:
        print(f"ERROR: no chapters under {args.source_dir}")
        return 1
    results, book_text = [], []
    for path in chapters:
        text = clean_markdown(path.read_text(encoding="utf-8"))
        book_text.append(text)
        if len(CJK.findall(text)) < args.min_chars:
            continue
        item = profile_text(text)
        item["chapter"] = path.relative_to(root).as_posix()
        results.append(item)
    book = profile_text("\n".join(book_text))
    flagged = [item for item in results if item["flags"]]
    report = {
        "schema_version": "1.0",
        "thresholds_per_10k": THRESHOLDS,
        "sentence_mean_band": SENTENCE_MEAN_BAND,
        "book": book,
        "flagged_chapter_count": len(flagged),
        "chapters": results,
        "review_rule_zh": "列出的章节必须由评审引用具体句子复核；确属翻译腔的按句型重写，不得只换词或只改标点。",
        "review_rule_en": "Flagged chapters need a review that quotes the sentences; rewrite real translationese by sentence pattern, not by swapping words or punctuation.",
    }
    if args.write_report:
        out = root / DEFAULT_REPORT
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"book: {', '.join(book['flags']) or 'no flags'}")
    print(f"flagged chapters: {len(flagged)}/{len(results)}")
    for item in flagged[:20]:
        print(f"  {item['chapter']}: {'; '.join(item['flags'])}")
    return 1 if (args.fail_on_flag and flagged) else 0


if __name__ == "__main__":
    raise SystemExit(main())
