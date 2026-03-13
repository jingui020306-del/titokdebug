"use client";

import Link from "next/link";
import { useParams } from "next/navigation";
import { useEffect, useState } from "react";

import { PageHeader } from "@/components/ui/page-header";
import { ErrorState, LoadingState } from "@/components/ui/view-state";
import { getReviewCompare, getReviewLabReport, type BenchmarkCompareData, type ReviewLabReport } from "@/lib/api";

export default function ReviewLabReportPage() {
  const { id } = useParams<{ id: string }>();
  const [data, setData] = useState<ReviewLabReport | null>(null);
  const [compare, setCompare] = useState<BenchmarkCompareData | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const load = async () => {
      try {
        setError(null);
        const report = await getReviewLabReport(id);
        setData(report);
        try { setCompare(await getReviewCompare(id)); } catch { setCompare(null); }
      } catch {
        setError("复盘报告加载失败，请稍后重试。");
      }
    };
    void load();
  }, [id]);

  if (error) return <main className="grid-shell min-h-screen p-10"><ErrorState message={error} /></main>;
  if (!data) return <main className="grid-shell min-h-screen p-10"><LoadingState message="加载复盘报告中..." /></main>;

  return (
    <main className="grid-shell min-h-screen">
      <div className="mx-auto w-full max-w-6xl px-6 py-10 md:px-10">
        <PageHeader eyebrow="review-lab / report" title="对标驱动复盘报告" description={data.performance_summary} />

        <section className="mt-5 grid gap-5 md:grid-cols-2">
          <article className="rounded-2xl border border-line bg-panel/90 p-5">
            <p className="text-xs text-subInk">这次学的是哪类强账号模式</p>
            <p className="mt-2 text-sm text-subInk">{data.best_account_playbook_match}</p>
            <p className="mt-1 text-sm text-subInk">有没有更接近有效模式：{data.upgrade_progress_assessment}</p>
          </article>
          <article className="rounded-2xl border border-line bg-panel/90 p-5">
            <p className="text-xs text-subInk">咨询转化真值</p>
            <p className="mt-2 text-sm text-subInk">{data.consultation_performance_summary}</p>
            <p className="mt-1 text-sm text-subInk">信号：{data.consultation_quality_signal}</p>
            <p className="mt-1 text-sm text-subInk">评估：{data.conversion_readiness_assessment}</p>
          </article>
        </section>

        <section className="mt-5 rounded-2xl border border-line bg-panel/90 p-5">
          <p className="text-xs text-subInk">差距 → 改法（Gap to Action）</p>
          {compare ? (
            <ul className="mt-2 list-disc pl-5 text-sm text-subInk">
              {compare.benchmark_gap_summary.items.map((x, i) => <li key={i}>{x.dimension}：{x.suggested_change}（{x.urgency}）</li>)}
            </ul>
          ) : <p className="mt-2 text-sm text-subInk">暂无可用对标池，先去 discovery 建立学习对象。</p>}
        </section>

        <section className="mt-5 rounded-2xl border border-line bg-panel/90 p-5">
          <p className="text-xs text-subInk">下一轮动作</p>
          <ul className="mt-2 list-disc pl-5 text-sm text-subInk">{data.next_iteration_actions.map((x) => <li key={x}>{x}</li>)}</ul>
        </section>

        <div className="mt-6 flex gap-3 text-sm">
          <Link href="/review-lab/discovery" className="rounded border border-line px-3 py-2">继续强账号发现</Link>
          <Link href="/content-studio" className="rounded border border-line px-3 py-2">去内容台执行下一条</Link>
          <Link href="/workspace" className="rounded border border-line px-3 py-2">返回工作台继续下一步</Link>
        </div>
      </div>
    </main>
  );
}
