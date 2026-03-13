import "./globals.css";
import type { Metadata } from "next";

import { TopNav } from "@/components/top-nav";

export const metadata: Metadata = {
  title: "creator-os",
  description: "让账号增长，从猜测变成诊断"
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="zh-CN">
      <body>
        <TopNav />
        {children}
      </body>
    </html>
  );
}
