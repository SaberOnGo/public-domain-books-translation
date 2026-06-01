# AI クライアント利用ガイド：このリポジトリの prompt で本を作る方法

このガイドは、AI クライアントを使って翻訳公版書を作りたい人向けです。プログラミングができなくても大丈夫です。プロジェクトを開き、短い依頼文を貼り付け、AI が作った書籍ファイルを確認できれば始められます。

## まず理解する 3 つのこと

1. **通常のユーザーが入力するのは 3 項目だけです。**
   AI に「翻訳したい本」「対象言語」「正しい翻訳 prompt を自動選択するルール」を伝えるだけでかまいません。このルールの完全な書き方は下の[いちばん簡単な開始 prompt](#いちばん簡単な開始-prompt)にあります。信頼できる原文、原言語、テンプレート、プロジェクトフォルダ、release、検証コマンドは AI が処理します。

2. **ルールは AI に読ませます。**
   ユーザーがリポジトリの規則を理解する必要はありません。正しい公開 prompt を AI に自動選択させてください。

3. **完成扱いできるのは release または private artifact の結果だけです。**
   AI が出典確認、権利確認、翻訳、レビュー、EPUB ビルド、抜き取り検査、release を行います。パブリックドメインまたは許諾済みプロジェクトでは `output/release/`、個人利用プロジェクトでは `output/private_artifacts/` を確認してください。

## いちばん簡単な開始 prompt

使っている AI クライアントでこのプロジェクトを開くか、LifeBook Launcher に開かせます。

次の prompt を AI クライアントに貼り付け、`{...}` を本と対象言語に置き換えてください。

### パブリックドメイン書籍翻訳 prompt

```text
翻訳したい本：{書名、作者（任意）。信頼できる原文リンクがあれば一緒に貼ってよい}
対象言語：{例：簡体字中国語}

正しい翻訳 prompt を自動的に選んでください。
- 対応する原言語テンプレートがすでにある場合は、doc/public/user_prompt/book_translation_existing_template.md を実行してください。
- 対応する原言語テンプレートがまだない場合は、doc/public/user_prompt/book_translation_new_template.md を実行してください。

権利または出典証拠を確認できない場合を除き、技術項目を私に入力させないでください。信頼できるパブリックドメイン原文を自動で探し、書籍プロジェクトを作成し、翻訳、レビュー、EPUB ビルド、層化ランダム抜き取り検査、release まで完了してください。
```

## 個人利用の書籍翻訳 prompt

自分が持っているローカル書源を、個人学習用としてのみ翻訳し、再配布も商用利用もしない場合は、次の prompt を使います。

```text
翻訳したい本：{書名、ローカルフォルダ/パス: XXX}
対象言語：{例：簡体字中国語}

正しい翻訳 prompt を自動的に選んでください。
- 対応する原言語テンプレートがすでにある場合は、doc/public/user_prompt/book_translation_private_existing_template.md を実行してください。
- 対応する原言語テンプレートがまだない場合は、doc/public/user_prompt/book_translation_private_new_template.md を実行してください。

これは私の個人利用です。再配布せず、商用利用もしません。私が指定したローカル書源を使用してください。
プロジェクトを自動作成し、テンプレートが定める体系的な翻訳フロー全体を厳格に完了してください。いかなる漏れも許可しません。
```

個人利用プロジェクトは `books/private/{target}/{number}_{目标语言书名}_{目标语言作者名}/` に作成してください。最終版の成果物は `output/private_artifacts/` に置かれます。これは公開 release ではなく、GitHub に公開してはいけません。

## 精密レビュー prompt（任意）

最初の EPUB が生成されたあと、訳文の品質をさらに高めたい場合は次の prompt を使います。`N` は「問題なしの連続 round 数」です。`1` は token を節約する最低強度、`3` はより厳格で高品質を狙う設定です。迷う場合は `2` にします。

```text
書籍プロジェクト：{書籍プロジェクトのパス。例：books/{target}/{number}_{目标语言书名}_{目标语言作者名}}
終了に必要な問題なし連続 round 数 N：{1/2/3。既定は 2}

まず AGENTS.md、この書籍の SKILL.md（あれば）、template/epub_pipeline/README.md、template/epub_pipeline/common/README.md、および cover、book-info/frontmatter、assets、quality gates、stratified random spot-check、release に関する規則を読んでください。

/goal を設定してください：生成済み EPUB を精密レビューし、テンプレート要件に従って cover、最初のページ/frontmatter、metadata、nav、目次、本文、注、図、数式、表、画像、style、読者に見える内容、EPUB build、release を確認してください。私が明示した項目だけに限定しないでください。

2 つの独立 review agent を起動し、層化ランダム抜き取り検査を行ってください。最低 4 round 実行します。各 round で新しい seed を使い、samples、evidence、reviews、fixes、closure records をテンプレートどおり保存してください。いずれかの round で P0/P1/P2、単項目 <70、読者が理解できない箇所、事実/用語/図表/数式の誤り、またはテンプレートの hard gate failure が見つかった場合は、修正後に新しい round を追加してください。

終了条件：直近 N round 連続で新しい blocking issue がなく、npm run review:random-validate:pass が通ること。N=1 は token 節約向けの最低強度、N=3 はより厳格で、レビュー後の訳本品質を高める設定です。ユーザーが自由に選べます。

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

どちらを使うべきか分からない場合は、まずテンプレートが存在するか AI に確認させてください。通常のユーザーは `source-target`、slug、profile、release version、npm コマンドを理解する必要はありません。

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
