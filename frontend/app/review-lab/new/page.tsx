"use client";

import { useRouter } from "next/navigation";
import { useState } from "react";

import { PageHeader } from "@/components/ui/page-header";
import { createReviewLab } from "@/lib/api";

export default function ReviewLabNewPage() {
  const router = useRouter();
  const [loading, setLoading] = useState(false);
  const [form, setForm] = useState({
    source_type: "manual",
    content_item_id: "",
    publish_record_id: "",
    version_id: "",
    content_title: "",
    publish_time: new Date().toISOString(),
    content_pillar: "定位",
    rewrite_version: "",
    views: 0,
    likes: 0,
    comments: 0,
    favorites: 0,
    shares: 0,
    profile_visits: 0,
    dm_count: 0,
    inquiry_count: 0,
    conversion_count: 0,
    subjective_feedback: ""
  });

  return <main className="grid-shell min-h-screen"><div className="mx-auto w-full max-w-5xl px-6 py-10 md:px-10">
    <PageHeader eyebrow="review-lab / new" title="新建复盘" description="默认展示平台表现 + 咨询表现，复盘结论才会更接近真实业务。" />
    <section className="mt-6 rounded-2xl border border-line bg-panel/90 p-6 space-y-3 text-sm">
      <input className="w-full rounded border border-line bg-base px-3 py-2" placeholder="内容标题" value={form.content_title} onChange={(e)=>setForm({...form,content_title:e.target.value})}/>
      <input className="w-full rounded border border-line bg-base px-3 py-2" placeholder="内容支柱" value={form.content_pillar} onChange={(e)=>setForm({...form,content_pillar:e.target.value})}/>
      <div className="grid grid-cols-2 gap-3 md:grid-cols-5">
        {(["views","likes","comments","favorites","shares","profile_visits","dm_count","inquiry_count","conversion_count"] as const).map((k)=><input key={k} type="number" className="rounded border border-line bg-base px-3 py-2" placeholder={k} value={form[k]} onChange={(e)=>setForm({...form,[k]:Number(e.target.value)})} />)}
      </div>
      <textarea className="w-full rounded border border-line bg-base px-3 py-2" placeholder="主观感受（可选）" value={form.subjective_feedback} onChange={(e)=>setForm({...form,subjective_feedback:e.target.value})}/>
      <button className="rounded border border-accent px-3 py-2" disabled={loading} onClick={async()=>{setLoading(true);try{const r=await createReviewLab(form);router.push(`/review-lab/report/${r.review_id}`);}finally{setLoading(false);}}}>{loading?"生成中...":"生成复盘报告"}</button>
    </section>
  </div></main>;
}
