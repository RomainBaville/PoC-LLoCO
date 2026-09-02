# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025-2026 AKKODIS.

import streamlit as st

import ui.theme as theme
from llm.client.llama_client import close_llama_server, start_llama_server
from llm.model_picker import get_models
from ui.registry import PROBLEM_REGISTRY


# ── Model picker (always at top) ────────────────────────────────────────────
def _render_model_picker():
    st.session_state.setdefault( "llama_server", None )
    available_models = get_models()
    model_options = {
        m.key: m
        for m in available_models
    }

    if available_models:
        selected_key = st.selectbox(
            "Modèle IA",
            options=[ "none" ] + list( model_options.keys() ),
            format_func=lambda k: "— None —" if k == "none" else model_options[ k ].label,
            label_visibility="visible",
            key="llm_model_key",
        )
        if selected_key != "none":
            m = model_options[ selected_key ]
            st.session_state.llm_url = m.api_url
            st.session_state.llm_model_name = m.model_name
            st.session_state.llm_source = m.source
            st.session_state.llm_model_label = m.label
        else:
            st.session_state.llm_url = None
            st.session_state.llm_model_name = None
            st.session_state.llm_source = None
            st.session_state.llm_model_label = None
    else:
        st.session_state.llm_url = None
        st.session_state.llm_model_name = None
        st.session_state.llm_model_label = None

    if st.session_state.llm_source == "llama-server":
        st.session_state.llama_server = start_llama_server(
            st.session_state.llama_server, st.session_state.llm_url, st.session_state.llm_model_name
        )
    elif st.session_state.llama_server is not None:
        st.session_state.llama_server = close_llama_server( st.session_state.llama_server )

    if st.session_state.llm_model_label:
        st.markdown(
            f'<div class="ui-model-banner">'
            f'<span class="ui-model-banner-label">Modèle actif</span>'
            f'<span class="ui-model-banner-value">⬤ { st.session_state.llm_model_label }</span>'
            f'</div>',
            unsafe_allow_html=True,
        )
    elif not available_models:
        st.markdown(
            '<div class="ui-model-banner">'
            '<span class="ui-model-banner-label">Modèle IA</span>'
            '<span class="ui-model-banner-none">Aucun modèle détecté</span>'
            '</div>',
            unsafe_allow_html=True,
        )


# ── Config panel — shown before validation ───────────────────────────────────


def _render_config_panel():
    st.markdown( "## Configuration" )

    # ── Problem ─────────────────────────────────────
    theme.section_label( "Problem" )
    problem_options = [ "Chose your problem" ] + list( PROBLEM_REGISTRY.keys() )
    current_problem = st.session_state.get( "problem_key" )
    problem_index = problem_options.index( current_problem ) if current_problem in problem_options else 0

    selected_problem = st.selectbox(
        "Problem",
        options=problem_options,
        index=problem_index,
        format_func=lambda k: "Chose your problem" if k == "Chose your problem" else PROBLEM_REGISTRY[ k ].label,
        label_visibility="collapsed"
    )
    st.session_state.problem_key = None if selected_problem == "Chose your problem" else selected_problem

    # ── Validate button ───────────────────────────────
    st.markdown( "" )
    can_validate = ( st.session_state.get( "problem_key" ) )
    if st.button( "✔  Valider la configuration", type="primary", use_container_width=True, disabled=not can_validate ):
        st.session_state.config_validated = True
        st.session_state.step = 1
        st.session_state.journey[ "Problem type" ] = st.session_state.problem_key
        st.rerun()

    if not can_validate:
        st.markdown(
            '<p class="ui-hint">→ Analysez d\'abord votre problème dans la zone centrale.</p>',
            unsafe_allow_html=True
        )


# ── Guide panel — shown after validation ────────────────────────────────────


def _render_guide_panel():
    # Guard: if required keys were lost (hot reload, session reset), fall back to config panel
    if not st.session_state.get( "problem_key" ):
        st.session_state.config_validated = False
        st.rerun()
        return

    # Configuration summary
    theme.section_label( "Configuration active" )

    problem_label = PROBLEM_REGISTRY[ st.session_state.problem_key ].label

    st.markdown( f"**{problem_label}**" )

    st.markdown( "" )
    if st.button( "✏  Modifier", use_container_width=True ):
        for k in [ "config_validated", "step", "solution", "ai_summary", "solve_error" ]:
            st.session_state.pop( k, None )
        st.rerun()

    theme.divider()

    # AI guide
    theme.section_label( "Guide IA" )
    if st.session_state.get( "onboarding_result" ):
        theme.ai_block( st.session_state.onboarding_result )
    elif st.session_state.get( "llm_model_name" ):
        st.markdown(
            '<p class="ui-hint">Décrivez votre problème sur la page d\'accueil '
            'pour obtenir un guide personnalisé.</p>',
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            '<p class="ui-hint">Sélectionnez un modèle IA pour activer le guide.</p>',
            unsafe_allow_html=True,
        )

    theme.divider()

    # Compact journal
    theme.section_label( "Journal" )
    entries = st.session_state.get( "journey", {} )
    if entries:
        for entry, value in entries.items():
            st.markdown(
                f'<div class="ui-journal">· { entry }: { value }</div>',
                unsafe_allow_html=True,
            )
    else:
        st.markdown(
            '<p class="ui-hint">Aucune action enregistrée.</p>',
            unsafe_allow_html=True,
        )

    st.markdown( "" )
    if st.button( "↺  Réinitialiser", use_container_width=True ):
        st.session_state.clear()
        st.rerun()


# ── Public entry point ───────────────────────────────────────────────────────
def render():
    with st.sidebar:
        _render_model_picker()
        theme.divider()

        if st.session_state.get( "config_validated" ):
            _render_guide_panel()
        else:
            _render_config_panel()
