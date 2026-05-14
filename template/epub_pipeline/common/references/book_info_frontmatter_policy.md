# 书籍信息页与前置页规则 / Book Info and Added Frontmatter Policy

policy_status: "ACTIVE"
scope: "all language pairs / 所有语言方向"

## 目的 / Purpose

本规则把模板中分散在预制作、样章、全书制作、独立评审、最终输出和既有成功 EPUB 返工记录里的“书籍信息页 / 版本说明页 / 翻译添加前置页”要求集中到一处。

Here, “book info” means reader-visible pages added by the translation project before the original text begins. It may be one page or two pages. It is not the same as the author's original preface, source front matter, or original title page.

## 来源 / Extracted From

- `template/epub_pipeline/common/preproduction/stage1/_TEMPLATE.production_spec.md`
- `template/epub_pipeline/common/epub_production_lessons.md`
- `template/epub_pipeline/en-zh-Hans/prompts/13_preproduction_stage1_spec_zh_en.md`
- `template/epub_pipeline/en-zh-Hans/prompts/14_preproduction_stage2_sample_zh_en.md`
- `template/epub_pipeline/en-zh-Hans/prompts/15_full_book_production_zh_en.md`
- `template/epub_pipeline/en-zh-Hans/prompts/16_independent_review_agents_zh_en.md`
- `template/epub_pipeline/en-zh-Hans/prompts/18_final_output_zh_en.md`
- prior successful EPUB build scripts and QA revision records / 既有成功 EPUB 的构建脚本与整改记录

## 定义 / Definition

翻译项目添加的前置页通常包括：

1. 封面页：`cover.xhtml`。
2. 书籍信息页：`book-info.xhtml`，建议读者可见标题为“书籍信息”或目标语言等效标题。
3. 可选译者说明页：当公版说明、译者说明或版本说明较长时，可以拆成第二个前置页。

这些页面必须清楚标明是本项目添加的信息，不能伪装成原书内容。原书自带的序言、题辞、目录、献词、作者说明等应作为原书前置内容保留，并与本项目添加页区分。

## 硬性要求 / Hard Requirements

- EPUB 必须包含 `book-info.xhtml` 或等效书籍信息页。
- `nav.xhtml` 必须有读者可见入口，推荐标题为“书籍信息”。
- OPF manifest 必须列出书籍信息页。
- spine 中书籍信息页应位于封面之后、正文或原书前置内容之前。
- landmarks 中应把书籍信息页标为 frontmatter。
- 书籍信息页必须使用目标语言贡献者能读懂的本地语言；英文可以并列补充，但不能只用英文，除非目标语言本身是英语。
- 书籍信息页、封面、OPF metadata、`metadata/book.yaml` 中的书名、作者、译者/译制者、出版方、来源和版权说明必须一致。
- 不得保留旧品牌名，例如 `LifeBook 翻译组`。
- 书籍信息页中的译者/译制者必须写详细，格式为 `LifeBook 书坊 + 个人名`，个人名按 contributor 提供的拼写精确写入。

## 必备内容 / Required Content

书籍信息页必须优先展示本项目版本信息，然后再展示原书信息。

必备字段：

- 目标语言书名。
- 原书名。
- 作者：目标语言常用译名 + 括号原名。
- 译者/译制者：`LifeBook 书坊 + 个人名` 或对应项目规则。
- 翻译/译制时间。
- 公版来源名称与 URL，例如 Project Gutenberg 编号和链接。
- 公版/版权说明：说明源文本公版依据，并提醒跨地区发行需复核目标地区版权状态。
- 本书简介：只介绍作品内容、叙事方式、题材气质和核心看点，不写成广告文案。
- 作者简介：国籍、生卒年、基本人生经历、代表作。
- 本书创作基本背景：创作背景、时代背景、题材背景，帮助读者理解作者和本书。

可选字段：

- 关于本书的其他内容：只放对读者理解作品确有帮助的信息。
- 本项目说明：说明这是公版原文新译、校订或整理版本。
- 译者说明：仅在确有必要时说明译名原则、术语原则、版本选择或特殊排版处理。
- 权利与发行说明：中文译本或目标语译本的项目授权状态。

长度要求：

- 书籍信息页应短而完整，提供基本背景即可。
- “本书简介”不得混入本项目制作信息、译者署名、EPUB 制作说明、公版来源 URL、版权/地域复核提醒；这些内容应分别放在译者、原文来源、公版说明或 metadata 中。
- 作者简介和创作背景不应写成长篇研究文章。
- 额外内容必须克制，不能变成百科条目、宣传文案或制作日志。

## 页面拆分 / One or Two Page Model

如果内容较短，使用单个 `book-info.xhtml`：

- 书籍身份。
- 本项目版本信息。
- 本书简介。
- 作者简介。
- 本书创作基本背景。
- 公版说明。

如果内容较长，可以拆成两个前置页：

- `book-info.xhtml`：只放读者最需要的书籍身份、译制信息、来源、公版说明、本书简介、作者简介和创作背景。
- `translator-note.xhtml` 或 `edition-note.xhtml`：放译者说明、术语说明、版本选择、制作说明、更长的版权/地域提醒或“关于本书的其他内容”。

拆分原则：

- 第一页必须短、清楚、能快速告诉读者“这是什么书、谁译制、依据什么来源制作”。
- 第二页只能承载确有价值的说明，不得成为 AI 工作日志或制作流水账。
- 原书作者序言不得混入本项目说明页。

