"use client";

import Link from "next/link";
import { useParams } from "next/navigation";
import { useCallback, useEffect, useState } from "react";

import { PageHeader } from "@/components/ui/page-header";
import { createBenchmarkSample, getBenchmark, listBenchmarkSamples, type BenchmarkAccountSummary, type BenchmarkContentSample } from "@/lib/api";

export default function BenchmarkDetailPage() {
  const { id } = useParams<{ id: string }>();
  const [bm, setBm] = useState<BenchmarkAccountSummary | null>(null);
  const [samples, setSamples] = useState<BenchmarkContentSample[]>([]);

  const load = useCallback(async () => {
    const [b, s] = await Promise.all([getBenchmark(id), listBenchmarkSamples(id)]);
    setBm(b); setSamples(s);
  }, [id]);
  useEffect(() => { void load(); }, [load]);

  if (!bm) return <main className="grid-shell min-h-screen p-10 text-subInk">加载拆解页中...</main>;

  return (
    <main className="grid-shell min-h-screen"><div className="mx-auto w-full max-w-6xl px-6 py-10 md:px-10">
      <PageHeader eyebrow="review-lab / benchmark detail" title={`${bm.account_name} 拆解页`} description="目标：学有效模式，不盲抄。" />
      <section className="rounded-2xl border border-line bg-panel/90 p-5 text-sm text-subInk">
        <p>一句话定位：{bm.positioning_summary}</p>
        <p className="mt-1">最值得学：{bm.learnability_reason}</p>
        <p className="mt-1">不建议盲学：头部账号高强度情绪表达节奏</p>
      </section>
      <section className="mt-5 rounded-2xl border border-line bg-panel/90 p-5 text-sm">
        <p className="text-xs text-subInk">代表性强样本</p>
        <button className="mt-2 rounded border border-accent px-3 py-2" onClick={async()=>{await createBenchmarkSample(id,{ title: "强样本：先结论后证据", sample_url: "https://example.com/sample", content_type: "案例拆解", pillar_guess: "咨询策略", hook_style: "问题开场", conversion_style: "评论区+私信双承接", sample_heat_level: "strong", why_it_worked: "结构化且承接清晰"}); await load();}}>添加样本</button>
        <ul className="mt-2 space-y-2">{samples.map((x)=><li key={x.id} className="rounded border border-line/60 p-3">{x.title} · {x.sample_heat_level} · {x.why_it_worked}</li>)}</ul>
      </section>
      <div className="mt-6 flex gap-3 text-sm"><Link href="/review-lab/benchmarks" className="rounded border border-line px-3 py-2">返回对标池</Link><Link href="/workspace" className="rounded border border-line px-3 py-2">返回工作台</Link></div>
    </div></main>
  );
}
