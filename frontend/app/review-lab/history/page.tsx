"use client";

import Link from "next/link";
import { useCallback, useEffect, useState } from "react";

import { PageHeader } from "@/components/ui/page-header";
import { EmptyState, ErrorState, LoadingState } from "@/components/ui/view-state";
import { getReviewLabHistory, type ReviewHistoryItem } from "@/lib/api";

export default function ReviewLabHistoryPage() {
  const [items, setItems] = useState<ReviewHistoryItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [pillar, setPillar] = useState("");

  const load = useCallback(async () => {
    try { setError(null); setItems(await getReviewLabHistory(pillar || undefined)); } catch { setError("复盘时间线加载失败，请确认服务状态。"); } finally { setLoading(false); }
  }, [pillar]);
  useEffect(() => { void load(); }, [load]);

  return (
    <main className="grid-shell min-h-screen">
      <div className="mx-auto w-full max-w-6xl px-6 py-10 md:px-10">
        <PageHeader eyebrow="review-lab / history" title="复盘策略时间线" description="支持按支柱筛选，并快速看出比上一版更好还是更差。" />
        <div className="mt-3"><input className="w-full rounded border border-line bg-base px-3 py-2 text-sm md:w-72" placeholder="按支柱筛选（如：定位）" value={pillar} onChange={(e)=>setPillar(e.target.value)} /></div>
        {loading ? <LoadingState message="加载复盘时间线..." /> : null}
        {error ? <ErrorState message={error} /> : null}
        {!loading && !error && items.length === 0 ? <EmptyState title="还没有复盘记录" description="先提交一次复盘，系统会开始沉淀你的策略时间线。" /> : null}

        <div className="mt-5 space-y-3">
          {items.map((item) => (
            <article key={item.review_id} className="rounded-2xl border border-line bg-panel/90 p-5 text-sm">
              <p className="text-[11px] uppercase tracking-[0.12em] text-subInk">{new Date(item.created_at).toLocaleString()}</p>
              <p className="mt-1 text-base text-ink">{item.content_title} · {item.content_pillar}</p>
              <p className="mt-1 text-subInk">{item.major_metrics}</p>
              <p className="mt-1 text-subInk">对比信号：{item.comparison_signal}</p>
              <p className="mt-1 text-subInk">放大建议：{item.worth_scaling}</p>
              <p className="mt-1 text-subInk">下一步动作：{item.next_action}</p>
              <Link href={`/review-lab/report/${item.review_id}`} className="mt-2 inline-block text-accent underline">查看完整复盘</Link>
            </article>
          ))}
        </div>
        <div className="mt-5"><Link href="/workspace" className="rounded border border-line px-3 py-2 text-sm">返回工作台继续下一步</Link></div>
      </div>
    </main>
  );
}
