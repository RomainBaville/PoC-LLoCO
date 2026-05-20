# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025-2026 AKKODIS.

import streamlit as st


def render_results(solution: dict, state) -> None:
    left_lbl = state.left_label
    right_lbl = state.right_label

    st.markdown("### Résultats — Couverture de compétences")
    st.caption(
        f"Chaque {left_lbl.lower()} est affecté au {right_lbl.lower()} "
        "dont il couvre le mieux les compétences requises."
    )
    st.dataframe(
        state.solution_rows,
        use_container_width=True,
        hide_index=True,
    )
