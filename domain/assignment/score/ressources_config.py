# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025-2026 AKKODIS.
# SPDX-FileContributor: Romain Baville

from dataclasses import dataclass, field

from domain.objective import Objective


@dataclass
class RessourcesConfig:
    """Configure resource-based score computation."""

    labels: tuple[ str, ...] = field( metadata={
        "description": "Resource labels used in score computation."
    } )

    vals: dict[ tuple[ str, str ], float ] = field( metadata={
        "description": "Resource values of left entities."
    } )

    objectives: dict[ str,
                      Objective ] = field( metadata={
                          "description": "Optimization objective for each resource."
                      } )

    weights: dict[ str, float ] = field( metadata={
        "description": "Weight applied to each resource."
    } )

    max_vals: dict[ tuple[ str, ...], float ] | None = field(
        default=None, metadata={
            "description": "Maximum accepted resource values per right entity."
        }
    )

    min_vals: dict[ tuple[ str, ...], float ] | None = field(
        default=None, metadata={
            "description": "Minimum accepted resource values per right entity."
        }
    )

    max_global_vals: dict[ tuple[ str, ...], float ] | None = field(
        default=None, metadata={
            "description": "Maximum accepted resource values globally."
        }
    )

    min_global_vals: dict[ tuple[ str, ...], float ] | None = field(
        default=None, metadata={
            "description": "Minimum accepted resource values globally."
        }
    )
