# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025-2026 AKKODIS.
# SPDX-FileContributor: Romain Baville

from dataclasses import dataclass
from typing import Type, Dict
from solvers.base import Solver
from solvers.assignment.skills.ortools_cp_sat import ORToolsSkillAssignmentSolver


@dataclass
class SolverDefinition:
    key: str
    label: str
    solver_class: Type[Solver]


SOLVER_REGISTRY = {
    "assignment": {
        "skills_coverage": {
            "ortools": SolverDefinition(
                key="ortools",
                label="OR-Tools CP-SAT",
                solver_class=ORToolsSkillAssignmentSolver,
            ),
        },
        "skills_best_fit": {
            "ortools": SolverDefinition(
                key="ortools",
                label="OR-Tools CP-SAT",
                solver_class=ORToolsSkillAssignmentSolver,
            ),
        },
        "skills_team": {
            "ortools": SolverDefinition(
                key="ortools",
                label="OR-Tools CP-SAT",
                solver_class=ORToolsSkillAssignmentSolver,
            ),
        },
        "skills_portfolio": {
            "ortools": SolverDefinition(
                key="ortools",
                label="OR-Tools CP-SAT",
                solver_class=ORToolsSkillAssignmentSolver,
            ),
        },
    }
}
