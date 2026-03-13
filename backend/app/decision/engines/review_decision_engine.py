from __future__ import annotations

"""Review decision engine (rule + basic metric comparison, phase-1)."""

from app.decision.snapshot.schemas import UserGrowthSnapshot
from app.schemas.decision import ReviewDecisionSummary


class ReviewDecisionEngine:
    def run(self, snapshot: UserGrowthSnapshot) -> ReviewDecisionSummary:
        pubs = snapshot.publish_records[-5:]
        if not pubs:
            return ReviewDecisionSummary(
                bottleneck_stage="暂无发布样本",
                problem_level="切口问题",
                recommended_action="继续测试",
                benchmark_learning_status="未开始学习",
                what_worked=["暂无"],
                what_failed=["缺少发布样本"],
                next_iteration_actions=["先发布一条可复盘内容"],
                should_scale_or_stop="继续测试",
                why="无可用发布样本，先建立最小复盘闭环。",
            )

        views = sum(x.views for x in pubs)
        inquiries = sum(x.inquiry_count for x in pubs)
        conversions = sum(x.conversion_count for x in pubs)

        if views > 0 and inquiries == 0:
            problem_level = "表达问题"
            action = "回内容执行"
            status = "正在模仿"
            bottleneck = "兴趣到咨询断层"
        elif inquiries > 0 and conversions == 0:
            problem_level = "题型问题"
            action = "改题型"
            status = "已初步贴近"
            bottleneck = "咨询到成单断层"
        elif conversions > 0:
            problem_level = "支柱问题"
            action = "放大"
            status = "已形成自己的版本"
            bottleneck = "主链路有效"
        else:
            problem_level = "切口问题"
            action = "继续测试"
            status = "正在模仿"
            bottleneck = "稳定性不足"

        return ReviewDecisionSummary(
            bottleneck_stage=bottleneck,
            problem_level=problem_level,
            recommended_action=action,
            benchmark_learning_status=status,
            what_worked=["案例型内容更易触发咨询动作"],
            what_failed=["评论区承接动作波动"],
            next_iteration_actions=["固定结尾 CTA", "评论区置顶咨询触发句", "同题型再测一条"],
            should_scale_or_stop="放大" if action == "放大" else "继续优化",
            why="基于 views/互动/咨询/转化综合判断。",
        )


review_decision_engine = ReviewDecisionEngine()
