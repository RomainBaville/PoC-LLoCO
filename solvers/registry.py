# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025-2026 AKKODIS.
# SPDX-FileContributor: Romain Baville

from dataclasses import dataclass


@dataclass
class ProblemsSolverGroup:
    """The class with all the type of problem that can be solve.

    Args:
        key (str): The type of problem.
        description (str): The discription of the problem type.
        registry_module (str): The path to the module with the implementation of the solver.
    """
    key: str
    description: str
    registry_module: str


PROBLEM_SOLVER_GROUPS: dict[ str, ProblemsSolverGroup ] = {
    "assignments":
    ProblemsSolverGroup(
        key="assignments",
        description="Solvers for assignment problems",
        registry_module="solvers.assignment.registry"
    )
}
