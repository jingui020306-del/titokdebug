export type ReportStatus = "loading" | "ready" | "insufficient-data" | "permission-insufficient" | "error";
export type JobStatus = "created" | "syncing_fast" | "fast_ready" | "syncing_deep" | "deep_ready" | "failed";

type ApiResponse<T> = { success: boolean; data: T | null; error: string | null; meta?: Record<string, unknown> | null };

export type ReportData = {
  job_id: string;
  report_title: string;
  preview_text: string;
  summary: string;
  executive_summary: string;
  scores: Array<{ name: string; score: number; reason: string }>;
  top_issues: Array<{ issue: string; severity: "low" | "medium" | "high"; evidence: string }>;
  profile_diagnosis: Record<string, string>;
  content_diagnosis: Record<string, string>;
  growth_bottleneck: Record<string, string>;
  bottleneck_explanation: string;
  risk_alerts: string[];
  action_plan: Array<{ phase: "7d" | "30d" | "60d"; action: string; expected_outcome: string }>;
  profile_rewrite_suggestions: { nickname_suggestion: string; bio_suggestion: string; profile_positioning_statement: string };
  content_pillars: Array<{ pillar: string; why: string; suitable_audience: string }>;
  seven_day_action_plan: Array<{ day: "day1" | "day2" | "day3" | "day4" | "day5" | "day6" | "day7"; action: string }>;
  avoid_now: string[];
  routing: { recommended_module: string; reason: string; next_step: string };
  recommended_next_module: "niche_map" | "rewrite_engine" | "stay_in_account_audit";
};
export type ReportResponse = { status: ReportStatus; message: string; data: ReportData | null };
export type HistoryItem = { id: string; source_type: "mock" | "oauth"; status: JobStatus; report_mode_available: Array<"fast" | "deep">; created_at: string; updated_at: string; account_nickname: string };

export type TodoItem = {
  id: string; user_id: string; title: string; source_module: "positioning" | "content_studio" | "review_lab" | "workspace";
  source_report_id: string | null; priority: "high" | "medium" | "low"; status: "todo" | "in_progress" | "paused" | "done";
  action_type: "rewrite_profile" | "generate_weekly_plan" | "rewrite_single_post" | "fill_review" | "scale_pillar" | "stop_direction";
  suggested_due_label: string; created_at: string; updated_at: string;
};
export type PatternItem = {
  id: string; user_id: string; pattern_type: "title_style" | "hook_style" | "pillar" | "profile_expression" | "conversion_cta" | "risk_direction";
  label: string; summary: string; evidence_source: string; confidence: number; current_status: "candidate" | "validated" | "deprecated";
  created_at: string; updated_at: string;
};
export type TimelineItem = { id: string; event_type: string; title: string; summary: string; created_at: string };
export type WorkflowRecommendationSummary = { current_workflow_stage: string; best_next_action: string; best_next_action_reason: string };

export type WorkspaceSummary = {
  latest_positioning_summary: string;
  active_content_plan_summary: string;
  latest_review_summary: string;
  current_best_next_step: string;
  current_workflow_stage: string;
  best_next_action: string;
  best_next_action_reason: string;
  pending_content_items: number;
  unpublished_adopted_items: number;
  unreviewed_published_items: number;
  recent_7d_consultation_content_count: number;
  recent_7d_total_inquiries: number;
  top_consultation_pillar: string;
  active_frozen_positioning: string;
  benchmark_pool_size: number;
  strongest_accounts_to_learn: string[];
  current_main_gap: string;
  current_upgrade_focus: string;
  next_post_recommendation: Record<string, string>;
  why_next_post_now: string;
  current_learning_target: string;
  upgrade_plan_progress: string;
  todo_list: TodoItem[];
  learned_patterns_preview: PatternItem[];
  stopped_directions_preview: PatternItem[];
  best_to_scale_pattern: PatternItem | null;
  workflow_recommendation: WorkflowRecommendationSummary;
  decision_cards?: Record<string, Record<string, string>>;
};
export type WorkspaceTimeline = { positioning_shifts: TimelineItem[]; pillar_shifts: TimelineItem[]; recent_reviews: TimelineItem[]; validated_patterns: PatternItem[]; stopped_directions: PatternItem[]; timeline_items: TimelineItem[] };


export type CurrentBestNextStepSummary = { action: string; reason: string; href: string };

export type HomeSummary = {
  account_stage: string;
  learning_target: string;
  main_gap: string;
  next_post: Record<string, string>;
  weekly_focus: string;
  best_next_action: string;
  best_next_action_reason: string;
  decision_cards?: Record<string, Record<string, string>>;
  douyin_status: string;
  last_review_time: string;
};

