# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025-2026 AKKODIS.
# SPDX-FileContributor: Romain Baville

import streamlit as st
from typing_extensions import Optional

from domain.objective import Objective
from ui.assignment.builder import build_val_dict

def use_costs( state ):
    state.use_costs = st.checkbox( "Use costs to constrain left entity assignment (e.g. Salary)" )


def map_costs( state ):
    costs_label = st.multiselect(
        f"Columns identifying costs",
        state.left_cols,
    )
    state.costs_label = { cost_label: None for cost_label in costs_label }
    state.costs_val = build_val_dict( state.left_entities, state.costs_label.keys(), state.left_rows )

    use_costs_limit = st.checkbox( f"Use a limit for at least for one cost per left entities" )
    if use_costs_limit:
        for cost in state.costs_label:
            state.costs_label[ cost ] = st.selectbox( f" What is the limit for { cost }", [ None ]+ state.right_cols )

        limit_costs_label: list[ Optional[ float ] ] = list( state.costs_label.values() )
        nb_none: int = limit_costs_label.count( None )
        for _ in range( nb_none ):
            limit_costs_label.remove( None )

        if len( limit_costs_label ) > 0:
            state.limit_costs_val = build_val_dict( state.right_entities, limit_costs_label, state.right_rows )
        else:
            state.limit_costs_val = None


def costs_strategy( state ):
    state.costs_objective = {}
    for cost in state.costs_label:
        state.costs_objective[ cost ] = st.selectbox( f" What is the objective with { cost }", Objective )
