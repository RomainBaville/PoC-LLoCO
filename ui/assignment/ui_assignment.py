# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025-2026 AKKODIS.
# SPDX-FileContributor: Romain Baville

import streamlit as st

from infrastructure.registry import DATA_SOURCE_REGISTRY

# from llm.session_model import OptimizationSession
from solvers.assignment.registry import SOLVERS
from ui.assignment.builder import build_entities_labels, build_problem
from ui.assignment.constraints.ui_logicals_constraints import logicals_constraints
from ui.assignment.constraints.ui_quantities_constraints import quantities_constraints
from ui.assignment.score.ui_matching import map_matching, matching_constraints, matching_strategy
from ui.assignment.score.ui_ressources import map_ressources, ressources_constraints, ressources_strategy
from ui.utils import (
    navigation_buttons,
    # generate_ai_summary,
    # describe_data_source,
    # build_results_zip,
)

DATA_DIR = "data"


def render( state ):
    # ==================================================
    # STEP 1 — Naming entities types
    # ==================================================
    if state.step == 1:
        st.header( "Define your left and right entities types" )

        state.left_entities_type = st.text_input( "Set the type of the left entity (e.g. Candidates)", "Candidates" )
        state.right_entities_type = st.text_input( "Set the type of the right entity (e.g. Targets)", "Targets" )

        navigation_buttons()
        st.stop()

    # ==================================================
    # STEP 2 — Score parameters
    # ==================================================
    if state.step == 2:
        st.header(
            f"How to compute the score to associate { state.left_entities_type} and { state.right_entities_type }"
        )

        state.use_matching = st.checkbox(
            "Use a scoring optimization involving a score computation from a matching between left and right variables sharing the same label (e.g. python_level, english_level, ...)"
        )

        state.use_ressources = st.checkbox(
            "Use a scoring optimization involving a score computation from an addition of the left entities ressources (e.g. Salary, years_of_experiances, ...)"
        )

        navigation_buttons()
        st.stop()

    # ==================================================
    # STEP 3 — Data source
    # ==================================================
    if state.step == 3:
        st.header( "Choose your data format" )

        for ds in DATA_SOURCE_REGISTRY.values():
            if st.button( ds.label ):
                state.data_source = ds.key

            st.caption( ds.description )

        if state.data_source == "csv_two_tables":
            st.subheader( "Upload CSV files" )

            left_file = st.file_uploader( f"{ state.left_entities_type } dataset", type=[ "csv" ], key="left_csv" )

            right_file = st.file_uploader( f"{ state.right_entities_type } dataset", type=[ "csv" ], key="right_csv" )

            loader = DATA_SOURCE_REGISTRY[ state.data_source ].loader_factory()

            if left_file and right_file:
                state.left_cols, state.left_rows = loader.load( left_file )
                state.right_cols, state.right_rows = loader.load( right_file )

                navigation_buttons()
                st.stop()

        navigation_buttons( show_next=False )

    # ==================================================
    # STEP 4 — Mapping
    # ==================================================
    if state.step == 4:
        st.header( "Map your data" )

        # -----------------------------
        # 1. Entities
        # -----------------------------
        st.subheader( "1. Identify entities" )

        state.left_entities_col_label = st.selectbox(
            f"Columns identifying { state.left_entities_type }", state.left_cols
        )

        state.right_entities_col_label = st.selectbox(
            f"Column identifying { state.right_entities_type }", state.right_cols
        )

        state.left_labels = build_entities_labels( state.left_entities_col_label, state.left_rows )
        state.right_labels = build_entities_labels( state.right_entities_col_label, state.right_rows )

        # -----------------------------
        # 2. Scoring variables
        # -----------------------------
        st.subheader( "2. Identify scoring variables" )
        if state.use_matching:
            map_matching( state )

        if state.use_ressources:
            map_ressources( state )

        navigation_buttons()
        st.stop()

    # ==================================================
    # STEP 5 — Strategy
    # ==================================================
    if state.step == 5:
        st.header( "Score optimization strategy" )

        if state.use_matching:
            matching_strategy( state )

        if state.use_ressources:
            ressources_strategy( state )

        navigation_buttons()
        st.stop()

    # ==================================================
    # STEP 6 — Constraints
    # ==================================================
    if state.step == 6:
        st.header( "Define constraints" )

        # -----------------------------
        # 1. Assignment constraints
        # -----------------------------
        st.subheader( "1. Assignment constraints" )

        state.use_quantities_constraints = st.checkbox(
            "Is there quantities constraints in the problem (e.g. max number of employees per project)"
        )
        state.use_logicals_constraints = st.checkbox(
            "Is there logicals constraints in the problem (e.g. if employee A is assigned to project I then employee B is assigned to project II)"
        )

        if state.use_quantities_constraints:
            quantities_constraints( state )

        if state.use_logicals_constraints:
            logicals_constraints( state )

        # -----------------------------
        # 2. Scoring variables constraints
        # -----------------------------
        st.subheader( "2. Scoring variables constraints" )
        if state.use_matching:
            matching_constraints( state )

        if state.use_ressources:
            ressources_constraints( state )

        navigation_buttons()
        st.stop()

    # ==================================================
    # STEP 7 — Solver
    # ==================================================
    if state.step == 7:
        st.header( "Choose solver" )

        solver_cols = st.columns( len( SOLVERS ) )
        for solver_col, solver in zip( solver_cols, SOLVERS.values() ):
            with solver_col:
                if st.button( solver.label ):
                    state.solver_key = solver.key
                    state.step += 1

        navigation_buttons( show_next=False )
        st.stop()

    # ==================================================
    # STEP 8 — Solve
    # ==================================================
    if state.step == 8:

        problem = build_problem( state )

        # ---------------------------------
        # Solve
        # ---------------------------------
        if state.solver_key in SOLVERS:
            try:
                with st.spinner( "Optimizing..." ):
                    solver_def = SOLVERS[ state.solver_key ]
                    solution: dict[ str, list[ tuple[ str, int ] ] ] = solver_def.solver_fn( problem )

                state.solution_rows = []

                for left_label, assignments in solution.items():
                    solution_row = {}
                    solution_row[ state.left_entities_type ] = left_label

                    right_labels = ""
                    nb_assignments = ""
                    for right_label, nb_assignment in assignments:
                        right_labels = f"{ right_labels } { right_label }"
                        nb_assignments = f"{ nb_assignments } { nb_assignment }"

                    if len( state.right_labels ) > 1:
                        solution_row[ state.right_entities_type ] = right_labels

                    if state.use_quantities_constraints and state.multiple_same_assignment:
                        solution_row[ f"Number of assignments per { state.right_entities_type }" ] = nb_assignments

                    state.solution_rows.append( solution_row )

                st.success( "Solution computed" )
                st.table( state.solution_rows )
            except RuntimeError as e:
                st.error( e )

                navigation_buttons( show_next=False )
                st.stop()

        # ---------------------------------
        # AI explanation
        # ---------------------------------
        # st.divider()
        # st.subheader( "AI explanation" )

        # if st.button( "Generate explanation by AI" ):
        #     session = OptimizationSession(
        #         problem_family="Assignment",
        #         problem_type=st.session_state.assignment_type,
        #         problem_variant="generic",
        #         steps=st.session_state.journey,
        #         data_description=describe_data_source(
        #             state.data_source
        #         ),
        #         solver_name=st.session_state.solver.label,
        #         result_summary=f"{ len( solution ) } assignments",
        #         config_summary=f"Objective: maximize",
        #     )

        #     state.ai_summary = generate_ai_summary( session )
        #     st.markdown( state.ai_summary )

        # if "ai_summary" in state:
        #     zip_bytes = build_results_zip(
        #         solution_rows=st.session_state.solution_rows,
        #         ai_summary=st.session_state.ai_summary,
        #         metadata={
        #             "solver": state.solver.label,
        #             "type": "assignment",
        #         },
        #     )

        #     st.download_button(
        #         "Download results (ZIP)",
        #         data=zip_bytes,
        #         file_name="assignment_results.zip",
        #         mime="application/zip",
        #     )

        navigation_buttons( show_next=False )
        st.stop()
