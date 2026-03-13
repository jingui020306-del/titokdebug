from __future__ import annotations

from app.decision.explain.prompt_templates import explain_prompt


class LlmExplainer:
    def explain(self, section: str, payload: dict) -> str:
        # LLM only for explanation; decision already produced by engines.
        return explain_prompt(section, payload)


llm_explainer = LlmExplainer()
