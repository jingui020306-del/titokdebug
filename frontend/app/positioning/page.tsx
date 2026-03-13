"use client";

import { useRouter } from "next/navigation";
import { useEffect, useState } from "react";

import { PageHeader } from "@/components/ui/page-header";
import { EmptyState, LoadingState } from "@/components/ui/view-state";
import { createPositioning, getDouyinOAuthStart, getDouyinOAuthStatus, type DouyinStatus } from "@/lib/api";

export default function PositioningPage() {
  const router = useRouter();
  const [oauth, setOauth] = useState<DouyinStatus | null>(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    void getDouyinOAuthStatus().then(setOauth).catch(() => setOauth(null));
  }, []);

  const onConnect = async () => {
    setLoading(true);
    try {
      const res = await getDouyinOAuthStart();
      if (res.configured) window.location.href = res.authorize_url;
      else {
        const job = await createPositioning({ account_id: `fallback_${Date.now()}`, nickname: "基础体验账号", source_type: "mock" });
        router.push(`/positioning/report/${job.job_id}`);
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="grid-shell min-h-screen">
      <div className="mx-auto w-full max-w-6xl px-6 py-10 md:px-10">
        <PageHeader eyebrow="positioning / 定位台" title="定位台" description="判断你是谁、你服务谁、该发什么、主页怎么写。" />
        <section className="mt-6 rounded-2xl border border-line bg-panel/90 p-6">
          <p className="text-sm text-subInk">授权说明：使用抖音官方 OAuth，不保存账号密码，仅用于你的账号分析与复盘。</p>
          <p className="mt-2 text-sm text-subInk">授权状态：{oauth?.status ?? "未检测"}{oauth?.fallback_mode ? "（开发fallback）" : ""}</p>
          <button type="button" onClick={onConnect} disabled={loading} className="mt-4 rounded border border-accent bg-accent/10 px-4 py-2 text-sm disabled:opacity-60">{loading ? "处理中..." : "连接抖音账号"}</button>
        </section>
        <section className="mt-6">
          {oauth ? null : <LoadingState message="正在检测授权状态..." />}
          <div className="mt-4"><EmptyState title="还没有定位报告" description="连接账号后将自动生成一份定位决策报告。" /></div>
        </section>
      </div>
    </main>
  );
}
