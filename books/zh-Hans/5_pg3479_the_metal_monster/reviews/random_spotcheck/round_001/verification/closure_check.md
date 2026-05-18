# 抽检闭环验证 / Spot-Check Closure Verification

status: "DRAFT" # PASS | FAIL
open_p0_p1_p2_count: 0
new_seed_required_after_fix: true

## Required Checks

- [ ] 所有已发现 P0/P1/P2 均已定点复查关闭。
- [ ] 修复后的文件重新通过 lint/build/EPUBCheck 中相关检查。
- [ ] 若发生返工，下一轮使用新 seed 重新抽样。
- [ ] 人工可在本轮目录下查看样本、证据、评审、修复和闭环记录。