# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025-2026 AKKODIS.

import streamlit as st


def render_results(solution: dict, state) -> None:
    left_lbl = state.left_label
    right_lbl = state.right_label

    st.markdown("### Résultats — Meilleure correspondance")
    st.caption(
        f"Chaque {left_lbl.lower()} est apparié au {right_lbl.lower()} "
        "maximisant la compatibilité globale de compétences."
    )
    st.dataframe(
        state.solution_rows,
        use_container_width=True,
        hide_index=True,
    )
