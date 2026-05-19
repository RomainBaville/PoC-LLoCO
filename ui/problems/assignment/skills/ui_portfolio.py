# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025-2026 AKKODIS.
# SPDX-FileContributor: Romain Baville

import streamlit as st
from ui.utils import navigation_buttons


def render(step: int):
    st.header("Skill portfolio selection")

    st.info(
        "This variant selects a subset of people whose combined "
        "skills cover all required competencies."
    )

    navigation_buttons(show_next=False)
    st.stop()
