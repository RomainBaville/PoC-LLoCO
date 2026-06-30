# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025-2026 AKKODIS.
# SPDX-FileContributor: Romain Baville

"""LLM onboarding prompt builder.

Explains how the optimization platform works based entirely on registries
(problem families, assignment types, variants, and solvers).
"""

from llm.onboarding_context import build_onboarding_context


def build_onboarding_prompt(user_description: str) -> str:
    """Build a generic AI onboarding explanation aligned with platform registries.
    """
    context = build_onboarding_context()
    reward_text = ", ".join( context.get( "reward_functions", [] ) )
    penalty_text = ", ".join( context.get( "penalty_functions", [] ) )

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

Scoring functions (reward and penalty) available for advanced matching:
{reward_text} and {penalty_text}


Important concept:
For best-fit assignment, the platform allows configuring how matches are evaluated:
- a reward function (what makes a match valuable)
- an optional penalty function (what should be avoided)
- weights and configuration for fine-tuning behavior

Explain clearly:
- how the platform can model such problems
- how the user will progressively choose:
  1. problem type
  2. formulation
  3. data
  4. configuration (matching behavior)
  5. solver
- why configuration and scoring choices impact the result

Guidelines:
- Do NOT invent capabilities
- Do NOT mention internal code or implementation details
- Use clear, professional, user-facing language
"""
