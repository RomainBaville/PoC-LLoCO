# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025-2026 AKKODIS.
# SPDX-FileContributor: Romain Baville

def apply_logical_constraints( model, x, problem ):
    cfg = problem.config

    if cfg.candidates_mutual_exclusion is not None:
        for r in problem.right_entities:
            for l1, l2 in cfg.candidates_mutual_exclusion:
                model.Add( x[ l1, r ] + x[ l2, r ] <= 1 )

    if cfg.implications is not None:
        for ( l1, r1 ), ( l2, r2 ) in cfg.implications:
            model.Add( x[ l1, r1 ] <= x[ l2, r2 ] )
