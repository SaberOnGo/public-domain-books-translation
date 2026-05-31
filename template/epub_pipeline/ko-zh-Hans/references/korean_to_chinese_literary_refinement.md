# 韩语/朝鲜语到简体中文文学精修策略 / Korean-to-Simplified-Chinese Literary Refinement

本文件把 common 层的文学精修规则应用到韩语/朝鲜语公版书译入简体中文的场景。它不替代 `template/epub_pipeline/targets/zh-Hans/quality_framework/`，只补充韩语/朝鲜语源文特有风险。

This file applies the common refinement policy to Korean public-domain books translated into Simplified Chinese.

## 目标 / Aim

韩语/朝鲜语到中文的 EPUB 不是“意思大概对、文件能打开”就完成。合格译文必须像一部完成的中文书，同时保留韩语/朝鲜语原作的时代质地、叙述距离、暧昧程度和文学节奏。

## 标题与原题 / Titles

- 必须读取 `references/korean_title_strategy.md`。
- 书名、篇名、章题必须建立中文题名策略，避免把韩文/朝鲜文原题、读音或解释性括注塞进 EPUB 目录。
- 如果原文只有编号、短题或无题分隔，不得为中文 EPUB 自创可见小标题；概括只能放入 `title_note`、QA 或制作说明。
- 题名涉及官能、身体、心理控制或审美意象时，不得用比原文更露骨、更猎奇的中文标题。

## 句法与叙述 / Syntax And Narration

- 韩语/朝鲜语长修饰链可以拆分，但不能拆散视角焦点。
- 韩语/朝鲜语省主语、省宾语时，中文可补出必要关系；不得补出原文没有的心理动机、事实或评价。
- 韩语/朝鲜语句末语气常承载迟疑、回避、委婉、压迫或冷淡，中文不能一律译成明确判断。
- 第一人称、转述、内心独白和自由间接引语必须保留叙述距离；不得把暧昧的心理变成解释性旁白。

## 汉字词与时代感 / Hanja Terms And Period Register

- 韩语/朝鲜语汉字词必须逐项判断：可直接译、需换成现代中文、需保留古意、需加短注，还是需在术语表中说明。
- 旧时代称谓、阶层、艺道、佛教、服饰、器物、都市地名和风俗词，不得现代化到失去时代感。
- 但也不能堆砌生僻词让中文读者无法进入叙事；古意应服务作品，不是炫技。

## 官能文学与心理边界 / Sensual Literature And Psychological Boundary

- 官能描写要保留原作的暗示、身体性、权力关系和心理张力。
- 不得为了“文学化”删掉原文的欲望、羞耻、疼痛、控制或不适。
- 不得为了“刺激”增加露骨词、身体细节或色情化视角。
- 不得用现代诊断标签替代原文叙事，除非作者文本本身如此表达。
- 对日据时期文学，尤其要区分人物理想、叙述者距离、殖民地现实、启蒙话语和作者立场；不能把复杂叙事压成单一政治口号或道德评价。

## 意象与声调 / Imagery And Voice

- 韩语/朝鲜语拟声拟态词要转成中文可感的节奏、动作、触感或心理色彩。
- 重复、停顿、含糊、冷淡和突然的强烈表达，应在中文中保留功能，不要为了“顺”全部抹平。
- 关键物象和身体动作必须具体；不要把画面词偷懒译成抽象说明词。

## 译注边界 / Note Boundary

- 译注只解释必要的时代、制度、称谓、典故、艺道、佛教或文本形态问题。
- 译注必须短，优先不打断阅读。
- 韩语/朝鲜语旧作中的货币、物价、年龄算法、尺贯法、佛事日期、学校/职业/交通制度等，若原文无误但会让现代中文读者形成错误常识判断，必须在首次出现处加一条短注或在译制说明中集中说明。
- 不得因“有时代感”就密集加注；能由上下文理解的普通地名、器物、交通设施、都市风俗词，通常只保留时代译名，不做百科式解释。
- 确认原文确实如此时，注释用于防误读，不用于替正文辩解；正文仍要保持小说叙述的自然节奏。
- 版权、底本、OCR、QA、prompt 和工作流说明不得进入读者正文；应写在 metadata、QA 或 release 记录中。

## 精修门禁 / Refinement Gate

任一样本存在以下问题，即使平均分达标，也必须回到精校或更早阶段修复：

- 事实误解、人物关系误判、视角误判。
- 韩语/朝鲜语句法外壳明显，中文不自然。
- 官能或暴力内容被加重、削弱、猎奇化或道德化。
- 汉字词照搬导致现代中文误读。
- 敬语、称谓、亲疏关系、时代语气处理错误。
- 原文标题、输入者说明、底本注、编者注或 OCR 残留进入读者正文。
- 术语、专名、译注、表格、图片或 metadata 不一致。

修复后必须在旧轮次关闭问题，并使用新 seed 重新生成样本。

## Layering / 分层

规则分三层：

1. `template/epub_pipeline/common/`：所有语言共享的 EPUB、抽检、发布和前置页规则。
2. `template/epub_pipeline/targets/zh-Hans/quality_framework/`：所有译入简体中文的中文质量规则。
3. `template/epub_pipeline/ko-zh-Hans/`：韩语/朝鲜语源文到简体中文的专用问题，例如韩文/汉字混排、旧拼写、敬语、题名、殖民地时期语境、官能文学边界和韩语/朝鲜语句法干扰。

## 随机抽检同类问题全书审计 / Book-Wide Similar-Issue Audit

随机抽检一旦发现任何需要修复或可能系统性复现的问题，包括但不限于 P0/P1/P2、单项 <70、读者不可理解、事实/术语/图表/公式/注释错误，或本模板硬门禁失败，主执行 AI 不得只修被抽中的样本，也不得等到第二轮才全书检查。必须先把发现归纳为问题族，再对整本读者可见书稿执行全书同类问题审计，覆盖 `chapters/final/`、frontmatter、metadata、nav、表格、图片、公式、图注、注释和生成 EPUB 中相应 XHTML；修复所有确认命中，记录合理例外，并在该轮 `fix_log.md` 与 `closure_check.md` 中关闭该问题族后，才能使用新 seed 复抽。

If a random sample exposes any issue that needs correction or may recur systemically, treat it as a possible systemic defect family immediately in the current round. Audit the whole reader-facing book for similar cases, fix all confirmed matches, document justified exceptions, and close the family in the same round before a new-seed resample.
