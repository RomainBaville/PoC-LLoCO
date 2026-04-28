# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025-2026 AKKODIS.
# SPDX-FileContributor: Romain Baville

import streamlit as st


def next_step():
    st.session_state.step += 1


def prev_step():
    if st.session_state.step > 0:
        st.session_state.step -= 1


def reset_app():
    st.session_state.clear()
    st.session_state.step = 0


def navigation_buttons(show_back=True, show_next=True, show_close=True):
    cols = st.columns(3)

    if show_back:
        with cols[0]:
            st.button("Back", on_click=prev_step)

    if show_next:
        with cols[1]:
            st.button("Next", on_click=next_step)

    if show_close:
        with cols[2]:
            st.button("Close", on_click=reset_app)

