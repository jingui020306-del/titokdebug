"use client";
import Link from "next/link";
import { useParams, useRouter } from "next/navigation";
import { useEffect, useState } from "react";

import { PageHeader } from "@/components/ui/page-header";
import { getContentPlan } from "@/lib/api";

export default function ContentPlanReportPage() {
  const { id } = useParams<{ id: string }>();
  const router = useRouter();
  const [data, setData] = useState<any>(null);
  useEffect(() => { void getContentPlan(id).then((r) => setData(r.data)); }, [id]);
  if (!data) return <main className="grid-shell min-h-screen p-10 text-subInk">加载周计划中...</main>;
  return <main className="grid-shell min-h-screen"><div className="mx-auto w-full max-w-6xl px-6 py-10 md:px-10"><PageHeader eyebrow="content-studio / weekly-plan" title="周计划策略板" description={data.weekly_strategy_summary} />
    <div className="mt-6 grid gap-3">{data.content_calendar.map((x:any)=><article key={x.day} className="rounded-xl border border-line bg-panel/90 p-4 text-sm"><p className="font-medium">{x.day.toUpperCase()} · {x.title_direction}</p><p className="text-subInk">目的：{x.content_purpose} · 支柱：{x.pillar}</p><div className="mt-2 flex gap-3"><button className="rounded border border-line px-2 py-1" onClick={()=>router.push(`/content-studio?tab=rewrite&title=${encodeURIComponent(x.title_direction)}&pillar=${encodeURIComponent(String(x.pillar))}`)}>去改单条</button></div></article>)}</div>
    <div className="mt-6"><Link href="/content-studio" className="text-subInk underline">返回内容台</Link></div></div></main>;
}
