# English Revision Prompt / 英文返修 Prompt

Read the exact issue evidence and current source-target unit plus neighboring context. Repair the canonical target through a chapter patch. Explain the source-supported reason in QA. Search cheap candidates for the same mechanism throughout the book, confirm matches against source, record exceptions, and close the family. A repair round is FIXED_RECHECK_REQUIRED; independent full-chapter recheck is required before PASS.

只通过 canonical patch 修复；以原文支持判断，用低 token 检索追查同族，保存失败与修复证据，不得手改投影或提高评分绕过门禁。
