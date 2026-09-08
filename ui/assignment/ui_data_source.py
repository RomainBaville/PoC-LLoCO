# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025-2026 AKKODIS.
# SPDX-FileContributor: Romain Baville

from collections.abc import Callable

import streamlit as st
from streamlit.runtime.state.session_state_proxy import SessionStateProxy
from streamlit.runtime.uploaded_file_manager import UploadedFile

from ui.utils import navigation_buttons


def two_csv( session_state: SessionStateProxy ) -> None:
    """Configure the interface to load the two csv file.

    Args:
        session_state (SessionStateProxy): The session state.
    """
    st.subheader( "Upload CSV files" )
    show_next: bool = False

    left_file: UploadedFile | None = st.file_uploader(
        f"{ session_state.left_entities_type } dataset",
        type=[ "csv" ],
        key="left_csv",
        disabled=session_state.lock_data_source
    )

    right_file: UploadedFile | None = st.file_uploader(
        f"{ session_state.right_entities_type } dataset",
        type=[ "csv" ],
        key="right_csv",
        disabled=session_state.lock_data_source
    )

    if isinstance( left_file, UploadedFile ) and isinstance( right_file, UploadedFile ):
        session_state.left_cols, session_state.left_rows = session_state.data_source.loader_fn( left_file )
        session_state.right_cols, session_state.right_rows = session_state.data_source.loader_fn( right_file )
        show_next = True
    else:
        show_next = False

    if not session_state.lock_data_source:
        navigation_buttons( session_state, show_next=show_next )


UI_ASSIGNMENT_DATA_SOURCE_LOADER: dict[ str, Callable[ [ SessionStateProxy ], None ] ] = {
    "csv_two_tables": two_csv
}
