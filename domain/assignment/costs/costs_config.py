# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025-2026 AKKODIS.
# SPDX-FileContributor: Romain Baville

from dataclasses import dataclass
from typing_extensions import Optional

from domain.objective import Objective


@dataclass
class CostsConfig:
    costs_label: list[ str ]
    costs_val: dict[ list[ str ], float ]
    costs_objective: dict[ str, Objective ]

    limit_costs_label: Optional[ dict[ str, str ] ] = None
    limit_costs_val: Optional[ dict[ list[ str ], float ] ] = None
