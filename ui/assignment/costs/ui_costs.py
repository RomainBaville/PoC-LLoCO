# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025-2026 AKKODIS.
# SPDX-FileContributor: Romain Baville

import streamlit as st

from domain.objective import Objective
from ui.assignment.builder import build_val_dict

def use_costs( state ):
    state.use_costs = st.checkbox( "Use feature to constrain left entity assignment (e.g. Costs)" )
    if state.use_costs:
        state.cost_label = st.text_input(
            "Feature label (e.g. Costs)", "Costs"
        )

def map_costs( state ):
    state.costs_label = st.multiselect(
        f"Columns identifying { st.session_state.cost_label }",
        state.left_cols,
    )

    limit_costs_label = {}
    for cost in state.costs_label:
        use_costs_limit = st.checkbox( f"Use a right entity limit for { cost } (e.g. Budget for Salary)" )
        if use_costs_limit:
            limit_costs_label[ cost ] = st.selectbox( f" What is the limit for the { state.cost_label } { cost }", state.right_cols )

    state.costs_val = build_val_dict( state.left_entities, state.costs_label, state.left_rows )
    state.limit_costs_label = None if limit_costs_label == {} else limit_costs_label

    if state.limit_costs_label is not None:
        limit_costs_val = build_val_dict( state.right_entities, state.limit_costs_label.values(), state.right_rows )
    else:
        limit_costs_val = None

    st.session_state.limit_costs_val = limit_costs_val


def costs_strategy( state ):
    state.costs_objective = {}
    for cost in state.costs_label:
        state.costs_objective[ cost ] = st.selectbox( f" What is the objective with the { state.cost_label } { cost }", Objective )