export type MyAccountSummary = {
  current_positioning_summary: string;
  account_stage: string;
  active_positioning: Record<string, unknown> | null;
  frozen: boolean;
  three_pillars: string[];
  off_limits: string[];
  evidence_chain: string[];
  next_actions: string[];
};

export type LearnFromSummary = {
  benchmark_pool_size: number;
  top_accounts: BenchmarkAccountSummary[];
  entry_actions: string[];
  recent_added: string[];
  priority_samples: string;
};

export type UpgradePlanSummary = {
  current_main_gap: string;
  top3_changes: string[];
  profile_upgrade: string[];
  content_structure_upgrade: string[];
  content_type_upgrade: string[];
  next_7_posts: string[];
};

export type ExecuteSummary = {
  weekly_plan_summary: string;
  next_post_recommendation: Record<string, string>;
  pending_publish: number;
  recent_rewrites: string;
  benchmark_learning_preview: string[];
  actions: string[];
};

export type ReviewSummary = {
  latest_review_summary: string;
  best_pillar: string;
  best_content_type: string;
  stopped_directions: string[];
  latest_better_or_worse: string;
  actions: string[];
};

export type ReviewLabReport = {
  performance_summary: string;
  self_comparison: string;
  pillar_comparison: string;
  benchmark_comparison: string;
  best_account_playbook_match: string;
  content_type_assessment: string;
  consultation_performance_summary: string;
  upgrade_progress_assessment: string;
  decision: Record<string, string>;
  next_iteration_actions: string[];
  linked_content_context: Record<string, string>;
  comparison_summary: string;
  previous_version_comparison: Record<string, string | number>;
  pillar_benchmark: Record<string, string | number | boolean>;
  strategy_window_comparison: Record<string, string | number>;
  consultation_quality_signal: string;
  conversion_readiness_assessment: string;
};
export type ReviewHistoryItem = {
  review_id: string; created_at: string; content_title: string; content_pillar: string; major_metrics: string;
  comparison_signal: string; worth_scaling: string; bottleneck_stage: string; decision: string; next_action: string; pattern_impact: string;
};

export type ContentItemSummary = {
  id: string; title_or_working_title: string; pillar: string; content_goal: string;
  status: "planned" | "drafted" | "adopted" | "published" | "reviewed" | "archived";
  chosen_version_id: string | null; latest_publish_record_id: string | null; latest_review_id: string | null; updated_at: string;
};
export type ContentVersionSummary = { id: string; content_item_id: string; version_label: string; title: string; hook: string; is_adopted: boolean; created_at: string };
export type PublishRecordSummary = { id: string; content_item_id: string; version_id: string | null; platform: string; published_at: string; views: number; inquiry_count: number; conversion_count: number };
export type ContentItemDetail = { item: ContentItemSummary; chosen_version: ContentVersionSummary | null; versions: ContentVersionSummary[]; publish_records: PublishRecordSummary[]; latest_review_summary: string; next_action: string };
export type ContentItemTimeline = { item_id: string; timeline: TimelineItem[] };

export type PositioningVersionSummary = {
  positioning_version_id: string; job_id: string; report_title: string; preview_text: string;
  is_active: boolean; is_frozen: boolean; frozen_at: string | null; supersedes_version_id: string | null; change_level: "minor" | "moderate" | "major"; created_at: string;
};

export type ProviderMode = "platform" | "byok";
export type ProviderCredential = { id: string; owner_type: "platform" | "user"; provider_name: "openai" | "anthropic" | "qwen" | "deepseek" | "other"; masked_key: string; is_active: boolean; created_at: string };
export type DouyinStatus = { status: "未连接" | "已连接" | "access_token即将过期" | "需要重新授权"; fallback_mode: boolean; authorized_at?: string; scope_list: string[]; message: string };

const API_BASE = process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8000";

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const res = await fetch(`${API_BASE}${path}`, {
    ...init,
    headers: { "Content-Type": "application/json", "x-user-id": "dev-user", ...(init?.headers ?? {}) },
    cache: "no-store"
  });
  if (!res.ok) throw new Error(`API request failed: ${res.status}`);
  return (await res.json()) as T;
}
async function requestApiData<T>(path: string, init?: RequestInit): Promise<T> {
  const res = await request<ApiResponse<T>>(path, init);
  if (!res.success || !res.data) throw new Error(res.error ?? "API response invalid");
  return res.data;
}

