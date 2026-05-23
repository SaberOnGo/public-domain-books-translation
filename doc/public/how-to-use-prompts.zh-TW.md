# AI 用戶端使用說明：如何讓 AI 依照本倉庫模板製作書籍

這份說明寫給希望用 AI 用戶端協作製書的人。你不需要會寫程式；只需要打開專案、複製一段文字、檢查 AI 做出的書籍檔案。

## 先理解 3 件事

1. **普通用戶只需要提供三項內容。**
   你只需要告訴 AI「我要翻譯的書」「目標語言」和「自動選擇翻譯 prompt 的規則」。「自動選擇翻譯 prompt 的規則」的完整寫法見下面的[最簡單的啟動方式](#最簡單的啟動方式)。可靠來源、源語言、模板、目錄名、release 和檢查命令都由 AI 自動處理。

2. **讓 AI 自己讀規則。**
   你不需要理解倉庫規則，只要要求 AI 自動選擇正確的公共 prompt。

3. **最後只看 release 結果。**
   AI 會自動完成來源核查、版權核查、翻譯、審校、EPUB 建置、抽檢和發布。你最後檢查 `output/release/` 裡的成品。

## 最簡單的啟動方式

打開你正在使用的 AI 用戶端，進入這個專案或讓 Launcher 打開專案。

然後把下面這段貼給 AI，將 `{...}` 換成你的書名和目標語言：

```text
我要翻譯的書：{書名、作者（可選）；如果你已經有可靠來源連結，也可以貼上}
目標語言：{例如 簡體中文}

請自動選擇正確的翻譯 prompt：
- 如已有對應源語言模板，執行 doc/public/user_prompt/book_translation_existing_template.md。
- 如無對應源語言模板，執行 doc/public/user_prompt/book_translation_new_template.md。

除非版權或來源無法確認，不要讓我填寫技術欄位。請自動查找可靠公版來源，自動建立專案，完成翻譯、審校、EPUB 建置、分層隨機抽檢和 release。
```

## 你需要知道的關鍵位置

- `.\template\epub_pipeline`：查看目前有哪些源語言/語言方向模板。AI 會據此判斷該用已有模板 prompt，還是新建語言模板 prompt。
- `.\tools\ai-client-launcher\opencode`：OpenCode 用戶端下載和啟動目錄。使用者需要知道這個位置，方便確認 Launcher 把 OpenCode 放在哪裡、從哪裡啟動用戶端。
- `.\doc\public\user_prompt`：公共 prompt 放在這裡。想了解 prompt 細節，或想手動修改 prompt 時，看這個目錄。
- `.\books\zh-Hans`：最重要的成書目錄。翻譯成簡體中文成功後，到對應書籍目錄裡找 `output\release\`；只有 release 目錄裡的成品才算可發布結果。

## 兩個公共 prompt 是什麼

- `doc/public/user_prompt/book_translation_existing_template.md`：倉庫已經有對應源語言模板時使用，例如日語到簡體中文、英語到簡體中文、古希臘語到簡體中文。
- `doc/public/user_prompt/book_translation_new_template.md`：倉庫還沒有對應源語言模板時使用，例如第一次做法語到簡體中文。
- `doc/public/user_prompt/how_to_use_book_translation_prompts.md`：更短的小白版說明，只解釋怎麼填寫三項內容。

如果你不確定該用哪個，就讓 AI 先檢查模板是否存在。普通用戶不需要理解 `source-target`、slug、profile、release version 或 npm 命令。

## 選哪個用戶端

| 用戶端 | 適合誰 | 怎麼用本倉庫 prompt |
| --- | --- | --- |
| Codex App | 想要圖形介面、diff、終端、瀏覽器整合的人 | 打開倉庫，新建 thread，貼上 `/goal` |
| Claude Code | 熟悉終端、想用命令列 Agent 的人 | 在倉庫中啟動 Claude Code，貼上目標 prompt |
| LifeBook Launcher | 想要最少手動步驟的人；<br>需安裝 OpenCode 用戶端支援 | 打開 Launcher，安裝 OpenCode；<br>OpenCode 支援市面大多數模型（如 DeepSeek、豆包等）；<br>在 OpenCode 裡選擇翻譯書籍任務，貼上三項內容（見[完整範例](#最簡單的啟動方式)） |
| Google Antigravity | 想在 AI IDE 裡讓 agent 計畫、改檔、跑命令的人 | 打開 workspace，在 agent 輸入框貼上 prompt |

## LifeBook Launcher

如果不想手動處理專案和用戶端，可以使用 LifeBook Launcher。Launcher 可以下載並打開 OpenCode 用戶端；OpenCode 支援市面上大多數 AI 模型，例如 DeepSeek、豆包等。使用前需要在 OpenCode 裡配置對應模型的 API Key。

- 打開 **LifeBook Launcher**。
- 選擇或打開本專案。
- 按需要下載或打開 OpenCode 用戶端，並在 OpenCode 中配置 API Key。
- 貼上三項內容：我要翻譯的書、目標語言、自動選擇 prompt 的規則（見[最簡單的啟動方式](#最簡單的啟動方式)裡的完整範例）。
- 等 AI 完成後，檢查書籍目錄裡的 `output/release/`。

## Codex App

1. 安裝並打開 Codex App。
2. 選擇本倉庫目錄。
3. 新建 thread。
4. 貼上 `/goal`。
5. 等 AI 先讀 `AGENTS.md` 和 `template/`。
6. 審查它要修改的檔案。
7. 最後檢查 `books/zh-Hans/.../output/release/`，或對應目標語言的 `books/{target}/.../output/release/`。

Codex App 適合本倉庫的長流程任務，因為它方便查看 AI 修改了哪些檔案。

## Google Antigravity

1. 安裝 Google Antigravity。
2. 打開本倉庫 workspace。
3. 在 agent 輸入框貼上目標 prompt。
4. 要求 agent 先讀 `AGENTS.md` 和 `template/epub_pipeline/`。
5. 使用需要確認的執行模式，避免未審查就執行危險命令。
6. 最後檢查 diff、測試輸出和 release 檔案。

## 常見錯誤

- 讓 AI 不讀模板就直接翻整本。
- 只生成 `output/book.epub`，沒有 `output/release/`。
- 版權未查清就開始翻譯。
- 使用現代譯本作為參考或改寫來源。
- 抽檢發現問題後沒有追加新一輪。
- 把某本書的資料寫回 `template/`。
