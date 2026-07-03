# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025-2026 AKKODIS.
# SPDX-FileContributor: Romain Baville

from ortools.sat.python.cp_model import CpModel, IntVar

from domain.assignment.base import AssignmentProblem
from domain.assignment.score.matching_config import MatchingConfig


def apply_matching_constraints(
    model: CpModel,
    is_assigned: dict[ tuple[ str, str ], IntVar ],
    problem: AssignmentProblem,
) -> None:
    """Add to the model the matching constraints if needed.

    Args:
        model (CpModel): The model used.
        is_assigned (dict[tuple[str, str], IntVar]): The binary variable with 1 for assigned 0 otherwize.
        problem (AssignmentProblem): The assignment problem.
    """
    if problem.score_config.use_matching:
        matching_config: MatchingConfig = problem.score_config.matching_config
        if matching_config.max_vals is not None:
            for left_label in problem.left_labels:
                for ( right_label, left_variable_label ), max_val in matching_config.max_vals.items():
                    left_val = int( matching_config.left_vals[ left_label, left_variable_label ] )
                    model.Add( left_val * is_assigned[ left_label, right_label ] <= int( max_val ) )

        if matching_config.min_vals is not None:
            for left_label in problem.left_labels:
                for ( right_label, left_variable_label ), min_val in matching_config.min_vals.items():
                    left_val = int( matching_config.left_vals[ left_label, left_variable_label ] )
                    model.Add( left_val * is_assigned[ left_label, right_label ] >= int( min_val ) )
