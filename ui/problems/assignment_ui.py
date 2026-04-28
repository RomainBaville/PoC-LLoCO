# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025-2026 AKKODIS.
# SPDX-FileContributor: Romain Baville
import os
import streamlit as st

from infrastructure.generic_csv import load_csv
from domain.assignment_problem import AssignmentProblem
from solvers.assignment_ortools import ORToolsAssignmentSolver

from ui.utils import navigation_buttons
from llm.summary import build_summary_prompt
from llm.client import ask_llm_request


DATA_DIR = "data"


def render_assignment_step(step: int):
    """
    Render the Assignment problem UI for the given step.
    Steps handled here: 1 -> 4
    """

    # ==================================================
    # STEP 1 – Name the entities
    # ==================================================
    if step == 1:
        st.header("1. Define what you want to associate")

        st.session_state.left_entity = st.text_input(
            "Left entity name",
            value=st.session_state.get("left_entity", "Employees"),
        )

        st.session_state.right_entity = st.text_input(
            "Right entity name",
            value=st.session_state.get("right_entity", "Projects"),
        )

        navigation_buttons()
        st.stop()

    # ==================================================
    # STEP 2 – Select CSV files (from disk)
    # ==================================================
    if step == 2:
        st.header("2. Select data files")

        if not os.path.exists(DATA_DIR):
            st.error(f"Data directory '{DATA_DIR}' does not exist.")
            st.stop()

        csv_files = [f for f in os.listdir(DATA_DIR) if f.endswith(".csv")]

        if not csv_files:
            st.error(f"No CSV files found in '{DATA_DIR}'.")
            st.stop()

        st.session_state.left_csv = st.selectbox(
            f"{st.session_state.left_entity} CSV file",
            csv_files,
            index=0,
        )

        st.session_state.right_csv = st.selectbox(
            f"{st.session_state.right_entity} CSV file",
            csv_files,
            index=1 if len(csv_files) > 1 else 0,
        )

        navigation_buttons()
        st.stop()

    # ==================================================
    # STEP 3 – Define schemas
    # ==================================================
    if step == 3:
        st.header("3. Define data schemas")

        left_path = os.path.join(DATA_DIR, st.session_state.left_csv)
        right_path = os.path.join(DATA_DIR, st.session_state.right_csv)

        left_columns, left_rows = load_csv(left_path)
        right_columns, right_rows = load_csv(right_path)

        st.subheader(f"{st.session_state.left_entity} schema")

        st.session_state.left_id_cols = st.multiselect(
            "Identifier columns",
            left_columns,
            default=st.session_state.get("left_id_cols", left_columns[:1]),
        )

        st.session_state.left_skill_cols = st.multiselect(
            "Skill columns",
            [c for c in left_columns if c not in st.session_state.left_id_cols],
            default=st.session_state.get("left_skill_cols", []),
        )

        st.subheader(f"{st.session_state.right_entity} schema")

        st.session_state.right_id_col = st.selectbox(
            "Identifier column",
            right_columns,
            index=right_columns.index(
                st.session_state.get("right_id_col", right_columns[0])
            ),
        )

        navigation_buttons()
        st.stop()

    # ==================================================
    # STEP 4 – Solve & results
    # ==================================================
    if step == 4:
        st.header("4. Solve assignment")

        left_path = os.path.join(DATA_DIR, st.session_state.left_csv)
        right_path = os.path.join(DATA_DIR, st.session_state.right_csv)

        left_columns, left_rows = load_csv(left_path)
        right_columns, right_rows = load_csv(right_path)

        # Normalize left entities
        left_entities = []
        skill_matrix = {}

        for row in left_rows:
            entity = " ".join(row[c] for c in st.session_state.left_id_cols)
            left_entities.append(entity)

            for skill in st.session_state.left_skill_cols:
                skill_matrix[(entity, skill)] = int(row[skill])

        # Normalize right entities
        right_entities = []
        requirements = {}

        for row in right_rows:
            entity = row[st.session_state.right_id_col]
            right_entities.append(entity)

            for skill in st.session_state.left_skill_cols:
                requirements[(entity, skill)] = int(row.get(skill, 0))

        problem = AssignmentProblem(
            employees=left_entities,
            projects=right_entities,
            skills=st.session_state.left_skill_cols,
            skill_matrix=skill_matrix,
            requirements=requirements,
        )

        solver = ORToolsAssignmentSolver()

        with st.spinner("Solving optimization problem..."):
            problem.validate()
            solution = solver.solve(problem)

        st.success("Solution found")

        result = []
        for left, right in solution.items():
            result.append(
                {
                    st.session_state.left_entity: left,
                    st.session_state.right_entity: right,
                }
            )

        st.table(result)

        # -------------------------------
        # AI summary
        # -------------------------------
        st.divider()
        st.subheader("AI summary")

        if st.button("🤖 Generate AI summary"):
            with st.spinner("Generating summary..."):
                prompt = build_summary_prompt(
                    left_entity_name=st.session_state.left_entity,
                    right_entity_name=st.session_state.right_entity,
                    assignments=solution,
                    skills=st.session_state.left_skill_cols,
                )

                summary = ask_llm_request(prompt)

            st.markdown(summary)

        navigation_buttons( show_next=False )
        st.stop()
