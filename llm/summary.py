# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025-2026 AKKODIS.
# SPDX-FileContributor: Romain Baville


"""
Builds the prompt used to generate an AI summary
of the optimization result.
"""


def build_summary_prompt(
    left_entity_name: str,
    right_entity_name: str,
    assignments: dict,
    skills: list[str],
) -> str:
    """
    Create a clean, deterministic prompt for the LLM.

    Parameters
    ----------
    left_entity_name : str
        Name of the left entity (e.g. Employees)
    right_entity_name : str
        Name of the right entity (e.g. Projects)
    assignments : dict
        Mapping {left_entity -> right_entity}
    skills : list[str]
        List of skills involved in the optimization

    Returns
    -------
    str
        Prompt to send to the LLM
    """

    assignments_text = "\n".join(
        f"- {left} → {right}"
        for left, right in assignments.items()
    )

    skills_text = ", ".join(skills)

    return f"""
You are an assistant helping to explain an optimization result.

The goal was to assign {left_entity_name} to {right_entity_name}
based on skill compatibility and requirements.

Skills considered:
{skills_text}

Final assignment:
{assignments_text}

Write a clear and professional summary that explains:
- what problem was solved
- how the constraints were respected
- why this solution is efficient

Do not invent data.
Do not mention algorithms or solvers.
"""
"""
Prompt builders for LLM explanations.
"""


def build_onboarding_prompt(user_description: str) -> str:
    """
    Build a prompt that explains how to use the UI
    based on the user's natural-language problem description.
    """

    return f"""
You are guiding a user through an optimization UI.

The user described their problem as follows:
\"\"\"
{user_description}
\"\"\"

The UI follows these fixed steps:
1. Choose the assignment problem
2. Name the two entities to associate (for example: Employees and Projects)
3. Select the CSV files containing the data
4. Define which columns identify entities and which columns represent skills
5. Run the optimization and view the result

Explain clearly:
- how these steps match the user's problem
- what the user should do at each step
- what kind of data is expected

Do NOT invent new steps.
Do NOT generate code.
Do NOT explain algorithms.
"""
