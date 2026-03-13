import { redirect } from "next/navigation";

export default function LegacyAccountAuditReportPage({ params }: { params: { id: string } }) {
  redirect(`/positioning/report/${params.id}`);
}
