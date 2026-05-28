# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025-2026 AKKODIS.
# SPDX-FileContributor: Romain Baville

import os
import streamlit as st
from importlib import import_module

from ui.utils import (
    navigation_buttons,
    generate_ai_summary,
    log_step,
    describe_data_source,
    build_results_zip,
)
from infrastructure.registry import DATA_SOURCE_REGISTRY
from ui.problems.assignment.skills.builder import build_problem
from llm.session_model import OptimizationSession
from solvers.assignment.registry import ASSIGNMENT_SOLVER_GROUPS

DATA_DIR = "data"


def render(step: int):

    # --------------------------------------------------
    # Defensive defaults
    # --------------------------------------------------
    st.session_state.setdefault("left_label", "Candidates")
    st.session_state.setdefault("right_label", "Targets")
    st.session_state.setdefault("skill_label", "Skills")

    # ==================================================
    # STEP 4 — Naming
    # ==================================================
    if step == 4:
        st.header("Define entities and skills")

        st.session_state.left_label = st.text_input(
            "Left entities (e.g. Employees)", st.session_state.left_label
        )
        st.session_state.right_label = st.text_input(
            "Right entities (e.g. Projects)", st.session_state.right_label
        )
        st.session_state.skill_label = st.text_input(
            "Skill label", st.session_state.skill_label
        )

        log_step(
            f"Configured best-fit assignment between "
            f"'{st.session_state.left_label}' and "
            f"'{st.session_state.right_label}' based on skill matching."
        )

        navigation_buttons()
        st.stop()

    # ==================================================
    # STEP 5 — CSV selection
    # ==================================================
    if step == 5:
        csv_files = sorted(f for f in os.listdir(DATA_DIR) if f.endswith(".csv"))

        st.session_state.left_csv = st.selectbox(
            f"{st.session_state.left_label} CSV", csv_files
        )
        st.session_state.right_csv = st.selectbox(
            f"{st.session_state.right_label} CSV", csv_files
        )

        log_step(
            f"Selected CSV files '{st.session_state.left_csv}' "
            f"and '{st.session_state.right_csv}'."
        )

        navigation_buttons()
        st.stop()

    # ==================================================
    # STEP 6 — Schema mapping
    # ==================================================
    if step == 6:
        loader = DATA_SOURCE_REGISTRY[st.session_state.data_source].loader_factory()

        left_cols, _ = loader.load(os.path.join(DATA_DIR, st.session_state.left_csv))
        right_cols, _ = loader.load(os.path.join(DATA_DIR, st.session_state.right_csv))

        st.session_state.left_id_cols = st.multiselect(
            "Left identifier columns", left_cols
        )
        st.session_state.skill_cols = st.multiselect(
            "Skill columns",
            [c for c in left_cols if c not in st.session_state.left_id_cols],
        )
        st.session_state.right_id_col = st.selectbox(
            "Right identifier column", right_cols
        )

        navigation_buttons()
        st.stop()

    # ==================================================
    # STEP 7 — Solver selection
    # ==================================================
    if step == 7:
        st.header("Choose solver")

        assignment_type, _ = st.session_state.assignment_variant.split("_", 1)
        solver_group = ASSIGNMENT_SOLVER_GROUPS[assignment_type]
        solver_registry = import_module(solver_group.registry_module)

        compatible_solvers = {
            k: s
            for k, s in solver_registry.SOLVERS.items()
            if st.session_state.assignment_variant in s.supported_variants
        }

        for key, solver in compatible_solvers.items():
            if st.button(solver.label):
                st.session_state.solver_key = key
                st.session_state.step += 1

            st.caption(solver.description)

        navigation_buttons(show_next=False)
        st.stop()

    # ==================================================
    # STEP 8 — Solve
    # ==================================================
    if step == 8:
        loader = DATA_SOURCE_REGISTRY[st.session_state.data_source].loader_factory()
        _, left_rows = loader.load(os.path.join(DATA_DIR, st.session_state.left_csv))
        _, right_rows = loader.load(os.path.join(DATA_DIR, st.session_state.right_csv))

        if "solution" not in st.session_state:

            problem, left_labels = build_problem(
                st.session_state, left_rows, right_rows
            )

            assignment_type, _ = st.session_state.assignment_variant.split("_", 1)
            solver_group = ASSIGNMENT_SOLVER_GROUPS[assignment_type]
            solver_registry = import_module(solver_group.registry_module)

            solver_def = solver_registry.SOLVERS[st.session_state.solver_key]
            solver = solver_def.solver_class()

            with st.spinner("Optimizing best-fit matching..."):
                solution = solver.solve(problem)

            st.session_state.solution = solution
            st.session_state.left_labels = left_labels

            st.session_state.solution_rows = [
                {
                    st.session_state.left_label: left_labels[l],
                    st.session_state.right_label: r,
                }
                for l, r in solution.items()
            ]

            st.session_state.solver_label = solver_def.label

            log_step(f"Solved using solver '{solver_def.label}'.")

        st.success("Best-fit matching computed")
        st.table(st.session_state.solution_rows)

        # ==================================================
        # AI summary
        # ==================================================
        st.divider()
        st.subheader("AI-generated explanation")

        if st.button("Generate AI summary"):
            session = OptimizationSession(
                problem_family="Assignment",
                problem_type=st.session_state.assignment_type,
                problem_variant=st.session_state.assignment_variant,
                steps=st.session_state.journey,
                data_description=(
                    f"Data source: {describe_data_source(st.session_state.data_source)}"
                ),
                solver_name=st.session_state.solver_label,
                result_summary=(
                    f"{len(st.session_state.solution)} "
                    f"{st.session_state.left_label.lower()} optimally matched."
                ),
            )

            ai_summary = generate_ai_summary(session)
            st.session_state.ai_summary = ai_summary
            st.markdown(ai_summary)

        if "ai_summary" in st.session_state:
            zip_bytes = build_results_zip(
                solution_rows=st.session_state.solution_rows,
                ai_summary=st.session_state.ai_summary,
                metadata={
                    "solver": st.session_state.solver_label,
                    "variant": st.session_state.assignment_variant,
                },
            )

            st.download_button(
                "Download results",
                data=zip_bytes,
                file_name="best_fit_results.zip",
                mime="application/zip",
            )

        navigation_buttons(show_next=False)
        st.stop()
