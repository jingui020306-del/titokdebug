from __future__ import annotations

"""Gap priority engine (ranking interface attached, currently rule scoring dominant)."""

from app.decision.ranking.gap_ranker import gap_ranker
from app.decision.snapshot.schemas import UserGrowthSnapshot
from app.schemas.decision import GapItem, GapSummary


DIMENSIONS = [
    "定位表达",
    "主页承接",
    "内容支柱结构",
    "题型分布",
    "钩子方式",
    "叙述方式",
    "咨询承接方式",
    "发布节奏",
]


class GapPriorityEngine:
    def run(self, snapshot: UserGrowthSnapshot) -> GapSummary:
        items: list[GapItem] = []
        for d in DIMENSIONS:
            gap_score = int(min(100, max(1, gap_ranker.score(d, snapshot) * 35)))
            my_score = max(20, 80 - gap_score)
            bm_score = 78
            urgency = "now" if gap_score >= 22 else "this_week" if gap_score >= 14 else "later"
            impact = "高" if d in {"主页承接", "咨询承接方式", "定位表达"} else "中"
            effort = "medium" if d in {"主页承接", "咨询承接方式"} else "low"
            items.append(
                GapItem(
                    dimension=d,
                    my_score=my_score,
                    benchmark_score=bm_score,
                    gap_score=gap_score,
                    urgency=urgency,
                    expected_impact=impact,
                    effort_level=effort,
                    why_gap_exists="最近复盘样本显示该维度动作不稳定。",
                    first_fix_action=f"先在{d}上执行一条可复用标准动作",
                )
            )

        top = sorted(items, key=lambda x: x.gap_score, reverse=True)[0]
        return GapSummary(
            gap_items=items,
            current_top_gap=top.dimension,
            why_it_is_top_priority=f"{top.dimension} gap_score={top.gap_score}，对咨询转化链路影响最大。",
            what_happens_if_not_fixed="会持续出现有播放但无咨询的低效循环。",
            what_to_fix_first=top.first_fix_action,
        )


gap_priority_engine = GapPriorityEngine()
