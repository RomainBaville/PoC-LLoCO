# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025-2026 AKKODIS.
# SPDX-FileContributor: Romain Baville

from dataclasses import dataclass
from typing_extensions import Optional

from domain.objective import Objective


@dataclass
class SingleConfig:
    labels: list[ str ]
    vals: dict[ list[ str ], float ]

    # Scoring config
    objectives: dict[ str, Objective ]

    # Constraints
    weights: Optional[ dict[ str, float ] ] = None

    max_vals: Optional[ dict[ list[ str ], float ] ] = None
    min_vals: Optional[ dict[ list[ str ], float ] ] = None

    max_all_vals: Optional[ dict[ str, float ] ] = None
    min_all_vals: Optional[ dict[ str, float ] ] = None

    max_vals_global: Optional[ dict[ str, float ] ] = None
    min_vals_global: Optional[ dict[ str, float ] ] = None

    max_all_vals_global: Optional[ float ] = None
    min_all_vals_global: Optional[ float ] = None
