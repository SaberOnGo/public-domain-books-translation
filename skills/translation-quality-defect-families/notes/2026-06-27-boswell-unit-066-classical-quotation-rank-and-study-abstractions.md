# 鲍斯威尔第66单元：古典引文、英国头衔与学习抽象词接口

## 发现方式

- 章节译后全量复查。
- 命中对象包括拉丁诗句 `Formosam resonare...`、`Baronet`、`grand scale of human knowledge`、`inclination to do nothing`、`privileged man`。

## 问题族

传记和18世纪谈话中常同时出现古典引文、英国社会头衔和抽象化学习/性格词组。若只保留外文或按词面直译，中文读者会遇到三类接口问题：裸外文不可读、头衔等级误译、抽象词组像分析笔记。

## 修复模式

- 古典外文引文若以音韵或学问为论点，可以保留原文，但应紧接提供中文大意，使读者有入口。
- `Baronet` 应译为“准男爵”，不得泛化成“男爵”。
- 抽象词组先判断语用功能，再改写为中文可读关系：
  - `grand scale of human knowledge` -> “人类知识的宏大范围”。
  - `inclination to do nothing` -> “想闲着不动的倾向”。
  - `privileged man` 在亲密圈层语境中 -> “特许亲近之人”。

## 复查办法

用 `rg` 扫描 `Formosam|Amarillida|Baronet|男爵|宏大阶梯|什么也不做|享有特权的人`，对照源文判断是古典引文、头衔还是抽象性格/学习短语；修复后追加整章复查，不能让修复轮直接 PASS。
