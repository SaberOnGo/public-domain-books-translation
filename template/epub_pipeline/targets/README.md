# Target-Language Quality Frameworks

Target-language directories store quality rules that depend on the language readers will actually read.

目标语言目录用于存放取决于读者实际阅读语言的质量规则。

## Layout / 目录

- `zh-Hans/`: Simplified Chinese target-language quality rules.
- `zh-Hans/`：简体中文目标语言质量规则。

## Rule / 规则

Do not put target-language prose, punctuation, typography, or reader-experience rules into `common/`. Put them under `targets/{target}/`, and let each source-target template combine them with its source-language-specific rules.

不要把目标语言文体、标点、排版和读者体验规则放进 `common/`。这些内容应放在 `targets/{target}/`，再由各个源语言到目标语言模板叠加自己的源语言专用规则。
