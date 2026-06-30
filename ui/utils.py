# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025-2026 AKKODIS.
# SPDX-FileContributor: Romain Baville

import io
import json
import zipfile

import streamlit as st

from infrastructure.registry import DATA_SOURCE_REGISTRY
from llm.client import ask_llm_request
from llm.session_model import OptimizationSession
from llm.session_prompt import build_session_summary_prompt

# --------------------------------------------------
# Navigation helpers
# --------------------------------------------------


def next_step():
    st.session_state.step += 1


def prev_step():
    if st.session_state.step > 0:
        st.session_state.step -= 1


def reset_app():
    st.session_state.clear()
    st.session_state.step = 0


def navigation_buttons( show_back=True, show_next=True, show_close=True ):
    cols = st.columns( 3 )

    if show_back:
        with cols[ 0 ]:
            st.button( "Back", on_click=prev_step )

    if show_next:
        with cols[ 1 ]:
            st.button( "Next", on_click=next_step )

    if show_close:
        with cols[ 2 ]:
            st.button( "Close", on_click=reset_app )


# --------------------------------------------------
# Optimization journey helpers
# --------------------------------------------------


def init_journey():
    if "journey" not in st.session_state:
        st.session_state.journey = []


def log_step( message: str ):
    init_journey()
    st.session_state.journey.append( message )


def describe_data_source( data_source_key: str ) -> str:
    ds = DATA_SOURCE_REGISTRY.get( data_source_key )
    return ds.label if ds else str( data_source_key )


# --------------------------------------------------
# AI summary helper
# --------------------------------------------------


def generate_ai_summary( session: OptimizationSession ) -> str:
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
    """Build a ZIP file containing:
    - solution.csv
    - ai_summary.txt
    - metadata.json
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
