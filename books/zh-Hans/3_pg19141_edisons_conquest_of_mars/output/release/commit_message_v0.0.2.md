# GitHub Commit Message / GitHub 提交信息 / GitHub コミットメッセージ

## 中文

```text
修复《爱迪生征服火星》读者反馈与随机抽检问题，发布 v0.0.2

原因：
- 读者反馈指出首章 `puny efforts` 旧译“微弱的努力”非常生硬，语义和中文表达都不达出版标准。
- 按模板要求，读者反馈触发 EPUB 后分层随机抽检闭环；第 1-9 轮发现 P1/P2 阻断项和可定位 P3 表达问题。

修改：
- 将 `puny efforts` 重译为“我们那点微不足道的抵抗”，恢复原文“并非人类真正击败火星人，而是疾病导致其败亡”的因果和自贬语气。
- 修复洪水与粮食储备逻辑反向、行动者关系错误、避难容量误译、小行星坠毁推理错位等事实/逻辑问题。
- 修复战斗高潮中的 `I cannot make it work` 反向误译、停火对白双重否定、闪电长度修饰错位和 `four-fifths of an inch` 数值错误。
- 统一术语：地球方 `electrical ship/electric ship` 译为“电力飞船/飞船”，火星方 `airship/aerial vessel` 译为“飞艇/火星飞艇”，清除“空中舰艇/电气飞船/电气飞艇/电气战舰”等混称。
- 修复 Princess Masaco/公主雅子、Zanzibar/维多利亚女王一行等人物地名语义。
- 删除源小标题污染正文和“啃人骨头的恶棍”等无依据增译，精修错字、长句、直译腔和专业表达。
- 补齐 `output/release` 发布记录，写明 v0.0.2 的修复点、QA 证据和提交说明。
- 按本次推送要求，纳入 `doc/public/开发计划.md` 与 `doc/public/细节修复_prompt.md` 两份公共文档记录。

验证：
- 分层随机抽检第 10 轮 PASS：Agent A 平均 91.18、最低 84、阻断 0；Agent B 平均 95.05、最低 93、阻断 0。
- `npm run review:random-validate:pass` 通过，release_confidence=1.0。
- EPUBCheck fatal/error/warning = 0/0/0。
- publication lint issue_count = 0。
- 正式发布产物：`output/release/book_v0.0.2.epub`。
- 公共文档：`doc/public/开发计划.md`、`doc/public/细节修复_prompt.md`。

推送注意：
- 如本机 GitHub 访问需要代理，只在当前 shell 临时设置代理环境变量后执行 push。
- 不要把本机代理地址、端口或任何私人网络配置写入项目文件或 commit。
```

## English

```text
Refine Edison's Conquest of Mars after reader feedback and spot checks; release v0.0.2

Why:
- Reader feedback flagged the old Chinese rendering of `puny efforts` as stiff, unnatural, and below publication quality.
- Per the template, reader feedback triggered the post-EPUB stratified random spot-check loop; rounds 1-9 found P1/P2 blockers and localized P3 prose issues.

What changed:
- Retranslated `puny efforts` to convey humble human resistance and preserve the source logic that disease, not human military success, defeated the Martians.
- Fixed factual and logic errors in the flood/provisions probability, actor relations, refuge capacity, and asteroid wreckage reasoning.
- Fixed battle-climax problems including the reversed `I cannot make it work`, a double-negative ceasefire line, a misplaced lightning-length modifier, and the `four-fifths of an inch` numeric error.
- Normalized terminology: Earth `electrical ship/electric ship` is rendered as "electric ship/ship" in Chinese, while Martian `airship/aerial vessel` is rendered as "airship/Martian airship"; removed inconsistent Chinese terms such as aerial warship/electrical airship variants.
- Corrected name/place handling including Princess Masaco and the Zanzibar/Victoria context.
- Removed source-subtitle contamination and unsupported embellishment, and refined typos, long sentences, literal phrasing, and technical wording.
- Completed `output/release` records with v0.0.2 fix points, QA evidence, and commit guidance.
- Included the requested public documentation files under `doc/public/`.

Verification:
- Stratified random spot-check round 10 PASS: Agent A average 91.18, lowest 84, blockers 0; Agent B average 95.05, lowest 93, blockers 0.
- `npm run review:random-validate:pass` passed, release_confidence=1.0.
- EPUBCheck fatal/error/warning = 0/0/0.
- publication lint issue_count = 0.
- Formal artifact: `output/release/book_v0.0.2.epub`.
- Public docs included: `doc/public/开发计划.md`, `doc/public/细节修复_prompt.md`.

Push note:
- If GitHub access on this machine requires a proxy, set proxy environment variables only in the current shell before pushing.
- Do not store local proxy addresses, ports, or private network settings in project files or commits.
```

## 日本語

```text
読者フィードバックとランダム抽検に基づき『エジソンの火星征服』を精修し、v0.0.2 を公開

理由：
- 読者から、冒頭の `puny efforts` の旧訳が中国語として不自然で、出版品質に達していないとの指摘があった。
- テンプレート規則に従い、読者フィードバック後に EPUB 後工程の層化ランダム抽検を実施し、第 1-9 ラウンドで P1/P2 の阻断問題と局所的な P3 表現問題を確認した。

変更内容：
- `puny efforts` を再訳し、人類の抵抗の小ささと、火星人敗北の原因が人類の軍事的勝利ではなく疾病であるという原文の因果を回復した。
- 洪水と食糧備蓄の確率、行為者関係、避難可能人数、小惑星での墜落推理などの事実・論理ミスを修正した。
- 戦闘の山場における `I cannot make it work` の反対方向の誤訳、停戦台詞の二重否定、稲妻の長さの修飾関係、`four-fifths of an inch` の数値ミスを修正した。
- 用語を統一し、地球側の `electrical ship/electric ship` と火星側の `airship/aerial vessel` を中国語訳で明確に区別した。
- Princess Masaco、公主雅子、Zanzibar とヴィクトリア女王一行に関する人名・地名の意味関係を修正した。
- 原文小見出しの本文混入、根拠のない加筆、誤字、長文の硬さ、直訳調、専門表現の不自然さを修正した。
- `output/release` に v0.0.2 の修正点、QA 証拠、コミット説明を追記した。
- 今回の push 対象として、`doc/public/开发计划.md` と `doc/public/细节修复_prompt.md` の公開文書も追加した。

検証：
- 層化ランダム抽検第 10 ラウンド PASS：Agent A 平均 91.18、最低 84、阻断 0；Agent B 平均 95.05、最低 93、阻断 0。
- `npm run review:random-validate:pass` 通過、release_confidence=1.0。
- EPUBCheck fatal/error/warning = 0/0/0。
- publication lint issue_count = 0。
- 正式成果物：`output/release/book_v0.0.2.epub`。
- 追加公開文書：`doc/public/开发计划.md`、`doc/public/细节修复_prompt.md`。

push 時の注意：
- この端末で GitHub アクセスにプロキシが必要な場合は、push 前に現在の shell だけで一時的にプロキシ環境変数を設定する。
- ローカルのプロキシアドレス、ポート、私的ネットワーク設定をプロジェクトファイルや commit に保存しない。
```
