"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";

const primaryLinks = [
  { href: "/", label: "首页" },
  { href: "/my-account", label: "我的账号" },
  { href: "/learn-from", label: "值得学的账号" },
  { href: "/upgrade-plan", label: "改造方案" },
  { href: "/execute", label: "内容执行" },
  { href: "/review", label: "复盘" }
] as const;

const secondaryLinks = [
  { href: "/history", label: "历史" },
  { href: "/review-lab/benchmarks", label: "资产" },
  { href: "/settings/providers", label: "设置" }
] as const;

export function TopNav() {
  const pathname = usePathname();

  const navClass = (href: string) => {
    const active = pathname === href || (href !== "/" && pathname.startsWith(href));
    return `whitespace-nowrap rounded border px-2.5 py-1.5 transition ${
      active ? "border-accent text-ink" : "border-line text-subInk hover:border-accent hover:text-ink"
    }`;
  };

  return (
    <header className="sticky top-0 z-40 border-b border-line/80 bg-[#070b14]/90 backdrop-blur">
      <nav className="mx-auto flex w-full max-w-7xl flex-wrap items-center gap-2 px-4 py-3 text-sm md:px-8">
        <div className="flex flex-wrap items-center gap-2">
          {primaryLinks.map((item) => (
            <Link key={item.href} href={item.href} className={navClass(item.href)}>
              {item.label}
            </Link>
          ))}
        </div>
        <div className="h-4 w-px bg-line/80" />
        <div className="flex flex-wrap items-center gap-2">
          {secondaryLinks.map((item) => (
            <Link key={item.href} href={item.href} className={navClass(item.href)}>
              {item.label}
            </Link>
          ))}
        </div>
      </nav>
    </header>
  );
}
