# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025-2026 AKKODIS.
# SPDX-FileContributor: Romain Baville

from dataclasses import dataclass, field

from domain.assignment.score.matching_config import MatchingConfig
from domain.assignment.score.ressources_config import RessourcesConfig


@dataclass
class ScoreConfig:
    """Configure score computation for the assignment problem."""

    use_matching: bool = field( default=False, metadata={
        "description": "Enable matching-based score computation."
    } )

    matching_config: MatchingConfig | None = field(
        default=None, metadata={
            "description": "Matching score configuration."
        }
    )

    use_ressources: bool = field(
        default=False, metadata={
            "description": "Enable resource-based score computation."
        }
    )

    ressources_config: RessourcesConfig | None = field(
        default=None, metadata={
            "description": "Resource score configuration."
        }
    )
