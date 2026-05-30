# LifeBook Digest QA 清单

本清单用于审校每本书生成的 `qa/digest/digest_review_checklist.md` 和 `output/digest/` 产物。

## 结构

- [ ] Digest 是 post-EPUB optional step，不接管原翻译主流程。
- [ ] 具体书籍内容只写入该书工程下的 `output/digest/` 和 `qa/digest/`。
- [ ] 若合并 EPUB，新增章节已进入 OPF manifest、spine、nav。
- [ ] 输出仍是标准 EPUB，不要求阅读器支持专用格式。

## 内容

- [ ] 摘要忠实于原书或译文，没有虚构信息。
- [ ] 章节拓扑与 EPUB spine 阅读顺序一致。
- [ ] 知识脉络图的节点和关系有正文依据。
- [ ] 不包含 prompt、制作日志、本地绝对路径、QA 草稿或模型痕迹。
- [ ] 私人自用项目没有被写入可发布目录或 GitHub。

## 发布

- [ ] 合并后的 EPUB 已重新做结构校验。
- [ ] Digest 章节通过专项 QA。
- [ ] 如果发布，已生成新的 release 或 private artifact。
