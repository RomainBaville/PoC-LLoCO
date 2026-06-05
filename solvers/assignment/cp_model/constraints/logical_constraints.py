# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025-2026 AKKODIS.
# SPDX-FileContributor: Romain Baville

def apply_logical_constraints( model, x, problem ):
    if problem.left_mutual_exclusions is not None:
        for r in problem.right_entities:
            for l_exclusion in problem.left_mutual_exclusions:
                model.Add( sum( x[ l, r ] for l in l_exclusion ) <= 1 )

    if problem.right_mutual_exclusions is not None:
        for l in problem.left_entities:
            for r_exclusion in problem.right_mutual_exclusions:
                model.Add( sum( x[ l, r ] for r in r_exclusion ) <= 1 )
