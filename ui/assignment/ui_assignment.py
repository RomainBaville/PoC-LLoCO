# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025-2026 AKKODIS.
# SPDX-FileContributor: Romain Baville

import streamlit as st
from streamlit.runtime.state.session_state_proxy import SessionStateProxy

from infrastructure.registry import DATA_SOURCE_REGISTRY
from llm.summary.summary_context import OptimizationSession
from llm.summary.summary_prompt import build_session_summary_prompt
from llm.summary.utils import build_results_zip
from solvers.assignment.registry import ASSIGNEMENT_SOLVERS
from ui.assignment.builder import build_entities_labels, build_problem
from ui.assignment.constraints.ui_logicals_constraints import logicals_constraints
from ui.assignment.constraints.ui_quantities_constraints import quantities_constraints
from ui.assignment.score.ui_matching import map_matching, matching_constraints, matching_strategy
from ui.assignment.score.ui_ressources import map_ressources, ressources_constraints, ressources_strategy
from ui.assignment.ui_data_source import UI_ASSIGNMENT_DATA_SOURCE_LOADER
from ui.utils import navigation_buttons, select_data_source, select_solver


def render( session_state: SessionStateProxy ) -> None:
    """Define the user interface for assignment problem.

    Args:
        session_state (SessionStateProxy): The session state.
    """
    # Assignment session defaults
    session_state.setdefault( "data_source", None)
    session_state.setdefault( "solver", None )

    # ==================================================
    # STEP 1 — Naming entities types
    # ==================================================
    if session_state.step >= 1:
        st.header( "Define your left and right entities types" )
        if session_state.step == 1:
            session_state.lock_naming = False
            if "Score computation" in session_state.journey:
                del ( session_state.journey[ "Score computation" ] )
                st.rerun()
        else:
            session_state.lock_naming = True

        session_state.left_entities_type = st.text_input(
            "Set the type of the left entity (e.g. Candidates)", "Candidates", disabled=session_state.lock_naming
        )
        session_state.journey[ "Left entities type" ] = session_state.left_entities_type

        session_state.right_entities_type = st.text_input(
            "Set the type of the right entity (e.g. Targets)", "Targets", disabled=session_state.lock_naming
        )
        session_state.journey[ "Right entities type" ] = session_state.right_entities_type

        if not session_state.lock_naming:
            navigation_buttons( session_state, show_back=False )

    # ==================================================
    # STEP 2 — Score parameters
    # ==================================================
    if session_state.step >= 2:
        st.header(
            f"How to compute the score to associate { session_state.left_entities_type }  " \
            f" and { session_state.right_entities_type }"
        )
        if session_state.step == 2:
            session_state.lock_score_parameters = False
            if "Data source" in session_state.journey:
                del ( session_state.journey[ "Data source" ] )
                st.rerun()
        else:
            session_state.lock_score_parameters = True

        show_next: bool = False
        session_state.use_matching = st.checkbox(
            "Use a scoring optimization involving a score computation from a matching between left and right " \
            "variables sharing the same label (e.g. python_level, english_level, ...)",
            disabled=session_state.lock_score_parameters
        )

        session_state.use_ressources = st.checkbox(
            "Use a scoring optimization involving a score computation from an addition of the left entities" \
            " ressources (e.g. Salary, years_of_experiances, ...)",
            disabled=session_state.lock_score_parameters
        )

        if session_state.use_matching or session_state.use_ressources:
            show_next = True
            if not session_state.use_matching:
                session_state.journey[ "Score computation" ] = "Additioning ressources"
            elif not session_state.use_ressources:
                session_state.journey[ "Score computation" ] = "Matching ressources"
            else:
                session_state.journey[ "Score computation" ] = "Matching ressouces and additioning ressources"

        if not session_state.lock_score_parameters:
            navigation_buttons( session_state, show_next=show_next )

    # ==================================================
    # STEP 3 — Data source
    # ==================================================
    if session_state.step >= 3:
        st.header( "Choose your data format" )

        if session_state.step == 3:
            session_state.lock_data_source = False
            if "Left labels" in session_state.journey:
                del ( session_state.journey[ "Left labels" ] )
                st.rerun()
            if "Right labels" in session_state.journey:
                del ( session_state.journey[ "Right labels" ] )
                st.rerun()
            if "Matching variables" in session_state.journey:
                del ( session_state.journey[ "Matching variables" ] )
                st.rerun()
            if "Ressources variables" in session_state.journey:
                del ( session_state.journey[ "Ressources variables" ] )
                st.rerun()
        else:
            session_state.lock_data_source = True

        for ds in DATA_SOURCE_REGISTRY:
            st.button(
                ds.label,
                on_click=select_data_source,
                args=( session_state, ds ),
                disabled=session_state.lock_data_source
            )
            st.caption( ds.description )

        if session_state.data_source is not None:
            UI_ASSIGNMENT_DATA_SOURCE_LOADER[ session_state.data_source.key ]( session_state )

    # ==================================================
    # STEP 4 — Mapping
    # ==================================================
    if session_state.step >= 4:
        st.header( "Map your data" )
        if session_state.step == 4:
            session_state.lock_mapping = False
            if "Matching objective" in session_state.journey:
                del ( session_state.journey[ "Matching objective" ] )
                st.rerun()
            if "Reward function" in session_state.journey:
                del ( session_state.journey[ "Reward function" ] )
                st.rerun()
            if "Penalty function" in session_state.journey:
                del ( session_state.journey[ "Penalty function" ] )
                st.rerun()
            if "Matching weights" in session_state.journey:
                del ( session_state.journey[ "Matching weights" ] )
                st.rerun()
            if "Ressources objectives" in session_state.journey:
                del ( session_state.journey[ "Ressources objectives" ] )
                st.rerun()
            if "Ressources weights" in session_state.journey:
                del ( session_state.journey[ "Ressources weights" ] )
                st.rerun()
        else:
            session_state.lock_mapping = True

        # -----------------------------
        # 1. Entities
        # -----------------------------
        st.subheader( "1. Identify entities" )

        session_state.left_entities_col_label = st.selectbox(
            f"Columns identifying { session_state.left_entities_type }",
            session_state.left_cols,
            disabled=session_state.lock_mapping
        )

        session_state.right_entities_col_label = st.selectbox(
            f"Column identifying { session_state.right_entities_type }",
            session_state.right_cols,
            disabled=session_state.lock_mapping
        )

        session_state.left_labels = build_entities_labels(
            session_state.left_entities_col_label, session_state.left_rows
        )
        session_state.journey[ "Left labels" ] = session_state.left_labels

        session_state.right_labels = build_entities_labels(
            session_state.right_entities_col_label, session_state.right_rows
        )
        session_state.journey[ "Right labels" ] = session_state.right_labels

        # -----------------------------
        # 2. Scoring variables
        # -----------------------------
        st.subheader( "2. Identify scoring variables" )
        if session_state.use_matching:
            map_matching( session_state )

        if session_state.use_ressources:
            map_ressources( session_state )

        if not session_state.lock_mapping:
            navigation_buttons( session_state )

    # ==================================================
    # STEP 5 — Strategy
    # ==================================================
    if session_state.step >= 5:
        st.header( "Score optimization strategy" )
        if session_state.step == 5:
            session_state.lock_strategy = False
            if "Multiple same assignment" in session_state.journey:
                del ( session_state.journey[ "Multiple same assignment" ] )
                st.rerun()
            if "Max right entities" in session_state.journey:
                del ( session_state.journey[ "Max right entities" ] )
                st.rerun()
            if "Min right entities" in session_state.journey:
                del ( session_state.journey[ "Min right entities" ] )
                st.rerun()
            if "Max left entities" in session_state.journey:
                del ( session_state.journey[ "Max left entities" ] )
                st.rerun()
            if "Min left entities" in session_state.journey:
                del ( session_state.journey[ "Min left entities" ] )
                st.rerun()
            if "Max same assignments" in session_state.journey:
                del ( session_state.journey[ "Max same assignments" ] )
                st.rerun()
            if "Min same assignments" in session_state.journey:
                del ( session_state.journey[ "Min same assignments" ] )
                st.rerun()
            if "Max right assignments" in session_state.journey:
                del ( session_state.journey[ "Max right assignments" ] )
                st.rerun()
            if "Min right assignments" in session_state.journey:
                del ( session_state.journey[ "Min right assignments" ] )
                st.rerun()
            if "Max left assignments" in session_state.journey:
                del ( session_state.journey[ "Max left assignments" ] )
                st.rerun()
            if "Min left assignments" in session_state.journey:
                del ( session_state.journey[ "Min left assignments" ] )
                st.rerun()
            if "Left mutual exclusions" in session_state.journey:
                del ( session_state.journey[ "Left mutual exclusions" ] )
                st.rerun()
            if "Right mutual exclusions" in session_state.journey:
                del ( session_state.journey[ "Right mutual exclusions" ] )
                st.rerun()
            if "Implications" in session_state.journey:
                del ( session_state.journey[ "Implications" ] )
                st.rerun()
            if "Matching max vals" in session_state.journey:
                del ( session_state.journey[ "Matching max vals" ] )
                st.rerun()
            if "Matching min vals" in session_state.journey:
                del ( session_state.journey[ "Matching min vals" ] )
                st.rerun()
            if "Constraints max vals" in session_state.journey:
                del ( session_state.journey[ "Constraints max vals" ] )
                st.rerun()
            if "Constraints min vals" in session_state.journey:
                del ( session_state.journey[ "Constraints min vals" ] )
                st.rerun()
            if "Constraints max global vals" in session_state.journey:
                del ( session_state.journey[ "Constraints max global vals" ] )
                st.rerun()
            if "Constraints min global vals" in session_state.journey:
                del ( session_state.journey[ "Constraints min global vals" ] )
                st.rerun()
        else:
            session_state.lock_strategy = True

        if session_state.use_matching:
            matching_strategy( session_state )

        if session_state.use_ressources:
            ressources_strategy( session_state )

        if not session_state.lock_strategy:
            navigation_buttons( session_state )

    # ==================================================
    # STEP 6 — Constraints
    # ==================================================
    if session_state.step >= 6:
        st.header( "Define constraints" )
        if session_state.step == 6:
            session_state.lock_constraints = False
            if "Solver" in session_state.journey:
                del ( session_state.journey[ "Solver" ] )
                st.rerun()
        else:
            session_state.lock_constraints = True

        # -----------------------------
        # 1. Assignment constraints
        # -----------------------------
        st.subheader( "1. Assignment constraints" )

        session_state.multiple_same_assignment = st.checkbox(
            f"{ session_state.left_entities_type } can be assigned multiple " \
            f"time to the same { session_state.right_entities_type } ?",
            value=True, disabled=session_state.lock_constraints
        )
        session_state.journey[ "Multiple same assignment" ] = session_state.multiple_same_assignment

        session_state.use_quantities_constraints = st.checkbox(
            "Is there quantities constraints in the problem (e.g. max number of employees per project)",
            disabled=session_state.lock_constraints
        )
        session_state.use_logicals_constraints = st.checkbox(
            "Is there logicals constraints in the problem " \
            "(e.g. if employee A is assigned to project I then employee B is assigned to project II)",
            disabled=session_state.lock_constraints
        )

        if session_state.use_quantities_constraints:
            quantities_constraints( session_state )
        else:
            if "Max right entities" in session_state.journey:
                del ( session_state.journey[ "Max right entities" ] )
                st.rerun()
            if "Min right entities" in session_state.journey:
                del ( session_state.journey[ "Min right entities" ] )
                st.rerun()
            if "Max left entities" in session_state.journey:
                del ( session_state.journey[ "Max left entities" ] )
                st.rerun()
            if "Min left entities" in session_state.journey:
                del ( session_state.journey[ "Min left entities" ] )
                st.rerun()
            if "Max same assignments" in session_state.journey:
                del ( session_state.journey[ "Max same assignments" ] )
                st.rerun()
            if "Min same assignments" in session_state.journey:
                del ( session_state.journey[ "Min same assignments" ] )
                st.rerun()
            if "Max right assignments" in session_state.journey:
                del ( session_state.journey[ "Max right assignments" ] )
                st.rerun()
            if "Min right assignments" in session_state.journey:
                del ( session_state.journey[ "Min right assignments" ] )
                st.rerun()
            if "Max left assignments" in session_state.journey:
                del ( session_state.journey[ "Max left assignments" ] )
                st.rerun()
            if "Min left assignments" in session_state.journey:
                del ( session_state.journey[ "Min left assignments" ] )
                st.rerun()

        if session_state.use_logicals_constraints:
            logicals_constraints( session_state )
        else:
            if "Left mutual exclusions" in session_state.journey:
                del ( session_state.journey[ "Left mutual exclusions" ] )
                st.rerun()
            if "Right mutual exclusions" in session_state.journey:
                del ( session_state.journey[ "Right mutual exclusions" ] )
                st.rerun()
            if "Implications" in session_state.journey:
                del ( session_state.journey[ "Implications" ] )
                st.rerun()

        # -----------------------------
        # 2. Scoring variables constraints
        # -----------------------------
        st.subheader( "2. Scoring variables constraints" )
        if session_state.use_matching:
            matching_constraints( session_state )

        if session_state.use_ressources:
            ressources_constraints( session_state )

        if not session_state.lock_constraints:
            navigation_buttons( session_state )

    # ==================================================
    # STEP 7 — Solver
    # ==================================================
    if session_state.step >= 7:
        st.header( "Choose solver" )
        if session_state.step == 7:
            session_state.lock_solver = False
        else:
            session_state.lock_solver = True

        solver_cols = st.columns( len( ASSIGNEMENT_SOLVERS ) )
        for solver_col, solver in zip( solver_cols, ASSIGNEMENT_SOLVERS, strict=False ):
            with solver_col:
                st.button(
                    solver.label,
                    on_click=select_solver,
                    args=( session_state, solver ),
                    disabled=session_state.lock_solver
                )

        if not session_state.lock_solver:
            navigation_buttons( session_state, show_next=False )

    # ==================================================
    # STEP 8 — Solve
    # ==================================================
    if session_state.step == 8:
        problem = build_problem( session_state )

        # ---------------------------------
        # Solve
        # ---------------------------------
        if session_state.solver is not None:
            try:
                with st.spinner( "Optimizing..." ):
                    solution: dict[ str, list[ tuple[ str, int ] ] ] = session_state.solver.solver_fn( problem )

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

                    if session_state.multiple_same_assignment:
                        solution_row[ f"Number of assignments per { session_state.right_entities_type }"
                                     ] = nb_assignments

                    session_state.solution_rows.append( solution_row )

                st.success( "Solution computed" )
                st.table( session_state.solution_rows )
            except RuntimeError as e:
                st.error( e )

                navigation_buttons( session_state, show_next=False )
                st.stop()

        # ---------------------------------
        # AI explanation
        # ---------------------------------
        if session_state.model_info is not None:
            st.divider()
            st.subheader( "AI explanation" )
            session_state.summary = None
            if st.button( "Generate explanation by AI" ):
                session = OptimizationSession(
                    journey=session_state.journey,
                    user_desc=session_state.user_desc,
                    onboarding=session_state.onboarding,
                    result=solution
                )
                summary_prompt = build_session_summary_prompt( session )
                with st.spinner( "Summerize" ):
                    session_state.summary = session_state.model_info.ask_client( summary_prompt, session_state.model_info.name )
                st.markdown( session_state.summary )

            if session_state.summary is not None:
                zip_bytes = build_results_zip( summary=session_state.summary )
                st.download_button(
                    "Download results (ZIP)",
                    data=zip_bytes,
                    file_name="assignment_results.zip",
                    mime="application/zip"
                )

        navigation_buttons( session_state, show_next=False )
