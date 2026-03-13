"use client";

import Link from "next/link";
import { useEffect, useState } from "react";

import {
  AccountStageCard,
  FrontstageCardSkeleton,
  GapSummaryCard,
  LearningTargetCard,
  NextPostCard,
  NextStepCTA,
  WeeklyFocusCard
} from "@/components/frontstage-cards";
import { getHomeSummary, type HomeSummary } from "@/lib/api";

const DEMO_HOME_SUMMARY: HomeSummary = {
  account_stage: "有方向但不稳：正在把“泛表达”收敛到“可承接咨询”结构",
  learning_target: "优先学习：同赛道“案例拆解 + 评论区承接”稳定的中腰部咨询账号",
  main_gap: "主页承接断层：看完内容后，用户不知道下一步该找你做什么",
  next_post: {
    recommended_topic: "先发：高频问题 + 真实案例 + 明确承接动作",
    why_this_now: "当前最缺的不是选题，而是把兴趣转成咨询的第一条验证内容",
    recommended_content_type: "案例拆解型",
    recommended_goal: "咨询",
    recommended_hook_direction: "先抛高频问题，再给反直觉案例"
  },
  weekly_focus: "本周唯一重点：统一主页承接 + 补 3 条咨询承接内容",
  best_next_action: "今天先去执行“下一条咨询承接内容”",
  best_next_action_reason: "最近 3 条内容有兴趣但承接弱，先补承接链路才能降低不确定性。",
  douyin_status: "开发模式（OAuth 未配置，仍可完整体验流程）",
  last_review_time: "2 天前"
};

