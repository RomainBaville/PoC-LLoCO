# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025-2026 AKKODIS.
# SPDX-FileContributor: Romain Baville

from typing import Any

import streamlit as st
from streamlit.runtime.state.session_state_proxy import SessionStateProxy


def logicals_constraints( session_state: SessionStateProxy ) -> None:
    """Configure the interface to set the logicals constraints of the problem.

    Args:
        session_state (SessionStateProxy): The session state.
    """
    st.subheader( "Logicals constraints" )

    if "max_left_entities" not in session_state:
        session_state.max_left_entities = None

    if "max_right_entities" not in session_state:
        session_state.max_right_entities = None

    session_state.left_mutual_exclusions = mutual_exclusions(
        labels=session_state.left_labels,
        entities_type_constrained=session_state.left_entities_type,
        entities_type_constraining=session_state.right_entities_type,
        lock_constraints=session_state.lock_constraints,
        max_associations=session_state.max_left_entities
    )
    if session_state.left_mutual_exclusions is not None:
        session_state.journey[ "Left mutual exclusions" ] = session_state.left_mutual_exclusions
    elif "Left mutual exclusions" in session_state.journey:
        del ( session_state.journey[ "Left mutual exclusions" ] )
        st.rerun()

    session_state.right_mutual_exclusions = mutual_exclusions(
        labels=session_state.right_labels,
        entities_type_constrained=session_state.right_entities_type,
        entities_type_constraining=session_state.left_entities_type,
        lock_constraints=session_state.lock_constraints,
        max_associations=session_state.max_right_entities
    )
    if session_state.right_mutual_exclusions is not None:
        session_state.journey[ "Right mutual exclusions" ] = session_state.right_mutual_exclusions
    elif "Right mutual exclusions" in session_state.journey:
        del ( session_state.journey[ "Right mutual exclusions" ] )
        st.rerun()

    labels: tuple[ tuple[ str, ...], tuple[ str, ...] ] = ( session_state.left_labels, session_state.right_labels )
    entities_types: tuple[ str, str ] = ( session_state.left_entities_type, session_state.right_entities_type )

    session_state.implications = implications(
        labels, entities_types, session_state.multiple_same_assignment, session_state.lock_constraints
    )
    if session_state.implications is not None:
        session_state.journey[ "Implications" ] = session_state.implications
    elif "Implications" in session_state.journey:
        del ( session_state.journey[ "Implications" ] )
        st.rerun()


def mutual_exclusions(
    labels: tuple[ str, ...],
    entities_type_constrained: str,
    entities_type_constraining: str,
    lock_constraints: bool,
    max_associations: dict[ str, float ] | None
) -> tuple[ tuple[ str, ...], ...] | None:
    """Build the mutual exclusions constraints of the problem if it exist.

    Args:
        labels (tuple[str, ...]): The entitie labels.
        entities_type_constrained (str): The type of the entities constrained.
        entities_type_constraining (str): The type of the entities constraining.
        max_associations (dict[str, float] | None): The maximum number of association per entity.

    Returns:
        tuple[tuple[str, ...], ...] | None: The mutual exclusions constraints of the problem.
    """
    mutual_exclusions_constraints: tuple[ tuple[ str, ...], ...] | None = None
    if (
        max_associations is None or ( isinstance( max_associations, dict ) and max( max_associations.values() ) > 1 )
    ) and len( labels ) > 1:  # Only if an entity can be assigned to several
        define_mutual_exclusions: bool = st.checkbox(
            f"Is there groups of { entities_type_constrained } who can't be " \
            f"assigned to the same { entities_type_constraining }", disabled=lock_constraints
        )
        if define_mutual_exclusions:
            nb_groups: int = st.number_input(
                f"How many group of { entities_type_constrained } ?", min_value=1, disabled=lock_constraints
            )

            constraints: list[ list[ str ] ] = [ [] for _ in range( nb_groups ) ]
            for group in range( nb_groups ):
                nb_entities: int = st.number_input(
                    f"How many { entities_type_constrained } are conserned for the group { group + 1 } ?",
                    min_value=2,
                    max_value=len( labels ),
                    disabled=lock_constraints
                )
                constraints[ group ] = [ labels[ entity ] for entity in range( nb_entities ) ]
                exclusions_cols = st.columns( nb_entities )
                for id, col in enumerate( exclusions_cols ):
                    with col:
                        constraints[ group ][ id ] = st.selectbox(
                            f"{ entities_type_constrained } { id + 1 } for the group { group + 1 }",
                            labels,
                            disabled=lock_constraints
                        )

            mutual_exclusions_constraints = tuple( map( tuple, constraints ) )

        else:
            mutual_exclusions_constraints = None

    return mutual_exclusions_constraints


