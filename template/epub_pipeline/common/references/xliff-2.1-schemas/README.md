# XLIFF 2.1 official schema snapshot / XLIFF 2.1 官方 Schema 快照

本目录保存 OASIS XLIFF 2.1 Standard（2018-02-13）发布包中的官方 core XSD 及它引用的 W3C XML namespace XSD，用于离线校验可选的 CAT/TMS 交换文件。XLIFF 2.1 沿用 `urn:oasis:names:tc:xliff:document:2.0` namespace；core XSD 的官方文件名仍为 `xliff_core_2.0.xsd`。

- 上游目录：<https://docs.oasis-open.org/xliff/xliff-core/v2.1/os/schemas/>
- 叙述性规范：<https://docs.oasis-open.org/xliff/xliff-core/v2.1/xliff-core-v2.1.html>
- 上游 core XSD 原始字节 SHA-256：`5686d2dbe9dac95e34d1b06a805e1e0f4999db5d5a67dc8bb8514c780592a84d`
- 仓库 LF 与行尾空白规范化 core XSD SHA-256：`211693e0bfdece92dd41cfc539021946d119bcba0a28df7809335848edc611cb`
- 上游 W3C XML XSD 原始字节 SHA-256：`61960fb3131e38022caad5360e2f33a3382578ab3c80cd58bd74320ede61b20c`
- 仓库 LF 规范化 W3C XML XSD SHA-256：`06cfb971ad5327e78c7af7e04f50f8fb9d161dae7fe45ed836e808cb55694962`

Schema 校验只在显式导出或导入 XLIFF 时运行，不进入普通翻译、章节并行或 EPUB 构建关键路径。缺少 Python `lxml` 时，XLIFF 命令应明确失败并提示安装；不启用 XLIFF 的项目不受影响。