export async function createSeedAllDemo() { return request<{ status: string }>("/api/v1/dev/seed-all-demo", { method: "POST" }); }
export async function getFastReport(jobId: string) { return request<ReportResponse>(`/api/v1/account-audit/${jobId}/fast-report`); }
export async function getDeepReport(jobId: string) { return request<ReportResponse>(`/api/v1/account-audit/${jobId}/deep-report`); }

export async function getWorkspaceSummary() { return requestApiData<WorkspaceSummary>("/api/v1/workspace/summary"); }
export async function getWorkspaceTimeline() { return requestApiData<WorkspaceTimeline>("/api/v1/workspace/timeline"); }
export async function updateWorkspaceTodo(todoId: string, status: TodoItem["status"]) { return requestApiData<{ todo_id: string; status: TodoItem["status"] }>(`/api/v1/workspace/todos/${todoId}`, { method: "PATCH", body: JSON.stringify({ status }) }); }

export async function getDouyinOAuthStatus() { return request<DouyinStatus>("/api/v1/douyin/oauth/status"); }
export async function getDouyinOAuthStart() { return request<{ authorize_url: string; configured: boolean; message: string }>("/api/v1/douyin/oauth/start"); }

export async function createPositioning(payload: { account_id: string; nickname: string; source_type?: "mock" | "oauth" }) { return request<{ job_id: string; status: string; message: string }>("/api/v1/positioning/mock-create", { method: "POST", body: JSON.stringify(payload) }); }
export async function getPositioningReport(jobId: string) { return request<{ status: string; message: string; data: ReportData | null }>(`/api/v1/positioning/${jobId}/report`); }
export async function getPositioningHistory() { return requestApiData<PositioningVersionSummary[]>("/api/v1/positioning/history"); }
export async function freezePositioning(jobId: string) { return requestApiData<{ job_id: string; status: string }>(`/api/v1/positioning/${jobId}/freeze`, { method: "POST" }); }
export async function setActivePositioning(jobId: string) { return requestApiData<{ job_id: string; status: string }>(`/api/v1/positioning/${jobId}/set-active`, { method: "POST" }); }
export async function getActivePositioning() { return requestApiData<PositioningVersionSummary>("/api/v1/positioning/active"); }

export async function createContentPlan(payload: Record<string, unknown>) { return request<{ plan_id: string; status: string }>("/api/v1/content-studio/plan/mock-create", { method: "POST", body: JSON.stringify(payload) }); }
export async function getContentPlan(planId: string) { return request<{ status: string; data: any }>(`/api/v1/content-studio/plan/${planId}`); }
export async function createContentRewrite(payload: Record<string, unknown>) { return request<{ rewrite_id: string; status: string }>("/api/v1/content-studio/rewrite/mock-create", { method: "POST", body: JSON.stringify(payload) }); }
export async function getContentRewrite(rewriteId: string) { return request<{ status: string; data: any }>(`/api/v1/content-studio/rewrite/${rewriteId}`); }
export async function adoptContentRewrite(rewriteId: string) { return request<{ status: string; message: string; version_id: string }>(`/api/v1/content-studio/rewrite/${rewriteId}/adopt`, { method: "POST" }); }
export async function getContentStudioHistory() { return request<{ items: Array<{ id: string; kind: string; created_at: string; title: string; status: string }> }>("/api/v1/content-studio/history"); }
export async function getContentItems() { return requestApiData<ContentItemSummary[]>("/api/v1/content-studio/items"); }
export async function getContentItem(id: string) { return requestApiData<ContentItemDetail>(`/api/v1/content-studio/items/${id}`); }
export async function getContentItemVersions(id: string) { return requestApiData<ContentVersionSummary[]>(`/api/v1/content-studio/items/${id}/versions`); }
export async function getContentItemTimeline(id: string) { return requestApiData<ContentItemTimeline>(`/api/v1/content-studio/items/${id}/timeline`); }
export async function markContentPublished(id: string, payload: Record<string, unknown>) { return requestApiData<{ item_id: string; publish_record_id: string }>(`/api/v1/content-studio/items/${id}/mark-published`, { method: "POST", body: JSON.stringify(payload) }); }
export async function archiveContentItem(id: string) { return requestApiData<{ item_id: string; status: string }>(`/api/v1/content-studio/items/${id}/archive`, { method: "POST" }); }

export async function createReviewLab(payload: Record<string, unknown>) { return requestApiData<{ review_id: string; status: string }>("/api/v1/review-lab/new", { method: "POST", body: JSON.stringify(payload) }); }
export async function getReviewLabReport(id: string) { return requestApiData<ReviewLabReport>(`/api/v1/review-lab/report/${id}`); }
export async function getReviewLabHistory(pillar?: string) { return requestApiData<ReviewHistoryItem[]>(`/api/v1/review-lab/history${pillar ? `?pillar=${encodeURIComponent(pillar)}` : ""}`); }

