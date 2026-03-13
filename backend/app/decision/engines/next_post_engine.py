from __future__ import annotations

"""Next post engine (candidate+ranking with bandit hook; online learning not enabled)."""

from app.decision.bandit.next_post_bandit import next_post_bandit
from app.decision.ranking.next_post_ranker import next_post_ranker
from app.decision.snapshot.schemas import UserGrowthSnapshot
from app.schemas.decision import GapSummary, LearningTargetSummary, NextPostRecommendation


class NextPostEngine:
    def _candidates(self, top_gap: str) -> list[dict[str, str]]:
        return [
            {
                "topic": "高频问题 + 真实案例 + 明确承接动作",
                "pillar": "案例拆解",
                "content_type": "咨询承接型",
                "goal": "咨询",
                "hook": "先抛高频问题，再给案例反转",
                "conversion": "结尾明确咨询入口 + 评论区触发问题",
            },
            {
                "topic": "评论区高频问题拆解",
                "pillar": "咨询策略",
                "content_type": "痛点型",
                "goal": "承接",
                "hook": "先展示错误做法",
                "conversion": "引导私信关键词",
            },
            {
                "topic": "常见误区纠偏 + 可执行动作",
                "pillar": "表达优化",
                "content_type": "避坑型",
                "goal": "咨询",
                "hook": "反常识开头",
                "conversion": "评论区领取清单",
            },
        ]

    def run(self, snapshot: UserGrowthSnapshot, gap_summary: GapSummary, learning_target: LearningTargetSummary) -> NextPostRecommendation:
        candidates = self._candidates(gap_summary.current_top_gap)
        scored = [(c, next_post_ranker.score(c, snapshot, gap_summary.current_top_gap)) for c in candidates]
        chosen = next_post_bandit.choose(scored)

        return NextPostRecommendation(
            recommended_topic=chosen.get("topic", candidates[0]["topic"]),
            recommended_pillar=chosen.get("pillar", "咨询策略"),
            recommended_content_type=chosen.get("content_type", "咨询承接型"),
            recommended_goal=chosen.get("goal", "咨询"),
            recommended_hook_direction=chosen.get("hook", "先抛问题"),
            recommended_conversion_direction=chosen.get("conversion", "明确咨询入口"),
            why_this_now=f"当前 top gap={gap_summary.current_top_gap}，先用一条承接型内容做最小验证。",
            benchmark_reference_ids=[x.id for x in snapshot.benchmark_accounts[:2]],
            do_not_do="不要泛科普、不要无承接动作、不要只讲观点不放案例。",
            alternative_options=[x["topic"] for x in candidates[1:]],
        )


next_post_engine = NextPostEngine()
