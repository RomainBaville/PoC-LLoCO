# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025-2026 AKKODIS.
# SPDX-FileContributor: Romain Baville

from domain.registry import DOMAIN_REGISTRY
from infrastructure.registry import DATA_SOURCE_REGISTRY
from solvers.registry import DOMAINS_SOLVER_GROUP
from ui.registry import UI_DOMAIN_REGISTRY


def build_onboarding_context() -> dict[ str, list[ dict[ str, str ] ] ]:
    """Build a structured description of platform capabilities based on registries.

    Returns:
        dict[str, list[dict[str, str]]]: The data (name, description) of the tools(domain, solvers...).

    """
    domains: list[ dict[ str, str ] ] = []
    solvers: list[ dict[ str, str ] ] = []
    for ui_domain in UI_DOMAIN_REGISTRY:
        for domain in DOMAIN_REGISTRY:
            if ui_domain.key == domain.key:
                domains.append[ {
                    "key": domain.key,
                    "label": domain.label,
                    "description": domain.description,
                    "attributes": domain.get_schema()
                } ]

        for domain_solvers in DOMAINS_SOLVER_GROUP:
            if ui_domain.key == domain_solvers.key:
                for solver in domain_solvers:
                    solvers.append[ {
                        "key": solver.key,
                        "label": solver.label,
                        "description": solver.description
                    } ]

    input_data: list[ dict[ str, str ] ] = [
        {
            "key": d.key,
            "label": d.label,
            "description": d.description
        } for d in DATA_SOURCE_REGISTRY
    ]

    return {
        "domains": domains,
        "solvers": solvers,
        "input data": input_data
    }
