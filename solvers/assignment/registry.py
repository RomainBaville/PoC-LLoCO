# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025-2026 AKKODIS.
# SPDX-FileContributor: Romain Baville

from collections.abc import Callable
from dataclasses import dataclass

from domain.assignment.base import AssignmentProblem
from solvers.assignment.cp_model.ortools_cp_sat import solve_assignment_problem


@dataclass
class AssignmentSolvers:
    """The dataclass with all the solvers that can be used for an assignment problem.

    Args:
        key (str): The name of the solver use for the code.
        label (str): The label of the solver use for the user.
        description (str): The description of the solver capabilities.
        solver_fn (Callable[[AssignmentProblem], dict[str, list[tuple[str, int]]]]): The function to solve the problem.
    """
    key: str
    label: str
    description: str
    solver_fn: Callable[ [ AssignmentProblem ], dict[ str, list[ tuple[ str, int ] ] ] ]


ASSIGNEMENT_SOLVERS: list[ AssignmentSolvers ] = [
    AssignmentSolvers(
        key="ortools_cp_sat",
        label="OR-Tools CP-SAT - Assignment",
        description="Constraint Programming solver suitable for assignment problems with configurable behavior.",
        solver_fn=solve_assignment_problem
    )
]
