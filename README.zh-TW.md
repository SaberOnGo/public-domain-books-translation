# LifeBook 書坊：公版書翻譯與 EPUB 製作協作專案

<table align="center">
  <tr>
    <td align="center"><h3><a href="./README.md">简体中文</a></h3></td>
    <td align="center"><h3><a href="./README.zh-TW.md">繁體中文</a></h3></td>
    <td align="center"><h3><a href="./README.en.md">English</a></h3></td>
    <td align="center"><h3><a href="./README.ja.md">日本語</a></h3></td>
  </tr>
</table>

LifeBook 書坊是一個面向公版書的翻譯與電子書製作專案。我們希望把一些已經進入公版、但中文世界還不容易讀到的書，重新整理、翻譯、審校，並製作成可閱讀的 EPUB。

這裡的“翻譯”不是把原文丟給 AI 後直接釋出。AI 可以幫我們做很多重複工作，例如清洗文本、初譯、分章、生成術語表、檢查漏譯、構建 EPUB；但一本書要真正好讀，仍然需要人來判斷：句子順不順，人物名是否統一，歷史稱謂是否妥當，譯文有沒有機械味，書在手機閱讀器裡看起來是否舒服。

如果你愛讀書、願意翻幾段文字、願意幫忙校對、能發現錯別字、喜歡查資料，或者只是願意試讀一章並指出哪裡讀不下去，都可以參與。

## 專案想做什麼

我們想做幾件具體的小事：

- 從可靠來源選擇公版書，例如 Project Gutenberg、Wikisource、Standard Ebooks 等。
- 在翻譯前先儲存版權與來源證據，避免使用現代出版社版本、現代註釋版或不明來源文本。
- 讓 AI 做可追蹤的初譯和檢查，而不是一次性生成不可複核的整本譯文。
- 把每章拆成原文、初譯、終稿、審校報告、術語報告等可檢查檔案。
- 讓更多人可以只參與一小段工作：查資料、統一術語、審一章、試讀 EPUB、檢查目錄和封面。
- 最終生成格式有效、讀起來舒服、來源清楚的 EPUB。

我們不想把這個專案說得很宏大。它更像一個小型書坊：有人找書，有人翻譯，有人校對，有人排版，有人試讀。每個人做一點，書就會比一個人單獨做得更穩。

## 最簡單怎麼開始

普通參與者不需要手動填寫一堆工程檔案。最簡單的方式是：把模板目錄和一本書的公版來源交給 AI，讓 AI 按流水線自動建立書籍工程、填寫後設資料、抓取原文、分章、翻譯、審校、排版和生成 EPUB。

你通常只需要告訴 AI 三件事：

- 想做哪本書。
- 公版來源 URL，如果有的話。
- 翻譯方向，例如英文到中文、中文到英文、日文到中文。

例如，可以這樣發給 AI：

```text
/goal 按 D:\project\49_public-domain-books-translation\books\pg20923_a_negro_explorer_at_the_north_pole 工程製作《黑人北極探險家》中文 EPUB，
從 https://www.gutenberg.org/ebooks/20923 抓取原文，
按 template/epub_pipeline/common 與 template/epub_pipeline/en-zh-Hans 的 00_orchestrator_zh_en.md 串聯執行當前完整流程，
覆蓋來源核查、譯前研究、預翻譯、分章翻譯、章節審校、章節門禁、預製作階段 1、樣章檢查、全書 EPUB 製作、獨立評審、返工路由、最終輸出和覆盤，
生成 output/book.epub，並通過 epubcheck。
```

如果你只知道書名，不知道 URL，也可以先讓 AI 幫你找可靠公版來源：

```text
請幫我查詢《某本書》的可靠公版原文來源，優先 Project Gutenberg、Wikisource、Standard Ebooks。
確認來源和版權風險後，先複製 template/epub_pipeline/common，再覆蓋複製 template/epub_pipeline/en-zh-Hans，建立 books/ 下的新書工程。
```

AI 會自動處理大部分工程檔案。人類更適合在關鍵節點介入：看研究是否靠譜、試譯是否好讀、術語是否統一、某章是否需要返工、樣章 EPUB 在閱讀器裡是否舒服。

## 當前倉庫裡有什麼

### `template/epub_pipeline/`

