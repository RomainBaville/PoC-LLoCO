# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025-2026 AKKODIS.
# SPDX-FileContributor: Romain Baville

import streamlit as st

from domain.objective import Objective
from domain.assignment.skills.skills_reward_functions import RewardFunction
from domain.assignment.skills.skills_penalty_functions import PenaltyFunctions
from ui.assignment.builder import build_val_dict

def use_skills( state ):
    state.use_skills = st.checkbox( "Use feature to compare between entites (e.g. Skills)" )
    if state.use_skills:
        state.skill_label = st.text_input(
            "Feature label (e.g. Skills)", "Skills"
        )

def map_skills( state ):
    state.skills_label = st.multiselect(
        f"Columns identifying { st.session_state.skill_label }",
        state.left_cols,
    )
    state.left_skills_val = build_val_dict( state.left_entities, state.skills_label, state.left_rows )
    state.right_skills_val = build_val_dict( state.right_entities, state.skills_label, state.right_rows )

def skills_strategy( state ):
    state.skills_objective = st.selectbox( f" What is the objective with the { state.skill_label }", Objective )

    state.skills_reward_function = st.selectbox(
        "Reward function",
        RewardFunction,
    )

    state.skills_penalty_function = st.selectbox(
        "Penalty function",
        PenaltyFunctions,
    )

    use_skill_weights = st.checkbox( f"Use { state.skill_label } weights" )
    if use_skill_weights:
        state.skills_weight = {}
        for skill_label in st.session_state.skills_label:
            state.skills_weight[ skill_label ] = st.number_input( f"Weight for { skill_label }", value=1.0 )
    else:
        state.skills_weight = None
