# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025-2026 AKKODIS.
# SPDX-FileContributor: Romain Baville

from collections.abc import MutableMapping
from typing import Any

import streamlit as st

SessionState = MutableMapping[ str, Any ]


def logicals_constraints( session_state: SessionState ) -> None:
    """Configure the interface to set the logicals constraints of the problem.

    Args:
        session_state (SessionState): The session state.
    """
    st.subheader( "Logicals constraints" )

    if "max_left_entities" not in session_state:
        session_state.max_left_entities = None

    if "max_right_entities" not in session_state:
        session_state.max_right_entities = None

    labels: tuple[ tuple[ str, ...], tuple[ str, ...] ] = ( session_state.left_labels, session_state.right_labels )
    entities_types: tuple[ str, str ] = ( session_state.left_entities_type, session_state.right_entities_type )
    max_associations: tuple[ dict[ str, float ] | None, dict[ str, float ] | None ] = (
        session_state.max_left_entities, session_state.max_right_entities
    )
    mutual_exclusion: list[ list[ tuple[ str, ...] ] | None ] = [ None, None ]

    for side in range( 2 ):  # Left then right
        if ( max_associations[ side ] is None or max( max_associations[ side ].values() )
             > 1 ) and len( labels[ side ] ) > 1:  # Only if an entity can be assigned to several
            define_mutual_exclusion: bool = st.checkbox(
                f"Is there groups of { entities_types[ side ] } who can't be assigned " \
                f"to the same { entities_types[ 1 - side ] }"
            )
            if define_mutual_exclusion:
                nb_groups: int = st.number_input( f"How many group of { entities_types[ side ] } ?", min_value=1 )

                mutual_exclusion[ side ] = [ [] for _ in range( nb_groups ) ]
                for group in range( nb_groups ):
                    nb_entities: int = st.number_input(
                        f"How many { entities_types[ side ] } are conserned for the group { group + 1 } ?",
                        min_value=2,
                    )
                    mutual_exclusion[ side ][ group ] = [ None for _ in range( nb_entities ) ]
                    exclusion_cols = st.columns( nb_entities )
                    for id, col in enumerate( exclusion_cols ):
                        with col:
                            mutual_exclusion[ side ][ group ][ id ] = st.selectbox(
                                f"{ entities_types[ side ] } { id + 1 } for the group { group + 1 }",
                                labels[ side ],
                            )
                    mutual_exclusion[ side ][ group ] = tuple( mutual_exclusion[ side ][ group ] )
            else:
                mutual_exclusion[ side ] = None
        else:
            mutual_exclusion[ side ] = None

    session_state.left_mutual_exclusions = tuple( mutual_exclusion[ 0 ] ) if mutual_exclusion[ 0 ] is not None \
        else None
    session_state.right_mutual_exclusions = tuple( mutual_exclusion[ 1 ] ) if mutual_exclusion[ 1 ] is not None \
        else None

    session_state.implications = None
    use_implications: bool = st.checkbox( "Is there assignments implie other ?" )
    if use_implications:
        session_state.implications = {}
        nb_assignments_with_implications: int = st.number_input(
            "How many assignments implies others ?",
            min_value=1,
        )
        for assignment_with_implications in range( nb_assignments_with_implications ):
            st.subheader( f"Rules for the assignment number { assignment_with_implications }" )
            assignment_with_implications_labels = [ None, None ]
            nb_assignment_with_implications_cols: int = 2
            if len( session_state.right_labels ) == 1:
                nb_assignment_with_implications_cols = 1
                assignment_with_implications_labels[ 1 ] = session_state.right_labels[ 0 ]

            assignment_with_implications_cols = st.columns( nb_assignment_with_implications_cols )
            for side, assignment_with_implications_col in enumerate( assignment_with_implications_cols ):
                if len( labels[ side ] ) > 1:
                    with assignment_with_implications_col:
                        assignment_with_implications_labels[ side ] = st.selectbox(
                            f"Selecte the { entities_types[ side ] } of the assignment "\
                            f"number { assignment_with_implications } implies other.",
                            labels[ side ],
                        )
                else:
                    assignment_with_implications_labels[ side ] = labels[ side ][ 0 ]

            nb_implies_assignments: int = st.number_input(
                f"How many assignments implies the assignment { assignment_with_implications } " \
                f"{ assignment_with_implications_labels }",
                min_value=1,
            )
            list_implies_assignments = []
            for implies_assignment in range( nb_implies_assignments ):
                implies_assignment_parameters = [ None, None, 1. ]
                nb_implies_assignment_cols: int = 2

                if session_state.use_quantities_constraints and session_state.multiple_same_assignment:
                    nb_implies_assignment_cols += 1

                set_right_label: bool = True
                if len( session_state.right_labels ) == 1:
                    nb_implies_assignment_cols -= 1
                    implies_assignment_parameters[ 1 ] = session_state.right_labels[ 0 ]
                    set_right_label = False

                implies_assignment_cols = st.columns( nb_implies_assignment_cols )
                for param, implies_assignment_col in enumerate( implies_assignment_cols ):
                    with implies_assignment_col:
                        if param == 0 or (
                            param == 1 and set_right_label
                        ):  # Left and right labels of the implies assignment
                            if len( labels[ param ] ) > 1:
                                implies_assignment_parameters[ param ] = st.selectbox(
                                    f"Selecte the { entities_types[ param ] } of the assignment " \
                                    f"{ assignment_with_implications } { assignment_with_implications_labels } " \
                                    f"implie's assignment number { implies_assignment }",
                                    labels[ param ],
                                )
                            else:
                                implies_assignment_parameters[ param ] = labels[ param ][ 0 ]
                        elif param >= 1:  # The number of assignments implies
                            implies_assignment_parameters[ param ] = st.number_input(
                                f"Set the number of { implies_assignment_parameters[ :2 ] } assignment " \
                                f"implis by the { assignment_with_implications_labels } assignment.",
                                min_value=1.,
                            )

                list_implies_assignments.append( tuple( implies_assignment_parameters ) )

            session_state.implications[ tuple( assignment_with_implications_labels ) ] = tuple(
                list_implies_assignments
            )
    else:
        session_state.implications = None
