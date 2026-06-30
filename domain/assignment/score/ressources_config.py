# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025-2026 AKKODIS.
# SPDX-FileContributor: Romain Baville

from dataclasses import dataclass
from typing import Optional

from domain.objective import Objective


@dataclass
class RessourcesConfig:
    """Dataclass to configure the scoring optimization involving a score computation from an addition of the left entities ressources.
    This Dataclass also configure optionnal right constraints associated to the left ressources.

    Args:
        labels (tuple[str, ...]): The ressources labels for the left entities.
        vals (dict[tuple[str, str], float]): The dictionary with the value of the left entities for all the ressources used in the score computation:
            - keys (tuple[str, str]): The left entitiy label, the ressource label.
            - values (float): The ressource value used in the score computation.
        objectives (dict[str, Objective]): The dictionary with ressources objectives used in the score computation:
            - keys (str): The label of the ressources used used in the score computation.
            - values (Objective): The objective of the ressources (maximize, minimize).
        weights (dict[str, float]): The dictionary with the ressources weights used in the score computation:
            - keys (str): The label of the ressource with a weight.
            - values (float): The value of the weight.
        max_vals (Optional[dict[tuple[str, ...], float]]): The dictionary whit the maximum ressources values accepted per right entities:
            - keys (tuple[str, ...]): The right entity label, the ressources labels constrainted.
            - value (float): The maximum value accepted for the ressources listed for the right entity.
        min_vals (Optional[dict[tuple[str, ...], float]]): The dictionary whit the minimum ressources values accepted per right entities:
            - keys (tuple[str, ...]): The right entity label, the ressources labels constrainted.
            - value (float): The minimum value accepted for the ressources listed for the right entity.
        max_global_vals (Optional[dict[tuple[str, ...], float]]): The dictionary whit the maximum ressources values accepted for all the right entities:
            - keys (tuple[str, ...]): The ressources labels constrainted at once.
            - value (float): The maximum value accepted for the ressources listed for all the right entities.
        min_global_vals (Optional[dict[tuple[str, ...], float]]): The dictionary whit the minimum ressources values accepted for all the right entities:
            - keys (tuple[str, ...]): The ressources labels constrainted at once.
            - value (float): The minimum value accepted for the ressources listed for all the right entities.

    """
    labels: tuple[ str, ...]
    vals: dict[ tuple[ str, str ], float ]
    objectives: dict[ str, Objective ]
    weights: dict[ str, float ]

    # Constraints
    max_vals: Optional[ dict[ tuple[ str, ...], float ] ] = None
    min_vals: Optional[ dict[ tuple[ str, ...], float ] ] = None

    max_global_vals: Optional[ dict[ tuple[ str, ...], float ] ] = None
    min_global_vals: Optional[ dict[ tuple[ str, ...], float ] ] = None
