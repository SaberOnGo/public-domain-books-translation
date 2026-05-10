# 13 预制作阶段 1：全书制作规格 / Preproduction Stage 1: Book Production Specification

## 目的 / Purpose

全部翻译完成且章节门禁通过后，不得直接构建整本 EPUB。必须先定义全书制作规格，避免出现封面缺失、metadata 粗糙、字体难看、标题过大、章节标题层级不统一、封面体积过大等问题。

## 输入 / Input

- `chapters/final/*.md`
- `metadata/book.yaml`
- `metadata/source_evidence.md`
- `metadata/rights_checklist.md`
- `metadata/style_profile.md`
- 作者资料、原书资料、公版来源 URL。

## 必做规格 / Required Specification

生成：

- `preproduction/stage1/production_spec.md`

必须包含：

1. 封面方案：图像来源、尺寸、格式、压缩目标、OPF `cover-image` 写入方式。
2. 书籍详情页：优先显示本项目版本信息，包括 `LifeBook 书坊`、译制时间、公版来源 URL、公版说明；之后才是原书信息。
3. 作者信息：生卒年、国籍、基本人生、代表作、与本书关系。
4. 原书信息：英文书名、出版年代、来源版本、Project Gutenberg 或其他公版来源。
5. 字体策略：默认不得锁死难看字体；除非做字体子集化，不得嵌入完整中文字体。
6. 排版策略：正文行距、段首缩进、目录、封面页、版本说明页、章节标题。
7. 标题策略：手机窄屏下不得过大；`第X章` 与章节说明字号必须一致或视觉协调。
8. 文件体积策略：封面建议 JPG/WebP/压缩 PNG；EPUB 总体积不能被封面或字体异常撑大。
9. EPUB 结构：`cover.xhtml`、`book-info.xhtml`、`nav.xhtml`、`package.opf`、CSS、正文 spine。
10. 校验策略：EPUBCheck 必须 0 fatal、0 error；警告需解释或修复。

## 来自《黑人北极探险家》的教训 / Lessons Learned

- 不要只生成能打开的 EPUB；书架封面、详情页、metadata 同样是正本书质量。
- 封面 PNG 可能过大，3MB 封面对于 280KB 正文不合理，应压缩为数百 KB 级 JPG。
- 直接嵌入完整中文字体可能达到几十 MB，不适合批量公版 EPUB；如需指定字体，必须做字体子集化。
- 写死 `font-family` 可能导致读书 App 无法切换字体；默认应让阅读器字体接管。
- `LifeBook 翻译组` 这种名称像字幕组，正式出版品牌使用 `LifeBook 书坊`。

## 输出 / Output

- `preproduction/stage1/production_spec.md`
- `metadata/book.yaml` 更新后的版本信息
- `state/pipeline_state.json.status = PREPRODUCTION_SPEC_DONE`