這是製作一本書時要複製使用的模板目錄。不要直接在這個目錄裡做某本書。`common/` 放通用 EPUB 流水線、版權核查、狀態機、構建腳本和製作規則；`en-zh-Hans/` 放英文到簡體中文的提示詞、術語、文風和審校規則。普通參與者只需要知道“做新書時讓 AI 複製 common，再覆蓋對應語言方向模板，不要改模板原件”。

裡面包含：

- `template/epub_pipeline/README.md`：模板組織說明。
- `template/epub_pipeline/common/PIPELINE_SPEC.md`：流水線規範，說明每一步的輸入、輸出、狀態和目錄約定。
- `template/epub_pipeline/en-zh-Hans/README.md`：英文到簡體中文模板說明。
- `template/epub_pipeline/en-zh-Hans/MASTER_PROMPT.md`：啟動 AI 製作一本書時可以使用的主控提示詞。
- `prompts/`：從抓取原文、分章、研究、試譯、翻譯、審校到構建 EPUB 的分步提示詞。
- `metadata/`：書籍資訊、版權核查、來源證據、文體畫像等模板檔案。
- `chapters/`：章節原文、初譯、終稿的放置位置。
- `qa/`：忠實度、可讀性、術語、意象詞、章節門禁等審校檔案。
- `preproduction/`：封面、版式、metadata、樣章 EPUB 等出版前規格。
- `reviews/`：獨立評審與評分表。
- `output/`：最終 EPUB 與校驗結果。
- `retrospective/`：一本書完成後的覆盤和模板改進建議。

### `books/`

這裡放每一本具體書的工程目錄。每本書都應該是從模板複製出來的獨立目錄。

當前已有一本樣例書：

`books/pg20923_a_negro_explorer_at_the_north_pole/`

這本書基於 Project Gutenberg #20923，作者 Matthew A. Henson，中文題名暫作《黑人北極探險家》。它已經完成：

- 原文來源與版權初篩記錄。
- 26 個章節的原文、譯文和終稿。
- 術語、文體、預翻譯、章節審校等質量檔案。
- EPUB 構建。
- EPUBCheck 校驗，結果為 fatal=0、error=0、warning=0。

注意：樣例書證明這套流程可以跑通，但不代表所有章節已經經過人工出版編輯終審。公開發布前，仍建議繼續做逐章人工精修、專名統一和試讀反饋。

### `translation_quality_framework/`

這是翻譯質量框架。它不繫結某一本書，用來說明“好譯文”應該怎樣被研究、試譯、審校和返工。

重點包括：

- 翻譯前要做作者、時代、文體、術語、敏感點研究。
- 正式翻譯前要做預翻譯試譯，試譯不通過就不能批次翻譯。
- 每章要檢查準確性、中文性、文學/敘事效果和出版性。
- 不把“通順”誤認為“好譯文”。
- 不儲存或使用受版權保護的現代譯本作為翻譯來源。

### `doc/public/`

這裡放公開的選題、版權初篩、候選書報告等資料。它們可以幫助我們選擇下一本適合製作的公版書。

## 誰可以參與

你不需要會寫程式碼，也不需要懂 EPUB。下面這些工作都很有價值。

### 1. 試讀者

適合喜歡讀書的人。

你可以：

- 開啟 `books/.../output/book.epub` 試讀。
- 記錄哪一章讀起來不順。
- 標出明顯彆扭的句子。
- 反饋人物、地點、術語哪裡讓你困惑。
- 檢查手機、平板、電腦閱讀器裡的排版是否舒服。

最簡單的反饋格式：

```text
書名：
章節：
原句或位置：
問題：這裡讀起來不順 / 疑似錯譯 / 術語前後不一致 / 排版有問題
建議：如果有建議可以寫，沒有也沒關係
```

### 2. 校對者

適合細心的人。

你可以檢查：

- 錯別字。
- 標點問題。
- 重複段落。
- 漏譯段落。
- 人名、地名、船名、部落名是否統一。
- 章節標題是否前後一致。

### 3. 譯文審校者

適合懂原文或願意對照原文的人。

你可以做：

