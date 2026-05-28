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
from domain.assignment.skills.scoring import ScoringEngine

DATA_DIR = "data"


def render(step: int):

    # --------------------------------------------------
    # Defaults
    # --------------------------------------------------
    st.session_state.setdefault("left_label", "Candidates")
    st.session_state.setdefault("right_label", "Targets")
    st.session_state.setdefault("skill_label", "Skills")

    st.session_state.setdefault("objective_mode", "Maximize matching quality")
    st.session_state.setdefault("max_left", 1)
    st.session_state.setdefault("max_right", 1)
    st.session_state.setdefault("force_all", False)

    st.session_state.setdefault("reward_mode", "min")
    st.session_state.setdefault("penalty_mode", None)
    st.session_state.setdefault("penalty_weight", 1.0)

    # ==================================================
    # STEP 3 — Naming
    # ==================================================
    if step == 3:
        st.header("Define entities and skills")

        st.session_state.left_label = st.text_input(
            "Left entities", st.session_state.left_label
        )
        st.session_state.right_label = st.text_input(
            "Right entities", st.session_state.right_label
        )
        st.session_state.skill_label = st.text_input(
            "Skill label", st.session_state.skill_label
        )

        navigation_buttons()
        st.stop()

    # ==================================================
    # STEP 4 — CSV
    # ==================================================
    if step == 4:
        csv_files = sorted(f for f in os.listdir(DATA_DIR) if f.endswith(".csv"))

        st.session_state.left_csv = st.selectbox("Left CSV", csv_files)
        st.session_state.right_csv = st.selectbox("Right CSV", csv_files)

        navigation_buttons()
        st.stop()

    # ==================================================
    # STEP 5 — Mapping
    # ==================================================
    if step == 5:
        loader = DATA_SOURCE_REGISTRY[st.session_state.data_source].loader_factory()

        left_cols, _ = loader.load(os.path.join(DATA_DIR, st.session_state.left_csv))
        right_cols, _ = loader.load(os.path.join(DATA_DIR, st.session_state.right_csv))

        st.session_state.left_id_cols = st.multiselect("Left IDs", left_cols)

        st.session_state.skill_cols = st.multiselect(
            "Skill columns",
            [c for c in left_cols if c not in st.session_state.left_id_cols],
        )

        st.session_state.right_id_col = st.selectbox("Right ID", right_cols)

        navigation_buttons()
        st.stop()

    # ==================================================
    # STEP 6 — CONFIGURATION
    # ==================================================
    if step == 6:
        st.header("Configure assignment model")

        st.subheader("Objective")

        st.session_state.objective_mode = st.radio(
            "What is your goal?",
            [
                "Maximize matching quality",
                "Ensure all requirements are satisfied",
                "Balance both (recommended)",
            ]
        )

        st.subheader("Assignment rules")

        st.session_state.max_left = st.number_input(
            "Max assignments per left entity",
            min_value=1,
            value=st.session_state.max_left,
        )

        st.session_state.max_right = st.number_input(
            "Max assignments per right entity",
            min_value=1,
            value=st.session_state.max_right,
        )

        st.session_state.force_all = st.checkbox(
            "Assign all left entities",
            value=st.session_state.force_all,
        )

        st.subheader("Matching behavior")

        st.session_state.reward_mode = st.selectbox(
            "Reward function",
            ["min", "product", "sqrt_product", "ratio"],
        )

        st.session_state.penalty_mode = st.selectbox(
            "Penalty function",
            [None, "shortfall", "relative_shortfall", "absdiff"],
        )

        if st.session_state.penalty_mode:
            st.session_state.penalty_weight = st.slider(
                "Penalty weight",
                0.0,
                5.0,
                st.session_state.penalty_weight,
            )

        navigation_buttons()
        st.stop()

    # ==================================================
    # STEP 7 — Solver selection
    # ==================================================
    if step == 7:
        st.header("Choose solver")

        assignment_type = "skills"

        solver_group = ASSIGNMENT_SOLVER_GROUPS[assignment_type]
        solver_registry = import_module(solver_group.registry_module)

        for _, solver in solver_registry.SOLVERS.items():
            if st.button(solver.label):
                st.session_state.solver = solver
                st.session_state.step += 1

        navigation_buttons(show_next=False)
        st.stop()

    # ==================================================
    # STEP 8 — Solve
    # ==================================================
    if step == 8:
        loader = DATA_SOURCE_REGISTRY[st.session_state.data_source].loader_factory()
        _, left_rows = loader.load(os.path.join(DATA_DIR, st.session_state.left_csv))
        _, right_rows = loader.load(os.path.join(DATA_DIR, st.session_state.right_csv))


        problem, left_labels = build_problem(
            st.session_state, left_rows, right_rows
        )

        cfg = problem.config

        cfg.max_assignments_per_left = st.session_state.max_left
        cfg.max_assignments_per_right = st.session_state.max_right
        cfg.force_all_left_assigned = st.session_state.force_all

        cfg.reward_mode = st.session_state.reward_mode
        cfg.penalty_mode = st.session_state.penalty_mode
        cfg.penalty_weight = st.session_state.penalty_weight

        if st.session_state.objective_mode == "Ensure all requirements are satisfied":
            cfg.enforce_full_coverage = True
        elif st.session_state.objective_mode == "Balance both (recommended)":
            cfg.enforce_full_coverage = False
            cfg.penalty_mode = "shortfall"
            cfg.penalty_weight = 2.0
        else:
            cfg.enforce_full_coverage = False

        with st.spinner("Optimizing..."):
            solution = st.session_state.solver.solver_class().solve(problem)

        engine = ScoringEngine(cfg)

        def compute_score(l, r):
            return engine.compute(problem, l, r)

        st.session_state.solution = solution

        st.session_state.solution_rows = [
            {
                st.session_state.left_label: left_labels[l],
                st.session_state.right_label: r,
                "Score": compute_score(l, r),
            }
            for l, r in solution.items()
        ]

        st.success("Solution computed")
        st.table(st.session_state.solution_rows)

        # ==================================================
        # AI summary + ZIP
        # ==================================================
        st.divider()
        st.subheader("AI-generated explanation")

        if st.button("Generate AI summary"):
            session = OptimizationSession(
                problem_family="Assignment",
                problem_type=st.session_state.assignment_type,
                problem_variant="generic_assignment",
                steps=st.session_state.journey,
                data_description=describe_data_source(st.session_state.data_source),
                solver_name=st.session_state.solver.label,
                result_summary=f"{len(st.session_state.solution)} assignments.",
                config_summary=(
                    f"Objective: {st.session_state.objective_mode}, "
                    f"Reward: {cfg.reward_mode}, "
                    f"Penalty: {cfg.penalty_mode}"
                ),
            )

            st.session_state.ai_summary = generate_ai_summary(session)
            st.markdown(st.session_state.ai_summary)

        if "ai_summary" in st.session_state:
            zip_bytes = build_results_zip(
                solution_rows=st.session_state.solution_rows,
                ai_summary=st.session_state.ai_summary,
                metadata={
                    "solver": st.session_state.solver_label,
                    "variant": "generic_assignment",
                },
            )

            st.download_button(
                "Download results",
                data=zip_bytes,
                file_name="assignment_results.zip",
                mime="application/zip",
            )

        navigation_buttons(show_next=False)
        st.stop()
