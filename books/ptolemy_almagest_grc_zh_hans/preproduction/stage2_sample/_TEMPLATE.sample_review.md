# 样章检查模板 / Sample Chapter Review Template

sample_review_status: "DRAFT" # PASS | FAIL
human_required: false

## 检查项 / Checklist

- [ ] 样章 EPUB 可打开。
- [ ] EPUBCheck fatal=0。
- [ ] EPUBCheck error=0。
- [ ] 封面存在。
- [ ] OPF `cover-image` 正确。
- [ ] 版本说明页存在。
- [ ] 书籍信息页含 `LifeBook 书坊 + 个人名`。
- [ ] 无 `LifeBook 翻译组` 等旧品牌残留。
- [ ] 字体未被不合理锁死。
- [ ] 未嵌入完整超大中文字体。
- [ ] `第X章` 与章节说明字号协调。
- [ ] 正文段落、行距、缩进适合中文长文阅读。
- [ ] 若样章含图，Markdown 图片已转换为 XHTML `<figure>`，图片文件存在。
- [ ] 若样章含图，`img alt`、`figcaption` 和必要长描述存在。
- [ ] 若样章含表，表格为 XHTML `<table>`，含 `caption`、`thead`、`th`。
- [ ] 样章 EPUB 的 OPF manifest 登记所有图片、样式、字体等资源。
- [ ] `output/asset_manifest_check.json` 或样章等效资源检查无硬错误。
- [ ] 文件体积合理。

## 自动结论 / Auto Conclusion

若任一核心项失败，`sample_review_status=FAIL` 并回到预制作阶段修正。
