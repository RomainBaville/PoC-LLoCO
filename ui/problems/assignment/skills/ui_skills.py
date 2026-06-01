# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025-2026 AKKODIS.
# SPDX-FileContributor: Romain Baville

import os
import streamlit as st
from importlib import import_module

from ui.utils import (
    navigation_buttons,
    generate_ai_summary,
    describe_data_source,
    build_results_zip,
)
from infrastructure.registry import DATA_SOURCE_REGISTRY
from ui.problems.assignment.skills.builder import build_problem
from llm.session_model import OptimizationSession
from solvers.assignment.registry import ASSIGNMENT_SOLVER_GROUPS
from domain.assignment.skills.scoring import ScoringEngine

DATA_DIR = "data"


def render(step: int):

    # --------------------------------------------------
    # Defaults
    # --------------------------------------------------
    st.session_state.setdefault("left_label", "Candidates")
    st.session_state.setdefault("right_label", "Targets")
    st.session_state.setdefault("skill_label", "Skills")

    st.session_state.setdefault("objective", "maximize")

    st.session_state.setdefault("max_left", 1)
    st.session_state.setdefault("max_right", 1)
    st.session_state.setdefault("force_all", False)

    st.session_state.setdefault("reward_mode", "min")
    st.session_state.setdefault("penalty_mode", None)
    st.session_state.setdefault("penalty_weight", 1.0)

    st.session_state.setdefault("use_skills", True)
    st.session_state.setdefault("use_cost", False)
    st.session_state.setdefault("use_preferences", False)

    st.session_state.setdefault("cost_weight", 1.0)
    st.session_state.setdefault("preference_weight", 1.0)

    # ==================================================
    # STEP 3 — Naming
    # ==================================================
    if step == 3:
        st.header("Define your entities")

        st.markdown(
            "Give meaningful names to your entities to make the results easier to understand."
        )

        st.session_state.left_label = st.text_input(
            "Left entities (e.g. Employees)", st.session_state.left_label
        )
        st.session_state.right_label = st.text_input(
            "Right entities (e.g. Projects)", st.session_state.right_label
        )
        st.session_state.skill_label = st.text_input(
            "Feature name (e.g. Skills, Metrics)", st.session_state.skill_label
        )

        navigation_buttons()
        st.stop()

    # ==================================================
    # STEP 4 — CSV selection
    # ==================================================
    if step == 4:
        st.header("Select your datasets")

        st.markdown(
            "Choose files containing your entities and their attributes."
        )

        csv_files = sorted(
            f for f in os.listdir(DATA_DIR) if f.endswith(".csv")
        )

        st.session_state.left_csv = st.selectbox("Left dataset", csv_files)
        st.session_state.right_csv = st.selectbox("Right dataset", csv_files)

        navigation_buttons()
        st.stop()

    # ==================================================
    # STEP 5 — Mapping
    # ==================================================
    if step == 5:
        st.header("Map your data")

        loader = DATA_SOURCE_REGISTRY[
            st.session_state.data_source
        ].loader_factory()

        left_cols, _ = loader.load(
            os.path.join(DATA_DIR, st.session_state.left_csv)
        )
        right_cols, _ = loader.load(
            os.path.join(DATA_DIR, st.session_state.right_csv)
        )

        st.markdown(
            "Select identifiers and features used for optimization."
        )

        st.session_state.left_id_cols = st.multiselect(
            "Columns identifying left entities", left_cols
        )

        st.session_state.skill_cols = st.multiselect(
            "Feature columns (skills / metrics)",
            [c for c in left_cols if c not in st.session_state.left_id_cols],
        )

        st.session_state.right_id_col = st.selectbox(
            "Right entity identifier", right_cols
        )

        navigation_buttons()
        st.stop()

    # ==================================================
    # STEP 6 — Configuration
    # ==================================================
    if step == 6:
        st.header("Define your optimization strategy")

        st.markdown(
            "We will guide you through a few simple choices."
        )

        # -----------------------------
        # Objective
        # -----------------------------
        st.subheader("1. Objective")

        choice = st.radio(
            "What do you want to optimize?",
            [
                "Best matching (skills / compatibility)",
                "Lowest cost / effort",
                "Hybrid (combine multiple factors)",
            ],
        )

        if "matching" in choice.lower():
            st.session_state.objective = "maximize"
            st.session_state.use_skills = True
            st.session_state.use_cost = False

        elif "cost" in choice.lower():
            st.session_state.objective = "minimize"
            st.session_state.use_cost = True
            st.session_state.use_skills = False

        else:
            st.session_state.objective = "maximize"
            st.session_state.use_cost = True
            st.session_state.use_skills = True

        st.info(
            "Matching = ensures best compatibility\n"
            "Cost = minimizes expenses or time\n"
            "Hybrid = balances both"
        )

        # -----------------------------
        # Assignment rules
        # -----------------------------
        st.subheader("2. Assignment rules")

        st.session_state.max_left = st.number_input(
            "Max assignments per left entity", 1, 10, st.session_state.max_left
        )

        st.session_state.max_right = st.number_input(
            "Capacity per right entity", 1, 10, st.session_state.max_right
        )

        st.session_state.force_all = st.checkbox(
            "Force assignment of all entities",
            value=st.session_state.force_all,
        )

        # -----------------------------
        # Scoring
        # -----------------------------
        st.subheader("3. Scoring behavior")

        if st.session_state.use_skills:
            st.markdown("**Feature matching**")

            st.session_state.reward_mode = st.selectbox(
                "Compatibility evaluation",
                ["min", "product", "ratio"],
            )

            st.session_state.penalty_mode = st.selectbox(
                "Penalty (optional)",
                [None, "shortfall", "absdiff"],
            )

            if st.session_state.penalty_mode:
                st.session_state.penalty_weight = st.slider(
                    "Penalty importance",
                    0.0,
                    5.0,
                    st.session_state.penalty_weight,
                )

        if st.session_state.use_cost:
            st.markdown("**Cost importance**")

            st.session_state.cost_weight = st.slider(
                "Cost weight",
                0.0,
                5.0,
                st.session_state.cost_weight,
            )

        # -----------------------------
        # Advanced
        # -----------------------------
        with st.expander("4. Advanced options"):
            st.session_state.use_preferences = st.checkbox(
                "Include preference scoring"
            )

            if st.session_state.use_preferences:
                st.session_state.preference_weight = st.slider(
                    "Preference importance",
                    0.0,
                    5.0,
                    st.session_state.preference_weight,
                )

        navigation_buttons()
        st.stop()

    # ==================================================
    # STEP 7 — Solver
    # ==================================================
    if step == 7:
        st.header("Choose solver")

        solver_group = ASSIGNMENT_SOLVER_GROUPS["skills"]
        solver_registry = import_module(solver_group.registry_module)

        for _, solver in solver_registry.SOLVERS.items():
            if st.button(solver.label):
                st.session_state.solver = solver
                st.session_state.step += 1

        navigation_buttons(show_next=False)
        st.stop()

    # ==================================================
    # STEP 8 — Solve + Results
    # ==================================================
    if step == 8:

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
            st.session_state, left_rows, right_rows
        )

        cfg = problem.config

        # Apply config
        cfg.max_assignments_per_left = st.session_state.max_left
        cfg.max_assignments_per_right = st.session_state.max_right
        cfg.force_all_left_assigned = st.session_state.force_all

        cfg.objective = st.session_state.objective

        cfg.use_cost = st.session_state.use_cost
        cfg.use_preferences = st.session_state.use_preferences

        cfg.cost_weight = st.session_state.cost_weight
        cfg.preference_weight = st.session_state.preference_weight

        cfg.reward_mode = st.session_state.reward_mode
        cfg.penalty_mode = st.session_state.penalty_mode
        cfg.penalty_weight = st.session_state.penalty_weight

        # Solve
        with st.spinner("Optimizing..."):
            solution = st.session_state.solver.solver_class().solve(problem)

        engine = ScoringEngine(cfg)

        st.session_state.solution_rows = [
            {
                st.session_state.left_label: left_labels[l],
                st.session_state.right_label: r,
                "Score": engine.compute(problem, l, r),
            }
            for l, r in solution.items()
        ]

        st.success("Solution computed")
        st.table(st.session_state.solution_rows)

        # ---------------------------------------------
        # AI explanation
        # ---------------------------------------------
        st.divider()
        st.subheader("AI explanation")

        if st.button("Generate explanation"):
            session = OptimizationSession(
                problem_family="Assignment",
                problem_type=st.session_state.assignment_type,
                problem_variant="generic",
                steps=st.session_state.journey,
                data_description=describe_data_source(
                    st.session_state.data_source
                ),
                solver_name=st.session_state.solver.label,
                result_summary=f"{len(solution)} assignments",
                config_summary=f"Objective: {cfg.objective}",
            )

            st.session_state.ai_summary = generate_ai_summary(session)
            st.markdown(st.session_state.ai_summary)

        if "ai_summary" in st.session_state:

            zip_bytes = build_results_zip(
                solution_rows=st.session_state.solution_rows,
                ai_summary=st.session_state.ai_summary,
                metadata={
                    "solver": st.session_state.solver.label,
                    "type": "assignment",
                },
            )

            st.download_button(
                "Download results (ZIP)",
                data=zip_bytes,
                file_name="assignment_results.zip",
                mime="application/zip",
            )

        navigation_buttons(show_next=False)
        st.stop()
