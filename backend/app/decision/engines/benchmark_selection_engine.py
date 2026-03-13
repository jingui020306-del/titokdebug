from __future__ import annotations

"""Benchmark selection engine (retrieval + ranking interface, rule-fallback dominant)."""

from app.decision.ranking.benchmark_ranker import benchmark_ranker
from app.decision.retrieval.benchmark_retriever import benchmark_retriever
from app.decision.snapshot.schemas import UserGrowthSnapshot
from app.schemas.decision import LearningTargetSummary


class BenchmarkSelectionEngine:
    def run(self, snapshot: UserGrowthSnapshot, top_gap: str) -> LearningTargetSummary:
        if not snapshot.benchmark_accounts:
            return LearningTargetSummary(
                selected_benchmark_account="暂无",
                learning_target_dimension="先建立对标池",
                why_this_account_now="当前无可学习账号，先补 3-5 个正式对标对象。",
                why_not_others="对标池为空，无法进行召回与排序。",
                what_to_learn="优先补充案例拆解+评论区承接稳定样本。",
                what_not_to_copy="不要盲选最火账号，先看可学性与阶段匹配。",
                confidence=40,
                evidence=["benchmark_pool_size=0"],
            )

        query = f"top_gap={top_gap};goal={snapshot.account_goal};stage={snapshot.current_stage_hint or ''}"
        recalled = benchmark_retriever.retrieve(snapshot.benchmark_accounts, query, top_k=5)
        ranked = sorted(recalled, key=lambda a: benchmark_ranker.score(a, snapshot), reverse=True)
        top = ranked[0]

        return LearningTargetSummary(
            selected_benchmark_account=top.account_name,
            learning_target_dimension="咨询承接结构" if top_gap in {"主页承接", "咨询承接方式"} else "题型与钩子结构",
            why_this_account_now="当前最大缺口与该账号优势能力高度重叠，学习收益最高。",
            why_not_others="其余账号要么样本覆盖不足，要么阶段匹配度更低。",
            what_to_learn="结尾承接动作、评论区触发问题、案例切入顺序。",
            what_not_to_copy="不要复制夸张语气和高频产出强度，只学结构。",
            confidence=78,
            evidence=[f"recalled={len(recalled)}", f"top_gap={top_gap}", f"tier={top.account_tier}"],
        )


benchmark_selection_engine = BenchmarkSelectionEngine()
