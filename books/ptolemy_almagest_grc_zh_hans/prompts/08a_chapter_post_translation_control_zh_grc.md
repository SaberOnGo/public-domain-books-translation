# 08A 每章节译后控制 / Per-Chapter Post-Translation Control

## 目的 / Purpose

在每章翻译完成后立即控制质量，避免整本翻完才发现风格、语气、可读性、术语或机械直译问题，导致大规模返工。

## 输入 / Input

- `chapters/src/{NNN_slug}.md`
- `chapters/translated/{NNN_slug}.md`
- `metadata/style_profile.md`
- `metadata/book_specific_translation_research.md`
- `glossary/terms.csv`
- `qa/chapter_controls/_TEMPLATE.control.md`

## 执行规则 / Execution Rules

每个章节翻译后，AI 必须创建：

- `qa/chapter_controls/{NNN_slug}.control.md`

该文件必须记录：

- 本章译后自检结果。
- 标题人名检查结果：章节标题/副标题/目录题名只使用中文译名；标题中的人名不计入“正文首次出现”；古希腊文原名、拉丁化转写或外文括注只出现在正文第一次自然出现处、译注或术语表。
- 技术证明可读性检查：不得保留大量“所对弧之半所对的直线”“将割”“超过某线”这类直译腔；必要时应改为现代中文表达，并在章末注说明。
- 外部证明依据检查：不得裸写 `Eucl.`；《几何原本》等依据应使用读者可识别标记，并在章末注释说明对应命题、定义或系的大意。
- 章末注检查：古今概念差异、直译会造成误解的术语、技术依据和六十进制显示法，必须集中列入本章注释。
- 数值显示检查：读者版正文不得裸用 `;`/`,` 六十进制内部记法，不得把非角度六十进制值十进制化。
- 是否有人类反馈。
- 是否需要回到本章重译。
- 关键修改项。
- 最终 PASS/FAIL。

## 人类反馈 / Human Feedback

如果用户对某一章不满意：

1. 把用户反馈原文写入该章 control 文件。
2. 设置 `control_status=REWORK_REQUIRED`。
3. 只回到该章 `07_translate_chapters`，不得影响其他已经 PASS 的章节。
4. 重译后再次运行本流程。

如果用户没有说明，且 `human_required=false`：

- AI 自动按 `_TEMPLATE.control.md` 检查。
- 通过则 `PASS`。
- 不通过则自动返工，不得假装通过。

## 并行 / Parallelism

章节可并行翻译、并行控制。每章 control 文件互不覆盖。

## 输出 / Output

- `qa/chapter_controls/{NNN_slug}.control.md`
- `state/pipeline_state.json.quality_gate.chapter_post_controls_status`

## PASS 条件 / PASS Criteria

- 所有章节均有 control 文件。
- 所有 control 文件 `control_status=PASS`。
- 不存在把古希腊文原名、拉丁化转写或外文括注塞进章节标题、副标题或目录题名的情况。
- 本章没有从第二语言参考译本直接转译的痕迹。
- 本章异文、残损、OCR 不确定处或语法歧义已有记录。
- 技术术语、六十进制数值和章末注符合本书 style profile。
- 任何用户明确指出的问题已回写并修正。
