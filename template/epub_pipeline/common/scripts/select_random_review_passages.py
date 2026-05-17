from __future__ import annotations

import argparse
import json
import random
import secrets
from dataclasses import dataclass
from pathlib import Path


BOOK_ROOT = Path(__file__).resolve().parents[1]


@dataclass(frozen=True)
class Paragraph:
    id: str
    file: str
    heading: str
    paragraph_index: int
    text: str


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Select auditable random paragraph samples for independent review agents.")
    parser.add_argument("--source-dir", default="chapters/final", help="Directory containing reader-facing Markdown chapters.")
    parser.add_argument("--output-dir", default="reviews/random_spotcheck", help="Output directory for sample manifests.")
    parser.add_argument("--agents", type=int, default=2, help="Number of independent reviewer sample sets.")
    parser.add_argument("--samples-per-agent", type=int, default=10, help="Minimum random paragraphs per agent.")
    parser.add_argument("--seed", default=None, help="Optional seed. If omitted, a random seed is generated and recorded.")
    return parser.parse_args()


def normalize(text: str) -> str:
    return " ".join(text.replace("\r\n", "\n").split())


def paragraphs_from_file(path: Path) -> list[Paragraph]:
    rel = path.relative_to(BOOK_ROOT).as_posix()
    text = path.read_text(encoding="utf-8").replace("\r\n", "\n")
    blocks = [block.strip() for block in text.split("\n\n") if block.strip()]
    heading = ""
    out: list[Paragraph] = []
    para_index = 0

    for block in blocks:
        first = block.splitlines()[0].strip()
        if first.startswith("#"):
            heading = first.lstrip("#").strip()
            continue
        if block.startswith("```") or block.startswith("|") or block.startswith("!["):
            continue
        if block.startswith(">"):
            continue
        plain = normalize(block)
        if len(plain) < 40:
            continue
        para_index += 1
        out.append(Paragraph(
            id=f"{path.stem}::p{para_index:04d}",
            file=rel,
            heading=heading,
            paragraph_index=para_index,
            text=plain,
        ))
    return out


def collect_paragraphs(source_dir: Path) -> list[Paragraph]:
    if not source_dir.exists():
        raise SystemExit(f"source directory does not exist: {source_dir}")
    paragraphs: list[Paragraph] = []
    for path in sorted(source_dir.rglob("*.md")):
        paragraphs.extend(paragraphs_from_file(path))
    return paragraphs


def write_agent_samples(output_dir: Path, agent_name: str, samples: list[Paragraph], seed: str) -> None:
    lines = [
        f"# {agent_name} 随机段落抽检样本",
        "",
        f"seed: `{seed}`",
        f"samples: `{len(samples)}`",
        "",
        "## 评审要求",
        "",
        "- 假设自己是认真阅读本书的中文读者。",
        "- 严格依据模板、本书文体画像、章节控制、数学/天文学证明控制和 EPUB 读者版要求检查。",
        "- 每段必须给出 0-100 分、问题类型、是否需要精校返工、简短理由。",
        "- 若任何段落存在读不懂、数学证明链断裂、天文学概念误导、术语/数值/图表关系错误，即使总分达标也必须判为返工。",
        "- 抽检平均分必须 >= 75，且不得有单段 < 70，才可认为本 agent 抽检通过。",
        "",
        "## 抽检段落",
        "",
    ]
    for idx, sample in enumerate(samples, 1):
        lines.extend([
            f"### Sample {idx}: `{sample.id}`",
            "",
            f"- file: `{sample.file}`",
            f"- heading: `{sample.heading or '(none)'}`",
            f"- paragraph_index: `{sample.paragraph_index}`",
            "",
            sample.text,
            "",
            "| score | issue_type | rework_required | reason |",
            "| --- | --- | --- | --- |",
            "|  |  |  |  |",
            "",
        ])
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / f"{agent_name.lower()}_samples.md").write_text("\n".join(lines), encoding="utf-8", newline="\n")


def main() -> None:
    args = parse_args()
    source_dir = (BOOK_ROOT / args.source_dir).resolve()
    output_dir = (BOOK_ROOT / args.output_dir).resolve()
    seed = args.seed or secrets.token_hex(16)
    rng = random.Random(seed)
    paragraphs = collect_paragraphs(source_dir)
    required = args.agents * args.samples_per_agent
    if len(paragraphs) < required:
        raise SystemExit(
            f"not enough paragraphs for independent random sampling: have {len(paragraphs)}, need at least {required}"
        )

    shuffled = paragraphs[:]
    rng.shuffle(shuffled)
    manifest = {
        "seed": seed,
        "source_dir": str(source_dir.relative_to(BOOK_ROOT).as_posix()),
        "agents": args.agents,
        "samples_per_agent": args.samples_per_agent,
        "total_candidate_paragraphs": len(paragraphs),
        "sample_sets": {},
    }

    for agent_index in range(args.agents):
        name = f"agent_{chr(ord('a') + agent_index)}"
        start = agent_index * args.samples_per_agent
        end = start + args.samples_per_agent
        samples = shuffled[start:end]
        write_agent_samples(output_dir, name, samples, seed)
        manifest["sample_sets"][name] = [sample.id for sample in samples]

    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "random_sample_manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2),
        encoding="utf-8",
        newline="\n",
    )
    print(f"wrote random review samples to {output_dir.relative_to(BOOK_ROOT)}")
    print(f"seed={seed}")


if __name__ == "__main__":
    main()
