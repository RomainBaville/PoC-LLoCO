# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025-2026 AKKODIS.
# SPDX-FileContributor: Romain Baville

def apply_logical_constraints( model, x, problem ):
    cfg = problem.config

    if cfg.candidates_mutual_exclusion is not None:
        for r in problem.right_entities:
            for l_exclusion in cfg.candidates_mutual_exclusion:
                model.Add( sum( x[ l, r ] for l in l_exclusion ) <= 1 )

    if cfg.targets_mutual_exclusion is not None:
        for l in problem.left_entities:
            for r_exclusion in cfg.targets_mutual_exclusion:
                model.Add( sum( x[ l, r ] for r in r_exclusion ) <= 1 )
