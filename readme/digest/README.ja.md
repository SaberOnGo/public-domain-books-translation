# LifeBook Digest

<table align="center">
  <tr>
    <td align="center"><h3><a href="../../digest/README.md">简体中文</a></h3></td>
    <td align="center"><h3><a href="./README.zh-TW.md">繁體中文</a></h3></td>
    <td align="center"><h3><a href="./README.en.md">English</a></h3></td>
    <td align="center"><h3><a href="./README.ja.md">日本語</a></h3></td>
  </tr>
</table>

LifeBook Digest は、LifeBook 翻訳公開システムの任意の EPUB 後処理モジュールです。リポジトリ直下の `digest/` に置かれ、既存の翻訳、EPUB ビルド、ランダム検査、リリース主フローを直接置き換えません。

## クイックスタート / Quick Start

<table align="center">
  <tr>
    <td align="center"><a href="../../digest/README.md#快速开始--quick-start">简体中文</a></td>
    <td align="center"><a href="./README.zh-TW.md#快速開始--quick-start">繁體中文</a></td>
    <td align="center"><a href="./README.en.md#quick-start">English</a></td>
    <td align="center"><a href="./README.ja.md#クイックスタート--quick-start">日本語</a></td>
  </tr>
</table>

具体的な書籍プロジェクトのルートに `digest.config.json` を作成します。

```json
{
  "enabled": true,
  "merge_into_epub": true,
  "source_epub": "output/book.epub",
  "output_epub": "output/book_digest.epub",
  "title": "読書ガイド",
  "language": "ja",
  "max_section_chars": 240
}
```

リポジトリのルートから実行します。

```powershell
python -m digest.lifebook_digest --book-root books/{target}/{number}_{目标语言书名}_{目标语言作者名}
```

## 境界

- 入力はすでに生成済みの標準 EPUB で、既定は `output/book.epub` です。
- 各書籍は自分の `digest.config.json` で有効化と EPUB への統合を制御します。
- サイドカーモードは `output/digest/digest.xhtml`、`output/digest/digest_state.json`、`qa/digest/digest_report.json` を書きます。
- 統合モードは新しい標準 EPUB を出力し、既定は `output/book_digest.epub` です。
- 統合時は読者に見える章を一つ追加し、OPF manifest、spine、nav を更新します。
- 既存の本文、表紙、書籍情報ページ、frontmatter、翻訳 QA 記録は書き換えません。
- `digest_state.json` には軽量なトポロジー node と読書順 edge を保存し、後続レビューや可視化拡張に使えます。

## 品質要件

Digest 章を EPUB に統合する場合、公開前に書籍プロジェクト自身のゲートで新しい EPUB を検証してください。Digest は読者に見える内容です。将来 LLM 出力を接続する場合も、未レビューのまま公開してはいけません。

## 謝辞

本モジュールは [spinedigest](https://github.com/oomol-lab/spinedigest) から着想を得ています。長文要約、章トポロジー、再利用可能な中間処理状態の設計を示した同プロジェクトに感謝します。LifeBook Digest は独立した LifeBook 後処理モジュールであり、読者向け出力は標準 EPUB のままです。

## ライセンス

[DIGEST_LICENSE.ja.md](../../license/DIGEST_LICENSE.ja.md) を参照してください。

