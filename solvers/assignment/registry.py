# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025-2026 AKKODIS.
# SPDX-FileContributor: Romain Baville

from dataclasses import dataclass


@dataclass
class AssignmentSolverGroup:
    key: str
    description: str
    registry_module: str  # import path


ASSIGNMENT_SOLVER_GROUPS = {
    "skills": AssignmentSolverGroup(
        key="skills",
        description="Solvers for skill-based assignment problems",
        registry_module="solvers.assignment.skills.registry",
    ),

    # Future:
    # "cost": AssignmentSolverGroup(
    #     key="cost",
    #     description="Solvers for cost-based assignment problems",
    #     registry_module="solvers.assignment.cost.registry",
    # ),
}
