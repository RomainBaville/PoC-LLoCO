# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025-2026 AKKODIS.
# SPDX-FileContributor: Romain Baville

from llm.session_model import OptimizationSession


def build_session_summary_prompt(session: OptimizationSession) -> str:
    """
    Build a generic, solver-aware explanation prompt.
    """

    steps_text = "\n".join(
        f"{i + 1}. {step}" for i, step in enumerate(session.steps)
    )

    solver_text = (
        f"{session.solver_name}"
        + (f" ({session.solver_family})" if session.solver_family else "")
    )

    details_text = ""
    if session.result_details:
        details_text = "\n\nAdditional details:\n" + "\n".join(
            f"- {k}: {v}" for k, v in session.result_details.items()
        )

    return f"""
You are an expert optimization analyst.

Explain the result of the following optimization session in a clear,
professional, and neutral tone.

Problem family:
{session.problem_family}

Problem type:
{session.problem_type}

Formulation / variant:
{session.problem_variant}

Workflow:
{steps_text}

Data used:
{session.data_description}

Solver:
{solver_text}

Result summary:
{session.result_summary}
{details_text}

Guidelines:
- Be factual and precise
- Do not invent data
- Do not reference implementation details
- Do not mention programming languages
- Focus on decision rationale and outcome quality
"""
