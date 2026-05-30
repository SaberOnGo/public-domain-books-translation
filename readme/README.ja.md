# LifeBook 書坊 パブリックドメイン書籍翻訳プロジェクト

<table align="center">
  <tr>
    <td align="center"><h3><a href="../README.zh-CN.md">简体中文</a></h3></td>
    <td align="center"><h3><a href="./README.zh-TW.md">繁體中文</a></h3></td>
    <td align="center"><h3><a href="../README.md">English</a></h3></td>
    <td align="center"><h3><a href="./README.ja.md">日本語</a></h3></td>
  </tr>
</table>

LifeBook 書坊は、パブリックドメイン書籍を多言語で翻訳し、レビュー済みの読みやすい EPUB にするためのワークフローです。AI の初稿をそのまま公開するのではなく、出典証拠、権利確認、下訳、レビュー、EPUB 検証、層化ランダム抜き取り検査、バージョン付きリリースを残します。

プログラミングができなくても参加できます。本の提案、出典調査、試読、原文との比較、読みにくい箇所の報告、EPUB テスト、テンプレートやスクリプトの改善が役に立ちます。

## クイックスタート

短い利用ガイド：

- [日本語ガイド](../doc/public/how-to-use-prompts.ja.md)
- [English guide](../doc/public/how-to-use-prompts.en.md)
- [简体中文说明](../doc/public/how-to-use-prompts.zh-CN.md)
- [繁體中文說明](../doc/public/how-to-use-prompts.zh-TW.md)

AI クライアントに渡す最小 prompt：

```text
翻訳したい本：{書名、作者（任意）。信頼できる原文 URL があれば貼る}
対象言語：{例：日本語、英語、スペイン語、簡体字中国語}

正しい翻訳 prompt を自動的に選んでください。
- 対応する原言語テンプレートがすでにある場合は、doc/public/user_prompt/book_translation_existing_template.md を実行してください。
- 対応する原言語テンプレートがまだない場合は、doc/public/user_prompt/book_translation_new_template.md を実行してください。

権利または出典証拠を確認できない場合を除き、技術項目を私に入力させないでください。信頼できるパブリックドメイン原文を自動で探し、書籍プロジェクトを作成し、翻訳、レビュー、EPUB ビルド、層化ランダム抜き取り検査、release まで完了してください。
LifeBook Digest の利用が明示されていない場合は自動判断します。長編小説、専門書、哲学書は EPUB 出力後に Digest を生成し、短編小説、自然科学系、その他の種類では生成しません。
Digest を生成する場合は、書籍プロジェクトのルートに `digest.config.json`（`enabled=true`、`merge_into_epub=true`）を書き、リポジトリルートから `python -m digest.lifebook_digest --book-root books/{target}/{number}_{book_id_slug}` を実行してください。出力は標準 EPUB のままです。
```

パブリックドメインではない本は、ローカルの private-use モードだけで扱います。ユーザーは自分のローカル電子書籍ファイルを提供し、個人学習用のみ、再配布なし、商用利用なしと明示する必要があります。AI は `books/private/{target}/{number}_{book_slug}/` に private project を作成します。スクリプトは `template/epub_pipeline/modes/private_use/` を重ね、private-use の cover、frontmatter、artifact ルールを公開用ルールから分離します。`books/private/` は Git で無視され、原文、訳文、QA、EPUB、private artifact を GitHub に公開してはいけません。

## AI クライアント

このリポジトリは特定のモデルに依存しません。Codex App、Claude Code、OpenCode、aider、Antigravity、その他ローカルファイルを扱える AI クライアントを利用できます。条件は、リポジトリを読めること、ファイル編集とコマンド実行ができること、`AGENTS.md` に従うことです。

一般ユーザーが使いやすい入口として **LifeBook Launcher** を使います。

- Windows ユーザーは現在、`tools\lifebook-launcher\LifeBook Launcher Setup.exe` をダブルクリックできます。
- リリース版のユーザーは **LifeBook Launcher** アプリまたはインストーラーだけをダウンロードして起動できます。Launcher が LifeBook プロジェクトフォルダを自動で準備・更新します。Windows の既定フォルダは `D:\LifeBook` です。
- このリポジトリ内のソースフォルダは `tools/lifebook-launcher/source/` で、開発者とパッケージ担当者向けです。
- LifeBook プロジェクト更新の自動管理、OpenCode Desktop の確認/更新、LifeBook Launcher 自体の更新、自動起動設定を扱います。

