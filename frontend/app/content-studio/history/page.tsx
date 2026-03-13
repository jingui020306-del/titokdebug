"use client";
import Link from "next/link";
import { useEffect, useState } from "react";

import { PageHeader } from "@/components/ui/page-header";
import { getContentStudioHistory } from "@/lib/api";

export default function ContentStudioHistoryPage() {
  const [items, setItems] = useState<any[]>([]);
  useEffect(() => { void getContentStudioHistory().then((r)=>setItems(r.items)); }, []);
  return <main className="grid-shell min-h-screen"><div className="mx-auto w-full max-w-5xl px-6 py-10 md:px-10"><PageHeader eyebrow="content-studio / history" title="内容台历史" /><div className="mt-5 space-y-2">{items.map((x)=> <article key={`${x.kind}-${x.id}`} className="rounded-xl border border-line bg-panel/90 p-4 text-sm"><p>{x.title}</p><p className="text-subInk">{x.kind} · {x.status}</p><Link className="underline" href={x.kind==='weekly_plan'?`/content-studio/plan/${x.id}`:`/content-studio/rewrite/${x.id}`}>查看</Link></article>)}</div></div></main>;
}
