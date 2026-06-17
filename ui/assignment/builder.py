# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025-2026 AKKODIS.
# SPDX-FileContributor: Romain Baville
from typing import Optional
from domain.assignment.base import AssignmentProblem
from domain.assignment.matching.matching_config import MatchingConfig
from domain.assignment.ressources.ressources_config import RessourcesConfig


def build_entities_labels(
    entity_col_label: str,
    entity_rows: tuple[ dict[ str, str ], ...],
) -> tuple[ str, ...]:
    entities_labels: list[ str ] = []
    for entity_row in entity_rows:
        entities_labels.append( entity_row[ entity_col_label ] )

    return tuple( entities_labels )


def build_generic_constraints(
    entity_col_label: str,
    entity_rows: tuple[ dict[ str, str ], ...],
    generic_constraints_col_label: Optional[ str ] = None,
    generic_constraints_val: Optional[ float ] = None,
) -> dict[ str, float ]:
    generic_constraints: dict[ str, float ] = {}
    for entity_row in entity_rows:
        if generic_constraints_col_label is None and generic_constraints_val is not None:
            generic_constraints[ entity_row[ entity_col_label ] ] = generic_constraints_val
        elif generic_constraints_val is None and generic_constraints_col_label is not None:
            generic_constraints[ entity_row[ entity_col_label ] ] = float( entity_row[ generic_constraints_col_label ] )

    return generic_constraints


def build_vals(
    entity_col_label: str,
    variables_labels: tuple[ str, ... ] | dict[ str, str ],
    entity_rows: tuple[ dict[ str, str ], ...],
) -> dict[ tuple[ str, str ], float ]:
    vals: dict[ tuple[ str, str ], float ] = {}
    for entity_row in entity_rows:
        for variable_label in variables_labels:
            val: float
            try:
                val = float( entity_row[ variables_labels[ variable_label ] ] )
            except:
                val = float( entity_row[ variable_label ] )

            entity_label: str = entity_row[ entity_col_label ]
            vals[ ( entity_label, variable_label ) ] = val

    return vals


def build_problem( state ):
    """Build a generic assignment problem from raw CSV data."""

    matching_config: Optional[ MatchingConfig ] = None
    if state.use_matching:
        matching_config = MatchingConfig(
            labels = state.matching_labels,
            left_vals = state.matching_left_vals,
            right_vals = state.matching_right_vals,
            objective = state.matching_objective,
            reward_function = state.reward_function,
            penalty_function = state.penalty_function,
            weights = state.matching_weights,
            max_vals = state.matching_max_vals,
            min_vals = state.matching_min_vals,
        )

    ressources_config: Optional[ RessourcesConfig ] = None
    if state.use_ressources:
        ressources_config = RessourcesConfig(
            labels = state.ressources_labels,
            vals = state.ressources_vals,
            objectives = state.ressoucres_objectives,
            max_vals = state.ressoucres_max_vals,
            min_vals = state.ressoucres_min_vals,
            max_vals_global = state.ressoucres_max_vals_global,
            min_vals_global = state.ressoucres_min_vals_global,
        )

    problem: AssignmentProblem = AssignmentProblem(
        left_labels = state.left_labels,
        right_labels = state.right_labels,
        use_matching = state.use_matching,
        matching_config = matching_config,
        use_ressources = state.use_ressources,
        ressources_config = ressources_config,
        max_assignments = state.max_assignments,
        min_assignments = state.min_assignments,
        max_capacities = state.max_capacities,
        min_capacities = state.min_capacities,
        left_mutual_exclusions = state.left_mutual_exclusions,
        right_mutual_exclusions = state.right_mutual_exclusions,
    )

    return problem
