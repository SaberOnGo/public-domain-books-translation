# LifeBook 書坊公版書翻譯專案

<table align="center">
  <tr>
    <td align="center"><h3><a href="../README.zh-CN.md">简体中文</a></h3></td>
    <td align="center"><h3><a href="./README.zh-TW.md">繁體中文</a></h3></td>
    <td align="center"><h3><a href="../README.md">English</a></h3></td>
    <td align="center"><h3><a href="./README.ja.md">日本語</a></h3></td>
  </tr>
</table>

LifeBook 書坊是一套多語言公版書翻譯與 EPUB 製作流程。它不是把 AI 初稿直接發布的專案，而是保留來源證據、版權核查、初譯、審校、EPUB 校驗、分層隨機抽檢和版本化發布，方便人與 AI 一起複核。

不會寫程式也可以參與：推薦書、查公版來源、試讀章節、對照原文、回報彆扭句子、測試 EPUB，或改進模板和腳本都很有價值。

## 快速開始

簡短使用說明：

- [繁體中文說明](../doc/public/how-to-use-prompts.zh-TW.md)
- [简体中文说明](../doc/public/how-to-use-prompts.zh-CN.md)
- [English guide](../doc/public/how-to-use-prompts.en.md)
- [日本語ガイド](../doc/public/how-to-use-prompts.ja.md)

給 AI 用戶端的最小提示：

```text
我要翻譯的書：{書名、作者（可選）；如果已有可靠來源 URL，也可以貼上}
目標語言：{例如 繁體中文、英文、日文、西班牙文}

請自動選擇正確的翻譯 prompt：
- 如已有對應源語言模板，執行 doc/public/user_prompt/book_translation_existing_template.md。
- 如無對應源語言模板，執行 doc/public/user_prompt/book_translation_new_template.md。

除非版權或來源無法確認，不要讓我填寫技術欄位。請自動查找可靠公版來源，自動建立專案，完成翻譯、審校、EPUB 建置、分層隨機抽檢和 release。
```

## AI 用戶端

本倉庫不綁定模型。Codex App、Claude Code、OpenCode、aider、Antigravity 或其他能讀取本機檔案的 AI 用戶端都可以使用，只要它能讀倉庫、改檔、執行命令，並遵守 `AGENTS.md`。

若想讓普通使用者開箱即用，使用 **LifeBook Launcher**：

- Windows 使用者目前可雙擊：`tools\lifebook-launcher\LifeBook Launcher Setup.exe`。
- 發布版使用者只需要下載並雙擊 **LifeBook Launcher** 應用或安裝包；Launcher 會自動準備和更新 LifeBook 專案目錄，Windows 預設專案目錄是 `D:\LifeBook`。
- 倉庫中的原始碼目錄是 `tools/lifebook-launcher/source/`，供開發者打包和維護。
- 它會自動維護 LifeBook 專案更新、檢查/更新 OpenCode Desktop、支援 LifeBook Launcher 自更新，並允許使用者設定開機自動啟動。

Launcher 不會保存 API Key，也不會把 OpenCode 本體放進本倉庫。詳見 [LifeBook Launcher 設計說明](../docs/lifebook-launcher/design.zh-CN.md) 和 [OpenCode 用戶端說明](../docs/ai-clients/opencode.zh-CN.md)。

## 使用者需要知道的重要目錄

- `.\template\epub_pipeline`：查看目前有哪些源語言/語言方向模板。`en-zh-Hans`、`ja-zh-Hans`、`grc-zh-Hans` 等目錄都在這裡。
- `.\tools\ai-client-launcher\opencode`：OpenCode 用戶端下載和啟動目錄。使用者需要知道這個位置，方便確認 Launcher 把 OpenCode 放在哪裡、從哪裡啟動用戶端。
- `.\doc\public\user_prompt`：公共啟動 prompt 目錄。若想了解 prompt 細節，或手動調整給 AI 的 prompt，可以看這裡。
- `.\books\zh-Hans`：最重要的成書目錄。翻譯成簡體中文成功後，到對應書籍目錄裡找 `output\release\`；只有 release 目錄裡的成品才算可發布結果。

## 倉庫結構

- `AGENTS.md`：所有 AI agent 必須先讀的規則。
- `template/epub_pipeline/`：權威流程模板與規則。
- `template/epub_pipeline/common/`：通用 EPUB 流程、腳本、來源證據、版權核查、品質門禁、隨機抽檢和發布規則。
- `template/epub_pipeline/{source-target}/`：具體語言方向的 prompt、術語、文風和審校規則。
- `template/epub_pipeline/targets/{target}/`：目標語言品質規則。
- `template/epub_pipeline/profiles/{profile-target}/`：特殊書籍類型的附加規則。
- `books/{target}/{number}_{book_slug}/`：具體書籍工程。書籍內容只能寫在這裡。
- `books/`：共享 Node.js 工具依賴，統一安裝一次。
- `doc/public/`：公開說明、prompt 使用文件和候選書資料。
- `research/{source-target}/`：特定語言方向調研產物。
- `.opencode/` 與 `opencode.jsonc`：OpenCode 薄適配層，不是流程規則源。
- `tools/lifebook-launcher/`：LifeBook Launcher 桌面啟動器入口；`source/` 內是開發原始碼。

## 建立新書

不要手動複製模板，使用腳本：

```powershell
cd books
npm run new:book -- {book_id_slug} --source-target {source-target}
```

新書目錄格式：

```text
books/{target}/{number}_{book_id_slug}/
```

腳本會先複製 `template/epub_pipeline/common`，再覆蓋對應語言方向模板。若書籍需要特殊 profile，再疊加 `profiles/{profile-target}/`。

## 核心規則

- 翻譯前必須保留來源證據和版權核查記錄。
- 不使用現代受版權保護譯本、盜版站或來源不明 EPUB。
- AI 初稿不能直接發布。
- 具體書籍內容不能寫回 `template/`。
- 面向人的重要模板文件必須包含目標貢獻者能讀懂的本地語言。
- 最終交付前必須經過 EPUB 校驗、讀者可見內容檢查、分層隨機抽檢和版本化 release。

## 書籍工具

共享依賴只安裝一次：

```powershell
cd books
npm install
```

然後進入具體書籍工程執行：

```powershell
npm run build:epub
npm run check:epub
npm run review:random-samples
npm run review:random-validate:pass
npm run release:create
```

## 參與方式

有價值的貢獻包括：找公版來源、查版權、審譯文、統一術語、測試 EPUB、回饋排版可讀性、改進自動化腳本。優先做小而可複核的修改，不做無法追蹤的大段重寫。

## 版權和授權

每本源書都要單獨核查版權。某文本在一個國家進入公版，不代表自動在所有地區都進入公版。

本專案產生的譯文、註釋、封面、排版和 EPUB 打包等非程式碼內容，預設按 `CC BY-NC-SA 4.0` 發布；第三方商業使用必須另行取得 LifeBook 書坊及相關權利人的授權。

參見：

- [LICENSE.zh-TW.md](../license/LICENSE.zh-TW.md)
- [CONTRIBUTING.zh-TW.md](../license/CONTRIBUTING.zh-TW.md)
- [COMMERCIAL_LICENSE.zh-TW.md](../license/COMMERCIAL_LICENSE.zh-TW.md)