export default function HomePage() {
  const [summary, setSummary] = useState<HomeSummary | null>(null);
  const [useDemo, setUseDemo] = useState(false);

  useEffect(() => {
    const run = async () => {
      try {
        const live = await getHomeSummary();
        setSummary(live);
        setUseDemo(false);
      } catch {
        setSummary(DEMO_HOME_SUMMARY);
        setUseDemo(true);
      }
    };
    void run();
  }, []);

  const current = summary ?? DEMO_HOME_SUMMARY;
  const cards = current.decision_cards ?? {};

  return (
    <main className="grid-shell min-h-screen">
      <div className="mx-auto w-full max-w-7xl px-6 py-8 md:px-10 md:py-9">
        <section className="rounded-2xl border border-line bg-panel/90 px-4 py-3 text-xs text-subInk md:flex md:items-center md:justify-between">
          <p>抖音连接：{current.douyin_status}</p>
          <p>当前账号阶段：{current.account_stage}</p>
          <p>最近复盘：{current.last_review_time}</p>
        </section>

        <header className="mt-4 rounded-2xl border border-accent/45 bg-panel/95 p-5 md:p-6">
          <div className="flex flex-wrap items-center justify-between gap-2">
            <p className="text-xs uppercase tracking-[0.2em] text-subInk">creator-os / 我的账号改造工作台</p>
            {useDemo ? <p className="rounded border border-line px-2 py-1 text-[11px] text-subInk">当前为演示数据（后端未连接）</p> : null}
          </div>
          <h1 className="mt-2 text-2xl font-semibold md:text-3xl">先看我的账号，再学强账号，最后决定下一条怎么发。</h1>
          <div className="mt-4 flex flex-wrap gap-3 text-sm">
            <Link href="/workspace" className="rounded border border-accent px-4 py-2">去执行今天这一步</Link>
            <Link href="/upgrade-plan" className="rounded border border-line px-4 py-2">去看改造方案</Link>
          </div>
        </header>

        <section className="mt-4 grid gap-4 md:grid-cols-6">
          {!summary ? (
            <>
              <FrontstageCardSkeleton /><FrontstageCardSkeleton /><FrontstageCardSkeleton /><FrontstageCardSkeleton /><FrontstageCardSkeleton />
            </>
          ) : (
            <>
              <div className="md:col-span-2">
                <GapSummaryCard
                  title="当前最大差距（主决策）"
                  conclusion={current.main_gap}
                  reason={cards.gap_summary?.reason ?? "你现在不是缺流量，而是缺“内容到咨询”的承接闭环；不先改会持续高播放低咨询。"}
                  riskNote={cards.gap_summary?.risk_note ?? "不要继续堆泛内容，不要先追播放，先补承接再放大量。"}
                  actionLabel="去统一主页与承接"
                  actionHref="/upgrade-plan"
                  emphasis="strong"
                />
              </div>
              <div className="md:col-span-2">
                <NextPostCard
                  title="下一条最该发什么（主决策）"
                  conclusion={current.next_post.recommended_topic ?? "先发一条咨询承接内容"}
                  reason={cards.next_post?.reason ?? `${current.next_post.why_this_now ?? "先修复承接链路"}；题型：${(current.next_post as Record<string, string>).recommended_content_type ?? "案例拆解型"}；目标：${(current.next_post as Record<string, string>).recommended_goal ?? "咨询"}。`}
                  riskNote={cards.next_post?.risk_note ?? "不要做泛流程科普，不要只讲观点不放案例，不要省略评论区承接动作。"}
                  actionLabel="去执行这一条"
                  actionHref="/execute"
                  emphasis="strong"
                />
              </div>
              <LearningTargetCard
                title="当前最该学的强账号"
                conclusion={current.learning_target}
                reason={cards.learning_target?.reason ?? "你当前缺的是稳定咨询承接样本，不是流量样本；优先学“结尾动作 + 评论区引导”结构。"}
                riskNote={cards.learning_target?.risk_note ?? "不要盲抄夸张表达，只学承接结构与题型节奏。"}
                actionLabel="去学这个账号"
                actionHref="/learn-from"
              />
              <AccountStageCard
                title="我的账号现在处于什么阶段"
                conclusion={current.account_stage}
                reason={cards.account_stage?.reason ?? current.best_next_action_reason}
                actionLabel="去看账号基线"
                actionHref="/my-account"
              />
              <WeeklyFocusCard
                title="本周改造重点"
                conclusion={current.weekly_focus}
                reason={cards.weekly_focus?.reason ?? "本周不要分散动作，先把“主页承接 + 3 条咨询承接内容”跑通。"}
                riskNote={cards.weekly_focus?.risk_note ?? "不要同时开太多方向，否则无法验证改造是否有效。"}
                actionLabel="去执行本周三件事"
                actionHref="/workspace"
              />
            </>
          )}
        </section>

        <section className="mt-4 grid gap-4 md:grid-cols-3">
          <article className="rounded-2xl border border-line bg-panel/90 p-5">
            <p className="text-xs uppercase tracking-[0.16em] text-subInk">我的账号摘要</p>
            <p className="mt-2 text-sm text-subInk">阶段：{current.account_stage}</p>
            <p className="mt-1 text-sm text-subInk">当前命令：{current.best_next_action}</p>
          </article>
          <article className="rounded-2xl border border-line bg-panel/90 p-5">
            <p className="text-xs uppercase tracking-[0.16em] text-subInk">值得学的账号 / 强样本</p>
            <p className="mt-2 text-sm text-subInk">当前学习对象：{current.learning_target}</p>
            <p className="mt-1 text-sm text-subInk">执行建议：先拆 3 条代表内容再改稿。</p>
          </article>
          <article className="rounded-2xl border border-line bg-panel/90 p-5">
            <p className="text-xs uppercase tracking-[0.16em] text-subInk">执行与复盘摘要</p>
            <p className="mt-2 text-sm text-subInk">本周唯一重点：{current.weekly_focus}</p>
            <p className="mt-1 text-sm text-subInk">发布后 24~48 小时内补复盘。</p>
          </article>
        </section>

        <NextStepCTA
          title="今日最佳下一步"
          conclusion={current.best_next_action}
          reason={current.best_next_action_reason}
          riskNote={cards.next_step?.risk_note ?? "不要再拖到看完更多报表才执行，先做最小验证动作。"}
          primary={{ label: "立即执行这一步", href: "/workspace" }}
          secondary={{ label: "看完整改造路径", href: "/my-account" }}
        />
      </div>
    </main>
  );
}
