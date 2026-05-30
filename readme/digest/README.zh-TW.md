# LifeBook Digest

<table align="center">
  <tr>
    <td align="center"><h3><a href="../../digest/README.md">简体中文</a></h3></td>
    <td align="center"><h3><a href="./README.zh-TW.md">繁體中文</a></h3></td>
    <td align="center"><h3><a href="./README.en.md">English</a></h3></td>
    <td align="center"><h3><a href="./README.ja.md">日本語</a></h3></td>
  </tr>
</table>

LifeBook Digest 是 LifeBook 翻譯發布系統的可選 EPUB 後處理模組。它位於倉庫根目錄 `digest/`，不直接接管既有翻譯、建置、抽檢或發布主流程。

## 快速開始 / Quick Start

<table align="center">
  <tr>
    <td align="center"><a href="../../digest/README.md#快速开始--quick-start">简体中文</a></td>
    <td align="center"><a href="./README.zh-TW.md#快速開始--quick-start">繁體中文</a></td>
    <td align="center"><a href="./README.en.md#quick-start">English</a></td>
    <td align="center"><a href="./README.ja.md#クイックスタート--quick-start">日本語</a></td>
  </tr>
</table>

在具體書籍工程根目錄建立 `digest.config.json`：

```json
{
  "enabled": true,
  "merge_into_epub": true,
  "source_epub": "output/book.epub",
  "output_epub": "output/book_digest.epub",
  "title": "全書導讀",
  "language": "zh-TW",
  "max_section_chars": 240
}
```

從倉庫根目錄執行：

```powershell
python -m digest.lifebook_digest --book-root books/{target}/{number}_{book_id_slug}
```

## 設計邊界

- 輸入是已經生成的標準 EPUB，預設為 `output/book.epub`。
- 每本書用自己的 `digest.config.json` 控制是否啟用、是否合併。
- 旁路模式寫入 `output/digest/digest.xhtml`、`output/digest/digest_state.json` 和 `qa/digest/digest_report.json`。
- 合併模式輸出新的標準 EPUB，預設為 `output/book_digest.epub`。
- 合併只新增一個讀者可見章節，並更新 OPF manifest、spine 和 nav。
- 既有正文、封面、書籍資訊頁、前置頁和翻譯 QA 記錄不會被重寫。
- `digest_state.json` 保存輕量拓撲節點和閱讀順序邊，供後續審校或視覺化擴展。

## 品質要求

若 Digest 章節合併進 EPUB，正式發布前必須按書籍工程自己的門禁驗證新 EPUB。Digest 是讀者可見內容；未來若接入 LLM 輸出，不能未審校即發布。

## 致謝

本模組的方向受到 [spinedigest](https://github.com/oomol-lab/spinedigest) 啟發，感謝該專案展示長文本摘要、章節拓撲和可復用中間狀態的設計思路。LifeBook Digest 仍是獨立的 LifeBook 後處理模組，讀者輸出格式保持為標準 EPUB。

## 授權

見 [DIGEST_LICENSE.zh-TW.md](../../license/DIGEST_LICENSE.zh-TW.md)。

