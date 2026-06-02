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
from ui.problems.assignment.skills.builder import build_problem, build_dict, build_parameters
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

    st.session_state.setdefault("min_left", 0)
    st.session_state.setdefault("max_left", 1)
    st.session_state.setdefault("min_right", 0)
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
            "Give meaningful names to your entities to make results easier to read."
        )

        st.session_state.left_label = st.text_input(
            "Left entities (e.g. Employees)", st.session_state.left_label
        )
        st.session_state.right_label = st.text_input(
            "Right entities (e.g. Projects)", st.session_state.right_label
        )
        st.session_state.skill_label = st.text_input(
            "Feature name (e.g. Skills)", st.session_state.skill_label
        )

        navigation_buttons()
        st.stop()

    # ==================================================
    # STEP 4 — CSV
    # ==================================================
    if step == 4:
        st.header("Select datasets")

        csv_files = sorted(
            f for f in os.listdir(DATA_DIR) if f.endswith(".csv")
        )

        st.session_state.left_csv = st.selectbox("Left dataset", csv_files)
        st.session_state.right_csv = st.selectbox("Right dataset", csv_files)

        navigation_buttons()
        st.stop()

    # ==================================================
    # STEP 5 — Mapping + assignment behavior
    # ==================================================
    if step == 5:
        st.header("Map your data")

        loader = DATA_SOURCE_REGISTRY[
            st.session_state.data_source
        ].loader_factory()

        left_cols, left_rows = loader.load(
            os.path.join(DATA_DIR, st.session_state.left_csv)
        )
        right_cols, right_rows = loader.load(
            os.path.join(DATA_DIR, st.session_state.right_csv)
        )

        # -----------------------------
        # 1. Entities & skills labels
        # -----------------------------
        st.subheader( f"1. Identify entities and { st.session_state.skill_label }" )

        left_entity_col_id = st.selectbox(
            f"Columns identifying { st.session_state.left_label }",
            left_cols
        )

        right_entity_col_id = st.selectbox(
            f"Column identifying { st.session_state.right_label }",
            right_cols
        )

        skills_labels = st.multiselect(
            f"Columns identifying { st.session_state.skill_label }",
            [ c for c in left_cols if c != left_entity_col_id ],
        )

        st.session_state.left_entity, st.session_state.left_skills = build_parameters( skills_labels, left_entity_col_id, left_rows )
        st.session_state.right_entity, st.session_state.right_requirements = build_parameters( skills_labels, right_entity_col_id, right_rows )
        st.session_state.skills_labels = skills_labels

        # -----------------------------
        # 2. LEFT ASSIGNMENT
        # -----------------------------
        st.subheader( f"2. Assignment rules for { st.session_state.left_label }" )

        assignment_mode = st.radio(
            f"Define minimum and maximum assignments per { st.session_state.left_label }",
            [
                "Use data column",
                f"Set manually for all { st.session_state.left_label } at once",
                "No minimum and maximum assignment",
            ],
        )

        if assignment_mode == "Use data column":
            min_left_col_label = st.selectbox(
                "Column identifying minimum assignments",
                left_cols,
                index=len(left_cols)-2
            )
            min_assignments_per_left = build_dict( left_entity_col_id, left_rows, extrema_col_label=min_left_col_label )

            max_left_col_label = st.selectbox(
                "Column identifying maximum assignments",
                left_cols,
                index=len(left_cols)-1
            )
            max_assignments_per_left = build_dict( left_entity_col_id, left_rows, extrema_col_label=max_left_col_label )

        elif assignment_mode == f"Set manually for all { st.session_state.left_label } at once":
            min_left_number = st.number_input(
                f"Minimum assignments per { st.session_state.left_label }",
                min_value=0,
                max_value=len(left_rows),
            )
            min_assignments_per_left = build_dict( left_entity_col_id, left_rows, extrema=min_left_number )


            max_left_number = st.number_input(
                f"Maximum assignments per { st.session_state.left_label }",
                min_value=0,
                max_value=len(left_rows)
            )
            max_assignments_per_left = build_dict( left_entity_col_id, left_rows, extrema=max_left_number )

        else:
            min_assignments_per_left = None
            max_assignments_per_left = None

        st.session_state.min_assignments_per_left = min_assignments_per_left
        st.session_state.max_assignments_per_left = max_assignments_per_left

        # -----------------------------
        # 3. RIGHT CAPACITY
        # -----------------------------
        st.subheader( f"3. Capacity rules for { st.session_state.right_label }" )

        capacity_mode = st.radio(
            f"Define minminum and maximum capacities per { st.session_state.right_label }",
            [
                "Use data column",
                f"Set manually for all { st.session_state.right_label } at once",
                "No minimum and maximum requirement",
            ],
        )

        if capacity_mode == "Use data column":
            min_right_col_label = st.selectbox(
                "Column identifying minimum capacities",
                right_cols,
                index=len(right_cols)-2
            )
            min_capacities_per_right = build_dict( right_entity_col_id, right_rows, extrema_col_label=min_right_col_label )

            max_right_col_label = st.selectbox(
                "Column identifying maximum capacities",
                right_cols,
                index=len(right_cols)-1
            )
            max_capacities_per_right = build_dict( right_entity_col_id, right_rows, extrema_col_label=max_right_col_label )

        elif capacity_mode == f"Set manually for all { st.session_state.right_label } at once":
            min_right_number = st.number_input(
                f"Minimum assignments per { st.session_state.right_label }",
                min_value=0,
                max_value=len(right_rows),
            )
            min_capacities_per_right = build_dict( right_entity_col_id, right_rows, extrema=min_right_number )

            max_right_number = st.number_input(
                f"Maximum capacities per { st.session_state.right_label }",
                min_value=0,
                max_value=len(right_rows)
            )
            max_capacities_per_right = build_dict( right_entity_col_id, right_rows, extrema=max_right_number )

        else:
            min_capacities_per_right = None
            max_capacities_per_right = None

        st.session_state.min_capacities_per_right = min_capacities_per_right
        st.session_state.max_capacities_per_right = max_capacities_per_right

        navigation_buttons()
        st.stop()

    # ==================================================
    # STEP 6 — Strategy
    # ==================================================
    if step == 6:
        st.header("Optimization strategy")

        choice = st.radio(
            "What do you want to optimize?",
            [
                "Best matching",
                "Lowest cost",
                "Hybrid",
            ],
        )

        if "matching" in choice.lower():
            st.session_state.objective = "maximize"
            st.session_state.use_cost = False
            st.session_state.use_skills = True

        elif "cost" in choice.lower():
            st.session_state.objective = "minimize"
            st.session_state.use_cost = True
            st.session_state.use_skills = False

        else:
            st.session_state.objective = "maximize"
            st.session_state.use_cost = True
            st.session_state.use_skills = True

        st.subheader("Scoring behavior")

        if st.session_state.use_skills:
            st.session_state.reward_mode = st.selectbox(
                "Compatibility evaluation",
                ["min", "product", "ratio"],
            )

            st.session_state.penalty_mode = st.selectbox(
                "Penalty",
                [None, "shortfall", "absdiff"],
            )

            if st.session_state.penalty_mode:
                st.session_state.penalty_weight = st.slider(
                    "Penalty weight", 0.0, 5.0, 1.0
                )

        if st.session_state.use_cost:
            st.session_state.cost_weight = st.slider(
                "Cost importance", 0.0, 5.0, 1.0
            )

        with st.expander("Advanced"):
            st.session_state.use_preferences = st.checkbox("Use preferences")

            if st.session_state.use_preferences:
                st.session_state.preference_weight = st.slider(
                    "Preference weight", 0.0, 5.0, 1.0
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
    # STEP 8 — Solve
    # ==================================================
    if step == 8:

        problem = build_problem( st.session_state )

        # ---------------------------------
        # Solve
        # ---------------------------------
        with st.spinner("Optimizing..."):
            solution = st.session_state.solver.solver_class().solve(problem)

        engine = ScoringEngine(problem.config)

        st.session_state.solution_rows = [
            {
                st.session_state.left_label: l,
                st.session_state.right_label: r,
                "Score": engine.compute(problem, l, r),
            }
            for l, r in solution.items()
        ]

        st.success("Solution computed")
        st.table(st.session_state.solution_rows)

        # ---------------------------------
        # AI explanation
        # ---------------------------------
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
                config_summary=f"Objective: {problem.config.objective}",
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
