# 18 最终输出 / Final Output

## 前置门禁

- `npm run check:epub` 通过。
- `npm run review:random-validate:pass` 通过。
- 所有 P0/P1/P2 已关闭。
- 可复用经验已回填或已有明确回填记录。

## 公版或授权项目

运行：

```powershell
npm run release:create
```

必须生成：

- `output/release/{目标语言书名}_vX.X.X.epub`
- `output/release/release_notes.md`
- `output/release/release_state.json`
- `output/release/release_index.md`

## 私人自用项目

运行：

```powershell
npm run private:artifact:create
```

不得创建公开 release。
