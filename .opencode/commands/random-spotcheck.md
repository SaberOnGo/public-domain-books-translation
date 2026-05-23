---
description: Run or plan the post-EPUB stratified random spot-check gate.
agent: book-runner
---

在 `$ARGUMENTS` 指定的书籍工程目录内执行或规划 EPUB 后分层随机抽检。

执行前必须读取：

- `AGENTS.md`
- `template/epub_pipeline/README.md`
- `template/epub_pipeline/common/README.md`
- `template/epub_pipeline/common/references/stratified_random_spotcheck.md`
- `template/epub_pipeline/common/prompts/16a_stratified_random_spotcheck.md`
- 书籍工程内复制后的对应 references/prompts/state 文件

默认流程：

```powershell
npm run review:random-samples
npm run review:random-validate
```

最终 release 前必须通过：

```powershell
npm run review:random-validate:pass
```

注意：

- 样本必须来自读者可见 audit units，不是人工挑选的“看起来没问题”的段落。
- 至少两个独立 agent 审查样本；主执行 agent 不能自证通过。
- 任一 P0/P1/P2 必须写入修复路径、fix log 和 closure check；修复后使用新 seed 重新抽检。
