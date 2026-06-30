# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025-2026 AKKODIS.
# SPDX-FileContributor: Romain Baville

from dataclasses import dataclass


@dataclass
class AssignmentSolverGroup:
    key: str
    description: str
    registry_module: str


ASSIGNMENT_SOLVER_GROUPS = {
    "assignments":
    AssignmentSolverGroup(
        key="assignments",
        description="Solvers for assignment problems",
        registry_module="solvers.assignment.registry",
    ),
}
