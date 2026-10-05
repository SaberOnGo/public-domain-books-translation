# 雪月（Snowmoon）v0.0.2

作者：维塔利克·布特林（Vitalik Buterin）。译制署名：LifeBook 书坊 SaberOnGo 译制；封面署名：LifeBook 书坊译制。

正式质量状态：PASS。此版本基于 2026-10-02 的32章官方书源及作者声明；原作仍可能继续更新。

## 阅读与下载

- [雪月_v0.0.2.epub](https://github.com/SaberOnGo/public-domain-books-translation/releases/download/snowmoon-v0.0.2/Snowmoon_zh-Hans_v0.0.2.epub)
- [雪月_中英双语_v0.0.2.epub](https://github.com/SaberOnGo/public-domain-books-translation/releases/download/snowmoon-v0.0.2/Snowmoon_zh-Hans-en_v0.0.2.epub)
- [雪月_英文原文_v0.0.2.epub](https://github.com/SaberOnGo/public-domain-books-translation/releases/download/snowmoon-v0.0.2/Snowmoon_en_v0.0.2.epub)
- [中文与中英双语网页版 ZIP](https://github.com/SaberOnGo/public-domain-books-translation/releases/download/snowmoon-v0.0.2/Snowmoon_Web_v0.0.2.zip)
- [可编辑 GPL 对应源码 ZIP](https://github.com/SaberOnGo/public-domain-books-translation/releases/download/snowmoon-v0.0.2/Snowmoon_Corresponding_Source_v0.0.2.zip)

网页包解压后，用任意静态网页服务器提供 `Snowmoon_Web_v0.0.2/`；中文入口为 `zh-Hans/index.html`，双语入口为 `bilingual/index.html`。保留完整目录，不拆散章节与资源。LifeBook书库接入尚未配置，当前为待接入版本；这里不代表书库已上线。日常原文更新监测已启用，首版后仅在上游有意义变更且质量门禁通过时生成并发布新版本。

远程 EPUB 附件使用 `Snowmoon_zh-Hans_v0.0.2.epub`、`Snowmoon_zh-Hans-en_v0.0.2.epub`、`Snowmoon_en_v0.0.2.epub`，分别对应本地简中、双语和英文文件；内容哈希相同。`SHA256SUMS.txt` 使用远程附件名。

## 来源与许可

[官方原文](https://vitalik.eth.limo/snowmoon/)按 GNU GPL v3 授权，本改编译本亦按 GPL v3 交付；完整许可证见 `COPYING-GPL-3.0.txt`。保留原作者身份、原文声明、来源及翻译/排版修改说明。对应源码包含原始HTML、译文canonical/XLIFF、词表、图片/样式及真实构建脚本；内容和源码在同一GitHub release同时提供。源码包 SHA256：`ebbaed15e57a401b80489d5fb1217ed16000a57698c8a92cbc1494bef8bcba7b`。

## 校验与范围

33/33部分、4373单元经独立全量审校；已发现问题族闭环。当前稿两轮连续独立A/B优秀分层抽检通过；三版EPUBCheck均为0 fatal/0 error/0 warning，原生阅读器证据PASS。三EPUB和完整两网页树的六步隔离源码重建及基线比较PASS。原文图片和相关样式保留，不含LifeBook Digest。

v0.0.1仅为本地源码候选，OPF生成时间比较未认namespace前缀，总报告未通过；旧包和失败记录已保留。v0.0.2修复比较器，38项回归和新的完整重建通过。正式EPUB与之前冻结的读者可见内容一致。

详见 `release_state.json`、`release_notes.md`、`source_delivery_manifest.json`、`source_rebuild_verification.json`、`gpl_source_delivery_verification.json`及`translation_metrics.md`。源码包内的生产配置/交接记录冻结于最终验证之前，后续验证与分发状态以本目录为准；保留冻结输入以保证重建。

实际统计以九个自有线程的质量封版截止窗口为界，输入包含缓存、输出包含推理；不推算费用或有效工时。共启动5个seed评审轮，3轮收到A/B实际裁决（含1轮FAIL），最终当前稿2轮连续优秀PASS。预估记录在开工后补齐，历史时序保留，不称严格事前预测。抽检置信字段不是全书绝对无错保证。

## English

Three validated EPUB editions and both deployable static web editions are supplied with the editable GPL v3 corresponding source. The full six-phase isolated rebuild and content comparison passed; the verification uses this host's shared Node dependencies and is not a clean-machine or cross-platform claim. LifeBook deployment remains unconfigured. Historical estimate timing and unavailable active hours are disclosed, and token measurements are bounded at the quality cutoff.

Remote EPUB assets use distinct ASCII names; local Chinese filenames retain identical bytes. SHA256SUMS.txt refers to the remote asset names.
