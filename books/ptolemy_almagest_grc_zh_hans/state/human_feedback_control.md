# 人类反馈控制 / Human Feedback Control

human_required: false
formal_translation_allowed: false

## 中文说明

此文件用于控制“人类是否必须检查”。如果设为 `true`，AI 必须停止在对应阶段，等待用户明确反馈；如果设为 `false`，AI 必须按模板内评分标准自动检查、自动返工或自动继续。

## English

This file controls whether human review is mandatory. If `human_required` is `true`, the AI must pause for explicit user feedback. If `false`, the AI must evaluate, revise, or continue automatically according to the pipeline rules.

## 默认规则 / Default Rule

- 默认值：`false`。
- 用户明确要求检查时：改为 `true`。
- 用户没有说明时：AI 自动执行，不得因“等用户看”而停工。

## Almagest 当前限制 / Current Almagest Restriction

- 当前工程只允许研究与预翻译准备。
- 禁止正式分章翻译。
- 禁止向 `chapters/translated/` 或 `chapters/final/` 写入正式译文。
- 若要进入正式翻译，必须先由用户明确解除 `formal_translation_allowed: false`，并完成 Book I 预翻译 PASS。

## Book I.10 试译反馈固化 / Book I.10 Trial Feedback Lock

- 正式翻译前必须继承 Book I.10 试译反馈：现代中文可读性、六十进制显示、facsimile 图裁剪、响应式 EPUB 图像、《几何原本》依据注释和古典作图语简洁现代化。
- 不能只靠 prompt 约束。凡能脚本化检查的旧问题，应进入构建或章节门禁脚本，例如裸 `Eucl.`、内部六十进制记法、`37份4′55″`、十进制化、未注释《几何原本》依据、典型硬译作图语和图像资源缺失。
- 全书正式翻译和正式 EPUB 构建必须先运行 `npm run quality:translation`；全书级构建入口 `npm run build:epub` 必须在正式构建前运行 `npm run quality:all`。
- 第一版 EPUB 后的每轮精校，都必须运行 `npm run review:random-samples` 或等效脚本，生成双 Agent 随机抽检样本；两个独立 Agent 各抽检不少于 10 个随机段落，平均分均 >= 75 且无单段 < 70，才允许认为本轮精校完成。
- 任一随机抽检 Agent 指出读不懂、数学/天文学链条断裂、术语/数值/图表错误或 EPUB 阅读阻断时，必须回到精校或更早阶段，修复后重新抽样，不得复用旧样本。
- 用户反馈指出的问题必须先写入规范和脚本，再作为后续正式翻译的前置质量要求。
