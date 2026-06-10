# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025-2026 AKKODIS.

import os
import sys
from pathlib import Path
from importlib import import_module

ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT_DIR))

import streamlit as st

import ui.theme as theme
from ui.sidebar import render as render_sidebar
from ui.utils import build_results_zip, log_step
from ui.problems.assignment.skills.builder import build_problem
from ui.problems.assignment.registry import ASSIGNMENT_TYPES
from infrastructure.registry import DATA_SOURCE_REGISTRY
from llm.onboarding_prompt import build_onboarding_prompt
from llm.session_prompt import build_session_summary_prompt
from llm.client import ask_llm_request
from llm.session_model import OptimizationSession
from solvers.assignment.registry import ASSIGNMENT_SOLVER_GROUPS

_DATA_DIR = "data"
_LOADER_KEY = "csv_two_tables"


# ── Page setup ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Optimization Playground",
    page_icon="⚙️",
    layout="wide",
)
theme.inject()

# ── Session defaults ─────────────────────────────────────────────────────────
st.session_state.setdefault("config_validated", False)
st.session_state.setdefault("data_step", 1)
st.session_state.setdefault("solution", None)
st.session_state.setdefault("ai_summary", None)
st.session_state.setdefault("journey", [])
st.session_state.setdefault("onboarding_result", None)
st.session_state.setdefault("solve_error", None)
st.session_state.setdefault("analysis_done", False)
st.session_state.setdefault("analysis_recommendation", None)
# Config fields start as None — only populated after AI analysis
st.session_state.setdefault("problem_key", None)
st.session_state.setdefault("assignment_type", None)
st.session_state.setdefault("assignment_variant", None)

# ── Sidebar ──────────────────────────────────────────────────────────────────
render_sidebar()


# ── Problem configuration inference ─────────────────────────────────────────

def infer_problem_configuration(user_desc: str, ai_text: str | None = None) -> dict:
    """Deterministic keyword-based recommendation — no extra LLM call."""
    text = f"{user_desc}\n{ai_text or ''}".lower()

    assignment_keywords = [
        "assign", "affect", "affectation", "affecter", "assignment",
        "employee", "employé", "project", "projet", "skill", "compétence", "competence",
    ]
    if not any(w in text for w in assignment_keywords):
        return {}

    problem_key = "assignment"
    assignment_type = "skills"

    if any(w in text for w in ["coverage", "required", "requirement", "besoin", "couverture", "requis"]):
        variant_local = "coverage"
    elif any(w in text for w in ["best fit", "best_fit", "matching", "compatibility", "score", "compatibilité"]):
        variant_local = "best_fit"
    elif any(w in text for w in ["team", "équipe", "group", "groupe"]):
        variant_local = "team"
    elif any(w in text for w in ["portfolio", "selection", "budget", "sélection"]):
        variant_local = "portfolio"
    else:
        variant_local = "coverage"

    return {
        "problem_key": problem_key,
        "assignment_type": assignment_type,
        "variant_local": variant_local,
        "assignment_variant": f"{assignment_type}_{variant_local}",
    }


# ── Helpers ──────────────────────────────────────────────────────────────────

def _csv_files():
    if not os.path.isdir(_DATA_DIR):
        return []
    return sorted(f for f in os.listdir(_DATA_DIR) if f.endswith(".csv"))


def _load_columns(csv_file: str):
    loader = DATA_SOURCE_REGISTRY[_LOADER_KEY].loader_factory()
    cols, _ = loader.load(os.path.join(_DATA_DIR, csv_file))
    return cols


def _sanitize_multiselect(key: str, valid_pool: list):
    stored = st.session_state.get(key, [])
    valid = [c for c in stored if c in valid_pool]
    if stored != valid:
        st.session_state[key] = valid


def _sanitize_selectbox(key: str, valid_pool: list):
    if key in st.session_state and st.session_state[key] not in valid_pool:
        del st.session_state[key]


def _llm_ask(prompt: str) -> str:
    source = st.session_state.get("llm_source", "ollama")
    model_name = st.session_state.llm_model_name
    if source == "akkodis":
        from ui.akkodis_client import ask as akkodis_ask
        return akkodis_ask(prompt, model_name)
    else:
        import llm.client as _llm
        _llm.LLM_SERVER_URL = st.session_state.llm_url
        _llm.LLM_MODEL_NAME = model_name
        return ask_llm_request(prompt)


