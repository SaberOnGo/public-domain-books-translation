# AI クライアント利用ガイド：このリポジトリの prompt で本を作る方法

このガイドは、AI クライアントを使って翻訳公版書を作りたい人向けです。プログラミングができなくても大丈夫です。プロジェクトを開き、短い依頼文を貼り付け、AI が作った書籍ファイルを確認できれば始められます。

## まず理解する 4 つのこと

1. **通常のユーザーが入力するのは 3 項目だけです。**
   AI に「翻訳したい本」「対象言語」「正しい翻訳 prompt を自動選択するルール」を伝えるだけでかまいません。このルールの完全な書き方は下の[いちばん簡単な開始 prompt](#いちばん簡単な開始-prompt)にあります。信頼できる原文、原言語、テンプレート、プロジェクトフォルダ、release、検証コマンドは AI が処理します。

2. **ルールは AI に読ませます。**
   ユーザーがリポジトリの規則を理解する必要はありません。正しい公開 prompt を AI に自動選択させてください。

3. **完成扱いできるのは release または private artifact の結果だけです。**
   AI が出典確認、権利確認、翻訳、レビュー、EPUB ビルド、抜き取り検査、release を行います。パブリックドメインまたは許諾済みプロジェクトでは `output/release/`、個人利用プロジェクトでは `output/private_artifacts/` を確認してください。

4. **英語から簡体字中国語へのプロジェクトでは、既定で 2 種類の EPUB を出力します。**
   原言語が英語、対象言語が簡体字中国語の場合、AI は対象言語のみの簡体字中国語 EPUB と英中対照 EPUB の両方を出力します。これは公開プロジェクトか個人利用プロジェクトかとは独立した設定です。他の言語ペアで対照版も必要な場合だけ、prompt に次の一文を追加してください：`请输出 edition_type: bilingual_parallel，同时生成目标语言版 EPUB 和源语言-目标语言双语对照版 EPUB。`

## いちばん簡単な開始 prompt

使っている AI クライアントでこのプロジェクトを開くか、LifeBook Launcher に開かせます。

次の prompt を AI クライアントに貼り付け、`{...}` を本と対象言語に置き換えてください。

### パブリックドメイン書籍翻訳 prompt

```text
翻訳したい本：{書名、作者（任意）。信頼できる原文リンクがあれば一緒に貼ってよい}
対象言語：{例：簡体字中国語}
[重要な固有名詞（人名、地名、用語、まれな名前、音訳すると読みにくい名前など）の翻訳形式] 設定 = 3

正しい翻訳 prompt を自動的に選んでください。
- 対応する原言語テンプレートがすでにある場合は、doc/public/user_prompt/book_translation_existing_template.md を実行してください。
- 対応する原言語テンプレートがまだない場合は、doc/public/user_prompt/book_translation_new_template.md を実行してください。

権利または出典証拠を確認できない場合を除き、技術項目を私に入力させないでください。信頼できるパブリックドメイン原文を自動で探し、書籍プロジェクトを作成し、翻訳、レビュー、EPUB ビルド、層化ランダム抜き取り検査、release まで完了してください。
原言語が英語、対象言語が簡体字中国語の場合は、既定で `edition_type: bilingual_parallel` とし、対象言語のみの簡体字中国語 EPUB と英中対照 EPUB の両方を生成してください。他の言語ペアでは、私が明示的に要求した場合だけ対照版を出力してください。
翻訳中は、各章ごとに「翻訳後の全量チェックと修正」を必ず実行してください。章全体の原文と訳文を照合し、忠実度、対象言語としての読みやすさ、用語、タイトル/小見出し、注、図表・数式まわりの本文接続、原文構文の残留、硬すぎる直訳、過剰説明、根拠のない加筆を確認します。問題が見つかったら修正しますが、その round は PASS にしてはいけません。新しい章全体の再チェックを追加し、最新 round がゼロ問題 PASS になるまで続けてください。
最初の EPUB 生成後は、「層化ランダム抜き取り検査と defect family の追跡」を実行してください。サンプルで問題が出た場合、そのサンプルだけを直してはいけません。同じ round で defect family として分類し、`rg`、用語表、タイトル表、sample manifest、小さな原文照合を使って全書の同類候補を監査し、確認済みの命中を修正し、例外を記録し、新しい seed で次 round を実行します。翻訳品質の defect family には `skills/translation-quality-defect-families/SKILL.md` を使用してください。
```

固有名詞の翻訳形式設定は省略可能で、既定値は `3` です。値の意味：`1` 対象言語へ直接翻訳、`2` 原文のまま翻訳しない、`3` 本文初出は `訳名（原文）`・以後は訳名、`4` 本文初出は `訳名（原文）`・以後は原文、`5` 本文初出は `訳名（原文）` に承認済み注番号を付け、以後は訳名。

## 個人利用の書籍翻訳 prompt

自分が持っているローカル書源を、個人学習用としてのみ翻訳し、再配布も商用利用もしない場合は、次の prompt を使います。

```text
翻訳したい本：{書名、ローカルフォルダ/パス: XXX}
対象言語：{例：簡体字中国語}
[重要な固有名詞（人名、地名、用語、まれな名前、音訳すると読みにくい名前など）の翻訳形式] 設定 = 3

正しい翻訳 prompt を自動的に選んでください。
- 対応する原言語テンプレートがすでにある場合は、doc/public/user_prompt/book_translation_private_existing_template.md を実行してください。
- 対応する原言語テンプレートがまだない場合は、doc/public/user_prompt/book_translation_private_new_template.md を実行してください。

これは私の個人利用です。再配布せず、商用利用もしません。私が指定したローカル書源を使用してください。
プロジェクトを自動作成し、テンプレートが定める体系的な翻訳フロー全体を厳格に完了してください。いかなる漏れも許可しません。
原言語が英語、対象言語が簡体字中国語の場合は、既定で `edition_type: bilingual_parallel` とし、対象言語のみの簡体字中国語 EPUB と英中対照 EPUB の両方を private artifact として生成してください。他の言語ペアでは、私が明示的に要求した場合だけ対照版を出力してください。
翻訳中は各章ごとの全量チェックと修正を必ず実行してください。最初の EPUB 後は層化ランダム抜き取り検査と defect family closure を実行してください。翻訳品質の defect family は、まずその書籍内で閉じ、再利用できる教訓を `skills/translation-quality-defect-families/SKILL.md` に統合してください。
```

個人利用プロジェクトは `books/private/{target}/{number}_{対象言語の書名}_{対象言語の著者名}/` に作成してください。最終版の成果物は `output/private_artifacts/` に置かれます。これは公開 release ではなく、GitHub に公開してはいけません。

## EPUB 後の精密レビュー prompt（任意）

最初の EPUB が生成されたあと、AI に単に「精密に直して」とだけ依頼しないでください。目的に応じて次の 2 つを使い分けます。

- **Prompt B：章ごとの全量再点検と修正。** 古いフローのプロジェクト、各章のゼロ問題 `qa/chapter_controls/*.control.md` がない場合、または各章が十分に点検済みか不安な場合に使います。
- **Prompt C：層化ランダム抜き取り検査と defect family closure。** 最初の EPUB 後の公開前ゲートです。システム的な盲点を見つけ、全書の同類箇所を監査し、修正し、新しい seed で再検査してから release/private artifact に進みます。

推奨順序：古いプロジェクトまたは不確かなプロジェクトでは **Prompt B** を先に実行し、その後 **Prompt C** を実行します。各章に信頼できるゼロ問題 control 記録がある場合は、**Prompt C** から始めてもかまいません。

### Prompt B：章ごとの全量再点検と修正

```text
書籍プロジェクト：{書籍プロジェクトのパス。例：books/{target}/{number}_{対象言語の書名}_{対象言語の著者名}}

まず AGENTS.md、この書籍の SKILL.md（あれば）、template/epub_pipeline/README.md、template/epub_pipeline/common/README.md、template/epub_pipeline/common/prompts/08a_chapter_post_translation_control.md、template/epub_pipeline/common/references/quality_gate_framework.md、対象言語の品質フレームワーク、`skills/translation-quality-defect-families/SKILL.md` を読んでください。

/goal を設定してください：この書籍の翻訳済み全章について「翻訳後の章全量再点検と修正」を実行します。各章では章全体の原文、章全体の訳文、読者に見える文脈を照合し、忠実度、訳抜け/誤訳、対象言語としての読みやすさ、文学性、読者を引き込む力、必要な場合の説明リズム、用語の安定性、人名/地名/書名/船名/機関名、タイトルと小見出し、注、図表/数式/表/画像と本文の接続、原文構文の残留、硬すぎる直訳、過剰説明、根拠のない加筆、読者に見える AI/制作痕跡、異常な空白/文字化け、古い紙本目次の残留を確認してください。

環境が許すなら章ごとに並列処理してもよいですが、各章は独立して閉じてください。各 round は章全体を点検します。問題が見つかった場合、その章を修正しますが、その round は `FIXED_RECHECK_REQUIRED` と記録し、PASS にしてはいけません。その後、新しい章全体の再チェックを追加します。最新 round が `scope: FULL_CHAPTER`、`issues_found: 0`、`fixes_applied: 0`、`unresolved_blocking_issues: 0`、`latest_round_status: PASS`、`allow_next_chapter: true` を記録した場合だけ、その章は通過です。

いずれかの章で再発し得る翻訳品質 defect family が見つかった場合、たとえば短文への切断、比喩の衝突、列挙句読点の引きずり、代名詞の指示不明、原文構文の残留、用語の揺れ、タイトル過積載、過剰説明、根拠のない加筆については、`skills/translation-quality-defect-families/SKILL.md` に従ってください。発見方法、分類、低 token 監査、修正、再チェックを記録します。まず `rg`、用語表、禁止表記、タイトル表、章 control 記録、小さな原文照合で候補を集め、候補だけを agent に確認させます。agent に全書を盲目的に読ませないでください。

完了後、`qa/chapter_controls/*.control.md`、必要な `qa/fidelity/`、`qa/readability/`、`qa/terminology/`、`qa/gates/` を作成または更新し、通過した章を `chapters/final/` に反映してください。その後 EPUB を再構築し、利用可能な chapter-control、preflight、publication lint、asset、EPUBCheck コマンドを実行してください。修正した章、defect family、検証結果、Prompt C に残る作業を報告してください。
```

### Prompt C：層化ランダム抜き取り検査と defect family closure

`N` は「問題なしの連続 spot-check round 数」です。`1` は token 節約向けの最低強度、`2` は通常の本に推奨、`3` は用語密度が高い本、科学・数学・図表の多い本、または高品質版向けです。

```text
書籍プロジェクト：{書籍プロジェクトのパス。例：books/{target}/{number}_{対象言語の書名}_{対象言語の著者名}}
終了に必要な問題なし連続 spot-check round 数 N：{1/2/3。既定は 2}

まず AGENTS.md、この書籍の SKILL.md（あれば）、template/epub_pipeline/README.md、template/epub_pipeline/common/README.md、template/epub_pipeline/common/prompts/16a_stratified_random_spotcheck.md、template/epub_pipeline/common/references/stratified_random_spotcheck.md、template/epub_pipeline/common/references/quality_gate_framework.md、cover、book-info/frontmatter、assets、release に関する規則、`skills/translation-quality-defect-families/SKILL.md` を読んでください。

/goal を設定してください：生成済み EPUB に対して「層化ランダム抜き取り検査と defect family closure」を実行し、通過後に release または private artifact を再生成します。これは普通の推敲ではありません。目的は、公開前にシステム的な盲点を見つけ、全書の同類箇所を監査し、修正を閉じ、新しい seed round を通すことです。

reader-facing audit units を対象に層化ランダム抽出を実行してください。ページ数でも段落だけでもありません。実際に存在する paragraph、table、figure、formula/proof、caption/note をすべて層として扱います。最低 2 つの独立 review agent を使い、互いの結論を参照させないでください。`reviews/random_spotcheck/round_XXX/` に seed、manifest、samples、evidence、reviews、fixes/fix_log.md、verification/closure_check.md を保存します。

サンプルのいずれかで P0/P1/P2、単項目 <80、読者が理解できない箇所、忠実度のずれ、事実/用語/人名/タイトル/注/図表/数式の誤り、原文構文の残留、硬い直訳、短文への切断、比喩の衝突、列挙句読点の引きずり、代名詞の指示不明、過剰説明、根拠のない加筆が見つかった場合、同じ round で defect family として分類してください。全書の同類候補を監査し、確認済みの命中をすべて修正します。サンプルだけを修正してはいけません。2 回目の失敗まで全書監査を待ってはいけません。

翻訳品質 defect family では、低 token 監査を先に行ってください。`rg`、`glossary/terms.csv`、`forbidden_body_renderings`、タイトル表、章 control 記録、sample manifest、小さな原文照合で候補を集め、候補だけを agent に渡します。再利用できる教訓は `skills/translation-quality-defect-families/SKILL.md` に統合してください。

修正のたびに EPUB を再構築し、新しい seed で次の spot-check round を実行します。終了条件：直近 N 個の新 seed round が PASS、発見済み defect family がすべて閉じている、`npm run review:random-validate:pass` が通る、release_confidence がテンプレート要件を満たすこと。

通過後は staging を清掃または再構築し、EPUB を再生成し、publication lint、asset manifest、cover output、reader-facing policy、EPUBCheck、および release または private artifact script を実行してください。パブリックドメインまたは許諾済みプロジェクトでは公開可能な EPUB をこの書籍の output/release/ に出力し、release_state.json.latest_status を PASS にしてください。個人利用プロジェクトでは最終 private artifact を output/private_artifacts/ に出力し、private_artifact_state.json.latest_status を PASS にしてください。release EPUB path または private artifact path、抜き取り検査 round、修正概要、検証コマンド結果、残りリスクを報告してください。
```

## 知っておくべき重要な場所

- `.\template\epub_pipeline`：現在どの原言語・言語方向テンプレートがあるか確認する場所です。AI はここを見て、既存テンプレート prompt か新規テンプレート prompt かを判断します。
- `.\tools\lifebook-launcher`：LifeBook Launcher クライアントのインストール・起動フォルダです。LifeBook プロジェクトを使い、OpenCode をインストールするためにユーザーが知っておくべき場所です。
- `.\doc\public\user_prompt`：公開 prompt はここにあります。prompt の詳細を確認したり、手動で調整したりできます。
- `.\books\zh-Hans`：もっとも重要な完成本の場所です。簡体字中国語への翻訳が完了したら、該当する書籍フォルダの `output\release\` を確認します。公開可能なのは release 成果物です。
- `.\books\private`：個人利用の書籍プロジェクト用フォルダです。パブリックドメインではない私的翻訳の原文、訳文、QA、EPUB 出力、`output\private_artifacts\` の私的成果物はここだけに保存します。このフォルダは Git で無視され、GitHub には公開されません。

## 4 つの翻訳 prompt とは

- `doc/public/user_prompt/book_translation_existing_template.md`：このリポジトリに対応する原言語テンプレートがすでにある場合に使います。例：日本語から簡体字中国語、英語から簡体字中国語、古代ギリシア語から簡体字中国語。
- `doc/public/user_prompt/book_translation_new_template.md`：対応する原言語テンプレートがまだない場合に使います。例：初めてフランス語から簡体字中国語の本を作る場合。
- `doc/public/user_prompt/book_translation_private_existing_template.md`：個人利用のローカル書源で、対応する原言語テンプレートがすでにある場合に使います。
- `doc/public/user_prompt/book_translation_private_new_template.md`：個人利用のローカル書源で、対応する原言語テンプレートがまだない場合に使います。
- `doc/public/user_prompt/how_to_use_book_translation_prompts.md`：3 項目の入力方法だけを説明する、さらに短い初心者向けガイドです。

どちらを使うべきか分からない場合は、まずテンプレートが存在するか AI に確認させてください。通常のユーザーは `language-pair template name`、slug、profile、release version、npm コマンドを理解する必要はありません。

## どのクライアントを使うべきか

| クライアント | 向いている人 | prompt の使い方 |
| --- | --- | --- |
| Codex App | GUI、diff、terminal、browser、Git review をまとめて使いたい人 | リポジトリを開き、新しい thread に `/goal` を貼る |
| Claude Code | ターミナルでコマンドライン Agent を使いたい人 | リポジトリで Claude Code を起動し、prompt を貼る |
| LifeBook Launcher | 手作業をできるだけ減らしたい人。<br>OpenCode クライアントのインストールが必要 | Launcher を開いて OpenCode をインストールします。<br>OpenCode は DeepSeek、豆包など多くの主要モデルに対応しています。<br>OpenCode で書籍翻訳タスクを選び、3 項目を貼ります（[完全な例](#いちばん簡単な開始-prompt)） |
| Google Antigravity | AI IDE で agent に計画、編集、実行を任せたい人 | workspace を開き、agent 入力欄に prompt を貼る |

## LifeBook Launcher

プロジェクトやクライアント設定を手作業で扱いたくない場合は、LifeBook Launcher を使えます。Launcher は OpenCode クライアントをダウンロードして開けます。OpenCode は DeepSeek、豆包など、市場の多くの AI モデルに対応しています。使用前に OpenCode 内で対象モデルの API Key を設定してください。

- **LifeBook Launcher** を開きます。
- このプロジェクトを選ぶ、または開きます。
- 必要に応じて OpenCode クライアントをダウンロードまたは開き、OpenCode で API Key を設定します。
- 「翻訳したい本」「対象言語」「prompt 自動選択ルール」の 3 項目を貼り付けます。完全な書き方は[いちばん簡単な開始 prompt](#いちばん簡単な開始-prompt)にあります。
- AI が完了したら、パブリックドメインまたは許諾済みプロジェクトでは書籍フォルダの `output/release/`、個人利用プロジェクトでは `output/private_artifacts/` を確認します。

## Codex App

1. Codex App をインストールして開く。
2. このリポジトリのフォルダを選ぶ。
3. 新しい thread を作る。
4. `/goal` を貼り付ける。
5. AI が `AGENTS.md` と `template/` を読むのを待つ。
6. 変更予定ファイルを確認する。
7. 最後に `books/zh-Hans/.../output/release/`、または対象言語に対応する `books/{target}/.../output/release/` を確認する。個人利用プロジェクトでは `books/private/{target}/.../output/private_artifacts/` を確認する。

Codex App は、AI が変更したファイルを確認しやすいので、このリポジトリの長い作業に向いています。

## Google Antigravity

1. Google Antigravity をインストールする。
2. このリポジトリを workspace として開く。
3. agent 入力欄にスターター prompt を貼る。
4. `AGENTS.md` と `template/epub_pipeline/` を先に読むよう指示する。
5. コマンド実行やファイル編集は確認モードで進める。
6. diff、テスト結果、release ファイルを確認する。

## よくあるミス

- AI にテンプレートを読ませず、いきなり全訳させる。
- `output/book.epub` だけで完成扱いし、公開プロジェクトで `output/release/`、個人利用プロジェクトで `output/private_artifacts/` を作らない。
- 権利確認前に翻訳を始める。
- 現代翻訳を参考・改写元にする。
- 抜き取り検査で問題が出たのに新 round を追加しない。
- 書籍固有データを `template/` に書く。
