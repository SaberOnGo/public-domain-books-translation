# LifeBook Digest

<table align="center">
  <tr>
    <td align="center"><h3><a href="./README.zh-CN.md">简体中文</a></h3></td>
    <td align="center"><h3><a href="./README.zh-TW.md">繁體中文</a></h3></td>
    <td align="center"><h3><a href="./README.en.md">English</a></h3></td>
    <td align="center"><h3><a href="./README.ja.md">日本語</a></h3></td>
  </tr>
</table>

LifeBook Digest 是 LifeBook 翻译发布系统的可选 EPUB 后处理模块。它位于仓库根目录 `digest/`，不直接接管原有翻译、构建、抽检或发布主流程。子模块入口也保留在 [digest/README.md](../../digest/README.md)。

## 快速开始 / Quick Start

<table align="center">
  <tr>
    <td align="center"><a href="./README.zh-CN.md#快速开始--quick-start">简体中文</a></td>
    <td align="center"><a href="./README.zh-TW.md#快速開始--quick-start">繁體中文</a></td>
    <td align="center"><a href="./README.en.md#quick-start">English</a></td>
    <td align="center"><a href="./README.ja.md#クイックスタート--quick-start">日本語</a></td>
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
- 启用但不合并时，只生成 `output/digest/` 和 `qa/digest/` 下的旁路文件。
- 启用并合并时，输出仍是标准 EPUB，默认写到 `output/book_digest.epub`。
- 合并只新增一个读者可见章节，并更新该 EPUB 内部的 OPF manifest、spine 和 nav。
- 原有正文、封面、书籍信息页、前置页和翻译 QA 记录不被重写。

## 质量要求

若把 Digest 合并进 EPUB，正式发布前必须按书籍工程自己的门禁验证新 EPUB。Digest 内容是读者可见内容；未来若接入 LLM 输出，不能未经审校直接发布。

## 致谢

本模块的方向受到 [spinedigest](https://github.com/oomol-lab/spinedigest) 的启发，感谢该项目展示了长文本摘要、章节拓扑和可复用处理中间状态的设计思路。LifeBook Digest 当前实现为独立的 LifeBook 后处理模块，输出目标保持为标准 EPUB。

## 许可证

见 [DIGEST_LICENSE.md](../../license/DIGEST_LICENSE.md)。

