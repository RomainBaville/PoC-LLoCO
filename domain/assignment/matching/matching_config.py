# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025-2026 AKKODIS.
# SPDX-FileContributor: Romain Baville

from dataclasses import dataclass
from typing import Optional

from domain.objective import Objective
from domain.assignment.matching.matching_reward_functions import RewardFunctions
from domain.assignment.matching.matching_penalty_functions import PenaltyFunctions


@dataclass
class MatchingConfig:
    labels: list[ str ]
    left_vals: dict[ list[ str ], float ]
    right_vals: dict[ list[ str ], float ]

    # Scoring config
    objective: Objective
    reward_function: RewardFunctions
    penalty_function: PenaltyFunctions

    # Constraints
    weights: Optional[ dict[ str, float ] ] = None

    max_vals: Optional[ dict[ list[ str ], float ] ] = None
    min_vals: Optional[ dict[ list[ str ], float ] ] = None
