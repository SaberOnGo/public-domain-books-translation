# LifeBook Digest

<table align="center">
  <tr>
    <td align="center"><h3><a href="../../digest/README.md">简体中文</a></h3></td>
    <td align="center"><h3><a href="./README.zh-TW.md">繁體中文</a></h3></td>
    <td align="center"><h3><a href="./README.en.md">English</a></h3></td>
    <td align="center"><h3><a href="./README.ja.md">日本語</a></h3></td>
  </tr>
</table>

LifeBook Digest is an optional post-EPUB module for the LifeBook translation publishing system. It lives in the repository-level `digest/` directory and does not take over the existing translation, EPUB build, random review, or release pipeline.

## Quick Start

<table align="center">
  <tr>
    <td align="center"><a href="../../digest/README.md#快速开始--quick-start">简体中文</a></td>
    <td align="center"><a href="./README.zh-TW.md#快速開始--quick-start">繁體中文</a></td>
    <td align="center"><a href="./README.en.md#quick-start">English</a></td>
    <td align="center"><a href="./README.ja.md#クイックスタート--quick-start">日本語</a></td>
  </tr>
</table>

Create `digest.config.json` in a concrete book project:

```json
{
  "enabled": true,
  "merge_into_epub": true,
  "source_epub": "output/book.epub",
  "output_epub": "output/book_digest.epub",
  "title": "Book Digest",
  "language": "en",
  "max_section_chars": 240
}
```

Run from the repository root:

```powershell
python -m digest.lifebook_digest --book-root books/{target}/{number}_{目标语言书名}_{目标语言作者名}
```

## Boundary

- Input is an already built standard EPUB, defaulting to `output/book.epub`.
- Each book controls the feature through its own `digest.config.json`.
- Sidecar mode writes `output/digest/digest.xhtml`, `output/digest/digest_state.json`, and `qa/digest/digest_report.json`.
- Merge mode writes a new standard EPUB, defaulting to `output/book_digest.epub`.
- Merge mode adds one reader-visible chapter and updates OPF manifest, spine, and nav.
- Existing body text, cover, book-info page, frontmatter, and translation QA records are not rewritten.
- `digest_state.json` stores lightweight topology nodes and reading-order edges for later review or visualization.

## Quality Expectations

If the digest chapter is merged into an EPUB, validate the resulting EPUB with the book project's own gates before publishing it. Digest text is reader-facing content; future LLM output must be reviewed before release.

## Acknowledgement

This module is inspired by [spinedigest](https://github.com/oomol-lab/spinedigest). Thanks to that project for demonstrating long-text summarization, chapter topology, and reusable intermediate processing state. LifeBook Digest remains a separate LifeBook post-processing module and keeps EPUB as the reader-facing output format.

## License

See [DIGEST_LICENSE.en.md](../../license/DIGEST_LICENSE.en.md).

