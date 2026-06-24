# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025-2026 AKKODIS.
# SPDX-FileContributor: Romain Baville

from ortools.sat.python.cp_model import CpModel
from domain.assignment.base import AssignmentProblem

def apply_logical_constraints( model: CpModel, x, problem: AssignmentProblem ):
    if problem.left_mutual_exclusions is not None:
        for right_label in problem.right_labels:
            for left_mutual_exclusion in problem.left_mutual_exclusions:
                model.add(
                    sum(
                        x[ left_label, right_label ] for left_label in left_mutual_exclusion
                    ) < 1
                )

    if problem.right_mutual_exclusions is not None:
        for left_label in problem.left_labels:
            for right_mutual_exclusion in problem.right_mutual_exclusions:
                model.add(
                    sum(
                        x[ left_label, right_label ] for right_label in right_mutual_exclusion
                    ) < 1
                )

    if problem.implications is not None:
        for ( left_label, right_label ), a in problem.implications.items():
            for ( left_forced_label, right_forced_label, _ ) in a:
                model.add_implication( x[ left_label, right_label ], x[ left_forced_label, right_forced_label ] )
