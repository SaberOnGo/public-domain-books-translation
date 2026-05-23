# AI 用戶端使用說明：如何讓 AI 依照本倉庫模板製作書籍

這份說明寫給希望用 AI 用戶端協作製書的人。你不需要會寫程式；只需要會打開這個倉庫、複製一段 prompt、檢查 AI 產出的檔案。

> 重要：不要把 API Key 寫進倉庫檔案，不要提交 `auth.json`、`.env`、設定截圖或任何金鑰。

## 先理解 3 件事

1. **普通用戶只需要提供兩項資訊。**
   你只需要告訴 AI「我要翻譯的書」和「目標語言」。可靠來源、源語言、模板、目錄名、release 和檢查命令都由 AI 自動處理。

2. **本倉庫必須先讀規則。**
   每次都要求 AI 先讀 `AGENTS.md`，再讀 `template/epub_pipeline/` 下的模板規則。

3. **AI 初稿不能直接發布。**
   正確流程是：來源核查、版權核查、譯前研究、試譯、分章翻譯、章節審校、EPUB 建置、EPUBCheck、分層隨機抽檢、release。

## 最簡單的啟動方式

先進入倉庫根目錄：

```powershell
cd D:\project\49_public-domain-books-translation
```

如果你是從發布版只安裝了 LifeBook Launcher，就進入 Launcher 自動準備好的專案目錄；Windows 預設是 `D:\LifeBook`。

然後把下面這段貼給 AI，將 `{...}` 換成你的書名和目標語言：

```text
我要翻譯的書：{書名、作者；如果你已經有可靠來源連結，也可以貼上}
目標語言：{例如 簡體中文}

請在目前倉庫自動選擇正確的公版書翻譯 prompt：
- 如果已有對應源語言模板，執行 doc/public/user_prompt/book_translation_existing_template.md。
- 如果沒有對應源語言模板，執行 doc/public/user_prompt/book_translation_new_template.md。

除非版權或來源無法確認，不要讓我填寫技術欄位。請自動查找可靠公版來源，自動建立專案，完成翻譯、審校、EPUB 建置、分層隨機抽檢和 release。
```

沒有 `/goal` 的用戶端也可以用，把第一行改成：

```text
目標：請在目前倉庫製作一本新的公版書翻譯 EPUB。
```

## 你需要知道的 4 個目錄

- `.\template\epub_pipeline`：查看目前有哪些源語言/語言方向模板。
- `.\tools\lifebook-launcher`：倉庫副本裡的 LifeBook Launcher 入口目錄。發布版使用者通常直接啟動已安裝的 Launcher，它會自動準備專案目錄。
- `.\doc\public\user_prompt`：公共 prompt 目錄；想看 prompt 細節或手動調整時看這裡。
- `.\books\zh-Hans`：簡體中文書籍輸出目錄；書做好後，到對應書籍目錄找 `output\book.epub` 和 `output\release\`。

## 兩個公共 prompt 是什麼

- `doc/public/user_prompt/book_translation_existing_template.md`：倉庫已經有對應源語言模板時使用，例如日語到簡體中文、英語到簡體中文、古希臘語到簡體中文。
- `doc/public/user_prompt/book_translation_new_template.md`：倉庫還沒有對應源語言模板時使用，例如第一次做法語到簡體中文。
- `doc/public/user_prompt/how_to_use_book_translation_prompts.md`：更短的小白版說明，只解釋怎麼填寫「我要翻譯的書」和「目標語言」。

如果你不確定該用哪個，就讓 AI 先檢查模板是否存在。普通用戶不需要理解 `source-target`、slug、profile、release version 或 npm 命令。

## 選哪個用戶端

| 用戶端 | 適合誰 | 怎麼用本倉庫 prompt |
| --- | --- | --- |
| Codex App | 想要圖形介面、diff、終端、瀏覽器整合的人 | 打開倉庫，新建 thread，貼上 `/goal` |
| Claude Code | 想在終端用 Claude 或 DeepSeek 跑 agent 的人 | 進入倉庫，執行 `claude`，貼上目標 prompt |
| Google Antigravity | 想在 AI IDE 裡讓 agent 計畫、改檔、跑命令的人 | 打開 workspace，在 agent 輸入框貼上 prompt |
| OpenCode | 想用開源用戶端，並方便接 DeepSeek 的人 | 用 LifeBook Launcher 檢查/更新 OpenCode Desktop，打開倉庫後貼 prompt |

## LifeBook Launcher

如果不想手動處理專案和用戶端更新，可以使用 LifeBook Launcher。它不會保存 API Key，也不會把 OpenCode 本體放進倉庫。

- 普通使用者拿到發布包後，雙擊 **LifeBook Launcher** 應用或安裝包即可。
- 目前 Windows 本機入口：`tools\lifebook-launcher\LifeBook Launcher Setup.exe`。
- 開發者原始碼目錄：`tools/lifebook-launcher/source/`。
- 它會自動準備並更新 LifeBook 專案；Windows 預設專案目錄是 `D:\LifeBook`。
- 它可以檢查並更新 OpenCode Desktop，也可以下載、安裝並重新啟動 LifeBook Launcher 本身。
- 使用者可以在設定裡開啟或關閉開機自動啟動。

## Codex App

1. 安裝並打開 Codex App。
2. 選擇本倉庫目錄。
3. 新建 thread。
4. 貼上 `/goal`。
5. 等 AI 先讀 `AGENTS.md` 和 `template/`。
6. 審查它要修改的檔案。
7. 最後檢查 `books/.../output/release/`。

Codex App 適合本倉庫的長流程任務，因為它有 thread、worktree、內建終端、diff review 和 Git 操作。

DeepSeek 說明：Codex App 通常使用 OpenAI/Codex 登入後的模型。若要用 DeepSeek，優先使用 OpenCode 或 Claude Code；只有你的 Codex CLI 或中間網關明確支援對應協議時，才嘗試自訂 provider。

## Claude Code 接入 DeepSeek

Windows PowerShell：

```powershell
$env:ANTHROPIC_BASE_URL="https://api.deepseek.com/anthropic"
$env:ANTHROPIC_AUTH_TOKEN="<你的 DeepSeek API Key>"
$env:ANTHROPIC_MODEL="deepseek-v4-pro[1m]"
$env:ANTHROPIC_DEFAULT_OPUS_MODEL="deepseek-v4-pro[1m]"
$env:ANTHROPIC_DEFAULT_SONNET_MODEL="deepseek-v4-pro[1m]"
$env:ANTHROPIC_DEFAULT_HAIKU_MODEL="deepseek-v4-flash"
$env:CLAUDE_CODE_SUBAGENT_MODEL="deepseek-v4-flash"
$env:CLAUDE_CODE_EFFORT_LEVEL="max"

