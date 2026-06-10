# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025-2026 AKKODIS.
# SPDX-FileContributor: Romain Baville

import streamlit as st

from domain.objective import Objective
from domain.assignment.skills.skills_reward_functions import RewardFunction
from domain.assignment.skills.skills_penalty_functions import PenaltyFunctions
from ui.assignment.builder import build_val_dict

def use_skills( state ):
    state.use_skills = st.checkbox( "Use skills to compare between entites (e.g. python_level)" )

def map_skills( state ):
    state.skills_label = st.multiselect(
        f"Columns identifying skills",
        state.left_cols,
    )
    state.skills_val = build_val_dict( state.left_entities, state.skills_label, state.left_rows )
    state.requirement_skills_val = build_val_dict( state.right_entities, state.skills_label, state.right_rows )

def skills_strategy( state ):
    state.skills_objective = st.selectbox( f" What is the objective with skills", Objective )

    state.skills_reward_function = st.selectbox(
        "Reward function",
        RewardFunction,
    )

    state.skills_penalty_function = st.selectbox(
        "Penalty function",
        PenaltyFunctions,
    )

    use_skills_weight = st.checkbox( f"Use skills weight" )
    if use_skills_weight:
        state.skills_weight = {}
        for skill in state.skills_label:
            state.skills_weight[ skill ] = st.number_input( f"Weight for { skill }", value=1.0 )
    else:
        state.skills_weight = None
