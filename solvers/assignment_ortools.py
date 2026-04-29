# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025-2026 AKKODIS.
# SPDX-FileContributor: Romain Baville

from ortools.sat.python import cp_model
from solvers.base import Solver


class ORToolsAssignmentSolver(Solver):
    """
    Generic OR-Tools solver for AssignmentStructure
    """

    def solve(self, structure):
        structure.validate()

        model = cp_model.CpModel()

        x = {
            (l, r): model.NewBoolVar(f"x_{l}_{r}")
            for l in structure.left_entities
            for r in structure.right_entities
        }

        # Capacity constraint
        for l in structure.left_entities:
            model.Add(
                sum(x[l, r] for r in structure.right_entities)
                <= structure.max_left_assignments
            )

        # Requirements
        for r in structure.right_entities:
            for a in structure.attributes:
                model.Add(
                    sum(
                        structure.left_attributes[l, a] * x[l, r]
                        for l in structure.left_entities
                    )
                    >= structure.right_requirements[r, a]
                )

        # Objective
        model.Maximize(
            sum(
                structure.left_attributes[l, a] * x[l, r]
                for l in structure.left_entities
                for r in structure.right_entities
                for a in structure.attributes
            )
        )

        solver = cp_model.CpSolver()
        status = solver.Solve(model)

        if status not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
            raise RuntimeError("No feasible assignment")

        return {
            l: r
            for (l, r) in x
            if solver.Value(x[l, r]) == 1
        }
