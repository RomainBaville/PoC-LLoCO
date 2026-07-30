# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025-2026 AKKODIS.
# SPDX-FileContributor: Romain Baville

from ortools.sat.python.cp_model import CpModel, IntVar

from domain.assignment.score.matching_config import MatchingConfig


def apply_matching_constraints(
    model: CpModel,
    is_assigned: dict[ tuple[ str, str ], IntVar ],
    matching_config: MatchingConfig,
    left_labels: tuple[ str, ...]
) -> None:
    """Add to the model the matching constraints if needed.

    Args:
        model (CpModel): The model used.
        is_assigned (dict[tuple[str, str], IntVar]): The binary variable with 1 for assigned 0 otherwize.
        matching_config (MatchingConfig): The matching config with the constraints of assignment problem.
        left_labels (tuple[str, ...]): The left entities labels.
    """
    if isinstance( matching_config.max_vals, dict ):
        for left_label in left_labels:
            for ( right_label, left_variable_label ), max_val in matching_config.max_vals.items():
                left_val = int( matching_config.left_vals[ left_label, left_variable_label ] )
                model.add( left_val * is_assigned[ left_label, right_label ] <= int( max_val ) )

    if isinstance( matching_config.min_vals, dict ):
        for left_label in left_labels:
            for ( right_label, left_variable_label ), min_val in matching_config.min_vals.items():
                left_val = int( matching_config.left_vals[ left_label, left_variable_label ] )
                model.add( left_val * is_assigned[ left_label, right_label ] >= int( min_val ) )
