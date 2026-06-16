# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025-2026 AKKODIS.
# SPDX-FileContributor: Romain Baville

from domain.assignment.base import AssignmentProblem

def apply_matching_constraints( model, x, problem: AssignmentProblem ):
    if problem.use_matching:
        if problem.matching_config.max_vals is not None:
            for left_label in problem.left_labels:
                for ( right_label, left_variable_label ), max_val in problem.matching_config.max_vals.items():
                    left_val = int( problem.matching_config.left_vals[ left_label, left_variable_label ] )
                    model.Add( left_val * x[ left_label, right_label ] <= int( max_val ) )

        if problem.matching_config.min_vals is not None:
            for left_label in problem.left_labels:
                for ( right_label, left_variable_label ), min_val in problem.matching_config.min_vals.items():
                    left_val = int( problem.matching_config.left_vals[ left_label, left_variable_label ] )
                    model.Add( left_val * x[ left_label, right_label ] >= int( min_val ) )
