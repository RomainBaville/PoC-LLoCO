# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025-2026 AKKODIS.
# SPDX-FileContributor: Romain Baville

from llm.summary.session_model import OptimizationSession


def build_session_summary_prompt( session: OptimizationSession ) -> str:
    """Build a generic, solver-aware explanation prompt.

    Args:
        session (OptimizationSession): The session with all the user data.

    Retruns:
        str: The prompt for the llm to summeryze the session.
    """
    steps_text = "\n".join( f"{ i + 1 }. { step }" for i, step in enumerate( session.steps ) )

    details_text = ""
    if session.result_details:
        details_text = "\n\nAdditional details:\n" + "\n".join(
            f"- { k }: { v }" for k, v in session.result_details.items()
        )

    config_text = ""
    if session.config_summary:
        config_text = f"\n\nConfiguration:\n{ session.config_summary }"

    return f"""
You are an expert optimization analyst.

Explain the result of the following optimization session in a clear,
professional, and neutral tone.

Problem type:
{ session.problem_type }

Workflow:
{ steps_text }

Data used:
{ session.data_description }

Solver:
{ session.solver_name + session.solver_description }

Result summary:
{ session.result_summary }
{ config_text }
{ details_text }

Guidelines:
- Be factual and precise
- Do not invent data
- Do not reference implementation details
- Do not mention programming languages
- Focus on decision rationale and outcome quality
"""
