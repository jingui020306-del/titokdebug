"use client";

import Link from "next/link";
import { useParams } from "next/navigation";
import { useCallback, useEffect, useState } from "react";

import { PageHeader } from "@/components/ui/page-header";
import { ErrorState, LoadingState } from "@/components/ui/view-state";
import { freezePositioning, getActivePositioning, getPositioningReport, setActivePositioning, type PositioningVersionSummary, type ReportData } from "@/lib/api";

export default function PositioningReportPage() {
  const { id } = useParams<{ id: string }>();
  const [data, setData] = useState<ReportData | null>(null);
  const [active, setActive] = useState<PositioningVersionSummary | null>(null);
  const [error, setError] = useState<string | null>(null);

  const load = useCallback(async () => {
    try {
      setError(null);
      const r = await getPositioningReport(id);
      setData(r.data);
      try { setActive(await getActivePositioning()); } catch { setActive(null); }
    } catch {
      setError("定位报告加载失败，请稍后重试。");
    }
  }, [id]);

  useEffect(() => { void load(); }, [load]);

  if (error) return <main className="grid-shell min-h-screen p-10"><ErrorState message={error} /></main>;
  if (!data) return <main className="grid-shell min-h-screen p-10"><LoadingState message="加载定位报告中..." /></main>;

  return (
    <main className="grid-shell min-h-screen">
      <div className="mx-auto w-full max-w-6xl px-6 py-10 md:px-10">
        <PageHeader eyebrow="positioning / report" title={data.report_title} description={data.preview_text} />
        <section className="rounded-2xl border border-line bg-panel/90 p-5 text-sm text-subInk">
          <p>当前有效定位：{active ? active.preview_text : "暂无"}</p>
          <p className="mt-1">变化等级：{active?.change_level ?? "minor"}（规则比较）</p>
          <p className="mt-1">冻结状态：{active?.is_frozen ? "已冻结" : "未冻结"}</p>
          <div className="mt-3 flex gap-2">
            <button className="rounded border border-line px-3 py-2" onClick={async()=>{await setActivePositioning(id);await load();}}>将此版本设为当前定位</button>
            <button className="rounded border border-line px-3 py-2" onClick={async()=>{await freezePositioning(id);await load();}}>冻结此定位版本</button>
          </div>
        </section>
        <div className="mt-6 flex gap-3 text-sm">
          <Link href="/content-studio" className="rounded border border-line px-3 py-2">去内容台生成计划</Link>
          <Link href="/workspace" className="rounded border border-line px-3 py-2">返回工作台继续下一步</Link>
        </div>
      </div>
    </main>
  );
}
