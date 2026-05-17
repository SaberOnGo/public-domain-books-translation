# GPT-Image-2 图表重绘工作流 / GPT-Image-2 Diagram Workflow

## 目的 / Purpose

GPT-Image-2 可用于生成图表草图、风格稿和辅助理解图，但古典科学书的最终图表必须经过结构化复核。

## 允许用途 / Allowed Uses

- 根据原书图和正文说明生成清晰草图。
- 生成面向读者的现代化辅助示意图。
- 帮助识别模糊扫描图中的标签、点线关系和空间布局。
- 生成后再转写为 SVG、TikZ 或结构化图表规格。

## 禁止用途 / Forbidden Uses

- 不得把 GPT-Image-2 输出直接当作最终学术图。
- 不得让模型自行补图中不存在的点、线、圆、箭头或标签。
- 不得用美观图替代数学关系正确的图。
- 不得输出无法追溯源图和正文依据的图。

## 必须产物 / Required Outputs

每个重绘图必须有：

- `source_figure_id`
- `source_location`
- `source_caption_or_context`
- `redraw_prompt`
- `draft_image_path`
- `final_structured_asset_path`
- `label_mapping`
- `geometry_check`
- `text_reference_check`
- `accessibility_description`
- `status`

## 最终格式 / Final Format

优先级：

1. SVG。
2. TikZ 或可复现绘图源。
3. 结构化 HTML/CSS 图。
4. 位图，仅用于无法结构化表达的场景，并必须保留高分辨率源和说明。