## 设计与排版 / Design and Layout

书籍信息页应像正式出版物的版权页/版本页，而不是 README。

推荐结构：

```html
<section epub:type="frontmatter" class="book-info">
  <h1>书籍信息</h1>
  <dl>
    <dt>中文书名</dt><dd>...</dd>
    <dt>英文原名</dt><dd><em>...</em></dd>
    <dt>作者</dt><dd>作者译名（Original Name）</dd>
    <dt>译者</dt><dd>LifeBook 书坊 + 个人名</dd>
    <dt>译制时间</dt><dd>2026-05</dd>
    <dt>原文来源</dt><dd>Project Gutenberg #xxxxx，https://...</dd>
    <dt>公版说明</dt><dd>...</dd>
  </dl>
  <h2>本书简介</h2>
  <p>...</p>
  <h2>作者简介</h2>
  <p>...</p>
  <h2>创作背景</h2>
  <p>...</p>
</section>
```

排版要求：

- `h1` 不得过大，手机窄屏不应压迫。
- 信息列表推荐使用 `dl/dt/dd` 或清晰列表，不要堆成一大段。
- 段落行距、段首缩进和正文一致或略紧凑。
- URL 可以保留可读文本，但要允许换行，不得撑破屏幕。
- 信息页应在阅读器目录中可找到，但目录题名应短。
- 不要在信息页中放过长宣传语、AI 生成说明、内部 QA 细节或工作流日志。

## Metadata 同步 / Metadata Synchronization

书籍信息页不是孤立页面。以下位置必须同步：

- `metadata/book.yaml`
- OPF `dc:title`
- OPF `dc:creator`
- OPF `dc:contributor`
- OPF `dc:publisher`
- OPF `dc:source`
- OPF `dc:description`
- OPF `dc:rights`
- `book-info.xhtml`
- `nav.xhtml`
- 封面文字
- `output/final_manifest.md`

如果改译者名、书名、来源 URL、公版说明或简介，必须同步以上位置并重新构建 EPUB。

## 生成 Prompt 模板 / Book Info Generation Prompt

```text
Create the reader-visible book information frontmatter for this public-domain translation EPUB.

Inputs:
- Target language: {target_language}
- Target title: {target_title}
- Original title: {original_title}
- Author target-language name and original name: {author_names}
- Translator/producer: {translator_name}
- Translation or production date: {production_date}
- Public-domain source: {source_name_and_url}
- Rights evidence summary: {rights_evidence_summary}
- Original publication information: {original_publication_info}
- Book description: {book_description_only_about_the_work}
- Author background: {author_nationality_life_dates_life_experience_major_works}
- Composition and historical background: {composition_and_period_background}
- Optional other book context: {optional_other_book_context}
- Optional translator note topics: {translator_note_topics}

Rules:
- Use the target language as the primary reader-facing language.
- Prioritize project version information before original-book information.
- Use the translator naming rule exactly: LifeBook 书坊 + personal name, with the personal name spelling exactly as provided.
- Keep the first book-info page concise and reader-facing.
- Keep the book description strictly about the work itself; do not include EPUB production notes, translator credits, source URLs, public-domain notices, or regional rights reminders in the description.
- Include enough author and book background for readers to understand the work, but keep it brief.
- If explanations are long, split them into an optional second frontmatter page.
- Do not write marketing copy.
- Do not include AI workflow logs, QA logs, or internal production details.
- Do not invent publication facts not supported by metadata or source evidence.

Output:
1. `book-info.xhtml` or Markdown source that can build to it.
2. Optional `translator-note.xhtml` or Markdown source only if genuinely needed.
3. A metadata synchronization checklist covering OPF, nav, cover text, and final manifest.
```

## 样章与最终检查 / Sample and Final Checks

样章阶段必须检查：

- 书籍信息页是否存在。
- 目录是否有“书籍信息”或目标语言等效入口。
- 是否包含 `LifeBook 书坊 + 个人名`、译制时间、公版来源 URL、公版说明。
- 是否包含作者简介和本书创作/时代背景，且长度克制。
- “本书简介”是否只介绍作品本身，没有混入 EPUB 制作、译者署名、来源 URL 或版权复核提醒。
- 是否仍有旧品牌名。
- 页面是否过长、像 README 或像制作日志。
- 手机窄屏下 `h1`、`dl`、URL、段落是否可读。

最终输出阶段必须检查：

- EPUB 内存在 `EPUB/book-info.xhtml` 或等效文件。
- OPF manifest 与 spine 均包含该页。
- `nav.xhtml` 和 landmarks 均能到达该页。
- OPF metadata 与书籍信息页字段一致。
- 封面、metadata、书籍信息页使用同一译者/译制者。
- EPUBCheck fatal=0、error=0，warning 需修复或记录。
- `output/final_manifest.md` 记录最终书名、译者、来源、EPUB 大小、SHA256 和校验结果。

## 禁止事项 / Forbidden

- 禁止没有书籍信息页就发布 EPUB。
- 禁止只在 OPF metadata 写信息，而没有读者可见书籍信息页。
- 禁止书籍信息页缺少公版来源 URL 或公版说明。
- 禁止把原书作者序言改写成本项目说明。
- 禁止把制作日志、prompt、QA 过程或 AI 自述放进读者前置页。
- 禁止封面、书籍信息页和 metadata 的品牌名、译者名不一致。
- 禁止使用“LifeBook 翻译组”等旧名称。
