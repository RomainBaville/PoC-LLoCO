# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025-2026 AKKODIS.
# SPDX-FileContributor: Romain Baville

from dataclasses import dataclass
from typing import Optional

from domain.objective import Objective


@dataclass
class RessourcesConfig:
    """Dataclass to configure the scoring optimization involving a score computation from an addition of the left entities ressources.
    This Dataclass also configure optionnal constraints associated to the ressources.

    Args:
        labels (list[str]): The list with the ressources labels for the left entities.
        vals (dict[list[str], float]): The dictionary with the value of the left entities for all the ressources used in the score computation:
            - keys (list[str]): The left entitiy label and the ressource label.
            - values (float): The value used in the score computation.
        objectives (dict[str, Objective]): The dictionary with ressources objectives used used in the score computation:
            - keys (str): The label of the ressources used used in the score computation.
            - values (Objective): The objective of the ressources (maximize, minimize).
        weights (Optional[dict[str, float]]): The dictionary with the ressources weights used in the score computation:
            - keys (str): The label of the ressource used in the score computation with a weight.
            - values (float): The value of the weight.
        max_vals (Optional[dict[list[str], float]]): The dictionary whit the maximum ressources values accepted per right entities:
            - keys (list[str]): The ressource label.
            - value (float): The maximum value accepted for the ressources per right entities.
        min_vals (Optional[dict[list[str], float]]): The dictionary whit the minimum ressources values accepted per right entities:
            - keys (list[str]): The list of the ressources labels constrainted at once.
            - value (float): The minimum value accepted for the ressources per right entities.
        max_vals_global (Optional[dict[list[str], float]]): The dictionary whit the maximum ressources values accepted for all the right entities:
            - keys (list[str]): The list of the ressources labels constrainted at once.
            - value (float): The minimum value accepted for the ressources for all the right entities.
        min_vals_global (Optional[dict[list[str], float]]): The dictionary whit the minimum ressources values accepted for all the right entities:
            - keys (list[str]): The list of the ressources labels constrainted at once.
            - value (float): The global minimum value accepted for the ressources for all the right entities.

    """
    labels: list[ str ]
    vals: dict[ list[ str ], float ]

    # Scoring config
    objectives: dict[ str, Objective ]

    # Constraints
    weights: Optional[ dict[ str, float ] ] = None

    max_vals: Optional[ dict[ list[ str ], float ] ] = None
    min_vals: Optional[ dict[ list[ str ], float ] ] = None

    max_vals_global: Optional[ dict[ list[ str ], float ] ] = None
    min_vals_global: Optional[ dict[ list[ str ], float ] ] = None
