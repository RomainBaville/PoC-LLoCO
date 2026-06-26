# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025-2026 AKKODIS.
# SPDX-FileContributor: Romain Baville

from typing import Optional

from ortools.sat.python.cp_model import CpModel
from domain.assignment.base import AssignmentProblem
from domain.assignment.constraints.logicals_constraints import LogicalsConstraints

def apply_logical_constraints( model: CpModel, x, q, problem: AssignmentProblem ):
    logicals_constraints: Optional[ LogicalsConstraints ] = problem.constraints_config.logicals_constraints
    if logicals_constraints is not None:
        if logicals_constraints.left_mutual_exclusions is not None:
            for right_label in problem.right_labels:
                for left_mutual_exclusion in logicals_constraints.left_mutual_exclusions:
                    model.add(
                        sum(
                            x[ left_label, right_label ] for left_label in left_mutual_exclusion
                        ) < 1
                    )

        if logicals_constraints.right_mutual_exclusions is not None:
            for left_label in logicals_constraints.left_labels:
                for right_mutual_exclusion in logicals_constraints.right_mutual_exclusions:
                    model.add(
                        sum(
                            x[ left_label, right_label ] for right_label in right_mutual_exclusion
                        ) < 1
                    )

        if logicals_constraints.implications is not None:
            for ( left_label, right_label ), a in logicals_constraints.implications.items():
                for ( left_forced_label, right_forced_label, nb_implications ) in a:
                    model.add_implication( x[ left_label, right_label ], x[ left_forced_label, right_forced_label ] )
                    model.add( q[ left_forced_label, right_forced_label ] >= int( nb_implications ) * q[ left_label, right_label ] )
