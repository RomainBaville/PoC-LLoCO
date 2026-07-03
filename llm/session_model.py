# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025-2026 AKKODIS.
# SPDX-FileContributor: Romain Baville

from dataclasses import dataclass, field


@dataclass
class OptimizationSession:
    """Structured representation of a complete optimization run passed to the LLM prompt builder.

    Args:
        problem_type (str): The problem type.
        steps: (list[str]): All the ui step.
        data_description (str): The data description.
        solver_name (str): The name of the solver.
        solver_description str): The solver description.
        result_summary (str): The summary of the result.
        config_summary (str | None): The summary of the problem configuration.
            Defaults to None.
        result_details (dict) = field( default_factory=dict )
    """
    problem_type: str
    steps: list[ str ]
    data_description: str
    solver_name: str
    solver_description: str
    result_summary: str
    config_summary: str | None = None
    result_details: dict = field( default_factory=dict )
