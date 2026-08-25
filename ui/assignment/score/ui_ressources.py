# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025-2026 AKKODIS.
# SPDX-FileContributor: Romain Baville

import streamlit as st
from streamlit.runtime.state.session_state_proxy import SessionStateProxy

from domain.objective import Objective
from ui.assignment.builder import build_vals


def map_ressources( session_state: SessionStateProxy ) -> None:
    """Configure the interface to set the data in order to map the ressources.

    Args:
        session_state (SessionStateProxy): The session state.
    """
    session_state.ressources_labels = tuple(
        st.multiselect(
            "Select columns identifying your ressources",
            session_state.left_cols,
            session_state.lock_mapping
        )
    )
    session_state.journey[ "Ressources variables" ] = session_state.ressources_labels

    session_state.ressources_vals = build_vals(
        session_state.left_entities_col_label,
        session_state.ressources_labels,
        session_state.left_rows
    )


def ressources_strategy( session_state: SessionStateProxy ) -> None:
    """Configure the interface to set the assignment ressources strategy.

    Args:
        session_state (SessionStateProxy): The session state.
    """
    session_state.ressoucres_objectives = {}
    for ressource_label in session_state.ressources_labels:
        session_state.ressoucres_objectives[ ressource_label ] = st.selectbox(
            f"Select the objective for { ressource_label }", Objective, disabled=session_state.lock_strategy
        )
    session_state.journey[ "Ressources objectives" ] = session_state.ressoucres_objectives

    session_state.ressources_weights = dict.fromkeys( session_state.ressources_labels, 1.0 )
    use_ressources_weights: bool = st.checkbox( "Is there ressources with weights", disabled=session_state.lock_strategy )
    if use_ressources_weights:
        ressources_labels: tuple[ str, ...] = tuple(
            st.multiselect( "Select the ressources with a weight", session_state.ressources_labels, disabled=session_state.lock_strategy )
        )
        if len( ressources_labels ) > 0:
            for ressource_label in ressources_labels:
                session_state.ressources_weights[ ressource_label ] = st.number_input(
                    f"Weight for { ressource_label }", value=1., disabled=session_state.lock_strategy
                )
            session_state.journey[ "Ressources weights" ] = session_state.ressources_weights
    else:
        if "Ressources weights" in session_state.journey:
            del( session_state.journey[ "Ressources weights" ] )
            st.rerun()


