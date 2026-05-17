# Book I.10 试译样本 EPUB 评审

sample_review_status: "PASS_FOR_TRIAL_PREVIEW__NOT_FOR_PUBLICATION"
full_book_translation_status: "BLOCKED"
epubcheck_status: "BLOCKED_LOCAL_JAVA_NOT_AVAILABLE"
latest_rework_status: "USER_FEEDBACK_APPLIED_2026_05_17"
human_required: false

## 产物

- EPUB：`preproduction/stage2_sample/sample_book.epub`
- XHTML：`preproduction/stage2_sample/sample_chapter.xhtml`
- EPUB 源目录：`preproduction/stage2_sample/sample_epub_source/`
- 预览截图：
  - `preproduction/stage2_sample/screenshots/book_i10_facsimile_phone_480.png`
  - `preproduction/stage2_sample/screenshots/book_i10_facsimile_desktop.png`
  - `preproduction/stage2_sample/screenshots/book_i10_revised_phone_480.png`
  - `preproduction/stage2_sample/screenshots/book_i10_p_notation_phone_480.png`
- 原书裁图联系表：`preproduction/stage2_sample/facsimile_work/book_i10_facsimile_figures_contact.jpg`
- PDF 对照图：`qa/technical/page_screenshots/book_i10_pdf_pages_019_028_contact_sheet.jpg`

## 自动检查

| item | result | note |
|---|---|---|
| EPUB zip 可读 | PASS | `python -m zipfile -t` 通过 |
| 必需文件 | PASS | `mimetype`, `container.xml`, `package.opf`, `nav.xhtml`, `book-info.xhtml`, `sample_chapter.xhtml`, CSS, cover image 均存在 |
| XHTML/XML 可解析 | PASS | `package.opf`, `nav.xhtml`, `cover.xhtml`, `book-info.xhtml`, `sample_chapter.xhtml` 可解析 |
| 图像数量 | PASS | 7 张 Book I.10 PDF facsimile PNG 进入 EPUB；SVG 草图仅作为 QA 辅助，不再作为样本 EPUB 正文图 |
| 图像响应式 | PASS_FOR_TRIAL | EPUB CSS 设置 `img max-width: 100%; height: auto`，facsimile 图使用整行居中显示，480px 手机宽度截图可读 |
| 裁图标签完整性 | PASS_AFTER_REWORK | 图 2、图 4 已重裁；脚本现在检测原始裁框边缘墨迹，并自动补白边 |
| 读者版数值显示 | PASS_AFTER_REWORK | 弧和角用 `1°30′` 等显示；弦长、平方量等非角度六十进制值用 `37p04′55″` 等显示，不裸露 `37;4,55`，也不转成十进制小数 |
| 章末集中注释 | PASS_AFTER_REWORK | 本章新增集中注释，说明“弦”术语、六十进制显示和半弧概念 |
| 《几何原本》依据显示 | PASS_AFTER_REWORK | 正文依据标记使用小号“依据《几何原本》...”格式，章末列出本章各条依据的大意 |
| 古典作图语可读性 | PASS_AFTER_REWORK | “将割/超过”等硬译已改为简洁现代几何关系；脚本门禁拦截典型旧写法 |
| 全书翻译脚本门禁 | PASS_AFTER_REWORK | `check_translation_constraints.py` 已作为全书门禁；Book I.10 样本构建以 trial scope 复用该门禁 |
| OPF cover-image | PASS | `images/cover.svg` 登记为 `cover-image` |
| 本机绝对路径/热链接 | PASS | 样本输出未检出 `file://`, `D:`, `C:` |
| 旧品牌残留 | PASS | 样本输出未检出 `LifeBook Translation Group` 或 `LifeBook 翻译组` |
| EPUBCheck | BLOCKED | `epubchecker` jar 已安装在共享 `books/node_modules`，但当前环境没有 `java`，书籍目录也没有 `tools/zulu17-jre` |

## 视觉预览

- 480px 手机宽度预览：标题、元数据、正文、PDF facsimile 图 1 可正常排布；图像按屏幕宽度缩放，未横向撑破页面。
- 桌面宽度预览：正文行长较长但可读；PDF facsimile 图居中、图注跟随。
- 试译样本的顶部 metadata 仍偏工程化，适合作为审校样本，不适合作为最终读者版。最终版应把这些控制字段移入版本说明页或删除。

## 与原语言 PDF 比较

| dimension | PDF 原版 | Book I.10 样本 EPUB | 评审 |
|---|---|---|---|
| 页面结构 | 双页扫描/纸书版式，含页眉、页码和注释区 | 单栏可重排中文正文 | PASS_FOR_TRIAL；EPUB 不应照搬扫描页 |
| 原文层级 | 希腊正文与校勘/脚注混排 | 中文试译正文，保留试译控制说明 | PASS_FOR_TRIAL；正式版需决定是否附原文/页码锚点 |
| 图形位置 | 几何图嵌入相关证明附近 | 7 张 PDF facsimile 裁图按证明段落插入 | PASS_FOR_TRIAL；当前比示意 SVG 更接近原书 |
| 点名/线段标签 | 希腊字母点名可见 | 希腊大写字母点名保留 | PASS_FOR_TRIAL |
| 数值表边界 | viewer page 028 转入 Book I.11 弦表 | 样本在 Book I.10 末尾停止并注明弦表不在范围内 | PASS |
| 纸书特征 | 保留扫描、页码、版心、注释密度 | 不保留纸书版心和页码视觉 | ACCEPTED_FOR_EPUB；正式版可加页码锚点，不应做扫描复刻 |

## 结论

Book I.10 样本 EPUB 可作为单章节试译预制作效果讨论样本。当前图像路线改为 PDF facsimile 裁图，视觉上明显比示意 SVG 接近原书；手机端可自动缩放到屏幕宽度。用户指出的图 2、图 4 标签裁切问题已通过脚本化裁图流程修正。正文已改用更现代的中文表述，并将六十进制数值改成读者版显示：角度保留 `°′″`，非角度弦长和平方量保留六十进制但使用 `p` 记法。《几何原本》依据改为小号正文标记，并在章末注释说明各条依据的大意。古典作图语按“清楚但不啰嗦”的原则处理，并由样本构建脚本拦截典型旧问题。它仍没有通过正式 EPUB 生产门禁，因为 EPUBCheck 尚未在本机完成，facsimile 图仍需全书级批量抽检和来源页标注，权利与全书级门禁仍未完成。

本评审不允许进入全书翻译，不允许翻译 Book I.11 弦表，不允许写入 `chapters/final/`，不允许生成正式 `output/book.epub`。