def _do_solve():
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
            problem_type=st.session_state.get("assignment_type", ""),
            problem_variant=st.session_state.assignment_variant,
            steps=st.session_state.journey,
            data_description="Source : CSV",
            solver_name=solver_def.label,
            result_summary=(
                f"{len(solution)} {st.session_state.left_label.lower()} assigné(s)."
            ),
        )
        if st.session_state.get("llm_model_name"):
            try:
                with st.spinner("Analyse IA en cours…"):
                    st.session_state.ai_summary = _llm_ask(
                        build_session_summary_prompt(session)
                    )
            except Exception as exc:
                st.session_state.ai_summary = f"_Résumé IA indisponible : {exc}_"
        else:
            st.session_state.ai_summary = "_Aucun modèle IA sélectionné._"

    except NotImplementedError:
        st.session_state.solve_error = (
            "Ce variant n'est pas encore supporté par le solver sélectionné."
        )
    except RuntimeError as exc:
        st.session_state.solve_error = f"Échec de la résolution : {exc}"


# ── Progressive data-entry steps ─────────────────────────────────────────────

def _render_step1():
    csv_files = _csv_files()
    with st.container(border=True):
        st.markdown("#### Étape 1 — Fichiers CSV")

        if not csv_files:
            st.warning("Aucun fichier CSV trouvé dans `data/`.")
            return

        col_a, col_b = st.columns(2)
        with col_a:
            st.text_input("Entités", value="Personnes", key="left_label")
        with col_b:
            st.text_input("Cibles", value="Projets", key="right_label")

        left_label = st.session_state.get("left_label", "Entités")
        right_label = st.session_state.get("right_label", "Cibles")

        prev_left = st.session_state.get("_prev_left_csv")
        prev_right = st.session_state.get("_prev_right_csv")

        left_csv = st.selectbox(f"CSV · {left_label}", csv_files, key="left_csv")
        right_csv = st.selectbox(f"CSV · {right_label}", csv_files, key="right_csv")

        # Detect CSV change → clear all downstream state
        csv_changed = (
            (prev_left is not None and prev_left != left_csv)
            or (prev_right is not None and prev_right != right_csv)
        )
        if csv_changed:
            for k in ["left_id_cols", "skill_cols", "right_id_col", "solver_key",
                      "solution", "ai_summary", "solve_error"]:
                st.session_state.pop(k, None)
            st.session_state["_prev_left_csv"] = left_csv
            st.session_state["_prev_right_csv"] = right_csv
            st.rerun()

        st.session_state["_prev_left_csv"] = left_csv
        st.session_state["_prev_right_csv"] = right_csv

        st.markdown("")
        if st.button("Suivant →", key="step1_next", type="primary"):
            st.session_state.data_step = max(st.session_state.get("data_step", 1), 2)
            st.rerun()


def _render_step2():
    with st.container(border=True):
        st.markdown("#### Étape 2 — Colonnes d'identité")

        left_cols = _load_columns(st.session_state.left_csv)
        right_cols = _load_columns(st.session_state.right_csv)
        left_label = st.session_state.get("left_label", "Entités")
        right_label = st.session_state.get("right_label", "Cibles")

        _sanitize_multiselect("left_id_cols", left_cols)
        st.multiselect(
            f"Colonnes ID · {left_label}",
            left_cols,
            key="left_id_cols",
        )

        _sanitize_selectbox("right_id_col", right_cols)
        st.selectbox(
            f"Colonne ID · {right_label}",
            right_cols,
            key="right_id_col",
        )

        st.markdown("")
        if st.button("Suivant →", key="step2_next", type="primary"):
            st.session_state.data_step = max(st.session_state.get("data_step", 1), 3)
            st.rerun()


def _render_step3():
    with st.container(border=True):
        st.markdown("#### Étape 3 — Colonnes de compétences")

        left_cols = _load_columns(st.session_state.left_csv)
        left_id_cols = st.session_state.get("left_id_cols", [])
        remaining = [c for c in left_cols if c not in left_id_cols]

        _sanitize_multiselect("skill_cols", remaining)
        st.multiselect("Colonnes compétences", remaining, key="skill_cols")

        st.markdown("")
        if st.button("Suivant →", key="step3_next", type="primary"):
            st.session_state.data_step = max(st.session_state.get("data_step", 1), 4)
            st.rerun()


