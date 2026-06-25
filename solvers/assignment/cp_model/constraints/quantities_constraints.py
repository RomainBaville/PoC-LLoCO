# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025-2026 AKKODIS.
# SPDX-FileContributor: Romain Baville

from domain.assignment.base import AssignmentProblem
from domain.assignment.constraints.quantities_constraints import QuantitiesConstraints
from ortools.sat.python.cp_model import CpModel, IntVar

def apply_quantities_constraints(
    model: CpModel,
    quantities_variable: dict[ tuple[ str, str ], IntVar ],
    assignment_variable: dict[ tuple[ str, str ], IntVar ],
    problem: AssignmentProblem,
) -> None:
    if problem.constraints_config.use_quantities_constraints:
        quantities_constraints: QuantitiesConstraints = problem.constraints_config.quantities_constraints

        if quantities_constraints.max_right_entities is not None:
            for left_label in problem.left_labels:
                max_right_entities: int = int( quantities_constraints.max_right_entities[ left_label ] )
                model.add(
                    sum(
                        assignment_variable[ left_label, right_label ] for right_label in problem.right_labels
                    ) <= max_right_entities
                )

        if quantities_constraints.min_right_entities is not None:
            for left_label in problem.left_labels:
                min_right_entities: int = int( quantities_constraints.min_right_entities[ left_label ] )
                model.add(
                    sum(
                        assignment_variable[ left_label, right_label ] for right_label in problem.right_labels
                    ) >= min_right_entities
                )

        if quantities_constraints.max_left_entities is not None:
            for right_label in problem.right_labels:
                max_left_entities: int = int( quantities_constraints.max_left_entities[ right_label ] )
                model.add(
                    sum(
                        assignment_variable[ left_label, right_label ] for left_label in problem.left_labels
                    ) <= max_left_entities
                )

        if quantities_constraints.min_left_entities is not None:
            for right_label in problem.right_labels:
                min_left_entities: int = int( quantities_constraints.min_left_entities[ right_label ] )
                model.add(
                    sum(
                        assignment_variable[ left_label, right_label ] for left_label in problem.left_labels
                    ) >= min_left_entities
                )

        if not quantities_constraints.multiple_same_assignment:
            for left_label, right_label in quantities_variable:
                model.add( quantities_variable[ left_label, right_label ] <= 1 )
