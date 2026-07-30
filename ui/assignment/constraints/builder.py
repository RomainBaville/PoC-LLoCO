# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025-2026 AKKODIS.
# SPDX-FileContributor: Romain Baville

from streamlit.runtime.state.session_state_proxy import SessionStateProxy

from domain.assignment.constraints.constraints_config import ConstraintsConfig
from domain.assignment.constraints.logicals_constraints import LogicalsConstraints
from domain.assignment.constraints.quantities_constraints import QuantitiesConstraints


def build_quantities_constraints(
    entity_col_label: str,
    entity_rows: tuple[ dict[ str, str ], ...],
    quantities_constraints_col_label: str | None = None,
    quantities_constraints_val: float | None = None
) -> dict[ str, float ]:
    """Builder of the constraints of the quantities constraints of an assignment problem.

    This function can use a column of a csv file or a single float.

    Args:
        entity_col_label (str): The label of the column with the entitie labels.
        entity_rows (tuple[dict[str, str], ...]): The csv rows of the entity with the values.
        quantities_constraints_col_label (Optional[str]): The label of the column with the constraints
            values for each entity.
        quantities_constraints_val (Optional[float]): The value of the constraints for all entities.

    retunrs:
        dict[str, float]: The dictionary with the constraints number of assignments (values) for the entities (keys).
    """
    quantities_constraints: dict[ str, float ] = {}
    for entity_row in entity_rows:
        if quantities_constraints_col_label is None and quantities_constraints_val is not None:
            quantities_constraints[ entity_row[ entity_col_label ] ] = quantities_constraints_val
        elif quantities_constraints_val is None and quantities_constraints_col_label is not None:
            quantities_constraints[ entity_row[ entity_col_label ]
                                   ] = float( entity_row[ quantities_constraints_col_label ] )

    return quantities_constraints


def build_constraints_config( session_state: SessionStateProxy ) -> ConstraintsConfig:
    """Build the constraints config of the assignment problem.

    Args:
        session_state (SessionStateProxy): the session state.

    Returns:
        ConstraintsConfig: The configuration of the constraints of the assignment problem.
    """
    logicals_constraints: LogicalsConstraints | None = None
    if session_state.use_logicals_constraints:
        logicals_constraints = LogicalsConstraints(
            left_mutual_exclusions=session_state.left_mutual_exclusions,
            right_mutual_exclusions=session_state.right_mutual_exclusions,
            implications=session_state.implications
        )

    quantities_constraints: QuantitiesConstraints | None = None
    if session_state.use_quantities_constraints:
        quantities_constraints = QuantitiesConstraints(
            max_right_entities=session_state.max_right_entities,
            min_right_entities=session_state.min_right_entities,
            max_left_entities=session_state.max_left_entities,
            min_left_entities=session_state.min_left_entities,
            max_same_assignments=session_state.max_same_assignments,
            min_same_assignments=session_state.min_same_assignments,
            max_right_assignments=session_state.max_right_assignments,
            min_right_assignments=session_state.min_right_assignments,
            max_left_assignments=session_state.max_left_assignments,
            min_left_assignments=session_state.min_left_assignments
        )

    constraints_config: ConstraintsConfig = ConstraintsConfig(
        multiple_same_assignment=session_state.multiple_same_assignment,
        use_logicals_constraints=session_state.use_logicals_constraints,
        logicals_constraints=logicals_constraints,
        use_quantities_constraints=session_state.use_quantities_constraints,
        quantities_constraints=quantities_constraints
    )

    return constraints_config
