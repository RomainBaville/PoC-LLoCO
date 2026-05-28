# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025-2026 AKKODIS.
# SPDX-FileContributor: Romain Baville

from importlib import import_module
from domain.entity_registry import EntityRegistry


def build_problem(state, left_rows, right_rows):
    """
    Build a generic assignment problem from raw CSV data.

    This function is type-driven (skills, cost, etc.),
    not variant-driven anymore.
    """

    # ---------------------------------------------
    # Build LEFT entities
    # ---------------------------------------------
    left_registry = EntityRegistry(prefix="left")

    left_entities = []
    left_skills = {}

    for row in left_rows:
        label = " ".join(row[c] for c in state.left_id_cols)
        left_id = left_registry.create(label)
        left_entities.append(left_id)

        for skill in state.skill_cols:
            left_skills[(left_id, skill)] = int(row.get(skill, 0))

    # ---------------------------------------------
    # Build RIGHT entities
    # ---------------------------------------------
    right_entities = []
    right_requirements = {}

    for row in right_rows:
        right_id = row[state.right_id_col]
        right_entities.append(right_id)

        for skill in state.skill_cols:
            right_requirements[(right_id, skill)] = int(row.get(skill, 0))

    # ---------------------------------------------
    # Build domain problem via TYPE registry
    # ---------------------------------------------
    assignment_type = state.assignment_type  # ✅ ONLY TYPE

    type_registry = import_module(
        f"ui.problems.assignment.{assignment_type}.registry"
    )

    model = type_registry.ASSIGNMENT_MODEL

    problem_data = {
        "left_entities": left_entities,
        "right_entities": right_entities,
        "skills": state.skill_cols,
        "left_skills": left_skills,
        "right_requirements": right_requirements,
    }

    problem = model.builder_fn(problem_data)

    return problem, left_registry.labels
