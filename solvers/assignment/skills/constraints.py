# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025-2026 AKKODIS.
# SPDX-FileContributor: Romain Baville

def apply_left_constraints(model, x, problem):
    cfg = problem.config
    for l in problem.left_entities:
        model.Add(
            sum(x[l, r] for r in problem.right_entities)
            <= cfg.max_assignments_per_left
        )


def apply_right_constraints(model, x, problem):
    cfg = problem.config
    if cfg.max_assignments_per_right:
        for r in problem.right_entities:
            model.Add(
                sum(x[l, r] for l in problem.left_entities)
                <= cfg.max_assignments_per_right
            )
