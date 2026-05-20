# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025-2026 AKKODIS.

import sys
from pathlib import Path
from importlib import import_module

ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT_DIR))

import streamlit as st

import ui.theme as theme
from ui.sidebar import render as render_sidebar
from ui.utils import build_results_zip, generate_ai_summary, log_step
from ui.problems.assignment.skills.builder import build_problem
from infrastructure.registry import DATA_SOURCE_REGISTRY
from llm.onboarding_prompt import build_onboarding_prompt
from llm.client import ask_llm_request
from llm.session_model import OptimizationSession
from solvers.assignment.registry import ASSIGNMENT_SOLVER_GROUPS

_DATA_DIR = "data"
_LOADER_KEY = "csv_two_tables"

# ── Page setup ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Optimization Playground",
    page_icon="⚙️",
    layout="wide",
)
theme.inject()

# ── Session defaults ───────────────────────────────────────────────────────
st.session_state.setdefault("solution", None)
st.session_state.setdefault("ai_summary", None)
st.session_state.setdefault("journey", [])
st.session_state.setdefault("onboarding_result", None)
st.session_state.setdefault("solve_error", None)

# ── Sidebar (configuration) ────────────────────────────────────────────────
solve_triggered = render_sidebar()

# ── Solve logic ────────────────────────────────────────────────────────────
if solve_triggered:
    st.session_state.solve_error = None
    st.session_state.solution = None
    st.session_state.ai_summary = None

    try:
        loader = DATA_SOURCE_REGISTRY[_LOADER_KEY].loader_factory()
        _, left_rows = loader.load(f"{_DATA_DIR}/{st.session_state.left_csv}")
        _, right_rows = loader.load(f"{_DATA_DIR}/{st.session_state.right_csv}")

        problem, left_labels = build_problem(st.session_state, left_rows, right_rows)

        solver_group = ASSIGNMENT_SOLVER_GROUPS[st.session_state.assignment_type]
        solver_reg = import_module(solver_group.registry_module)
        solver_def = solver_reg.SOLVERS[st.session_state.solver_key]

        with st.spinner("Résolution en cours…"):
            solution = solver_def.solver_class().solve(problem)

        _, variant_key = st.session_state.assignment_variant.split("_", 1)
        variant_reg = import_module(
            f"ui.problems.assignment.{st.session_state.assignment_type}.registry"
        )
        variant_def = variant_reg.VARIANTS[variant_key]

        st.session_state.solution = solution
        st.session_state.left_labels = left_labels
        st.session_state.solution_rows = [
            {
                st.session_state.left_label: left_labels[l],
                st.session_state.right_label: r,
            }
            for l, r in solution.items()
        ]
        st.session_state.solver_label = solver_def.label
        st.session_state.variant_label = variant_def.label

        log_step(
            f"Résolu avec {solver_def.label} — "
            f"{len(solution)} {st.session_state.left_label.lower()} assigné(s)."
        )

        session = OptimizationSession(
            problem_family="Assignment",
            problem_variant=st.session_state.assignment_variant,
            steps=st.session_state.journey,
            data_description="Source : CSV",
            solver_name=solver_def.label,
            solver_type="Constraint Programming",
            result_summary=(
                f"{len(solution)} {st.session_state.left_label.lower()} assigné(s)."
            ),
        )
        with st.spinner("Analyse IA en cours…"):
            st.session_state.ai_summary = generate_ai_summary(session)

    except NotImplementedError:
        st.session_state.solve_error = (
            "Ce variant n'est pas encore supporté par le solver sélectionné."
        )
    except RuntimeError as exc:
        st.session_state.solve_error = f"Échec de la résolution : {exc}"

    st.rerun()


# ── Main area ──────────────────────────────────────────────────────────────

def _render_onboarding():
    theme.hero(
        "Optimization Playground",
        "Décrivez votre problème, configurez-le dans la barre latérale, et résolvez.",
    )

    if st.session_state.get("solve_error"):
        st.error(st.session_state.solve_error)
        st.markdown("")

    st.markdown("### Analyser votre problème avec l'IA")
    user_desc = st.text_area(
        "Description",
        height=110,
        placeholder=(
            "Exemple : Je veux affecter des employés à des projets "
            "en fonction de leurs compétences…"
        ),
        label_visibility="collapsed",
    )

    if st.button("Analyser", type="primary"):
        if not user_desc.strip():
            st.warning("Saisissez une description avant d'analyser.")
        else:
            with st.spinner("Analyse en cours…"):
                prompt = build_onboarding_prompt(user_desc)
                st.session_state.onboarding_result = ask_llm_request(prompt)

    if st.session_state.get("onboarding_result"):
        st.markdown("**Guidage IA**")
        theme.ai_block(st.session_state.onboarding_result)

    st.markdown("")
    st.markdown(
        '<p class="ui-hint">→ Configurez votre problème dans la barre latérale pour commencer.</p>',
        unsafe_allow_html=True,
    )


def _render_results():
    solution = st.session_state.solution

    theme.hero(
        f"{len(solution)} {st.session_state.left_label.lower()} assigné(s)",
        f"{st.session_state.variant_label}  ·  {st.session_state.solver_label}",
    )

    col1, col2, col3 = st.columns(3)
    col1.metric(
        f"{st.session_state.left_label} assignés",
        f"{len(solution)} / {len(st.session_state.solution_rows)}",
    )
    col2.metric("Solveur", st.session_state.solver_label)
    col3.metric("Formulation", st.session_state.variant_label)

    st.markdown("")

    # Dispatch to variant-specific renderer
    _, variant_key = st.session_state.assignment_variant.split("_", 1)
    assignment_type = st.session_state.assignment_type
    variant_module = import_module(
        f"ui.problems.assignment.{assignment_type}.ui_{variant_key}"
    )
    variant_module.render_results(solution, st.session_state)

    # AI summary
    if st.session_state.get("ai_summary"):
        st.markdown("---")
        st.markdown("### Analyse IA")
        theme.ai_block(st.session_state.ai_summary)

        zip_bytes = build_results_zip(
            solution_rows=st.session_state.solution_rows,
            ai_summary=st.session_state.ai_summary,
            metadata={
                "solver": st.session_state.solver_label,
                "variant": st.session_state.assignment_variant,
            },
        )
        st.markdown("")
        st.download_button(
            "⬇  Télécharger les résultats (.zip)",
            data=zip_bytes,
            file_name="optimization_results.zip",
            mime="application/zip",
        )


if st.session_state.solution is None:
    _render_onboarding()
else:
    _render_results()
