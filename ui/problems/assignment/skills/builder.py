# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025-2026 AKKODIS.
# SPDX-FileContributor: Romain Baville

from importlib import import_module


def build_dict( entity_col_id, rows, extrema_col_label=None, extrema=None ):
    dict = {}
    for row in rows:
        if extrema_col_label is None:
            dict[ row[ entity_col_id ] ] = extrema
        else:
            dict[ row[ entity_col_id ] ] = int(row[ extrema_col_label ])
    return dict


def build_parameters( skills_labels, entity_col_id, rows ):
    dict_skills = {}
    entity_labels = []
    for row in rows:
        entity_label = row[ entity_col_id ]
        entity_labels.append( entity_label )
        for skill_label in skills_labels:
            dict_skills[ ( entity_label, skill_label) ] = int(row[ skill_label ])

    return entity_labels, dict_skills


def build_problem(state):
    """
    Build a generic assignment problem from raw CSV data.

    This function is type-driven (skills, cost, etc.),
    not variant-driven anymore.
    """
    # ---------------------------------------------
    # Build domain problem via TYPE registry
    # ---------------------------------------------
    assignment_type = state.assignment_type

    type_registry = import_module(
        f"ui.problems.assignment.{assignment_type}.registry"
    )

    model = type_registry.ASSIGNMENT_MODEL

    problem_data = {
        "left_entities": state.left_entities,
        "right_entities": state.right_entities,
        "skills": state.skill_labels,
        "left_skills": state.left_skills,
        "right_requirements": state.right_requirements,
    }

    problem = model.builder_fn(problem_data)

    cfg = problem.config

    # --- structure
    cfg.min_assignments_per_left = state.min_assignments_per_left
    cfg.max_assignments_per_left = state.max_assignments_per_left

    cfg.min_capacities_per_right = state.min_capacities_per_right
    cfg.max_capacities_per_right = state.max_capacities_per_right

    # --- objective
    cfg.objective = state.objective

    cfg.reward_mode = state.reward_mode
    cfg.penalty_mode = state.penalty_mode
    cfg.penalty_weight = state.penalty_weight
    cfg.skill_weight = state.skill_weights

    return problem
