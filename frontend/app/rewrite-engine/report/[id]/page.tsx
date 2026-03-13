import { redirect } from "next/navigation";

export default function LegacyRewriteReportPage({ params }: { params: { id: string } }) {
  redirect(`/content-studio/rewrite/${params.id}`);
}
