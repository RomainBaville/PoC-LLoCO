# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025-2026 AKKODIS.
# SPDX-FileContributor: Romain Baville

import streamlit as st

from domain.objective import Objective
from ui.assignment.builder import build_vals


def map_ressources( state ):
    state.ressources_labels = tuple( st.multiselect(
        "Select columns identifying your ressources",
        state.left_cols,
    ) )
    state.ressources_vals = build_vals( state.left_entities_col_label, state.ressources_labels, state.left_rows )


def ressources_strategy( state ):
    state.ressoucres_objectives = {}
    for ressource_label in state.ressources_labels:
        state.ressoucres_objectives[ ressource_label ] = st.selectbox(
            f"Select the objective for { ressource_label }", Objective
        )

    state.ressources_weights = dict.fromkeys( state.ressources_labels, 1.0 )
    use_ressources_weights: bool = st.checkbox( "Is there ressources with weights" )
    if use_ressources_weights:
        ressources_labels: tuple[ str, ...] = tuple(
            st.multiselect( "Select the ressources with a weight", state.ressources_labels )
        )
        if len( ressources_labels ) > 0:
            for ressource_label in ressources_labels:
                state.ressources_weights[ ressource_label ] = st.number_input(
                    f"Weight for { ressource_label }", value=1.
                )


def ressources_constraints( state ):
    extrema: tuple[ str, str ] = ( "maximum", "minimum" )
    constraints_extrema_cols = st.columns( 2 )
    constraints_extrema_vals: list[ dict[ tuple[ str, ...], float ] | None ] = [ None, None ]
    for id, constraints_extrema_col in enumerate( constraints_extrema_cols ):
        with constraints_extrema_col:
            use_constraints_extrema_vals: bool = st.checkbox(
                f"Is there ressources constrained by a { extrema[ id ] } value ?"
            )
            if use_constraints_extrema_vals:
                constraints_labels: tuple[ str, ...] = tuple(
                    st.multiselect( f"Select all variables used as { extrema[ id ] } constraint", state.right_cols )
                )
                if len( constraints_labels ) > 0:
                    constraints_ressources_labels: dict[ str, list[ str ] ] = {}
                    for constraint_label in constraints_labels:
                        constraints_ressources_labels[ constraint_label ] = st.multiselect(
                            f"Select ressources constrainning by { constraint_label }", state.ressources_labels
                        )

                    vals: dict[ tuple[ str, ...], float ] = {}
                    for right_row in state.right_rows:
                        right_label: str = right_row[ state.right_entities_col_label ]
                        for constraint_label, ressources_labels in constraints_ressources_labels.items():
                            key = [ right_label ]
                            key.extend( ressources_labels )
                            if len( key ) > 1:
                                vals[ tuple( key ) ] = float( right_row[ constraint_label ] )
                            elif tuple( key ) in vals:
                                del vals[ tuple[ key ] ]

                    if vals != {}:
                        constraints_extrema_vals[ id ] = vals
                    else:
                        constraints_extrema_vals[ id ] = None
                else:
                    constraints_extrema_vals[ id ] = None
            else:
                constraints_extrema_vals[ id ] = None

    state.constraints_max_vals = constraints_extrema_vals[ 0 ]
    state.constraints_min_vals = constraints_extrema_vals[ 1 ]

    constraints_extrema_global_vals: list[ dict[ tuple[ str, ...], float ] | None ] = [ None, None ]
    if len( state.right_labels ) > 1:
        constraints_extrema_global_cols = st.columns( 2 )
        for id, constraints_extrema_global_col in enumerate( constraints_extrema_global_cols ):
            with constraints_extrema_global_col:
                use_constraints_extrema_global_vals: bool = st.checkbox(
                    f"Is there group of ressources constrained with a { extrema[ id ] } value for all { state.right_entities_type }"
                )
                if use_constraints_extrema_global_vals:
                    constraints_extrema_global_vals[ id ] = {}
                    nb_constrained_groups: int = st.number_input(
                        "How many group of ressources are constrained", value=1
                    )
                    for _ in range( nb_constrained_groups ):
                        constrained_ressources: tuple[ str, ...] = tuple(
                            st.multiselect(
                                f"Select the ressources constrained by the same { extrema[ id ] } value for all { state.right_entities_type }",
                                state.ressources_labels
                            )
                        )
                        if len( constrained_ressources ) > 0:
                            constraint_val: float = st.number_input(
                                f"Set the { extrema[ id ] } value constrainning the { constrained_ressources }",
                                value=1.
                            )
                            constraints_extrema_global_vals[ id ][ constrained_ressources ] = constraint_val
                        else:
                            if constrained_ressources in constraints_extrema_global_vals[ id ]:
                                del constraints_extrema_global_vals[ id ][ constrained_ressources ]
                else:
                    constraints_extrema_global_vals[ id ] = None

    state.constraints_max_global_vals = constraints_extrema_global_vals[ 0 ]
    state.constraints_min_global_vals = constraints_extrema_global_vals[ 1 ]
