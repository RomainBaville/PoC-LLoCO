# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025-2026 AKKODIS.
# SPDX-FileContributor: Romain Baville

"""
LLM onboarding prompt builder.

Explains how the optimization platform works based entirely on registries
(problem families, assignment types, variants, and solvers).
"""

from llm.onboarding_context import build_onboarding_context


def build_onboarding_prompt(user_description: str) -> str:
    """
    Build a generic AI onboarding explanation aligned with platform registries.
    """

    context = build_onboarding_context()

    # -------------------------------
    # Assignment types & variants
    # -------------------------------
    assignment_text = "\n".join(
        f"- {t['label']}: {', '.join(t['variants'])}"
        for t in context.get("assignment_types", [])
    )

    # -------------------------------
    # Solvers
    # -------------------------------
    solver_text = "\n".join(
        f"- {t['label']}: {', '.join(t['solvers'])}"
        for t in context.get("assignment_types", [])
        if t.get("solvers")
    )

    return f"""
You are an AI assistant helping a user understand how to use
an optimization platform.

The user describes their problem as follows:

\"\"\"
{user_description}
\"\"\"

The platform supports structured optimization problems, including
assignment problems with different semantic types and formulations.

Assignment types and available formulations:
{assignment_text}

Available solvers:
{solver_text}

Explain clearly:
- how the platform can model such problems
- how the user will progressively choose the problem type,
  formulation, data, and solver
- why choosing an appropriate solver matters

Guidelines:
- Do NOT invent capabilities
- Do NOT mention internal code or implementation details
- Use clear, professional, user-facing language
"""
