# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025-2026 AKKODIS.
# SPDX-FileContributor: Romain Baville

import streamlit as st
from streamlit.runtime.state.session_state_proxy import SessionStateProxy

from ui.assignment.constraints.builder import build_quantities_constraints


def quantities_constraints( session_state: SessionStateProxy ) -> None:
    """Configure the interface to set the quantities constraints of the problem.

    Args:
        session_state (SessionStateProxy): The session state.
    """
    st.subheader( "Quantities constraints" )
    # -----------------------------
    # Extrema side entities
    # -----------------------------
    session_state.max_right_entities = extremum_assignments(
        extremum="maximum",
        labels=session_state.left_labels,
        entities_type=session_state.left_entities_type,
        entities_rows=session_state.left_rows,
        entities_cols=session_state.left_cols,
        entities_col_label=session_state.left_entities_col_label,
        message="all the several assignments to the same entity count for one.",
        lock_constraints=session_state.lock_constraints
    )
    if session_state.max_right_entities is not None:
        session_state.journey[ "Max right entities" ] = session_state.max_right_entities
    elif "Max right entities" in session_state.journey:
        del ( session_state.journey[ "Max right entities" ] )
        st.rerun()

    session_state.min_right_entities = extremum_assignments(
        extremum="minimum",
        labels=session_state.left_labels,
        entities_type=session_state.left_entities_type,
        entities_rows=session_state.left_rows,
        entities_cols=session_state.left_cols,
        entities_col_label=session_state.left_entities_col_label,
        message="all the several assignments to the same entity count for one.",
        lock_constraints=session_state.lock_constraints
    )
    if session_state.min_right_entities is not None:
        session_state.journey[ "Min right entities" ] = session_state.min_right_entities
    elif "Min right entities" in session_state.journey:
        del ( session_state.journey[ "Min right entities" ] )
        st.rerun()

    session_state.max_left_entities = extremum_assignments(
        extremum="maximum",
        labels=session_state.right_labels,
        entities_type=session_state.right_entities_type,
        entities_rows=session_state.right_rows,
        entities_cols=session_state.right_cols,
        entities_col_label=session_state.right_entities_col_label,
        message="all the several assignments to the same entity count for one.",
        lock_constraints=session_state.lock_constraints
    )
    if session_state.max_left_entities is not None:
        session_state.journey[ "Max left entities" ] = session_state.max_left_entities
    elif "Max left entities" in session_state.journey:
        del ( session_state.journey[ "Max left entities" ] )
        st.rerun()

    session_state.min_left_entities = extremum_assignments(
        extremum="minimum",
        labels=session_state.right_labels,
        entities_type=session_state.right_entities_type,
        entities_rows=session_state.right_rows,
        entities_cols=session_state.right_cols,
        entities_col_label=session_state.right_entities_col_label,
        message="all the several assignments to the same entity count for one.",
        lock_constraints=session_state.lock_constraints
    )
    if session_state.min_left_entities is not None:
        session_state.journey[ "Min left entities" ] = session_state.min_left_entities
    elif "Min left entities" in session_state.journey:
        del ( session_state.journey[ "Min left entities" ] )
        st.rerun()

    # -----------------------------
    # Mutiple same assignment
    # -----------------------------
    if session_state.multiple_same_assignment:
        # -----------------------------
        # Extrema same assignments
        # -----------------------------
        entities_types: tuple[ str, str ] = ( session_state.left_entities_type, session_state.right_entities_type )
        entities_cols: tuple[ tuple[ str, ...], tuple[ str,
                                                       ...] ] = ( session_state.left_cols, session_state.right_cols )

        session_state.max_same_assignments = extremum_same_assignments(
            extremum="maximum",
            entities_types=entities_types,
            entities_cols=entities_cols,
            lock_constraints=session_state.lock_constraints
        )
        session_state.min_same_assignments = extremum_same_assignments(
            extremum="minimum",
            entities_types=entities_types,
            entities_cols=entities_cols,
            lock_constraints=session_state.lock_constraints
        )

        # -----------------------------
        # Extrema side assignments
        # -----------------------------
        session_state.max_right_assignments = extremum_assignments(
            extremum="maximum",
            labels=session_state.left_labels,
            entities_type=session_state.left_entities_type,
            entities_rows=session_state.left_rows,
            entities_cols=session_state.left_cols,
            entities_col_label=session_state.left_entities_col_label,
            message="all the several assignments to the same entity count.",
            lock_constraints=session_state.lock_constraints
        )
        session_state.min_right_assignments = extremum_assignments(
            extremum="minimum",
            labels=session_state.left_labels,
            entities_type=session_state.left_entities_type,
            entities_rows=session_state.left_rows,
            entities_cols=session_state.left_cols,
            entities_col_label=session_state.left_entities_col_label,
            message="all the several assignments to the same entity count.",
            lock_constraints=session_state.lock_constraints
        )
        session_state.max_left_assignments = extremum_assignments(
            extremum="maximum",
            labels=session_state.right_labels,
            entities_type=session_state.right_entities_type,
            entities_rows=session_state.right_rows,
            entities_cols=session_state.right_cols,
            entities_col_label=session_state.right_entities_col_label,
            message="all the several assignments to the same entity count.",
            lock_constraints=session_state.lock_constraints
        )
        session_state.min_left_assignments = extremum_assignments(
            extremum="minimum",
            labels=session_state.right_labels,
            entities_type=session_state.right_entities_type,
            entities_rows=session_state.right_rows,
            entities_cols=session_state.right_cols,
            entities_col_label=session_state.right_entities_col_label,
            message="all the several assignments to the same entity count.",
            lock_constraints=session_state.lock_constraints
        )
    else:
        session_state.max_same_assignments = None
        session_state.min_same_assignments = None
        session_state.max_right_assignments = None
        session_state.min_right_assignments = None
        session_state.max_left_assignments = None
        session_state.min_left_assignments = None

    if session_state.max_same_assignments is not None:
        session_state.journey[ "Max same assignments" ] = session_state.max_same_assignments
    elif "Max same assignments" in session_state.journey:
        del ( session_state.journey[ "Max same assignments" ] )
        st.rerun()
    if session_state.min_same_assignments is not None:
        session_state.journey[ "Min same assignments" ] = session_state.min_same_assignments
    elif "Min same assignments" in session_state.journey:
        del ( session_state.journey[ "Min same assignments" ] )
        st.rerun()
    if session_state.max_right_assignments is not None:
        session_state.journey[ "Max right assignments" ] = session_state.max_right_assignments
    elif "Max right assignments" in session_state.journey:
        del ( session_state.journey[ "Max right assignments" ] )
        st.rerun()
    if session_state.min_right_assignments is not None:
        session_state.journey[ "Min right assignments" ] = session_state.min_right_assignments
    elif "Min right assignments" in session_state.journey:
        del ( session_state.journey[ "Min right assignments" ] )
        st.rerun()
    if session_state.max_left_assignments is not None:
        session_state.journey[ "Max left assignments" ] = session_state.max_left_assignments
    elif "Max left assignments" in session_state.journey:
        del ( session_state.journey[ "Max left assignments" ] )
        st.rerun()
    if session_state.min_left_assignments is not None:
        session_state.journey[ "Min left assignments" ] = session_state.min_left_assignments
    elif "Min left assignments" in session_state.journey:
        del ( session_state.journey[ "Min left assignments" ] )
        st.rerun()


