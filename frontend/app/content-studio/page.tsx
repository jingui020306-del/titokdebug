"use client";

import Link from "next/link";
import { useRouter } from "next/navigation";
import { useCallback, useEffect, useState } from "react";

import { PageHeader } from "@/components/ui/page-header";
import { createContentPlan, createContentRewrite, getContentItems, getContentStudioNextPost, type ContentItemSummary } from "@/lib/api";

export default function ContentStudioPage() {
  const router = useRouter();
  const [tab, setTab] = useState<"plan" | "rewrite">("plan");
  const [loading, setLoading] = useState(false);
  const [items, setItems] = useState<ContentItemSummary[]>([]);
  const [selectedItemId, setSelectedItemId] = useState<string>("");
  const [nextPost, setNextPost] = useState<Record<string, unknown> | null>(null);

  const [plan, setPlan] = useState({ one_line_positioning: "", content_pillars: [] as string[], target_audience_summary: "", weekly_goal: "涨粉", posts_per_week: 7, has_live: false, primary_service: "咨询服务" });
  const [rw, setRw] = useState({ platform: "抖音", goal_action: "转咨询", original_title: "", original_script: "", original_cover_text: "", pillar: "定位", risk_limits: ["避免敏感承诺"], target_audience: "咨询型人群" });

  const reloadItems = useCallback(async () => {
    const [rows, np] = await Promise.all([getContentItems(), getContentStudioNextPost()]);
    setItems(rows);
    setNextPost(np);
    if (!selectedItemId && rows[0]) setSelectedItemId(rows[0].id);
  }, [selectedItemId]);

  useEffect(() => { void reloadItems(); }, [reloadItems]);

  const createPlan = async () => {
    setLoading(true);
    try {
      const res = await createContentPlan(plan);
      await reloadItems();
      router.push(`/content-studio/plan/${res.plan_id}`);
    } finally { setLoading(false); }
  };
  const createRewrite = async () => {
    setLoading(true);
    try {
      const res = await createContentRewrite({ ...rw, content_item_id: selectedItemId || undefined });
      await reloadItems();
      router.push(`/content-studio/rewrite/${res.rewrite_id}`);
    } finally { setLoading(false); }
  };

  return (
    <main className="grid-shell min-h-screen"><div className="mx-auto w-full max-w-6xl px-6 py-10 md:px-10">
      <PageHeader eyebrow="content-studio / 内容台" title="内容台" description="围绕内容对象推进：计划 → 改稿 → 发布 → 复盘。" />
      <section className="mt-4 rounded-2xl border border-line bg-panel/90 p-5">
        <p className="text-xs text-subInk">下一条建议</p>
        <p className="mt-1 text-sm text-subInk">{String(nextPost?.recommended_topic ?? "正在生成建议...")}</p>
        <p className="mt-1 text-xs text-subInk">现在该发它的原因：{String(nextPost?.why_this_now ?? "")}</p>
      </section>

      <section className="mt-4 rounded-2xl border border-line bg-panel/90 p-5">
        <p className="text-xs text-subInk">内容对象列表</p>
        <div className="mt-2 grid gap-2 md:grid-cols-2">
          {items.slice(0, 6).map((item) => (
            <Link key={item.id} href={`/content-studio/item/${item.id}`} className="rounded border border-line/60 p-3 text-sm text-subInk">{item.title_or_working_title} · {item.status}</Link>
          ))}
        </div>
      </section>

      <div className="mt-6 flex gap-2 text-sm"><button className={`rounded border px-3 py-2 ${tab==='plan'?'border-accent bg-accent/10':'border-line'}`} onClick={()=>setTab('plan')}>生成周计划</button><button className={`rounded border px-3 py-2 ${tab==='rewrite'?'border-accent bg-accent/10':'border-line'}`} onClick={()=>setTab('rewrite')}>改单条</button></div>
      {tab==='plan' ? <section className="mt-5 rounded-2xl border border-line bg-panel/90 p-6 space-y-3 text-sm">
        <input className="w-full rounded border border-line bg-base px-3 py-2" placeholder="一句话定位" value={plan.one_line_positioning} onChange={(e)=>setPlan({...plan,one_line_positioning:e.target.value})}/>
        <input className="w-full rounded border border-line bg-base px-3 py-2" placeholder="内容支柱（|分隔）" value={plan.content_pillars.join('|')} onChange={(e)=>setPlan({...plan,content_pillars:e.target.value.split('|').filter(Boolean)})}/>
        <input className="w-full rounded border border-line bg-base px-3 py-2" placeholder="目标用户摘要" value={plan.target_audience_summary} onChange={(e)=>setPlan({...plan,target_audience_summary:e.target.value})}/>
        <button className="rounded border border-accent px-3 py-2" disabled={loading} onClick={createPlan}>{loading?'生成中...':'生成周内容计划'}</button>
      </section> : <section className="mt-5 rounded-2xl border border-line bg-panel/90 p-6 space-y-3 text-sm">
        <select className="w-full rounded border border-line bg-base px-3 py-2" value={selectedItemId} onChange={(e) => setSelectedItemId(e.target.value)}>
          <option value="">不关联已有内容对象（新建）</option>
          {items.map((item) => <option key={item.id} value={item.id}>{item.title_or_working_title}</option>)}
        </select>
        <input className="w-full rounded border border-line bg-base px-3 py-2" placeholder="原标题" value={rw.original_title} onChange={(e)=>setRw({...rw,original_title:e.target.value})}/>
        <textarea className="w-full rounded border border-line bg-base px-3 py-2" placeholder="原脚本" value={rw.original_script} onChange={(e)=>setRw({...rw,original_script:e.target.value})}/>
        <input className="w-full rounded border border-line bg-base px-3 py-2" placeholder="原封面文案" value={rw.original_cover_text} onChange={(e)=>setRw({...rw,original_cover_text:e.target.value})}/>
        <button className="rounded border border-accent px-3 py-2" disabled={loading} onClick={createRewrite}>{loading?'生成中...':'生成改单条结果'}</button>
      </section>}
    </div></main>
  );
}
