# 《幽灵海盗》GPT-IMAGE-2 封面重制记录

review_status: "PASS"
date: "2026-05-14"

## 问题

旧封面存在以下问题：

- 主视觉偏几何化，不够贴合《幽灵海盗》的海洋恐怖情境。
- 中文书名与图像元素有重叠风险。
- 封面文字包含过多信息，不符合新版 `cover_design_policy.md` 的“只放必要封面文字”规则。

## 重制方案

- 使用 GPT-IMAGE-2 生成无文字背景图：`assets/cover_background_gpt_image_2.png`。
- 背景 prompt：`assets/cover_background_prompt_gpt_image_2.txt`。
- 背景内容依据本书情境：夜雾、十九世纪全帆装船、幽灵船、灰色影子登船、海洋恐怖氛围。
- 使用 `scripts/generate_cover.py` 确定性叠加封面文字，避免图像模型生成中文错字或文字错位。

## 封面文字

最终封面只包含：

- `幽灵海盗`
- `The Ghost Pirates`
- `威廉·霍普·霍奇森 著`
- `LifeBook 书坊 译制`
- `依据 Project Gutenberg #10966 公版原文制作`

封面不再包含个人译者名；个人译者名保留在书籍信息页、metadata 和 OPF 中。

## 输出

- 最终封面：`assets/cover.jpg`
- 封面尺寸：1600 x 2400
- 封面体积：519920 bytes
- 封面 SHA256：`43A95197DDA1944CA4D487D4A591D653E1C8A08F567028913BF829B819892E4F`

## 验证

- 中文大标题居中，一行展示。
- 英文标题居中，一行展示。
- 作者、译制、底部来源均为独立行。
- 标题区位于上方暗色负空间，没有压住船体主视觉。
- EPUB 内部使用 `EPUB/images/cover.jpg`。
- EPUB 未打包 `cover.svg`。
- OPF `cover-image` 指向 JPG。
- `npm run build:epub`：PASS。
- `npm run check:epub`：PASS，EPUBCheck `fatal=0`、`error=0`、`warning=0`。
