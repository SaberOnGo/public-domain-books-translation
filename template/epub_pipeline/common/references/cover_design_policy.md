# 封面设计与生成规则 / Cover Design and Generation Policy

policy_status: "ACTIVE"
scope: "all language pairs / 所有语言方向"

## 目的 / Purpose

本规则把模板中原本分散在预制作、样章、全书制作、最终输出和 EPUB 经验记录里的封面要求集中到一处。所有新书在制作封面前，必须先读取本文件，再写入书本自己的 `preproduction/stage1/production_spec.md`。

This policy centralizes cover requirements that were previously scattered across preproduction prompts, sample review prompts, full-build prompts, final-output prompts, and EPUB production lessons. Read this file before designing a cover for any book project.

## 来源 / Extracted From

- `template/epub_pipeline/common/preproduction/stage1/_TEMPLATE.production_spec.md`
- `template/epub_pipeline/common/epub_production_lessons.md`
- `template/epub_pipeline/en-zh-Hans/prompts/13_preproduction_stage1_spec_zh_en.md`
- `template/epub_pipeline/en-zh-Hans/prompts/14_preproduction_stage2_sample_zh_en.md`
- `template/epub_pipeline/en-zh-Hans/prompts/15_full_book_production_zh_en.md`
- `template/epub_pipeline/en-zh-Hans/prompts/16_independent_review_agents_zh_en.md`
- `template/epub_pipeline/en-zh-Hans/prompts/18_final_output_zh_en.md`
- prior successful EPUB QA and cover revision records / 既有成功 EPUB 的封面整改记录

## 硬性要求 / Hard Requirements

- EPUB 必须有内部封面图片，不得只依赖阅读器自动生成封面。
- EPUB 必须有 `cover.xhtml`。
- OPF manifest 必须把封面图片标记为 `properties="cover-image"`。
- EPUB 内封面推荐使用 `cover.jpg`；高清 PNG/PSD/工程源文件可以保留在书籍工程目录，但不得直接把超大未压缩源图塞入 EPUB。
- 封面比例建议为 2:3 或接近传统书封比例；推荐尺寸为 1600 x 2400 px，长边可在 1600-2560 px 范围内。
- EPUB 内封面体积建议控制在 200KB-800KB；除非有明确理由，不应达到数 MB。
- 封面、书籍信息页、OPF metadata 中的书名、作者、译者/译制者、品牌名必须一致。
- 封面图像必须有可理解的替代文本，例如书名或“书名封面”。
- 不能使用现代受版权保护的封面、插画、影视剧照、盗版图片或来源权利不明的图片。

## 设计目标 / Design Goals

封面不是“能显示一张图”即可。封面必须承担四个读者信号：

1. 书籍身份：目标语书名是第一视觉层级，原名或副标题是第二层级。
2. 题材气质：视觉主题必须来自本书内容、时代、地域、人物或核心意象。
3. 版本身份：封面使用简洁统一署名 `LifeBook 书坊 译制`，个人译者名放入书籍信息页。
4. 公版来源：底部最多一行小字说明 Project Gutenberg 或其他公版来源，不得压过书名。

视觉上应做到：

- 标题清楚、居中或按明确网格排版，窄缩略图中也能识别。
- 文字与背景有足够对比，不被复杂图像吞掉。
- 主视觉与书名互相支持，不使用空泛装饰图。
- 保留安全边距，避免标题、作者、品牌贴边。
- 色彩服务题材，不使用与作品气质冲突的廉价渐变或无关素材。

## 可复用封面原则 / Reusable Cover Principles

- 使用 1600 x 2400 的竖版封面比例。
- 用确定性排版控制目标语书名、原书名、作者、译制署名和来源说明。
- 主视觉必须围绕书本核心意象，不使用无关风景或泛泛装饰。
- 中文大标题应居中对齐，尽量只占一行；英文标题字体较小，居中对齐，也尽量只占一行。
- 如确有额外内容，可使用副标题或另起一行小字；不要把说明性内容堆到封面。
- EPUB 内封面应使用压缩后的 JPG，视觉可用且体积合理。
- 封面文字不依赖图像模型自动生成；文字居中、层级和品牌信息应由确定性排版核验。
- AI 图像模型适合生成背景图或主视觉，不适合直接生成精确中文标题。
- 封面文字应后期用 SVG/Canvas/HTML/CSS/图像处理脚本确定性叠加。
- 如果生成式背景图质量不够，应重做主视觉，不要靠文字遮掩。

## 封面生成 Prompt 模板 / Cover Image Prompt Template

