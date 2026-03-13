"use client";

import { NextPostCard, NextStepCTA, PendingContentCard } from "@/components/frontstage-cards";
import { PageHeader } from "@/components/ui/page-header";
import { ErrorState, LoadingState } from "@/components/ui/view-state";
import { getExecuteSummary, type ExecuteSummary } from "@/lib/api";
import { useEffect, useState } from "react";

export default function ExecutePage() {
  const [data, setData] = useState<ExecuteSummary | null>(null);
  const [error, setError] = useState<string | null>(null);
  useEffect(() => { void getExecuteSummary().then(setData).catch(() => setError("内容执行页加载失败。")); }, []);

  return (
    <main className="grid-shell min-h-screen"><div className="mx-auto w-full max-w-7xl px-6 py-10 md:px-10">
      <PageHeader eyebrow="内容执行 / 内容台能力" title="这一周到底发什么，在这里落地" description="聚焦下一条建议、待发布队列和强样本学习动作。" />
      {error ? <ErrorState message={error} /> : null}
      {!error && !data ? <LoadingState message="正在加载内容执行摘要..." /> : null}
      {data ? <>
        <section className="mt-5 grid gap-4 md:grid-cols-2">
          <NextPostCard title="下一条建议" summary={data.next_post_recommendation.recommended_topic ?? "先发一条咨询承接内容"} evidence={data.next_post_recommendation.why_this_now ?? "当前最优先修复承接链路"} actionLabel="去改单条" actionHref="/content-studio" />
          <PendingContentCard title="当前待发布内容" summary={`待发布：${data.pending_publish}`} evidence={data.weekly_plan_summary} actionLabel="去标记已发布" actionHref="/content-studio" />
        </section>
        <section className="mt-5 grid gap-4 md:grid-cols-2">
          <article className="rounded-2xl border border-line bg-panel/90 p-5"><p className="text-xs text-subInk">最近改好的内容</p><p className="mt-2 text-sm text-subInk">{data.recent_rewrites}</p></article>
          <article className="rounded-2xl border border-line bg-panel/90 p-5"><p className="text-xs text-subInk">从强样本学来的做法</p><p className="mt-2 text-sm text-subInk">{data.benchmark_learning_preview.join(" / ") || "先建立对标池"}</p></article>
        </section>
        <NextStepCTA description="发完再复盘，才能知道这次改法是否有效。" primary={{ label: "去复盘", href: "/review" }} secondary={{ label: "进入内容台完整功能", href: "/content-studio" }} />
      </> : null}
    </div></main>
  );
}
