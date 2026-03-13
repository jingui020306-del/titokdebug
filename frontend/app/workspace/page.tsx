"use client";

import {
  BenchmarkAccountCard,
  FrozenPositioningCard,
  FrontstageCardSkeleton,
  GapSummaryCard,
  NextPostCard,
  NextStepCTA,
  PatternAssetPreviewCard,
  PendingContentCard,
  PendingReviewCard,
  UpgradeActionCard,
  WeeklyFocusCard
} from "@/components/frontstage-cards";
import { PageHeader } from "@/components/ui/page-header";
import { createSeedAllDemo, getWorkspaceSummary, type WorkspaceSummary } from "@/lib/api";
import Link from "next/link";
import { useCallback, useEffect, useState } from "react";

const DEMO_WORKSPACE_SUMMARY: WorkspaceSummary = {
  latest_positioning_summary: "当前定位清晰，但主页承接表达偏弱。",
  active_content_plan_summary: "本周计划 7 条，先执行 3 条咨询承接内容。",
  latest_review_summary: "最近一条内容有流量，但咨询转化偏低。",
  current_best_next_step: "先发一条案例型咨询承接内容",
  current_workflow_stage: "执行改造中（有方向但结果不稳）",
  best_next_action: "今天先做：发布 1 条“问题 + 案例 + 承接”内容",
  best_next_action_reason: "当前最缺的是验证承接动作是否有效，而不是新增选题池。",
  pending_content_items: 4,
  unpublished_adopted_items: 2,
  unreviewed_published_items: 1,
  recent_7d_consultation_content_count: 3,
  recent_7d_total_inquiries: 12,
  top_consultation_pillar: "案例拆解",
  active_frozen_positioning: "帮助咨询型创作者把内容变成稳定咨询入口",
  benchmark_pool_size: 5,
  strongest_accounts_to_learn: ["高承接案例型账号", "稳咨询叙事型账号"],
  current_main_gap: "主页承接路径断层，用户看完内容后不知道下一步怎么找你",
  current_upgrade_focus: "统一主页 headline、结尾 CTA、评论区引导",
  next_post_recommendation: {
    recommended_topic: "高频问题拆解：为什么你有播放却没有咨询？",
    do_not_do: "不要泛讲道理，不要缺少具体承接动作",
    recommended_content_type: "案例拆解型",
    recommended_goal: "咨询",
    recommended_hook_direction: "先抛高频问题，再给真实案例反转"
  },
  why_next_post_now: "先修复承接链路，再放大流量型选题。",
  current_learning_target: "学“案例拆解 + 评论区承接”模式",
  upgrade_plan_progress: "改造进度：2/5 关键动作已完成",
  todo_list: [
    { id: "d1", user_id: "demo", title: "统一主页简介与置顶引导", source_module: "positioning", source_report_id: null, priority: "high", status: "todo", action_type: "rewrite_profile", suggested_due_label: "今天", created_at: new Date().toISOString(), updated_at: new Date().toISOString() },
    { id: "d2", user_id: "demo", title: "发布 1 条案例型咨询承接内容", source_module: "content_studio", source_report_id: null, priority: "high", status: "todo", action_type: "rewrite_single_post", suggested_due_label: "今天", created_at: new Date().toISOString(), updated_at: new Date().toISOString() }
  ],
  learned_patterns_preview: [],
  stopped_directions_preview: [],
  best_to_scale_pattern: { id: "p1", user_id: "demo", pattern_type: "hook_style", label: "问题开场 + 案例反转", summary: "前 3 秒抛问题，随后用真实案例反转。", evidence_source: "最近 3 条复盘", confidence: 0.78, current_status: "validated", created_at: new Date().toISOString(), updated_at: new Date().toISOString() },
  workflow_recommendation: { current_workflow_stage: "执行改造中", best_next_action: "先发一条承接内容", best_next_action_reason: "先验证承接链路" }
};

