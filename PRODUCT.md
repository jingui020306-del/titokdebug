# PRODUCT

## 核心定位
creator-os 是“单账号咨询型 IP 的对标改造工作台”。

## 本次升级
已把关键判断收口到 Unified Decision Engine：
- 首页/workspace/my-account/learn-from/upgrade-plan/execute/review 共用同一决策脑。
- 前台主要做展示，不再各自拼关键判断。

## 六个核心引擎职责
1. account_stage_engine：阶段判断
2. benchmark_selection_engine：最该学账号选择
3. gap_priority_engine：top gap 选择
4. next_post_engine：下一条作战命令
5. review_decision_engine：复盘后动作决策
6. workflow_recommendation_engine：今天先做什么

## 当前边界
- 保持 mock intelligence + real architecture
- 不接真实 LLM
- 不做非官方登录抓取
