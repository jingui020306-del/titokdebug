# creator-os

单账号咨询型 IP 的账号改造工作台（mock intelligence + real architecture）。

## Unified Decision Engine（Phase-1）
后台新增 `backend/app/decision/` 统一决策层，关键判断统一由 orchestrator 产出：
1. 我的账号现在处于什么阶段
2. 当前最该学的强账号是谁
3. 当前最大差距在哪
4. 下一条最该发什么
5. 本周改造重点是什么
6. 今天先做什么

> 权威入口：`app.decision.engines.orchestrator.decision_orchestrator`。
> 旧 `backend/app/engines/*` 已移除，不再作为业务判断入口。

## 决策层结构
- `decision/snapshot`: `UserGrowthSnapshot` 归一化快照
- `decision/retrieval`: embedding/faiss 召回接口（可选依赖）
- `decision/ranking`: benchmark/gap/next-post 排序接口（可选模型）
- `decision/bandit`: VW 接口与 reward logger（可降级）
- `decision/topics`: taxonomy + BERTopic 接口（可降级）
- `decision/engines`: 6 个核心引擎 + orchestrator
- `decision/explain`: LLM explain hook（仅解释，不做裁判）

## Optional 算法依赖
基础运行只需 `backend/requirements.txt`。
可选算法栈在 `backend/requirements-optional-algo.txt`：
- sentence-transformers
- faiss-cpu
- lightgbm
- vowpalwabbit
- bertopic

缺失时系统自动回退到规则版，不阻塞 API 启动。

## 仍是 mock 的部分
- 引擎当前以规则 + 检索/排序/bandit/topic 的可替换骨架为主。
- 未接真实 LLM 生产调用。
- 抖音仅官方 OAuth 架构占位。

## 六个引擎当前运行模式（如实）
- account_stage_engine：规则状态机
- benchmark_selection_engine：检索 + 排序接口，当前规则 fallback 主导
- gap_priority_engine：排序接口已接，当前规则评分主导
- next_post_engine：候选生成 + 排序 + bandit hook，未启用正式在线学习
- review_decision_engine：规则 + 指标对比
- workflow_recommendation_engine：规则状态机
