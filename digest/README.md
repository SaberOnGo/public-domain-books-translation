# LifeBook Digest

<table align="center">
  <tr>
    <td align="center"><h3><a href="./README.md">简体中文</a></h3></td>
    <td align="center"><h3><a href="../readme/digest/README.zh-TW.md">繁體中文</a></h3></td>
    <td align="center"><h3><a href="../readme/digest/README.en.md">English</a></h3></td>
    <td align="center"><h3><a href="../readme/digest/README.ja.md">日本語</a></h3></td>
  </tr>
</table>

LifeBook Digest 是 LifeBook 翻译发布系统的可选 EPUB 后处理模块。它放在仓库根目录 `digest/`，不直接接管原有翻译、构建、抽检或发布主流程。

## 快速开始 / Quick Start

<table align="center">
  <tr>
    <td align="center"><a href="./README.md#快速开始--quick-start">简体中文</a></td>
    <td align="center"><a href="../readme/digest/README.zh-TW.md#快速開始--quick-start">繁體中文</a></td>
    <td align="center"><a href="../readme/digest/README.en.md#quick-start">English</a></td>
    <td align="center"><a href="../readme/digest/README.ja.md#クイックスタート--quick-start">日本語</a></td>
  </tr>
</table>

在书籍工程根目录写入 `digest.config.json`：

```json
{
  "enabled": true,
  "merge_into_epub": true,
  "source_epub": "output/book.epub",
  "output_epub": "output/book_digest.epub",
  "title": "全书导读",
  "language": "zh-CN",
  "max_section_chars": 240
}
```

从仓库根目录运行：

```powershell
python -m digest.lifebook_digest --book-root books/{target}/{number}_{book_id_slug}
```

## 设计边界

- 输入是某本书已经生成的标准 EPUB，默认 `output/book.epub`。
- 每本书通过自己的 `digest.config.json` 决定是否启用、是否合并进 EPUB。
- 启用但不合并时，只生成旁路文件：
  - `output/digest/digest.xhtml`
  - `output/digest/digest_state.json`
  - `qa/digest/digest_report.json`
- Digest XHTML 包含章节摘录和内联阅读地图，不依赖额外专用阅读器格式。
- `digest_state.json` 保存轻量拓扑：章节节点和阅读顺序边，便于后续扩展审校、可视化或更强摘要算法。
- 启用并合并时，输出仍是标准 EPUB，默认写到 `output/book_digest.epub`。
- 合并只新增一个读者可见章节，并更新该 EPUB 内部的 OPF manifest、spine 和 nav。
- 原有正文、封面、书籍信息页、前置页和翻译 QA 记录不被重写。

## Per-Book Configuration

在书籍工程根目录写入：

```json
{
  "enabled": true,
  "merge_into_epub": true,
  "source_epub": "output/book.epub",
  "output_epub": "output/book_digest.epub",
  "title": "全书导读",
  "language": "zh-CN",
  "max_section_chars": 240
}
```

字段说明：

- `enabled`: `false` 时模块直接跳过，不改动 EPUB。
- `merge_into_epub`: `false` 时只生成旁路 Digest 文件；`true` 时生成新的 EPUB。
- `source_epub`: 输入 EPUB，相对于书籍工程根目录。
- `output_epub`: 合并后的输出 EPUB，相对于书籍工程根目录。
- `title`: 合并进目录和章节页的标题。
- `language`: Digest XHTML 的语言标签；省略时读取源 EPUB metadata。
- `max_section_chars`: 每个章节提取的摘要片段最大字符数。

## Usage

从仓库根目录运行：

```powershell
python -m digest.lifebook_digest --book-root books/{target}/{number}_{book_id_slug}
```

也可以从 Python 调用：

```python
from digest.lifebook_digest import run_digest

result = run_digest("books/zh-Hans/1_example")
```

## Quality Expectations

这个模块只是 post-EPUB optional step。若把 Digest 合并进 EPUB，后续应至少验证：

- 生成的新 EPUB 能被 EPUBCheck 接受。
- 新增章节没有 prompt、QA 日志、制作说明或内部路径。
- 新增章节的 nav、spine、manifest 一致。
- 若该 EPUB 要作为正式产物发布，应按书籍工程自己的 release 规则生成新版本。

Digest 内容是读者可见内容；如果未来接入 LLM 摘要，不能把原始 AI 输出直接作为发布文本。

## Acknowledgement

本模块的方向受到 [spinedigest](https://github.com/oomol-lab/spinedigest) 的启发，感谢该项目展示了长文本摘要、章节拓扑和可复用处理中间状态的设计思路。LifeBook Digest 当前实现为独立的 LifeBook 后处理模块，输出目标保持为标准 EPUB。

## 许可证 / License

LifeBook Digest 的多语言许可证说明保存在：

- [简体中文](../license/DIGEST_LICENSE.md)
- [繁體中文](../license/DIGEST_LICENSE.zh-TW.md)
- [English](../license/DIGEST_LICENSE.en.md)
- [日本語](../license/DIGEST_LICENSE.ja.md)
