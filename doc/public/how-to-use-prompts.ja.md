# AI クライアント利用ガイド：このリポジトリの prompt で本を作る方法

このガイドは、AI クライアントを使って翻訳公版書を作りたい人向けです。プログラミングができなくても大丈夫です。プロジェクトを開き、短い依頼文を貼り付け、AI が作った書籍ファイルを確認できれば始められます。

## まず理解する 3 つのこと

1. **通常のユーザーが入力するのは 2 項目だけです。**
   AI に「翻訳したい本」と「対象言語」を伝えるだけでかまいません。信頼できる原文、原言語、テンプレート、プロジェクトフォルダ、release、検証コマンドは AI が処理します。

2. **ルールは AI に読ませます。**
   ユーザーがリポジトリの規則を理解する必要はありません。正しい公開 prompt を AI に自動選択させてください。

3. **完成扱いできるのは release 結果だけです。**
   AI が出典確認、権利確認、翻訳、レビュー、EPUB ビルド、抜き取り検査、release を行います。最後に `output/release/` の成果物を確認してください。

## いちばん簡単な開始 prompt

使っている AI クライアントでこのプロジェクトを開くか、LifeBook Launcher に開かせます。

次の prompt を AI クライアントに貼り付け、`{...}` を本と対象言語に置き換えてください。

```text
翻訳したい本：{書名、作者。信頼できる原文リンクがあれば一緒に貼ってよい}
対象言語：{例：簡体字中国語}

現在のリポジトリで、正しいパブリックドメイン書籍翻訳 prompt を自動的に選んでください。
- 対応する原言語テンプレートがすでにある場合は、doc/public/user_prompt/book_translation_existing_template.md を実行してください。
- 対応する原言語テンプレートがまだない場合は、doc/public/user_prompt/book_translation_new_template.md を実行してください。

権利または出典証拠を確認できない場合を除き、技術項目を私に入力させないでください。信頼できるパブリックドメイン原文を自動で探し、書籍プロジェクトを作成し、翻訳、レビュー、EPUB ビルド、層化ランダム抜き取り検査、release まで完了してください。
```

## 知っておくべき 2 つの場所

- `doc/public/user_prompt/`：公開 prompt はここにあります。
- `books/.../output/release/`：AI 完了後、公開可能な EPUB はここに出力されます。

## 2 つの公開 prompt とは

- `doc/public/user_prompt/book_translation_existing_template.md`：このリポジトリに対応する原言語テンプレートがすでにある場合に使います。例：日本語から簡体字中国語、英語から簡体字中国語、古代ギリシア語から簡体字中国語。
- `doc/public/user_prompt/book_translation_new_template.md`：対応する原言語テンプレートがまだない場合に使います。例：初めてフランス語から簡体字中国語の本を作る場合。
- `doc/public/user_prompt/how_to_use_book_translation_prompts.md`：本と対象言語だけをどう入力するか説明する、さらに短い初心者向けガイドです。

どちらを使うべきか分からない場合は、まずテンプレートが存在するか AI に確認させてください。通常のユーザーは `source-target`、slug、profile、release version、npm コマンドを理解する必要はありません。

## どのクライアントを使うべきか

| クライアント | 向いている人 | prompt の使い方 |
| --- | --- | --- |
| Codex App | GUI、diff、terminal、browser、Git review をまとめて使いたい人 | リポジトリを開き、新しい thread に `/goal` を貼る |
| LifeBook Launcher | 手作業をできるだけ減らしたい人 | Launcher を開き、書籍翻訳タスクを選び、2 行の入力を貼る |
| Google Antigravity | AI IDE で agent に計画、編集、実行を任せたい人 | workspace を開き、agent 入力欄に prompt を貼る |

## LifeBook Launcher

プロジェクトやクライアント設定を手作業で扱いたくない場合は、LifeBook Launcher を使えます。

- **LifeBook Launcher** を開きます。
- このプロジェクトを選ぶ、または開きます。
- 「翻訳したい本」と「対象言語」の 2 行を貼り付けます。
- AI が完了したら、書籍フォルダの `output/release/` を確認します。

## Codex App

1. Codex App をインストールして開く。
2. このリポジトリのフォルダを選ぶ。
3. 新しい thread を作る。
4. `/goal` を貼り付ける。
5. AI が `AGENTS.md` と `template/` を読むのを待つ。
6. 変更予定ファイルを確認する。
7. 最後に `books/.../output/release/` を確認する。

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
- `output/book.epub` だけで完成扱いし、`output/release/` を作らない。
- 権利確認前に翻訳を始める。
- 現代翻訳を参考・改写元にする。
- 抜き取り検査で問題が出たのに新 round を追加しない。
- 書籍固有データを `template/` に書く。
