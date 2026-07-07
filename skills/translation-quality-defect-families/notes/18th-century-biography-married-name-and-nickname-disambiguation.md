# 18th-Century Biography: Married Name and Nickname Disambiguation

## 中文经验

- 发现方式：章节全量复查中检查 `Mrs. X`、婚前/婚后称呼、母亲与妻子同姓称呼、
  地方昵称和人物索引相关段落。
- 问题族：18 世纪英语传记常用婚后姓氏和礼貌称谓，不显式说明亲属关系。直译为
  “某某夫人”有时会让中文读者把母亲、妻子、寡妇、女儿或其他同姓女性混淆；
  昵称如 `Tetty/Tetsey/Betty/Betsey` 又同时承担人物关系、地方用法和讽刺效果。
- 审计方法：先用 `rg -n "Mrs\\.|Miss\\.|Tetty|Tetsey|Betty|Betsey|Elisabeth"`
  收集候选，再只读命中段前后小上下文，确认每个称谓在该处指向谁。
- 修复方式：中文正文优先消歧人物关系；必要时把 `Mrs. Johnson` 译成“约翰生的母亲”
  或“约翰生夫人”，而不是机械保持同一译名。昵称首次出现应保留源文接口，并说明
  它是教名的地方缩写；后文按中文可读性使用稳定译名。
- 复查方式：不看英文只读中文段落，应能判断被谈论者是母亲、妻子、女儿还是
  见证人；再回看原文确认没有把礼貌称谓改成无依据的身份判断。

## English Note

- Detection: during full-chapter review, inspect `Mrs. X`, premarital and marital
  naming, same-surname mother/wife references, local nicknames, and index-like
  biographical passages.
- Family: eighteenth-century biography often relies on married names and courtesy
  titles without restating kinship. A mechanical Chinese `X 夫人` can confuse a
  mother, wife, widow, daughter, or another same-surname woman. Nicknames such as
  `Tetty/Tetsey/Betty/Betsey` carry relationship, provincial usage, and comic tone.
- Audit: use `rg -n "Mrs\\.|Miss\\.|Tetty|Tetsey|Betty|Betsey|Elisabeth"` to collect
  candidates, then read only nearby context to identify each referent.
- Fix: prioritize reader-facing disambiguation in Chinese. Translate `Mrs. Johnson`
  as `约翰生的母亲` or `约翰生夫人` according to referent instead of mechanically
  reusing one form. For nicknames, keep the source interface at first occurrence
  and explain the local shortening of the given name.
- Recheck: target-only reading should make clear whether the person is mother,
  wife, daughter, or witness; source comparison should confirm that courtesy
  titles were not turned into unsupported identity claims.
