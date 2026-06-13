# Russian-to-Simplified-Chinese 复盘经验 / Retrospective Lessons

本文件只记录跨书可复用的俄语到简体中文模板经验。具体书籍的人物、章节、样本、QA、release 记录必须留在书籍工程内，不得复制到模板。

## 记录格式 / Entry Format

```text
date:
source:
defect_or_lesson:
finding_method:
low_token_audit:
fix_pattern:
recheck:
template_update:
```

## 当前模板基线 / Current Baseline

- 俄语长句先处理词序、格关系、分词/副动词结构、体貌、运动动词、反身/无人称结构和否定作用域，再重组成自然中文。
- 小说项目必须锁定人名、父称、昵称、军阶、官职、地名、宗教/民族称呼和社会身份词。
- 法语夹杂、旧正字法、现代化转写、扫描证据和删节风险必须在书籍工程的来源证据与文本疑难记录中说明。
- 每章译后全量检查和 EPUB 后分层随机抽检发现的可复用译文质量问题族，应优先回填到 `skills/translation-quality-defect-families/SKILL.md`；本文件只记录俄语方向模板层面的补充。
