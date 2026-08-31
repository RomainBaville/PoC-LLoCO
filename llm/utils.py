# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025-2026 AKKODIS.
# SPDX-FileContributor: Romain Baville

from llm.client.llama_client import ask_llama_client

# ── Problem configuration inference ─────────────────────────────────────────
def infer_problem_configuration( user_desc: str, ai_text: str | None = None ) -> dict:
    """Deterministic keyword-based recommendation — no extra LLM call."""
    text = f"{user_desc}\n{ai_text or ''}".lower()

    assignment_keywords = [
        "assign",
        "affect",
        "affectation",
        "affecter",
        "assignment",
        "employee",
        "employé",
        "project",
        "projet",
        "skill",
        "compétence",
        "competence",
    ]
    if not any( w in text for w in assignment_keywords ):
        return {}

    problem_key = "assignment"

    return {
        "problem_key": problem_key,
    }


# ── Helpers ──────────────────────────────────────────────────────────────────
def _llm_ask( prompt: str, source: str, model_name: str ) -> str:
    if source == "akkodis":
        from llm.client.akkodis_client import ask_akkodis_client as akkodis_ask
        return akkodis_ask( prompt, model_name )
    else:
        import llm.client.llama_client as _llm
        _llm.LLM_SERVER_URL = st.session_state.llm_url
        _llm.LLM_MODEL_NAME = model_name
        return ask_llama_client( prompt )

