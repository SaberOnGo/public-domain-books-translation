# 00 主控流程

按 `AGENTS.md`、公共模板、`targets/zh-Hans` 和 `Italian-to-Simplified-Chinese` 执行。先建立来源与权利证据，再研究、试译、分章、审校、构建、抽检、release。任何具体书籍产物只写入书籍工程。

顺序：读取 `README.md`、`PIPELINE_SPEC.md`、`automation_contract.md`、`metadata/italian_source_profile.md` 模板、本目录 references；然后执行 01-19 prompts。权利不清楚时停止。
