# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025-2026 AKKODIS.
# SPDX-FileContributor: Romain Baville

import os
import streamlit as st

from ui.utils import (
    navigation_buttons,
    generate_ai_summary,
    log_step,
    describe_data_source,
    build_results_zip,
)
from infrastructure.registry import DATA_SOURCE_REGISTRY
from solvers.registry import SOLVER_REGISTRY
from ui.problems.assignment.skills.builder import build_problem
from domain.entity_registry import check_unique_identifiers
from llm.session_model import OptimizationSession

DATA_DIR = "data"


def render(step: int):


    # ==================================================
    # STEP 4 — Naming
    # ==================================================
    if step == 4:
        st.header("Define entities and skills")

        st.session_state.left_label = st.text_input(
            "Left entities (e.g. Employees)",
            st.session_state.get("left_label", "Employees"),
        )
        st.session_state.right_label = st.text_input(
            "Right entities (e.g. Projects)",
            st.session_state.get("right_label", "Projects"),
        )
        st.session_state.skill_label = st.text_input(
            "Skill label",
            st.session_state.get("skill_label", "Skills"),
        )

        log_step(
            f"Defined left entities as '{st.session_state.left_label}', "
            f"right entities as '{st.session_state.right_label}', "
            f"and skills as '{st.session_state.skill_label}'."
        )

        navigation_buttons()
        st.stop()

    # ==================================================
    # STEP 5 — CSV selection
    # ==================================================
    if step == 5:
        csv_files = sorted(
            f for f in os.listdir(DATA_DIR) if f.endswith(".csv")
        )

        st.session_state.left_csv = st.selectbox(
            f"{st.session_state.left_label} CSV",
            csv_files,
        )
        st.session_state.right_csv = st.selectbox(
            f"{st.session_state.right_label} CSV",
            csv_files,
        )

        log_step(
            f"Selected data source "
            f"{describe_data_source(st.session_state.data_source)} "
            f"with files '{st.session_state.left_csv}' and "
            f"'{st.session_state.right_csv}'."
        )

        navigation_buttons()
        st.stop()

    # ==================================================
    # STEP 6 — Schema mapping + validation
    # ==================================================
    if step == 6:
        loader = DATA_SOURCE_REGISTRY[
            st.session_state.data_source
        ].loader_factory()

        left_cols, left_rows = loader.load(
            os.path.join(DATA_DIR, st.session_state.left_csv)
        )
        right_cols, _ = loader.load(
            os.path.join(DATA_DIR, st.session_state.right_csv)
        )

        st.session_state.left_id_cols = st.multiselect(
            "Columns that uniquely identify left entity",
            left_cols,
            default=st.session_state.get("left_id_cols", left_cols[:1]),
        )

        st.session_state.skill_cols = st.multiselect(
            f"{st.session_state.skill_label} columns",
            [c for c in left_cols if c not in st.session_state.left_id_cols],
        )

        st.session_state.right_id_col = st.selectbox(
            "Right entity identifier column",
            right_cols,
        )

        duplicates = check_unique_identifiers(
            left_rows,
            st.session_state.left_id_cols,
        )

        if duplicates:
            st.error(
                "Identifiers are not unique:\n"
                + "\n".join(f"- {d}" for d in duplicates)
            )
            navigation_buttons(show_next=False)
            st.stop()

        log_step(
            f"Mapped identifiers with columns "
            f"{', '.join(st.session_state.left_id_cols)} "
            f"and selected skills {', '.join(st.session_state.skill_cols)}."
        )

        navigation_buttons()
        st.stop()

    # ==================================================
    # STEP 7 — Solve
    # ==================================================
    if step == 7:
        loader = DATA_SOURCE_REGISTRY[
            st.session_state.data_source
        ].loader_factory()

        _, left_rows = loader.load(
            os.path.join(DATA_DIR, st.session_state.left_csv)
        )
        _, right_rows = loader.load(
            os.path.join(DATA_DIR, st.session_state.right_csv)
        )

        problem, left_labels = build_problem(
            st.session_state,
            left_rows,
            right_rows,
        )

        solver_def = SOLVER_REGISTRY["assignment"]["skills_coverage"]["ortools"]
        solver = solver_def.solver_class()

        with st.spinner("Solving optimization problem..."):
            solution = solver.solve(problem)

        st.session_state.solution = solution
        st.session_state.left_labels = left_labels
        st.session_state.solver_label = solver_def.label

        st.session_state.solution_rows = [
            {
                st.session_state.left_label: left_labels[left_id],
                st.session_state.right_label: right_id,
            }
            for left_id, right_id in solution.items()
        ]

        log_step(f"Ran solver '{solver_def.label}' to compute the solution.")

        st.success("Solution found")
        st.table(st.session_state.solution_rows)

    # ==================================================
    # STEP 7 bis — AI summary & download
    # ==================================================
        st.header("AI-generated explanation")

        if st.button("Generate AI summary"):
            with st.spinner("Generating explanation..."):

                session = OptimizationSession(
                    problem_family="Assignment",
                    problem_variant="Skill-based assignment",
                    steps=st.session_state.journey,
                    data_description=(
                        f"Data provided via "
                        f"{describe_data_source(st.session_state.data_source)} "
                        f"using files '{st.session_state.left_csv}' and "
                        f"'{st.session_state.right_csv}'."
                    ),
                    solver_name=st.session_state.solver_label,
                    solver_type="Constraint Programming",
                    result_summary=(
                        f"{len(st.session_state.solution)} "
                        f"{st.session_state.left_label.lower()} "
                        f"assigned to "
                        f"{st.session_state.right_label.lower()}."
                    ),
                    result_details={
                        "Skills considered": ", ".join(st.session_state.skill_cols),
                    },
                )

                ai_summary = generate_ai_summary(session)
                st.session_state.ai_summary = ai_summary

            st.markdown(ai_summary)

        if "ai_summary" in st.session_state:
            zip_bytes = build_results_zip(
                solution_rows=st.session_state.solution_rows,
                ai_summary=st.session_state.ai_summary,
                metadata={
                    "problem_family": "Assignment",
                    "problem_variant": "Skill-based assignment",
                    "solver": st.session_state.solver_label,
                    "data_source": st.session_state.data_source,
                },
            )

            st.download_button(
                label="📥 Download results (ZIP)",
                data=zip_bytes,
                file_name="optimization_results.zip",
                mime="application/zip",
            )

        navigation_buttons(show_next=False)
        st.stop()
