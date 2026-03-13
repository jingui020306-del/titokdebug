# ARCHITECTURE

## Decision Layer（backend/app/decision）

统一权威约束：
- 决策判断唯一权威层是 `backend/app/decision/engines/*`。
- 前台 summary（home/workspace/my-account/learn-from/upgrade-plan/execute/review）必须来自 orchestrator bundle。
- 旧 `backend/app/engines/*` 已移除，避免新旧双引擎并行。

### 1) Snapshot
`snapshot_builder` 统一构建 `UserGrowthSnapshot`，供所有引擎共享输入，避免每个引擎重复查库。

### 2) Retrieval + Ranking + Bandit + Topics（Phase-1 插入）
- Retrieval：embedding/faiss 召回接口（依赖缺失自动降级）
- Ranking：benchmark/gap/next-post ranker（模型文件缺失自动规则分）
- Bandit：VW hook + reward logger（VW 不可用则直接采用 ranker top）
- Topics：taxonomy + BERTopic 接口（bertopic 不可用则规则标签）

### 3) Engines
- account_stage：规则状态机
- benchmark_selection：检索+排序接口，规则 fallback 主导
- gap_priority：排序接口已接，规则评分主导
- next_post：候选生成+排序+bandit hook（未在线学习）
- review_decision：规则+指标对比
- workflow_recommendation：规则状态机

### 4) Orchestrator
`decision/engines/orchestrator.py` 是前台 summary 的统一入口：
- build snapshot
- run six engines
- produce `FrontstageDecisionBundle`

这样可保证首页和 workspace 不会“各说各话”。
