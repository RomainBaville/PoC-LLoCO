# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025-2026 AKKODIS.
# SPDX-FileContributor: Romain Baville

import os
import streamlit as st
from importlib import import_module

from ui.utils import (
    navigation_buttons,
    # generate_ai_summary,
    # describe_data_source,
    # build_results_zip,
)
from infrastructure.registry import DATA_SOURCE_REGISTRY
from ui.assignment.builder import build_entities, build_extrema_dict, build_problem
# from llm.session_model import OptimizationSession
from solvers.registry import ASSIGNMENT_SOLVER_GROUPS
from ui.assignment.matching.ui_matching import map_matching, matching_strategy, matching_constraints
from ui.assignment.ressources.ui_ressources import map_ressources, ressources_strategy, ressources_constraints

DATA_DIR = "data"


def render( state ):
    # ==================================================
    # STEP 1 — Naming entities
    # ==================================================
    if state.step == 1:
        st.header( "Define your left and right entities" )

        state.left_entities = st.text_input(
            "Set the label of the left entity (e.g. Candidates)", "Candidates"
        )
        state.right_entities = st.text_input(
            "Set the label of the right entity (e.g. Targets)", "Targets"
        )

        navigation_buttons()
        st.stop()

    # ==================================================
    # STEP 2 — Score parameters
    # ==================================================
    if state.step == 2:
        st.header( "How to compute the score to associate entities" )

        state.use_matching = st.checkbox( "Use a scoring optimization involving a score computation from a matching between left and right variables sharing the same label (e.g. python_level, english_level, ...)" )

        state.use_ressources = st.checkbox( "Use a scoring optimization involving a score computation from an addition of the left entities ressources (e.g. Salary, years_of_experiances, ...)" )

        navigation_buttons()
        st.stop()

    # ==================================================
    # STEP 3 — Data source
    # ==================================================
    if state.step == 3:
        st.header("Choose your data format")

        for ds in DATA_SOURCE_REGISTRY.values():
            if st.button(ds.label):
                state.data_source = ds.key
                state.step += 1

            st.caption(ds.description)

        if state.data_source == "csv_two_tables":
            csv_files = sorted(
                f for f in os.listdir( DATA_DIR ) if f.endswith( ".csv" )
            )

            left_csv = st.selectbox( f"{ state.left_entities } dataset", csv_files )
            right_csv = st.selectbox( f"{ state.right_entities } dataset", csv_files )

            loader = DATA_SOURCE_REGISTRY[
                state.data_source
            ].loader_factory()

            state.left_cols, state.left_rows = loader.load(
                os.path.join( DATA_DIR, left_csv )
            )
            state.right_cols, state.right_rows = loader.load(
                os.path.join( DATA_DIR, right_csv )
            )

        navigation_buttons()
        st.stop()

    # ==================================================
    # STEP 4 — Mapping
    # ==================================================
    if state.step == 4:
        st.header( "Map your data" )

        # -----------------------------
        # 1. Entities
        # -----------------------------
        st.subheader( f"1. Identify entities" )

        state.left_entities_col_id = st.selectbox(
            f"Columns identifying { state.left_entities }",
            state.left_cols
        )

        state.right_entities_col_id = st.selectbox(
            f"Column identifying { state.right_entities }",
            state.right_cols
        )

        state.left_labels = build_entities( state.left_entities_col_id, state.left_rows )
        state.right_labels = build_entities( state.right_entities_col_id, state.right_rows )

        # -----------------------------
        # 2. Scoring variables
        # -----------------------------
        st.subheader( f"2. Identify scoring variables" )
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
        st.header( "Define association constraints" )

        # -----------------------------
        # 1. Generic constraints
        # -----------------------------

        # Assignments constraints
        st.subheader( f"1.1. Assignment constraints for { state.left_entities }" )

        extrema = [ "minimum", "maximum" ]
        assignments_cols = st.columns( 2 )
        assignments_per_left = [ None, None ]

        for id, col in enumerate( assignments_cols ):
            with col:
                assignment_mode = st.radio(
                    f"Define { extrema[ id ] } assignments per { state.left_entities }",
                    [
                        "Use data column",
                        f"Set manually for each { state.left_entities }",
                        f"Set manually for all { state.left_entities } at once",
                        f"No { extrema[ id ] } assignment",
                    ],
                )

                if assignment_mode == "Use data column":
                    left_col_label = st.selectbox(
                        f"Column identifying { extrema[ id ] } assignments",
                        state.left_cols,
                        index=len( state.left_cols ) - 1
                    )
                    assignments_per_left[ id ] = build_extrema_dict( state.left_entities_col_id, state.left_rows, extrema_col_label=left_col_label )

                elif assignment_mode == f"Set manually for each { state.left_entities }":
                    assignments_per_left[ id ] = {}
                    for left_entity in state.left_labels:
                        assignments_per_left[ id ][ left_entity ] = st.number_input(
                            f"{ extrema[ id ] } assignments for { left_entity }",
                            min_value=1,
                            max_value=len( state.right_rows ),
                        )

                elif assignment_mode == f"Set manually for all { state.left_entities } at once":
                    left_number = st.number_input(
                        f"{ extrema[ id ] } assignments per { state.left_entities }",
                        min_value=1,
                        max_value=len( state.right_rows ),
                    )
                    assignments_per_left[ id ] = build_extrema_dict( state.left_entities_col_id, state.left_rows, extrema=left_number )

                else:
                    assignments_per_left[ id ] = None

        state.min_assignments = assignments_per_left[ 0 ]
        state.max_assignments = assignments_per_left[ 1 ]

        # Capacities constraints
        st.subheader( f"1.2. Capacity constraints for { state.right_entities }" )

        capacities_cols = st.columns( 2 )
        capacities_per_right = [ None, None ]

        for id, col in enumerate( capacities_cols ):
            with col:
                capacity_mode = st.radio(
                    f"Define { extrema[ id ] } capacities per { state.right_entities }",
                    [
                        "Use data column",
                        f"Set manually for each { state.right_entities }",
                        f"Set manually for all { state.right_entities } at once",
                        f"No { extrema[ id ] } capacity",
                    ],
                )

                if capacity_mode == "Use data column":
                    right_col_label = st.selectbox(
                        f"Column identifying { extrema[ id ] } capacities",
                        state.right_cols,
                        index=len( state.right_cols ) - 1
                    )
                    capacities_per_right[ id ] = build_extrema_dict( state.right_entities_col_id, state.right_rows, extrema_col_label=right_col_label )

                elif capacity_mode == f"Set manually for each { state.right_entities }":
                    capacities_per_right[ id ] = {}
                    for right_entity in state.right_labels:
                        capacities_per_right[ id ][ right_entity ] = st.number_input(
                            f"{ extrema[ id ] } capacities for { right_entity }",
                            min_value=1,
                            max_value=len( state.left_rows ),
                        )

                elif capacity_mode == f"Set manually for all { state.right_entities } at once":
                    right_number = st.number_input(
                        f"{ extrema[ id ] } capacities per { state.right_entities }",
                        min_value=1,
                        max_value=len( state.left_rows ),
                    )
                    capacities_per_right[ id ] = build_extrema_dict( state.right_entities_col_id, state.right_rows, extrema=right_number )

                else:
                    capacities_per_right[ id ] = None

        state.min_capacities = capacities_per_right[ 0 ]
        state.max_capacities = capacities_per_right[ 1 ]

        # -----------------------------
        # 2. logical constraints
        # -----------------------------
        st.subheader( "2. Logical constraints" )
        max_associations = [ state.max_capacities, state.max_assignments ]
        entities = [ state.left_entities, state.right_entities ]
        labels = [ state.left_labels, state.right_labels ]
        mutual_exclusion = [ None, None ]

        for i in range( 2 ):
            if max_associations[ i ] is None or max( max_associations[ i ].values() ) > 1:
                define_mutual_exclusion = st.checkbox( f"Is there groups of { entities[ i ] } who can't be assigned to the same { entities[ 1 - i ] }" )
                if define_mutual_exclusion:
                    nb_groups = st.number_input( f"How many group of { entities[ i ] } ?", 1 )

                    mutual_exclusion[ i ] = [ [] for _ in range( nb_groups ) ]
                    for group in range( nb_groups ):
                        nb = st.number_input( f"How many { entities[ i ] } are conserned for the group { group + 1 } ?", 2 )
                        mutual_exclusion[ i ][ group ] = [ None for _ in range( nb ) ]
                        exclusion_cols = st.columns( nb )
                        for id, col in enumerate( exclusion_cols ):
                            with col:
                                mutual_exclusion[ i ][ group ][ id ] = tuple( st.selectbox( f"{ entities[ i ] } { id + 1 } for the group { group + 1 }", labels[ i ], index=id ) )
                else:
                    mutual_exclusion[ i ] = None
            else:
                mutual_exclusion[ i ] = None

        state.left_mutual_exclusions = tuple( mutual_exclusion[ 0 ] ) if mutual_exclusion[ 0 ] is not None else None
        state.right_mutual_exclusions = tuple( mutual_exclusion[ 1 ] ) if mutual_exclusion[ 1 ] is not None else None

        # -----------------------------
        # 2. Scoring variables constraints
        # -----------------------------
        st.subheader( "3. Scoring variables constraints" )
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

        solver_group = ASSIGNMENT_SOLVER_GROUPS[ "assignments" ]
        solver_registry = import_module( solver_group.registry_module )

        for _, solver in solver_registry.SOLVERS.items():
            if st.button( solver.label ):
                state.solver = solver
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
        try:
            with st.spinner( "Optimizing..." ):
                solution = state.solver.solver_class().solve( problem )

            state.solution_rows = [
                {
                    state.left_entities: l,
                    state.right_entities: r,
                }
                for l, r in solution.items()
            ]

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
