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
from ui.assignment.builder import build_problem, build_dict, build_entities
# from llm.session_model import OptimizationSession
from solvers.registry import ASSIGNMENT_SOLVER_GROUPS
from ui.assignment.skills.ui_skills import use_skills, map_skills, skills_strategy

DATA_DIR = "data"


def render( step: int ):

    # ==================================================
    # STEP 1 — Data source
    # ==================================================
    if st.session_state.step == 1:
        st.header("Choose your data format")

        for ds in DATA_SOURCE_REGISTRY.values():
            if st.button(ds.label):
                st.session_state.data_source = ds.key
                st.session_state.step += 1

            st.caption(ds.description)

        navigation_buttons()
        st.stop()

    # ==================================================
    # STEP 2 — Naming entities
    # ==================================================
    if step == 2:
        st.header( "Define your left and right entities" )

        st.session_state.left_label = st.text_input(
            "Left entity label (e.g. Candidates)", "Candidates"
        )
        st.session_state.right_label = st.text_input(
            "Right entity label (e.g. Targets)", "Targets"
        )

        navigation_buttons()
        st.stop()


    # ==================================================
    # STEP 3 — CSV
    # ==================================================
    if step == 3:
        st.header( "Select datasets" )

        csv_files = sorted(
            f for f in os.listdir( DATA_DIR ) if f.endswith( ".csv" )
        )

        st.session_state.left_csv = st.selectbox( f"{ st.session_state.left_label } dataset", csv_files )
        st.session_state.right_csv = st.selectbox( f"{ st.session_state.right_label } dataset", csv_files )

        navigation_buttons()
        st.stop()


    if step == 4:
        st.header( "How to assigned entities" )

        use_skills( st.session_state )

        navigation_buttons()
        st.stop()

    # ==================================================
    # STEP 5 — Mapping + assignment behavior
    # ==================================================
    if step == 5:
        st.header( "Map your data" )

        loader = DATA_SOURCE_REGISTRY[
            st.session_state.data_source
        ].loader_factory()

        st.session_state.left_cols, st.session_state.left_rows = loader.load(
            os.path.join( DATA_DIR, st.session_state.left_csv )
        )
        st.session_state.right_cols, st.session_state.right_rows = loader.load(
            os.path.join( DATA_DIR, st.session_state.right_csv )
        )

        # -----------------------------
        # 1. Entities
        # -----------------------------
        st.subheader( f"1. Identify entities and { st.session_state.feature_label }" )

        st.session_state.left_entities_col_id = st.selectbox(
            f"Columns identifying { st.session_state.left_label }",
            st.session_state.left_cols
        )

        st.session_state.right_entities_col_id = st.selectbox(
            f"Column identifying { st.session_state.right_label }",
            st.session_state.right_cols
        )

        st.session_state.left_entities = build_entities( st.session_state.left_entities_col_id, st.session_state.left_rows )
        st.session_state.right_entities = build_entities( st.session_state.right_entities_col_id, st.session_state.right_rows )

        # -----------------------------
        # 2. Skills
        # -----------------------------

        if st.session_state.use_skills:
            map_skills( st.session_state )

        # -----------------------------
        # 3. LEFT ASSIGNMENT
        # -----------------------------
        st.subheader( f"2. Assignment rules for { st.session_state.left_label }" )

        extrema = [ "minimum", "maximum" ]
        assignments_cols = st.columns( 2 )
        assignments_per_left = [ None, None ]

        for id, col in enumerate( assignments_cols ):
            with col:
                assignment_mode = st.radio(
                    f"Define { extrema[ id ] } assignments per { st.session_state.left_label }",
                    [
                        "Use data column",
                        f"Set manually for each { st.session_state.left_label }",
                        f"Set manually for all { st.session_state.left_label } at once",
                        f"No { extrema[ id ] } assignment",
                    ],
                )

                if assignment_mode == "Use data column":
                    left_col_label = st.selectbox(
                        f"Column identifying { extrema[ id ] } assignments",
                        st.session_state.left_cols,
                        index=len( st.session_state.left_cols ) - 1
                    )
                    assignments_per_left[ id ] = build_dict( st.session_state.left_entities_col_id, st.session_state.left_rows, extrema_col_label=left_col_label )

                elif assignment_mode == f"Set manually for each { st.session_state.left_label }":
                    assignments_per_left[ id ] = {}
                    for left_entity in st.session_state.left_entities:
                        assignments_per_left[ id ][ left_entity ] = st.number_input(
                            f"{ extrema[ id ] } assignments for { left_entity }",
                            min_value=1,
                            max_value=len( st.session_state.right_rows ),
                        )

                elif assignment_mode == f"Set manually for all { st.session_state.left_label } at once":
                    left_number = st.number_input(
                        f"{ extrema[ id ] } assignments per { st.session_state.left_label }",
                        min_value=1,
                        max_value=len( st.session_state.right_rows ),
                    )
                    assignments_per_left[ id ] = build_dict( st.session_state.left_entities_col_id, st.session_state.left_rows, extrema=left_number )

                else:
                    assignments_per_left[ id ] = None

        st.session_state.min_assignments_per_left = assignments_per_left[ 0 ]
        st.session_state.max_assignments_per_left = assignments_per_left[ 1 ]

        # -----------------------------
        # 4. RIGHT CAPACITY
        # -----------------------------
        st.subheader( f"3. Capacity rules for { st.session_state.right_label }" )

        capacities_cols = st.columns( 2 )
        capacities_per_right = [ None, None ]

        for id, col in enumerate( capacities_cols ):
            with col:
                capacity_mode = st.radio(
                    f"Define { extrema[ id ] } capacities per { st.session_state.right_label }",
                    [
                        "Use data column",
                        f"Set manually for each { st.session_state.right_label }",
                        f"Set manually for all { st.session_state.right_label } at once",
                        f"No { extrema[ id ] } capacity",
                    ],
                )

                if capacity_mode == "Use data column":
                    right_col_label = st.selectbox(
                        f"Column identifying { extrema[ id ] } capacities",
                        st.session_state.right_cols,
                        index=len( st.session_state.right_cols ) - 1
                    )
                    capacities_per_right[ id ] = build_dict( st.session_state.right_entities_col_id, st.session_state.right_rows, extrema_col_label=right_col_label )

                elif capacity_mode == f"Set manually for each { st.session_state.right_label }":
                    capacities_per_right[ id ] = {}
                    for right_entity in st.session_state.right_entities:
                        capacities_per_right[ id ][ right_entity ] = st.number_input(
                            f"{ extrema[ id ] } capacities for { right_entity }",
                            min_value=1,
                            max_value=len( st.session_state.left_rows ),
                        )

                elif capacity_mode == f"Set manually for all { st.session_state.right_label } at once":
                    right_number = st.number_input(
                        f"{ extrema[ id ] } capacities per { st.session_state.right_label }",
                        min_value=1,
                        max_value=len( st.session_state.left_rows ),
                    )
                    capacities_per_right[ id ] = build_dict( st.session_state.right_entities_col_id, st.session_state.right_rows, extrema=right_number )

                else:
                    capacities_per_right[ id ] = None

        st.session_state.min_capacities_per_right = capacities_per_right[ 0 ]
        st.session_state.max_capacities_per_right = capacities_per_right[ 1 ]


        navigation_buttons()
        st.stop()

    # ==================================================
    # STEP 6 — Strategy
    # ==================================================
    if step == 6:
        st.header( "Optimization strategy" )

        if st.session_state.max_capacities_per_right is None or max( st.session_state.max_capacities_per_right.values() ) > 1:
            define_left_mutual_exclusion = st.checkbox( f"Is there groups of { st.session_state.left_label } who can't be assigned to the same { st.session_state.right_label }" )
            if define_left_mutual_exclusion:
                nb_left_groups = st.number_input( f"How many group of { st.session_state.left_label } ?", 1 )

                st.session_state.left_mutual_exclusions = [ [] for _ in range( nb_left_groups ) ]
                for left_group in range( nb_left_groups ):
                    nb_left = st.number_input( f"How many { st.session_state.left_label } are conserned for the group { left_group + 1 } ?", 2 )
                    st.session_state.left_mutual_exclusions[ left_group ] = [ None for _ in range( nb_left ) ]
                    left_exclusion_cols = st.columns( nb_left )
                    for id, left_col in enumerate( left_exclusion_cols ):
                        with left_col:
                            st.session_state.left_mutual_exclusions[ left_group ][ id ] = st.selectbox( f"{ st.session_state.left_label } { id + 1 } for the group { left_group + 1 }", st.session_state.left_entities, index=id )
            else:
                st.session_state.left_mutual_exclusions = None
        else:
            st.session_state.left_mutual_exclusions = None

        if st.session_state.max_assignments_per_left is None or max( st.session_state.max_assignments_per_left.values() ) > 1:
            define_right_mutual_exclusions = st.checkbox( f"Is there groups of { st.session_state.right_label } who can't contain the same { st.session_state.left_label }" )
            if define_right_mutual_exclusions:
                nb_right_groups = st.number_input( f"How many group of { st.session_state.right_label }?", 1 )
                st.session_state.right_mutual_exclusions = [ [] for _ in range( nb_right_groups ) ]
                for right_group in range( nb_right_groups ):
                    nb_right = st.number_input( f"How many { st.session_state.right_label } are conserned for the group { right_group + 1 } ?", 2 )
                    st.session_state.right_mutual_exclusions[ right_group ] = [ None for _ in range( nb_right ) ]
                    right_exclusion_cols = st.columns( nb_right )
                    for id, right_col in enumerate( right_exclusion_cols ):
                        with right_col:
                            st.session_state.right_mutual_exclusions[ right_group ][ id ] = st.selectbox( f"{ st.session_state.right_label } { id + 1 } for the group { right_group + 1 }", st.session_state.right_entities, index=id )
            else:
                st.session_state.right_mutual_exclusions = None
        else:
            st.session_state.right_mutual_exclusions = None

        if st.session_state.use_skills:
            skills_strategy( st.session_state )

        navigation_buttons()
        st.stop()

    # ==================================================
    # STEP 7 — Solver
    # ==================================================
    if step == 7:
        st.header( "Choose solver" )

        solver_group = ASSIGNMENT_SOLVER_GROUPS[ "assignments" ]
        solver_registry = import_module( solver_group.registry_module )

        for _, solver in solver_registry.SOLVERS.items():
            if st.button( solver.label ):
                st.session_state.solver = solver
                st.session_state.step += 1

        navigation_buttons( show_next=False )
        st.stop()

    # ==================================================
    # STEP 8 — Solve
    # ==================================================
    if step == 8:

        problem = build_problem( st.session_state )

        # ---------------------------------
        # Solve
        # ---------------------------------
        try:
            with st.spinner( "Optimizing..." ):
                solution = st.session_state.solver.solver_class().solve( problem )

            st.session_state.solution_rows = [
                {
                    st.session_state.left_label: l,
                    st.session_state.right_label: r,
                }
                for l, r in solution.items()
            ]

            st.success( "Solution computed" )
            st.table( st.session_state.solution_rows )
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
        #             st.session_state.data_source
        #         ),
        #         solver_name=st.session_state.solver.label,
        #         result_summary=f"{ len( solution ) } assignments",
        #         config_summary=f"Objective: maximize",
        #     )

        #     st.session_state.ai_summary = generate_ai_summary( session )
        #     st.markdown( st.session_state.ai_summary )

        # if "ai_summary" in st.session_state:
        #     zip_bytes = build_results_zip(
        #         solution_rows=st.session_state.solution_rows,
        #         ai_summary=st.session_state.ai_summary,
        #         metadata={
        #             "solver": st.session_state.solver.label,
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
