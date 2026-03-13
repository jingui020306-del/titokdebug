import Link from "next/link";

import { PageHeader } from "@/components/ui/page-header";

export default function HistoryPage() {
  return (
    <main className="grid-shell min-h-screen">
      <div className="mx-auto w-full max-w-5xl px-6 py-10 md:px-10">
        <PageHeader eyebrow="history / 统一历史入口" title="历史" description="按新闭环拆分查看：定位台历史、内容台历史、复盘台历史。" />
        <div className="mt-6 grid gap-3 md:grid-cols-3 text-sm">
          <Link href="/positioning/history" className="rounded-xl border border-line bg-panel/90 p-4">定位台历史</Link>
          <Link href="/content-studio/history" className="rounded-xl border border-line bg-panel/90 p-4">内容台历史</Link>
          <Link href="/review-lab/history" className="rounded-xl border border-line bg-panel/90 p-4">复盘台历史</Link>
        </div>
      </div>
    </main>
  );
}
