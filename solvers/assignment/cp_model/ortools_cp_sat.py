# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025-2026 AKKODIS.
# SPDX-FileContributor: Romain Baville

from ortools.sat.python.cp_model import FEASIBLE, OPTIMAL, CpModel, CpSolver, CpSolverStatus, IntVar

from domain.assignment.base import AssignmentProblem
from solvers.assignment.cp_model.constraints.solver_constraints import apply_constraints


def solve_assignment_problem( problem: AssignmentProblem ) -> dict[ str, list[ tuple[ str, int ] ] ]:
    """Solve an assignment problem using cp_model.

    Args:
        problem (AssignmentProblem): The assignment problem to solve

    Returns:
        dict[str, list[tuple[str, int]]]: The result of the assignment problem:
            keys (str): The left entity label assigned.
            values (list[tuple[str, int]]): All the right labels with its number of assignment for the left label.

    Raises:
        RuntimeError: No feasible assignment found for the problem.

    """
    model: CpModel = CpModel()

    # --------------------------------------------------
    # Variables
    # --------------------------------------------------
    is_assigned: dict[ tuple[ str, str ], IntVar ] = {}
    quantities: dict[ tuple[ str, str ], IntVar ] = {}

    for left_label in problem.left_labels:
        for right_label in problem.right_labels:
            is_assigned[ left_label,
                         right_label ] = model.new_bool_var( f"{ left_label } is associated with { right_label }" )
            quantities[ left_label, right_label ] = model.new_int_var(
                0, 1000000000, f"quantity of { left_label } associated with { right_label }"
            )

            model.add( quantities[ left_label,
                                   right_label ] == 0 ).OnlyEnforceIf( is_assigned[ left_label, right_label ].Not() )
            model.add( quantities[ left_label,
                                   right_label ] >= 1 ).OnlyEnforceIf( is_assigned[ left_label, right_label ] )

    # --------------------------------------------------
    # Constraints
    # --------------------------------------------------
    apply_constraints( model, is_assigned, quantities, problem )

    # --------------------------------------------------
    # Objective
    # --------------------------------------------------
    model.maximize(
        sum(
            problem.compute_matching_score( left_label, right_label ) * is_assigned[ left_label, right_label ] +
            problem.compute_ressources_score( left_label ) * quantities[ left_label, right_label ]
            for left_label, right_label in is_assigned
        )
    )

    # --------------------------------------------------
    # Solve
    # --------------------------------------------------
    solver: CpSolver = CpSolver()
    status: CpSolverStatus = solver.solve( model )

    if status not in ( OPTIMAL, FEASIBLE ):
        raise RuntimeError( "No feasible assignment found for the problem." )

    # --------------------------------------------------
    # Extract solution
    # --------------------------------------------------
    result: dict[ str, list[ tuple[ str, int ] ] ] = {}
    for ( left_label, right_label ) in quantities:
        nb_assignments: int = solver.value( quantities[ left_label, right_label ] )
        if nb_assignments >= 1:
            if left_label not in result:
                result[ left_label ] = []
            result[ left_label ].append( ( right_label, nb_assignments ) )

    return result
