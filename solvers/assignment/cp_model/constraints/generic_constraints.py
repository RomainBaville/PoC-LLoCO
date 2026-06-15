# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025-2026 AKKODIS.
# SPDX-FileContributor: Romain Baville

def apply_generic_constraints( model, x, problem ):
    for left_label in problem.left_labels:
        if problem.max_assignments is not None:
            max_assi = int( problem.max_assignments[ left_label ] )
            model.Add(
                sum(
                    x[ left_label, right_label ] for right_label in problem.right_labels
                ) <= max_assi
            )

        if problem.min_assignments is not None:
            min_assi = int( problem.min_assignments[ left_label ] )
            model.Add(
                sum(
                    x[ left_label, right_label ] for right_label in problem.right_labels
                ) >= min_assi
            )

    for right_label in problem.right_labels:
        if problem.max_capacities is not None:
            max_cap = int( problem.max_capacities[ right_label ] )
            model.Add(
                sum(
                    x[ left_label, right_label ] for left_label in problem.left_labels
                ) <= max_cap
            )

        if problem.min_capacities is not None:
            min_cap = int( problem.min_capacities[ right_label ] )
            model.Add(
                sum(
                    x[ left_label, right_label ] for left_label in problem.left_labels
                ) >= min_cap
            )
