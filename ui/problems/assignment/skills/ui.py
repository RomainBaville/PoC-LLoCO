# SPDX-License-Identifier: Apache-2.0
import os
import streamlit as st

from infrastructure.csv_loader import CSVLoader
from solvers.registry import SOLVER_REGISTRY
from ui.utils import navigation_buttons
from ui.problems.assignment.skills.builder import build_problem

DATA_DIR = "data"
loader = CSVLoader()


def render(step: int):

    # --------------------------------------------
    # STEP 2 — Naming
    # --------------------------------------------
    if step == 2:
        st.header("Define entities and skills")

        st.session_state.left_label = st.text_input("Left entities", "Employees")
        st.session_state.right_label = st.text_input("Right entities", "Projects")
        st.session_state.skill_label = st.text_input("Skill label", "Skills")

        navigation_buttons()
        st.stop()

    # --------------------------------------------
    # STEP 3 — CSV selection
    # --------------------------------------------
    if step == 3:
        csv_files = [f for f in os.listdir(DATA_DIR) if f.endswith(".csv")]

        st.session_state.left_csv = st.selectbox(
            f"{st.session_state.left_label} CSV",
            csv_files,
        )
        st.session_state.right_csv = st.selectbox(
            f"{st.session_state.right_label} CSV",
            csv_files,
        )

        navigation_buttons()
        st.stop()

    # --------------------------------------------
    # STEP 4 — Schema mapping
    # --------------------------------------------
    if step == 4:
        left_cols, _ = loader.load(os.path.join(DATA_DIR, st.session_state.left_csv))
        right_cols, _ = loader.load(os.path.join(DATA_DIR, st.session_state.right_csv))

        st.session_state.left_id_cols = st.multiselect(
            "Left identifier columns",
            left_cols,
            default=left_cols[:1],
        )

        st.session_state.skill_cols = st.multiselect(
            "Skill columns",
            [c for c in left_cols if c not in st.session_state.left_id_cols],
        )

        st.session_state.right_id_col = st.selectbox(
            "Right identifier column",
            right_cols,
        )

        navigation_buttons()
        st.stop()

    # --------------------------------------------
    # STEP 5 — Solve
    # --------------------------------------------
    if step == 5:
        _, left_rows = loader.load(os.path.join(DATA_DIR, st.session_state.left_csv))
        _, right_rows = loader.load(os.path.join(DATA_DIR, st.session_state.right_csv))

        problem = build_problem(st.session_state, left_rows, right_rows)

        solver = SOLVER_REGISTRY["assignment"]["skills"]["ortools"].solver_class()
        solution = solver.solve(problem)

        st.success("Solution found")
        st.table([
            {
                st.session_state.left_label: l,
                st.session_state.right_label: r,
            }
            for l, r in solution.items()
        ])

        navigation_buttons(show_next=False)
        st.stop()
