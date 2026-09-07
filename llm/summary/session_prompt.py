# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025-2026 AKKODIS.
# SPDX-FileContributor: Romain Baville

from domain.registry import DOMAIN_REGISTRY
from llm.summary.session_model import OptimizationSession


def build_session_summary_prompt( session: OptimizationSession ) -> str:
    """Build a generic, solver-aware explanation prompt.

    Args:
        session (OptimizationSession): The session with all the user data.

    Retruns:
        str: The prompt for the llm to summeryze the session.
    """
    user_desc: str
    if session.user_desc is None:
        user_desc = "No description was given."
    else:
        user_desc = session.user_desc

    onboarding: str
    if session.onboarding is None:
        onboarding = "No onbording was used."
    else:
        onboarding = session.onboarding

    domain = ""
    for d in DOMAIN_REGISTRY:
        if d.label == session.journey[ "Problem type" ]:
            domain = d.get_schema()

    return f"""
You are an expert optimization analyst.

Explain the result of the following optimization session in a clear,
professional, and neutral tone from the given data.

The user description of its problem is:
{ user_desc }

The AI onboarding is:
{ onboarding }

The porblem use the domain:
{ domain }

The data set by the user are stock in the journey:
{ session.journey }

The result of the optimization is:
{ session.result }

Guidelines:
- Be factual and precise
- Do not invent data
- Do not reference implementation details
- Do not mention programming languages
- Focus on decision rationale and outcome quality
"""
