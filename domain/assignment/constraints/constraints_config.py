# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025-2026 AKKODIS.
# SPDX-FileContributor: Romain Baville

from dataclasses import dataclass
from typing import Optional

from domain.assignment.constraints.quantities_constraints import QuantitiesConstraints
from domain.assignment.constraints.logicals_constraints import LogicalsConstraints


@dataclass
class ConstraintsConfig:
        """Dataclass to configure constraints of the assignment problem.

        Args:
            use_quantities_constraints (bool): True if the assignment problem has quantities constraints.
                Defaults to False.
            quantities_constraints (Optional[QuantitiesConstraints]): The quantities constraints of the problem.
            use_logicals_constraints (bool): True if the assignment problem has logicals constraints.
                Defaults to False.
            logicals_constraints (Optional[LogicalsConstraints]): The logicals constraints of the problem.
        """
        use_quantities_constraints: bool = False
        quantities_constraints: Optional[ QuantitiesConstraints ] = None

        use_logicals_constraints: bool = False
        logicals_constraints: Optional[ LogicalsConstraints ] = None
