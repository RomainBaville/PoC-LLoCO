# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025-2026 AKKODIS.
# SPDX-FileContributor: Romain Baville

from dataclasses import dataclass

from domain.assignment.score.matching_config import MatchingConfig
from domain.assignment.score.ressources_config import RessourcesConfig


@dataclass
class ScoreConfig:
    """Dataclass to configure the score evaluation of the assignment problem.

    Args:
        use_matching (bool): True if the problem optimization score uses left and right entities matching (e.g. skills, production ...):
            Defaults to False.
        matching_config (Optional[MatchingConfig]): The configuration of the matching to make.
        use_ressources (bool): True if the problem optimisation score uses left entities ressources (e.g. salary, time ...):
            Defaults to False.
        ressources_config (Optional[RessourcesConfig]): The configuration of the ressources to use.

    """
    use_matching: bool = False
    matching_config: MatchingConfig | None = None

    use_ressources: bool = False
    ressources_config: RessourcesConfig | None = None
