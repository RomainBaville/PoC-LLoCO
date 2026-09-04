# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025-2026 AKKODIS.
# SPDX-FileContributor: Romain Baville, Fidel Monteiro

import streamlit as st

import ui.theme as theme
from llm.client.llama_client import close_llama_server, start_llama_server
from llm.model_picker import ModelInfo, get_models
from ui.registry import PROBLEM_REGISTRY, ProblemType


def ai_models() -> None:
    """Configure the ui to chose the AI model to use."""
    # Default configuration
    st.session_state.setdefault( "llama_server_pid", 0 )

    available_models: list[ ModelInfo ] = get_models()
    if available_models == []:
        st.markdown(
            '<div class="ui-model-banner">'
            '<span class="ui-model-banner-label">AI Model</span>'
            '<span class="ui-model-banner-none">No model detected</span>'
            '</div>',
            unsafe_allow_html=True
        )
    else:
        model: ModelInfo | None = st.selectbox(
            "**AI models**",
            options=available_models,
            placeholder="Chose your AI model",
            index=None,
            disabled=st.session_state.step
        )
        st.session_state.model_info = model
        if st.session_state.model_info is not None:
            st.markdown(
                f'<div class="ui-model-banner">'
                f'<span class="ui-model-banner-label">AI Model</span>'
                f'<span class="ui-model-banner-value">{ st.session_state.model_info.label }</span>'
                f'</div>',
                unsafe_allow_html=True
            )

        # Open or close the llama server
        if st.session_state.get( "model_info" ) and st.session_state.model_info.source == "llama-server":
            st.session_state.llama_server_pid = start_llama_server(
                st.session_state.model_info.name, llama_server_pid=st.session_state.llama_server_pid
            )
        elif st.session_state.llama_server_pid != 0:
            close_llama_server( st.session_state.llama_server_pid )
            st.session_state.llama_server_pid = 0


def problems_configuration() -> None:
    """Configure the ui to chose the problem configuration."""
    # Default configuration
    st.session_state.setdefault( "problem_type", None )
    st.session_state.setdefault( "config_validated", False )
    st.session_state.setdefault( "journey", {} )

    problem: ProblemType | None = st.selectbox(
        "**Problems configuration**", options=PROBLEM_REGISTRY, placeholder="Chose your problem", index=None
    )
    st.session_state.problem_type = problem

    can_validate = ( st.session_state.get( "problem_type" ) )
    if st.button( "Validate configuration", type="primary", use_container_width=True, disabled=not can_validate ):
        st.session_state.config_validated = True
        st.session_state.step = 1
        st.session_state.journey[ "Problem type" ] = st.session_state.problem_type.label
        st.rerun()

    if not can_validate:
        st.markdown( '<p class="ui-hint">-> Chose your problem first</p>', unsafe_allow_html=True )


def guide_panel() -> None:
    """Configure the guide panel."""
    # Guard: if required keys were lost (hot reload, session reset), fall back to config panel
    if st.session_state.problem_type is None:
        st.error( "No problem configuration set." )
        st.session_state.config_validated = False
        st.rerun()

    # Configuration summary
    theme.section_label( "Active configuration" )
    st.markdown( f"**{ st.session_state.problem_type.label }**" )

    theme.divider()

    # AI guide
    theme.section_label( "AI guide" )
    if st.session_state.get( "onboarding_result" ):
        theme.ai_block( st.session_state.onboarding_result )
    elif st.session_state.get( "model_info" ):
        st.markdown(
            '<p class="ui-hint">Describe your problem and analyse it to get an AI guide.</p>', unsafe_allow_html=True
        )
    else:
        st.markdown( '<p class="ui-hint">Select an AI model if you want an AI guide.</p>', unsafe_allow_html=True )

    theme.divider()

    # Compact journal
    theme.section_label( "Journal" )
    entries = st.session_state.get( "journey", {} )
    if entries:
        for entry, value in entries.items():
            st.markdown( f'<div class="ui-journal">· { entry }: { value }</div>', unsafe_allow_html=True )
    else:
        st.markdown( '<p class="ui-hint">No action yet</p>', unsafe_allow_html=True )

    st.markdown( "" )
    if st.button( "Reste", use_container_width=True ):
        st.session_state.clear()
        st.rerun()


# ── Public entry point ───────────────────────────────────────────────────────
def render() -> None:
    """Configure the sidebar."""
    with st.sidebar:
        ai_models()
        theme.divider()

        if st.session_state.get( "config_validated" ):
            guide_panel()
        else:
            problems_configuration()
