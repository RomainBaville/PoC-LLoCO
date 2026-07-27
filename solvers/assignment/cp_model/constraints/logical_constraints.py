# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025-2026 AKKODIS.
# SPDX-FileContributor: Romain Baville

from ortools.sat.python.cp_model import CpModel, IntVar

from domain.assignment.base import AssignmentProblem
from domain.assignment.constraints.logicals_constraints import LogicalsConstraints


def apply_logical_constraints(
    model: CpModel,
    is_assigned: dict[ tuple[ str, str ], IntVar ],
    quantities: dict[ tuple[ str, str ], IntVar ],
    problem: AssignmentProblem,
) -> None:
    """Add to the model the logical constraints if needed.

    Args:
        model (CpModel): The model used.
        is_assigned (dict[tuple[str, str], IntVar]): The binary variable with 1 for assigned 0 otherwize.
        quantities (dict[tuple[str, str], IntVar]): The integrable variable with the number of assocciation.
        problem (AssignmentProblem): The assignment problem.
    """
    if isinstance( problem.constraints_config.logicals_constraints, LogicalsConstraints ):
        logicals_constraints: LogicalsConstraints = problem.constraints_config.logicals_constraints
        if logicals_constraints.left_mutual_exclusions is not None:
            for right_label in problem.right_labels:
                for left_mutual_exclusion in logicals_constraints.left_mutual_exclusions:
                    model.add(
                        sum( is_assigned[ left_label, right_label ] for left_label in left_mutual_exclusion ) < 1
                    )

        if logicals_constraints.right_mutual_exclusions is not None:
            for left_label in problem.left_labels:
                for right_mutual_exclusion in logicals_constraints.right_mutual_exclusions:
                    model.add(
                        sum( is_assigned[ left_label, right_label ] for right_label in right_mutual_exclusion ) < 1
                    )

        if logicals_constraints.implications is not None:
            for ( left_label, right_label ), a in logicals_constraints.implications.items():
                for ( left_forced_label, right_forced_label, nb_implications ) in a:
                    model.add_implication(
                        is_assigned[ left_label, right_label ], is_assigned[ left_forced_label, right_forced_label ]
                    )
                    model.add(
                        quantities[ left_forced_label, right_forced_label ] >= int( nb_implications ) *
                        quantities[ left_label, right_label ]
                    )
