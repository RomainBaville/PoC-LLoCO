# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025-2026 AKKODIS.
# SPDX-FileContributor: Romain Baville

from dataclasses import dataclass
from typing_extensions import Optional

from domain.objective import Objective


@dataclass
class CostsConfig:
    costs_label: dict[ str, Optional[ str ] ]

    costs_val: dict[ list[ str ], float ]
    costs_objective: dict[ str, Objective ]

    limit_costs_val: Optional[ dict[ list[ str ], float ] ] = None
    limit_entities_costs_val: Optional[ dict[ str, float ] ] = None
    limit_assignment_costs_val: Optional[ float ] = None
