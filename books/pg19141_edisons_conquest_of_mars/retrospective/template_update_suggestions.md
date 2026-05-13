# 模板更新建议 / Template Update Suggestions

status: "PASS"

## 建议

- 对 Project Gutenberg 同书多条目情况，可在通用来源证据模板中增加 `duplicate_reference_url` 字段。
- 对源文只有章节编号的小说，应在 `chapter_title_map.yaml` 和制作规格中明确“不添加读者可见概括标题”。
- 批量翻译时，建议在出版 lint 前单独扫描每章中文分号数量，优先修复超过阈值章节。

## Decision

本书暂无必须立即回填模板的阻塞项；以上为后续优化建议。
