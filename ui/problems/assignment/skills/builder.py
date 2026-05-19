# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025-2026 AKKODIS.
# SPDX-FileContributor: Romain Baville

from importlib import import_module
from domain.entity_registry import EntityRegistry


def build_problem(state, left_rows, right_rows):
    """
    Generic builder for skill-based assignment problems.
    Completely registry-driven.
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
    # Resolve variant registry dynamically
    # ---------------------------------------------
    assignment_type, variant_key = state.assignment_variant.split("_", 1)

    type_registry = import_module(
        f"ui.problems.assignment.{assignment_type}.registry"
    )
    variant = type_registry.VARIANTS.get(variant_key)

    if not variant:
        raise ValueError(f"Unknown assignment variant: {state.assignment_variant}")

    # ---------------------------------------------
    # Build domain problem via variant builder
    # ---------------------------------------------
    problem_data = {
        "left_entities": left_entities,
        "right_entities": right_entities,
        "skills": state.skill_cols,
        "left_skills": left_skills,
        "right_requirements": right_requirements,
    }

    problem = variant.builder_fn(problem_data)

    return problem, left_registry.labels
