# AI クライアント利用ガイド：このリポジトリの prompt で本を作る方法

このガイドは、AI クライアントを使って書籍制作に参加したい人向けです。プログラミングができなくても大丈夫です。リポジトリを開き、prompt を貼り付け、AI が作ったファイルを確認できれば始められます。

> 重要：API Key をリポジトリ内のファイルに書かないでください。`auth.json`、`.env`、設定画面のスクリーンショット、秘密情報を commit しないでください。

## まず理解する 3 つのこと

1. **通常のユーザーが入力するのは 2 項目だけです。**
   AI に「翻訳したい本」と「対象言語」を伝えるだけでかまいません。信頼できる原文、原言語、テンプレート、プロジェクトフォルダ、release、検証コマンドは AI が処理します。

2. **このリポジトリには必読ルールがあります。**
   毎回、AI に `AGENTS.md` を先に読ませ、その後 `template/epub_pipeline/` の関連テンプレートを読ませます。

3. **AI の初稿はそのまま公開できません。**
   正しい流れは、出典証拠、権利確認、調査、試訳、章ごとの翻訳、レビュー、EPUB ビルド、EPUBCheck、層化ランダム抜き取り検査、release です。

## いちばん簡単な開始 prompt

まずリポジトリのルートへ移動します。

```powershell
cd D:\project\49_public-domain-books-translation
```

リリース版から LifeBook Launcher だけをインストールした場合は、Launcher が自動で準備したプロジェクトフォルダを開いてください。Windows の既定は `D:\LifeBook` です。

次の prompt を AI クライアントに貼り付け、`{...}` を本と対象言語に置き換えてください。

```text
翻訳したい本：{書名、作者。信頼できる原文リンクがあれば一緒に貼ってよい}
対象言語：{例：簡体字中国語}

現在のリポジトリで、正しいパブリックドメイン書籍翻訳 prompt を自動的に選んでください。
- 対応する原言語テンプレートがすでにある場合は、doc/public/user_prompt/book_translation_existing_template.md を実行してください。
- 対応する原言語テンプレートがまだない場合は、doc/public/user_prompt/book_translation_new_template.md を実行してください。

権利または出典証拠を確認できない場合を除き、技術項目を私に入力させないでください。信頼できるパブリックドメイン原文を自動で探し、書籍プロジェクトを作成し、翻訳、レビュー、EPUB ビルド、層化ランダム抜き取り検査、release まで完了してください。
```

`/goal` が使えないクライアントでは、最初の行を次のように変えてください。

```text
目標：現在のリポジトリで新しいパブリックドメイン書籍翻訳 EPUB を作成してください。
```

## 知っておくべき 4 つのフォルダ

- `.\template\epub_pipeline`：現在どの原言語・言語方向テンプレートがあるか確認する場所です。
- `.\tools\lifebook-launcher`：リポジトリコピー内の LifeBook Launcher 入口フォルダです。リリース版ユーザーは通常、インストール済み Launcher を起動します。Launcher がプロジェクトフォルダを自動で準備します。
- `.\doc\public\user_prompt`：公開スターター prompt の場所です。prompt の詳細確認や手動調整に使います。
- `.\books\zh-Hans`：簡体字中国語の書籍出力場所です。完成後は該当書籍フォルダの `output\book.epub` と `output\release\` を確認します。

## 2 つの公開 prompt とは

- `doc/public/user_prompt/book_translation_existing_template.md`：このリポジトリに対応する原言語テンプレートがすでにある場合に使います。例：日本語から簡体字中国語、英語から簡体字中国語、古代ギリシア語から簡体字中国語。
- `doc/public/user_prompt/book_translation_new_template.md`：対応する原言語テンプレートがまだない場合に使います。例：初めてフランス語から簡体字中国語の本を作る場合。
- `doc/public/user_prompt/how_to_use_book_translation_prompts.md`：本と対象言語だけをどう入力するか説明する、さらに短い初心者向けガイドです。

どちらを使うべきか分からない場合は、まずテンプレートが存在するか AI に確認させてください。通常のユーザーは `source-target`、slug、profile、release version、npm コマンドを理解する必要はありません。

## どのクライアントを使うべきか

| クライアント | 向いている人 | prompt の使い方 |
| --- | --- | --- |
| Codex App | GUI、diff、terminal、browser、Git review をまとめて使いたい人 | リポジトリを開き、新しい thread に `/goal` を貼る |
| Claude Code | terminal で Claude / DeepSeek を使いたい人 | リポジトリで `claude` を実行し、prompt を貼る |
| Google Antigravity | AI IDE で agent に計画、編集、実行を任せたい人 | workspace を開き、agent 入力欄に prompt を貼る |
| OpenCode | オープンソースクライアントで DeepSeek を使いたい人 | LifeBook Launcher で OpenCode Desktop を確認/更新し、リポジトリを開いて prompt を貼る |

## LifeBook Launcher

プロジェクトとクライアント更新を手動で扱いたくない場合は、LifeBook Launcher を使えます。API Key は保存せず、OpenCode 本体もこのリポジトリには入れません。

- 一般ユーザーはリリースパッケージ内の **LifeBook Launcher** アプリまたはインストーラーをダブルクリックします。
- 現在の Windows ローカル入口：`tools\lifebook-launcher\LifeBook Launcher Setup.exe`。
- 開発者向けソースフォルダ：`tools/lifebook-launcher/source/`。
- LifeBook プロジェクトを自動で準備・更新します。Windows の既定プロジェクトフォルダは `D:\LifeBook` です。
- OpenCode Desktop の確認/更新、LifeBook Launcher 自体のダウンロード、インストール、再起動ができます。
- 自動起動は設定画面でオン/オフできます。

## Codex App

1. Codex App をインストールして開く。
2. このリポジトリのフォルダを選ぶ。
3. 新しい thread を作る。
4. `/goal` を貼り付ける。
5. AI が `AGENTS.md` と `template/` を読むのを待つ。
6. 変更予定ファイルを確認する。
7. 最後に `books/.../output/release/` を確認する。

Codex App は thread、worktree、内蔵 terminal、diff review、Git 操作があるため、このリポジトリの長い作業に向いています。

DeepSeek について：Codex App は通常、OpenAI/Codex アカウントのモデルを使います。DeepSeek を使いたい場合は OpenCode または Claude Code が簡単です。Codex CLI の custom provider は、使用中のバージョンや gateway が必要なプロトコルを明確にサポートしている場合だけ試してください。

## Claude Code で DeepSeek を使う

Windows PowerShell：

```powershell
$env:ANTHROPIC_BASE_URL="https://api.deepseek.com/anthropic"
$env:ANTHROPIC_AUTH_TOKEN="<your DeepSeek API Key>"
$env:ANTHROPIC_MODEL="deepseek-v4-pro[1m]"
$env:ANTHROPIC_DEFAULT_OPUS_MODEL="deepseek-v4-pro[1m]"
$env:ANTHROPIC_DEFAULT_SONNET_MODEL="deepseek-v4-pro[1m]"
$env:ANTHROPIC_DEFAULT_HAIKU_MODEL="deepseek-v4-flash"
$env:CLAUDE_CODE_SUBAGENT_MODEL="deepseek-v4-flash"
$env:CLAUDE_CODE_EFFORT_LEVEL="max"

