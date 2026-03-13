"use client";

import { FrozenPositioningCard, NextStepCTA } from "@/components/frontstage-cards";
import { PageHeader } from "@/components/ui/page-header";
import { ErrorState, LoadingState } from "@/components/ui/view-state";
import { getMyAccountSummary, type MyAccountSummary } from "@/lib/api";
import { useEffect, useState } from "react";

export default function MyAccountPage() {
  const [data, setData] = useState<MyAccountSummary | null>(null);
  const [error, setError] = useState<string | null>(null);
  useEffect(() => { void getMyAccountSummary().then(setData).catch(() => setError("我的账号页加载失败。")); }, []);

  return (
    <main className="grid-shell min-h-screen"><div className="mx-auto w-full max-w-7xl px-6 py-10 md:px-10">
      <PageHeader eyebrow="我的账号 / 定位台能力" title="先把自己的账号基线看清楚" description="这里收口定位摘要、冻结状态和主页改造方向，保证后续学习与改造不跑偏。" />
      {error ? <ErrorState message={error} /> : null}
      {!error && !data ? <LoadingState message="正在加载账号基线..." /> : null}
      {data ? <>
        <section className="mt-5 grid gap-4 md:grid-cols-2">
          <FrozenPositioningCard title="当前定位摘要" summary={data.current_positioning_summary} evidence={`当前阶段：${data.account_stage}`} actionLabel="查看定位详情" actionHref="/positioning" />
          <FrozenPositioningCard title="定位版本状态" summary={data.frozen ? "已冻结" : "未冻结"} evidence={data.active_positioning?.report_title as string ?? "暂无有效定位版本"} actionLabel="去定位历史" actionHref="/positioning/history" />
        </section>
        <section className="mt-5 grid gap-4 md:grid-cols-3">
          <article className="rounded-2xl border border-line bg-panel/90 p-5"><p className="text-xs text-subInk">三个内容支柱</p><p className="mt-2 text-sm text-subInk">{data.three_pillars.join(" / ")}</p></article>
          <article className="rounded-2xl border border-line bg-panel/90 p-5"><p className="text-xs text-subInk">不该混入的方向</p><p className="mt-2 text-sm text-subInk">{data.off_limits.join(" / ")}</p></article>
          <article className="rounded-2xl border border-line bg-panel/90 p-5"><p className="text-xs text-subInk">证据链简版</p><p className="mt-2 text-sm text-subInk">{data.evidence_chain.join("；")}</p></article>
        </section>
        <NextStepCTA description="先确认账号基线，再去建立正式对标池。" primary={{ label: "去值得学的账号", href: "/learn-from" }} secondary={{ label: "去改造方案", href: "/upgrade-plan" }} />
      </> : null}
    </div></main>
  );
}