用于生成“无文字背景图”时，先填以下设计 brief。封面文字另行确定性排版。

```text
Book cover background art only, no text, no letters, no logos.

Book:
- Target-language title: {target_title}
- Original title: {original_title}
- Author: {author}
- Source and period: {public_domain_source_and_publication_period}
- Genre and tone: {genre_tone}
- Core scene or symbol from the book: {core_scene_or_symbol}
- Important things that must appear: {must_have_visual_elements}
- Things that must not appear: {forbidden_elements}

Composition:
- Vertical 2:3 book-cover composition.
- Leave clean negative space for later title placement in the upper or middle area.
- Strong single focal scene, readable as a small bookshelf thumbnail.
- Historically plausible clothing, objects, ships, landscape, architecture, or tools.
- Atmospheric but concrete; avoid generic stock-photo mood.

Style:
- {visual_style}, publication-quality illustration.
- Controlled palette matching the book's genre and period.
- High contrast where title text will be placed later.
- No modern copyrighted character likenesses, no movie-poster imitation, no fake publisher logos.

Output:
- 1600 x 2400 px or larger, suitable for downsampling to EPUB JPG.
- No embedded typography.
```

## 封面文字排版模板 / Deterministic Cover Typography Template

封面文字应由脚本、SVG、HTML/CSS 截图或图像处理流程生成，不交给图像模型自由绘制。

必备文字层级：

1. 目标语书名：最大字号，居中对齐，尽量一行展示。
2. 原书名：小于主标题，居中对齐，尽量一行展示。
3. 可选副标题或额外信息：仅在必要时使用，另起一行小字。
4. 作者：目标语言常用译名 + “著”等本地化署名方式。
5. 译制者：固定使用 `LifeBook 书坊 译制`。
6. 来源说明：封面底部最多一行小字，例如“依据 Project Gutenberg #xxxxx 公版原文制作”。

排版要求：

- 主标题与作者、译制者之间必须有清晰层级。
- 中文大标题和英文标题尽量分别只占一行；只有在一行会明显不可读时，才允许按语义断行。
- 额外内容必须使用副标题或小字另起一行，不能挤入主标题。
- 不要把所有文字都堆在同一块区域。
- 底部来源说明可以小，但不能糊成不可辨认的噪声。
- 除目标语书名、原书名、可选副标题/额外信息、作者、`LifeBook 书坊 译制`、底部来源说明外，不要在封面写其他内容。
- 生成后必须人工或脚本检查居中、边距、错字、品牌一致性。

## 预制作检查 / Preproduction Checks

在 `preproduction/stage1/production_spec.md` 中必须写明：

- 封面来源：AI 生成 / 公版图片 / 自制设计 / 其他。
- 主视觉依据：来自哪一章、哪一场景、哪一历史背景或哪一核心意象。
- 图像权利：公版证据、AI 生成说明或自制说明。
- 尺寸、格式、压缩目标。
- EPUB 内部文件名，通常为 `assets/cover.jpg` 和 `EPUB/images/cover.jpg`。
- `cover.xhtml` 和 OPF `cover-image` 写入方式。
- 封面文字排版方式：确定性 SVG、Canvas、HTML/CSS 截图或图像处理脚本。

## 样章和最终检查 / Sample and Final Checks

样章阶段必须检查：

- 封面是否存在。
- OPF 是否写入 `cover-image`。
- 封面体积是否合理。
- 书架缩略图能否识别书名。
- 封面、书籍信息页、metadata 的品牌和译制者是否一致。
- 是否仍有旧品牌名。
- 是否把超大 PNG 或工程源文件打进 EPUB。

最终输出阶段必须检查：

- `EPUB/images/cover.jpg` 或等效封面资源存在。
- `EPUB/cover.xhtml` 存在。
- `package.opf` 只有一个正确的 `cover-image`。
- EPUBCheck fatal=0、error=0，warning 需修复或记录。
- `output/final_manifest.md` 记录封面文件、EPUB 大小、SHA256 和校验结果。

## 禁止事项 / Forbidden

- 禁止没有封面就发布 EPUB。
- 禁止只有外部封面文件而 EPUB 内部没有封面。
- 禁止把 2MB-10MB 的未压缩封面直接塞入普通文本 EPUB。
- 禁止使用权利不清晰的现代封面或图片。
- 禁止让图像模型直接生成最终中文书名后不检查。
- 禁止封面、metadata、书籍信息页使用不同译者名或旧品牌名。
- 禁止用无关风景、抽象渐变或空洞装饰替代书本核心意象。