Launcher は API Key を保存せず、OpenCode 本体もこのリポジトリに含めません。OpenCode クライアントの使い方は [OpenCode クライアント説明](../docs/ai-clients/opencode.zh-CN.md) を参照してください。

## ユーザーが知っておくべき重要フォルダ

- `.\template\epub_pipeline`：現在どの原言語・言語方向テンプレートがあるか確認する場所です。`en-zh-Hans`、`ja-zh-Hans`、`grc-zh-Hans` などがあります。
- `.\tools\lifebook-launcher`：LifeBook Launcher クライアントのインストール・起動フォルダです。LifeBook プロジェクトを使い、OpenCode をインストールするためにユーザーが知っておくべき場所です。
- `.\doc\public\user_prompt`：公開スターター prompt の場所です。AI に渡す prompt の詳細を確認したり、手動で調整したりできます。
- `.\books\zh-Hans`：もっとも重要な完成本の場所です。簡体字中国語への翻訳が完了したら、該当する書籍フォルダの `output\release\` を確認します。公開可能なのは release 成果物です。
- `.\books\private`：ローカル private-use 書籍プロジェクト用フォルダです。ユーザー提供のローカル書源を使う非パブリックドメインの個人学習用翻訳はここに置きます。このフォルダは Git で無視され、GitHub に公開してはいけません。

## LifeBook Digest

<table align="center">
  <tr>
    <td align="center"><h3><a href="./digest/README.ja.md">LifeBook Digest ガイド</a></h3></td>
    <td align="center"><h3><a href="../license/DIGEST_LICENSE.ja.md">Digest ライセンス</a></h3></td>
  </tr>
</table>

LifeBook 翻訳公開システムに LifeBook Digest モジュールが追加されました。これは本を薄く読むための後処理です。EPUB 出力後、LifeBook Digest は長い本を AI agent に渡して核となる内容を抽出できます。結果は単なる文章要約ではなく、章トポロジーと知識の流れも含み、本全体の構造を一目で把握しやすくします。

LifeBook Digest は現在、独立した LifeBook 後処理モジュールとして実装されています。謝辞と第三者プロジェクトからの着想については [LifeBook Digest ガイド](./digest/README.ja.md) と [Digest ライセンス](../license/DIGEST_LICENSE.ja.md) を参照してください。ライセンスと今後の再利用条件は [Digest ライセンス](../license/DIGEST_LICENSE.ja.md) に従います。

## リポジトリ構成

- `AGENTS.md`：すべての AI agent が最初に読む必須ルール。
- `digest/`：LifeBook Digest の共通後処理モジュール。各書籍は `digest.config.json` で有効化と EPUB 統合を制御します。
- `template/epub_pipeline/`：正式なワークフローテンプレートとルール。
- `template/epub_pipeline/common/`：共通 EPUB ワークフロー、スクリプト、出典証拠、権利確認、品質ゲート、ランダム検査、リリース規則。
- `template/epub_pipeline/{source-target}/`：言語方向ごとの prompt、用語、文体、レビュー規則。
- `template/epub_pipeline/targets/{target}/`：対象言語の品質ルール。
- `template/epub_pipeline/profiles/{profile-target}/`：特殊な本の種類に対する追加ルール。
- `template/epub_pipeline/modes/private_use/`：非パブリックドメインの個人利用プロジェクトだけにコピーされる mode overlay です。private-use cover、frontmatter、artifact、gate scripts を含みます。
- `books/{target}/{number}_{book_slug}/`：実際の書籍プロジェクト。本固有の内容はここに置きます。
- `books/`：共有 Node.js ツール依存関係。一度だけインストールします。
- `doc/public/`：公開ガイド、prompt 説明、候補書籍資料。
- `research/{source-target}/`：言語方向ごとの調査成果物。
- `.opencode/` と `opencode.jsonc`：OpenCode 用の薄いアダプター。ワークフロー規則ではありません。
- `tools/lifebook-launcher/`：LifeBook Launcher デスクトップ入口です。開発ソースは `source/` にあります。

## 新しい本を作る

テンプレートを手でコピーせず、スクリプトを使います。

```powershell
cd books
npm run new:book -- {book_id_slug} --source-target {source-target}
```

新しい書籍ディレクトリ：

```text
books/{target}/{number}_{book_id_slug}/
```

スクリプトは `template/epub_pipeline/common` を先にコピーし、対応する言語方向テンプレートを重ねます。必要な場合は、その後 `profiles/{profile-target}/` を重ねます。private-use project では最後に `template/epub_pipeline/modes/private_use/` を重ねます。

private-use project は明示的に `private-use` モードで作成します。

```powershell
cd books
npm run new:book -- {book_id_slug} --source-target {source-target} --mode private-use --local-source-file "{path_to_local_ebook}" --private-use-declaration "個人学習用のみ。再配布なし。商用利用なし。"
```

private mode は翻訳、レビュー、EPUB 検証、層化ランダム抜き取り検査の品質基準を下げません。ただし権利境界、読者に見える文言、artifact の意味を変えます。private cover の下部は `个人学习版`、private frontmatter は `参考LifeBook书坊 个人自制` を使い、パブリックドメイン説明を削除し、個人利用のみ、再配布なし、商用利用なし、リスクは個人が負うことを明記します。private artifact は `output/private_artifacts/` に書き込み、公開 release ではありません。

## 基本ルール

- 翻訳前に出典証拠と権利確認を残す。公開プロジェクトにはパブリックドメインまたは許諾済みの出典が必要です。
- 非パブリックドメインの個人利用プロジェクトは `private_use` モードを使い、Git で無視される `books/private/` に置きます。
- private-use project は `modes/private_use` overlay を持ち、公開用 cover、frontmatter、release 文言を再利用してはいけません。
- 現代の著作権付き翻訳、海賊版サイト、出所不明の EPUB を使わない。
- AI 初稿をそのまま公開しない。
- 本固有の内容を `template/` に書かない。
- 人が読む重要なテンプレートファイルには、想定される貢献者が読めるローカル言語を含める。
- 最終納品前に EPUB 検証、読者に見える内容の検査、層化ランダム抜き取り検査、バージョン付き release を通す。

## 書籍ツール

共有依存関係は一度だけインストールします。

```powershell
cd books
npm install
```

その後、具体的な書籍プロジェクトで実行します。

```powershell
npm run build:epub
npm run check:epub
npm run review:random-samples
npm run review:random-validate:pass
npm run release:create
```

private-use project では、同じ build、EPUBCheck、層化ランダム抜き取り検査を通した後、private artifact command を使います。

```powershell
npm run build:private-epub
npm run check:epub
npm run review:random-samples
npm run review:random-validate:pass
npm run private:artifact:create
```

## 参加方法

出典調査、権利確認、翻訳レビュー、用語確認、EPUB テスト、レイアウトの読みやすさのフィードバック、自動化改善などが役立ちます。大きな追跡不能の書き換えより、小さく確認できる修正を優先します。

## 権利とライセンス

各原書は個別に権利確認が必要です。ある国でパブリックドメインでも、すべての地域で自動的にパブリックドメインとは限りません。

このプロジェクトで作られた翻訳、注記、表紙、組版、EPUB パッケージなどの非コードコンテンツは、別記がない限り `CC BY-NC-SA 4.0` で公開されます。第三者による商業利用には、LifeBook 書坊および関係する権利者からの別途許可が必要です。

`books/private/` 下の private-use project は公開コンテンツではなく、既定の公開ライセンスの対象ではなく、GitHub に commit または公開してはいけません。private translation は個人利用のみ、再配布なし、商用利用なしです。関連リスクは個人が負います。LifeBook書坊は LifeBook 翻訳發布系統だけを公開し、他の個人による非パブリックドメイン内容の翻訳、保存、配布、利用から生じる著作権リスクまたは責任を負いません。

参照：

- [LICENSE.ja.md](../license/LICENSE.ja.md)
- [CONTRIBUTING.ja.md](../license/CONTRIBUTING.ja.md)
- [COMMERCIAL_LICENSE.ja.md](../license/COMMERCIAL_LICENSE.ja.md)
