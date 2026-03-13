from __future__ import annotations

"""Account stage engine (rule-based state machine, phase-1)."""

from app.decision.snapshot.feature_store import SnapshotFeatureStore
from app.decision.snapshot.schemas import UserGrowthSnapshot
from app.schemas.decision import AccountStageSummary


class AccountStageEngine:
    def run(self, snapshot: UserGrowthSnapshot) -> AccountStageSummary:
        fs = SnapshotFeatureStore(snapshot)
        score = 0
        evidence: list[str] = []

        if snapshot.active_positioning.has_active:
            score += 20
            evidence.append("已有 active positioning")
        if snapshot.active_positioning.has_frozen:
            score += 20
            evidence.append("已有 frozen positioning")
        if fs.benchmark_pool_size >= 3:
            score += 15
            evidence.append("对标池样本达到最小规模")
        if fs.validated_pattern_count >= 2:
            score += 20
            evidence.append("已有可复用 validated patterns")
        if fs.total_inquiries > 0:
            score += 15
            evidence.append("已有咨询行为数据")
        if len(snapshot.recent_reviews) >= 2:
            score += 10
            evidence.append("复盘样本已形成连续性")

        if score < 25:
            stage = "冷启动"
            reason = "关键输入不足，先建立定位与首批可复盘内容。"
            milestone = "完成定位并发布首条可复盘内容"
        elif score < 50:
            stage = "有方向但不稳"
            reason = "已有方向，但承接链路与复盘闭环还不稳定。"
            milestone = "建立 3-5 个对标账号并固定承接动作"
        elif score < 75:
            stage = "正在贴近可承接咨询的结构"
            reason = "关键结构正在成型，需要连续验证。"
            milestone = "连续两周保持咨询承接动作有效"
        else:
            stage = "已形成主打法"
            reason = "定位、承接、复盘和模式资产已形成正反馈。"
            milestone = "扩大有效支柱并固化周节奏"

        return AccountStageSummary(
            stage=stage,
            confidence=min(95, max(55, score)),
            reason=reason,
            evidence=evidence or ["系统默认冷启动证据"],
            next_expected_milestone=milestone,
        )


account_stage_engine = AccountStageEngine()
