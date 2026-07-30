# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025-2026 AKKODIS.
# SPDX-FileContributor: Romain Baville

from dataclasses import dataclass

from domain.assignment.constraints.logicals_constraints import LogicalsConstraints
from domain.assignment.constraints.quantities_constraints import QuantitiesConstraints


@dataclass
class ConstraintsConfig:
    """Dataclass to configure constraints of the assignment problem.

    Args:
        multiple_same_assignment (bool): True if a left entity can be assigned more than once to the same right entity.
            Defaults to True.
        use_quantities_constraints (bool): True if the assignment problem has quantities constraints.
            Defaults to False.
        quantities_constraints (Optional[QuantitiesConstraints]): The quantities constraints of the problem.
        use_logicals_constraints (bool): True if the assignment problem has logicals constraints.
            Defaults to False.
        logicals_constraints (Optional[LogicalsConstraints]): The logicals constraints of the problem.
    """
    multiple_same_assignment: bool = True

    use_quantities_constraints: bool = False
    quantities_constraints: QuantitiesConstraints | None = None

    use_logicals_constraints: bool = False
    logicals_constraints: LogicalsConstraints | None = None
