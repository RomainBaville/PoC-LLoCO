# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025-2026 AKKODIS.
# SPDX-FileContributor: Romain Baville

import streamlit as st

from domain.objective import Objective
from domain.assignment.matching.matching_reward_functions import RewardFunctions
from domain.assignment.matching.matching_penalty_functions import PenaltyFunctions
from ui.assignment.builder import build_val_dict


def use_matching( state ):
    state.use_matching = st.checkbox( "Use a matching between the two entities variables to evaluate the association score (e.g. python_level, english_level ...)" )


def map_matching( state ):
    state.matching_labels = st.multiselect(
        f"Select columns identifying the variable to match between { state.left_entities } and { state.right_entities }",
        set( state.left_cols ).intersection( set( state.right_cols ) ),
    )
    state.matching_left_vals = build_val_dict( state.left_labels, state.matching_labels, state.left_rows )
    state.matching_right_vals = build_val_dict( state.right_labels, state.matching_labels, state.right_rows )


def matching_strategy( state ):
    state.matching_objective = st.selectbox( f" Set the objective for the matching", Objective )

    state.reward_function = st.selectbox(
        "Set the reward function used in the computation of the score matching",
        RewardFunctions,
    )

    state.penalty_function = st.selectbox(
        "Set the penalty function used in the computation of the score matching",
        PenaltyFunctions,
    )


def matching_constraints( state ):
    use_matching_weights = st.checkbox( f"Is there varibales to match with weights" )
    if use_matching_weights:
        matching_labels: list[ str ] = st.multiselect( "Select the variables with a weight", state.matching_labels )
        if len( matching_labels ) > 0:
            state.matching_weights = {}
            for matching_label in matching_labels:
                state.matching_weights[ matching_label ] = st.number_input( f"Weight for { matching_label }", value=1.0 )
        else:
            state.matching_weights = None
    else:
        state.matching_weights = None

    extrema = [ "maximum", "minimum" ]
    cols = st.columns( 2 )
    constraints_vals = [ None, None ]
    for id, col in enumerate( cols ):
        with col:
            use_constraints_vals = st.checkbox( f"Is there variables with a { extrema[ id ] } value constraint" )
            if use_constraints_vals:
                constraints_labels = st.multiselect( f"Select variables with a { extrema[ id ] } value constraint", state.matching_labels )
                if len( constraints_labels ) > 0:
                    constrainning_labels = {}
                    for constraint_label in constraints_labels:
                        constrainning_labels[ constraint_label ] = st.selectbox( f"Select the column identifying the variable with the { extrema[ id ] } values constraint the { constraint_label } in the { state.right_entities }", state.right_cols )

                    constraints_vals[ id ] = build_val_dict( state.right_labels, constrainning_labels, state.right_rows )
                else:
                    constraints_vals[ id ] = None
            else:
                constraints_vals[ id ] = None

    state.matching_max_vals = constraints_vals[ 0 ]
    state.matching_min_vals = constraints_vals[ 1 ]
