# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025-2026 AKKODIS.
# SPDX-FileContributor: Romain Baville
import sys
from pathlib import Path

# --- make project root importable ---
ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT_DIR))

import streamlit as st
from ui.utils import navigation_buttons
from ui.problems.assignment_ui import render_assignment_step
from llm.summary import build_onboarding_prompt
from llm.client import ask_llm_request


# --------------------------------------------------
# App setup
# --------------------------------------------------
st.set_page_config(page_title="Optimization Playground", layout="wide")
st.title("Optimization Playground")


# ==================================================
# STEP -1 – LLM onboarding / explanation
# ==================================================
if "step" not in st.session_state:
    st.session_state.step = -1

if "problem_type" not in st.session_state:
    st.session_state.problem_type = None

if st.session_state.step == -1:
    st.header("Describe your problem")

    user_description = st.text_area(
        "Explain in plain language what you want to optimize",
        height=150,
        placeholder="Example: I want to assign employees to projects based on their skills...",
    )

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Explain how to use the tool"):

            with st.spinner("Analyzing your problem..."):
                prompt = build_onboarding_prompt(user_description)
                explanation = ask_llm_request(prompt)

            st.subheader("How the tool will help you")
            st.markdown(explanation)

    with col2:
        navigation_buttons( show_back=False, show_close=False )

    st.stop()


# --------------------------------------------------
# STEP 0 — Problem selection
# --------------------------------------------------
if st.session_state.step == 0:
    st.header("Choose a problem type")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Assignment problem"):
            st.session_state.problem_type = "assignment"
            st.session_state.step = 1

    with col2:
        if st.button("Other problem"):
            st.session_state.problem_type = "traveler"
            st.session_state.step = 1

    st.stop()


# --------------------------------------------------
# Delegate to problem-specific UI
# --------------------------------------------------
if st.session_state.problem_type == "assignment":
    render_assignment_step(st.session_state.step)

else:
    st.error("Unknown problem type")
    navigation_buttons( show_back=False, show_next=False )
