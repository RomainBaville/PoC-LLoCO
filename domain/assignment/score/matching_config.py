# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025-2026 AKKODIS.
# SPDX-FileContributor: Romain Baville

from dataclasses import dataclass, field

from domain.assignment.score.matching_penalty_functions import PenaltyFunctions
from domain.assignment.score.matching_reward_functions import RewardFunctions
from domain.objective import Objective


@dataclass
class MatchingConfig:
    """Configure matching-based score computation."""

    labels: tuple[ str, ...] = field( metadata={
        "description": "Variables used for matching."
    } )

    left_vals: dict[ tuple[ str, str ],
                     float ] = field( metadata={
                         "description": "Variable values for left entities."
                     } )

    right_vals: dict[ tuple[ str, str ],
                      float ] = field( metadata={
                          "description": "Variable values for right entities."
                      } )

    objective: Objective = field( metadata={
        "description": "Optimization objective."
    } )

    weights: dict[ str, float ] = field( metadata={
        "description": "Weight applied to each matching variable."
    } )

    reward_function: RewardFunctions = field(
        metadata={
            "description": "Reward function used to compute matching score."
        }
    )

    penalty_function: PenaltyFunctions = field(
        default=PenaltyFunctions.NONE, metadata={
            "description": "Penalty function used to compute matching score."
        }
    )

    max_vals: dict[ tuple[ str, str ], float ] | None = field(
        default=None, metadata={
            "description": "Maximum accepted variable values for assignments."
        }
    )

    min_vals: dict[ tuple[ str, str ], float ] | None = field(
        default=None, metadata={
            "description": "Minimum accepted variable values for assignments."
        }
    )
