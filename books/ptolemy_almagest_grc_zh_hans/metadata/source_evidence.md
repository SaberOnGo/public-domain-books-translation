# 来源证据 / Source Evidence

source_evidence_status: `FACSIMILE_DOWNLOADED_HASHED`

## 候选主底本 / Candidate Base Text

- work: Ptolemy, `Mathematike Syntaxis` / `Almagest`
- Chinese working title: 《天文学大成》/《至大论》
- source language: Ancient Greek
- candidate edition: J. L. Heiberg Greek critical edition
- candidate URL: https://commons.wikimedia.org/wiki/File:Almagest_Complete,_Heiberg.pdf
- expected use: primary Ancient Greek base text after download, hash, page verification, OCR/transcription check, and Book I segmentation.

## 本地保存与哈希 / Local Preservation and Hashes

- local_path: `source/facsimile/Almagest_Complete_Heiberg_1898.pdf`
- downloaded_at_utc: `2026-05-16T15:18:01Z`
- bytes: `18277108`
- sha1: `e7c2a35f90202e8f23103e54a8fb3c90fd303b0b`
- sha256: `b5115c91265e7997236d54bb6e421eff6308ef3639681e4a6ab6bcfc37a1c32b`
- page_count_control: `589`
- page_count_method: PDF 内部页树最大 `/Count` 值为 `589`；直接扫描 `/Type /Page` 得到 `590`，包含页树噪声，因此不作为主控页数。
- hash_note: 当前本地文件来自 Wikimedia `Special:Redirect/file/Almagest_Complete%2C_Heiberg.pdf`。上一轮记录的 Wikimedia SHA1 与本地下载文件不一致，出版前必须复核 Wikimedia file history；本项目先以本地 SHA256 作为保存与复现控制值。

## 参考来源 / Reference Sources

- Internet Archive search for historical scans: https://archive.org/search?query=Almagest%20Heiberg
- Modern English reference witness: G. J. Toomer, `Ptolemy's Almagest`, Princeton University Press. Candidate publisher page: https://press.princeton.edu/books/paperback/9780691002606/ptolemys-almagest

## 当前状态 / Current Status

- PDF 已下载并本地哈希。
- 尚未生成 `source/source_text_raw.txt`。
- 尚未 OCR。
- Book I 已建立研究切分草案；尚未生成可作为正式底稿的 OCR/转写文本。
- 尚未进入正式翻译。

## 下一步要求 / Required Next Steps

1. 用 PDF 页图抽样复核 Book I 起止页、图表页和缺页状态。
2. 判断是否使用 OCR、人工转写或已有 Heiberg 转写文本。
3. 将 Book I 的图、表、证明段和弦表分别列入 QA 控制。
4. 只在 Book I 范围选择预翻译样本。
5. 在 `qa/pretranslation/pretranslation_report.md` 未 PASS 前禁止正式分章翻译。
