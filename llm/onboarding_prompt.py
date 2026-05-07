# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025-2026 AKKODIS.
# SPDX-FileContributor: Romain Baville

from llm.onboarding_context import build_onboarding_context


def build_onboarding_prompt(user_description: str) -> str:
    """
    Build a generic, registry-driven onboarding prompt.
    """

    context = build_onboarding_context()

    problem_list = "\n".join(
        f"- {p['label']}"
        for p in context["problems"]
    )

    data_source_list = "\n".join(
        f"- {ds['label']}: {ds['description']}"
        for ds in context["data_sources"]
    )

    solver_text = []
    for problem_type, variants in context["solvers"].items():
        for variant, solvers in variants.items():
            solver_text.append(
                f"- {problem_type} / {variant}: {', '.join(solvers)}"
            )

    solver_list = "\n".join(solver_text)

    return f"""
You are an intelligent assistant guiding a user through an optimization platform.

The user describes their problem as follows:
\"\"\"
{user_description}
\"\"\"

The platform supports the following types of optimization problems:
{problem_list}

Depending on the problem type, the platform may ask the user to:
- choose a specific formulation or variant
- describe entities and constraints
- provide data using one of the supported data formats
- select an appropriate solver
- review and export results with an AI-generated explanation

Supported data input formats include:
{data_source_list}

Available solvers (by problem type and formulation):
{solver_list}

Your task:
- Explain how this platform can help solve the user's problem
- Describe the general workflow WITHOUT listing exact UI step numbers
- Emphasize that the interface adapts dynamically based on user choices
- Encourage the user to proceed step by step

Rules:
- Do NOT invent features
- Do NOT mention implementation details
- Do NOT generate code
- Be clear, concise, and reassuring
"""
