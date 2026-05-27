# 12 构建与基础校验 / Build and Validate

## 任务

在进入最终出版前运行：

```powershell
npm run preflight:template
npm run lint:publication
npm run lint:assets
npm run cover:check
npm run reader:check
npm run build:epub
npm run check:epub
```

## 特别检查

- staging 输出必须来自最新 `chapters/final/`。
- `chapters/final/` 不得保留生产 YAML front matter，因为 common 构建器会把正文文件转换为读者 XHTML。
- 对照正文 raw XHTML 必须被保留，不得在 EPUB 中显示成 `&lt;section class="parallel-passage"...&gt;`。
- 生成 XHTML 必须绑定 `xmlns:epub`，以支持注释中的 `epub:type`。
- `package.opf` 中的 identifier 必须合法；`urn:uuid:` 后必须是合法 UUID。
- 对照正文 CSS 和 XHTML 不得破坏手机阅读。
- 注释链接、返回链接和 passage id 必须稳定。
- 不得把 `qa/`、prompt、工作流日志或底本下载说明误放入读者正文。
