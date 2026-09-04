# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025-2026 AKKODIS.
# SPDX-FileContributor: Romain Baville

from collections.abc import Callable

import streamlit as st
from streamlit.runtime.state.session_state_proxy import SessionStateProxy


# --------------------------------------------------
# Selection functions
# --------------------------------------------------
def select_data_source( session_state: SessionStateProxy, data_source_key: str ) -> None:
    """Set the data source key in the session state.

    Args:
        session_state (SessionStateProxy): The session state.
        data_source_key (str): The data source key.
    """
    session_state.data_source = data_source_key


def select_problem( session_state: SessionStateProxy, problem_key: str ) -> None:
    """Set the problem key in the session state and go to the next step.

    Args:
        session_state (SessionStateProxy): The session state.
        problem_key (str): The problem key.
    """
    session_state.problem_key = problem_key
    session_state.step = 1


def select_solver( session_state: SessionStateProxy, solver_key: str ) -> None:
    """Set the solver key in the session state and go to the next step.

    Args:
        session_state (SessionStateProxy): The session state.
        solver_key (str): The solver key.
    """
    session_state.solver_key = solver_key
    session_state.journey[ "Solver" ] = solver_key
    session_state.step += 1


# --------------------------------------------------
# Navigation functions
# --------------------------------------------------
def next_step( session_state: SessionStateProxy ) -> None:
    """Go to the next step of the state.

    Args:
        session_state (SessionStateProxy): The session state.
    """
    session_state.step += 1


def back_step( session_state: SessionStateProxy ) -> None:
    """Go to the previous step of the state.

    Args:
        session_state (SessionStateProxy): The session state.
    """
    if session_state.step >= 0:
        session_state.step -= 1


def reset_app( session_state: SessionStateProxy ) -> None:
    """Reste the session state and go to the first step.

    Args:
        session_state (SessionStateProxy): The session state.
    """
    session_state.clear()


def navigation_buttons(
    session_state: SessionStateProxy,
    show_back: bool = True,
    show_next: bool = True,
    show_close: bool = True,
) -> None:
    """Create the navigation buttons on the session state.

    Args:
        session_state (SessionStateProxy): The session state.
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
    functions: tuple[ Callable[ [ SessionStateProxy ], None ],
                      Callable[ [ SessionStateProxy ], None ],
                      Callable[ [ SessionStateProxy ], None ] ] = ( back_step, next_step, reset_app )

    for id, col in enumerate( cols ):
        with col:
            st.button( names[ id ], on_click=functions[ id ], args=( session_state, ), disabled=show[ id ] )
