# 《幽灵海盗》EPUB 预制作规格

production_spec_status: "PASS"
human_required: false

## 书籍身份

- 中文书名：《幽灵海盗》
- 英文原名：The Ghost Pirates
- 作者：William Hope Hodgson
- 译制：LifeBook 书坊 SaberOnGo
- 译制日期：2026-05-13
- 公版来源：https://www.gutenberg.org/ebooks/10966
- 原文文件：https://www.gutenberg.org/ebooks/10966.txt.utf-8
- 公版说明：Project Gutenberg 标记为美国公版文本；作者 1918 年去世，按 life+50 基线亦可进入中国大陆公版判断。译制不使用现代中译本。

## 封面

- 封面来源：GPT-IMAGE-2 生成无文字主视觉 `assets/cover_background_gpt_image_2.png`，再由 `scripts/generate_cover.py` 确定性叠加封面文字，最终工程文件为 `assets/cover.jpg`。
- EPUB 内封面：`cover.xhtml` + `EPUB/images/cover.jpg`。
- OPF 要求：manifest 必须含 `properties="cover-image"`。
- 封面策略：夜雾、全帆装船、幽灵船和灰色影子登船的海洋恐怖情境；上方留负空间，中文大标题和英文标题居中且各占一行。
- 封面文字：仅包含《幽灵海盗》、`The Ghost Pirates`、`威廉·霍普·霍奇森 著`、`LifeBook 书坊 译制`、底部一行“依据 Project Gutenberg #10966 公版原文制作”。

## 版本说明页

EPUB 必须包含 `book-info.xhtml`，并列出：

- 中文书名、英文原名、作者、译制方和译制日期。
- Project Gutenberg 来源 URL。
- 公版说明。
- 本书简介：只介绍作品内容、叙事方式和题材气质，不混入 EPUB 制作、译者署名、来源 URL 或版权复核提醒。
- 作者简介：国籍、生卒年、基本人生经历、代表作。
- 创作背景：本书出版年代、时代背景、题材背景和霍奇森海洋恐怖写作脉络。

## 字体与排版

- 不嵌入完整中文字体。
- 不锁死具体中文字体，允许阅读器与用户设置接管。
- 正文段首缩进 `2em`，行距适合中文长文阅读。
- 章节导航使用短标题：题名页、作者序、船歌、第一章至第十六章。
- 旧纸书目录、页码和 Project Gutenberg boilerplate 不进入正文。

## 构建前检查

- `output/publication_lint.json` 必须存在。
- `publication_lint` 不得有硬错误。
- 所有章节必须有 translated、final、control、fidelity、readability、imagery、terminology、gate 记录。

## PASS 条件

- 来源证据和版权核查为 PASS。
- 译前研究、风格档案、试译样本为 PASS。
- 19/19 章节通过章节门禁。
- 构建脚本能生成完整 EPUB。
- EPUBCheck fatal=0、error=0。