def ressources_constraints( session_state: SessionStateProxy ) -> None:
    """Configure the interface to set the constraints data.

    Args:
        session_state (SessionStateProxy): The session state.
    """
    extrema: tuple[ str, str ] = ( "maximum", "minimum" )
    constraints_extrema_cols = st.columns( 2 )
    constraints_extrema_vals: list[ dict[ tuple[ str, ...], float ] | None ] = [ None, None ]
    for id, constraints_extrema_col in enumerate( constraints_extrema_cols ):
        with constraints_extrema_col:
            use_constraints_extrema_vals: bool = st.checkbox(
                f"Is there ressources constrained by a { extrema[ id ] } value ?", disabled=session_state.lock_constraints
            )
            if use_constraints_extrema_vals:
                constraints_labels: tuple[ str, ...] = tuple(
                    st.multiselect(
                        f"Select all variables used as { extrema[ id ] } constraint",
                        session_state.right_cols, disabled=session_state.lock_constraints
                    )
                )
                if len( constraints_labels ) > 0:
                    constraints_ressources_labels: dict[ str, list[ str ] ] = {}
                    for constraint_label in constraints_labels:
                        constraints_ressources_labels[ constraint_label ] = st.multiselect(
                            f"Select ressources constrainning by { constraint_label }",
                            session_state.ressources_labels, disabled=session_state.lock_constraints
                        )

                    vals: dict[ tuple[ str, ...], float ] = {}
                    for right_row in session_state.right_rows:
                        right_label: str = right_row[ session_state.right_entities_col_label ]
                        for constraint_label, ressources_labels in constraints_ressources_labels.items():
                            key = [ right_label ]
                            key.extend( ressources_labels )
                            if len( key ) > 1:
                                vals[ tuple( key ) ] = float( right_row[ constraint_label ] )
                            elif tuple( key ) in vals:
                                del vals[ tuple( key ) ]

                    if vals != {}:
                        constraints_extrema_vals[ id ] = vals
                    else:
                        constraints_extrema_vals[ id ] = None
                else:
                    constraints_extrema_vals[ id ] = None
            else:
                constraints_extrema_vals[ id ] = None

    session_state.constraints_max_vals = constraints_extrema_vals[ 0 ]
    if session_state.constraints_max_vals is not None:
        session_state.journey[ "Constraints max vals" ] = session_state.constraints_max_vals
    elif "Constraints max vals" in session_state.journey:
        del( session_state.journey[ "Constraints max vals" ] )
        st.rerun()

    session_state.constraints_min_vals = constraints_extrema_vals[ 1 ]
    if session_state.constraints_min_vals is not None:
        session_state.journey[ "Constraints min vals" ] = session_state.constraints_min_vals
    elif "Constraints min vals" in session_state.journey:
        del( session_state.journey[ "Constraints min vals" ] )
        st.rerun()

    constraints_extrema_global_vals: list[ dict[ tuple[ str, ...], float ] | None ] = [ None, None ]
    if len( session_state.right_labels ) > 1:
        constraints_extrema_global_cols = st.columns( 2 )
        for id, constraints_extrema_global_col in enumerate( constraints_extrema_global_cols ):
            with constraints_extrema_global_col:
                use_constraints_extrema_global_vals: bool = st.checkbox(
                    f"Is there group of ressources constrained with a " \
                    f"{ extrema[ id ] } value for all { session_state.right_entities_type }", disabled=session_state.lock_constraints
                )
                if use_constraints_extrema_global_vals:
                    curent_constraints_extrema_global_vals: dict[ tuple[ str, ...], float ] = {}
                    nb_constrained_groups: int = st.number_input(
                        "How many group of ressources are constrained", value=1, disabled=session_state.lock_constraints
                    )
                    for _ in range( nb_constrained_groups ):
                        constrained_ressources: tuple[ str, ...] = tuple(
                            st.multiselect(
                                f"Select the ressources constrained by the same { extrema[ id ] } " \
                                f"value for all { session_state.right_entities_type }",
                                session_state.ressources_labels, disabled=session_state.lock_constraints
                            )
                        )
                        if len( constrained_ressources ) > 0:
                            constraint_val: float = st.number_input(
                                f"Set the { extrema[ id ] } value constrainning the { constrained_ressources }",
                                value=1., disabled=session_state.lock_constraints
                            )
                            curent_constraints_extrema_global_vals[ constrained_ressources ] = constraint_val
                        else:
                            if constrained_ressources in curent_constraints_extrema_global_vals:
                                del curent_constraints_extrema_global_vals[ constrained_ressources ]
                    constraints_extrema_global_vals[ id ] = curent_constraints_extrema_global_vals
                else:
                    constraints_extrema_global_vals[ id ] = None

    session_state.constraints_max_global_vals = constraints_extrema_global_vals[ 0 ]
    if session_state.constraints_max_global_vals is not None:
        session_state.journey[ "Constraints max global vals" ] = session_state.constraints_max_global_vals
    elif "Constraints max global vals" in session_state.journey:
        del( session_state.journey[ "Constraints max global vals" ] )
        st.rerun()

    session_state.constraints_min_global_vals = constraints_extrema_global_vals[ 1 ]
    if session_state.constraints_min_global_vals is not None:
        session_state.journey[ "Constraints min global vals" ] = session_state.constraints_min_global_vals
    elif "Constraints min global vals" in session_state.journey:
        del( session_state.journey[ "Constraints min global vals" ] )
        st.rerun()
