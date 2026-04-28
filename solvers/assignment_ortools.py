# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025-2026 AKKODIS.
# SPDX-FileContributor: Romain Baville

from ortools.sat.python import cp_model
from solvers.base import Solver

class ORToolsAssignmentSolver(Solver):
    def solve(self, problem):
        model = cp_model.CpModel()

        x = {
            (i, j): model.NewBoolVar(f"x_{i}_{j}")
            for i in problem.employees
            for j in problem.projects
        }

        # One project per employee
        for i in problem.employees:
            model.Add(sum(x[i, j] for j in problem.projects) <= 1)

        # Skill requirements
        for j in problem.projects:
            for k in problem.skills:
                model.Add(
                    sum(
                        problem.skill_matrix[i, k] * x[i, j]
                        for i in problem.employees
                    ) >= problem.requirements[j, k]
                )

        # Objective: maximize total skill contribution
        model.Maximize(
            sum(
                problem.skill_matrix[i, k] * x[i, j]
                for i in problem.employees
                for j in problem.projects
                for k in problem.skills
            )
        )

        solver = cp_model.CpSolver()
        status = solver.Solve(model)

        if status not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
            raise RuntimeError("No feasible assignment")

        return {
            i: j
            for i in problem.employees
            for j in problem.projects
            if solver.Value(x[i, j]) == 1
        }
