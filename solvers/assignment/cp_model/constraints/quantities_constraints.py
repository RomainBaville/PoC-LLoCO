# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025-2026 AKKODIS.
# SPDX-FileContributor: Romain Baville

from ortools.sat.python.cp_model import CpModel, IntVar

from domain.assignment.base import AssignmentProblem
from domain.assignment.constraints.quantities_constraints import QuantitiesConstraints


def apply_quantities_constraints(
    model: CpModel,
    is_assigned: dict[ tuple[ str, str ], IntVar ],
    quantities: dict[ tuple[ str, str ], IntVar ],
    problem: AssignmentProblem,
) -> None:
    """Add to the model the quantities constraints if needed.

    Args:
        model (CpModel): The model used.
        is_assigned (dict[tuple[str, str], IntVar]): The binary variable with 1 for assigned 0 otherwize.
        quantities (dict[tuple[str, str], IntVar]): The integrable variable with the number of assocciation.
        problem (AssignmentProblem): The assignment problem.
    """
    if problem.constraints_config.use_quantities_constraints and isinstance(
        problem.constraints_config.quantities_constraints, QuantitiesConstraints
    ):
        quantities_constraints: QuantitiesConstraints = problem.constraints_config.quantities_constraints

        if isinstance( quantities_constraints.max_right_entities, dict ):
            for left_label in problem.left_labels:
                max_right_entities: int = int( quantities_constraints.max_right_entities[ left_label ] )
                model.add(
                    sum( is_assigned[ left_label, right_label ]
                         for right_label in problem.right_labels ) <= max_right_entities
                )

        if isinstance( quantities_constraints.min_right_entities, dict ):
            for left_label in problem.left_labels:
                min_right_entities: int = int( quantities_constraints.min_right_entities[ left_label ] )
                model.add(
                    sum( is_assigned[ left_label, right_label ]
                         for right_label in problem.right_labels ) >= min_right_entities
                )

        if isinstance( quantities_constraints.max_left_entities, dict ):
            for right_label in problem.right_labels:
                max_left_entities: int = int( quantities_constraints.max_left_entities[ right_label ] )
                model.add(
                    sum( is_assigned[ left_label, right_label ]
                         for left_label in problem.left_labels ) <= max_left_entities
                )

        if isinstance( quantities_constraints.min_left_entities, dict ):
            for right_label in problem.right_labels:
                min_left_entities: int = int( quantities_constraints.min_left_entities[ right_label ] )
                model.add(
                    sum( is_assigned[ left_label, right_label ]
                         for left_label in problem.left_labels ) >= min_left_entities
                )

        if quantities_constraints.multiple_same_assignment:
            if isinstance( quantities_constraints.max_same_assignments, dict ):
                for ( left_label,
                      right_label ), max_same_assignments in quantities_constraints.max_same_assignments.items():
                    model.add( quantities[ left_label, right_label ] <= int( max_same_assignments ) )

            if isinstance( quantities_constraints.min_same_assignments, dict ):
                for ( left_label,
                      right_label ), min_same_assignments in quantities_constraints.min_same_assignments.items():
                    model.add( quantities[ left_label, right_label ] >= int( min_same_assignments ) )

            if isinstance( quantities_constraints.max_right_assignments, dict ):
                for left_label in problem.left_labels:
                    max_right_assignments: int = int( quantities_constraints.max_right_assignments[ left_label ] )
                    model.add(
                        sum( quantities[ left_label, right_label ]
                             for right_label in problem.right_labels ) <= max_right_assignments
                    )

            if isinstance( quantities_constraints.min_right_assignments, dict ):
                for left_label in problem.left_labels:
                    min_right_assignments: int = int( quantities_constraints.min_right_assignments[ left_label ] )
                    model.add(
                        sum( quantities[ left_label, right_label ]
                             for right_label in problem.right_labels ) >= min_right_assignments
                    )

            if isinstance( quantities_constraints.max_left_assignments, dict ):
                for right_label in problem.right_labels:
                    max_left_assignments: int = int( quantities_constraints.max_left_assignments[ right_label ] )
                    model.add(
                        sum( quantities[ left_label, right_label ]
                             for left_label in problem.left_labels ) <= max_left_assignments
                    )

            if isinstance( quantities_constraints.min_left_assignments, dict ):
                for right_label in problem.right_labels:
                    min_left_assignments: int = int( quantities_constraints.min_left_assignments[ right_label ] )
                    model.add(
                        sum( quantities[ left_label, right_label ]
                             for left_label in problem.left_labels ) >= min_left_assignments
                    )
        else:
            for left_label, right_label in quantities:
                model.add( quantities[ left_label, right_label ] <= 1 )
