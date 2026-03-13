import type { ReportStatus } from "@/lib/api";

const statusCopy: Record<Exclude<ReportStatus, "ready">, { title: string; desc: string }> = {
  loading: { title: "报告生成中", desc: "系统正在处理你的体检数据，请稍后刷新。" },
  "insufficient-data": { title: "数据不足", desc: "近 30 天有效内容样本不足，建议补充发布后再体检。" },
  "permission-insufficient": { title: "授权不足", desc: "当前授权范围不足，无法生成完整诊断。" },
  error: { title: "生成失败", desc: "报告服务暂时异常，请稍后再试。" }
};

export function StatusPanel({ status, message }: { status: Exclude<ReportStatus, "ready">; message: string }) {
  const copy = statusCopy[status];

  return (
    <section className="rounded-2xl border border-line bg-panel/90 p-7 shadow-soft">
      <p className="text-xs uppercase tracking-[0.2em] text-subInk">状态</p>
      <h2 className="mt-3 text-2xl font-semibold">{copy.title}</h2>
      <p className="mt-3 text-subInk">{copy.desc}</p>
      <p className="mt-2 text-sm text-[#A7B7FF]">{message}</p>
    </section>
  );
}
