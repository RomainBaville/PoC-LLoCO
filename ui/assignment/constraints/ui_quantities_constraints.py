# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025-2026 AKKODIS.
# SPDX-FileContributor: Romain Baville

import streamlit as st
from typing import Optional

from ui.assignment.constraints.builder import build_quantities_constraints

def quantities_constraints( state ) -> None:
    st.subheader( "Quantities constraints" )

    labels: tuple[ tuple[ str, ...], tuple[ str, ...] ] = ( state.left_labels, state.right_labels )
    entities_types: tuple[ str, str ] = ( state.left_entities_type, state.right_entities_type )
    entities_cols: tuple[ tuple[ str, ...], tuple[ str, ...] ] = ( state.left_cols, state.right_cols )
    entities_rows: tuple[ dict[ str, str ], dict[ str, str ] ] = ( state.left_rows, state.right_rows )
    entities_col_label: tuple[ str, str ] = ( state.left_entities_col_label, state.right_entities_col_label )
    extrema: tuple[ str, str ] = ( "maximum", "minimum" )

    # -----------------------------
    # Extrema side entities
    # -----------------------------
    extrema_side_entities: list[ list[ Optional[ dict[ str, float ] ] ] ] = [ [ None, None ], [ None, None ] ]
    for side in range( 2 ): # left then right
        extrema_side_entities_cols = st.columns( 2 )
        for id, extrema_side_entities_col in enumerate( extrema_side_entities_cols ): # max and min columns
            with extrema_side_entities_col:
                use_extrema_side_entities: bool = st.checkbox( f"Is there a { extrema[ id ] } number of { entities_types[ 1 - side ] } that can be assigned to one { entities_types[ side ] } ?" )

                if use_extrema_side_entities:
                    entities_mode: str = st.radio(
                        f"How to define the { extrema[ id ] } number of { entities_types[ 1 - side ] } that can be assigned to one { entities_types[ side ] } ?",
                        [
                            "With data column",
                            f"Set it manually for each { entities_types[ side ] }",
                            f"Set it manually for all { entities_types[ side ] }",
                        ],
                    )

                    if entities_mode == "With data column":
                        extrema_side_entities_col_label: str = st.selectbox(
                            f"Select the column identifying the { extrema[ id ] } number of { entities_types[ 1 - side ] } that can be assigned to one { entities_types[ side ] }",
                            entities_cols[ side ],
                        )
                        extrema_side_entities[ side ][ id ] = build_quantities_constraints(
                            entities_col_label[ side ],
                            entities_rows[ side ],
                            quantities_constraints_col_label = extrema_side_entities_col_label,
                        )

                    elif entities_mode == f"Set it manually for each { entities_types[ side ] }":
                        for label in labels[ side ]:
                            extrema_side_entities[ side ][ id ][ label ] = st.number_input(
                                f"Set the { extrema[ id ] } number of { entities_types[ 1 - side ] } that can be assigned to { label }",
                                min_value = 1.,
                            )

                    elif entities_mode == f"Set it manually for all { entities_types[ side ] }":
                        extrema_side_entities_val: float = st.number_input(
                            f"Set the { extrema[ id ] } number of { entities_types[ 1 - side ] } that can be assigned to one { entities_types[ side ] }",
                            min_value = 1.,
                        )
                        extrema_side_entities[ side ][ id ] = build_quantities_constraints( entities_col_label[ side ], entities_rows[ side ], quantities_constraints_val=extrema_side_entities_val )
                else:
                    extrema_side_entities[ side ][ id ] = None

    state.max_right_entities = extrema_side_entities[ 0 ][ 0 ]
    state.min_right_entities = extrema_side_entities[ 0 ][ 1 ]
    state.max_left_entities = extrema_side_entities[ 1 ][ 0 ]
    state.min_left_entities = extrema_side_entities[ 1 ][ 1 ]

    # -----------------------------
    # Mutiple same assignment
    # -----------------------------
    state.multiple_same_assignment = st.checkbox( f"{ state.left_entities_type } can be assigned multiple time to the same { state.right_entities_type } ?" )

    extrema_same_assignments: list[ Optional[ dict[ tuple[ str, str ], float ] ] ] = [ None, None ]
    extrema_side_assignments: list[ list[ Optional[ dict[ str, float ] ] ] ] = [ [ None, None ], [ None, None ] ]

    if state.multiple_same_assignment:
        # -----------------------------
        # Extrema same assignments
        # -----------------------------
        for id in range( 2 ): # max then min
            use_extrema_same_assignments: bool = st.checkbox( f"Is there { state.left_entities_type } with a { extrema[ id ] } number of assignment to the same { state.right_entities_type } ?" )
            if use_extrema_same_assignments:
                extrema_same_assignments[ id ] = {}
                left_labels_constrainted: tuple[ str, ... ] = tuple( st.multiselect( f"Select all the { state.left_entities_type } with a constraint", state.left_cols ) )
                for left_label_constrainted in left_labels_constrainted:
                    right_labels_constrainted: tuple[ str, ...] = tuple(
                        st.multiselect(
                            f"Select all the { state.right_entities_type } with a { extrema[ id ] }constraint du to the { left_label_constrainted }",
                            state.right_cols,
                        )
                    )
                    for right_label_constrainted in right_labels_constrainted:
                        extrema_same_assignments[ id ][ left_label_constrainted, right_label_constrainted] = st.number_input(
                            f"Set the { extrema[ id ] } numuber of assignement allowed between { left_label_constrainted } and { right_label_constrainted }",
                            min_value = 1.,
                        )
                if extrema_same_assignments[ id ] == {}:
                    extrema_same_assignments[ id ] = None
            else:
                extrema_same_assignments[ id ] = None

        # -----------------------------
        # Extrema side assignments
        # -----------------------------
        for side in range( 2 ): # left then right
            extrema_side_assignments_cols = st.columns( 2 )
            for id, extrema_side_assignments_col in enumerate( extrema_side_assignments_cols ): # max and min columns
                with extrema_side_assignments_col:
                    use_extrema_side_assignments: bool = st.checkbox( f"Is there a { extrema[ id ] } number of assignments allowed per { entities_types[ side ] } ?" )

                    if use_extrema_side_assignments:
                        assignments_mode: str = st.radio(
                            f"How to define the { extrema[ id ] } number of assignments allowed per { entities_types[ side ] } ?",
                            [
                                "With data column",
                                f"Set it manually for each { entities_types[ side ] }",
                                f"Set it manually for all { entities_types[ side ] }",
                            ],
                        )

                        if assignments_mode == "With data column":
                            extrema_side_assignments_col_label: str = st.selectbox(
                                f"Select the column identifying the { extrema[ id ] } number of assignments allowed per { entities_types[ side ] }",
                                entities_cols[ side ],
                            )
                            extrema_side_assignments[ side ][ id ] = build_quantities_constraints( entities_col_label[ side ], entities_rows[ side ], quantities_constraints_col_label=extrema_side_assignments_col_label )

                        elif assignments_mode == f"Set it manually for each { entities_types[ side ] }":
                            for label in labels[ side ]:
                                extrema_side_assignments[ side ][ id ][ label ] = st.number_input(
                                    f"Set the { extrema[ id ] } number of assignments allowed for the { label }",
                                    min_value = 1.,
                                )

                        elif assignments_mode == f"Set it manually for all { entities_types[ side ] }":
                            extrema_side_assignments_val: float = st.number_input(
                                f"Set the { extrema[ id ] } number of assignments allowed per { entities_types[ side ] }",
                                min_value = 1.,
                            )
                            extrema_side_assignments[ side ][ id ] = build_quantities_constraints( entities_col_label[ side ], entities_rows[ side ], quantities_constraints_val=extrema_side_assignments_val )
                    else:
                        extrema_side_assignments[ side ][ id ] = None
    else:
        extrema_same_assignments = [ None, None ]
        extrema_side_assignments = [ [ None, None ], [ None, None ] ]

    state.max_same_assignments = extrema_same_assignments[ 0 ]
    state.min_same_assignments = extrema_same_assignments[ 1 ]

    state.max_right_assignments = extrema_side_assignments[ 0 ][ 0 ]
    state.min_right_assignments = extrema_side_assignments[ 0 ][ 1 ]
    state.max_left_assignments = extrema_side_assignments[ 1 ][ 0 ]
    state.min_left_assignments = extrema_side_assignments[ 1 ][ 1 ]
