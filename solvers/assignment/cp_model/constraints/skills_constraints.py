# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025-2026 AKKODIS.
# SPDX-FileContributor: Romain Baville

def apply_skill_constraints(model, x, problem):
    if problem.use_skills:
        if problem.skills_config.min_requirement_skills_val is not None:
            for ( right, skill ), min_val in problem.min_requirement_skills_val.items():
                model.Add(
                    sum(
                        problem.skills_val[ left, skill ] * x[ left, right ]
                        for left in problem.left_entities
                    ) >= int( min_val )
                )