- 對照 `chapters/src/` 原文和 `chapters/final/` 終稿。
- 檢查是否漏譯、誤譯、數字錯誤、方向錯誤。
- 判斷語氣是否偏離原文。
- 指出機械直譯、過度發揮、省字式翻譯。
- 幫忙改寫一小段，讓它更像自然中文或自然英文。

### 4. 術語和資料協作者

適合喜歡查資料的人。

你可以幫助：

- 查作者、出版年份、歷史背景。
- 統一專有名詞。
- 補充地名、人名、民族稱謂、歷史稱謂說明。
- 檢查某本書是否真的公版。
- 確認來源文本是否來自可靠公版來源。

### 5. EPUB 試製和技術協作者

適合願意折騰工具的人。

你可以幫助：

- 構建 EPUB。
- 檢查封面、目錄、metadata。
- 執行 EPUBCheck。
- 修復 CSS、標題層級、圖片體積、閱讀器相容性。
- 改進自動化指令碼和模板。

## 一本書怎麼從 0 開始製作

下面是給新手看的流程。它不是要求你手動做完每一步，而是告訴你 AI 會做什麼、你可以在哪裡檢查和參與。

### 第一步：選書

先從 `doc/public/` 裡的候選書報告看起，或者自己提出一本書。

選書時要先問：

- 原書是不是公版？
- 作者去世年份是否足夠早？
- 使用的文本來源是否可靠？
- 有沒有現代編輯、現代註釋、現代插圖等可能受版權保護的內容？
- 是否已經有很多成熟中文譯本或英文譯本？
- 這本書是否適合現在投入時間？

重要提醒：Project Gutenberg 常說 “Public domain in the USA”。這隻說明美國維度，不能自動等同於全球都無風險。正式公開發布前，仍應按目標地區複核。

### 第二步：把書名或公版 URL 交給 AI

你不需要自己複製目錄、填寫 YAML、寫工程檔案。把書名、公版 URL 和翻譯方向告訴 AI 即可。

如果已經有可靠來源，可以這樣說：

```text
請用 template/epub_pipeline/common 和 template/epub_pipeline/en-zh-Hans 建立一本新的書籍工程。
原文來源：https://www.gutenberg.org/ebooks/20923
翻譯方向：英文到中文
目標：生成可閱讀的中文 EPUB，並通過 EPUBCheck。
```

如果想參考已經跑通的樣例工程，可以補一句：

```text
請參考 books/pg20923_a_negro_explorer_at_the_north_pole 的工程結構和質量控制方式。
```

AI 應該自動完成：

- 複製模板。
- 建立 `books/{book_id_or_author_title_slug}/`。
- 填寫專案說明、metadata、來源證據和版權核查檔案。
- 抓取或讀取原文。
- 清洗、分章、建立術語表和文體畫像。
- 進入試譯、分章翻譯、審校和 EPUB 製作。

新書工程會放在：

```text
books/{book_id_or_author_title_slug}/
```

例如：

```text
books/pg20923_a_negro_explorer_at_the_north_pole/
```

### 第三步：讓 AI 自動生成來源和專案說明

這些檔案主要由 AI 自動填寫，人類只需要複核，不需要手動從零填寫。

AI 會把關鍵資訊寫入：

- `PROJECT_BRIEF_ZH_EN.md`
- `metadata/book.yaml`
- `metadata/rights_checklist.md`
- `metadata/source_evidence.md`

你可以檢查這些問題：

- 書名、作者、生卒年是否正確。
- 原文來源 URL 是否可靠。
- 版權判斷是否寫得謹慎，沒有把“美國公版”直接說成“全球公版”。
- 翻譯方向是否正確。
- 有沒有誤用了現代出版社版本、現代註釋版或盜版來源。

### 第四步：在人類可干預點檢查

AI 可以全流程自動跑，但最好在幾個節點請人看一眼。你不需要懂全部工程，只要開啟對應檔案，提出“通過 / 不通過 / 哪裡不對”即可。

#### 譯前研究階段

看這些檔案：

- `metadata/book_specific_translation_research.md`
- `metadata/style_profile.md`
- `glossary/terms.csv`
- `glossary/style_guide.md`

適合檢查：

- 作者、時代、題材理解是否靠譜。
- 文體判斷是否符合原書。
- 人名、地名、術語是否統一。
- 歷史稱謂、民族稱謂、宗教或文化內容是否需要譯註。

