# EPUB 质量复核 / EPUB Quality Review

结论：PASS_REFINED_WITH_RECORDED_LIMITATIONS

## 构建前要求

- 已运行 `npm run lint:publication`，硬错误为 0。
- 已运行 `npm run build:epub`，生成 `output/book.epub` 和 `output/环球航海记.epub`。
- 已运行 `npm run check:epub`，`fatal=0`、`error=0`、`warning=0`。
- 本轮精修后已重新构建 EPUB；封面与 metadata 均显示 `LifeBook 书坊 SaberOnGo`。

## 重点检查

- 封面、版本说明、目录、正文开始位置。
- 章节标题是否使用中文短题名。
- 正文是否存在 mojibake、异常空格、英文标题残留、纸书页码目录或 Gutenberg 许可证。
- 移动端下术语表长条目是否可读。
- 书籍首页信息页含译制者、来源、版权状态、原书信息与简介。

## 限制

当前 EPUB 格式校验通过，且关键章节已完成机器辅助信达雅精修。公开发布前仍建议人工抽查长章、术语表和广州/澳门相关章节。
