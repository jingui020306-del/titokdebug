import { redirect } from "next/navigation";

export default function LegacyNicheMapReportPage({ params }: { params: { id: string } }) {
  redirect(`/positioning/report/${params.id}`);
}
