# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025-2026 AKKODIS.
# SPDX-FileContributor: Romain Baville

from ortools.sat.python import cp_model

from solvers.base import Solver
from domain.assignment.skills.scoring import ScoringEngine

from solvers.assignment.skills.constraints import (
    apply_left_constraints,
    apply_right_constraints,
)

from solvers.assignment.skills.coverage_constraints import apply_coverage_constraints
from solvers.assignment.skills.logical_constraints import apply_logical_constraints


class ORToolsSkillAssignmentSolver(Solver):
    """
    Generic OR-Tools CP-SAT solver for skill-based assignment problems.

    Behavior (coverage, best-fit, hybrid, constraints) is controlled
    entirely via problem.config.
    """

    def solve(self, problem):
        problem.validate()

        model = cp_model.CpModel()

        # --------------------------------------------------
        # Variables
        # --------------------------------------------------
        x = {
            (l, r): model.NewBoolVar(f"x_{l}_{r}")
            for l in problem.left_entities
            for r in problem.right_entities
        }

        # --------------------------------------------------
        # Constraints (modular)
        # --------------------------------------------------
        apply_left_constraints(model, x, problem)
        apply_right_constraints(model, x, problem)
        apply_coverage_constraints(model, x, problem)
        apply_logical_constraints(model, x, problem)

        # --------------------------------------------------
        # Objective (scoring engine)
        # --------------------------------------------------
        engine = ScoringEngine(problem.config)

        model.Maximize(
            sum(
                engine.compute(problem, l, r) * x[l, r]
                for (l, r) in x
            )
        )

        # --------------------------------------------------
        # Solve
        # --------------------------------------------------
        solver = cp_model.CpSolver()
        status = solver.Solve(model)

        if status not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
            raise RuntimeError("No feasible assignment found")

        # --------------------------------------------------
        # Extract solution
        # --------------------------------------------------
        return {
            l: r for (l, r) in x if solver.Value(x[l, r]) == 1
        }
