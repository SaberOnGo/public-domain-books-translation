# 01 来源获取与清洗 / Ingest and Clean

## 输入

- `SOURCE_URL` 或 `LOCAL_SOURCE_FILE`
- `metadata/source_evidence.md`
- `metadata/rights_checklist.md`

## 任务

1. 获取文言文底本，保留原始来源文件到 `source/`。
2. 记录来源 URL、获取日期、权利口径、底本说明和文本形态。
3. 区分正文、题解、现代注释、站点说明、版权说明和转写者说明。
4. 不改写原始 evidence；清洗后的工作文本另存。
5. 创建或更新 `metadata/classical_chinese_source_profile.md`、`metadata/source_witness_manifest.md` 和 `qa/textual/classical_chinese_textual_notes.md`。

## 门禁

- 公开项目权利不清楚时停止。
- 现代版权译文、商业校注或盗版 EPUB 不能作为来源。
- 未区分现代标点/注释/转写成分时不得进入分章。
