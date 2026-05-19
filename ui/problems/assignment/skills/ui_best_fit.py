# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025-2026 AKKODIS.
# SPDX-FileContributor: Romain Baville

import streamlit as st
from ui.utils import navigation_buttons


def render(step: int):
    st.header("Best-fit skill matching")

    st.info(
        "This variant matches people to projects by maximizing "
        "overall skill compatibility instead of enforcing hard requirements."
    )

    navigation_buttons(show_next=False)
    st.stop()