def _render_step4():
    assignment_type = st.session_state.assignment_type
    full_variant = st.session_state.assignment_variant

    solver_group = ASSIGNMENT_SOLVER_GROUPS.get(assignment_type)
    if not solver_group:
        st.error("Aucun groupe de solvers disponible.")
        return

    solver_reg = import_module(solver_group.registry_module)
    compatible = {
        k: s for k, s in solver_reg.SOLVERS.items()
        if full_variant in s.supported_variants
    }
    if not compatible:
        st.error("Aucun solver compatible avec cette formulation.")
        return

    with st.container(border=True):
        st.markdown("#### Étape 4 — Solveur")

        st.selectbox(
            "Solveur",
            options=list(compatible.keys()),
            format_func=lambda k: compatible[k].label,
            label_visibility="collapsed",
            key="solver_key",
        )

        st.markdown("")
        if st.button("▶  Résoudre", key="solve_btn", type="primary", use_container_width=True):
            _do_solve()
            st.rerun()


# ── Main area renderers ───────────────────────────────────────────────────────

def _render_onboarding():
    theme.hero(
        "Optimization Playground",
        "Décrivez votre problème en langage naturel. L'IA configurera automatiquement la barre latérale.",
    )

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
        elif not st.session_state.get("llm_model_name"):
            st.warning("Sélectionnez un modèle IA dans la barre latérale.")
        else:
            try:
                with st.spinner("Analyse en cours…"):
                    result = _llm_ask(build_onboarding_prompt(user_desc))

                st.session_state.onboarding_result = result
                st.session_state.analysis_done = True

                # Infer and immediately apply configuration recommendation
                rec = infer_problem_configuration(user_desc, result)
                st.session_state.analysis_recommendation = rec
                if rec:
                    st.session_state["problem_key"] = rec["problem_key"]
                    st.session_state["assignment_type"] = rec["assignment_type"]
                    st.session_state["assignment_variant"] = rec["assignment_variant"]

                # Reset any prior validation so user re-confirms the new config
                st.session_state.config_validated = False
                st.session_state.data_step = 1
                st.session_state.solution = None
                st.session_state.ai_summary = None

                st.rerun()

            except Exception as exc:
                st.error(f"Erreur lors de l'appel au modèle IA : {exc}")

    if st.session_state.get("onboarding_result"):
        st.markdown("**Guidage IA**")
        theme.ai_block(st.session_state.onboarding_result)
        st.markdown("")
        st.markdown(
            '<p class="ui-hint">✓ Configuration proposée dans la barre latérale. '
            'Vous pouvez la modifier, puis cliquer sur '
            '<strong>Valider la configuration</strong>.</p>',
            unsafe_allow_html=True,
        )
    else:
        st.markdown("")
        st.markdown(
            '<p class="ui-hint">→ Décrivez votre problème ci-dessus. '
            'L\'IA proposera automatiquement une configuration dans la barre latérale.</p>',
            unsafe_allow_html=True,
        )


def _render_data_workflow():
    atype_def = ASSIGNMENT_TYPES[st.session_state.assignment_type]
    _, variant_key = st.session_state.assignment_variant.split("_", 1)
    variant_reg = import_module(atype_def.registry_module)
    subtitle = f"{atype_def.label} · {variant_reg.VARIANTS[variant_key].label}"

    theme.hero("Saisie des données", subtitle)

    if st.session_state.get("solve_error"):
        st.error(st.session_state.solve_error)

    data_step = st.session_state.get("data_step", 1)

    _render_step1()
    if data_step >= 2:
        _render_step2()
    if data_step >= 3:
        _render_step3()
    if data_step >= 4:
        _render_step4()


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

    _, variant_key = st.session_state.assignment_variant.split("_", 1)
    variant_module = import_module(
        f"ui.problems.assignment.{st.session_state.assignment_type}.ui_{variant_key}"
    )
    variant_module.render_results(solution, st.session_state)

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

    st.markdown("")
    if st.button("← Modifier les données"):
        st.session_state.solution = None
        st.session_state.ai_summary = None
        st.session_state.solve_error = None
        st.rerun()


# ── Main routing ──────────────────────────────────────────────────────────────

if not st.session_state.get("config_validated"):
    _render_onboarding()
elif st.session_state.solution is None:
    _render_data_workflow()
else:
    _render_results()
