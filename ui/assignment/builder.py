# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025-2026 AKKODIS.
# SPDX-FileContributor: Romain Baville
from typing import Optional
from domain.assignment.base import AssignmentProblem
from domain.assignment.skills.skills_config import SkillsConfig
from domain.assignment.costs.costs_config import CostsConfig


def build_entities( entity_col_id, rows ):
    entities = []
    for row in rows:
        entity = row[ entity_col_id ]
        entities.append( entity )

    return entities


def build_extrema_dict( entity_col_id, rows, extrema_col_label=None, extrema=None ):
    extrema_dict = {}
    for row in rows:
        if extrema_col_label is None:
            extrema_dict[ row[ entity_col_id ] ] = extrema
        else:
            extrema_dict[ row[ entity_col_id ] ] = int(row[ extrema_col_label ])
    return extrema_dict


def build_val_dict( entities: list[ str ], features_label: list[ str ], rows ):
    val_dict: dict[ list[ str ], float ] = {}
    for i, row in enumerate( rows ):
        entity: str = entities[ i ]
        for feature in features_label:
            val_dict[ ( entity, feature ) ] = float( row[ feature ] )

    return val_dict



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

    costs_config: Optional[ CostsConfig ]
    if state.use_costs:
        costs_config = CostsConfig(
            costs_label = state.costs_label,
            costs_val = state.costs_val,
            costs_objective = state.costs_objective,
            limit_costs_label = state.limit_costs_label,
            limit_costs_val = state.limit_costs_val,
        )
    else:
        costs_config = None

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
        use_costs = state.use_costs,
        costs_config = costs_config,
    )

    return problem
