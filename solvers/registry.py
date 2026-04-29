# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025-2026 AKKODIS.
# SPDX-FileContributor: Romain Baville

from dataclasses import dataclass
from typing import Type, Dict
from solvers.base import Solver
from solvers.assignment_ortools import ORToolsAssignmentSolver


@dataclass
class SolverDefinition:
    key: str
    label: str
    solver_class: Type[Solver]


# --------------------------------------------------
# Solver registry per problem type
# --------------------------------------------------

SOLVER_REGISTRY: Dict[str, Dict[str, SolverDefinition]] = {

    "assignment": {
        "ortools_cp": SolverDefinition(
            key="ortools_cp",
            label="OR-Tools CP-SAT",
            solver_class=ORToolsAssignmentSolver,
        ),

        # Future assignment solvers:
        # "gurobi": SolverDefinition(...)
        # "pulp": SolverDefinition(...)
    },

    # Other problems:
    # "knapsack": {...}
}
