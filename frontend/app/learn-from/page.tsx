"use client";

import { BenchmarkAccountCard, NextStepCTA } from "@/components/frontstage-cards";
import { PageHeader } from "@/components/ui/page-header";
import { ErrorState, LoadingState } from "@/components/ui/view-state";
import { getLearnFromSummary, type LearnFromSummary } from "@/lib/api";
import Link from "next/link";
import { useEffect, useState } from "react";

export default function LearnFromPage() {
  const [data, setData] = useState<LearnFromSummary | null>(null);
  const [error, setError] = useState<string | null>(null);
  useEffect(() => { void getLearnFromSummary().then(setData).catch(() => setError("值得学的账号页加载失败。")); }, []);

  return (
    <main className="grid-shell min-h-screen"><div className="mx-auto w-full max-w-7xl px-6 py-10 md:px-10">
      <PageHeader eyebrow="值得学的账号 / 复盘台能力" title="强账号中心：先选值得学，再做拆解" description="不是竞品库，而是你的正式对标池入口。" />
      {error ? <ErrorState message={error} /> : null}
      {!error && !data ? <LoadingState message="正在加载对标池..." /> : null}
      {data ? <>
        <section className="mt-5 rounded-2xl border border-line bg-panel/90 p-5"><p className="text-sm text-subInk">当前对标池规模：{data.benchmark_pool_size}</p></section>
        <section className="mt-5 grid gap-4 md:grid-cols-3">
          {data.top_accounts.map((x) => <BenchmarkAccountCard key={x.id} title={x.account_name} summary={x.learnability_reason} evidence={x.similarity_reason} actionLabel="去拆解" actionHref={`/review-lab/benchmarks/${x.id}`} />)}
        </section>
        <section className="mt-5 grid gap-4 md:grid-cols-2">
          <article className="rounded-2xl border border-accent/40 bg-panel/90 p-5"><p className="text-sm">入口一：我自己添加 5 个账号</p><Link href="/review-lab/discovery" className="mt-2 inline-block rounded border border-line px-3 py-1.5 text-xs">去添加</Link></article>
          <article className="rounded-2xl border border-accent/40 bg-panel/90 p-5"><p className="text-sm">入口二：帮我找像我且值得学的账号</p><Link href="/review-lab/discovery" className="mt-2 inline-block rounded border border-line px-3 py-1.5 text-xs">去发现</Link></article>
        </section>
        <NextStepCTA description={`优先拆样本：${data.priority_samples}`} primary={{ label: "去改造方案", href: "/upgrade-plan" }} secondary={{ label: "看全部对标账号", href: "/review-lab/benchmarks" }} />
      </> : null}
    </div></main>
  );
}
