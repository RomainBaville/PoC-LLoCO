# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025-2026 AKKODIS.
# SPDX-FileContributor: Romain Baville

from dataclasses import dataclass, field

from domain.assignment.constraints.logicals_constraints import LogicalsConstraints
from domain.assignment.constraints.quantities_constraints import QuantitiesConstraints


@dataclass
class ConstraintsConfig:
    """Configure assignment constraints."""

    multiple_same_assignment: bool = field(
        default=True,
        metadata={
            "description": "Allow multiple assignments of the same left entity to the same right entity."
        }
    )

    use_quantities_constraints: bool = field(
        default=False, metadata={
            "description": "Enable quantity constraints."
        }
    )

    quantities_constraints: QuantitiesConstraints | None = field(
        default=None, metadata={
            "description": "Quantity constraints configuration."
        }
    )

    use_logicals_constraints: bool = field( default=False, metadata={
        "description": "Enable logical constraints."
    } )

    logicals_constraints: LogicalsConstraints | None = field(
        default=None, metadata={
            "description": "Logical constraints configuration."
        }
    )
