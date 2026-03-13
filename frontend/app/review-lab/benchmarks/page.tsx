"use client";

import Link from "next/link";
import { useEffect, useState } from "react";

import { PageHeader } from "@/components/ui/page-header";
import { createBenchmark, listBenchmarks, type BenchmarkAccountSummary } from "@/lib/api";

export default function BenchmarksPage() {
  const [items, setItems] = useState<BenchmarkAccountSummary[]>([]);

  const load = async () => setItems(await listBenchmarks());
  useEffect(() => { void load(); }, []);

  return (
    <main className="grid-shell min-h-screen"><div className="mx-auto w-full max-w-6xl px-6 py-10 md:px-10">
      <PageHeader eyebrow="review-lab / benchmarks" title="正式对标池" description="这里不是资料库，而是你账号改造的学习对象池。" />
      <button className="mt-4 rounded border border-accent px-3 py-2 text-sm" onClick={async()=>{await createBenchmark({ account_name: "手动样本账号", platform: "抖音", account_url: "https://www.douyin.com/user/manual", similarity_reason: "同赛道", learnability_reason: "承接强", positioning_summary: "咨询型表达", why_selected: "结构稳定", source_mode: "manual" }); await load();}}>手动添加一个样本账号</button>
      <div className="mt-5 space-y-3 text-sm">
        {items.map((x)=><article key={x.id} className="rounded-2xl border border-line bg-panel/90 p-5"><p>{x.account_name} · {x.account_tier}</p><p className="mt-1 text-subInk">像我：{x.similarity_reason}</p><p className="mt-1 text-subInk">可学：{x.learnability_reason}</p><Link href={`/review-lab/benchmarks/${x.id}`} className="mt-2 inline-block text-accent underline">进入拆解页</Link></article>)}
      </div>
      <div className="mt-6"><Link href="/workspace" className="rounded border border-line px-3 py-2 text-sm">返回工作台</Link></div>
    </div></main>
  );
}
