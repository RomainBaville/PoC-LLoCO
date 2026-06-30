# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025-2026 AKKODIS.
# SPDX-FileContributor: Romain Baville

import streamlit as st

from domain.assignment.score.matching_penalty_functions import PenaltyFunctions
from domain.assignment.score.matching_reward_functions import RewardFunctions
from domain.objective import Objective
from ui.assignment.builder import build_vals


def map_matching( state ):
    state.matching_labels = tuple(
        st.multiselect(
            f"Select columns identifying variables to match between { state.left_entities_type } and { state.right_entities_type }",
            set( state.left_cols ).intersection( set( state.right_cols ) ),
        )
    )
    state.matching_left_vals = build_vals( state.left_entities_col_label, state.matching_labels, state.left_rows )
    state.matching_right_vals = build_vals( state.right_entities_col_label, state.matching_labels, state.right_rows )


def matching_strategy( state ):
    state.matching_objective = st.selectbox( " Set the objective for the matching", Objective )

    state.reward_function = st.selectbox(
        "Set the reward function used in the computation of the score matching",
        RewardFunctions,
    )

    state.penalty_function = st.selectbox(
        "Set the penalty function used in the computation of the score matching",
        PenaltyFunctions,
    )

    state.matching_weights = dict.fromkeys( state.matching_labels, 1.0 )
    use_matching_weights: bool = st.checkbox( "Is there varibales to match with weights" )
    if use_matching_weights:
        matching_labels: tuple[ str, ...] = tuple(
            st.multiselect( "Select the variables with a weight", state.matching_labels )
        )
        if len( matching_labels ) > 0:
            for matching_label in matching_labels:
                state.matching_weights[ matching_label ] = st.number_input( f"Weight for { matching_label }", value=1. )


def matching_constraints( state ):
    extrema: tuple[ str, str ] = ( "maximum", "minimum" )
    matching_extrema_cols = st.columns( 2 )
    matching_extrema_vals: list[ dict[ tuple[ str, str ], float ] | None ] = [ None, None ]
    for id, matching_extrema_col in enumerate( matching_extrema_cols ):
        with matching_extrema_col:
            use_matching_extrema_vals: bool = st.checkbox(
                f"Is there variables constrained by a { extrema[ id ] } value ?"
            )
            if use_matching_extrema_vals:
                variables_labels: tuple[ str, ...] = tuple(
                    st.multiselect(
                        f"Select variables constrained by a { extrema[ id ] } value", state.matching_labels
                    )
                )
                if len( variables_labels ) > 0:
                    matching_extrema_variables_labels: dict[ str, str ] = {}
                    for variable_label in variables_labels:
                        matching_extrema_variables_labels[ variable_label ] = st.selectbox(
                            f"Select the column identifying the constrainning variable with the { extrema[ id ] } values of the { variable_label }",
                            state.right_cols
                        )

                    matching_extrema_vals[ id ] = build_vals(
                        state.right_entities_col_label, matching_extrema_variables_labels, state.right_rows
                    )
                else:
                    matching_extrema_vals[ id ] = None
            else:
                matching_extrema_vals[ id ] = None

    state.matching_max_vals = matching_extrema_vals[ 0 ]
    state.matching_min_vals = matching_extrema_vals[ 1 ]
