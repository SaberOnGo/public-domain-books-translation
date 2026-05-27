# 古文今译对照正文规则 / Source-Modern Parallel Text Policy

## 核心规则

文言文到现代中文 EPUB 的默认读者版正文为：

1. 古文原文一段。
2. 对应现代中文今译一段。
3. 必要注释紧随相关 passage 或集中到章末/节末。

## XHTML 建议结构

```html
<section class="parallel-passage" id="p001">
  <p class="source-text" lang="lzh">臣闻之，...</p>
  <p class="modern-text" lang="zh-Hans">我听说，...</p>
  <aside epub:type="footnote" id="note-p001-1">...</aside>
</section>
```

## 构建要求

- `chapters/final/*.md` 不得带生产 YAML front matter、章节控制说明、QA 状态或 prompt 痕迹。
- EPUB 构建器必须保留 `section.parallel-passage`、`p.source-text`、`p.modern-text` 和 `aside epub:type="footnote"` 等 raw XHTML 结构，不得把它们转义成 `&lt;section...&gt;` 这类可见源码。
- 生成的 XHTML 根元素必须绑定 `xmlns:epub="http://www.idpf.org/2007/ops"`，否则 `epub:type` 注释属性会造成 EPUBCheck fatal。
- OPF identifier 必须是合法标识符。若使用 `urn:uuid:`，值必须是合法 UUID。
- 样章或正式 EPUB 构建后必须直接检查 `output/epub_work/EPUB/*.xhtml`，确认存在 `parallel-passage`，且不存在被转义的 `&lt;section`。
- 对照正文 CSS 应提供 `source-text`、`modern-text`、`aside` 的基本区分，但不得锁死中文字体或字号。

## 对齐要求

- `source-text` 和 `modern-text` 必须表达同一 passage，不得把多个古文段落合并成一个大意段。
- 如原文极短、连续虚词或称谓无法单独成义，可按语义合并，但必须在章节控制记录。
- 如原文极长，必须按语义、话语轮次、事件动作或论证单位拆分。
- 注释引用必须能回到具体 passage。

## 读者体验

- 原文段不应被缩成不可读的小字；它是读者版正文的一部分。
- 今译段应明显区分于原文段，但不要制造复杂装饰。
- 手机窄屏下 passage block 不得因标签、注释或编号撑破布局。

## 抽检要求

分层随机抽检必须把原文段、今译段、注释作为独立或可追溯的审计单位。评审必须检查：

- 原文和今译是否一一对应。
- 今译是否误解原文。
- 必要注释是否缺失。
- 注释是否过度、错误或与正文冲突。
