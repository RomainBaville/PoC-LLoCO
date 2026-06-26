# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025-2026 AKKODIS.
# SPDX-FileContributor: Romain Baville

from domain.assignment.base import AssignmentProblem

from ui.assignment.score.builder import build_score_config
from ui.assignment.constraints.builder import build_constraints_config

def build_entities_labels(
    entity_col_label: str,
    entity_rows: tuple[ dict[ str, str ], ...],
) -> tuple[ str, ...]:
    entities_labels: list[ str ] = []
    for entity_row in entity_rows:
        entities_labels.append( entity_row[ entity_col_label ] )

    return tuple( entities_labels )


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


def build_problem( state ) -> AssignmentProblem:
    """Build a generic assignment problem.

    Args:
        state (): ...

    Returns
        AssignmentProblem: The assignment problem.
    """

    problem: AssignmentProblem = AssignmentProblem(
        left_labels = state.left_labels,
        right_labels = state.right_labels,
        score_config = build_score_config( state ),
        constraints_config = build_constraints_config( state ),
    )

    return problem
