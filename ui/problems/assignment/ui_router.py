# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025-2026 AKKODIS.
# SPDX-FileContributor: Romain Baville

import streamlit as st
from importlib import import_module

from ui.utils import navigation_buttons
from ui.problems.assignment.registry import ASSIGNMENT_VARIANTS
from infrastructure.registry import DATA_SOURCE_REGISTRY


def render_assignment(step: int):

    # ==================================================
    # STEP 1 — Assignment variant selection
    # ==================================================
    if step == 1:
        st.header("Choose assignment type")

        for variant in ASSIGNMENT_VARIANTS.values():
            if st.button(variant.label):
                st.session_state.assignment_variant = variant.key
                st.session_state.step += 1

            st.caption(variant.description)

        navigation_buttons(show_next=False)
        st.stop()

    # ==================================================
    # STEP 2 — Data source selection
    # ==================================================
    if step == 2:
        st.header("Choose your data format")

        for ds in DATA_SOURCE_REGISTRY.values():
            if st.button(ds.label):
                st.session_state.data_source = ds.key
                st.session_state.step += 1

            st.caption(ds.description)

        navigation_buttons(show_next=False)
        st.stop()

    # ==================================================
    # Delegate to variant-specific UI
    # ==================================================
    variant_key = st.session_state.assignment_variant
    variant = ASSIGNMENT_VARIANTS.get(variant_key)

    if not variant:
        st.error("Unknown assignment variant")
        st.stop()

    module_path, fn_name = variant.render_fn.rsplit(".", 1)
    module = import_module(module_path)
    render_fn = getattr(module, fn_name)

    render_fn(step)
