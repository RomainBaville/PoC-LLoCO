# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025-2026 AKKODIS.
# SPDX-FileContributor: Romain Baville

import streamlit as st

from domain.objective import Objective
from ui.assignment.builder import build_val_dict, build_extrema_dict

def use_costs( state ):
    state.use_costs = st.checkbox( "Use costs to associate entities with score optimization or constraints (e.g. Salary, Budget ...)" )


def map_costs( state ):
    state.costs_label = st.multiselect( "Select columns identifying your costs", state.left_cols, )
    state.costs_val = build_val_dict( state.left_entities, state.costs_label, state.left_rows )


    use_limit_costs_entities = st.checkbox( f"Is there a limit per costs per { state.right_label }" )
    if use_limit_costs_entities:
        costs_entities_limited_label = st.multiselect( f"Select costs of { state.left_label } with a limit per { state.right_label }", state.costs_label )
        nb_costs_entities_limited = len( costs_entities_limited_label )
        if nb_costs_entities_limited > 0:
            state.limit_costs_entities_label = {}
            limit_costs_entities_cols = st.columns( nb_costs_entities_limited )
            for id, limit_costs_entities_col in enumerate( limit_costs_entities_cols ):
                with limit_costs_entities_col:
                    cost_entities_limited_label = costs_entities_limited_label[ id ]
                    limit_cost_entities_label = st.selectbox( f"Select the column identifying the cost limit for the { cost_entities_limited_label } in the { state.right_label }", state.right_cols )
                    state.limit_costs_entities_label[ limit_cost_entities_label ] = cost_entities_limited_label

            state.limit_costs_entities_val = build_val_dict( state.right_entities, state.limit_costs_entities_label, state.right_rows )
        else:
            state.limit_costs_entities_label = None
            state.limit_costs_entities_val = None
    else:
        state.limit_costs_entities_label = None
        state.limit_costs_entities_val = None


    use_limit_all_costs_entities = st.checkbox( f"Is there a limit for all costs per { state.right_label }" )
    if use_limit_all_costs_entities:
        limit_all_costs_entities_label = st.selectbox( f"Select the column identifying the cost limit per { state.right_label } for all costs of { state.left_label }", state.right_cols )
        state.limit_all_costs_entities_val = build_extrema_dict( state.right_entities_col_id, state.right_rows, extrema_col_label=limit_all_costs_entities_label )
    else:
        state.limit_all_costs_entities_val = None


    use_limit_costs_all_entities = st.checkbox( f"Is there a limit per costs for all { state.right_label }" )
    if use_limit_costs_all_entities:
        costs_all_entities_limited_label = st.multiselect( f"Select costs of { state.left_label } with a limit for all {state.right_label }", state.costs_label )
        nb_costs_all_entities_limited = len( costs_all_entities_limited_label )
        if nb_costs_all_entities_limited > 0:
            costs_all_entities_limited_cols = st.columns( nb_costs_all_entities_limited )
            state.limit_costs_all_entities_val = {}
            for id, costs_all_entities_limited_col in enumerate( costs_all_entities_limited_cols ):
                with costs_all_entities_limited_col:
                    cost_all_entities_limited_label = costs_all_entities_limited_label[ id ]
                    state.limit_costs_all_entities_val[ cost_all_entities_limited_label ] = st.number_input( f"Set the limit for all { state.right_label } for the { cost_all_entities_limited_label }", value=1. )
        else:
            state.limit_costs_all_entities_val = None
    else:
        state.limit_costs_all_entities_val = None


    use_limit_all_costs_all_entities = st.checkbox( f"Is there a limit for all costs of {state.left_label } for all { state.right_label }" )
    if use_limit_all_costs_all_entities:
        state.limit_all_costs_all_entities_val = st.number_input( f"Set the limit for all costs of { state.left_label } for all { state.right_label }", value=1 )
    else:
        state.limit_all_costs_all_entities_val = None


def costs_strategy( state ):
    state.costs_objective = {}
    for cost in state.costs_label:
        state.costs_objective[ cost ] = st.selectbox( f"Select the objective for { cost }", Objective )
