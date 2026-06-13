# AI 用戶端使用說明：如何讓 AI 依照本倉庫模板製作書籍

這份說明寫給希望用 AI 用戶端協作製書的人。您不需要會寫程式；只需要打開專案、複製一段文字、檢查 AI 做出的書籍檔案。

## 先理解 3 件事

1. **普通用戶只需要提供三項內容。**
   您只需要告訴 AI「我要翻譯的書」「目標語言」和「自動選擇翻譯 prompt 的規則」。「自動選擇翻譯 prompt 的規則」的完整寫法見下面的[最簡單的啟動方式](#最簡單的啟動方式)。可靠來源、源語言、模板、目錄名、release 和檢查命令都由 AI 自動處理。

2. **讓 AI 自己讀規則。**
   您不需要理解倉庫規則，只要要求 AI 自動選擇正確的公共 prompt。

3. **最後只看 release 或私人產物結果。**
   AI 會自動完成來源核查、版權核查、翻譯、審校、EPUB 建置、抽檢和發布。公版或授權專案最後檢查 `output/release/`；個人自用專案最後檢查 `output/private_artifacts/`。

## 最簡單的啟動方式

打開您正在使用的 AI 用戶端，進入這個專案或讓 Launcher 打開專案。

然後把下面這段貼給 AI，將 `{...}` 換成您的書名和目標語言：

### 公版書翻譯 prompt

```text
我要翻譯的書：{書名、作者（可選）；如果您已經有可靠來源連結，也可以貼上}
目標語言：{例如 簡體中文}

請自動選擇正確的翻譯 prompt：
- 如已有對應源語言模板，執行 doc/public/user_prompt/book_translation_existing_template.md。
- 如無對應源語言模板，執行 doc/public/user_prompt/book_translation_new_template.md。

除非版權或來源無法確認，不要讓我填寫技術欄位。請自動查找可靠公版來源，自動建立專案，完成翻譯、審校、EPUB 建置、分層隨機抽檢和 release。
翻譯執行時必須逐章執行「每章譯後全量檢查並修復」：每章都要對照整章原文和整章譯文檢查忠實度、中文順讀、術語、標題/小標題、註釋、圖表文字介面、源語句法殘留、過硬過直句、過度解釋或加戲等問題；發現問題後先修復，但該輪不能 PASS，必須追加新一輪整章複查，直到最新一輪零問題 PASS。
第一版 EPUB 生成後必須執行「分層隨機抽檢與問題族追殺」：抽檢發現問題時，不得只修被抽樣本，必須在當輪歸納為問題族，用 `rg`、術語表、標題表、抽樣 manifest 和小上下文原文對照做全書同類審計，修復確認命中，記錄例外，再用新 seed 追加一輪。譯文品質問題族必須使用 `skills/translation-quality-defect-families/SKILL.md` 做經驗沉澱。
```

## 個人自用書翻譯 prompt

如果這是您自己已有的本地書源，只供個人學習自用，不傳播、不商業使用，可以使用下面這段：

```text
我要翻譯的書：{書名、本地目錄: XXX }
目標語言： {例如 簡體中文}

請自動選擇正確的翻譯 prompt：
- 如已有對應源語言模板，執行 doc/public/user_prompt/book_translation_private_existing_template.md。
- 如無對應源語言模板，執行 doc/public/user_prompt/book_translation_private_new_template.md。

這是我個人自用的，不傳播，不用於商業，使用我給出的本地書源。
請自動建立專案，嚴格完成整個模板規定的系統翻譯流程，不允許有任何遺漏。
翻譯執行時必須逐章執行「每章譯後全量檢查並修復」；第一版 EPUB 後必須執行「分層隨機抽檢與問題族追殺」。發現譯文品質問題族時，先在本書閉環，再把可復用經驗合併進 `skills/translation-quality-defect-families/SKILL.md`。
```

個人自用專案必須建立在 `books/private/{target}/{number}_{目標語言書名}_{目標語言作者名}/`，最終版本化產物在 `output/private_artifacts/`，不是公開 release，不得發布到 GitHub。

## EPUB 後精修審校 prompt（可選）

第一版 EPUB 已經生成後，不要只給 AI 一句「幫我精修」。請依目的選擇下面兩個 prompt：

- **Prompt B：章節全量複檢與修復。** 適用於舊流程專案、缺少每章零問題 control 記錄，或您不確定每章是否已完整檢查時。
- **Prompt C：分層隨機抽檢與問題族追殺。** 適用於第一版 EPUB 後的發布前信心檢查；負責抽樣發現系統性盲點、全書同類審計、新 seed 複抽和 release/private artifact。

建議順序：如果是舊流程或不確定每章是否已零問題閉環，先跑 **Prompt B**，再跑 **Prompt C**。若每章已有可靠的零問題 control 記錄，可以直接跑 **Prompt C**。

### Prompt B：章節全量複檢與修復

```text
本書專案：{書籍專案路徑，例如 books/{target}/{number}_{目標語言書名}_{目標語言作者名}}

請先讀取 AGENTS.md、該書 SKILL.md（如有）、template/epub_pipeline/README.md、template/epub_pipeline/common/README.md、template/epub_pipeline/common/prompts/08a_chapter_post_translation_control.md、template/epub_pipeline/common/references/quality_gate_framework.md、目標語言品質框架，以及 `skills/translation-quality-defect-families/SKILL.md`。

請設定 /goal：對本書所有已翻譯章節執行「每章譯後全量複檢並修復」。每章必須對照整章原文、整章譯文和讀者可見上下文，覆蓋但不限於忠實度、漏譯誤譯、中文順讀、文學性、可讀性和吸引力、教學/解釋節奏、術語穩定、案例/專名/地名/書名/船名/機構名、標題與小標題、註釋、圖表/公式/表格/圖片文字介面、源語句法殘留、過硬過直過板句、過度解釋、無依據加戲、讀者可見 AI/製作痕跡、異常空格/亂碼、舊紙書目錄殘留。

可並行處理不同章節，但每個章節必須獨立閉環：每一輪都檢查整章；只要發現任何問題，先修復該章，但該輪只能記為 `FIXED_RECHECK_REQUIRED`，不能 PASS；隨後追加新一輪整章複查。只有最新一輪記錄 `scope: FULL_CHAPTER`、`issues_found: 0`、`fixes_applied: 0`、`unresolved_blocking_issues: 0`、`latest_round_status: PASS`、`allow_next_chapter: true` 時，該章才算通過。

若任一章發現可複現譯文品質問題族，例如短句切斷、比喻自撞、排比標點拖拽、代詞指代不清、源語句法殘留、術語漂移、標題超載、過度解釋或加戲，必須按 `skills/translation-quality-defect-families/SKILL.md` 處理：記錄如何發現、如何歸納、如何用低 token 方法查全書同類、如何修復、如何複查。先用 `rg`、術語表、禁用寫法、標題表、章節控制記錄和小上下文原文對照收集候選，只把候選片段交給 agent 複核；不要讓 agent 盲讀全書。

完成後重新生成或更新 `qa/chapter_controls/*.control.md`、必要的 `qa/fidelity/`、`qa/readability/`、`qa/terminology/`、`qa/gates/` 記錄，把通過章節寫入或更新到 `chapters/final/`。然後重建 EPUB，執行可用的 chapter-control/preflight/publication lint/asset/EPUBCheck 命令。報告修復章節、問題族、驗證命令結果和仍需進入 Prompt C 的事項。
```

### Prompt C：分層隨機抽檢與問題族追殺

`N` 是「連續無問題抽檢輪數」：`1` 最省 token，是模板最低退出強度；`2` 更穩，建議普通書使用；`3` 更嚴格，適合術語密集、科學/數學/圖表多或追求更高品質的書。

```text
本書專案：{書籍專案路徑，例如 books/{target}/{number}_{目標語言書名}_{目標語言作者名}}
連續無問題抽檢輪數 N：{1/2/3；預設 2}

請先讀取 AGENTS.md、該書 SKILL.md（如有）、template/epub_pipeline/README.md、template/epub_pipeline/common/README.md、template/epub_pipeline/common/prompts/16a_stratified_random_spotcheck.md、template/epub_pipeline/common/references/stratified_random_spotcheck.md、template/epub_pipeline/common/references/quality_gate_framework.md、封面、book-info/frontmatter、圖表資產、release 相關規則，以及 `skills/translation-quality-defect-families/SKILL.md`。

請設定 /goal：對已生成 EPUB 執行「分層隨機抽檢與問題族追殺」，並在通過後重新生成 release 或 private artifact。不要把本 prompt 當作普通潤色；它的核心是發布前發現系統性盲點、全書同類審計、修復閉環和新 seed 複抽。

執行分層隨機抽樣，抽樣總體是 reader-facing audit units，不是頁數，也不只是段落。必須覆蓋實際存在的 paragraph、table、figure、formula/proof、caption/note。至少派生 2 個獨立評審 agent，互不參考，並按模板保存 `reviews/random_spotcheck/round_XXX/` 下的 seed、manifest、samples、evidence、reviews、fixes/fix_log.md、verification/closure_check.md。

若任一樣本發現 P0/P1/P2、單項 <80、讀者不可理解、忠實度偏移、事實/術語/專名/標題/註釋/圖表/公式錯誤、源語句法殘留、過硬過直句、短句切斷、比喻自撞、排比標點拖拽、代詞指代不清、過度解釋或加戲，必須在本輪把它歸納為問題族，執行全書同類問題審計並修復所有確認命中。不得只修被抽中的樣本，不得等第二輪才查全書。

譯文品質問題族必須優先低 token 審計：先用 `rg`、`glossary/terms.csv`、`forbidden_body_renderings`、標題映射、章節控制記錄、抽樣 manifest 和小上下文原文對照收集候選，再把候選片段交給 agent 複核。修復後在本輪 `fix_log.md` 和 `closure_check.md` 寫清問題族、檢索式/審計方法、命中數、修復位置、合理例外和複查結果；可復用經驗合併進 `skills/translation-quality-defect-families/SKILL.md`，不要重複堆條目。

每次修復後必須重建 EPUB，並用新 seed 追加下一輪抽檢。退出條件：最近連續 N 個新 seed 抽檢輪均 PASS，所有已發現問題族均關閉，`npm run review:random-validate:pass` 通過，且 release_confidence 達到模板要求。

通過後清理或重建 staging，重新生成 EPUB，執行 publication lint、asset manifest、cover output、reader-facing policy、EPUBCheck，以及 release 或 private artifact 腳本。公版或授權專案的最終可發布 EPUB 必須輸出到該書 output/release/，release_state.json.latest_status 必須為 PASS。個人自用專案的最終私人產物必須輸出到 output/private_artifacts/，private_artifact_state.json.latest_status 必須為 PASS。報告 release EPUB 或 private artifact 路徑、抽檢輪次、修復摘要、驗證命令結果和剩餘風險。
```

## 您需要知道的關鍵位置

- `.\template\epub_pipeline`：查看目前有哪些源語言/語言方向模板。AI 會據此判斷該用已有模板 prompt，還是新建語言模板 prompt。
- `.\tools\lifebook-launcher`：LifeBook Launcher 用戶端安裝啟動目錄。使用者需要知道這個位置，以使用 LifeBook 專案和安裝 OpenCode。
- `.\doc\public\user_prompt`：公共 prompt 放在這裡。想了解 prompt 細節，或想手動修改 prompt 時，看這個目錄。
- `.\books\zh-Hans`：最重要的成書目錄。翻譯成簡體中文成功後，到對應書籍目錄裡找 `output\release\`；只有 release 目錄裡的成品才算可發布結果。
- `.\books\private`：個人自用書籍專案目錄。非公版私人翻譯的原文、譯文、QA、EPUB 和 `output\private_artifacts\` 私人產物只應保存在這裡；此目錄被 Git 忽略，不發布到 GitHub。

## 四個翻譯 prompt 是什麼

- `doc/public/user_prompt/book_translation_existing_template.md`：倉庫已經有對應源語言模板時使用，例如日語到簡體中文、英語到簡體中文、古希臘語到簡體中文。
- `doc/public/user_prompt/book_translation_new_template.md`：倉庫還沒有對應源語言模板時使用，例如第一次做法語到簡體中文。
- `doc/public/user_prompt/book_translation_private_existing_template.md`：個人自用、本地書源、已有對應源語言模板時使用。
- `doc/public/user_prompt/book_translation_private_new_template.md`：個人自用、本地書源、還沒有對應源語言模板時使用。
- `doc/public/user_prompt/how_to_use_book_translation_prompts.md`：更短的小白版說明，只解釋怎麼填寫三項內容。

如果您不確定該用哪個，就讓 AI 先檢查模板是否存在。普通用戶不需要理解 `language-pair template name`、slug、profile、release version 或 npm 命令。

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
- 等 AI 完成後，公版或授權專案檢查書籍目錄裡的 `output/release/`；個人自用專案檢查 `output/private_artifacts/`。

## Codex App

1. 安裝並打開 Codex App。
2. 選擇本倉庫目錄。
3. 新建 thread。
4. 貼上 `/goal`。
5. 等 AI 先讀 `AGENTS.md` 和 `template/`。
6. 審查它要修改的檔案。
7. 最後檢查 `books/zh-Hans/.../output/release/`，或對應目標語言的 `books/{target}/.../output/release/`；個人自用專案檢查 `books/private/{target}/.../output/private_artifacts/`。

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
- 只生成 `output/book.epub`，公版專案沒有 `output/release/`，或個人自用專案沒有 `output/private_artifacts/`。
- 版權未查清就開始翻譯。
- 使用現代譯本作為參考或改寫來源。
- 抽檢發現問題後沒有追加新一輪。
- 把某本書的資料寫回 `template/`。