export default function WorkspacePage() {
  const [summary, setSummary] = useState<WorkspaceSummary | null>(null);
  const [useDemo, setUseDemo] = useState(false);

  const reload = useCallback(async () => {
    try {
      setSummary(await getWorkspaceSummary());
      setUseDemo(false);
    } catch {
      setSummary(DEMO_WORKSPACE_SUMMARY);
      setUseDemo(true);
    }
  }, []);

  useEffect(() => {
    void reload();
  }, [reload]);

  const current = summary ?? DEMO_WORKSPACE_SUMMARY;
  const cards = current.decision_cards ?? {};

  return (
    <main className="grid-shell min-h-screen">
      <div className="mx-auto w-full max-w-7xl px-6 py-8 md:px-10 md:py-9">
        <PageHeader eyebrow="workspace / 执行主操作台" title="今天先做什么，直接执行" description="这里不是说明页，而是今日作战台：先做哪一步、为什么先做、做完看什么结果。" />

        <section className="mt-4 rounded-2xl border border-accent/45 bg-panel/95 px-4 py-3">
          <div className="flex flex-wrap items-center justify-between gap-2">
            <p className="text-sm">当前工作阶段：<span className="font-medium">{current.current_workflow_stage}</span></p>
            {useDemo ? <p className="rounded border border-line px-2 py-1 text-[11px] text-subInk">当前为演示数据（后端未连接）</p> : null}
          </div>
          <p className="mt-1 text-sm text-subInk">今日最佳下一步：{current.best_next_action}</p>
          <p className="mt-1 text-sm text-subInk">依据：{current.best_next_action_reason}</p>
          <div className="mt-3 flex flex-wrap gap-2">
            <button onClick={() => void createSeedAllDemo().then(reload)} className="rounded border border-line px-3 py-1.5 text-xs text-subInk">刷新演示数据</button>
            <Link href="/execute" className="rounded border border-accent px-3 py-1.5 text-xs">立即执行这一条</Link>
          </div>
        </section>

        <section className="mt-4 grid gap-4 md:grid-cols-6">
          {!summary ? (
            <>
              <FrontstageCardSkeleton /><FrontstageCardSkeleton /><FrontstageCardSkeleton /><FrontstageCardSkeleton />
            </>
          ) : (
            <>
              <div className="md:col-span-3">
                <NextPostCard
                  title="下一条最该发什么（主决策）"
                  conclusion={current.next_post_recommendation.recommended_topic ?? "先发一条咨询承接内容"}
                  reason={cards.next_post?.reason ?? `目标：${(current.next_post_recommendation as Record<string, string>).recommended_goal ?? "咨询"}；题型：${(current.next_post_recommendation as Record<string, string>).recommended_content_type ?? "案例拆解型"}；钩子：${(current.next_post_recommendation as Record<string, string>).recommended_hook_direction ?? "问题开场"}。`}
                  riskNote={cards.next_post?.risk_note ?? current.next_post_recommendation.do_not_do ?? "不要做无承接动作的泛内容。"}
                  actionLabel="去执行这一条"
                  actionHref="/execute"
                  emphasis="strong"
                />
              </div>
              <div className="md:col-span-3">
                <NextStepCTA
                  title="今日最佳下一步（主决策）"
                  conclusion={current.best_next_action}
                  reason={cards.next_step?.reason ?? current.best_next_action_reason}
                  riskNote={cards.next_step?.risk_note ?? "不要先开新方向；今天先完成这一条并记录复盘。"}
                  primary={{ label: "立即执行", href: "/execute" }}
                  secondary={{ label: "去看改造原因", href: "/upgrade-plan" }}
                />
              </div>
              <FrozenPositioningCard
                title="当前冻结定位"
                conclusion={current.active_frozen_positioning}
                reason="定位已冻结，内容执行先围绕同一承接目标推进。"
                actionLabel="去确认定位"
                actionHref="/my-account"
              />
              <BenchmarkAccountCard
                title="当前最该学的强账号"
                conclusion={current.strongest_accounts_to_learn.join(" / ") || "先建立对标池"}
                reason={cards.learning_target?.reason ?? "优先学其评论区承接结构与结尾动作，不要盲抄夸张表达。"}
                riskNote={cards.learning_target?.risk_note ?? "不要追“像”，先追“能学会且能复用”的承接模式。"}
                actionLabel="去拆这 3 条"
                actionHref="/learn-from"
              />
              <GapSummaryCard
                title="当前最大差距"
                conclusion={current.current_main_gap}
                reason={cards.gap_summary?.reason ?? "若不先补承接链路，后续内容会继续高播放低咨询。"}
                actionLabel="去补承接动作"
                actionHref="/upgrade-plan"
              />
              <WeeklyFocusCard
                title="本周改造重点"
                conclusion={current.current_upgrade_focus}
                reason={cards.weekly_focus?.reason ?? "本周仅做能直接影响咨询转化的动作，不再分散尝试。"}
                actionLabel="去执行本周三件事"
                actionHref="/workspace"
              />
            </>
          )}
        </section>

        <section className="mt-4 grid gap-4 md:grid-cols-3">
          <UpgradeActionCard
            title="本周待办动作"
            conclusion={`待处理 ${current.todo_list.length} 项，先做最高优先级 2 项`}
            reason={current.todo_list.slice(0, 2).map((x) => x.title).join("；") || "暂无待办"}
            actionLabel="去执行待办"
            actionHref="/workspace"
          />
          <PendingContentCard
            title="待发布内容"
            conclusion={`已采用未发布：${current.unpublished_adopted_items}`}
            reason={`当前待处理内容对象：${current.pending_content_items}`}
            actionLabel="去发布这条"
            actionHref="/execute"
          />
          <PendingReviewCard
            title="待复盘内容"
            conclusion={`已发布未复盘：${current.unreviewed_published_items}`}
            reason={`最近 7 天总咨询：${current.recent_7d_total_inquiries}`}
            actionLabel="去补复盘"
            actionHref="/review"
          />
        </section>

        <section className="mt-4 grid gap-4 md:grid-cols-2">
          <PatternAssetPreviewCard
            title="最近验证有效的模式"
            conclusion={current.best_to_scale_pattern?.label ?? "暂无明确可放大模式"}
            reason={current.best_to_scale_pattern?.summary ?? "先补 2~3 条复盘样本再判断放大。"}
            actionLabel="去看可复用模式"
            actionHref="/review-lab/benchmarks"
          />
          <WeeklyFocusCard
            title="当前最值得放大的支柱/题型"
            conclusion={current.top_consultation_pillar}
            reason={current.current_upgrade_focus}
            actionLabel="去放大这个支柱"
            actionHref="/execute"
          />
        </section>
      </div>
    </main>
  );
}
