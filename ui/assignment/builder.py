# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025-2026 AKKODIS.
# SPDX-FileContributor: Romain Baville

from streamlit.runtime.state.session_state_proxy import SessionStateProxy

from domain.assignment.base import AssignmentProblem
from ui.assignment.constraints.builder import build_constraints_config
from ui.assignment.score.builder import build_score_config


def build_entities_labels(
    entity_col_label: str,
    entity_rows: tuple[ dict[ str, str ], ...]
) -> tuple[ str, ...]:
    """Build the entities labels from csv col label and rows.

    Args:
        entity_col_label (str): The label of the column with the label.
        entity_rows (tuple[dict[str, str]]): The rows of the csv files.

    Returns:
        tuple[str, ...]: All the entities labels from a side of the assignment problem.
    """
    entities_labels: list[ str ] = []
    for entity_row in entity_rows:
        entities_labels.append( entity_row[ entity_col_label ] )

    return tuple( entities_labels )


def build_vals(
    entity_col_label: str,
    variables_labels: tuple[ str, ...] | dict[ str, str ],
    entity_rows: tuple[ dict[ str, str ], ...]
) -> dict[ tuple[ str, str ], float ]:
    """Build the dictionary with the value of an entity variable.

    Args:
        entity_col_label (str): The label of the column with the label.
        variables_labels (tuple[str, ...] | dict[str, str]): The entity variable labels
        entity_rows (tuple[dict[str, str]]): The rows of the csv files.

    Returns:
        dict[tuple[str, str], float]: The dictionary with the value (values) of an entity variable (keys).
    """
    vals: dict[ tuple[ str, str ], float ] = {}
    for entity_row in entity_rows:
        for variable_label in variables_labels:
            val: float
            if isinstance( variables_labels, dict ):
                val = float( entity_row[ variables_labels[ variable_label ] ] )
            else:
                val = float( entity_row[ variable_label ] )

            entity_label: str = entity_row[ entity_col_label ]
            vals[ ( entity_label, variable_label ) ] = val

    return vals


def build_problem( session_state: SessionStateProxy ) -> AssignmentProblem:
    """Build the assignment problem.

    Args:
        session_state (SessionStateProxy): The session state.

    Returns:
        AssignmentProblem: The assignment problem.
    """
    problem: AssignmentProblem = AssignmentProblem(
        left_labels=session_state.left_labels,
        right_labels=session_state.right_labels,
        score_config=build_score_config( session_state ),
        constraints_config=build_constraints_config( session_state )
    )

    return problem
