import Link from "next/link";

import { PageHeader } from "@/components/ui/page-header";

export default function DashboardPage() {
  return (
    <main className="grid-shell min-h-screen">
      <div className="mx-auto w-full max-w-6xl px-6 py-10 md:px-10">
        <PageHeader eyebrow="dashboard / 单账号总览" title="数据总览" description="这里展示改造进度概览，主入口仍是 workspace 的“今日改造动作”。" />
        <section className="mt-6 rounded-2xl border border-line bg-panel/90 p-6 text-sm text-subInk">
          当前产品闭环：定位台 → 内容台 → 发布 → 复盘台 → 再定位。
        </section>
        <div className="mt-6 flex gap-3 text-sm">
          <Link href="/workspace" className="rounded border border-accent px-3 py-2">进入工作台</Link>
          <Link href="/positioning" className="rounded border border-line px-3 py-2">进入定位台</Link>
          <Link href="/content-studio" className="rounded border border-line px-3 py-2">进入内容台</Link>
          <Link href="/review-lab" className="rounded border border-line px-3 py-2">进入复盘台</Link>
        </div>
      </div>
    </main>
  );
}
