# TODO_REAL_INTEGRATIONS

## 决策层模型化升级
当前为规则版 + 可替换骨架，后续可升级为：
1. 检索：接入稳定 embedding 服务和持久化 FAISS 索引
2. 排序：上线 LightGBM/XGBoost artifact 与离线特征校准
3. Bandit：接入 VW 在线策略与真实 reward 回传
4. Topics：BERTopic 训练与主题漂移监控
5. Explain：接入真实 LLM 解释器（仍保持“LLM 只解释不裁判”）

## 当前运行模式（避免误解）
- account_stage_engine：规则状态机（非模型）
- benchmark_selection_engine：检索+排序接口已接，规则 fallback 主导
- gap_priority_engine：排序接口已接，规则评分主导
- next_post_engine：候选生成+排序+bandit hook，尚未在线学习
- review_decision_engine：规则+指标对比
- workflow_recommendation_engine：规则状态机

## 可选算法依赖
见 `backend/requirements-optional-algo.txt`。
若缺失，系统自动降级规则版，不影响 API 可用性。

降级统一目标：
- import 不失败
- orchestrator 始终可产出 decision bundle
- summary API 始终返回可消费结构

## 抖音接入
仅官方 OAuth 架构占位，真实 token exchange/refresh 仍为 TODO。
