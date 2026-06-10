# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025-2026 AKKODIS.
# SPDX-FileContributor: Romain Baville

from ortools.sat.python import cp_model

from solvers.base import Solver
from domain.assignment.scoring import compute

from solvers.assignment.cp_model.constraints.generic_constraints import (
    apply_left_constraints,
    apply_right_constraints,
)

from solvers.assignment.cp_model.constraints.logical_constraints import apply_logical_constraints
from solvers.assignment.cp_model.constraints.skills_constraints import apply_skill_constraints
from solvers.assignment.cp_model.constraints.costs_contraints import apply_cost_constraints

class ORToolsAssignmentSolver( Solver ):
    """
    Generic OR-Tools CP-SAT solver for assignment problems.
    """

    def solve( self, problem ):

        model = cp_model.CpModel()

        # --------------------------------------------------
        # Variables
        # --------------------------------------------------
        x = {
            ( l, r ): model.NewBoolVar( f"x_{ l }_{ r }" )
            for l in problem.left_entities
            for r in problem.right_entities
        }

        # --------------------------------------------------
        # Constraints
        # --------------------------------------------------
        apply_left_constraints( model, x, problem )
        apply_right_constraints( model, x, problem )
        apply_logical_constraints( model, x, problem )
        apply_skill_constraints( model, x, problem )
        apply_cost_constraints( model, x, problem )

        # --------------------------------------------------
        # Objective
        # --------------------------------------------------
        model.Maximize( sum( compute( problem, l, r ) * x[ l, r ] for l, r in x ) )

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
        for ( l, r ) in x:
            if solver.Value( x[ l, r ] ) == 1:
                if l not in result:
                    result[ l ] = []
                result[ l ].append( r )

        return result
