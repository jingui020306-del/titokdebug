"use client";
import Link from "next/link";
import { useParams } from "next/navigation";
import { useEffect, useState } from "react";

import { PageHeader } from "@/components/ui/page-header";
import { adoptContentRewrite, getContentRewrite } from "@/lib/api";

export default function ContentRewriteReportPage() {
  const { id } = useParams<{ id: string }>();
  const [data, setData] = useState<any>(null);
  const [msg, setMsg] = useState("");
  useEffect(() => { void getContentRewrite(id).then((r) => setData(r.data)); }, [id]);
  if (!data) return <main className="grid-shell min-h-screen p-10 text-subInk">加载改单条结果...</main>;
  return <main className="grid-shell min-h-screen"><div className="mx-auto w-full max-w-6xl px-6 py-10 md:px-10"><PageHeader eyebrow="content-studio / rewrite" title="单条改稿结果" description={data.diagnosis_summary} />
    <section className="mt-5 rounded-2xl border border-line bg-panel/90 p-5"><p className="text-xs text-subInk">标题A/B/C</p><ul className="mt-2 space-y-2 text-sm">{data.title_variants.map((x:any)=><li key={x.label}>{x.label}：{x.content}</li>)}</ul></section>
    <section className="mt-5 rounded-2xl border border-line bg-panel/90 p-5"><p className="text-xs text-subInk">封面A/B</p><ul className="mt-2 space-y-2 text-sm">{data.cover_variants.map((x:any)=><li key={x.label}>{x.label}：{x.content}</li>)}</ul></section>
    <div className="mt-6 flex gap-3"><button className="rounded border border-accent px-3 py-2 text-sm" onClick={async()=>{const r=await adoptContentRewrite(id);setMsg(r.message);}}>标记为已采用</button><Link href="/review-lab/new" className="rounded border border-line px-3 py-2 text-sm">进入复盘台</Link><Link href="/workspace" className="rounded border border-line px-3 py-2 text-sm">返回工作台继续下一步</Link></div>
    {msg ? <p className="mt-2 text-xs text-subInk">{msg}</p> : null}
  </div></main>;
}
