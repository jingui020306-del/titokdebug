import type { PatternItem } from "@/lib/api";

type Props = {
  title: string;
  items: PatternItem[];
  emptyText: string;
};

export function PatternsPreview({ title, items, emptyText }: Props) {
  return (
    <article className="rounded-2xl border border-line bg-panel/90 p-5">
      <p className="text-xs uppercase tracking-[0.16em] text-subInk">{title}</p>
      {items.length === 0 ? (
        <p className="mt-3 text-sm text-subInk">{emptyText}</p>
      ) : (
        <ul className="mt-3 space-y-2 text-sm text-subInk">
          {items.map((item) => (
            <li key={item.id} className="rounded-xl border border-line/70 bg-bg/60 p-3">
              <p className="font-medium text-ink">{item.label}</p>
              <p className="mt-1 text-xs">{item.summary}</p>
              <p className="mt-1 text-[11px] text-subInk">置信度 {item.confidence}% · {item.pattern_type}</p>
            </li>
          ))}
        </ul>
      )}
    </article>
  );
}
