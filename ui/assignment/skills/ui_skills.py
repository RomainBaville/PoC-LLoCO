# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025-2026 AKKODIS.
# SPDX-FileContributor: Romain Baville

import streamlit as st

from domain.objective import Objective
from domain.assignment.skills.skills_reward_functions import RewardFunction
from domain.assignment.skills.skills_penalty_functions import PenaltyFunctions
from ui.assignment.builder import build_val_dict

def use_skills( state ):
    state.use_skills = st.checkbox( "Use skills to associate entites with score or constraints (e.g. python_level, produciton_rate ...)" )

def map_skills( state ):

    state.skills_label = st.multiselect(
        f"Select columns identifying skills in both { state.left_label } and { state.right_label }",
        set( state.left_cols ).intersection( set( state.right_cols ) ),
    )
    state.skills_val = build_val_dict( state.left_entities, state.skills_label, state.left_rows )
    state.requirement_skills_val = build_val_dict( state.right_entities, state.skills_label, state.right_rows )

    use_min_requirement_skills = st.checkbox( f"Is there skills with minimum requirement" )
    if use_min_requirement_skills:
        skills_min_requirement_label = st.multiselect( f"Select the skills with a minimum requirement per { state.right_label }", state.skills_label )
        nb_skills_min_requirement = len( skills_min_requirement_label )
        if nb_skills_min_requirement > 0:
            state.min_requirement_skills_label = {}
            min_requirement_skills_cols = st.columns( nb_skills_min_requirement )
            for id, min_requirement_skills_col in enumerate( min_requirement_skills_cols ):
                with min_requirement_skills_col:
                    skill_min_requirement_label = skills_min_requirement_label[ id ]
                    min_requirement_skill_label = st.selectbox( f"Select the column identifying the skill minimum requirement for the { skill_min_requirement_label } in the { state.right_label }", state.right_cols )
                    state.min_requirement_skills_label[ min_requirement_skill_label ] = skill_min_requirement_label

            state.min_requirement_skills_val = build_val_dict( state.right_entities, state.min_requirement_skills_label, state.right_rows )
        else:
            state.min_requirement_skills_label = None
            state.min_requirement_skills_val = None
    else:
        state.min_requirement_skills_label = None
        state.min_requirement_skills_val = None

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
