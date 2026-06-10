# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025-2026 AKKODIS.

from importlib import import_module

import streamlit as st

import ui.theme as theme
from ui.registry import PROBLEM_REGISTRY
from ui.problems.assignment.registry import ASSIGNMENT_TYPES
from ui.model_picker import discover as discover_models


# ── Model picker (always at top) ────────────────────────────────────────────

def _render_model_picker():
    available_models = discover_models()
    model_options = {m.key: m for m in available_models}

    if available_models:
        selected_key = st.selectbox(
            "Modèle IA",
            options=["none"] + list(model_options.keys()),
            format_func=lambda k: "— Aucun —" if k == "none" else model_options[k].label,
            label_visibility="visible",
            key="llm_model_key",
        )
        if selected_key != "none":
            m = model_options[selected_key]
            st.session_state.llm_url = m.api_url
            st.session_state.llm_model_name = m.model_name
            st.session_state.llm_source = m.source
            active_label = m.label
        else:
            st.session_state.llm_url = None
            st.session_state.llm_model_name = None
            st.session_state.llm_source = None
            active_label = None
    else:
        st.session_state.llm_url = None
        st.session_state.llm_model_name = None
        active_label = None

    if active_label:
        st.markdown(
            f'<div class="ui-model-banner">'
            f'<span class="ui-model-banner-label">Modèle actif</span>'
            f'<span class="ui-model-banner-value">⬤ {active_label}</span>'
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
    st.markdown("## Configuration")

    theme.section_label("Problème")
    st.selectbox(
        "Problème",
        options=list(PROBLEM_REGISTRY.keys()),
        format_func=lambda k: PROBLEM_REGISTRY[k].label,
        label_visibility="collapsed",
        key="problem_key",
    )

    theme.section_label("Type & Formulation")
    assignment_type = st.selectbox(
        "Type",
        options=list(ASSIGNMENT_TYPES.keys()),
        format_func=lambda k: ASSIGNMENT_TYPES[k].label,
        label_visibility="collapsed",
        key="_ui_atype",
    )
    st.session_state.assignment_type = assignment_type

    atype_def = ASSIGNMENT_TYPES[assignment_type]
    variant_reg = import_module(atype_def.registry_module)
    variants = variant_reg.VARIANTS

    variant_local = st.selectbox(
        "Formulation",
        options=list(variants.keys()),
        format_func=lambda k: variants[k].label,
        label_visibility="collapsed",
        key="_ui_variant",
    )
    st.session_state.assignment_variant = f"{assignment_type}_{variant_local}"

    st.markdown("")
    if st.button("✔  Valider la configuration", type="primary", use_container_width=True):
        st.session_state.config_validated = True
        st.session_state.data_step = 1
        st.rerun()


# ── Guide panel — shown after validation ────────────────────────────────────

def _render_guide_panel():
    # Guard: if required keys were lost (hot reload, session reset), fall back to config panel
    if not st.session_state.get("problem_key") or not st.session_state.get("assignment_type") \
            or not st.session_state.get("assignment_variant"):
        st.session_state.config_validated = False
        st.rerun()
        return

    # Configuration summary
    theme.section_label("Configuration active")

    problem_label = PROBLEM_REGISTRY[st.session_state.problem_key].label
    atype_def = ASSIGNMENT_TYPES[st.session_state.assignment_type]
    _, variant_key = st.session_state.assignment_variant.split("_", 1)
    variant_reg = import_module(atype_def.registry_module)
    variant_label = variant_reg.VARIANTS[variant_key].label

    st.markdown(f"**{problem_label}**  \n{atype_def.label} · {variant_label}")

    st.markdown("")
    if st.button("✏  Modifier", use_container_width=True):
        for k in [
            "config_validated", "data_step",
            "solution", "ai_summary", "solve_error",
            "_prev_left_csv", "_prev_right_csv",
        ]:
            st.session_state.pop(k, None)
        st.rerun()

    theme.divider()

    # AI guide
    theme.section_label("Guide IA")
    if st.session_state.get("onboarding_result"):
        theme.ai_block(st.session_state.onboarding_result)
    elif st.session_state.get("llm_model_name"):
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
    theme.section_label("Journal")
    entries = st.session_state.get("journey", [])
    if entries:
        for entry in entries[-6:]:
            st.markdown(
                f'<div class="ui-journal">· {entry}</div>',
                unsafe_allow_html=True,
            )
    else:
        st.markdown(
            '<p class="ui-hint">Aucune action enregistrée.</p>',
            unsafe_allow_html=True,
        )

    st.markdown("")
    if st.button("↺  Réinitialiser", use_container_width=True):
        st.session_state.clear()
        st.rerun()


# ── Public entry point ───────────────────────────────────────────────────────

def render():
    with st.sidebar:
        _render_model_picker()
        theme.divider()

        if st.session_state.get("config_validated"):
            _render_guide_panel()
        else:
            _render_config_panel()
