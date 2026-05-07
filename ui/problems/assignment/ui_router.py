# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025-2026 AKKODIS.
# SPDX-FileContributor: Romain Baville

import streamlit as st
from importlib import import_module

from ui.utils import navigation_buttons
from ui.problems.assignment.registry import ASSIGNMENT_TYPES
from infrastructure.registry import DATA_SOURCE_REGISTRY


def render_assignment(step: int):

    # ==================================================
    # STEP 1 — Assignment TYPE
    # ==================================================
    if step == 1:
        st.header("Choose assignment problem type")

        for atype in ASSIGNMENT_TYPES.values():
            if st.button(atype.label):
                st.session_state.assignment_type = atype.key
                st.session_state.step += 1

            st.caption(atype.description)

        navigation_buttons(show_next=False)
        st.stop()

    # ==================================================
    # STEP 2 — Assignment VARIANT
    # ==================================================
    if step == 2:
        atype = ASSIGNMENT_TYPES.get(st.session_state.assignment_type)
        if not atype:
            st.error("Unknown assignment type")
            st.stop()

        registry = import_module(atype.registry_module)
        variants = registry.VARIANTS

        st.header(f"{atype.label} — Choose formulation")

        for variant in variants.values():
            if st.button(variant.label):
                st.session_state.assignment_variant = (
                    f"{atype.key}_{variant.key}"
                )
                st.session_state.step += 1

            st.caption(variant.description)

        navigation_buttons(show_next=False)
        st.stop()

    # ==================================================
    # STEP 3 — Data source
    # ==================================================
    if step == 3:
        st.header("Choose your data format")

        for ds in DATA_SOURCE_REGISTRY.values():
            if st.button(ds.label):
                st.session_state.data_source = ds.key
                st.session_state.step += 1

            st.caption(ds.description)

        navigation_buttons(show_next=False)
        st.stop()

    # ==================================================
    # Delegate to VARIANT UI
    # ==================================================
    atype = ASSIGNMENT_TYPES.get(st.session_state.assignment_type)
    if not atype:
        st.error("Invalid assignment type")
        st.stop()

    registry = import_module(atype.registry_module)
    variants = registry.VARIANTS

    try:
        _, variant_key = st.session_state.assignment_variant.split("_", 1)
    except Exception:
        st.error("Invalid assignment variant")
        st.stop()

    variant = variants.get(variant_key)
    if not variant:
        st.error("Unknown assignment variant")
        st.stop()

    module_path, fn_name = variant.render_fn.rsplit(".", 1)
    module = import_module(module_path)
    getattr(module, fn_name)(step)
