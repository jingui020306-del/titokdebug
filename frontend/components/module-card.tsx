import Link from "next/link";

type ModuleCardProps = {
  title: string;
  subtitle: string;
  href?: string;
  enabled: boolean;
};

export function ModuleCard({ title, subtitle, href, enabled }: ModuleCardProps) {
  const cardBody = (
    <article className="group relative h-full rounded-2xl border border-line bg-panel/95 p-7 shadow-soft transition hover:border-accent/60">
      <div className="mb-6 flex items-center justify-between">
        <h2 className="text-2xl font-semibold tracking-wide">{title}</h2>
        <span className={`rounded-md px-2 py-1 text-xs ${enabled ? "terminal-chip" : "border border-line text-subInk"}`}>
          {enabled ? "进入模块" : "即将开放"}
        </span>
      </div>
      <p className="text-sm leading-7 text-subInk">{subtitle}</p>
      {enabled && <p className="mt-7 text-xs uppercase tracking-[0.25em] text-accent">Tap to continue →</p>}
    </article>
  );

  if (!enabled || !href) {
    return <div className="h-full">{cardBody}</div>;
  }

  return (
    <Link href={href} className="block h-full focus:outline-none focus-visible:ring-2 focus-visible:ring-accent">
      {cardBody}
    </Link>
  );
}
