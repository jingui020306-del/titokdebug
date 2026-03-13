"use client";

import Link from "next/link";
import { useState } from "react";

import { PageHeader } from "@/components/ui/page-header";
import { discoveryConfirm, discoverySearch, type DiscoveryCandidate } from "@/lib/api";

export default function DiscoveryPage() {
  const [candidates, setCandidates] = useState<DiscoveryCandidate[]>([]);
  const [manual, setManual] = useState({ account_name: "", account_url: "", similarity_reason: "", learnability_reason: "", account_tier: "peer" });

  return (
    <main className="grid-shell min-h-screen"><div className="mx-auto w-full max-w-6xl px-6 py-10 md:px-10">
      <PageHeader eyebrow="review-lab / discovery" title="强账号发现与确认" description="先找值得学的同类强账号，再确认加入正式对标池。" />

      <section className="mt-5 rounded-2xl border border-line bg-panel/90 p-5 text-sm">
        <p className="text-xs text-subInk">模式1：我自己添加 5 个账号</p>
        <div className="mt-2 grid gap-2 md:grid-cols-2">
          <input className="rounded border border-line bg-base px-3 py-2" placeholder="账号名" value={manual.account_name} onChange={(e)=>setManual({...manual,account_name:e.target.value})} />
          <input className="rounded border border-line bg-base px-3 py-2" placeholder="账号链接" value={manual.account_url} onChange={(e)=>setManual({...manual,account_url:e.target.value})} />
          <input className="rounded border border-line bg-base px-3 py-2" placeholder="为什么像我" value={manual.similarity_reason} onChange={(e)=>setManual({...manual,similarity_reason:e.target.value})} />
          <input className="rounded border border-line bg-base px-3 py-2" placeholder="为什么值得学" value={manual.learnability_reason} onChange={(e)=>setManual({...manual,learnability_reason:e.target.value})} />
        </div>
      </section>

      <section className="mt-5 rounded-2xl border border-line bg-panel/90 p-5 text-sm">
        <p className="text-xs text-subInk">模式2：系统帮我找值得学的账号</p>
        <button className="mt-2 rounded border border-accent px-3 py-2" onClick={async()=>{
          const data = await discoverySearch({ my_positioning: "咨询型IP", niche_keyword: "咨询", goal: "咨询", target_audience: "职场管理者", content_style: "结构化", learning_preference: "更稳咨询" });
          setCandidates(data);
        }}>帮我找值得学的同类账号</button>

        <ul className="mt-3 space-y-2">
          {candidates.map((c, i) => <li key={i} className="rounded border border-line/60 p-3">
            <p>{c.account_name}</p><p className="text-subInk">像我：{c.similarity_reason}</p><p className="text-subInk">可学：{c.learnability_reason}</p>
          </li>)}
        </ul>
        {candidates.length > 0 ? <button className="mt-3 rounded border border-accent px-3 py-2" onClick={async()=>{await discoveryConfirm(candidates);}}>确认加入正式对标池</button> : null}
      </section>

      <div className="mt-6 flex gap-3 text-sm"><Link href="/review-lab/benchmarks" className="rounded border border-line px-3 py-2">查看对标池</Link><Link href="/workspace" className="rounded border border-line px-3 py-2">返回工作台</Link></div>
    </div></main>
  );
}
