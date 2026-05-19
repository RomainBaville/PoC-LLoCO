# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025-2026 AKKODIS.
# SPDX-FileContributor: Romain Baville

import streamlit as st
from ui.utils import navigation_buttons


def render(step: int):
    st.header("Team formation by skills")

    st.info(
        "This variant forms multi-person teams so that skills "
        "are covered collectively."
    )

    navigation_buttons(show_next=False)
    st.stop()