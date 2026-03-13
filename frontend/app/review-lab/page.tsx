import Link from "next/link";

import { PageHeader } from "@/components/ui/page-header";

export default function ReviewLabPage() {
  return (
    <main className="grid-shell min-h-screen">
      <div className="mx-auto w-full max-w-6xl px-6 py-10 md:px-10">
        <PageHeader eyebrow="review-lab / 复盘台" title="复盘台" description="记录发布结果、识别瓶颈层级、决定下一轮动作。" />
        <div className="mt-6 flex gap-3 text-sm">
          <Link href="/review-lab/new" className="rounded border border-accent px-3 py-2">新建复盘</Link>
          <Link href="/review-lab/history" className="rounded border border-line px-3 py-2">查看复盘历史</Link>
          <Link href="/review-lab/discovery" className="rounded border border-line px-3 py-2">强账号发现</Link>
          <Link href="/review-lab/benchmarks" className="rounded border border-line px-3 py-2">对标池</Link>
        </div>
      </div>
    </main>
  );
}
