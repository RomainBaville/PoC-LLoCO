# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025-2026 AKKODIS.
# SPDX-FileContributor: Romain Baville

def apply_left_constraints( model, x, problem ):
    cfg = problem.config

    for l in problem.left_entities:

        # ---------------------------------------
        # MAX assignments per left
        # ---------------------------------------
        if cfg.max_assignments_per_left is not None:
            max_cap = cfg.max_assignments_per_left[ l ]
            model.Add(
                sum( x[ l, r ] for r in problem.right_entities ) <= max_cap
            )

        # ---------------------------------------
        # MIN assignments per left
        # ---------------------------------------
        if cfg.min_assignments_per_left is not None:
            min_cap = cfg.min_assignments_per_left[ l ]
            model.Add(
                sum( x[ l, r ] for r in problem.right_entities ) >= min_cap
            )


def apply_right_constraints( model, x, problem ):
    cfg = problem.config

    for r in problem.right_entities:

        # ---------------------------------------
        # MAX capacities
        # ---------------------------------------
        if cfg.max_capacities_per_right is not None:
            max_cap = cfg.max_capacities_per_right[ r ]
            model.Add(
                sum( x[ l, r ] for l in problem.left_entities ) <= max_cap
            )

        # ---------------------------------------
        # MIN capacities
        # ---------------------------------------
        if cfg.min_capacities_per_right is not None:
            min_cap = cfg.min_capacities_per_right[ r ]
            model.Add(
                sum( x[ l, r ] for l in problem.left_entities ) >= min_cap
            )
