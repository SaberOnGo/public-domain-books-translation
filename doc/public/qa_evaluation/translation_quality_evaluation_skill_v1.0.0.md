---
name: translation-quality-evaluation
version: 1.0.0
description: 跨书种、跨语言方向的译本质量评估 skill，用于对已完成译本、候选译稿、EPUB/PDF/MOBI 成品或多译本对照材料进行独立评分、缺陷归类、质量分级和后续返修建议。
---

# 译本质量评估 Skill v1.0.0

## 适用范围

本 skill 用于评估不同书籍、不同语言方向、不同介质的译本质量。它适用于公版、授权出版、私人自用项目，也适用于外部出版译本的短样本私有比较评审。

Use this skill to evaluate translation quality across books, languages, and formats. It supports public-domain, licensed, private-use, and privately supplied comparison materials.

不要把本 skill 用作版权授权判断。版权、来源、私人自用边界和发布资格必须先按仓库 `AGENTS.md`、`template/epub_pipeline/common/references/quality_gate_framework.md`、`template/epub_pipeline/modes/private_use/` 等规则确认。

## 触发条件

当用户要求以下任一任务时使用本 skill：

- 给一个译本、多个译本或不同版本 EPUB/PDF/MOBI 打分。
- 比较不同译者、不同出版社、AI 译制版和人工出版版。
- 判断译本是否适合作主读本、精校底本、旧译参考、训练样本或发布候选。
- 评估忠实性、文学性、读者体验、自然度、术语、注释、出版清洁度或基本错误。
- 总结可复用的译本质量评估规则。

## 输入前检查

评估前先记录材料状态：

| 项目 | 必填内容 |
|---|---|
| 版本身份 | 书名、作者、译者/译制者、出版社或制作标识、版本号、文件路径或书目信息 |
| 权利边界 | 公版、授权、私人自用、外部出版短样本评估、未知 |
| 文件介质 | EPUB、MOBI、PDF、扫描图像、OCR 文本、Markdown、DOCX、纯文本 |
| 可检索性 | 全文可检索、OCR 可用、仅图像可见、结构损坏 |
| 源文可用性 | 有完整源文、有局部源文、无源文、只能做目标语阅读评估 |
| 评估置信度 | 高、中、低，并说明原因 |

如果是扫描 PDF 或 OCR 质量不明，不得把它与全文可检索 EPUB 等量比较；只能给暂定分，除非完成 OCR、版面复核、章节完整性检查和抽样对照。

## 独立评审规则

正式评估建议至少两个独立评审 agent。两个 agent 必须读取同一批材料，但不得共享中间结论、评分、问题清单或推理过程。

当两个 agent 总分差异超过 8 分，主评审者必须记录分歧原因，并复核以下项目：

- 是否一个 agent 只看了目标语，另一个做了源文对照。
- 是否一个 agent 把电子书结构问题计入翻译分，另一个只评文本。
- 是否某个 agent 对文学声调、术语或私人自用边界采用了不同权重。
- 是否存在抽样偏差，例如只读开头、只读尾注、只读低风险章节。

## 抽样方法

优先使用分层抽样，而不是随机翻几页。

| 层级 | 检查重点 |
|---|---|
| 开头入口 | 声调建立、读者是否愿意继续读、标题/前置页是否清洁 |
| 高信息密度段 | 事实、因果、概念链、论证层级、术语稳定性 |
| 文学/批评段 | 隐喻、节奏、叙述距离、讽刺、身体感、审美功能 |
| 对话/引文段 | 角色声音、口语自然度、引文接口、标点和段落 |
| 文化与专名段 | 人名、地名、作品名、时代词、制度词、注释策略 |
| 章节结尾 | 收束力、主题回响、是否漏译或误改重心 |
| 电子书结构 | 目录、metadata、书籍信息页、注释、图片、表格、乱码、重复段 |

可用源文时，每本至少抽 8-12 个源文对照点；无源文时，明确标记为目标语可读性与出版质量评估，忠实性分只能低置信度给出。

## 100 分评分表

| 维度 | 分值 | 核心问题 | 常见扣分 |
|---|---:|---|---|
| 忠实性与事实准确 | 25 | 是否正确传达事实、数字、人物关系、因果、视角、语气、暧昧程度 | 误译、漏译、加戏、把比喻读实、把含混处译死 |
| 概念、术语与知识结构 | 15 | 专业概念、定义、术语组、作品名和人名是否稳定且可读 | 术语漂移、概念硬壳、伪专业词、源语括注泛滥 |
| 目标语自然度 | 15 | 是否像自然目标语书写，句法是否有呼吸，段落是否顺 | 翻译腔、长句不断气、源语语序残留、标点拖拽 |
| 文学/批评表达质量 | 15 | 是否保留原作审美功能、叙述距离、节奏、意象、批评锋芒 | 声调变平、意象自撞、解释化、把文学段译成说明书 |
| 读者体验与吸引力 | 10 | 开头是否抓人，关键段是否有推进力，注释是否扰民 | 入口劝退、信息密度失控、正文夹制作痕迹、注释打断阅读 |
| 注释、文化接口与跨语策略 | 8 | 注释是否必要、短、准；源语接口是否服务阅读 | 百科式长注、正文裸露源语、译名不统一、文化词误导 |
| 出版与电子书质量 | 7 | EPUB/PDF/目录/metadata/前置页/样式是否干净可用 | 乱码、重复段、目录错位、旧纸书页码、封面/书籍信息不合规 |
| 可验收证据 | 5 | 是否有来源、版本、抽样、审校、问题族闭环证据 | 无底本说明、无评审证据、无法复现评分、私人/公开边界不清 |

