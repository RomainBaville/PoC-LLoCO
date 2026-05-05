# SPDX-License-Identifier: Apache-2.0
from dataclasses import dataclass
from typing import Type, Dict
from solvers.base import Solver
from solvers.assignment.ortools_skills import ORToolsSkillAssignmentSolver


@dataclass
class SolverDefinition:
    key: str
    label: str
    solver_class: Type[Solver]


SOLVER_REGISTRY: Dict[str, Dict[str, Dict[str, SolverDefinition]]] = {
    "assignment": {
        "skills": {
            "ortools": SolverDefinition(
                key="ortools",
                label="OR‑Tools CP‑SAT (skills)",
                solver_class=ORToolsSkillAssignmentSolver,
            )
        }
    }
}
