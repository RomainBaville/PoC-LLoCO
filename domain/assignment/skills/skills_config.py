# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025-2026 AKKODIS.
# SPDX-FileContributor: Romain Baville

from dataclasses import dataclass
from typing import Optional

from domain.objective import Objective
from domain.assignment.skills.skills_reward_functions import RewardFunction
from domain.assignment.skills.skills_penalty_functions import PenaltyFunctions


@dataclass
class SkillsConfig:
    skills_label: list[ str ]

    left_skills_val: dict[ list[ str ], float ]
    right_skills_val: dict[ list[ str ], float ]

    skills_objective: Objective = Objective.MAXIMIZE

    skills_weight: Optional[ dict[ str, float ] ] = None

    skills_reward_function: RewardFunction = RewardFunction.MIN
    skills_penalty_function: PenaltyFunctions = PenaltyFunctions.NONE
