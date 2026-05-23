# 人类反馈控制 / Human Feedback Control

human_required: false

## 中文说明

此文件用于控制“人类是否必须检查”。如果设为 `true`，AI 必须停止在对应阶段，等待用户明确反馈；如果设为 `false`，AI 必须按模板内评分标准自动检查、自动返工或自动继续。

## English

This file controls whether human review is mandatory. If `human_required` is `true`, the AI must pause for explicit user feedback. If `false`, the AI must evaluate, revise, or continue automatically according to the pipeline rules.

## 默认规则 / Default Rule

- 默认值：`false`。
- 用户明确要求检查时：改为 `true`。
- 用户没有说明时：AI 自动执行，不得因“等用户看”而停工。
