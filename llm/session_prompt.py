# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025-2026 AKKODIS.
# SPDX-FileContributor: Romain Baville

from llm.session_model import OptimizationSession


def build_session_summary_prompt(session: OptimizationSession) -> str:
    """
    Build a generic explanation prompt for an optimization session.
    """

    steps_text = "\n".join(
        f"{i + 1}. {step}"
        for i, step in enumerate(session.steps)
    )

    details_text = ""
    if session.result_details:
        details_lines = [
            f"- {k}: {v}" for k, v in session.result_details.items()
        ]
        details_text = "\n\nAdditional result details:\n" + "\n".join(details_lines)

    solver_info = session.solver_name
    if session.solver_type:
        solver_info += f" ({session.solver_type})"

    return f"""
You are a professional optimization analyst.

You are explaining the result of an optimization session to a business or technical user.

Problem family:
{session.problem_family}

Problem variant:
{session.problem_variant}

User workflow:
{steps_text}

Data used:
{session.data_description}

Solver:
{solver_info}

Result:
{session.result_summary}
{details_text}

Write a clear, structured explanation that:
- explains what problem was solved
- summarizes how the user configured the problem
- explains how the result satisfies the constraints
- explains why the solution is efficient or reasonable

Rules:
- Be factual and concise
- Do NOT invent data
- Do NOT reference internal code
- Do NOT output markdown code blocks
"""
