"use client";

import { NextStepCTA, PatternAssetPreviewCard, PendingReviewCard } from "@/components/frontstage-cards";
import { PageHeader } from "@/components/ui/page-header";
import { ErrorState, LoadingState } from "@/components/ui/view-state";
import { getReviewSummary, type ReviewSummary } from "@/lib/api";
import { useEffect, useState } from "react";

export default function ReviewPage() {
  const [data, setData] = useState<ReviewSummary | null>(null);
  const [error, setError] = useState<string | null>(null);
  useEffect(() => { void getReviewSummary().then(setData).catch(() => setError("复盘页加载失败。")); }, []);

  return (
    <main className="grid-shell min-h-screen"><div className="mx-auto w-full max-w-7xl px-6 py-10 md:px-10">
      <PageHeader eyebrow="复盘 / 复盘台能力" title="发完之后，判断改得对不对" description="看有效支柱、有效题型和该停止方向，再决定下一轮动作。" />
      {error ? <ErrorState message={error} /> : null}
      {!error && !data ? <LoadingState message="正在加载复盘摘要..." /> : null}
      {data ? <>
        <section className="mt-5 rounded-2xl border border-line bg-panel/90 p-5"><p className="text-xs text-subInk">最近一次复盘摘要</p><p className="mt-2 text-sm text-subInk">{data.latest_review_summary}</p></section>
        <section className="mt-5 grid gap-4 md:grid-cols-3">
          <PatternAssetPreviewCard title="当前最有效支柱" summary={data.best_pillar} evidence="建议继续放大此方向。" />
          <PatternAssetPreviewCard title="当前最有效题型" summary={data.best_content_type} evidence={data.latest_better_or_worse} />
          <PendingReviewCard title="建议停止方向" summary={data.stopped_directions.join(" / ") || "暂无"} evidence="避免继续在低效方向消耗。" />
        </section>
        <NextStepCTA description="复盘结论应回流到改造方案与下一条建议。" primary={{ label: "去改造方案", href: "/upgrade-plan" }} secondary={{ label: "去完整复盘", href: "/review-lab" }} />
      </> : null}
    </div></main>
  );
}
