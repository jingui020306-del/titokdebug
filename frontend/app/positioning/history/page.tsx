"use client";

import Link from "next/link";
import { useEffect, useState } from "react";

import { PageHeader } from "@/components/ui/page-header";
import { ErrorState, LoadingState } from "@/components/ui/view-state";
import { freezePositioning, getPositioningHistory, setActivePositioning, type PositioningVersionSummary } from "@/lib/api";

export default function PositioningHistoryPage() {
  const [items, setItems] = useState<PositioningVersionSummary[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const load = async () => {
    try { setError(null); setItems(await getPositioningHistory()); } catch { setError("定位历史加载失败。"); } finally { setLoading(false); }
  };
  useEffect(() => { void load(); }, []);

  return (
    <main className="grid-shell min-h-screen">
      <div className="mx-auto w-full max-w-6xl px-6 py-10 md:px-10">
        <PageHeader eyebrow="positioning / history" title="定位版本历史" description="可设置当前有效定位，并冻结稳定版本。" />
        {loading ? <LoadingState message="加载定位版本中..." /> : null}
        {error ? <ErrorState message={error} /> : null}
        <div className="mt-4 space-y-3 text-sm">
          {items.map((x) => (
            <article key={x.positioning_version_id} className="rounded-2xl border border-line bg-panel/90 p-5">
              <p className="text-ink">{x.report_title}</p>
              <p className="mt-1 text-subInk">{x.preview_text}</p>
              <p className="mt-1 text-subInk">变化等级：{x.change_level} · {x.is_active ? "当前有效" : "非当前"} · {x.is_frozen ? "已冻结" : "未冻结"}</p>
              <div className="mt-2 flex gap-2">
                <button className="rounded border border-line px-2 py-1" onClick={async()=>{await setActivePositioning(x.job_id);await load();}}>设为当前</button>
                <button className="rounded border border-line px-2 py-1" onClick={async()=>{await freezePositioning(x.job_id);await load();}}>冻结</button>
                <Link href={`/positioning/report/${x.job_id}`} className="rounded border border-line px-2 py-1">查看报告</Link>
              </div>
            </article>
          ))}
        </div>
        <div className="mt-6"><Link href="/workspace" className="rounded border border-line px-3 py-2 text-sm">返回工作台继续下一步</Link></div>
      </div>
    </main>
  );
}
