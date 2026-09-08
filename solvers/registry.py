# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025-2026 AKKODIS.
# SPDX-FileContributor: Romain Baville

from dataclasses import dataclass
from solvers.assignment.registry import ASSIGNEMENT_SOLVERS

from typing_extensions import Any


@dataclass
class DomainsSolverGroup:
    """The class with all the type of domain that can be solve.

    Args:
        key (str): The type of problem.
        description (str): The discription of the problem type.
        solvers (str): All the solvers available for the domain.
    """
    key: str
    description: str
    solvers: list[ Any ]


DOMAINS_SOLVER_GROUP: list[ DomainsSolverGroup ] = [
    DomainsSolverGroup(
        key="assignments",
        description="Solvers for assignment problems",
        solvers=ASSIGNEMENT_SOLVERS
    )
]
