# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025-2026 AKKODIS.
# SPDX-FileContributor: Romain Baville

from collections.abc import MutableMapping
from typing import Any

import streamlit as st

from infrastructure.registry import DATA_SOURCE_REGISTRY
from solvers.assignment.registry import SOLVERS
from ui.assignment.builder import build_entities_labels, build_problem
from ui.assignment.constraints.ui_logicals_constraints import logicals_constraints
from ui.assignment.constraints.ui_quantities_constraints import quantities_constraints
from ui.assignment.score.ui_matching import map_matching, matching_constraints, matching_strategy
from ui.assignment.score.ui_ressources import map_ressources, ressources_constraints, ressources_strategy
from ui.utils import navigation_buttons

SessionState = MutableMapping[ str, Any ]


def render( session_state: SessionState ) -> None:
    """Define the user interface for assignment problem.

    Args:
        session_state (SessionState): The session state.
    """
    # ==================================================
    # STEP 1 — Naming entities types
    # ==================================================
    if session_state.step == 1:
        st.header( "Define your left and right entities types" )

        session_state.left_entities_type = st.text_input(
            "Set the type of the left entity (e.g. Candidates)", "Candidates"
        )
        session_state.right_entities_type = st.text_input(
            "Set the type of the right entity (e.g. Targets)", "Targets"
        )

        navigation_buttons( session_state )
        st.stop()

    # ==================================================
    # STEP 2 — Score parameters
    # ==================================================
    if session_state.step == 2:
        st.header(
            f"How to compute the score to associate { session_state.left_entities_type}  " \
            f" and { session_state.right_entities_type }"
        )

        session_state.use_matching = st.checkbox(
            "Use a scoring optimization involving a score computation from a matching between left and right " \
            "variables sharing the same label (e.g. python_level, english_level, ...)"
        )

        session_state.use_ressources = st.checkbox(
            "Use a scoring optimization involving a score computation from an addition of the left entities" \
            " ressources (e.g. Salary, years_of_experiances, ...)"
        )

        navigation_buttons( session_state )
        st.stop()

    # ==================================================
    # STEP 3 — Data source
    # ==================================================
    if session_state.step == 3:
        st.header( "Choose your data format" )
        show_next: bool = False

        for ds in DATA_SOURCE_REGISTRY.values():
            if st.button( ds.label ):
                session_state.data_source = ds.key

            st.caption( ds.description )

        if session_state.data_source == "csv_two_tables":
            st.subheader( "Upload CSV files" )

            left_file = st.file_uploader(
                f"{ session_state.left_entities_type } dataset", type=[ "csv" ], key="left_csv"
            )

            right_file = st.file_uploader(
                f"{ session_state.right_entities_type } dataset", type=[ "csv" ], key="right_csv"
            )

            loader = DATA_SOURCE_REGISTRY[ session_state.data_source ].loader_factory()

            if left_file and right_file:
                session_state.left_cols, session_state.left_rows = loader.load( left_file )
                session_state.right_cols, session_state.right_rows = loader.load( right_file )
                show_next = True
            else:
                show_next = False

        navigation_buttons( session_state, show_next=show_next )
        st.stop()

    # ==================================================
    # STEP 4 — Mapping
    # ==================================================
    if session_state.step == 4:
        st.header( "Map your data" )

        # -----------------------------
        # 1. Entities
        # -----------------------------
        st.subheader( "1. Identify entities" )

        session_state.left_entities_col_label = st.selectbox(
            f"Columns identifying { session_state.left_entities_type }", session_state.left_cols
        )

        session_state.right_entities_col_label = st.selectbox(
            f"Column identifying { session_state.right_entities_type }", session_state.right_cols
        )

        session_state.left_labels = build_entities_labels(
            session_state.left_entities_col_label, session_state.left_rows
        )
        session_state.right_labels = build_entities_labels(
            session_state.right_entities_col_label, session_state.right_rows
        )

        # -----------------------------
        # 2. Scoring variables
        # -----------------------------
        st.subheader( "2. Identify scoring variables" )
        if session_state.use_matching:
            map_matching( session_state )

        if session_state.use_ressources:
            map_ressources( session_state )

        navigation_buttons( session_state )
        st.stop()

    # ==================================================
    # STEP 5 — Strategy
    # ==================================================
    if session_state.step == 5:
        st.header( "Score optimization strategy" )

        if session_state.use_matching:
            matching_strategy( session_state )

        if session_state.use_ressources:
            ressources_strategy( session_state )

        navigation_buttons( session_state )
        st.stop()

    # ==================================================
    # STEP 6 — Constraints
    # ==================================================
    if session_state.step == 6:
        st.header( "Define constraints" )

        # -----------------------------
        # 1. Assignment constraints
        # -----------------------------
        st.subheader( "1. Assignment constraints" )

        session_state.use_quantities_constraints = st.checkbox(
            "Is there quantities constraints in the problem (e.g. max number of employees per project)"
        )
        session_state.use_logicals_constraints = st.checkbox(
            "Is there logicals constraints in the problem " \
            "(e.g. if employee A is assigned to project I then employee B is assigned to project II)"
        )

        if session_state.use_quantities_constraints:
            quantities_constraints( session_state )

        if session_state.use_logicals_constraints:
            logicals_constraints( session_state )

        # -----------------------------
        # 2. Scoring variables constraints
        # -----------------------------
        st.subheader( "2. Scoring variables constraints" )
        if session_state.use_matching:
            matching_constraints( session_state )

        if session_state.use_ressources:
            ressources_constraints( session_state )

        navigation_buttons( session_state )
        st.stop()

    # ==================================================
    # STEP 7 — Solver
    # ==================================================
    if session_state.step == 7:
        st.header( "Choose solver" )

        solver_cols = st.columns( len( SOLVERS ) )
        for solver_col, solver in zip( solver_cols, SOLVERS.values(), strict=False ):
            with solver_col:
                if st.button( solver.label ):
                    session_state.solver_key = solver.key
                    session_state.step += 1

        navigation_buttons( session_state, show_next=False )
        st.stop()

    # ==================================================
    # STEP 8 — Solve
    # ==================================================
    if session_state.step == 8:

        problem = build_problem( session_state )

        # ---------------------------------
        # Solve
        # ---------------------------------
        if session_state.solver_key in SOLVERS:
            try:
                with st.spinner( "Optimizing..." ):
                    solver_def = SOLVERS[ session_state.solver_key ]
                    solution: dict[ str, list[ tuple[ str, int ] ] ] = solver_def.solver_fn( problem )

                session_state.solution_rows = []

                for left_label, assignments in solution.items():
                    solution_row = {}
                    solution_row[ session_state.left_entities_type ] = left_label

                    right_labels = ""
                    nb_assignments = ""
                    for right_label, nb_assignment in assignments:
                        right_labels = f"{ right_labels } { right_label }"
                        nb_assignments = f"{ nb_assignments } { nb_assignment }"

                    if len( session_state.right_labels ) > 1:
                        solution_row[ session_state.right_entities_type ] = right_labels

                    if session_state.use_quantities_constraints and session_state.multiple_same_assignment:
                        solution_row[
                            f"Number of assignments per { session_state.right_entities_type }"
                        ] = nb_assignments

                    session_state.solution_rows.append( solution_row )

                st.success( "Solution computed" )
                st.table( session_state.solution_rows )
            except RuntimeError as e:
                st.error( e )

                navigation_buttons( session_state, show_next=False )
                st.stop()

        # TODO in a futur PR
        """
        ---------------------------------
        AI explanation
        ---------------------------------
        st.divider()
        st.subheader( "AI explanation" )
        if st.button( "Generate explanation by AI" ):
            session = OptimizationSession(
                problem_family="Assignment",
                problem_type=st.session_state.assignment_type,
                problem_variant="generic",
                steps=st.session_state.journey,
                data_description=describe_data_source(
                    state.data_source
                ),
                solver_name=st.session_state.solver.label,
                result_summary=f"{ len( solution ) } assignments",
                config_summary=f"Objective: maximize",
            )
            state.ai_summary = generate_ai_summary( session )
            st.markdown( state.ai_summary )
        if "ai_summary" in state:
            zip_bytes = build_results_zip(
                solution_rows=st.session_state.solution_rows,
                ai_summary=st.session_state.ai_summary,
                metadata={
                    "solver": state.solver.label,
                    "type": "assignment",
                },
            )
            st.download_button(
                "Download results (ZIP)",
                data=zip_bytes,
                file_name="assignment_results.zip",
                mime="application/zip",
            )
        """

        navigation_buttons( session_state, show_next=False )
        st.stop()
