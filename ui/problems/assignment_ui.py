# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025-2026 AKKODIS.
# SPDX-FileContributor: Romain Baville

import os
import streamlit as st

from infrastructure.csv_loader import CSVLoader
from domain.assignment_structure import AssignmentStructure
from solvers.registry import SOLVER_REGISTRY
from ui.utils import navigation_buttons
from llm.summary import build_summary_prompt
from llm.client import ask_llm_request

DATA_DIR = "data"

# --------------------------------------------------
# Data loader (infrastructure)
# --------------------------------------------------
loader = CSVLoader()


def render_assignment_step(step: int):

    # --------------------------------------------------
    # STEP 1 — Naming
    # --------------------------------------------------
    if step == 1:
        st.header("1. Define what you want to associate")

        st.session_state.left_label = st.text_input(
            "Left entity label",
            value=st.session_state.get("left_label", "Employees"),
        )
        st.session_state.right_label = st.text_input(
            "Right entity label",
            value=st.session_state.get("right_label", "Projects"),
        )
        st.session_state.attribute_label = st.text_input(
            "Attribute label",
            value=st.session_state.get("attribute_label", "Skills"),
        )

        navigation_buttons()
        st.stop()

    # --------------------------------------------------
    # STEP 2 — CSV selection
    # --------------------------------------------------
    if step == 2:
        st.header("2. Select data files")

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

    # --------------------------------------------------
    # STEP 3 — Schema mapping
    # --------------------------------------------------
    if step == 3:
        st.header("3. Define data schemas")

        left_cols, _ = loader.load(os.path.join(DATA_DIR, st.session_state.left_csv))
        right_cols, _ = loader.load(os.path.join(DATA_DIR, st.session_state.right_csv))

        st.session_state.left_id_cols = st.multiselect(
            "Left identifiers",
            left_cols,
            default=left_cols[:1],
        )

        st.session_state.attribute_cols = st.multiselect(
            f"{st.session_state.attribute_label} columns",
            [c for c in left_cols if c not in st.session_state.left_id_cols],
        )

        st.session_state.right_id_col = st.selectbox(
            "Right identifier column",
            right_cols,
        )

        navigation_buttons()
        st.stop()

    # --------------------------------------------------
    # STEP 4 — Solver selection
    # --------------------------------------------------
    if step == 4:
        st.header("4. Choose a solver")

        solver_defs = SOLVER_REGISTRY["assignment"]

        st.session_state.solver_key = st.selectbox(
            "Solver",
            list(solver_defs.keys()),
            format_func=lambda k: solver_defs[k].label,
        )

        solver_info = solver_defs[st.session_state.solver_key]
        st.info(f"Selected solver: **{solver_info.label}**")

        navigation_buttons()
        st.stop()

    # --------------------------------------------------
    # STEP 5 — Solve & results
    # --------------------------------------------------
    if step == 5:
        st.header("5. Solve and view results")

        SolverClass = SOLVER_REGISTRY["assignment"][
            st.session_state.solver_key
        ].solver_class

        # ----------------------------
        # Load & normalize data
        # ----------------------------
        _, left_rows = loader.load(os.path.join(DATA_DIR, st.session_state.left_csv))
        _, right_rows = loader.load(os.path.join(DATA_DIR, st.session_state.right_csv))

        left_entities = []
        right_entities = []
        left_attributes = {}
        right_requirements = {}

        for row in left_rows:
            l = " ".join(row[c] for c in st.session_state.left_id_cols)
            left_entities.append(l)
            for a in st.session_state.attribute_cols:
                left_attributes[(l, a)] = int(row.get(a, 0))

        for row in right_rows:
            r = row[st.session_state.right_id_col]
            right_entities.append(r)
            for a in st.session_state.attribute_cols:
                right_requirements[(r, a)] = int(row.get(a, 0))

        structure = AssignmentStructure(
            left_entities=left_entities,
            right_entities=right_entities,
            attributes=st.session_state.attribute_cols,
            left_attributes=left_attributes,
            right_requirements=right_requirements,
        )

        solver = SolverClass()

        with st.spinner("Solving optimization problem..."):
            solution = solver.solve(structure)

        st.success("Solution found")

        st.table([
            {
                st.session_state.left_label: l,
                st.session_state.right_label: r,
            }
            for l, r in solution.items()
        ])

        # ----------------------------
        # AI summary
        # ----------------------------
        st.divider()
        if st.button("Generate AI summary"):
            prompt = build_summary_prompt(
                left_entity_name=st.session_state.left_label,
                right_entity_name=st.session_state.right_label,
                assignments=solution,
                skills=st.session_state.attribute_cols,
            )
            st.markdown(ask_llm_request(prompt))

        navigation_buttons(show_next=False)
        st.stop()