cd D:\project\49_public-domain-books-translation
claude
```

macOS/Linux：

```bash
export ANTHROPIC_BASE_URL=https://api.deepseek.com/anthropic
export ANTHROPIC_AUTH_TOKEN="<your DeepSeek API Key>"
export ANTHROPIC_MODEL="deepseek-v4-pro[1m]"
export ANTHROPIC_DEFAULT_OPUS_MODEL="deepseek-v4-pro[1m]"
export ANTHROPIC_DEFAULT_SONNET_MODEL="deepseek-v4-pro[1m]"
export ANTHROPIC_DEFAULT_HAIKU_MODEL="deepseek-v4-flash"
export CLAUDE_CODE_SUBAGENT_MODEL="deepseek-v4-flash"
export CLAUDE_CODE_EFFORT_LEVEL=max

cd /path/to/49_public-domain-books-translation
claude
```

進入後貼上啟動 prompt。

## OpenCode 接入 DeepSeek

1. 安裝 OpenCode。
2. 進入倉庫並啟動：

```powershell
cd D:\project\49_public-domain-books-translation
opencode
```

3. 在 OpenCode 裡輸入：

```text
/connect
```

4. 搜尋並選擇 `deepseek`。
5. 貼上 DeepSeek API Key。
6. 選擇 `DeepSeek-V4-Pro`。
7. 貼上本說明的 `/goal` prompt。

若你想先看計畫，不想立刻改檔，補一句：

```text
先只給執行計畫和將要修改的檔案列表，等我確認後再寫檔案。
```

## Google Antigravity

1. 安裝 Google Antigravity。
2. 打開本倉庫 workspace。
3. 在 agent 輸入框貼上目標 prompt。
4. 要求 agent 先讀 `AGENTS.md` 和 `template/epub_pipeline/`。
5. 使用需要確認的執行模式，避免未審查就執行危險命令。
6. 最後檢查 diff、測試輸出和 release 檔案。

DeepSeek 說明：如果 Antigravity 當前介面沒有 DeepSeek provider，不要硬改設定。需要 DeepSeek 時使用 OpenCode 或 Claude Code。

## 常用檢查命令

進入某本書目錄後：

```powershell
npm run build:epub
npm run check:epub
npm run review:random-samples
npm run review:random-validate:pass
npm run release:create
```

若還沒安裝依賴，先在 `books/` 執行一次：

```powershell
cd D:\project\49_public-domain-books-translation\books
npm install
```

## 常見錯誤

- 把 API Key 寫入 Markdown 或提交到 Git。
- 讓 AI 不讀模板就直接翻整本。
- 只生成 `output/book.epub`，沒有 `output/release/`。
- 版權未查清就開始翻譯。
- 使用現代譯本作為參考或改寫來源。
- 抽檢發現問題後沒有追加新一輪。
- 把某本書的資料寫回 `template/`。

## 參考連結

- Codex App 官方說明：https://developers.openai.com/codex/app
- Codex 配置參考：https://developers.openai.com/codex/config-reference
- DeepSeek API 快速開始：https://api-docs.deepseek.com/
- DeepSeek 接入 Claude Code：https://api-docs.deepseek.com/guides/agent_integrations/claude_code
- DeepSeek 接入 OpenCode：https://api-docs.deepseek.com/guides/agent_integrations/opencode
- OpenCode provider 文件：https://open-code.ai/en/docs/providers
- Google Antigravity 文件：https://www.antigravity.google/docs/overview
