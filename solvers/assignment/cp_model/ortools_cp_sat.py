# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025-2026 AKKODIS.
# SPDX-FileContributor: Romain Baville

from ortools.sat.python import cp_model

from solvers.base import Solver
from domain.assignment.base import AssignmentProblem

from solvers.assignment.cp_model.constraints.generic_constraints import apply_generic_constraints
from solvers.assignment.cp_model.constraints.logical_constraints import apply_logical_constraints
from solvers.assignment.cp_model.constraints.matching_constraints import apply_matching_constraints
from solvers.assignment.cp_model.constraints.ressources_contraints import apply_ressources_constraints

class ORToolsAssignmentSolver( Solver ):
    """
    Generic OR-Tools CP-SAT solver for assignment problems.
    """

    def solve( self, problem: AssignmentProblem ):

        model = cp_model.CpModel()

        # --------------------------------------------------
        # Variables
        # --------------------------------------------------
        x = {
            ( left_label, right_label ): model.NewBoolVar( f"x_{ left_label }_{ right_label }" )
            for left_label in problem.left_labels
            for right_label in problem.right_labels
        }

        # --------------------------------------------------
        # Constraints
        # --------------------------------------------------
        apply_generic_constraints( model, x, problem )
        apply_logical_constraints( model, x, problem )
        apply_matching_constraints( model, x, problem )
        apply_ressources_constraints( model, x, problem )

        # --------------------------------------------------
        # Objective
        # --------------------------------------------------
        model.Maximize(
            sum(
                problem.compute_score( left_label, right_label ) * x[ left_label, right_label ] for left_label, right_label in x
            )
        )

        # --------------------------------------------------
        # Solve
        # --------------------------------------------------
        solver = cp_model.CpSolver()
        status = solver.Solve( model )

        if status not in ( cp_model.OPTIMAL, cp_model.FEASIBLE ):
            raise RuntimeError( "No feasible assignment found" )

        # --------------------------------------------------
        # Extract solution
        # --------------------------------------------------
        result = {}
        for ( left_label, right_label ) in x:
            if solver.Value( x[ left_label, right_label ] ) == 1:
                if left_label not in result:
                    result[ left_label ] = []
                result[ left_label ].append( right_label )

        return result
