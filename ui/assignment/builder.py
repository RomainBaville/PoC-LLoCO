# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025-2026 AKKODIS.
# SPDX-FileContributor: Romain Baville
from typing import Optional
from domain.assignment.base import AssignmentProblem
from domain.assignment.skills.skills_config import SkillsConfig


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
            dict_skills[ ( entity_label, skill_label ) ] = int( row[ skill_label ] )

    return entity_labels, dict_skills


def build_problem( state ):
    """Build a generic assignment problem from raw CSV data."""

    skills_config: Optional[ SkillsConfig ]
    if state.use_skills:
        skills_config = SkillsConfig(
            skills_label = state.skills_label,
            left_skills_val = state.left_skills_val,
            right_skills_val = state.right_skills_val,
            skills_objective = state.skills_objective,
            skills_weight = state.skills_weight,
            skills_reward_function = state.skills_reward_function,
            skills_penalty_function = state.skills_penalty_function,
        )
    else:
        skills_config = None

    problem: AssignmentProblem = AssignmentProblem(
        left_entities = state.left_entities,
        right_entities = state.right_entities,
        min_assignments_per_left = state.min_assignments_per_left,
        max_assignments_per_left = state.max_assignments_per_left,
        min_capacities_per_right = state.min_capacities_per_right,
        max_capacities_per_right = state.max_capacities_per_right,
        left_mutual_exclusions = state.left_mutual_exclusions,
        right_mutual_exclusions = state.right_mutual_exclusions,
        use_skills = state.use_skills,
        skills_config = skills_config,
    )

    return problem
