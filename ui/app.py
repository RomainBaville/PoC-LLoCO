# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025-2026 AKKODIS.
# SPDX-FileContributor: Romain Baville, Fidel Monteiro
# ruff: noqa: E402 # disable Module level import not at top of file

import sys
from pathlib import Path

import streamlit as st

ROOT_DIR = Path( __file__ ).resolve().parents[ 1 ]
sys.path.append( str( ROOT_DIR ) )

import ui.theme as theme
from llm.onbording.onboarding_prompt import build_onboarding_prompt
from llm.onbording.utils import infer_problem_configuration
from ui.sidebar import render as render_sidebar

# ── Page setup ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Optimization Playground",
    page_icon="⚙️",
    layout="wide"
)
theme.inject()

# ── Session defaults ─────────────────────────────────────────────────────────
st.session_state.setdefault( "step", 0 )
st.session_state.setdefault( "model_info", None )
st.session_state.setdefault( "problem_type", None )
st.session_state.setdefault( "user_description", None )
st.session_state.setdefault( "onboarding", None )
st.session_state.setdefault( "analysis_done", False )

# ── Sidebar + top bar ────────────────────────────────────────────────────────
render_sidebar()
theme.topbar( st.session_state.model_info )


# ── Main area renderers ───────────────────────────────────────────────────────
def ai_onboarding() -> None:
    """Configure the ui to get the AI onbording."""
    theme.hero(
        "Optimization Playground",
        "Describe you problem. A configuration will automaticly be set from the AI analyse"
    )

    st.markdown( "### Analyse your problem with AI" )
    st.session_state.user_desc = st.text_area(
        "Description",
        height=110,
        placeholder=( "Example : I want to affect employees and projects from the employees skills." ),
        label_visibility="collapsed"
    )

    if st.button( "Analyse", type="primary" ):
        if not st.session_state.user_desc.strip():
            st.warning( "Set your problem description first." )
        elif not st.session_state.get( "model_info" ):
            st.warning( "Select an AI model first." )
        else:
            try:
                with st.spinner( "Analysing ..." ):
                    prompt = build_onboarding_prompt( st.session_state.user_desc )
                    st.session_state.onboarding = st.session_state.model_info.ask_client( prompt, st.session_state.model_info.name )

                st.session_state.analysis_done = True

                # Infer and immediately apply configuration recommendation
                try:
                    st.session_state.problem_type = infer_problem_configuration(
                        st.session_state.user_desc, st.session_state.onboarding
                    )
                except ValueError as e:
                    st.warning( f"{ e } Chose your problem manualy." )

                # Reset any prior validation so user re-confirms the new config
                st.session_state.config_validated = False
                st.session_state.data_step = 1

                st.rerun()

            except Exception as exc:
                st.error( f"Erreor while using AI: { exc }" )

    if st.session_state.get( "onboarding" ):
        st.markdown( "**AI guide**" )
        theme.ai_block( st.session_state.onboarding )
        st.markdown( "" )
        st.markdown(
            '<p class="ui-hint">The configuration has been set, check and modify it if needed then click on the buton'
            '<strong>Validate configuration</strong>.</p>',
            unsafe_allow_html=True
        )
    else:
        st.markdown( "" )
        st.markdown(
            '<p class="ui-hint">Describe you problem. '
            'A configuration will automaticly be set from the AI analyse.</p>',
            unsafe_allow_html=True
        )


def problem_resolution_workflow() -> None:
    """Delegate to the correct problem ui."""
    theme.hero( "Problem resolution workflow" )
    if st.session_state.get( "problem_type" ):
        st.session_state.problem_type.render_fn( st.session_state )
    else:
        st.error( "No problem configuration set." )
        st.session_state.config_validated = False
        st.rerun()


# ── Main routing ──────────────────────────────────────────────────────────────
if not st.session_state.get( "config_validated" ):
    ai_onboarding()
else:
    problem_resolution_workflow()
