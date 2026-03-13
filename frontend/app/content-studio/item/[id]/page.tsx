"use client";

import Link from "next/link";
import { useParams } from "next/navigation";
import { useCallback, useEffect, useState } from "react";

import { PageHeader } from "@/components/ui/page-header";
import { ErrorState, LoadingState } from "@/components/ui/view-state";
import { getContentItem, getContentItemTimeline, markContentPublished, type ContentItemDetail, type ContentItemTimeline } from "@/lib/api";

export default function ContentItemPage() {
  const { id } = useParams<{ id: string }>();
  const [detail, setDetail] = useState<ContentItemDetail | null>(null);
  const [timeline, setTimeline] = useState<ContentItemTimeline | null>(null);
  const [error, setError] = useState<string | null>(null);

  const load = useCallback(async () => {
    try {
      setError(null);
      const [d, t] = await Promise.all([getContentItem(id), getContentItemTimeline(id)]);
      setDetail(d);
      setTimeline(t);
    } catch {
      setError("内容对象详情加载失败，请稍后再试。");
    }
  }, [id]);

  useEffect(() => { void load(); }, [load]);

  const onMarkPublished = async () => {
    try {
      await markContentPublished(id, {
        published_at: new Date().toISOString(),
        views: 3200,
        likes: 218,
        comments: 44,
        favorites: 27,
        shares: 15,
        profile_visits: 48,
        dm_count: 6,
        inquiry_count: 3,
        conversion_count: 1,
        manual_notes: "演示模式手动回填"
      });
      await load();
    } catch {
      setError("标记发布失败，请确认当前内容已采用版本。");
    }
  };

  if (error) return <main className="grid-shell min-h-screen p-10"><ErrorState message={error} /></main>;
  if (!detail) return <main className="grid-shell min-h-screen p-10"><LoadingState message="加载内容对象中..." /></main>;

  return (
    <main className="grid-shell min-h-screen">
      <div className="mx-auto w-full max-w-6xl px-6 py-10 md:px-10">
        <PageHeader eyebrow="content-studio / item" title={detail.item.title_or_working_title} description={`支柱：${detail.item.pillar} · 目标：${detail.item.content_goal} · 状态：${detail.item.status}`} />

        <section className="grid gap-5 md:grid-cols-2">
          <article className="rounded-2xl border border-line bg-panel/90 p-5">
            <p className="text-xs text-subInk">版本与发布</p>
            <p className="mt-2 text-sm text-subInk">当前采用版本：{detail.chosen_version?.version_label ?? "暂无"}</p>
            <p className="mt-1 text-sm text-subInk">最近发布时间：{detail.publish_records[0] ? new Date(detail.publish_records[0].published_at).toLocaleString() : "尚未发布"}</p>
            <button onClick={onMarkPublished} className="mt-3 rounded border border-accent px-3 py-2 text-xs">标记为已发布</button>
          </article>

          <article className="rounded-2xl border border-line bg-panel/90 p-5">
            <p className="text-xs text-subInk">咨询结果</p>
            <p className="mt-2 text-sm text-subInk">最近一条咨询数：{detail.publish_records[0]?.inquiry_count ?? 0}</p>
            <p className="mt-1 text-sm text-subInk">最近一条成单数：{detail.publish_records[0]?.conversion_count ?? 0}</p>
            <p className="mt-1 text-sm text-subInk">最近复盘：{detail.latest_review_summary}</p>
            <p className="mt-1 text-sm text-subInk">下一步动作：{detail.next_action}</p>
          </article>
        </section>

        <section className="mt-6 rounded-2xl border border-line bg-panel/90 p-5">
          <p className="text-xs text-subInk">版本列表</p>
          <ul className="mt-2 space-y-2 text-sm text-subInk">
            {detail.versions.map((v) => <li key={v.id} className="rounded border border-line/60 p-3">{v.version_label} · {v.title} · {v.is_adopted ? "已采用" : "未采用"}</li>)}
          </ul>
        </section>

        <section className="mt-6 rounded-2xl border border-line bg-panel/90 p-5">
          <p className="text-xs text-subInk">内容对象时间线</p>
          <ul className="mt-2 space-y-2 text-sm text-subInk">
            {timeline?.timeline.map((x) => <li key={x.id} className="rounded border border-line/60 p-3">{new Date(x.created_at).toLocaleString()} · {x.title} · {x.summary}</li>)}
          </ul>
        </section>

        <div className="mt-6 flex gap-3 text-sm">
          <Link href="/content-studio" className="rounded border border-line px-3 py-2">回到内容台</Link>
          <Link href="/workspace" className="rounded border border-line px-3 py-2">返回工作台继续下一步</Link>
        </div>
      </div>
    </main>
  );
}
