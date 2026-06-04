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
from domain.assignment.skills.scoring import REWARD_FUNCTIONS, PENALTY_FUNCTIONS

DATA_DIR = "data"


def render(step: int):

    # ==================================================
    # STEP 3 — Naming
    # ==================================================
    if step == 3:
        st.header( "Define your entities" )

        st.markdown(
            "Give meaningful names to your entities to make results easier to read."
        )

        st.session_state.left_label = st.text_input(
            "Left entities (e.g. Candidates)", "Candidates"
        )
        st.session_state.right_label = st.text_input(
            "Right entities (e.g. Targets)", "Targets"
        )
        st.session_state.feature_label = st.text_input(
            "Feature label (e.g. Skills)", "Skills"
        )

        navigation_buttons()
        st.stop()

    # ==================================================
    # STEP 4 — CSV
    # ==================================================
    if step == 4:
        st.header( "Select datasets" )

        csv_files = sorted(
            f for f in os.listdir( DATA_DIR ) if f.endswith( ".csv" )
        )

        st.session_state.left_csv = st.selectbox( f"{ st.session_state.left_label } dataset", csv_files )
        st.session_state.right_csv = st.selectbox( f"{ st.session_state.right_label } dataset", csv_files )

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

        left_cols, left_rows = loader.load(
            os.path.join( DATA_DIR, st.session_state.left_csv )
        )
        right_cols, right_rows = loader.load(
            os.path.join( DATA_DIR, st.session_state.right_csv )
        )

        # -----------------------------
        # 1. Entities & skills labels
        # -----------------------------
        st.subheader( f"1. Identify entities and { st.session_state.feature_label }" )

        left_entities_col_id = st.selectbox(
            f"Columns identifying { st.session_state.left_label }",
            left_cols
        )

        right_entities_col_id = st.selectbox(
            f"Column identifying { st.session_state.right_label }",
            right_cols
        )

        skill_labels = st.multiselect(
            f"Columns identifying { st.session_state.feature_label }",
            [ c for c in left_cols if c != left_entities_col_id ],
        )

        st.session_state.left_entities, st.session_state.left_skills = build_parameters( skill_labels, left_entities_col_id, left_rows )
        st.session_state.right_entities, st.session_state.right_requirements = build_parameters( skill_labels, right_entities_col_id, right_rows )
        st.session_state.skill_labels = skill_labels

        # -----------------------------
        # 2. LEFT ASSIGNMENT
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
                        left_cols,
                        index=len( left_cols ) - 1
                    )
                    assignments_per_left[ id ] = build_dict( left_entities_col_id, left_rows, extrema_col_label=left_col_label )

                elif assignment_mode == f"Set manually for each { st.session_state.left_label }":
                    assignments_per_left[ id ] = {}
                    for left_entity in st.session_state.left_entities:
                        assignments_per_left[ id ][ left_entity ] = st.number_input(
                            f"{ extrema[ id ] } assignments for { left_entity }",
                            min_value=0,
                            max_value=len(right_rows),
                        )

                elif assignment_mode == f"Set manually for all { st.session_state.left_label } at once":
                    left_number = st.number_input(
                        f"{ extrema[ id ] } assignments per { st.session_state.left_label }",
                        min_value=0,
                        max_value=len(right_rows),
                    )
                    assignments_per_left[ id ] = build_dict( left_entities_col_id, left_rows, extrema=left_number )

                else:
                    assignments_per_left[ id ] = None

        st.session_state.min_assignments_per_left = assignments_per_left[ 0 ]
        st.session_state.max_assignments_per_left = assignments_per_left[ 1 ]

        # -----------------------------
        # 3. RIGHT CAPACITY
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
                        right_cols,
                        index=len(right_cols) - 1
                    )
                    capacities_per_right[ id ] = build_dict( right_entities_col_id, right_rows, extrema_col_label=right_col_label )

                elif capacity_mode == f"Set manually for each { st.session_state.right_label }":
                    capacities_per_right[ id ] = {}
                    for right_entity in st.session_state.right_entities:
                        capacities_per_right[ id ][ right_entity ] = st.number_input(
                            f"{ extrema[ id ] } capacities for { right_entity }",
                            min_value=0,
                            max_value=len(left_rows),
                        )

                elif capacity_mode == f"Set manually for all { st.session_state.right_label } at once":
                    right_number = st.number_input(
                        f"{ extrema[ id ] } capacities per { st.session_state.right_label }",
                        min_value=0,
                        max_value=len(left_rows),
                    )
                    capacities_per_right[ id ] = build_dict( right_entities_col_id, right_rows, extrema=right_number )

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

        st.session_state.reward_mode = st.selectbox(
            "Compatibility evaluation",
            REWARD_FUNCTIONS,
        )

        use_penalty = st.checkbox( "Use penalty" )
        if use_penalty:
            st.session_state.penalty_mode = st.selectbox(
            "Penalty mode",
            PENALTY_FUNCTIONS,
        )
            st.session_state.penalty_weight = st.slider(
                "Penalty weight", 0.0, 5.0, 1.0
            )
        else:
            st.session_state.penalty_mode = None
            st.session_state.penalty_weight = 1

        use_skill_weights = st.checkbox( f"Use { st.session_state.feature_label } weights" )
        if use_skill_weights:
            st.session_state.skill_weights = {}
            for skill_label in st.session_state.skill_labels:
                st.session_state.skill_weights[ skill_label ] = st.number_input(f"Weight for { skill_label }", value=1.0)
        else:
            st.session_state.skill_weights = None

        define_candidates_mutual_exclusion = st.checkbox( f"Is there paires of { st.session_state.left_label } who can't be assigned to the same { st.session_state.right_label }" )
        if define_candidates_mutual_exclusion:
            nb_paires = st.number_input( "How many paires ?", 1 )
            st.session_state.candidates_mutual_exclusion = [ [ None, None ] for _ in range( nb_paires ) ]
            for paire in range( nb_paires ):
                exclusion_cols = st.columns( 2 )
                for id, col in enumerate( exclusion_cols ):
                    with col:
                        st.session_state.candidates_mutual_exclusion[ paire ][ id ] = st.selectbox( f"{ st.session_state.left_label } for the paire { paire + 1 }", st.session_state.left_entities, index=id )
        else:
            st.session_state.candidates_mutual_exclusion = None


        navigation_buttons()
        st.stop()

    # ==================================================
    # STEP 7 — Solver
    # ==================================================
    if step == 7:
        st.header( "Choose solver" )

        solver_group = ASSIGNMENT_SOLVER_GROUPS[ "skills" ]
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
        st.divider()
        st.subheader( "AI explanation" )

        if st.button( "Generate explanation by AI" ):
            session = OptimizationSession(
                problem_family="Assignment",
                problem_type=st.session_state.assignment_type,
                problem_variant="generic",
                steps=st.session_state.journey,
                data_description=describe_data_source(
                    st.session_state.data_source
                ),
                solver_name=st.session_state.solver.label,
                result_summary=f"{ len( solution ) } assignments",
                config_summary=f"Objective: maximize",
            )

            st.session_state.ai_summary = generate_ai_summary( session )
            st.markdown( st.session_state.ai_summary )

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

        navigation_buttons( show_next=False )
        st.stop()
