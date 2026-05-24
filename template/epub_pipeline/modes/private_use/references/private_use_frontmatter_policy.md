# Private-Use Frontmatter Policy / 私人自用首页与前置页规则

policy_status: "ACTIVE"
scope: "publication_mode=private_use only / 仅私人自用模式"

## Purpose / 目的

Private-use frontmatter must separate the user's private translation from public-domain publication, licensed publication, and LifeBook Shufang publication.

私人自用首页/前置页必须把用户的私人译本与公版发布、授权发布、LifeBook 书坊发布清楚分开。

## Required Content / 必备内容

Use the target language as the primary reader-facing language. For Simplified Chinese private-use projects, use the exact wording below.

读者可见语言以目标语言为主。简体中文私人自用工程使用以下固定措辞。

- Edition label: `私人学习版本`.
- Producer line: `参考LifeBook书坊 个人自制`.
- Source evidence: local source file name and SHA256 summary only; do not show the user's local absolute path.
- Use boundary: `仅供个人自用，不传播，不商业使用`.
- Risk boundary: `风险由个人承担。LifeBook书坊仅发布 LifeBook 翻译发布系统，不承担任何因其他个人翻译、保存、传播或使用非公版内容导致的版权风险及责任。`

## Forbidden Content / 禁止内容

- No public-domain notice.
- No public-domain source field.
- No public license paragraph.
- No `CC BY-NC-SA 4.0` statement for the private EPUB.
- No public release wording.
- No claim that LifeBook Shufang translated, published, licensed, approved, or distributed the private EPUB.
- No `LifeBook 书坊 SaberOnGo`, `LifeBook 书坊 + 个人名`, or `LifeBook 书坊 译制`.

- 不写公版说明。
- 不写公版来源字段。
- 不写公开授权段落。
- 不把私人 EPUB 标为 `CC BY-NC-SA 4.0`。
- 不写公开 release 措辞。
- 不声称 LifeBook 书坊翻译、出版、授权、审核或分发该私人 EPUB。
- 不使用 `LifeBook 书坊 SaberOnGo`、`LifeBook 书坊 + 个人名` 或 `LifeBook 书坊 译制`。

## Recommended Short Layout / 推荐短版结构

```text
# 书籍信息

书名：...
作者：...
版本：私人学习版本
制作：参考LifeBook书坊 个人自制
本地书源：{file_name}
书源校验：SHA256 {short_or_full_hash}

## 使用边界

仅供个人自用，不传播，不商业使用。

风险由个人承担。LifeBook书坊仅发布 LifeBook 翻译发布系统，不承担任何因其他个人翻译、保存、传播或使用非公版内容导致的版权风险及责任。
```
