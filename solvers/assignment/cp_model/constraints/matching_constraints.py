# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025-2026 AKKODIS.
# SPDX-FileContributor: Romain Baville

def apply_matching_constraints( model, x, problem ):
    if problem.use_matching:
        matching_config = problem.matching_config
        if matching_config.max_vals is not None:
            for left_label in problem.left_labels:
                for ( right_label, matching_label ), max_val in matching_config.max_vals.items():
                    left_val = int( matching_config.left_vals[ left_label, matching_label ] )
                    model.Add( left_val * x[ left_label, right_label ] >= int( max_val ) )

        if matching_config.min_vals is not None:
            for left_label in problem.left_labels:
                for ( right_label, matching_label ), min_val in matching_config.min_vals.items():
                    left_val = int( matching_config.left_vals[ left_label, matching_label ] )
                    model.Add( left_val * x[ left_label, right_label ] <= int( min_val ) )
