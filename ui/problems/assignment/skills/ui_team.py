# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025-2026 AKKODIS.

import streamlit as st


def render_results(solution: dict, state) -> None:
    left_lbl = state.left_label
    right_lbl = state.right_label

    st.markdown("### Résultats — Formation d'équipes")
    st.caption(
        f"Les {left_lbl.lower()} sont regroupés par {right_lbl.lower()} "
        "de façon à couvrir collectivement les compétences requises."
    )

    # Group members by team
    teams: dict[str, list[str]] = {}
    for row in state.solution_rows:
        team = row[right_lbl]
        teams.setdefault(team, []).append(row[left_lbl])

    for team_name, members in sorted(teams.items()):
        with st.expander(
            f"**{team_name}** — {len(members)} membre(s)",
            expanded=True,
        ):
            for member in members:
                st.markdown(f"- {member}")
