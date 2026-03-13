import Link from "next/link";

import type { ReportData } from "@/lib/api";

function scoreBar(score: number) {
  return `${Math.max(8, Math.min(100, score))}%`;
}

const moduleLabel = {
  niche_map: "赛道地图",
  rewrite_engine: "改稿引擎",
  stay_in_account_audit: "继续账户体检"
} as const;

const moduleHref = {
  niche_map: "/niche-map",
  rewrite_engine: "/rewrite-engine",
  stay_in_account_audit: "/account-audit"
} as const;

export function ReportSections({ report }: { report: ReportData }) {
  return (
    <div className="space-y-5">
      <section className="rounded-2xl border border-line bg-panel/95 p-7 shadow-soft">
        <p className="text-xs uppercase tracking-[0.2em] text-subInk">顶部执行摘要</p>
        <h2 className="mt-3 text-2xl font-semibold leading-9">{report.executive_summary}</h2>
        <p className="mt-3 text-sm text-subInk">{report.bottleneck_explanation}</p>
      </section>

      <section className="grid gap-5 md:grid-cols-2">
        <article className="rounded-2xl border border-line bg-panel/90 p-6 shadow-soft">
          <p className="text-xs uppercase tracking-[0.2em] text-subInk">六维评分（策略雷达替代视图）</p>
          <div className="mt-4 space-y-3">
            {report.scores.map((item) => (
              <div key={item.name}>
                <div className="mb-1 flex items-center justify-between text-sm">
                  <span>{item.name}</span>
                  <span className="text-subInk">{item.score}</span>
                </div>
                <div className="h-2 rounded-full bg-[#1B2232]">
                  <div className="h-2 rounded-full bg-accent" style={{ width: scoreBar(item.score) }} />
                </div>
                <p className="mt-1 text-xs text-subInk">{item.reason}</p>
              </div>
            ))}
          </div>
        </article>

        <article className="rounded-2xl border border-line bg-panel/90 p-6 shadow-soft">
          <p className="text-xs uppercase tracking-[0.2em] text-subInk">主页改造建议卡</p>
          <div className="mt-4 space-y-3 text-sm">
            <p><span className="text-subInk">昵称建议：</span>{report.profile_rewrite_suggestions.nickname_suggestion}</p>
            <p><span className="text-subInk">Bio 建议：</span>{report.profile_rewrite_suggestions.bio_suggestion}</p>
            <p><span className="text-subInk">定位陈述：</span>{report.profile_rewrite_suggestions.profile_positioning_statement}</p>
          </div>
        </article>
      </section>

      <section className="grid gap-5 md:grid-cols-2">
        <article className="rounded-2xl border border-line bg-panel/90 p-6 shadow-soft">
          <p className="text-xs uppercase tracking-[0.2em] text-subInk">推荐内容支柱卡</p>
          <ul className="mt-4 space-y-3">
            {report.content_pillars.map((pillar) => (
              <li key={pillar.pillar} className="rounded-lg border border-line p-3 text-sm">
                <p className="font-medium">{pillar.pillar}</p>
                <p className="mt-1 text-subInk">为什么：{pillar.why}</p>
                <p className="mt-1 text-subInk">适合人群：{pillar.suitable_audience}</p>
              </li>
            ))}
          </ul>
        </article>

        <article className="rounded-2xl border border-line bg-panel/90 p-6 shadow-soft">
          <p className="text-xs uppercase tracking-[0.2em] text-subInk">未来 7 天行动清单卡</p>
          <ol className="mt-4 space-y-2 text-sm">
            {report.seven_day_action_plan.map((item) => (
              <li key={item.day} className="rounded-lg border border-line px-3 py-2">
                <span className="mr-2 text-subInk">{item.day.toUpperCase()}</span>
                {item.action}
              </li>
            ))}
          </ol>
        </article>
      </section>

      <section className="grid gap-5 md:grid-cols-2">
        <article className="rounded-2xl border border-line bg-panel/90 p-6 shadow-soft">
          <p className="text-xs uppercase tracking-[0.2em] text-subInk">核心问题 Top 3</p>
          <ul className="mt-4 space-y-2 text-sm text-subInk">
            {report.top_issues.map((issue) => (
              <li key={issue.issue} className="rounded-lg border border-line p-3">
                <p className="font-medium text-ink">{issue.issue}</p>
                <p className="mt-1">{issue.evidence}</p>
              </li>
            ))}
          </ul>
        </article>

        <article className="rounded-2xl border border-line bg-panel/90 p-6 shadow-soft">
          <p className="text-xs uppercase tracking-[0.2em] text-subInk">现在先避免</p>
          <ul className="mt-4 list-disc space-y-2 pl-5 text-sm text-subInk">
            {report.avoid_now.map((x) => (
              <li key={x}>{x}</li>
            ))}
          </ul>
        </article>
      </section>

      <section className="rounded-2xl border border-line bg-panel/90 p-6 shadow-soft">
        <p className="text-xs uppercase tracking-[0.2em] text-subInk">下一步模块推荐卡</p>
        <p className="mt-3 text-xl font-semibold">{moduleLabel[report.recommended_next_module]}</p>
        <p className="mt-2 text-sm text-subInk">{report.routing.reason}</p>
        <Link href={moduleHref[report.recommended_next_module]} className="mt-4 inline-block text-sm text-accent underline underline-offset-4">
          前往下一步
        </Link>
      </section>
    </div>
  );
}
