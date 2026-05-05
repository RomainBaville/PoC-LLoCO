# SPDX-License-Identifier: Apache-2.0
from ortools.sat.python import cp_model
from solvers.base import Solver
from domain.assignment.skills import SkillBasedAssignmentProblem


class ORToolsSkillAssignmentSolver(Solver):

    def solve(self, problem: SkillBasedAssignmentProblem):
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
                        problem.left_skills[l, s] * x[l, r]
                        for l in problem.left_entities
                    )
                    >= problem.right_requirements[r, s]
                )

        model.Maximize(
            sum(
                problem.left_skills[l, s] * x[l, r]
                for (l, r) in x
                for s in problem.skills
            )
        )

        solver = cp_model.CpSolver()
        solver.Solve(model)

        return {
            l: r for (l, r) in x if solver.Value(x[l, r]) == 1
        }
