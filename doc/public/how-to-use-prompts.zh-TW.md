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

## 精修審校 prompt（可選）

第一版 EPUB 已經生成後，如果想繼續提高譯本品質，可以再使用下面這段。`N` 是「連續無問題輪數」：`1` 最省 token，`3` 更嚴格，品質要求更高；不確定時填 `2`。

```text
本書專案：{書籍專案路徑，例如 books/{target}/{number}_{slug}}
連續無問題退出輪數 N：{1/2/3；預設 2}

請先讀取 AGENTS.md、該書 SKILL.md（如有）、template/epub_pipeline/README.md、template/epub_pipeline/common/README.md，以及封面、book-info/frontmatter、圖表資產、品質門禁、分層隨機抽檢、release 相關規則。

請設定 /goal：對已生成 EPUB 做精修審校，嚴格按模板要求檢查封面、首頁/前置頁、metadata、nav、目錄、正文、註釋、圖表、公式、表格、圖片、樣式、讀者可見內容、EPUB 建置與 release。不得只檢查我點名的項目。

啟動 2 個獨立評審 agent 做分層隨機抽檢。至少執行 4 輪；每輪使用新 seed，並按模板保存樣本、證據、評審、修復和閉環記錄。若任何輪發現 P0/P1/P2、單項 <70、讀者不可理解、事實/術語/圖表/公式錯誤或模板硬門禁失敗，修復後必須追加新一輪。

退出條件：最近連續 N 輪均無新增阻塞問題，且 npm run review:random-validate:pass 通過。N=1 為最低強度，較省 token；N=3 更嚴格，審校後譯本品質更高，用戶可自行調整。

通過後清理或重建 staging，重新生成 EPUB，執行 publication lint、asset manifest、cover output、reader-facing policy、EPUBCheck 和 release 腳本。最終可發布 EPUB 必須輸出到該書 output/release/，release_state.json.latest_status 必須為 PASS。報告 release EPUB 路徑、抽檢輪次、修復摘要、驗證命令結果和剩餘風險。
```

## 你需要知道的關鍵位置

- `.\template\epub_pipeline`：查看目前有哪些源語言/語言方向模板。AI 會據此判斷該用已有模板 prompt，還是新建語言模板 prompt。
- `.\tools\lifebook-launcher`：LifeBook Launcher 用戶端安裝啟動目錄。使用者需要知道這個位置，以使用 LifeBook 專案和安裝 OpenCode。
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
