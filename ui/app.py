# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025-2026 AKKODIS.
# SPDX-FileContributor: Romain Baville

import sys
from pathlib import Path

import streamlit as st

from ui.registry import PROBLEM_REGISTRY
from ui.utils import select_problem

# --- make project root importable ---
ROOT_DIR = Path( __file__ ).resolve().parents[ 1 ]
sys.path.append( str( ROOT_DIR ) )


# --------------------------------------------------
# App setup
# --------------------------------------------------
st.set_page_config( page_title="Optimization Playground", layout="wide" )
st.title( "Optimization Playground" )

st.session_state.setdefault( "step", 0 )
st.session_state.setdefault( "problem_type", None )
st.session_state.setdefault( "data_source", None )

# ==================================================
# STEP -1 — LLM onboarding
# ==================================================
if st.session_state.step == -1:
    st.header( "Describe your problem" )

    user_description = st.text_area(
        "Explain in plain language what you want to optimize",
        height=150,
        placeholder="Example: I want to assign employees to projects based on their skills...",
    )

    # TODO in a futur PR
    """
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Explain how to use the tool"):
            with st.spinner("Analyzing your problem..."):
                prompt = build_onboarding_prompt(user_description)
                explanation = ask_llm_request(prompt)
            st.subheader("How the tool will help you")
            st.markdown(explanation)
    with col2:
        navigation_buttons(show_back=False, show_close=False)
    """

    st.stop()

# ==================================================
# STEP 0 — Problem selection
# ==================================================
if st.session_state.step == 0:
    st.header( "Choose a problem type" )

    cols = st.columns( len( PROBLEM_REGISTRY ) )

    for col, problem in zip( cols, PROBLEM_REGISTRY.values(), strict=False ):
        with col:
            st.button( problem.label, on_click=select_problem, args=( st.session_state, problem.key ) )

    st.stop()

# ==================================================
# Delegate to registered problem UI
# ==================================================
if st.session_state.problem_key in PROBLEM_REGISTRY:
    PROBLEM_REGISTRY[ st.session_state.problem_key ].render_fn( st.session_state )
