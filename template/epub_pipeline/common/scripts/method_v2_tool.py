#!/usr/bin/env python3
"""Helper for translation method v2 (see references/translation_method_v2.md).

Subcommands / 子命令:
  prepare <book_dir>                 build qa/method_v2/_shared and chNNN/source_numbered.md + terms_hits.md
  recheck <book_dir> <NNN> <old> <new>  list paragraphs changed between two numbered files (+1 neighbour each side)
                                     and write chNNN/input_recheck.md (source + current target)
  check   <book_dir> <NNN> <target>  structural check of a finished chapter against the source numbering

Paths are resolved from the book directory argument; nothing is hard-coded.
路径全部由书籍目录参数解析，不写死本机路径。
"""
import argparse
import csv
import re
import sys
from pathlib import Path

PID = re.compile(r"^\[(P\d+)\]\s*(.*)$")
CJK = re.compile(r"[一-鿿]")


def out(text):
    sys.stdout.buffer.write((text + "\n").encode("utf-8"))


def paragraphs(text):
    """Return (headings, [(id, text)]) from a blank-line separated file with optional [Pnn] ids."""
    blocks = [b.strip() for b in re.split(r"\n\s*\n", text) if b.strip()]
    cut = max((i + 1 for i, b in enumerate(blocks[:3]) if b.startswith("#")), default=0)
    heads, paras = blocks[:cut], blocks[cut:]
    return heads, paras


def read_numbered(path):
    paras, notes, in_notes = {}, [], False
    for line in Path(path).read_text(encoding="utf-8").splitlines():
        if line.strip().startswith("## 注释"):
            in_notes = True
            continue
        m = PID.match(line.strip())
        if m and not in_notes:
            paras[m.group(1)] = m.group(2).strip()
        elif in_notes and line.strip():
            notes.append(line.strip())
    return paras, notes


def brief_sections(brief_text):
    parts = re.split(r"(?m)^## ", brief_text)
    sections = {}
    for part in parts[1:]:
        num = re.match(r"(\d+)\.", part)
        if num:
            sections[int(num.group(1))] = "## " + part.rstrip() + "\n"
    return sections


def prepare(book):
    src_dir, qa = book / "chapters/src", book / "qa/method_v2"
    shared = qa / "_shared"
    shared.mkdir(parents=True, exist_ok=True)
    brief = (book / "preproduction/translator_brief.md").read_text(encoding="utf-8")
    sec = brief_sections(brief)
    (shared / "brief_full.md").write_text(brief, encoding="utf-8")
    (shared / "brief_7_8.md").write_text(sec.get(7, "") + "\n" + sec.get(8, ""), encoding="utf-8")
    (shared / "brief_2_3_11.md").write_text("\n".join(sec.get(n, "") for n in (2, 3, 11)), encoding="utf-8")
    profile = sec.get(1, "")
    body = [l for l in profile.splitlines()[1:] if l.strip()]
    (shared / "reader_profile.txt").write_text("\n".join(body), encoding="utf-8")
    terms = list(csv.DictReader((book / "glossary/terms.csv").open(encoding="utf-8")))
    for path in sorted(src_dir.glob("*.md")):
        num = path.name.split("_")[0]
        cdir = qa / f"ch{num}"
        cdir.mkdir(parents=True, exist_ok=True)
        heads, paras = paragraphs(path.read_text(encoding="utf-8"))
        lines = list(heads) + [""]
        for i, p in enumerate(paras, 1):
            lines.append(f"[P{i:02d}] " + " ".join(p.split()))
            lines.append("")
        (cdir / "source_numbered.md").write_text("\n".join(lines), encoding="utf-8")
        old_final = next((book / "chapters/final").glob(f"{num}_*.md"), None)
        if old_final:
            zh_heads, _ = paragraphs(old_final.read_text(encoding="utf-8"))
            (cdir / "heading_zh.md").write_text("\n\n".join(zh_heads) + "\n", encoding="utf-8")
        whole = "\n".join(paras)
        hits = []
        for row in terms:
            s = (row.get("source_term") or "").strip()
            if s and re.search(r"(?<![A-Za-z])" + re.escape(s) + r"(?![A-Za-z])", whole):
                forbid = row.get("forbidden_body_renderings") or ""
                hits.append(f"{s} → {row['target_term']}  [{row.get('domain','')}; {row.get('term_control','')}"
                            + (f"; 禁用:{forbid}" if forbid else "") + "]")
        (cdir / "terms_hits.md").write_text("\n".join(hits) + "\n", encoding="utf-8")
        out(f"ch{num}: {len(paras)} paragraphs, {sum(len(p) for p in paras)} source chars, {len(hits)} term hits")


def recheck(book, num, old, new):
    cdir = book / f"qa/method_v2/ch{num}"
    src, _ = read_numbered(cdir / "source_numbered.md")
    a, _ = read_numbered(old)
    b, _ = read_numbered(new)
    ids = sorted(src, key=lambda k: int(k[1:]))
    changed = [i for i in ids if a.get(i) != b.get(i)]
    keep = set()
    for i in changed:
        n = ids.index(i)
        keep.update(ids[max(0, n - 1):n + 2])
    lines = []
    for i in ids:
        if i in keep:
            lines += [f"### {i}", f"原文：{src[i]}", f"译文：{b.get(i, '')}", ""]
    (cdir / "input_recheck.md").write_text("\n".join(lines), encoding="utf-8")
    out(f"changed {len(changed)} / {len(ids)}; recheck covers {len(keep)} paragraphs")
    out("changed ids: " + " ".join(changed))


