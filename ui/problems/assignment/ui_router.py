# SPDX-License-Identifier: Apache-2.0
import streamlit as st
from importlib import import_module

from ui.problems.assignment.registry import ASSIGNMENT_VARIANTS
from ui.utils import navigation_buttons


def render_assignment(step: int):

    # --------------------------------------------
    # STEP 1 — Select assignment variant
    # --------------------------------------------
    if step == 1:
        st.header("Choose assignment type")

        for variant in ASSIGNMENT_VARIANTS.values():
            if st.button(variant.label):
                st.session_state.assignment_variant = variant.key
                st.session_state.step += 1
            st.caption(variant.description)

        navigation_buttons(show_next=False)
        st.stop()

    # --------------------------------------------
    # Delegate to variant UI
    # --------------------------------------------
    variant_key = st.session_state.assignment_variant
    variant = ASSIGNMENT_VARIANTS.get(variant_key)

    if not variant:
        st.error("Unknown assignment variant")
        st.stop()

    module_path, fn_name = variant.render_fn.rsplit(".", 1)
    module = import_module(module_path)
    getattr(module, fn_name)(step)
