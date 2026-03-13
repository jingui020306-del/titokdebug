import Link from "next/link";

type CardProps = {
  title: string;
  conclusion?: string;
  reason?: string;
  summary?: string;
  evidence?: string;
  actionLabel?: string;
  actionHref?: string;
  riskNote?: string;
  emphasis?: "normal" | "strong";
};

function SummaryCard({ title, conclusion, reason, summary, evidence, actionLabel, actionHref, riskNote, emphasis = "normal" }: CardProps) {
  const strong = emphasis === "strong";

  return (
    <article className={`flex min-h-[240px] flex-col rounded-2xl border bg-panel/90 p-5 ${strong ? "border-accent/80 shadow-soft" : "border-line"}`}>
      <p className="text-xs uppercase tracking-[0.16em] text-subInk">{title}</p>

      <div className="mt-3 rounded-xl border border-line/70 bg-bg/40 p-3">
        <p className="text-[11px] uppercase tracking-[0.14em] text-subInk">结论</p>
        <p className="mt-1 text-base font-semibold leading-7">{conclusion ?? summary ?? "待补充结论"}</p>
      </div>

      <div className="mt-3 rounded-xl border border-line/70 bg-bg/40 p-3">
        <p className="text-[11px] uppercase tracking-[0.14em] text-subInk">依据</p>
        <p className="mt-1 text-sm leading-6 text-subInk">{reason ?? evidence ?? "基于当前工作流阶段与最近复盘信号生成。"}</p>
      </div>

      {riskNote ? (
        <div className="mt-3 rounded-xl border border-amber-300/30 bg-amber-300/5 p-3">
          <p className="text-[11px] uppercase tracking-[0.14em] text-amber-200">风险提醒</p>
          <p className="mt-1 text-sm leading-6 text-amber-100/90">{riskNote}</p>
        </div>
      ) : null}

      {actionLabel && actionHref ? (
        <Link href={actionHref} className={`mt-auto inline-flex w-fit rounded border px-3 py-1.5 text-xs ${strong ? "border-accent text-ink" : "border-accent/70 text-ink"}`}>
          {actionLabel}
        </Link>
      ) : null}
    </article>
  );
}

export function FrontstageCardSkeleton() {
  return (
    <article className="min-h-[240px] animate-pulse rounded-2xl border border-line bg-panel/90 p-5">
      <div className="h-3 w-24 rounded bg-line/70" />
      <div className="mt-3 h-16 rounded bg-line/60" />
      <div className="mt-3 h-16 rounded bg-line/50" />
      <div className="mt-3 h-12 rounded bg-line/40" />
      <div className="mt-4 h-8 w-28 rounded bg-line/70" />
    </article>
  );
}

export function AccountStageCard(props: CardProps) { return <SummaryCard {...props} />; }
export function LearningTargetCard(props: CardProps) { return <SummaryCard {...props} />; }
export function GapSummaryCard(props: CardProps) { return <SummaryCard {...props} />; }
export function NextPostCard(props: CardProps) { return <SummaryCard {...props} />; }
export function WeeklyFocusCard(props: CardProps) { return <SummaryCard {...props} />; }
export function FrozenPositioningCard(props: CardProps) { return <SummaryCard {...props} />; }
export function BenchmarkAccountCard(props: CardProps) { return <SummaryCard {...props} />; }
export function UpgradeActionCard(props: CardProps) { return <SummaryCard {...props} />; }
export function PendingContentCard(props: CardProps) { return <SummaryCard {...props} />; }
export function PendingReviewCard(props: CardProps) { return <SummaryCard {...props} />; }
export function PatternAssetPreviewCard(props: CardProps) { return <SummaryCard {...props} />; }

export function NextStepCTA({
  title = "今日指令",
  conclusion,
  reason,
  description,
  primary,
  secondary,
  riskNote
}: {
  title?: string;
  conclusion?: string;
  reason?: string;
  description?: string;
  primary: { label: string; href: string };
  secondary?: { label: string; href: string };
  riskNote?: string;
}) {
  return (
    <section className="mt-6 rounded-2xl border border-accent/50 bg-panel/95 p-5">
      <p className="text-xs uppercase tracking-[0.16em] text-subInk">{title}</p>
      <p className="mt-2 text-lg font-semibold">{conclusion ?? "下一步执行指令"}</p>
      <p className="mt-2 text-sm text-subInk">{reason ?? description ?? "基于当前阶段与复盘结论生成。"}</p>
      {riskNote ? <p className="mt-2 text-xs text-amber-200">注意：{riskNote}</p> : null}
      <div className="mt-4 flex flex-wrap gap-3">
        <Link href={primary.href} className="rounded border border-accent px-3 py-2 text-sm">{primary.label}</Link>
        {secondary ? <Link href={secondary.href} className="rounded border border-line px-3 py-2 text-sm">{secondary.label}</Link> : null}
      </div>
    </section>
  );
}