def check(book, num, target):
    cdir = book / f"qa/method_v2/ch{num}"
    src, _ = read_numbered(cdir / "source_numbered.md")
    tgt, notes = read_numbered(target)
    problems = []
    missing = [i for i in src if i not in tgt]
    extra = [i for i in tgt if i not in src]
    if missing:
        problems.append("missing: " + " ".join(missing))
    if extra:
        problems.append("extra: " + " ".join(extra))
    text = Path(target).read_text(encoding="utf-8")
    if "[疑" in text:
        problems.append("unresolved [疑] marker")
    for i, t in tgt.items():
        if re.fullmatch(r"[\s*_\-—·]+", t):
            continue  # scene-break separator such as "* * *"
        if t.startswith("[IMAGE:"):
            continue  # production image marker keeps its path
        if not CJK.search(t) and len(t) > 12:
            problems.append(f"{i}: no Chinese characters")
        if i in src and len(src[i]) > 80:
            ratio = len(CJK.findall(t)) / max(len(src[i]), 1)
            if ratio < 0.12 or ratio > 0.6:
                problems.append(f"{i}: length ratio {ratio:.2f} (CJK chars / source chars)")
    body_text = re.sub(r"\[P\d+\]", "", text.split("## 注释")[0])
    marks = {int(x) for x in re.findall(r"\[(\d+)\]", body_text)}
    defs = [int(m.group(1)) for n in notes for m in [re.match(r"^\[(\d+)\]", n)] if m]
    if marks != set(defs) or len(defs) != len(set(defs)):
        problems.append(f"note markers {sorted(marks)} do not match note definitions {sorted(defs)}")
    out(f"ch{num}: {len(tgt)}/{len(src)} paragraphs, {len(notes)} note lines")
    for p in problems:
        out("PROBLEM " + p)
    out("CHECK PASS" if not problems else "CHECK FAIL")
    return 0 if not problems else 1


def merge(book, num, out_path, files):
    cdir = book / f"qa/method_v2/ch{num}"
    paras, notes, dup_notes = {}, {}, []
    for f in files:
        p, n = read_numbered(f)
        paras.update(p)
        for line in n:
            m = re.match(r"^\[(\d+)\]", line)
            if m:
                key = int(m.group(1))
                if key in notes and notes[key] != line:
                    out(f"WARNING duplicate note number [{key}] with different text in {f}; renumber the unit's notes")
                    dup_notes.append(key)
                notes[key] = line
    head = (cdir / "heading_zh.md").read_text(encoding="utf-8").strip()
    lines = [head, ""]
    for i in sorted(paras, key=lambda k: int(k[1:])):
        lines += [f"[{i}] {paras[i]}", ""]
    if notes:
        lines += ["## 注释", ""]
        for k in sorted(notes):
            lines += [notes[k], ""]
    Path(out_path).write_text("\n".join(lines), encoding="utf-8")
    out(f"merged {len(paras)} paragraphs, {len(notes)} notes -> {out_path}")
    return 1 if dup_notes else 0


def profile(target):
    import importlib.util
    spec = importlib.util.spec_from_file_location("profile_translationese", Path(__file__).with_name("profile_translationese.py"))
    mod = importlib.util.module_from_spec(spec)
    sys.modules["profile_translationese"] = mod
    spec.loader.exec_module(mod)
    text = Path(target).read_text(encoding="utf-8").split("## 注释")[0]
    text = re.sub(r"\[P\d+\]\s*", "", text)
    text = re.sub(r"\[\d+\]", "", text)
    result = mod.profile_text(mod.clean_markdown(text))
    import json
    out(json.dumps({k: v for k, v in result.items() if k != "examples"}, ensure_ascii=False))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("prepare"); p.add_argument("book")
    p = sub.add_parser("recheck"); p.add_argument("book"); p.add_argument("num"); p.add_argument("old"); p.add_argument("new")
    p = sub.add_parser("check"); p.add_argument("book"); p.add_argument("num"); p.add_argument("target")
    p = sub.add_parser("profile"); p.add_argument("target")
    p = sub.add_parser("merge"); p.add_argument("book"); p.add_argument("num"); p.add_argument("out"); p.add_argument("files", nargs="+")
    a = ap.parse_args()
    if a.cmd == "profile":
        return profile(a.target)
    if a.cmd == "merge":
        sys.exit(merge(Path(a.book).resolve(), a.num, a.out, a.files))
    book = Path(a.book).resolve()
    if a.cmd == "prepare":
        prepare(book)
    elif a.cmd == "recheck":
        recheck(book, a.num, a.old, a.new)
    else:
        sys.exit(check(book, a.num, a.target))


if __name__ == "__main__":
    main()
