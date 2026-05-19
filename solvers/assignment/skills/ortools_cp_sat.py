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
    OR-Tools CP-SAT solver for all skill-based assignment variants.
    """

    def solve(self, problem):
        if isinstance(problem, SkillCoverageAssignment):
            return self._solve_coverage(problem)

        if isinstance(problem, SkillBestFitAssignment):
            return self._solve_best_fit(problem)

        if isinstance(problem, SkillTeamAssignment):
            raise NotImplementedError(
                "Team-based skill assignment not implemented yet"
            )

        if isinstance(problem, SkillPortfolioSelection):
            raise NotImplementedError(
                "Skill portfolio selection not implemented yet"
            )

        raise TypeError(
            f"Unsupported problem type: {type(problem).__name__}"
        )

    # --------------------------------------------------
    # Coverage variant
    # --------------------------------------------------
    def _solve_coverage(self, problem: SkillCoverageAssignment):
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

        for r in problem.right_entities:
            for s in problem.skills:
                model.Add(
                    sum(
                        problem.left_skills[(l, s)] * x[l, r]
                        for l in problem.left_entities
                    )
                    >= problem.right_requirements[(r, s)]
                )

        model.Maximize(
            sum(
                problem.left_skills[(l, s)] * x[l, r]
                for l, r in x
                for s in problem.skills
            )
        )

        solver = cp_model.CpSolver()
        status = solver.Solve(model)

        if status not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
            raise RuntimeError("No feasible assignment found")

        return {
            l: r for (l, r) in x if solver.Value(x[l, r]) == 1
        }

    # --------------------------------------------------
    # Best-fit variant
    # --------------------------------------------------
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
            raise RuntimeError("No feasible assignment found")

        return {
            l: r for (l, r) in x if solver.Value(x[l, r]) == 1
        }
