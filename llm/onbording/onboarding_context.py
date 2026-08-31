# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025-2026 AKKODIS.
# SPDX-FileContributor: Romain Baville
# SPDX-License-Identifier: Apache-2.0

from infrastructure.registry import DATA_SOURCE_REGISTRY
from solvers.registry import PROBLEM_SOLVER_GROUPS
from ui.registry import PROBLEM_REGISTRY


def build_onboarding_context() -> dict[ str, list[ dict[ str, str ] ] ]:
    """Build a structured description of platform capabilities based on registries.

    Returns:
        dict[str, list[dict[str, str]]]: The data (name, description) of the tools(domain, solvers...).

    """
    problems: list[ dict[ str, str ] ] = [
        {
            "key": p.key,
            "label": p.label,
            "description": p.description
        } for p in PROBLEM_REGISTRY.values()
    ]

    solvers: list[ dict[ str, str ]
                  ] = [ {
                      "key": s.key,
                      "description": s.description
                  } for s in PROBLEM_SOLVER_GROUPS.values() ]

    input_data: list[ dict[ str, str ] ] = [
        {
            "key": d.key,
            "label": d.label,
            "description": d.description
        } for d in DATA_SOURCE_REGISTRY.values()
    ]

    return {
        "problems": problems,
        "solvers": solvers,
        "input data": input_data
    }