export async function listProviders() { return request<{ default_provider_mode: ProviderMode; items: ProviderCredential[] }>("/api/v1/settings/providers"); }
export async function addProvider(payload: { owner_type: "platform" | "user"; provider_name: ProviderCredential["provider_name"]; api_key: string; is_active: boolean }) { return request<{ data: ProviderCredential }>("/api/v1/settings/providers", { method: "POST", body: JSON.stringify(payload) }); }
export async function patchProvider(id: string, payload: { is_active?: boolean }) { return request<{ data: ProviderCredential }>(`/api/v1/settings/providers/${id}`, { method: "PATCH", body: JSON.stringify(payload) }); }
export async function deleteProvider(id: string) { return request<{ status: string }>(`/api/v1/settings/providers/${id}`, { method: "DELETE" }); }


export type BenchmarkAccountSummary = { id: string; account_name: string; platform: string; account_url: string; account_tier: "head" | "mid" | "peer"; similarity_reason: string; learnability_reason: string; positioning_summary: string; why_selected: string; notes?: string | null; source_mode: "manual" | "discovered" | "import"; created_at: string; updated_at: string };
export type DiscoveryCandidate = { account_name: string; platform: string; account_url: string; similarity_reason: string; learnability_reason: string; learn_target: string; should_add: boolean };
export type BenchmarkContentSample = { id: string; benchmark_account_id: string; title: string; sample_url?: string; content_type: string; pillar_guess: string; hook_style: string; conversion_style: string; sample_heat_level: "normal" | "strong" | "viral"; why_it_worked: string; created_at: string; updated_at: string };
export type BenchmarkCompareData = { benchmark_gap_summary: { benchmark_account_id: string; items: Array<Record<string, string>> }; account_upgrade_plan: { next_7_post_strategy: Array<Record<string, string>> } };


export async function discoverySearch(payload: Record<string, unknown>) { return requestApiData<DiscoveryCandidate[]>("/api/v1/review-lab/discovery/search", { method: "POST", body: JSON.stringify(payload) }); }
export async function discoveryConfirm(candidates: DiscoveryCandidate[]) { return requestApiData<BenchmarkAccountSummary[]>("/api/v1/review-lab/discovery/confirm", { method: "POST", body: JSON.stringify({ candidates }) }); }
export async function listBenchmarks() { return requestApiData<BenchmarkAccountSummary[]>("/api/v1/review-lab/benchmarks"); }
export async function createBenchmark(payload: Record<string, unknown>) { return requestApiData<BenchmarkAccountSummary>("/api/v1/review-lab/benchmarks", { method: "POST", body: JSON.stringify(payload) }); }
export async function getBenchmark(id: string) { return requestApiData<BenchmarkAccountSummary>(`/api/v1/review-lab/benchmarks/${id}`); }
export async function patchBenchmark(id: string, payload: Record<string, unknown>) { return requestApiData<BenchmarkAccountSummary>(`/api/v1/review-lab/benchmarks/${id}`, { method: "PATCH", body: JSON.stringify(payload) }); }
export async function listBenchmarkSamples(id: string) { return requestApiData<BenchmarkContentSample[]>(`/api/v1/review-lab/benchmarks/${id}/samples`); }
export async function createBenchmarkSample(id: string, payload: Record<string, unknown>) { return requestApiData<BenchmarkContentSample>(`/api/v1/review-lab/benchmarks/${id}/samples`, { method: "POST", body: JSON.stringify(payload) }); }
export async function getReviewCompare(id: string) { return requestApiData<BenchmarkCompareData>(`/api/v1/review-lab/compare/${id}`); }
export async function getContentStudioNextPost() { return requestApiData<Record<string, unknown>>("/api/v1/content-studio/next-post"); }


export async function getHomeSummary() { return requestApiData<HomeSummary>("/api/v1/home/summary"); }
export async function getMyAccountSummary() { return requestApiData<MyAccountSummary>("/api/v1/my-account/summary"); }
export async function getLearnFromSummary() { return requestApiData<LearnFromSummary>("/api/v1/learn-from/summary"); }
export async function getUpgradePlanSummary() { return requestApiData<UpgradePlanSummary>("/api/v1/upgrade-plan/summary"); }
export async function getExecuteSummary() { return requestApiData<ExecuteSummary>("/api/v1/execute/summary"); }
export async function getReviewSummary() { return requestApiData<ReviewSummary>("/api/v1/review/summary"); }
