# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025-2026 AKKODIS.
# SPDX-FileContributor: Romain Baville

import io
import json
import zipfile
from collections.abc import Callable, MutableMapping
from typing import Any

import streamlit as st

from infrastructure.registry import DATA_SOURCE_REGISTRY
from llm.client import ask_llm_request
from llm.session_model import OptimizationSession
from llm.session_prompt import build_session_summary_prompt

SessionState = MutableMapping[ str, Any ]


def select_problem( session_state: SessionState, problem_key: str ) -> None:
    """Set the problem key in the session state and go to the next step.

    Args:
        session_state (SessionState): The session state.
        problem_key (str): The problem key.
    """
    session_state.problem_key = problem_key
    session_state.step = 1


# --------------------------------------------------
# Navigation helpers
# --------------------------------------------------


def next_step( session_state: SessionState ) -> None:
    """Go to the next step of the state.

    Args:
        session_state (SessionState): The session state.
    """
    session_state.step += 1


def back_step( session_state: SessionState ) -> None:
    """Go to the previous step of the state.

    Args:
        session_state (SessionState): The session state.
    """
    if session_state.step > 0:
        session_state.step -= 1


def reset_app( session_state: SessionState ) -> None:
    """Reste the session state and go to the first step.

    Args:
        session_state (SessionState): The session state.
    """
    session_state.clear()
    session_state.step = 0
    session_state.problem_key = None


def navigation_buttons(
    session_state: SessionState,
    show_back: bool = True,
    show_next: bool = True,
    show_close: bool = True,
) -> None:
    """Create the navigation buttons on the session state.

    Args:
        session_state (SessionState): The session state.
        show_back (bool): True if the back button is available.
            Defaults to True.
        show_next (bool): True if the next button is available.
            Defaults to True.
        show_close (bool): True if the reste button is available.
            Defaults to True.
    """
    cols = st.columns( 3 )
    names: tuple[ str, str, str ] = ( "Back", "Next", "Close" )
    show: tuple[ bool, bool, bool ] = ( not show_back, not show_next, not show_close )
    functions: tuple[ Callable ] = ( back_step, next_step, reset_app )

    for id, col in enumerate( cols ):
        with col:
            st.button( names[ id ], on_click=functions[ id ], args=( session_state, ), disabled=show[ id ] )


# --------------------------------------------------
# Optimization journey helpers
# --------------------------------------------------


def log_step( session_state: SessionState, message: str ) -> None:
    """Write a message in the session state journey.

    Args:
        session_state (SessionState): The session state.
        message (str): The message to write in the journey.
    """
    session_state.journey.append( message )


def describe_data_source( data_source_key: str ) -> str:
    """Get the description of the data source.

    Args:
        data_source_key (str): The key to acces the data source description.

    Returns:
        str: The data source description.
    """
    ds = DATA_SOURCE_REGISTRY.get( data_source_key )
    return ds.label if ds else str( data_source_key )


# --------------------------------------------------
# AI summary helper
# --------------------------------------------------


def generate_ai_summary( session: OptimizationSession ) -> str:
    """Generate the summary of the problem resolution.

    Args:
        session (OptimizationSession): All the data of the resolution to create the summary.

    Returns:
        str: The summary.
    """
    prompt = build_session_summary_prompt( session )
    return ask_llm_request( prompt )


# --------------------------------------------------
# Results export helper
# --------------------------------------------------


def build_results_zip(
    solution_rows: list[ dict[ str, str ] ],
    ai_summary: str,
    metadata: dict,
) -> bytes:
    """Build a ZIP file containing: solution.csv, ai_summary.txt and metadata.json.

    Args:
        solution_rows (list[dict[str, str]]): The solution of the problem.
        ai_summary (str): The summary of the problem.
        metadata (dict): The data of the problem.

    Returns:
        bytes: A zip file with the data, the summary and the resulte of the problem.
    """
    buffer = io.BytesIO()

    with zipfile.ZipFile( buffer, mode="w", compression=zipfile.ZIP_DEFLATED ) as zf:

        # -----------------------------
        # Solution CSV
        # -----------------------------
        if solution_rows:
            headers = solution_rows[ 0 ].keys()
            csv_content = ",".join( headers ) + "\n"
            csv_content += "\n".join( ",".join( str( row[ h ] ) for h in headers ) for row in solution_rows )
            zf.writestr( "solution.csv", csv_content )

        # -----------------------------
        # AI Summary
        # -----------------------------
        zf.writestr( "ai_summary.txt", ai_summary )

        # -----------------------------
        # Metadata
        # -----------------------------
        zf.writestr( "metadata.json", json.dumps( metadata, indent=2 ) )

    buffer.seek( 0 )
    return buffer.read()
