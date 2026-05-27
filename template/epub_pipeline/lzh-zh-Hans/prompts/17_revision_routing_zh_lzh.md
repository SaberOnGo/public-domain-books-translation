# 17 返工路由 / Revision Routing

## 任务

根据章节 gate、样章、EPUB 校验、随机抽检和独立评审结果，将问题路由回正确阶段：

- 底本或断句问题：回到 `01`、`02` 或文本疑难记录。
- 人物、地名、制度背景问题：回到本书研究、术语表或历史 profile。
- 今译误解：回到章节翻译和忠实度审校。
- 注释缺失或过度：回到注释策略和术语审校。
- EPUB 呈现问题：回到预制作或构建脚本。

## 输出

- `qa/revision_routing.md`
- 对应 fix log
- 必要时更新 `state/pipeline_state.json`

返工后必须重建 EPUB，并使用新 seed 复抽。
