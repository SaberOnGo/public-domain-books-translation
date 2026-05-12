# LifeBook 書坊：パブリックドメイン書籍の翻訳と EPUB 制作プロジェクト

<table align="center">
  <tr>
    <td align="center"><h3><a href="./README.md">简体中文</a></h3></td>
    <td align="center"><h3><a href="./README.zh-TW.md">繁體中文</a></h3></td>
    <td align="center"><h3><a href="./README.en.md">English</a></h3></td>
    <td align="center"><h3><a href="./README.ja.md">日本語</a></h3></td>
  </tr>
</table>

LifeBook 書坊は、パブリックドメインの書籍を翻訳し、読みやすい EPUB として制作するための協作プロジェクトです。

目的は、AI が出した未確認の翻訳をそのまま公開することではありません。AI は、原文の取得、整形、章分け、下訳、用語表作成、漏れの確認、EPUB 作成などを助けられます。しかし、良い本にするには人間の判断が必要です。文章が自然か、名前や用語が統一されているか、歴史的な表現が適切か、読書アプリで読みやすいかを、人が確認する必要があります。

プログラミングができなくても参加できます。数ページ読んで「ここが分かりにくい」と伝えるだけでも役に立ちます。

## このプロジェクトがしたいこと

- Project Gutenberg、Wikisource、Standard Ebooks など、信頼できる公開元からパブリックドメイン書籍を選ぶ。
- 翻訳前に、出典と権利状態の証拠を残す。
- 現代出版社版、現代注釈版、出所不明のテキストを避ける。
- AI を「追跡可能な下訳と確認」のために使い、一回で出した文章をそのまま完成品にしない。
- 原文、下訳、最終稿、レビュー、用語表、EPUB 出力を、他の人が確認しやすい形で残す。
- 試読、校正、用語確認、資料調査、レイアウト確認、EPUB テストなど、小さな作業でも参加できるようにする。

大きな運動というより、小さな本づくりの場です。誰かが本を探し、誰かが出典を確認し、誰かが一章を読み、誰かが EPUB を試す。そうした小さな作業の積み重ねで、一冊の本はよくなります。

## いちばん簡単な始め方

多くの参加者は、フォルダを手でコピーしたり、metadata ファイルを自分で書いたりする必要はありません。AI にテンプレートフォルダ、パブリックドメインの URL、翻訳方向を渡します。AI が書籍プロジェクトを作成し、metadata を記入し、出典証拠を残し、翻訳パイプラインを実行し、EPUB を作成します。

通常、AI に伝えるのは次の三つです。

- 作りたい本。
- 分かっていれば、パブリックドメインの原文 URL。
- 翻訳方向。例：英語から中国語、中国語から英語、日本語から中国語。

プロンプト例：

```text
/goal D:\project\49_public-domain-books-translation\books\pg20923_a_negro_explorer_at_the_north_pole の工程を参考に、
『A Negro Explorer at the North Pole』の中国語 EPUB を制作してください。
https://www.gutenberg.org/ebooks/20923 から原文を取得してください。
template/epub_pipeline/common と template/epub_pipeline/en-zh-Hans を使い、00_orchestrator_zh_en.md から現在の完全な工程を実行してください：
出典と権利確認、書籍調査、試訳、章ごとの翻訳、章ごとのレビュー、章ゲート、
プリプロダクション段階 1、サンプル EPUB 確認、全書 EPUB 制作、独立レビュー、
修正ルート、最終出力、振り返り。
output/book.epub を生成し、epubcheck を通過させてください。
```

書名しか分からない場合は、先に AI に信頼できる公版ソースを探してもらえます。

```text
{書名} の信頼できるパブリックドメイン原文を探してください。
Project Gutenberg、Wikisource、Standard Ebooks を優先してください。
出典と権利リスクを確認したあと、template/epub_pipeline/common を先にコピーし、template/epub_pipeline/en-zh-Hans を上書きして books/ 以下に新しい書籍工程を作成してください。
```

## リポジトリ構成

### `template/epub_pipeline/`

書籍制作のための再利用テンプレート領域です。`common/` には共通の EPUB ワークフロー、権利確認、状態ファイル、スクリプト、制作ルールがあります。`en-zh-Hans/` には英語から簡体字中国語へのプロンプト、用語・文体ガイド、レビュー規則があります。新しい本を作るときは、AI に `common/` を `books/` 以下の新しいフォルダへコピーさせ、その上に該当する言語方向テンプレートを重ねます。

主な内容：

- `template/epub_pipeline/README.md`：テンプレート構成の説明。
- `template/epub_pipeline/common/PIPELINE_SPEC.md`：パイプラインとディレクトリ規約。
- `template/epub_pipeline/en-zh-Hans/README.md`：英語から簡体字中国語へのテンプレート説明。
- `template/epub_pipeline/en-zh-Hans/MASTER_PROMPT.md`：新しい本を始めるための主プロンプト。
- `prompts/`：原文取得からレビュー、EPUB 制作、振り返りまでの手順プロンプト。
- `metadata/`：書籍情報、権利確認、出典証拠、文体プロファイル。
- `chapters/`：原文、下訳、最終稿。
- `qa/`：忠実度、可読性、用語、イメージ語、章ゲートのレビュー。
- `preproduction/`：表紙、metadata、組版、サンプル EPUB 確認。
- `reviews/`：独立レビューと採点表。
- `output/`：最終 EPUB と検証結果。

