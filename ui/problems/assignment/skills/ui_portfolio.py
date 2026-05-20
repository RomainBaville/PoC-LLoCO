# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025-2026 AKKODIS.

import streamlit as st


def render_results(solution: dict, state) -> None:
    left_lbl = state.left_label

    st.markdown("### Résultats — Sélection de portfolio")
    st.caption(
        f"Sous-ensemble de {left_lbl.lower()} dont les compétences combinées "
        "couvrent l'ensemble des compétences requises."
    )
    st.dataframe(
        state.solution_rows,
        use_container_width=True,
        hide_index=True,
    )

    skills = state.get("skill_cols") or []
    if skills:
        st.markdown("**Compétences couvertes**")
        st.markdown("  ".join(f"`{s}`" for s in skills))
