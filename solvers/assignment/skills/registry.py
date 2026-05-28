# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025-2026 AKKODIS.
# SPDX-FileContributor: Romain Baville

from dataclasses import dataclass
from typing import Type

from solvers.base import Solver
from solvers.assignment.skills.ortools_cp_sat import ORToolsSkillAssignmentSolver


@dataclass
class SolverDefinition:
    key: str
    label: str
    description: str
    solver_class: Type[Solver]


SOLVERS = {
    "ortools_cp_sat": SolverDefinition(
        key="ortools_cp_sat",
        label="OR-Tools CP-SAT",
        description=(
            "Constraint Programming solver suitable for "
            "skill-based assignment problems with configurable behavior "
            "(matching, coverage, hybrid, constraints)."
        ),
        solver_class=ORToolsSkillAssignmentSolver,
    ),
}
