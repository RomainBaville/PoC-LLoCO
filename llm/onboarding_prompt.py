# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025-2026 AKKODIS.
# SPDX-FileContributor: Romain Baville

from llm.onboarding_context import build_onboarding_context


def build_onboarding_prompt( user_description: str ) -> str:
    """Build a generic AI onboarding explanation aligned with platform registries.

    Args:
        user_description (str): The problem description.

    Returns:
        str: The prompt for the llm.
    """
    context = build_onboarding_context()

    return f"""
You are an AI assistant helping a user understand how to use
an optimization platform.

The user describes their problem as follows:

\"\"\"
{user_description}
\"\"\"

The platform supports structured optimization problems

Problem types:
{ context[ "problems" ] }

Available solvers:
{ context[ "solvers" ] }

Available input data:
{ context[ "input data" ] }


Explain clearly:
- how the platform can model such problems
- how the user will progressively choose:
  1. problem type
  2. formulation
  3. data
  4. configuration
  5. solver
- why configuration and scoring choices impact the result

Guidelines:
- Do NOT invent capabilities
- Do NOT mention internal code or implementation details
- Use clear, professional, user-facing language
"""