#### 預翻譯階段

看這個檔案：

- `qa/pretranslation/pretranslation_report.md`

適合檢查：

- 試譯是否像自然中文或自然英文。
- 有沒有明顯機器味。
- 難句、關鍵句、開篇語氣是否處理得好。
- 如果試譯不好，要求 AI 回到研究或試譯階段返工，不要直接翻整本。

#### 章節翻譯控制階段

看這些目錄：

- `chapters/src/`：原文。
- `chapters/translated/`：初譯。
- `chapters/final/`：通過審校後的終稿。
- `qa/chapter_controls/`
- `qa/fidelity/`
- `qa/readability/`
- `qa/terminology/`
- `qa/imagery/`
- `qa/gates/`

適合檢查：

- 有沒有漏譯、誤譯。
- 人名、地名、數字、方向是否錯誤。
- 讀起來是否順。
- 是否有機械直譯、過度發揮、省字式翻譯。
- 術語是否前後一致。

#### 預製作階段 1

看這個檔案：

- `preproduction/stage1/production_spec.md`

適合檢查：

- 書名、作者、譯製資訊是否正確。
- 封面方向是否合適。
- metadata 是否包含來源、公版說明、LifeBook 書坊資訊。
- 標題、目錄、版式、字型策略是否適合閱讀器。

#### 預製作階段 2

看這些檔案：

- `preproduction/stage2_sample/sample_book.epub`
- `preproduction/stage2_sample/sample_review.md`

適合檢查：

- 樣章 EPUB 能否開啟。
- 手機窄屏下標題是否太大。
- 正文行距、縮排、封面、目錄是否舒服。
- 如果樣章不好看，讓 AI 先修樣章，不要急著生成整本。

#### 全書 EPUB 和最終評審

看這些檔案：

- `output/book.epub`
- `output/epubcheck.json` 或 `output/epubcheck.log`
- `reviews/agent_a/review.md`
- `reviews/agent_b/review.md`
- `reviews/scorecards/final_quality_score.md`
- `reviews/revision_route.md`

適合檢查：

- EPUB 是否能在常用閱讀器開啟。
- EPUBCheck 是否 fatal=0、error=0。
- 獨立評審是否還有必須修的問題。
- 如果還有 P0/P1/P2 問題，應讓 AI 回到對應階段返工。

### 第五步：讓 AI 繼續，直到生成 EPUB

如果你不想參與中間階段，也可以讓 AI 全自動跑完。只要記住最終至少檢查這幾個結果：

- `output/book.epub` 存在。
- EPUB 可以開啟。
- `output/epubcheck.json` 或 `output/epubcheck.log` 沒有 fatal/error。
- `metadata/rights_checklist.md` 沒有明顯版權風險。
- 至少有人試讀過一部分正文。

## 如果你只想幫一點點

完全可以。

你可以只做下面任意一件事：

- 試讀 3 頁。
- 檢查一個章節標題。
- 幫忙確認一個人名怎麼譯。
- 找出一處錯別字。
- 對照一段原文看有沒有漏譯。
- 在手機閱讀器裡開啟 EPUB，看看排版是否舒服。
- 查一本候選書的作者死亡年份。
- 幫忙確認某個來源是不是公版。

這些小工作累積起來，就是一本書質量提升的來源。

## 提交反饋的建議方式

如果你熟悉 GitHub：

- 可以開 Issue。
- 可以提交 Pull Request。
- 可以直接評論某個檔案。

如果你不熟悉 GitHub：

- 複製有問題的句子。
- 寫明書名和章節。
- 用普通文字說明哪裡不順。
- 發給專案維護者即可。

反饋不需要完美。能指出“這裡我讀不懂”“這裡像機器翻譯”“這裡名字前後不一樣”，就已經很有幫助。

## 翻譯方向

當前模板按語言方向組織。`en-zh-Hans` 表示英文翻譯為簡體中文，`common` 表示所有語言方向共享的 EPUB 製作流水線。

未來可以支援更多方向：

- 英文公版書譯成中文。
- 法文、德文、日文等其他外文公版書譯成中文。
- 中文公版書譯成英文。
- 中文公版書譯成其他語言。

無論方向如何，原則不變：

