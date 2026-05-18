# /goal：补齐 GPT-IMAGE 封面、书籍信息页与全书二次精修复核

status: "PASS"

## 目标

在已完成《爱迪生征服火星》出版级术语、标题和长段落精修的基础上，补齐与 `1_pg20923_a_negro_explorer_at_the_north_pole`、`2_pg10966_the_ghost_pirates` 同级的栅格封面产物，并再次复核书籍首页信息、译者署名、EPUB 内封面引用、重点段落文学性和全书“信达雅”闭环。

## 执行边界

- 书籍目录：`books/zh-Hans/3_pg19141_edisons_conquest_of_mars/`
- 译者署名：`LifeBook 书坊 SaberOnGo`
- 图像生成：使用 GPT-IMAGE 生成符合本书情节的源图，不再使用脚本绘制的几何 SVG 作为最终封面主体。
- EPUB 内封面：使用压缩后的 `assets/cover.jpg`，控制体积，不把大源图直接打入 EPUB。
- 历史记录：本轮曾保留脚本生成的 `output/cover.svg` 作为工程备用产物；此规则已被 2026-05-14 最新封面规则取代，最终输出不再保留 `output/cover.svg`。

## 参考经验

- `1_pg20923_a_negro_explorer_at_the_north_pole`：保留高清源图，EPUB 内使用压缩 JPG；封面页和 OPF `cover-image` 必须存在。
- `2_pg10966_the_ghost_pirates`：封面必须与本书情节一致，书籍信息页要包含 `LifeBook 书坊 + 个人名`、译制时间、公版来源 URL、公版说明。
- 本模板要求：封面、书籍信息页、metadata、目录、EPUBCheck 和 publication lint 都是最终质量的一部分。

## 执行清单

1. 使用 GPT-IMAGE 生成本书专属源图：火星、地球、电力飞船舰队、维多利亚时代电气机械、分解射线。
2. 将源图保存为 `assets/cover_source_gpt_image.png`。
3. 叠加确定性中文书名、英文原名、作者、译者和 Project Gutenberg 来源信息，压缩为 `assets/cover.jpg`。
4. 把书籍首页从“版本说明”统一为“书籍信息”。
5. 重新构建 EPUB，确认 OPF `cover-image` 指向 `EPUB/images/cover.jpg`。
6. 补写本轮 QA，记录封面、首页、全书文学性和重点段落复核结果。
7. 运行 publication lint、EPUBCheck、refinement check，并复制最新样书。

## 完成记录

- GPT-IMAGE 源图已保存：`assets/cover_source_gpt_image.png`。
- EPUB 封面图已保存：`assets/cover.jpg`，约 286KB，符合模板 200KB-800KB 建议区间。
- 封面内容与本书情节相符：火星、地球、爱迪生式电力飞船舰队、分解射线、电气火花。
- 历史记录：本轮封面可见文字曾包含个人名；此规则已被 2026-05-14 最新封面规则取代，最终封面只包含书名、原名、作者、`LifeBook 书坊 译制` 和一句公版来源说明。
- 书籍首页已统一为“书籍信息”，并包含译者、译制时间、公版来源和公版说明。
- 重新构建后 EPUB 内封面使用 `cover.jpg`，不是 SVG 占位封面。
- 历史记录：本轮解包抽查的旧封面尺寸记录已作废；2026-05-14 重制后 `EPUB/images/cover.jpg` 为 456011 bytes，OPF `cover-image` 指向 `images/cover.jpg`。
- 校验状态：publication lint PASS；EPUBCheck fatal 0，error 0，warning 0；refinement check 出版范围 BOM 0，mojibake 0，中文异常空格 0。

## Decision

PASS。封面、书籍信息页、全书复核和 EPUB 工程闭环已补齐。
