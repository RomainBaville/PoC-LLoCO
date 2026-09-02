# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025-2026 AKKODIS.
# SPDX-FileContributor: Romain Baville


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