评级：

- 95-100：S，标杆级。极少数版本可达；必须同时有优秀文本和完整证据。
- 90-94：A，优秀成品。可作为主读本或发布候选，但仍需常规校验。
- 80-89：B，可用但需精修。80 只是硬失败线以上，不等于优秀。
- 70-79：C，有参考价值。可局部借鉴，但不宜直接作为主读本或发布底本。
- 60-69：D，仅限研究或局部对照。
- 0-59：F，不可用或风险过高。

## 一票否决

出现以下任一问题时，不能仅靠总分通过：

- 整段、整节、整章漏译。
- 关键事实、数字、人物身份、地点、时间或因果错误。
- 叙述视角、论证立场、人物关系或原作暧昧性被明显改坏。
- 大面积机器翻译腔或目标语无法自然阅读。
- 正文混入 prompt、QA 报告、制作日志、盗版站信息、模板说明。
- EPUB/PDF 结构严重损坏，目录不可用，章节缺失，乱码影响阅读。
- 公版/授权/私人自用边界不清，且该评估结果会被用于发布决策。

## 错误分级

| 等级 | 定义 | 处理 |
|---|---|---|
| P0 | 来源/权利边界不清、整章缺失、结构损坏、严重误导读者的事实错误 | 停止发布或停止作为候选，必须修复 |
| P1 | 忠实性、概念、人物关系、叙述视角、风格功能被破坏 | 修复后重评相关章节 |
| P2 | 明显翻译腔、术语不一、注释扰民、电子书清洁度问题 | 进入精修清单，修复后抽检 |
| P3 | 局部可优化表达、轻微标点、可接受但不优的译名 | 可批量修订或记录 |
| Note | 风格偏好、历史译法差异、合理替代方案 | 记录，不强制修 |

## 问题族闭环

若发现可能复现的质量问题，不要只修抽中样本。必须：

1. 给问题族命名。
2. 说明发现方式。
3. 定义读者风险或忠实性风险。
4. 先用低 token 方法查同类，例如 `rg`、术语表、标题映射、抽样 manifest、短上下文源文对照。
5. 记录确认命中和合理例外。
6. 修复后重新抽检。
7. 若问题族可复用，合并到 `skills/translation-quality-defect-families/SKILL.md` 或本目录后续版本。

## 输出模板

每个译本至少输出以下结构：

```markdown
### {编号} {书名/版本}

- 译者/译制者：
- 文件/版本：
- 总分：
- 评级：
- 置信度：
- 适合用途：

| 维度 | 分数 | 说明 |
|---|---:|---|
| 忠实性与事实准确 | /25 |  |
| 概念、术语与知识结构 | /15 |  |
| 目标语自然度 | /15 |  |
| 文学/批评表达质量 | /15 |  |
| 读者体验与吸引力 | /10 |  |
| 注释、文化接口与跨语策略 | /8 |  |
| 出版与电子书质量 | /7 |  |
| 可验收证据 | /5 |  |

高信号发现：
-

P0/P1/P2：
-

后续建议：
-
```

多译本评估还必须给出汇总排名、分歧说明和“不等量比较”提醒。例如扫描 PDF、OCR 文本、商业出版 EPUB、私人自用 AI 译制 EPUB不能在不说明置信度的情况下直接排序。

## 理论和项目依据

本 skill 采用“项目门禁 + 分析错误标注 + 文本功能评估”的混合模型：

- LifeBook 仓库 `doc/public/translation_quality_evaluation_framework.md`：多译本评分、材料置信度、分层抽样、P0-P3 分级。
- LifeBook 仓库 `template/epub_pipeline/common/references/quality_gate_framework.md`：章节全量检查、随机抽检、优秀出版线、问题族闭环。
- LifeBook 仓库 `template/epub_pipeline/targets/zh-Hans/quality_framework/templates/evaluation_rubric.md`：80 硬失败线与 92+ 优秀线。
- MQM: analytic Translation Quality Evaluation, shared error typology, scoring, sampling, repeated-error and root-cause guidance. https://themqm.org/
- ATA Framework for Standardized Error Marking: target-language mechanics, meaning transfer, writing quality, terminology, omission, addition, faithfulness, literalness and misunderstanding categories. https://www.atanet.org/certification/how-the-exam-is-graded/error-categories/
- Juliane House, Translation Quality Assessment: use source/target functional comparison, register and discourse profile rather than isolated word matching. https://www.routledge.com/Translation-Quality-Assessment-Past-and-Present/House/p/book/9781138795488
- Katharina Reiss text-type theory: informative, expressive, operative and audio-medial functions help decide whether accuracy, aesthetic form, reader response, or media interface should dominate scoring.

## 版本记录

### v1.0.0

- 建立通用译本质量评估流程。
- 合并 100 分评分表、P0-P3 错误分级、独立 agent 评审、分层抽样、问题族闭环和输出模板。
- 从既有《痴人之爱》评估框架抽象为不限书种的评估 skill。