def implications(
    labels: tuple[ tuple[ str, ...], tuple[ str, ...] ],
    entities_types: tuple[ str, str ],
    multiple_same_assignment: bool,
    lock_constraints: bool
) -> dict[ tuple[ str, str ], tuple[ tuple[ str, str, float ], ...] ] | None:
    """Build the implications constraints of the problem if it exist.

    Args:
        labels (tuple[tuple[str, ...], tuple[str, ...]]): The left and right entities labels.
        entities_types (tuple[str, str]): The left and right entities types.
        use_quantities_constraints (bool): True if the problem use quantities constraints.
        multiple_same_assignment (bool): True if one left entity can be assigned several time to the same right entity.

    Returns:
        dict[tuple[str, str], tuple[tuple[str, str, float], ...]] | None: The implications constraints of the problem.

    """
    implications_constraints: dict[ tuple[ str, str ], tuple[ tuple[ str, str, float ], ...] ] | None = None
    use_implications: bool = st.checkbox( "Is there assignments implie other ?", disabled=lock_constraints )
    if use_implications:
        constraints: dict[ tuple[ str, str ], tuple[ tuple[ str, str, float ], ...] ] = {}
        nb_assignments_with_implications: int = st.number_input(
            "How many assignments implies others ?", min_value=1, disabled=lock_constraints
        )
        for assignment_with_implications in range( nb_assignments_with_implications ):
            st.subheader( f"Rules for the assignment number { assignment_with_implications }" )
            assignment_with_implications_labels: list[ str ] = [ "", "" ]
            nb_assignment_with_implications_cols: int = 2
            if len( labels[ 1 ] ) == 1:
                nb_assignment_with_implications_cols = 1
                assignment_with_implications_labels[ 1 ] = labels[ 1 ][ 0 ]

            assignment_with_implications_cols = st.columns( nb_assignment_with_implications_cols )
            for side, assignment_with_implications_col in enumerate( assignment_with_implications_cols ):
                if len( labels[ side ] ) > 1:
                    with assignment_with_implications_col:
                        assignment_with_implications_labels[ side ] = st.selectbox(
                            f"Select the { entities_types[ side ] } of the assignment "\
                            f"number { assignment_with_implications } implying other.",
                            labels[ side ], disabled=lock_constraints
                        )
                else:
                    assignment_with_implications_labels[ side ] = labels[ side ][ 0 ]

            nb_implies_assignments: int = st.number_input(
                f"How many assignments implies the assignment { assignment_with_implications } " \
                f"{ assignment_with_implications_labels }",
                min_value=1, disabled=lock_constraints
            )
            implies_assignments: list[ list[ Any ] ] = []
            for implies_assignment in range( nb_implies_assignments ):
                implies_assignment_parameters: list[ Any ] = [ "", "", 1. ]
                nb_implies_assignment_cols: int = 2

                if multiple_same_assignment:
                    nb_implies_assignment_cols += 1

                set_right_label: bool = True
                if len( labels[ 1 ] ) == 1:
                    nb_implies_assignment_cols -= 1
                    implies_assignment_parameters[ 1 ] = labels[ 1 ][ 0 ]
                    set_right_label = False

                implies_assignment_cols = st.columns( nb_implies_assignment_cols )
                for param, implies_assignment_col in enumerate( implies_assignment_cols ):
                    with implies_assignment_col:
                        if param == 0 or (
                            param == 1 and set_right_label
                        ):  # Left and right labels of the implies assignment
                            if len( labels[ param ] ) > 1:
                                implies_assignment_parameters[ param ] = st.selectbox(
                                    f"Select the { entities_types[ param ] } of the assignment " \
                                    f"{ assignment_with_implications } { assignment_with_implications_labels } " \
                                    f"implie's assignment number { implies_assignment }",
                                    labels[ param ], disabled=lock_constraints
                                )
                            else:
                                implies_assignment_parameters[ param ] = labels[ param ][ 0 ]
                        elif param >= 1:  # The number of assignments implied
                            implies_assignment_parameters[ param ] = st.number_input(
                                f"Set the number of { implies_assignment_parameters[ :2 ] } assignment " \
                                f"implied by the { assignment_with_implications_labels } assignment.",
                                min_value=1., disabled=lock_constraints
                            )

                implies_assignments.append( implies_assignment_parameters )

            constraints[ ( assignment_with_implications_labels[ 0 ], assignment_with_implications_labels[ 1 ] )
                        ] = tuple( map( tuple, implies_assignments ) )

        implications_constraints = constraints

    return implications_constraints
