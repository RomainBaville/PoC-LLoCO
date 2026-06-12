# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025-2026 AKKODIS.
# SPDX-FileContributor: Romain Baville

def compute( problem, left_label, right_label ):
        total: float = 0

        if problem.use_matching:
            matching_config = problem.matching_config
            for matching_label in matching_config.labels:
                left_val = matching_config.left_vals[ ( left_label, matching_label ) ]
                right_val = matching_config.right_vals[ ( right_label, matching_label ) ]

                matching_weight: float = 1.
                if matching_config.weights is not None:
                    matching_weight = matching_config.weights[ matching_label ]

                reward: float = matching_config.reward_function( left_val, right_val )
                penalty: float = matching_config.penalty_function( left_val, right_val )

                total += matching_config.objective.value * matching_weight * ( reward + penalty )

        if problem.use_single:
            single_config = problem.single_config
            for label in single_config.labels:
                total += single_config.objectives[ label ].value * single_config.vals[ ( left_label, label ) ]

        return total
