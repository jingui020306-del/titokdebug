export function PageHeader({
  eyebrow,
  title,
  description
}: {
  eyebrow: string;
  title: string;
  description?: string;
}) {
  return (
    <header className="border-l border-accent/60 pl-4 md:pl-6">
      <p className="text-xs uppercase tracking-[0.28em] text-subInk">{eyebrow}</p>
      <h1 className="mt-2 text-3xl font-semibold md:text-4xl">{title}</h1>
      {description ? <p className="mt-3 max-w-3xl text-sm leading-7 text-subInk md:text-base">{description}</p> : null}
    </header>
  );
}