- 先確認版權和來源。
- 先做譯前研究。
- 先試譯，再批次翻譯。
- 初譯不能直接釋出。
- 譯文必須經過人和 AI 的多輪檢查。
- EPUB 必須經過格式校驗和實際試讀。

如果是中文譯英文，需要相應調整：

- `metadata/style_profile.md` 中的目標文體。
- `glossary/terms.csv` 中的術語方向。
- `qa/readability/` 的審校標準。
- `prompts/` 中關於目標語言的表述。
- EPUB metadata 的語言欄位，例如 `en` 或 `en-US`。

## 重要原則

### 1. 不使用已有現代譯本作為翻譯來源

即使網上能找到中文譯本，也不要把它複製進專案，不要讓 AI 參考、改寫或對照它。我們只從公版原文重新翻譯。

### 2. 不使用盜版來源

不要從盜版站、網盤、非授權 EPUB 站下載文本作為底本。

### 3. 不把 AI 初稿當成成品

AI 初稿只是起點。真正重要的是審校、返工、統一、試讀和出版前檢查。

### 4. 保留失敗記錄

如果某次試譯失敗，應該記錄失敗原因。失敗記錄會幫助後面的人少走彎路。

### 5. 模板目錄只讀

`template/epub_pipeline/` 是模板區。做新書時讓 AI 複製 `common/` 並覆蓋對應語言方向目錄，例如 `en-zh-Hans/`，不要直接在模板目錄裡寫某本書的資料。普通參與者不需要閱讀模板裡的每個提示詞檔案。

## 給 AI 助手的最小啟動提示詞

如果你想讓 AI 幫你從一本公版書開始，可以使用下面這段，然後替換書名和來源。

```text
請在本倉庫中製作一本新的公版書翻譯工程。

共享模板目錄：template/epub_pipeline/common
語言模板目錄：template/epub_pipeline/en-zh-Hans
新書目錄：books/{請用書號或書名生成清晰目錄名}
原文來源：{填寫 Project Gutenberg / Wikisource / Standard Ebooks 等可靠來源 URL}
翻譯方向：{例如 英文到中文 / 中文到英文 / 日文到中文}

要求：
1. 不要直接修改模板目錄。
2. 先複製 common 模板到新書目錄，再覆蓋複製語言方向模板。
3. 先做來源與版權核查，不能確認公版就停止。
4. 不要使用已有現代譯本作為翻譯來源。
5. 先做譯前研究、術語表、文體畫像和預翻譯試譯。
6. 預翻譯沒有 PASS，不要批次翻譯。
7. 每章必須經過忠實度、可讀性、術語、意象詞和章節門禁檢查。
8. 最終生成 EPUB，並執行 EPUBCheck 或等價校驗。
9. 記錄所有關鍵產物路徑，方便其他人繼續審校。
```

## 版權和授權說明

每一本源書都要單獨核查版權。某個文本在一個國家或地區進入公版，不代表自動在所有地區都進入公版。

Project Gutenberg 文本通常說明其在美國為公版。若要面向其他地區公開發布，仍應按目標地區複核版權狀態。

本專案中產生的譯文、註釋、封面、排版和 EPUB 打包等非程式碼內容，預設面向公眾按 `CC BY-NC-SA 4.0` 發布；第三方商業使用必須另行取得 LifeBook 書坊及相關權利人的授權。

貢獻者提交內容，即表示同意其貢獻可納入本專案公開發布，並可由 LifeBook 書坊用於 LifeBook 產品與服務。LifeBook 書坊負責專案組織、發布、品質控制、授權管理和貢獻者回饋安排；具體署名和回饋方式按貢獻情況與專案規則決定。

更多說明：

- [LICENSE.md](LICENSE.md)：公開授權和程式碼授權。
- [CONTRIBUTING.md](CONTRIBUTING.md)：貢獻者授權與參與規則。
- [COMMERCIAL_LICENSE.md](COMMERCIAL_LICENSE.md)：第三方商業使用授權說明。

## 一個實際邀請

如果你喜歡書，也願意讓一些被忽略的公版作品被更多人讀到，可以從很小的事情開始：試讀一章，標出一句彆扭的話，檢查一個人名，開啟一次 EPUB。一本書就是靠這些小而具體的注意力慢慢變好的。
