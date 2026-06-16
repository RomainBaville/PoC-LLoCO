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
    """Dataclass to configure the scoring optimization involving a score computation from a matching between left and right variables sharing the same label.
    This Dataclass also configure optional constraints associated with this matching.

    Args:
        labels (tuple[str, ...]): The variables labels for both left and right entities used in the computation of the score matching.
        left_vals (dict[tuple[str, str], float]): The dictionary with the value of the left entities for all the variables used in the computation of the score matching:
            - keys (tuple[str, str]): The left entitiy label, the variable label.
            - values (float): The left value used in the computation of the matching score.
        right_vals (dict[tuple[str, str], float]): The dictionary with the value of the right entities for all the variables used in the computation of the score matching:
            - keys (tuple[str, str]): The right entitiy label, the variable label.
            - values (float): The right value used in the computation of the matching socre.
        objective (Objective): The objective of the score matching (maximize or minimize).
        reward_function (RewardFunctions): The reward function used in the computation of the matching score.
        penalty_function (PenaltyFunctions): The penalty function used in the computation of the matching score.
        weights (Optional[dict[str, float]]): The dictionary with the variables weights used in the computation of the score:
            - keys (str): The label of the variable with a weight.
            - values (float): The value of the weight.
        max_vals (Optional[dict[tuple[str, str], float]]): The dictionary whit the maximum variables values accepted for the assignment of the left entities by the right entities:
            - keys (tuple[str, str]): The right entity label, the left variable label.
            - value (float): The maximum value accepted by the right entity for the left variable.
        min_vals (Optional[dict[tuple[str, str], float]]): The dictionary whit the minimum variables values accepted for the assignment of the left entities by the right entities:
            - keys (tuple[str, str]): The right entity label, the left variable label.
            - value (float): The minimum value accepted by the right entity for the left variable.
    """
    labels: tuple[ str, ...]
    left_vals: dict[ tuple[ str, str ], float ]
    right_vals: dict[ tuple[ str, str ], float ]

    # Scoring config
    objective: Objective
    reward_function: RewardFunctions
    penalty_function: PenaltyFunctions

    # Constraints
    weights: Optional[ dict[ str, float ] ] = None

    max_vals: Optional[ dict[ tuple[ str, str ], float ] ] = None
    min_vals: Optional[ dict[ tuple[ str, str ], float ] ] = None
