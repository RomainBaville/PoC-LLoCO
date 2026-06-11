# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025-2026 AKKODIS.
# SPDX-FileContributor: Romain Baville

def apply_skill_constraints(model, x, problem):
    if problem.use_skills:
        skills_config = problem.skills_config
        if skills_config.min_requirement_skills_val is not None:
            for ( right, min_requirement_skill_label ), min_requirement_skill_val in skills_config.min_requirement_skills_val.items():
                skill_min_requirement_val = skills_config.min_requirement_skills_label[ min_requirement_skill_label ]
                model.Add(
                    sum(
                        skills_config.skills_val[ left, skill_min_requirement_val ] * x[ left, right ]
                        for left in problem.left_entities
                    ) >= int( min_requirement_skill_val )
                )
