# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025-2026 AKKODIS.
# SPDX-FileContributor: Romain Baville, Fidel Monteiro

from ui.registry import UI_DOMAIN_REGISTRY, UiDomainType


def infer_problem_configuration( user_desc: str, ai_text: str | None = None ) -> UiDomainType:
    """Deterministic keyword-based recommendation — no extra LLM call.

    Args:
        user_desc (str): The user description of the problem.
        ai_text (str | None): The AI generated text describing the problem if exist.
            Defaults to None.

    Returns:
        ProblemType: The problem type infered.

    Raises:
        ValueError: Fail to infer the problem configuration.
    """
    text: str = f"{ user_desc }\n{ ai_text or '' }".lower()

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
        "competence"
    ]
    if any( w in text for w in assignment_keywords ):
        for problem in UI_DOMAIN_REGISTRY:
            if problem.key == "assignment":
                return problem

    raise ValueError( "Fail to infer the problem configuration." )
