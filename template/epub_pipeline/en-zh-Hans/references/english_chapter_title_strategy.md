# 英文纸书长章节标题的中文处理策略

本文件适用于英文源文译入简体中文时的章节标题处理。

## 背景

19 世纪和 20 世纪初英文纸书常用长章节标题，尤其是探险、旅行、回忆录、传记类作品。这些标题常用 `--` 串联几个小题，功能接近纸书目录摘要。

翻译时不能把 `--` 一律替换为中文破折号 `——`。否则中文 EPUB 会出现标题过长、标题像目录串、手机屏幕折行严重的问题。

## 处理流程

1. 读取完整原文标题，不得只使用被自动分章脚本截断的第一行。
2. 判断标题结构：
   - 主事件。
   - 并列小题。
   - 结果或情绪收束。
   - 人名/地名/器物名。
3. 生成三种中文标题：
   - `nav_title`：短目录题名。
   - `display_title`：页面主标题。
   - `subtitle`：副标题或标题说明。
4. 只有在破折号本身有修辞功能时才保留 `——`。
5. 纸书目录式并列信息优先转为副标题，不塞进同一个 `<h1>`。

## 示例

```text
Source:
CHAPTER V MAKING PEARY SLEDGES--HUNTING IN THE ARCTIC NIGHT--THE EXCITABLE DOGS AND THEIR HABITS

Weak:
第五章 制作皮里式雪橇——在北极之夜狩猎——容易激动的狗及其习性

Preferred:
nav_title: 第五章 制作皮里式雪橇
display_title: 第五章 制作皮里式雪橇
subtitle: 北极之夜的狩猎与躁动的狗群
```

```text
Source:
CHAPTER XX TWO NARROW ESCAPES--ARRIVAL AT ETAH--HARRY WHITNEY--DR. COOK'S CLAIMS

Preferred:
nav_title: 第二十章 两次险些遇难
display_title: 第二十章 两次险些遇难
subtitle: 抵达伊塔、哈里·惠特尼与库克医生的声明
```

章节标题和副标题中的人物名必须优先使用中文译名。标题中的人名不算“正文首次出现”；即使某个人名第一次被读者看到是在标题里，也不得在标题后追加英文原名或英文括注。英文原名应放在正文第一次自然出现该人名的位置、译注或术语表中，不放入标题。

## 禁止

- 禁止用被截断的 `#` 标题作为唯一标题依据。
- 禁止让三个以上英文标题片段全部挤进中文主标题。
- 禁止把英文 `--` 机械替换成中文 `——`。
- 禁止让 EPUB nav 使用冗长标题链。
- 禁止在章节标题、副标题或目录题名中写 `鲁道夫·弗兰克（Rudolph Franke）`、`发现 Rudolph Franke` 这类英文原名残留。

## 输出要求

如果书中存在这种标题，必须在 `metadata/style_profile.md` 或 `preproduction/stage1/production_spec.md` 中写出标题策略，并在构建脚本或手工 XHTML 中落实。
