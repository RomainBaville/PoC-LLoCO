# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025-2026 AKKODIS.
# SPDX-FileContributor: Romain Baville

from ortools.sat.python import cp_model
from solvers.base import Solver

from domain.assignment.skills.coverage import SkillCoverageAssignment
from domain.assignment.skills.best_fit import SkillBestFitAssignment
from domain.assignment.skills.team import SkillTeamAssignment
from domain.assignment.skills.portfolio import SkillPortfolioSelection


class ORToolsSkillAssignmentSolver(Solver):
    """
    OR-Tools CP-SAT solver for skill-based assignment problems.

    Supports multiple skill assignment variants via domain dispatch.
    """

    # ==================================================
    # Public entry point
    # ==================================================
    def solve(self, problem):
        if isinstance(problem, SkillCoverageAssignment):
            return self._solve_coverage(problem)

        if isinstance(problem, SkillBestFitAssignment):
            return self._solve_best_fit(problem)

        if isinstance(problem, SkillTeamAssignment):
            return self._solve_team(problem)

        if isinstance(problem, SkillPortfolioSelection):
            return self._solve_portfolio(problem)

        raise TypeError(
            f"Unsupported skill assignment problem type: {type(problem)}"
        )

    # ==================================================
    # Variant 1 — Skill coverage assignment
    # ==================================================
    def _solve_coverage(self, problem: SkillCoverageAssignment):
        problem.validate()

        model = cp_model.CpModel()

        x = {
            (l, r): model.NewBoolVar(f"x_{l}_{r}")
            for l in problem.left_entities
            for r in problem.right_entities
        }

        # Left capacity
        for l in problem.left_entities:
            model.Add(
                sum(x[l, r] for r in problem.right_entities)
                <= problem.max_assignments_per_left
            )

        # Skill requirements
        for r in problem.right_entities:
            for s in problem.skills:
                model.Add(
                    sum(
                        problem.left_skills[(l, s)] * x[l, r]
                        for l in problem.left_entities
                    )
                    >= problem.right_requirements[(r, s)]
                )

        # Objective: maximize total skill coverage
        model.Maximize(
            sum(
                problem.left_skills[(l, s)] * x[l, r]
                for (l, r) in x
                for s in problem.skills
            )
        )

        solver = cp_model.CpSolver()
        status = solver.Solve(model)

        if status not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
            raise RuntimeError("No feasible skill coverage assignment found")

        return {
            l: r for (l, r) in x if solver.Value(x[l, r]) == 1
        }

    # ==================================================
    # Variant 2 — Best-fit matching (soft skills)
    # ==================================================
    def _solve_best_fit(self, problem: SkillBestFitAssignment):
        problem.validate()

        model = cp_model.CpModel()

        x = {
            (l, r): model.NewBoolVar(f"x_{l}_{r}")
            for l in problem.left_entities
            for r in problem.right_entities
        }

        for l in problem.left_entities:
            model.Add(
                sum(x[l, r] for r in problem.right_entities)
                <= problem.max_assignments_per_left
            )

        # Objective: maximize similarity
        model.Maximize(
            sum(
                min(
                    problem.left_skills[(l, s)],
                    problem.target_preferences.get((r, s), 0),
                ) * x[l, r]
                for l, r in x
                for s in problem.skills
            )
        )

        solver = cp_model.CpSolver()
        status = solver.Solve(model)

        if status not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
            raise RuntimeError("No feasible best-fit assignment found")

        return {
            l: r for (l, r) in x if solver.Value(x[l, r]) == 1
        }

    # ==================================================
    # Variant 3 — Team formation
    # ==================================================
    def _solve_team(self, problem: SkillTeamAssignment):
        raise NotImplementedError(
            "Team-based skill assignment is not implemented yet."
        )

    # ==================================================
    # Variant 4 — Portfolio selection
    # ==================================================
    def _solve_portfolio(self, problem: SkillPortfolioSelection):
        raise NotImplementedError(
            "Skill portfolio selection is not implemented yet."
        )
