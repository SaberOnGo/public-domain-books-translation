# 19 复盘与模板回填 / Retrospective and Template Update

## 任务

成书或试译结束后，必须复盘：

1. 哪些文言文问题是本书特有。
2. 哪些问题应回填到 `lzh-zh-Hans`。
3. 哪些问题属于 `targets/zh-Hans`。
4. 哪些问题属于 `common`。
5. 历史叙事、人物关系、国家关系、制度注释等是否应回填到 `classical-history-zh-Hans`。

## 输出

- `qa/retrospective/template_backfill_report.md`
- 对模板的最小必要修改。
- 回填后重新运行 create-book dry-run 和相关测试。

## 门禁

如果试译暴露了可复用模板缺陷，却没有回填，不能开始正式批量翻译。
