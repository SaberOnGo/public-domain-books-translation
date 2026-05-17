# 《Almagest》图表重绘工作流 / Diagram Redraw Workflow

diagram_redraw_workflow_status: `PROVISIONAL_FOR_PRETRANSLATION`

| figure_id | source_location | figure_type | gpt_image_2_allowed | draft_path | final_asset_path | label_check | geometry_check | accessibility_check | status |
|---|---|---|---|---|---|---|---|---|---|
| BookI-figure-TBD | Book I | geometry/astronomy | yes_draft_only | assets/figures/drafts/ | TBD SVG/TikZ | TODO | TODO | TODO | TODO |

## GPT-Image-2 使用规则

- GPT-Image-2 只用于草图、视觉辅助和重绘初稿。
- 最终图必须转成 SVG、TikZ、结构化 HTML 或可校验高分辨率图。
- 所有标签必须和术语表、notation registry、正文引用一致。
- 几何关系必须由数学/天文学校对确认。
- 复杂图必须有中文替代文本或长描述。

## Almagest 专门要求

- 模型图必须区分圆心、地球、偏心点、等分点、均轮、本轮和观察方向。
- 几何证明图必须保持点名、线段、弧、圆和角度关系。
- 图注必须说明“原图重绘”或“现代辅助示意图”，不得混淆。
- Book I.10 试制 EPUB 使用 Heiberg PDF facsimile 裁图时，必须由脚本保证：完整保留原图字母标签，自动补少量白边，检测边缘墨迹，避免裁掉标签。
- 若原书正文紧贴图形，允许脚本白除邻近正文，但遮盖区域必须写入脚本配置；不得在 EPUB 中使用夹带正文、脚注或页码的裁图。
- 手机 EPUB 图像必须响应式缩放，使用整行 `<figure>`，不得与正文并排压缩。
