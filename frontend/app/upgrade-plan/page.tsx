"use client";

import { GapSummaryCard, NextStepCTA, UpgradeActionCard } from "@/components/frontstage-cards";
import { PageHeader } from "@/components/ui/page-header";
import { ErrorState, LoadingState } from "@/components/ui/view-state";
import { getUpgradePlanSummary, type UpgradePlanSummary } from "@/lib/api";
import { useEffect, useState } from "react";

export default function UpgradePlanPage() {
  const [data, setData] = useState<UpgradePlanSummary | null>(null);
  const [error, setError] = useState<string | null>(null);
  useEffect(() => { void getUpgradePlanSummary().then(setData).catch(() => setError("改造方案页加载失败。")); }, []);

  return (
    <main className="grid-shell min-h-screen"><div className="mx-auto w-full max-w-7xl px-6 py-10 md:px-10">
      <PageHeader eyebrow="改造方案 / gap-to-action" title="把差距翻译成可执行改法" description="这页不是泛建议，而是本周必须改的动作清单。" />
      {error ? <ErrorState message={error} /> : null}
      {!error && !data ? <LoadingState message="正在生成改造方案摘要..." /> : null}
      {data ? <>
        <section className="mt-5"><GapSummaryCard title="当前最大差距" summary={data.current_main_gap} evidence="这是当前改造优先级最高的问题。" /></section>
        <section className="mt-5 grid gap-4 md:grid-cols-3">
          {data.top3_changes.map((x) => <UpgradeActionCard key={x} title="本周最该改" summary={x} actionLabel="去执行" actionHref="/execute" />)}
        </section>
        <section className="mt-5 grid gap-4 md:grid-cols-2">
          <article className="rounded-2xl border border-line bg-panel/90 p-5"><p className="text-xs text-subInk">主页改造摘要</p><p className="mt-2 text-sm text-subInk">{data.profile_upgrade.join("；")}</p></article>
          <article className="rounded-2xl border border-line bg-panel/90 p-5"><p className="text-xs text-subInk">内容结构改造摘要</p><p className="mt-2 text-sm text-subInk">{data.content_structure_upgrade.join("；")}</p></article>
        </section>
        <section className="mt-5 rounded-2xl border border-line bg-panel/90 p-5"><p className="text-xs text-subInk">未来 7 条简版策略</p><ul className="mt-2 space-y-1 text-sm text-subInk">{data.next_7_posts.map((x) => <li key={x}>- {x}</li>)}</ul></section>
        <NextStepCTA description="把改造建议落成实际内容，才会产生结果。" primary={{ label: "去内容执行", href: "/execute" }} secondary={{ label: "去复盘", href: "/review" }} />
      </> : null}
    </div></main>
  );
}
