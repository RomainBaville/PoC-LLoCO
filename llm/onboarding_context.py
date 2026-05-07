# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025-2026 AKKODIS.
# SPDX-FileContributor: Romain Baville
# SPDX-License-Identifier: Apache-2.0

from importlib import import_module

from ui.registry import PROBLEM_REGISTRY
from ui.problems.assignment.registry import ASSIGNMENT_TYPES
from solvers.assignment.registry import ASSIGNMENT_SOLVER_GROUPS


def build_onboarding_context() -> dict:
    """
    Build a structured description of platform capabilities
    based on registries.
    """

    problems = [
        {"key": p.key, "label": p.label}
        for p in PROBLEM_REGISTRY.values()
    ]

    assignment_types = []
    for atype in ASSIGNMENT_TYPES.values():
        type_registry = import_module(atype.registry_module)
        variants = [
            v.label for v in type_registry.VARIANTS.values()
        ]

        solver_group = ASSIGNMENT_SOLVER_GROUPS.get(atype.key)

        assignment_types.append({
            "label": atype.label,
            "description": atype.description,
            "variants": variants,
            "solvers": (
                list(
                    import_module(solver_group.registry_module)
                    .SOLVERS
                    .keys()
                )
                if solver_group else []
            ),
        })

    return {
        "problems": problems,
        "assignment_types": assignment_types,
    }
