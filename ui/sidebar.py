# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025-2026 AKKODIS.

import os
from importlib import import_module

import streamlit as st

import ui.theme as theme
from ui.registry import PROBLEM_REGISTRY
from ui.problems.assignment.registry import ASSIGNMENT_TYPES
from infrastructure.registry import DATA_SOURCE_REGISTRY

_DATA_DIR = "data"
_LOADER_KEY = "csv_two_tables"


# ── Helpers ────────────────────────────────────────────────────────────────

def _csv_files():
    if not os.path.isdir(_DATA_DIR):
        return []
    return sorted(f for f in os.listdir(_DATA_DIR) if f.endswith(".csv"))


def _load_columns(csv_file: str):
    loader = DATA_SOURCE_REGISTRY[_LOADER_KEY].loader_factory()
    cols, _ = loader.load(os.path.join(_DATA_DIR, csv_file))
    return cols


def _data_ready() -> bool:
    return bool(
        st.session_state.get("left_id_cols")
        and st.session_state.get("skill_cols")
        and st.session_state.get("right_id_col")
    )


def _sanitize_multiselect(key: str, valid_pool: list):
    """Remove stale values from a multiselect key before rendering."""
    stored = st.session_state.get(key, [])
    valid = [c for c in stored if c in valid_pool]
    if stored != valid:
        st.session_state[key] = valid


def _sanitize_selectbox(key: str, valid_pool: list):
    """Clear a selectbox key if its stored value is no longer in the options."""
    if key in st.session_state and st.session_state[key] not in valid_pool:
        del st.session_state[key]


# ── Public entry point ─────────────────────────────────────────────────────

def render() -> bool:
    """
    Render the full sidebar configuration.
    Returns True when the user clicks the Résoudre button.
    """
    with st.sidebar:
        st.markdown("## Configuration")

        # ── Problem ───────────────────────────────────────────────
        theme.section_label("Problème")
        problem_key = st.selectbox(
            "Problème",
            options=list(PROBLEM_REGISTRY.keys()),
            format_func=lambda k: PROBLEM_REGISTRY[k].label,
            label_visibility="collapsed",
            key="problem_key",
        )

        # ── Type & Formulation ────────────────────────────────────
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
        full_variant = f"{assignment_type}_{variant_local}"
        st.session_state.assignment_variant = full_variant

        # ── Données ───────────────────────────────────────────────
        theme.divider()
        theme.section_label("Données")

        csv_files = _csv_files()
        if not csv_files:
            st.warning("Aucun fichier CSV trouvé dans `data/`.")
            return False

        col_a, col_b = st.columns(2)
        with col_a:
            st.text_input("Entités", value="Personnes", key="left_label")
        with col_b:
            st.text_input("Cibles", value="Projets", key="right_label")

        left_csv = st.selectbox(
            f"CSV · {st.session_state.left_label}",
            csv_files,
            key="left_csv",
        )
        right_csv = st.selectbox(
            f"CSV · {st.session_state.right_label}",
            csv_files,
            key="right_csv",
        )

        left_cols = _load_columns(left_csv)
        right_cols = _load_columns(right_csv)

        # Validate stored selections against current column lists
        _sanitize_multiselect("left_id_cols", left_cols)
        left_id_cols = st.multiselect(
            f"Colonnes ID · {st.session_state.left_label}",
            left_cols,
            key="left_id_cols",
        )

        remaining = [c for c in left_cols if c not in left_id_cols]
        _sanitize_multiselect("skill_cols", remaining)
        st.multiselect(
            "Colonnes compétences",
            remaining,
            key="skill_cols",
        )

        _sanitize_selectbox("right_id_col", right_cols)
        st.selectbox(
            f"Colonne ID · {st.session_state.right_label}",
            right_cols,
            key="right_id_col",
        )

        # ── Solveur ───────────────────────────────────────────────
        if not _data_ready():
            theme.divider()
            st.markdown(
                '<p class="ui-hint">Configurez les colonnes pour accéder au solver.</p>',
                unsafe_allow_html=True,
            )
            return False

        theme.divider()
        theme.section_label("Solveur")

        from solvers.assignment.registry import ASSIGNMENT_SOLVER_GROUPS
        solver_group = ASSIGNMENT_SOLVER_GROUPS.get(assignment_type)
        if not solver_group:
            st.error("Aucun groupe de solvers disponible.")
            return False

        solver_reg = import_module(solver_group.registry_module)
        compatible = {
            k: s
            for k, s in solver_reg.SOLVERS.items()
            if full_variant in s.supported_variants
        }
        if not compatible:
            st.error("Aucun solver compatible avec cette formulation.")
            return False

        st.selectbox(
            "Solveur",
            options=list(compatible.keys()),
            format_func=lambda k: compatible[k].label,
            label_visibility="collapsed",
            key="solver_key",
        )

        st.markdown("")
        solve_clicked = st.button(
            "▶  Résoudre",
            type="primary",
            use_container_width=True,
        )

        # ── Journal ───────────────────────────────────────────────
        theme.divider()
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

        return solve_clicked