def extremum_same_assignments(
    extremum: str,
    entities_types: tuple[ str, str ],
    entities_cols: tuple[ tuple[ str, ...], tuple[ str, ...] ],
    lock_constraints: bool
) -> dict[ tuple[ str, str ], float ] | None:
    """Build the extremum same assignment constraints of the problem.

    Args:
        extremum (str): The extremum.
        entities_types (tuple[str, str]): The left and right entities types.
        entities_cols (tuple[tuple[str, ...], tuple[str, ...]]): The left and right entities columns.

    Returns:
        dict[tuple[str, str], float] | None: The extremum same assignment constraints.
    """
    extremum_same_assignments_constraints: dict[ tuple[ str, str ], float ] | None = None
    use_extremum_same_assignments: bool = st.checkbox(
        f"Is there { entities_types[ 0 ] } with a { extremum } number of " \
        f"assignment to the same { entities_types[ 1 ] } ?", disabled=lock_constraints
    )
    if use_extremum_same_assignments:
        constraints: dict[ tuple[ str, str ], float ] = {}
        left_labels_constrainted: list[ str ] = st.multiselect(
            f"Select all the { entities_types[ 0 ] } with a constraint",
            entities_cols[ 0 ],
            disabled=lock_constraints
        )
        for left_label_constrainted in left_labels_constrainted:
            right_labels_constrainted: list[ str ] = st.multiselect(
                f"Select all the { entities_types[ 1 ] } with a { extremum } " \
                f"constraint due to the { left_label_constrainted }",
                entities_cols[ 1 ], disabled=lock_constraints
            )
            for right_label_constrainted in right_labels_constrainted:
                constraints[ ( left_label_constrainted, right_label_constrainted ) ] = st.number_input(
                    f"Set the { extremum } numuber of assignement allowed between " \
                    f"{ left_label_constrainted } and { right_label_constrainted }",
                    min_value=1., disabled=lock_constraints
                )
        if constraints != {}:
            extremum_same_assignments_constraints = constraints

    return extremum_same_assignments_constraints