### `books/`

実際の書籍プロジェクトを置くフォルダです。現在のサンプルは次の通りです。

```text
books/pg20923_a_negro_explorer_at_the_north_pole/
```

これは Project Gutenberg #20923、Matthew A. Henson の *A Negro Explorer at the North Pole* をもとにした工程です。出典証拠、権利メモ、26 章の原文、翻訳、最終稿、レビュー、生成済み EPUB、EPUBCheck 結果を含みます。EPUBCheck は fatal=0、error=0、warning=0 です。

このサンプルは工程が最後まで動くことを示しています。ただし、全章が人間の出版編集レベルで最終承認済みという意味ではありません。

### `translation_quality_framework/`

翻訳品質のためのフレームワークです。正式翻訳の前に何を調べ、どう試訳し、どうレビューし、どう差し戻すかを定義します。

### `doc/public/`

候補書籍、著作権の初期確認、出典調査などの公開メモを置く場所です。

## 参加できること

短時間でも参加できます。

- 数ページ読んで、読みにくい箇所を報告する。
- 原文の一段落と翻訳を比べる。
- 人名、地名、繰り返し出る用語を確認する。
- 誤字、句読点、重複を見つける。
- EPUB をスマホ、タブレット、電子書籍リーダーで開いて確認する。
- 候補書籍が本当にパブリックドメインか調べる。
- 表紙、metadata、レイアウト、EPUB 互換性を改善する。
- 章の文章が自然な中国語または自然な英語になっているか確認する。

簡単なフィードバック形式：

```text
書名：
章：
位置または文：
問題：
提案があれば：
```

## 人間が確認するとよいポイント

AI は多くの工程を自動で進められますが、次の段階では人間の確認が特に役立ちます。

- 書籍調査：`metadata/book_specific_translation_research.md`、`metadata/style_profile.md`、`glossary/terms.csv`。
- 試訳：`qa/pretranslation/pretranslation_report.md`。
- 章レビュー：`chapters/src/`、`chapters/translated/`、`chapters/final/`、`qa/chapter_controls/`、`qa/fidelity/`、`qa/readability/`、`qa/terminology/`、`qa/imagery/`、`qa/gates/`。
- プリプロダクション段階 1：`preproduction/stage1/production_spec.md`。
- プリプロダクション段階 2：`preproduction/stage2_sample/sample_book.epub` と `sample_review.md`。
- 最終出力：`output/book.epub`、`output/epubcheck.json`、`reviews/`。

## 翻訳方向

最初のサンプルは英語から中国語ですが、今後は他の方向にも広げられます。

- 英語の公版書を中国語へ。
- その他の外国語の公版書を中国語へ。
- 中国語の公版書を英語へ。
- 中国語の公版書をその他の言語へ。

どの方向でも、原則は同じです。権利を確認し、出典を記録し、翻訳前に調査し、まず試訳し、章ごとにレビューし、最後に EPUB を検証します。

## 大切にしているルール

- 現代の著作権保護された翻訳を翻訳元として使わない。
- 海賊版サイトや出所不明の EPUB を使わない。
- AI の初稿を完成品として扱わない。
- テンプレートフォルダに実際の本のデータを書き込まない。
- レビュー記録と失敗記録を残す。
- 追跡できない全体書き換えより、小さく確認できる改善を優先する。

## 権利とライセンスについて

各原書は個別に権利確認が必要です。ある国で公版でも、すべての地域で自動的に公版とは限りません。

Project Gutenberg のテキストは、多くの場合「米国で公版」とされています。別の地域で公開する場合は、その地域の著作権状態を改めて確認してください。

このプロジェクトで作られた翻訳、注記、表紙、組版、EPUB パッケージ、その他の非コードコンテンツは、既定では `CC BY-NC-SA 4.0` で一般公開されます。第三者による商業利用には、LifeBook 書坊および関係する権利者からの別途許可が必要です。

貢献を提出することで、貢献者は、その貢献が本プロジェクトに取り込まれて公開され、LifeBook 書坊により LifeBook products and services に利用されることに同意したものとします。LifeBook 書坊は、プロジェクトの組織、公開、品質管理、ライセンス管理、貢献者への還元に関する取り決めを担当します。具体的な表示と還元方法は、貢献状況とプロジェクトルールに従って決定されます。

詳しくは次を参照してください。

- [LICENSE.md](LICENSE.md)：公開コンテンツライセンスとコードライセンス。
- [CONTRIBUTING.md](CONTRIBUTING.md)：貢献者の利用許諾と参加ルール。
- [COMMERCIAL_LICENSE.md](COMMERCIAL_LICENSE.md)：第三者による商業利用の説明。

## 小さな参加を歓迎します

本が好きで、見過ごされがちな公版作品をもっと読まれる形にしたいと思うなら、小さく始められます。一章を読む。一文を指摘する。名前を一つ確認する。EPUB を一度開く。そうした小さな注意が、本をよくしていきます。
