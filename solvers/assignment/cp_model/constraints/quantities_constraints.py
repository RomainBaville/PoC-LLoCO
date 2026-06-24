# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025-2026 AKKODIS.
# SPDX-FileContributor: Romain Baville

from domain.assignment.base import AssignmentProblem
from ortools.sat.python.cp_model import CpModel, IntVar

def apply_quantities_constraints(
    model: CpModel,
    quantities_variable: dict[ tuple[ str, str ], IntVar ],
    assignment_variable: dict[ tuple[ str, str ], IntVar ],
    problem: AssignmentProblem,
) -> None:
    if problem.max_assignments is not None:
        for ( left_label, right_label ), max_assignments in problem.max_assignments.items():
            model.add( quantities_variable[ left_label, right_label ] <= int( max_assignments ) )

    if problem.min_assignments is not None:
        for ( left_label, right_label ), min_assignments in problem.min_assignments.items():
            model.add( quantities_variable[ left_label, right_label ] <= int( min_assignments ) )

    for left_label in problem.left_labels:
        if problem.max_several_assignments is not None:
            max_several_assignments = int( problem.max_several_assignments[ left_label ] )
            model.add(
                sum(
                    assignment_variable[ left_label, right_label ] for right_label in problem.right_labels
                ) <= max_several_assignments
            )

        if problem.min_several_assignments is not None:
            min_several_assignments = int( problem.min_several_assignments[ left_label ] )
            model.add(
                sum(
                    assignment_variable[ left_label, right_label ] for right_label in problem.right_labels
                ) >= min_several_assignments
            )

        if problem.max_assignments_global is not None:
            max_assignments_global = int( problem.max_assignments_global[ left_label ] )
            model.add(
                sum(
                    quantities_variable[ left_label, right_label ] for right_label in problem.right_labels
                ) <= max_assignments_global
            )

        if problem.min_assignments_global is not None:
            min_assignments_global = int( problem.min_assignments_global[ left_label ] )
            model.add(
                sum(
                    quantities_variable[ left_label, right_label ] for right_label in problem.right_labels
                ) >= min_assignments_global
            )

    if problem.max_capacities is not None:
        for ( left_label, right_label ), max_capacities in problem.max_capacities.items():
            model.add( quantities_variable[ left_label, right_label ] <= int( max_capacities ) )

    if problem.min_capacities is not None:
        for ( left_label, right_label ), min_capacities in problem.min_capacities.items():
            model.add( quantities_variable[ left_label, right_label ] <= int( min_capacities ) )

    for right_label in problem.right_labels:
        if problem.max_several_capacities is not None:
            max_several_capacities = int( problem.max_several_capacities[ left_label ] )
            model.add(
                sum(
                    assignment_variable[ left_label, right_label ] for right_label in problem.right_labels
                ) <= max_several_capacities
            )

        if problem.min_several_capacities is not None:
            min_several_capacities = int( problem.min_several_capacities[ left_label ] )
            model.add(
                sum(
                    assignment_variable[ left_label, right_label ] for right_label in problem.right_labels
                ) >= min_several_capacities
            )

        if problem.max_capacities_global is not None:
            max_capacities_global = int( problem.max_capacities_global[ right_label ] )
            model.add(
                sum(
                    quantities_variable[ left_label, right_label ] for left_label in problem.left_labels
                ) <= max_capacities_global
            )

        if problem.min_capacities_global is not None:
            min_capacities_global = int( problem.min_capacities_global[ right_label ] )
            model.add(
                sum(
                    quantities_variable[ left_label, right_label ] for left_label in problem.left_labels
                ) >= min_capacities_global
            )
