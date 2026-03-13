"use client";

import { useEffect, useState } from "react";

import { addProvider, deleteProvider, listProviders, patchProvider, type ProviderCredential, type ProviderMode } from "@/lib/api";

const providers = ["openai", "anthropic", "qwen", "deepseek", "other"] as const;

export default function ProvidersSettingsPage() {
  const [items, setItems] = useState<ProviderCredential[]>([]);
  const [mode, setMode] = useState<ProviderMode>("platform");
  const [apiKey, setApiKey] = useState("");
  const [providerName, setProviderName] = useState<(typeof providers)[number]>("openai");
  const [loading, setLoading] = useState(false);
  const [msg, setMsg] = useState("");

  const reload = async () => {
    const res = await listProviders();
    setItems(res.items);
    setMode(res.default_provider_mode);
  };

  useEffect(() => {
    void reload();
  }, []);

  const onAdd = async () => {
    if (!apiKey.trim()) return;
    setLoading(true);
    try {
      await addProvider({ owner_type: mode === "platform" ? "platform" : "user", provider_name: providerName, api_key: apiKey, is_active: items.length === 0 });
      setApiKey("");
      setMsg("已保存，前端仅显示 masked key。\n");
      await reload();
    } finally {
      setLoading(false);
    }
  };

  const onSetDefault = async (id: string) => {
    await patchProvider(id, { is_active: true });
    await reload();
  };

  const onDelete = async (id: string) => {
    await deleteProvider(id);
    await reload();
  };

  return (
    <main className="grid-shell min-h-screen">
      <div className="relative mx-auto w-full max-w-6xl px-6 py-12 md:px-10">
        <p className="text-xs uppercase tracking-[0.28em] text-subInk">settings / providers</p>
        <h1 className="mt-2 text-4xl font-semibold">模型与密钥管理</h1>
        <p className="mt-3 max-w-3xl text-subInk">
          平台托管模式：由平台代调用模型。用户自带 Key：你自己的 key，仅用于你的分析任务。
        </p>
        <p className="mt-2 text-xs text-subInk">TODO：接入真实用户鉴权后按用户隔离密钥与权限。</p>

        <section className="mt-8 grid gap-5 md:grid-cols-2">
          <article className="rounded-2xl border border-line bg-panel/90 p-6 shadow-soft">
            <h2 className="text-lg font-medium">添加 Provider Key</h2>
            <div className="mt-4 space-y-3">
              <select
                className="w-full rounded-lg border border-line bg-base px-3 py-2 text-sm"
                value={providerName}
                onChange={(e) => setProviderName(e.target.value as (typeof providers)[number])}
              >
                {providers.map((name) => (
                  <option key={name} value={name}>
                    {name}
                  </option>
                ))}
              </select>
              <select className="w-full rounded-lg border border-line bg-base px-3 py-2 text-sm" value={mode} onChange={(e) => setMode(e.target.value as ProviderMode)}>
                <option value="platform">平台托管模式</option>
                <option value="byok">用户自带 Key（BYOK）</option>
              </select>
              <input
                className="w-full rounded-lg border border-line bg-base px-3 py-2 text-sm"
                type="password"
                value={apiKey}
                onChange={(e) => setApiKey(e.target.value)}
                placeholder="输入 API Key（仅发送后端）"
              />
              <button
                type="button"
                disabled={loading}
                onClick={onAdd}
                className="rounded-lg border border-accent bg-accent/15 px-4 py-2 text-sm disabled:opacity-60"
              >
                {loading ? "保存中..." : "添加 key"}
              </button>
              {msg && <p className="text-xs text-[#A7B7FF]">{msg}</p>}
            </div>
          </article>

          <article className="rounded-2xl border border-line bg-panel/90 p-6 shadow-soft">
            <h2 className="text-lg font-medium">已绑定 Provider</h2>
            <ul className="mt-4 space-y-3 text-sm">
              {items.map((item) => (
                <li key={item.id} className="rounded-lg border border-line p-3">
                  <p>{item.provider_name} · {item.owner_type === "platform" ? "平台" : "BYOK"}</p>
                  <p className="mt-1 text-subInk">{item.masked_key}</p>
                  <div className="mt-3 flex gap-2">
                    <button type="button" onClick={() => onSetDefault(item.id)} className="rounded border border-line px-2 py-1 text-xs">
                      {item.is_active ? "默认中" : "设为默认 provider"}
                    </button>
                    <button type="button" onClick={() => onDelete(item.id)} className="rounded border border-line px-2 py-1 text-xs text-rose-300">
                      删除
                    </button>
                  </div>
                </li>
              ))}
              {items.length === 0 && <li className="text-subInk">暂无已绑定 provider。</li>}
            </ul>
          </article>
        </section>
      </div>
    </main>
  );
}