def extremum_assignments(
    extremum: str,
    labels: tuple[ str, ...],
    entities_type: str,
    entities_rows: tuple[ dict[ str, str ], ...],
    entities_cols: tuple[ str, ...],
    entities_col_label: str,
    message: str,
    lock_constraints: bool
) -> dict[ str, float ] | None:
    """Build the extremum entities constraints of the problem if it exits.

    This function can build the eights quantities constraints about the number of assignments per entity.
    The variable message allows to explain the diffences between the four constraint taking into acount two
    assignments to a same entity and the four other. Here is an example of the two messages:

        - extremum_side_assignments: all the several assignments to the same entity count.
        - extremum_side_entities: all the several assignments to the same entity count for one.

    Args:
        extremum (str): The extremum.
        labels (tuple[str, ...]): The entities labels.
        entities_type (str): The entities type.
        entities_rows (tuple[dict[str, str], ...]): The entities rows.
        entities_cols (tuple[str, ...]): The entities columns.
        entities_col_label (str): The entities column label.
        message (str): The message to make the difference between the two family of constraints

    Retunrs:
        dict[str, float] | None: The extremum entities constraints of the problem.
    """
    extremum_assignments_constraints: dict[ str, float ] | None = None
    use_extremum_assignments: bool = st.checkbox(
        f"Is there a { extremum } number of assignments allowed per { entities_type } ? Note that { message }",
        disabled=lock_constraints
    )
    if use_extremum_assignments:
        constraints: dict[ str, float ] = {}
        assignments_mode: str = st.radio(
            f"How to define the { extremum } number of assignments allowed per { entities_type } ?" \
            f"Note that { message }",
            [
                "With data column",
                f"Set it manually for each { entities_type }",
                f"Set it manually for all { entities_type }",
            ], disabled=lock_constraints
        )

        if assignments_mode == "With data column":
            extremum_assignments_col_label: str = st.selectbox(
                f"Select the column identifying the { extremum } number of assignments allowed per { entities_type }" \
                f" Note that { message }",
                entities_cols, disabled=lock_constraints
            )
            constraints = build_quantities_constraints(
                entities_col_label, entities_rows, quantities_constraints_col_label=extremum_assignments_col_label
            )

        elif assignments_mode == f"Set it manually for each { entities_type }":
            for label in labels:
                constraints[ label ] = st.number_input(
                    f"Set the { extremum } number of assignments allowed for the { label }" \
                    f" Note that { message }",
                    min_value=1., disabled=lock_constraints
                )

        elif assignments_mode == f"Set it manually for all { entities_type }":
            extremum_assignments_val: float = st.number_input(
                f"Set the { extremum } number of assignments allowed per { entities_type }" \
                f" Note that { message }",
                min_value=1., disabled=lock_constraints
            )
            constraints = build_quantities_constraints(
                entities_col_label, entities_rows, quantities_constraints_val=extremum_assignments_val
            )

        if constraints != {}:
            extremum_assignments_constraints = constraints

    return extremum_assignments_constraints
