# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025-2026 AKKODIS.
# SPDX-FileContributor: Romain Baville

def apply_coverage_constraints(model, x, problem):
    cfg = problem.config

    if not cfg.enforce_full_coverage:
        return

    for r in problem.right_entities:
        for s in problem.skills:
            model.Add(
                sum(
                    problem.left_skills[(l, s)] * x[l, r]
                    for l in problem.left_entities
                )
                >= problem.right_requirements[(r, s)]
            )
