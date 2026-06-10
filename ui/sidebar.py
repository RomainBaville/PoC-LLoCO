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

_PLACEHOLDER = "__placeholder__"
_PLACEHOLDER_PROBLEM = "Sélection automatique après analyse"
_PLACEHOLDER_TYPE = "—"
_PLACEHOLDER_VARIANT = "—"


def _render_config_panel():
    analysis_done = st.session_state.get("analysis_done", False)

    st.markdown("## Configuration")

    # ── Problème ─────────────────────────────────────
    theme.section_label("Problème")
    problem_options = [_PLACEHOLDER] + list(PROBLEM_REGISTRY.keys())
    current_problem = st.session_state.get("problem_key")
    problem_index = problem_options.index(current_problem) if current_problem in problem_options else 0

    selected_problem = st.selectbox(
        "Problème",
        options=problem_options,
        index=problem_index,
        format_func=lambda k: _PLACEHOLDER_PROBLEM if k == _PLACEHOLDER else PROBLEM_REGISTRY[k].label,
        label_visibility="collapsed",
        disabled=not analysis_done,
    )
    st.session_state.problem_key = None if selected_problem == _PLACEHOLDER else selected_problem

    # ── Type ──────────────────────────────────────────
    theme.section_label("Type & Formulation")
    type_options = [_PLACEHOLDER] + list(ASSIGNMENT_TYPES.keys())
    current_type = st.session_state.get("assignment_type")
    type_index = type_options.index(current_type) if current_type in type_options else 0

    selected_type = st.selectbox(
        "Type",
        options=type_options,
        index=type_index,
        format_func=lambda k: _PLACEHOLDER_TYPE if k == _PLACEHOLDER else ASSIGNMENT_TYPES[k].label,
        label_visibility="collapsed",
        disabled=not analysis_done,
    )
    assignment_type = None if selected_type == _PLACEHOLDER else selected_type
    st.session_state.assignment_type = assignment_type

    # ── Formulation ───────────────────────────────────
    if assignment_type:
        atype_def = ASSIGNMENT_TYPES[assignment_type]
        variant_reg = import_module(atype_def.registry_module)
        variants = variant_reg.VARIANTS

        variant_options = [_PLACEHOLDER] + list(variants.keys())
        current_variant_full = st.session_state.get("assignment_variant") or ""
        # Extract local key: "skills_coverage" → "coverage"
        current_variant_local = current_variant_full.split("_", 1)[1] if "_" in current_variant_full else None
        variant_index = variant_options.index(current_variant_local) if current_variant_local in variant_options else 0

        selected_variant = st.selectbox(
            "Formulation",
            options=variant_options,
            index=variant_index,
            format_func=lambda k: _PLACEHOLDER_VARIANT if k == _PLACEHOLDER else variants[k].label,
            label_visibility="collapsed",
            disabled=not analysis_done,
        )
        variant_local = None if selected_variant == _PLACEHOLDER else selected_variant
        st.session_state.assignment_variant = (
            f"{assignment_type}_{variant_local}" if variant_local else None
        )

        # Recommendation hint
        rec = st.session_state.get("analysis_recommendation")
        if rec and rec.get("variant_local") in variants:
            rec_label = variants[rec["variant_local"]].label
            st.markdown(
                f'<p class="ui-hint">💡 Recommandation IA : <strong>{rec_label}</strong></p>',
                unsafe_allow_html=True,
            )
    else:
        st.selectbox(
            "Formulation",
            options=[_PLACEHOLDER],
            format_func=lambda k: _PLACEHOLDER_VARIANT,
            label_visibility="collapsed",
            disabled=True,
        )
        st.session_state.assignment_variant = None

    # ── Validate button ───────────────────────────────
    st.markdown("")
    can_validate = (
        analysis_done
        and st.session_state.get("problem_key")
        and st.session_state.get("assignment_type")
        and st.session_state.get("assignment_variant")
    )
    if st.button(
        "✔  Valider la configuration",
        type="primary",
        use_container_width=True,
        disabled=not can_validate,
    ):
        st.session_state.config_validated = True
        st.session_state.data_step = 1
        st.rerun()

    if not can_validate:
        st.markdown(
            '<p class="ui-hint">→ Analysez d\'abord votre problème dans la zone centrale.</p>',
            unsafe_allow_html=True,
        )


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
