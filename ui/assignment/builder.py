# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025-2026 AKKODIS.
# SPDX-FileContributor: Romain Baville
from typing import Optional
from domain.assignment.base import AssignmentProblem
from domain.assignment.matching.matching_config import MatchingConfig
from domain.assignment.ressources.ressources_config import RessourcesConfig


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


def build_val_dict( entities: list[ str ], features_label: list[ str ] | dict[ str, str ], rows ):
    val_dict: dict[ list[ str ], float ] = {}
    for i, row in enumerate( rows ):
        entity: str = entities[ i ]
        for feature in features_label:
            try:
                val_dict[ ( entity, features_label[ feature ] ) ] = float( row[ feature ] )
            except:
                val_dict[ ( entity, feature ) ] = float( row[ feature ] )


    return val_dict



def build_problem( state ):
    """Build a generic assignment problem from raw CSV data."""

    matching_config: Optional[ MatchingConfig ] = None
    if state.use_matching:
        matching_config = MatchingConfig(
            labels=state.matching_labels,
            left_vals=state.matching_left_vals,
            right_vals=state.matching_right_vals,
            objective=state.matching_objective,
            reward_function=state.reward_function,
            penalty_function=state.penalty_function,
            weights=state.matching_weights,
            max_vals=state.matching_max_vals,
            min_vals=state.matching_min_vals,
        )

    ressources_config: Optional[ RessourcesConfig ] = None
    if state.use_ressources:
        ressources_config = RessourcesConfig(
            labels=state.ressources_labels,
            vals = state.ressources_vals,
            objectives = state.ressoucres_objectives,
            max_vals=state.ressoucres_max_vals,
            min_vals=state.ressoucres_min_vals,
            max_vals_global=state.ressoucres_max_vals_global,
            min_vals_global=state.ressoucres_min_vals_global,
        )

    problem: AssignmentProblem = AssignmentProblem(
        left_labels=state.left_labels,
        right_labels=state.right_labels,
        use_matching=state.use_matching,
        matching_config=matching_config,
        use_ressources=state.use_ressources,
        ressources_config=ressources_config,
        max_assignments=state.max_assignments,
        min_assignments=state.min_assignments,
        max_capacities=state.max_capacities,
        min_capacities=state.min_capacities,
        left_mutual_exclusions=state.left_mutual_exclusions,
        right_mutual_exclusions=state.right_mutual_exclusions,
    )

    return problem
