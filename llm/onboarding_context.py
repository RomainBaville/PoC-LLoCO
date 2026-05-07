# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025-2026 AKKODIS.
# SPDX-FileContributor: Romain Baville

from ui.registry import PROBLEM_REGISTRY
from infrastructure.registry import DATA_SOURCE_REGISTRY
from solvers.registry import SOLVER_REGISTRY


def build_onboarding_context() -> dict:
    """
    Build a structured description of the platform capabilities
    based on registries.
    """

    problems = []
    for p in PROBLEM_REGISTRY.values():
        problems.append({
            "key": p.key,
            "label": p.label,
        })

    data_sources = []
    for ds in DATA_SOURCE_REGISTRY.values():
        data_sources.append({
            "key": ds.key,
            "label": ds.label,
            "description": ds.description,
        })

    solvers = {}
    for problem_type, variants in SOLVER_REGISTRY.items():
        solvers[problem_type] = {}
        for variant, solver_defs in variants.items():
            solvers[problem_type][variant] = [
                solver.label for solver in solver_defs.values()
            ]

    return {
        "problems": problems,
        "data_sources": data_sources,
        "solvers": solvers,
    }
