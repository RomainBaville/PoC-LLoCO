# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025-2026 AKKODIS.
# SPDX-FileContributor: Romain Baville

from ortools.sat.python.cp_model import CpModel, CpSolver, IntVar, CpSolverStatus, OPTIMAL, FEASIBLE

from domain.assignment.base import AssignmentProblem

from solvers.assignment.cp_model.constraints.quantities_constraints import apply_quantities_constraints
from solvers.assignment.cp_model.constraints.logical_constraints import apply_logical_constraints
from solvers.assignment.cp_model.constraints.matching_constraints import apply_matching_constraints
from solvers.assignment.cp_model.constraints.ressources_contraints import apply_ressources_constraints


def solve_assignment_problem( problem: AssignmentProblem ) -> dict[ str, tuple[ tuple[ str, int ], ...] ]:
    """Solve an assignment problem using cp_model.

    Args:
        problem (AssignmentProblem): The assignment problem to solve

    Returns:
        dict[str, tuple[tuple[str, int], ...]]: The result of the assignment problem:
            keys (str): The left entity label assigned.
            values (tuple[tuple[str, int], ...]): All the right labels with its number of assignment for the left label.

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
            is_assigned[ left_label, right_label ] = model.new_bool_var( f"{ left_label } is associated with { right_label }" )
            quantities[ left_label, right_label ] = model.new_int_var( 0, 1000000000, f"quantity of { left_label } associated with { right_label }")

            model.add( quantities[ left_label, right_label ] == 0 ).OnlyEnforceIf( is_assigned[ left_label, right_label ].Not() )
            model.add( quantities[ left_label, right_label ] >= 1 ).OnlyEnforceIf( is_assigned[ left_label, right_label ] )

    # --------------------------------------------------
    # Constraints
    # --------------------------------------------------
    apply_quantities_constraints( model, quantities, is_assigned, problem )
    apply_logical_constraints( model, is_assigned, problem )
    apply_matching_constraints( model, is_assigned, problem )
    apply_ressources_constraints( model, quantities, problem )

    # --------------------------------------------------
    # Objective
    # --------------------------------------------------
    model.maximize(
        sum(
            problem.compute_matching_score( left_label, right_label ) * is_assigned[ left_label, right_label ] + problem.compute_ressources_score( left_label ) * quantities[ left_label, right_label ] for left_label, right_label in is_assigned
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
        if solver.Value( quantities[ left_label, right_label ] ) >= 1:
            if left_label not in result:
                result[ left_label ] = []
            result[ left_label ].append( ( right_label, solver.value( quantities[ left_label, right_label ] ) ) )

    return result
