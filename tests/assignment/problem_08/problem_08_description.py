# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025-2026 AKKODIS.
# SPDX-FileContributor: Romain Baville

from domain.assignment.base import AssignmentProblem
from domain.assignment.constraints.constraints_config import ConstraintsConfig
from domain.assignment.constraints.quantities_constraints import QuantitiesConstraints
from domain.assignment.score.matching_config import MatchingConfig
from domain.assignment.score.matching_reward_functions import RewardFunctions
from domain.assignment.score.score_config import ScoreConfig
from domain.objective import Objective

problem_08_prompt: str = (
    "Now, we need to determine 4 out of 5 workers to complete one of the four tasks respectively. Due to each "
    "worker's different technical specialties, the time required for them to complete each task varies. The hours "
    "required by each worker to complete each task are shown in Table 5-2.\n\n"
    "Table 5-2\n"
    "| Worker | $A$ | $B$ | $C$ | $D$ |\n"
    "|--------|-----|-----|-----|-----|\n"
    "| I      | 9   | 4   | 3   | 7   |\n"
    "| II     | 4   | 6   | 5   | 6   |\n"
    "| III    | 5   | 4   | 7   | 5   |\n"
    "| IV     | 7   | 5   | 2   | 3   |\n"
    "| V      | 10  | 6   | 7   | 4   |\n\n"
    "Try to find a job assignment plan that minimizes the total working hours."
)

# Problem
left_labels: tuple[ str, ...] = ( "I", "II", "III", "IV", "V" )
right_labels: tuple[ str, ...] = ( "A", "B", "C", "D" )

# Score config
labels: tuple[ str, ...] = ( "T_A", "T_B", "T_C", "T_D" )
left_vals: dict[ tuple[ str, str ], float ] = {
    ( "I", "T_A" ): 9.,
    ( "I", "T_B" ): 4.,
    ( "I", "T_C" ): 3.,
    ( "I", "T_D" ): 7.,
    ( "II", "T_A" ): 4.,
    ( "II", "T_B" ): 6.,
    ( "II", "T_C" ): 5.,
    ( "II", "T_D" ): 6.,
    ( "III", "T_A" ): 5.,
    ( "III", "T_B" ): 4.,
    ( "III", "T_C" ): 7.,
    ( "III", "T_D" ): 5.,
    ( "IV", "T_A" ): 7.,
    ( "IV", "T_B" ): 5.,
    ( "IV", "T_C" ): 2.,
    ( "IV", "T_D" ): 3.,
    ( "V", "T_A" ): 10.,
    ( "V", "T_B" ): 6.,
    ( "V", "T_C" ): 7.,
    ( "V", "T_D" ): 4.
}
right_vals: dict[ tuple[ str, str ], float ] = {
    ( "A", "T_A" ): 1.,
    ( "A", "T_B" ): 0.,
    ( "A", "T_C" ): 0.,
    ( "A", "T_D" ): 0.,
    ( "B", "T_A" ): 0.,
    ( "B", "T_B" ): 1.,
    ( "B", "T_C" ): 0.,
    ( "B", "T_D" ): 0.,
    ( "C", "T_A" ): 0.,
    ( "C", "T_B" ): 0.,
    ( "C", "T_C" ): 1.,
    ( "C", "T_D" ): 0.,
    ( "D", "T_A" ): 0.,
    ( "D", "T_B" ): 0.,
    ( "D", "T_C" ): 0.,
    ( "D", "T_D" ): 1.
}
objective: Objective = Objective.MINIMIZE
weights: dict[ str, float ] = {
    "T_A": 1.,
    "T_B": 1.,
    "T_C": 1.,
    "T_D": 1.
}
reward_function: RewardFunctions = RewardFunctions.PRODUCT

matching_config: MatchingConfig = MatchingConfig(
    labels=labels,
    left_vals=left_vals,
    right_vals=right_vals,
    objective=objective,
    weights=weights,
    reward_function=reward_function
)

score_config: ScoreConfig = ScoreConfig( use_matching=True, matching_config=matching_config )

# Constraints
max_right_entities: dict[ str, float ] = {
    "I": 1.,
    "II": 1.,
    "III": 1.,
    "IV": 1.,
    "V": 1.
}
max_left_entities: dict[ str, float ] = {
    "A": 1.,
    "B": 1.,
    "C": 1.,
    "D": 1.
}
min_left_entities: dict[ str, float ] = {
    "A": 1.,
    "B": 1.,
    "C": 1.,
    "D": 1.
}

quantities_constraints: QuantitiesConstraints = QuantitiesConstraints(
    max_right_entities=max_right_entities, max_left_entities=max_left_entities, min_left_entities=min_left_entities
)

constraints_config: ConstraintsConfig = ConstraintsConfig(
    multiple_same_assignment=False, use_quantities_constraints=True, quantities_constraints=quantities_constraints
)

problem_08_domain: AssignmentProblem = AssignmentProblem(
    left_labels=left_labels,
    right_labels=right_labels,
    score_config=score_config,
    constraints_config=constraints_config
)

solutions_08: list[ dict[ str, list[ tuple[ str, int ] ] ] ] = [
    {
        "I": [ ( "C", 1 ) ],
        "II": [ ( "A", 1 ) ],
        "III": [ ( "B", 1 ) ],
        "IV": [ ( "D", 1 ) ]
    }, {
        "I": [ ( "B", 1 ) ],
        "II": [ ( "A", 1 ) ],
        "IV": [ ( "C", 1 ) ],
        "V": [ ( "D", 1 ) ]
    }
]
