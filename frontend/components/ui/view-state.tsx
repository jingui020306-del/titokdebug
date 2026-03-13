export function LoadingState({ message = "加载中..." }: { message?: string }) {
  return <div className="rounded-2xl border border-line bg-panel/80 p-6 text-sm text-subInk">{message}</div>;
}

export function EmptyState({ title, description }: { title: string; description: string }) {
  return (
    <div className="rounded-2xl border border-dashed border-line bg-panel/50 p-6">
      <p className="text-base font-medium">{title}</p>
      <p className="mt-2 text-sm text-subInk">{description}</p>
    </div>
  );
}

export function ErrorState({ message = "请求失败，请稍后重试。" }: { message?: string }) {
  return <div className="rounded-2xl border border-red-400/35 bg-red-400/5 p-6 text-sm text-red-200">{message}</div>;
}