cd D:\project\49_public-domain-books-translation
claude
```

macOS/Linux：

```bash
export ANTHROPIC_BASE_URL=https://api.deepseek.com/anthropic
export ANTHROPIC_AUTH_TOKEN="<your DeepSeek API Key>"
export ANTHROPIC_MODEL="deepseek-v4-pro[1m]"
export ANTHROPIC_DEFAULT_OPUS_MODEL="deepseek-v4-pro[1m]"
export ANTHROPIC_DEFAULT_SONNET_MODEL="deepseek-v4-pro[1m]"
export ANTHROPIC_DEFAULT_HAIKU_MODEL="deepseek-v4-flash"
export CLAUDE_CODE_SUBAGENT_MODEL="deepseek-v4-flash"
export CLAUDE_CODE_EFFORT_LEVEL=max

cd /path/to/49_public-domain-books-translation
claude
```

起動後、スターター prompt を貼り付けます。

## OpenCode で DeepSeek を使う

OpenCode は DeepSeek を試すのに分かりやすい選択肢です。

1. OpenCode をインストールする。
2. リポジトリで起動する。

```powershell
cd D:\project\49_public-domain-books-translation
opencode
```

3. OpenCode で次を入力する。

```text
/connect
```

4. `deepseek` を検索して選択する。
5. DeepSeek API Key を貼り付ける。
6. `DeepSeek-V4-Pro` を選ぶ。
7. このガイドの `/goal` prompt を貼り付ける。

先に計画だけ見たい場合は、次を追加してください。

```text
まず実行計画と変更予定ファイル一覧だけを出してください。ファイルを書く前に私の確認を待ってください。
```

## Google Antigravity

1. Google Antigravity をインストールする。
2. このリポジトリを workspace として開く。
3. agent 入力欄にスターター prompt を貼る。
4. `AGENTS.md` と `template/epub_pipeline/` を先に読むよう指示する。
5. コマンド実行やファイル編集は確認モードで進める。
6. diff、テスト結果、release ファイルを確認する。

DeepSeek について：Antigravity の画面に DeepSeek provider が無い場合、無理に設定しないでください。DeepSeek が必要な場合は OpenCode または Claude Code を使います。

## よく使う確認コマンド

書籍プロジェクト内で：

```powershell
npm run build:epub
npm run check:epub
npm run review:random-samples
npm run review:random-validate:pass
npm run release:create
```

依存関係が無い場合は、`books/` で一度だけ：

```powershell
cd D:\project\49_public-domain-books-translation\books
npm install
```

## よくあるミス

- API Key を commit する。
- AI にテンプレートを読ませず、いきなり全訳させる。
- `output/book.epub` だけで完成扱いし、`output/release/` を作らない。
- 権利確認前に翻訳を始める。
- 現代翻訳を参考・改写元にする。
- 抜き取り検査で問題が出たのに新 round を追加しない。
- 書籍固有データを `template/` に書く。

## 参考リンク

- Codex App：https://developers.openai.com/codex/app
- Codex configuration reference：https://developers.openai.com/codex/config-reference
- DeepSeek API quick start：https://api-docs.deepseek.com/
- DeepSeek with Claude Code：https://api-docs.deepseek.com/guides/agent_integrations/claude_code
- DeepSeek with OpenCode：https://api-docs.deepseek.com/guides/agent_integrations/opencode
- OpenCode providers：https://open-code.ai/en/docs/providers
- Google Antigravity docs：https://www.antigravity.google/docs/overview
