# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025-2026 AKKODIS.
# SPDX-FileContributor: Romain Baville

def compute( problem, left, right ):
        total: float = 0

        if problem.use_skills:
            skills_config = problem.skills_config
            for skill in skills_config.skills_label:
                left_skill_val = skills_config.left_skills_val[ ( left, skill ) ]
                right_skill_val = skills_config.right_skills_val[ ( right, skill ) ]

                skills_weight: float = 1
                if skills_config.skills_weight is not None:
                    skills_weight = skills_config.skills_weight[ skill ]

                reward: float = skills_config.skills_reward_function( left_skill_val, right_skill_val )
                penalty: float = skills_config.skills_penalty_function( left_skill_val, right_skill_val )

                total += skills_config.skills_objective.value * skills_weight * ( reward + penalty )

        if problem.use_costs:
            costs_config = problem.costs_config
            for cost in costs_config.costs_label:
                total += costs_config.costs_objective[ cost ].value * costs_config.costs_val[ ( left, cost ) ]


        return total