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
from llm.registry import CLIENTS
from ui.registry import PROBLEM_REGISTRY
from ui.sidebar import render as render_sidebar

# ── Page setup ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Optimization Playground",
    page_icon="⚙️",
    layout="wide",
)
theme.inject()

# ── Session defaults ─────────────────────────────────────────────────────────
st.session_state.setdefault( "config_validated", False )
st.session_state.setdefault( "step", 0 )
st.session_state.setdefault( "ai_summary", None )
st.session_state.setdefault( "journey", {} )
st.session_state.setdefault( "onboarding_result", None )
st.session_state.setdefault( "solve_error", None )
st.session_state.setdefault( "analysis_done", False )
st.session_state.setdefault( "analysis_recommendation", None )
st.session_state.setdefault( "problem_key", None )

# ── Sidebar + top bar ────────────────────────────────────────────────────────
render_sidebar()
theme.render_topbar( st.session_state.get( "llm_model_label" ) )


# ── Problem configuration inference ─────────────────────────────────────────
def infer_problem_configuration( user_desc: str, ai_text: str | None = None ) -> dict:
    """Deterministic keyword-based recommendation — no extra LLM call."""
    text = f"{ user_desc }\n{ ai_text or '' }".lower()

    assignment_keywords = [
        "assign",
        "affect",
        "affectation",
        "affecter",
        "assignment",
        "employee",
        "employé",
        "project",
        "projet",
        "skill",
        "compétence",
        "competence",
    ]
    if not any( w in text for w in assignment_keywords ):
        return {}

    problem_key = "assignment"

    return {
        "problem_key": problem_key
    }


# ── Main area renderers ───────────────────────────────────────────────────────
def _render_onboarding():
    theme.hero(
        "Optimization Playground",
        "Décrivez votre problème en langage naturel. L'IA configurera automatiquement la barre latérale.",
    )

    st.markdown( "### Analyser votre problème avec l'IA" )
    user_desc = st.text_area(
        "Description",
        height=110,
        placeholder=( "Exemple : Je veux affecter des employés à des projets "
                      "en fonction de leurs compétences…" ),
        label_visibility="collapsed",
    )

    if st.button( "Analyser", type="primary" ):
        if not user_desc.strip():
            st.warning( "Saisissez une description avant d'analyser." )
        elif not st.session_state.get( "llm_model_name" ):
            st.warning( "Sélectionnez un modèle IA dans la barre latérale." )
        else:
            try:
                with st.spinner( "Analyse en cours…" ):
                    prompt: str = build_onboarding_prompt( user_desc )
                    result = CLIENTS[ st.session_state.llm_source ].ask_fn( prompt, st.session_state.llm_model_name )

                st.session_state.onboarding_result = result
                st.session_state.analysis_done = True

                # Infer and immediately apply configuration recommendation
                rec = infer_problem_configuration( user_desc, result )
                st.session_state.analysis_recommendation = rec
                if rec:
                    st.session_state[ "problem_key" ] = rec[ "problem_key" ]

                # Reset any prior validation so user re-confirms the new config
                st.session_state.config_validated = False
                st.session_state.data_step = 1
                st.session_state.solution = None
                st.session_state.ai_summary = None

                st.rerun()

            except Exception as exc:
                st.error( f"Erreur lors de l'appel au modèle IA : {exc}" )

    if st.session_state.get( "onboarding_result" ):
        st.markdown( "**Guidage IA**" )
        theme.ai_block( st.session_state.onboarding_result )
        st.markdown( "" )
        st.markdown(
            '<p class="ui-hint">✓ Configuration proposée dans la barre latérale. '
            'Vous pouvez la modifier, puis cliquer sur '
            '<strong>Valider la configuration</strong>.</p>',
            unsafe_allow_html=True,
        )
    else:
        st.markdown( "" )
        st.markdown(
            '<p class="ui-hint">→ Décrivez votre problème ci-dessus. '
            'L\'IA proposera automatiquement une configuration dans la barre latérale.</p>',
            unsafe_allow_html=True,
        )


def _render_data_workflow():
    theme.hero( "Saisie des données" )
    if st.session_state.problem_key in PROBLEM_REGISTRY:
        PROBLEM_REGISTRY[ st.session_state.problem_key ].render_fn( st.session_state )


# ── Main routing ──────────────────────────────────────────────────────────────
if not st.session_state.get( "config_validated" ):
    _render_onboarding()
else:
    _render_data_workflow()
